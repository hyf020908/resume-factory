#!/usr/bin/env python3
"""Validate one-page resume PDF geometry and portrait placement."""

from __future__ import annotations

import argparse
import hashlib
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

try:
    import fitz  # type: ignore
except ImportError:
    fitz = None

PYMUPDF_AVAILABLE = fitz is not None


WORKSPACE_ROOT = Path.cwd().resolve()
INPUTS_DIR = WORKSPACE_ROOT / "inputs"
MM_TO_PT = 72.0 / 25.4
PORTRAIT_SUFFIXES = {".jpg", ".jpeg", ".png"}


@dataclass
class CheckReport:
    pdf_path: Path
    metrics: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors

    def print(self) -> None:
        print(f"Layout check: {self.pdf_path}")
        for metric in self.metrics:
            print(f"  METRIC: {metric}")
        for warning in self.warnings:
            print(f"  WARNING: {warning}")
        for error in self.errors:
            print(f"  ERROR: {error}")
        print("Layout check passed." if self.passed else "Layout check failed.")


def path_is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def normalized_pixmap_digest(pixmap: "fitz.Pixmap") -> bytes:
    if pixmap.colorspace is None:
        return b""
    if pixmap.colorspace.n != 3 or pixmap.alpha:
        pixmap = fitz.Pixmap(fitz.csRGB, pixmap)
    payload = (
        f"{pixmap.width}x{pixmap.height}:".encode("ascii") + bytes(pixmap.samples)
    )
    return hashlib.sha256(payload).digest()


def find_portrait_rectangles(
    document: "fitz.Document", page: "fitz.Page", portrait_path: Path
) -> List["fitz.Rect"]:
    target = normalized_pixmap_digest(fitz.Pixmap(str(portrait_path)))
    rectangles: List["fitz.Rect"] = []
    seen_xrefs = set()

    for image in page.get_images(full=True):
        xref = int(image[0])
        if xref <= 0 or xref in seen_xrefs:
            continue
        seen_xrefs.add(xref)
        try:
            embedded = fitz.Pixmap(document, xref)
            if normalized_pixmap_digest(embedded) != target:
                continue
            rectangles.extend(page.get_image_rects(xref))
        except (RuntimeError, ValueError):
            continue
    return rectangles


def collect_words(page: "fitz.Page") -> List[Tuple["fitz.Rect", str, int, int]]:
    words = []
    for item in page.get_text("words"):
        text = str(item[4]).strip()
        if text:
            words.append((fitz.Rect(item[:4]), text, int(item[5]), int(item[6])))
    return words


def collect_font_sizes_and_text_bottom(page: "fitz.Page") -> Tuple[List[float], float]:
    sizes: List[float] = []
    bottom = 0.0
    text = page.get_text("dict")
    for block in text.get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if not span.get("text", "").strip():
                    continue
                sizes.append(float(span.get("size", 0.0)))
                bottom = max(bottom, float(span.get("bbox", (0, 0, 0, 0))[3]))
    return sizes, bottom


def overlapping_word_pairs(
    words: Sequence[Tuple["fitz.Rect", str, int, int]], limit: int = 12
) -> List[Tuple[str, str]]:
    ordered = sorted(words, key=lambda item: (item[0].y0, item[0].x0))
    overlaps: List[Tuple[str, str]] = []
    for index, (left_rect, left_text, left_block, left_line) in enumerate(ordered):
        for right_rect, right_text, right_block, right_line in ordered[index + 1 :]:
            if right_rect.y0 >= left_rect.y1:
                break
            if left_block == right_block and left_line == right_line:
                continue
            intersection = left_rect & right_rect
            if intersection.is_empty:
                continue
            smaller_area = min(abs(left_rect), abs(right_rect))
            if smaller_area <= 0:
                continue
            if abs(intersection) / smaller_area >= 0.15:
                overlaps.append((left_text, right_text))
                if len(overlaps) >= limit:
                    return overlaps
    return overlaps


def validate_resume(
    pdf_path: Path,
    portrait_path: Path,
    max_bottom_margin_mm: float = 15.0,
    min_font_size_pt: float = 5.0,
    min_edge_margin_mm: float = 3.0,
    portrait_clearance_mm: float = 2.0,
    max_text_density: float = 0.45,
    hard_max_text_density: float = 0.58,
    render_preview: Optional[Path] = None,
    require_portrait_in_inputs: bool = True,
) -> CheckReport:
    pdf_path = pdf_path.expanduser().resolve()
    portrait_path = portrait_path.expanduser().resolve()
    report = CheckReport(pdf_path=pdf_path)

    if not PYMUPDF_AVAILABLE:
        report.errors.append(
            "PyMuPDF is not installed. Run: python3 -m pip install -r requirements.txt"
        )
        return report
    if not pdf_path.is_file():
        report.errors.append(f"PDF does not exist: {pdf_path}")
        return report
    if portrait_path.suffix.lower() not in PORTRAIT_SUFFIXES:
        report.errors.append("Portrait must be a .jpg, .jpeg, or .png file.")
        return report
    if not portrait_path.is_file():
        report.errors.append(f"Portrait does not exist: {portrait_path}")
        return report
    if require_portrait_in_inputs and not path_is_within(
        portrait_path, INPUTS_DIR.resolve()
    ):
        report.errors.append(f"Portrait must be stored under {INPUTS_DIR.resolve()}.")
        return report

    try:
        document = fitz.open(str(pdf_path))
    except (RuntimeError, ValueError) as exc:
        report.errors.append(f"Cannot open PDF: {exc}")
        return report

    try:
        report.metrics.append(f"pages={document.page_count}")
        if document.page_count != 1:
            report.errors.append(
                f"Resume must contain exactly one page; found {document.page_count}."
            )
            return report

        page = document[0]
        page_rect = page.rect
        words = collect_words(page)
        font_sizes, text_bottom = collect_font_sizes_and_text_bottom(page)

        if render_preview is not None:
            preview = render_preview.expanduser().resolve()
            preview.parent.mkdir(parents=True, exist_ok=True)
            page.get_pixmap(dpi=150, alpha=False).save(str(preview))
            report.metrics.append(f"preview={preview}")

        if not words or not font_sizes:
            report.errors.append("No extractable resume text was found in the PDF.")
            return report

        bottom_margin_mm = max(0.0, page_rect.y1 - text_bottom) / MM_TO_PT
        smallest_font = min(font_sizes)
        word_area = sum(abs(rect) for rect, _, _, _ in words)
        text_density = word_area / abs(page_rect)
        report.metrics.extend(
            [
                f"page_size={page_rect.width / MM_TO_PT:.1f}x{page_rect.height / MM_TO_PT:.1f}mm",
                f"bottom_text_margin={bottom_margin_mm:.1f}mm (maximum {max_bottom_margin_mm:.1f}mm)",
                f"minimum_font_size={smallest_font:.1f}pt (minimum {min_font_size_pt:.1f}pt)",
                f"text_density={text_density:.3f} (recommended maximum {max_text_density:.3f}, hard maximum {hard_max_text_density:.3f})",
            ]
        )

        if bottom_margin_mm > max_bottom_margin_mm:
            report.warnings.append(
                "Bottom whitespace is larger than recommended; consider rebalancing the layout."
            )
        if smallest_font + 0.01 < min_font_size_pt:
            report.errors.append(
                "Text is below the absolute legibility floor. Keep every source content unit, restore the font to the floor, and reflow the layout."
            )
        if text_density > hard_max_text_density:
            report.errors.append(
                "Text density exceeds the hard safety limit. Keep every source content unit and reflow the layout; do not summarize or delete content."
            )
        elif text_density > max_text_density:
            report.warnings.append(
                "Text density is above the recommended level; inspect the preview before delivery."
            )

        edge_inset = min_edge_margin_mm * MM_TO_PT
        safe_rect = fitz.Rect(
            page_rect.x0 + edge_inset,
            page_rect.y0 + edge_inset,
            page_rect.x1 - edge_inset,
            page_rect.y1 - edge_inset,
        )
        outside = [text for rect, text, _, _ in words if not safe_rect.contains(rect)]
        if outside:
            sample = ", ".join(repr(text) for text in outside[:6])
            report.warnings.append(
                f"Text is outside the {min_edge_margin_mm:.1f}mm page-edge safety area: {sample}."
            )

        overlaps = overlapping_word_pairs(words)
        if overlaps:
            sample = ", ".join(f"{left!r}/{right!r}" for left, right in overlaps[:6])
            report.warnings.append(
                f"Possible overlapping text was detected; inspect visually: {sample}."
            )

        portrait_rects = find_portrait_rectangles(document, page, portrait_path)
        report.metrics.append(f"portrait_instances={len(portrait_rects)}")
        if not portrait_rects:
            report.errors.append(
                "The supplied portrait was not found in the PDF; embed the exact image file instead of a placeholder."
            )
        else:
            clearance = portrait_clearance_mm * MM_TO_PT
            collisions = []
            for portrait_rect in portrait_rects:
                expanded = fitz.Rect(
                    portrait_rect.x0 - clearance,
                    portrait_rect.y0 - clearance,
                    portrait_rect.x1 + clearance,
                    portrait_rect.y1 + clearance,
                )
                for word_rect, text, _, _ in words:
                    if not (expanded & word_rect).is_empty:
                        collisions.append(text)
            if collisions:
                sample = ", ".join(repr(text) for text in collisions[:8])
                report.errors.append(
                    f"Portrait overlaps or crowds text within {portrait_clearance_mm:.1f}mm: {sample}."
                )

        report.warnings.append(
            "Automated geometry checks cannot judge visual quality completely; inspect the rendered preview before delivery."
        )
        return report
    finally:
        document.close()


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check one-page resume layout, whitespace, legibility, and portrait placement."
    )
    parser.add_argument("pdf_path", type=Path, help="generated resume PDF")
    parser.add_argument(
        "--portrait", type=Path, required=True, help="exact portrait image under inputs/"
    )
    parser.add_argument("--max-bottom-margin-mm", type=float, default=15.0)
    parser.add_argument("--min-font-size-pt", type=float, default=5.0)
    parser.add_argument("--min-edge-margin-mm", type=float, default=3.0)
    parser.add_argument("--portrait-clearance-mm", type=float, default=2.0)
    parser.add_argument("--max-text-density", type=float, default=0.45)
    parser.add_argument("--hard-max-text-density", type=float, default=0.58)
    parser.add_argument(
        "--render-preview", type=Path, help="optional PNG path for visual inspection"
    )
    return parser.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    report = validate_resume(
        args.pdf_path,
        args.portrait,
        max_bottom_margin_mm=args.max_bottom_margin_mm,
        min_font_size_pt=args.min_font_size_pt,
        min_edge_margin_mm=args.min_edge_margin_mm,
        portrait_clearance_mm=args.portrait_clearance_mm,
        max_text_density=args.max_text_density,
        hard_max_text_density=args.hard_max_text_density,
        render_preview=args.render_preview,
    )
    report.print()
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
