#!/bin/bash
cd /workspace/s01v9/p9
declare -A S=([W1]=S2-medium [W2]=S3-medcloseup [W3]=S1-wide [W5]=S4-34left [W6]=S7-gesture [W8]=S6-walk [W9]=S5-34right [W11]=S3-medcloseup [W12m]=S1-wide [W14]=S4-34left [C1]=S5-34right [C2]=S7-gesture)
one(){ k=$1; s=${S[$k]}; /workspace/cvenv/bin/python comp9.py "{\"name\":\"$k\",\"video\":\"/workspace/s01v9/p9/hg/$k.mp4\",\"still\":\"$s\"}" > logs/$k.comp.log 2>&1 && /workspace/cvenv/bin/python gate9.py $k $s > logs/$k.gate.log 2>&1; echo "$k $(tail -1 logs/$k.gate.log | python3 -c 'import json,sys;d=json.loads(sys.stdin.read());print({x:d[x] for x in d if x.startswith("pass")})' 2>/dev/null || echo FAIL)"; }
export -f one; export S
mkdir -p logs
for k in W1 W2 W3 W5 W6 W8 W9 W11 W12m W14 C1 C2; do echo $k; done | xargs -P 1 -I{} bash -c "$(declare -p S); $(declare -f one); one {}"
echo ALLDONE
