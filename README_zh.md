# Resume Factory（简历工厂）

[阅读英文版 README](README.md)

Resume Factory 是一个面向用户的 Codex Skill 项目，用于根据已核实的个人信息和用户提供的头像生成经过视觉验收的 LaTeX 简历。项目提供 10 套视觉模板及对应预览图，以及用于受控调整排版、XeLaTeX 编译、PDF 检查和中间文件清理的 Python 工具。

本项目支持两种输入方式：在一条提示词中直接提供详细资料，或使用存放在 `inputs/` 下的现有简历。所有生成的简历必须存放在 `outputs/` 下。

## 目录结构

```text
RESUME FACTORY/
├── examples/                 # 10 种风格的渲染预览图
├── inputs/                   # 必需的头像与可选的源简历
├── outputs/                  # 生成的 .tex 和 .pdf 文件
├── scripts/
│   ├── adjust_resume.py      # 受控调整生成文件的排版
│   ├── check_resume.py       # PDF 几何与头像检查
│   └── compile_resume.py     # XeLaTeX 编译、验收与清理
├── templates/                # 10 个 LaTeX 源模板
├── README.md
├── README_zh.md
├── requirements.txt          # Python 排版检查依赖
└── SKILL.md                  # AI 编码智能体加载的操作说明
```

生成简历时不要直接修改源模板。应将模板结构复制到 `outputs/` 下的新 `.tex` 文件中，并且只替换示例简历内容。

## 风格目录

| 风格 ID | 中文风格名称 | 示例 | 模板 | 适用场景与视觉特征 |
| --- | --- | --- | --- | --- |
| `resume_template_1` | 极简黑白 UI/UX 简历 | `examples/resume_template_1.png`<br><img src="examples/resume_template_1.png" alt="模板 1 预览" width="120"> | `templates/resume_template_1.tex` | 适合 UI/UX 与产品设计岗位；使用克制的黑白配色、清晰的信息层级和少量装饰。 |
| `resume_template_2` | 国风水墨文化简历 | `examples/resume_template_2.png`<br><img src="examples/resume_template_2.png" alt="模板 2 预览" width="120"> | `templates/resume_template_2.tex` | 适合文化、教育、写作和传统文化相关岗位；采用水墨审美与编辑式构图。 |
| `resume_template_3` | 赛博朋克开发者仪表盘简历 | `examples/resume_template_3.png`<br><img src="examples/resume_template_3.png" alt="模板 3 预览" width="120"> | `templates/resume_template_3.tex` | 适合软件工程、数据和技术岗位；采用仪表盘结构、高对比度与赛博朋克视觉点缀。 |
| `resume_template_4` | 马卡龙新拟物 UI/UX 简历 | `examples/resume_template_4.png`<br><img src="examples/resume_template_4.png" alt="模板 4 预览" width="120"> | `templates/resume_template_4.tex` | 适合 UI/UX 与数字产品岗位；使用柔和的马卡龙配色、圆角模块和新拟物层次。 |
| `resume_template_5` | 商务蓝侧栏产品经理简历 | `examples/resume_template_5.png`<br><img src="examples/resume_template_5.png" alt="模板 5 预览" width="120"> | `templates/resume_template_5.tex` | 适合产品管理、运营、咨询和企业岗位；采用结构化蓝色侧栏与稳健的信息层级。 |
| `resume_template_6` | 包豪斯强视觉创意简历 | `examples/resume_template_6.png`<br><img src="examples/resume_template_6.png" alt="模板 6 预览" width="120"> | `templates/resume_template_6.tex` | 适合品牌、视觉设计、广告和创意岗位；使用几何形状、强色块与醒目字体。 |
| `resume_template_7` | 法式新古典优雅简历 | `examples/resume_template_7.png`<br><img src="examples/resume_template_7.png" alt="模板 7 预览" width="120"> | `templates/resume_template_7.tex` | 适合奢侈品、时尚、酒店及高级客户岗位；采用精致留白、古典细节与优雅语调。 |
| `resume_template_8` | 手帐拼贴 UI/UX 简历 | `examples/resume_template_8.png`<br><img src="examples/resume_template_8.png" alt="模板 8 预览" width="120"> | `templates/resume_template_8.tex` | 适合 UI/UX、插画和作品集导向岗位；使用分层拼贴元素与轻松的编辑节奏。 |
| `resume_template_9` | 全息 Web3 玻璃拟态简历 | `examples/resume_template_9.png`<br><img src="examples/resume_template_9.png" alt="模板 9 预览" width="120"> | `templates/resume_template_9.tex` | 适合 Web3、新兴技术、数字艺术和创新岗位；采用全息渐变、半透明面板与玻璃拟态。 |
| `resume_template_10` | 植物水彩心理咨询简历 | `examples/resume_template_10.png`<br><img src="examples/resume_template_10.png" alt="模板 10 预览" width="120"> | `templates/resume_template_10.tex` | 适合心理、咨询、健康、教育和照护岗位；使用植物水彩细节与平和亲切的构图。 |

## 环境要求

- 能够读取和编辑本仓库的 Codex 或其他 AI 编码智能体。
- Python 3.8 或更高版本。
- 用于检查 PDF 几何信息和嵌入图片的 PyMuPDF。
- 提供 `xelatex` 的 TeX 发行版，以及模板使用的 `geometry`、`xcolor`、`tikz`、`fontspec`、`xeCJK`、`graphicx`、`fontawesome5` 宏包。
- `TeX Gyre Heros` 和 `Noto Sans CJK SC` 字体；如果本机没有这些字体，应仅在生成的输出文件中有意识地替换字体。

生成前检查本地工具：

```bash
python3 --version
xelatex --version
```

安装 Python 依赖：

```bash
python3 -m pip install -r requirements.txt
```

使用任一种生成模式前，都必须提前将清晰头像以 `.jpg`、`.jpeg` 或 `.png` 格式放入 `inputs/`，并在提示词中写明准确路径。头像必须嵌入简历，不能变形，也不能接触简历文字。

## 用法一：手动输入详细经历生成简历

当已有简历事实但没有源简历文件时，使用此模式。此模式要求提供详细资料；请尽量包含：

- 目标语言；
- 风格 ID；
- 输出文件基础名；
- `inputs/` 下头像图片的准确路径；
- 姓名与目标岗位；
- 联系方式；
- 个人简介；
- 教育经历；
- 工作经历；
- 项目经历；
- 技能；
- 奖项与证书；
- 语言能力；
- 链接；
- 单页、ATS 侧重、措辞稳健或双语内容等限制条件。

智能体必须确认指定头像确实存在；如果缺少的信息会导致编造事实，必须先向用户询问澄清。

### 单条提示词示例

复制并修改以下一条提示词即可：

```text
请调用当前仓库中的 Resume Factory Skill 生成我的简历。

- 风格 ID：resume_template_5
- 目标语言：中文
- 输出文件基础名：zhangwei_resume
- 头像图片：inputs/zhangwei_portrait.jpg
- 保留 resume_template_5 的视觉风格，头像不得变形或接触文字。
- 生成 outputs/zhangwei_resume.tex 和 outputs/zhangwei_resume.pdf，并按 SKILL.md 完成 XeLaTeX 编译、单页排版验收、目视检查和清理。
- 措辞简洁稳健；在不破坏所选设计的前提下，突出适合 ATS 检索的产品管理关键词。
- 仅使用以下资料，以中文撰写，不得编造缺失信息；必要信息不明确时先询问我。

简历资料：
- 姓名：张伟
- 目标岗位：高级产品经理
- 所在地：中国上海
- 电话：+86 138 0000 0000
- 邮箱：zhangwei@example.com
- LinkedIn：https://www.linkedin.com/in/zhang-wei-example
- 个人简介：专注 B2B SaaS 工作流产品与跨职能交付的产品经理。
- 教育经历：
  - 示例大学，信息系统学士，2014 年 9 月至 2018 年 6 月
- 工作经历：
  - 示例云科技有限公司，产品经理，2021 年 7 月至今
    - 负责 B2B SaaS 产品的工作流与权限功能。
    - 协调研发、设计、销售与客户成功团队。
    - 已核实指标：工作流改版后，配置时长中位数从 40 分钟降至 25 分钟。
  - 示例软件有限公司，助理产品经理，2018 年 7 月至 2021 年 6 月
    - 开展客户访谈并维护季度路线图。
- 项目经历：
  - 企业审批工作流改版，2023 年
    - 定义需求、发布阶段与采用情况监测方案。
- 技能：产品发现、路线图规划、SQL、数据分析、Figma、利益相关方管理
- 证书：无
- 奖项：无
- 语言：普通话（母语）、英语（工作熟练）
- 其他链接：无

最终只返回 .tex 和 .pdf 文件路径。
```

## 用法二：从 `inputs/` 中的现有简历文件生成简历

将源简历和单独的头像文件放入 `inputs/`。源简历支持以下文件类型：

- `.pdf`
- `.md`
- `.markdown`
- `.txt`

头像支持 `.jpg`、`.jpeg` 和 `.png`。即使源简历中已经包含照片，也必须单独提供原始头像文件，以便可靠检查头像位置。

提示词中应优先写明确切文件名。如果目录中有多个文件，请明确指定智能体必须使用哪个源简历和哪张头像。智能体可以为了表达清楚、简洁、目标语言一致和适配版式而改写文字，但必须保持事实准确，不得编造缺失信息。如果 PDF 提取失败或源文件无法读取，智能体必须清楚报告问题，不得猜测。

### 单条提示词示例

```text
请调用当前仓库中的 Resume Factory Skill 重新设计简历。

- 源文件：inputs/zhangwei_existing_resume.pdf
- 头像图片：inputs/zhangwei_portrait.png
- 风格 ID：resume_template_3
- 目标语言：中文
- 输出文件基础名：zhangwei_developer_resume
- 仅将源文件作为简历资料使用；可以为清晰和版式适配而改写，但不得编造缺失信息。文件无法读取或事实存在歧义时请说明。
- 使用中文，保留 resume_template_3 的视觉风格，头像不得变形或接触文字。
- 生成 outputs/zhangwei_developer_resume.tex 和 outputs/zhangwei_developer_resume.pdf，并按 SKILL.md 完成 XeLaTeX 编译、单页排版验收、目视检查和清理。

最终只返回 .tex 和 .pdf 文件路径。
```

## 编译、检查、调整与清理

对于已经生成在 `outputs/` 下的文件，运行：

```bash
python3 scripts/compile_resume.py outputs/zhangwei_resume.tex \
  --portrait inputs/zhangwei_portrait.jpg \
  --render-preview /tmp/zhangwei_resume_preview.png
```

也可以显式指定输出目录：

```bash
python3 scripts/compile_resume.py outputs/zhangwei_resume.tex \
  --portrait inputs/zhangwei_portrait.jpg \
  --output-dir outputs
```

辅助脚本会在隔离的临时构建目录中运行两遍 XeLaTeX，并拒绝不符合单页、底部留白、字号、文字密度、碰撞、页面安全区或头像要求的结果。PDF 只有通过验收后才会复制到指定输出目录；脚本会保留最终 `.tex` 并删除当前任务的中间文件。如果输出目录中已存在另一个同名但不同的 `.tex` 文件，脚本会拒绝覆盖。

排查现有 PDF 时，可以单独运行检查脚本：

```bash
python3 scripts/check_resume.py outputs/zhangwei_resume.pdf \
  --portrait inputs/zhangwei_portrait.jpg \
  --render-preview /tmp/zhangwei_resume_preview.png
```

每个生成的 `.tex` 文件都必须定义并实际使用 `SKILL.md` 规定的标准控制项。无需改动源模板即可调整这些参数：

```bash
python3 scripts/adjust_resume.py outputs/zhangwei_resume.tex \
  --section-gap 4.5pt \
  --line-stretch 1.02 \
  --bottom-inset 7mm \
  --portrait-width 28mm \
  --portrait-y-shift 1mm
```

每次调整后必须重新编译。适当增大章节间距或行距可以减少底部留白；精简低优先级表述或减小间距可以缓解拥挤；头像宽度和偏移量用于建立头像与文字之间的安全距离。不得为了填满页面而编造内容。

当输出基础名为 `zhangwei_resume` 时，最终应仅保留以下简历文件：

```text
outputs/zhangwei_resume.tex
outputs/zhangwei_resume.pdf
```

成功构建后，不得残留 `.aux`、`.log`、`.out`、`.toc`、`.fls`、`.fdb_latexmk`、`.synctex.gz` 等中间文件。不要把最终简历存放在仓库根目录或 `templates/` 下。

自动检查只能提供可量化的保护，不能完整判断审美质量。AI 编码智能体必须在交付前目视检查渲染出的 PNG，确认间距均衡、层级清楚、头像未变形，并且没有视觉碰撞。

## 语言与事实准确性

- 如果用户需要中文简历，最终简历必须使用中文。
- 如果用户需要英文简历，最终简历必须使用英文。
- 除非用户明确要求双语内容，否则不要混用语言。专有名词可以保留其通行的标准写法。
- 不得编造学历、公司、职位、日期、指标、奖项、证书、项目、链接或其他事实。
- 如果所提供的信息不足或存在重要歧义，应向用户询问澄清。
- 在进行简洁的编辑性改写时，必须保留源简历中的事实。

## 常见问题

### 找不到 `xelatex`

安装包含 XeLaTeX 的 TeX 发行版，确保其二进制目录已加入 `PATH`，然后再次运行 `xelatex --version`。

### 缺少 LaTeX 宏包或字体

根据 XeLaTeX 输出安装缺失的宏包。安装 `TeX Gyre Heros` 与 `Noto Sans CJK SC`，或者仅在生成的输出 `.tex` 文件中替换为合适的本机字体。不要为了修复一次本机构建而修改全部源模板。

### PDF 提取失败

确认 PDF 包含可选择的文本，且没有加密，也不是纯扫描图片。可以提供基于文本的 `.md`、`.markdown` 或 `.txt` 版本，或直接补充缺失事实。不得使用猜测的文字。

### 内容超出页面

删除重复表达，优先保留与目标岗位相关的事实，并在保持可读性和所选风格的前提下谨慎调整生成文件中的排版控制项。不得为未知事实编造更短的替代内容。

### 排版检查失败

读取脚本报告的指标与错误，检查渲染预览图，并且只调整生成的 `.tex` 文件。底部留白超过 15 mm 时重新平衡章节间距；文字密度过高时精简内容；头像安全区接触文字时调整头像大小或位置。必须重新编译，直到自动检查和目视检查均通过。

### 无法识别头像

确认 `--portrait` 指定的准确 `.jpg`、`.jpeg` 或 `.png` 文件位于 `inputs/`，并且生成的 `.tex` 直接嵌入了该文件。不要替换为截图或占位图片。

## 许可证说明

本仓库目前没有 `LICENSE` 文件。公开分发前应添加合适的许可证；不能因为该文件缺失而推定已获得任何许可授权。
