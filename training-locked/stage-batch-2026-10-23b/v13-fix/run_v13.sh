set -e
cd /workspace/artifacts/training/w01-poc/stage-1023b
/workspace/tools/swap-venv/bin/python work/post_v13.py 2>&1|grep -i error||true
O=swapped/T03-talk-P03-trim0-5.5-v13.mp4
ffmpeg -v error -y -framerate 24 -i work/T03frames_v13/%05d.png -i swapped/T03-talk-P03-trim0-5.5-v10.mp4 -map 0:v -map 1:a -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a copy -shortest $O
/workspace/tools/swap-venv/bin/python work/rescore.py $O 2>&1|tail -1
ffmpeg -v error -y -i swapped/T03-talk-P03-trim0-5.5-v10.mp4 -i $O -filter_complex "[0:v]drawtext=text='v10 (approved)':x=20:y=20:fontsize=36:fontcolor=white:box=1:boxcolor=black@0.5[a];[1:v]drawtext=text='v13 candidate':x=20:y=20:fontsize=36:fontcolor=white:box=1:boxcolor=black@0.5[b];[a][b]hstack" -map 1:a -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac swapped/T03-v10-vs-v13-sbs.mp4
echo ALLDONE
