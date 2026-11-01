#!/usr/bin/env python3
"""ARC FOUR-CORE287 compact independent replay. stdlib, exact finite loops.
Run at repository root: python experiments/arc/lspv1_287/check_four_core287.py
Scope: bounded monotone residuals, not all-input SAT/FLMV lower bounds.
"""
import ast, collections, itertools, pathlib, json
from math import comb
P=pathlib.Path(__file__).resolve()
ROOT=P.parents[3] if 'experiments' in str(P) else P.parent
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
K=((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(-1,-5,-9),(-1,-6,-8),(-2,-4,-9),(-2,-6,-7),(-3,-4,-8),(-3,-5,-7))
Q=((1,2),(-1,-2),(2,3),(-2,-3),(1,3),(-1,-3))
W='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'
TEMPLATES={'A':((1,),(2,),(3,),(-1,-2,-3)),
           'B':((1,),(2,3),(-1,-2),(-1,-3)),
           'C':((1,),(-2,),(2,3),(-1,-3))}
def mask(c,n):
 return sum(1<<a for a in range(1<<n) if any(bool(a>>(abs(l)-1)&1)==(l>0) for l in c))
def catalogue(n,unitfree=False,k=4):
 cc=[tuple(s*i for i in v) for width in ((2,3) if unitfree else (1,2,3))
      for v in itertools.combinations(range(1,n+1),width) for s in (1,-1)]
 masks=[mask(c,n) for c in cc];N=0;ans=[]
 for ix in itertools.combinations(range(len(cc)),k):
  N+=1
  m=(1<<(1<<n))-1
  for i in ix:m &= masks[i]
  if m:continue
  if not unitfree and k==4 and not all(__import__('functools').reduce(lambda a,j:a & masks[j], (j for j in ix if j!=t), (1<<(1<<n))-1) for t in ix):continue
  ans.append(tuple(cc[i] for i in ix))
 return N,ans
def canon(f):
 vs=sorted(set(abs(l) for c in f for l in c));out=[]
 if len(vs)>3:return None
 for p in itertools.permutations(range(1,len(vs)+1)):
  ren=dict(zip(vs,p))
  for sign in (1,-1):
   out.append(tuple(sorted(tuple(sorted(sign*(1 if l>0 else -1)*ren[abs(l)] for l in c)) for c in f)))
 return min(out)
def valid(F,n):
 if 3*len(F)!=4*n:return False
 seen=set();degrees=collections.Counter()
 for c in F:
  if len(c)!=3 or len({abs(x) for x in c})!=3 or not(all(x>0 for x in c) or all(x<0 for x in c)) or any(abs(x)>n for x in c):return False
  key=tuple(sorted(c))
  if key in seen:return False
  seen.add(key)
  for x in c:degrees[abs(x),x>0]+=1
 return all(degrees[x,sgn]==2 for x in range(1,n+1) for sgn in (0,1))
def sat(F,n):
 return sum(all(any(bool(a>>(abs(x)-1)&1)==(x>0) for x in c) for c in F) for a in range(1<<n))
def res(F,p):
 return [(i,tuple(l for l in c if p[abs(l)-1]<0)) for i,c in enumerate(F)
         if not any(p[abs(l)-1]==int(l>0) for l in c)]
def certificate_U(U):
 mods=[]
 for i in range(6):
  V=set(range(1+32*i,33+32*i))
  G=[c for c in U[2:254] if any(abs(l) in V for l in c)]
  assert len(G)==42 and all(all(abs(l) in V or abs(l)>=193 for l in c) for c in G)
  mods.append(G)
 def dpll(G):
  while 1:
   if not G:return True
   if any(not c for c in G):return False
   lit=next((c[0] for c in G if len(c)==1),None)
   if lit is None:break
   G=tuple(tuple(x for x in c if x!=-lit) for c in G if lit not in c)
  lit=G[0][0]
  return any(dpll(tuple(tuple(x for x in c if x!=-v) for c in G if v not in c)) for v in (lit,-lit))
 allrows=0;calls=0
 for vals in itertools.product((False,True),repeat=6):
  a=dict(zip(range(193,199),vals));allrows+=1
  if any(all(a[abs(l)]!=(l>0) for l in c) for c in U[:2]):continue
  failed=False
  for M in mods:
   H=tuple(tuple(l for l in c if abs(l)<=192) for c in M if not any(abs(l)>=193 and a[abs(l)]==(l>0) for l in c))
   calls+=1
   if not dpll(H):failed=True;break
  assert failed
 assert allrows==64 and calls==152
 return (allrows,calls)
def main():
 n,cores=catalogue(3);assert n==1001 and len(cores)==14
 C=collections.Counter({v:0 for v in TEMPLATES})
 norms={canon(v):k for k,v in TEMPLATES.items()}
 for f in cores:
  assert canon(f) in norms
  C[norms[canon(f)]]+=1
 assert dict(C)=={'A':2,'B':6,'C':6}
 n5,cores5=catalogue(5);assert n5==230300 and len(cores5)==140
 assert all(canon(f) in norms for f in cores5)
 nf,bad=catalogue(4,True,5);assert nf==15504 and not bad
 assert not (mask(Q[0],3)&mask(Q[1],3)&mask(Q[2],3)&mask(Q[3],3)&mask(Q[4],3)&mask(Q[5],3))
 assert all(__import__('functools').reduce(lambda a,c:a & mask(c,3),Q[:i]+Q[i+1:],(1<<8)-1) for i in range(6))
 assert valid(Y,6) and valid(K,9) and sat(Y,6)==20 and sat(K,9)==18
 p=(-1,0,1,0,-1,-1,0,1,1);G=res(K,p)
 assert [j for j,c in G]==[1,3,6,7]
 assert [c for j,c in G]==[(5,6),(1,),(-1,-5),(-1,-6)]
 assert canon([c for j,c in G])==canon(TEMPLATES['B'])
 assert all(__import__('functools').reduce(lambda a,c:a & mask(c,9),[G[j][1] for j in range(4) if j!=i],(1<<512)-1) for i in range(4))
 assert all((not all(any(bool(a>>(abs(l)-1)&1)==(l>0) for l in c) for c in K)) or any(bool(a>>(abs(l)-1)&1)==(l>0) for l in (4,7,-8,-9)) for a in range(1<<9))
 fixture=ROOT/'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt'
 if not fixture.exists():fixture=P.parent/'DOECKER61_original_source.txt'
 s=fixture.read_text();U=tuple(tuple(x) for x in ast.literal_eval(s[s.index('[['):]))
 V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2];V=tuple(tuple(c) for c in V)
 assert valid(U,198) and valid(V,198) and len(W)==198
 assert all(any((W[abs(x)-1]=='1')==(x>0) for x in c) for c in V)
 cert=certificate_U(U)
 out={'status':'PASS','four_catalogue_3vars_1001':dict(C),'four_catalogue_5vars_230300':len(cores5),
      'unitfree_5clauses_15504_all_SAT':True,'six_clause_UP_stall_UNSAT':True,
      'canonical_K33_four_core_original_indices':[j for j,c in G],
      'canonical_K33_SAT_models':18,'U198_UNSAT_boundary_rows':cert[0],
      'U198_UNSAT_module_calls':cert[1],'V198_SAT_witness':True,
      'P_vs_NP':'OPEN','full_FLVM_native_work_tape_tracing':'NOT PERFORMED'}
 print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':main()
