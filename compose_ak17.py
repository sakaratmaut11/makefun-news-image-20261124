#!/usr/bin/env python3
"""ONE DAY CHRONICLE — Akun 17, NI24 (Tuesday 24 November 2026).
Fresh compose engine written in this session for this account only.
Renders a 3900x3900 square front page, then downscales to 1024x1024
(256-colour quantised) for the entry. Requires Pillow locally; the
submitted main.py is stdlib-only copy-only and never runs this file.
"""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
PF = os.path.join(FONT_DIR, "PlayfairDisplay.ttf")
PFI = os.path.join(FONT_DIR, "PlayfairDisplay-Italic.ttf")
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

_cache = {}
def F(path, size, wght=None):
    key = (path, size, wght)
    if key in _cache:
        return _cache[key]
    f = ImageFont.truetype(path, size)
    if wght is not None:
        try:
            f.set_variation_by_axes([wght])
        except Exception:
            pass
    _cache[key] = f
    return f

def pf(size, wght=900):
    return F(PF, size, wght)
def pfi(size, wght=400):
    return F(PFI, size, wght)
def sans(size, bold=False):
    return F(SANSB if bold else SANS, size)

# ---------- palette: plum / ivory (Akun 17 identity) ----------
IVORY = (247, 241, 227)
IVORY2 = (238, 230, 210)
PLUM = (91, 35, 51)
PLUM_D = (62, 22, 34)
PLUM_M = (122, 48, 73)
GOLD = (196, 154, 60)
GOLD_L = (214, 178, 94)
INK = (34, 26, 26)
MUT = (107, 91, 82)
RED = (163, 30, 34)
NAVY = (34, 48, 74)
TEAL = (15, 107, 122)
GREEN = (31, 107, 74)
OCHRE = (138, 90, 24)
STEEL = (46, 74, 122)
CREAM_CARD = (252, 248, 238)

REGION_COL = {
    "EUROPE": STEEL, "MIDDLE EAST": OCHRE, "AMERICAS": GREEN,
    "OCEANIA": TEAL, "WORLD": PLUM, "GLOBAL": (90, 60, 110),
}

# ---------- content (pool ni24-pool.md + refresh 0700; angka induk) ----------
LEADS = [
    dict(num=1, place="WELLINGTON", region="OCEANIA", topic="CRICKET",
         head="New Zealand bat out draw with India",
         deck="NZ 239/5 — Mitchell 49* off 186 balls, Phillips 26* off 126; "
              "63-run stand over 258 balls. India 720/9d: Rahul 136, Pant 128, Gill 98.",
         src="HS · WicketPulse · QNC — REPORTED · first reported 23 Nov",
         chip="DRAW 239/5", kind="cricket"),
    dict(num=2, place="LIVERPOOL", region="EUROPE", topic="FOOTBALL",
         head="Liverpool 4–0 Man Utd; debut disaster for Pochettino",
         deck="Yoro sent off in the 8th minute; United down to ten. "
              "Defeat leaves United 19th in the Premier League on 8 points.",
         src="Mint · NextSportsWeb — REPORTED · first reported 23 Nov",
         chip="4–0", kind="football"),
    dict(num=3, place="BENGHAZI, LIBYA", region="EUROPE", topic="WAR",
         head="Ukraine sinks Russian warship Merkury off Libya",
         deck="7 sea drones launched; Steregushchiy-class corvette sunk at Benghazi. "
              "Ka-27 helicopter destroyed aboard; MV Angara cargo vessel hit.",
         src="CNN · Times · WSJ · AP — REPORTED · first reported 23 Nov",
         chip="7 SEA DRONES", kind="ship"),
]
MINIS = [
    dict(num=4, place="ANTALYA, TÜRKIYE", region="WORLD", topic="CLIMATE",
         head="COP31 ends with no deal — first since 2000",
         deck="The Antalya Pact was NOT adopted; final text dropped every mention of "
              "fossil fuels. 44 h overtime, longest COP ever.",
         src="Times · Guardian — REPORTED", chip="NO DEAL", kind="climate"),
    dict(num=5, place="GULF OF FINLAND", region="EUROPE", topic="SEA",
         head="Russian cargo ship Sparta II hit, towed clear",
         deck="Hit by drones Saturday; Finland led the rescue, all 16 crew off. "
              "Towed out Sunday night; bound for Kaliningrad, hit by 2 drones.",
         src="Reuters · Times · WSJ — REPORTED", chip="16 CREW SAFE", kind="sea"),
    dict(num=6, place="KYIV STRIKES — KYIV REGION", region="EUROPE", topic="WAR",
         head="Russian strikes kill at least 15 near Kyiv",
         deck="11 killed in a block of flats in Dymer; a drone hit a 6-floor building "
              "in Kyiv Monday, 5 injured.",
         src="Times · AP — REPORTED", chip="15 KILLED", kind="strikes"),
    dict(num=7, place="WASHINGTON", region="MIDDLE EAST", topic="SANCTIONS",
         head="US sanctions ~30 Iran-linked exchange houses",
         deck="Treasury Monday: ~30 Iran-based and linked exchange houses plus executives, "
              "core of shadow banking evading sanctions on Iranian banks.",
         src="AP · Treasury — REPORTED", chip="~30 SANCTIONED", kind="sanctions"),
    dict(num=8, place="GAZA CITY", region="MIDDLE EAST", topic="CONFLICT",
         head="Israeli strikes kill 3 in Gaza",
         deck="3 killed Monday in separate strikes, including a UNRWA employee; "
              "Shifa Hospital and the agency confirm.",
         src="AP — REPORTED", chip="3 KILLED", kind="gaza"),
    dict(num=9, place="WESTERN YEMEN", region="MIDDLE EAST", topic="WAR",
         head="Strike kills 11 in western Yemen",
         deck="Houthis say a Saudi-backed forces' strike Monday killed 11 and wounded 19.",
         src="AP — REPORTED", chip="11 KILLED", kind="yemen"),
    dict(num=10, place="NEW YORK", region="AMERICAS", topic="MARKETS",
         head="Gold rebounds 1.5% to $3,588",
         deck="Bullion up Monday after its worst week in 8 months, off a 14-month low. "
              "Traders await the US PCE inflation report due 25 Nov; 10-year yield ~4.96%.",
         src="Reuters — REPORTED", chip="GOLD $3,588", kind="gold"),
    dict(num=11, place="GLOBAL", region="WORLD", topic="CRYPTO",
         head="Bitcoin steadies near $61,284",
         deck="$61,284 Mon 12:52 UTC, +1.1% in 24 h, −4.5% in 7 d. "
              "Weekend low ~$55,100; Kraken CAD flash crash to ~$17,000 Sat, trades stand.",
         src="CoinPaprika — REPORTED", chip="$61,284", kind="bitcoin"),
    dict(num=12, place="LOS ANGELES", region="AMERICAS", topic="BUSINESS",
         head="GTA VI takes $3.8bn on day one",
         deck="Biggest entertainment launch on record — past every game launch "
              "and single-day film box office.",
         src="ActiveInvestorMag — REPORTED", chip="$3.8BN DAY ONE", kind="game"),
    dict(num=13, place="SANTA CLARA", region="AMERICAS", topic="MARKETS",
         head="Nvidia brings back Jensen Huang as CEO",
         deck="Board reinstates Huang effective immediately Monday, after Trump intervened "
              "over the weekend. Shares +31% Monday, Nasdaq +6%, S&P 500 +5%.",
         src="Reuters — REPORTED", chip="+31% HUANG BACK", kind="nvidia"),
    dict(num=14, place="WASHINGTON", region="AMERICAS", topic="POLITICS",
         head="Democrats take both chambers",
         deck="Largest House majority since 1992, 258–173, after a North Carolina pickup. "
              "Van Hollen challenges Schumer for Senate leader; secret ballot 1 Dec.",
         src="BBC · ActiveInvestorMag — REPORTED", chip="258–173", kind="politics"),
]
BRIEFS = [
    (15, "Nepal PM Shah ends Delhi visit; met Modi Monday (IANS, 23 Nov)"),
    (16, "Thousands march in Lisbon on cost of living (JagranJosh, 23 Nov)"),
    (17, "UK–EU reset deal: Burnham calls it “landmark” (BBC, 23 Nov)"),
    (18, "India–EU trade pact likely signed 16 Dec (JagranJosh, 23 Nov)"),
    (19, "Tata Steel sells pipe business, ₹28,000 cr (ObserverVoice, 23 Nov)"),
    (20, "Congo halts cobalt exports from 30 Nov (Reuters, 23 Nov)"),
    (21, "Indonesia factory blaze kills 24; dozens missing (Reuters, 23 Nov)"),
    (22, "CrowdStrike buys Zscaler in $44bn deal (Reuters, 23 Nov)"),
    (23, "US weighs training Syrian forces, first since 2024 (Reuters, 23 Nov)"),
    (24, "Euro zone growth steady; PMI 51.7 in November (Reuters, 23 Nov)"),
    (25, "Trump hosts meme-coin gala; token at record lows (Reuters, 23 Nov)"),
    (26, "US Army to blast 68 barrels of lead azide in Iowa (Reuters, 23 Nov)"),
    (27, "India weighs rice export duties as prices rise (Reuters, 23 Nov)"),
    (28, "Modi opens AI Centre at IIT Patna (ObserverVoice, 23 Nov)"),
    (29, "Shah launches ₹4,000 cr Arunachal push (ObserverVoice, 23 Nov)"),
    (30, "Miley Cyrus weds Maxx Morando in California (Reuters, 23 Nov)"),
    (31, "Solana launches solana.ai for AI agents (Gadgets360, 23 Nov)"),
    (32, "US stocks fall again; Nasdaq 100 futures +3% Mon (AP, 23 Nov)"),
    (33, "UN to keep negotiating lethal AI weapons (salonvision, 23 Nov)"),
    (34, "Goldman sees +18% S&P 500 by 2027 (ActiveInvestorMag, 23 Nov)"),
    (35, "KOSPI −3% Monday to 10-month low; Taiwan steadies (Reuters, 23 Nov)"),
    (36, "FBI probes hack of crime database; van checks paused (AP, 23 Nov)"),
]
NUMBERS = [
    ("7", "SEA DRONES LAUNCHED"), ("239/5", "WELLINGTON DRAW"),
    ("4–0", "LIVERPOOL ROUT"), ("NO DEAL", "COP31 · SINCE 2000"),
    ("$3,588", "GOLD PER OZ"), ("$61,284", "BITCOIN"),
    ("$3.8BN", "GTA VI DAY ONE"), ("+31%", "NVIDIA · HUANG BACK"),
]
TIMELINE = [
    ("04:24 WIB TUE", "KCNA: North Korea weighs closing its Swiss office", "Reuters"),
    ("07:23 WIB TUE", "Gold edges up in early Asia trade", "Reuters · 00:23 GMT"),
    ("07:45 WIB TUE", "Huang return lifts markets; gold climbs in Asia", "TalkMarkets · 00:45 UTC"),
    ("MON EVE · UTC", "Zelenskyy: Ukraine sank the Merkury off Benghazi", "CNN"),
    ("MON EVE · UTC", "Treasury sanctions ~30 Iran exchange houses", "AP"),
    ("MON EVE · UTC", "COP31 collapses with no deal after 44 h overtime", "Reuters"),
]
DATECHECK = [
    "186-drone night over Ukraine, 161 downed — Fri 21–Sun 22 Nov",
    "Hong Kong Election Committee: 856 candidates, 723 seats — Sun 22 Nov",
    "Alcaraz beats Zverev for first ATP Finals title — Sun 22 Nov",
    "Verstappen wins the Las Vegas Grand Prix — Sun 22 Nov",
    "Wembanyama scores 50, Spurs 114–91 Pelicans — Sun 22 Nov",
    "India declare 720/9 — Sun 22 Nov (the DRAW came Monday)",
    "Huang resigns as Nvidia CEO — Thu 12 Nov (the RETURN came Monday)",
]
PINS = {  # story num -> (lon, lat)
    1: (174.8, -41.3), 2: (-3.0, 53.4), 3: (20.1, 32.1), 4: (30.7, 36.9),
    5: (25.0, 59.8), 6: (30.5, 50.45), 7: (-77.0, 38.9), 8: (34.45, 31.5),
    9: (43.5, 15.0), 10: (-74.0, 40.7), 12: (-118.25, 34.05),
    13: (-121.95, 37.37), 14: (-76.4, 39.2),
}
CONTINENTS = [
    [(-168,66),(-140,70),(-125,72),(-110,73),(-95,80),(-85,80),(-80,73),(-70,62),(-60,55),(-55,47),(-65,44),(-75,35),(-80,25),(-85,20),(-90,15),(-95,17),(-105,22),(-115,28),(-125,40),(-125,49),(-140,60),(-155,58),(-165,60)],
    [(-80,10),(-70,12),(-60,8),(-50,5),(-40,0),(-35,-8),(-40,-20),(-48,-28),(-58,-38),(-65,-45),(-70,-54),(-73,-40),(-72,-25),(-77,-12),(-80,-3),(-80,5)],
    [(-17,15),(-15,27),(-10,31),(-5,35),(10,37),(20,32),(30,31),(35,28),(40,20),(43,11),(48,11),(51,10),(44,0),(40,-10),(35,-20),(30,-30),(20,-35),(15,-30),(12,-18),(13,-8),(9,4),(-8,4),(-13,8),(-17,12)],
    [(-10,36),(-9,43),(-2,48),(-5,50),(0,51),(5,53),(8,57),(10,59),(18,69),(25,71),(40,68),(55,68),(70,72),(90,75),(110,76),(130,72),(150,70),(170,66),(178,65),(170,60),(160,55),(150,60),(140,55),(135,45),(127,40),(120,35),(110,25),(105,15),(100,8),(95,15),(90,22),(80,15),(75,8),(70,20),(65,25),(60,25),(55,26),(50,29),(48,30),(43,35),(36,36),(30,36),(25,35),(20,40),(15,44),(10,44),(3,42),(0,40),(-2,37),(-9,37)],
    [(-5,50),(-3,53),(-5,56),(-2,58),(0,53),(-1,51)],
    [(130,31),(133,34),(137,35),(140,38),(142,42),(144,44),(141,40),(138,36),(133,33)],
    [(109,1),(113,4),(117,6),(119,0),(116,-4),(111,-3)],
    [(95,5),(100,0),(104,-3),(106,-6),(101,-5),(97,2)],
    [(131,-1),(136,-2),(141,-3),(146,-6),(150,-8),(146,-8),(141,-8),(136,-4),(131,-3)],
    [(113,-22),(114,-30),(115,-35),(120,-34),(129,-32),(137,-35),(142,-38),(147,-39),(150,-37),(153,-32),(153,-27),(150,-22),(146,-19),(142,-15),(142,-11),(137,-12),(135,-15),(132,-12),(130,-13),(126,-14),(122,-17),(118,-20)],
]

# ---------- text helpers ----------
def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(d, x, y, text, font, color, max_w, leading, max_lines=None):
    lines = wrap(d, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=color)
        y += leading
    return y

def centre(d, cx, y, text, font, color):
    d.text((cx - d.textlength(text, font=font) / 2, y), text, font=font, fill=color)

def chip(d, x, y, text, font, fg=IVORY, bg=PLUM):
    w = d.textlength(text, font=font) + 28
    h = font.size + 18
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=bg)
    d.text((x + 14, y + 9), text, font=font, fill=fg)
    return w, h

def num_badge(d, x, y, n, r=30):
    d.ellipse([x - r, y - r, x + r, y + r], fill=PLUM, outline=GOLD, width=4)
    t = str(n)
    f = sans(34 if len(t) < 2 else 30, bold=True)
    d.text((x - d.textlength(t, font=f) / 2, y - f.size / 2 - 2), t, font=f, fill=IVORY)

# ---------- flat scene bands (original drawings, one per story kind) ----------
def scene(d, box, kind, accent):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    skies = {"cricket": (46, 92, 58), "football": (31, 107, 74), "ship": (34, 48, 74),
             "climate": (122, 48, 73), "sea": (46, 74, 122), "strikes": (62, 22, 34),
             "sanctions": (138, 90, 24), "gaza": (90, 60, 110), "yemen": (122, 72, 30),
             "gold": (138, 90, 24), "bitcoin": (196, 110, 20), "game": (60, 30, 90),
             "nvidia": (31, 107, 74), "politics": (46, 74, 122)}
    sky = skies.get(kind, PLUM_M)
    d.rectangle(box, fill=sky)
    d.rectangle([x0, y0 + h * 0.68, x1, y1], fill=(30, 26, 24))
    if kind == "cricket":
        d.rectangle([x0 + w * 0.42, y0 + h * 0.55, x0 + w * 0.58, y1], fill=(214, 190, 140))
        d.line([x0 + w * 0.42, y0 + h * 0.55, x0 + w * 0.58, y0 + h * 0.55], fill=IVORY, width=4)
        for i, dx in enumerate((-14, 0, 14)):
            d.rectangle([x0 + w * 0.5 + dx - 5, y0 + h * 0.30, x0 + w * 0.5 + dx + 5, y0 + h * 0.58], fill=(232, 200, 90))
        d.ellipse([x0 + w * 0.72, y0 + h * 0.30, x0 + w * 0.72 + 34, y0 + h * 0.30 + 34], fill=RED)
        d.polygon([(x0 + w * 0.20, y0 + h * 0.62), (x0 + w * 0.30, y0 + h * 0.30),
                   (x0 + w * 0.36, y0 + h * 0.34), (x0 + w * 0.27, y0 + h * 0.66)], fill=(150, 100, 55))
    elif kind == "football":
        d.line([x0 + w * 0.5, y0 + h * 0.12, x0 + w * 0.5, y0 + h * 0.68], fill=IVORY, width=5)
        d.ellipse([x0 + w * 0.5 - 68, y0 + h * 0.26, x0 + w * 0.5 + 68, y0 + h * 0.26 + 136], fill=IVORY, outline=INK, width=6)
        d.polygon([(x0 + w * 0.5 - 18, y0 + h * 0.26 + 50), (x0 + w * 0.5 + 18, y0 + h * 0.26 + 50),
                   (x0 + w * 0.5 + 10, y0 + h * 0.26 + 86), (x0 + w * 0.5 - 10, y0 + h * 0.26 + 86)], fill=INK)
        d.rectangle([x0 + w * 0.10, y0 + h * 0.20, x0 + w * 0.28, y0 + h * 0.68], outline=IVORY, width=6)
        d.line([x0 + w * 0.10, y0 + h * 0.44, x0 + w * 0.28, y0 + h * 0.44], fill=IVORY, width=4)
    elif kind in ("ship", "sea"):
        for i in range(3):
            yy = y0 + h * (0.72 + i * 0.10)
            d.arc([x0 + 20, yy - 26, x1 - 20, yy + 26], 200, 340, fill=(180, 200, 220), width=6)
        d.polygon([(x0 + w * 0.18, y0 + h * 0.62), (x0 + w * 0.82, y0 + h * 0.62),
                   (x0 + w * 0.74, y0 + h * 0.82), (x0 + w * 0.26, y0 + h * 0.82)], fill=(70, 76, 84))
        d.rectangle([x0 + w * 0.44, y0 + h * 0.34, x0 + w * 0.56, y0 + h * 0.62], fill=(120, 126, 134))
        for cx, cy in ((0.30, 0.30), (0.68, 0.22)):
            d.ellipse([x0 + w * cx - 16, y0 + h * cy - 16, x0 + w * cx + 16, y0 + h * cy + 16], fill=(40, 40, 44))
            d.line([x0 + w * cx, y0 + h * cy + 16, x0 + w * cx, y0 + h * cy + 52], fill=(40, 40, 44), width=4)
        d.polygon([(x0 + w * 0.60, y0 + h * 0.30), (x0 + w * 0.66, y0 + h * 0.44),
                   (x0 + w * 0.60, y0 + h * 0.52), (x0 + w * 0.54, y0 + h * 0.44)], fill=(255, 140, 40))
        d.ellipse([x0 + w * 0.58, y0 + h * 0.34, x0 + w * 0.58 + 44, y0 + h * 0.34 + 44], fill=(255, 190, 60))
    elif kind == "climate":
        d.ellipse([x0 + w * 0.78, y0 + h * 0.14, x0 + w * 0.78 + 90, y0 + h * 0.14 + 90], fill=GOLD)
        for i, c in enumerate(((46, 74, 122), (31, 107, 74), (163, 30, 34), (196, 154, 60))):
            bx = x0 + w * (0.14 + i * 0.16)
            d.rectangle([bx, y0 + h * 0.42, bx + 46, y0 + h * 0.68], fill=c)
        d.rectangle([x0 + w * 0.10, y0 + h * 0.66, x0 + w * 0.90, y0 + h * 0.72], fill=(60, 50, 44))
    elif kind == "strikes":
        for bx, bh in ((0.10, 0.55), (0.30, 0.72), (0.55, 0.48), (0.72, 0.62)):
            d.rectangle([x0 + w * bx, y0 + h * (0.68 - bh), x0 + w * (bx + 0.16), y0 + h * 0.68], fill=(52, 44, 46))
        d.polygon([(x0 + w * 0.38, y0 + h * 0.10), (x0 + w * 0.46, y0 + h * 0.34),
                   (x0 + w * 0.62, y0 + h * 0.34), (x0 + w * 0.50, y0 + h * 0.46),
                   (x0 + w * 0.56, y0 + h * 0.62), (x0 + w * 0.38, y0 + h * 0.52),
                   (x0 + w * 0.20, y0 + h * 0.62), (x0 + w * 0.26, y0 + h * 0.46),
                   (x0 + w * 0.14, y0 + h * 0.34), (x0 + w * 0.30, y0 + h * 0.34)], fill=(255, 170, 50))
        d.ellipse([x0 + w * 0.66, y0 + h * 0.18, x0 + w * 0.66 + 70, y0 + h * 0.18 + 70], fill=(150, 140, 135))
    elif kind == "sanctions":
        d.polygon([(x0 + w * 0.30, y0 + h * 0.30), (x0 + w * 0.70, y0 + h * 0.30), (x0 + w * 0.62, y0 + h * 0.18), (x0 + w * 0.38, y0 + h * 0.18)], fill=IVORY)
        for i in range(3):
            bx = x0 + w * (0.36 + i * 0.12)
            d.rectangle([bx, y0 + h * 0.32, bx + 26, y0 + h * 0.66], fill=IVORY)
        d.rectangle([x0 + w * 0.28, y0 + h * 0.66, x0 + w * 0.72, y0 + h * 0.74], fill=IVORY)
        d.ellipse([x0 + w * 0.74, y0 + h * 0.30, x0 + w * 0.74 + 86, y0 + h * 0.30 + 86], outline=RED, width=8)
        d.line([x0 + w * 0.74 + 12, y0 + h * 0.30 + 74, x0 + w * 0.74 + 74, y0 + h * 0.30 + 12], fill=RED, width=8)
    elif kind in ("gaza", "yemen"):
        for bx, bh in ((0.08, 0.50), (0.26, 0.66), (0.46, 0.44), (0.64, 0.58), (0.80, 0.40)):
            d.rectangle([x0 + w * bx, y0 + h * (0.68 - bh), x0 + w * (bx + 0.13), y0 + h * 0.68], fill=(70, 62, 66))
        for cx, cy, r in ((0.30, 0.28, 42), (0.42, 0.18, 56), (0.58, 0.30, 40)):
            d.ellipse([x0 + w * cx - r, y0 + h * cy - r, x0 + w * cx + r, y0 + h * cy + r], fill=(168, 158, 150))
        if kind == "yemen":
            d.polygon([(x0 + w * 0.10, y0 + h * 0.68), (x0 + w * 0.30, y0 + h * 0.18), (x0 + w * 0.50, y0 + h * 0.68)], fill=(90, 80, 70))
    elif kind == "gold":
        for i, (bx, bw, bh) in enumerate(((0.16, 0.22, 0.30), (0.42, 0.22, 0.44), (0.68, 0.22, 0.58))):
            d.polygon([(x0 + w * bx, y0 + h * (0.68 - bh)), (x0 + w * (bx + bw), y0 + h * (0.68 - bh)),
                       (x0 + w * (bx + bw - 0.03), y0 + h * 0.68), (x0 + w * (bx + 0.03), y0 + h * 0.68)], fill=GOLD_L)
        d.line([(x0 + w * 0.10, y0 + h * 0.55), (x0 + w * 0.35, y0 + h * 0.40),
                (x0 + w * 0.55, y0 + h * 0.48), (x0 + w * 0.85, y0 + h * 0.18)], fill=IVORY, width=8)
        d.polygon([(x0 + w * 0.85, y0 + h * 0.18), (x0 + w * 0.78, y0 + h * 0.16), (x0 + w * 0.85, y0 + h * 0.30)], fill=IVORY)
    elif kind == "bitcoin":
        d.ellipse([x0 + w * 0.5 - 70, y0 + h * 0.14, x0 + w * 0.5 + 70, y0 + h * 0.14 + 140], fill=(240, 150, 40), outline=IVORY, width=5)
        d.text((x0 + w * 0.5 - 26, y0 + h * 0.14 + 26), "₿", font=sans(92, bold=True), fill=IVORY)
        d.line([(x0 + w * 0.12, y0 + h * 0.60), (x0 + w * 0.30, y0 + h * 0.42),
                (x0 + w * 0.48, y0 + h * 0.52), (x0 + w * 0.70, y0 + h * 0.30),
                (x0 + w * 0.88, y0 + h * 0.38)], fill=IVORY, width=7)
    elif kind == "game":
        d.rounded_rectangle([x0 + w * 0.22, y0 + h * 0.30, x0 + w * 0.78, y0 + h * 0.72], radius=34, fill=(30, 20, 40), outline=GOLD_L, width=5)
        d.ellipse([x0 + w * 0.32, y0 + h * 0.42, x0 + w * 0.32 + 34, y0 + h * 0.42 + 34], fill=RED)
        d.ellipse([x0 + w * 0.62, y0 + h * 0.42, x0 + w * 0.62 + 34, y0 + h * 0.42 + 34], fill=GOLD)
        d.text((x0 + w * 0.44, y0 + h * 0.16), "VI", font=pf(96), fill=IVORY)
    elif kind == "nvidia":
        d.rectangle([x0 + w * 0.34, y0 + h * 0.26, x0 + w * 0.66, y0 + h * 0.66], fill=(20, 140, 80), outline=IVORY, width=5)
        for i in range(3):
            yy = y0 + h * (0.36 + i * 0.12)
            d.line([x0 + w * 0.34, yy, x0 + w * 0.66, yy], fill=(120, 220, 160), width=5)
        d.line([(x0 + w * 0.80, y0 + h * 0.60), (x0 + w * 0.86, y0 + h * 0.34), (x0 + w * 0.92, y0 + h * 0.52)], fill=GOLD, width=8)
        d.polygon([(x0 + w * 0.86, y0 + h * 0.26), (x0 + w * 0.80, y0 + h * 0.38), (x0 + w * 0.92, y0 + h * 0.38)], fill=GOLD)
    elif kind == "politics":
        d.pieslice([x0 + w * 0.38, y0 + h * 0.14, x0 + w * 0.62, y0 + h * 0.50], 180, 360, fill=IVORY)
        d.rectangle([x0 + w * 0.30, y0 + h * 0.48, x0 + w * 0.70, y0 + h * 0.56], fill=IVORY)
        for i in range(4):
            bx = x0 + w * (0.33 + i * 0.10)
            d.rectangle([bx, y0 + h * 0.56, bx + 20, y0 + h * 0.68], fill=IVORY)
        for sx, sy in ((0.16, 0.22), (0.84, 0.18), (0.12, 0.48), (0.88, 0.46)):
            d.text((x0 + w * sx, y0 + h * sy), "★", font=sans(40, bold=True), fill=GOLD_L)
    d.rectangle([x0, y0, x1, y0 + 6], fill=GOLD)

# ---------- dotted world map ----------
def point_in_poly(x, y, poly):
    inside, n = False, len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]; xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside

def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(232, 226, 208))
    d.rectangle(box, outline=PLUM, width=4)
    mw, mh = x1 - x0, y1 - y0
    def proj(lon, lat):
        return (x0 + (lon + 180) / 360 * mw, y0 + (90 - lat) / 180 * mh)
    polys = [[proj(lon, lat) for lon, lat in c] for c in CONTINENTS]
    step = 11
    yy = y0 + 8
    while yy < y1 - 6:
        xx = x0 + 8
        while xx < x1 - 6:
            lon = (xx - x0) / mw * 360 - 180
            lat = 90 - (yy - y0) / mh * 180
            if any(point_in_poly(lon, lat, c) for c in CONTINENTS):
                d.ellipse([xx - 4, yy - 4, xx + 4, yy + 4], fill=NAVY)
            xx += step
        yy += step
    for num, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        r = 30
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=IVORY, width=4)
        t = str(num)
        f = sans(32 if len(t) < 2 else 28, bold=True)
        d.text((px - d.textlength(t, font=f) / 2, py - f.size / 2 - 2), t, font=f, fill=IVORY)

# ---------- card painters ----------
def lead_card(d, x, y, w, h, c, variant):
    d.rectangle([x, y, x + w, y + h], fill=CREAM_CARD, outline=PLUM, width=4)
    scene(d, (x + 4, y + 4, x + w - 4, y + 300), c["kind"], PLUM)
    chip(d, x + 24, y + 300 - 62, c["chip"], sans(34, bold=True))
    num_badge(d, x + w - 56, y + 56, c["num"])
    yy = y + 318
    rc = REGION_COL[c["region"]]
    d.text((x + 24, yy), f"{c['place']}  ·  {c['region']}  ·  {c['topic']}", font=sans(30, bold=True), fill=rc)
    yy += 46
    yy = para(d, x + 24, yy, c["head"], pf(76), PLUM_D, w - 48, 86, max_lines=2)
    yy += 8
    yy = para(d, x + 24, yy, c["deck"], sans(40), INK, w - 48, 50, max_lines=3)
    d.text((x + 24, y + h - 40), c["src"], font=sans(28), fill=MUT)

def mini_card(d, x, y, w, h, c, variant):
    d.rectangle([x, y, x + w, y + h], fill=CREAM_CARD, outline=PLUM, width=3)
    scene(d, (x + 3, y + 3, x + w - 3, y + 100), c["kind"], PLUM)
    chip(d, x + 16, y + 100 - 52, c["chip"], sans(27, bold=True))
    num_badge(d, x + w - 44, y + 44, c["num"], r=26)
    yy = y + 112
    rc = REGION_COL[c["region"]]
    d.text((x + 16, yy), f"{c['place']} · {c['region']} · {c['topic']}", font=sans(26, bold=True), fill=rc)
    yy += 32
    d.text((x + 16, yy), c["src"], font=sans(25), fill=MUT)
    yy += 36
    yy = para(d, x + 16, yy, c["head"], pf(54), PLUM_D, w - 32, 60, max_lines=2)
    yy += 4
    para(d, x + 16, yy, c["deck"], sans(34), INK, w - 32, 40, max_lines=3)

# ---------- page ----------
def render(variant):
    W = 3900
    H = 3900
    img = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(img)
    M = 90
    X0, X1 = M, W - M
    CW = X1 - X0
    y = 40
    # kicker
    d.rectangle([X0, y, X1, y + 88], fill=PLUM_D)
    centre(d, W // 2, y + 20, "36 STORIES  ·  7 REGIONS  ·  EVERY ONE FROM TUESDAY 24 NOVEMBER 2026",
           sans(52, bold=True), IVORY)
    y += 108
    # masthead
    name_col = PLUM if variant == "A" else PLUM_D
    centre(d, W // 2, y, "ONE DAY CHRONICLE", pf(190), name_col)
    y += 216
    d.line([X0, y + 18, W // 2 - 780, y + 18], fill=GOLD, width=6)
    d.line([W // 2 + 780, y + 18, X1, y + 18], fill=GOLD, width=6)
    centre(d, W // 2, y - 28, "Tuesday 24 November 2026", pf(112, 900), PLUM)
    y += 118
    centre(d, W // 2, y, "Wellington holds its nerve, Liverpool run riot — and a warship sinks off Benghazi.",
           pfi(56), PLUM_M)
    y += 78
    # numbers strip
    d.rectangle([X0, y, X1, y + 130], fill=PLUM)
    cw = CW / len(NUMBERS)
    for i, (v, lab) in enumerate(NUMBERS):
        cx = X0 + cw * i + cw / 2
        centre(d, cx, y + 12, v, sans(62, bold=True), IVORY)
        centre(d, cx, y + 82, lab, sans(29, bold=True), GOLD_L)
        if i:
            d.line([X0 + cw * i, y + 16, X0 + cw * i, y + 114], fill=GOLD, width=3)
    y += 144
    # region strip
    parts = [("EUROPE 4", STEEL), ("MIDDLE EAST 3", OCHRE), ("AMERICAS 4", GREEN),
             ("WORLD 2", PLUM), ("OCEANIA 1", TEAL)]
    tx = X0
    d.text((tx, y), "REGIONS: ", font=sans(34, bold=True), fill=PLUM_D)
    tx += d.textlength("REGIONS: ", font=sans(34, bold=True))
    for label, col in parts:
        d.ellipse([tx, y + 8, tx + 22, y + 30], fill=col)
        tx += 30
        d.text((tx, y), label + "   ", font=sans(34, bold=True), fill=INK)
        tx += d.textlength(label + "   ", font=sans(34, bold=True))
    d.text((tx, y), "·  AFRICA + ASIA-PACIFIC IN ALSO ON", font=sans(34), fill=MUT)
    y += 56
    # lead row
    leads = LEADS if variant == "A" else [LEADS[2], LEADS[0], LEADS[1]]
    lw = (CW - 80) // 3
    lh = 730
    for i, c in enumerate(leads):
        lead_card(d, X0 + i * (lw + 40), y, lw, lh, c, variant)
    y += lh + 16
    # mini grid: rows 4+4, then 3 wide
    minis = MINIS if variant == "A" else [MINIS[1], MINIS[0], MINIS[3], MINIS[2],
                                           MINIS[5], MINIS[4], MINIS[7], MINIS[6],
                                           MINIS[8], MINIS[9], MINIS[10]]
    mw = (CW - 120) // 4
    mh = 430
    for r in range(2):
        for i in range(4):
            mini_card(d, X0 + i * (mw + 40), y + r * (mh + 18), mw, mh, minis[r * 4 + i], variant)
    y += 2 * mh + 18 + 16
    # row 3: three wide minis
    tail = minis[8:11]
    tw = (CW - 80) // 3
    for i, c in enumerate(tail):
        mini_card(d, X0 + i * (tw + 40), y, tw, mh, c, variant)
    y += mh + 16
    # timeline
    d.rectangle([X0, y, X1, y + 160], fill=PLUM_D)
    centre(d, W // 2, y + 10, "TUESDAY IN TIME (WIB) — PLUS MONDAY-EVENING WIRES, LABELLED AS REPORTED",
           sans(34, bold=True), GOLD_L)
    tw6 = CW / 6
    for i, (t, ev, src) in enumerate(TIMELINE):
        cx = X0 + tw6 * i
        d.text((cx + 16, y + 52), t, font=sans(32, bold=True), fill=IVORY)
        para(d, cx + 16, y + 90, ev, sans(33), IVORY, tw6 - 32, 38, max_lines=2)
        if i:
            d.line([cx, y + 48, cx, y + 150], fill=GOLD, width=2)
    y += 160 + 14
    # bottom row: map left, DATE CHECK right
    by = y
    bh = 360
    map_w = 1500
    d.text((X0, by), "WHERE IT HAPPENED — pins match story numbers · 11 BITCOIN is worldwide, no single pin",
           font=sans(30, bold=True), fill=PLUM_D)
    draw_map(d, (X0, by + 40, X0 + map_w, by + bh))
    dx = X0 + map_w + 36
    dw = X1 - dx
    d.rectangle([dx, by, X1, by + bh], fill=(250, 232, 228), outline=RED, width=4)
    d.text((dx + 20, by + 12), "DATE CHECK — NOT TUESDAY, NOT NEWS TODAY", font=sans(34, bold=True), fill=RED)
    yy = by + 58
    for item in DATECHECK:
        para(d, dx + 20, yy, "✕  " + item, sans(32), INK, dw - 40, 40, max_lines=1)
        yy += 42
    y = by + bh + 14
    # ALSO ON (one line per brief)
    d.text((X0, y), "ALSO ON — TUESDAY'S REST, IN BRIEF", font=sans(36, bold=True), fill=PLUM_D)
    y += 46
    col_w = (CW - 60) // 3
    rows = 8
    briefs = BRIEFS if variant == "A" else BRIEFS[::-1]
    for col in range(3):
        bx = X0 + col * (col_w + 30)
        for r in range(rows):
            idx = col * rows + r
            if idx >= len(briefs):
                break
            n, txt = briefs[idx]
            yy = y + r * 40
            d.text((bx, yy), f"{n}.", font=sans(32, bold=True), fill=PLUM)
            d.text((bx + 52, yy), txt, font=sans(32), fill=INK)
    y += rows * 40 + 8
    # footer
    d.line([X0, y, X1, y], fill=GOLD, width=4)
    y += 12
    para(d, X0, y, "Sources: Reuters · AP · CNN · The Times · WSJ · BBC · Guardian · CoinPaprika · "
         "ActiveInvestorMag · HS · WicketPulse · QNC · Mint · NextSportsWeb · IANS · JagranJosh · "
         "ObserverVoice · Gadgets360 · salonvision · TalkMarkets · KCNA.  REPORTED = confirmed by named "
         "sources.  Pictures and map: original, drawn in code.  Original drawings.", sans(28), MUT, CW, 36, max_lines=3)
    print("render", variant, "final y =", y)
    return img

def finalize(src, dst):
    im = Image.open(src).convert("RGB")
    im = im.resize((1024, 1024), Image.LANCZOS)
    im = im.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    im.save(dst, "PNG", optimize=True)  # keep palette mode: small file, crisp text

if __name__ == "__main__":
    for v in ("A", "B"):
        big = os.path.join(HERE, f"compose-{v}-3900.png")
        small = os.path.join(HERE, f"variant-{v}.png")
        render(v).save(big, "PNG")
        finalize(big, small)
        print(v, os.path.getsize(small), "bytes")
