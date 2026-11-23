#!/usr/bin/env python3
"""The World Today -- Monday 23 November 2026.

A one-day world news front page, drawn from scratch in pure Python 3
standard library: a 5x7 bitmap font, a small canvas, and a hand-rolled
PNG encoder. No network, no files read, no timestamps anywhere, so two
runs write byte-identical output.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py   (writes out/entry.png)
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 234)   # warm newsprint
INK = (17, 17, 17)        # near-black text
MUTED = (96, 90, 80)      # grey-brown secondary text
RULE = (17, 17, 17)
RED = (176, 30, 30)       # masthead accent
BLUE = (29, 78, 158)      # markets
GREEN = (30, 107, 58)     # climate
TEAL = (15, 118, 110)     # africa
PURPLE = (107, 63, 160)   # europe
ORANGE = (194, 65, 12)    # asia
BROWN = (138, 90, 0)      # middle east
SLATE = (51, 65, 85)      # sport
LIGHT = (238, 231, 218)   # light panel

REGION_COLOR = {
    "CLIMATE": GREEN,
    "MARKETS": BLUE,
    "TECH": BLUE,
    "MIDDLE EAST": BROWN,
    "UKRAINE": PURPLE,
    "EUROPE": PURPLE,
    "AMERICAS": RED,
    "ASIA": ORANGE,
    "AFRICA": TEAL,
    "SPORT": SLATE,
}

# ------------------------------------------------------- 5x7 bitmap font
# Each glyph is 7 rows of 5 cells; '1' is ink, '0' is empty. Uppercase,
# lowercase, digits and punctuation. Unknown characters render as '?'.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "10110", "11001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01110", "10001", "10000", "10001", "01110"),
    "d": ("00001", "00001", "01101", "10011", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    "g": ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    "h": ("10000", "10000", "10110", "11001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00010", "00010", "00010", "10010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "10110", "11001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "00000", "10110", "11001", "10001", "11110", "10000"),
    "q": ("00000", "00000", "01101", "10011", "10001", "01111", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("01000", "01000", "11100", "01000", "01000", "01001", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "*": ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    ",": ("00000", "00000", "00000", "00000", "00100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "[": ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
    "\\": ("10000", "01000", "01000", "00100", "00010", "00010", "00001"),
    "]": ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
    "^": ("00100", "01010", "10001", "00000", "00000", "00000", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "`": ("01000", "00100", "00010", "00000", "00000", "00000", "00000"),
    "{": ("00110", "01000", "01000", "11110", "01000", "01000", "00110"),
    "|": ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
    "}": ("01100", "00010", "00010", "01111", "00010", "00010", "01100"),
    "~": ("00000", "00000", "01001", "10110", "00000", "00000", "00000"),
}

# Trim empty side columns once, so the font is proportional: narrow
# letters (i, l, t, f) take less room than wide ones (m, w).
_TRIM = {}
for _ch, _rows in FONT.items():
    _cols = [c for c in range(5) if any(r[c] == "1" for r in _rows)]
    if _cols:
        _TRIM[_ch] = (min(_cols), max(_cols))
    else:
        _TRIM[_ch] = (0, -1)  # blank glyph


def glyph_width(ch, scale):
    lo, hi = _TRIM.get(ch, _TRIM["?"])
    if hi < lo:
        return 3 * scale  # space
    # Trimmed glyph width plus a half-cell of tracking: a condensed face
    # that still reads at small sizes.
    return (hi - lo + 1) * scale + max(1, scale // 2)


def text_width(text, scale):
    return sum(glyph_width(c, scale) for c in text)


def wrap_text(text, scale, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

# ------------------------------------------------------------------ canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        r, g, b = color
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = r, g, b

    def hline(self, x, y, w, color, thick=1):
        self.fill_rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.fill_rect(x, y, thick, h, color)

    def circle(self, cx, cy, r, color, thick=1):
        # Midpoint circle outline.
        x, y, d = 0, r, 1 - r
        while x <= y:
            for dx, dy in ((x, y), (y, x), (-x, y), (-y, x),
                           (x, -y), (y, -x), (-x, -y), (-y, -x)):
                self.fill_rect(cx + dx - thick // 2, cy + dy - thick // 2,
                               thick, thick, color)
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1

    def draw_text(self, x, y, text, scale, color, bold=False):
        """Draw text at (x, y); returns the width drawn."""
        cx = x
        for ch in text:
            rows = FONT.get(ch, FONT["?"])
            lo, hi = _TRIM.get(ch, _TRIM["?"])
            if hi >= lo:
                for ry, row in enumerate(rows):
                    for rx in range(lo, hi + 1):
                        if row[rx] == "1":
                            px, py = cx + (rx - lo) * scale, y + ry * scale
                            self.fill_rect(px, py, scale, scale, color)
                            if bold:
                                self.fill_rect(px + max(1, scale // 2), py,
                                               scale, scale, color)
            cx += glyph_width(ch, scale)
        return cx - x

    def draw_lines(self, x, y, lines, scale, color, leading=None, bold=False):
        """Draw wrapped lines; returns the height used."""
        lh = leading if leading is not None else 7 * scale + max(2, scale * 2)
        for i, line in enumerate(lines):
            self.draw_text(x, y + i * lh, line, scale, color, bold=bold)
        return len(lines) * lh

    def draw_tag(self, x, y, label, scale, color):
        """A small filled colour chip with white text, e.g. CLIMATE."""
        pad = 2 * scale
        tw = text_width(label, scale)
        self.fill_rect(x, y, tw + 2 * pad, 7 * scale + 2 * pad, color)
        self.draw_text(x + pad, y + pad, label, scale, PAPER, bold=True)
        return tw + 2 * pad


# -------------------------------------------------------------- PNG writer
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    return out + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def write_png(canvas, path):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        raw += canvas.px[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)

# ------------------------------------------------------------- the day's news
# Every story below was reported on Monday 23 November 2026 (or over the
# weekend and first summarised that day) by BBC, Reuters, AP, NYT, NPR,
# WSJ, Al Jazeera, Axios, WIRED, OkayAfrica and others. Headlines are
# written as plain statements of what was reported; nothing is invented.

HERO = {
    "region": "CLIMATE",
    "place": "ANTALYA, TURKEY",
    "headline": "COP31 collapses: no deal as the fossil-fuel fight sinks the climate talks",
    "summary": (
        "Two weeks of UN talks ended on Sunday, two days late and with no "
        "agreement - the longest climate summit ever, and the first to "
        "collapse since 2009. The EU and island states rejected a draft "
        "that never mentioned fossil fuels; about 90 nations signed a side "
        "pledge to lift electricity to 35% of energy use by 2035."
    ),
}

LEADS = [
    {
        "region": "MARKETS",
        "headline": "Nvidia brings back Jensen Huang as CEO; shares soar 30%",
        "summary": (
            "Nvidia's board brought back its co-founder, 11 days after "
            "he quit. S&P 500 +4.8%."
        ),
    },
    {
        "region": "MIDDLE EAST",
        "headline": "Iran vows to fight US blockade as Trump warns of strikes",
        "summary": (
            "Tehran vows all means against the US blockade; Trump warns "
            "strikes may resume."
        ),
    },
    {
        "region": "UKRAINE",
        "headline": "Zelenskyy confirms Ukraine hit Russian warship in Libya",
        "summary": (
            "Seven sea drones struck the corvette Merkury. Moscow cried "
            "'terrorist activity'."
        ),
    },
    {
        "region": "AMERICAS",
        "headline": "Democrats take largest House majority since 1992",
        "summary": (
            "Democrats won 258+ seats; Hubbard beat Foxx "
            "by 330 votes in N. Carolina."
        ),
    },
]

# Compact stories: one complete sentence each, kept short enough to fit
# two lines in a column. A coloured square marks the region; the legend
# above the columns names the colours.
COMPACT = [
    ("UKRAINE", "Drone strike levels Dymer flats: 11 dead, 14 missing."),
    ("UKRAINE", "Russian attacks on Kryvyi Rih kill 11, incl. a child."),
    ("EUROPE", "Russian cargo ship hit by drones in the Baltic."),
    ("EUROPE", "NATO vows to defend Poland 'every inch'."),
    ("EUROPE", "Denmark expels Russian attache over Kyivstoner plot."),
    ("EUROPE", "Russia plans a nuclear-armed satellite, NATO spies say."),
    ("EUROPE", "EU proposes a 22nd sanctions package on Russia."),
    ("MIDDLE EAST", "Iranian missiles hit a civilian site in Bahrain."),
    ("MIDDLE EAST", "Israeli strike hits Gaza truck; three killed."),
    ("MIDDLE EAST", "Eisenkot calls settler arson 'Jewish terrorism'."),
    ("AMERICAS", "'Chapo Isidro' seized by Mexico in Sinaloa."),
    ("AMERICAS", "Masked ICE agents detain father, daughter in Seattle."),
    ("AMERICAS", "Judge keeps Oscar Belgal jailed after ICE shooting."),
    ("AMERICAS", "Army to detonate bomb chemicals in Iowa."),
    ("AMERICAS", "Court scraps pregnant-workers law."),
    ("AMERICAS", "Second judge blocks Trump's 'triumphal arch'."),
    ("AMERICAS", "Judge blocks shift of housing aid to treatment-first."),
    ("AMERICAS", "Trump plays down breach of the FBI's database."),
    ("SPORT", "Broncos 38, Raiders 24; Chiefs 34, Cardinals 7."),
    ("AMERICAS", "RFK Jr. gives $47m to test diet, exercise for Medicare."),
    ("ASIA", "India pledges $1.62bn to Nepal after glacier flood."),
    ("ASIA", "S. Korea's Lee names first woman spy chief in reshuffle."),
    ("ASIA", "S. Korea education minister quits over AI exam rules."),
    ("ASIA", "Bangladesh vows to jail ex-PM Hasina if she returns."),
    ("ASIA", "Thai court cuts MP's jail term to 3 years."),
    ("AFRICA", "Kenya, DR Congo restore ambassador ties."),
    ("AFRICA", "African oil exporters gained $21.6bn in Iran war."),
    ("AFRICA", "South Sudan delays first election to Feb 2027."),
    ("TECH", "SEC is probing Nvidia's accounting, sources say."),
    ("TECH", "Oregon, Virginia sue SpaceX over Grok safety claims."),
]

# ------------------------------------------------------------------ layout
MARGIN = 28
CONTENT_W = W - 2 * MARGIN  # 968


def draw_globe(c, cx, cy, r, color):
    """A small line-drawn globe: circle, meridian, equator, parallels."""
    c.circle(cx, cy, r, color, thick=2)
    import math
    for t in range(0, 360, 3):
        a = math.radians(t)
        c.set(int(cx + (r // 2) * math.cos(a)), int(cy + r * math.sin(a)), color)
        c.set(int(cx - (r // 2) * math.cos(a)), int(cy + r * math.sin(a)), color)
    c.hline(cx - r, cy, 2 * r, color)
    half = int((r * r - (r // 2) * (r // 2)) ** 0.5)
    c.hline(cx - half, cy - r // 2, 2 * half, color)
    c.hline(cx - half, cy + r // 2, 2 * half, color)


def draw_masthead(c):
    draw_globe(c, 62, 48, 24, BLUE)
    title = "THE WORLD TODAY"
    tw = text_width(title, 7)
    c.draw_text((W - tw) // 2, 18, title, 7, INK, bold=True)
    date = "MONDAY 23 NOVEMBER 2026"
    dw = text_width(date, 3)
    c.draw_text((W - dw) // 2, 76, date, 3, RED, bold=True)
    c.hline(MARGIN, 106, CONTENT_W, RULE, thick=3)
    c.hline(MARGIN, 112, CONTENT_W, RULE, thick=1)


def draw_hero(c, y):
    tag = HERO["region"]
    w = c.draw_tag(MARGIN, y, tag, 2, REGION_COLOR[tag])
    place = HERO["place"]
    c.draw_text(MARGIN + w + 10, y + 2, place, 2, MUTED, bold=True)
    head_lines = wrap_text(HERO["headline"], 4, CONTENT_W)
    assert len(head_lines) <= 2, head_lines
    hy = y + 32
    c.draw_lines(MARGIN, hy, head_lines, 4, INK, leading=36, bold=True)
    sum_lines = wrap_text(HERO["summary"], 2, CONTENT_W)
    assert len(sum_lines) <= 4, sum_lines
    sy = hy + len(head_lines) * 36 + 8
    c.draw_lines(MARGIN, sy, sum_lines, 2, INK, leading=17)
    return sy + len(sum_lines) * 17


def draw_leads(c, y):
    col_w = (CONTENT_W - 20) // 2  # 474
    row_h = 118
    for i, lead in enumerate(LEADS):
        x = MARGIN + (i % 2) * (col_w + 20)
        yy = y + (i // 2) * (row_h + 10)
        tag = lead["region"]
        c.draw_tag(x, yy, tag, 2, REGION_COLOR[tag])
        head_lines = wrap_text(lead["headline"], 3, col_w)
        assert len(head_lines) <= 2, head_lines
        hy = yy + 28
        c.draw_lines(x, hy, head_lines, 3, INK, leading=26, bold=True)
        sum_lines = wrap_text(lead["summary"], 2, col_w)
        assert len(sum_lines) <= 2, sum_lines
        sy = hy + len(head_lines) * 26 + 4
        c.draw_lines(x, sy, sum_lines, 2, MUTED, leading=17)
    return y + 2 * row_h + 10


def draw_compact(c, y):
    # Legend of the region colours.
    legend = [("CLIMATE", GREEN), ("MARKETS", BLUE), ("MIDDLE EAST", BROWN),
              ("EUROPE", PURPLE), ("AMERICAS", RED), ("ASIA", ORANGE),
              ("AFRICA", TEAL), ("SPORT", SLATE)]
    total = 0
    for label, _ in legend:
        total += 10 + 4 + text_width(label, 2) + 16
    total -= 16
    x = (W - total) // 2
    for label, color in legend:
        c.fill_rect(x, y + 2, 10, 10, color)
        x += 14
        x += c.draw_text(x, y, label, 2, MUTED, bold=True)
        x += 16
    # Three columns of ten stories each.
    col_w = (CONTENT_W - 2 * 16) // 3  # 312
    line_h = 16
    gap = 5
    top = y + 24
    for i, (region, text) in enumerate(COMPACT):
        col = i // 10
        row = i % 10
        x = MARGIN + col * (col_w + 16)
        yy = top + row * (2 * line_h + gap)
        lines = wrap_text(text, 2, col_w - 16)
        assert len(lines) <= 2, (region, text, lines)
        c.fill_rect(x, yy + 2, 10, 10, REGION_COLOR[region])
        c.draw_lines(x + 16, yy, lines, 2, INK, leading=line_h)
    return top + 10 * (2 * line_h + gap) - gap


def draw_footer(c, y):
    c.hline(MARGIN, y, CONTENT_W, RULE, thick=1)
    foot = "Sources: BBC, Reuters, AP, NYT, NPR, WSJ, Al Jazeera, Axios, WIRED, OkayAfrica"
    fw = text_width(foot, 2)
    c.draw_text((W - fw) // 2, y + 8, foot, 2, MUTED)


def build():
    c = Canvas(W, H, PAPER)
    draw_masthead(c)
    end = draw_hero(c, 122)
    c.hline(MARGIN, end + 8, CONTENT_W, RULE, thick=1)
    end = draw_leads(c, end + 16)
    c.hline(MARGIN, end + 8, CONTENT_W, RULE, thick=1)
    end = draw_compact(c, end + 14)
    draw_footer(c, end + 8)
    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    canvas = build()
    path = os.path.join(out_dir, "entry.png")
    size = write_png(canvas, path)
    print(f"wrote {path} ({size} bytes)")


if __name__ == "__main__":
    main()
