#!/usr/bin/env python3
"""Exact saturated-cycle GF(2) terminal on one authenticated canonical SAT source.

This is a restricted parameterized decision action, NOT a P versus NP proof.
All source scans, cycle discovery, branch construction and GF2 row ops counted
as implementation-proxy work. No FLMV native time/space claims are made.
"""
from itertools import combinations, product
from collections import Counter
from pathlib import Path
import json, math

POS15=[(1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15)]
NEG15=[(1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15)]
F15=tuple(POS15)+tuple(tuple(-x for x in c) for c in NEG15)
P6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
N6=[(1,2,4),(1,3,6),(2,3,5),(4,5,6)]
Y6=tuple(P6)+tuple(tuple(-x for x in c) for c in N6)
P_U=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
P_S=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))

def valid(F):
 if not F: return False
 n=max(abs(l) for c in F for l in c)
 counts=Counter((abs(l),l>0) for c in F for l in c)
 return all(len(c)==3 and len({abs(l) for l in c})==3 and (all(x>0 for x in c) or all(x<0 for x in c)) for c in F) and len(set(tuple(sorted(c)) for c in F))==len(F) and all(counts[v,True]==counts[v,False]==2 for v in range(1,n+1))

def satisfies(F,a):
 return all(any(a[abs(l)]==(1 if l>0 else 0) for l in c) for c in F)

def all_models(F,p):
 n=max(abs(l) for c in F for l in c)
 free=[v for v in range(1,n+1) if v not in p]
 for seq in product((0,1),repeat=len(free)):
  a=dict(p);a.update(zip(free,seq))
  if satisfies(F,a):yield a

def signed_gate(F,p):
 n=max(abs(l) for c in F for l in c)
 free=[v for v in range(1,n+1) if v not in p]
 uclauses=[];covered=[];scans=0
 for j,c in enumerate(F):
  scans+=len(c)
  if any(abs(l) in p and p[abs(l)]==(l>0) for l in c):covered.append(j)
  else:uclauses.append(j)
 s=Counter()
 for j in covered:
  for lit in F[j]:
   if abs(lit) not in p:s[abs(lit),lit>0]+=1
 eta=sum(min(s[v,True],s[v,False]) for v in free)
 preferred={v:(0 if s[v,True]>s[v,False] else 1) for v in free if s[v,True]!=s[v,False]}
 edges=[]
 for j in uclauses:
  r=[abs(lit) for lit in F[j] if abs(lit) not in p]
  if not r: return {'status':'UNSAT_EMPTY','source_clause':j,'checked_literals':scans}
  if len(r)==2:edges.append((j,r[0],r[1]))
 tris=[];candidate_count=0
 for select in combinations(edges,3):
  candidate_count+=1
  deg=Counter(v for j,u,w in select for v in (u,w))
  if len(deg)==3 and set(deg.values())=={2}:
   tris.append(tuple(sorted(j for j,_,_ in select)))
 # Choose a maximum edge-disjoint triangle packing; exact backtracking here
 # is EXPONENTIAL in candidate count and must be charged. Other authenticated
 # packings (not necessarily maximum) are also sound.
 # Polynomial source-authenticated greedy triangle packing: each original
 # binary clause ID can be used once. Unlike maximum packing this has a
 # polynomial acquisition bound on every input.
 best=[];used=set()
 for cyc in sorted(tris):
  if not used.intersection(cyc):
   best.append(cyc)
   used.update(cyc)
 nodes=len(tris)
 best=tuple(best)
 delta=2*len(free)-len(uclauses)-eta-len(best)
 return {'status':'GATE','free':free,'uncovered':uclauses,'covered':covered,'pref':preferred,'eta':eta,'e':2*len(free)-len(uclauses),'nu':len(best),'delta':delta,'cycles':best,'source_clause_scans':len(F),'source_literal_reads':scans,'cycle_candidate_checks':candidate_count,'cycle_search_nodes':nodes}

def gaussian(rows,n):
 """Rows are [mask, rhs, set of original authenticated row IDs]."""
 basis={};steps=0;reads=0
 for mask,rhs,origin in rows:
  reads+=1;orig=set(origin)
  while mask:
   steps+=1
   pivot=mask.bit_length()-1
   if pivot not in basis:
    basis[pivot]=(mask,rhs,orig)
    break
   bm,br,bp=basis[pivot]
   mask^=bm;rhs^=br;orig^=bp
  if mask==0 and rhs:
   return {'consistent':False,'rank':len(basis),'row_xors':steps,'rows':reads,'refutation_sources':sorted(orig)}
 a_bits=0
 for pivot in sorted(basis):
  mask,rhs,_=basis[pivot]
  val=rhs^((mask&a_bits).bit_count()&1)
  if val:a_bits|=1<<pivot
 return {'consistent':True,'rank':len(basis),'row_xors':steps,'rows':reads,'bits':a_bits}

def exact_terminal(F,p,cap=100000):
 if not valid(F):return {'status':'MALFORMED'}
 g=signed_gate(F,p)
 if g['status']=='UNSAT_EMPTY':return g
 if g['delta']<0:return {'status':'UNSAT_GAP','gate':g,'branches':0}
 if g['delta']!=0:return {'status':'UNRESOLVED','gate':g,'branches':0}
 cycles=g['cycles'];covered_ids={j for cyc in cycles for j in cyc}
 base=[];n=max(abs(l) for c in F for l in c)
 def row_from_clause(j):
  clause=F[j];rest=[lit for lit in clause if abs(lit) not in p]
  mask=sum(1<<(abs(x)-1) for x in rest)
  rhs=1 if clause[0]>0 else 1 ^ (len(rest)&1)
  return (mask,rhs,{('clause',j)})
 for j in g['uncovered']:
  if j not in covered_ids:base.append(row_from_clause(j))
 for v,b in g['pref'].items():base.append((1<<(v-1),b,{('pref',v)}))
 cases=math.prod(len(c) for c in cycles)
 if cases>cap:return {'status':'UNRESOLVED_CAP','gate':g,'branch_bound':cases}
 outcomes=[];work=0
 for picks in product(*cycles):
  chosen=set(picks)
  rows=list(base)
  for cyc in cycles:
   for j in cyc:
    c=F[j];rest=[abs(lit) for lit in c if abs(lit) not in p]
    assert len(rest)==2
    if j in chosen:
     for v in rest:rows.append((1<<(v-1),1 if c[0]>0 else 0,{('double',j,v)}))
    else:rows.append(((1<<(rest[0]-1))^(1<<(rest[1]-1)),1,{('xor',j)}))
  result=gaussian(rows,n)
  work+=result['row_xors']+result['rows']
  if result['consistent']:
   witness={v:(result['bits']>>(v-1))&1 for v in range(1,n+1)}
   witness.update(p)
   if not satisfies(F,witness):
    raise AssertionError('AFFINE SAT MODEL FALSE: '+str((g,p,picks,witness)))
   return {'status':'SAT','gate':g,'branches':len(outcomes)+1,'branch_total':cases,'affine_work':work,'selected_edges':picks,'witness':[witness[v] for v in range(1,n+1)],'rank':result['rank']}
  outcomes.append({'selected_edges':picks,'refutation_rows':result['refutation_sources']})
 return {'status':'UNSAT_AFFINE_EXHAUSTED','gate':g,'branches':len(outcomes),'affine_work':work,'branch_refutations':outcomes}

def main():
 result={'mode':'restricted_delta_zero_cycle_affine_terminal','method':'polynomial greedy original-source triangle pack; saturated affine-cycle terminal','corpus':{},'adversarial':{},'counter_examples':[]}
 for name,F,roots in [('Y6',Y6,[{}]),('F15',F15,[P_U,P_S])]:
  assert valid(F)
  counts=Counter();branch_counts=Counter();interesting=[]
  for root in roots:
   free0=[v for v in range(1,max(abs(l) for c in F for l in c)+1) if v not in root]
   for states in product((-1,0,1),repeat=len(free0)):
    p={**root,**{v:s for v,s in zip(free0,states) if s!=-1}}
    res=exact_terminal(F,p)
    brute=bool(next(all_models(F,p),None))
    if res['status'] in ('SAT','UNSAT_GAP','UNSAT_EMPTY','UNSAT_AFFINE_EXHAUSTED'):
     assert (res['status']=='SAT')==brute,(name,p,res,brute)
     counts['correctly_decided']+=1
    else:counts['unresolved']+=1
    counts['total']+=1
    counts[res['status']]+=1
    if res.get('gate',{}).get('delta')==0:
     branch_counts[res['status']]+=1
     if len(interesting)<5:interesting.append({'p':p,'label':brute,'status':res['status'],'nu':res['gate']['nu'],'branches':res.get('branches'),'total_picks':res.get('branch_total')})
  result['corpus'][name]={'counters':dict(counts),'saturated':dict(branch_counts),'examples':interesting,'models_full':sum(1 for _ in all_models(F,{}))}
 # run identity/malformed cases
 for invalid in [(),((1,1,2),),((1,2,3),(1,2,3)),((1,-2,3),),((1,2,3),),((1,2,3),(-1,-2,-3))]:
  assert exact_terminal(invalid,{})['status']=='MALFORMED'
 result['adversarial']['malformed_rejected']=6
 u=exact_terminal(F15,P_U);s=exact_terminal(F15,P_S)
 assert u['status']=='UNSAT_GAP' and s['status']=='SAT'
 result['adversarial']['F15_unsat_cube']={'status':u['status'],'delta':u['gate']['delta']}
 result['adversarial']['F15_sat_cube']={'status':s['status'],'delta':s['gate']['delta'],'cycles':s['gate']['cycles'],'branch_total':s['branch_total'],'chosen_edges':s['selected_edges'],'rank':s['rank'],'witness':s['witness']}
 dest=Path(__file__).resolve().parent / 'saturated_cycle_affine_terminal_greedy_results.json'
 dest.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'source':{k:v['counters'] for k,v in result['corpus'].items()},'F15':result['adversarial'],'out':str(dest)},indent=2))



# ARC-DEFECT-SATURATION299. This extension is a source-authenticated
# small-positive-delta XP terminal; it does not create canonical children.
# It retains the producer's earlier valid/signed_gate/gaussian helpers.
def defect_affine_terminal299(F,p,max_delta=2,cap=100000):
 if not valid(F):return {'status':'MALFORMED'}
 g=signed_gate(F,p)
 if g['status']=='UNSAT_EMPTY':return {'status':'UNSAT_EMPTY','source_clause':g['source_clause']}
 d=g['delta']
 if d<0:return {'status':'UNSAT_BUDGET','delta':d}
 if d>max_delta:return {'status':'UNRESOLVED_BUDGET','delta':d}
 n=max(abs(l) for c in F for l in c)
 free=g['free']
 active={j:tuple(l for l in F[j] if abs(l) not in p) for j in g['uncovered']}
 cycles=g['cycles']
 cycle_ids={j for cyc in cycles for j in cyc}
 work=Counter();count=0;count_models=0;first=None;rejected=0;row_certs=[]
 def odd(rest,ref):
  mask=0;rhs=1
  for l in rest:mask^=1<<(abs(l)-1);rhs^=int(l<0)
  return (mask,rhs,{ref})
 def fixed(l,v,ref):
  return (1<<(abs(l)-1),int(v)^int(l<0),{ref})
 for bases in product(*cycles):
  work['cycle_bases']+=1
  base=[];groups=[]
  for ci,(cyc,j0) in enumerate(zip(cycles,bases)):
   for j in cyc:
    rest=active[j]
    if j==j0:
     base.extend(fixed(l,1,('base',ci,j,abs(l))) for l in rest)
    elif j<j0:base.append(odd(rest,('before',ci,j)))
    else:groups.append([
      (0,[odd(rest,('cycle_one',ci,j))]),
      (1,[fixed(l,1,('cycle_double',ci,j,abs(l))) for l in rest])])
  for j in g['uncovered']:
   if j in cycle_ids:continue
   rest=active[j]
   opts=[(0,[odd(rest,('outside_odd',j))])]
   if len(rest)==2:opts.append((1,[fixed(l,1,('outside_double',j,abs(l))) for l in rest]))
   elif len(rest)==3:
    for k in range(3):
     opts.append((1,[fixed(l,int(i!=k),('outside_two',j,k,i)) for i,l in enumerate(rest)]))
    opts.append((2,[fixed(l,1,('outside_triple',j,abs(l))) for l in rest]))
   groups.append(opts)
  for v,b in g['pref'].items():
   pos=sum(v in F[j] for j in g['covered'])
   neg=sum(-v in F[j] for j in g['covered'])
   w=abs(pos-neg)
   groups.append([(0,[fixed(v,b,('pref',v))]),
                  (w,[fixed(v,1-b,('mismatch',v))])])
  def descend(i,remaining,rows):
   nonlocal count,count_models,first,rejected
   work['ticket_nodes']+=1
   if i==len(groups):
    if remaining: return
    count+=1
    if count>cap:return
    z=gaussian(rows,n);work['row_xors']+=z['row_xors'];work['rows']+=z['rows']
    if z['consistent']:
     a={v:(z['bits']>>(v-1))&1 for v in range(1,n+1)}
     a.update(p)
     if not satisfies(F,a):raise AssertionError(('false-SAT-model',p,bases,a))
     count_models+=1<<(len(free)-z['rank'])
     if first is None:first=[a[v] for v in range(1,n+1)]
    else:
     rejected+=1
     if len(row_certs)<4:row_certs.append(z['refutation_sources'])
    return
   for cost,rs in groups[i]:
    work['policy_checks']+=1
    if cost<=remaining:descend(i+1,remaining-cost,rows+rs)
  descend(0,d,base)
  if count>cap:return {'status':'UNRESOLVED_CAP','systems_visited':count,'work':dict(work)}
 return {'status':'SAT' if first is not None else 'UNSAT_AFFINE_EXHAUSTED',
         'delta':d,'cycles':cycles,'systems':count,'models':count_models,
         'witness':first,'row_XOR_refutations':rejected,
         'refutation_provenance_sample':row_certs,
         'work':dict(work),'source_reads':g['source_literal_reads'],
         'triangle_checks':g['cycle_candidate_checks'],
         'guest_calls':0,'canonical_children':0,
         'native_FLMV_tape_costs':'UNMEASURED'}

# Exactly the same original valid 9-variable source yields opposite labels
# when x1 changes, with delta=0 and delta=2 respectively.
F9_299=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
        (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
P9_U299={8:0,3:0,7:0,6:0,1:1,5:1}
P9_S299={**P9_U299,1:0}
def main299():
 assert valid(F9_299)
 checks={}
 for name,F,p in [('F9_UNSAT',F9_299,P9_U299),
                  ('F9_SAT_flip_x1',F9_299,P9_S299),
                  ('Y6_delta2',Y6,{4:0,6:1}),
                  ('F15_SAT',F15,P_S),
                  ('F15_UNSAT',F15,P_U)]:
  z=defect_affine_terminal299(F,p)
  truth=bool(next(all_models(F,p),None))
  assert z['status'] in ('SAT','UNSAT_AFFINE_EXHAUSTED','UNSAT_BUDGET')
  assert (z['status']=='SAT')==truth,(name,z)
  checks[name]={'truth':'SAT' if truth else 'UNSAT','status':z['status'],
                'delta':z.get('delta'),'systems':z.get('systems'),
                'count':z.get('models'),'work':z.get('work')}
 print(json.dumps({'status':'PASS','theorem':'restricted positive-defect exact affine union',
                   'checks':checks,'P_vs_NP':'OPEN'},indent=2,sort_keys=True))
if __name__=='__main__':main299()
