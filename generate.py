#!/usr/bin/env python3
"""Generate the front-page image for the 19 November 2026 world news.

Original artwork drawn with Pillow: a classic newspaper front page with a
large masthead, a readable date line, one lead story and three supporting
stories. Run locally to produce entry.png; main.py only copies it.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
ACCENT = (160, 32, 28)
GREY = (90, 86, 78)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to the given pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, fill=INK, leading=None):
    leading = leading or int(fnt.size * 1.35)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 44  # margin
    cx = W - mx

    # ---- Masthead ----
    f_mast = font(SERIF_B, 78)
    mast = "THE WORLD TODAY"
    tw = d.textlength(mast, font=f_mast)
    d.text(((W - tw) / 2, 30), mast, font=f_mast, fill=INK)
    rule(d, mx, 148, cx, 3)
    f_date = font(SANS_B, 30)
    date = "THURSDAY  •  19 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 162), date, font=f_date, fill=ACCENT)
    rule(d, mx, 208, cx, 3)

    # ---- Lead story: trilateral summit ----
    y = 232
    f_kick = font(SANS_B, 24)
    d.text((mx, y), "SUMMIT IN SHENZHEN", font=f_kick, fill=ACCENT)
    y += 36
    f_lead = font(SERIF_B, 62)
    y = para(d, mx, y, cx - mx,
             "Trump, Xi and Putin meet in Shenzhen",
             f_lead, leading=70)
    y += 6
    f_deck = font(SERIF, 26)
    y = para(d, mx, y, cx - mx,
             "Xi greets Trump with a hug on the tarmac as the three leaders "
             "open a trilateral summit in southern China.",
             f_deck, leading=34)
    y += 14

    # Skyline illustration: abstract towers under a red sun.
    ill_y0, ill_y1 = y, y + 118
    d.rectangle([mx, ill_y0, cx, ill_y1], fill=(233, 227, 210))
    d.ellipse([mx + 8, ill_y0 + 6, mx + 72, ill_y0 + 70], fill=ACCENT)
    base = ill_y1
    towers = [(mx + 30, 46), (mx + 130, 78), (mx + 240, 58), (mx + 350, 92),
              (mx + 470, 64), (mx + 580, 84), (mx + 700, 52), (mx + 800, 70)]
    for tx, th in towers:
        d.rectangle([tx, base - th, tx + 78, base], fill=INK)
    for tx, th in towers:
        for wy in range(base - th + 10, base - 8, 18):
            d.rectangle([tx + 10, wy, tx + 22, wy + 8], fill=PAPER)
            d.rectangle([tx + 46, wy, tx + 58, wy + 8], fill=PAPER)
    d.text((cx - 138, ill_y0 + 10), "SHENZHEN", font=font(SANS_B, 20), fill=GREY)
    y = ill_y1 + 20
    rule(d, mx, y, cx, 2)
    y += 18

    # ---- Three supporting stories in columns ----
    col_w = 292
    gap = 26
    stories = [
        ("GAMING", "GTA VI rolls out worldwide",
         "Gamers step back into Vice City as Grand Theft Auto VI begins its "
         "global rollout, thirteen years after the last entry."),
        ("BUSINESS", "Anthropic IPO raises $81.3bn",
         "The maker of Claude lists in the largest initial public offering "
         "on record, raising $81.3 billion."),
        ("SPACE", "Voyager 1 reaches one light-day",
         "NASA's Voyager 1 passes one light-day from Earth, fifty years "
         "after the probe was launched."),
    ]
    f_ck = font(SANS_B, 20)
    f_ch = font(SERIF_B, 30)
    f_cb = font(SERIF, 20)
    top = y
    for i, (kick, head, body) in enumerate(stories):
        x = mx + i * (col_w + gap)
        yy = top
        d.text((x, yy), kick, font=f_ck, fill=ACCENT)
        yy += 30
        yy = para(d, x, yy, col_w, head, f_ch, leading=36)
        yy += 8
        para(d, x, yy, col_w, body, f_cb, leading=27)
        if i < 2:
            d.line([(x + col_w + gap // 2, top),
                    (x + col_w + gap // 2, top + 218)], fill=GREY, width=1)

    # ---- Footer ----
    fy = H - 56
    rule(d, mx, fy - 14, cx, 2)
    f_foot = font(SANS, 19)
    foot = "THE WORLD TODAY — 19 NOVEMBER 2026  •  ONE IMAGE, FOUR STORIES"
    tw = d.textlength(foot, font=f_foot)
    d.text(((W - tw) / 2, fy), foot, font=f_foot, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
