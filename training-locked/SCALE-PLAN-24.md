# 24-session scale plan (waist-up, lip-synced, never-repeat plates) - v3 target (~50% cut)

## What changed in S01 v3 (184 s proof)
- 13 lip-synced Wes clips instead of 28. Average talking clip 9.8 s (v2: 6.0 s).
- Boards and splits now cover ~38% of the runtime (v2: ~25%). That adds 4 new full boards: boots, on-time, guest and checking.
- Wes is on screen ~127 s out of 184 s (69%).
- Every plate is Real-ESRGAN x4 upscaled on the box (CPU, free, ~2.5 min/plate). It is blended back with a little original texture so skin doesn't look waxy, and it has the locked STEADFAST screen stamped in before rendering.
- **Measured HeyGen spend for v3:** 60 premium credits (4,020 -> 3,960). That covers 13 Avatar IV clips (127 s) plus one 9 s image-to-video walk test, which was rejected. That works out to ~0.44 credit per rendered second, walk test included.
- **New image generations in v3:** 0 (it reused S01's own clean plates).

## Per 30-min session (1,800 s) at the v3 rhythm
- Wes on screen ~1,245 s at ~9.8 s per shot -> ~127 unique plates per session (v2 plan: ~225).
- Plate yield was 57% in v2. At that yield it takes ~223 image gens x ~$0.50, or ~$110 per session (v2 plan: ~$200).
- HeyGen: 1,245 s x 1.10 rework x ~0.35 credit/s -> ~480 credits per session.

## All 24 sessions
| | v2 plan | v3 plan | change |
|---|---|---|---|
| Unique plates | ~5,400 | ~3,050 | -44% |
| Image gens | ~9,500 | ~5,350 | -44% |
| Image cash | ~$4,750 | ~$2,700 | -43% |
| HeyGen render seconds | ~37,700 | ~32,900 | -13% |
| HeyGen credits | ~12,000 | ~11,500 | -4% to -13% |

Plain answer: the cash (image) cost drops about 45%. HeyGen barely moves, because it charges per second of Wes on screen, and longer shots don't reduce Wes's screen time. Only more board time does.

## To get a full 50% on both lines
- Go to ~45% boards/splits per session. Wes would be ~990 s per session, ~100 plates, ~$87 per session in images, and ~380 HeyGen credits per session.
- 24-session total: ~$2,100 in images (-56%) and ~9,100 HeyGen credits (-25%).
- Raise plate yield by prompting pure profile / three-quarter only (frontal plates pull the eyes to the lens). 57% -> 75% yield cuts image cash another ~25%.

## Not included
- **Walking while talking.** Image-to-video invents background (exit signs, doors, podiums, a laptop, pans). create_lipsync jobs have sat in "running" for 2+ hours. Plan for at most ~1 walk per session until a walk passes the locked-room check. Budget ~10 credits per attempt.
