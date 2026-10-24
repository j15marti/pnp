#!/usr/bin/env python3
"""GRID-CLONE89: exact connected-copy equality-cloud transport control.
The output is an independently encoded ordinary proper 3CNF, not a pointer.
Run beside 2026-10-24_2202_GRID_BRAMBLE89_MINI.py.
"""
import json, random, itertools, importlib.util
from collections import defaultdict
from pathlib import Path
p=Path(__file__).with_name('2026-10-24_2202_GRID_BRAMBLE89_MINI.py')
spec=importlib.util.spec_from_file_location('grid89',p)
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
checks=0

def req(cond,msg):
 global checks
 checks+=1
 if not cond:raise AssertionError(msg)

def clone_formula(r,label):
 source=base.spec(r,label); E=source['es']; grid=r*r
 inc=defaultdict(list)
 for idx,(u,v) in enumerate(source['edges']):
  inc[u].append(idx);inc[v].append(idx)
 clones={}; nextid=1
 for v in range(1,grid+1):
  for idx in sorted(inc[v]): clones[(v,idx)]=nextid;nextid+=1
 req(nextid==2*E+1,'two clones per edge')
 clauses=[]
 zlist=[]
 for idx,(u,v) in enumerate(source['edges']):
  z=nextid;nextid+=1;zlist.append(z)
  clauses.extend(((clones[(u,idx)],clones[(v,idx)],z),
                  (clones[(u,idx)],clones[(v,idx)],-z)))
 links=0;eq_au=[]
 for v in range(1,grid+1):
  ids=[clones[(v,i)] for i in sorted(inc[v])]
  for s,t in zip(ids,ids[1:]):
   q=nextid;qq=nextid+1;nextid+=2;eq_au.extend((q,qq));links+=1
   clauses.extend(((-s,t,q),(-s,t,-q),(s,-t,qq),(s,-t,-qq)))
 a=nextid;b=nextid+1;c=nextid+2;y=nextid+3;nextid+=4
 x11=clones[(1,inc[1][0])]
 clauses.extend(((a,x11,y),(a,x11,-y)))
 for mask in range(8):
  effective=1 if label=='SAT' and mask==0 else mask
  clauses.append(tuple(-v if (effective>>j)&1 else v for j,v in enumerate((a,b,c))))
 n=nextid-1;m=len(clauses)
 req(links==2*E-grid,'connected-clone tree link count')
 req(n==7*E-2*grid+4,'variable ledger')
 req(m==10*E-4*grid+10,'clause ledger')
 h=(64*(n+m+1)-1).bit_length()
 return dict(r=r,n=n,m=m,N=(4*m+2)*h,h=h,es=E,grid=grid,
             clauses=clauses,clones=clones,inc=inc,links=links,
             a=a,b=b,c=c,y=y,label=label,free=E+2*links+1)

def eq_pair_truth(s,t,q,qq):
 return all(any(base.value_literal(l,(s<<0)|(t<<1)|(q<<2)|(qq<<3)) for l in cl)
            for cl in ((-1,2,3),(-1,2,-3),(1,-2,4),(1,-2,-4)))

def main():
 rng=random.Random(202610242202);rows=[]
 for s,t in itertools.product((0,1),repeat=2):
  tally=sum(eq_pair_truth(s,t,q,qq) for q,qq in itertools.product((0,1),repeat=2))
  req(tally==(4 if s==t else 0),'equality semantic truth table')
 for r in range(2,8):
  u=clone_formula(r,'UNSAT');v=clone_formula(r,'SAT')
  req((u['n'],u['m'],u['N'])==(v['n'],v['m'],v['N']),'matched encodings')
  for F in (u,v):
   deg,occ,k4=base.primal_stats(F['clauses'],F['n'])
   req(not k4 and deg<=8 and occ<=10,'bounded local structure')
   req(all(len(set(map(abs,c)))==3 for c in F['clauses']),'proper ternaries')
   for _ in range(20):
    order=list(range(F['m']));rng.shuffle(order)
    req(base.scope_for_clause_order(F,order)>=r,'connected-copy width')
  w=(1<<(2*u['es']))-1
  req(base.sat_clauses(v['clauses'],w),'SAT source all-clones-one witness')
  ir=base.row_dp_indsets(r)
  models=ir*(1<<v['free'])
  rows.append(dict(r=r,clones_per_edge=2,original_grid_variables=r*r,
      clone_variables=2*u['es'],equality_links=u['links'],
      total_variables=u['n'],clauses=u['m'],N=u['N'],
      width_lower=r,max_primal_degree=8,max_variable_occurrences=10,
      SAT_model_count=models,UNSAT_model_count=0,
      free_variables=v['free']))
 print(json.dumps({'run':'GRID-CONNECTED-CLONE89','checks':checks,'failures':0,
       'semantics':'Equality pair has 4 extensions if both clones agree, none otherwise; original SAT/UNSAT labels retained.',
       'limitations':'No all-input size-shrinking contractor; no physical FLMV trace; source-copy identity is a declared restriction.',
       'rows':rows},indent=2))

if __name__=='__main__':main()
