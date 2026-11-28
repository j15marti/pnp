"""Exact rational verification of regional polynomial cancellation, no LP solver."""
import json,hashlib,itertools as it,collections as co,sys,math
from fractions import Fraction
from pathlib import Path
from verify_compact36 import reconstruct,J,H

def check(raw,cert):
 C=json.loads(cert);instance='STRICT-EB4-v1:sha256:'+H(raw);assert C['instance_id']==instance and C['original_N_bits']==8*len(raw)
 F,M,pre=reconstruct(raw);ch,mh,gh=H(J(F)),H(J(M)),H(J([[10,0]]));assert (ch,mh,gh)==(C['chart_sha256'],C['map_sha256'],C['guard_sha256']);g='GUARD-v1:sha256:'+H(J(['PNP-GUARD-v1',instance,'EB-PORT-PINS-v1',gh]));assert g==C['guard_id'];assert C['residual_id']=='RESIDUAL-v1:sha256:'+H(J(['PNP-RESIDUAL-v1',instance,g,'FP51-ENERGY-TABLE-v1',ch,mh]))
 total=co.defaultdict(Fraction);checks=rows=0;seen=set();terms=0;maxbits=0
 for V,P in C['regional_polynomials']:
  assert tuple(V)==tuple(sorted(set(V))) and tuple(V) not in seen and len(V)<=8;seen.add(tuple(V));S=set(V);I=[i for i,q in enumerate(F) if set(q['vs'])<=S];assert S=={x for i in I for x in F[i]['vs']};p={}
  for T,a,b in P:
   assert b>0 and a and tuple(T)==tuple(sorted(set(T))) and set(T)<=S and tuple(T) not in p
   p[tuple(T)]=Fraction(a,b);total[tuple(T)]+=p[tuple(T)];terms+=1;maxbits=max(maxbits,abs(a).bit_length(),b.bit_length())
  for z in it.product((0,1),repeat=len(V)):
   h=dict(zip(V,z))
   for i in I:
    q=F[i];checks+=1
    if q['cost'][sum(h[x]<<j for j,x in enumerate(q['vs']))]:break
   else:
    rows+=1;checks+=len(p);assert sum((c for T,c in p.items() if all(h[x] for x in T)),Fraction())>=0
 assert total[()]<0 and all(not c for T,c in total.items() if T)
 return dict(status='UNSAT',regions=len(seen),terms=terms,allowed_rows=rows,checks=checks,projection_checks=pre,max_coefficient_bits=maxbits,constant=str(total[()]),certificate_sha256=H(cert))
if __name__=='__main__':print(check(*(Path(x).read_bytes() for x in sys.argv[1:])))
