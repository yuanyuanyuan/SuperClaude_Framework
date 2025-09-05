# /sc:quickref - SuperClaude 速查系统

## 🎯 指令目的

提供快速访问SuperClaude速查表的专用指令，解决工作流混乱和参数记忆困难的问题。

## 🚀 使用语法

```bash
/sc:quickref [查询类型] [具体查询] [选项]
```

## 📋 查询类型

### 🎪 场景查询 (scenario/s)
```bash
# 查询特定开发场景的最佳工作流
/sc:quickref scenario "需求分析"
/sc:quickref s "代码重构"
/sc:quickref scenario "性能优化" --framework nextjs
/sc:quickref s "故障诊断" --detail comprehensive

# 支持的场景关键词
- 需求分析 | requirements | brainstorm
- 架构设计 | architecture | design  
- 代码分析 | analysis | understand
- 功能实现 | implement | develop | build
- 代码重构 | refactor | improve | cleanup
- 性能优化 | performance | optimize | speed
- 故障诊断 | troubleshoot | debug | fix
- 质量保证 | testing | quality | validation
- 文档生成 | document | docs | explain
```

### 🔧 命令查询 (command/c)
```bash
# 查询特定命令的参数和用法
/sc:quickref command analyze
/sc:quickref c implement --examples
/sc:quickref command troubleshoot --params-only
/sc:quickref c build --advanced

# 支持所有22个SuperClaude命令
- analyze, brainstorm, build, design, implement, improve
- troubleshoot, test, document, explain, estimate, task
- workflow, reflect, save, load, spawn, select-tool
- cleanup, git, business-panel, index
```

### 👥 专家查询 (agent/a)
```bash
# 查询特定专家代理的能力和使用场景
/sc:quickref agent system-architect
/sc:quickref a frontend-architect --use-cases
/sc:quickref agent python-expert --with-commands
/sc:quickref a root-cause-analyst --troubleshooting

# 支持所有15个专家代理
- system-architect, frontend-architect, backend-architect
- python-expert, performance-engineer, security-engineer
- quality-engineer, refactoring-expert, requirements-analyst
- root-cause-analyst, learning-guide, socratic-mentor
- technical-writer, devops-architect, business-panel-experts
```

### 🔗 工作流查询 (workflow/w)
```bash
# 查询组合工作流和最佳实践
/sc:quickref workflow "nextjs开发"
/sc:quickref w "typescript项目" --full-cycle
/sc:quickref workflow "企业项目" --team-collaboration
/sc:quickref w "性能调优" --systematic

# 专项工作流
- frontend-development | 前端开发
- backend-development | 后端开发  
- fullstack-development | 全栈开发
- performance-tuning | 性能调优
- architecture-design | 架构设计
- quality-assurance | 质量保证
- troubleshooting | 故障排除
- project-management | 项目管理
```

### 🎛️ 参数查询 (params/p)
```bash
# 查询命令参数详细说明
/sc:quickref params analyze --all
/sc:quickref p implement --focus quality
/sc:quickref params global --modifiers
/sc:quickref p troubleshoot --examples

# 参数类别
- command-specific | 命令特定参数
- global-modifiers | 全局修饰符
- output-format | 输出格式参数
- integration-params | 集成参数
- debug-params | 调试参数
```

## 🎯 选项参数

### 📊 输出控制
```bash
--format [type]           # 输出格式 (quick|detailed|comprehensive|table)
--examples               # 包含使用示例
--params-only            # 仅显示参数信息
--use-cases              # 包含使用场景
--with-commands          # 包含相关命令
--framework [name]       # 特定框架信息 (nextjs|react|typescript)
--full-cycle             # 完整生命周期信息
--systematic            # 系统性方法
--advanced              # 高级用法
--troubleshooting       # 故障排除重点
--team-collaboration    # 团队协作重点
```

### 🔍 过滤和搜索
```bash
--filter [criteria]      # 过滤条件 (beginner|intermediate|expert)
--search [keywords]      # 关键词搜索
--category [type]        # 分类 (dev|arch|qa|mgmt|debug)
--priority [level]       # 优先级 (high|medium|low)
--complexity [level]     # 复杂度 (simple|moderate|complex)
```

## 🚀 智能响应机制

### 🧠 自动场景识别
当用户查询时，系统会：
1. **分析查询意图** - 识别是场景、命令还是工作流查询
2. **匹配最佳答案** - 从速查表中提取最相关的信息
3. **提供后续建议** - 给出下一步行动建议
4. **关联参考** - 链接到相关的其他查询

### 🎯 上下文感知
```bash
# 基于当前项目类型自动调整建议
当前项目：Next.js + TypeScript
/sc:quickref scenario "性能优化"
→ 自动提供Next.js特定的性能优化工作流

# 基于历史查询优化建议
最近查询：architecture相关
/sc:quickref command analyze  
→ 突出显示架构分析相关参数
```

### ⚡ 快速响应模板

#### 场景查询响应格式
```markdown
# 🎯 [场景名称] 工作流

## ⚡ 快速启动
[核心命令组合]

## 🔧 详细步骤  
[分步骤工作流]

## 👥 推荐专家
[相关代理专家]

## 📋 常用参数
[关键参数说明]

## 🚀 下一步建议
[后续行动建议]
```

#### 命令查询响应格式
```markdown
# 🔧 [命令名称] 详细用法

## 📝 基础语法
[语法格式]

## 🎛️ 核心参数
[重要参数解释]

## 💡 使用示例  
[实际示例]

## 🔗 相关命令
[关联命令建议]

## ⚠️ 注意事项
[使用要点]
```

## 🛠️ 实现逻辑

### 📚 数据源集成
```bash
# 自动读取速查表文件
→ SCENARIO_QUICK_REFERENCE.md (场景工作流)
→ COMMAND_PARAMETER_REFERENCE.md (命令参数)
→ PROJECT_INDEX.md (完整索引)
→ CROSS_REFERENCES.md (交叉引用)

# 智能解析和匹配
→ 关键词提取和语义匹配
→ 上下文相关性分析  
→ 个性化建议生成
```

### 🎯 查询处理流程
```
用户查询 → 意图识别 → 数据匹配 → 格式化输出 → 建议生成
    ↓
自动学习用户偏好 → 优化后续响应
```

## 💡 使用示例

### 🚀 典型使用场景
```bash
# 场景1：迷失在复杂项目中
用户感到混乱时：
/sc:quickref scenario "项目分析" --framework nextjs
→ 获得结构化的Next.js项目分析工作流

# 场景2：忘记命令参数  
需要实现功能时：
/sc:quickref command implement --examples --advanced
→ 获得implement命令的详细参数和高级用法

# 场景3：寻找最佳工作流
开始新任务时：
/sc:quickref workflow "fullstack开发" --full-cycle
→ 获得完整的全栈开发生命周期工作流

# 场景4：专家选择困难
不确定用哪个专家时：
/sc:quickref agent --category arch --use-cases
→ 获得架构相关专家的能力对比和使用场景
```

### 🎪 组合查询示例
```bash
# 连续查询优化工作流
/sc:quickref scenario "性能问题"
→ 获得诊断步骤
/sc:quickref command troubleshoot --systematic
→ 获得详细诊断参数
/sc:quickref agent performance-engineer --troubleshooting  
→ 获得专家协作建议
```

## 🎯 预期效果

### ✅ 解决核心痛点
- **工作流混乱** → 清晰的步骤指引
- **参数记忆困难** → 即时参数查询  
- **专家选择困难** → 智能推荐系统
- **上下文丢失** → 结构化信息保持

### 📈 效率提升指标
- **查询时间**: 30秒 → 5秒 (83%提升)
- **工作流执行错误率**: 40% → 10% (75%降低)
- **任务完成一致性**: 60% → 90% (50%提升)
- **学习曲线**: 减少60%的试错时间

---

## 🔧 技术实现建议

### 🎯 MCP集成策略
```bash
# 与现有MCP服务器协同
Context7 MCP → 官方文档验证和补充
Sequential MCP → 复杂查询的系统性分析  
Serena MCP → 项目上下文感知和个性化建议

# 独立查询能力
本地速查表缓存 → 快速响应
智能语义匹配 → 模糊查询支持
学习用户偏好 → 个性化优化
```

### 📊 数据结构设计  
```json
{
  "scenarios": {
    "performance-optimization": {
      "keywords": ["性能", "优化", "缓慢", "卡顿"],
      "workflow": "详细工作流步骤",
      "commands": ["analyze", "troubleshoot", "improve"],
      "agents": ["performance-engineer", "root-cause-analyst"],
      "frameworks": {
        "nextjs": "Next.js特定优化步骤"
      }
    }
  },
  "commands": {
    "analyze": {
      "syntax": "命令语法",
      "parameters": "参数详解",  
      "examples": "使用示例",
      "related": "相关命令"
    }
  }
}
```

这个 `/sc:quickref` 系统将成为您的SuperClaude使用助手，随时解决工作流混乱的问题！