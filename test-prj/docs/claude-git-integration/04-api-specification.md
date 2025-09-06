# Claude Code + Git Hooks API接口规范

## 📋 文档信息

**文档版本**: 1.0  
**创建日期**: 2025年1月20日  
**目标受众**: 前端开发工程师、集成开发者、第三方开发者  
**依赖文档**: [01-系统架构设计](./01-system-architecture.md)  

## 🎯 API概览

Claude Code + Git Hooks集成系统提供RESTful API和WebSocket API，支持代码分析、文档生成、Hook管理等核心功能。

### API特性

- **RESTful设计**: 遵循REST架构原则
- **统一认证**: JWT Token + API Key双重认证
- **版本控制**: URL版本控制，向后兼容
- **实时通信**: WebSocket支持实时事件推送
- **批量操作**: 支持批量请求优化性能
- **限流保护**: API调用频率限制和配额管理

### 基础信息

- **基础URL**: `https://api.claude-git-integration.com/api/v1`
- **认证方式**: Bearer Token (JWT) 或 API Key
- **内容类型**: `application/json`
- **字符编码**: UTF-8
- **WebSocket**: `wss://api.claude-git-integration.com/ws`

## 🔐 认证和授权

### 1. JWT认证

**获取Token**

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "developer@example.com",
  "password": "your_password"
}
```

**响应**
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 3600,
    "tokenType": "Bearer"
  }
}
```

**使用Token**
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2. API Key认证

**创建API Key**
```http
POST /api/v1/auth/api-keys
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "name": "CI/CD Integration",
  "permissions": ["analysis:execute", "docs:write"],
  "expiresAt": "2025-12-31T23:59:59Z"
}
```

**使用API Key**
```http
X-API-Key: claude_git_1234567890abcdef
```

## 📊 代码分析API

### 1. 提交代码分析请求

```http
POST /api/v1/analysis/code
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**
```json
{
  "files": [
    {
      "path": "src/components/Button.tsx",
      "content": "import React from 'react';\n\ninterface ButtonProps {\n  children: React.ReactNode;\n  onClick?: () => void;\n}\n\nexport const Button: React.FC<ButtonProps> = ({ children, onClick }) => {\n  return (\n    <button onClick={onClick}>\n      {children}\n    </button>\n  );\n};",
      "language": "typescript",
      "changeType": "added"
    }
  ],
  "analysisTypes": ["code-quality", "security", "performance"],
  "context": {
    "projectType": "react",
    "techStack": ["typescript", "react"],
    "codingStandards": "airbnb"
  },
  "options": {
    "includeFixSuggestions": true,
    "confidenceThreshold": 0.8,
    "forceRefresh": false,
    "cacheTtl": 3600
  }
}
```

**响应**
```json
{
  "success": true,
  "data": {
    "analysisId": "analysis_1234567890",
    "status": "completed",
    "overallScore": 8.5,
    "results": [
      {
        "type": "code-quality",
        "score": 8.2,
        "issues": [
          {
            "severity": "warning",
            "type": "accessibility",
            "message": "Button缺少accessibility属性",
            "file": "src/components/Button.tsx",
            "line": 9,
            "column": 5,
            "suggestion": "添加aria-label或其他accessibility属性"
          }
        ],
        "suggestions": [
          {
            "category": "best-practices",
            "message": "建议添加PropTypes或使用TypeScript接口",
            "confidence": 0.9,
            "autoFixable": true
          }
        ]
      },
      {
        "type": "security",
        "score": 9.0,
        "issues": [],
        "suggestions": [
          {
            "category": "security",
            "message": "考虑添加XSS防护",
            "confidence": 0.7,
            "autoFixable": false
          }
        ]
      }
    ],
    "autoFixable": [
      {
        "type": "import-organization",
        "description": "重新组织import语句",
        "file": "src/components/Button.tsx",
        "originalCode": "import React from 'react';",
        "fixedCode": "import type { FC, ReactNode } from 'react';\nimport React from 'react';",
        "confidence": 0.95
      }
    ],
    "metadata": {
      "analyzedAt": "2025-01-20T10:30:00Z",
      "analysisCount": 2,
      "executionTime": 2.3,
      "tokensUsed": 1200
    }
  }
}
```

### 2. 获取分析结果

```http
GET /api/v1/analysis/{analysisId}
Authorization: Bearer {token}
```

**响应**
```json
{
  "success": true,
  "data": {
    "id": "analysis_1234567890",
    "status": "completed",
    "progress": 100,
    "result": {
      // ... 分析结果同上
    }
  }
}
```

### 3. 批量代码分析

```http
POST /api/v1/analysis/batch
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**
```json
{
  "requests": [
    {
      "files": [...],
      "analysisTypes": ["code-quality"],
      "context": {...}
    },
    {
      "files": [...],
      "analysisTypes": ["security"],
      "context": {...}
    }
  ],
  "options": {
    "parallel": true,
    "maxConcurrency": 3
  }
}
```

### 4. 应用自动修复

```http
POST /api/v1/analysis/{analysisId}/apply-fixes
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**
```json
{
  "fixes": [
    {
      "id": "fix_001",
      "apply": true
    },
    {
      "id": "fix_002", 
      "apply": false
    }
  ],
  "options": {
    "createCommit": true,
    "commitMessage": "fix: Apply Claude AI code improvements"
  }
}
```

## 📚 文档生成API

### 1. 生成API文档

```http
POST /api/v1/documentation/generate
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**
```json
{
  "type": "api",
  "sources": [
    {
      "path": "src/api/auth.ts",
      "content": "...",
      "language": "typescript"
    }
  ],
  "template": "default",
  "context": {
    "projectName": "Claude Git Integration",
    "version": "1.0.0",
    "baseUrl": "https://api.example.com"
  },
  "options": {
    "includeExamples": true,
    "outputFormat": "markdown",
    "updateMode": "replace"
  }
}
```

**响应**
```json
{
  "success": true,
  "data": {
    "documentId": "doc_1234567890",
    "content": "# API Documentation\n\n## Authentication\n\n### POST /auth/login\n\n...",
    "metadata": {
      "generatedAt": "2025-01-20T10:30:00Z",
      "wordCount": 1500,
      "outputFormat": "markdown"
    }
  }
}
```

### 2. 更新现有文档

```http
PUT /api/v1/documentation/{documentId}
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**
```json
{
  "changes": [
    {
      "type": "section-update",
      "section": "authentication", 
      "content": "Updated authentication section content"
    }
  ],
  "mergeStrategy": "merge",
  "options": {
    "preserveCustomizations": true
  }
}
```

### 3. 获取文档模板

```http
GET /api/v1/documentation/templates
Authorization: Bearer {token}
```

**查询参数**
- `type`: 模板类型 (api, architecture, user-guide, changelog)
- `category`: 模板分类

**响应**
```json
{
  "success": true,
  "data": {
    "templates": [
      {
        "id": "api-default",
        "name": "API文档默认模板",
        "type": "api",
        "description": "标准的API文档模板",
        "preview": "# {{projectName}} API\n\n## Overview\n...",
        "variables": [
          "projectName",
          "version", 
          "baseUrl"
        ]
      }
    ],
    "categories": ["default", "technical", "business"]
  }
}
```

## 🔗 Hook管理API

### 1. 获取Hook配置

```http
GET /api/v1/hooks
Authorization: Bearer {token}
```

**查询参数**
- `type`: Hook类型 (pre-commit, post-commit, pre-push, etc.)
- `active`: 是否激活 (true/false)
- `project`: 项目ID

**响应**
```json
{
  "success": true,
  "data": {
    "hooks": [
      {
        "id": "hook_001",
        "type": "pre-commit",
        "name": "Code Quality Check",
        "description": "自动执行代码质量检查",
        "active": true,
        "config": {
          "timeout": 30000,
          "retries": 3,
          "qualityThreshold": 7.5
        },
        "createdAt": "2025-01-15T09:00:00Z",
        "updatedAt": "2025-01-20T10:00:00Z"
      }
    ],
    "total": 5,
    "active": 4
  }
}
```

### 2. 注册新Hook

```http
POST /api/v1/hooks/register
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**
```json
{
  "type": "pre-commit",
  "name": "Custom Security Check",
  "description": "自定义安全检查Hook",
  "handler": {
    "type": "webhook",
    "url": "https://your-server.com/security-check",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer your-token"
    }
  },
  "config": {
    "timeout": 45000,
    "retries": 2,
    "failureAction": "block"
  },
  "filters": {
    "filePatterns": ["*.js", "*.ts"],
    "excludePatterns": ["node_modules/**"]
  }
}
```

**响应**
```json
{
  "success": true,
  "data": {
    "hookId": "hook_002",
    "registrationToken": "reg_token_1234567890",
    "webhookUrl": "https://api.claude-git-integration.com/webhooks/hook_002",
    "status": "registered"
  }
}
```

### 3. 手动执行Hook

```http
POST /api/v1/hooks/{hookId}/execute
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**
```json
{
  "context": {
    "files": [
      {
        "path": "src/test.js",
        "changeType": "modified"
      }
    ],
    "commit": {
      "hash": "abc123def456",
      "message": "fix: Update security implementation"
    },
    "author": "developer@example.com"
  },
  "options": {
    "dryRun": false,
    "skipCache": true
  }
}
```

### 4. Hook执行历史

```http
GET /api/v1/hooks/{hookId}/executions
Authorization: Bearer {token}
```

**查询参数**
- `page`: 页码 (默认: 1)
- `limit`: 每页数量 (默认: 20, 最大: 100)
- `status`: 执行状态 (success, failed, timeout)
- `from`: 开始时间
- `to`: 结束时间

**响应**
```json
{
  "success": true,
  "data": {
    "executions": [
      {
        "id": "exec_001",
        "hookId": "hook_001",
        "status": "success",
        "startedAt": "2025-01-20T10:25:00Z",
        "completedAt": "2025-01-20T10:25:03Z",
        "duration": 3.2,
        "result": {
          "success": true,
          "actions": ["quality-check"],
          "suggestions": 2
        },
        "context": {
          "triggerType": "commit",
          "filesCount": 3
        }
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "hasNext": true
    }
  }
}
```

## 📊 项目管理API

### 1. 项目配置

```http
GET /api/v1/projects/{projectId}/config
Authorization: Bearer {token}
```

**响应**
```json
{
  "success": true,
  "data": {
    "projectId": "proj_001",
    "name": "My React Project",
    "config": {
      "quality": {
        "threshold": 7.5,
        "autoFix": true,
        "confidenceThreshold": 0.9
      },
      "documentation": {
        "autoUpdate": true,
        "formats": ["markdown", "html"],
        "coverageThreshold": 0.8
      },
      "integrations": {
        "gitHooks": true,
        "cicd": false,
        "monitoring": true
      },
      "ai": {
        "provider": "claude",
        "model": "claude-3-opus-20240229",
        "maxTokens": 4000
      }
    },
    "updatedAt": "2025-01-20T10:00:00Z"
  }
}
```

### 2. 更新项目配置

```http
PUT /api/v1/projects/{projectId}/config
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**
```json
{
  "quality": {
    "threshold": 8.0
  },
  "ai": {
    "maxTokens": 6000
  }
}
```

### 3. 项目统计信息

```http
GET /api/v1/projects/{projectId}/stats
Authorization: Bearer {token}
```

**查询参数**
- `period`: 时间段 (7d, 30d, 90d, 1y)
- `metrics`: 指标类型 (quality, performance, usage)

**响应**
```json
{
  "success": true,
  "data": {
    "period": "30d",
    "metrics": {
      "codeQuality": {
        "averageScore": 8.3,
        "trend": "+0.5",
        "totalAnalyses": 156
      },
      "documentation": {
        "coverage": 0.85,
        "autoGenerated": 45,
        "manualUpdates": 12
      },
      "hookExecutions": {
        "total": 234,
        "successful": 221,
        "failed": 13,
        "successRate": 0.944
      },
      "performance": {
        "averageAnalysisTime": 2.8,
        "cacheHitRate": 0.72,
        "apiResponseTime": 0.45
      }
    }
  }
}
```

## 🌐 WebSocket实时API

### 1. 连接WebSocket

```javascript
const ws = new WebSocket('wss://api.claude-git-integration.com/ws');

// 认证
ws.send(JSON.stringify({
  type: 'auth',
  token: 'your-jwt-token'
}));

// 订阅事件
ws.send(JSON.stringify({
  type: 'subscribe',
  events: ['analysis:progress', 'hook:triggered', 'quality:alert']
}));
```

### 2. 事件类型

**分析进度事件**
```json
{
  "type": "analysis:progress",
  "data": {
    "analysisId": "analysis_1234567890",
    "progress": 65,
    "stage": "security-analysis",
    "message": "正在执行安全检查...",
    "timestamp": "2025-01-20T10:30:15Z"
  }
}
```

**Hook触发事件**
```json
{
  "type": "hook:triggered",
  "data": {
    "hookId": "hook_001",
    "hookType": "pre-commit",
    "projectId": "proj_001",
    "status": "executing",
    "timestamp": "2025-01-20T10:30:00Z"
  }
}
```

**质量警报事件**
```json
{
  "type": "quality:alert",
  "data": {
    "projectId": "proj_001",
    "alert": {
      "type": "quality-degradation",
      "message": "代码质量评分下降至6.2",
      "threshold": 7.5,
      "currentValue": 6.2
    },
    "severity": "high",
    "timestamp": "2025-01-20T10:30:00Z"
  }
}
```

### 3. 实时分析请求

```json
{
  "type": "analysis:start",
  "data": {
    "requestId": "req_1234567890",
    "files": [...],
    "analysisTypes": ["code-quality"],
    "options": {
      "realtime": true
    }
  }
}
```

## 📈 监控和指标API

### 1. 系统健康状态

```http
GET /api/v1/health
```

**响应**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-20T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": {
      "status": "healthy",
      "responseTime": 5.2
    },
    "redis": {
      "status": "healthy", 
      "responseTime": 1.8
    },
    "claude-api": {
      "status": "healthy",
      "responseTime": 320.5
    }
  },
  "metrics": {
    "uptime": 2592000,
    "memoryUsage": 0.65,
    "cpuUsage": 0.23
  }
}
```

### 2. 性能指标

```http
GET /api/v1/metrics
Authorization: Bearer {token}
```

**查询参数**
- `from`: 开始时间 (ISO 8601)
- `to`: 结束时间 (ISO 8601) 
- `granularity`: 时间粒度 (1m, 5m, 1h, 1d)

**响应**
```json
{
  "success": true,
  "data": {
    "timeRange": {
      "from": "2025-01-20T09:00:00Z",
      "to": "2025-01-20T10:00:00Z"
    },
    "metrics": [
      {
        "timestamp": "2025-01-20T09:30:00Z",
        "apiRequests": 145,
        "analysisExecutions": 23,
        "averageResponseTime": 0.45,
        "errorRate": 0.02,
        "cacheHitRate": 0.78
      }
    ]
  }
}
```

## ❌ 错误处理

### 错误响应格式

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": [
      {
        "field": "files",
        "message": "files字段不能为空"
      }
    ],
    "requestId": "req_1234567890"
  }
}
```

### 常见错误码

| 错误码 | HTTP状态码 | 描述 |
|--------|------------|------|
| `INVALID_TOKEN` | 401 | 无效的认证令牌 |
| `INSUFFICIENT_PERMISSIONS` | 403 | 权限不足 |
| `VALIDATION_ERROR` | 400 | 请求参数验证失败 |
| `RESOURCE_NOT_FOUND` | 404 | 请求的资源不存在 |
| `RATE_LIMIT_EXCEEDED` | 429 | 请求频率超过限制 |
| `ANALYSIS_FAILED` | 500 | 代码分析执行失败 |
| `CLAUDE_API_ERROR` | 502 | Claude API调用失败 |
| `INTERNAL_ERROR` | 500 | 内部服务器错误 |

### 错误重试策略

- **网络错误**: 使用指数退避重试，最多重试3次
- **速率限制**: 根据`Retry-After`头等待后重试
- **服务器错误**: 短暂等待后重试，避免雪崩效应

## 🔄 API版本控制

### 版本策略

- **URL版本控制**: `/api/v1/`, `/api/v2/`
- **向后兼容**: 同一主版本内保持向后兼容
- **废弃通知**: 提前6个月通知API废弃

### 版本信息

```http
GET /api/v1/version
```

**响应**
```json
{
  "version": "1.0.0",
  "apiVersion": "v1",
  "releaseDate": "2025-01-01",
  "deprecationWarnings": [],
  "supportedUntil": "2026-01-01"
}
```

## 📋 API使用示例

### JavaScript/TypeScript客户端

```typescript
// claude-git-client.ts
class ClaudeGitClient {
  private baseUrl: string;
  private token: string;

  constructor(baseUrl: string, token: string) {
    this.baseUrl = baseUrl;
    this.token = token;
  }

  async analyzeCode(files: FileInput[]): Promise<AnalysisResult> {
    const response = await fetch(`${this.baseUrl}/api/v1/analysis/code`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        files,
        analysisTypes: ['code-quality', 'security'],
        options: { includeFixSuggestions: true }
      })
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`);
    }

    return response.json();
  }

  async generateDocumentation(sources: SourceFile[]): Promise<DocumentationResult> {
    const response = await fetch(`${this.baseUrl}/api/v1/documentation/generate`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        type: 'api',
        sources,
        options: { includeExamples: true }
      })
    });

    return response.json();
  }
}

// 使用示例
const client = new ClaudeGitClient('https://api.claude-git-integration.com', 'your-token');

const analysisResult = await client.analyzeCode([
  {
    path: 'src/components/Button.tsx',
    content: '...',
    language: 'typescript'
  }
]);

console.log('Quality Score:', analysisResult.data.overallScore);
```

### Python客户端

```python
# claude_git_client.py
import requests
from typing import List, Dict, Any

class ClaudeGitClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    def analyze_code(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        response = self.session.post(
            f'{self.base_url}/api/v1/analysis/code',
            json={
                'files': files,
                'analysisTypes': ['code-quality', 'security'],
                'options': {'includeFixSuggestions': True}
            }
        )
        response.raise_for_status()
        return response.json()

    def generate_documentation(self, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        response = self.session.post(
            f'{self.base_url}/api/v1/documentation/generate',
            json={
                'type': 'api',
                'sources': sources,
                'options': {'includeExamples': True}
            }
        )
        response.raise_for_status()
        return response.json()

# 使用示例
client = ClaudeGitClient('https://api.claude-git-integration.com', 'your-token')

result = client.analyze_code([{
    'path': 'src/main.py',
    'content': 'def hello(): print("Hello World")',
    'language': 'python'
}])

print(f"Quality Score: {result['data']['overallScore']}")
```

## 📋 API规范总结

Claude Code + Git Hooks集成系统API提供了：

- **完整的代码分析功能**: 质量检查、安全分析、性能优化建议
- **智能文档生成**: 多种文档类型，自定义模板支持
- **Hook管理系统**: 完整的Hook生命周期管理
- **实时通信**: WebSocket支持实时事件推送
- **企业级特性**: 认证授权、限流保护、监控指标

API设计遵循RESTful原则，提供清晰的错误处理和完整的文档支持，确保开发者能够快速集成和使用。