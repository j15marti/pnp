#!/usr/bin/env python3
"""BALANCED-TWO-COORD249. Exact source-indexed clause extrema and local-log
radius polynomial in generic 4-coordinate and balanced-sign 2-coordinate rings.
Standard-library producer. Requires networkx for no operation: matching is
not used.  Execute: python SCRIPT [output.json]
No equity/valuation scores, no SAT-answer oracle in compiler.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from time import perf_counter
from pathlib import Path
import json, hashlib, random, sys, tracemalloc, math

W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
S15='-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'

def parse(s):return tuple(tuple(map(int,z.split())) for z in s.split(';'))
def nvars(F):return max(abs(x) for c in F for x in c)
def signed_degree(F):
 z=Counter(x for c in F for x in c)
 return [tuple((z[i],z[-i])) for i in range(1,nvars(F)+1)]
def balanced(F):return all(a==b for a,b in signed_degree(F))
def strict22(F):
 return balanced(F) and all(a==2 for a,b in signed_degree(F)) and all(len(c)==3 and len(set(map(abs,c)))==3 for c in F)
def connected(F):
 n=nvars(F);g={i:set() for i in range(1,n+1)}
 for c in F:
  for i,j in combinations([abs(z) for z in c],2):g[i].add(j);g[j].add(i)
 seen={1};queue=[1]
 for v in queue:
  for j in g[v]-seen:seen.add(j);queue.append(j)
 return len(seen)==n

def true_count(F,a):return [sum((a[abs(z)]==int(z>0)) for z in c) for c in F]
def nvec(F,a):
 t=true_count(F,a);return tuple(t.count(i) for i in range(4))
def assignment(n,flips=(),anchor=0):
 f=set(flips);return {i:(anchor ^ int(i in f)) for i in range(1,n+1)}
def witness(F,a):return nvec(F,a)[0]==0

def audit(F,tag):
 n=nvars(F);m=len(F);ext=[]
 for j,c in enumerate(F,1):
  occ=[]
  for lit in c:
   occ.append({'x_i_j':[abs(lit),j],'signed_source_literal':lit,'polarity':'+' if lit>0 else '-',
               'S_j_all_literals_true':int(lit>0),'invert_S_j_U_j':int(lit<0),
               'U_j_all_literals_false':int(lit<0),'invert_U_j_S_j':int(lit>0)})
  ext.append({'source_clause_index':j,'signed_literals':list(c),'occurrences':occ,
              'S_j':{str(abs(z)):int(z>0) for z in c},
              'invert_S_j':{str(abs(z)):int(z<0) for z in c},
              'U_j':{str(abs(z)):int(z<0) for z in c},
              'invert_U_j':{str(abs(z)):int(z>0) for z in c}})
 pairs=[];checks=0
 for j,k in combinations(range(m),2):
  p={abs(z):int(z>0) for z in F[j]};q={abs(z):int(z>0) for z in F[k]}
  same=sorted(i for i in p.keys() & q.keys() if p[i]==q[i]);opp=sorted(i for i in p.keys() & q.keys() if p[i]!=q[i])
  modes={'SS':not bool(opp),'SU':not bool(same),'US':not bool(same),'UU':not bool(opp)}
  scope=sorted(p.keys()|q.keys());actual=dict.fromkeys(modes,False);both_disjunctions_sat=False
  for b in product((0,1),repeat=len(scope)):
   a=dict(zip(scope,b));t1=sum(a[abs(z)]==int(z>0) for z in F[j]);t2=sum(a[abs(z)]==int(z>0) for z in F[k]);
   x=('S' if t1==len(F[j]) else 'U' if t1==0 else 'M')+('S' if t2==len(F[k]) else 'U' if t2==0 else 'M')
   if t1>0 and t2>0:both_disjunctions_sat=True
   if x in actual:actual[x]=True
   checks+=1
  assert modes==actual, (tag,j,k,modes,actual)
  pairs.append({'source_clause_pair':[j+1,k+1], 'same_polarity_shared':same,'opposite_polarity_shared':opp,
    'SS_SU_US_UU':modes,'both_original_disjunctions_may_be_SAT':both_disjunctions_sat,
    'forced_one_middle_clause':not any(modes.values())})
 trails={}
 for anchor in (0,1):
  base=assignment(n,anchor=anchor);seq=[(),(1,),(1,2),(1,2,3),(1,2,3,4),tuple(range(1,min(n,7)+1))]
  rows=[]
  for S in seq:
   a=assignment(n,S,anchor);t=true_count(F,a);v=nvec(F,a)
   ca={i:1-a[i] for i in a}
   if all(len(c)==3 for c in F):assert nvec(F,ca)==v[::-1]
   rows.append({'flipped_original_variables':list(S),'assignment':''.join(str(a[i]) for i in range(1,n+1)),
    'per_original_clause_true_literal_counts':t,'N0_N1_N2_N3':list(v),'original_formula_SAT':v[0]==0,
    'complement_N0_N1_N2_N3':list(nvec(F,ca))})
  trails[str(anchor)+'^n']=rows
 forbidden=[]
 for j,k in combinations(range(m),2):
  for pivot in sorted({abs(x) for x in F[j]}&{abs(x) for x in F[k]}):
   sj=next(x>0 for x in F[j] if abs(x)==pivot);sk=next(x>0 for x in F[k] if abs(x)==pivot)
   if sj==sk:continue
   raw=[z for z in F[j]+F[k] if abs(z)!=pivot]
   if any(-z in raw for z in raw):continue
   R=tuple(dict.fromkeys(raw));cube={abs(z):int(z<0) for z in R}
   if len(cube)!=len(R):continue
   # Parent-based proof: under negated resolvent, two parents demand opposite pivot values.
   assert all(not any((cube[abs(z)]==int(z>0)) for z in parent if abs(z)!=pivot) for parent in (F[j],F[k]))
   forbidden.append({'parent_indices':[j+1,k+1],'pivot_original_variable':pivot,'resolvent':list(R),
                     'forbidden_original_variable_cube':{str(i):b for i,b in cube.items()},
                     'proof':'Both source parents become opposite singleton pivot demands on this cube.'})
   if len(forbidden)>=6:break
  if len(forbidden)>=6:break
 return {'case':tag,'n':n,'m':m,'signed_occurrences':ext,'pair_matrix':pairs,
         'pair_mode_coherent_enumerations':checks,'coherent_endpoint_and_flip_trails':trails,
         'source_parent_non_tautological_resolvents':forbidden,
         'strict_signed_exact22':strict22(F),'balanced_per_original_variable':balanced(F),
         'primal_connected':connected(F)}

class Work:
 def __init__(self):self.ops=Counter()
 def inc(self,key,num=1):self.ops[key]+=num

# A polynomial is indexed (t degree, Laurent deltas...) -> exact rational coefficient.
def poly_mul(A,B,r,w):
 out=defaultdict(Fraction)
 for (i,*da),av in A.items():
  for (j,*db),bv in B.items():
   w.inc('polynomial_term_pairs')
   if i+j>r:continue
   key=(i+j,)+tuple(x+y for x,y in zip(da,db));out[key]+=av*bv
 return {k:v for k,v in out.items() if v}

def poly_log(P,r,dim,w):
 zero=(0,)+(0,)*dim;q={key:c for key,c in P.items() if key!=zero};power={zero:Fraction(1)};result=defaultdict(Fraction)
 for k in range(1,r+1):
  power=poly_mul(power,q,r,w)
  coeff=Fraction(1 if k%2 else -1,k)
  for key,c in power.items():result[key]+=coeff*c;w.inc('polynomial_log_terms')
 return {k:v for k,v in result.items() if v}

def poly_exp(L,r,dim,w):
 zero=(0,)+(0,)*dim;E={0:{(0,)*dim:Fraction(1)}}
 # Direct recurrence k E_k = sum_{j=1}^k j L_j E_{k-j}.
 bydeg={k:{tuple(a):v for (d,*a),v in L.items() if d==k} for k in range(1,r+1)}
 for k in range(1,r+1):
  acc=defaultdict(Fraction)
  for j in range(1,k+1):
   for a,va in bydeg[j].items():
    for b,vb in E[k-j].items():
     w.inc('polynomial_exp_term_pairs');acc[tuple(x+y for x,y in zip(a,b))]+=Fraction(j,k)*va*vb
  E[k]={k0:v for k0,v in acc.items() if v}
 return E

def connected_subsets(g,r,w):
 starts=[frozenset((i,)) for i in g];stack=starts[:];seen=set();out=[]
 while stack:
  H=stack.pop();w.inc('connected_subset_pop')
  if H in seen:continue
  seen.add(H);out.append(H)
  if len(H)==r:continue
  adj=set().union(*(g[v] for v in H))-set(H)
  for v in adj:stack.append(H|{v});w.inc('connected_subset_expansion')
 out.sort(key=lambda z:(len(z),tuple(sorted(z))));return out

def compile_spectrum(F,anchor,r,dim):
 assert dim in (1,2,4)
 if dim==2:assert balanced(F) and all(len(c)==3 for c in F), 'the two-coordinate theorem REQUIRES width-three original-sign balance'
 n=nvars(F);m=len(F);w=Work();base=assignment(n,anchor=anchor);Nbase=nvec(F,base)
 g={i:set() for i in range(1,n+1)};inc={i:set() for i in range(1,n+1)}
 for ci,c in enumerate(F):
  w.inc('source_clause_scan')
  for z in c:inc[abs(z)].add(ci);w.inc('source_literal_scan')
  for i,j in combinations([abs(z) for z in c],2):g[i].add(j);g[j].add(i)
 connected=connected_subsets(g,r,w);deltas={frozenset():tuple([0]*dim)};log_cache={frozenset():{}}
 def delta(S):
  if S in deltas:return deltas[S]
  touched=set().union(*(inc[x] for x in S))
  # Value derivation uses unchanged source variables, not separate occurrence variables.
  a=dict(base)
  for i in S:a[i]^=1
  changes=[0]*4
  for j in touched:
   w.inc('touched_source_clause_rechecks')
   old=sum(base[abs(z)]==int(z>0) for z in F[j]);new=sum(a[abs(z)]==int(z>0) for z in F[j]);w.inc('touched_original_literals',6)
   changes[old]-=1;changes[new]+=1
  ans=tuple((changes[0],) if dim==1 else (changes[0],changes[3]) if dim==2 else changes)
  if dim==2:assert changes[1]==-2*changes[0]+changes[3] and changes[2]==changes[0]-2*changes[3]
  deltas[S]=ans;return ans
 def local_log(U):
  if U in log_cache:return log_cache[U]
  zz=(0,)+(0,)*dim;P={zz:Fraction(1)};us=sorted(U)
  for t in range(1,len(us)+1):
   for small in combinations(us,t):
    D=delta(frozenset(small));P[(t,)+D]=P.get((t,)+D,Fraction(0))+1;w.inc('local_subset_coefficient')
  L=poly_log(P,r,dim,w);log_cache[U]=L;return L
 global_L=defaultdict(Fraction)
 for H in connected:
  v=sorted(H)
  contribution=defaultdict(Fraction)
  for t in range(len(v)+1):
   for small in combinations(v,t):
    U=frozenset(small);sign=(-1)**(len(H)-len(U))
    for key,num in local_log(U).items():
     contribution[key]+=sign*num;w.inc('mobius_sum_terms')
  for key,c in contribution.items():
   if c:global_L[key]+=c;w.inc('connected_log_terms')
 global_L={k:v for k,v in global_L.items() if v}
 E=poly_exp(global_L,r,dim,w)
 radius={tuple(Nbase[i]+D[i] for i in range(4)):int(c) for D,c in E[r].items()} if dim==4 else {}
 if dim==1:
  for (d0,),v in E[r].items():
   assert v.denominator==1
   radius[(Nbase[0]+d0,)]=int(v)
 if dim==2:
  for (d0,d3),v in E[r].items():
   d1=-2*d0+d3;d2=d0-2*d3
   nv=(Nbase[0]+d0,Nbase[1]+d1,Nbase[2]+d2,Nbase[3]+d3)
   assert all(k>=0 for k in nv),(nv,r)
   assert v.denominator==1
   radius[nv]=int(v)
 else:
  assert all(v.denominator==1 for v in E[r].values())
 assert sum(radius.values())==math.comb(n,r),(n,r,dim,sum(radius.values()))
 return {'histogram':{'/'.join(map(str,k)):v for k,v in sorted(radius.items())},
   'sat_count_at_radius':sum(v for k,v in radius.items() if k[0]==0),
   'method':'connected_log_'+str(dim)+'D','n':n,'m':m,'r':r,
   'connected_source_supports':len(connected),'cached_source_deltas':len(deltas),
   'formal_laurent_monomials':sum(len(v) for v in E.values()),
   'source_base_vector':Nbase,'work':dict(w.ops)}

def explicit_radius(F,anchor,r):
 n=nvars(F);hist=Counter();checks=0;sat_first=None
 for flip in combinations(range(1,n+1),r):
  a=assignment(n,flip,anchor);v=nvec(F,a);hist[v]+=1;checks+=1
  if sat_first is None and v[0]==0:sat_first=list(flip)
 return {'histogram':{'/'.join(map(str,k)):v for k,v in sorted(hist.items())},
         'sat_count_at_radius':sum(v for k,v in hist.items() if k[0]==0),'explicit_candidates':checks,
         'source_literal_checks':checks*3*len(F),'first_witness_flips':sat_first}

def unit_propagate(F,partial,work):
 a=dict(partial);inferences=[]
 while True:
  changed=False
  for ci,c in enumerate(F,1):
   work.inc('up_clause_scans');remaining=[];valid=False
   for z in c:
    work.inc('up_literal_checks')
    if abs(z) in a:
     if a[abs(z)]==int(z>0):valid=True;break
    else:remaining.append(z)
   if valid:continue
   if not remaining:return None,inferences,ci
   if len(remaining)==1:
    lit=remaining[0];i=abs(lit);value=int(lit>0)
    if i in a and a[i]!=value:return None,inferences,ci
    if i not in a:a[i]=value;inferences.append({'source_clause':ci,'forced_variable':i,'forced_value':value});work.inc('up_forced_literals');changed=True
  if not changed:return a,inferences,None

def dpll(F,work):
 n=nvars(F);nodes=0;leaves=[]
 def search(partial,branch_path):
  nonlocal nodes
  nodes+=1;work.inc('search_nodes')
  a,units,conf=unit_propagate(F,partial,work)
  if a is None:
   leaves.append({'branch_path':list(branch_path),'unit_deductions':units,'conflicting_source_clause':conf});return None
  if len(a)==n:
   if witness(F,a):return a
   raise AssertionError('unit propagation missed an original source clause')
  i=next(i for i in range(1,n+1) if i not in a)
  for value in (0,1):
   work.inc('branch_attempts');nxt=dict(a);nxt[i]=value
   ans=search(nxt,branch_path+[(i,value)])
   if ans is not None:return ans
  return None
 result=search({},[])
 if result is None:
  for leaf in leaves:
   direct={i:v for i,v in leaf['branch_path']};res,_,con=unit_propagate(F,direct,Work())
   assert res is None and con is not None
 return {'SAT':result is not None,'witness':''.join(str(result[i]) for i in range(1,n+1)) if result else None,
         'visited_states':nodes,'UNSAT_conflict_leaves':leaves if result is None else [],
         'work':dict(work.ops)}

def measure(fn):
 tracemalloc.start();t=perf_counter();out=fn();elapsed=perf_counter()-t;_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
 out['elapsed_s']=elapsed;out['peak_tracemalloc_bytes']=peak;return out

def random_formula(n,m,seed):
 rng=random.Random(seed)
 return tuple(tuple((1 if rng.random()<0.5 else -1)*x for x in rng.sample(range(1,n+1),3)) for _ in range(m))

def phase_rename(F):
 n=nvars(F);return tuple(tuple((1 if z>0 else -1)*(-1 if abs(z)%3==0 else 1)*(n+1-abs(z)) for z in c) for c in reversed(F))

def xor3(even):
 # 4-clause encoding of xor_3=even/odd; counts each variable exactly +2,-2.
 return tuple(tuple((i+1) if bits[i]==0 else -(i+1) for i in range(3)) for bits in product((0,1),repeat=3) if sum(bits)%2==int(even))

def main(path):
 cases=[('W1_STRICT22_UNSAT',parse(W1)),('S15_STRICT22_SAT',parse(S15)),
        ('W1_SIGN_PERMUTATION',phase_rename(parse(W1))),('XOR3_AFFINE',xor3(False)),
        ('2SAT_SAT',((1,2),(-1,2),(1,-2))),('2SAT_UNSAT',((1,2),(-1,2),(1,-2),(-1,-2))),
        ('HORN',((-1,-2,3),(-3,4),(-4,5),(1,), (2,))),
        ('DENSE_RANDOM',random_formula(8,20,249))]
 results={'run':'LSPV-2_BALANCED_TWO_COORD249','timestamp':'2026-10-30 04:13 America/Los_Angeles',
          'status':'PROVED/EXACT restricted identity; computational controlled local-log comparisons; independent referee pending',
          'environment':{'python':sys.version,'seed':249,'machine':'Python dictionary/Fraction selected operations, RAM conceptual proof only'},
          'cases':[]}
 for tag,F in cases:
  n=nvars(F);a=audit(F,tag);row={'name':tag,'source_CNF':F,'audit':a,
       'source_sha256':hashlib.sha256(str(F).encode()).hexdigest(),
       'source_n':n,'source_m':len(F),'balanced_formula':balanced(F),'strict22':strict22(F),'connected':connected(F)}
  row['solver_baseline']=measure(lambda:dpll(F,Work()))
  if balanced(F) and all(len(c)==3 for c in F) and n<=15:
   row['radius_tests']=[]
   for r in ((2,3) if n>=8 else (1,2)):
    for anchor in ((0,1) if n>=8 else (0,)):
     direct=measure(lambda:explicit_radius(F,anchor,r))
     p1=measure(lambda:compile_spectrum(F,anchor,r,1))
     p2=measure(lambda:compile_spectrum(F,anchor,r,2))
     p4=measure(lambda:compile_spectrum(F,anchor,r,4))
     assert direct['histogram']==p2['histogram']==p4['histogram'],(tag,r,anchor)
     assert direct['sat_count_at_radius']==p1['sat_count_at_radius']
     marginal=Counter()
     for key,num in direct['histogram'].items():marginal[key.split('/')[0]]+=num
     assert p1['histogram']==dict(marginal),(tag,r,anchor)
     row['radius_tests'].append({'anchor':anchor,'radius':r,'explicit':direct,'one_coordinate_SAT_only':p1,'two_coordinate':p2,'four_coordinate':p4})
   # Uniform controller pays an unsuccessful compiler first and then pays a source-aware baseline.
   def hybrid():
    p=compile_spectrum(F,0,2,2);w=Work();ans=dpll(F,w);ans['compiler_work']=p['work'];return ans
   row['solver_hybrid']=measure(hybrid)
  results['cases'].append(row)
  print(tag,'n=',n,'m=',len(F),'UP-DPLL nodes=',row['solver_baseline']['visited_states'],
        'hist_tests=',len(row.get('radius_tests',[])),flush=True)
 Path(path).write_text(json.dumps(results,indent=2,default=list)+'\n')
 print('saved',path,'bytes',Path(path).stat().st_size)

if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else '/mnt/data/pnp_run249/run249_raw.json')