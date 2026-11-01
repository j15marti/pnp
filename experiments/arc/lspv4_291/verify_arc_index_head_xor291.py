#!/usr/bin/env python3
"""Independent certificate and head-recoding audit, no producer import."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from itertools import product
import json
P=Path(__file__).resolve().parent
R=json.loads((P/'arc_index_head_xor291_raw.json').read_text())
U=json.loads((P/'U_source.json').read_text())
Y=json.loads((P/'Y6_source.json').read_text())
V=[c.copy() for c in U];V[1][0],V[7][0]=V[7][0],V[1][0]
V_witness=[int(b) for b in json.loads((P/'V_witness.json').read_text())]
assertions=0

def check(cond,reason):
 global assertions
 if not cond:raise AssertionError(reason)
 assertions+=1

def good(f,n):
 if len(f)*3!=4*n:return False
 Pp=[0]*(n+1);Nn=[0]*(n+1);S=set()
 for C in f:
  if len(C)!=3 or any(x==0 or abs(x)>n for x in C):return False
  if len(set(map(abs,C)))!=3:return False
  if any((v>0)!=(C[0]>0) for v in C):return False
  key=tuple(sorted(C))
  if key in S:return False
  S.add(key)
  for v in C:
   if v>0:Pp[v]+=1
   else:Nn[-v]+=1
 return all(Pp[i]==Nn[i]==2 for i in range(1,n+1))

def tcount(C,A):return sum((A[abs(v)-1]==1)==(v>0) for v in C)
def ismodel(F,A):return all(tcount(C,A)>0 for C in F)
def counted(f,a):return [tcount(c,a) for c in f]

def refute_U_source(f):
 def dpll(C):
  while True:
   if not C:return True
   if any(not c for c in C):return False
   unit=next((c[0] for c in C if len(c)==1),None)
   if unit is None:break
   C=[[z for z in c if z!=-unit] for c in C if unit not in c]
  var=C[0][0]
  return any(dpll([[z for z in c if z!=-choice] for c in C if choice not in c]) for choice in (var,-var))
 external=[]
 for k in range(6):
  block=f[2+42*k:2+42*(k+1)]
  inner=[[z for z in c if abs(z)<=192] for c in block]
  check(not dpll(inner),f'private group {k} refuted')
  external.append(sorted(set(z for c in block for z in c if abs(z)>192)))
 for bits in product((0,1),repeat=6):
  a=[0]*192+list(bits)
  check(any(tcount(c,a)==0 for c in f[:2]) or any(tcount(c,a)==0 for c in external),
        'boundary 64 patterns eliminated')

def code_len(f,n):
 m=len(f);w=m.bit_length()
 return w+1+2*w+len(f)*3*(w+1)

def g(v):return v^(v>>1)

def verify_source(name,F,n):
 C=R['sources'][name];check(good(F,n),name+' membership')
 check(C['n']==n and C['m']==len(F),'size')
 check(C['encoded_bits']==code_len(F,n),'length codec')
 original=C['controls']['original'];check(len(original)==len(F),'all source records')
 for j,cl in enumerate(F):
  s=[[abs(l),int(l>0)] for l in cl];u=[[abs(l),int(l<0)] for l in cl]
  v=original[j]
  check(v['source_clause_index']==j and v['signed_occurrences']==cl,'source exact')
  check(v['S_local_all_true']==s and v['U_local_all_false']==u,'S U exact')
  check(v['inverted_S_to_U']==u and v['inverted_U_to_S']==s,'complements exact')
 a=[0]*n
 hist=[counted(F,a).count(t) for t in range(4)]
 check(hist==C['controls']['allzero_hist'],'zero endpoint')
 hist=[counted(F,[1]*n).count(t) for t in range(4)]
 check(hist==C['controls']['allone_hist'],'one endpoint')
 pairrows=C['controls']['pair_modes'];check(len(pairrows)==len(F)*(len(F)-1)//2,'pairs length')
 for p in pairrows:
  i,j=p['clause_pair'];c=F[i];d=F[j]
  s={abs(x):int(x>0) for x in c};z={abs(x):int(x>0) for x in d}
  same=any(s[v]==z[v] for v in set(s)&set(z))
  opposite=any(s[v]!=z[v] for v in set(s)&set(z))
  check(p['SS_SU_US_UU']==[int(not opposite),int(not same),int(not same),int(not opposite)],'SS SU US UU')
 for r in C['controls']['flip_trail']:
  k=r['variable']-1
  old=counted(F,a)
  oldbits=list(a)+[z for v in old for z in ((v>>1)&1,v&1)]+[int(v>0) for v in old]
  a[k]^=1;new=counted(F,a)
  newbits=list(a)+[z for v in new for z in ((v>>1)&1,v&1)]+[int(v>0) for v in new]
  check([i for i,(x,y) in enumerate(zip(old,new)) if x!=y]==r['changed_original_clause_ids'],'changed ids')
  check(sum(x!=y for x,y in zip(oldbits,newbits))==r['logical_xor_popcount'],'logical Hamming')
 H=C['head_motion'];bits=C['encoded_bits'];h=bits.bit_length()-1
 check(h==H['h'],'bitlength chosen')
 a=(1<<h)-1;N=8*a
 check(H['boundary']==a and H['other']==a+1 and H['oscillation_steps']==N,'head positions')
 check(H['prep_steps']==a and H['total_native_head_moves']==a+N,'native head operations')
 binary=gray=0
 for i in range(a):
  binary+=(i^(i+1)).bit_count()
  gray+=(g(i)^g(i+1)).bit_count()
 check(binary==H['prep_binary_head_xor'] and gray==H['prep_gray_head_xor'],'all preparation moves')
 same=0;db=dg=ctrl=0;state=0;pos=a
 for _ in range(N):
  newpos=a+1 if pos==a else a
  db+=(pos^newpos).bit_count()
  dg+=(g(pos)^g(newpos)).bit_count()
  newstate=1-state;ctrl+=(state^newstate).bit_count()
  pos=newpos;state=newstate
 check(pos==a and state==0,'loop endpoint restored')
 check(db==H['oscillation_binary_head_xor'] and dg==H['oscillation_gray_head_xor'],'adjacent head XOR')
 check(ctrl==H['oscillation_control_bit_xor'],'finite control changes')
 check(db+ctrl==H['oscillation_full_binary_code_xor'],'complete binary metadata')
 check(dg+ctrl==H['oscillation_full_gray_code_xor'],'complete Gray metadata')
 check(H['index_tape_content_writes']==0 and H['index_tape_erasure_events']==0
       and H['oscillation_tape_content_xor']==0,'zero physical tape writes')
 check(H['oscillation_full_endpoint_xor']==0,'full endpoint unchanged')
 L=C['head_motion_logspace']; lowh=L['h']; lowp=(1<<lowh)-1; lowR=8*lowp
 check(lowp+1<=2*bits.bit_length(), 'polylog high-water location')
 check(L['oscillation_binary_head_xor']==lowR*(lowh+1), 'logspace binary coded head')
 check(L['oscillation_gray_head_xor']==lowR,'logspace Gray coded head')
 check(L['oscillation_full_endpoint_xor']==0 and L['oscillation_tape_content_xor']==0,'logspace physical tapes blank')
 if name=='Y6_SAT':check(sum(ismodel(F,a) for a in product((0,1),repeat=6))==20,'Y6 exhaustive')
 if name=='U198_UNSAT':refute_U_source(F)
 if name=='V198_SAT':check(ismodel(F,V_witness),'V198 full witness')
 return {'name':name,'h':h,'adjacent_binary_head_xor':db,'adjacent_gray_head_xor':dg,
         'native_head_moves':a+N,'zero_tape_writes':True}

results=[verify_source('Y6_SAT',Y,6),verify_source('U198_UNSAT',U,198),verify_source('V198_SAT',V,198)]
# Malformed negative controls, all preserve or perturb quota distinctly.
check(not good(Y+Y[:1],6),'extra clause')
Z=[c.copy() for c in Y];Z[0]=Z[1].copy();check(not good(Z,6),'duplicate')
Z=[c.copy() for c in Y];Z[0][0]*=-1;check(not good(Z,6),'mixed sign')
Z=[c.copy() for c in Y];Z[0][1]=Z[0][0];check(not good(Z,6),'repeated variable')
Z=[c.copy() for c in Y];Z[0][1]=0;check(not good(Z,6),'zero literal')
for i,c in enumerate([Fraction(6,5),Fraction(241,200)]):
 f=Fraction(1);ds=[]
 for k in range(1,4):
  f=c*f/(1+f)
  ds.append(min((1/f-c)/k,c**(-k)))
 record=R['flmv'][i]
 check(record['c']==str(c) and record['k_1_2_3']==list(map(str,ds)),'exact fractions')
 check(ds[1]>ds[0] and ds[1]>ds[2] and ds[1]>c**(-4),'strict k2 and infinite tail')
 check(record['tail_cap']==str(c**(-4)),'tail exact')
check(Fraction(R['flmv'][0]['k_1_2_3'][1])==Fraction(23,45),'c=6/5')
check(Fraction(R['flmv'][1]['k_1_2_3'][1])==Fraction(11642479,23232400),'c=241/200')
result={'status':'PASS','independent_no_producer_imports':True,'assertions':assertions,
        'sources':results,'SAT_UNSAT_certificates_replayed':True,'actual_native_sat_machine':False,
        'head_code_is_offline_not_physical_write':True,'P_vs_NP':'OPEN'}
(P/'arc_index_head_xor291_verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))