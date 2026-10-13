import json,subprocess,sys,os
os.chdir('/workspace/s01v7')
from concurrent.futures import ThreadPoolExecutor
A4='/workspace/s01v8/a4'
# shot: (angle, cx, top, dering)
SP={'W1':('a3',0.80,0.30,True),'W2':('a6',0.76,0.33,False),'W3':('a2',0.78,0.31,True),
    'W5':('a8',0.76,0.34,False),'W6':('a4',0.77,0.30,True),'W8':('a5',0.78,0.33,True),'W9':('a7',0.77,0.31,True),
    'W11':('a1',0.75,0.35,True),'W12m':('a3',0.79,0.32,True),'W14':('a6',0.77,0.30,False),'C1':('a4',0.76,0.33,True),'C2':('a2',0.78,0.31,False)}
def go(k):
    bg,cx,top,dr=SP[k]
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{A4}/{k}.mp4'],capture_output=True,text=True).stdout)
    j=dict(name=k,video=f'{A4}/{k}.mp4',t0=0,dur=round(d,3),src='id',bg=bg,cx=cx,top=top,audio=f'{A4}/{k}.mp4',fps=25,stab=2.5,stabkeep=0.2 if k!='W1' else 0.0,dering=dr)
    r=subprocess.run(['python3','comp8.py',json.dumps(j)],capture_output=True,text=True); print(k,r.returncode,r.stderr[-400:],flush=True)
ks=sys.argv[1:] or list(SP)
with ThreadPoolExecutor(3) as ex: list(ex.map(go,ks))
print('ALLDONE')
