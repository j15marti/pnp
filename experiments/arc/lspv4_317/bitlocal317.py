#!/usr/bin/env python3
"""Independent no-producer-import source-indexed individual output-clause accessor.
Explicitly charges naive prefix width-type scan for each arbitrary record lookup.
This is a Python counted-record experiment, not a native FLMV TM run.
"""
import ast,json,pathlib,hashlib
ROOT=pathlib.Path(__file__).resolve().parent
U=ast.literal_eval(''.join(l for l in (ROOT/'u198_source.txt').read_text().splitlines(True) if not l.startswith('#')))
D=U[:1]+U[2:]
Y6=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]]
F9=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[7,8,9],[2,4,7],[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]]
H=[[1,2],[5,3],[6,8]]+F9[2:]

def shift(c,a):return [(-1 if v<0 else 1)*(abs(v)+a) for v in c]

metrics={'width_record_reads':0,'source_clause_full_reads':0,'gadget_record_reads':0,'queries':0}
def original_output_record(q):
    assert 0<=q<1064*len(H)
    j,k=divmod(q,1064)
    # Every type bit in a prefix is read from the original source in this stateless implementation.
    bpre=0
    for i in range(j):
        metrics['width_record_reads']+=1
        if len(H[i])==2:bpre+=1
    metrics['source_clause_full_reads']+=1
    original=H[j]
    a=12*9+789*j+3*bpre
    metrics['queries']+=1
    if len(original)==2:
        group,local=divmod(k,266)
        dbase=a+198*group
        if local<3:
            return shift(original,9*(3*group+local))+[dbase+(194,196,197)[local]]
        metrics['gadget_record_reads']+=1
        return shift(D[local-3],dbase)
    if k<12:return shift(original,9*k)
    k-=12
    if k<130*8:
        module,local=divmod(k,8)
        metrics['gadget_record_reads']+=1
        return shift(Y6[local],a+6*module)
    metrics['gadget_record_reads']+=1
    return shift(F9[k-130*8],a+130*6)

out=json.loads((ROOT/'bridge317_compiled_formula.json').read_text())
assert len(out)==13832
for q,c in enumerate(out):
    v=original_output_record(q)
    assert v==c,(q,c,v)
assert metrics['queries']==13832
assert metrics['width_record_reads']==82992
metrics['match_all_output_records']=True
metrics['same_machine_FLMV_TIMING']='NOT MEASURED'
metrics['charged_prefix_scan_work']='Theta(m) source width-record reads per individual guest output record in this stateless implementation'
metrics['linear_rolling_rank_alternative']='One source scan for monotonically increasing q, but random guest queries require charged cache or rescanning'
(ROOT/'bridge317_bitlocal_results.json').write_text(json.dumps(metrics,indent=2,sort_keys=True)+'\n')
print(json.dumps(metrics,indent=2,sort_keys=True))
