#!/usr/bin/env python3
"""Independent no-producer-import source-indexed individual output-clause accessor.
Explicitly charges naive prefix width-type scan for each arbitrary record lookup.
This is a Python counted-record experiment, not a native FLMV TM run.
"""
import ast,json,pathlib,hashlib
HERE=pathlib.Path(__file__).resolve().parent
U_FILE=HERE/'u198_source.txt'
if not U_FILE.exists():U_FILE=HERE.parents[2]/'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt'
U=ast.literal_eval(''.join(l for l in U_FILE.read_text().splitlines(True) if not l.startswith('#')))
D=U[:1]+U[2:]
Y6=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]]
F9=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]]
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

if (HERE/'bridge317_compiled_formula.json').exists():
    out=json.loads((HERE/'bridge317_compiled_formula.json').read_text())
else:
    # Fully source-indexed independent materializer, for repository-only execution.
    out=[];base=12*9
    for cl in H:
        if len(cl)==2:
            for group in range(4):
                dbase=base+198*group
                for cp,port in enumerate((194,196,197)):
                    out.append(shift(cl,9*(3*group+cp))+[dbase+port])
                out.extend(shift(z,dbase) for z in D)
            base+=792
        else:
            out.extend(shift(cl,9*cp) for cp in range(12))
            for z in range(130):out.extend(shift(y,base+6*z) for y in Y6)
            out.extend(shift(z,base+780) for z in F9)
            base+=789
    assert base==10374
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
(HERE/'bridge317_bitlocal_results.json').write_text(json.dumps(metrics,indent=2,sort_keys=True)+'\n')
print(json.dumps(metrics,indent=2,sort_keys=True))
