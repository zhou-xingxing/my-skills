#!/usr/bin/env python3
"""
Markdown 文件统计脚本
读取指定路径的 markdown 文件，输出字符数和预估阅读时间
"""

import sys
import re
import argparse
from pathlib import Path


# 阅读类型配置
READING_TYPES = {
    "tech": {
        "name": "技术文档",
        "wpm": 200,
        "description": "适合需要深入理解的技术类文章"
    },
    "normal": {
        "name": "普通阅读",
        "wpm": 350,
        "description": "适合一般性的文章阅读"
    },
    "skim": {
        "name": "快速浏览",
        "wpm": 550,
        "description": "适合快速了解大意"
    }
}


def extract_text(content: str) -> str:
    """提取纯文本（去除 markdown 标记）"""
    # 移除代码块标记（```language），但保留内容
    text = re.sub(r'^```[\w]*\n', '', content, flags=re.MULTILINE)
    text = re.sub(r'\n?```\s*$', '', text, flags=re.MULTILINE)
    # 移除行内代码标记（`），但保留内容
    text = re.sub(r'`([^`]*)`', r'\1', text)

    # 移除图片
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', text)
    # 移除链接，保留链接文字
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # 移除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    # 移除 markdown 标题、列表等标记
    text = re.sub(r'^[#\-\*\+>]+\s*', '', text, flags=re.MULTILINE)
    # 移除粗体、斜体标记
    text = re.sub(r'\*\*?|__?', '', text)

    return text


def count_cjk_chars(text: str) -> int:
    """
    统计 CJK (中日韩) 统一表意文字数量
    范围: \u4e00-\u9fff (基本汉字), \u3400-\u4dbf (扩展A), 等
    """
    cjk_pattern = re.compile(
        r'['
        r'\u4e00-\u9fff'
        r'\u3400-\u4dbf'
        r'\U00020000-\U0002a6df'
        r'\U0002a700-\U0002b73f'
        r'\U0002b740-\U0002b81f'
        r']',
        re.UNICODE
    )
    return len(cjk_pattern.findall(text))


def count_english_words(text: str) -> int:
    """
    统计英文单词数量
    规则：连续的 [a-zA-Z] 字符算一个单词
    """
    word_pattern = re.compile(r'[a-zA-Z]+')
    return len(word_pattern.findall(text))


def count_reading_units(content: str) -> dict:
    """
    按阅读单位统计：
    - 1 个中文汉字 = 1 单位
    - 1 个英文单词 = 1 单位
    """
    # 提取纯文本（去除 markdown 标记）
    text = extract_text(content)

    # 中文字数（每个汉字算 1 单位）
    chinese = count_cjk_chars(text)

    # 英文单词数（每个单词算 1 单位）
    english_words = count_english_words(text)

    # 总阅读单位
    total = chinese + english_words

    return {
        "chinese": chinese,           # 中文字数
        "english_words": english_words,  # 英文单词数
        "total": total,               # 总阅读单位
    }


def estimate_reading_time(total_units: int, wpm: int = 200) -> dict:
    """
    预估阅读时间
    :param total_units: 总阅读单位（中文字数 + 英文单词数）
    :param wpm: 每分钟阅读单位数（默认 200 个/分钟，适合技术文档）
    :return: 包含分钟和秒的字典

    阅读速度参考：
    - 快速浏览: 500-600 个/分钟
    - 普通阅读: 300-400 个/分钟
    - 技术文档: 150-200 个/分钟
    """
    minutes = total_units / wpm
    total_seconds = int(minutes * 60)

    return {
        "minutes": total_seconds // 60,
        "seconds": total_seconds % 60,
        "total_seconds": total_seconds,
    }


def analyze_markdown(file_path: str, reading_type: str = "tech") -> dict:
    """分析 markdown 文件

    Args:
        file_path: Markdown 文件路径
        reading_type: 阅读类型，可选 tech/normal/skim
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    if not path.is_file():
        raise ValueError(f"路径不是文件: {file_path}")

    content = path.read_text(encoding='utf-8')

    # 原始字符数
    raw_chars = len(content)
    # 阅读单位统计（中文字数 + 英文单词数）
    reading_units = count_reading_units(content)
    # 行数
    lines = content.count('\n') + 1

    # 获取阅读速度
    wpm = READING_TYPES.get(reading_type, READING_TYPES["tech"])["wpm"]

    # 预估阅读时间
    reading_time = estimate_reading_time(reading_units["total"], wpm)

    return {
        "file_path": str(path.absolute()),
        "file_name": path.name,
        "raw_chars": raw_chars,
        "reading_units": reading_units,
        "lines": lines,
        "reading_time": reading_time,
        "reading_type": reading_type,
        "wpm": wpm
    }


def format_output(stats: dict) -> str:
    """格式化输出"""
    units = stats['reading_units']
    rt = stats['reading_time']
    reading_type_name = READING_TYPES.get(stats['reading_type'], READING_TYPES['tech'])['name']

    lines = [
        f"📄 文件: {stats['file_name']}",
        f"📁 路径: {stats['file_path']}",
        "",
        f"📖 阅读类型: {reading_type_name}（{stats['wpm']} 字/分钟）",
        "",
        "📊 统计信息:",
        f"  • 总行数: {stats['lines']:,} 行",
        f"  • 原始字符: {stats['raw_chars']:,} 个",
        "",
        "📝 阅读单位统计（1 汉字 = 1 英文单词 = 1 单位）:",
        f"  • 中文字数: {units['chinese']:,} 字",
        f"  • 英文单词: {units['english_words']:,} 个",
        f"  • 总阅读单位: {units['total']:,} 个",
        "",
        f"⏱️ 预估阅读时间（{reading_type_name}速度）:",
        f"  • {rt['minutes']} 分 {rt['seconds']} 秒",
        f"  • 约 {rt['total_seconds'] // 60 + (1 if rt['seconds'] > 30 else 0)} 分钟",
    ]
    return "\n".join(lines)


def format_reading_time(stats: dict) -> str:
    """格式化阅读时间为简洁字符串"""
    rt = stats['reading_time']
    if rt['total_seconds'] < 60:
        return "< 1 分钟"
    elif rt['seconds'] > 30:
        return f"约 {rt['minutes'] + 1} 分钟"
    else:
        return f"约 {rt['minutes']} 分钟"


def insert_stats_banner(content: str, stats: dict) -> str:
    """
    在文件头部插入阅读统计信息提示框

    格式:
    > [!TIP]
    >
    > *<small>本文约 X 字，预估阅读时间 Y 分钟。</small>*

    Args:
        content: 原始文件内容
        stats: 统计信息字典

    Returns:
        更新后的内容
    """
    units = stats['reading_units']
    reading_time_str = format_reading_time(stats)

    # 构建提示框
    banner = f"> [!TIP]\n>\n> *<small>本文约 {units['total']} 字，预估阅读时间 {reading_time_str}。</small>*\n\n"

    # 检查是否已存在统计提示框（可能在文件开头或 frontmatter 之后）
    existing_banner_pattern = r'> \[!TIP\]\n>\n> \*<small>.*?</small>\*\n\n'
    if re.search(existing_banner_pattern, content):
        # 替换现有的提示框
        new_content = re.sub(existing_banner_pattern, banner, content, count=1)
        return new_content

    # 检查是否有 frontmatter
    frontmatter_match = re.match(r'^(---\s*\n.*?---\s*\n)', content, re.DOTALL)
    if frontmatter_match:
        # 在 frontmatter 后插入提示框
        end_pos = frontmatter_match.end()
        new_content = content[:end_pos] + '\n' + banner + content[end_pos:]
        return new_content

    # 在文件开头插入提示框
    return banner + content


def insert_stats_to_file(file_path: str, reading_type: str = "tech", dry_run: bool = False) -> dict:
    """
    分析 markdown 文件并将统计信息插入到文件头部

    Args:
        file_path: Markdown 文件路径
        reading_type: 阅读类型，可选 tech/normal/skim
        dry_run: 如果为 True，则不实际修改文件，只返回统计信息

    Returns:
        统计信息字典
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    content = path.read_text(encoding='utf-8')
    stats = analyze_markdown(file_path, reading_type)

    if not dry_run:
        updated_content = insert_stats_banner(content, stats)
        path.write_text(updated_content, encoding='utf-8')

    return stats


def main():
    # 构建阅读类型帮助文本
    type_help = "阅读类型，可选:"
    for key, value in READING_TYPES.items():
        type_help += f"\n    {key} - {value['name']}({value['wpm']}字/分钟) - {value['description']}"

    parser = argparse.ArgumentParser(
        description="Markdown 文件统计工具 - 统计字符数和预估阅读时间",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  python scripts/markdown_stats.py article.md
  python scripts/markdown_stats.py article.md --type normal
  python scripts/markdown_stats.py article.md --insert --type skim

阅读类型说明:
  tech   - 技术文档(200字/分钟) - 适合需要深入理解的技术类文章
  normal - 普通阅读(350字/分钟) - 适合一般性的文章阅读
  skim   - 快速浏览(550字/分钟) - 适合快速了解大意
        """
    )

    parser.add_argument("file", help="Markdown 文件路径")
    parser.add_argument(
        "--insert", "-i",
        action="store_true",
        help="将统计信息以提示框格式插入到文件头部"
    )
    parser.add_argument(
        "--type", "-t",
        choices=list(READING_TYPES.keys()),
        default="tech",
        help="阅读类型 (默认: tech)"
    )

    args = parser.parse_args()

    try:
        if args.insert:
            stats = insert_stats_to_file(args.file, args.type, dry_run=False)
            print(format_output(stats))
            print("\n✅ 已更新文件，添加了阅读统计提示框")
        else:
            stats = analyze_markdown(args.file, args.type)
            print(format_output(stats))
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
