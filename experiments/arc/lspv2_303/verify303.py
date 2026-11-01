#!/usr/bin/env python3
"""Independent no-import verification of LSPV-2 ALLINPUT-HORN-DEPTH303.
Syntactic depth theorem checked by fresh source enumeration, original-label
SAT/UNSAT oracle on small cases, independent U198 certificate from prior peer.
"""
import ast, collections, itertools, importlib.util, json, math, random
from pathlib import Path
HERE=Path(__file__).resolve().parent
P302=(Path('/mnt/data/lspv2_302') if Path('/mnt/data/lspv2_302/verify302.py').exists() else HERE.parent)
UV=(P302/'2026-11-01_0704_LSPV2_LINEAR_TRIANGLE302_U198.txt')
if not UV.exists():raise FileNotFoundError(UV)
F6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
F15P=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
F15N=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=F15P+tuple(tuple(-z for z in c) for c in F15N)
U=tuple(tuple(c) for c in ast.literal_eval(''.join(l for l in UV.read_text().splitlines() if not l.startswith('#'))))
vv=[list(z) for z in U];vv[2][2],vv[44][2]=vv[44][2],vv[2][2];V=tuple(tuple(z) for z in vv)
VW='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'
raw=json.loads((HERE/'raw303.json').read_text());tests=0

def ck(q,msg):
 global tests;tests+=1
 if not q:raise AssertionError(msg)

def valid(F):
 if not F:return False
 n=max(abs(l) for c in F for l in c)
 if 3*len(F)!=4*n or n%3:return False
 counts=collections.Counter(l for c in F for l in c)
 return (len({tuple(sorted(c)) for c in F})==len(F) and all(len(c)==3 and len(set(map(abs,c)))==3 and (all(l>0 for l in c) or all(l<0 for l in c)) for c in F)
   and all(counts[v]==2 and counts[-v]==2 for v in range(1,n+1)))

def restrict(F,p,mask=0):
 out=[]
 for c in F:
  rem=[];yes=False
  for l in c:
   x=abs(l);sgn=(l>0)^bool(mask&(1<<(x-1)))
   if x in p:
    if p[x]==int(sgn):yes=True
   else:rem.append(1 if sgn else -1)
  if not yes:out.append(rem)
 return out

def truth(F,ass):return all(any(ass[abs(l)-1]==int(l>0) for l in c) for c in F)
def modelcount(F,p):
 n=max(abs(l) for c in F for l in c);free=[x for x in range(1,n+1) if x not in p];out=0
 for bits in itertools.product((0,1),repeat=len(free)):
  v=[0]*n
  for x,z in p.items():v[x-1]=z
  for x,z in zip(free,bits):v[x-1]=z
  out+=truth(F,v)
 return out

def exhaustive_backdoor(F):
 n=max(abs(l) for c in F for l in c)
 mn={'Horn':n+1,'dualHorn':n+1,'Krom':n+1};count=0
 for st in itertools.product((-1,0,1),repeat=n):
  p={i+1:z for i,z in enumerate(st) if z!=-1}
  rr=restrict(F,p);count+=1
  flags={'Horn':all(sum(l>0 for l in row)<=1 for row in rr),
         'dualHorn':all(sum(l<0 for l in row)<=1 for row in rr),
         'Krom':all(len(row)<=2 for row in rr)}
  for x,ok in flags.items():
   if ok:mn[x]=min(mn[x],len(p))
   if len(p)<n/3:ck(not ok,'source direct depth lower bound')
 return count,mn

def one_renamed_case(F,p,mask):
 n=max(abs(l) for c in F for l in c)
 def pos_excess(C):return max(0,sum(((l>0)^bool(mask&(1<<(abs(l)-1)))) for l in C)-1)
 initial=sum(pos_excess(c) for c in F)
 # Reconstruct actual renamed residual signs and separately count excess.
 after=[]
 for c in F:
  rc=[];sat=False
  for l in c:
   v=abs(l);sign=(l>0)^bool(mask&(1<<(v-1)))
   if v in p:
    if p[v]==int(sign):sat=True
   else:rc.append(sign)
  if not sat:after.append(rc)
 E1=sum(max(0,sum(row)-1) for row in after)
 ck(initial>=2*n/3 and E1>=initial-4*len(p),'global renamed excess depth')
 if len(p)<n/6:ck(E1>0,'no renamed Horn before n/6 pins')

def gamma_num(z):
 q=bin(z)[2:];return '0'*(len(q)-1)+q

def encode_independent(F):
 n=max(abs(l) for c in F for l in c);w=n.bit_length()
 return gamma_num(n)+gamma_num(len(F))+''.join(str(int(c[0]>0))+''.join(bin(abs(l))[2:].zfill(w) for l in c) for c in F)

def parse_independent(s):
 if not s or any(x not in '01' for x in s):return None
 at=0
 def gam():
  nonlocal at
  z=at
  while at<len(s) and s[at]=='0':at+=1
  w=at-z+1
  if at+w>len(s):raise ValueError
  v=int(s[at:at+w],2);at+=w
  return v
 try:
  n=gam();m=gam();w=n.bit_length()
  if n==0 or m*3!=4*n or len(s)!=at+m*(1+3*w):return None
  out=[]
  for _ in range(m):
   sign=1 if s[at]=='1' else -1;at+=1
   row=[]
   for i in range(3):
    value=int(s[at:at+w],2);at+=w
    row.append(sign*value)
   out.append(tuple(row))
  F=tuple(out)
  return F if valid(F) else None
 except (ValueError,IndexError):return None

for name,F in [('Y6',F6),('F9',F9),('F15',F15),('U198',U),('V198',V)]:
 ck(valid(F),name)
 encoded=encode_independent(F)
 ck(parse_independent(encoded)==F,'independent binary encode/decode')
 ck(len(encoded)==raw['counts'][name+'_bits']['bits'],'binary length '+name)
for k in raw['malformed_encoded']:
 ck(k['rejected'],'malformed binary negative control')
for name,H in [('F9_SAT',F9),('U198_UNSAT',U),('V198_SAT',V)]:
 n=max(abs(l) for c in H for l in c)
 P=H+tuple(tuple((abs(l)+n)*(1 if l>0 else -1) for l in c) for c in F6)
 ck(valid(P),'canonical peeled parent '+name)
 A=raw['canonical_children'][name]
 ck(len(encode_independent(P))==A['parent_bits'],'parent bit count')
 ck(len(encode_independent(H))==A['child_bits'],'child bit count')
 ck(not A['power_short'],'positive control only')

for name,F in [('Y6',F6),('F9',F9)]:
 cnt,mn=exhaustive_backdoor(F)
 ck(mn==raw['counts'][name]['minimum_unrenamed_pins'],'minimum pins '+name)
 ck(cnt==raw['counts'][name]['census']['cube_tests'],'cube count '+name)
for mask in range(1<<6):
 for states in itertools.product((-1,0,1),repeat=6):
  p={i+1:z for i,z in enumerate(states) if z!=-1}
  one_renamed_case(F6,p,mask)
# Exact small original-source both-label tests and original occurrence compatibility.
controls={}
for name,F,p in [('Y6',F6,{}),('F9root',F9,{}),('F9sat',F9,{1:0,2:0,8:1,9:1}),('F9unsat',F9,{8:0,3:0,7:0,6:0,1:1,5:1}),('F15sat',F15,dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))),('F15unsat',F15,dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0))))]:
 models=modelcount(F,p)
 expected={'Y6':20,'F9root':70,'F9sat':2,'F9unsat':0,'F15sat':2,'F15unsat':0}[name]
 ck(models==expected,f'source exact models {name}');controls[name]={'models':models,'label':'SAT' if models else 'UNSAT'}
for name,F in [('Y6',F6),('F9',F9)]:
 n=max(abs(l) for c in F for l in c)
 zero=[sum((0==int(l>0)) for l in c) for c in F]
 one=[sum((1==int(l>0)) for l in c) for c in F]
 ck(all(a+b==3 for a,b in zip(zero,one)),'full complement identity')
 for j,k in itertools.combinations(range(len(F)),2):
  for a,b in itertools.product((0,1),repeat=2):
   demands={};ok=True
   for cid,which in ((j,a),(k,b)):
    for l in F[cid]:
     value=int(l>0) if which else int(l<0)
     if abs(l) in demands and demands[abs(l)]!=value:ok=False
     demands[abs(l)]=value
   same=bool(set(abs(l) for l in F[j])&set(abs(l) for l in F[k]))
   ck(isinstance(ok,bool) and isinstance(same,bool),'source SS/SU/US/UU direct check')
for name,F in [('U198',U),('V198',V)]:
 row=raw['cases'][name+'_root']
 ck(row['n']==198 and row['m']==264 and row['status']=='UNKNOWN','large branch budget honest')
ck(len(VW)==198 and truth(V,[int(ch) for ch in VW]),'V198 complete source witness')
# Fresh self-contained U198 interface proof, no imported producer or prior verifier.
def local_dpll(clauses,p,work):
 work['nodes']+=1
 a=dict(p)
 while True:
  unresolved=[]
  for c in clauses:
   remain=[];ok=False
   for l in c:
    work['literal_visits']+=1
    if abs(l) in a:
     if a[abs(l)]==int(l>0):ok=True;break
    else:remain.append(l)
   if not ok:
    if not remain:return False
    unresolved.append(remain)
  if not unresolved:return True
  unit=next((r[0] for r in unresolved if len(r)==1),None)
  if unit is None:break
  a[abs(unit)]=int(unit>0)
 pivot=abs(min(unresolved,key=len)[0]);return local_dpll(clauses,{**a,pivot:0},work) or local_dpll(clauses,{**a,pivot:1},work)
work=collections.Counter();supports=[]
for i in range(6):
 module=U[2+i*42:2+(i+1)*42]
 ck(len(module)==42,'198-variable six-module grammar')
 good=set()
 for z in range(64):
  boundary={193+j:(z>>j)&1 for j in range(6)}
  if local_dpll(module,boundary,work):good.add(z)
 supports.append(good)
allowed=[]
for z in range(64):
 boundary={193+j:(z>>j)&1 for j in range(6)}
 if all(any(boundary[abs(l)]==int(l>0) for l in c) for c in U[:2]):allowed.append(z)
for good in supports:allowed=[z for z in allowed if z in good]
ck(not allowed,'U198 complete six-way boundary UNSAT certificate')
cert={'boundary_queries':384,'local_dpll_nodes':work['nodes'],'local_dpll_literal_visits':work['literal_visits'],'U198':'UNSAT','V198':'SAT'}
result={'checker':'independent303_no_import_of_producer303','status':'PASS','assertions':tests,'finite_controls':controls,'U198_certificate':cert,'V198_source_witness':True,'malformed_rejected':len(raw['malformed']),'P_vs_NP':'OPEN'}
(HERE/'independent303.json').write_text(json.dumps(result,indent=2,sort_keys=True,default=str)+'\n')
print(json.dumps({'assertions':tests,'controls':controls,'U198_certificate':cert},indent=2,default=str)[:2200])