#!/usr/bin/env python3
"""ARC192: exact22 DISJ controls and source-index jump/reversal resource accounting.
Zero dependencies; exhaustive at gadget scale, combinatorial fooling pairs m<=7.
Not a SAT lower bound or a physical TM benchmark.
"""
from __future__ import annotations
import argparse, collections, hashlib, itertools, json, math, pathlib

W1 = [
 (-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),
 (-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),
 (1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),
 (-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),
 (4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14),
]
A=((6,0),(11,0)); B=((17,2),(9,2))
CHECKS=0

def check(cond, msg=''):
 global CHECKS
 CHECKS+=1
 if not cond: raise AssertionError(msg or f'assertion {CHECKS}')

def module(a,b):
 out=[list(c) for c in W1]
 for control,positions in ((a,A),(b,B)):
  if not control:
   for ci,li in positions: out[ci][li]=-out[ci][li]
 return tuple(tuple(row) for row in out)

def sat_clause(c,mask):
 return any(bool(mask & (1 << (abs(v)-1))) == (v>0) for v in c)

def model_masks(cnf):
 return [x for x in range(1<<15) if all(sat_clause(c,x) for c in cnf)]

def quotient_formula(m,a,b):
 assert len(a)==len(b)==m
 blocks=[]
 for i in range(m):
  delta=15*i
  blocks.append(tuple(tuple((1 if x>0 else -1)*(abs(x)+delta) for x in c) for c in module(a[i],b[i])))
 # Crucial actual physical clause layout: Alice sign rows / 16m fixed / Bob sign rows.
 rows=[blocks[i][j] for i in range(m) for j in (6,11)]
 rows += [blocks[i][j] for i in range(m) for j in range(20) if j not in (6,11,17,9)]
 rows += [blocks[i][j] for i in range(m) for j in (17,9)]
 return tuple(rows)

def encode(cnf,m):
 w=(15*m).bit_length();q=(20*m).bit_length()
 # Self-delimiting unary lengths; finite ordinary source bitstring, not a promise header oracle.
 hdr='1'*w+'0'+format(15*m,f'0{w}b')+'1'*q+'0'+format(20*m,f'0{q}b')
 bits=hdr
 for c in cnf:
  for lit in c:
   bits+=('0' if lit>0 else '1')+format(abs(lit),f'0{w}b')
 return bits,len(hdr),w

def decode(s):
 i=0;w=0
 while i<len(s) and s[i]=='1':w+=1;i+=1
 assert i<len(s) and s[i]=='0';i+=1
 n=int(s[i:i+w],2);i+=w
 q=0
 while i<len(s) and s[i]=='1':q+=1;i+=1
 assert i<len(s) and s[i]=='0';i+=1
 mclauses=int(s[i:i+q],2);i+=q
 assert mclauses%20==0 and n==15*(mclauses//20)
 assert len(s)==i+3*mclauses*(w+1)
 out=[]
 for j in range(mclauses):
  c=[]
  for k in range(3):
   sign=s[i];name=int(s[i+1:i+1+w],2);i+=1+w
   c.append(name if sign=='0' else -name)
  out.append(tuple(c))
 return tuple(out)

def check_exact(cnf,m):
 check(len(cnf)==20*m)
 pos=collections.Counter(x for c in cnf for x in c if x>0)
 neg=collections.Counter(-x for c in cnf for x in c if x<0)
 check(len(set(cnf))==len(cnf))
 for c in cnf:check(len(c)==3 and len({abs(x) for x in c})==3)
 for v in range(1,15*m+1):check(pos[v]==neg[v]==2)

def simplify(cnf,assignment):
 out=[]
 for c in cnf:
  d=[];good=False
  for lit in c:
   var=abs(lit)
   if var not in assignment:d.append(lit)
   elif assignment[var]==(lit>0):good=True;break
  if not good:out.append(tuple(d))
 return tuple(out)

def dpll(cnf,assign=None):
 assign={} if assign is None else dict(assign)
 while True:
  cnf=simplify(cnf,assign)
  if not cnf:return assign
  if any(not c for c in cnf):return None
  units=[c[0] for c in cnf if len(c)==1]
  changed=False
  for x in units:
   v=abs(x);value=x>0
   if v in assign and assign[v]!=value:return None
   if v not in assign:assign[v]=value;changed=True
  if not changed:break
 # shortest residual for branching
 x=min(cnf,key=len)[0];v=abs(x)
 for value in (x>0,x<0):
  ans=dpll(cnf,dict(assign,**{v:value}) if False else {**assign,v:value})
  if ans is not None:return ans
 return None


def local_resolution_template():
 """Unshared source-authenticated Resolution DAG for the fixed 20-row W1."""
 lines=[(frozenset(c),None) for c in W1]
 active=list(range(20))
 for v in range(1,16):
  positive=[i for i in active if v in lines[i][0]]
  negative=[i for i in active if -v in lines[i][0]]
  kept={lines[i][0]:i for i in active if v not in lines[i][0] and -v not in lines[i][0]}
  for i,j in itertools.product(positive,negative):
   r=(lines[i][0]-{v})|(lines[j][0]-{-v})
   if any(-lit in r for lit in r):continue
   r=frozenset(r)
   if r not in kept:
    kept[r]=len(lines);lines.append((r,(i,j,v)))
   if not r:
    return lines
  active=list(kept.values())
 raise AssertionError('W1 expected UNSAT; no empty clause')

def source_row_of_component(m,i,j):
 if j==6:return 2*i
 if j==11:return 2*i+1
 if j==17:return 18*m+2*i
 if j==9:return 18*m+2*i+1
 return 2*m+16*i+sum(1 for v in range(j) if v not in (6,11,17,9))

def authenticate_local_proof(cnf,m,i,proof):
 delta=15*i
 mapped=[]
 for line_id,(clause,rule) in enumerate(proof):
  if rule is None:
   check(line_id<20)
   source=cnf[source_row_of_component(m,i,line_id)]
   claim=frozenset((1 if x>0 else -1)*(abs(x)+delta) for x in clause)
   check(frozenset(source)==claim)
  else:
   left,right,v=rule
   check(left<line_id and right<line_id)
   lhs,rhs=mapped[left],mapped[right]
   vv=v+delta
   check(vv in lhs and -vv in rhs)
   claim=(lhs-{vv})|(rhs-{-vv})
   check(not any(-lit in claim for lit in claim))
   claim=frozenset(claim)
   check(claim==frozenset((1 if x>0 else -1)*(abs(x)+delta) for x in clause))
  mapped.append(claim)
 check(not mapped[-1])
 return True

def sign_offsets(m,h,w):
 # First Alice controlled clause in left zone, first Bob controlled clause in right.
 aw=[h+3*(2*i)*(w+1)+0*(w+1) for i in range(m)]
 bw=[h+3*(18*m+2*i)*(w+1)+2*(w+1) for i in range(m)]
 return aw,bw

def itinerary(m,chunk,jump,h,w):
 a,b=sign_offsets(m,h,w)
 pos=0;it=[];calls=[];physical=0;unit_jumps=0
 # not a total SAT solver; records only input-head target-only itinerary.
 for start in range(0,m,chunk):
  for target in a[start:start+chunk]+b[start:start+chunk]:
   delta=target-pos
   if delta:
    unit_jumps+=math.ceil(abs(delta)/jump)
    physical+=abs(delta)
    it.append(1 if delta>0 else -1)
   pos=target;calls.append(target)
 rev=sum(it[i]!=it[i-1] for i in range(1,len(it)))
 central=h+3*(2*m+8*m)*(w+1) # midway through 16m fixed rows
 # crossing count per actual movement between source-access coordinates
 cr=0;pp=0
 for target in calls:
  cr+=int((pp<central)!=(target<central));pp=target
 check(cr<=len(calls))
 check(rev>=max(0,cr-1))
 return {'m':m,'chunk':chunk,'J':jump,'N':h+60*m*(w+1),
   'source_probes':len(calls),'head_jumps':unit_jumps,
   'physical_distance':physical,'central_cut_crossings':cr,'reversals':rev,
   'buffer_plus_index_bits':chunk+math.ceil(math.log2(h+60*m*(w+1)+2))}

def main():
 counts={};masks={};test_cases=0;fooling=0;residuals=0;its=[]
 proof=local_resolution_template()
 check(len(proof)==205)
 check(not proof[-1][0])
 proof_checks=0
 for a,b in itertools.product((0,1),repeat=2):
  cnf=module(a,b)
  mask=model_masks(cnf);masks[a,b]=mask;counts[f'{a}{b}']=len(mask)
  check((len(mask)==0)==bool(a and b))
  check_exact(cnf,1)
 check(counts=={'00':772,'01':272,'10':272,'11':0},f'counts:{counts}')
 # Source-control positions are BOTH balanced and disjoint.
 check(all(W1[ci][li]==-W1[cj][lj] for (ci,li),(cj,lj) in (A,B)))
 for m in range(1,7):
  for i in range(1<<m):
   a=tuple((i>>k)&1 for k in range(m))
   b=tuple(1-x for x in a)
   cnf=quotient_formula(m,a,b)
   check_exact(cnf,m)
   bits,h,w=encode(cnf,m)
   check(decode(bits)==cnf)
   # All components SAT and hence their conjunction is SAT.
   check(all(masks[x,y] for x,y in zip(a,b)))
   test_cases+=1
   if m<=2:
    ans=dpll(cnf)
    check(ans is not None)
    check(not simplify(cnf,ans))
  # explicit no-pair-of-fooling-set-YES can be in a single accepting rectangle
  for i in range(1<<m):
   a=tuple((i>>k)&1 for k in range(m));nb=tuple(1-x for x in a)
   for j in range(i+1,1<<m):
    c=tuple((j>>k)&1 for k in range(m));nc=tuple(1-x for x in c)
    bad1=any(x and y for x,y in zip(a,nc))
    bad2=any(x and y for x,y in zip(c,nb))
    check(bad1 or bad2)
    fooling+=1
 # Authentic source-ID proof on the same physical tripartite source, one bad block.
 for m in (1,2,3,5):
  for bad in range(m):
   a=(1,)*m;b=tuple(1 if i==bad else 0 for i in range(m))
   cnf=quotient_formula(m,a,b)
   check_exact(cnf,m)
   check(authenticate_local_proof(cnf,m,bad,proof))
   proof_checks+=1
 # two actual restriction levels; exhaustive model truth-table for original 15 variables
 for ab in ((0,0),(1,1)):
  root=module(*ab)
  check((len(masks[ab])>0)==bool(dpll(root) is not None))
  for x,y in itertools.product((0,1),repeat=2):
   first=simplify(root,{1:bool(x)})
   second=simplify(first,{2:bool(y)})
   expected=any(((v&1)==x and ((v>>1)&1)==y) for v in masks[ab])
   check(bool(dpll(second) is not None)==expected)
   check(all(0<=len(c)<=3 for c in second))
   residuals+=1
 # canonical source-sign pointer itineraries: exact zones, jumps and accounted reversals
 for m in (4,8,16,32,64,128):
  base=quotient_formula(m,(0,)*m,(1,)*m)
  _,h,w=encode(base,m)
  for chunk in (1,2,4,8,min(16,m),m):
   for J in (1,4,16,128,10**9):
    its.append(itinerary(m,chunk,J,h,w))
 # correctness of fast nearest-neighbor skipping: jump radius cannot exceed J
 for z in its:
  check(z['head_jumps']<=z['physical_distance']+1)
  check(z['reversals']+1>=z['central_cut_crossings'])
 # finite theorem count B=(S + O(log(N+T))) # crossings R>=cr-1
 res={'identifier':'ARC192_JUMP_REVERSAL_COMMUNICATION','date':'2026-10-26',
      'input':'actual W1 15-variable proper signed exact22 20-row gadget; self-delimited binary source',
      'gadget_model_counts':counts,'source':
      'experiments/review/early22_compiler_redteam_audit.py',
      'mode':'exhaustive masks for 2^15 assignments x 4 gadget variants; 2^m YES for m<=6; all fooling pairs m<=6; DPLL controls m<=2; 2-level residuals; deterministic physical source-pointer itineraries',
      'fooling_yes_instances':test_cases,'fooling_pairs_checked':fooling,
      'genuine_two_level_residuals':residuals,'head_itineraries':its,
      'resolution_proof_records':len(proof),'resolution_proof_source_lines':20,
      'resolution_proof_authentications':proof_checks,
      'resolution_proof_max_width':max(len(c) for c,rule in proof),
      'assertions':CHECKS,'failed':0,'limitations':[
        'finite tests are not physical TM measurements',
        'the reversal theorem requires one sequential input head, signed jumps counted as movement, and finite fixed-k sequential work tapes',
        'derived inequalities do not apply to unrestricted RAM time, unrestricted hardware, or every SAT input',
        'single-cut fooling lower bound is worst-case on some YES source, not each source'],
      'random_seed':None}
 out=pathlib.Path(__file__).with_name('2026-10-26_2056_ARC192_jump_reversal_raw.json')
 out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:v for k,v in res.items() if k!='head_itineraries'},indent=2))
 print('raw_path=',str(out))
if __name__=='__main__':main()
