#!/usr/bin/env python3
"""Simple CLI tool to convert images into a single PDF."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List

from PIL import Image

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}


def find_images(paths: Iterable[str]) -> List[Path]:
    files: List[Path] = []
    for raw in paths:
        path = Path(raw).expanduser().resolve()
        if path.is_dir():
            for candidate in sorted(path.rglob("*")):
                if candidate.suffix.lower() in SUPPORTED_EXTENSIONS:
                    files.append(candidate)
        elif path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)
    unique_files = []
    seen = set()
    for file in files:
        if file not in seen:
            unique_files.append(file)
            seen.add(file)
    return unique_files


def load_rgb_image(path: Path) -> Image.Image:
    raw = Image.open(path)
    if raw.mode in ("RGBA", "LA"):
        background = Image.new("RGB", raw.size, (255, 255, 255))
        background.paste(raw, mask=raw.split()[-1])
        return background
    return raw.convert("RGB")


def convert_to_pdf(images: List[Path], output: Path) -> None:
    if not images:
        raise ValueError("No valid images supplied.")
    first, *rest = images
    cover = load_rgb_image(first)
    pages = [load_rgb_image(img) for img in rest]
    cover.save(output, save_all=True, append_images=pages)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Combine one or more images into a PDF file.",
    )
    parser.add_argument(
        "sources",
        nargs="+",
        help="Image files or directories containing images.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.pdf",
        help="Path for the generated PDF (default: output.pdf).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    images = find_images(args.sources)
    if not images:
        raise SystemExit("지원되는 이미지 파일을 찾을 수 없습니다.")
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    convert_to_pdf(images, output)
    print(f"총 {len(images)}장의 이미지를 '{output}' PDF로 변환했습니다.")


if __name__ == "__main__":
    main()
