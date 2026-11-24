#!/usr/bin/env python3
"""THE TUESDAY MERIDIAN - SUN-YELLOW EDITION.
Renders news-image-20261124 entry.png (1024x1024) from stories.json.
Deterministic: no randomness, no timestamps, no network.
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
YELLOW = (255, 210, 31)
BLACK = (12, 12, 12)
RED = (200, 16, 46)
RED_SOFT = (255, 62, 62)
WHITE = (255, 255, 255)
GREY = (210, 210, 210)

FONT_DIR = Path("/home/hatch/workspace/fonts")
ANTON = FONT_DIR / "Anton-Regular.ttf"
MONT = FONT_DIR / "Montserrat-Bold.ttf"


def anton(size):
    return ImageFont.truetype(str(ANTON), size)


def mont(size, weight=800):
    """Montserrat is a VARIABLE font in this install: it defaults to Thin.
    Always pin the weight axis explicitly (800 = ExtraBold) or the text
    renders hairline. weight=400 gives the regular reading face."""
    f = ImageFont.truetype(str(MONT), size)
    f.set_variation_by_axes([weight])
    return f


def tw(draw, s, font):
    return draw.textlength(s, font=font)


def fit(draw, s, font_fn, start, max_w, min_size=8):
    """Shrink a font until the string fits max_w; return (font, size)."""
    size = start
    while size > min_size:
        f = font_fn(size)
        if tw(draw, s, f) <= max_w:
            return f, size
        size -= 1
    return font_fn(min_size), min_size


def centered(draw, s, font, y, fill, cx=W // 2):
    draw.text((cx - tw(draw, s, font) / 2, y), s, font=font, fill=fill)


def wrap(draw, s, font, max_w):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(draw, t, font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(draw, s, font, x, y, max_w, lh, fill, max_lines=None):
    lines = wrap(draw, s, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for i, ln in enumerate(lines):
        draw.text((x, y + i * lh), ln, font=font, fill=fill)
    return y + len(lines) * lh


def main():
    data = json.loads((HERE / "stories.json").read_text(encoding="utf-8"))
    img = Image.new("RGB", (W, H), YELLOW)
    d = ImageDraw.Draw(img)
    MX = 18  # page margin

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 94], fill=BLACK)
    f_title, _ = fit(d, data["title"], lambda s: anton(s), 76, W - 24)
    centered(d, data["title"], f_title, 12, YELLOW)

    # ---------- markets ticker ----------
    d.rectangle([0, 94, W, 126], fill=RED)
    f_tick, _ = fit(d, data["ticker"], lambda s: mont(s, 800), 17, W - 32)
    centered(d, data["ticker"], f_tick, 101, WHITE)

    # ---------- dateline ----------
    f_date, _ = fit(d, data["dateline"], lambda s: mont(s, 800), 20, W - 32)
    centered(d, data["dateline"], f_date, 134, BLACK)

    # ---------- hero panel ----------
    hero = data["hero"]
    hx0, hy0, hx1, hy1 = MX, 166, W - MX, 386
    d.rectangle([hx0, hy0, hx1, hy1], fill=BLACK)
    chip = "TOP STORY"
    f_chip = mont(15, 800)
    cw = tw(d, chip, f_chip) + 18
    d.rectangle([hx0 + 16, hy0 + 14, hx0 + 16 + cw, hy0 + 40], fill=RED)
    d.text((hx0 + 25, hy0 + 19), chip, font=f_chip, fill=WHITE)
    f_kick = mont(17, 800)
    d.text((hx0 + 28 + cw, hy0 + 18), hero["kicker"], font=f_kick, fill=RED_SOFT)
    # headline: yellow part + red final word group, one line, Anton
    f_hl, hl_size = fit(
        d, hero["headline_yellow"] + " " + hero["headline_red"],
        lambda s: anton(s), 64, hx1 - hx0 - 32)
    ytxt = hero["headline_yellow"] + " "
    d.text((hx0 + 16, hy0 + 46), ytxt, font=f_hl, fill=YELLOW)
    d.text((hx0 + 16 + tw(d, ytxt, f_hl), hy0 + 46),
           hero["headline_red"], font=f_hl, fill=RED_SOFT)
    yy = hy0 + 46 + hl_size + 12
    yy = block(d, hero["deck"], mont(20, 800), hx0 + 16, yy, hx1 - hx0 - 32, 24, WHITE, 2)
    yy += 2
    block(d, hero["body"], mont(13, 400), hx0 + 16, yy, hx1 - hx0 - 32, 17, GREY, 3)

    # ---------- second row: two columns ----------
    sec = data["second"]
    col_w = (W - 2 * MX - 24) // 2
    xs = [MX, MX + col_w + 24]
    sy = 398
    for i, story in enumerate(sec):
        x = xs[i]
        d.rectangle([x, sy, x + col_w, sy + 6], fill=BLACK)
        d.text((x, sy + 13), story["kicker"], font=mont(14, 800), fill=RED)
        f_sh, _ = fit(d, story["headline"], lambda s: anton(s), 37, col_w)
        d.text((x, sy + 33), story["headline"], font=f_sh, fill=BLACK)
        block(d, story["body"], mont(13, 400), x, sy + 78, col_w, 16, BLACK, 5)

    # ---------- mini-features: four columns ----------
    feats = data["features"]
    fw = (W - 2 * MX - 3 * 16) // 4
    fy = 564
    cont_color = {c["name"]: tuple(int(c["color"][i:i + 2], 16) for i in (1, 3, 5))
                  for c in data["continents"]}
    for i, story in enumerate(feats):
        x = MX + i * (fw + 16)
        d.rectangle([x, fy, x + fw, fy + 5], fill=cont_color[story["region"]])
        f_fk, _ = fit(d, story["kicker"], lambda s: mont(s, 800), 12, fw)
        d.text((x, fy + 11), story["kicker"], font=f_fk, fill=RED)
        hy = block(d, story["headline"], mont(19, 800), x, fy + 29, fw, 22, BLACK, 2)
        block(d, story["body"], mont(12, 400), x, hy + 2, fw, 14, BLACK, 4)

    # ---------- the day in brief ----------
    by = 700
    d.rectangle([MX, by, W - MX, by + 30], fill=BLACK)
    d.text((MX + 12, by + 6), "THE DAY IN BRIEF", font=mont(17, 800), fill=YELLOW)
    right = "01–30 · EVERY CONTINENT, ONE LINE EACH"
    f_r = mont(12, 800)
    d.text((W - MX - 12 - tw(d, right, f_r), by + 9), right, font=f_r, fill=WHITE)
    briefs = data["briefs"]
    f_num = mont(12, 800)
    f_br = mont(12, 400)
    bx = [MX + 4, W // 2 + 8]
    bw = W // 2 - MX - 44
    for idx, b in enumerate(briefs):
        col = 0 if idx < 15 else 1
        row = idx % 15
        x, y = bx[col], by + 40 + row * 15.5
        d.text((x, y), b["n"], font=f_num, fill=RED)
        f_one, _ = fit(d, b["text"], lambda s: mont(s, 400), 12, bw, min_size=9)
        d.text((x + 30, y), b["text"], font=f_one, fill=BLACK)

    # ---------- eight continents strip ----------
    ty = 972
    d.rectangle([0, ty, W, H], fill=BLACK)
    d.text((MX, ty + 5), "EIGHT CONTINENTS", font=mont(13, 800), fill=YELLOW)
    cw8 = (W - 2 * MX) / 8
    for i, c in enumerate(data["continents"]):
        x = MX + i * cw8
        col = cont_color[c["name"]]
        d.ellipse([x, ty + 27, x + 9, ty + 36], fill=col)
        f_cn, _ = fit(d, c["name"], lambda s: mont(s, 800), 11, cw8 - 13, min_size=7)
        d.text((x + 13, ty + 25), c["name"], font=f_cn, fill=col)
        f_cue, _ = fit(d, c["cue"], lambda s: mont(s, 400), 9, cw8 - 2, min_size=6)
        d.text((x, ty + 40), c["cue"], font=f_cue, fill=WHITE)

    img.save(HERE / "entry.png")
    print("wrote", HERE / "entry.png", img.size)


if __name__ == "__main__":
    main()
