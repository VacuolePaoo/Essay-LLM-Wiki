---
name: ingest
description: >
  Ingest raw materials (素材) or essays (范文) into the high school Chinese essay wiki.
  Use this skill whenever the user provides a raw file to add to the wiki —
  even if they just say "ingest", "add this", "处理这个素材", "导入范文",
  or paste an essay/material without explicit instructions.
---

# Ingest Skill

You are processing raw input for a high school Chinese essay wiki. There are only two input types:

1. **素材** — placed in `raw/material/`: character stories, events, reasoning evidence
2. **范文** — placed in `raw/essay/`: complete essays, possibly with prompts and writing guidance

Read the raw file first, then determine which workflow to follow.

---

## 素材 Ingest

### Step 1: Read and Classify

Read the file from `raw/material/`. Determine the subtype: **人物** / **事件** / **道理**.

### Step 2: Create Material Page

Create `wiki/material/{素材名称}.md` using this template:

```markdown
---
title: 素材名称
type: 素材
subtype: 人物 | 事件 | 道理
tags: []
---

## 人物简介

（一句话或几句话概括核心定位）

## 关键事迹

- 事迹1
- 事迹2
- 事迹3

## 使用示例

（如果已有匹配的主题页，按下面格式添加；否则留空）

### [[主题名称]]-[[来源]]
> 原文引用

## 关联素材

- [[素材链接]] - 关联理由
```

Naming rules:
- Use the person's real name (e.g., `苏轼.md`, not `宋代诗人苏轼.md`)
- For events/reasoning, use a concise descriptive name

### Step 3: Update Topic Pages

Scan `wiki/topic/` for existing topic pages. If any topic is relevant to this material, add a link in that topic page's "关联素材" section.

### Step 4: Update Material Index

Edit `wiki/material/index.md` — add an entry under the matching type (人物/事件/道理):

```markdown
### 素材名
**人物简介**
...
**人物事件**
...
**可用主题**
[[主题]]
**关联文章**
[[文章]]
```

### Step 5: Update Main Index

Edit `wiki/index.md` — add a line in the "素材" section:

```markdown
- [[素材名]] — 简介 | 可用主题
```

### Step 6: Log

Append to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] ingest 素材 | 素材名 — 一句话说明
```

---

## 范文 Ingest

### Step 1: Read

Read the file from `raw/essay/`.

### Step 2: Create Essay Page

Create `wiki/essay/{来源-作文标题}.md` using this template:

```markdown
---
title: 作文标题
type: 范文
from: 考试名称（可选）
tags: []
---

## 题目

（原题，如果没有则不写此节）

## 全文

（原文，禁止任何改动）

## 结构分析

（段落结构、论证方式、行文逻辑）

## 写作指导

（来自 raw 中的写作指导内容，如果没有则禁止 AI 编写此节）

## 关联素材

### 人物
- [[素材链接]]

### 事件
- [[素材链接]]

（按素材类型分组）

## 可学习之处

- （可借鉴的技巧、表达、结构等）
```

Naming rules:
- With source: `2024全国甲-选择与担当.md`
- Without source (non-exam): just the title, e.g., `青春与责任.md`

**Hard rules:**
- The "全文" section must be the original text verbatim — no modifications allowed
- The "写作指导" section must only contain content from raw — if none exists, omit the section entirely. AI must never write this section on its own

### Step 3: Extract Materials

Identify all materials (素材) used in the essay. For each:

- If the material page already exists (`wiki/material/`): append a usage example
- If not: create a new material page

Usage example format (appended to existing material page's "使用示例"):

```markdown
### [[主题名称]]-[[来源]]
> 原文引用（从范文中提取的具体段落）
```

### Step 4: Create or Update Topic Pages

If the essay has a prompt or writing guidance, identify the topic. Create or update `wiki/topic/{主题}.md`:

```markdown
---
title: 主题名称
type: 主题
---

## 主题分析

（破题思路、与现实的联系、中学生应该怎么写、怎么降维）

## 常见出题角度

- 角度1
- 角度2

## 关联素材

- [[素材链接]]

## 范文参考

- [[范文链接]]

## 审题关键词

（常见于作文题目中的关键词，用于判断题目是否属于此主题）
```

Topic naming: use 4- or 6-character phrases (e.g., `家国情怀.md`, `个人成长.md`)

### Step 5: Update Material Index

For every material touched, update `wiki/material/index.md` — refresh the "关联文章" field.

### Step 6: Update Main Index

Edit `wiki/index.md`:
- Add the essay under "范文": `- [[范文]] | 主题：xxx | 素材：[[xxx]], [[xxx]]`
- If a new topic was created, add under "主题": `- [[主题]] | 关键词：xxx`

### Step 7: Log

Append to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] ingest 范文 | 来源-标题 — 一句话说明
```

---

## Cross-Reference Rules

All links use Obsidian `[[双链]]` syntax. Maintain bidirectional links:

| Link | Direction | Where |
|------|-----------|-------|
| Material <-> Topic | Bidirectional | Material "可用主题" <-> Topic "关联素材" |
| Material -> Material | Via "关联素材" section | Material "关联素材" with reason |
| Essay -> Material | Essay links to material | Essay "关联素材" |
| Topic -> Essay | Topic links to essay | Topic "范文参考" |
| Material -> Essay | Via "使用示例" | Material "使用示例" `[[来源]]` links to essay |

When creating links, always check the target page exists. If not, create it.
