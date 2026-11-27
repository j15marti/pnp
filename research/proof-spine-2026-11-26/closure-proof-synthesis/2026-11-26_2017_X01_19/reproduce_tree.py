"""Reproduce X01-19 central tree experiment on source.json, Python 3 stdlib only.
Source closure itself is checked by the separate full archive verifier.
"""
from pathlib import Path
import json,hashlib,itertools as it
from collections import defaultdict
P=Path(__file__).resolve().parent
x=json.load(open(P/'source.json'));q,T,L=x['q'],x['T'],x['live_ids']
assert hashlib.sha256(json.dumps({k:x[k] for k in ('q','T','guard')},separators=(',',':')).encode()).hexdigest()=='f2f17606f508eb8644f36634a32291fbdc84a121043eb4b0f44c76b4c5d19aeb'
assert not x['chosen_ids'] and not set(L)&set(x['guard'])
def basis(A):
 B={}
 for a in A:
  while a:
   k=a.bit_length()-1
   if k not in B:B[k]=a;break
   a^=B[k]
 return B
def inspan(a,B):
 while a:
  k=a.bit_length()-1
  if k not in B:return False
  a^=B[k]
 return True

def solve(c,mode='rank',cap=2000000):
 d,e=[v for v in range(3) if v!=c];G={v:[i for i in L if T[i][c]==v] for v in range(q)};z={i:(1<<T[i][d])|(1<<(q+T[i][e])) for i in L};target=(1<<(2*q))-1
 D={}
 for v,ids in G.items():
  b=z[ids[0]];target^=b;D[v]=[z[i]^b for i in ids]
 U=set(G);R=len(basis(a for v in U for a in D[v]));B={};rank_calls=0
 def span(S):
  nonlocal rank_calls
  key=frozenset(S)
  if key not in B:B[key]=basis(a for v in key for a in D[v]);rank_calls+=1
  return B[key]
 def width(S):return len(span(S))+len(span(U-S))-R
 if not inspan(target,span(U)):return dict(count=0,work=0,peak=0,width=0)
 nodes=[(frozenset([v]),v) for v in sorted(U)];trace=[];w=max(width(s) for s,_ in nodes)
 while len(nodes)>1:
  # combine by smallest outside intersection, then smaller product leaf size and deterministic ID tie break
  i,j=min(it.combinations(range(len(nodes)),2),key=lambda ij:(width(nodes[ij[0]][0]|nodes[ij[1]][0]),len(nodes[ij[0]][0]|nodes[ij[1]][0]),ij))
  A,a=nodes[i];C,b=nodes[j];S=A|C;w=max(w,width(S));nodes=[n for k,n in enumerate(nodes) if k not in (i,j)]+[(S,[a,b])]
 work=0;peak=0
 def f(tree):
  nonlocal work,peak
  if isinstance(tree,int):S=frozenset([tree]);X={0:1};Y=defaultdict(int)
  else:
   A,X=f(tree[0]);C,Y=f(tree[1]);S=A|C
  if isinstance(tree,int):
   for a in D[tree]:Y[a]+=1
  out=defaultdict(int);outside=span(U-S);support=0
  for a in outside.values():support|=a
  for a,na in X.items():
   for b,nb in Y.items():
    work+=1
    if work>cap:raise OverflowError
    s=a^b;r=target^s
    if r&~support or (mode=='rank' and not inspan(r,outside)):continue
    out[s]+=na*nb
  peak=max(peak,len(out));trace.append([sorted(S),width(S),len(out)])
  if mode=='rank':assert len(out)<=1<<width(S)
  return S,out
 try:
  _,F=f(nodes[0][1]);count=F.get(target,0)
 except OverflowError:count=None
 return dict(count=count,work=work,peak_single_table=peak,width=w,rank_calls=rank_calls,tree=nodes[0][1],trace=trace)
if __name__=='__main__':
 out={}
 for c in range(3):
  for mode in ('coordinate','rank'):
   z=solve(c,mode);out[f'{c}_{mode}']=z;print(c,mode,{k:v for k,v in z.items() if k not in ('tree','trace')},flush=True);assert z['count'] in (0,None)
 json.dump(out,open(P/'tree_reproduced.json','w'),indent=2)
