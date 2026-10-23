set -e
cd /workspace/artifacts/training/w01-poc/stage-1023b
TEETH=0.9 PORE=0 CREASE=0 TONAL=0 BROW=0 SPEC=0 REFW=0 /workspace/tools/swap-venv/bin/python work/post_v14.py 2>&1|grep -i error||true
O=swapped/T03-talk-P03-trim0-5.5-v14.mp4
ffmpeg -v error -y -framerate 24 -i work/T03frames_v14/%05d.png -i swapped/T03-talk-P03-trim0-5.5-v10.mp4 -map 0:v -map 1:a -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a copy -shortest $O
/workspace/tools/swap-venv/bin/python work/rescore.py $O 2>&1|tail -1
echo ALLDONE
