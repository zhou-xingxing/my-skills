---
name: markdown-stats
description: 为 Markdown 文件统计字符数和预估阅读时间，支持三种阅读类型（技术文档、普通阅读、快速浏览），并将统计信息以提示框格式插入文件头部。用于处理需要添加阅读统计信息的 markdown 文件，支持中文（每个汉字算1单位）和英文（每个单词算1单位）的混合统计。
---

# Markdown Stats

为 Markdown 文件添加字符统计和预估阅读时间信息，支持根据文章类型选择不同的阅读速度。

## 功能

- **字符统计**：统计中文字数 + 英文单词数（去除 markdown 标记后）
- **多类型阅读时间估算**：支持技术文档、普通阅读、快速浏览三种模式
- **自动插入提示框**：将统计信息以美观的提示框格式添加到文件头部

## 阅读类型

| 类型 | 速度 | 适用场景 |
|------|------|----------|
| `tech` | 200 字/分钟 | 技术文档，需要深入理解代码和概念 |
| `normal` | 350 字/分钟 | 普通文章，一般性阅读 |
| `skim` | 550 字/分钟 | 快速浏览，了解大致内容 |

## 输出格式

统计信息将以以下格式插入到文件头部（frontmatter 之后，如果有的话）：

```markdown
> [!TIP]
>
> *<small>本文约 1500 字，预估阅读时间 8 分钟。</small>*

# 文章标题

正文内容...
```

## 使用方法

使用命令行执行脚本，脚本位置：`scripts/markdown_stats.py`

### 交互式使用流程

当用户请求统计 markdown 文件时，按以下流程执行：

**第一步：询问文章类型**

向用户展示阅读类型选项：

```
请文章类型：
1. tech   - 技术文档（200 字/分钟）- 适合需要深入理解代码和概念的技术类文章
2. normal - 普通阅读（350 字/分钟）- 适合一般性的文章阅读
3. skim   - 快速浏览（550 字/分钟）- 适合快速了解大致内容

请回复数字 1、2 或 3，或直接回复 tech/normal/skim
```

**第二步：根据用户选择执行**

| 用户输入 | 对应参数 |
|----------|----------|
| `1` 或 `tech` | `--type tech` |
| `2` 或 `normal` | `--type normal` |
| `3` 或 `skim` | `--type skim` |

**第三步：询问是否插入到文件**

询问用户："是否将统计信息插入到文件头部？(y/n)"

- 如果用户回复 `y` 或 `yes`，添加 `--insert` 参数
- 如果用户回复 `n` 或 `no`，不添加 `--insert` 参数

**执行命令示例**

根据用户的选择组合参数：

```bash
# 示例 1：用户选择技术文档(1)，并同意插入
python3 scripts/markdown_stats.py <文件路径> --type tech --insert

# 示例 2：用户选择普通阅读(2)，不插入
python3 scripts/markdown_stats.py <文件路径> --type normal

# 示例 3：用户选择快速浏览(3)，并同意插入
python3 scripts/markdown_stats.py <文件路径> --type skim --insert
```

### 完整使用示例

**场景 1：用户提供了文件路径**

```
用户：请帮我统计一下 article.md

Claude：
请选择文章类型：
1. tech   - 技术文档（200 字/分钟）- 适合需要深入理解代码和概念的技术类文章
2. normal - 普通阅读（350 字/分钟）- 适合一般性的文章阅读
3. skim   - 快速浏览（550 字/分钟）- 适合快速了解大致内容

请回复数字 1、2 或 3，或直接回复 tech/normal/skim

用户：2

Claude：
是否将统计信息插入到文件头部？(y/n)

用户：y

Claude：
[执行] python3 scripts/markdown_stats.py article.md --type normal --insert

📄 文件: article.md
📖 阅读类型: 普通阅读（350 字/分钟）
📊 统计信息: ...
✅ 已更新文件，添加了阅读统计提示框
```

**场景 2：用户请求直接插入**

```
用户：帮我把 README.md 加上阅读时间提示

Claude：
请选择文章类型：
1. tech   - 技术文档（200 字/分钟）...
2. normal - 普通阅读（350 字/分钟）...
3. skim   - 快速浏览（550 字/分钟）...

用户：1

Claude：
[执行] python3 scripts/markdown_stats.py README.md --type tech --insert
...
```

## 统计规则

| 类型 | 计算方式 |
|------|----------|
| 中文字符 | 每个汉字 = 1 单位（包括 CJK 统一表意文字） |
| 英文单词 | 每个连续英文字母序列 = 1 单位 |

### 命令行快速使用

如果你希望通过命令行直接使用而不需要交互式提问，可以使用以下参数：

```bash
# 基本用法（默认使用技术文档模式）
python3 scripts/markdown_stats.py <文件路径>

# 指定阅读类型，只展示统计结果不修改原文件
python3 scripts/markdown_stats.py <文件路径> --type tech    # 技术文档
python3 scripts/markdown_stats.py <文件路径> --type normal  # 普通阅读
python3 scripts/markdown_stats.py <文件路径> --type skim    # 快速浏览

# 指定阅读类型，并插入提示框到原文件
python3 scripts/markdown_stats.py <文件路径> --insert
python3 scripts/markdown_stats.py <文件路径> -i --type normal
```

### 查看脚本帮助

```bash
python3 scripts/markdown_stats.py --help
```
