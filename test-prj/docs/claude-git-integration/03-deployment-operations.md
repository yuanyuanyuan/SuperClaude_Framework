# Claude Code + Git Hooks 部署与运维方案

## 📋 文档信息

**文档版本**: 1.0  
**创建日期**: 2025年1月20日  
**目标受众**: DevOps工程师、运维工程师、系统管理员  
**依赖文档**: [01-系统架构设计](./01-system-architecture.md), [02-技术实现方案](./02-technical-implementation.md)  

## 🎯 部署概览

本文档详细描述Claude Code + Git Hooks集成系统的完整部署方案，包括环境准备、容器化部署、Kubernetes集群部署、监控配置以及运维最佳实践。

## 🏗️ 部署架构设计

### 总体部署架构

```mermaid
graph TB
    subgraph "生产环境"
        subgraph "负载均衡层"
            ALB[应用负载均衡器]
            CDN[内容分发网络]
        end
        
        subgraph "应用层"
            API1[API服务节点1]
            API2[API服务节点2]
            API3[API服务节点3]
            Worker1[后台任务节点1]
            Worker2[后台任务节点2]
        end
        
        subgraph "数据层"
            PrimaryDB[(主数据库)]
            ReadDB[(只读副本)]
            Redis[(Redis集群)]
            S3[(对象存储)]
        end
        
        subgraph "监控层"
            Prometheus[Prometheus]
            Grafana[Grafana]
            AlertManager[AlertManager]
        end
    end
    
    subgraph "预发布环境"
        StagingAPI[预发布API]
        StagingDB[(预发布数据库)]
        StagingRedis[(预发布Redis)]
    end
    
    subgraph "开发环境"
        DevAPI[开发API]
        DevDB[(开发数据库)]
    end
    
    CDN --> ALB
    ALB --> API1
    ALB --> API2
    ALB --> API3
    
    API1 --> PrimaryDB
    API1 --> ReadDB
    API1 --> Redis
    Worker1 --> S3
    
    PrimaryDB -.-> ReadDB
    
    Prometheus --> API1
    Prometheus --> Worker1
    Grafana --> Prometheus
    AlertManager --> Prometheus
```

## 🐳 容器化部署

### 1. Docker镜像构建

#### 1.1 主应用Dockerfile

```dockerfile
# Dockerfile
FROM node:20-alpine AS base

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apk add --no-cache \
    git \
    curl \
    bash \
    python3 \
    make \
    g++

FROM base AS deps

# 复制依赖文件
COPY package.json package-lock.json ./

# 安装依赖
RUN npm ci --only=production && npm cache clean --force

FROM base AS build

# 复制源代码
COPY . .
COPY --from=deps /app/node_modules ./node_modules

# 构建应用
RUN npm run build

# 运行测试
RUN npm test

FROM base AS runtime

# 创建非root用户
RUN addgroup -g 1001 -S nodejs && \
    adduser -S claude-git -u 1001

# 复制构建产物
COPY --from=build /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
COPY package.json ./

# 设置权限
RUN chown -R claude-git:nodejs /app

USER claude-git

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080

CMD ["node", "dist/index.js"]
```

#### 1.2 多阶段构建优化

```dockerfile
# Dockerfile.optimized
# 第一阶段：构建环境
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production --silent

# 第二阶段：开发依赖
FROM node:20-alpine AS dev-deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --silent

# 第三阶段：构建应用
FROM dev-deps AS build
COPY . .
RUN npm run build && npm run test

# 第四阶段：运行时环境
FROM node:20-alpine AS runtime
RUN apk add --no-cache dumb-init git curl
WORKDIR /app

# 创建用户
RUN addgroup -g 1001 -S nodejs && \
    adduser -S claude-git -u 1001 -G nodejs

# 复制文件
COPY --from=builder --chown=claude-git:nodejs /app/node_modules ./node_modules
COPY --from=build --chown=claude-git:nodejs /app/dist ./dist
COPY --chown=claude-git:nodejs package.json ./

USER claude-git

EXPOSE 8080
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/index.js"]
```

### 2. Docker Compose配置

#### 2.1 开发环境配置

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  # 主应用
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: runtime
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:password@db:5432/claude_git_dev
      - REDIS_URL=redis://redis:6379
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
      - LOG_LEVEL=debug
    volumes:
      - .:/app
      - node_modules:/app/node_modules
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  # 数据库
  db:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=claude_git_dev
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_dev_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis缓存
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_dev_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # 开发工具
  mailhog:
    image: mailhog/mailhog
    ports:
      - "8025:8025"  # Web界面
      - "1025:1025"  # SMTP

volumes:
  postgres_dev_data:
  redis_dev_data:
  node_modules:
```

#### 2.2 生产环境配置

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # 应用负载均衡
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./config/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/ssl/certs:ro
    depends_on:
      - app
    restart: always

  # 主应用 - 多实例
  app:
    image: claude-git-engine:${VERSION:-latest}
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
          cpus: '0.25'
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
      - LOG_LEVEL=info
      - METRICS_ENABLED=true
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped

  # 后台任务处理器
  worker:
    image: claude-git-worker:${VERSION:-latest}
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure
    environment:
      - NODE_ENV=production
      - REDIS_URL=${REDIS_URL}
      - DATABASE_URL=${DATABASE_URL}
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
    restart: unless-stopped

  # 数据库
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: always

  # Redis集群
  redis:
    image: redis:7
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_prod_data:/data
    ports:
      - "6379:6379"
    restart: always

  # 监控组件
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_INSTALL_PLUGINS=grafana-piechart-panel
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana:/etc/grafana/provisioning

volumes:
  postgres_prod_data:
  redis_prod_data:
  prometheus_data:
  grafana_data:

networks:
  default:
    driver: bridge
```

### 3. Nginx配置

```nginx
# config/nginx.conf
upstream app_backend {
    least_conn;
    server app:8080 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name claude-git-integration.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name claude-git-integration.com;

    # SSL配置
    ssl_certificate /etc/ssl/certs/fullchain.pem;
    ssl_certificate_key /etc/ssl/certs/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # 安全头
    add_header Strict-Transport-Security "max-age=63072000" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;

    # 限流
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    location / {
        limit_req zone=api burst=20 nodelay;
        
        proxy_pass http://app_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # 健康检查
        proxy_next_upstream error timeout http_500 http_502 http_503 http_504;
    }

    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }

    location /metrics {
        allow 10.0.0.0/8;
        allow 172.16.0.0/12;
        allow 192.168.0.0/16;
        deny all;
        
        proxy_pass http://app_backend;
    }
}
```

## ☁️ Kubernetes部署

### 1. Namespace和资源配额

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: claude-git
  labels:
    name: claude-git
    environment: production

---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: claude-git-quota
  namespace: claude-git
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    persistentvolumeclaims: "10"
    services: "10"
    secrets: "20"
    configmaps: "20"
```

### 2. 配置管理

```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: claude-git-config
  namespace: claude-git
data:
  NODE_ENV: "production"
  LOG_LEVEL: "info"
  METRICS_ENABLED: "true"
  REDIS_MAX_RETRIES: "3"
  DATABASE_POOL_SIZE: "10"
  
---
apiVersion: v1
kind: Secret
metadata:
  name: claude-git-secrets
  namespace: claude-git
type: Opaque
data:
  database-url: <base64-encoded-database-url>
  claude-api-key: <base64-encoded-api-key>
  redis-password: <base64-encoded-redis-password>
```

### 3. 主应用部署

```yaml
# k8s/api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: claude-git-api
  namespace: claude-git
  labels:
    app: claude-git-api
    version: v1.0.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  selector:
    matchLabels:
      app: claude-git-api
  template:
    metadata:
      labels:
        app: claude-git-api
        version: v1.0.0
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/path: /metrics
        prometheus.io/port: "8080"
    spec:
      serviceAccountName: claude-git-sa
      containers:
      - name: api
        image: claude-git-engine:v1.0.0
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        env:
        - name: NODE_ENV
          valueFrom:
            configMapKeyRef:
              name: claude-git-config
              key: NODE_ENV
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: claude-git-secrets
              key: database-url
        - name: CLAUDE_API_KEY
          valueFrom:
            secretKeyRef:
              name: claude-git-secrets
              key: claude-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2
        securityContext:
          runAsNonRoot: true
          runAsUser: 1001
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache
      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir:
          sizeLimit: 1Gi
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - claude-git-api
              topologyKey: kubernetes.io/hostname

---
apiVersion: v1
kind: Service
metadata:
  name: claude-git-service
  namespace: claude-git
  labels:
    app: claude-git-api
spec:
  type: LoadBalancer
  selector:
    app: claude-git-api
  ports:
  - name: http
    port: 80
    targetPort: http
    protocol: TCP
  sessionAffinity: None

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: claude-git-hpa
  namespace: claude-git
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: claude-git-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
```

### 4. 数据库部署

```yaml
# k8s/postgres.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: claude-git
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
          name: postgres
        env:
        - name: POSTGRES_DB
          value: claude_git
        - name: POSTGRES_USER
          value: postgres
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        livenessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - postgres
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - postgres
          initialDelaySeconds: 5
          periodSeconds: 5
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: "fast-ssd"
      resources:
        requests:
          storage: 100Gi

---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: claude-git
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
  clusterIP: None
```

## 📊 监控和日志

### 1. Prometheus配置

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  # 应用监控
  - job_name: 'claude-git-api'
    kubernetes_sd_configs:
    - role: pod
      namespaces:
        names:
        - claude-git
    relabel_configs:
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
      action: keep
      regex: true
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
      action: replace
      target_label: __metrics_path__
      regex: (.+)
    - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
      action: replace
      regex: ([^:]+)(?::\d+)?;(\d+)
      replacement: $1:$2
      target_label: __address__

  # 节点监控
  - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
    - role: node
    relabel_configs:
    - action: labelmap
      regex: __meta_kubernetes_node_label_(.+)

  # Redis监控
  - job_name: 'redis'
    static_configs:
    - targets: ['redis:6379']
    metrics_path: /metrics

  # PostgreSQL监控
  - job_name: 'postgres'
    static_configs:
    - targets: ['postgres:5432']
```

### 2. 告警规则

```yaml
# monitoring/alert_rules.yml
groups:
- name: claude-git-alerts
  rules:
  # API服务告警
  - alert: APIHighErrorRate
    expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "API error rate is above 5%"
      description: "Error rate is {{ $value | humanizePercentage }} for the last 5 minutes"

  - alert: APIHighLatency
    expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 0.5
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "API 95th percentile latency is above 500ms"

  # 资源告警
  - alert: HighMemoryUsage
    expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.85
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "High memory usage detected"
      description: "Memory usage is above 85% on {{ $labels.instance }}"

  - alert: HighCPUUsage
    expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "High CPU usage detected"
      description: "CPU usage is above 80% on {{ $labels.instance }}"

  # 数据库告警
  - alert: PostgreSQLDown
    expr: up{job="postgres"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "PostgreSQL is down"
      description: "PostgreSQL has been down for more than 1 minute"

  - alert: RedisDown
    expr: up{job="redis"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Redis is down"
      description: "Redis has been down for more than 1 minute"
```

### 3. Grafana仪表板配置

```json
{
  "dashboard": {
    "title": "Claude Git Integration Dashboard",
    "tags": ["claude-git", "monitoring"],
    "panels": [
      {
        "title": "API Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (status)",
            "legendFormat": "{{status}}"
          }
        ],
        "yAxes": [
          {
            "label": "Requests/sec",
            "min": 0
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "50th percentile"
          },
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
            "legendFormat": "95th percentile"
          }
        ],
        "yAxes": [
          {
            "label": "Seconds",
            "min": 0
          }
        ]
      },
      {
        "title": "Code Quality Score",
        "type": "singlestat",
        "targets": [
          {
            "expr": "avg(analysis_quality_score)",
            "legendFormat": "Average Score"
          }
        ],
        "thresholds": "6,8",
        "colorBackground": true
      },
      {
        "title": "Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "process_resident_memory_bytes / 1024 / 1024",
            "legendFormat": "{{instance}}"
          }
        ],
        "yAxes": [
          {
            "label": "MB",
            "min": 0
          }
        ]
      }
    ]
  }
}
```

## 🔧 CI/CD流水线

### 1. GitHub Actions工作流

```yaml
# .github/workflows/deploy.yml
name: Claude Git Engine CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4
      
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linting
        run: npm run lint
      
      - name: Run type checking
        run: npm run typecheck
      
      - name: Run tests
        run: npm run test:coverage
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379
      
      - name: Run security audit
        run: npm audit --audit-level high
      
      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info

  build:
    needs: test
    runs-on: ubuntu-latest
    outputs:
      image: ${{ steps.image.outputs.image }}
      digest: ${{ steps.build.outputs.digest }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable={{is_default_branch}}
      
      - name: Build and push Docker image
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          platforms: linux/amd64,linux/arm64

  security-scan:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ needs.build.outputs.image }}
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy scan results to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  deploy-staging:
    if: github.ref == 'refs/heads/develop'
    needs: [build, security-scan]
    runs-on: ubuntu-latest
    environment: staging
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure kubectl
        uses: azure/k8s-set-context@v1
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_STAGING }}
      
      - name: Deploy to staging
        run: |
          sed -i "s|IMAGE_TAG|${{ needs.build.outputs.digest }}|g" k8s/staging/*.yaml
          kubectl apply -f k8s/staging/
          kubectl rollout status deployment/claude-git-api -n claude-git-staging

  deploy-production:
    if: github.ref == 'refs/heads/main'
    needs: [build, security-scan]
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure kubectl
        uses: azure/k8s-set-context@v1
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_PROD }}
      
      - name: Deploy to production
        run: |
          sed -i "s|IMAGE_TAG|${{ needs.build.outputs.digest }}|g" k8s/production/*.yaml
          kubectl apply -f k8s/production/
          kubectl rollout status deployment/claude-git-api -n claude-git
      
      - name: Verify deployment
        run: |
          kubectl get pods -n claude-git
          kubectl get services -n claude-git
```

## 🔒 安全配置

### 1. 网络安全

```yaml
# k8s/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: claude-git-network-policy
  namespace: claude-git
spec:
  podSelector:
    matchLabels:
      app: claude-git-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: nginx-ingress
    ports:
    - protocol: TCP
      port: 8080
  egress:
  # 允许访问数据库
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  # 允许访问Redis
  - to:
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 6379
  # 允许访问Claude API
  - to: []
    ports:
    - protocol: TCP
      port: 443
```

### 2. RBAC配置

```yaml
# k8s/rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: claude-git-sa
  namespace: claude-git

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: claude-git
  name: claude-git-role
rules:
- apiGroups: [""]
  resources: ["pods", "services", "endpoints"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "watch"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: claude-git-binding
  namespace: claude-git
subjects:
- kind: ServiceAccount
  name: claude-git-sa
  namespace: claude-git
roleRef:
  kind: Role
  name: claude-git-role
  apiGroup: rbac.authorization.k8s.io
```

## 📋 运维最佳实践

### 1. 健康检查

- **Liveness Probe**: 检查应用是否运行正常
- **Readiness Probe**: 检查应用是否准备好接收流量
- **Startup Probe**: 检查应用启动状态

### 2. 资源管理

- **Resource Requests**: 确保资源分配
- **Resource Limits**: 防止资源滥用
- **Pod Disruption Budget**: 确保服务可用性

### 3. 备份和恢复

```bash
# 数据库备份脚本
#!/bin/bash
# scripts/backup-db.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/postgres"
DB_NAME="claude_git"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 执行备份
kubectl exec -n claude-git postgres-0 -- pg_dump -U postgres $DB_NAME | gzip > $BACKUP_DIR/backup_${DATE}.sql.gz

# 清理旧备份(保留30天)
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

echo "Backup completed: backup_${DATE}.sql.gz"
```

### 4. 日志管理

```yaml
# logging/fluent-bit.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluent-bit
  namespace: kube-system
spec:
  selector:
    matchLabels:
      name: fluent-bit
  template:
    metadata:
      labels:
        name: fluent-bit
    spec:
      serviceAccount: fluent-bit
      containers:
      - name: fluent-bit
        image: fluent/fluent-bit:latest
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
        - name: fluent-bit-config
          mountPath: /fluent-bit/etc/
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
      - name: fluent-bit-config
        configMap:
          name: fluent-bit-config
```

## 📋 部署总结

Claude Code + Git Hooks集成系统的部署方案提供了：

- **多环境支持**: 开发、预发布、生产环境完整配置
- **容器化部署**: Docker + Kubernetes云原生架构
- **监控体系**: Prometheus + Grafana全方位监控
- **安全保障**: 网络策略、RBAC、安全扫描
- **运维自动化**: CI/CD流水线、备份恢复、日志管理

这个部署方案确保了系统的高可用性、可扩展性和安全性，支持从开发到生产的完整生命周期管理。