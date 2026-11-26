from audit import *
O=list(I.product(range(2),repeat=3)); out={'octahedron':test(O,2,2),'V_full':test(V,3,3)}
T=ring(16);out['ring16']=test(T,48,1)
T=ring(8);S=close(T,24);W=run(T,24,0,1,1)['witness'];j=next(j for j in S if j not in W);out['ring8_sat_deleted']=test([t for i,t in enumerate(T) if i!=j],24,1);out['ring8_sat_deleted']['deleted']=[j]
for c,i in [(c,i) for c in range(3) for i in range(24)]:
 for d,l in [(d,l) for d in range(3) for l in range(24) if d!=c]:
  for a,b in I.product([j for j,t in enumerate(T) if t[c]==i],[j for j,t in enumerate(T) if t[d]==l]):
   if a==b or not any(T[a][q]==T[b][q] for q in range(3)):continue
   S=[t for j,t in enumerate(T) if (t[c]!=i or j==a) and (t[d]!=l or j==b)]
   if T[a] in S and T[b] in S and all(len({t[q] for t in S})==24 for q in range(3)):
    out['ring8_unsat_deleted']=test(S,24,1);out['ring8_unsat_deleted']['deleted']=[i for i,t in enumerate(T) if t not in S];break
  if 'ring8_unsat_deleted' in out:break
 if 'ring8_unsat_deleted' in out:break
print(json.dumps(out,indent=2))
