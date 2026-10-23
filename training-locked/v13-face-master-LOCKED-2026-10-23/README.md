# v13 face master: LOCKED by Aaron (2026-10-23)

**Status:** LOCKED by Aaron 2026-10-23. v13 supersedes v10 as the canonical source for ALL new generations and face swaps.
- Identity checks: ArcFace cosine **≥0.85 against the v13 master** (`mean_arcface_embedding.npy` in this folder).
- **Never paint v13 texture onto video.** Use v13 as the source/reference image so texture is generated natively; video fixes stay teeth-only.
- v10 (`../v10-face-master-STUDIO-2026-10-22/`) is kept untouched as history; scripts can still use it via `--master v10`.

## History (candidate notes)
v13 face master: CANDIDATE (2026-10-23). NOT LOCKED. Pending Aaron's sign-off; v10 remains canonical. Supersedes v11/v12 candidates.
v10 M1-M8 + detail13.py (local, $0; crease 1.8, brow 1.4, tonal 1.3, spec 1.3): 3 strong horizontal forehead creases with shading (dark valley + lit shoulder) sized to read at full-frame 1280x720, brow-ridge definition, skin-tone variation, specular breakup of forehead shine, fine pores, plus real skin high-frequency transplanted from a CC BY-SA 2.0 reference forehead (REF-Ben_Affleck_by_Gage_Skidmore_3, Wikimedia Commons, Gage Skidmore). Delta is zero-mean over the forehead so tone matches v10 (measured forehead L 106.4->105.3, M1). Teeth at v12 level. Hair/beard/eyes/expression untouched.
ArcFace v13 frame vs its v10 frame: 0.964-0.986, mean-vs-mean 0.9828 (v13-scores.json; key names say v11, legacy).

## Use (added 2026-10-23 11:35 CDT)
v13 is a STILL-IMAGE candidate. It is meant to be the source/reference image for NEW generations so forehead texture is generated natively and moves with expression. Do NOT paint its texture onto video: the v13 clip overlay (T03 v13) failed independent video review (static smudges that don't deform, flicker, gray teeth). Video fixes stay teeth-only (see T03 v14).
