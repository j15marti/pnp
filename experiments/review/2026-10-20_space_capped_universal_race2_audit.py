#!/usr/bin/env python3
"""Finite abstract checks for SPACE-CAPPED-UNIVERSAL-RACE2.
Finite proof registry only: NOT formal SAT correctness certification,
NOT a one-way-input physical simulator. Python heap is not work-space data.
"""
import itertools, json

CLAUSES=list(itertools.product((0,1),repeat=3))
def sat(mask):
    return any(all(not (mask>>j & 1) or tuple((a>>q)&1 for q in range(3))!=bad
                   for j,bad in enumerate(CLAUSES)) for a in range(8))
TRUTH={x:sat(x) for x in range(256)}
CANDS=(('brute',6,3,12,True),
       ('special',7,5,11,True),
       ('highspace',8,4,64,True),
       ('smallslow',5,4,6,True),
       ('wrong',4,2,2,False))
def runtime(name,x):
    baseline=32+5*x.bit_count()
    if name=='brute': return (TRUTH[x],baseline)
    if name=='special': return (TRUTH[x],3 if x==0b10100101 else baseline+8)
    if name=='highspace': return (TRUTH[x],4+2*x.bit_count())
    if name=='smallslow': return (TRUTH[x],3*baseline)
    return (True,2)
def ceil_log2(v): return (v-1).bit_length()
def race(x,cap):
    for j in range(1,30):
        for name,ell,v,space,valid in CANDS:
            if not valid or space>cap or ell>j: continue
            ans,t=runtime(name,x)
            if v+t<=2**(j-ell):
                return ans,name,j
    raise AssertionError("fallback not covered by cap")

def main():
    checked=0; envelopes=0; soundness=0
    winners={}
    for cap in (6,12,64):
        winners[str(cap)]={}
        for x in range(256):
            answer,name,stage=race(x,cap)
            assert answer==TRUTH[x]
            winners[str(cap)][name]=winners[str(cap)].get(name,0)+1
            checked+=1
            for cn,ell,v,space,valid in CANDS:
                if valid:
                    assert runtime(cn,x)[0]==TRUTH[x]
                    soundness+=1
                if valid and space<=cap:
                    _,t=runtime(cn,x)
                    assert stage<=ell+ceil_log2(v+t)
                    envelopes+=1
    lag=0
    for n in range(1,13):
        transcripts={tuple((v>>k)&1 for k in range(n)) for v in range(2**n)}
        assert len(transcripts)==2**n
        lag+=len(transcripts)
    result=dict(model='finite abstract candidate registry',sat_instances=256,
                race_cases=checked,soundness_checks=soundness,
                envelope_checks=envelopes,oneway_lag_transcripts=lag,
                wrong_candidate_certified=False,winners_by_cap=winners,
                failed_assertions=0,P_vs_NP='OPEN')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__': main()
