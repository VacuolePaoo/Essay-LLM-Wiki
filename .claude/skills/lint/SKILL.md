---
name: lint
description: >
  Run a health check on the essay wiki — check link integrity, coverage gaps, and index sync.
  Use this skill when the user says "lint", "健康检查", "check wiki", "检查链接",
  "wiki 健康", or asks whether the wiki is in good shape.
---

# Lint Skill

You are running a health check on the high school Chinese essay wiki. Read all relevant files and report issues found.

## Checks to Perform

### 1. Bidirectional Link Integrity

For every material page, check that:
- Each topic listed in "可用主题" has this material listed in its "关联素材" (and vice versa)
- If a link is one-way, report the missing reverse link

### 2. Topic Coverage

For every topic page, count the linked materials in "关联素材":
- Fewer than 3 materials: flag as "素材偏少，建议补充"
- Zero materials: flag as "缺少关联素材"

### 3. Material Usage Examples

For every material page, check "使用示例":
- Empty "使用示例": flag as "没有实战引用的素材价值较低"
- At least one entry present: pass

### 4. Essay Material Coverage

For every essay page, check "关联素材":
- Empty: flag as "未提取素材的范文分析不完整"
- Has entries: pass

### 5. Index Synchronization

**Material index (`wiki/material/index.md`):**
- Every material file in `wiki/material/*.md` (excluding index.md) should have a corresponding entry in the index
- Every entry in the index should correspond to an existing file
- Report any mismatches

**Main index (`wiki/index.md`):**
- Every topic file in `wiki/topic/*.md` should appear in the "主题" section
- Every essay file in `wiki/essay/*.md` should appear in the "范文" section
- Every material file in `wiki/material/*.md` (excluding index.md) should appear in the "素材" section
- Report any mismatches

## Output Format

Group findings by severity:

```markdown
# Wiki 健康检查报告

## 链接完整性
- ...

## 素材覆盖
- ...

## 索引同步
- ...

## 总结
- X 个问题需要修复
```

After reporting, ask the user if they want to fix the issues found.
