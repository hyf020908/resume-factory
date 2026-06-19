# Resume Factory

[Read the Chinese version](README_zh.md)

Resume Factory is a user-facing Codex Skill project for producing visually validated LaTeX resumes from verified personal information and a user-supplied portrait. It provides ten visual templates, matching preview images, and Python tools for controlled layout adjustment, XeLaTeX compilation, PDF inspection, and intermediate-file cleanup.

The project supports either detailed information supplied directly in one prompt or an existing resume stored under `inputs/`. Generated resumes always belong under `outputs/`.

## Directory structure

```text
RESUME FACTORY/
├── examples/                 # Rendered previews for the ten styles
├── inputs/                   # Required portrait and optional source resume
├── outputs/                  # Generated .tex and .pdf files
├── scripts/
│   ├── adjust_resume.py      # Controlled generated-layout adjustments
│   ├── check_resume.py       # PDF geometry and portrait checks
│   └── compile_resume.py     # XeLaTeX compilation, validation, and cleanup
├── templates/                # Ten source LaTeX templates
├── README.md
├── README_zh.md
├── requirements.txt          # Python layout-check dependency
└── SKILL.md                  # Instructions loaded by an AI coding agent
```

Do not edit a source template to create a resume. Copy its structure into a new `.tex` file under `outputs/` and replace only the sample resume content.

## Style catalog

| Style ID | Style name | Example | Template | Suitable use cases and visual characteristics |
| --- | --- | --- | --- | --- |
| `resume_template_1` | Minimal Monochrome UI/UX Resume | `examples/resume_template_1.png`<br><img src="examples/resume_template_1.png" alt="Template 1 preview" width="120"> | `templates/resume_template_1.tex` | UI/UX and product design roles; restrained monochrome palette, clear hierarchy, and minimal decoration. |
| `resume_template_2` | Chinese Ink Cultural Resume | `examples/resume_template_2.png`<br><img src="examples/resume_template_2.png" alt="Template 2 preview" width="120"> | `templates/resume_template_2.tex` | Culture, education, writing, and heritage-related roles; Chinese ink aesthetics and an editorial composition. |
| `resume_template_3` | Cyberpunk Developer Dashboard Resume | `examples/resume_template_3.png`<br><img src="examples/resume_template_3.png" alt="Template 3 preview" width="120"> | `templates/resume_template_3.tex` | Software engineering, data, and technical roles; dashboard structure, high contrast, and cyberpunk accents. |
| `resume_template_4` | Pastel Neumorphism UI/UX Resume | `examples/resume_template_4.png`<br><img src="examples/resume_template_4.png" alt="Template 4 preview" width="120"> | `templates/resume_template_4.tex` | UI/UX and digital product roles; soft pastel colors, rounded modules, and neumorphic depth. |
| `resume_template_5` | Corporate Blue Sidebar Resume | `examples/resume_template_5.png`<br><img src="examples/resume_template_5.png" alt="Template 5 preview" width="120"> | `templates/resume_template_5.tex` | Product management, operations, consulting, and corporate roles; structured blue sidebar and conservative information hierarchy. |
| `resume_template_6` | Bauhaus Bold Creative Resume | `examples/resume_template_6.png`<br><img src="examples/resume_template_6.png" alt="Template 6 preview" width="120"> | `templates/resume_template_6.tex` | Branding, visual design, advertising, and creative roles; geometric forms, strong color blocks, and bold typography. |
| `resume_template_7` | French Neoclassical Luxury Resume | `examples/resume_template_7.png`<br><img src="examples/resume_template_7.png" alt="Template 7 preview" width="120"> | `templates/resume_template_7.tex` | Luxury, fashion, hospitality, and senior client-facing roles; refined spacing, classical detail, and an elegant tone. |
| `resume_template_8` | Scrapbook Collage UI/UX Resume | `examples/resume_template_8.png`<br><img src="examples/resume_template_8.png" alt="Template 8 preview" width="120"> | `templates/resume_template_8.tex` | UI/UX, illustration, and portfolio-oriented roles; layered collage elements and an informal editorial rhythm. |
| `resume_template_9` | Holographic Web3 Glassmorphism Resume | `examples/resume_template_9.png`<br><img src="examples/resume_template_9.png" alt="Template 9 preview" width="120"> | `templates/resume_template_9.tex` | Web3, emerging technology, digital art, and innovation roles; holographic gradients, translucent panels, and glassmorphism. |
| `resume_template_10` | Botanical Watercolor Psychology Resume | `examples/resume_template_10.png`<br><img src="examples/resume_template_10.png" alt="Template 10 preview" width="120"> | `templates/resume_template_10.tex` | Psychology, counseling, wellness, education, and care roles; botanical watercolor details and a calm, approachable composition. |

## Requirements

- Codex or another AI coding agent capable of reading and editing this repository.
- Python 3.8 or later.
- PyMuPDF for PDF geometry and embedded-image inspection.
- A TeX distribution that provides `xelatex` and the packages used by the templates: `geometry`, `xcolor`, `tikz`, `fontspec`, `xeCJK`, `graphicx`, and `fontawesome5`.
- The `TeX Gyre Heros` and `Noto Sans CJK SC` fonts, or deliberate substitutions in the generated output file if those fonts are unavailable.

Verify the local tools before generation:

```bash
python3 --version
xelatex --version
```

Install the Python dependency:

```bash
python3 -m pip install -r requirements.txt
```

Before either usage mode, place a clear portrait under `inputs/` in `.jpg`, `.jpeg`, or `.png` format. Use the exact portrait path in the prompt. The portrait is required and must be embedded without distortion or contact with resume text.

## Usage Mode 1: Create from detailed manual input

Use this mode when the resume facts are available but no source resume file exists. Detailed input is required. Supply, when available:

- target language;
- style ID;
- output file base name;
- exact portrait image path under `inputs/`;
- name and target role;
- contact information;
- personal summary or profile;
- education;
- work experience;
- project experience;
- skills;
- awards and certificates;
- languages;
- links;
- constraints such as one page, ATS emphasis, conservative wording, or bilingual content.

The agent must confirm that the named portrait exists and ask for clarification if missing information would otherwise require fabrication.

### One-shot prompt example

Copy and edit this single prompt:

```text
Use the Resume Factory Skill in this repository to create my resume.

- Style ID: resume_template_5
- Target language: English
- Output file base name: alex_chen_resume
- Portrait image: inputs/alex_chen_portrait.jpg
- Preserve the visual style of resume_template_5 and place the portrait without distortion or contact with text.
- Generate outputs/alex_chen_resume.tex and outputs/alex_chen_resume.pdf. Follow SKILL.md for XeLaTeX compilation, one-page layout validation, visual inspection, and cleanup.
- Use concise and conservative wording and emphasize ATS-readable product-management terms without damaging the selected design.
- Use only the facts below, write the resume in English, and do not invent missing information. Ask me if essential information is unclear.

Resume data:
- Name: Alex Chen
- Target role: Senior Product Manager
- Location: Shanghai, China
- Phone: +86 138 0000 0000
- Email: alex.chen@example.com
- LinkedIn: https://www.linkedin.com/in/alex-chen-example
- Profile: Product manager focused on B2B SaaS workflow products and cross-functional delivery.
- Education:
  - B.S. in Information Systems, Example University, September 2014–June 2018
- Work experience:
  - Product Manager, Example Cloud Co., July 2021–present
    - Owned workflow and permissions features for a B2B SaaS product.
    - Coordinated engineering, design, sales, and customer-success teams.
    - Verified metric: reduced median configuration time from 40 minutes to 25 minutes after the workflow redesign.
  - Associate Product Manager, Sample Software Ltd., July 2018–June 2021
    - Conducted customer interviews and maintained the quarterly roadmap.
- Project experience:
  - Enterprise approval workflow redesign, 2023
    - Defined requirements, rollout stages, and adoption monitoring.
- Skills: Product discovery, roadmap planning, SQL, analytics, Figma, stakeholder management
- Certificates: None
- Awards: None
- Languages: Mandarin Chinese (native), English (professional working proficiency)
- Additional links: None

Return only the final .tex and .pdf paths.
```

## Usage Mode 2: Create from a source resume in `inputs/`

Place the source resume and a separate portrait under `inputs/`. Supported source resume types are:

- `.pdf`
- `.md`
- `.markdown`
- `.txt`

Supported portrait types are `.jpg`, `.jpeg`, and `.png`. The portrait is required even when the source resume already contains a photograph; provide the original image separately so placement can be checked reliably.

Prefer naming the exact file in the prompt. If several files exist, specify which one the agent must use. The agent may rewrite wording for clarity, concision, target-language consistency, and layout fit, but it must preserve factual accuracy and must not invent missing information. If PDF extraction fails or a source is unreadable, the agent must report the problem clearly rather than guessing.

### One-shot prompt example

```text
Use the Resume Factory Skill in this repository to create a restyled resume.

- Source file: inputs/alex_chen_existing_resume.pdf
- Portrait image: inputs/alex_chen_portrait.png
- Style ID: resume_template_3
- Target language: English
- Output file base name: alex_chen_developer_resume
- Use the source only as resume data. Preserve its facts, but rewrite for clarity and fit when useful. Do not invent missing information; report unreadable or ambiguous content.
- Write the resume in English, preserve the visual style of resume_template_3, and place the portrait without distortion or contact with text.
- Generate outputs/alex_chen_developer_resume.tex and outputs/alex_chen_developer_resume.pdf. Follow SKILL.md for XeLaTeX compilation, one-page layout validation, visual inspection, and cleanup.

Return only the final .tex and .pdf paths.
```

## Compile, inspect, adjust, and clean

For a generated file already under `outputs/`, run:

```bash
python3 scripts/compile_resume.py outputs/alex_chen_resume.tex \
  --portrait inputs/alex_chen_portrait.jpg \
  --render-preview /tmp/alex_chen_resume_preview.png
```

An explicit output directory is also supported:

```bash
python3 scripts/compile_resume.py outputs/alex_chen_resume.tex \
  --portrait inputs/alex_chen_portrait.jpg \
  --output-dir outputs
```

The helper runs XeLaTeX twice in an isolated temporary build directory and rejects output that fails the one-page, bottom-margin, font-size, text-density, collision, page-edge, or portrait checks. It copies the final PDF only after validation, retains the final `.tex`, and removes job-specific intermediate files. It refuses to overwrite a different existing `.tex` file with the same name.

Run the checker independently when diagnosing an existing PDF:

```bash
python3 scripts/check_resume.py outputs/alex_chen_resume.pdf \
  --portrait inputs/alex_chen_portrait.jpg \
  --render-preview /tmp/alex_chen_resume_preview.png
```

Every generated `.tex` file must define and use the standardized controls documented in `SKILL.md`. Adjust them without touching source templates:

```bash
python3 scripts/adjust_resume.py outputs/alex_chen_resume.tex \
  --section-gap 4.5pt \
  --line-stretch 1.02 \
  --bottom-inset 7mm \
  --portrait-width 28mm \
  --portrait-y-shift 1mm
```

Recompile after every adjustment. Increasing section spacing or line stretch can reduce excessive bottom whitespace; shortening low-priority wording or reducing spacing can relieve crowding. Use portrait width and shifts to establish clear separation from text. Do not add invented content merely to fill the page.

For a base name such as `alex_chen_resume`, the only final resume artifacts should be:

```text
outputs/alex_chen_resume.tex
outputs/alex_chen_resume.pdf
```

Intermediate files such as `.aux`, `.log`, `.out`, `.toc`, `.fls`, `.fdb_latexmk`, and `.synctex.gz` must not remain after a successful build. Do not store final resumes in the repository root or under `templates/`.

Automated checks provide measurable safeguards, not a complete aesthetic judgment. The AI coding agent must inspect the rendered PNG before delivery and confirm balanced spacing, readable hierarchy, an undistorted portrait, and no visual collisions.

## Language and factual accuracy

- A Chinese resume must be written in Chinese.
- An English resume must be written in English.
- Do not mix languages unless the user explicitly requests bilingual content. Established proper nouns may retain their standard form.
- Never invent degrees, companies, roles, dates, metrics, awards, certificates, projects, links, or other facts.
- Ask for clarification when the supplied information is insufficient or materially ambiguous.
- Preserve facts from a source resume while allowing concise editorial rewriting.

## Troubleshooting

### `xelatex` is not found

Install a TeX distribution that includes XeLaTeX, ensure its binary directory is on `PATH`, and rerun `xelatex --version`.

### A LaTeX package or font is missing

Install the package reported in the XeLaTeX output. Install `TeX Gyre Heros` and `Noto Sans CJK SC`, or update only the generated output `.tex` file with a suitable available font. Do not modify all source templates merely to fix one local build.

### PDF extraction fails

Confirm that the PDF contains selectable text and is not encrypted or image-only. Provide a text-based `.md`, `.markdown`, or `.txt` version, or supply the missing facts directly. Do not use guessed text.

### Content overflows the page

Reduce repetition, prioritize facts relevant to the target role, and adjust the generated layout controls conservatively while retaining legibility and the selected style. Do not fabricate shorter substitutes for unknown facts.

### The layout check fails

Read the reported metric and error, inspect the rendered preview, and adjust only the generated `.tex` file. Rebalance section spacing when the bottom margin exceeds 15 mm, shorten content when density is excessive, and resize or reposition the portrait when its safety area touches text. Recompile until both automated and visual checks pass.

### The portrait is not detected

Confirm that the exact `.jpg`, `.jpeg`, or `.png` named with `--portrait` is stored under `inputs/` and embedded directly in the generated `.tex` file. Do not substitute a screenshot or placeholder.

## License

This repository currently has no `LICENSE` file. Add an appropriate license before public distribution; no license grant should be inferred from the absence of that file.
