#!/usr/bin/env python3
"""REFEREE290: source-isomorphism escape from relabeling OBDD barriers."""
from __future__ import annotations
import argparse,ast,collections,functools,itertools,json,random
from pathlib import Path

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Z6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
VW='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'

def load_uv(root):
 s=(root/'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt').read_text();U=tuple(tuple(c) for c in ast.literal_eval(s[s.index('[['):]))
 V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2]
 return U,tuple(tuple(c) for c in V)
def valid(F,n):
 if n<=0 or n%3 or len(F)*3!=4*n:return False
 q=collections.Counter();seen=set()
 for c in F:
  if len(c)!=3 or len(set(map(abs,c)))!=3 or not(all(x>0 for x in c) or all(x<0 for x in c)):return False
  if any(type(x) is not int or x==0 or abs(x)>n for x in c):return False
  k=tuple(sorted(c))
  if k in seen:return False
  seen.add(k);q.update(c)
 return all(q[v]==q[-v]==2 for v in range(1,n+1))
def holds(F,a):return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)
def ass(n,z):return {i:(z>>(i-1))&1 for i in range(1,n+1)}
def components(F):
 adj=collections.defaultdict(set)
 for c in F:
  vs=list(map(abs,c))
  for x in vs:
   adj[x].update(y for y in vs if y!=x)
 unseen=set(adj);parts=[]
 while unseen:
  todo=[unseen.pop()];S=set(todo)
  while todo:
   x=todo.pop()
   for y in adj[x]:
    if y in unseen:unseen.remove(y);S.add(y);todo.append(y)
  parts.append(tuple(c for c in F if abs(c[0]) in S))
 return parts
def pair_data(F):
 vs=sorted({abs(x) for c in F for x in c});M={}
 for i,x in enumerate(vs):
  for y in vs[i+1:]:
   M[x,y]=(sum(x in map(abs,c) and y in map(abs,c) for c in F if c[0]>0),sum(x in map(abs,c) and y in map(abs,c) for c in F if c[0]<0))
 def get(x,y):return M[min(x,y),max(x,y)] if x!=y else None
 feat={x:tuple(sorted(get(x,y) for y in vs if y!=x)) for x in vs}
 return vs,get,feat
def source_iso(T,G):
 """Exact variable isomorphism G -> T, ignoring clause/literal order."""
 if len(T)!=len(G):return None,0
 tv,tget,tf=pair_data(T);gv,gget,gf=pair_data(G)
 if len(tv)!=len(gv):return None,0
 cand={x:[y for y in tv if gf[x]==tf[y]] for x in gv}
 order=sorted(gv,key=lambda x:(len(cand[x]),x));used=set();mp={};nodes=0
 Tset={tuple(sorted(c)) for c in T}
 def rec(k):
  nonlocal nodes;nodes+=1
  if k==len(order):
   image={tuple(sorted((1 if z>0 else -1)*mp[abs(z)] for z in c)) for c in G}
   return dict(mp) if image==Tset else None
  x=order[k]
  for y in cand[x]:
   if y in used:continue
   if all(gget(x,u)==tget(y,mp[u]) for u in mp):
    mp[x]=y;used.add(y);r=rec(k+1)
    if r is not None:return r
    used.remove(y);del mp[x]
  return None
 return rec(0),nodes
def scramble(blocks,seed):
 F=[];off=0
 for B in blocks:
  n=max(abs(x) for c in B for x in c)
  F.extend(tuple((1 if x>0 else -1)*(abs(x)+off) for x in c) for c in B);off+=n
 rng=random.Random(seed);p=list(range(1,off+1));rng.shuffle(p);ren={i+1:p[i] for i in range(off)}
 G=[tuple((1 if x>0 else -1)*ren[abs(x)] for x in c) for c in F]
 for c in G:rng.shuffle(c) if isinstance(c,list) else None
 G=[tuple(rng.sample(list(c),3)) for c in G];rng.shuffle(G)
 return tuple(G),off
def find_witness(F,n):
 for z in range(1<<n):
  a=ass(n,z)
  if holds(F,a):return a
 raise AssertionError
def dictionary_decide(F,n,D):
 if not valid(F,n):return 'MALFORMED',{},0
 out={};total=0;labels=[]
 for C in components(F):
  found=None
  cvs=sorted({abs(x) for c in C for x in c});Cset={tuple(sorted(c)) for c in C}
  for name,(T,label,wit) in D.items():
   tvs=sorted({abs(x) for c in T for x in c})
   if cvs==tvs and Cset=={tuple(sorted(c)) for c in T}:
    found=(name,label,wit,{x:x for x in cvs});total+=1;break
  if found is None:
   for name,(T,label,wit) in D.items():
    mp,nodes=source_iso(T,C);total+=nodes
    if mp is not None:found=(name,label,wit,mp);break
  if found is None:return None,{},total
  name,label,wit,mp=found;labels.append((name,label))
  if label:
   for x,y in mp.items():out[x]=wit[y]
 return all(x[1] for x in labels),{'labels':labels,'witness':out},total
def gf2rank(rows):
 a=[x for x in rows if x];r=0
 while a:
  p=max(a);b=p.bit_length()-1;r+=1;a=[x^(p if x>>b&1 else 0) for x in a if x!=p];a=[x for x in a if x]
 return r
def cut_ranks(F,n):
 table=[int(holds(F,ass(n,z))) for z in range(1<<n)];R={}
 for mask in range(1<<n):
  L=[i for i in range(n) if mask>>i&1];Q=[i for i in range(n) if not(mask>>i&1)];rows=[]
  for a in range(1<<len(L)):
   base=sum(((a>>j)&1)<<v for j,v in enumerate(L));row=0
   for b in range(1<<len(Q)):
    z=base|sum(((b>>j)&1)<<v for j,v in enumerate(Q));row|=table[z]<<b
   rows.append(row)
  R[mask]=gf2rank(rows)
 return R
def obdd(F,n):
 T=tuple(int(holds(F,ass(n,z))) for z in range(1<<n));edge={}
 for S in range(1<<n):
  pre=[i for i in range(n) if S>>i&1]
  for v in range(n):
   if S>>v&1:continue
   rest=[i for i in range(n) if not(S>>i&1) and i!=v];pairs=set()
   for a in range(1<<len(pre)):
    base=sum(((a>>j)&1)<<u for j,u in enumerate(pre));p=[]
    for bit in (0,1):
     q=0
     for b in range(1<<len(rest)):
      z=base|(bit<<v)|sum(((b>>j)&1)<<u for j,u in enumerate(rest));q|=T[z]<<b
     p.append(q)
    if p[0]!=p[1]:pairs.add(tuple(p))
   edge[S,v]=len(pairs)
 full=(1<<n)-1
 @functools.lru_cache(None)
 def best(S):return 0 if S==full else min(edge[S,v]+best(S|1<<v) for v in range(n) if not(S>>v&1))
 @functools.lru_cache(None)
 def worst(S):return 0 if S==full else max(edge[S,v]+worst(S|1<<v) for v in range(n) if not(S>>v&1))
 S=nat=0
 for v in range(n):nat+=edge[S,v];S|=1<<v
 return {'best':best(0),'natural':nat,'worst':worst(0)}
def circuit(F,n):
 g=[];out=[];d={i:0 for i in range(1,n+1)}
 def add(op,x,y):
  z=n+len(g)+1;g.append((z,op,x,y));d[z]=1+max(d[abs(x)],d[abs(y)]);return z
 for c in F:out.append(add('O',add('O',c[0],c[1]),c[2]))
 while len(out)>1:out=[add('A',out[i],out[i+1]) if i+1<len(out) else out[i] for i in range(0,len(out),2)]
 for z in range(1<<n):
  a=ass(n,z);b=dict(a)
  for q,o,x,y in g:
   X=b[abs(x)] if x>0 else 1-b[abs(x)];Y=b[abs(y)] if y>0 else 1-b[abs(y)];b[q]=int((X or Y) if o=='O' else (X and Y))
  assert bool(b[out[0]])==holds(F,a)
 return len(g),d[out[0]],1<<n
def cert_u(U):
 mods=[]
 for i in range(6):
  S=set(range(1+32*i,33+32*i));mods.append([c for c in U[2:254] if any(abs(x) in S for x in c)])
 def dpll(G):
  while True:
   if not G:return True
   if any(not c for c in G):return False
   u=next((c[0] for c in G if len(c)==1),None)
   if u is None:break
   G=tuple(tuple(x for x in c if x!=-u) for c in G if u not in c)
  u=G[0][0];return any(dpll(tuple(tuple(x for x in c if x!=-v) for c in G if v not in c)) for v in (u,-u))
 rows=calls=0
 for b in itertools.product((False,True),repeat=6):
  a=dict(zip(range(193,199),b));rows+=1
  if any(all(a[abs(x)]!=(x>0) for x in c) for c in U[:2]):continue
  ok=False
  for M in mods:
   H=tuple(tuple(x for x in c if abs(x)<=192) for c in M if not any(abs(x)>192 and a[abs(x)]==(x>0) for x in c));calls+=1
   if not dpll(H):ok=True;break
  assert ok
 return rows,calls
def su(F,n):
 q=0
 for i,j in itertools.combinations(range(len(F)),2):
  for A,B in itertools.product((0,1),repeat=2):
   req={};good=True
   for c,m in ((F[i],A),(F[j],B)):
    for x in c:
     v=int(x>0) if m else int(x<0)
     if abs(x) in req and req[abs(x)]!=v:good=False
     req[abs(x)]=v
   brute=False
   for z in range(1<<n):
    a=ass(n,z)
    if all((all(a[abs(x)]==int(x>0) for x in c) if m else all(a[abs(x)]==int(x<0) for x in c)) for c,m in ((F[i],A),(F[j],B))):brute=True;break
   assert brute==good;q+=1
 return q

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();root=Path(__file__).resolve().parents[3]
 U,V=load_uv(root);assert valid(U,198) and valid(V,198);assert cert_u(U)==(64,152)
 fw=find_witness(F9,9);zw=find_witness(Z6,6);vw={i:int(VW[i-1]) for i in range(1,199)};assert holds(V,vw)
 D={'F9':(F9,True,fw),'Z6':(Z6,True,zw),'U198':(U,False,None),'V198':(V,True,vw)}
 tests=[]
 cases=[]
 for name,blocks in [('sat_mix',[F9,Z6,F9]),('f9_product',[F9]*6)]:cases.append((name,*scramble(blocks,29000+len(cases)),True))
 cases.extend([('exact_U198',U,198,False),('exact_V198',V,198,True)])
 for name,G,n,label in cases:
  got,proof,nodes=dictionary_decide(G,n,D);assert got==label
  if got:assert holds(G,proof['witness'])
  tests.append({'name':name,'n':n,'m':len(G),'label':got,'components':proof.get('labels',[]),'iso_backtrack_nodes':nodes})
 ranks=cut_ranks(F9,9);non=[ranks[s] for s in range(1,511)];assert min(non)==2 and ranks[15]==14
 f9models=sum(holds(F9,ass(9,z)) for z in range(512));assert f9models==70
 common={1:0,2:0,3:0,6:1};free=[4,5,7,8,9]
 def pc(x1):return sum(holds(F9,{**common,1:x1,**{v:(z>>i)&1 for i,v in enumerate(free)}}) for z in range(32))
 pins=[pc(0),pc(1)];assert pins==[1,0]
 bad=[(),((1,1,2),),((1,-2,3),),F9+(F9[0],),((1,2,3),),tuple(reversed(F9))]
 malformed=sum(dictionary_decide(F,max((abs(x) for c in F for x in c),default=3),D)[0]=='MALFORMED' for F in bad);assert malformed>=5
 result={'run':'COMPONENT-CANONICALIZATION-ESCAPE-REFEREE290','timestamp_pacific':'2026-11-02T06:48:00-08:00','P_vs_NP':'OPEN',
  'status':'PROVED_EXACT_FIXED_DICTIONARY_ISOMORPHISM_CLOSURE_PLUS_COMPUTATIONAL_CONTROLS',
  'obstruction':'Adversarial variable relabeling can force every input-oblivious OBDD order in a polynomial portfolio to be exponential while leaving the source a polynomially recognizable disjoint union of fixed certified components.',
  'theorem':'For any fixed finite dictionary of connected canonical originals with checked SAT witnesses or UNSAT certificates, the isomorphism-closed set of disjoint unions of dictionary members is decidable in polynomial total source work. Strict grammar and primal components are acquired; each colored incidence component has maximum degree four and is matched to the fixed dictionary by bounded-degree graph isomorphism (or constant-template exhaustive bijections); SAT iff every component label is SAT. Arbitrary variable renaming, clause order, literal order and component order do not change this result.',
  'scope':'This subsumes GATE331 product relabelings and strengthens REFEREE289 from one exact serialization to its isomorphism closure. GATE331 already stated the F9 SAT-only recognition escape; the new increment is the all-fixed-dictionary both-label theorem and U198/V198 proof-carrying closure. It does not decide unknown components.',
  'GATE331_audit':{'all_nontrivial_F9_cuts':510,'minimum_GF2_rank':min(non),'rank_cut_x1_x2_x3_x4':ranks[15],'two_block_interleaved_rank_by_tensor':ranks[15]**2,'result':'rank lower bound valid for prescribed OBDD orders; irrelevant to source-aware dictionary decision'},
  'controls':{'dictionary_scrambles':tests,'U198_certificate':[64,152],'V198_witness_clauses':264,'F9_models':f9models,'F9_circuit':circuit(F9,9),'F9_OBDD':obdd(F9,9),'F9_same_original_pins':pins,'F9_SU_modes':su(F9,9),'malformed_rejected':malformed},
  'charged_recurrence':{'time':'T=T_grammar+T_primal_components+sum_C sum_D T_colored_iso(C,D)+T_certificate_init+T_label_join+T_output; on unknown components add the full exact fallback and all failed-policy costs','peak':'S_peak=max simultaneously live parser, incidence/primal index, one isomorphism guest, certificate map, output witness/proof and any fallback guest; polynomial for fixed dictionary','no_free_work':'dictionary labels are justified once by stored witnesses/UNSAT proof; every component map and output is checked. No SAT-label, best-order, continuation-equivalence or OBDD oracle.'},
  'falsifiers':['adversarial renaming alone creates SAT hardness','polynomial input-oblivious OBDD portfolios cover source-aware order selection','exponential prescribed-order OBDD output is necessary SAT decision work','fixed certified component products require semantic cofactor comparison'],
  'literature':[{'query':'Luks bounded valence graph isomorphism 1982','finding':'primary theorem gives polynomial isomorphism for degree-bounded colored incidence graphs'},{'query':'OBDD communication rank variable ordering','finding':'rank is a valid restricted OBDD lower-bound technique, not an arbitrary SAT lower bound'},{'query':'project finite dictionary component isomorphism','finding':'GATE331 already contains F9-only recognition escape; no exact both-label dictionary theorem hit; failed search is not novelty evidence'},{'query':'github.com/openai SAT component isomorphism OBDD relabeling','finding':'no relevant indexed implementation; failed search is not evidence'}],
  'gap':'No polynomial solver for sources with unknown components, no all-input core lower bound, no arbitrary-A power-short Phi(A), no strict same-machine numerical FLMV transfer, and no P-versus-NP conclusion.'}
 Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'run':result['run'],'tests':tests,'rank':[min(non),ranks[15]],'F9':[f9models,result['controls']['F9_circuit'],result['controls']['F9_OBDD'],pins],'ok':True},sort_keys=True))
if __name__=='__main__':main()
