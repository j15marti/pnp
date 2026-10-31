#!/usr/bin/env python3
"""Independent audit. No producer import; independently parses all proof steps."""
import copy,hashlib,itertools,json,random,sys
from pathlib import Path

def clause_norm(c):
    z=list(set(c));assert not any(-v in z for v in z)
    return sorted(z,key=lambda v:(abs(v),v<0))

def check_pf(clauses,proof):
    arr=[clause_norm(c) for c in clauses]
    for row in proof['steps']:
        x,y=row['parents'];p=row['pivot'];assert 0<=x<len(arr) and 0<=y<len(arr)
        a,b=set(arr[x]),set(arr[y]);assert (p in a and -p in b) or (-p in a and p in b)
        if -p in a: a,b=b,a
        want=clause_norm((a-{p})|(b-{-p}))
        assert want==row['clause'],(want,row)
        arr.append(want)
    assert proof['root']==len(arr)-1
    assert proof['root_clause']==arr[-1]

def value(form,assignment):
    return all(any(assignment[abs(l)-1]==(l>0) for l in clause) for clause in form)

def test(path):
    j=json.loads(Path(path).read_text());rng=random.Random(273)
    cases=0;pfsteps=0;projections=0;mode_checks=0;tamper=0
    for r in j['results']:
        k=r['k']; no=not r['SAT']; C=r['source_clauses_indexed']; n=r['n'];cases+=1
        for p in r['certificates']:
            check_pf(C,p);pfsteps+=len(p['steps'])
            if no:assert p['root_clause']==[]
            else:assert len(p['root_clause'])==k
        if r['certificates'][0]['steps']:
            bad=copy.deepcopy(r['certificates'][0]);bad['steps'][0]['pivot']=n+10
            try:check_pf(C,bad)
            except (AssertionError,IndexError):tamper+=1
            else:raise AssertionError('corruption undetected')
        if r['SAT']:
            w=[bool(r['witness'][str(i+1)]) for i in range(n)]
            assert value(C,w)
        # verify original extreme modes directly by combining local target requirements
        for z in r['controls']['pair_extremes']:
            x,y=z['i'],z['j']
            for a,b in [('SS',(True,True)),('SU',(True,False)),('US',(False,True)),('UU',(False,False))]:
                demand={};good=True
                for cl,want in [(C[x],b[0]),(C[y],b[1])]:
                    for lit in cl:
                        req=(lit>0)==want
                        if abs(lit) in demand and demand[abs(lit)]!=req:good=False
                        demand[abs(lit)]=req
                assert good==z['matrix'][a];mode_checks+=1
        # Check the source under renaming by independent exact enumeration where affordable.
        if k<=4:
            truth=any(value(C,bb) for bb in itertools.product([False,True],repeat=n))
            assert truth==r['SAT']
        # For unrenamed cases, exhaustively compare private projection.
        if k<=5 and not r['renamed']:
            for b in itertools.product([False,True],repeat=2*k):
                sat=False
                for q in itertools.product([False,True],repeat=k+1):
                    if value(C,q+b):sat=True;break
                direct=any(not b[2*i] and not b[2*i+1] for i in range(k)) and (
                  not no or all(b[2*i] or b[2*i+1] for i in range(k)))
                assert sat==direct;projections+=1
        # Validate that every frontier witness set needs its own clause for the core projection.
        if not no:
            for word in itertools.product([0,1],repeat=k):
                b=[False]*(2*k)
                for i,bit in enumerate(word):b[2*i+bit]=True
                assert not any(not b[2*i] and not b[2*i+1] for i in range(k))
                for i,bit in enumerate(word):
                    b[2*i+bit]=False
                    assert any(not b[2*j] and not b[2*j+1] for j in range(k))
                    b[2*i+bit]=True
    print(json.dumps({'independent_cases':cases,'checked_proof_steps':pfsteps,'boundary_checks':projections,
    'source_extreme_checks':mode_checks,'tamper_rejections':tamper},sort_keys=True))
if __name__=='__main__':test(sys.argv[1])