#!/usr/bin/env python3
"""Fetch and cache NIV passages from Bible Gateway for script verification.

Usage:
  python3 podcast/scripts-v2/tools/niv.py "James 4:17" "Matthew 5:23-24"
  python3 podcast/scripts-v2/tools/niv.py --refresh "Psalm 27:14"

Each passage is cached as JSON in tools/niv-cache/. check_script.py reads the
cache to confirm that every quoted verse in a script, board cue or show-notes
file is exact NIV text. Keep requests to single verses or short ranges.
"""
import datetime
import html
import json
import os
import re
import subprocess
import sys
import urllib.parse
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "niv-cache")
URL = "https://www.biblegateway.com/passage/?search={q}&version=NIV&interface=print"

SKIP_CLASSES = {"versenum", "chapternum", "crossreference", "footnote", "footnotes", "crossrefs"}


def slug(ref):
    s = ref.strip().lower().replace("–", "-").replace("—", "-")
    s = re.sub(r"\s+", "-", s)
    s = s.replace(":", "_")
    return re.sub(r"[^a-z0-9_\-]", "", s)


class Passage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_passage = 0
        self.depth = 0
        self.skip_depth = None
        self.verse_stack = []
        self.verses = {}
        self.order = []
        self.heading = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = set((a.get("class") or "").split())
        if not self.in_passage:
            if tag == "div" and "passage-text" in cls:
                self.in_passage = 1
                self.depth = 0
            return
        if tag in ("br", "img", "hr", "input", "meta", "link"):
            cur = next((k for k in reversed(self.verse_stack) if k), None) or (self.order[-1] if self.order else None)
            if tag == "br" and cur:
                self.verses[cur] += " "
            return
        self.depth += 1
        if self.skip_depth is None and (cls & SKIP_CLASSES or tag in ("h1", "h2", "h3", "h4")):
            self.skip_depth = self.depth
        key = None
        if tag == "span" and "text" in cls:
            for c in cls:
                if re.match(r"^[0-9A-Za-z]+-\d+-\d+$", c):
                    key = c
        self.verse_stack.append(key)
        if key and key not in self.verses:
            self.verses[key] = ""
            self.order.append(key)
        elif key:
            self.verses[key] += " "

    def handle_endtag(self, tag):
        if not self.in_passage or tag in ("br", "img", "hr", "input", "meta", "link"):
            return
        if self.skip_depth is not None and self.depth == self.skip_depth:
            self.skip_depth = None
        self.depth -= 1
        if self.verse_stack:
            self.verse_stack.pop()
        if self.depth < 0:
            self.in_passage = 0

    def handle_data(self, data):
        if not self.in_passage or self.skip_depth is not None:
            return
        key = next((k for k in reversed(self.verse_stack) if k), None)
        if key:
            self.verses[key] += data


def fetch(ref):
    q = urllib.parse.quote_plus(ref)
    out = subprocess.run(
        ["curl", "-s", "-m", "30", "-A", "Mozilla/5.0", URL.format(q=q)],
        capture_output=True, text=True, check=False,
    ).stdout
    if "passage-text" not in out:
        raise SystemExit(f"niv.py: no passage returned for {ref!r}")
    p = Passage()
    p.feed(out)
    verses = []
    for k in p.order:
        t = html.unescape(p.verses[k])
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            verses.append({"id": k, "text": t})
    if not verses:
        raise SystemExit(f"niv.py: could not parse verses for {ref!r}")
    return verses


def load_cache():
    data = {}
    if not os.path.isdir(CACHE):
        return data
    for name in sorted(os.listdir(CACHE)):
        if name.endswith(".json"):
            with open(os.path.join(CACHE, name), encoding="utf-8") as f:
                d = json.load(f)
            data[d["ref"]] = d
    return data


def get(ref, refresh=False):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, slug(ref) + ".json")
    if os.path.exists(path) and not refresh:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    verses = fetch(ref)
    d = {
        "ref": ref.strip(),
        "version": "NIV",
        "source": URL.format(q=urllib.parse.quote_plus(ref)),
        "fetched": datetime.date.today().isoformat(),
        "verses": verses,
        "text": " ".join(v["text"] for v in verses),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    return d


def main(argv):
    refresh = "--refresh" in argv
    refs = [a for a in argv if not a.startswith("--")]
    if not refs:
        print(__doc__)
        return 1
    for ref in refs:
        d = get(ref, refresh)
        print(f"{d['ref']} (NIV, fetched {d['fetched']})")
        for v in d["verses"]:
            print(f"  [{v['id']}] {v['text']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
