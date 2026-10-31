#!/usr/bin/env python3
"""Charged adaptive policy countercontrol for ARC-BRANCH-MASS-GATE261."""
import json,pathlib,importlib.util
here=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('arc261',here/'arc261_experiment.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
F={'W1_UNSAT':m.W1,'SWAP6_SAT':m.SWAP6,'W1_RENAMED_UNSAT':m.rename(m.W1,81),'SWAP6_RENAMED_SAT':m.rename(m.SWAP6,81)}
out=[];full={}
for name,f in F.items():
 n=15
 for p in ('first','max','min'):
  r=m.branch_partition(f,n,8,policy=p)
  full[name+':'+p]=r
  out.append({'name':name,'policy':p,'cutoff':8,'q_children':r['child_leaves'],'certified_P_volume':r['pruned_volume'],'terminal_S_volume':r['sat_terminal_volume'],'child_E_volume':r['child_volume'],'child_bits_max':r['max_child_bits'],'selected_events':r['combined_events'],'visited_nodes':r['nodes'],'candidate_tests':r['counts'].get('candidate_tests',0),'models':r['oracle_model_count']})
(here/'policy_full.json').write_text(json.dumps(full,indent=2,sort_keys=True))
(here/'policy.json').write_text(json.dumps(out,indent=2,sort_keys=True))
print(json.dumps(out,indent=2))
