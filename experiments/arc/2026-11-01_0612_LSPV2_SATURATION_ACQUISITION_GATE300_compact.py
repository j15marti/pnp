#!/usr/bin/env python3
"""Source-authenticated elementary saturation gate. Standard library only.
This mirrors the standalone full producer and independently checked 21,870 cubes;
not an FLMV machine simulator or a universal polynomial SAT algorithm.
"""
from itertools import product,combinations
from collections import Counter

Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
Q15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-x for x in c) for c in Q15)
U=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
S=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))

def valid(F):
 if not F:return False
 n=max(abs(x) for c in F for x in c)
 c=Counter(x for C in F for x in C)
 return len(F)*3==4*n and len(set(tuple(sorted(C)) for C in F))==len(F) and all(len(C)==3 and len({abs(x) for x in C})==3 and (all(x>0 for x in C) or all(x<0 for x in C)) for C in F) and all(c[x]==c[-x]==2 for x in range(1,n+1))

def scan(F,p):
 n=max(abs(x) for C in F for x in C)
 f=n-len(p)
 covered=0;uncovered=0;eta_occ=Counter();edges=[];empty=False
 for j,C in enumerate(F):
  if any(abs(x) in p and p[abs(x)]==int(x>0) for x in C):
   covered+=1
   for x in C:
    if abs(x) not in p:eta_occ[abs(x),x>0]+=1
  else:
   uncovered+=1
   free=[abs(x) for x in C if abs(x) not in p]
   if not free:empty=True
   if len(free)==2:edges.append((j,free[0],free[1]))
 eta=sum(min(eta_occ[x,True],eta_occ[x,False]) for x in range(1,n+1) if x not in p)
 e=2*f-uncovered
 b=len(edges)
 assert eta<=covered and b<=2*len(p)
 return {'n':n,'k':len(p),'c':covered,'b':b,'eta':eta,'e':e,'empty':empty,'edges':edges,'lower':e-eta-b//3}

def triangles(edges):
 out=[];checks=0
 for comb in combinations(edges,3):
  checks+=1
  deg=Counter(x for _,u,v in comb for x in (u,v))
  if len(deg)==3 and set(deg.values())=={2}:
   out.append(tuple(sorted(t[0] for t in comb)))
 return sorted(out),checks

def control(F,p):
 q=scan(F,p)
 # Baseline scans all candidate binary-edge triples.
 ts,cost=triangles(q['edges']);used=set();chosen=[]
 for t in ts:
  if not used.intersection(t):
   used.update(t);chosen.append(t)
 nu=len(chosen);delta=q['e']-q['eta']-nu
 assert 3*delta>=2*q['n']-8*q['k'] and delta>=q['lower']
 if 4*q['k']<q['n']:assert delta>0
 if q['lower']>0:assert delta>0
 early='EMPTY' if q['empty'] else 'SPILL' if q['e']<q['eta'] else 'SKIP' if q['lower']>0 else 'SEARCH'
 return {'baseline':cost,'charged':cost if early=='SEARCH' else 0,'skip':int(early=='SKIP'),
         'triangle':int(early=='SEARCH'),'status':early,'delta':delta,'nu':nu}

def all_cubes(root,n):
 free=[v for v in range(1,n+1) if v not in root]
 for row in product((-1,0,1),repeat=len(free)):
  p=dict(root)
  p.update({v:b for v,b in zip(free,row) if b>=0})
  yield p

def count(F,p):
 n=max(abs(x) for C in F for x in C)
 free=[v for v in range(1,n+1) if v not in p]
 return sum(all(any({**p,**dict(zip(free,bits))}[abs(x)]==int(x>0) for x in C) for C in F) for bits in product((0,1),repeat=len(free)))

def main():
 observed={}
 for name,F,root in (('Y6',Y6,{}),('F9',F9,{}),('F15_UNSAT_window',F15,U),('F15_SAT_window',F15,S)):
  assert valid(F)
  n=max(abs(x) for C in F for x in C)
  rows=[control(F,p) for p in all_cubes(root,n)]
  observed[name]={'cubes':len(rows),'guard_skips':sum(x['skip'] for x in rows),
                  'baseline_triangle_checks':sum(x['baseline'] for x in rows),
                  'guard_triangle_checks':sum(x['charged'] for x in rows)}
 for name,F,p,expected in (('F9_cube_UNSAT',F9,{8:0,3:0,7:0,6:0,1:1,5:1},0),
                            ('F15_SAT',F15,S,2),('F15_UNSAT',F15,U,0),('Y6_root',Y6,{},20)):
  value=count(F,p);assert value==expected,(name,value)
 assert observed['Y6']==dict(cubes=729,guard_skips=211,baseline_triangle_checks=68,guard_triangle_checks=36)
 assert observed['F9']==dict(cubes=19683,guard_skips=5998,baseline_triangle_checks=10161,guard_triangle_checks=3483)
 assert observed['F15_UNSAT_window']==dict(cubes=729,guard_skips=2,baseline_triangle_checks=869,guard_triangle_checks=665)
 assert observed['F15_SAT_window']==dict(cubes=729,guard_skips=21,baseline_triangle_checks=555,guard_triangle_checks=418)
 print('PASS',observed,'P versus NP OPEN')
if __name__=='__main__':main()
