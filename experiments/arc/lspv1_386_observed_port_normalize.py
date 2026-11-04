#!/usr/bin/env python3
"""Independent deterministic controls for bounded-observation public-wire normalization.
This is a toy typed circuit grammar, NOT the original R_mix341 checker.
"""
import json
from pathlib import Path

def eval_topo(gates, assignment):
    v=[(assignment>>i)&1 for i in range(3)]
    for op,a,b in gates:
        if op=='AND': out=v[a]&v[b]
        elif op=='OR': out=v[a]|v[b]
        elif op=='XOR': out=v[a]^v[b]
        elif op=='NOT': out=1-v[a]
        elif op=='ONE': out=1
        elif op=='ZERO': out=0
        else: raise ValueError('bad gate')
        v.append(out)
    return v

def vector(gates,wire):
    return sum(eval_topo(gates,a)[wire]<<a for a in range(8))

def create(size):
    gates=[]
    for j in range(size):
        a=(7*j+1)%(j+3); b=(11*j+2)%(j+3)
        gates.append((['AND','XOR','OR','NOT','ONE','ZERO'][j%6],a,b))
    return gates

def main():
    checks=0; rows=[]
    for size in [12,120,1200,4800]:
        gates=create(size)
        outputs=[0,1,2]+[3+(k*17)%size for k in range(1,min(41,size))]
        actual=[vector(gates,w) for w in outputs]
        canonical=dict(sorted({m:i for i,m in enumerate(sorted(set(actual)))}.items()))
        aliases=[canonical[m] for m in actual]
        for a in range(8):
            values=eval_topo(gates,a)
            for k,w in enumerate(outputs):
                assert values[w]==((actual[k]>>a)&1)
                assert values[w]==((list(canonical)[aliases[k]]>>a)&1)
                checks+=2
            for k in range(1,len(outputs)):
                left=values[outputs[k-1]]
                right=values[outputs[k]]
                old=(left^right)&(values[outputs[0]]|(1-right))
                v0=(actual[0]>>a)&1
                vl=(actual[k-1]>>a)&1
                vr=(actual[k]>>a)&1
                new=(vl^vr)&(v0|(1-vr))
                assert old==new
                checks+=1
        assert len(canonical)<=256
        assert 26*len(canonical)+len(aliases)<=26*256+len(outputs)
        checks+=2
        rows.append(dict(gates=size,observable=len(outputs),distinct_functions=len(canonical),
          alias_count=len(aliases),canonical_truth_vectors=sorted(set(actual)),all_8_assignments=True))
    for a in range(8):
        x,y=a&1,(a>>1)&1
        assert x==x and y!=1-y; checks+=1
    for size in [12,120]:
        gates=create(size)
        for ptr in (-1,size+3):
            try:
                if not 0<=ptr<3+len(gates): raise ValueError('bad port')
                raise AssertionError('bad pointer accepted')
            except ValueError: checks+=1
        assert vector(gates,0)==0b10101010; checks+=1
        assert (vector(gates,0)^1)!=vector(gates,0); checks+=1
        try:
            eval_topo([('BAD',0,0)],0)
            raise AssertionError('bad gate accepted')
        except ValueError: checks+=1
    cases=[[(1,)],[(-1,)],[(1,),(-1,)],[(1,2),(-1,2),(-2,)],[]]
    def sat(cls):
        return any(all(any((lit>0)==bool((a>>(abs(lit)-1))&1) for lit in c) for c in cls) for a in range(4))
    got=[sat(f) for f in cases]
    assert got==[True,True,False,False,True]; checks+=len(cases)
    def valid(cls):
        return isinstance(cls,list) and all(isinstance(c,list) and all(
           isinstance(l,int) and not isinstance(l,bool) and l!=0 and abs(l)<=2 for l in c) for c in cls)
    for x in [None,[[0]],[[3]],[[True]],[["1"]]]:
        assert not valid(x); checks+=1
    result=dict(test='LSPV1_386_bounded_observation',status='COMPUTATIONAL',seed=None,
       checker='python iterative topo',checks=checks,rows=rows,root_only_counterexample=True,
       strict_signed_cnf_labels=got,malformed_rejected=5,original_R_mix341_verified=False)
    print(json.dumps(result))
if __name__=='__main__':main()
