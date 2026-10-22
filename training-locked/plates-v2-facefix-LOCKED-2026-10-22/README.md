# LOCKED: v2 plates, face fix (2026-10-22, revised: inswapper)

Locked 2026-10-22 by Aaron Maberry. **No changes without Aaron sign-off.**

**Revision 2 (2026-10-22, ~3:30 PM CT):** The earlier Grok image-edit head fixes were replaced. Aaron found they didn't match the master, and ArcFace scored them only 0.28–0.69 vs S3. Each face here is now a true face swap:
1. **inswapper_128** with the identity source **S3-medcloseup** from `training-locked/v9-face-master/`. S3 is canonical; plate 69 is not a face reference.
2. Lab color match to the plate's skin.
3. GFPGAN 1.4 restoration blended at 0.3.
4. A local mouth relaxation: the base plate's neutral mouth region is color-matched and feathered back in, at 0.85 (P04 at 0.6), so he reads as engaged and neutral or slightly warm rather than grinning.

Only the face region changes. A pixel diff confirms that nothing outside the face bounding box changed.

Identity = ArcFace (insightface buffalo_l) cosine vs S3. For reference, the S1–S7 masters score 0.878–0.907 vs S3; the bar is ≥ 0.85.

| Plate | File | Swap base | ArcFace vs S3 |
|---|---|---|---|
| P02 medium center | P02-med-center-FACEFIX-LOCKED.jpg | v2 original | 0.906 |
| P03 low stride right | P03-low-stride-right-FACEFIX-LOCKED.jpg | rev-1 facefix plate | 0.923 |
| P04 profile walk left | P04-profile-walk-left-FACEFIX-LOCKED.jpg | rev-1 facefix plate | 0.859 |
| P05 medium-wide right | P05-medwide-right-FACEFIX-LOCKED.jpg | rev-1 facefix plate | 0.918 |
| P07 high walk right | P07-high-walk-right-FACEFIX-LOCKED.jpg | v2 original | 0.874 |
| P08 MCU right | P08-mcu-right-FACEFIX-LOCKED.jpg | v2 original | 0.881 |

v2 originals: `training-locked/plates-v2-LOCKED-2026-10-22/`. Working files, scripts (`work/id/swap2.py`, `mouth.py`, `score.py`) and final-compare.jpg are in `artifacts/training/w01-poc/lesson01-v3/` (api-requests.md Round 11). Cost: $0 (all local).

**These supersede the v2 originals for all generation.**

- P01 (wide back view, no face visible): keep using the v2 original `plates-v2-LOCKED-2026-10-22/P01-wide-back-LOCKED.jpg`.
- P06 (over the audience seats): RETIRED. Audience seats are banned; do not use.
