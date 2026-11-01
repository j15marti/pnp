#!/usr/bin/env python3
"""LSPV-5 finite certified-portfolio restart diagnostic.

This is a source-authenticated finite control, not an all-input polynomial SAT
algorithm and not an FLMV machine simulation.  Every restart pays for a fresh
scan of the exact gamma-header/fixed-record source encoding.  Logical XOR is
computed only after the run as an offline diagnostic.
"""
from __future__ import annotations

import argparse
import collections
import itertools
import json
import math
from pathlib import Path

Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-v for v in c) for c in N15)

CASES={
 "Y6_ROOT":(Y6,{}),
 "F9_SAT":(F9,{1:0,2:0,8:1,9:1}),
 "F9_PARITY_ONLY_UNSAT":(F9,{8:0,3:0,7:0,6:0,1:1,5:1}),
 "F15_SAT":(F15,dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))),
 "F15_UNSAT":(F15,dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))),
}

def grammar(F):
 try:
  if not F:return False
  n=max(abs(x) for c in F for x in c)
  if n%3 or 3*len(F)!=4*n:return False
  if any(len(c)!=3 or len(set(map(abs,c)))!=3 or (min(c)<0<max(c)) for c in F):return False
  if len(set(tuple(sorted(c)) for c in F))!=len(F):return False
  q=collections.Counter(x for c in F for x in c)
  return all(q[v]==q[-v]==2 for v in range(1,n+1))
 except Exception:return False

def gamma(z):
 b=format(z,'b');return '0'*(len(b)-1)+b

def encode(F):
 assert grammar(F)
 n=max(abs(x) for c in F for x in c);w=n.bit_length()
 return gamma(n)+gamma(len(F))+''.join(('1' if c[0]>0 else '0')+''.join(format(abs(x),f'0{w}b') for x in c) for c in F)

def clause_true(c,a):
 return any(a[abs(x)]==int(x>0) for x in c)

def source_sat(F,a):
 return all(clause_true(c,a) for c in F)

def enumerate_extensions(F,pins,order):
 n=max(abs(x) for c in F for x in c);free=[v for v in range(1,n+1) if v not in pins]
 seq=range(1<<len(free))
 if order=='reverse':seq=reversed(range(1<<len(free)))
 probes=0;bad=[];first=None
 for z in seq:
  q=(z^(z>>1)) if order=='gray' else z
  a=dict(pins);a.update({v:(q>>i)&1 for i,v in enumerate(free)})
  failed=None
  for j,c in enumerate(F):
   ok=False
   for x in c:
    probes+=1
    if a[abs(x)]==int(x>0):ok=True;break
   if not ok:failed=j;break
  if failed is None:
   first=a;break
  bad.append((q,failed))
 return first,bad,probes,len(free)

def certificate(F,pins):
 first,bad,probes,q=enumerate_extensions(F,pins,'lex')
 if first is not None:
  cert={'kind':'SAT','assignment':[first[v] for v in range(1,max(first)+1)]}
  out_bits=1+len(cert['assignment'])
 else:
  m=len(F);w=max(1,(m-1).bit_length())
  cert={'kind':'UNSAT_TABLE','free':[v for v in range(1,max(abs(x) for c in F for x in c)+1) if v not in pins],
        'rows':[[z,j] for z,j in bad]}
  out_bits=1+len(bad)*(q+w)
 return cert,probes,out_bits

def verify_certificate(F,pins,cert):
 probes=0;n=max(abs(x) for c in F for x in c)
 if cert.get('kind')=='SAT':
  bits=cert.get('assignment',[])
  if len(bits)!=n or any(b not in (0,1) for b in bits):return False,probes
  a={i+1:b for i,b in enumerate(bits)}
  if any(a.get(v)!=b for v,b in pins.items()):return False,probes
  for c in F:
   ok=False
   for x in c:
    probes+=1
    if a[abs(x)]==int(x>0):ok=True;break
   if not ok:return False,probes
  return True,probes
 if cert.get('kind')!='UNSAT_TABLE':return False,probes
 free=[v for v in range(1,n+1) if v not in pins]
 if cert.get('free')!=free:return False,probes
 rows=cert.get('rows',[])
 if len(rows)!=(1<<len(free)):return False,probes
 seen=set()
 for z,j in rows:
  if not isinstance(z,int) or z<0 or z>=(1<<len(free)) or z in seen:return False,probes
  if not isinstance(j,int) or not 0<=j<len(F):return False,probes
  seen.add(z);a=dict(pins);a.update({v:(z>>i)&1 for i,v in enumerate(free)})
  for x in F[j]:probes+=1
  if clause_true(F[j],a):return False,probes
 return len(seen)==(1<<len(free)),probes

def dpll_cost(F,pins):
 n=max(abs(x) for c in F for x in c);nodes=0;probes=0;answer=None
 def walk(a):
  nonlocal nodes,probes,answer
  nodes+=1;all_sat=True
  for c in F:
   sat=False;open_=False
   for x in c:
    probes+=1;v=abs(x)
    if v not in a:open_=True
    elif a[v]==int(x>0):sat=True;break
   if not sat and not open_:return False
   if not sat:all_sat=False
  if all_sat:
   answer={v:a.get(v,0) for v in range(1,n+1)};return True
  v=next(v for v in range(1,n+1) if v not in a)
  for b in (0,1):
   a[v]=b
   if walk(a):return True
  del a[v];return False
 walk(dict(pins));return answer,nodes+probes

def policy_records(F,pins):
 N=len(encode(F));cert,cert_work,out_bits=certificate(F,pins)
 records=[]
 for name,order in [('LEX_FALLBACK','lex'),('GRAY','gray'),('REVERSE','reverse')]:
  ans,bad,work,q=enumerate_extensions(F,pins,order)
  records.append({'name':name,'runtime':N+work+out_bits,'source_scan_bits':N,'solver_work':work,
                  'certificate_output_bits':out_bits,'delay_steps':0,'copy_writes':0,'recomp_work':0,'cert':cert})
 ans,dwork=dpll_cost(F,pins)
 records.append({'name':'DPLL','runtime':N+dwork+out_bits+cert_work,'source_scan_bits':N,'solver_work':dwork,
                 'certificate_output_bits':out_bits,'certificate_construction_work':cert_work,'delay_steps':0,'copy_writes':0,'recomp_work':0,'cert':cert})
 records.append({'name':'DELAY_COPY_RECOMP','runtime':2*N+2*dwork+out_bits+cert_work+4096,
                 'source_scan_bits':2*N,'solver_work':dwork,'certificate_output_bits':out_bits,
                 'certificate_construction_work':cert_work,'delay_steps':4096,'copy_writes':N,
                 'recomp_work':dwork,'logical_delta_during_delay':0,'cert':cert})
 return records

def schedule(F,pins,policies):
 best=min(p['runtime'] for p in policies);allocated=dispatch=0;phase=0;winner=None;budget=1
 while winner is None:
  for p in policies:
   dispatch+=1;allocated+=min(budget,p['runtime'])
   if p['runtime']<=budget:
    ok,vwork=verify_certificate(F,pins,p['cert'])
    if ok:winner=p;break
  if winner is None:phase+=1;budget*=2
 bound=4*len(policies)*best
 return {'winner':winner['name'],'winner_runtime':winner['runtime'],'best_runtime':best,'phases':phase+1,
         'final_budget':budget,'allocated_policy_steps':allocated,'dispatch_steps':dispatch,
         'verification_steps':vwork,'total_charged_work':allocated+dispatch+vwork,
         'four_k_t_bound_excluding_dispatch_and_verification':bound,'bound_holds':allocated<bound,
         'peak_writable_bits_bound':'max active policy workspace + O(log k + log budget); no saved policy states'}

def su_control(F):
 n=max(abs(x) for c in F for x in c);rows=[];pair_checks=0
 for j,c in enumerate(F):
  S={abs(x):int(x>0) for x in c};U={v:1-b for v,b in S.items()}
  rows.append({'clause':j,'literals':list(c),'S':S,'invert_S':U,'U':U,'invert_U':S})
 modes=[]
 for j,k in itertools.combinations(range(len(F)),2):
  a,b=F[j],F[k];same=any(abs(x)==abs(y) and (x>0)==(y>0) for x in a for y in b)
  opp=any(abs(x)==abs(y) and (x>0)!=(y>0) for x in a for y in b)
  predicted={'SS':not opp,'UU':not opp,'SU':not same,'US':not same}
  actual={mode:False for mode in predicted}
  for z in range(1<<n):
   ass={v:(z>>(v-1))&1 for v in range(1,n+1)}
   st=[all(ass[abs(x)]==int(x>0) for x in F[t]) for t in (j,k)]
   ut=[all(ass[abs(x)]!=int(x>0) for x in F[t]) for t in (j,k)]
   actual['SS']|=st[0] and st[1];actual['SU']|=st[0] and ut[1]
   actual['US']|=ut[0] and st[1];actual['UU']|=ut[0] and ut[1]
  assert actual==predicted;pair_checks+=4
  modes.append({'clauses':[j,k],'same_shared':same,'opposite_shared':opp,'modes':actual})
 def counts(z):
  a={v:(z>>(v-1))&1 for v in range(1,n+1)};q=[0,0,0,0]
  for c in F:q[sum(a[abs(x)]==int(x>0) for x in c)]+=1
  return q
 trail=[]
 for z in [0]+[(1<<i)-1 for i in range(1,n+1)]:trail.append({'assignment':z,'N0123':counts(z)})
 return {'clauses':rows,'pair_modes':modes,'pair_mode_checks':pair_checks,'zero_N0123':counts(0),
         'one_N0123':counts((1<<n)-1),'flip_trail':trail}

def xor_diag(F):
 n=max(abs(x) for c in F for x in c)
 def state(z):
  a={v:(z>>(v-1))&1 for v in range(1,n+1)};bits=[a[v] for v in range(1,n+1)]
  for c in F:
   t=sum(a[abs(x)]==int(x>0) for x in c);bits.extend([t&1,(t>>1)&1])
  return bits
 def path(gray):
  ss=[state((z^(z>>1)) if gray else z) for z in range(1<<n)]
  ds=[sum(x!=y for x,y in zip(a,b)) for a,b in zip(ss,ss[1:])]
  return {'sum_adjacent_d_logic':sum(ds),'endpoint_d_logic':sum(x!=y for x,y in zip(ss[0],ss[-1])),'steps':len(ds)}
 return {'classification':'OFFLINE_ONLY','binary':path(False),'gray':path(True),
         'warning':'logical XOR is not a native-write lower bound; DELAY may have zero logical delta'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='portfolio268_raw.json');args=ap.parse_args()
 out={'run':'CERTIFIED_PORTFOLIO_DOVETAIL_REFEREE268','status':'PROVED_RESTRICTED_PLUS_COMPUTATIONAL',
      'theorem_scope':'fixed finite deterministic certified portfolio; no all-input polynomial envelope',
      'P_vs_NP':'OPEN','cases':{},'malformed':[]}
 for name,(F,pins) in CASES.items():
  assert grammar(F);pol=policy_records(F,pins);sched=schedule(F,pins,pol)
  cert=pol[0]['cert'];ok,v=verify_certificate(F,pins,cert);assert ok
  models=sum(source_sat(F,{**pins,**dict(zip([x for x in range(1,max(abs(y) for c in F for y in c)+1) if x not in pins],b))})
             for b in itertools.product((0,1),repeat=max(abs(y) for c in F for y in c)-len(pins)))
  out['cases'][name]={'source_bits':len(encode(F)),'pins':pins,'models':models,'label':'SAT' if models else 'UNSAT',
                      'certificate_kind':cert['kind'],'certificate_verified':ok,'policies':[{k:v for k,v in q.items() if k!='cert'} for q in pol],
                      'scheduler':sched}
 out['F9_SU']=su_control(F9);out['F9_XOR']=xor_diag(F9)
 bad=[(),((1,1,2),),((1,-2,3),),((1,2,3),),F9+(F9[0],)]
 out['malformed']=[{'index':i,'rejected':not grammar(x)} for i,x in enumerate(bad)];assert all(x['rejected'] for x in out['malformed'])
 cert,_w,_b=certificate(F9,{1:0,2:0,8:1,9:1});forged=json.loads(json.dumps(cert));forged['assignment'][0]^=1
 ok,_=verify_certificate(F9,{1:0,2:0,8:1,9:1},forged);assert not ok
 cert,_w,_b=certificate(F9,{8:0,3:0,7:0,6:0,1:1,5:1});forged=json.loads(json.dumps(cert));forged['rows'].pop()
 ok,_=verify_certificate(F9,{8:0,3:0,7:0,6:0,1:1,5:1},forged);assert not ok
 out['forgery_controls']={'bad_SAT_witness_rejected':True,'incomplete_UNSAT_table_rejected':True}
 Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'PASS','cases':{k:(v['label'],v['models'],v['scheduler']['winner']) for k,v in out['cases'].items()},
                   'all_restart_bounds':all(v['scheduler']['bound_holds'] for v in out['cases'].values()),'P_vs_NP':'OPEN'},indent=2))

if __name__=='__main__':main()
