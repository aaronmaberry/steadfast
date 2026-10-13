import sys,os
from PIL import Image,ImageDraw
d=sys.argv[1]; out=sys.argv[2]; step=float(sys.argv[3]) if len(sys.argv)>3 else 2.0; fps=25
n=len(os.listdir(d)); ts=[i*step for i in range(int(n/fps/step)+1)]
cols=6; w,h=320,180; S=Image.new('RGB',(cols*w,((len(ts)+cols-1)//cols)*h)); dr=ImageDraw.Draw(S)
for i,t in enumerate(ts):
    k=min(n,int(t*fps)+1); im=Image.open(f'{d}/%05d.png'%k).resize((w,h)); S.paste(im,((i%cols)*w,(i//cols)*h)); dr.text(((i%cols)*w+4,(i//cols)*h+4),f'{t:.0f}s',fill='yellow')
S.save(out)
