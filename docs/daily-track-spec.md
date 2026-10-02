# Daily track spec

The daily walk is the JSON feed at `app/daily.json`. This repository does not contain the generator. There is no script, prompt, template, or GitHub Action here that writes that file. Whatever automation produces the next dates lives outside this repo. It should follow this spec.

The site reads `feed.items` from `site.js`. `carryBody` and `body` are the same text. The reader, the home tiles, and `/daily` all use this feed.

## Length

Word counts were measured on the 49 items in the feed before the October 2 to 6 rewrite. A word is a whitespace-separated token.

| Section | Field | Average words | New items |
| --- | --- | --- | --- |
| Silent Touch | `silentBody` | 202 | 404 to 606 words (2 to 3 times that average) |
| Daily challenge | `carryBody` (mirrored in `body`) | 105 | 210 to 315 words |
| Guided prayer | `prayer` | 44 | 88 to 132 words |

The challenge and the prayer together averaged 149 words. Hitting the two ranges above also lands the combined Challenge/Prayer section between 298 and 447 words.

Count only that field. Do not pad `reflection` or `silentLine` to make the total look longer. `reflection` stays one or two sentences. `silentLine` stays one sentence.

## Fields to keep stable

Keep the day's topic, `verse`, and `verseRef`. `verse` is NIV wording only. `verseRef` is book chapter:verse, or a verse range such as `Hebrews 10:24-25`, with no translation name appended. A range hyphen inside a reference is the existing citation form. Do not put an em dash, an en dash, or a spaced hyphen in the prose.

`body` must equal `carryBody` exactly, including paragraph breaks.

Paragraphs are separated by a blank line (`\n\n`).

## Voice

Plain, warm, direct speech. Longer natural sentences. Address the reader as you.

Do not use:

- Dashes as punctuation in prose (em dash, en dash, or spaced hyphen).
- The phrase "real man".
- The names Robert Lewis, Men's Fraternity, Authentic Manhood, or 33 The Series.
- The names Wes or Jonathan.
- AI vocabulary and chatbot phrasing, including delve, journey, tapestry, unlock, empower, transformative, navigate, embrace, foster, elevate, profound, and testament.
- "Not just X but Y" constructions.
- Rule-of-three filler.
- Stacked "the man who / the man who".

## Four marks

The marks are locked. Use these names and do not invent another:

- Stop Waiting
- Pick Up the Weight
- Go First
- Work for God’s Pay

The creed, when quoted, is copied exactly from the site:

A steadfast man stops waiting, picks up the weight, goes first, and works for God’s pay, not the room’s.

The apostrophe in God’s and room’s is the typographic apostrophe already used on the site.

## Reader behavior (site)

Opening a track opens a full-screen reading view. A share link is `https://www.walksteadfast.com/daily?day=YYYY-MM-DD`. A hash of `#day=YYYY-MM-DD` also opens that day. Like and comments go through the adapter in `daily-engage.js`. This preview stores both on the device. The comment sheet is the public shape: a list with name, relative time, and text, an empty state, a name field and a text field, and a Report control on each comment. The copy says public comments are coming soon. No backend is attached.
