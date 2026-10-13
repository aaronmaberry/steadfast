import json,subprocess,sys
h=sys.argv[1];tl=json.load(open('audio/timeline.json'));segs=[x for x in tl if x['h']==h]
names={'W':['wes_talk1','wes_talk2'],'J':['jon_talk1','jon_talk2']}[h]
# normalized pingpong pool
pool=[]
for n in names:
    subprocess.run(f'ffmpeg -v error -y -i clips/{n}.mp4 -vf "scale=1344:768,fps=24,format=yuv420p" -an ls/{n}_f.mp4 && ffmpeg -v error -y -i ls/{n}_f.mp4 -vf reverse ls/{n}_r.mp4',shell=True)
    pool+= [f'ls/{n}_f.mp4',f'ls/{n}_r.mp4']
tot=sum(x['d'] for x in segs)
reps=int(tot//10)+2
with open(f'ls/{h}_list.txt','w') as f:
    for i in range(reps): f.write(f"file '{pool[i%len(pool)].split('/')[1]}'\n")
with open(f'ls/{h}_alist.txt','w') as f:
    for x in segs: f.write(f"file '../audio/{x['f']}'\n")
subprocess.run(f'ffmpeg -v error -y -f concat -safe 0 -i ls/{h}_alist.txt -c:a pcm_s16le ls/{h}_speech.wav',shell=True)
subprocess.run(f'ffmpeg -v error -y -f concat -safe 0 -i ls/{h}_list.txt -i ls/{h}_speech.wav -map 0:v -map 1:a -c:v libx264 -crf 16 -preset fast -c:a aac -b:a 192k -shortest ls/{h}_base.mp4',shell=True)
print(h,tot)
