#!/usr/bin/env python3
"""Compile and validate a generated resume, then remove intermediate files."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable, List, Optional

from check_resume import (
    PORTRAIT_SUFFIXES,
    PYMUPDF_AVAILABLE,
    path_is_within,
    validate_resume,
)


WORKSPACE_ROOT = Path.cwd().resolve()
DEFAULT_OUTPUT_DIR = WORKSPACE_ROOT / "outputs"
INPUTS_DIR = (WORKSPACE_ROOT / "inputs").resolve()
SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = (SKILL_ROOT / "templates").resolve()
FONT_DECLARATION_PREFIXES = (
    r"\setmainfont",
    r"\setsansfont",
    r"\setmonofont",
    r"\setCJKmainfont",
    r"\setCJKsansfont",
    r"\setCJKmonofont",
    r"\newfontfamily",
    r"\newCJKfontfamily",
)
INTERMEDIATE_SUFFIXES = (
    ".aux",
    ".bbl",
    ".bcf",
    ".blg",
    ".dvi",
    ".fdb_latexmk",
    ".fls",
    ".glg",
    ".glo",
    ".gls",
    ".idx",
    ".ilg",
    ".ind",
    ".ist",
    ".lof",
    ".log",
    ".lot",
    ".nav",
    ".out",
    ".run.xml",
    ".snm",
    ".synctex.gz",
    ".toc",
    ".vrb",
    ".xdv",
)


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compile a resume .tex file with XeLaTeX, validate its one-page "
            "layout and portrait placement, retain the final .tex and .pdf, "
            "and remove intermediate files."
        )
    )
    parser.add_argument("tex_path", type=Path, help="path to the input .tex file")
    parser.add_argument(
        "--template",
        type=Path,
        required=True,
        help="exact source template under the installed skill's templates/ directory",
    )
    parser.add_argument(
        "--portrait",
        type=Path,
        required=True,
        help="exact .jpg, .jpeg, or .png portrait file under inputs/",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"final output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument("--max-bottom-margin-mm", type=float, default=15.0)
    parser.add_argument("--min-font-size-pt", type=float, default=5.0)
    parser.add_argument("--min-edge-margin-mm", type=float, default=3.0)
    parser.add_argument("--portrait-clearance-mm", type=float, default=2.0)
    parser.add_argument("--max-text-density", type=float, default=0.45)
    parser.add_argument("--hard-max-text-density", type=float, default=0.58)
    parser.add_argument(
        "--render-preview",
        type=Path,
        help="optional PNG path used for final visual inspection",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return a failure status when layout validation reports errors",
    )
    return parser.parse_args(argv)


def remove_known_intermediates(directory: Path, stem: str) -> None:
    """Remove only known LaTeX artifacts belonging to the requested job."""
    for suffix in INTERMEDIATE_SUFFIXES:
        candidate = directory / f"{stem}{suffix}"
        if candidate.is_file() or candidate.is_symlink():
            candidate.unlink()


def same_path(left: Path, right: Path) -> bool:
    try:
        return left.samefile(right)
    except FileNotFoundError:
        return left.resolve() == right.resolve()


def font_declarations(tex_path: Path) -> List[str]:
    declarations = []
    for line in tex_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith(FONT_DECLARATION_PREFIXES):
            declarations.append(stripped)
    return declarations


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    source = args.tex_path.expanduser().resolve()
    template = args.template.expanduser().resolve()
    portrait = args.portrait.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()

    if source.suffix.lower() != ".tex":
        print(f"Error: input must be a .tex file: {source}", file=sys.stderr)
        return 2
    if not source.is_file():
        print(f"Error: input file does not exist: {source}", file=sys.stderr)
        return 2
    if template.suffix.lower() != ".tex" or not template.is_file():
        print(f"Error: source template does not exist: {template}", file=sys.stderr)
        return 2
    if not path_is_within(template, TEMPLATES_DIR):
        print(f"Error: template must be stored under {TEMPLATES_DIR}.", file=sys.stderr)
        return 2
    try:
        expected_fonts = font_declarations(template)
        generated_fonts = font_declarations(source)
    except (OSError, UnicodeError) as exc:
        print(f"Error: could not read font declarations: {exc}", file=sys.stderr)
        return 2
    if not expected_fonts or generated_fonts != expected_fonts:
        print(
            "Error: generated font declarations differ from the selected template; "
            "copy every template font declaration verbatim and do not add replacements.",
            file=sys.stderr,
        )
        return 2
    if portrait.suffix.lower() not in PORTRAIT_SUFFIXES or not portrait.is_file():
        print(
            f"Error: portrait must be an existing .jpg, .jpeg, or .png file: {portrait}",
            file=sys.stderr,
        )
        return 2
    if not path_is_within(portrait, INPUTS_DIR):
        print(f"Error: portrait must be stored under {INPUTS_DIR}.", file=sys.stderr)
        return 2
    if not PYMUPDF_AVAILABLE:
        print(
            "Warning: PyMuPDF is unavailable, so layout validation will be "
            "skipped. Install it with: python3 -m pip install -r requirements.txt",
            file=sys.stderr,
        )

    xelatex = shutil.which("xelatex")
    if xelatex is None:
        print(
            "Error: xelatex is not installed or is not available on PATH. "
            "Install a TeX distribution with XeLaTeX and try again.",
            file=sys.stderr,
        )
        return 127

    output_dir.mkdir(parents=True, exist_ok=True)
    final_tex = output_dir / source.name
    final_pdf = output_dir / f"{source.stem}.pdf"

    if final_tex.exists() and not same_path(source, final_tex):
        print(
            f"Error: refusing to overwrite an existing output file: {final_tex}",
            file=sys.stderr,
        )
        return 2

    command_base = [xelatex, "-interaction=nonstopmode", "-file-line-error"]

    validation_failed = False
    validation_skipped = not PYMUPDF_AVAILABLE
    compilation_warnings = False

    try:
        if not same_path(source, final_tex):
            shutil.copy2(source, final_tex)
        with tempfile.TemporaryDirectory(
            prefix=f".{source.stem}-xelatex-", dir=str(output_dir)
        ) as temporary_dir:
            build_dir = Path(temporary_dir)
            command = command_base + [f"-output-directory={build_dir}", str(source)]

            for pass_number in (1, 2):
                result = subprocess.run(
                    command,
                    cwd=str(WORKSPACE_ROOT),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    check=False,
                )
                built_pdf = build_dir / f"{source.stem}.pdf"
                if result.returncode != 0 and not built_pdf.is_file():
                    print(
                        f"Error: XeLaTeX pass {pass_number} failed for {source}.",
                        file=sys.stderr,
                    )
                    print(result.stdout.rstrip(), file=sys.stderr)
                    return result.returncode or 1
                if result.returncode != 0:
                    compilation_warnings = True
                    print(
                        f"Warning: XeLaTeX pass {pass_number} reported errors but "
                        "still produced a PDF; retaining the generated files.",
                        file=sys.stderr,
                    )

            built_pdf = build_dir / f"{source.stem}.pdf"
            if not built_pdf.is_file():
                print(
                    f"Error: XeLaTeX completed without producing {built_pdf.name}.",
                    file=sys.stderr,
                )
                return 1

            shutil.copy2(built_pdf, final_pdf)

            if PYMUPDF_AVAILABLE:
                try:
                    report = validate_resume(
                        final_pdf,
                        portrait,
                        max_bottom_margin_mm=args.max_bottom_margin_mm,
                        min_font_size_pt=args.min_font_size_pt,
                        min_edge_margin_mm=args.min_edge_margin_mm,
                        portrait_clearance_mm=args.portrait_clearance_mm,
                        max_text_density=args.max_text_density,
                        hard_max_text_density=args.hard_max_text_density,
                        render_preview=args.render_preview,
                    )
                    report.print()
                    validation_failed = not report.passed
                except Exception as exc:
                    validation_skipped = True
                    print(
                        f"Warning: layout validation could not complete ({exc}); "
                        "the final files have still been retained.",
                        file=sys.stderr,
                    )
                if validation_failed:
                    print(
                        "Warning: PDF layout validation reported issues. The final "
                        "files will still be retained so the resume can be delivered "
                        "and refined.",
                        file=sys.stderr,
                    )
    except OSError as exc:
        print(f"Error: could not compile resume: {exc}", file=sys.stderr)
        return 1
    finally:
        remove_known_intermediates(output_dir, source.stem)

    if validation_skipped:
        print("Resume compiled successfully; layout validation was skipped.")
    elif validation_failed or compilation_warnings:
        print("Resume compiled successfully with compilation or validation warnings.")
    else:
        print("Resume compiled and validated successfully.")
    print(f"TeX: {final_tex}")
    print(f"PDF: {final_pdf}")
    return 1 if validation_failed and args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
