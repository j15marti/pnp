#!/usr/bin/env python3
"""No-producer-import verifier for REFEREE269 raw JSON."""
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);o=json.loads(p.read_text());checks=0
def ck(x,m):
 global checks;checks+=1
 if not x:raise AssertionError(m)
ck(o['run']=='SEMANTIC_INTERFACE_TRANSFER_REFEREE269','run')
ck(o['P_vs_NP']=='OPEN','status')
ck(o['matrix']==[[34,47],[23,36]],'W')
ck(o['matrix_PA']==[[1,1],[0,0]],'WA')
ck(o['matrix_PB']==[[0,0],[0,0]],'WB')
ck([x['trace_count'] for x in o['family'][:4]]==[70,4614,312970,21248098],'counts')
for x in o['family']:
 ck(x['grammar'] and x['connected'],'family grammar/connected')
 if x['t']<=3:ck(x['P_models']==1 and x['Q_models']==0,'both labels')
ck(len(o['Q_local_complete_UNSAT_cover'])==32,'cover size')
ck(all(x['bad_clause_ids'] for x in o['Q_local_complete_UNSAT_cover']),'cover sound')
ck(o['controls']=={'F15_SAT_models':2,'F15_UNSAT_models':0,'F9_SAT_models':2,'F9_SU_pair_modes':264,'F9_parity_only_UNSAT_models':0,'Y6_models':20,'malformed_rejected':6},'controls')
ck(o['semantic_cache_firewall']['exact_matrices_differ'],'cache')
ck(not o['charged_recurrence']['all_input_condition_proved'],'scope')
ck(o['wrappers']['DELAY_logical_delta']==0 and o['offline_XOR']['binary']['steps']==511,'xor scope')
print(json.dumps({'status':'PASS','checks':checks,'P_vs_NP':'OPEN'},indent=2))
