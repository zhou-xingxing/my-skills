# My Skills

这里存放我创建的 Agent Skills。

[Agent Skills 定义](https://agentskills.io/home)

## Skills 列表

### markdown-stats

为 Markdown 文件统计字符数和预估阅读时间，支持三种阅读类型（技术文档、普通阅读、快速浏览），并将统计信息以提示框格式插入文件头部。

## 安装方法
### Claude Code

以安装 `markdown-stats` skill 为例：

```bash
# 1. 克隆仓库到本地（示例路径：~/projects/my-skills）
git clone https://github.com/zhou-xingxing/my-skills ~/projects/my-skills
cd ~/projects/my-skills

# 2. 复制 skill 目录到 Claude Code skills 目录
mkdir -p ~/.claude/skills
cp -r ~/projects/my-skills/markdown-stats ~/.claude/skills/

# 3. 重启 Claude Code
```

**说明：**
- 你可以将 `~/projects/my-skills` 替换为你想要的任何路径
- Skills 目录位置：macOS/Linux 是 `~/.claude/skills/`，Windows 是 `%LOCALAPPDATA%\Claude\skills\`
- 复制完成后需要重启 Claude Code 才能加载新 skill

### OpenCode

以安装 `markdown-stats` skill 为例：

```bash
# 1. 克隆仓库到本地（示例路径：~/projects/my-skills）
git clone https://github.com/zhou-xingxing/my-skills ~/projects/my-skills
cd ~/projects/my-skills

# 2. 复制 skill 目录到 OpenCode skills 目录
mkdir -p ~/.opencode/skills
cp -r ~/projects/my-skills/markdown-stats ~/.opencode/skills/

# 3. 重启 OpenCode
```

**说明：**
- Skills 目录位置：macOS/Linux 是 `~/.opencode/skills/`，Windows 是 `%LOCALAPPDATA%\OpenCode\skills\`
- 你也可以直接将仓库链接 `https://github.com/zhou-xingxing/my-skills` 发送给 OpenCode，告诉它你想安装的 skill

### OpenClaw
直接把仓库链接 `https://github.com/zhou-xingxing/my-skills` 发给它，告诉它你想安装的 skill
