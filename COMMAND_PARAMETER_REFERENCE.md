# 🔧 SuperClaude 命令参数详细速查表

## 🎯 命令分类和参数体系

### 📋 核心开发命令详解

#### 🧠 `/sc:brainstorm` - 创意发现和需求探索
```bash
# 基础语法
/sc:brainstorm "主题描述" [选项]

# 参数详解
--focus [domain]          # 聚焦特定领域 (tech|business|user|market)
--depth [level]           # 探索深度 (surface|detailed|comprehensive)
--stakeholders [list]     # 考虑相关方 (users|developers|business|partners)
--constraints [type]      # 约束条件 (time|budget|technical|regulatory)
--output-format [format]  # 输出格式 (mindmap|structured|narrative|actionable)

# 实用示例
/sc:brainstorm "Next.js电商平台" --focus tech --depth comprehensive
/sc:brainstorm "用户体验改进" --stakeholders users,business --output-format actionable
/sc:brainstorm "技术债务解决方案" --constraints time,technical --depth detailed

# 自动触发的模式和工具
→ MODE_Brainstorming (自动激活)
→ @agent-requirements-analyst (需求相关时)
→ @agent-business-panel-experts (商业场景时)
```

#### 🔍 `/sc:analyze` - 代码和系统分析
```bash
# 基础语法  
/sc:analyze [目标路径] [选项]

# 参数详解
--focus [aspect]          # 分析重点 (architecture|performance|security|quality|patterns)
--depth [level]           # 分析深度 (quick|standard|comprehensive|expert)
--scope [range]           # 分析范围 (file|module|project|system)
--language [lang]         # 目标语言 (typescript|javascript|python|all)
--framework [fw]          # 框架特定 (nextjs|react|vue|express)
--output [format]         # 输出格式 (summary|detailed|report|recommendations)
--include-deps            # 包含依赖分析
--exclude-tests           # 排除测试文件
--metrics                 # 生成定量指标

# 实用示例
/sc:analyze src/ --focus architecture --depth comprehensive --framework nextjs
/sc:analyze components/ --focus patterns --language typescript --output recommendations  
/sc:analyze . --scope project --include-deps --metrics

# 自动触发的工具组合
→ Sequential MCP (复杂分析)
→ Serena MCP (语义理解)
→ @agent-system-architect (架构分析)
→ @agent-root-cause-analyst (问题识别)
```

#### 🚀 `/sc:implement` - 功能实现
```bash
# 基础语法
/sc:implement "功能描述" [选项]

# 参数详解  
--expert-mode             # 启用专家协作模式
--quality-first           # 质量优先模式
--framework [name]        # 目标框架 (nextjs|react|express)
--language [lang]         # 编程语言 (typescript|javascript)
--pattern [style]         # 设计模式 (mvc|mvp|clean|hexagonal)
--testing [approach]      # 测试策略 (unit|integration|e2e|all)
--performance            # 性能优化重点
--security               # 安全性重点
--accessibility          # 可访问性重点
--docs                   # 同时生成文档
--no-validation          # 跳过验证步骤

# 实用示例
/sc:implement "用户认证系统" --expert-mode --quality-first --framework nextjs --testing all
/sc:implement "购物车功能" --language typescript --pattern clean --performance --docs
/sc:implement "数据可视化组件" --framework react --accessibility --testing unit

# 自动触发的专家组合
→ MODE_Orchestration (协调优化)
→ 相关领域专家 (基于功能自动选择)
→ @agent-quality-engineer (质量保证)
→ @agent-security-engineer (安全审查)
```

#### 🔧 `/sc:troubleshoot` - 问题诊断
```bash
# 基础语法
/sc:troubleshoot "问题描述" [选项]

# 参数详解
--systematic              # 系统性诊断方法
--quick                   # 快速诊断模式
--category [type]         # 问题类别 (performance|bug|security|architecture)  
--severity [level]        # 严重程度 (low|medium|high|critical)
--environment [env]       # 环境信息 (dev|staging|production)
--logs [path]             # 日志文件路径
--reproduce [steps]       # 复现步骤
--similar-issues          # 查找类似问题
--root-cause              # 根因分析重点

# 实用示例  
/sc:troubleshoot "Next.js页面加载缓慢" --systematic --category performance --environment production
/sc:troubleshoot "TypeScript编译错误" --quick --logs ./build.log
/sc:troubleshoot "用户登录失败" --severity critical --reproduce --root-cause

# 自动触发的诊断工具
→ Sequential MCP (系统分析)
→ MODE_Introspection (深度反思)
→ @agent-root-cause-analyst (根因分析)
→ @agent-performance-engineer (性能问题)
```

### 🏗️ 架构设计命令详解

#### 📐 `/sc:design` - 架构和设计  
```bash
# 基础语法
/sc:design "设计目标" [选项]

# 参数详解
--level [scope]           # 设计层级 (component|module|system|enterprise)
--methodology [method]    # 设计方法 (ddd|clean|mvc|microservices)
--scalability [target]    # 扩展性目标 (small|medium|large|enterprise)
--technology [stack]      # 技术栈 (mern|mean|jamstack|serverless)
--constraints [list]      # 设计约束 (performance|cost|time|compliance)
--stakeholders [roles]    # 干系人 (dev|ops|business|users)
--documentation [level]   # 文档详细度 (basic|detailed|comprehensive)
--review                  # 包含设计评审

# 实用示例
/sc:design "微服务架构" --level system --methodology microservices --scalability large
/sc:design "React状态管理" --level module --technology react --constraints performance
/sc:design "数据库设计" --methodology ddd --stakeholders dev,business --review

# 专家协作模式
→ @agent-system-architect (系统架构)
→ @agent-frontend-architect (前端架构)
→ @agent-backend-architect (后端架构)
→ Context7 MCP (官方最佳实践)
```

#### 📋 `/sc:task` - 任务分解和规划
```bash
# 基础语法
/sc:task "项目/功能描述" [选项]

# 参数详解
--breakdown [method]      # 分解方法 (wbs|agile|kanban|gtd)
--granularity [level]     # 任务粒度 (epic|story|task|subtask)
--estimation [approach]   # 估算方法 (story-points|hours|complexity)
--priority [system]       # 优先级系统 (moscow|kano|value|urgency)
--dependencies            # 包含依赖关系分析
--resources [info]        # 资源需求分析
--risks                   # 风险识别
--milestones              # 里程碑设置
--timeline [duration]     # 时间线规划 (days|weeks|months)

# 实用示例  
/sc:task "构建电商平台" --breakdown agile --granularity story --estimation story-points --dependencies
/sc:task "性能优化项目" --priority moscow --risks --timeline weeks
/sc:task "UI组件库开发" --granularity task --resources --milestones

# 自动激活系统
→ MODE_Task_Management (任务管理模式)
→ @agent-requirements-analyst (需求分析)
→ @agent-system-architect (技术评估)
```

### 🔧 质量保证命令详解

#### 🧪 `/sc:test` - 测试策略和实现
```bash
# 基础语法
/sc:test [测试目标] [选项]

# 参数详解
--strategy [approach]     # 测试策略 (unit|integration|e2e|performance|security)
--framework [tool]        # 测试框架 (jest|vitest|cypress|playwright)  
--coverage [target]       # 覆盖率目标 (percentage or detailed)
--automation             # 自动化测试设置
--mock [level]           # Mock策略 (none|partial|comprehensive)
--data [approach]        # 测试数据 (fixtures|generated|real)
--environment [env]      # 测试环境 (local|ci|staging)
--reports [format]       # 报告格式 (console|html|xml|json)
--continuous             # 持续测试集成

# 实用示例
/sc:test "用户认证模块" --strategy unit,integration --framework jest --coverage 90%
/sc:test --strategy e2e --framework playwright --automation --reports html
/sc:test "API接口" --strategy integration --mock partial --continuous

# 专家协作
→ @agent-quality-engineer (测试专家)
→ Playwright MCP (E2E测试)
→ @agent-security-engineer (安全测试)
```

#### 🏗️ `/sc:build` - 构建和部署
```bash  
# 基础语法
/sc:build [选项]

# 参数详解
--target [env]            # 目标环境 (development|staging|production)
--optimization [level]    # 优化级别 (none|basic|advanced|aggressive)
--bundle-analysis         # 包分析
--source-maps [type]      # Source Maps (inline|separate|none)
--compression [method]    # 压缩方式 (gzip|brotli|both)
--caching [strategy]      # 缓存策略 (aggressive|normal|minimal)
--validation             # 构建验证
--deployment [method]     # 部署方式 (static|serverless|docker|k8s)
--monitoring             # 监控集成
--rollback               # 回滚策略

# 实用示例
/sc:build --target production --optimization advanced --bundle-analysis --compression both
/sc:build --deployment serverless --monitoring --validation
/sc:build --target staging --source-maps separate --caching normal

# 工具集成  
→ @agent-devops-architect (部署专家)
→ @agent-performance-engineer (优化建议)
```

### 🔍 分析和改进命令详解

#### 📊 `/sc:improve` - 代码和架构改进
```bash
# 基础语法
/sc:improve [改进目标] [选项]

# 参数详解
--focus [aspect]          # 改进重点 (performance|security|maintainability|scalability)
--methodology [approach]  # 改进方法 (refactor|redesign|optimize|modernize)
--scope [range]          # 改进范围 (component|module|system|architecture)
--constraints [limits]    # 改进约束 (time|budget|compatibility|risk)
--metrics [targets]      # 目标指标 (performance|quality|maintainability)
--validation [method]    # 验证方式 (testing|benchmarks|review|monitoring)
--backward-compatibility # 向后兼容性
--incremental           # 增量改进模式
--documentation         # 更新文档

# 实用示例
/sc:improve "React组件性能" --focus performance --methodology optimize --validation benchmarks
/sc:improve "代码可维护性" --methodology refactor --scope module --incremental --documentation  
/sc:improve "系统架构" --focus scalability --methodology redesign --constraints compatibility

# 专家选择
→ @agent-refactoring-expert (重构专家)
→ @agent-performance-engineer (性能优化)
→ @agent-security-engineer (安全改进)
→ Morphllm MCP (批量重构)
```

### 📝 文档和交流命令详解

#### 📚 `/sc:document` - 文档生成
```bash
# 基础语法
/sc:document [文档类型] [选项]

# 参数详解
--type [category]         # 文档类型 (api|user|technical|architecture|deployment)
--audience [target]       # 目标受众 (developer|user|business|ops)
--format [style]         # 输出格式 (markdown|html|pdf|wiki|confluence)
--detail [level]         # 详细程度 (summary|standard|comprehensive|reference)
--interactive           # 交互式文档
--examples              # 包含示例代码
--diagrams             # 生成图表
--auto-update          # 自动更新机制
--translation [langs]   # 多语言支持

# 实用示例
/sc:document "API接口" --type api --audience developer --format markdown --examples
/sc:document "系统架构" --type architecture --audience business --diagrams --detail comprehensive
/sc:document "用户手册" --type user --audience user --interactive --translation en,zh

# 专家协作
→ @agent-technical-writer (技术写作)
→ @agent-system-architect (架构文档)
```

#### 💭 `/sc:explain` - 代码和概念解释
```bash
# 基础语法  
/sc:explain [解释对象] [选项]

# 参数详解
--audience [level]        # 受众水平 (beginner|intermediate|expert|mixed)
--depth [detail]         # 解释深度 (overview|detailed|comprehensive|internals)
--context [scope]        # 上下文范围 (local|module|system|domain)
--examples [type]        # 示例类型 (simple|practical|advanced|comprehensive)  
--analogies             # 使用类比解释
--step-by-step          # 分步骤解释
--visual               # 可视化解释
--interactive          # 交互式解释

# 实用示例
/sc:explain "React Hooks工作原理" --audience intermediate --depth detailed --examples practical
/sc:explain "微服务架构" --audience beginner --analogies --visual --step-by-step
/sc:explain components/UserAuth.tsx --context module --depth comprehensive

# 教学专家
→ @agent-learning-guide (学习指导)
→ @agent-socratic-mentor (苏格拉底式教学)
```

### 🔄 会话管理命令详解

#### 💾 `/sc:save` - 会话状态保存
```bash
# 基础语法
/sc:save [保存名称] [选项]

# 参数详解  
--context [scope]         # 保存范围 (current|project|global|custom)
--include [items]         # 包含内容 (code|analysis|decisions|progress|learnings)
--format [type]          # 保存格式 (structured|narrative|checklist|mindmap)
--tags [labels]          # 标签分类 (project-name|phase|priority|domain)
--encryption            # 加密保存
--compression           # 压缩保存
--metadata              # 包含元数据
--auto-cleanup [days]   # 自动清理策略

# 实用示例
/sc:save "电商项目-架构阶段" --context project --include analysis,decisions --tags ecommerce,architecture
/sc:save "性能优化经验" --format narrative --tags performance,learnings --metadata
/sc:save --context current --include progress --auto-cleanup 30

# 集成工具
→ Serena MCP (项目记忆)
→ MODE_Task_Management (任务状态)
```

#### 📂 `/sc:load` - 会话状态加载
```bash
# 基础语法
/sc:load [会话名称] [选项]

# 参数详解
--filter [criteria]      # 过滤条件 (recent|project|tag|date|priority)
--merge [strategy]       # 合并策略 (replace|append|selective|interactive)
--validate              # 验证完整性
--preview               # 预览模式
--partial [sections]    # 部分加载 (context|code|analysis|tasks)
--update-references     # 更新引用链接

# 实用示例  
/sc:load "电商项目-架构阶段" --validate --update-references
/sc:load --filter recent,project:ecommerce --preview
/sc:load "性能优化经验" --partial context,analysis --merge selective

# 恢复机制
→ Serena MCP (记忆恢复)
→ 自动重建上下文关系
```

---

## 🎛️ 全局参数和修饰符

### ⚡ 通用执行修饰符
```bash
--expert-mode            # 启用专家协作模式 (适用于所有命令)
--quick                  # 快速模式，减少详细分析 (分析类命令)
--comprehensive          # 全面模式，最大深度分析 (分析类命令)  
--interactive            # 交互式模式，逐步确认 (复杂命令)
--batch [list]           # 批处理模式，处理多个目标 (处理类命令)
--preview                # 预览模式，不执行实际操作 (修改类命令)
--force                  # 强制模式，跳过警告 (风险操作)
--verbose                # 详细输出模式 (所有命令)
--silent                 # 静默模式，最小输出 (自动化场景)
```

### 🔗 上下文和集成参数
```bash
--context [scope]        # 上下文范围控制
--mcp [services]         # 指定MCP服务 (sequential|serena|context7|playwright|magic|morphllm)
--agents [list]          # 指定代理列表
--mode [behavior]        # 强制特定模式 (brainstorming|orchestration|task-management|etc)
--workspace [path]       # 工作区路径
--config [file]          # 配置文件路径
```

### 📊 输出和格式参数
```bash
--format [type]          # 输出格式 (markdown|json|yaml|html|text)
--template [name]        # 输出模板
--export [destination]   # 导出目标
--language [lang]        # 输出语言 (en|zh|ja)
--style [preset]         # 输出风格 (professional|casual|technical|educational)
```

---

## 🚨 错误处理和调试参数

### 🔍 调试和诊断
```bash
--debug                  # 启用调试模式
--trace                  # 执行追踪
--profile                # 性能分析
--validate               # 验证模式
--dry-run                # 试运行模式
--checkpoint [frequency] # 设置检查点
--rollback [point]       # 回滚到检查点
```

### ⚠️ 安全和权限
```bash
--safe-mode              # 安全模式，额外验证
--permissions [level]    # 权限级别控制
--audit                  # 审计模式，记录所有操作
--encrypt                # 加密处理敏感数据
--sandbox                # 沙箱模式，隔离执行
```

---

*这个详细参数速查表帮助您精确控制每个命令的行为，避免参数混乱导致的执行偏差。*