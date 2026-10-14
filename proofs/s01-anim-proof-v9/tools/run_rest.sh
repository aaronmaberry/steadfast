#!/bin/bash
cd /workspace/s01v9/p9; F=/workspace/cvenv/bin/python
for x in "W12m S1-wide" "C2 S7-gesture" "W8b S2-medium"; do set -- $x
 $F comp9.py "{\"name\":\"$1\",\"video\":\"/workspace/s01v9/p9/hg/$1.mp4\",\"still\":\"$2\"}" > logs/$1.comp.log 2>&1 && $F gate9.py $1 $2 > logs/$1.gate.log 2>&1; echo "$1 rc=$?"; rm -rf work/$1/fr
done
echo RESTDONE
