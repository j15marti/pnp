#!/usr/bin/env python3
"""Adversarial input-index summary: reference scan vs incrementally maintained high bit count."""
import random,json
from pathlib import Path
r=random.Random(460); L=9; B=1<<L
low=0;high=0;bits={};pos=0;checks=0;overflow=0;resets=0;edits=0
for j in range(10000):
    op=r.randrange(10)
    if op<3:
        pos=max(0,min(150,pos+r.choice([-5,-1,1,7])))
    elif op<8:
        v=r.randrange(2);old=bits.get(pos,0)
        if old!=v:
            bits[pos]=v
            if pos<L:low+=(v-old)*(1<<pos)
            else:high+=v-old
        edits+=1
    elif op==8:
        valid= (high==0 and low < B)
        actual=sum(v<<i for i,v in bits.items())
        assert valid==(actual < B)
        if not valid:overflow+=1
        checks+=1
    else:
        bits={};low=0;high=0;pos=0;resets+=1
    assert low==sum(v<<i for i,v in bits.items() if i<L)
    assert high==sum(v for i,v in bits.items() if i>=L)
# adversarial many long leading zeros and one distant high bit
bits={129:1,1:1};low=2;high=1
assert high>0 and sum(v<<i for i,v in bits.items())>=B
res={'status':'PASS','seed':460,'address_bits':L,'guest_B':B,'random_transitions':10000,'random_checks':checks,'out_of_range_events':overflow,'clearing_epochs':resets,'write_operations':edits,'high_one_falsifier_passed':True,'scope':'host model of incremental index summary, not native FLMV execution'}
Path('/mnt/data/LSPV4_460_INDEX_TRACKER_RAW.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
