# 🎯 SuperClaude 场景导向速查表

## 🚀 针对您的专业场景：Next.js/TypeScript 全栈开发

### 🔥 核心痛点解决方案

#### 🎯 场景1：需求拆解 → 架构设计 (解决：容易迷失方向)
```bash
# 标准工作流：需求 → 设计 → 实现 (防迷失)
📋 第1步：需求澄清
/sc:brainstorm "具体项目需求" 
  ↓ 自动启动 MODE_Brainstorming
@agent-requirements-analyst "细化需求和用户故事"

📐 第2步：架构设计  
/sc:design "基于需求设计Next.js应用架构"
@agent-system-architect "评估技术选型和架构合理性"
@agent-frontend-architect "Next.js项目结构建议"

📝 第3步：任务分解
/sc:task "将设计分解为可执行任务"
  ↓ 启动 MODE_Task_Management
/sc:save "保存当前进度和下一步计划"
```

#### 🔍 场景2：代码分析 → 架构理解 (解决：复杂项目理解困难)
```bash
# 高效分析工作流 (5分钟掌握项目架构)
🔎 快速扫描
/sc:analyze project_root/ --focus architecture
  ↓ 自动启用 Sequential MCP + Serena MCP

🏗️ 架构洞察
@agent-system-architect "Next.js项目架构分析和改进建议"
@agent-frontend-architect "组件设计模式和状态管理评估"

📊 质量评估
@agent-quality-engineer "代码质量和测试覆盖度评估"
/sc:document "项目架构分析报告" --format structured
```

#### 🚀 场景3：功能实现 → 一次性完成 (解决：开发质量和完成度)
```bash
# 高质量实现工作流 (符合期望一次完成)
🎯 实现规划
/sc:implement "具体功能需求" --expert-mode --quality-first
  ↓ 自动选择相关专家
  ↓ 启用 MODE_Orchestration 优化协作

👨‍💻 专家协作 (并行处理)
@agent-frontend-architect "React/Next.js组件设计"
@agent-python-expert "Node.js/TypeScript后端逻辑" (如涉及后端)
@agent-quality-engineer "测试用例和质量标准"

🔒 安全和性能
@agent-security-engineer "安全漏洞检查"
@agent-performance-engineer "性能优化建议"

✅ 验证完成
/sc:test --comprehensive
/sc:build --production-ready
```

#### 🔧 场景4：故障诊断 → 性能优化 (解决：问题定位困难)
```bash
# 系统性诊断工作流
🚨 问题分析
/sc:troubleshoot "具体问题描述" --systematic
  ↓ Sequential MCP 深度分析
  ↓ MODE_Introspection 反思模式

🔍 根因分析  
@agent-root-cause-analyst "深度根因追溯"
@agent-performance-engineer "性能瓶颈识别" (如是性能问题)

⚡ 解决方案
/sc:improve "基于诊断结果的优化方案"
@agent-frontend-architect "前端优化策略" (如涉及前端)

📝 经验总结
/sc:reflect "问题解决过程总结"
/sc:save "添加到问题解决知识库"
```

---

## 🎪 按工作阶段的快速决策表

### 📋 项目启动阶段
| 情况 | 首选命令 | 配合专家 | 预期结果 |
|------|---------|---------|----------|
| 🤔 需求不明确 | `/sc:brainstorm` | `@agent-requirements-analyst` | 清晰的需求和用户故事 |
| 🏗️ 需要架构设计 | `/sc:design` | `@agent-system-architect` + `@agent-frontend-architect` | 技术选型和架构图 |
| 📝 需要任务规划 | `/sc:task` | `@agent-requirements-analyst` | 详细的开发计划 |
| ⏱️ 需要时间估算 | `/sc:estimate` | `@agent-system-architect` | 开发时间和资源预估 |

### 🔍 代码理解阶段  
| 情况 | 首选命令 | 配合专家 | 预期结果 |
|------|---------|---------|----------|
| 📊 分析新项目 | `/sc:analyze path/ --comprehensive` | `@agent-system-architect` | 全面的项目结构分析 |
| 🔍 理解复杂逻辑 | `/sc:explain "具体代码/模块"` | `@agent-frontend-architect` | 清晰的代码逻辑解释 |
| 🚨 诊断问题 | `/sc:troubleshoot "问题描述"` | `@agent-root-cause-analyst` | 问题根因和解决方案 |

### 🚀 开发实现阶段
| 情况 | 首选命令 | 配合专家 | 预期结果 |
|------|---------|---------|----------|
| ⚡ 快速开发功能 | `/sc:implement "功能需求"` | 自动选择相关专家 | 生产就绪的代码 |
| 🔧 代码重构 | `/sc:improve "重构目标"` | `@agent-refactoring-expert` | 优化后的代码结构 |
| 🧪 编写测试 | `/sc:test "测试策略"` | `@agent-quality-engineer` | 完整的测试套件 |
| 🏗️ 构建部署 | `/sc:build` | `@agent-devops-architect` | 部署就绪的构建 |

### 📊 质量保证阶段
| 情况 | 首选命令 | 配合专家 | 预期结果 |
|------|---------|---------|----------|
| 🔒 安全检查 | 自动触发 | `@agent-security-engineer` | 安全漏洞报告 |
| ⚡ 性能优化 | `/sc:improve --performance` | `@agent-performance-engineer` | 性能优化方案 |
| 📝 文档生成 | `/sc:document "文档类型"` | `@agent-technical-writer` | 专业文档 |

---

## 🔄 防迷失工作流控制策略

### ✅ 始终明确当前阶段
```bash
# 每个阶段开始前确认
/sc:reflect "当前处于什么阶段，下一步要做什么？"
  ↓ 获得阶段确认和方向指引

# 每个任务完成后保存进度  
/sc:save "当前进度和后续计划"
  ↓ 防止上下文丢失
```

### 🎯 任务分解最佳实践
```bash
# 复杂任务必须分解
大任务 → /sc:task "分解为小任务" 
  ↓ MODE_Task_Management 自动激活
  ↓ 每个小任务独立完成
  ↓ /sc:reflect "检查完成质量"
```

### 🚨 迷失时的重置流程
```bash
# 当感到混乱时立即执行
/sc:load "上次保存的进度" (如果有)
/sc:reflect "回顾当前目标和已完成的工作"
@agent-requirements-analyst "重新确认最初需求"
/sc:task "重新规划剩余任务"
```

---

## 🎯 Next.js/TypeScript 专项优化组合

### 🚀 现代前端开发黄金组合
```bash
# 组合1：React组件开发
Magic MCP + @agent-frontend-architect + Context7 MCP
  → UI组件生成 + 架构指导 + React最佳实践

# 组合2：TypeScript代码质量  
Serena MCP + @agent-refactoring-expert + @agent-quality-engineer
  → 代码理解 + 重构建议 + 质量保证

# 组合3：全栈Next.js开发
@agent-frontend-architect + @agent-system-architect + Context7 MCP
  → 前端架构 + 系统设计 + Next.js官方规范
```

### ⚡ 高频场景快速命令
```bash
# React组件分析和优化
/sc:analyze components/ --focus react-patterns
@agent-frontend-architect "组件设计模式评估"

# TypeScript类型问题诊断  
/sc:troubleshoot "TypeScript类型错误"
@agent-python-expert "TypeScript类型系统优化" 

# Next.js性能优化
/sc:improve --performance --focus next-js
@agent-performance-engineer "Next.js应用性能优化"

# 状态管理架构设计
/sc:design "React状态管理方案"
@agent-frontend-architect "状态管理最佳实践"
```

---

## 📊 效率提升指标

### ⏱️ 时间节省目标
- **需求分析**: 30分钟 → 10分钟 (66%节省)
- **架构设计**: 2小时 → 30分钟 (75%节省)  
- **代码实现**: 8小时 → 3小时 (62%节省)
- **问题诊断**: 1小时 → 15分钟 (75%节省)

### ✅ 质量提升目标
- **需求完整性**: 提升50%
- **代码质量**: 提升40% 
- **架构合理性**: 提升60%
- **一次完成率**: 提升80%

---

*这个速查表专门针对您的Next.js/TypeScript开发场景优化，解决工作流混乱的核心问题。*