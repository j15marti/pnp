#!/usr/bin/env python3
"""Independent original-clause source-indexed extreme controls and coherent flips.
All XOR is offline logical diagnostic, never free to the solver or a physical
write bound. Correctness uses coherent source variables, not occurrence bits.
"""
import json,gzip,ast,hashlib
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
P=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
Q=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P+tuple(tuple(-v for v in c) for c in Q)
from itertools import combinations
P5=((1,2),(2,3),(3,4),(4,5),(1,5))
Q5=tuple(e for e in combinations(range(1,6),2) if e not in P5)
K5=tuple((u,v,6+i) for i,(u,v) in enumerate(P5))+tuple((-u,-v,-11-i) for i,(u,v) in enumerate(Q5))+tuple((6+i,11+i,11+(i+1)%5) for i in range(5))+tuple((-(11+i),-(6+i),-(6+(i+1)%5)) for i in range(5))
U=tuple(map(tuple,ast.literal_eval(''.join(s for s in (R/'U198.txt').read_text().splitlines() if not s.startswith('#')))))
V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2];V=tuple(map(tuple,V))

def truth(c,a):return sum(a[abs(l)]==int(l>0) for l in c)
def gr(x):return (0,1,3,2)[x]
def work(name,F):
 n=max(abs(l) for c in F for l in c)
 a={v:0 for v in range(1,n+1)};zero=[truth(c,a) for c in F]
 b={v:1 for v in range(1,n+1)};one=[truth(c,b) for c in F]
 assert all(x+y==3 for x,y in zip(zero,one))
 out={'source':name,'n':n,'m':len(F),'clauses':[],'pair_extreme':[],'coherent_flip_trail':[],
      'zero_hist':[zero.count(t) for t in range(4)],'one_hist':[one.count(t) for t in range(4)]}
 for j,c in enumerate(F):
  s=[(abs(l),int(l>0)) for l in c];u=[(v,1-t) for v,t in s]
  out['clauses'].append({'id':j,'signed_literals':list(c),
    'S_occurrence_targets':s,'inverted_S_equals_U':u,
    'U_occurrence_targets':u,'inverted_U_equals_S':s})
 for j,c in enumerate(F):
  for k in range(j+1,len(F)):
   d=F[k];sames=any(l in d for l in c);opps=any(-l in d for l in c)
   modes=[int(not opps),int(not sames),int(not sames),int(not opps)]
   out['pair_extreme'].append([j,k,*modes])
 # Global complete-assignment trace. First 12 forward and reverse flips + final
 # endpoints are emitted; every intermediate state is computed/charged offline.
 t=list(zero);dlogic=0;steps=0;changed=[]
 incidence={v:[j for j,c in enumerate(F) if any(abs(l)==v for l in c)] for v in range(1,n+1)}
 for v in range(1,n+1):
  old={j:t[j] for j in incidence[v]}
  a[v]=1
  for j in incidence[v]:t[j]=truth(F[j],a)
  xor=1+sum((gr(old[j])^gr(t[j])).bit_count() for j in incidence[v])
  assert xor==5 and all(abs(t[j]-old[j])==1 for j in incidence[v])
  dlogic+=xor;steps+=1
  if steps<=12 or steps==n:
   out['coherent_flip_trail'].append({'step':steps,'variable':v,'changed_original_clause_ids':incidence[v],
       'gray_logic_xor':xor,'histogram':[t.count(q) for q in range(4)]})
 assert t==one and dlogic==5*n
 out['full_forward_gray_logic_xor_total']=dlogic
 out['coherent_flips_all']=n
 return out

def main():
 path=R/'signed_controls296.json.gz';count=0;paircount=0;records={}
 with gzip.open(path,'wt') as f:
  for name,F in [('F9',F9),('Y6',Y),('F15',F15),('K5',K5),('U198',U),('V198',tuple(V))]:
   out=work(name,F)
   f.write(json.dumps(out,separators=(',',':'))+'\n')
   records[name]={'clauses':out['m'],'pairs':len(out['pair_extreme']),
                  'zeros':out['zero_hist'],'ones':out['one_hist'],
                  'global_gray_xor':out['full_forward_gray_logic_xor_total']}
   count+=out['m'];paircount+=len(out['pair_extreme'])
 raw={'clauses':count,'pairs':paircount,'sources':records,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 (R/'signed_controls_summary295.json').write_text(json.dumps(raw,indent=2,sort_keys=True)+'\n')
 print(json.dumps(raw,indent=2))
if __name__=='__main__':main()
