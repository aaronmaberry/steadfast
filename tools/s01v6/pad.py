import json,random,subprocess
random.seed(6)
D=json.load(open('durs.json'))
for k,a,b in [('C1',0,7.12),('C2',7.12,11.39),('C3',11.39,18.44)]: D[k]=round(b-a,2)
src={'W1':'73','W2':'80','W3':'72','W4':'89','W5':'73','W6':'80','W7':'72','W8':'89','W9':'72','W10':'80','S1':'89','S2':'73','W11':'80','W12':'72','W13':'89','W14':'73','C1':'80','C2':'89','C3':'72'}
L={'73':12.25,'72':15,'80':15,'89':15}
plan={}
for k,s in src.items():
    d=D[k]; o=round(random.uniform(0.3,max(0.3,L[s]-d-0.4)),2)
    subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-t',str(o),'-i','anullsrc=r=44100:cl=mono','-i',f'aud/{k}.wav','-filter_complex','[0][1]concat=n=2:v=0:a=1,apad','-t',str(L[s]-0.05),'-ac','1','-b:a','192k',f'aud/P_{k}.mp3'],check=True)
    plan[k]=dict(src=s,dur=d,off=o)
json.dump(plan,open('lsplan.json','w'),indent=1); print(plan)
