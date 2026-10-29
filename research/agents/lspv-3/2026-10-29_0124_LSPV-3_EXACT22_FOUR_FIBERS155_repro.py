#!/usr/bin/env python3
"""LSPV-3 EXACT22 FOUR FIBERS155. No external packages/network.
Audits all four exact one-variable projections on a common connected proper
strict signed (2,2)-3CNF scope and proof-carrying conditional UNSAT.
This is finite evidence and an elementary reduction, not a P-vs-NP solution.
"""
from collections import Counter,defaultdict
from itertools import product
from pathlib import Path
import random,json,hashlib

U_STR='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
S_STR='-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'

def parse(s):return tuple(tuple(map(int,x.split())) for x in s.split(';'))
def check(cond,msg):
 global CHECKS
 CHECKS+=1
 if not cond:raise AssertionError(msg)
CHECKS=0

def exact22(F,n):
 counts=Counter(l for c in F for l in c)
 return (len(F)*3==4*n and all(len(c)==3 and len({abs(l) for l in c})==3 for c in F)
    and all(counts[i]==counts[-i]==2 for i in range(1,n+1))
    and len(set(tuple(sorted(c)) for c in F))==len(F))

def connected(F,n):
 v2c=[[] for _ in range(n+1)]
 for ci,c in enumerate(F):
  for lit in c:v2c[abs(lit)].append(ci)
 seenV={1};seenC=set();stack=[1]
 while stack:
  v=stack.pop()
  for ci in v2c[v]:
   if ci not in seenC:
    seenC.add(ci)
    for lit in F[ci]:
     w=abs(lit)
     if w not in seenV:seenV.add(w);stack.append(w)
 return len(seenV)==n and len(seenC)==len(F)

def holds(F,a):
 return all(any((((a>>(abs(l)-1))&1)==int(l>0)) for l in c) for c in F)

def brute_fiber(F,n,y):
 total=0;proj=0;first=None
 for a in range(1<<n):
  if holds(F,a):
   total+=1;proj|=1<<((a>>(y-1))&1)
   if first is None:first=a
 return proj,total,first

def bitset_support(n):
 full=(1<<(1<<n))-1
 litmask={}
 for v in range(1,n+1):
  positive=sum(1<<a for a in range(1<<n) if (a>>(v-1))&1)
  litmask[v]=positive
  litmask[-v]=full^positive
 return litmask,full

def bitset_profile(F,n,litmask,full):
 sats=full
 for c in F:
  sats &= litmask[c[0]]|litmask[c[1]]|litmask[c[2]]
 fibers={}
 for v in range(1,n+1):
  bits=int(bool(sats & litmask[-v])) | (int(bool(sats & litmask[v]))<<1)
  fibers[v]=bits
 return sats.bit_count(),fibers

def swapped(F, swaps):
 out=[list(c) for c in F]
 for i,j in swaps:out[i][j]=-out[i][j]
 return tuple(tuple(c) for c in out)

def canonical(c):
 a=set(c)
 if any(-x in a for x in a):return None
 return tuple(sorted(a,key=lambda z:(abs(z),z<0)))
def resolvent(A,B,p):
 if p not in A or -p not in B:raise ValueError('Bad resolution pivot')
 return canonical([v for v in A if v!=p]+[v for v in B if v!=-p])

def minfill(F,n):
 g={i:set() for i in range(1,n+1)}
 for c in F:
  for x in map(abs,c):g[x].update(set(map(abs,c))-{x})
 order=[]
 while g:
  def priority(x):
   ns=g[x];missing=sum(v not in g[u] for u in ns for v in ns if u!=v)//2
   return (missing,len(ns),x)
  x=min(g,key=priority);ns=set(g[x]);order.append(x)
  for u in ns:g[u].discard(x);g[u].update(ns-{u})
  del g[x]
 return order

def refute_with_unit(F,n,y,sign):
 # source IDs m+1: a unit hypothesis sign*y. Every resolution step is recorded.
 initial=tuple(F)+((sign*y,),)
 db={i:canonical(c) for i,c in enumerate(initial,1)}
 active=set(db);ids={c:i for i,c in db.items()}
 steps=[];pairs=0;peak=len(active);width=0
 for x in minfill(initial,n):
  pos=[i for i in sorted(active) if x in db[i]]
  neg=[i for i in sorted(active) if -x in db[i]]
  width=max(width,len({abs(v) for i in pos+neg for v in db[i]})-1 if pos or neg else 0)
  nxt={i for i in active if i not in pos and i not in neg}
  for i in pos:
   for j in neg:
    pairs+=1
    c=resolvent(db[i],db[j],x)
    if c is None:continue
    if c in ids:nxt.add(ids[c]);continue
    idx=len(db)+1;db[idx]=c;ids[c]=idx;nxt.add(idx)
    steps.append({'id':idx,'parents':[i,j],'pivot':x,'clause':list(c)})
  active=nxt;peak=max(peak,len(active))
  if () in ids:break
 if () not in ids:return {'label':'SAT','pairs':pairs,'derived':len(steps),'width':width,'peak_live':peak}
 # Replay from scratch (no solver internal active set trusted).
 checkdb={i:canonical(c) for i,c in enumerate(initial,1)}
 for s in steps:
  p,q=s['parents'];v=s['pivot'];c=tuple(s['clause'])
  check(s['id'] not in checkdb and p in checkdb and q in checkdb,'source parents must exist')
  check(resolvent(checkdb[p],checkdb[q],v)==c,'each derived clause authentic')
  checkdb[s['id']]=c
 check(any(c==() for c in checkdb.values()),'refutation must derive empty clause')
 return {'label':'UNSAT','pairs':pairs,'derived':len(steps),'width':width,'peak_live':peak,
         'source_count':len(initial),'last_empty_id':ids[()],
         'trace_sha256':hashlib.sha256(json.dumps(steps,sort_keys=True).encode()).hexdigest(),
         'steps':steps}

def verify_resolution_trace(F,unit,steps):
 # Independent replay: only source clauses, an explicit assumption and given trace.
 try:
  db={i:canonical(c) for i,c in enumerate(tuple(F)+(tuple(unit),),1)}
  for s in steps:
   idx=s['id'];p,q=s['parents'];pivot=s['pivot'];new=tuple(s['clause'])
   if idx in db or idx<=len(F)+1 or p not in db or q not in db:return False
   if canonical(new)!=new or resolvent(db[p],db[q],pivot)!=new:return False
   db[idx]=new
  return () in db.values()
 except (ValueError,TypeError,KeyError,IndexError):return False

def guard():
 # All clauses mixed; each of the three variables occurs twice with both signs.
 return ((-1,2,3),(1,-2,3),(-1,2,-3),(1,-2,-3))

def main():
 U,S=parse(U_STR),parse(S_STR);n=15;y=13
 # Swap exactly one positive and one negative occurrence of x1, maintaining exact22.
 L0=swapped(U,((7,0),(19,0)))
 # Complement one variable's occurrences. Satisfaction assignments biject under x13->not x13.
 L1=tuple(tuple(-v if abs(v)==13 else v for v in c) for c in L0)
 variants={'empty_U':U,'zero_L0':L0,'one_L1':L1,'full_S':S}
 probs={};firsts={}
 for tag,F in variants.items():
  check(exact22(F,n),tag+' strict22')
  check(connected(F,n),tag+' connected')
  check(tuple(tuple(map(abs,c)) for c in F)==tuple(tuple(map(abs,c)) for c in U),tag+' same ordered unsigned scopes')
  p,num,w=brute_fiber(F,n,y)
  probs[tag]={'projection_bitmask':p,'sat_assignments':num,'first_witness_mask':w}
  firsts[tag]=w
 check({tag:v['projection_bitmask'] for tag,v in probs.items()}=={'empty_U':0,'zero_L0':1,'one_L1':2,'full_S':3},'four exact tables on identical support')
 # Exhaustive independent fiber-specific checks using full assignments, no cached masks.
 for tag,F in variants.items():
  for b in (0,1):
   found=any(holds(F,a) for a in range(1<<n) if ((a>>(y-1))&1)==b)
   check(found==bool(probs[tag]['projection_bitmask']&(1<<b)),'independent fiber enumeration')
 # Every one-variable balanced swap around U. Count SAT and frozen variables.
 occ=defaultdict(lambda:{1:[],0:[]})
 for ci,c in enumerate(U):
  for li,v in enumerate(c):occ[abs(v)][int(v>0)].append((ci,li))
 litmask,full=bitset_support(n)
 neigh=[]
 for v in range(1,n+1):
  for p,q in product(occ[v][1],occ[v][0]):
   F=swapped(U,(p,q))
   check(exact22(F,n),'one-swap exact22')
   nw,fibers=bitset_profile(F,n,litmask,full)
   forced=[[z,bits] for z,bits in fibers.items() if bits in (1,2)]
   neigh.append({'source_variable':v,'positions':[list(p),list(q)],'sat_assignments':nw,'frozen':forced})
 check(len(neigh)==60 and all(t['sat_assignments']>0 for t in neigh),'all sixty U adjacent sign swaps SAT')
 # Authenticated source resolution for the two forbidden fibers. Neither result is
 # a general certificate-acquisition guarantee, just explicit restricted cases.
 proof0=refute_with_unit(L0,n,y,+1)
 proof1=refute_with_unit(L1,n,y,-1)
 proofU0=refute_with_unit(U,n,y,-1)
 proofU1=refute_with_unit(U,n,y,+1)
 check(all(r['label']=='UNSAT' for r in (proof0,proof1,proofU0,proofU1)),'all four forbidden fibers refuted')
 for ff,unit,trace in ((L0,(y,),proof0),(L1,(-y,),proof1),(U,(-y,),proofU0),(U,(y,),proofU1)):
  check(verify_resolution_trace(ff,unit,trace['steps']),'separate authenticated verifier')
 # Reject tampered resolvent, pivot, and source IDs without trusting construction.
 tamper=json.loads(json.dumps(proof0['steps']))
 tamper[0]['clause'][0] = -tamper[0]['clause'][0]
 check(not verify_resolution_trace(L0,(y,),tamper),'tampered clause rejected')
 tamper=json.loads(json.dumps(proof0['steps']))
 tamper[0]['parents'][0]=9999
 check(not verify_resolution_trace(L0,(y,),tamper),'tampered parent rejected')
 tamper=json.loads(json.dumps(proof0['steps']))
 tamper[0]['pivot']=-tamper[0]['pivot']
 check(not verify_resolution_trace(L0,(y,),tamper),'tampered pivot rejected')
 for tag,F in variants.items():
  for b in (0,1):
   if probs[tag]['projection_bitmask']&(1<<b):
    witness=next(a for a in range(1<<n) if ((a>>(y-1))&1)==b and holds(F,a))
    check(holds(F,witness),'fiber SAT witness authenticated against original clauses')
  
 # Small balanced guard and many-one translation within the *general* strict22 class.
 H=guard();check(exact22(H,3),'guard exact22')
 check(brute_fiber(H,3,1)[0]==3,'guard both fiber values')
 check(all(any(l<0 for l in c) and any(l>0 for l in c) for c in H),'mixed guard clauses')
 # Guard occupies new variables shifted beyond F, with boundary y=n+1.
 def lift(F,n):return tuple(F)+tuple(tuple((1 if v>0 else -1)*(abs(v)+n) for v in c) for c in H)
 for tag,F in variants.items():
  G=lift(F,n)
  check(exact22(G,n+3),'guard lift maintains exact22')
  check(not connected(G,n+3),'guard lift deliberately DISCONNECTED')
  p,_,_=brute_fiber(G,n+3,n+1)
  check(p==(3 if probs[tag]['projection_bitmask'] else 0),'fiber encodes SAT on strict22')
 # Independent finite signer control / prior archive rerun is done separately.
 result={'status':'PASS','assertion_groups':CHECKS,
    'theorem_scope':'proper strict signed exact-(2,2)-3CNF',
    'hardness_label':'NP-hard/coNP-hard follows from published NP-completeness, conditional consequences only',
    'common_support':{'n':n,'m':len(U),'boundary_var':y,'connected':True,'variants':probs},
    'L0_flip_source_coordinates_0based':[[7,0],[19,0]],
    'L1_complemented_variable':13,
    'one_balanced_sign_swap_neighbors':{'tested':len(neigh),
       'sat':sum(x['sat_assignments']>0 for x in neigh),
       'with_any_frozen_variable':sum(bool(x['frozen']) for x in neigh),
       'examples':neigh[:12]},
    'guard_H':{'clauses':H,'n':3,'fiber_mask':3,
      'disconnected_lift':True},
    'authenticated_resolution':{
       'L0_assume_x13_true':{k:v for k,v in proof0.items() if k!='steps'},
       'L1_assume_x13_false':{k:v for k,v in proof1.items() if k!='steps'},
       'U_assume_x13_false':{k:v for k,v in proofU0.items() if k!='steps'},
       'U_assume_x13_true':{k:v for k,v in proofU1.items() if k!='steps'}},
    'limitations':['Connected-class hardness is under polynomial-time nonadaptive Turing reductions by component decomposition, not an exhibited many-one reduction.',
      'The many-one guard lift is disconnected; it cannot be cited as a connected hard family.',
      'All exact projection tables on the four W1 controls are finite fully exhaustive tests.',
      'No universal affordable summary acquisition or P-vs-NP resolution.']}
 print(json.dumps(result,indent=2,sort_keys=True))
 # Store audited proof traces separately. Authenticated locally; not formally kernel certified.
 here=Path(__file__).resolve().parent
 (here/'2026-10-29_0124_EXACT22_FOUR_FIBERS155_proof_traces.json').write_text(json.dumps({
   'L0_source':L0,'L1_source':L1,'L0_assumption_unit':[13],
   'L1_assumption_unit':[-13],'L0_trace':proof0['steps'],'L1_trace':proof1['steps'],
   'U_assumption_false':[-13],'U_assumption_true':[13],
   'U_trace_false':proofU0['steps'],'U_trace_true':proofU1['steps']},indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()
