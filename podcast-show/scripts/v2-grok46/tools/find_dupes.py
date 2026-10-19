#!/usr/bin/env python3
"""Find spoken sentences of 6+ words that appear in 2+ episodes.

Excludes:
  - scripture quotes (straight or curly)
  - walksteadfast.com / @steadfastwalk CTA
  - fixed host ID ("This is Walk Steadfast. I'm Wes Hart.")

Also reports near-duplicates with SequenceMatcher ratio > 0.85.

Usage:
  python3 tools/find_dupes.py
  python3 tools/find_dupes.py --json /tmp/dupes.json
  python3 tools/find_dupes.py --quiet   # counts only
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from itertools import combinations

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINE = re.compile(r"^(WES|JONATHON):\s*(.*)$")
MIN_WORDS = 6
NEAR = 0.85

# Allowed exact repeats (show identity + CTA).
ALLOW_EXACT = {
    "this is walk steadfast i'm wes hart",
    "and i'm jonathon",
}
CTA_RE = re.compile(r"walksteadfast\.com|@steadfastwalk", re.I)

APOS = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"'})


def scripts():
    return sorted(
        p
        for p in glob.glob(os.path.join(ROOT, "E0*.md"))
        if not p.endswith("show-notes.md")
    )


def ep_id(path):
    return os.path.basename(path)[:4]


def strip_stage_and_quotes(text):
    text = re.sub(r"\[[^\]]*\]", " ", text)
    text = re.sub(r"“[^”]*”", " ", text)
    text = re.sub(r'"[^"]*"', " ", text)
    return re.sub(r"\s+", " ", text).strip()


def sentences(text):
    """Split a spoken line into sentences. Keep 6+ word ones."""
    if not text:
        return []
    # Treat em-dash cuts as sentence ends only when they close a clause.
    chunks = re.split(r"(?<=[.!?])\s+|(?<=—)\s+", text)
    out = []
    for chunk in chunks:
        s = chunk.strip(" \t-—")
        if not s:
            continue
        if CTA_RE.search(s):
            continue
        words = re.findall(r"[A-Za-z0-9']+", s.translate(APOS))
        if len(words) < MIN_WORDS:
            continue
        out.append(s)
    return out


def norm(s):
    s = s.translate(APOS).lower()
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    return re.findall(r"[a-z0-9']+", s)


def norm_key(s):
    return " ".join(norm(s))


def collect():
    """Return list of {ep, path, lineno, speaker, sentence, key}."""
    rows = []
    for path in scripts():
        text = open(path, encoding="utf-8").read()
        if "## OPEN" not in text:
            continue
        body = "## OPEN" + text.split("## OPEN", 1)[1]
        for i, raw in enumerate(body.splitlines(), start=text.split("## OPEN", 1)[0].count("\n") + 2):
            m = LINE.match(raw)
            if not m:
                continue
            spoken = strip_stage_and_quotes(m.group(2))
            for sent in sentences(spoken):
                key = norm_key(sent)
                if not key or key in ALLOW_EXACT:
                    continue
                rows.append(
                    {
                        "ep": ep_id(path),
                        "path": path,
                        "lineno": i,
                        "speaker": m.group(1),
                        "sentence": sent,
                        "key": key,
                    }
                )
    return rows


def exact_clusters(rows):
    by = defaultdict(list)
    for r in rows:
        by[r["key"]].append(r)
    clusters = []
    for key, hits in by.items():
        eps = sorted({h["ep"] for h in hits})
        if len(eps) < 2:
            continue
        clusters.append(
            {
                "kind": "exact",
                "key": key,
                "n_eps": len(eps),
                "eps": eps,
                "hits": hits,
            }
        )
    clusters.sort(key=lambda c: (-c["n_eps"], -len(c["key"])))
    return clusters


def token_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()


def near_clusters(exact, rows):
    """Near-dupes across episodes, skipping keys already in exact clusters."""
    exact_keys = {c["key"] for c in exact}
    # One representative per (ep, key)
    uniq = {}
    for r in rows:
        if r["key"] in exact_keys:
            continue
        uniq[(r["ep"], r["key"])] = r
    items = list(uniq.values())
    # Bucket by first 3 tokens to cut O(n^2)
    buckets = defaultdict(list)
    for r in items:
        toks = r["key"].split()
        buckets[" ".join(toks[:3])].append(r)
    seen_pairs = set()
    groups = defaultdict(set)  # key -> set of keys
    key_to_rows = defaultdict(list)
    for r in items:
        key_to_rows[r["key"]].append(r)

    for bucket in buckets.values():
        if len(bucket) < 2:
            continue
        for x, y in combinations(bucket, 2):
            if x["ep"] == y["ep"]:
                continue
            if x["key"] == y["key"]:
                continue
            pair = tuple(sorted((x["key"], y["key"])))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            if token_ratio(x["key"], y["key"]) >= NEAR:
                groups[x["key"]].add(y["key"])
                groups[y["key"]].add(x["key"])

    # Connected components
    visited = set()
    near = []
    for start in groups:
        if start in visited:
            continue
        stack = [start]
        comp = set()
        while stack:
            k = stack.pop()
            if k in visited:
                continue
            visited.add(k)
            comp.add(k)
            stack.extend(groups[k] - visited)
        hits = []
        for k in comp:
            hits.extend(key_to_rows[k])
        eps = sorted({h["ep"] for h in hits})
        if len(eps) < 2:
            continue
        near.append(
            {
                "kind": "near",
                "key": min(comp, key=len),
                "keys": sorted(comp),
                "n_eps": len(eps),
                "eps": eps,
                "hits": hits,
            }
        )
    near.sort(key=lambda c: (-c["n_eps"], -len(c["keys"])))
    return near


def print_report(exact, near, quiet=False):
    n_exact_sents = len(exact)
    n_exact_occ = sum(len(c["hits"]) for c in exact)
    n_near = len(near)
    print(
        f"EXACT: {n_exact_sents} sentences of {MIN_WORDS}+ words in 2+ episodes "
        f"({n_exact_occ} occurrences). "
        f"NEAR (>{int(NEAR*100)}%): {n_near} clusters."
    )
    if quiet:
        return
    print("\n=== EXACT (most shared first) ===")
    for c in exact:
        print(f"\n[{c['n_eps']} eps] {c['hits'][0]['sentence']}")
        for h in c["hits"]:
            print(f"  {h['ep']} L{h['lineno']} {h['speaker']}: {h['sentence']}")
    if near:
        print("\n=== NEAR-DUPLICATES ===")
        for c in near:
            print(f"\n[{c['n_eps']} eps / {len(c['keys'])} wordings]")
            shown = set()
            for h in c["hits"]:
                if h["key"] in shown:
                    continue
                shown.add(h["key"])
                print(f"  {h['ep']} L{h['lineno']} {h['speaker']}: {h['sentence']}")


def main(argv):
    out_json = None
    quiet = False
    args = argv[:]
    if "--quiet" in args:
        quiet = True
        args.remove("--quiet")
    if "--json" in args:
        i = args.index("--json")
        out_json = args[i + 1]
        del args[i : i + 2]
    rows = collect()
    exact = exact_clusters(rows)
    near = near_clusters(exact, rows)
    print_report(exact, near, quiet=quiet)
    if out_json:
        dump = []
        for c in exact + near:
            dump.append(
                {
                    "kind": c["kind"],
                    "n_eps": c["n_eps"],
                    "eps": c["eps"],
                    "keys": c.get("keys", [c["key"]]),
                    "hits": [
                        {
                            "ep": h["ep"],
                            "lineno": h["lineno"],
                            "speaker": h["speaker"],
                            "sentence": h["sentence"],
                            "file": os.path.basename(h["path"]),
                        }
                        for h in c["hits"]
                    ],
                }
            )
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(dump, f, indent=2)
        print(f"\nwrote {out_json} ({len(dump)} clusters)")


if __name__ == "__main__":
    main(sys.argv[1:])
