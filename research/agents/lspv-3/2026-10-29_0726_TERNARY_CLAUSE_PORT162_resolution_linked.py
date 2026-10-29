from collections import Counter
import runpy,json
from pathlib import Path
base=runpy.run_path(str(Path(__file__).with_name('2026-10-29_0726_LSPV-3_TERNARY_CLAUSE_PORT162_repro.py')))
G=base['make_chain'](2)
orig=[tuple(sorted(c,key=lambda x:(abs(x),x))) for c in G]+[(1,),(2,),(-13,)]
current={frozenset(x):i+1 for i,x in enumerate(orig)}
ledger={i+1:{'clause':tuple(x),'source':i+1} for i,x in enumerate(orig)}
nxt=len(orig)+1
order=[]
for iter in range(45):
 if frozenset() in current:break
 vs={abs(l) for cl in current for l in cl}
 if not vs:break
 def cost(v):
  P=[cl for cl in current if v in cl];N=[cl for cl in current if -v in cl]
  return (len(P)*len(N),len(P)+len(N),v)
 v=min(vs,key=cost);order.append((v, cost(v)[0],len(current)))
 P=[(cl,id) for cl,id in current.items() if v in cl];N=[(cl,id) for cl,id in current.items() if -v in cl]
 after={cl:id for cl,id in current.items() if v not in cl and -v not in cl}
 for a,ai in P:
  for b,bi in N:
   r=(a-{v})|(b-{-v})
   if any(-l in r for l in r):continue
   if any(x.issubset(r) for x in after):continue
   for old in list(after):
    if r.issubset(old):del after[old]
   if frozenset(r) not in after:
    id=nxt;nxt+=1
    after[frozenset(r)]=id
    ledger[id]={'clause':tuple(sorted(r,key=lambda x:(abs(x),x))),'parents':[ai,bi],'pivot':v}
 current=after
 print('eliminate',v,'clauses',len(current),'steps',len(ledger))
 if not current:break
print('order',order,'proof length',len(ledger)-len(orig),'empty step',current.get(frozenset()))
if frozenset() in current:
 def closure(id):
  d={id}; q=[id]
  while q:
   z=ledger[q.pop()]
   for par in z.get('parents',[]):
    if par not in d:d.add(par);q.append(par)
  return d
 cl=closure(current[frozenset()]);used={id:rec for id,rec in ledger.items() if id in cl}
 print('used proof steps',sum('parents' in x for x in used.values()),'used sources',sum('source' in x for x in used.values()))
 with open(Path(__file__).with_name('2026-10-29_0726_TERNARY_CLAUSE_PORT162_resolution.json'),'w') as f:json.dump({'orig':orig,'lines':used,'empty_id':current[frozenset()],'order':order,'total_steps_generated':len(ledger)-len(orig)},f,indent=2)
