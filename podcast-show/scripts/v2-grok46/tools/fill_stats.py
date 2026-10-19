#!/usr/bin/env python3
"""Fill the computed numbers in a v2 script header and its show notes, so the
counts the checker compares are never typed by hand.

Usage: python3 scripts/v2/tools/fill_stats.py scripts/v2/E003-nobody-ever-gave-you-the-sentence.md

Updates, in the script header: the 'Spoken words' row, the 'Line balance' row
and the 'Board cues' row. In the show notes: the '(N spoken words, about MM:SS)'
phrase, the chapter-table start times (in order), and the character counts on
the Title and Meta description blocks. Writing only; the checker still decides.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_script as cs  # noqa: E402


def stats(text):
    header, body = text.split("## OPEN", 1)
    body = "## OPEN" + body
    segs, lines, boards, cur = [], [], 0, None
    for raw in body.splitlines():
        if raw.startswith("## "):
            cur = raw[3:].strip()
            segs.append([cur, 0])
            continue
        m = re.match(r"^([A-Z][A-Z .'\-]*[A-Z]):\s*(.*)$", raw)
        if m:
            n = len(cs.words(m.group(2)))
            lines.append((m.group(1), n))
            segs[-1][1] += n
        boards += len(re.findall(r"\[BOARD:", raw))
    return segs, lines, boards


def main(path):
    text = open(path, encoding="utf-8").read()
    segs, lines, boards = stats(text)
    total = sum(n for _, n in lines)
    wes = [n for s, n in lines if s == "WES"]
    jon = [n for s, n in lines if s == "JONATHON"]
    short = [n for n in jon if n < cs.SHORT]
    ww, jw = sum(wes), sum(jon)
    text = re.sub(r"^\| Spoken words \|[^\n]*$",
                  f"| Spoken words | {total:,} (about {cs.mmss(total)} at 150 wpm, before laughs and pauses) |", text, flags=re.M)
    text = re.sub(r"^\| Line balance \|[^\n]*$",
                  f"| Line balance | WES {len(wes)} lines ({round(100*ww/total)}% of words). JONATHON {len(jon)} lines "
                  f"({round(100*jw/total)}% of words), {len(short)} under 12 words ({100*len(short)/max(1,len(jon)):.1f}%) |", text, flags=re.M)
    text = re.sub(r"^\| Board cues \| *\d+", f"| Board cues | {boards}", text, flags=re.M)
    open(path, "w", encoding="utf-8").write(text)
    m = re.match(r"^(E\d{3})-", os.path.basename(path))
    notes = os.path.join(os.path.dirname(path), f"{m.group(1)}-show-notes.md")
    if os.path.exists(notes):
        nt = open(notes, encoding="utf-8").read()
        nt = re.sub(r"\([\d,]+ spoken words, about \d\d:\d\d\)", f"({total:,} spoken words, about {cs.mmss(total)})", nt)
        times, t = [], 0
        for _, n in segs:
            times.append(cs.mmss(t))
            t += n
        it = iter(times)
        nt = re.sub(r"^\|\s*\d\d:\d\d\s*\|", lambda mm: f"| {next(it, '99:99')} |", nt, flags=re.M)
        for label in ("Title", "Meta description"):
            mm = re.search(r"\*\*" + label + r" \((\d+) characters\)\*\*\s*\n(.+)", nt)
            if mm:
                nt = nt.replace(mm.group(0), mm.group(0).replace(f"({mm.group(1)} characters)", f"({len(mm.group(2).strip())} characters)"), 1)
        open(notes, "w", encoding="utf-8").write(nt)
    print(f"{os.path.basename(path)}: {total} words ({cs.mmss(total)}), WES {round(100*ww/total)}% / JONATHON {round(100*jw/total)}%, "
          f"J short {len(short)}/{len(jon)}, boards {boards}, segments {len(segs)}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
