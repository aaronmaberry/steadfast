> **SUPERSEDED 2026-10-23:** v13 (`../v13-face-master-LOCKED-2026-10-23/`, LOCKED by Aaron) supersedes v10 for all new generations, face swaps, and identity checks (≥0.85 vs v13). v10 is kept as history.

# v10 face master: STUDIO (2026-10-22). PENDING Aaron's confirmation

Supersedes v9-face-master S1-S7 as the canonical Wes once Aaron confirms. v9 stays in place (not deleted) until then.

Source: the sharpest frames from the front studio takes that Aaron approved in testA-v2 (navy backdrop), raw i2v frames with no face swap.
- M1-M8: 8 frames, one per eighth of the 40 s front track, the sharpest (face Laplacian) in each window. Expressions vary (talking, mouth open/closed); yaw ranges from -7 to +1 degrees.
- mean_arcface_embedding.npy: the L2-normalised mean ArcFace (buffalo_l w600k_r50) embedding of M1-M8. All identity scores from now on are cosine against this vector.
- masters.json: per-frame source, sharpness, yaw and cosine to the mean (0.927-0.970).
- Face swaps to this master use inswapper_128 with this mean embedding as the source latent, then CodeFormer (w=0.8), a skin Lab colour match and grain matched to the body (studio-test/work/v2/hq.py with MASTER_MEAN set).
Target: every published Wes frame scores >= 0.88 against this mean.
