#!/usr/bin/env python3
"""Generate the site-wide Open Graph / Twitter card preview image (1200x630)."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ROOT / "assets" / "img" / "og-preview.png"
ICON_PATH = ROOT / "assets" / "img" / "favicons" / "android-chrome-512x512.png"

# Canvas dimensions (Standard 1.91:1 Open Graph banner)
W, H = 1200, 630
BG_COLOR = (24, 24, 27, 255)  # #18181b
BORDER_COLOR = (39, 39, 42, 255)  # #27272a

# Typography & Colors
FONT_BOLD_PATH = "/usr/share/fonts/opentype/FiraSans/FiraSans-Bold.otf"
FONT_ITALIC_PATH = "/usr/share/fonts/opentype/FiraSans/FiraSans-Italic.otf"
FONT_MEDIUM_PATH = "/usr/share/fonts/opentype/FiraSans/FiraSans-Medium.otf"

f_bold = ImageFont.truetype(FONT_BOLD_PATH, 68)
f_tagline = ImageFont.truetype(FONT_ITALIC_PATH, 34)
f_url = ImageFont.truetype(FONT_MEDIUM_PATH, 26)

COLOR_TITLE = (255, 255, 255, 255)
COLOR_TAGLINE = (161, 161, 170, 255)  # #a1a1aa
COLOR_URL = (113, 113, 122, 255)  # #71717a

# Initialize canvas
img = Image.new("RGBA", (W, H), BG_COLOR)
draw = ImageDraw.Draw(img)

# Load and resize icon
icon = Image.open(ICON_PATH).convert("RGBA")
icon_size = 220
icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)

# Measure text blocks
bbox_title = draw.textbbox((0, 0), "Doctor Psi", font=f_bold)
h_title = bbox_title[3] - bbox_title[1]

bbox_tag = draw.textbbox((0, 0), "half-baked physicist", font=f_tagline)
h_tag = bbox_tag[3] - bbox_tag[1]

bbox_url = draw.textbbox((0, 0), "doctorpsi.github.io", font=f_url)
h_url = bbox_url[3] - bbox_url[1]

gap_title_tag = 20
gap_tag_url = 24
total_text_h = h_title + gap_title_tag + h_tag + gap_tag_url + h_url

# Horizontal layout calculations
gap_icon_text = 55
total_w = icon_size + gap_icon_text + 480
start_x = (W - total_w) // 2

icon_y = (H - icon_size) // 2
text_y_start = (H - total_text_h) // 2

# Paste icon
img.paste(icon, (start_x, icon_y), icon)

# Draw text
text_x = start_x + icon_size + gap_icon_text
draw.text(
    (text_x, text_y_start - bbox_title[1]), "Doctor Psi", fill=COLOR_TITLE, font=f_bold
)

curr_y = text_y_start + h_title + gap_title_tag
draw.text(
    (text_x, curr_y - bbox_tag[1]),
    "half-baked physicist",
    fill=COLOR_TAGLINE,
    font=f_tagline,
)

curr_y += h_tag + gap_tag_url
draw.text(
    (text_x, curr_y - bbox_url[1]), "doctorpsi.github.io", fill=COLOR_URL, font=f_url
)

# Subtle outer border
draw.rectangle([(0, 0), (W - 1, H - 1)], outline=BORDER_COLOR, width=2)

# Save
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
img.save(OUTPUT_PATH)
print(f"Generated: {OUTPUT_PATH}")
