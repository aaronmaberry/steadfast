import json,subprocess,sys,os
os.chdir('/workspace/s01v7'); sys.path.insert(0,'/workspace/s01v7')
from shotplan import SP
from concurrent.futures import ThreadPoolExecutor
L=json.load(open('lsplan.json')); G=json.load(open('v7/lsids7g.json'))
SRC80={'W2':'72','W6':'89','W10':'72','W11':'89','C1':'72'}
def go(k):
    bg,cx,top=SP[k]; v=L[k]
    j=dict(name=k,video=f'v7/clips/ls_{k}.mp4',t0=v['off'],dur=round(v['dur']+0.4,2),src=v['src'],bg=bg,cx=cx,top=top,audio=f'aud/{k}.wav',stab=2.5)
    if v['src']=='73': j.update(stab=1.2,stabkeep=0.0,cx=round(cx-0.06,2))
    if k in G:
        j.update(video=f'v7/clips/lsg_{k}.mp4',dering=True)
        if k in SRC80: j.update(src=SRC80[k])
        if k in ('W10','W11'): j.update(flip=True)
    elif v['src']=='72': j.update(zoom=1.75,top=0.07,cx=0.85)
    r=subprocess.run(['python3','comp7.py',json.dumps(j)],capture_output=True,text=True); print(k,r.returncode,r.stderr[-300:],flush=True)
ks=sys.argv[1:] or list(SP)
with ThreadPoolExecutor(2) as ex: list(ex.map(go,ks))
print('ALLDONE')
