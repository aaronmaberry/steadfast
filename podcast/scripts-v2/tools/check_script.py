#!/usr/bin/env python3
"""Check a Walk Steadfast v2 script (and its show notes) against STYLE-GUIDE.md.

Usage:
  python3 podcast/scripts-v2/tools/check_script.py podcast/scripts-v2/E007-waiting-is-not-peace.md
  python3 podcast/scripts-v2/tools/check_script.py --all          # every script, plus a summary table
  python3 podcast/scripts-v2/tools/check_script.py FILE --quiet   # only FAIL/WARN lines

The show notes are found automatically (E0XX-show-notes.md in the same folder).
Exit code is 1 if any check FAILs. WARN lines are judgment calls for the writer.
Scripture quotes are checked against tools/niv-cache/ (fill it with niv.py).
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "niv-cache")
sys.path.insert(0, HERE)
from niv import slug  # noqa: E402

WPM = 150
WORDS_MIN, WORDS_MAX = 2800, 3200
J_SHARE_MIN, J_SHARE_MAX = 35.0, 50.0
SHORT = 12
SHORT_MAX_PCT = 20.0
HOOK_MAX = 75
BOARDS_MIN, BOARDS_MAX = 3, 5
CTA_SITE, CTA_HANDLE = "walksteadfast.com", "@steadfastwalk"
NIV_NOTICE = "Scripture quotations taken from The Holy Bible, New International Version"

BOOKS = (r"(?:[1-3] )?(?:Song of Songs|[A-Z][a-z]+)")
REF_RE = re.compile(BOOKS + r" \d+:\d+(?:[-–]\d+)?")

BANNED_ALL = [
    (r"\bAI\b", "mentions AI"), (r"\bA\.I\.", "mentions AI"), (r"artificial intelligence", "mentions AI"),
    (r"chat ?gpt", "mentions AI"), (r"chatbot", "mentions AI"), (r"language model", "mentions AI"),
]
BANNED_SPOKEN = [
    (r"off[- ]air", "off-air reference"), (r"\boff[- ]mic\b", "production talk"), (r"\bon[- ]mic\b", "production talk"),
    (r"\bmics?\b", "production talk"), (r"before we (started|recorded|went on|hit record|got going)", "off-air reference"),
    (r"after we (stopped|recorded|wrapped)", "off-air reference"), (r"\bwardrobe\b", "production talk"),
    (r"\bcameras?\b", "production talk"), (r"\bproducers?\b", "production talk"), (r"\bstudio\b", "production talk"),
    (r"\bshow bible\b", "production talk"), (r"\bcanon\b", "production talk"),
    (r"\bepisode (one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)\b", "episode-number callback"),
    (r"\b(last|previous|other|earlier) episode\b", "episode callback"), (r"\bback in episode\b", "episode callback"),
    (r"you know the story", "inside baseball"), (r"\bas you know\b", "inside baseball"),
    (r"fifty times", "inside baseball"), (r"\blike we (said|talked about)\b", "inside baseball"),
    (r"\blast week we\b", "inside baseball"), (r"\byou'?ve heard me (say|tell)\b", "inside baseball"),
]
BANNED_JONATHON = [
    (r"\by'?all\b", "country phrasing for Jonathon"), (r"\breckon", "country phrasing for Jonathon"),
    (r"\bfixin'?\b", "country phrasing for Jonathon"), (r"\byonder\b", "country phrasing for Jonathon"),
    (r"\bfeed store\b", "country phrasing for Jonathon"), (r"lord willin", "country phrasing for Jonathon"),
    (r"\bain'?t\b", "country phrasing for Jonathon"),
]
WARN_SPOKEN = [
    (r"\beverybody out there\b|\ball of you out there\b|\byou all\b", "plural listener; keep it singular"),
    (r"\bsegment\b", "production word spoken on air"),
]
TIME_CHECK = re.compile(r"\b(minutes? (left|to go)|got (about|a little under|a little over|maybe|around) \w+ minutes|halfway|half way|"
                        r"little under \w+ minutes|we've got \w+ minutes|about \w+ minutes|last few minutes|next few minutes|"
                        r"few minutes left|before we're done|before we go)\b", re.I)


def norm_tokens(s):
    s = s.lower().replace("’", "'").replace("‘", "'").replace("—", " ").replace("–", " ")
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", s)


def words(s):
    s = re.sub(r"\[[^\]]*\]", " ", s)
    return re.findall(r"[A-Za-z0-9@][A-Za-z0-9'’\.\-@]*", s)


def mmss(n_words):
    sec = int(round(n_words * 60 / WPM))
    return f"{sec // 60:02d}:{sec % 60:02d}"


def load_cache():
    out = {}
    for p in glob.glob(os.path.join(CACHE, "*.json")):
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        out[os.path.basename(p)[:-5]] = d
    return out


def contiguous(q, p):
    n = len(q)
    if n == 0 or n > len(p):
        return False
    first = q[0]
    for i in range(len(p) - n + 1):
        if p[i] == first and p[i:i + n] == q:
            return True
    return False


def grams(t, n=3):
    return set(tuple(t[i:i + n]) for i in range(len(t) - n + 1))


def verify_quote(qtext, cache, min_tokens=4):
    """Return (status, ref). status: 'exact', 'misquote', or None (not scripture-like)."""
    q = norm_tokens(qtext)
    if len(q) < min_tokens:
        return None, None
    qg = grams(q) or {tuple(q)}
    best, best_ref, best_hits = 0.0, None, 0
    for key, d in cache.items():
        p = norm_tokens(d["text"])
        if contiguous(q, p):
            return "exact", d["ref"]
        pg = grams(p)
        hits = len(qg & pg)
        score = hits / len(qg)
        if score > best:
            best, best_ref, best_hits = score, d["ref"], hits
    if best >= 0.5 or (best >= 0.3 and best_hits >= 3):
        return "misquote", best_ref
    return None, None


QUOTE_RE = re.compile(r"“([^”]+)”|\"([^\"]+)\"")


class Report:
    def __init__(self, name, quiet=False):
        self.name, self.quiet = name, quiet
        self.fails, self.warns = [], []

    def info(self, msg):
        if not self.quiet:
            print(msg)

    def fail(self, msg):
        self.fails.append(msg)
        print(f"FAIL  {msg}")

    def warn(self, msg):
        self.warns.append(msg)
        print(f"WARN  {msg}")


def header_row(header, label):
    for line in header.splitlines():
        m = re.match(r"^\|\s*" + re.escape(label) + r"[^|]*\|\s*(.*?)\s*\|\s*$", line)
        if m:
            return line, m.group(1)
    return None, None


def check_script(path, quiet=False):
    rep = Report(os.path.basename(path), quiet)
    text = open(path, encoding="utf-8").read()
    cache = load_cache()
    stats = {"file": os.path.basename(path)}
    if "## OPEN (word for word)" not in text:
        rep.fail("missing '## OPEN (word for word)' header")
    if "## CLOSE (word for word)" not in text:
        rep.fail("missing '## CLOSE (word for word)' header")
    if "## OPEN" not in text:
        return rep, stats
    header, body = text.split("## OPEN", 1)
    body = "## OPEN" + body

    for pat, why in BANNED_ALL:
        for m in re.finditer(pat, text, re.I if pat != r"\bAI\b" else 0):
            rep.fail(f"line {text[:m.start()].count(chr(10)) + 1}: {why} ({m.group(0)!r})")

    segments, lines, boards = [], [], []
    cur = None
    first_content = None
    sting_seen_at = None
    for i, raw in enumerate(body.splitlines()):
        if raw.startswith("## "):
            cur = raw[3:].strip()
            segments.append([cur, 0])
            continue
        if raw.strip() and raw.strip() != "---" and first_content is None:
            first_content = raw
        if "[STING" in raw and sting_seen_at is None:
            sting_seen_at = (len(lines), cur)
        m = re.match(r"^([A-Z][A-Z .'\-]*[A-Z]):\s*(.*)$", raw)
        if m:
            spk = m.group(1)
            if spk not in ("WES", "JONATHON"):
                rep.fail(f"speaker label {spk!r} (only WES: and JONATHON: may speak)")
            n = len(words(m.group(2)))
            lines.append((spk, n, m.group(2), cur))
            if segments:
                segments[-1][1] += n
        for b in re.findall(r"\[BOARD:([^\]]*)\]", raw):
            boards.append(b.strip())

    if not lines:
        rep.fail("no spoken lines found")
        return rep, stats
    total = sum(l[1] for l in lines)
    wes = [l for l in lines if l[0] == "WES"]
    jon = [l for l in lines if l[0] == "JONATHON"]
    jw = sum(l[1] for l in jon)
    ww = sum(l[1] for l in wes)
    jshort = [l for l in jon if l[1] < SHORT]
    jshare = 100 * jw / total
    jpct = 100 * len(jshort) / max(1, len(jon))
    stats.update(words=total, wes_lines=len(wes), jon_lines=len(jon), jon_short=len(jshort),
                 jon_short_pct=jpct, jon_share=jshare, boards=len(boards), minutes=total / WPM)

    rep.info(f"== {rep.name}")
    rep.info(f"Spoken words: {total} (about {mmss(total)} at {WPM} wpm)")
    rep.info(f"WES: {len(wes)} lines, {ww} words ({100 * ww / total:.0f}%)")
    rep.info(f"JONATHON: {len(jon)} lines, {jw} words ({jshare:.0f}%), {len(jshort)} under {SHORT} words ({jpct:.1f}%)")

    if not WORDS_MIN <= total <= WORDS_MAX:
        rep.fail(f"spoken words {total} outside {WORDS_MIN}-{WORDS_MAX}")
    if not J_SHARE_MIN <= jshare <= J_SHARE_MAX:
        rep.fail(f"Jonathon's share {jshare:.1f}% outside {J_SHARE_MIN:.0f}-{J_SHARE_MAX:.0f}%")
    if jpct >= SHORT_MAX_PCT:
        rep.fail(f"Jonathon short lines {jpct:.1f}% (must be under {SHORT_MAX_PCT:.0f}%)")
    if jshort and not quiet:
        rep.info("  Jonathon short lines:")
        for l in jshort:
            rep.info(f"    [{l[1]}] {l[2]}")

    if first_content is None or not re.match(r"^(WES|JONATHON):", first_content):
        rep.fail("the first thing in the OPEN must be a spoken line (no music or cue first)")
    if sting_seen_at is None:
        rep.fail("no [STING] found after the hook")
    else:
        hook_words = sum(l[1] for l in lines[:sting_seen_at[0]])
        stats["hook_words"] = hook_words
        rep.info(f"Hook before first sting: {hook_words} words (about {hook_words * 60 / WPM:.0f} s)")
        if hook_words > HOOK_MAX:
            rep.fail(f"hook is {hook_words} words before the first sting (max {HOOK_MAX}, about 30 s)")
        if not (sting_seen_at[1] or "").startswith("OPEN"):
            rep.fail("first [STING] is not inside the OPEN")

    last = lines[-1]
    if CTA_SITE not in last[2] or CTA_HANDLE not in last[2]:
        rep.fail(f"last spoken line must carry both {CTA_SITE} and {CTA_HANDLE}: {last[2][:80]!r}")
    if not (last[3] or "").startswith("CLOSE"):
        rep.fail("last spoken line is not in the CLOSE section")
    tail = [l.strip() for l in body.splitlines() if l.strip()]
    if not tail or not tail[-1].startswith("[STING"):
        rep.fail("the script must end with [STING 2s] after the CTA")

    close_words = sum(n for name, n in segments if name.startswith("CLOSE"))
    stats["close_words"] = close_words
    if close_words > 130:
        rep.warn(f"CLOSE runs {close_words} words (aim for about 50-110, 20-40 s)")

    rep.info("Segments (start times at 150 wpm):")
    t = 0
    seg_times = []
    for name, n in segments:
        seg_times.append((mmss(t), name, n))
        rep.info(f"  {mmss(t)}  {name}  ({n} words)")
        if not name.startswith(("OPEN", "CLOSE")) and n > 900:
            rep.warn(f"segment '{name}' runs {n} words (about {n / WPM:.1f} min); guide says 2-4 min")
        t += n
    rep.info(f"  {mmss(t)}  END")
    stats["seg_times"] = seg_times

    longest = max((l for l in wes), key=lambda l: l[1], default=None)
    if longest and longest[1] > 170:
        rep.warn(f"longest Wes turn is {longest[1]} words (guide: about 120, then a handoff)")
    longest_j = max((l for l in jon), key=lambda l: l[1], default=None)
    if longest_j and longest_j[1] > 170:
        rep.warn(f"longest Jonathon turn is {longest_j[1]} words (break it with a reaction)")
    tc = sum(1 for l in wes if TIME_CHECK.search(l[2]))
    if tc < 2:
        rep.warn(f"found {tc} Wes time checks (guide: two or three)")

    spoken_text = " ".join(re.sub(r"\[[^\]]*\]", " ", l[2]) for l in lines)
    spoken_tokens = norm_tokens(spoken_text)
    spoken_grams = grams(spoken_tokens, 4)
    rep.info(f"Board cues: {len(boards)}")
    if not BOARDS_MIN <= len(boards) <= BOARDS_MAX:
        rep.fail(f"{len(boards)} board cues (need {BOARDS_MIN}-{BOARDS_MAX})")
    for b in boards:
        bt = norm_tokens(b)
        hits = sorted({" ".join(bt[i:i + 4]) for i in range(len(bt) - 3) if tuple(bt[i:i + 4]) in spoken_grams})
        if hits:
            rep.fail(f"board repeats spoken words {hits}: {b[:70]!r}")
        mref = re.match(r"^\s*(" + REF_RE.pattern + r")", b)
        if mref:
            ref = mref.group(1).replace("–", "-")
            mq = re.match(r"^\s*" + re.escape(mref.group(1)) + r"\s*\(NIV\)\s*·\s*[\"“](.+)[\"”]\s*$", b)
            if not mq:
                rep.fail(f"scripture board must read 'Ref (NIV) · \"exact text\"': {b[:70]!r}")
                continue
            d = cache.get(slug(ref))
            if not d:
                rep.fail(f"board verse {ref} not in niv-cache (run niv.py \"{ref}\")")
            elif not contiguous(norm_tokens(mq.group(1)), norm_tokens(d["text"])):
                rep.fail(f"board text is not exact NIV for {ref}: {mq.group(1)[:60]!r}")
            else:
                rep.info(f"  ok (NIV exact) {ref}")
        else:
            rep.info(f"  ok (idea) {b[:60]}")

    _, srow = header_row(header, "Scripture")
    if srow is None:
        rep.fail("header has no Scripture row")
        refs = []
    else:
        if not re.search(r"verified \d{4}-\d{2}-\d{2}", header):
            rep.fail("Scripture header must log 'verified YYYY-MM-DD'")
        refs = [r.replace("–", "-") for r in REF_RE.findall(srow)]
        missing = [r for r in refs if slug(r) not in cache]
        for r in missing:
            rep.fail(f"header verse {r} not in niv-cache (run niv.py \"{r}\")")
        if not refs:
            rep.fail("Scripture header lists no references")
        nverses = 0
        for r in refs:
            d = cache.get(slug(r))
            if d:
                nverses += len(d["verses"])
        stats["verses"] = nverses
        if nverses > 14:
            rep.warn(f"{nverses} verses listed; keep per-episode NIV use modest")
    stats["refs"] = refs

    quotes = 0
    for spk, n, s, seg in lines:
        for m in QUOTE_RE.finditer(s):
            q = m.group(1) or m.group(2)
            st, ref = verify_quote(q, cache)
            if st == "exact":
                quotes += 1
                rep.info(f"  scripture quote ok ({ref}): {q[:60]!r}")
            elif st == "misquote":
                rep.fail(f"{spk} quote looks like {ref} but is not exact NIV: {q[:80]!r}")
    stats["quotes"] = quotes
    if quotes == 0:
        rep.warn("no spoken quotation matched a cached NIV verse; every episode should read at least one verse")

    for spk, n, s, seg in lines:
        clean = re.sub(r"\[[^\]]*\]", " ", s)
        for pat, why in BANNED_SPOKEN:
            for m in re.finditer(pat, clean, re.I):
                rep.fail(f"{spk} ({seg}): {why}: {m.group(0)!r}")
        for pat, why in WARN_SPOKEN:
            for m in re.finditer(pat, clean, re.I):
                rep.warn(f"{spk} ({seg}): {why}: {m.group(0)!r}")
        if spk == "JONATHON":
            for pat, why in BANNED_JONATHON:
                for m in re.finditer(pat, clean, re.I):
                    rep.fail(f"JONATHON ({seg}): {why}: {m.group(0)!r}")

    line, val = header_row(header, "Spoken words")
    if val is None:
        rep.fail("header has no 'Spoken words' row")
    else:
        mnum = re.match(r"([\d,]+)", val)
        if not mnum or int(mnum.group(1).replace(",", "")) != total:
            rep.fail(f"header says spoken words {val[:20]!r}; actual {total:,}")
    line, val = header_row(header, "Line balance")
    if val is None:
        rep.fail("header has no 'Line balance' row")
    else:
        mw = re.search(r"WES (\d+) lines", val)
        mj = re.search(r"JONATHON (\d+) lines", val)
        ms = re.search(r"(\d+) under 12 words", val)
        if not (mw and int(mw.group(1)) == len(wes)):
            rep.fail(f"header WES line count wrong (actual {len(wes)})")
        if not (mj and int(mj.group(1)) == len(jon)):
            rep.fail(f"header JONATHON line count wrong (actual {len(jon)})")
        if not (ms and int(ms.group(1)) == len(jshort)):
            rep.fail(f"header short-line count wrong (actual {len(jshort)})")
    line, val = header_row(header, "Board cues")
    if val is None or not re.match(r"\s*(\d+)", val) or int(re.match(r"\s*(\d+)", val).group(1)) != len(boards):
        rep.fail(f"header 'Board cues' row missing or wrong (actual {len(boards)})")

    notes = re.sub(r"-[^/]*\.md$", "-show-notes.md", path)
    m = re.match(r"^(.*/)?(E\d{3})-", path)
    if m:
        notes = os.path.join(os.path.dirname(path), f"{m.group(2)}-show-notes.md")
    check_notes(notes, rep, total, seg_times, cache)
    return rep, stats


def check_notes(path, rep, total, seg_times, cache):
    name = os.path.basename(path)
    if not os.path.exists(path):
        rep.fail(f"show notes missing: {name}")
        return
    text = open(path, encoding="utf-8").read()
    rep.info(f"Show notes: {name}")
    for pat, why in BANNED_ALL:
        for m in re.finditer(pat, text, re.I if pat != r"\bAI\b" else 0):
            rep.fail(f"{name} line {text[:m.start()].count(chr(10)) + 1}: {why}")
    for label, limit in (("Title", 60), ("Meta description", 160)):
        m = re.search(r"\*\*" + label + r" \((\d+) characters\)\*\*\s*\n(.+)", text)
        if not m:
            rep.fail(f"{name}: missing '**{label} (N characters)**' block")
            continue
        actual = len(m.group(2).strip())
        if actual > limit:
            rep.fail(f"{name}: {label.lower()} is {actual} characters (max {limit})")
        if int(m.group(1)) != actual:
            rep.fail(f"{name}: {label.lower()} says {m.group(1)} characters, actual {actual}")
    for need in ("https://www.walksteadfast.com", "@steadfastwalk", "#WalkSteadfast", "**Keywords**", NIV_NOTICE):
        if need not in text:
            rep.fail(f"{name}: missing {need[:40]!r}")
    m = re.search(r"\(([\d,]+) spoken words", text)
    if not m or int(m.group(1).replace(",", "")) != total:
        rep.fail(f"{name}: timestamp note must say '({total:,} spoken words, about {mmss(total)})'")
    times = re.findall(r"^\|\s*(\d\d:\d\d)\s*\|", text, re.M)
    want = [t for t, _, _ in seg_times]
    if times != want:
        rep.fail(f"{name}: chapter times {times} do not match script {want}")
    verified = 0
    for m in QUOTE_RE.finditer(text):
        q = m.group(1) or m.group(2)
        st, ref = verify_quote(q, cache, min_tokens=5)
        if st == "exact":
            verified += 1
        elif st == "misquote":
            rep.fail(f"{name}: quote looks like {ref} but is not exact NIV: {q[:70]!r}")
    rep.info(f"  show notes ok checks done; {verified} NIV quotes verified")


def main(argv):
    quiet = "--quiet" in argv
    args = [a for a in argv if not a.startswith("--")]
    if "--all" in argv:
        args = sorted(p for p in glob.glob(os.path.join(ROOT, "E[0-9][0-9][0-9]-*.md")) if not p.endswith("-show-notes.md"))
    if not args:
        print(__doc__)
        return 2
    results = []
    for p in args:
        rep, stats = check_script(p, quiet)
        results.append((rep, stats))
        if not quiet:
            print()
    bad = [r for r, _ in results if r.fails]
    if len(results) > 1:
        print(f"{'file':52} {'words':>5} {'min':>5} {'J lines':>7} {'J short%':>8} {'J share':>7} {'boards':>6}  status")
        for rep, s in results:
            if "words" not in s:
                print(f"{s['file']:52} {'-':>5}  FAIL")
                continue
            print(f"{s['file']:52} {s['words']:5d} {s['minutes']:5.1f} {s['jon_lines']:7d} {s['jon_short_pct']:7.1f}% "
                  f"{s['jon_share']:6.1f}% {s['boards']:6d}  {'FAIL' if rep.fails else 'ok'}{' (warn)' if rep.warns else ''}")
        ws = sorted(s["words"] for _, s in results if "words" in s)
        if ws:
            med = ws[len(ws) // 2] if len(ws) % 2 else (ws[len(ws) // 2 - 1] + ws[len(ws) // 2]) / 2
            worst = max(results, key=lambda r: r[1].get("jon_short_pct", 0))
            print(f"\n{len(results)} scripts. Words min {ws[0]}, median {med:g}, max {ws[-1]}. "
                  f"Worst Jonathon short-line rate {worst[1].get('jon_short_pct', 0):.1f}% ({worst[1]['file']}). "
                  f"{len(bad)} failing.")
    else:
        rep = results[0][0]
        print(f"RESULT {rep.name}: {'FAIL' if rep.fails else 'PASS'} ({len(rep.fails)} fail, {len(rep.warns)} warn)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
