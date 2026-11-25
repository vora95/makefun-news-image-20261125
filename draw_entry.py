#!/usr/bin/env python3
"""Draw the push entry image for make.fun news-image-20261125 (MAIN account).

THE WORLD TODAY - 50 stories, 6 continents, one front page and a map.
Wednesday 25 November 2026. All 50 stories were first reported 24-25 Nov
2026 (Reuters, BBC, CNN, AP, Al Jazeera, ESPN, Morningstar, Investopedia,
Channel NewsAsia, The Hindu, TOI). No forecasts, no invented stories.

Layout (1024x1024): masthead + date line; hero row (lead + 2 stories);
world-map band (proper lat/lon map on the left, 6 pinned stories on the
right); 6-story grid; ALSO ON list of 41 more stories; markets footer.
Deterministic: fixed fonts, no randomness, no network, no clock.
Regenerating produces a byte-identical PNG.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PAPER = (253, 253, 248)
INK = (17, 17, 17)
RED = (185, 28, 28)
GRAY = (85, 85, 85)
MAP_BG = (238, 243, 246)
LAND = (183, 201, 212)
LAND_EDGE = (120, 145, 160)
PIN = (193, 18, 31)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None,
                 max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
HERO_LEAD = (
    "LEAD  •  JUSTICE",
    "HUAWEI CONVICTED IN U.S. CRIMINAL TRIAL",
    "A Brooklyn jury found the Chinese telecom giant guilty on 10 of 12 "
    "counts - trade-secret theft and bank fraud. Jurors cleared it of "
    "racketeering.",
)
HERO_2 = (
    "WAR  •  RIYADH",
    "HOUTHIS HIT RIYADH'S TALLEST TOWER",
    "Eleven wounded, two of them Indian, as Houthis strike the PIF Tower "
    "a second time in five days.",
)
HERO_3 = (
    "EUROPE  •  NATO",
    "NATO SENDS EARLY-WARNING JETS TO POLAND",
    "Alliance vows to defend space against a new threat.",
)

GRID = [
    ("WASHINGTON",
     "CIA AND ODNI SUFFER CYBER BREACH",
     "U.S. intelligence agencies hit by a breach; some unclassified data "
     "exposed, a source says."),
    ("UKRAINE  •  GULF OF FINLAND",
     "ZELENSKIY CONFIRMS SHIP STRIKE",
     "Kyiv says it hit a Russian cargo ship with drones on Saturday. "
     "Norway urges caution. (Reuters)"),
    ("UKRAINE  •  LIBYA",
     "KYIV SINKS RUSSIAN WARSHIP OFF LIBYA",
     "Ukraine claims it sank a Russian warship off Libya, a new reach for "
     "long-range strikes. (Reuters)"),
    ("GAZA",
     "ISRAEL STRIKES GAZA CITY; HAMAS CHIEF KILLED",
     "Naim Abu Nakhla killed; six more die in two other strikes. 1,679 "
     "dead since the ceasefire."),
    ("MARKETS  •  TUESDAY CLOSE",
     "RALLY FADES: NASDAQ -1.5%, DOW +0.9%",
     "Tech gives back Monday's surge; gold -2.3% to $3,552, Bitcoin under "
     "$60,000."),
    ("SPORT  •  NFL WEEK 11",
     "COMMANDERS STUN BENGALS 22-20",
     "Drew Stevens' 26-yard field goal as time expires ends Cincinnati's "
     "five-game win streak."),
]

ALSO_ON = [
    "Sarkozy to face trial; hearing set for 1 Apr 2027",
    "Fort Hood gunman Hasan seeks stay of execution",
    "S. Korea education minister quits in exam-cheat row",
    "Quake, magnitude 5.6, shakes Nepal's Koshi Province",
    "UAE bus-truck crash kills 13 in Ras Al Khaimah",
    "England beat Australia by 8 wickets in 2nd T20I",
    "New Zealand hold India to a draw in 1st Test",
    "Sensex drops 1,484 pts; Nifty slips below 25,400",
    "Trump honours Giuliani with Medal of Freedom",
    "Nepal PM Shah's India visit hailed 'historic'",
    "Iran: three tankers hit by mines in Strait of Hormuz",
    "Houthis 'won't seize Aden', Yemeni forces say",
    "N. Korea threatens to shut Swiss office in Pyongyang",
    "Trump pardons turkeys Freedom and Feathers",
    "Russian jets enter S. Korea air defence zone",
    "UN court: Myanmar guilty of Rohingya genocide",
    "GTA 6 out worldwide since 19 Nov on PS5 and Xbox",
    "OpenAI publishes GPT-6 loss curve, urges limits",
    "Anthropic slips below IPO price, four days on",
    "U.S. to announce higher tariffs on China and the EU",
    "U.S. consumer confidence at near two-year high",
    "49ers cut Aiyuk; beat Vikings 35-10 in Mexico",
    "Shenzhou-24 carries Pakistan's first astronaut",
    "Moscow says 699 drones downed over Ukraine",
    "CAS restores Senegal as Africa Cup champions",
    "Shanghai party chief Chen Jining probed for graft",
    "Hungary's Magyar meets Zelenskiy in Uzhhorod",
    "Ethiopia offers to host Sudan peace talks",
    "WHO evacuates staff from Ituri, DR Congo",
    "Miley Cyrus marries Maxx Morando in Palm Springs",
    "Eisenkot seals first coalition pact in Israel",
    "Car bomb hits governor's office in Meta, Colombia",
    "U2 announce 15 North American stadium shows",
    "Tidal to drop fully AI-made music from 9 Dec",
    "Dozens feared trapped in West Java gold mine",
    "Russia extradites man over $2.3bn deposit fraud",
    "Microsoft declares 'Code Red' after huge outage",
    "Suryavanshi, 15, smashes record 204* off 53 balls",
    "Priyansh Arya hits 181, best T20 score by an Indian",
    "India to buy 76 naval helicopters for Rs 15,000 crore",
    "Hasina plans return to Bangladesh on 16 December",
]

PINNED = [
    ("Zelenskiy confirms drone strike on Russian cargo ship",
     "Gulf of Finland: Kyiv's drones hit a Russian freighter; Norway urges caution."),
    ("Houthis hit the capital's tallest tower",
     "Riyadh: eleven wounded in the second strike on the PIF Tower in five days."),
    ("CIA and ODNI suffer cyber breach",
     "Washington: some unclassified data exposed; extent still unclear."),
    ("Israel strikes kill Hamas security chief",
     "Gaza City: Naim Abu Nakhla among seven killed on Tuesday."),
    ("Three tankers hit by mines",
     "Strait of Hormuz: Iran blames mines in the strait; oil jumps, then eases."),
    ("Quake shakes province near Tibet border",
     "Koshi, Nepal: magnitude 5.6 tremor felt across eastern Nepal."),
]

# Continents as (lon, lat) polygons; projected equirectangular.
CONTINENTS_LL = [
    # North America
    [(-168, 66), (-162, 60), (-155, 58), (-148, 60), (-140, 60), (-134, 57),
     (-128, 52), (-124, 46), (-122, 38), (-118, 33), (-112, 28), (-107, 24),
     (-102, 19), (-96, 16), (-92, 15), (-88, 13), (-84, 10), (-80, 8),
     (-78, 8), (-81, 12), (-84, 15), (-87, 20), (-90, 21), (-92, 18),
     (-96, 19), (-97, 25), (-94, 29), (-89, 30), (-84, 30), (-81, 26),
     (-79, 33), (-75, 37), (-73, 41), (-69, 44), (-65, 44), (-60, 47),
     (-56, 51), (-60, 55), (-64, 59), (-68, 58), (-74, 62), (-80, 64),
     (-86, 66), (-92, 66), (-96, 69), (-108, 68), (-122, 70), (-135, 69),
     (-148, 70), (-158, 71), (-166, 68)],
    # Greenland
    [(-56, 64), (-50, 60), (-43, 60), (-38, 64), (-30, 68), (-24, 70),
     (-20, 74), (-26, 76), (-36, 77), (-48, 76), (-56, 74), (-58, 70)],
    # South America
    [(-79, 9), (-77, 5), (-75, 1), (-79, -3), (-81, -6), (-77, -12),
     (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -50),
     (-68, -55), (-65, -55), (-61, -49), (-57, -44), (-54, -36), (-49, -31),
     (-44, -27), (-40, -22), (-37, -15), (-34, -8), (-35, -6), (-40, -3),
     (-44, -2), (-50, 0), (-53, 4), (-57, 6), (-61, 9), (-66, 11),
     (-71, 12), (-75, 10)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-2, 51)],
    # Iceland
    [(-22, 64), (-18, 63), (-15, 64), (-14, 66), (-18, 66), (-22, 65)],
    # Europe
    [(-10, 36), (-9, 39), (-9, 43), (-3, 48), (-1, 50), (2, 51), (5, 53),
     (8, 57), (10, 59), (12, 61), (16, 64), (20, 67), (25, 71), (30, 70),
     (31, 66), (28, 62), (24, 60), (21, 55), (18, 54), (13, 54), (9, 55),
     (5, 53), (0, 51), (-3, 49), (-5, 48), (-2, 44), (-5, 43), (-9, 43),
     (-10, 38)],
    # Africa
    [(-6, 35), (-1, 35), (5, 37), (10, 37), (11, 34), (16, 32), (20, 32),
     (25, 31), (30, 31), (32, 30), (34, 28), (36, 24), (37, 20), (39, 16),
     (41, 12), (44, 11), (48, 11), (51, 11), (51, 13), (47, 14), (43, 12),
     (41, 9), (40, 4), (40, -1), (38, -6), (36, -11), (35, -16), (33, -21),
     (32, -26), (29, -31), (25, -34), (20, -35), (16, -33), (14, -29),
     (12, -24), (12, -18), (13, -12), (12, -6), (9, 0), (8, 4), (5, 5),
     (-1, 5), (-7, 5), (-12, 8), (-15, 11), (-17, 15), (-16, 20), (-16, 25),
     (-14, 29), (-10, 31)],
    # Madagascar
    [(44, -16), (47, -15), (50, -17), (49, -21), (47, -25), (44, -25),
     (43, -21), (43, -17)],
    # Asia
    [(28, 70), (35, 68), (42, 68), (48, 69), (55, 69), (62, 69), (68, 71),
     (75, 73), (82, 73), (90, 75), (98, 76), (106, 75), (113, 74), (120, 73),
     (128, 72), (135, 72), (142, 72), (150, 70), (157, 69), (162, 66),
     (158, 60), (153, 59), (146, 59), (141, 55), (139, 50), (136, 45),
     (132, 42), (128, 38), (125, 38), (121, 35), (118, 30), (112, 28),
     (108, 24), (105, 20), (102, 14), (100, 8), (98, 10), (96, 14), (93, 18),
     (91, 22), (88, 22), (86, 20), (82, 17), (80, 13), (77, 8), (75, 11),
     (73, 16), (70, 21), (67, 24), (64, 25), (60, 25), (57, 26), (55, 24),
     (58, 21), (55, 17), (50, 14), (44, 13), (42, 17), (40, 23), (38, 29),
     (36, 33), (33, 36), (30, 38), (28, 41), (28, 46), (28, 51), (28, 56),
     (28, 61), (28, 66)],
    # Japan
    [(130, 31), (132, 33), (135, 35), (137, 37), (139, 38), (141, 41),
     (141, 44), (139, 42), (137, 39), (134, 36), (131, 33)],
    # Borneo
    [(109, 1), (112, 4), (116, 6), (119, 3), (118, -1), (115, -3), (111, -2),
     (109, 0)],
    # Sumatra
    [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (103, -5), (100, -2),
     (96, 2)],
    # Java
    [(105, -6), (108, -7), (112, -7), (114, -8), (111, -9), (107, -8)],
    # New Guinea
    [(131, -1), (135, -2), (139, -3), (143, -5), (147, -7), (150, -9),
     (147, -9), (143, -8), (138, -6), (134, -4)],
    # Philippines
    [(120, 18), (121, 16), (122, 13), (124, 11), (122, 8), (120, 10),
     (119, 14)],
    # Sri Lanka
    [(80, 6), (81, 8), (80, 9), (79, 7)],
    # Taiwan
    [(120, 22), (121, 24), (120, 25), (119, 23)],
    # Australia
    [(114, -22), (114, -28), (115, -32), (118, -35), (123, -34), (128, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (144, -38), (148, -37),
     (151, -35), (153, -31), (153, -27), (151, -24), (148, -20), (145, -17),
     (142, -14), (142, -11), (139, -12), (136, -13), (134, -12), (131, -12),
     (128, -14), (125, -15), (122, -17), (118, -20)],
    # New Zealand (north)
    [(167, -35), (169, -37), (171, -39), (173, -41), (175, -41), (173, -39),
     (170, -37)],
    # New Zealand (south)
    [(167, -44), (169, -42), (171, -43), (170, -46), (168, -46), (166, -45)],
]

# Pins: (number, lon, lat, pin_x, pin_y) - pin_x/pin_y are display positions
# (offset with a leader line where the true spot is crowded).
PINS = [
    (1, 26, 59.5, None, None),      # Gulf of Finland
    (2, 46.7, 24.6, None, None),    # Riyadh
    (3, -77, 38.9, None, None),     # Washington
    (4, 34.5, 31.5, -4, -5),         # Gaza City (offset up-left)
    (5, 56.5, 26.5, 7, -6),          # Strait of Hormuz (offset up-right)
    (6, 87, 27, None, None),        # Koshi, Nepal
]

TICKER = ("DOW 50,026 +0.9%  •  S&P 7,202 -0.5%  •  NASDAQ 23,734 -1.5%  •  "
          "GOLD $3,552 -2.3%  •  BRENT $91.40 +2.3%  •  BTC $59,700 -2.4%")
SOURCES = ("Sources: Reuters, BBC, CNN, AP, Al Jazeera, Morningstar, "
           "Investopedia, ESPN, Channel NewsAsia. All stories first reported "
           "24-25 Nov 2026; no forecasts.")

# Map panel geometry (left half of the map band).
MAP_X0, MAP_X1 = 26, 496
MAP_Y0, MAP_Y1 = 318, 554
MAP_LON0, MAP_LON1 = -168, 192
MAP_LAT0, MAP_LAT1 = 72, -56


def project(lon, lat):
    x = MAP_X0 + (lon - MAP_LON0) / (MAP_LON1 - MAP_LON0) * (MAP_X1 - MAP_X0)
    y = MAP_Y0 + 24 + (MAP_LAT0 - lat) / (MAP_LAT0 - MAP_LAT1) * (MAP_Y1 - MAP_Y0 - 24)
    return x, y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx0, mx1 = 26, 998  # content margins

    # ---- masthead
    f_mast = font(SERIF_B, 62)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 14), title, font=f_mast, fill=INK)
    rule(d, mx0, mx1, 88, INK, 3)
    rule(d, mx0, mx1, 93, INK, 1)

    # ---- date line
    f_date = font(SANS_B, 16)
    f_date_r = font(SANS_B, 15)
    d.text((mx0, 100), "WEDNESDAY, 25 NOVEMBER 2026", font=f_date, fill=INK)
    right = "50 STORIES  •  6 CONTINENTS  •  ONE PAGE"
    d.text((mx1 - d.textlength(right, font=f_date_r), 101), right,
           font=f_date_r, fill=RED)
    rule(d, mx0, mx1, 122, INK, 2)

    # ---- hero row (132-308)
    f_kick = font(SANS_B, 13)
    f_head = font(SERIF_B, 36)
    f_deck = font(SANS, 15)
    d.text((mx0, 132), HERO_LEAD[0], font=f_kick, fill=RED)
    y2 = draw_wrapped(d, mx0, 152, HERO_LEAD[1], f_head, 600,
                      leading=41, max_lines=2)
    draw_wrapped(d, mx0, y2 + 4, HERO_LEAD[2], f_deck, 600, leading=18,
                 max_lines=2)
    # right column: two compact stories
    rx = 660
    d.line([(rx - 18, 132), (rx - 18, 308)], fill=(200, 200, 192), width=1)
    f_h2 = font(SERIF_B, 17)
    f_d2 = font(SANS, 12)
    yy = 132
    for kick, head, deck in (HERO_2, HERO_3):
        d.text((rx, yy), kick, font=f_kick, fill=RED)
        yy = draw_wrapped(d, rx, yy + 18, head, f_h2, 338, leading=20,
                          max_lines=2)
        yy = draw_wrapped(d, rx, yy + 2, deck, f_d2, 338, leading=14,
                          max_lines=2)
        yy += 10
        if kick == HERO_2[0]:
            d.line([(rx, yy - 4), (rx + 338, yy - 4)],
                   fill=(210, 210, 202), width=1)

    # ---- map band (318-554)
    d.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], fill=MAP_BG,
                outline=(200, 210, 216))
    f_map_t = font(SANS_B, 13)
    d.text((MAP_X0 + 10, MAP_Y0 + 6), "THE WORLD ON ONE MAP",
           font=f_map_t, fill=INK)
    # graticule
    for gx in range(MAP_X0 + 94, MAP_X1, 94):
        d.line([(gx, MAP_Y0 + 24), (gx, MAP_Y1)], fill=(214, 224, 230),
               width=1)
    for gy in range(MAP_Y0 + 24 + 41, MAP_Y1, 41):
        d.line([(MAP_X0, gy), (MAP_X1, gy)], fill=(214, 224, 230), width=1)
    for poly in CONTINENTS_LL:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    f_pin = font(SANS_B, 11)
    for num, lon, lat, dx, dy in PINS:
        tx, ty = project(lon, lat)
        px, py = tx + (dx or 0), ty + (dy or 0)
        if dx or dy:
            d.line([(tx, ty), (px, py)], fill=(120, 120, 120), width=1)
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=PIN)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=PIN,
                  outline=(255, 255, 255), width=2)
        t = str(num)
        d.text((px - d.textlength(t, font=f_pin) / 2, py - 7), t,
               font=f_pin, fill=(255, 255, 255))
    # right panel: pinned stories (2 lines each: headline + sub)
    px0 = 514
    d.text((px0, MAP_Y0 + 6), "PINNED ON THE MAP", font=f_map_t, fill=INK)
    f_ph = font(SANS_B, 14)
    f_ps = font(SANS, 12)
    f_num = font(SANS_B, 11)
    py = MAP_Y0 + 32
    for i, (head, sub) in enumerate(PINNED, start=1):
        cx, cy = px0 + 10, py + 9
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=PIN)
        t = str(i)
        d.text((cx - d.textlength(t, font=f_num) / 2, cy - 7), t,
               font=f_num, fill=(255, 255, 255))
        d.text((px0 + 28, py), head, font=f_ph, fill=INK)
        d.text((px0 + 28, py + 17), sub, font=f_ps, fill=GRAY)
        py += 34
        if i < len(PINNED):
            d.line([(px0, py - 6), (mx1, py - 6)], fill=(222, 222, 214),
                   width=1)

    # ---- grid: 6 stories, 3 cols x 2 rows (564-744)
    f_gk = font(SANS_B, 11)
    f_gh = font(SERIF_B, 17)
    f_gd = font(SANS, 12)
    col_w, gutter = 312, 18
    gy0 = 564
    for i, (kick, head, deck) in enumerate(GRID):
        col, row = i % 3, i // 3
        x = mx0 + col * (col_w + gutter)
        y = gy0 + row * 90
        d.text((x, y), kick, font=f_gk, fill=RED)
        y = draw_wrapped(d, x, y + 15, head, f_gh, col_w, leading=20,
                         max_lines=2)
        draw_wrapped(d, x, y + 2, deck, f_gd, col_w, leading=14,
                     max_lines=2)
        if col < 2:
            d.line([(x + col_w + 9, gy0), (x + col_w + 9, gy0 + 178)],
                   fill=(210, 210, 202), width=1)
    rule(d, mx0, mx1, 752, INK, 2)

    # ---- ALSO ON: 41 one-liners, 3 cols (760-959)
    f_ao_h = font(SANS_B, 13)
    f_ao = font(SANS, 11)
    d.text((mx0, 760), "ALSO ON  •  41 MORE STORIES FROM THE DAY",
           font=f_ao_h, fill=RED)
    cols = [ALSO_ON[0:14], ALSO_ON[14:28], ALSO_ON[28:41]]
    ay = 782
    for ci, items in enumerate(cols):
        x = mx0 + ci * (col_w + gutter)
        yy = ay
        for it in items:
            d.text((x, yy), "\u2022  " + it, font=f_ao, fill=INK)
            yy += 13
    rule(d, mx0, mx1, 964, INK, 2)

    # ---- footer
    f_tick = font(SANS_B, 12)
    tw2 = d.textlength(TICKER, font=f_tick)
    d.text(((W - tw2) / 2, 972), TICKER, font=f_tick, fill=INK)
    f_src = font(SANS, 10)
    sw = d.textlength(SOURCES, font=f_src)
    d.text(((W - sw) / 2, 991), SOURCES, font=f_src, fill=GRAY)

    img.save(OUT, format="PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
