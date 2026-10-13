import json
D=json.load(open('durs.json'))
S=[]; t=0.0
def add(**k):
    global t; k['t0']=round(t,3); S.append(k); t+=k['dur']
add(kind='clip',src='R1',plate=80,frames='clips/R1_f',dur=D['R1'],crop=[1.12,0.52,0.45],zend=1.16)
add(kind='clip',src='R2b',plate=80,frames='clips/R2b_f',dur=D['R2'],crop=[1.2,0.5,0.36],zend=1.24)
add(kind='board',board='luke',dur=D['B1'],vo='B1')
add(kind='clip',src='R3',plate=72,frames='clips/R3_f',dur=11.65,c0=0,crop=[1.1,0.52,0.45])
add(kind='clip',src='R3',plate=72,frames='clips/R3_f',dur=8.55,c0=11.65,crop=[1.18,0.53,0.38],zend=1.22)
add(kind='clip',src='R3',plate=72,frames='clips/R3_f',dur=D['R3']-20.2,c0=20.2,crop=[1.0,0.5,0.5],zend=1.04)
add(kind='board',board='point',dur=D['B2']+2.5,vo='B2')
add(kind='clip',src='R4b-walk',plate='89 on 69',frames='clips/W_f',dur=9.72,c0=0,crop=[1.0,0.49,0.5],zend=1.02)
add(kind='clip',src='R4b-walk',plate='89 on 69',frames='clips/W_f',dur=D['R4']-9.72,c0=9.72,crop=[1.18,0.417,0.42],zend=1.2)
add(kind='split',src='R5b',plate=72,frames='clips/R5b_f',board='door',dur=8.42,c0=0,crop=[1.0,0.66,0.5],slide=1)
b0=t; add(kind='split',src='R5b',plate=72,frames='clips/R5b_f',board='small',dur=D['R5']-8.42,c0=8.42,crop=[1.0,0.66,0.5]); S[-1]['b0']=round(b0,3)
add(kind='clip',src='R6',plate=73,frames='clips/R6_f',dur=9.32,c0=0,crop=[1.0,0.5,0.5],zend=1.03)
add(kind='clip',src='R6',plate=73,frames='clips/R6_f',dur=11.25,c0=9.32,crop=[1.15,0.42,0.45],zend=1.19)
add(kind='clip',src='R6',plate=73,frames='clips/R6_f',dur=D['R6']-20.57,c0=20.57,crop=[1.3,0.45,0.42],zend=1.36)
add(kind='clip',src='R7b',plate=89,frames='clips/R7b_f',dur=9.0,c0=0,crop=[1.15,0.43,0.4],zend=1.18)
add(kind='clip',src='R7b',plate=89,frames='clips/R7b_f',dur=D['R7']-9.0,c0=9.0,crop=[1.2,0.40,0.36],zend=1.25)
add(kind='end',dur=2.6)
json.dump(S,open('shots.json','w'),indent=0); print(round(t,2))
# audio placement: render audio starts at first shot of that render
A=[]; seen=set()
for s in S:
    k=s.get('vo') or s.get('src','').replace('-walk','').replace('b','') if s['kind']!='end' else None
    if not k or k in seen: continue
    seen.add(k); A.append((k,s['t0']))
json.dump(A,open('audplace.json','w')); print(A)
