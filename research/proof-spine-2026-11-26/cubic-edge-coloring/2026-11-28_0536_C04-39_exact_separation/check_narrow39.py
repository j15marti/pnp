"""Independent exact verifier for the two-parent boundary exclusion."""
import itertools as it,json,sys
from pathlib import Path
from verify_compact36 import reconstruct,J,H

def check(raw,cert):
 C=json.loads(cert);i='STRICT-EB4-v1:sha256:'+H(raw);assert C['instance_id']==i and C['original_N_bits']==8*len(raw)
 F,M,_=reconstruct(raw);ch,mh,gh=H(J(F)),H(J(M)),H(J([[10,0]]));assert (ch,mh,gh)==(C['chart_sha256'],C['map_sha256'],C['guard_sha256']);g='GUARD-v1:sha256:'+H(J(['PNP-GUARD-v1',i,'EB-PORT-PINS-v1',gh]));assert C['guard_id']==g and C['residual_id']=='RESIDUAL-v1:sha256:'+H(J(['PNP-RESIDUAL-v1',i,g,'FP51-ENERGY-TABLE-v1',ch,mh]))
 E=C['export'];V=E['boundary'];bad=E['bad'];owners=set();ps=[];total={};domains=[];checks=0
 def allowed(h,I):return all(F[k]['cost'][sum(h[v]<<j for j,v in enumerate(F[k]['vs']))]==0 for k in I)
 for S,P in zip(E['regions'],E['polynomials']):
  I=[k for k,f in enumerate(F) if set(f['vs'])<=set(S)];owners.update(o for k in I for o in F[k]['ids']);domains.append(I);Q={tuple(T):c for T,c in P};assert len(Q)==len(P) and all(set(T)<=set(S) for T in Q)
  for T,c in Q.items():total[T]=total.get(T,0)+c
  rows=[]
  for z in range(1<<len(S)):
   h={v:z>>j&1 for j,v in enumerate(S)};checks+=1
   if allowed(h,I):assert sum(c for T,c in Q.items() if all(h[v] for v in T))>=0;rows.append(z)
  ps.append(rows)
 assert sorted(owners)==E['owner_ids'];total={T:c for T,c in total.items() if c};assert set(v for T in total for v in T)==set(V);h=dict(zip(V,bad));assert sum(c for T,c in total.items() if all(h[v] for v in T))<0
 for S,z,R in zip(E['regions'],E['parent_extensions'],ps):assert z in R and all(z>>S.index(v)&1==b for v,b in zip(V,bad) if v in S)
 U=sorted(set().union(*map(set,E['regions'])));count=0;I=sorted(set().union(*map(set,domains)))
 for z in it.product((0,1),repeat=len(U)):
  h=dict(zip(U,z));checks+=1
  if allowed(h,I):count+=1;assert any(h[v]!=b for v,b in zip(V,bad))
 assert count==E['joint_support_size'];return {'certificate_sha256':H(cert),'enumerated_assignments':checks,'joint_support':count,'owners':len(owners),'status':'checked guarded exclusion'}
if __name__=='__main__':print(check(*(Path(p).read_bytes() for p in sys.argv[1:])))
