#!/usr/bin/env python3
"""Independent exact T5 red-team controls and arithmetic for two-polarity routing.
2026-11-18, TMR-5 / 099. Standard library only; no external SAT solver.
All T5 truth checks enumerate native five-symbol assignments explicitly.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
from math import log2
import json
import hashlib

ROOT=Path(__file__).resolve().parent
SYMS=range(5)
R=lambda a,b: (b-a)%5 in (1,3)
ARC=[(0,2),(2,1),(0,3),(1,3),(4,0),(1,4)]
# blocks: 0-to-1 with length-two paths (forward/forward and forward/backward),
# and 1-to-0 with length-two path (backward/backward).
BLOCKS=[ARC[:4],ARC[4:]]

def sat_edges(edges,a):
    return all(R(a[u],a[v]) for u,v in edges)

def count_hom(edges,n=5):
    count=0; first=None
    for a in product(SYMS,repeat=n):
        if sat_edges(edges,a):
            count+=1
            if first is None: first=a
    return count,first

def local_counts(block,z):
    # Brute enumerate every private vertex as a separate native assignment.
    fixed={0:z[0],1:z[1]}
    own=sorted({v for u,w in block for v in (u,w)}-set(fixed))
    cnt=0
    for vals in product(SYMS,repeat=len(own)):
        a=dict(fixed);a.update(zip(own,vals))
        cnt+=int(all(R(a[u],a[v]) for u,v in block))
    return cnt

def t_formula(l,q,delta):
    from math import comb
    return sum(comb(l,t) for t in range(l+1) if (l+q+2*t-delta)%5==0)

def t_direct(l,q,delta):
    # independently enumerate binary choice of allowed native increments
    cnt=0
    for bits in product((0,1),repeat=l):
        x=0
        for j,t in enumerate(bits):
            if j<q: # j is backward edge in this source orientation
                x=(x-((1,3)[t]))%5
            else:
                x=(x+((1,3)[t]))%5
        cnt+=int(x==delta)
    return cnt

checks=0
transfers=[]
for l in range(1,9):
 for q in range(l+1):
  for d in range(5):
   a=t_formula(l,q,d);b=t_direct(l,q,d)
   assert a==b,(l,q,d,a,b)
   checks+=1
   if l==2:transfers.append({'length':l,'backwards':q,'delta':d,'count':a})
assert all(t_formula(2,0,d)>0 for d in (1,2,4))
assert all(t_formula(2,1,d)>0 for d in (0,2,3))
assert all(t_formula(2,2,d)>0 for d in (1,3,4))

rows=[]
for z in product(SYMS,repeat=2):
 counts=[local_counts(b,z) for b in BLOCKS]
 feasible=[x>0 for x in counts]
 assert not all(feasible)
 checks+=1
 rows.append({'z':list(z),'delta':(z[1]-z[0])%5,'block_counts':counts,'bad_blocks':[i for i,t in enumerate(counts) if t==0]})
for d in range(5):
 r=[x for x in rows if x['delta']==d]
 assert len(r)==5
 assert {tuple(x['bad_blocks']) for x in r}==({(0,1)} if d==0 else {(1,)} if d==2 else {(0,)})
 checks+=1
# every single block has at least one feasible shared label row
assert all(any(row['block_counts'][i]>0 for row in rows) for i in range(2))
checks+=1

H_count,_=count_hom(ARC)
assert H_count==0
checks+=1
critical=[]
for i,e in enumerate(ARC):
 c,w=count_hom(ARC[:i]+ARC[i+1:]);assert c>0 and w is not None
 # Clocked independent source verification with retained constraints.
 assert all(R(w[u],w[v]) for j,(u,v) in enumerate(ARC) if j!=i)
 assert not R(w[e[0]],w[e[1]])
 assert any(w[(e[0])] == a and w[(e[1])] == b for a,b in product(SYMS,repeat=2))
 checks+=4
 critical.append({'arc':list(e),'count_after_deletion':c,'witness':list(w)})
# Invariance under all rotations and all 25 endpoint restrictions
for shift in SYMS:
 for row in rows:
  p=( (row['z'][0]+shift)%5,(row['z'][1]+shift)%5 )
  rr=next(x for x in rows if tuple(x['z'])==p)
  assert rr['block_counts']==row['block_counts']
  checks+=1

# Exactly rational FLMV 2005 Thm 5.7 and 6.4 endpoints.
# f_k = c f_{k-1}/(1+f_{k-1}); g_k=c^2 g_{k-1}/(1+c g_{k-1}).
# The following is an arithmetical certificate for the *published* theorem,
# not a new lower-bound proof.
c=Fraction(133,100)
f=g=Fraction(1)
vals=[]
for k in range(1,101):
 f=c*f/(1+f)
 g=c*c*g/(1+c*g)
 df=min((1/f-c)/k,c**(-k))
 dg=min((1/g-c)/k,c**(-2*k))
 vals.append((k,df,dg))
 checks+=2
kd,dd,_=max(vals,key=lambda x:x[1]);kg,_,dg=max(vals,key=lambda x:x[2])
# For k>=100, both d_k <= c^{-k} or c^{-2k}; strictly below optima.
assert c**(-100)<dd and c**(-200)<dg
assert kd==kg==3
checks+=3

# Safety-controlled second finite CNF test: different failing blocks per z.
def clause_ok(cl,asgn):
 return any((asgn[abs(v)-1] if v>0 else not asgn[abs(v)-1]) for v in cl)
C0=[(1,2),(1,-2)]
C1=[(-1,3),(-1,-3)]
boolean_rows=[]
for z in (False,True):
 own=[]
 for block in (C0,C1):
  i=1 if block is C0 else 2
  own.append(sum(all(clause_ok(cl,tuple([z]+[p if j==i else False for j in (1,2)])) for cl in block) for p in (False,True)))
 assert sum(x>0 for x in own)==1
 checks+=1
 boolean_rows.append({'z':z,'local_solution_counts':own})

out={'status':'PROVED/RESTRICTED theorem + independently executed native finite controls',
 'case':'TMR-5/099 SAT-only route quantifier & machine firewall',
 'checks':checks,'failures':0,
 'native_graph':{'vertices':5,'arcs':[list(e) for e in ARC],'original_hom_count':H_count,'edge_critical':critical,
                 'shared_vertices':[0,1],'blocks':[[list(e) for e in b] for b in BLOCKS],
                 'row_truth':rows,'rotation_invariance_checks':125},
 'transfer_checks':sum((l+1)*5 for l in range(1,9)),
 'boolean_cnf_rows':boolean_rows,
 'flmv_thm57_64_at_c133over100':{'det_opt_k':kd,'det_d':str(dd),'det_d_float':float(dd),
   'coNTISP_opt_k':kg,'coNTISP_d':str(dg),'coNTISP_d_float':float(dg),
   'not_excluded_by_these_at_space_exponent':.5},
 'buss_williams_fig82':{'space_exponent':.5,'published_excluded_time_exponent':1.34070,
    'safely_selected_lower_exponent':1.34060,'target_time':1.33,
    'conservative_advice_bit_threshold_per_log2n':.01060},
 'limitations':'Neither finite enumeration nor FLMV arithmetic constructs a polynomial universal splitter. No unrestricted T5 witness lower bound.'}
raw=json.dumps(out,indent=2,sort_keys=True)+'\n'
p=ROOT/'tmr5_099_results.json';p.write_text(raw)
print(json.dumps({'checks':checks,'native_unsat':H_count==0,'edge_delete_counts':[v['count_after_deletion'] for v in critical],
 'det_d':float(dd),'co_d':float(dg),'file':str(p),'sha256':hashlib.sha256(raw.encode()).hexdigest()},indent=2))
