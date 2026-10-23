import os,sys,json,base64,time,urllib.request
name,plate,kind,var=sys.argv[1:5]
H={"Authorization":"Bearer "+os.environ["XAI_API_KEY"],"Content-Type":"application/json"}
img={"url":"data:image/jpeg;base64,"+base64.b64encode(open(plate,'rb').read()).decode()}
HANDS=("His hands stay relaxed, fingers loosely curled or in soft fists, backs of the hands or knuckles facing the camera; small, varied, understated gestures that never repeat. "
"Never open palms, never spread fingers, never palms up, no thumbs-up, no pointing, no waving. ")
ID=("He is the only person visible: empty stage, no audience, no chairs or seats anywhere in frame, no props, no microphone, no watch, bare wrists, nothing in his hands, no text, no captions, no subtitles. "
"Keep exactly the same face, short dark-brown hair with lift, light beard, brown eyes, fair-olive skin, the same dark long-sleeve henley, same STEADFAST MEN backdrop and lighting. Photoreal, real hands with five normal fingers, no morphing. One continuous shot.")
TALK="His mouth is talking the entire time, lips and jaw clearly forming words in natural speech, as he speaks to the unseen room. "
if kind=="walk":
  P=(f"He walks 3-4 real full strides across the empty stage to screen-right, realistic human gait with visible weight shift and alternating legs, knees bending, heels and toes planting on the floor, {var}, no gliding, no hitching, no turning back. "
  +TALK+"His head stays turned toward the room off-screen, only one very brief glance toward the camera. Arms swing naturally at his sides. "+HANDS+
  "Camera pans smoothly to follow him, keeping framing from the knees up. "+ID)
else:
  P=(f"Steady stage camera, {var}, no cut. He stands on the stage explaining an idea about faithfulness and standing firm. "+TALK+
  "His gaze moves across the room from side to side, only one very brief glance toward the camera, occasional blinks. Natural torso motion: small weight shifts, a slight lean on an emphasis, shoulders turning with his gaze. "
  +HANDS+"Framing never reveals any audience or seats. "+ID)
body={"model":"grok-imagine-video-1.5","prompt":P,"image":img,"duration":10,"resolution":"720p"}
open(f"clips/{name}.prompt.txt","w").write(P)
r=json.load(urllib.request.urlopen(urllib.request.Request("https://api.x.ai/v1/videos/generations",json.dumps(body).encode(),H),timeout=120))
rid=r.get("request_id") or r.get("id"); print("rid",rid,flush=True)
while True:
    time.sleep(8)
    try: d=json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.x.ai/v1/videos/{rid}",headers=H),timeout=60))
    except Exception as e: print("poll err",e,flush=True); continue
    if d.get("status") not in ("pending","queued","processing","in_progress",None) or "video" in d: break
json.dump({"rid":rid,"resp":d,"plate":plate,"t":time.strftime("%Y-%m-%d %H:%M %Z")},open(f"clips/{name}.json","w"))
print("status",d.get("status"),"usage",d.get("usage"),flush=True)
v=d.get("video",{}).get("url")
if v: urllib.request.urlretrieve(v,f"clips/{name}.mp4"); print("ok",flush=True)
else: print(json.dumps(d)[:800])
