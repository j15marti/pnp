from itertools import product
import json, hashlib
from pathlib import Path
allowed={frozenset((i,(i+1)%5,(i+2)%5)) for i in range(5)}
def C(a,b,c): return len({a,b,c})==3 and frozenset((a,b,c)) in allowed
def enc(bits):
 k=len(bits); n=8*k; m=2*k; w=n.bit_length()
 g=bin(m+1)[2:]; head='1'*n+'0'+'0'*(len(g)-1)+g
 clauses=[]
 for j,b in enumerate(bits): clauses.extend([(8*j+1,8*j+2,8*j+3),(8*j+1,8*j+2,8*j+3+4*b)])
 assert all(len(set(t))==3 and all(1<=i<=n for i in t) for t in clauses)
 return head+''.join(format(i,f'0{w}b') for t in clauses for i in t)
# Full eight-variable enumeration, including all unused variables.
local=[]
for b in (0,1):
 z=sum(C(v[0],v[1],v[2]) and C(v[0],v[1],v[2+4*b]) for v in product(range(5),repeat=8))
 local.append(z)
assert local==[93750,31250]
rows=[]
for k in range(1,11):
 zero=enc([0]*k); pos=[]
 for j in range(k):
  bits=[0]*k;bits[j]=1
  diff=[i for i,(a,b) in enumerate(zip(zero,enc(bits))) if a!=b]
  assert len(diff)==1;pos+=diff
 assert len(set(pos))==k
 for bits in product((0,1),repeat=k):
  encoded=enc(bits); z=1
  for b in bits:z*=local[b]
  expected=31250**k*3**(k-sum(bits))
  assert z==expected and (z>>(k+1))&1==(k-sum(bits))%2
  assert all(encoded[p]==str(b) for p,b in zip(pos,bits))
  assert all(encoded[i]==zero[i] for i in range(len(zero)) if i not in pos)
  rows.append({'k':k,'bits':''.join(map(str,bits)),'N':len(encoded),'count':str(z),'bit':(z>>(k+1))&1})
result={'status':'PASS','local_full_assignments':2*5**8,'local_counts':local,'encoded_cases':len(rows),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'rows':rows}
Path('bounds_t5_run').mkdir(exist_ok=True)
Path('bounds_t5_run/raw.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
