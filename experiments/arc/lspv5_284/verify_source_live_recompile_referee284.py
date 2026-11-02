#!/usr/bin/env python3
"""Independent no-import verifier for REFEREE284."""
import argparse,collections,itertools,json

F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
   (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))

def truth(x,a):return None if abs(x) not in a else a[abs(x)]==(x>0)
def cofactor(a):
    out=[]
    for c in F:
        q=[truth(x,a) for x in c]
        if True in q:continue
        d=tuple(x for x,v in zip(c,q) if v is None)
        if not d:return False
        out.append(d)
    return tuple(out) if out else True
def source(a):return all(any(a[abs(x)]==(x>0) for x in c) for c in F)
def circuit(R,a):
    if isinstance(R,bool):return R
    # Independent recursive evaluation of the declared private topology.
    clause=[any(a[abs(x)]==(x>0) for x in c) for c in R]
    while len(clause)>1:clause=[clause[i] and clause[i+1] if i+1<len(clause) else clause[i] for i in range(0,len(clause),2)]
    return clause[0]
def count(p):
    free=[v for v in range(1,10) if v not in p];q=0
    for bits in itertools.product((0,1),repeat=len(free)):
        a=dict(p);a.update(zip(free,bits));q+=source(a)
    return q

def main():
    ap=argparse.ArgumentParser();ap.add_argument("raw");a=ap.parse_args();d=json.load(open(a.raw));checks=0
    assert d["run"]=="SOURCE-LIVE-RECOMPILE-REFEREE284" and d["P_vs_NP"]=="OPEN";checks+=2
    hist=collections.Counter();states=rows=0
    for vals in itertools.product((None,0,1),repeat=9):
        p={i+1:v for i,v in enumerate(vals) if v is not None};R=cofactor(p);states+=1
        g=0 if isinstance(R,bool) else sum(map(len,R))-1;hist[str(g)]+=1;checks+=1
        free=[v for v in range(1,10) if v not in p]
        for bits in itertools.product((0,1),repeat=len(free)):
            z=dict(p);z.update(zip(free,bits));assert source(z)==circuit(R,z);rows+=1;checks+=1
    assert states==d["F9"]["pin_states"]==19683;checks+=1
    assert rows==d["F9"]["continuation_rows"]==262144;checks+=1
    assert dict(sorted(hist.items(),key=lambda x:int(x[0])))==d["F9"]["gate_histogram"];checks+=1
    pins=[{1:0,4:0,5:1,8:0},{1:1,4:0,5:1,8:0}]
    assert [count(p) for p in pins]==[7,0];checks+=2
    assert [x["models"] for x in d["same_original_F9"]]==[7,0];checks+=2
    assert d["F9"]["source_width_le2_but_tseitin_ternary"]=={"SAT":951,"UNSAT":1};checks+=2
    assert d["F9_forward"]=={"depth":6,"models":70,"obdd":{"best":52,"natural":66,"worst":80},"private_gates":35};checks+=5
    assert d["controls"]["Y6_models"]==20 and d["controls"]["F15_models"]==1032;checks+=2
    assert [x["models"] for x in d["same_original_F15"]]==[2,0];checks+=2
    assert d["controls"]["malformed_rejected"]==6;checks+=1
    print(json.dumps({"run":"VERIFY-SOURCE-LIVE-RECOMPILE-REFEREE284","checks":checks,"states":states,"rows":rows,"status":"PASS","P_vs_NP":"OPEN"},sort_keys=True))
if __name__=="__main__":main()
