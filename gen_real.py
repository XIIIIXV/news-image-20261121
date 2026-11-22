#!/usr/bin/env python3
"""news-image-20261121 REAL build — 'THE WORLD IN ONE PAGE'.
Fresh generator written for the real (final) entry, 22 Nov 2026.
PIL + DejaVu only. Deterministic: no time/random input, fixed layout.
Reads nothing at runtime; every story is embedded below, date-checked
to Saturday 21 November 2026 by the builder (see BUILD-NOTES-REAL.md).
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 14
CW = W - 2 * MARGIN  # 996

PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (16, 35, 63)
NAVY2 = (28, 58, 96)
RED = (179, 39, 30)
GOLD = (200, 155, 60)
TEAL = (14, 124, 123)
GREY = (91, 103, 112)
LINE = (196, 188, 172)
CARD = (255, 255, 255)
SKY = (214, 228, 238)

FDIR = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(FDIR + name, size)

FB = lambda s: font("DejaVuSans-Bold.ttf", s)
FR = lambda s: font("DejaVuSans.ttf", s)
FI = lambda s: font("DejaVuSans-Oblique.ttf", s)

PILL = {
    "CONFIRMED": (14, 124, 123),
    "OFFICIAL": (31, 95, 191),
    "REPORTED": (91, 103, 112),
    "CLAIM": (183, 121, 31),
}

# ---------------------------------------------------------------- stories
# fields: n, city, region(short), headline, deck, source, pill, motif
LEADS = [
    dict(n=1, city="BAHRAIN", region="MID EAST",
         head="Iran hits Bahrain plant; two tankers struck",
         deck="Missile-and-drone barrage sets a Sitra site ablaze; two tankers hit near Hormuz.",
         src="REUTERS · UKMTO", pill="REPORTED", motif="missile"),
    dict(n=2, city="RIYADH", region="MID EAST",
         head="Saudi defences down three Houthi missiles",
         deck="Intercepts over Riyadh early Saturday, days after the PIF tower was hit.",
         src="REUTERS", pill="REPORTED", motif="shield"),
    dict(n=3, city="JUNIN", region="AMERICAS",
         head="M6.7 quake shakes central Peru",
         deck="Tremor at 00:09 UTC near Junin, 108 km deep. One dead, 16 hurt, 853 displaced.",
         src="USGS · AFP", pill="REPORTED", motif="quake"),
]

SMALL = [
    dict(n=4, city="ANTALYA", region="EUROPE",
         head="COP31 in overtime; text drops fossil fuels",
         deck="Kurum's last-minute draft omits fossil fuels; vote set for 06:00 GMT Sunday.",
         src="AP · REUTERS", pill="REPORTED", motif="cop"),
    dict(n=5, city="WARSAW", region="EUROPE",
         head="Rutte vows NATO will defend Poland",
         deck="In Warsaw after Friday breach; NATO council meets Monday.",
         src="REUTERS", pill="REPORTED", motif="nato"),
    dict(n=6, city="MERCURY", region="SPACE",
         head="BepiColombo enters Mercury orbit",
         deck="Four thrusters fire 37 minutes at 18:24 UTC after an eight-year voyage.",
         src="ESA · NATURE", pill="REPORTED", motif="space"),
    dict(n=7, city="GUASAVE", region="AMERICAS",
         head="'El Chapo Isidro' seized; 11 dead",
         deck="FBI most-wanted boss seized in Guasave; 4 soldiers dead.",
         src="CNN · AP", pill="REPORTED", motif="raid"),
    dict(n=8, city="BRUSSELS", region="EUROPE",
         head="EU and Indonesia sign CEPA trade deal",
         deck="98.5% of tariffs cut after a decade of talks; in force targeted for 2027.",
         src="EU · AFP", pill="OFFICIAL", motif="trade"),
    dict(n=9, city="BANDA SEA", region="ASIA",
         head="M6.8 quake strikes Banda Sea",
         deck="226 km north-east of Dili, 117 km deep; no tsunami threat, GFZ says.",
         src="GFZ · REUTERS", pill="REPORTED", motif="quake2"),
    dict(n=10, city="GULF OF FINLAND", region="EUROPE",
         head="Drones hit Russian ship Sparta II",
         deck="Fire in Gulf of Finland; 16 crew rescued as vessel drifts into Finnish waters.",
         src="REUTERS · BBC", pill="REPORTED", motif="ship"),
    dict(n=11, city="GENEVA", region="EUROPE",
         head="UN 'killer robot' talks end with no rules",
         deck="128 states agree only to keep talking; a pact may come by 2028.",
         src="AP · REUTERS", pill="REPORTED", motif="robot"),
    dict(n=12, city="LAS VEGAS", region="AMERICAS",
         head="Verstappen wins thrilling Las Vegas GP",
         deck="35 lead changes; Norris 2nd by 0.639s; Russell crashes out late.",
         src="REUTERS · F1", pill="REPORTED", motif="race"),
    dict(n=13, city="GAZA CITY", region="MID EAST",
         head="Strike kills three in Gaza food vehicle",
         deck="IDF says militants; witnesses dispute it. Hamas seeks mediator talks.",
         src="REUTERS · AL JAZEERA", pill="CLAIM", motif="gaza"),
]

# briefs: n, city, text (<= ~80 chars incl. source), source
BRIEFS = [
    (14, "HORMUZ", "Iran says it downed two US drones.", "IRIB"),
    (15, "PARIS", "Depardieu, Houellebecq face sex-crime inquiry.", "REUTERS"),
    (16, "JOHANNESBURG", "ANC battles to hold cities after worst vote.", "BBC"),
    (17, "HODEIDAH", "Saudi jets strike Hodeidah again on Saturday.", "XINHUA"),
    (18, "WASHINGTON", "Trump plays down FBI database breach.", "CNN"),
    (19, "BRASILIA", "Bolsonaro moved to ICU over bowel blockage.", "REUTERS"),
    (20, "OXFORD", "AI-assisted Riemann proof passes checks.", "SCI. AM."),
    (21, "KHARAGPUR", "Google gives $5m for AI research at IIT.", "HINDU"),
    (22, "SEOUL", "Korea chip exports hit $303bn in Jan-Oct.", "ETODAY"),
    (23, "ODISHA", "Cyclone Akvan weakens; 372,000 evacuated.", "IMD"),
    (24, "BITCOIN", "BTC hits $55,130 two-year low, rebounds over $60k.", "COINDESK"),
    (25, "BASRA", "Hartha power-station fire kills 4, injures 30.", "REUTERS"),
    (26, "PARIS", "France marches shrink: 82,500 out, 70,000 police.", "REUTERS"),
    (27, "LONDON", "England rout All Blacks 37-12, record margin.", "AP"),
    (28, "VANDENBERG", "Falcon 9 launches classified USSF-317.", "SFLIGHTNOW"),
    (29, "WELLINGTON", "Rahul 136 puts India 486/4, 118 ahead.", "AFP"),
    (30, "OSAKA", "BTS take five MAMA awards; CORTIS wins song.", "YONHAP"),
    (31, "NEWCASTLE", "Arsenal held 2-2; keeper Raya hurt.", "REUTERS"),
    (32, "BAYELSA", "Nigeria boat toll rises to 24 after Friday sinking.", "REUTERS"),
    (33, "CHANDEL", "Manipur liquor toll climbs to 16; 600 in hospital.", "PTI"),
    (34, "BELO HORIZONTE", "Wolbachia mosquitoes cut dengue ~69%.", "AP"),
    (35, "VINNYTSIA", "Russian strike hits energy site; part of city dark.", "H.UA"),
    (36, "KRYVYI RIH", "Toll from Friday missile strike climbs to 47 hurt.", "NOVYNY"),
]

REGIONS = [("MIDDLE EAST", 6), ("EUROPE", 12), ("AMERICAS", 6),
           ("ASIA", 6), ("AFRICA", 2), ("OCEANIA", 1),
           ("SPACE", 2), ("GLOBAL", 1)]

NUMBERS = [("36", "STORIES"), ("8", "REGIONS"),
           ("11", "DEAD IN GUASAVE RAID"),
           ("372,000", "EVACUATED: AKVAN"),
           ("$55,130", "BTC TWO-YEAR LOW"),
           ("98.5%", "TARIFFS CUT: CEPA")]

UTC_STRIP = [("JUNIN", "00:09"), ("RIYADH", "00:18"), ("BASRA", "03:00"),
             ("GENEVA", "03:45"), ("VANDENBERG", "04:20"),
             ("BANDA SEA", "09:42"), ("MERCURY", "18:24")]

# map pins: n, lon, lat, label offset (dx, dy) for the number badge
PINS = [
    (1, 50.6, 26.2, 0, 0), (2, 46.7, 24.7, 14, 12),
    (3, -75.9, -11.2, 0, 0), (4, 30.7, 36.9, 18, 10),
    (5, 21.0, 52.2, 14, -14), (7, -108.5, 25.6, 0, 0),
    (8, 4.35, 50.85, -24, -12), (9, 127.5, -6.8, 0, 0),
    (10, 27.0, 59.8, 16, -14), (11, 6.14, 46.2, -12, 12),
    (12, -115.1, 36.2, 0, -14), (13, 34.5, 31.5, 16, -12),
]

DATE_CHECK = (
    "NOT 21 NOV — LEFT OUT: Kyiv launcher strikes · EU €1bn Ukraine aid · Denmark–Greenland pact · "
    "daraxonrasib pill · FBI breach report (20 Nov) · homeless ruling · Hodeidah strikes (Fri) · PIF tower strike (Thu) · "
    "Kyiv barrage + Poland missile crash (20 Nov) · Akvan landfall (20 Nov) · S&P/Dow correction (20 Nov) · "
    "Nigeria boat sinking (Fri — toll update Sat) · Manipur deaths (18–20 Nov — toll update Sat) · "
    "Kryvyi Rih strike (Fri — toll update Sat).  NOT YET 22 NOV: COP31 final vote 06:00 GMT Sun · BepiColombo MPO/Mio split 9–10 Dec · Nepal PM India visit."
)

# ---------------------------------------------------------------- helpers
def tw(draw, text, f):
    return draw.textlength(text, font=f)

def wrap(draw, text, f, maxw):
    """Greedy word wrap; returns list of lines, each <= maxw."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def fit_font(draw, text, name, start, minsize, maxw):
    """Largest font size >= minsize whose text fits maxw; returns (font, size)."""
    size = start
    while size > minsize and draw.textlength(text, font=font(name, size)) > maxw:
        size -= 1
    return font(name, size), size

def pill(draw, x, y, label):
    """Status pill, right-aligned at x. Returns left edge."""
    f = FB(8)
    w = draw.textlength(label, font=f) + 12
    col = PILL[label]
    draw.rounded_rectangle([x - w, y, x, y + 14], radius=7, fill=col)
    draw.text((x - w + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return x - w

def source_pill_row(draw, x, y, w, src, label):
    """Bottom strip of a card: source left, pill right. Region never overlaps."""
    f = FR(8)
    px = pill(draw, x + w, y, label)
    # shrink source until it fits before the pill
    s = 8
    while s > 6 and draw.textlength(src, font=font("DejaVuSans.ttf", s)) > px - x - 6:
        s -= 1
    draw.text((x, y + 1), src, font=font("DejaVuSans.ttf", s), fill=GREY)

# ---------------------------------------------------------------- motifs
# Flat pictograms, drawn with PIL shapes only. Each takes (draw, x, y, w, h).

def _sky(draw, x, y, w, h, top, bot):
    for i in range(h):
        t = i / max(h - 1, 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        draw.line([(x, y + i), (x + w, y + i)], fill=c)

def _missile(draw, x, y, w, h):
    _sky(draw, x, y, w, h, (24, 42, 72), (90, 70, 60))
    for i in range(3):
        bx = x + w * (0.20 + 0.30 * i)
        by = y + h * (0.55 + 0.10 * i)
        # diagonal rocket body with flame trail
        draw.line([(bx - 26, by + 26), (bx, by)], fill=(255, 190, 90), width=4)
        draw.polygon([(bx, by - 12), (bx + 12, by + 2), (bx + 2, by + 12), (bx - 8, by + 4)],
                     fill=(235, 235, 235))
        draw.polygon([(bx + 12, by + 2), (bx + 20, by + 8), (bx + 6, by + 12)],
                     fill=(255, 120, 40))
    draw.ellipse([x + w - 26, y + 6, x + w - 10, y + 22], fill=(255, 220, 130))

def _shield(draw, x, y, w, h):
    _sky(draw, x, y, w, h, (16, 60, 90), (40, 110, 130))
    cx, cy = x + w // 2, y + h // 2 + 2
    draw.polygon([(cx - 26, cy - 20), (cx + 26, cy - 20), (cx + 26, cy + 2),
                  (cx, cy + 26), (cx - 26, cy + 2)], fill=(240, 200, 90),
                 outline=(255, 255, 255))
    draw.line([(cx - 12, cy), (cx - 3, cy + 9), (cx + 14, cy - 10)],
              fill=(16, 60, 90), width=4)

def _quake(draw, x, y, w, h):
    _sky(draw, x, y, w, h, (120, 90, 60), (70, 55, 45))
    pts = []
    for i in range(9):
        pts.append((x + 6 + i * (w - 12) / 8, y + h * (0.30 + (0.25 if i % 2 else -0.12))))
    draw.line(pts, fill=(255, 240, 200), width=3, joint="curve")
    draw.polygon([(x, y + h), (x, y + h - 18), (x + w * 0.3, y + h - 26),
                  (x + w * 0.45, y + h - 12), (x + w * 0.7, y + h - 24),
                  (x + w, y + h - 14), (x + w, y + h)], fill=(40, 32, 26))

def _cop(draw, x, y, w, h):
    _sky(draw, x, y, w, h, (30, 90, 70), (140, 180, 120))
    # sun top-left, leaf centre
    draw.ellipse([x + 10, y + 8, x + 30, y + 28], fill=(255, 220, 100))
    for a in range(0, 360, 45):
        import math
        r = math.radians(a)
        draw.line([(x + 20 + 13 * math.cos(r), y + 18 + 13 * math.sin(r)),
                   (x + 20 + 18 * math.cos(r), y + 18 + 18 * math.sin(r))],
                  fill=(255, 220, 100), width=2)
    cx, cy = x + w // 2 + 8, y + h // 2 + 6
    draw.polygon([(cx - 22, cy + 12), (cx - 6, cy - 16), (cx + 22, cy - 10), (cx + 6, cy + 16)],
                 fill=(60, 140, 80))
    draw.line([(cx - 18, cy + 10), (cx + 18, cy - 8)], fill=(220, 255, 220), width=2)
    for i, (lx, ly) in enumerate([(x + w - 16, y + 12), (x + 14, y + h - 14)]):
        draw.ellipse([lx - 4, ly - 6, lx + 4, ly + 6], fill=(120, 200, 90))

def _nato(draw, x, y, w, h):
    _sky(draw, x, y, w, h, (16, 35, 63), (50, 80, 130))
    cx, cy = x + w // 2, y + h // 2
    for ang in range(0, 360, 90):
        import math
        a = math.radians(ang)
        ex, ey = cx + 26 * math.cos(a), cy + 26 * math.sin(a)
        draw.polygon([(cx, cy), (cx + 7 * math.cos(a + 0.5), cy + 7 * math.sin(a + 0.5)),
                      (ex, ey), (cx + 7 * math.cos(a - 0.5), cy + 7 * math.sin(a - 0.5))],
                     fill=(255, 255, 255))
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(240, 200, 90))

def _space(draw, x, y, w, h):
    _sky(draw, x, y, w, h, (8, 10, 26), (30, 30, 60))
    for sx, sy in [(x + 10, y + 8), (x + w - 12, y + 14), (x + w // 2, y + 6), (x + 16, y + h - 12)]:
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    cx, cy = x + w // 2 - 8, y + h // 2 + 4
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(200, 120, 70))
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=(255, 200, 140))
    draw.ellipse([cx + 22, cy - 26, cx + 34, cy - 14], fill=(220, 220, 220))
    draw.line([(cx + 22, cy - 14), (cx + 34, cy - 26)], fill=(220, 220, 220), width=2)
    draw.arc([cx - 34, cy - 8, cx + 34, cy + 34], 200, 340, fill=(255, 220, 130), width=2)

def _raid(draw, x, y, w, h):
    _sky(draw, x, y, w, h, (60, 60, 70), (110, 100, 80))
    draw.rectangle([x + w * 0.15, y + h * 0.35, x + w * 0.85, y + h * 0.9], fill=(200, 180, 140))
    for i in range(3):
        draw.rectangle([x + w * (0.22 + 0.24 * i), y + h * 0.45,
                        x + w * (0.36 + 0.24 * i), y + h * 0.62], fill=(40, 40, 50))
    draw.polygon([(x + w // 2, y + h * 0.12), (x + w // 2 + 12, y + h * 0.3),
                  (x + w // 2 - 12, y + h * 0.3)], fill=(240, 200, 90))
    draw.ellipse([x + w // 2 - 4, y + h * 0.3, x + w // 2 + 4, y + h * 0.38], fill=(240, 200, 90))

def _trade(draw, x, y, w, h):
    _sky(draw, x, y, w, h, (20, 70, 110), (70, 130, 170))
    draw.ellipse([x + w - 30, y + 6, x + w - 8, y + 28], fill=(255, 220, 100))
    draw.rectangle([x + 8, y + h - 26, x + w - 8, y + h - 12], fill=(240, 200, 90))
    for i, col in enumerate([(180, 60, 50), (50, 120, 90), (60, 90, 160)]):
        draw.rectangle([x + 12 + i * (w - 24) // 3, y + h - 52,
                        x + 12 + (i + 1) * (w - 24) // 3 - 4, y + h - 26], fill=col)
        draw.rectangle([x + 12 + i * (w - 24) // 3, y + h - 52,
                        x + 12 + (i + 1) * (w - 24) // 3 - 4, y + h - 26],
                       outline=(255, 255, 255))

def _quake2(draw, x, y, w, h):
    _sky(draw, x, y, w, h, (10, 60, 90), (30, 100, 120))
    for i in range(3):
        yy = y + h * (0.55 + 0.15 * i)
        draw.arc([x + 6, yy - 8, x + w - 6, yy + 22], 0, 180, fill=(255, 255, 255), width=2)
    pts = []
    for i in range(9):
        pts.append((x + 6 + i * (w - 12) / 8, y + h * (0.22 + (0.16 if i % 2 else -0.08))))
    draw.line(pts, fill=(255, 220, 120), width=3, joint="curve")

def _ship(draw, x, y, w, h):
    _sky(draw, x, y, w, h, (90, 90, 95), (150, 150, 150))
    draw.polygon([(x + 10, y + h * 0.55), (x + w - 10, y + h * 0.55),
                  (x + w - 22, y + h * 0.8), (x + 22, y + h * 0.8)], fill=(120, 40, 30))
    draw.rectangle([x + w * 0.35, y + h * 0.3, x + w * 0.6, y + h * 0.55], fill=(220, 220, 220))
    for i in range(3):
        draw.ellipse([x + w * (0.3 + 0.18 * i), y + 6 + i * 4,
                      x + w * (0.42 + 0.18 * i), y + 18 + i * 4], fill=(80, 80, 80))
    draw.line([(x, y + h - 8), (x + w, y + h - 8)], fill=(40, 90, 130), width=3)

def _robot(draw, x, y, w, h):
    _sky(draw, x, y, w, h, (40, 45, 60), (80, 85, 100))
    cx, cy = x + w // 2, y + h // 2 + 2
    draw.line([(cx, cy - 34), (cx, cy - 22)], fill=(200, 200, 200), width=3)
    draw.ellipse([cx - 4, cy - 38, cx + 4, cy - 30], fill=(255, 80, 80))
    draw.rounded_rectangle([cx - 24, cy - 22, cx + 24, cy + 18], radius=8,
                           fill=(200, 205, 210), outline=(255, 255, 255))
    draw.ellipse([cx - 14, cy - 12, cx - 4, cy - 2], fill=(20, 120, 160))
    draw.ellipse([cx + 4, cy - 12, cx + 14, cy - 2], fill=(20, 120, 160))
    draw.line([(cx - 12, cy + 8), (cx + 12, cy + 8)], fill=(60, 60, 60), width=3)

def _race(draw, x, y, w, h):
    _sky(draw, x, y, w, h, (20, 20, 30), (70, 70, 80))
    for r in range(2):
        for c in range(4):
            if (r + c) % 2 == 0:
                draw.rectangle([x + 8 + c * 10, y + 8 + r * 10, x + 18 + c * 10, y + 18 + r * 10],
                               fill=(255, 255, 255))
    draw.line([(x + 48, y + 8), (x + 48, y + 34)], fill=(200, 200, 200), width=3)
    draw.polygon([(x + w * 0.3, y + h - 18), (x + w * 0.85, y + h - 18),
                  (x + w * 0.8, y + h - 8), (x + w * 0.35, y + h - 8)], fill=(200, 40, 30))
    draw.ellipse([x + w * 0.42, y + h - 10, x + w * 0.5, y + h - 2], fill=(20, 20, 20))
    draw.ellipse([x + w * 0.68, y + h - 10, x + w * 0.76, y + h - 2], fill=(20, 20, 20))

def _gaza(draw, x, y, w, h):
    _sky(draw, x, y, w, h, (150, 130, 100), (190, 175, 140))
    draw.rectangle([x + w * 0.2, y + h * 0.4, x + w * 0.8, y + h * 0.85], fill=(240, 240, 235))
    draw.rectangle([x + w * 0.44, y + h * 0.48, x + w * 0.56, y + h * 0.72], fill=(180, 40, 30))
    draw.rectangle([x + w * 0.38, y + h * 0.56, x + w * 0.62, y + h * 0.64], fill=(180, 40, 30))
    draw.line([(x, y + h - 6), (x + w, y + h - 6)], fill=(90, 80, 60), width=3)

MOTIFS = {"missile": _missile, "shield": _shield, "quake": _quake, "cop": _cop,
          "nato": _nato, "space": _space, "raid": _raid, "trade": _trade,
          "quake2": _quake2, "ship": _ship, "robot": _robot, "race": _race,
          "gaza": _gaza}

# ---------------------------------------------------------------- cards
def draw_lead(draw, x, y, w, h, st):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=CARD, outline=LINE)
    ill_h = 78
    MOTIFS[st["motif"]](draw, x + 1, y + 1, w - 2, ill_h)
    # number badge on illustration
    draw.ellipse([x + 8, y + 8, x + 30, y + 30], fill=NAVY)
    draw.text((x + 19, y + 12), str(st["n"]), font=FB(12), fill=(255, 255, 255), anchor="mm")
    ty = y + ill_h + 8
    # header: city left, region chip right (shrinks, never dropped)
    fcity, _ = fit_font(draw, st["city"], "DejaVuSans-Bold.ttf", 13, 8, w - 110)
    draw.text((x + 8, ty), st["city"], font=fcity, fill=RED)
    rf, _ = fit_font(draw, st["region"], "DejaVuSans-Bold.ttf", 8, 7, 64)
    rw = draw.textlength(st["region"], font=rf) + 10
    draw.rounded_rectangle([x + w - 8 - rw, ty, x + w - 8, ty + 14], radius=7, fill=NAVY2)
    draw.text((x + w - 8 - rw / 2, ty + 7), st["region"], font=rf, fill=(255, 255, 255), anchor="mm")
    ty += 18
    for ln in wrap(draw, st["head"], FB(15), w - 16):
        draw.text((x + 8, ty), ln, font=FB(15), fill=INK)
        ty += 18
    ty += 2
    for ln in wrap(draw, st["deck"], FR(11), w - 16):
        draw.text((x + 8, ty), ln, font=FR(11), fill=(50, 50, 50))
        ty += 13
    if ty > y + h - 20:
        print(f"OVERFLOW lead {st['n']}: content bottom {ty}, strip at {y + h - 20}")
    source_pill_row(draw, x + 8, y + h - 20, w - 16, st["src"], st["pill"])
    return ty

def draw_small(draw, x, y, w, h, st):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=5, fill=CARD, outline=LINE)
    ill_h = 42
    MOTIFS[st["motif"]](draw, x + 1, y + 1, w - 2, ill_h)
    draw.ellipse([x + 6, y + 6, x + 24, y + 24], fill=NAVY)
    draw.text((x + 15, y + 15), str(st["n"]), font=FB(10), fill=(255, 255, 255), anchor="mm")
    ty = y + ill_h + 6
    fcity, _ = fit_font(draw, st["city"], "DejaVuSans-Bold.ttf", 10, 7, w - 76)
    draw.text((x + 6, ty), st["city"], font=fcity, fill=RED)
    rf, _ = fit_font(draw, st["region"], "DejaVuSans-Bold.ttf", 7, 6, 58)
    rw = draw.textlength(st["region"], font=rf) + 8
    draw.rounded_rectangle([x + w - 6 - rw, ty, x + w - 6, ty + 12], radius=6, fill=NAVY2)
    draw.text((x + w - 6 - rw / 2, ty + 6), st["region"], font=rf, fill=(255, 255, 255), anchor="mm")
    ty += 15
    for ln in wrap(draw, st["head"], FB(11), w - 12):
        draw.text((x + 6, ty), ln, font=FB(11), fill=INK)
        ty += 13
    ty += 1
    for ln in wrap(draw, st["deck"], FR(9), w - 12):
        draw.text((x + 6, ty), ln, font=FR(9), fill=(50, 50, 50))
        ty += 11
    if ty > y + h - 17:
        print(f"OVERFLOW small {st['n']}: content bottom {ty}, strip at {y + h - 17}")
    source_pill_row(draw, x + 6, y + h - 17, w - 12, st["src"], st["pill"])
    return ty

# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = MARGIN
    log = []

    # masthead
    mh = 58
    d.rounded_rectangle([MARGIN, y, W - MARGIN, y + mh], radius=6, fill=NAVY)
    d.text((W // 2, y + 9), "THE WORLD IN ONE PAGE", font=FB(10),
           fill=(200, 155, 60), anchor="ma")
    d.text((W // 2, y + 36), "SATURDAY 21 NOVEMBER 2026", font=FB(26),
           fill=(255, 255, 255), anchor="ma")
    y += mh + 5
    # legend + subtitle
    sub = "36 STORIES  ·  8 REGIONS  ·  EVERY FACT DATE-CHECKED TO 21 NOV 2026"
    d.text((MARGIN, y), sub, font=FB(10), fill=INK)
    leg = "CONFIRMED 2+ outlets   OFFICIAL authority   REPORTED one outlet   CLAIM one party, unverified"
    d.text((W - MARGIN, y), leg, font=FR(8), fill=GREY, anchor="ra")
    y += 16
    log.append(f"masthead_end={y}")
    # UTC strip
    uh = 26
    d.rounded_rectangle([MARGIN, y, W - MARGIN, y + uh], radius=5, fill=(255, 255, 255), outline=LINE)
    d.text((MARGIN + 8, y + 14), "THE DAY IN UTC", font=FB(9), fill=RED, anchor="lm")
    x0 = MARGIN + 118
    step = (CW - 118 - 8) / len(UTC_STRIP)
    for i, (city, t) in enumerate(UTC_STRIP):
        cx = x0 + step * i + step / 2
        d.text((cx, y + 6), city, font=FB(8), fill=INK, anchor="ma")
        d.text((cx, y + 17), t + " UTC", font=FR(8), fill=GREY, anchor="ma")
        if i:
            d.line([(x0 + step * i, y + 14), (x0 + step * i, y + 14)], fill=LINE, width=1)
    y += uh + 6
    log.append(f"utc_end={y}")

    # leads: 3 across
    lh = 190
    lw = (CW - 16) // 3
    for i, st in enumerate(LEADS):
        draw_lead(d, MARGIN + i * (lw + 8), y, lw, lh, st)
    y += lh + 6
    log.append(f"leads_end={y}")

    # small cards: 5 across x 2 rows
    sh = 130
    sw = (CW - 32) // 5
    for r in range(2):
        for c in range(5):
            st = SMALL[r * 5 + c]
            draw_small(d, MARGIN + c * (sw + 8), y, sw, sh, st)
        y += sh + 6
    y -= 6
    log.append(f"small_end={y}")
    y += 6

    # numbers bar
    nh = 34
    d.rounded_rectangle([MARGIN, y, W - MARGIN, y + nh], radius=5, fill=(255, 255, 255), outline=LINE)
    seg = CW / len(NUMBERS)
    for i, (num, lab) in enumerate(NUMBERS):
        cx = MARGIN + seg * i + seg / 2
        d.text((cx, y + 8), num, font=FB(13), fill=RED, anchor="ma")
        d.text((cx, y + 24), lab, font=FB(7), fill=GREY, anchor="ma")
        if i:
            d.line([(MARGIN + seg * i, y + 6), (MARGIN + seg * i, y + nh - 6)], fill=LINE)
    y += nh + 6
    log.append(f"numbers_end={y}")

    # region bar
    rh = 26
    d.rounded_rectangle([MARGIN, y, W - MARGIN, y + rh], radius=5, fill=NAVY2)
    seg = CW / len(REGIONS)
    for i, (name, cnt) in enumerate(REGIONS):
        cx = MARGIN + seg * i + seg / 2
        d.text((cx, y + 13), f"{name} {cnt}", font=FB(9), fill=(255, 255, 255), anchor="mm")
        if i:
            d.line([(MARGIN + seg * i, y + 5), (MARGIN + seg * i, y + rh - 5)], fill=(120, 140, 170))
    y += rh + 6
    log.append(f"regions_end={y}")

    # map
    map_h = 132
    map_top = y
    d.rounded_rectangle([MARGIN, y, W - MARGIN, y + map_h], radius=5, fill=SKY, outline=LINE)
    d.text((MARGIN + 8, y + 8), "WHERE IT HAPPENED", font=FB(9), fill=NAVY)
    d.text((W - MARGIN - 8, y + 8), "6 MERCURY — NOT ON EARTH: ORBIT CAPTURE 18:24 UTC",
           font=FB(8), fill=RED, anchor="ra")
    mx0, my0, mx1, my1 = MARGIN + 6, y + 22, W - MARGIN - 6, y + map_h - 6
    mw, mh2 = mx1 - mx0, my1 - my0
    # rough continents (equirectangular, lat -55..83)
    def mxy(lon, lat):
        return (mx0 + (lon + 180) / 360 * mw, my0 + (83 - lat) / 138 * mh2)
    LAND = (232, 222, 198)
    d.polygon([mxy(-168, 66), mxy(-140, 70), mxy(-120, 71), mxy(-95, 80), mxy(-75, 73),
               mxy(-60, 62), mxy(-55, 47), mxy(-70, 42), mxy(-80, 32), mxy(-97, 26),
               mxy(-105, 20), mxy(-92, 14), mxy(-83, 9), mxy(-105, 23), mxy(-125, 40),
               mxy(-125, 49), mxy(-150, 60)], fill=LAND)  # N America
    d.polygon([mxy(-80, 10), mxy(-70, 12), mxy(-60, 5), mxy(-52, 5), mxy(-35, -8),
               mxy(-40, -20), mxy(-48, -28), mxy(-58, -35), mxy(-65, -45), mxy(-70, -54),
               mxy(-73, -37), mxy(-77, -20), mxy(-81, -5)], fill=LAND)  # S America
    d.polygon([mxy(-10, 36), mxy(-9, 43), mxy(-2, 48), mxy(0, 51), mxy(8, 57),
               mxy(18, 56), mxy(21, 55), mxy(28, 60), mxy(30, 70), mxy(40, 68),
               mxy(32, 60), mxy(28, 55), mxy(23, 45), mxy(19, 42), mxy(12, 44),
               mxy(3, 43), mxy(-6, 37)], fill=LAND)  # Europe
    d.polygon([mxy(-6, 35), mxy(10, 37), mxy(20, 32), mxy(32, 31), mxy(35, 28),
               mxy(43, 12), mxy(51, 12), mxy(48, 5), mxy(42, -2), mxy(40, -10),
               mxy(35, -18), mxy(32, -26), mxy(28, -33), mxy(20, -35), mxy(16, -28),
               mxy(12, -18), mxy(9, -1), mxy(9, 4), mxy(-8, 5), mxy(-17, 15),
               mxy(-16, 28)], fill=LAND)  # Africa
    d.polygon([mxy(30, 36), mxy(36, 36), mxy(43, 30), mxy(48, 30), mxy(52, 26),
               mxy(58, 25), mxy(62, 25), mxy(66, 25), mxy(72, 20), mxy(77, 8),
               mxy(80, 7), mxy(88, 22), mxy(92, 21), mxy(98, 16), mxy(100, 8),
               mxy(104, 2), mxy(108, 11), mxy(114, 22), mxy(120, 30), mxy(122, 40),
               mxy(127, 40), mxy(130, 42), mxy(135, 44), mxy(140, 45), mxy(142, 50),
               mxy(140, 60), mxy(158, 60), mxy(162, 66), mxy(170, 66), mxy(178, 65),
               mxy(160, 60), mxy(140, 55), mxy(130, 50), mxy(110, 55), mxy(100, 60),
               mxy(90, 62), mxy(80, 68), mxy(70, 68), mxy(60, 62), mxy(50, 55),
               mxy(45, 45), mxy(40, 42), mxy(35, 40)], fill=LAND)  # Asia
    d.polygon([mxy(114, -22), mxy(122, -14), mxy(132, -12), mxy(142, -11), mxy(147, -19),
               mxy(150, -23), mxy(153, -27), mxy(150, -37), mxy(140, -38), mxy(130, -32),
               mxy(124, -33), mxy(115, -35), mxy(113, -26)], fill=LAND)  # Australia
    # grid
    for lon in range(-150, 181, 30):
        gx, _ = mxy(lon, 0)
        d.line([(gx, my0), (gx, my1)], fill=(200, 212, 222))
    for n, lon, lat, dx, dy in PINS:
        px, py = mxy(lon, lat)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        bx, by = px + dx, py + dy
        if dx or dy:
            d.line([(px, py), (bx, by)], fill=RED, width=1)
        d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=RED, outline=(255, 255, 255))
        d.text((bx, by), str(n), font=FB(9), fill=(255, 255, 255), anchor="mm")
    y += map_h + 6
    log.append(f"map_end={y}")

    # ALSO list: 4 columns x 6 rows
    d.text((MARGIN, y), "ALSO ON SATURDAY — 14 TO 36", font=FB(10), fill=INK)
    y += 15
    colw = (CW - 24) // 4
    rowh = 21
    for idx, (n, city, text, src) in enumerate(BRIEFS):
        c, r = idx % 4, idx // 4
        bx = MARGIN + c * (colw + 8)
        by = y + r * rowh
        full = f"{n} · {city} — {text} {src}"
        ty = by
        for ln in wrap(d, full, FR(9), colw):
            d.text((bx, ty), ln, font=FR(9), fill=INK)
            ty += 11
    y += 6 * rowh + 4
    log.append(f"also_end={y}")

    # DATE CHECK
    dch = 52
    d.rounded_rectangle([MARGIN, y, W - MARGIN, y + dch], radius=5, fill=(255, 248, 220), outline=GOLD)
    d.text((MARGIN + 8, y + 6), "DATE CHECK", font=FB(9), fill=RED)
    lines = wrap(d, DATE_CHECK, FR(8), CW - 16)
    ty = y + 18
    for ln in lines[:3]:
        d.text((MARGIN + 8, ty), ln, font=FR(8), fill=(60, 50, 30))
        ty += 11
    log.append(f"datecheck_lines={len(lines)}")
    y += dch + 5

    # footer
    d.text((MARGIN, y), "SOURCES: REUTERS · AP · AFP · BBC · ESA · USGS · GFZ · CNN · XINHUA · EU COMMISSION · F1 · BCCI · YONHAP · IMD · NEMA · PTI · SPACEFLIGHT NOW · SCIENTIFIC AMERICAN · THE HINDU · ETODAY · H.UA · NOVYNY.LIVE",
           font=FR(7), fill=GREY)
    y += 12
    log.append(f"final_y={y} slack={H - y}")
    img.save("entry.png", optimize=True)
    print("\n".join(log))
    return img

if __name__ == "__main__":
    build()
    import os
    print("bytes:", os.path.getsize("entry.png"))
    print("sha256:", hashlib.sha256(open("entry.png", "rb").read()).hexdigest())
