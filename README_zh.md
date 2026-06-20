# Resume Factory（简历工厂）

[阅读英文版 README](README.md)

Resume Factory 是一个同时支持 Codex 和 Claude Code 的 Agent Skill，用于生成经过视觉验收的单页 LaTeX 简历。项目内含 10 套风格、对应效果图以及可重复的编译和排版检查工具。用户提供的每项正文内容都必须保留；写不下时优先缩小字号并调整排版，不得删减或编造内容。

## 安装 Skill

请将整个项目目录移动或复制到对应 Agent 的个人 Skill 目录中。操作后必须同时保留 `SKILL.md`、`templates/`、`examples/` 和 `scripts/`。

### Codex

在终端中打开下载好的 `resume-factory` 项目目录，然后在当前目录执行：

```bash
mkdir -p "$HOME/.codex/skills"
cd ..
mv "$PWD/resume-factory" "$HOME/.codex/skills/resume-factory"
```

### Claude Code

在终端中打开下载好的 `resume-factory` 项目目录，然后在当前目录执行：

```bash
mkdir -p "$HOME/.claude/skills"
cd ..
mv "$PWD/resume-factory" "$HOME/.claude/skills/resume-factory"
```

详见 [Claude Code Skills 官方文档](https://code.claude.com/docs/en/skills#where-skills-live)。

如果安装后未识别到 Skill，请重启对应 Agent。安装完成后，无需再将本项目作为工作目录打开。

## 准备工作目录

在任意工作目录中打开 Codex 或 Claude Code，然后执行：

```bash
mkdir -p inputs
mkdir -p outputs
```

将一张清晰头像放入 `inputs/`，支持 `.jpg`、`.jpeg` 和 `.png`，Resume Factory 会自动发现它。如果使用已有简历，还需将源 `.pdf` 或 `.md` 文件放入 `inputs/`。生成的 `.tex` 和 `.pdf` 将写入 `outputs/`。

如果 `inputs/` 中有多张头像，Agent 会询问使用哪一张。提示词中无需再填写头像路径或任何排版要求。

## 初次使用

Resume Factory 需要 Python 3.8 或更高版本、PyMuPDF、XeLaTeX、`geometry`、`xcolor`、`tikz`、`fontspec`、`xeCJK`、`graphicx`、`fontawesome5` 宏包，以及 TeX Gyre 和 Fandol OpenType 字体。请按照以下方法进行安装，不同操作系统的安装方式不同。

### macOS

在已安装的 Skill 目录中执行：

```bash
pip install -r requirements.txt
brew install --cask mactex-no-gui
eval "$(/usr/libexec/path_helper)"
```

上述命令会安装完整的命令行版 MacTeX。如果还需要 TeXShop 等图形应用，请将安装命令替换为 `brew install --cask mactex`。

### Linux

Ubuntu 或 Debian：

```bash
pip install -r requirements.txt
sudo apt update
sudo apt install -y texlive-full
```

Fedora 或 RHEL 系发行版：

```bash
pip install -r requirements.txt
sudo dnf install -y texlive-scheme-full
```

Arch Linux 或 Manjaro：

```bash
pip install -r requirements.txt
sudo pacman -Syu --needed texlive-meta
```

### Windows

在已安装的 Skill 目录中使用 PowerShell 或命令提示符执行：

```powershell
pip install -r requirements.txt
```

然后下载并运行官方 [TeX Live Windows 安装程序](https://mirror.ctan.org/systems/texlive/tlnet/install-tl-windows.exe)。打开 `Advanced`，选择 `full scheme (everything)`，完成安装后重新打开终端，使新的 `PATH` 生效。

任意系统安装完成后均可执行以下命令验证：

```bash
xelatex --version
kpsewhich geometry.sty
kpsewhich fontawesome5.sty
kpsewhich texgyreheros-regular.otf
kpsewhich FandolHei-Regular.otf
```

## 快速使用

### 用法 1：直接提供简历信息

```text
请调用resume-factory这个SKILL，按照以下配置帮我生成简历：
- 参考Style ID：resume_template_5
- 目标语言：中文
- 输出文件基础名（不含后缀）：zhangwei_resume
- 简历具体信息：[在此粘贴全部简历内容]
```

### 用法 2：使用已有简历作为参考(支持pdf、md)

```text
请调用resume-factory这个SKILL，按照以下配置帮我生成简历：
- 参考Style ID：resume_template_3
- 目标语言：中文
- 输入文件名：zhangwei_resume.pdf（或zhangwei_resume.md）
- 输出文件基础名（不含后缀）：zhangwei_restyled
```

不需要在提示词中增加其他要求。正文一致性、单页排版、模板字体保留、编译、检查和清理均由 `SKILL.md` 和脚本强制执行。

## 风格目录

| Style ID | 风格 | 效果图 |
| --- | --- | --- |
| `resume_template_1` | 极简黑白 UI/UX | <img src="examples/resume_template_1.png" alt="风格 1" width="120"> |
| `resume_template_2` | 国风水墨文化 | <img src="examples/resume_template_2.png" alt="风格 2" width="120"> |
| `resume_template_3` | 赛博朋克开发者仪表盘 | <img src="examples/resume_template_3.png" alt="风格 3" width="120"> |
| `resume_template_4` | 马卡龙新拟物 UI/UX | <img src="examples/resume_template_4.png" alt="风格 4" width="120"> |
| `resume_template_5` | 商务蓝侧栏 | <img src="examples/resume_template_5.png" alt="风格 5" width="120"> |
| `resume_template_6` | 包豪斯强视觉创意 | <img src="examples/resume_template_6.png" alt="风格 6" width="120"> |
| `resume_template_7` | 法式新古典优雅 | <img src="examples/resume_template_7.png" alt="风格 7" width="120"> |
| `resume_template_8` | 手帐拼贴 UI/UX | <img src="examples/resume_template_8.png" alt="风格 8" width="120"> |
| `resume_template_9` | 全息 Web3 玻璃拟态 | <img src="examples/resume_template_9.png" alt="风格 9" width="120"> |
| `resume_template_10` | 植物水彩心理咨询 | <img src="examples/resume_template_10.png" alt="风格 10" width="120"> |

## 项目结构

```text
resume-factory/
├── examples/                 # 10 套渲染效果图
├── scripts/
│   ├── adjust_resume.py      # 调整生成文件的排版控制项
│   ├── check_resume.py       # 检查 PDF 排版与头像位置
│   └── compile_resume.py     # 编译、验收与清理
├── templates/                # 10 套 LaTeX 源模板
├── LICENSE
├── README.md
├── README_zh.md
├── requirements.txt
└── SKILL.md
```

项目中不包含 `inputs/` 或 `outputs/`；这两个目录属于用户自己的工作目录。

## 验收工具

Skill 会使用安装目录下的绝对脚本路径，同时保持用户工作目录为当前目录。手动调用示例：

```bash
python3 "$HOME/.codex/skills/resume-factory/scripts/compile_resume.py" \
  outputs/zhangwei_resume.tex \
  --template "$HOME/.codex/skills/resume-factory/templates/resume_template_5.tex" \
  --portrait inputs/zhangwei_portrait.jpg \
  --render-preview outputs/zhangwei_resume_preview.png
```

Claude Code 用户将 Skill 根目录替换为 `$HOME/.claude/skills/resume-factory` 即可。编译脚本会先确认生成文件的字体声明与所选模板完全一致，再运行两遍 XeLaTeX，检查页数、字号、密度、页面边界、文字碰撞和头像位置，并清理中间文件。默认情况下，版式问题只作为诊断信息：即使检查报错，最终 `.tex` 和 `.pdf` 也会保留。`SKILL.md` 还要求继续优化排版，并在交付前完成正文逐项对照和效果图目视检查。

## 许可证

本项目使用 [MIT License](LICENSE)。
