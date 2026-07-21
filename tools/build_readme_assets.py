from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SOURCE = ASSETS / "hero-source.png"
OUTPUT = ASSETS / "hero-animated.gif"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


base = Image.open(SOURCE).convert("RGB")
width, height = base.size

# The generated patch used the wrong numerals. Repaint the tiny fabric label locally.
draw = ImageDraw.Draw(base)
patch_box = (1642, 699, 1740, 750)
draw.rounded_rectangle(patch_box, radius=5, fill=(24, 24, 27), outline=(82, 40, 42), width=2)
draw.text((1657, 703), "111", font=font("consolab.ttf", 34), fill=(211, 62, 57))

title_font = font("consolab.ttf", 54)
meta_font = font("consola.ttf", 24)
micro_font = font("consola.ttf", 15)

frames = []
frame_count = 24
for index in range(frame_count):
    frame = ImageEnhance.Brightness(base).enhance(1.0 + (0.012 if index % 15 == 0 else 0))
    frame = frame.copy()
    layer = ImageDraw.Draw(frame, "RGBA")

    # Controlled scan line and UI pulse. The character remains stable and readable.
    scan_y = int((index / frame_count) * height)
    layer.rectangle((0, scan_y, width, scan_y + 3), fill=(65, 220, 229, 34))
    layer.rectangle((0, scan_y + 4, width, scan_y + 14), fill=(21, 115, 126, 10))

    cyan = (80, 210, 220, 255)
    coral = (229, 75, 70, 255)
    muted = (150, 166, 172, 255)
    layer.text((94, 188), "CHAKE111", font=title_font, fill=(235, 238, 240, 255))
    layer.text((96, 253), "// FULL-STACK ENGINEER", font=meta_font, fill=coral)
    layer.line((96, 302, 690, 302), fill=(53, 185, 195, 220), width=2)
    layer.text((96, 328), "STATUS", font=micro_font, fill=muted)
    layer.text((236, 328), "ONLINE", font=micro_font, fill=cyan)
    layer.text((96, 360), "LOCATION", font=micro_font, fill=muted)
    layer.text((236, 360), "THE NET", font=micro_font, fill=cyan)

    # Short boot cursor cycle rather than constant noisy glitching.
    cursor_on = index % 10 < 6
    if cursor_on:
        layer.rectangle((319, 362, 331, 379), fill=cyan)
    if index in (0, 1, 15):
        layer.rectangle((91, 182, 710, 246), fill=(222, 62, 57, 20))

    frames.append(frame.resize((960, 360), Image.Resampling.LANCZOS).convert("P", palette=Image.Palette.ADAPTIVE, colors=96))

frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=110,
    loop=0,
    optimize=True,
    disposal=2,
)

print(f"created {OUTPUT} ({OUTPUT.stat().st_size} bytes)")


