# 24-session scale plan (waist-up, lip-synced, never-repeat plates) - v4 plan: boards ~45%

## CURRENT PLAN: S01 v4 (approved by Aaron 2026-10-12: "push boards")
Measured on the 184.3 s proof:
- Full boards cover 82.5 s (44.8%). Splits add 14.6 s, so boards or splits are on screen 53% of the time.
- Seconds of Wes that HeyGen has to render: 101.8 s (55%). v3 was 127 s.
- 10 Wes clips, about 10.2 s each on average. Each 3-minute stretch has about 11 boards.
- One walk-and-talk shot (8.4 s): image-to-video walk, then HeyGen lip-sync, then matted onto the locked plate-69 room on the box.
- New spend for v4: 0 credits and $0. It reuses v3 renders and the walk lip-sync that was already paid for.

Per 30-min session (1,800 s):
- About 994 s of Wes on screen, about 97 unique plates.
- At 57% yield, about 171 image gens x $0.50 = ~$85.
- HeyGen: 994 s x 1.10 rework x ~0.35 credit/s = ~383 credits, plus ~10 for one walk = ~393.

| All 24 sessions | v2 | v3 | **v4 (now)** |
|---|---|---|---|
| Unique plates | ~5,400 | ~3,050 | **~2,330** |
| Image cash | ~$4,750 | ~$2,700 | **~$2,050** (-57% vs v2) |
| HeyGen credits | ~12,000 | ~11,500 | **~9,400** incl. 24 walks (~9,150 without) (-22% vs v2) |

Assumptions: plate yield stays at 57%, rework at 10%, Avatar IV at ~0.35 credit/s. If plates are prompted as pure profile or three-quarter only and yield rises to 75%, image cash falls to ~$1,550.

---
(Older v3 notes follow, kept for history.)


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
