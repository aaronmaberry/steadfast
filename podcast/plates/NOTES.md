# Steadfast Men podcast — plate lock options (v1)

Masters: `optN-{idle,split,full}.jpg` = 1920x1080; `4k/optN-*-3840.jpg` = 3840x2160 (rendered natively at 4K, 1080 is a downscale). Generator: `comp.py`, upscaler: `esr.py`.

## Options
1. **Glass Bubbles** — two floating rounded 4:5 cams with periwinkle glow borders, frosted center card. Borrows: Aaron's bubble refs; Chris Williamson (Modern Wisdom) clean dark minimalism; DOAC color discipline. Full board keeps tiny cam pips top-right.
2. **Edge Split + Center Rail** — cams edge-to-edge, glowing periwinkle seams, branded rail; rail widens for board. Borrows: Flagrant / Rogan-clip two-up crops, PBD Podcast bold split.
3. **Barstool 3-Up** — three equal panels, center = plate/board, top header (EP, logo, URL). Borrows: Barstool/Pardon My Take 3-panel, The Pivot remote 3-ups.
4. **Lower-Third Bar** — big two-up cams + persistent branded lower-third (logo, quote, socials, subscribe). Borrows: Huberman / news-style persistent lower third, DOAC caption bar.
5. **Cinematic Letterbox** — 2.39 bars carrying all branding; center shows episode number. Borrows: DOAC/Huberman cinematic grade + film framing.
6. **Studio Desk** — blurred real studio wide as backdrop, circular cams, glass desk plate bottom-center. Borrows: PBD/Valuetainment desk graphics, Rogan studio feel.
(Layout notes from general knowledge of these shows' YouTube formats; no fresh web research pass was done.)

## Sources
- People/studio: `img/LOCKED-podcast-table.jpg` (site podcast image: Wes in charcoal henley + curly-haired co-host, acoustic foam, boom mics). Crops Real-ESRGAN x4plus (70/30 blend with Lanczos to avoid plastic skin). No AI generation used.
- Logo: `img/logo-lockup.jpg` (live site lockup, lighten-blended, not redrawn).
- Colors/font: `styles.css` --bg #07070a, --accent #8b9cff, --accent-2 #5b6ef5, Geist.
- Quote: index.html h2 "A son should be able to copy your walk."
- Verse: Luke 16:10 NIV text as used in tools/s01v4_build.py (first clause).
- Socials (index.html footer): x.com, tiktok.com/@, youtube.com/@, instagram.com, facebook.com — all /steadfastwalk. No Reddit or LinkedIn found in repo.
- Hashtag: **none found in repo — `#WalkSteadfast` is PROPOSED.**
- Spend: $0 (all local).
