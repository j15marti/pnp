"""Convert a pinned C04-36 compact certificate into a canonical monomial certificate."""
import json,base64,zlib,itertools as it,collections as co,sys
from pathlib import Path
from fractions import Fraction
from verify_compact36 import reconstruct,verify,J,H

def transport(raw,old):
 C=json.loads(old);verify(raw,old);F,M,_=reconstruct(raw);S=[set(q['vs']) for q in F];scopes={tuple(sorted(s)) for s in S}
 for A,B in it.combinations(S,2):
  if A&B and len(A|B)<=5:scopes.add(tuple(sorted(A|B)))
 scopes=sorted(scopes,key=lambda x:(len(x),x));Y={i:Fraction(x,y) for i,x,y in json.loads(zlib.decompress(base64.b64decode(C['dual_b64'])))}
 W=co.defaultdict(lambda:co.defaultdict(Fraction));ref={};row=0
 for V in scopes:
  if row in Y:W[V][()]+=Y.pop(row)
  row+=1
  for k in range(1,len(V)+1):
   for T in it.combinations(V,k):
    if T not in ref:ref[T]=V;continue
    B=ref[T]
    for z in range(2**k):
     if row in Y:
      c=Y.pop(row);pos=[x for j,x in enumerate(T) if z>>j&1];neg=[x for j,x in enumerate(T) if not(z>>j&1)]
      for h in range(len(neg)+1):
       for Z in it.combinations(neg,h):
        A=tuple(sorted(pos+list(Z)));v=c*(-1)**h;W[V][A]+=v;W[B][A]-=v
     row+=1
 assert not Y
 P=[[list(V),[[list(T),c.numerator,c.denominator] for T,c in sorted(Q.items()) if c]] for V,Q in sorted(W.items()) if any(Q.values())]
 meta={k:C[k] for k in ('problem_id','instance','instance_id','original_N_bits','source_pin','guard_id','residual_id','original_ids','chart_sha256','map_sha256','guard_sha256')}
 return J(dict(meta,parents=['CERT-v1:sha256:'+H(old)],claim='Exact monomial-basis transport of independently replayed C04-36 regional dual; not a new source-only refutation.',regional_polynomials=P))
if __name__=='__main__':
 raw,old=[Path(p).read_bytes() for p in sys.argv[1:3]];out=transport(raw,old);Path(sys.argv[3]).write_bytes(out);print(H(out))
