#!/usr/bin/env python3
"""Exact large-k virtual child lengths and far-address indexed output without materialization."""
import json,hashlib,random,math
from pathlib import Path
from horn_frontier273 import source,prefix_len,character

def go():
    out=[];rng=random.Random(202610310612)
    for k in [6,12,20,40]:
        for no in [False,True]:
            C,_,n=source(k,no)
            sr=f'p cnf {n} {len(C)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in C)
            h=f'p cnf {2*k} {(1<<k)+(k if no else 0)}\n'
            length=len(h)+prefix_len(k,1<<k)
            if no:length+=sum(len(f'{2*i+1} {2*i+2} 0\n') for i in range(k))
            positions=[0,len(h)-1,len(h),length//2,length-1]+[rng.randrange(length) for _ in range(4)]
            samples={str(x):character(k,no,x) for x in positions}
            out.append({'k':k,'label':'UNSAT' if no else 'SAT','source_bits':len(sr),'child_bits':length,
                        'power_short':length*length<=len(sr),'indexed_samples':samples,'source_sha256':hashlib.sha256(sr.encode()).hexdigest()})
    p=Path(__file__).with_name('symbolic_raw.json');p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'cases':len(out),'k40_sat_child_bits':out[-2]['child_bits'], 'k40_sat_source_bits':out[-2]['source_bits']}))
if __name__=='__main__':go()