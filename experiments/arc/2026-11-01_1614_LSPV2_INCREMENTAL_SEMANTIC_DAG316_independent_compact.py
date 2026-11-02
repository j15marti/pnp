#!/usr/bin/env python3
"""No-producer-import verification of the source-F9 control used by DAG316.
The full no-import 8,420-assertion table verifier is in the 14-file archive.
"""
import json,itertools,subprocess,sys,pathlib
P=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
N=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F=P+[tuple(-v for v in c) for c in N]
p={2:1,3:0,5:1,6:0,8:0}
q={2:0,3:1,5:1,6:1,8:0}
r={1:1,7:0}
def count(pins):
    free=[v for v in range(1,10) if v not in pins]
    result=0
    for z in itertools.product((0,1),repeat=len(free)):
        a=dict(pins);a.update(zip(free,z))
        if all(any(a[abs(x)]==(x>0) for x in c) for c in F):result+=1
    return result
assert count({})==70
assert (count(p),count(q),count(p|r),count(q|r))==(4,4,0,1)
checks=0
for i in range(len(F)):
    for j in range(i+1,len(F)):
        for a,b in itertools.product((0,1),repeat=2):
            req={};consistent=True
            for clause,ext in ((F[i],a),(F[j],b)):
                for z in clause:
                    bit=(z>0) if ext else (z<0)
                    if abs(z) in req and req[abs(z)]!=bit:consistent=False
                    req[abs(z)]=bit
            same=any(z in F[j] for z in F[i])
            opposite=any(-z in F[j] for z in F[i])
            assert consistent==(not opposite if a==b else not same)
            checks+=1
path=pathlib.Path(__file__).with_name(
    "2026-11-01_1614_LSPV2_INCREMENTAL_SEMANTIC_DAG316_compact.py")
res=subprocess.run([sys.executable,str(path)],capture_output=True,text=True,check=True)
record=json.loads(res.stdout)
assert record["A"]["decision"]=="UNSAT"
assert record["B"]["decision"]=="SAT"
assert record["A"]["after"]==0 and record["B"]["after"]==1
print(json.dumps({"status":"PASS","no_producer_import":True,
                  "same_source_F9":True,"signed_pair_modes":checks,
                  "F9_models":70,"p_q_models":[4,4],
                  "future_models":[0,1],"P_vs_NP":"OPEN"},indent=2))
