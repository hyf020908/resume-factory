#!/usr/bin/env python3
"""Compile and validate a generated resume, then remove intermediate files."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable, Optional

from check_resume import (
    PORTRAIT_SUFFIXES,
    PYMUPDF_AVAILABLE,
    path_is_within,
    validate_resume,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs"
INPUTS_DIR = (PROJECT_ROOT / "inputs").resolve()
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
    parser.add_argument("--min-font-size-pt", type=float, default=7.5)
    parser.add_argument("--min-edge-margin-mm", type=float, default=3.0)
    parser.add_argument("--portrait-clearance-mm", type=float, default=2.0)
    parser.add_argument("--max-text-density", type=float, default=0.38)
    parser.add_argument(
        "--render-preview",
        type=Path,
        help="optional PNG path used for final visual inspection",
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


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    source = args.tex_path.expanduser().resolve()
    portrait = args.portrait.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()

    if source.suffix.lower() != ".tex":
        print(f"Error: input must be a .tex file: {source}", file=sys.stderr)
        return 2
    if not source.is_file():
        print(f"Error: input file does not exist: {source}", file=sys.stderr)
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
            "Error: PyMuPDF is required for layout validation. "
            "Run: python3 -m pip install -r requirements.txt",
            file=sys.stderr,
        )
        return 2

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

    command_base = [
        xelatex,
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
    ]

    try:
        with tempfile.TemporaryDirectory(
            prefix=f".{source.stem}-xelatex-", dir=str(output_dir)
        ) as temporary_dir:
            build_dir = Path(temporary_dir)
            command = command_base + [f"-output-directory={build_dir}", str(source)]

            for pass_number in (1, 2):
                result = subprocess.run(
                    command,
                    cwd=str(source.parent),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    check=False,
                )
                if result.returncode != 0:
                    print(
                        f"Error: XeLaTeX pass {pass_number} failed for {source}.",
                        file=sys.stderr,
                    )
                    print(result.stdout.rstrip(), file=sys.stderr)
                    return result.returncode or 1

            built_pdf = build_dir / f"{source.stem}.pdf"
            if not built_pdf.is_file():
                print(
                    f"Error: XeLaTeX completed without producing {built_pdf.name}.",
                    file=sys.stderr,
                )
                return 1

            report = validate_resume(
                built_pdf,
                portrait,
                max_bottom_margin_mm=args.max_bottom_margin_mm,
                min_font_size_pt=args.min_font_size_pt,
                min_edge_margin_mm=args.min_edge_margin_mm,
                portrait_clearance_mm=args.portrait_clearance_mm,
                max_text_density=args.max_text_density,
                render_preview=args.render_preview,
            )
            report.print()
            if not report.passed:
                print(
                    "Error: PDF layout validation failed; adjust the generated .tex file and compile again.",
                    file=sys.stderr,
                )
                return 1

            if not same_path(source, final_tex):
                shutil.copy2(source, final_tex)
            shutil.copy2(built_pdf, final_pdf)
    except OSError as exc:
        print(f"Error: could not compile resume: {exc}", file=sys.stderr)
        return 1
    finally:
        remove_known_intermediates(output_dir, source.stem)

    print("Resume compiled and validated successfully.")
    print(f"TeX: {final_tex}")
    print(f"PDF: {final_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
