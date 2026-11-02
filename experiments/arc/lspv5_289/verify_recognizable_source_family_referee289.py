#!/usr/bin/env python3
"""No-producer-import referee for REFEREE289."""
import argparse,ast,collections,functools,itertools,json
from pathlib import Path

Z=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
K=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
W='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'

def valid(F,n):
 if n%3 or len(F)*3!=4*n:return False
 seen=set();q=collections.Counter()
 for c in F:
  if len(c)!=3 or len(set(map(abs,c)))!=3 or not(all(x>0 for x in c) or all(x<0 for x in c)):return False
  if any(not isinstance(x,int) or x==0 or abs(x)>n for x in c):return False
  k=tuple(sorted(c))
  if k in seen:return False
  seen.add(k);q.update(c)
 return all(q[i]==q[-i]==2 for i in range(1,n+1))
def holds(F,a):return all(any(a[abs(x)]==(x>0) for x in c) for c in F)
def z6shift(j):
 d=198+6*j
 return tuple(tuple((1 if x>0 else -1)*(abs(x)+d) for x in c) for c in Z)
def fam(B,t):return tuple(B)+sum((z6shift(j) for j in range(t)),())

def cert(U):
 mods=[]
 for i in range(6):
  S=set(range(1+32*i,33+32*i));G=[c for c in U[2:254] if any(abs(x) in S for x in c)]
  assert len(G)==42;mods.append(G)
 def dpll(G):
  while True:
   if not G:return True
   if any(len(c)==0 for c in G):return False
   u=next((c[0] for c in G if len(c)==1),None)
   if u is None:break
   G=tuple(tuple(x for x in c if x!=-u) for c in G if u not in c)
  u=G[0][0]
  return any(dpll(tuple(tuple(x for x in c if x!=-v) for c in G if v not in c)) for v in (u,-u))
 rows=calls=0
 for b in itertools.product((False,True),repeat=6):
  a=dict(zip(range(193,199),b));rows+=1
  if any(all(a[abs(x)]!=(x>0) for x in c) for c in U[:2]):continue
  ok=False
  for M in mods:
   H=tuple(tuple(x for x in c if abs(x)<=192) for c in M if not any(abs(x)>192 and a[abs(x)]==(x>0) for x in c))
   calls+=1
   if not dpll(H):ok=True;break
  assert ok
 return rows,calls

def obdd(F,n):
 T=tuple(int(holds(F,{i+1:bool(z>>i&1) for i in range(n)})) for z in range(1<<n))
 edge={}
 for mask in range(1<<n):
  done=[i for i in range(n) if mask>>i&1]
  for v in range(n):
   if mask>>v&1:continue
   tail=[i for i in range(n) if not(mask>>i&1) and i!=v];pairs=set()
   for x in range(1<<len(done)):
    pre=sum(((x>>j)&1)<<u for j,u in enumerate(done));p=[0,0]
    for val in (0,1):
     bits=0
     for y in range(1<<len(tail)):
      z=pre|(val<<v)|sum(((y>>j)&1)<<u for j,u in enumerate(tail));bits|=T[z]<<y
     p[val]=bits
    if p[0]!=p[1]:pairs.add(tuple(p))
   edge[mask,v]=len(pairs)
 full=(1<<n)-1
 @functools.lru_cache(None)
 def lo(s):return 0 if s==full else min(edge[s,v]+lo(s|1<<v) for v in range(n) if not(s>>v&1))
 @functools.lru_cache(None)
 def hi(s):return 0 if s==full else max(edge[s,v]+hi(s|1<<v) for v in range(n) if not(s>>v&1))
 s=nat=0
 for v in range(n):nat+=edge[s,v];s|=1<<v
 return [lo(0),nat,hi(0)]

def circuit_rows(F,n):
 g=[];out=[];d={i:0 for i in range(1,n+1)}
 def add(op,x,y):
  z=n+len(g)+1;g.append((z,op,x,y));d[z]=1+max(d[abs(x)],d[abs(y)]);return z
 for c in F:out.append(add('O',add('O',c[0],c[1]),c[2]))
 while len(out)>1:out=[add('A',out[i],out[i+1]) if i+1<len(out) else out[i] for i in range(0,len(out),2)]
 for z in range(1<<n):
  a={i+1:bool(z>>i&1) for i in range(n)};b=dict(a)
  for q,o,x,y in g:
   X=b[abs(x)] if x>0 else not b[abs(x)];Y=b[abs(y)] if y>0 else not b[abs(y)]
   b[q]=(X or Y) if o=='O' else (X and Y)
  assert b[out[0]]==holds(F,a)
 return len(g),d[out[0]],1<<n

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--raw',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
 raw=json.loads(Path(a.raw).read_text());root=Path(__file__).resolve().parents[3]
 txt=(root/'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt').read_text()
 U=tuple(tuple(c) for c in ast.literal_eval(txt[txt.index('[['):]));V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2];V=tuple(tuple(c) for c in V)
 checks=0
 assert valid(U,198) and valid(V,198);checks+=2
 assert cert(U)==(64,152);checks+=216
 va={i+1:W[i]=='1' for i in range(198)};assert holds(V,va);checks+=264
 zw=next(z for z in range(64) if holds(Z,{i+1:bool(z>>i&1) for i in range(6)}));checks+=64
 for t in range(5):
  for B,label in ((U,False),(V,True)):
   F=fam(B,t);n=198+6*t;assert valid(F,n);checks+=len(F)*3
   assert tuple(F[:264])==B and all(tuple(F[264+8*j:272+8*j])==z6shift(j) for j in range(t));checks+=264+8*t
   if label:
    aa=dict(va)
    for j in range(t):
     for i in range(1,7):aa[198+6*j+i]=bool(zw>>(i-1)&1)
    assert holds(F,aa);checks+=len(F)
 f9=sum(holds(K,{i+1:bool(z>>i&1) for i in range(9)}) for z in range(512));assert f9==70;checks+=512
 assert circuit_rows(K,9)==(35,6,512);checks+=512*35
 assert obdd(K,9)==[52,66,80];checks+=9*(1<<9)
 assert raw['proof_controls']['U198_boundary_rows']==64 and raw['proof_controls']['U198_module_calls']==152;checks+=2
 assert len(raw['family_controls'])==10 and raw['F9']['models']==70;checks+=11
 assert raw['P_vs_NP']=='OPEN' and 'worst-case' in raw['scope'];checks+=2
 out={'run':'RECOGNIZABLE-SOURCE-FAMILY-BYPASS-REFEREE289-INDEPENDENT','status':'PASS','checks':checks,
      'U198':[64,152],'V198_clauses':264,'family_cases':10,'F9_models':70,'F9_circuit':[35,6,512],'F9_OBDD':[52,66,80],
      'native_FLMV_trace':False,'P_vs_NP':'OPEN'}
 Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
