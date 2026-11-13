"""minipdf.py · the always-there fallback: the session as a plain one-page PDF, standard library only.

Used only when no browser can print the HTML. Helvetica, Latin script (accents included through
WinAnsi). It shrinks the type until the page fits, and never cuts content.
"""
import zlib

W, H = 595.0, 842.0           # A4 in points
LETTER = (612.0, 792.0)
M = 36.0


def _enc(t):
    t = str(t if t is not None else "")
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    b = t.encode("cp1252", "replace")
    return b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


def _width(t, size):
    return len(str(t)) * size * 0.52       # Helvetica average, good enough for wrapping


def _wrap(t, size, width):
    words, lines, cur = str(t or "").split(), [], ""
    for w in words:
        if _width(cur + " " + w, size) > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines or [""]


def _layout(s, L, scale, pw, ph):
    ops, y = [], ph - M
    width = pw - 2 * M

    def text(x, yy, t, size, bold=False):
        ops.append(b"BT /%s %.1f Tf %.1f %.1f Td (" % (b"F2" if bold else b"F1", size * scale, x, yy) + _enc(t) + b") Tj ET")

    def line(x1, y1, x2, y2, w=0.6):
        ops.append(b"%.1f w %.1f %.1f m %.1f %.1f l S" % (w, x1, y1, x2, y2))

    def box(x, yy, w, h):
        ops.append(b"0.8 w %.1f %.1f %.1f %.1f re S" % (x, yy, w, h))

    def para(t, size, bold=False, indent=0):
        nonlocal y
        for ln in _wrap(t, size * scale, width - indent):
            y -= size * scale * 1.3
            text(M + indent, y, ln, size, bold)

    para("PERSONAL TRAINER", 7)
    para(s.get("title", ""), 16, True)
    para(" · ".join(str(x) for x in [s.get("date"), s.get("program_name"), s.get("level_text")] if x), 8)
    y -= 4
    line(M, y, pw - M, y, 1.2)
    if s.get("score_to_beat"):
        para("%s: %s" % (L["score"], s["score_to_beat"]), 10, True)
    if s.get("why"):
        para(s["why"], 8.5)
    for b in s.get("blocks", []):
        y -= 6
        para(str(b.get("name", "")).upper() + ("   " + b["rest_note"] if b.get("rest_note") else ""), 10, True)
        line(M, y - 2, pw - M, y - 2)
        for it in b.get("items", []):
            row = "%s   %s x %s   %s   %s   %s %s" % (it.get("name") or it.get("ex"), it.get("sets", ""), it.get("reps", ""),
                                                  it.get("load", ""), it.get("effort", ""), L["rest"], it.get("rest_text", it.get("rest", "")))
            para(row, 9, True, 4)
            n = int(it.get("sets") or 1)
            for k in range(min(n, 10)):
                box(pw - M - (k + 1) * 11, y, 8 * scale, 8 * scale)
            if it.get("cue"):
                para(it["cue"], 8, False, 8)
            if it.get("first_outing"):
                para("%s: %s" % (L["first"], it["first_outing"]), 8, False, 8)
    y -= 6
    if s.get("low_energy"):
        para("%s: %s" % (L["low"], s["low_energy"]), 8.5)
    if s.get("log"):
        para(L["log"], 8.5, True)
        for x in s["log"]:
            para("%s ______________________________" % x, 8.5, False, 4)
    para(L["footer"], 7)
    return ops, y


def write(s, path, L):
    pw, ph = LETTER if str(s.get("paper", "A4")).lower().startswith("letter") else (W, H)
    scale = 1.0
    while True:
        ops, y = _layout(s, L, scale, pw, ph)
        if y > M or scale < 0.55:
            break
        scale -= 0.05
    content = zlib.compress(b"\n".join(ops))
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.0f %.0f] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>" % (pw, ph),
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
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
