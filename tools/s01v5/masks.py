import cv2,numpy as np,os,sys
from rembg import remove,new_session
s=new_session('u2net_human_seg'); os.makedirs('masks',exist_ok=True)
for k in sys.argv[1:]:
    d=f'clips/{k}_f'; n=len(os.listdir(d)); M=[]
    for i in range(1,n+1,5):
        im=cv2.resize(cv2.imread(f'{d}/%05d.png'%i),(480,270)); M.append(np.array(remove(im,session=s,only_mask=True)))
    M=np.array([(m>40).astype(np.uint8)*255 for m in M]); np.save(f'masks/{k}.npy',M); print(k,M.shape,flush=True)
