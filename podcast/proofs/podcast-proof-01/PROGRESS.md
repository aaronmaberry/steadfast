# podcast-proof-01 PROGRESS
Work dir: /workspace/pp1 (src/, clips/, audio/, ls/, out/)
HeyGen start balance 3688 (cap 150 -> floor 3538).
- assets: wes3.jpg c20f02ea5f884801999f585f567a8d2e ; jon.jpg b91818278e50433dbd4d4d5dd8457201
- i2v wes test 10s 1080p: 1942158de1474029b48283f362c8195d  -> cost 37 credits (3.7 cr/s!)
- 768p i2v costs ~3 cr/10s (verify). Clips (768p,10s): jon_talk1 eb8e507937b54173bdcb172359439f4e, wes_listen1 d8ace044a41c4a2db85060821c7b454c, wes_sip 920c8ab2580a4dc293c9c8db8b3e34f8, jon_listen1 bd61e1140573406987616cc7382d3917, jon_sip c74d1cc5d02c49caa455def3929df96e, wes_talk2 c47a5ce66c4c4262bcc2c91cba4f4982, jon_talk2 624fc322402c4eac87a498c0a7931f0d
- EL flow n5xeFBrU6kHihnBOn0fa: W session sgPcC1KupqM6OY7I9iKm (2032 cr ~$0.34), J session Ph8obdLqpSf2XRC7SdUz (690 cr ~$0.11)
- Script: biblical-manhood/studio/podcast-show/scripts/E007-waiting-is-not-peace.md, excerpt in /workspace/pp1/script.txt
- Balance after 7x768p clips: 3618 (spent 70). Clips downloaded to /workspace/pp1/clips, all usable.
- audio split -> /workspace/pp1/audio/*.wav, timeline.json (159s dialogue). bases: ls/J_base.mp4 (asset 5116751c148344cea3e71fa3e852deac), ls/W_base.mp4 (asset d75c686465a0417d992d9407d0fab329)
- lipsync J precision: 1bd282f75b2c41bbacc4eef928ce4b96 (balance right after: 3614)
- lipsync W precision: 8d3434cbb05b404f9d853949934d13ef. Balance after both submits: 3604 (HeyGen spent 84). J_ls done -> ls/J_ls.mp4 (aligned offset 0).
- build: /workspace/pp1/build/layers.py (plate layers, L/), render.py (args: W_ls J_ls out limit), mix.py -> mix.wav. Final mux: video_noaudio.mp4 + mix.wav
- W_ls done -> ls/W_ls.mp4 (offset 0). Final balance 3575 => HeyGen total 113 cr. EL $0.45.
- Rendered full: build/video_noaudio.mp4 + mix.wav -> walk-steadfast-podcast-proof-01.mp4 (2-pass 2050k, 47.6 MB, 174 s).
- STATUS: COMPLETE. To re-render: cd /workspace/pp1/build && python3 layers.py && python3 render.py ../ls/W_ls.mp4 ../ls/J_ls.mp4 x 174 && python3 mix.py, then the 2-pass mux (see NOTES).
- Pushed to branch podcast-proof-01 under podcast/proofs/podcast-proof-01/ (not merged).
