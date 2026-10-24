#!/usr/bin/env python3
"""Compact independent M22 total-anchor grammar audit; Python stdlib only.
No general-SAT complexity lower bound or machine-level FLMV trace claimed.
"""
import itertools, collections, json, random
Yp=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
Yq=((1,2,4),(1,3,6),(2,3,5),(4,5,6))
Y=tuple((0,)+t for t in Yp)+tuple((1,)+t for t in Yq)
def put(n,b):return format(n,'0%db'%b)
def encode(k,records):
 w=k.bit_length();m=len(records)
 return '1'*w+'0'+put(k,w)+put(m,w+1)+''.join(str(s)+put(a,w)+str(s)+put(b,w)+str(s)+put(c,w) for s,a,b,c in records)
def parse(x):
 N=len(x);w=0
 while w<min(N,N.bit_length()+2) and x[w]=='1':w+=1
 if w==0 or w==N or w>N.bit_length()+1:return None
 h=3*w+2
 if N<h:return None
 k=int(x[w+1:2*w+1],2);m=int(x[2*w+1:3*w+2],2)
 if k.bit_length()!=w or k<6 or k%3 or m!=4*k//3 or N!=h+3*m*(w+1):return None
 return (k,m,w,h)
def grammar(x):
 p=parse(x)
 if p is None:return None
 k,m,w,h=p;plus=collections.Counter();minus=collections.Counter();seen=set();rows=[]
 for j in range(m):
  b=h+3*j*(w+1);s=[];v=[]
  for i in range(3):
   z=b+i*(w+1);s.append(int(x[z]));v.append(int(x[z+1:z+w+1],2))
  if len(set(s))!=1 or not 1<=v[0]<v[1]<v[2]<=k:return None
  r=(s[0],)+tuple(v)
  if r in seen:return None
  seen.add(r);rows.append(r)
  (minus if s[0] else plus).update(v)
 if any(plus[a]!=2 or minus[a]!=2 for a in range(1,k+1)):return None
 return (k,tuple(rows))
def anchor(x):
 p=parse(x)
 if p is None:return '0'
 k,m,w,h=p;kn=k+6;mn=m+8;wn=kn.bit_length()
 z='1'*wn+'0'+put(kn,wn)+put(mn,wn+1)
 for j in range(3*m):
  b=h+j*(w+1);a=int(x[b+1:b+1+w],2)
  z+=x[b]+put(a if 1<=a<=k else 0,wn)
 for s,a,b,c in Y:
  z+=''.join(str(s)+put(k+v,wn) for v in (a,b,c))
 return z
def models(k,rows):
 return sum(all(any(((a>>(v-1))&1)!=(s) for v in vs) for s,*vs in rows) for a in range(1<<k))
def run():
 f=[]
 for fam in itertools.combinations(itertools.combinations(range(1,7),3),4):
  degree=collections.Counter(v for triple in fam for v in triple)
  if all(degree[i]==2 for i in range(1,7)):f.append(fam)
 assert len(f)==75 and grammar(encode(6,Y)) is not None
 assert models(6,Y)==20
 dist=collections.Counter()
 for P in f:
  for Q in f:
   x=encode(6,tuple((0,)+t for t in P)+tuple((1,)+t for t in Q))
   g=grammar(anchor(x));assert g is not None and g[0]==12
   dist[len(set(P)-set(Q))]+=1
 assert dist=={0:75,2:1260,3:1680,4:2610}
 base=encode(6,Y);bad=set(['','0',base[:-1],base+'0'])
 bad.update(base[:i]+('1' if base[i]=='0' else '0')+base[i+1:] for i in range(len(base)))
 rand=random.Random(202610241202)
 for _ in range(400):
  b=list(base)
  for j in rand.sample(range(len(base)),rand.choice([2,3,4])):b[j]='1' if b[j]=='0' else '0'
  bad.add(''.join(b))
 for x in bad:assert (grammar(x) is not None)==(grammar(anchor(x)) is not None)
 z=anchor(anchor(base));g=grammar(z)
 assert g is not None and g[0]==18 and len(g[1])==24
 return {'status':'COMPUTATIONAL','balanced_formulas':5625,'mutants':len(bad),
         'q_distribution':dict(dist),'two_level_variables':18,
         'two_level_clauses':24,'failures':0}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
