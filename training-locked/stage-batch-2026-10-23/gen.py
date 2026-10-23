import os,sys,json,base64,time,urllib.request
name,plate,kind,pace=sys.argv[1:5]
H={"Authorization":"Bearer "+os.environ["XAI_API_KEY"],"Content-Type":"application/json"}
img={"url":"data:image/jpeg;base64,"+base64.b64encode(open(plate,'rb').read()).decode()}
ID=("He is the only person visible: empty stage, no audience, no chairs or seats anywhere in frame, no props, no microphone, no watch, nothing in his hands, no text or captions. "
"Keep exactly the same face, short dark-brown hair with lift, light beard, brown eyes, fair-olive skin, the same dark long-sleeve henley, same STEADFAST MEN backdrop and lighting. Photoreal, real hands with five normal fingers, no morphing. One continuous shot.")
if kind=="walk":
  P=(f"He walks 3-4 real full strides across the empty stage to screen-right, realistic human gait with visible weight shift and alternating legs, knees bending, feet planting firmly, {pace} pace, no gliding, no hitches. "
  "He is talking to the room the whole time as he walks, mouth clearly and continuously moving with natural speech, lips and jaw forming words. His head is turned toward the unseen room in the direction he walks, maybe one brief glance toward the camera. "
  "Arms swing naturally; once his near hand lifts in a small relaxed beat gesture with curled fingers, then drops. No open palms, no thumbs-up, no pointing. Camera pans smoothly to follow him, keeping framing from the knees up, never revealing seating. "+ID)
else:
  P=("Stage camera, steady with a very slow subtle push-in, no cut. He stands on the stage speaking warmly and earnestly to the unseen room off-screen, explaining an idea about men standing firm; "
  "his mouth is clearly and continuously moving with natural speech, lips and jaw forming words, occasional blinks. His gaze moves across the room, left then right, with one brief glance toward the camera. "
  f"Natural varied torso motion: {pace}. His hands stay mostly low or loosely together, with a few different small beat gestures using relaxed curved fingers, never repeating the same move. "
  "No open palms toward the camera, no thumbs-up, no pointing, no waving. Camera framing stays tight enough that no audience or seats ever appear. "+ID)
body={"model":"grok-imagine-video-1.5","prompt":P,"image":img,"duration":10,"resolution":"720p"}
open(f"clips/{name}.prompt.txt","w").write(P)
t0=time.time()
r=json.load(urllib.request.urlopen(urllib.request.Request("https://api.x.ai/v1/videos/generations",json.dumps(body).encode(),H),timeout=120))
rid=r.get("request_id") or r.get("id"); print("rid",rid,flush=True)
while True:
    time.sleep(8)
    try: d=json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.x.ai/v1/videos/{rid}",headers=H),timeout=60))
    except Exception as e: print("poll err",e,flush=True); continue
    if d.get("status") not in ("pending","queued","processing","in_progress",None) or "video" in d: break
d.pop("video_b64",None)
json.dump({"rid":rid,"resp":d,"plate":plate,"t":time.strftime("%Y-%m-%d %H:%M %Z")},open(f"clips/{name}.json","w"))
print("status",d.get("status"),"usage",d.get("usage"),flush=True)
v=d.get("video",{}).get("url")
if v: urllib.request.urlretrieve(v,f"clips/{name}.mp4"); print("ok",int(time.time()-t0),flush=True)
else: print(json.dumps(d)[:800])
