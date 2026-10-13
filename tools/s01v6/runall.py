import json,subprocess,sys
from shotplan import SP
from concurrent.futures import ThreadPoolExecutor
L=json.load(open('lsplan.json'))
def go(k):
    bg,cx,top=SP[k]; v=L[k]
    j=dict(name=k,video=f'clips/ls_{k}.mp4',t0=v['off'],dur=round(v['dur']+0.4,2),src=v['src'],bg=bg,cx=cx,top=top,audio=f'aud/{k}.wav')
    if v['src']=='72': j.update(zoom=1.75,top=0.07,cx=0.85)
    r=subprocess.run(['python3','comp6.py',json.dumps(j)],capture_output=True,text=True); print(k,r.returncode,r.stderr[-300:],flush=True)
ks=sys.argv[1:] or list(SP)
with ThreadPoolExecutor(1) as ex: list(ex.map(go,ks))
