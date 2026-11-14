"""TMR-5/025 native reproducible syntax/oracle MCSP orientation audit."""
import itertools as it
import json

def block(v,i,b):
    j,k=(i+1)%v,(i+2)%v
    return [((i+1)*(1 if b else -1), (j+1)*(1 if a else -1),
             (k+1)*(1 if c else -1)) for a,c in it.product(range(2),repeat=2)]

def value(F,x):
    return all(any(x[abs(z)-1]==(z>0) for z in cl) for cl in F)

def pair(v,x):
    B=sum((block(v,i,b) for i,b in enumerate(x)),[])
    return B+block(v,0,x[0]),B+block(v,0,1-x[0])

def h_weight(F,v):
    return sum(value(F,x) for x in it.product(range(2),repeat=v))

def run():
    counts={'proper_formula':0,'witness_labels':0,'syntax_gap':0,
            'truth_table_composition':0,'cyclic_oracle_sharpness':0}
    small={(0,0,0,0),(1,1,1,1),(0,0,1,1),(0,1,0,1)}
    parity=(0,1,1,0)
    assert parity not in small and min(sum(a!=b for a,b in zip(parity,g)) for g in small)==2
    for v in range(3,7):
        for x in it.product(range(2),repeat=v):
            yes,no=pair(v,x)
            assert len(yes)==len(no)==4*(v+1)
            assert all(len({abs(t) for t in c})==3 for F in (yes,no) for c in F)
            counts['proper_formula']+=2
            assert [z for z in it.product(range(2),repeat=v) if value(yes,z)]==[x]
            assert not any(value(no,z) for z in it.product(range(2),repeat=v))
            counts['witness_labels']+=2
            assert ((yes[0][0]>0)==(yes[-4][0]>0))
            assert ((no[0][0]>0)!=(no[-4][0]>0))
            counts['syntax_gap']+=2
            assert h_weight(yes,v)==1 and h_weight(no,v)==0
            counts['truth_table_composition']+=2
    for v in range(1,6):
        M=2**v; N=3*M
        for q in range(M+1):
            ds=[sum(a in {(j+t)%M for t in range(q)} for j in range(N)) for a in range(M)]
            assert sum(ds)==N*q and len(set(ds))==1
            counts['cyclic_oracle_sharpness']+=2
    return {'status':'COMPUTATIONAL', 'input_v':'3..6 exhaustive assignments',
            'locality_v':'1..5 exhaustive singletons', 'seed':None,
            'checks':counts, 'total_checks':sum(counts.values()),
            'parity_gap_fraction':0.5, 'oracle_queries_for_syntax_family':0,
            'equal_clause_counts':True,'failed_assertions':0}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
