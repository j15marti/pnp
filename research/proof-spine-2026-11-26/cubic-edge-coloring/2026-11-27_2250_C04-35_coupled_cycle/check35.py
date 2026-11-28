"""Standalone independent verifier for coupled-cycle CNF certificates (no solver imports)."""
import sys,json,hashlib,itertools as it,collections as co
from pathlib import Path

def generate(m,d,odd):
 n=2*m+d*m+1;C=[]
 for j in range(2):
  for i in range(m):
   V=[j*m+i+1,j*m+(i+1)%m+1]+list(range(2*m+i*d+1,2*m+(i+1)*d+1))+([n] if j else [])
   for z in it.product((0,1),repeat=len(V)):
    b=int(all(z[2:2+d]))*(z[-1] if j else 1)^int(odd and j==1 and i==0)
    if z[0]^z[1]!=b:C.append(tuple(-v if k else v for v,k in zip(V,z)))
 return (f'p cnf {n} {len(C)}\n'+''.join(' '.join(map(str,q))+' 0\n' for q in C)).encode()

def check(raw,cert):
 assert cert['instance_id']=='DIMACS-CNF-v1:sha256:'+hashlib.sha256(raw).hexdigest()
 assert cert['original_N_bits']==8*len(raw) and cert['guard_id']=='EMPTY' and cert['residual_id']=='ROOT'
 lines=raw.decode('ascii').splitlines();_,_,n,m=lines[0].split();n,m=int(n),int(m);C=[tuple(map(int,l.split()[:-1])) for l in lines[1:]]
 assert len(C)==m and cert['original_ids']=={'variables':[1,n],'clauses':[1,m]}
 assert raw==generate(**cert['generator'])
 G={}
 for q in C:
  V=tuple(sorted(map(abs,q)));assert len(V)==len(set(V));G.setdefault(V,[]).append(q)
 polys=[];rows=[];checks=0
 for V,Q in G.items():
  W=[sum(1<<(v-1) for j,v in enumerate(V) if a>>j&1) for a in range(1<<len(V))];bad=[]
  for w in W:
   val=[not any(bool(w>>(abs(l)-1)&1)==(l>0) for l in q) for q in Q];checks+=len(Q);assert sum(val)<=1;bad.append(int(any(val)))
  M=set()
  for u in range(len(W)):
   t=u;b=0
   while True:
    checks+=1;b^=bad[t]
    if not t:break
    t=(t-1)&u
   if b:M.add(W[u])
  polys.append(M);rows.append((sum(1<<(v-1) for v in V),[w for w,b in zip(W,bad) if not b]))
 P=[];ids=[]
 for row in cert['proof']['components']:
  A=set();ids+=row['factors']
  for i in row['factors']:A.symmetric_difference_update(polys[i])
  assert A==set(row['poly']);P.append(A)
 assert sorted(ids)==list(range(len(polys))) and len(P)==2
 z=1<<(cert['proof']['multiplier']-1);A=set(P[1])
 for u in P[0]:A.symmetric_difference_update({u|z})
 assert A=={0}
 # Independently check pairwise normalized marginals on all intersections.
 pairs=0
 for i,(S,R) in enumerate(rows):
  assert R
  for T,Q in rows[:i]:
   I=S&T
   if not I:continue
   pairs+=1;a=co.Counter(w&I for w in R);b=co.Counter(w&I for w in Q)
   for w in a.keys()|b.keys():checks+=1;assert a[w]*len(Q)==b[w]*len(R)
 # Gaussian test, constant not in original unmultiplied rowspace.
 K=sorted({0}|set().union(*polys));pos={v:i for i,v in enumerate(K)};B={}
 for M in polys:
  x=sum(1<<pos[u] for u in M)
  while x:
   k=x.bit_length()-1
   if k in B:x^=B[k]
   else:B[k]=x;break
 x=1<<pos[0]
 while x and x.bit_length()-1 in B:x^=B[x.bit_length()-1]
 assert x
 assert [i+1 for i,q in enumerate(C) if all(l>0 for l in q)]==[cert['proof']['one_defect_clause']]
 return {'status':'NO','minimum_violated_clauses':1,'pair_checks':pairs,'local_checks':checks,'rank':len(B)}
if __name__=='__main__':
 raw=Path(sys.argv[1]).read_bytes();cert=Path(sys.argv[2]).read_bytes();print('CERT-v1:sha256:'+hashlib.sha256(cert).hexdigest(),check(raw,json.loads(cert)))
