"""minipdf.py · the always-there fallback: the session as a one-page PDF, standard library only.

Used when no browser can print the HTML (the web page runs the engine in the browser, where there
is no Chrome). It draws the same workout form as the HTML sheet, from the same model (sheet.form):
the title large with the date and the minutes, the warm-up, the work and the cool-down as sections,
per exercise the target in mono, a cell per set for the weight used and the reps done with a tick,
a "how hard" 1 to 5 to circle, then a notes area. Ink #2B1A1C, burgundy #8E2440 on rules and headers only. The 14 standard PDF fonts only
(Helvetica, Helvetica-Bold, Courier-Bold for the numbers), Latin script through WinAnsi. It shrinks
the whole layout until it fits one page, and never cuts content.
"""
import math, unicodedata, zlib

W, H = 595.0, 842.0           # A4 in points
LETTER = (612.0, 792.0)
M = 40.0                      # page margin

INK = (0.169, 0.102, 0.110)          # #2B1A1C
SOFT = (0.435, 0.384, 0.392)         # ink at about 65%
FAINT = (0.890, 0.863, 0.867)        # hairlines
ACCENT = (0.557, 0.141, 0.251)       # #8E2440
TINT = (0.973, 0.937, 0.945)         # the accent at about 7%, the score box
CARD = (0.984, 0.976, 0.973)         # the why box

# Helvetica and Helvetica-Bold advance widths (1/1000 em), ASCII 32 to 126, from the Adobe AFM files.
_HV = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278] + [556] * 10 + \
      [278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
       667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556,
       278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334,
       260, 334, 584]
_HB = [278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278] + [556] * 10 + \
      [333, 333, 584, 584, 584, 611, 975, 722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722, 778,
       667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584, 556, 333, 556, 611, 556, 611, 556,
       333, 611, 611, 278, 278, 556, 278, 889, 611, 611, 611, 611, 389, 556, 333, 611, 556, 778, 556, 556, 500, 389,
       280, 389, 584]
_EXTRA = {"·": 278, "×": 584, "’": 222, "‘": 222, "“": 333, "”": 333, "–": 556, "€": 556, "°": 400, "…": 1000}
FONTS = {"R": b"F1", "B": b"F2", "N": b"F3"}       # regular, bold, numbers


def _clean(t):
    return str(t if t is not None else "").replace("\n", " ")


def _enc(t):
    b = _clean(t).encode("cp1252", "replace")
    return b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


def _cw(ch, font):
    if font == "N":
        return 600
    table = _HB if font == "B" else _HV
    o = ord(ch)
    if 32 <= o <= 126:
        return table[o - 32]
    if ch in _EXTRA:
        return _EXTRA[ch]
    base = unicodedata.normalize("NFD", ch)[0]       # an accented letter is as wide as its letter
    return table[ord(base) - 32] if 32 <= ord(base) <= 126 else 556


def width(t, size, font="R", track=0.0):
    t = _clean(t)
    return sum(_cw(c, font) for c in t) * size / 1000.0 + track * len(t)


def wrap(t, size, w, font="R"):
    words, lines, cur = _clean(t).split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if cur and width(trial, size, font) > w:
            lines.append(cur)
            cur = wd
        else:
            cur = trial
        while width(cur, size, font) > w and len(cur) > 1:     # one word wider than the column: break it
            k = len(cur)
            while k > 1 and width(cur[:k], size, font) > w:
                k -= 1
            lines.append(cur[:k])
            cur = cur[k:]
    if cur:
        lines.append(cur)
    return lines or [""]


class Page:
    """A list of PDF drawing operators, y measured from the bottom of the page as PDF wants."""

    def __init__(self):
        self.ops = []

    def color(self, rgb, stroke=False):
        self.ops.append(b"%.3f %.3f %.3f %s" % (tuple(rgb) + ((b"RG",) if stroke else (b"rg",))))

    def text(self, x, y, t, size, font="R", rgb=INK, track=0.0):
        self.color(rgb)
        tc = b"%.2f Tc " % track if track else b""
        self.ops.append(b"BT /%s %.2f Tf %s%.2f %.2f Td (" % (FONTS[font], size, tc, x, y) + _enc(t) + b") Tj ET" +
                        (b" 0 Tc" if track else b""))

    def rtext(self, xr, y, t, size, font="R", rgb=INK, track=0.0):
        self.text(xr - width(t, size, font, track), y, t, size, font, rgb, track)

    def line(self, x1, y1, x2, y2, w=0.5, rgb=FAINT, dash=None):
        self.color(rgb, True)
        d = (b"[%.1f %.1f] 0 d " % dash) if dash else b""
        self.ops.append(d + b"%.2f w %.2f %.2f m %.2f %.2f l S" % (w, x1, y1, x2, y2) + (b" [] 0 d" if dash else b""))

    def rrect(self, x, y, w, h, r=4.0, fill=None, stroke=None, lw=0.6, dash=None):
        """A rounded rectangle, (x, y) its bottom left corner."""
        k = 0.5523 * r
        p = [b"%.2f %.2f m" % (x + r, y), b"%.2f %.2f l" % (x + w - r, y),
             b"%.2f %.2f %.2f %.2f %.2f %.2f c" % (x + w - r + k, y, x + w, y + r - k, x + w, y + r),
             b"%.2f %.2f l" % (x + w, y + h - r),
             b"%.2f %.2f %.2f %.2f %.2f %.2f c" % (x + w, y + h - r + k, x + w - r + k, y + h, x + w - r, y + h),
             b"%.2f %.2f l" % (x + r, y + h),
             b"%.2f %.2f %.2f %.2f %.2f %.2f c" % (x + r - k, y + h, x, y + h - r + k, x, y + h - r),
             b"%.2f %.2f l" % (x, y + r),
             b"%.2f %.2f %.2f %.2f %.2f %.2f c h" % (x, y + r - k, x + r - k, y, x + r, y)]
        if fill:
            self.color(fill)
        if stroke:
            self.color(stroke, True)
        d = (b"[%.1f %.1f] 0 d " % dash) if dash else b""
        op = b"B" if fill and stroke else (b"f" if fill else b"S")
        self.ops.append(d + b"%.2f w " % lw + b" ".join(p) + b" " + op + (b" [] 0 d" if dash else b""))

    def dot(self, cx, cy, r, rgb):
        self.rrect(cx - r, cy - r, 2 * r, 2 * r, r, fill=rgb)

    def star(self, cx, cy, r, rgb=ACCENT):
        pts = []
        for i in range(10):
            a = math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.42
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        self.color(rgb)
        self.ops.append(b"%.2f %.2f m " % pts[0] + b" ".join(b"%.2f %.2f l" % p for p in pts[1:]) + b" h f")


def _labels(L):
    base = {"score": "Score to beat", "why": "Why this session", "sets": "Sets x reps", "load": "Load", "effort": "Effort",
            "rest": "Rest", "total": "Total", "min": "min", "log": "After the session, write down", "low": "If your energy drops",
            "first": "First time: find your weight", "done": "Done", "footer": "", "rest_none": "none", "block": "Block",
            "week": "week"}
    base.update(L or {})
    return base


def _layout(s, L, k, pw, ph):
    """Draw the form at scale k (sheet.form is the one model both renderers draw). Returns (operators, lowest y)."""
    import sheet
    f = sheet.form(s)
    L = dict(f["L"], **{kk: v for kk, v in (L or {}).items() if v})
    pg = Page()
    m = M * (0.75 + 0.25 * k)
    x0, x1 = m, pw - m
    cw = x1 - x0
    y = ph - m

    def S(v):                                          # every size and gap scales together
        return v * k

    # · header: wordmark, title large, meta · on the right the date and the minutes · a thin burgundy rule
    y -= S(8)
    pg.dot(x0 + S(2.8), y + S(2.4), S(2.8), ACCENT)
    pg.text(x0 + S(10), y, "PERSONAL TRAINER", S(7.2), "B", SOFT, track=S(1.1))
    right_w = S(110)
    top_y = y
    for ln in wrap(f["title"], S(21), cw - right_w, "B"):
        y -= S(24)
        pg.text(x0, y, ln, S(21), "B", INK)
    for ln in wrap(f["meta"], S(8.4), cw - right_w):
        y -= S(11.5)
        pg.text(x0, y, ln, S(8.4), "R", SOFT)
    pg.rtext(x1, top_y, f["date"], S(8.6), "N", SOFT)
    mins = "%d" % f["minutes"]
    unit_w = width(" " + L["min"], S(9), "R")
    pg.rtext(x1, top_y - S(26), " " + L["min"], S(9), "R", SOFT)
    pg.rtext(x1 - unit_w, top_y - S(26), mins, S(20), "N", INK)
    y -= S(8)
    pg.line(x0, y, x1, y, S(1.1), ACCENT)
    y -= S(10)

    # · the score to beat and the why, side by side, neutral cards
    if f["beat"] or f["why"]:
        gap, pad = S(8), S(8)
        wl = (cw - gap) * 0.42
        wr = cw - gap - wl
        beat = wrap(f["beat"], S(10.2), wl - 2 * pad, "B")
        why = wrap(f["why"], S(8.2), wr - 2 * pad)
        h = 2 * pad + S(10) + max(len(beat) * S(13), len(why) * S(10.8))
        pg.rrect(x0, y - h, wl, h, S(4), fill=CARD, stroke=FAINT, lw=S(0.7))
        pg.rrect(x0 + wl + gap, y - h, wr, h, S(4), fill=CARD, stroke=FAINT, lw=S(0.7))
        yy = y - pad - S(6)
        pg.text(x0 + pad, yy, L["score"].upper(), S(6.6), "B", ACCENT, track=S(0.9))
        pg.text(x0 + wl + gap + pad, yy, L["why"].upper(), S(6.6), "B", SOFT, track=S(0.9))
        yb = yy - S(2)
        for ln in beat:
            yb -= S(13)
            pg.text(x0 + pad, yb, ln, S(10.2), "B", INK)
        yw = yy - S(1)
        for ln in why:
            yw -= S(10.8)
            pg.text(x0 + wl + gap + pad, yw, ln, S(8.2), "R", INK)
        y -= h + S(9)

    # · first outings: one legend, a star per distinct instruction
    if f["firsts"]:
        pad = S(7)
        indent = S(8) * len(f["firsts"]) + S(6)
        rows = [wrap(x, S(7.8), cw - 2 * pad - indent) for x in f["firsts"]]
        h = 2 * pad + S(9) + sum(len(r) * S(10.2) for r in rows)
        pg.rrect(x0, y - h, cw, h, S(4), stroke=SOFT, lw=S(0.6), dash=(S(2.5), S(2)))
        yy = y - pad - S(6)
        pg.text(x0 + pad, yy, L["first"].upper(), S(6.6), "B", ACCENT, track=S(0.9))
        for i, r in enumerate(rows):
            for j, ln in enumerate(r):
                yy -= S(10.2)
                if j == 0:
                    for n in range(i + 1):
                        pg.star(x0 + pad + S(3.5) + n * S(8), yy + S(2.7), S(3.2))
                pg.text(x0 + pad + indent, yy, ln, S(7.8), "R", INK)
        y -= h + S(10)

    # · the sections: warm-up, the work, cool-down
    lw = cw * 0.36                                     # the left column of a set row
    hard_w = S(74)
    cell_w, cell_h, cgap = S(62), S(30), S(4)
    cells_x = x0 + lw + S(10)
    cells_w = x1 - hard_w - S(10) - cells_x
    per_row = max(1, int((cells_w + cgap) // (cell_w + cgap)))
    for n_sec, sec in enumerate(f["sections"]):
        y -= S(10) if n_sec == 0 else S(20)
        pg.text(x0, y, str(sec["title"]).upper(), S(9.2), "B", ACCENT, track=S(1.0))
        right = ("%d %s" % (sec["minutes"], L["min"])) if sec.get("minutes") is not None else ""
        if right:
            pg.rtext(x1, y, right, S(8), "N", SOFT)
        if sec.get("note"):
            pg.rtext(x1 - (width(right, S(8), "N") + S(8) if right else 0), y, sec["note"] + (" ·" if right else ""), S(7.6), "R", SOFT)
        y -= S(4)
        pg.line(x0, y, x1, y, S(0.9), ACCENT)
        for r in sec["rows"]:
            if r["kind"] == "check":
                nx, tx, qx = x0 + S(14), x0 + cw * 0.40, x0 + cw * 0.58
                name = wrap(r["name"], S(9), tx - nx - S(6), "B")
                cue = wrap(r.get("cue", ""), S(7.4), x1 - qx) if r.get("cue") else []
                tgt = wrap(r.get("target", ""), S(8.4), qx - tx - S(6), "N")
                lines = max(len(name), len(cue), len(tgt), 1)
                yy = y - S(4)
                pg.rrect(x0 + S(1), yy - S(8.5), S(8), S(8), S(1.5), stroke=INK, lw=S(0.8))
                for j, ln in enumerate(name):
                    pg.text(nx, yy - S(8) - j * S(11), ln, S(9), "B", INK)
                for j, ln in enumerate(tgt):
                    pg.text(tx, yy - S(8) - j * S(11), ln, S(8.4), "N", INK)
                for j, ln in enumerate(cue):
                    pg.text(qx, yy - S(8) - j * S(11), ln, S(7.4), "R", SOFT)
                y = yy - S(4) - lines * S(11)
                pg.line(x0, y, x1, y, S(0.5), FAINT)
                continue
            yy = y - S(6)
            # left: name and stars, the target in mono, the effort, the cue
            star = r.get("star", 0)
            name = wrap(r["name"], S(9.6), lw - (star * S(7.5) + S(6) if star else 0), "B")
            ly = yy
            for j, ln in enumerate(name):
                ly -= S(10)
                pg.text(x0, ly, ln, S(9.6), "B", INK)
                if star and j == len(name) - 1:
                    sx = x0 + width(ln, S(9.6), "B") + S(6)
                    for q in range(star):
                        pg.star(sx + q * S(7.5), ly + S(3.3), S(3.1))
                ly -= S(2)
            tgt = " · ".join(v for v in [r.get("target"), r.get("load"), (L["rest"].lower() + " " + r["rest"]) if r.get("rest") else ""] if v)
            for ln in wrap(tgt, S(8.4), lw, "N"):
                ly -= S(10.5)
                pg.text(x0, ly, ln, S(8.4), "N", INK)
            for ln in wrap(r.get("effort", ""), S(7.6), lw) if r.get("effort") else []:
                ly -= S(9.6)
                pg.text(x0, ly, ln, S(7.6), "R", INK)
            for ln in wrap(r.get("cue", ""), S(7.4), lw) if r.get("cue") else []:
                ly -= S(9.4)
                pg.text(x0, ly, ln, S(7.4), "R", SOFT)
            # middle: one cell per set (weight, reps, tick) or one wide cell for a score
            if r["kind"] == "score":
                cells = [(cell_w * 2 + cgap, [r["cell"]], None)]
            else:
                labs = ([r["weight"]] if r.get("weight") else []) + [L["reps"]]
                cells = [(cell_w, labs, str(q + 1)) for q in range(r["n"])]
            cy = yy
            for q, (w_, labs, num) in enumerate(cells):
                col = q % per_row if r["kind"] == "sets" else 0
                if q and col == 0:
                    cy -= cell_h + cgap
                cx_ = cells_x + col * (cell_w + cgap)
                pg.rrect(cx_, cy - cell_h, w_, cell_h, S(2.5), stroke=INK, lw=S(0.8))
                tx_ = cx_ + S(3.5)
                if num:
                    pg.text(tx_, cy - S(7.5), num, S(6.4), "N", INK)
                    tx_ += width(num, S(6.4), "N") + S(4)
                if len(labs) == 2:                          # weight on the left, reps on the right, a faint divider
                    mid = cx_ + w_ * 0.5 + S(2)
                    pg.line(mid, cy - S(4), mid, cy - cell_h + S(4), S(0.5), FAINT)
                    pg.text(tx_, cy - S(7.5), labs[0].upper(), S(5.6), "N", SOFT)
                    pg.text(mid + S(3), cy - S(7.5), labs[1].upper(), S(5.6), "N", SOFT)
                else:
                    pg.text(tx_, cy - S(7.5), labs[0].upper(), S(5.6), "N", SOFT)
                pg.rrect(cx_ + w_ - S(11), cy - cell_h + S(3), S(8), S(8), S(1.5), stroke=INK, lw=S(0.7))
            cells_bottom = cy - cell_h
            # right: how hard, 1 to 5, to circle
            hx = x1 - hard_w
            pg.text(hx, yy - S(6.5), L["hard"].upper(), S(5.8), "B", SOFT, track=S(0.5))
            for q in range(5):
                ccx = hx + S(6) + q * S(14.5)
                pg.rrect(ccx - S(6), yy - S(23), S(12), S(12), S(6), stroke=SOFT, lw=S(0.6))
                pg.text(ccx - width(str(q + 1), S(6.6), "N") / 2, yy - S(19.3), str(q + 1), S(6.6), "N", INK)
            y = min(ly, cells_bottom, yy - S(25)) - S(7)
            pg.line(x0, y, x1, y, S(0.5), FAINT)

    # · notes: how it felt, any pain; what to tell the trainer; the low energy rule
    y -= S(20)
    pg.text(x0, y, L["notes"].upper(), S(9.2), "B", ACCENT, track=S(1.0))
    pg.rtext(x1, y, L["notes_hint"], S(7.8), "R", SOFT)
    y -= S(4)
    pg.line(x0, y, x1, y, S(0.9), ACCENT)
    for _ in range(3):
        y -= S(17)
        pg.line(x0, y, x1, y, S(0.6), INK)
    for lead, body in ((L["tell"], " · ".join(f["log"])), (L["low"], f["low"])):
        if not body:
            continue
        ind = width(lead + "  ", S(7.4), "B")
        y -= S(10)
        pg.text(x0, y, lead, S(7.4), "B", INK)
        for j, ln in enumerate(wrap(body, S(7.4), cw - ind)):
            if j:
                y -= S(9.4)
            pg.text(x0 + ind, y, ln, S(7.4), "R", SOFT)

    # · the footer
    y -= S(9)
    pg.line(x0, y, x1, y, S(0.5), FAINT)
    for ln in wrap(f["footer"], S(6.6), cw):
        y -= S(8.6)
        pg.text(x0, y, ln, S(6.6), "R", SOFT)
    return pg.ops, y


def write(s, path, L):
    pw, ph = LETTER if str(s.get("paper", "A4")).lower().startswith("letter") else (W, H)
    L = _labels(L)
    k = 1.0
    while True:
        ops, y = _layout(s, L, k, pw, ph)
        if y >= M * 0.6 or k < 0.5:
            break
        k -= 0.04
    content = zlib.compress(b"\n".join(ops))

    def font(name):
        return b"<< /Type /Font /Subtype /Type1 /BaseFont /%s /Encoding /WinAnsiEncoding >>" % name
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.0f %.0f] /Resources << /Font << /F1 4 0 R /F2 5 0 R /F3 6 0 R >> >> "
            b"/Contents 7 0 R >>" % (pw, ph),
            font(b"Helvetica"), font(b"Helvetica-Bold"), font(b"Courier-Bold"),
            b"<< /Length %d /Filter /FlateDecode >>\nstream\n" % len(content) + content + b"\nendstream"]
    out, offs = bytearray(b"%PDF-1.4\n"), []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for o in offs:
        out += b"%010d 00000 n \n" % o
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    open(path, "wb").write(bytes(out))
