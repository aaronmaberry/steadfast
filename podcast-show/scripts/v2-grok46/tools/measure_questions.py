#!/usr/bin/env python3
"""Count host-to-host questions: a spoken line with '?' whose next spoken line is the other host."""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINE = re.compile(r"^(WES|JONATHON):\s*(.*)$")


def spoken(path):
    text = open(path, encoding="utf-8").read()
    if "## OPEN" not in text:
        return []
    body = "## OPEN" + text.split("## OPEN", 1)[1]
    out = []
    for raw in body.splitlines():
        m = LINE.match(raw)
        if m:
            s = re.sub(r"\[[^\]]*\]", " ", m.group(2))
            s = re.sub(r"“[^”]*”", " ", s)
            s = re.sub(r'"[^"]*"', " ", s)
            out.append((m.group(1), s))
    return out


def count_q(path):
    lines = spoken(path)
    n = 0
    for i, (spk, text) in enumerate(lines[:-1]):
        if "?" not in text:
            continue
        nxt = lines[i + 1][0]
        if nxt != spk:
            n += 1
    return n, len(lines)


def main(paths):
    if not paths:
        paths = sorted(
            p
            for p in glob.glob(os.path.join(ROOT, "E0*.md"))
            if not p.endswith("show-notes.md")
        )
    rows = []
    for p in paths:
        q, nlines = count_q(p)
        rows.append((os.path.basename(p), q, nlines))
    qs = [r[1] for r in rows]
    print(f"{'file':52} q  lines")
    for name, q, n in rows:
        flag = "  **" if q < 4 and not name.startswith("E007") else ""
        print(f"{name:52} {q:2} {n:5}{flag}")
    print(
        f"\n{len(rows)} scripts. questions min={min(qs)} avg={sum(qs)/len(qs):.1f} max={max(qs)}."
    )


if __name__ == "__main__":
    main(sys.argv[1:])
