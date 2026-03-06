"""
image_processor.py – collage generation, cropping, and frame overlay.
"""

import logging
from pathlib import Path
from typing import List, Optional

from PIL import Image

logger = logging.getLogger(__name__)

# Output canvas dimensions
CANVAS_WIDTH = 1800
CANVAS_HEIGHT = 1200

# Supported collage layouts: (cols, rows)
LAYOUTS = {
    "2x2": (2, 2),
    "3x2": (3, 2),
    "1x3": (1, 3),
    "2x1": (2, 1),
}


def compose_collage(
    images: List[Path],
    output: Path,
    layout: str = "2x2",
    frame_path: Optional[Path] = None,
) -> bool:
    """
    Compose a collage from *images* using the named *layout* and save to
    *output*.  Returns True on success.
    """
    try:
        cols, rows = LAYOUTS.get(layout, LAYOUTS["2x2"])
        canvas = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "white")

        padding = 20
        cell_w = (CANVAS_WIDTH - padding * (cols + 1)) // cols
        cell_h = (CANVAS_HEIGHT - padding * (rows + 1)) // rows

        for idx, img_path in enumerate(images[: cols * rows]):
            col = idx % cols
            row = idx // cols
            x = padding + col * (cell_w + padding)
            y = padding + row * (cell_h + padding)

            img = Image.open(img_path)
            img = crop_and_resize(img, cell_w, cell_h)
            canvas.paste(img, (x, y))

        # Optional frame overlay
        if frame_path and frame_path.exists():
            frame = Image.open(frame_path).convert("RGBA")
            frame = frame.resize((CANVAS_WIDTH, CANVAS_HEIGHT))
            canvas = canvas.convert("RGBA")
            canvas = Image.alpha_composite(canvas, frame)
            canvas = canvas.convert("RGB")

        output.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(str(output), "JPEG", quality=95)
        logger.info("Collage saved: %s", output)
        return True
    except Exception as exc:  # noqa: BLE001
        logger.error("Collage generation failed: %s", exc)
        return False


def crop_and_resize(
    img: Image.Image, target_w: int, target_h: int
) -> Image.Image:
    """Centre-crop *img* to *target_w* × *target_h* preserving aspect ratio."""
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    target_ratio = target_w / target_h

    if src_ratio > target_ratio:
        # Image is wider → crop left/right
        new_w = int(src_h * target_ratio)
        offset = (src_w - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, src_h))
    else:
        # Image is taller → crop top/bottom
        new_h = int(src_w / target_ratio)
        offset = (src_h - new_h) // 2
        img = img.crop((0, offset, src_w, offset + new_h))

    return img.resize((target_w, target_h), Image.LANCZOS)


def apply_overlay(
    base: Image.Image, overlay_path: Path, opacity: float = 1.0
) -> Image.Image:
    """Composite *overlay_path* on top of *base* at the given *opacity*."""
    overlay = Image.open(overlay_path).convert("RGBA")
    overlay = overlay.resize(base.size)
    if opacity < 1.0:
        r, g, b, a = overlay.split()
        a = a.point(lambda v: int(v * opacity))
        overlay = Image.merge("RGBA", (r, g, b, a))
    base_rgba = base.convert("RGBA")
    result = Image.alpha_composite(base_rgba, overlay)
    return result.convert("RGB")
