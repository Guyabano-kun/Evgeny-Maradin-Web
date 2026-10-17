"""Generates the social preview image web/og.png (1200x630) and web/favicon.svg.

Run once after changing the headline or metrics; output is committed.
Needs Pillow and the Inter / Liberation Serif fonts (paths below).
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else "web"
INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
BG, INK, MUTED, LINE, ACCENT = "#f4f1ea", "#111111", "#68645d", "#d7d1c7", "#c84b2f"

W, H, PAD = 1200, 630, 72
im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
f = lambda w, s: ImageFont.truetype(INTER.format(w), s)

d.text((PAD, 64), "EM", font=f("Black", 40), fill=INK)
d.text((PAD + d.textlength("EM", font=f("Black", 40)), 64), ".", font=f("Black", 40), fill=ACCENT)
d.text((PAD, 150), "CONCEPT DEVELOPMENT / FEL  ·  UPSTREAM OIL & GAS", font=f("Bold", 20), fill=MUTED)
d.text((PAD, 196), "Engineering decisions", font=f("ExtraBold", 84), fill=INK)
d.text((PAD, 286), "before FEED.", font=ImageFont.truetype(SERIF_IT, 92), fill=ACCENT)
d.text((PAD, 406), "Evgeny Maradin — Senior Concept & Project Engineer", font=f("Medium", 28), fill=INK)

d.line((PAD, 482, W - PAD, 482), fill=LINE, width=2)
metrics = [("19", "years upstream"), ("50+", "studies"), ("$300M+", "project scale"), ("57%", "CAPEX reduction")]
col = (W - 2 * PAD) / len(metrics)
for i, (b, s) in enumerate(metrics):
    x = PAD + i * col
    d.text((x, 506), b, font=f("Black", 40), fill=INK)
    d.text((x, 560), s, font=f("Medium", 20), fill=MUTED)

os.makedirs(OUT, exist_ok=True)
im.save(os.path.join(OUT, "og.png"), optimize=True)

with open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8") as fh:
    fh.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#111"/>'
             '<text x="8" y="44" font-family="Inter,Arial,sans-serif" font-weight="900" font-size="30" fill="#f4f1ea">EM</text>'
             '<circle cx="54" cy="41" r="4" fill="#c84b2f"/></svg>')
print("og.png + favicon.svg written")
