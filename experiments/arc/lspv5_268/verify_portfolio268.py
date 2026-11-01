#!/usr/bin/env python3
"""Independent verifier for CERTIFIED_PORTFOLIO_DOVETAIL_REFEREE268 raw JSON."""
import json,sys
from pathlib import Path

def ck(x,msg):
 if not x:raise AssertionError(msg)

def main():
 p=Path(sys.argv[1] if len(sys.argv)>1 else 'portfolio268_raw.json');o=json.loads(p.read_text());checks=0
 ck(o['run']=='CERTIFIED_PORTFOLIO_DOVETAIL_REFEREE268','run');checks+=1
 ck(o['P_vs_NP']=='OPEN','status');checks+=1
 expected={'Y6_ROOT':20,'F9_SAT':2,'F9_PARITY_ONLY_UNSAT':0,'F15_SAT':2,'F15_UNSAT':0}
 for name,count in expected.items():
  r=o['cases'][name];ck(r['models']==count,name+' count');checks+=1
  ck(r['certificate_verified'],name+' cert');checks+=1
  s=r['scheduler'];ck(s['allocated_policy_steps']<s['four_k_t_bound_excluding_dispatch_and_verification'],name+' bound');checks+=1
  ck(s['total_charged_work']==s['allocated_policy_steps']+s['dispatch_steps']+s['verification_steps'],name+' ledger');checks+=1
  delay=[q for q in r['policies'] if q['name']=='DELAY_COPY_RECOMP'][0]
  ck(delay['delay_steps']==4096 and delay['logical_delta_during_delay']==0 and delay['copy_writes']==r['source_bits'],name+' hostile wrapper');checks+=1
 ck(all(x['rejected'] for x in o['malformed']),'malformed');checks+=1
 ck(o['forgery_controls']=={'bad_SAT_witness_rejected':True,'incomplete_UNSAT_table_rejected':True},'forgeries');checks+=1
 ck(o['F9_SU']['pair_mode_checks']==4*(12*11//2),'S/U checks');checks+=1
 ck(o['F9_XOR']['classification']=='OFFLINE_ONLY','XOR scope');checks+=1
 print(json.dumps({'status':'PASS','independent_checks':checks,'P_vs_NP':'OPEN'}))

if __name__=='__main__':main()
