"""Deterministic PHP SAT/UNSAT, signed occurrence, Tseitin, syntax, pivot controls.
These are finite independent encoding tests, NOT minimum-proof enumeration.
"""
import itertools, json
def php(h):
 def x(i,j):return 1+i*h+j
 return [[x(i,j) for j in range(h)] for i in range(h+1)]+[
  [-x(i,j),-x(k,j)] for j in range(h) for i in range(h+1) for k in range(i+1,h+1)]
def model(F,n):
 for bits in itertools.product((0,1),repeat=n):
  if all(any(bits[abs(l)-1]==(l>0) for l in C) for C in F):return bits
 return None
def proper(C):return len(set(C))==len(C) and all(-a not in C for a in C)
out=[]
for h in [1,2,3]:
 F=php(h);n=h*(h+1);assert model(F,n) is None
 num=0
 for j,C in enumerate(F):
  assert model(F[:j]+F[j+1:],n) is not None
  for k in range(len(C)):
   alt=C.copy();alt[k]=-alt[k]
   assert model(F[:j]+[alt]+F[j+1:],n) is not None;num+=1
 out.append({'holes':h,'vars':n,'sources':len(F),'deletions_sat':len(F),'signed_flips_sat':num})
edges=list(itertools.combinations(range(4),2))
def tseitin(charges):
 F=[]
 for u in range(4):
  idx=[j for j,e in enumerate(edges) if u in e]
  for signs in itertools.product((0,1),repeat=3):
   if sum(signs)%2==charges[u]:continue
   F.append([-(i+1) if s else i+1 for i,s in zip(idx,signs)])
 return F
def count(F,n):
 return sum(all(any(bits[abs(l)-1]==(l>0) for l in C) for C in F)
            for bits in itertools.product((0,1),repeat=n))
assert count(tseitin([1,0,0,0]),6)==0
assert count(tseitin([0,0,0,0]),6)==8
def parse(src):
 lines=src.strip().splitlines()
 hh=lines[0].split();assert len(hh)==4 and hh[:2]==['p','cnf']
 n=int(hh[2]);m=int(hh[3]);assert n>=0 and len(lines)-1==m
 for line in lines[1:]:
  C=list(map(int,line.split()));assert C and C[-1]==0 and 0 not in C[:-1]
  assert proper(C[:-1]) and all(abs(l)<=n for l in C[:-1])
for bad in ['p cnf 2 1\n1 0\n2 0\n','p cnf 2 1\n1 3 0\n',
            'p cnf 2 1\n1 -1 0\n','p cnf X 1\n1 0\n']:
 try:parse(bad)
 except (AssertionError,ValueError):pass
 else:raise AssertionError('malformed accepted')
result={'status':'PASS','php':out,'odd_k4_models':0,'even_k4_models':8,
        'malformed_rejections':4,'scope':'finite signed source controls only'}
print(json.dumps(result,indent=2))
