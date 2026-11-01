#!/usr/bin/env python3
"""Exact integrated fallback controller benchmark with charged policy proxy.
All selected work is a host-level proxy, not native FLMV time/space.
"""
import json
from pathlib import Path
import integrated_sat_wrapper_dag as old
import saturated_cycle_affine_terminal_greedy as new

def terminal_wrapper(F,p,z):
    gate=new.exact_terminal(F,p,cap=50000)
    z.policy_checks+=1
    g=gate.get('gate',{})
    z.source_gate_scans+=g.get('source_literal_reads',0)
    z.triangle_tests+=g.get('cycle_candidate_checks',0)
    z.triangle_search_nodes+=g.get('cycle_search_nodes',0)
    z.affine_xors+=gate.get('affine_work',0)
    if gate['status']=='SAT':
        a={v:x for v,x in enumerate(gate['witness'],1)}
        assert old.sat(F,a)
        z.literal_tests+=3*len(F)
        z.proof_records.append({'status':'SAT','source_witness':gate['witness'],'pack':g.get('cycles')})
        return True
    if gate['status'] in ('UNSAT_GAP','UNSAT_AFFINE_EXHAUSTED','UNSAT_EMPTY'):
        z.proof_records.append({'status':'UNSAT','exhaustive_affine_branches':gate.get('branches',0)})
        return False
    return None

def solve(F,p,z):
 def walk(p):
    z.nodes+=1;z.proof_nodes+=1
    if z.nodes>15000:raise RuntimeError('cap hit; never claim UNSAT')
    p,terminal=old.simplify_units(F,p,z)
    if terminal:return False
    facts=z.read(F,p)
    if all(t>0 for j,t,u in facts):
        a={v:p.get(v,0) for v in range(1,max(abs(l) for c in F for l in c)+1)}
        z.literal_tests+=3*len(F)
        assert old.sat(F,a)
        return True
    res=terminal_wrapper(F,p,z)
    if res is not None:return res
    v=next(v for v in range(1,max(abs(l) for c in F for l in c)+1) if v not in p)
    for b in (0,1):
        z.branch_edges+=1
        q=z.assign(F,p,v,b,'branch')
        if walk(q):return True
    return False
 return walk(p)

def main():
 cases=[('Y6',old.Y6,{}),('F15',old.F15,{}),('F15_U',old.F15,old.P_U),('F15_S',old.F15,old.P_S),('F15_Uplus6',old.F15,{**old.P_U,6:0})]
 obj={}
 for name,F,p in cases:
    zl=old.Ledger('UP-DPLL');zo=old.Ledger('prior-sign+affine');zn=old.Ledger('saturated-cycle-terminal')
    bl=old.controller(F,p,zl,gate=False)
    bo=old.controller(F,p,zo,gate=True)
    bn=solve(F,p,zn)
    actual=next(old.models(F,p),None) is not None
    assert bl==bo==bn==actual
    obj[name]={'status':'SAT' if actual else 'UNSAT',
        'baseline':{'nodes':zl.nodes,'selected_work':old.result_ledger(zl)['work_proxy']},
        'prior':{'nodes':zo.nodes,'selected_work':old.result_ledger(zo)['work_proxy']},
        'new':{'nodes':zn.nodes,'selected_work':old.result_ledger(zn)['work_proxy']}}
 print(json.dumps(obj,indent=2))
 with open(Path(__file__).resolve().parent / 'benchmark_saturated_cycle_controller_results.json','w') as out:json.dump(obj,out,indent=2)
if __name__=='__main__':main()
