#!/usr/bin/env python3
"""SOURCE-CUT-ENTROPY127. Dependency-free exhaustive hostile controls.
Finite branch/provenance/DIMACS tests; not an FLMV runtime measurement.
"""
import json,math,random
from pathlib import Path
from collections import Counter
SEED=12720261026
W='''-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;
5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;
-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;
2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'''
W1=tuple(tuple(map(int,c.split())) for c in W.replace('\n','').split(';'))
assert len(W1)==20
checks=0
def check(v,msg='assertion failed'):
 global checks
 checks+=1
 if not v:raise AssertionError(msg)
def tseitin(v,edges,charge):
 inc=[[] for _ in range(v)]
 for j,(a,b) in enumerate(edges,1):inc[a].append(j);inc[b].append(j)
 check(all(len(e)==3 for e in inc))
 return tuple(tuple(x if ((mask>>j)&1)==0 else -x for j,x in enumerate(inc[i]))
   for i in range(v) for mask in range(8) if mask.bit_count()%2!=charge[i])
def val_clause(cl,a):return any(((a>>(abs(l)-1))&1)==int(l>0) for l in cl)
def sat_witness(F,n):
 for a in range(1<<n):
  if all(val_clause(cl,a) for cl in F):return a
 return None
def private(F,n):
 out={}
 for a in range(1<<n):
  bad=[j for j,cl in enumerate(F) if not val_clause(cl,a)]
  if len(bad)==1:out.setdefault(bad[0],a)
 return out
def serialize(F,n):
 data=f'p cnf {n} {len(F)}\n'+''.join(' '.join(map(str,cl))+' 0\n' for cl in F)
 rows=data.strip().splitlines(); h=rows.pop(0).split()
 check(h==['p','cnf',str(n),str(len(F))])
 recovered=tuple(tuple(int(k) for k in row.split()[:-1]) for row in rows)
 check(recovered==F and all(row.split()[-1]=='0' for row in rows))
 check(all(0<abs(l)<=n for cl in F for l in cl))
 return len(data)
def signed22(F,n):
 co=Counter(l for cl in F for l in cl)
 return (all(len(cl)==3 and len({abs(l) for l in cl})==3 for cl in F)
  and len(set(F))==len(F) and all(co[v]==2 and co[-v]==2 for v in range(1,n+1)))
def branch(F,n,witnesses,adaptive=False):
 leaves=[];private_leaf={};counts={'nodes':0,'leaves':0}
 ws=tuple(sorted(witnesses.items()))
 def rec(assigned,domain,prefix,depth):
  counts['nodes']+=1
  falses=[j for j,cl in enumerate(F) if all(
   (domain>>(abs(l)-1)&1) and ((assigned>>(abs(l)-1)&1)!=int(l>0)
   for l in cl)]
  if falses:
   j=falses[0];leaves.append((prefix,depth,j))
   for k,w in ws:
    if all(((w>>(abs(x)-1))&1)==b for x,b in prefix):
     check(k==j,'wrong source clause ID')
     check(k not in private_leaf,'duplicate witness terminal')
     private_leaf[k]=(depth,j)
   counts['leaves']+=1
   return
  free=[i for i in range(n) if not(domain>>i&1)]
  check(bool(free),'SAT assignment passed an UNSAT branch tree')
  if not adaptive:var=free[0]
  else:
   comp=[w for _,w in ws if all(((w>>(abs(x)-1))&1)==b for x,b in prefix)]
   def score(x):
    n0=sum(not(w>>x&1) for w in comp)
    return(min(n0,len(comp)-n0),-x)
   var=max(free,key=score)
  for b in (0,1):rec(assigned|(b<<var),domain|(1<<var),prefix+((var+1,b),),depth+1)
 rec(0,0,tuple(),0)
 check(len(private_leaf)==len(witnesses))
 check(counts['nodes']==2*counts['leaves']-1)
 for k,w in ws:
  d,j=private_leaf[k]
  check(j==k)
  check(not val_clause(F[j],w))
 e=len(witnesses)
 mean=sum(d for d,j in private_leaf.values())/e
 kraft=sum(2.0**(-d) for d,j in private_leaf.values())
 check(mean+1e-10>=math.log2(e))
 check(kraft<=1+1e-12)
 check(sum(2.0**(-d) for p,d,j in leaves)<=1+1e-10)
 return dict(adaptive=adaptive,nodes=counts['nodes'],leaves=counts['leaves'],
  private_mean_depth=mean,private_kraft=kraft,max_leaf_depth=max(d for p,d,j in leaves),
  private_depths=dict(Counter(str(d) for d,j in private_leaf.values())),
  private_entropy_lower_bound=math.log2(e))
def pin(l,start):
 a,b=start,start+1
 return tuple((l,u*a,v*b) for u in (1,-1) for v in (1,-1))
def lifted2(clauses,start):
 out=[];p=start
 for a,b in clauses:
  check(abs(a)!=abs(b))
  out.extend(((a,b,p),(a,b,-p)));p+=1
 return tuple(out),p
def mismatch_join():
 eq,n1=lifted2(((-1,2),(1,-2)),4)
 anti,n2=lifted2(((-1,-3),(1,3)),n1)
 good=eq+anti
 bad=eq+tuple(tuple(2 if x==3 else -2 if x==-3 else x for x in cl) for cl in anti)
 check(sat_witness(eq,n2)!=None)
 check(sat_witness(anti,n2)!=None)
 for x in (0,1):
  pp=pin(1 if x else -1,n2+1)
  check(sat_witness(eq+pp,n2+2)!=None)
  check(sat_witness(anti+pp,n2+2)!=None)
  check(sat_witness(good+pp,n2+2)!=None)
  check(sat_witness(bad+pp,n2+2)==None)
 check(sat_witness(good,n2)!=None)
 check(sat_witness(bad,n2)==None)
 return dict(boundary_projection_both=[0,1],separate_names_SAT=True,
  collided_private_names_UNSAT=True,source_identity_required=True,
  good_bytes=serialize(good,n2),bad_bytes=serialize(bad,n2))
def derived_cut():
 source=pin(-1,2);valid=source+pin(5,6);invalid=source+pin(1,5)
 check(sat_witness(source,4)!=None)
 check(sat_witness(valid,7)!=None)
 check(sat_witness(invalid,6)==None)
 full=W1+pin(16,17)
 delete=W1[1:]+pin(16,17)
 full2=full+pin(19,20)
 delete2=delete+pin(19,20)
 check(sat_witness(full,18)==None)
 check(sat_witness(delete,18)!=None)
 check(sat_witness(full2,21)==None)
 check(sat_witness(delete2,21)!=None)
 return dict(valid_source_SAT=True,valid_fresh_child_SAT=True,
  wrong_alias_child_UNSAT=True,sourced_W1_full_UNSAT=True,
  sourced_W1_deleted_child_SAT=True,
  source_bytes=serialize(source,4),valid_bytes=serialize(valid,7),
  invalid_bytes=serialize(invalid,6),W1_full_child_bytes=serialize(full,18),
  W1_deleted_child_bytes=serialize(delete,18),
  W1_full_grandchild_bytes=serialize(full2,21),
  W1_deleted_grandchild_bytes=serialize(delete2,21))
def mutate(F,n,rng):
 c=[list(cl) for cl in F];pol=rng.choice((-1,1))
 slots=[(i,j) for i,cl in enumerate(c) for j,l in enumerate(cl)
        if int(l>0)==int(pol>0)]
 for _ in range(100):
  (i,j),(h,k)=rng.sample(slots,2)
  if i==h or abs(c[i][j])==abs(c[h][k]):continue
  c[i][j],c[h][k]=c[h][k],c[i][j]
  z=tuple(tuple(cl) for cl in c)
  if signed22(z,n):return z
  c[i][j],c[h][k]=c[h][k],c[i][j]
 return F
def main():
 rng=random.Random(SEED)
 cases={
  'odd_K4':(tseitin(4,[(i,j) for i in range(4) for j in range(i+1,4)],(1,0,0,0)),6),
  'odd_K33':(tseitin(6,[(i,j) for i in range(3) for j in range(3,6)],(1,0,0,0,0,0)),9),
  'strict_signed_W1':(W1,15),
  'odd_Petersen':(tseitin(10,
    [(i,(i+1)%5) for i in range(5)]+
    [(i,i+5) for i in range(5)]+
    [(i+5,((i+2)%5)+5) for i in range(5)],
    (1,0,0,0,0,0,0,0,0,0)),15)}
 results={}
 for key,(F,n) in cases.items():
  p=private(F,n)
  check(sat_witness(F,n)==None)
  check(len(p)==len(F))
  check(serialize(F,n)>0)
  for j,w in p.items():
   check(sat_witness(F[:j]+F[j+1:],n)!=None)
   check(all(val_clause(cl,w) for k,cl in enumerate(F) if k!=j))
  tests=[branch(F,n,p,False),branch(F,n,p,True)]
  results[key]=dict(n=n,m=len(F),essential=len(p),
   signed22=signed22(F,n),root_DIMACS_bytes=serialize(F,n),
   branch_strategies=tests,root_one_terminal_K=len(F),
   root_one_terminal_depth=0,root_one_terminal_entropy_check=True)
 check(signed22(W1,15))
 sample=[];cur=W1
 for k in range(24):
  if k%6==0:cur=W1
  else:cur=mutate(cur,15,rng)
  check(signed22(cur,15))
  witness=sat_witness(cur,15)
  sample.append(dict(case=k,sat=witness!=None,witness=witness,
   bytes=serialize(cur,15)))
 count=Counter('SAT' if x['sat'] else 'UNSAT' for x in sample)
 check(count['SAT']>=1)
 check(count['UNSAT']>=1)
 check(sat_witness(((1,),(-1,2),(-2,)),2)==None)
 check(sat_witness(((1,2),(-1,2),(-2,)),2)==None)
 check(sat_witness(((1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3)),3)!=None)
 a=mismatch_join();b=derived_cut()
 return dict(run='SOURCE_CUT_ENTROPY127',seed=SEED,checks=checks,
  cases=results,signed_mutation_counts=dict(count),signed_mutations=sample,
  bad_join=a,derived_cut=b,
  easy_controls=dict(Horn_UNSAT=True,twoSAT_UNSAT=True,affine_SAT=True),
  scope='finite exhaustively checked semantics, not an FLMV runtime lower bound')
if __name__=='__main__':
 out=main();out['checks']=checks
 with open(Path(__file__).with_name('2026-10-26_0024_SOURCE_CUT_ENTROPY127_raw.json'),'w') as f:
  json.dump(out,f,sort_keys=True,indent=2)
 print(json.dumps({'run':out['run'],'checks':out['checks'],
   'cases':out['cases'],'signed_mutation_counts':out['signed_mutation_counts'],
   'bad_join':out['bad_join'],'derived_cut':out['derived_cut']},indent=2))
