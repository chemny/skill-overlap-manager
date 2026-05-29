# Skill Overlap Manager

> 一个用于在创建或修改本地 Agent Skills 前检查能力重叠的 Codex skill。

[English README](README.md) · 中文

Skill Overlap Manager 用来帮助你管理不断增长的 skills 集合。在创建、安装或修改一个 skill 之前，它会先检查已有 skill 里是否已经存在相似能力，并帮助判断应该修改已有 skill，还是创建一个边界更清晰的新 skill。

---

## 它能做什么？

- 查找名称、触发词、领域或职责相似的已有 skill。
- 识别泛化 skill 和更专业 skill 之间的重叠。
- 帮助区分主工作流 skill、工具型 skill、风格层 skill、治理型 skill 和知识层 skill。
- 建议修改已有 skill、继续创建更窄的新 skill、归档旧 skill，或取消创建。
- 引导在 skill 描述里写清 `Use when`、`Do not use when`、`Prefer`、`Defer to`、`Pair with` 等边界。

---

## 它解决什么问题？

当本地 skills 越来越多时，`write`、`polish`、`frontend`、`design`、`PPT`、`debug` 这类触发词很容易被多个 skill 同时覆盖。新 skill 可能重复已有能力，泛化 skill 也可能和更专业的工作流 skill 抢触发。

这个 skill 的作用是在继续增加 skill 之前，先检查已有能力。

---

## 核心流程

```text
Inspect -> Compare -> Recommend -> Bound
```

- `Inspect`：理解用户想创建或修改的 skill。
- `Compare`：扫描已有 skill，找出相似名称、描述和触发词。
- `Recommend`：建议修改、新建、归档、删除或取消。
- `Bound`：如果继续变更，帮助定义更清晰的 skill 范围。

---

## 安装

这是一个单 skill 仓库，仓库根目录就是 skill 根目录。

必须满足这个结构：

```text
skill-overlap-manager/
└── SKILL.md
```

### 1. 克隆仓库

```bash
git clone https://github.com/chemny/skill-overlap-manager.git
```

### 2. 放到你的 Agent skills 目录

把克隆下来的目录复制或软链接到你的 Agent 使用的 skills 目录。

### 3. 开启新会话

很多 Agent 会在新会话启动时扫描 skill metadata。安装后建议开启一个新会话，让 Agent 重新读取 `SKILL.md`。

### 4. 验证

可以用类似这样的请求测试：

```text
我想创建一个新的 SEO 写作 skill，先帮我看看有没有类似的 skill。
```

### 后续更新

如果你是用 Git 安装的：

```bash
git pull
```

---

## 使用示例

```text
我想创建一个用于中文 AI 教程写作的 skill，先帮我查一下有没有和现有 skills 重叠。
```

```text
帮我优化这个 skill 的 description，确认它不会和附近的写作类 skill 冲突。
```

```text
我准备安装一个演示文稿 skill，先帮我判断它和现有 PPT / slides 类 skill 是否重叠。
```

---

## 安全边界

这个 skill 只负责 skill 重叠检查和范围管理。它不应该：

- 保存密钥、token、cookie 或凭证。
- 自动删除已有 skill。
- 发布或推送 GitHub 仓库。
- 在没有用户确认时修改已有 skill。
- 把机器环境策略写进 skill 内容。

---

## 仓库结构

```text
skill-overlap-manager/
├── SKILL.md
├── README.md
├── README.zh.md
├── LICENSE
└── scripts/
    └── audit_skill_overlap.py
```

---

## License

MIT
