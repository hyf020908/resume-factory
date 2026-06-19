#!/usr/bin/env python3
"""Update explicit layout controls in a generated resume TeX file."""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Dict, Iterable, Optional


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = (PROJECT_ROOT / "outputs").resolve()
BEGIN_MARKER = "% RESUME_FACTORY_LAYOUT_BEGIN"
END_MARKER = "% RESUME_FACTORY_LAYOUT_END"
CONTROL_OPTIONS = {
    "ResumeSectionGap": "section_gap",
    "ResumeLineStretch": "line_stretch",
    "ResumeBottomInset": "bottom_inset",
    "ResumePortraitWidth": "portrait_width",
    "ResumePortraitXShift": "portrait_x_shift",
    "ResumePortraitYShift": "portrait_y_shift",
}
DIMENSION_PATTERN = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:pt|mm|cm|em|ex)$")
NUMBER_PATTERN = re.compile(r"^(?:\d+(?:\.\d*)?|\.\d+)$")


def path_is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Adjust standardized layout controls in a generated .tex file. "
            "The file must use the Resume Factory layout marker block."
        )
    )
    parser.add_argument("tex_path", type=Path)
    parser.add_argument("--section-gap")
    parser.add_argument("--line-stretch")
    parser.add_argument("--bottom-inset")
    parser.add_argument("--portrait-width")
    parser.add_argument("--portrait-x-shift")
    parser.add_argument("--portrait-y-shift")
    return parser.parse_args(argv)


def validate_values(values: Dict[str, str]) -> Optional[str]:
    for macro, value in values.items():
        if macro == "ResumeLineStretch":
            if not NUMBER_PATTERN.fullmatch(value) or not 0.8 <= float(value) <= 1.2:
                return f"{macro} must be a number from 0.8 through 1.2."
        elif not DIMENSION_PATTERN.fullmatch(value):
            return f"{macro} must be a TeX dimension such as 4pt, 8mm, or -1.5mm."
    return None


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    tex_path = args.tex_path.expanduser().resolve()
    if tex_path.suffix.lower() != ".tex" or not tex_path.is_file():
        print(f"Error: generated .tex file does not exist: {tex_path}", file=sys.stderr)
        return 2
    if not path_is_within(tex_path, OUTPUTS_DIR):
        print(
            f"Error: only generated files under {OUTPUTS_DIR} may be adjusted.",
            file=sys.stderr,
        )
        return 2

    values = {
        macro: getattr(args, option)
        for macro, option in CONTROL_OPTIONS.items()
        if getattr(args, option) is not None
    }
    if not values:
        print("Error: provide at least one layout adjustment option.", file=sys.stderr)
        return 2
    validation_error = validate_values(values)
    if validation_error:
        print(f"Error: {validation_error}", file=sys.stderr)
        return 2

    content = tex_path.read_text(encoding="utf-8")
    if content.count(BEGIN_MARKER) != 1 or content.count(END_MARKER) != 1:
        print(
            "Error: the file must contain exactly one Resume Factory layout marker block.",
            file=sys.stderr,
        )
        return 2
    start = content.index(BEGIN_MARKER)
    end = content.index(END_MARKER, start)
    block = content[start:end]
    outside_block = content[:start] + content[end + len(END_MARKER) :]

    for macro, value in values.items():
        pattern = re.compile(
            r"(\\newcommand\{\\" + re.escape(macro) + r"\}\{)([^{}]+)(\})"
        )
        if len(pattern.findall(block)) != 1:
            print(f"Error: expected one definition for \\{macro} in the layout block.", file=sys.stderr)
            return 2
        if f"\\{macro}" not in outside_block:
            print(
                f"Error: \\{macro} is defined but not used by the resume layout.",
                file=sys.stderr,
            )
            return 2
        block = pattern.sub(lambda match: f"{match.group(1)}{value}{match.group(3)}", block)

    updated = content[:start] + block + content[end:]
    mode = tex_path.stat().st_mode
    temporary_name = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=str(tex_path.parent), delete=False
        ) as temporary:
            temporary.write(updated)
            temporary_name = temporary.name
        os.chmod(temporary_name, mode)
        os.replace(temporary_name, tex_path)
    except OSError as exc:
        if temporary_name:
            try:
                Path(temporary_name).unlink()
            except OSError:
                pass
        print(f"Error: could not update layout controls: {exc}", file=sys.stderr)
        return 1

    print(f"Updated layout controls: {tex_path}")
    for macro, value in values.items():
        print(f"  \\{macro}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
