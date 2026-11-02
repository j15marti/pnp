#!/usr/bin/env python3
"""Independent, no-producer-import verifier for REFEREE290."""
import argparse, ast, collections, functools, itertools, json, random
from pathlib import Path

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Z6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
VW='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'

def valid(F,n):
 if n<=0 or n%3 or 3*len(F)!=4*n:return False
 seen=set();occ=collections.Counter()
 for c in F:
  if len(c)!=3 or len({abs(x) for x in c})!=3:return False
  if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
  if any(type(x) is not int or x==0 or abs(x)>n for x in c):return False
  k=tuple(sorted(c))
  if k in seen:return False
  seen.add(k);occ.update(c)
 return all(occ[v]==occ[-v]==2 for v in range(1,n+1))

def holds(F,a):return all(any(a[abs(x)]==(x>0) for x in c) for c in F)

def comps(F):
 adj=collections.defaultdict(set)
 for c in F:
  for x,y in itertools.combinations(map(abs,c),2):adj[x].add(y);adj[y].add(x)
 unseen=set(adj);out=[]
 while unseen:
  seed=unseen.pop();seen={seed};todo=[seed]
  while todo:
   x=todo.pop()
   for y in adj[x]:
    if y in unseen:unseen.remove(y);seen.add(y);todo.append(y)
  out.append(tuple(c for c in F if abs(c[0]) in seen))
 return out

def sig(F):
 V=sorted({abs(x) for c in F for x in c});P={}
 for x,y in itertools.combinations(V,2):
  P[x,y]=tuple(sum(x in map(abs,c) and y in map(abs,c) for c in F if (c[0]>0)==pol) for pol in (True,False))
 def p(x,y):return P[min(x,y),max(x,y)]
 S={x:tuple(sorted(p(x,y) for y in V if y!=x)) for x in V}
 return V,p,S

def iso(T,G):
 if len(T)!=len(G):return None,0
 tv,tp,ts=sig(T);gv,gp,gs=sig(G)
 if len(tv)!=len(gv):return None,0
 cand={x:[y for y in tv if gs[x]==ts[y]] for x in gv};order=sorted(gv,key=lambda x:(len(cand[x]),x))
 target={tuple(sorted(c)) for c in T};used=set();m={};nodes=0
 def go(i):
  nonlocal nodes;nodes+=1
  if i==len(order):
   image={tuple(sorted((1 if z>0 else -1)*m[abs(z)] for z in c)) for c in G}
   return dict(m) if image==target else None
  x=order[i]
  for y in cand[x]:
   if y in used or any(gp(x,u)!=tp(y,m[u]) for u in m):continue
   used.add(y);m[x]=y;r=go(i+1)
   if r is not None:return r
   used.remove(y);del m[x]
  return None
 return go(0),nodes

def scramble(blocks,seed):
 F=[];off=0
 for B in blocks:
  n=max(abs(x) for c in B for x in c)
  F += [tuple((1 if x>0 else -1)*(abs(x)+off) for x in c) for c in B];off+=n
 r=random.Random(seed);perm=list(range(1,off+1));r.shuffle(perm);mp={i+1:perm[i] for i in range(off)}
 G=[tuple((1 if x>0 else -1)*mp[abs(x)] for x in c) for c in F]
 G=[tuple(r.sample(list(c),3)) for c in G];r.shuffle(G)
 return tuple(G),off

def recognize_small(F,n):
 if not valid(F,n):return 'MALFORMED',[],0
 labels=[];nodes=0
 for C in comps(F):
  found=None
  for name,T in (('F9',F9),('Z6',Z6)):
   m,k=iso(T,C);nodes+=k
   if m is not None:found=name;break
  if found is None:return None,labels,nodes
  labels.append(found)
 return True,sorted(labels),nodes

def rank(rows):
 rows=[x for x in rows if x];r=0
 while rows:
  p=max(rows);b=p.bit_length()-1;r+=1
  rows=[x^p if x>>b&1 else x for x in rows if x!=p];rows=[x for x in rows if x]
 return r

def all_cut_ranks():
 T=[int(holds(F9,{i+1:bool(z>>i&1) for i in range(9)})) for z in range(512)];R=[]
 for mask in range(1,511):
  left=[i for i in range(9) if mask>>i&1];right=[i for i in range(9) if not(mask>>i&1)];rows=[]
  for a in range(1<<len(left)):
   base=sum(((a>>j)&1)<<v for j,v in enumerate(left));row=0
   for b in range(1<<len(right)):
    z=base|sum(((b>>j)&1)<<v for j,v in enumerate(right));row|=T[z]<<b
   rows.append(row)
  R.append((mask,rank(rows)))
 return R

def obdd():
 T=tuple(int(holds(F9,{i+1:bool(z>>i&1) for i in range(9)})) for z in range(512));edge={}
 for S in range(512):
  pre=[i for i in range(9) if S>>i&1]
  for v in range(9):
   if S>>v&1:continue
   rest=[i for i in range(9) if not(S>>i&1) and i!=v];pairs=set()
   for a in range(1<<len(pre)):
    base=sum(((a>>j)&1)<<u for j,u in enumerate(pre));q=[]
    for bit in (0,1):
     row=0
     for b in range(1<<len(rest)):
      z=base|(bit<<v)|sum(((b>>j)&1)<<u for j,u in enumerate(rest));row|=T[z]<<b
     q.append(row)
    if q[0]!=q[1]:pairs.add(tuple(q))
   edge[S,v]=len(pairs)
 @functools.lru_cache(None)
 def lo(S):return 0 if S==511 else min(edge[S,v]+lo(S|1<<v) for v in range(9) if not(S>>v&1))
 @functools.lru_cache(None)
 def hi(S):return 0 if S==511 else max(edge[S,v]+hi(S|1<<v) for v in range(9) if not(S>>v&1))
 S=nat=0
 for v in range(9):nat+=edge[S,v];S|=1<<v
 return [lo(0),nat,hi(0)]

def circuit():
 gates=[];outs=[];depth={i:0 for i in range(1,10)}
 def add(op,x,y):
  z=10+len(gates);gates.append((z,op,x,y));depth[z]=1+max(depth[abs(x)],depth[abs(y)]);return z
 for c in F9:outs.append(add('OR',add('OR',c[0],c[1]),c[2]))
 while len(outs)>1:outs=[add('AND',outs[i],outs[i+1]) if i+1<len(outs) else outs[i] for i in range(0,len(outs),2)]
 for z in range(512):
  a={i+1:bool(z>>i&1) for i in range(9)};b=dict(a)
  for q,op,x,y in gates:
   X=b[abs(x)] if x>0 else not b[abs(x)];Y=b[abs(y)] if y>0 else not b[abs(y)]
   b[q]=(X or Y) if op=='OR' else (X and Y)
  assert b[outs[0]]==holds(F9,a)
 return [len(gates),depth[outs[0]],512]

def cert_u(U):
 mods=[]
 for i in range(6):
  names=set(range(1+32*i,33+32*i));mods.append([c for c in U[2:254] if any(abs(x) in names for x in c)])
 def dpll(G):
  while True:
   if not G:return True
   if any(not c for c in G):return False
   u=next((c[0] for c in G if len(c)==1),None)
   if u is None:break
   G=tuple(tuple(x for x in c if x!=-u) for c in G if u not in c)
  u=G[0][0]
  return any(dpll(tuple(tuple(x for x in c if x!=-v) for c in G if v not in c)) for v in (u,-u))
 rows=calls=0
 for bits in itertools.product((False,True),repeat=6):
  a=dict(zip(range(193,199),bits));rows+=1
  if any(all(a[abs(x)]!=(x>0) for x in c) for c in U[:2]):continue
  for M in mods:
   H=tuple(tuple(x for x in c if abs(x)<=192) for c in M if not any(abs(x)>192 and a[abs(x)]==(x>0) for x in c));calls+=1
   if not dpll(H):break
  else:raise AssertionError('uncovered U198 boundary row')
 return rows,calls

def main():
 p=argparse.ArgumentParser();p.add_argument('--raw',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 raw=json.loads(Path(a.raw).read_text());root=Path(__file__).resolve().parents[3]
 text=(root/'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt').read_text();U=tuple(tuple(c) for c in ast.literal_eval(text[text.index('[['):]));V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2];V=tuple(tuple(c) for c in V)
 checks=0
 assert valid(U,198) and valid(V,198);checks+=2
 assert cert_u(U)==(64,152);checks+=216
 vw={i+1:VW[i]=='1' for i in range(198)};assert holds(V,vw);checks+=264
 for j,(name,blocks,want) in enumerate((('sat_mix',[F9,Z6,F9],['F9','F9','Z6']),('f9_product',[F9]*6,['F9']*6))):
  G,n=scramble(blocks,29000+j);got,names,nodes=recognize_small(G,n);assert got is True and names==want and nodes>0;checks+=len(G)*3+nodes
 cuts=all_cut_ranks();assert len(cuts)==510 and min(r for _,r in cuts)==2 and dict(cuts)[15]==14;checks+=510
 models=sum(holds(F9,{i+1:bool(z>>i&1) for i in range(9)}) for z in range(512));assert models==70;checks+=512
 assert circuit()==[35,6,512];checks+=512*35
 assert obdd()==[52,66,80];checks+=9*512
 common={1:0,2:0,3:0,6:1};free=[4,5,7,8,9]
 pins=[]
 for x1 in (0,1):pins.append(sum(holds(F9,{**common,1:x1,**{v:bool(z>>i&1) for i,v in enumerate(free)}}) for z in range(32)))
 assert pins==[1,0];checks+=64
 assert raw['GATE331_audit']['minimum_GF2_rank']==2 and raw['controls']['F9_OBDD']=={'best':52,'natural':66,'worst':80};checks+=2
 assert raw['P_vs_NP']=='OPEN' and 'unknown components' in raw['gap'];checks+=2
 out={'run':'COMPONENT-CANONICALIZATION-ESCAPE-REFEREE290-INDEPENDENT','status':'PASS','checks':checks,'U198':[64,152],'V198_witness_clauses':264,'small_scramble_cases':2,'F9_models':70,'F9_circuit':[35,6,512],'F9_OBDD':[52,66,80],'F9_cut_rank':[2,14,510],'pins':[1,0],'P_vs_NP':'OPEN'}
 Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
