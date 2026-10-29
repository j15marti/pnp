#!/usr/bin/env python3
"""Build explicit DIMACS fixtures and CSV from the completed audit outputs."""
from pathlib import Path
import csv
from hashlib import sha256
import json
from math import ceil
import BOUNDARY_BURDEN1 as bq

HERE=Path(__file__).resolve().parent


def emit_fixture(name,clauses):
    n,_,_=bq.validate(clauses)
    path=HERE/'fixtures'/(name+'.cnf')
    path.parent.mkdir(exist_ok=True)
    text='p cnf '+str(n)+' '+str(len(clauses))+'\n'
    text+='\n'.join(' '.join(map(str,c))+' 0' for c in clauses)+'\n'
    path.write_text(text)
    return path.relative_to(HERE).as_posix()


def main():
    rows=[]
    codehash=sha256((HERE/'BOUNDARY_BURDEN1.py').read_bytes()).hexdigest()
    total_boundaries=0
    for case in ('6','9','12','15','W1'):
        raw=json.loads((HERE/('BOUNDARY_BURDEN1_small_'+case+'.json')).read_text())
        assert raw['code_sha256']==codehash
        r=raw['result']; total_boundaries+=r['boundary_sets']
        clauses=bq.TORUS.W1 if case=='W1' else bq.ORIGINAL.canonical_signed(int(case))
        row={'family':'W1' if case=='W1' else 'periodic cycle','n':r['n'],'m':r['m'],
             'label':'SAT' if r['source_models'] else 'UNSAT',
             'old_lower':r['bounds']['user_rounded'],
             'new_lower':r['bounds']['stronger_exact_integer'],
             'b':r['best']['b'],'q':r['best']['q'],'burden':r['global_burden_optimum_exact'],
             'status':'EXACT all boundaries', 'DPLL_nodes':r['independent_DPLL']['stats']['nodes'],
             'fixture':emit_fixture('W1_UNSAT' if case=='W1' else 'periodic_'+case,clauses)}
        rows.append(row)
        if case=='W1':
            decision=bq.independent_dpll(bq.TORUS.V)
            assert decision['answer']=='SAT'
            rows.append({**row,'family':'V same-scope mutation','label':'SAT',
                         'DPLL_nodes':decision['stats']['nodes'],'fixture':emit_fixture('V_SAT',bq.TORUS.V)})
    for stage,cases in [('cycle',(4,8,16)),('torus',(6,12,24))]:
        for case in cases:
            raw=json.loads((HERE/('BOUNDARY_BURDEN1_'+stage+'_'+str(case)+'.json')).read_text())
            assert raw['code_sha256']==codehash
            r=raw['result'];best=r['best_tested_decomposition']
            if stage=='cycle':
                formulas=[bq.CYCLE.build_cycle(case,['M']*case),
                          bq.CYCLE.build_cycle(case,['W']+['M']*(case-1))]
            else:
                torus,_=bq.TORUS.torus(case)
                formulas=[bq.TORUS.connector(torus,v)[0] for v in (bq.TORUS.V,bq.TORUS.W1)]
            for i,(label,clauses) in enumerate(zip(('SAT','UNSAT'),formulas)):
                assert r['independent_DPLL'][i]['answer']==label
                rows.append({'family':stage+' matched pair','n':r['n'],'m':r['m'],'label':label,
                             'old_lower':r['bounds']['user_rounded'],'new_lower':r['bounds']['stronger_exact_integer'],
                             'b':best['b'],'q':best['q'],'burden':best['burden'],
                             'status':'ACHIEVED upper bound; selected boundaries',
                             'DPLL_nodes':r['independent_DPLL'][i]['stats']['nodes'],
                             'fixture':emit_fixture(stage+'_'+str(case)+'_'+label,clauses)})
    for n in (30,60,120,300,600):
        emit_fixture('periodic_'+str(n),bq.ORIGINAL.canonical_signed(n))
    target=HERE/'BOUNDARY_BURDEN1_table.csv'
    with target.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    checks=[]
    for n in range(3,3001,3):
        bounds=bq.integer_bounds(n)
        assert bounds['stronger_exact_integer']==ceil(bounds['stronger_continuous']-1e-12)
        assert bounds['old_exact_integer_relaxation']==bounds['user_rounded']
        assert bounds['stronger_exact_integer']>=bounds['user_rounded']
    for n in (15,30,60,81,120,189,240,300,600,621,9999):
        checks.append({'n':n,**bq.integer_bounds(n)})
    (HERE/'BOUNDARY_BURDEN1_integer_bounds.json').write_text(json.dumps({'admissible_sizes_checked':1000,'bounds':checks},indent=2)+'\n')
    assert total_boundaries==70208
    print(json.dumps({'CSV_rows':len(rows),'DIMACS_fixtures':len(list((HERE/'fixtures').glob('*.cnf'))),
                      'exhaustive_boundary_evaluations':total_boundaries,
                      'integer_rounding_checks':1000}))


if __name__=='__main__':
    main()
