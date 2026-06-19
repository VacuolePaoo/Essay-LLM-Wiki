---
name: query
description: >
  Answer questions about the high school Chinese essay wiki — find materials, essays, topics,
  and provide analysis. Use this skill whenever the user asks about wiki content,
  such as "有哪些关于坚持的素材", "帮我找一篇范文", "这个主题下有什么素材",
  "推荐素材", "怎么写这个题目", or any question that would benefit from reading the wiki.
---

# Query Skill

You are answering questions using a high school Chinese essay wiki. Your goal is to find and synthesize relevant information from the wiki to give helpful, specific answers.

## Workflow

### Step 1: Read Main Index

Read `wiki/index.md` to get a global overview of available topics, essays, and materials.

### Step 2: Narrow Down

Based on the question:

- If about materials: read `wiki/material/index.md` for the detailed material index (grouped by type: 人物/事件/道理). This is the primary entry point for material lookup.
- If about a specific topic: read the relevant `wiki/topic/{主题}.md`
- If about a specific essay: read the relevant `wiki/essay/{范文}.md`

### Step 3: Read Target Pages

Navigate to the specific wiki pages identified in step 2 and read their full content.

### Step 4: Synthesize Answer

Combine information from all relevant pages into a coherent answer. Use `[[双链]]` references so the user can navigate directly in Obsidian.

### Step 5: Offer to Write Back

If your answer has lasting value (comparison analysis, topic outline, material recommendation), suggest writing it back to the wiki as a new page or updating an existing one. Ask the user before proceeding.
