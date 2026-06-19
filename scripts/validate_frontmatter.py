#!/usr/bin/env python3
"""Validate frontmatter of all wiki content pages.

Rules:
  Errors (exit code 1):
    - Missing or unclosed frontmatter
    - type missing or not in valid set
    - title missing or empty
    - subtype missing/invalid for 素材 type

  Warnings (exit code 0):
    - type 与实际目录不匹配
    - 文件名命名规范偏离

Usage:
    python scripts/validate_frontmatter.py
"""

from pathlib import Path
import re
import sys
import os

# ── Configuration ────────────────────────────────────────────────

WIKI_DIR = Path("wiki")

# 合法 type 取值
VALID_TYPES = {"素材", "范文", "主题"}

# type -> 合法 subtype
VALID_SUBTYPES = {
    "素材": {"人物", "事件", "道理"},
}

# 内容目录 -> 对应 type（用于目录一致性检查）
CONTENT_DIRS = {
    "material": "素材",
    "essay": "范文",
    "topic": "主题",
}


# ── Frontmatter Parser ───────────────────────────────────────────

def parse_frontmatter(filepath: Path) -> tuple[dict, str | None]:
    """解析 markdown 文件的 YAML frontmatter。

    Returns:
        (frontmatter_dict, error_message)
        若解析成功，error_message 为 None
        若无 frontmatter，返回 (None, error_message)
    """
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return None, f"无法读取文件: {e}"

    if not content.startswith("---"):
        return None, "缺少 frontmatter（文件必须以 '---' 开头）"

    # 查找结束的 ---
    end_idx = content.find("\n---", 3)
    if end_idx == -1:
        return None, "frontmatter 未闭合（缺少结尾 '---'）"

    fm_text = content[3:end_idx].strip()
    if not fm_text:
        return {}, None  # 空 frontmatter

    fm = {}
    current_key = None

    for line in fm_text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue

        # 列表项续行（如 tags: 下面的 - item）
        if stripped.startswith("- "):
            if current_key:
                if current_key not in fm or not isinstance(fm[current_key], list):
                    fm[current_key] = []
                fm[current_key].append(stripped[2:].strip())
            continue

        # key: value 行
        match = re.match(r'^(\w[\w]*)\s*:\s*(.*)', stripped)
        if match:
            key = match.group(1)
            value = match.group(2).strip()

            # 去掉首尾引号
            if len(value) >= 2:
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]

            fm[key] = value
            current_key = key if value == "" else None
        else:
            current_key = None

    return fm, None


# ── Validation ───────────────────────────────────────────────────

def validate_file(filepath: Path) -> tuple[list[str], list[str]]:
    """校验单个 wiki 文件。

    Returns:
        (errors, warnings) — 两个字符串列表
    """
    errors = []
    warnings = []

    fm, err = parse_frontmatter(filepath)
    if err:
        errors.append(err)
        return errors, warnings

    if fm is None:
        errors.append("frontmatter 解析失败")
        return errors, warnings

    # ── 必填字段校验 ──

    page_type = fm.get("type", "")
    if not page_type:
        errors.append("缺少必填字段 'type'")
    elif page_type not in VALID_TYPES:
        errors.append(
            f"type 值 '{page_type}' 无效，合法值: {', '.join(sorted(VALID_TYPES))}"
        )

    title = fm.get("title", "")
    if not title:
        errors.append("缺少必填字段 'title' 或 title 为空")

    if page_type == "素材":
        subtype = fm.get("subtype", "")
        valid_sub = VALID_SUBTYPES.get("素材", set())
        if not subtype:
            errors.append("素材类型缺少必填字段 'subtype'")
        elif subtype not in valid_sub:
            errors.append(
                f"subtype 值 '{subtype}' 无效，合法值: {', '.join(sorted(valid_sub))}"
            )

    # ── 目录一致性警告 ──

    try:
        relative = filepath.relative_to(WIKI_DIR)
        parts = relative.parts
        if len(parts) >= 2:
            dir_name = parts[0]
            expected = CONTENT_DIRS.get(dir_name)
            if expected and page_type and page_type != expected:
                warnings.append(
                    f"type='{page_type}' 与目录不匹配（{dir_name}/ 目录下应为 type='{expected}'）"
                )
    except ValueError:
        pass  # 不在 wiki/ 下的文件，跳过目录检查

    # ── 命名规范警告 ──

    stem = filepath.stem

    if page_type == "素材":
        if "-" in stem:
            warnings.append(
                f"素材文件名 '{stem}' 含连字符，素材应用本名命名（如 '苏轼'）"
            )

    elif page_type == "主题":
        char_count = len(stem)
        if char_count < 4 or char_count > 6:
            warnings.append(
                f"主题名 '{stem}' 长度为 {char_count} 字，规范为四至六字"
            )

    elif page_type == "范文":
        # 范文格式: 来源-标题，若有连字符则为正常格式
        # 无连字符也不算错，只是单独标题
        pass

    return errors, warnings


# ── Main ─────────────────────────────────────────────────────────

def main():
    # 确保 Windows 控制台能正常输出中文
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    wiki_path = WIKI_DIR.resolve()
    if not wiki_path.exists():
        print(f"[ERROR] Wiki 目录不存在: {wiki_path}")
        sys.exit(1)

    total_errors = 0
    total_warnings = 0
    file_count = 0

    for root, dirs, files in os.walk(wiki_path):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            if fname == "index.md":
                continue

            filepath = Path(root) / fname
            relative = filepath.relative_to(wiki_path.parent)

            # 只校验内容子目录下的文件（跳过 wiki 根目录的系统文件如 log.md）
            try:
                rel_to_wiki = filepath.relative_to(wiki_path)
                if len(rel_to_wiki.parts) < 2:
                    continue  # 跳过 wiki/ 根目录下的文件
            except ValueError:
                continue

            file_count += 1
            errors, warnings = validate_file(filepath)

            if errors:
                total_errors += len(errors)
                print(f"\n[FAIL] {relative}")
                for e in errors:
                    print(f"  ❌ {e}")
                for w in warnings:
                    print(f"  ⚠️  {w}")
                    total_warnings += 1
            elif warnings:
                total_warnings += len(warnings)
                print(f"\n[WARN] {relative}")
                for w in warnings:
                    print(f"  ⚠️  {w}")
            else:
                print(f"[OK]   {relative}")

    # ── 汇总 ──
    print(f"\n{'=' * 50}")
    print(f"扫描文件: {file_count}")
    print(f"错误: {total_errors}")
    print(f"警告: {total_warnings}")

    if total_errors > 0:
        print(f"\n❌ 校验未通过，存在 {total_errors} 个错误")
        sys.exit(1)
    else:
        if total_warnings > 0:
            print(f"\n✅ 校验通过（有 {total_warnings} 个警告）")
        else:
            print("\n✅ 所有文件 frontmatter 校验通过")
        sys.exit(0)


if __name__ == "__main__":
    main()
