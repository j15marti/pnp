#!/usr/bin/env python3
"""LSPV-4 SHUFFLED-UNSAT-ORDER313: exact source and order-statistic controls.
Run from a j15marti/pnp checkout. Standard-library Python only.
Original U198 and 198-bit V198 witness are independently archived in repo.
"""
import ast, itertools, json, math, pathlib, re
R=pathlib.Path(__file__).resolve().parents[3]
U_PATH=R/"research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt"
W_PATH=R/"experiments/arc/lspv1_286/verify_three_core286.py"
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
M=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=P+tuple(tuple(-v for v in c) for c in M)
checks=0
nodes=0
def ck(a,msg):
 global checks
 checks+=1
 if not a: raise AssertionError(msg)
def grammar(C,n):
 if len(C)*3!=4*n or n%3:return False
 q=[[0,0] for _ in range(n+1)];seen=set()
 for c in C:
  if len(c)!=3 or len(set(map(abs,c)))!=3 or any((l>0)!=(c[0]>0) for l in c):return False
  key=tuple(sorted(c))
  if key in seen:return False
  seen.add(key)
  for l in c:
   if not 1<=abs(l)<=n:return False
   q[abs(l)][int(l>0)]+=1
 return all(x==[2,2] for x in q[1:])
def evalc(c,a):return any(a[abs(l)-1]==int(l>0) for l in c)
def reduce(C,lit):return tuple(tuple(x for x in c if x!=-lit) for c in C if lit not in c)
def dpll(C):
 global nodes
 nodes+=1
 while 1:
  if not C:return True
  if () in C:return False
  u=next((c[0] for c in C if len(c)==1),None)
  if u is None:break
  C=reduce(C,u)
 lit=min(C,key=len)[0]
 return dpll(reduce(C,lit)) or dpll(reduce(C,-lit))
def count(pins):
 return sum(1 for a in itertools.product((0,1),repeat=9)
            if all(a[k-1]==v for k,v in pins.items()) and all(evalc(c,a) for c in F))
def run():
 text=U_PATH.read_text()
 U=tuple(tuple(c) for c in ast.literal_eval(text[text.index('[['):]))
 v=[list(c) for c in U]
 v[2][2],v[44][2]=v[44][2],v[2][2]
 V=tuple(tuple(c) for c in v)
 witness=tuple(map(int,re.search(r"S='([01]{198})'",W_PATH.read_text()).group(1)))
 ck(grammar(U,198) and grammar(V,198),"both genuine canonical originals")
 ck([j for j in range(264) if U[j]!=V[j]]==[2,44],"exact two changed clauses")
 ck(all(evalc(c,witness) for c in V),"198-bit complete SAT witness")
 direct=refuted=calls=0
 modules=[]
 for i in range(6):
  lo,hi=1+32*i,32+32*i
  part=[c for c in U[2:254] if any(lo<=abs(l)<=hi for l in c)]
  ck(len(part)==42 and all(all(abs(l)>=193 or lo<=abs(l)<=hi for l in c) for c in part),"modules")
  modules.append(part)
 for mask in range(64):
  pins={193+k:mask>>k&1 for k in range(6)}
  if any(all(pins[abs(l)]!=int(l>0) for l in c) for c in U[:2]):
   direct+=1;continue
  found=False
  for part in modules:
   calls+=1
   child=tuple(tuple(l for l in c if abs(l)<193) for c in part
       if not any(abs(l)>=193 and pins[abs(l)]==int(l>0) for l in c))
   if not dpll(child):found=True;break
  ck(found,"original U198 boundary proof")
  refuted+=1
 ck((direct,refuted,calls)==(16,48,152),"exhaustive UNSAT refutation")
 ck(grammar(F,9) and count({})==70,"F9 genuine source")
 ck(count({1:0,2:0,8:1,9:1})==2 and count({3:0,6:1,7:1,9:1})==0,"same-original SAT/UNSAT")
 pairs=0;comps=0
 for i,j in itertools.combinations(range(12),2):
  for ai,aj in itertools.product((0,3),repeat=2):
   wants={};compatible=True
   for c,target in ((F[i],ai),(F[j],aj)):
    for lit in c:
     w=int(lit>0) if target==3 else int(lit<0)
     if abs(lit) in wants and wants[abs(lit)]!=w:compatible=False
     wants[abs(lit)]=w
   observed=any(sum(a[abs(x)-1]==int(x>0) for x in F[i])==ai
      and sum(a[abs(x)-1]==int(x>0) for x in F[j])==aj
      for a in itertools.product((0,1),repeat=9))
   ck(compatible==observed,"S/U extreme compatibility");pairs+=1
 for a in itertools.product((0,1),repeat=9):
  for c in F:
   tc=sum(a[abs(l)-1]==int(l>0) for l in c)
   tr=sum((1-a[abs(l)-1])==int(l>0) for l in c)
   ck(tc+tr==3,"complement");comps+=1
 for bad in [F[:-1],F[:-1]+((1,1,2),),F[:-1]+((-1,2,3),),
             F[:-1]+(F[0],),F[:-1]+((1,2,10),),F[:-1]+((0,2,3),)]:
  ck(not grammar(bad,9),"malformed reject")
 rows=[]
 for t in (0,1,8,16,64,256,1024,16384):
  n,m=198+9*t,264+12*t;w=n.bit_length()
  h=lambda z:2*z.bit_length()-1
  N=h(n)+h(m)+m*(1+3*w)
  pref=h(n)+h(m)+264*(1+3*w)
  rows.append(dict(t=t,n=n,m=m,N=N,ordered_UNSAT_prefix_bits=pref,
             shuffled_min_expected_record_probes=(m+1)/3,
             randomized_two_thirds_cap_floor=math.ceil(m/6)))
 for m in (3,6,12,24,64,264):
  ranks=[min(i,j)+1 for i in range(m) for j in range(i+1,m)]
  ck(sum(ranks)*3==len(ranks)*(m+1),"exact order-statistic first hit")
  for q in range(m+1):
   miss=sum(r>q for r in ranks)
   expected=math.comb(m-2,q) if q<=m-2 else 0
   ck(miss*math.comb(m,q)==expected*len(ranks),"exact no-hit identity")
 return dict(run="LSPV4_SHUFFLED_UNSAT_ORDER313",status="PASS",P_vs_NP="OPEN",
       assertions=checks,U198=dict(label="UNSAT",boundary_direct=direct,
       module_refuted=refuted,module_calls=calls,dpll_nodes=nodes),
       V198=dict(label="SAT",checked_original_clauses=264,changed_rows=[2,44]),
       F9=dict(models=70,SAT_pinned_extensions=2,UNSAT_pinned_extensions=0,
               SS_SU_US_UU_modes=pairs,complement_checks=comps,malformed_rejects=6),
       rows=rows)
if __name__=="__main__":
 print(json.dumps(run(),indent=2,sort_keys=True))
