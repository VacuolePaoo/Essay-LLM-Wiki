# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 高中语文作文 Wiki

本项目是一个基于 LLM Wiki 模式的高中语文作文知识库，也是一个 Obsidian vault。LLM 负责维护 wiki 的全部内容，用户负责提供原始资料和提问。所有页面间关联使用 Obsidian `[[双链]]` 语法。

### 目录结构

```
├── raw/                        # 原始资料
│   └── archive/                # 已处理的资料（ingest 后移入）
├── wiki/                       # LLM 维护的 wiki
│   ├── material/               # 素材页面
│   │   └── index.md            # 素材专用详细索引
│   ├── essay/                  # 范文页面
│   ├── topic/                  # 主题页面
│   ├── issues/                  # 素材矛盾冲突问题报告
│   ├── index.md                # 主索引
│   └── log.md                  # 操作日志
├── scripts/                    # 辅助脚本
│   └── validate_frontmatter.py # frontmatter 校验（纯标准库，零依赖）
└── templates/                  # 页面模板
    ├── material-template.md
    ├── essay-template.md
    └── topic-template.md
```

### 输入类型

只有两种内容类型，可能出现在同一个文件中：

1. **范文** — 完整的作文原文，可能包含题目和写作指导
2. **素材** — 人物事迹、事件、道理论据等

### 工作流

详细工作流由对应的 skill 定义：

- **`/ingest`** — 导入素材或范文到 wiki。带文件参数时处理指定文件，不带参数时处理 `raw/` 下未归档的新文件。处理后文件移入 `raw/archive/`
- **`/query`** — 查询 wiki 内容，综合索引和页面回答问题
- **`/lint`** — 健康检查：链接完整性、素材覆盖、索引同步

### 硬性约束

- `raw/` 目录下文件 LLM 只读不改，处理后移入 `raw/archive/`
- 范文全文必须原样搬运，禁止任何改动
- 写作指导只允许来自 raw，禁止 AI 自行编写
- 所有关联使用 Obsidian `[[双链]]` 语法，双向链接必须完整
- `log.md` 为 append-only，只追加不修改
- 素材名称用本名，不用修饰语（如 `苏轼.md`，不写 `宋代诗人苏轼.md`）
- 主题用四字或六字短语命名（如 `家国情怀.md`）
- 范文文件名格式：`来源-作文标题.md`（无来源则只用标题）
- 作文原子化拆分时，素材的「关键事迹」「事件经过」等事实性内容应当来自作文原文；若 AI 使用通用知识库或联网搜索补充条目，必须在该条目前面标注 `【AI】` 前缀
- 若导入素材与已有素材存在事实性矛盾或冲突：在素材页底部追加 `## 矛盾冲突` 章节，原封搬运冲突双方的原文内容方便对比，并在 `wiki/issues/{素材名}-矛盾冲突.md` 创建问题报告

### Obsidian CLI

`/lint` 依赖 `obsidian` CLI 工具检查链接。关键命令均需加 `vault=EssaySystem`：

```bash
obsidian unresolved verbose vault=EssaySystem   # 全局死链扫描
obsidian orphans vault=EssaySystem               # 孤立笔记
obsidian deadends vault=EssaySystem              # 死端笔记（无出链）
obsidian backlinks file=<名> vault=EssaySystem    # 反向链接
obsidian links file=<名> vault=EssaySystem        # 出链
```
