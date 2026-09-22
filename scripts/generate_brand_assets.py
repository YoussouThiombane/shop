"""Regenerate the PNG favicons from the MT logo's visual language."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "static" / "images"


def font_for(size):
    candidates = [
        Path("C:/Windows/Fonts/georgiab.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def create_icon(size, filename):
    scale = 4
    canvas_size = size * scale
    image = Image.new("RGB", (canvas_size, canvas_size), "#FAF8F3")
    draw = ImageDraw.Draw(image)
    margin = int(canvas_size * 0.06)
    draw.ellipse(
        (margin, margin, canvas_size - margin, canvas_size - margin),
        fill="#FAF8F3",
        outline="#C69A45",
        width=max(8, canvas_size // 35),
    )
    draw.text(
        (canvas_size / 2, canvas_size / 2),
        "MT",
        font=font_for(int(canvas_size * 0.34)),
        fill="#222326",
        anchor="mm",
    )
    image.resize((size, size), Image.Resampling.LANCZOS).save(OUTPUT / filename, optimize=True)


create_icon(64, "favicon.png")
create_icon(180, "apple-touch-icon.png")
