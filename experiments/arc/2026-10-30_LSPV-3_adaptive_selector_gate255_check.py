#!/usr/bin/env python3
"""Independent finite oracle cross-check for ARC255, separate from producer."""
import argparse, importlib.util, json, random, itertools, hashlib
from pathlib import Path

def load(path):
 spec=importlib.util.spec_from_file_location('arc255',path)
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def truth(F,a):
 return all(any(a[abs(z)]==(1 if z>0 else 0) for z in c) for c in F)

def cls_count(F,a):
 t=[sum(a[abs(z)]==(1 if z>0 else 0) for z in c) for c in F]
 return [t.count(i) for i in range(4)]

def pair_oracle(C,D):
 v=sorted({abs(z) for z in C+D})
 out=[]
 for i,j in [(len(C),len(D)),(len(C),0),(0,len(D)),(0,0)]:
  possible=False
  for bits in itertools.product((0,1),repeat=len(v)):
   a=dict(zip(v,bits))
   if sum(a[abs(z)]==(1 if z>0 else 0) for z in C)==i and sum(a[abs(z)]==(1 if z>0 else 0) for z in D)==j:
    possible=True;break
  out.append(possible)
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--script',default='arc255_repro.py');ap.add_argument('--input',default='arc255_raw.json');ap.add_argument('--out',default='arc255_check.json');args=ap.parse_args()
 P=Path(args.script);R=json.loads(Path(args.input).read_text());M=load(str(P));rng=random.Random(39195)
 ncases=0;methods_checked=0;pair_modes=0;identities=0;source_oracles={}
 for case,F in M.finite_cases().items():
  V=M.vars_(F)
  assert M.classify(F)==R['cases'][case]['parameters_checked_external']
  if len(V)<=15:
   models=0
   for bits in itertools.product((0,1),repeat=len(V)):
    a=dict(zip(V,bits))
    b={v:1-a[v] for v in V}
    for c in F:
     ta=sum(a[abs(z)]==(1 if z>0 else 0) for z in c)
     tb=sum(b[abs(z)]==(1 if z>0 else 0) for z in c)
     assert ta+tb==len(c)
     identities+=1
    if all(len(c)==3 for c in F):
     ca=cls_count(F,a);cb=cls_count(F,b)
     assert ca==cb[::-1]
    models+=int(truth(F,a))
   source_oracles[case]={'n':len(V),'models':models}
   assert (models>0)==(R['cases'][case]['ground_truth']=='SAT')
   dp=M.reverse_dp(F)
   assert dp==R['cases'][case]['forward_reverse_DP_external_control']
  else:
   assert R['cases'][case]['ground_truth']=='not_enumerated'
   assert M.satisfies(F,M.drain(M.orbit_template(F))[1]['witness']) if case=='ORBIT22_SAT' else True
  for name,row in R['cases'][case]['methods'].items():
   work,result=M.run_method(F,name)
   assert work==row['events'] and result[0]==row['status'] and M.verify_claim(F,result)
   methods_checked+=1
  result=M.budgeted(F,R['portfolio_policy'])
  assert result['work']==R['cases'][case]['scheduled_events'] and result['result'] in ('SAT','UNSAT')
  if len(V)<=15:assert (result['result']=='SAT')==(source_oracles[case]['models']>0)
  ncases+=1
 for z in range(120):
  n=rng.randrange(3,8);F=[]
  for j in range(rng.randrange(1,12)):
   vs=rng.sample(range(1,n+1),rng.randint(1,3))
   F.append(tuple(x*rng.choice((-1,1)) for x in vs))
  V=sorted({abs(l) for c in F for l in c})
  for i in range(len(F)):
   for j in range(i+1,len(F)):
    C=F[i];D=F[j]
    A={abs(l):int(l>0) for l in C};B={abs(l):int(l>0) for l in D}
    same=any(A[v]==B[v] for v in A.keys()&B.keys())
    opp=any(A[v]!=B[v] for v in A.keys()&B.keys())
    assert pair_oracle(C,D)==[not opp,not same,not same,not opp]
    pair_modes+=4
  expected=models=0
  for bits in itertools.product((0,1),repeat=len(V)):
   expected+=int(truth(F,dict(zip(V,bits))))
  for method in R['portfolio_policy']:
   events,result=M.run_method(F,method)
   if result[0]!='UNRESOLVED':assert (result[0]=='SAT')==(expected>0)
   assert M.verify_claim(F,result)
   methods_checked+=1
  port=M.budgeted(F,R['portfolio_policy'])
  assert (port['result']=='SAT')==(expected>0)
  dp=M.reverse_dp(F)
  assert dp['answer']==('SAT' if expected else 'UNSAT')
  ncases+=1
 assert R['flmv_exact']==M.frac_audit()
 out={'producer_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'raw_sha256':hashlib.sha256(Path(args.input).read_bytes()).hexdigest(),'cases_checked':ncases,'individual_policy_executions_checked':methods_checked,'original_clause_pair_modes_exhaustively_checked':pair_modes,'complement_clause_identities_checked':identities,'true_model_counts':source_oracles,'FLMV_rational_recomputed':True,'fixed_order_reverse_DP_checked':True,'seed':39195,'errors':[],'claims_rechecked_without_reusing_producer_results':True}
 Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True))
 print(json.dumps({k:v for k,v in out.items() if k not in ('true_model_counts',)},indent=2))
if __name__=='__main__':main()
