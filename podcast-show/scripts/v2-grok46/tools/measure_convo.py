#!/usr/bin/env python3
"""Conversation-pass metrics for v2 scripts."""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINE = re.compile(r"^(WES|JONATHON):\s*(.*)$")
FULL = re.compile(
    r"\b(I am|do not|it is|that is|you are|we are|they are|I have|we have|"
    r"he is|she is|cannot|will not|would not|did not|was not|were not|"
    r"is not|are not)\b",
    re.I,
)
CONTR = re.compile(
    r"\b(I'm|don't|it's|that's|you're|we're|they're|I've|we've|he's|she's|"
    r"can't|won't|wouldn't|didn't|wasn't|weren't|isn't|aren't)\b",
    re.I,
)
WORD = re.compile(r"[A-Za-z0-9@][A-Za-z0-9'’.\-@]*")


def spoken_lines(path):
    text = open(path, encoding="utf-8").read()
    if "## OPEN" not in text:
        return []
    body = "## OPEN" + text.split("## OPEN", 1)[1]
    out = []
    for raw in body.splitlines():
        m = LINE.match(raw)
        if m:
            out.append((m.group(1), m.group(2)))
    return out


def strip_quotes(s):
    s = re.sub(r"\[[^\]]*\]", " ", s)
    s = re.sub(r"“[^”]*”", " ", s)
    s = re.sub(r'"[^"]*"', " ", s)
    return s


def metrics(path):
    lines = spoken_lines(path)
    run = max_run = 1
    stacks = 0
    for i in range(1, len(lines)):
        if lines[i][0] == lines[i - 1][0]:
            run += 1
            if run > max_run:
                max_run = run
            if run == 3:
                stacks += 1
        else:
            run = 1
    body = " ".join(strip_quotes(t) for _, t in lines)
    nf, nc = len(FULL.findall(body)), len(CONTR.findall(body))
    jl = [t for s, t in lines if s == "JONATHON"]
    jshort = sum(1 for t in jl if len(WORD.findall(re.sub(r"\[[^\]]*\]", " ", t))) < 12)
    return {
        "file": os.path.basename(path),
        "lines": len(lines),
        "max_run": max_run,
        "stacks3": stacks,
        "full": nf,
        "contr": nc,
        "contr_pct": round(100 * nc / max(1, nf + nc), 1),
        "j_lines": len(jl),
        "j_short": jshort,
        "j_short_pct": round(100 * jshort / max(1, len(jl)), 1),
    }


def main(paths):
    if not paths:
        paths = sorted(
            p
            for p in glob.glob(os.path.join(ROOT, "E0*.md"))
            if not p.endswith("show-notes.md")
        )
    rows = [metrics(p) for p in paths]
    print(
        f"{'file':48} maxrun stacks3 contr% jshort%"
    )
    worst_run = 0
    tot_j = tot_js = tot_f = tot_c = 0
    bad = 0
    for r in rows:
        flag = ""
        if r["max_run"] >= 3 or r["contr_pct"] < 80:
            flag = "  **"
            bad += 1
        print(
            f"{r['file']:48} {r['max_run']:6} {r['stacks3']:7} "
            f"{r['contr_pct']:6.1f} {r['j_short_pct']:7.1f}{flag}"
        )
        worst_run = max(worst_run, r["max_run"])
        tot_j += r["j_lines"]
        tot_js += r["j_short"]
        tot_f += r["full"]
        tot_c += r["contr"]
    print(
        f"\n{len(rows)} scripts. max consecutive={worst_run}. "
        f"contr {100*tot_c/max(1,tot_c+tot_f):.1f}%. "
        f"J short {100*tot_js/max(1,tot_j):.1f}%. "
        f"{bad} still over maxrun≥3 or contr<80%."
    )


if __name__ == "__main__":
    main(sys.argv[1:])
