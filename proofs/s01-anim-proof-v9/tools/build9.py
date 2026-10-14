import json,os,subprocess,sys,numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,'/workspace/s01v7'); sys.argv=[sys.argv[0]]
import b5lib as B
W,H,FPS=1280,720,25
V7A='/workspace/s01v7/aud'; SH='/workspace/s01v9/p9/shots'
D7={"W4":5.5,"W7":7.8,"B1":21.0,"B2":9.9,"W10":4.4,"S1":8.2,"S2":9.4,"C3":7.01}
SEQ=[('W1','clip'),('W2','clip'),('W3','clip'),('BL','board','luke',['B1','W4']),('W5','clip'),('W6','clip'),
     ('BP','board','point',['W7','B2']),('WK','walk'),('W8b','clip'),('W9','clip'),('BD','board','door',['W10','S1']),
     ('BS','board','small',['S2']),('W11','clip'),('W12m','clip'),('W14','clip'),('C1','clip'),('C2','clip'),('END','end',None,['C3'])]
def vdur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
def frames_of(f):
    p=subprocess.Popen(['ffmpeg','-v','error','-i',f,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        yield Image.frombytes('RGB',(W,H),b)
def enc(out):
    return subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
def lt_overlay(t):
    blank=Image.new('RGB',(1920,1080),(0,0,0)); 
    if not 1.5<=t<5.5: return None
    # render lower third on black and on white to recover alpha, then downscale overlay only (never resample Wes)
    a=np.asarray(B.lower_third(Image.new('RGB',(1920,1080),(0,0,0)),t)).astype(np.float32)
    b=np.asarray(B.lower_third(Image.new('RGB',(1920,1080),(255,255,255)),t)).astype(np.float32)
    al=1-(b-a)/255; al=al.mean(2,keepdims=True).clip(0,1); col=np.where(al>1e-3,a/np.maximum(al,1e-3),0)
    rgba=np.concatenate([col,al*255],2).clip(0,255).astype(np.uint8)
    return Image.fromarray(rgba,'RGBA').resize((W,H),Image.LANCZOS)
os.makedirs('seg9',exist_ok=True)
t=0; plan=[]; aud=[]
for i,s in enumerate(SEQ):
    k,kind=s[0],s[1]
    if kind=='clip': d=vdur(f'{SH}/{k}.mp4'); aud.append(('shot',k,t))
    elif kind=='walk': d=vdur(f'{SH}/{k}.mp4')
    else:
        d=0
        for p in s[3]: aud.append(('wav',p,t+d+0.15)); d+=D7[p]+0.4
        if k=='BP': d+=2.5
        if kind=='end': d+=1.6
    nf=round(d*FPS); plan.append(dict(i=i,k=k,kind=kind,t0=round(t,3),dur=round(nf/FPS,3))); t+=nf/FPS
json.dump(plan,open('timeline9.json','w'),indent=0); json.dump(aud,open('aud9.json','w'))
print('total',round(t,2))
def render(e):
    i,k,kind,t0,d=e['i'],e['k'],e['kind'],e['t0'],e['dur']; nf=round(d*FPS); out=f'seg9/{i:02d}.mp4'; P=enc(out); n=0; last=None
    if kind=='board':
        for j in range(nf): P.stdin.write(B.board(SEQ[i][2],t0+j/FPS,j/FPS).resize((W,H),Image.LANCZOS).tobytes())
        n=nf
    elif kind=='end':
        fs=sorted(os.listdir('/workspace/s01v7/v7/endf'))
        for j in range(nf): P.stdin.write(Image.open('/workspace/s01v7/v7/endf/'+fs[min(len(fs)-1,j)]).convert('RGB').resize((W,H),Image.LANCZOS).tobytes())
        n=nf
    else:
        for fr in frames_of(f'{SH}/{k}.mp4'):
            if n>=nf: break
            if k=='W1':
                ov=lt_overlay(n/FPS)
                if ov is not None: fr=fr.convert('RGBA'); fr.alpha_composite(ov); fr=fr.convert('RGB')
            P.stdin.write(fr.tobytes()); last=fr; n+=1
        while n<nf: P.stdin.write(last.tobytes()); n+=1
    P.stdin.close(); P.wait(); print('seg',i,k,flush=True)
def mix(T):
    inp=[]; fc=[]
    for j,(typ,k,t) in enumerate(aud):
        src=f'{SH}/{k}.mp4' if typ=='shot' else f'{V7A}/{k}.wav'
        inp+=['-i',src]; ms=int(round(t*1000)); fc.append(f'[{j}:a]aresample=48000,aformat=channel_layouts=mono,adelay={ms}|{ms},apad=whole_dur={T}[v{j}]')
    n=len(aud)
    bed=("sine=f=110:d=%.2f,volume=0.5[s1];sine=f=164.81:d=%.2f,volume=0.35[s2];sine=f=220:d=%.2f,volume=0.25[s3];sine=f=277.18:d=%.2f,volume=0.18[s4];"
     "anoisesrc=c=pink:d=%.2f:a=0.05,lowpass=f=500[nz];[s1][s2][s3][s4][nz]amix=inputs=5:normalize=0,tremolo=f=0.12:d=0.35,lowpass=f=900,"
     "aresample=48000,volume=0.2,afade=t=in:d=2.5,afade=t=out:st=%.2f:d=3[bed]")%(T,T,T,T,T,T-3)
    fc.append(bed); fc.append(''.join(f'[v{j}]' for j in range(n))+f'amix=inputs={n}:normalize=0[vox]')
    fc.append('[vox][bed]amix=inputs=2:normalize=0,pan=stereo|c0=c0|c1=c0,loudnorm=I=-14:TP=-1.5:LRA=11[out]')
    subprocess.run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fc),'-map','[out]','-t',str(T),'-ar','48000','mix9.wav'],check=True)
if __name__=='__main__':
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(2) as ex: list(ex.map(render,plan))
    mix(t)
    open('concat9.txt','w').write(''.join(f"file '/workspace/s01v9/p9/seg9/{e['i']:02d}.mp4'\n" for e in plan))
    out='/workspace/tmp-send/s01-anim-proof-v9/S01-anim-proof-v9-share.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','concat9.txt','-i','mix9.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest',out],check=True)
    print('OUT',out,vdur(out))
