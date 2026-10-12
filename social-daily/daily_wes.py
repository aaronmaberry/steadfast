"""Deterministic daily Wes pick from the pre-generated bank (zero image spend).
outfit      = BANK outfits[ordinal % 7]   (one outfit per day, 7-day cycle)
hook still  = <outfit>/cam-medium.jpg      (chest-up, to camera)
CTA still   = <outfit>/cam-close.jpg       (stage-right, to camera)
room shots  = 3 of the 4 room angles, dropping one per day: ROOM[(ordinal//7 + i) % 4] for i in 0..2,
              so a given outfit shows a different trio of angles each week (4-week cycle per outfit)."""
import datetime, json, os
HERE=os.path.dirname(os.path.abspath(__file__)); BANK=os.path.join(HERE,'wes-bank')
MAN=json.load(open(os.path.join(BANK,'bank.json')))
ROOM=['three-quarter','side-close','low-angle','walk']
def wes_for(date):
    o=date.toordinal(); outfit=MAN['outfits'][o%7]; s=(o//7)%4
    room=[ROOM[(s+i)%4] for i in range(3)]
    p=lambda a: os.path.join(BANK,outfit,a+'.jpg')
    return {'outfit':outfit,'hook':p('cam-medium'),'cta':p('cam-close'),'room':[p(a) for a in room],'room_angles':room}
def head_x(path):
    k='/'.join(path.split(os.sep)[-2:])[:-4]; return MAN['head_x'].get(k,0.5)
if __name__=='__main__':
    import sys
    d0=datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv)>1 else datetime.date.today()
    for i in range(8):
        d=d0+datetime.timedelta(i); w=wes_for(d); print(d,w['outfit'],'|',w['room_angles'])
