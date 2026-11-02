#!/usr/bin/env python3
"""No-producer-import original-source check of compact317.py."""
import itertools,json,subprocess,sys,pathlib
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=P+tuple(tuple(-z for z in c) for c in N)
def count(p):
    free=[x for x in range(1,10) if x not in p];s=0
    for values in itertools.product((0,1),repeat=len(free)):
        a=dict(p);a.update(zip(free,values))
        s+=all(any(a[abs(z)]==int(z>0) for z in c) for c in F)
    return s
A={2:1,3:0,5:1,6:0,8:0};B={2:0,3:1,5:1,6:1,8:0};R={1:1,7:0}
assert count({})==70 and count(A)==count(B)==4
assert count(A|R)==0 and count(B|R)==1
run=subprocess.run([sys.executable,str(pathlib.Path(__file__).with_name('compact317.py'))],
                   capture_output=True,text=True,check=True)
out=json.loads(run.stdout)
assert out['A']['labels'][-1]=='UNSAT' and out['B']['labels'][-1]=='SAT'
for side in ('A','B'):
    assert out[side]['early_buckets']<out[side]['eager_buckets']
checks=0
for i in range(12):
 for j in range(i+1,12):
  for ea,eb in itertools.product((0,1),repeat=2):
   need={};feasible=True
   for clause,e in ((F[i],ea),(F[j],eb)):
    for z in clause:
     x=abs(z);want=int(z>0) if e else int(z<0)
     if x in need and need[x]!=want:feasible=False
     need[x]=want
   same=any(z in F[j] for z in F[i]);opp=any(-z in F[j] for z in F[i])
   assert feasible==(not opp if ea==eb else not same)
   checks+=1
print(json.dumps({'status':'PASS','independent_original_source':True,
                  'F9_signed_SU_modes':checks,'A_R_count':0,'B_R_count':1,'P_vs_NP':'OPEN'},indent=2))
