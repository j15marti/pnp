#!/usr/bin/env python3
"""ARC-ADAPTIVE-COMB170: exact finite ordinary-CNF two-level falsification controls.
Deterministic; standard library only. Run: python arc_adaptive_comb170_repro.py > arc_adaptive_comb170_results.json
Every reported SAT call is independently parsed and decided by generic DP-resolution.
The script measures logical bits serialized, not FLMV TM cycles or peak tape cells.
"""
import json
from collections import Counter
from hashlib import sha256

SEED = 202610250637  # deterministic, no random sampling

def forced_gadget(x, a, b):
    return [(x, pa*a, pb*b) for pa in (1,-1) for pb in (1,-1)]

def sat_core(k, unsat):
    """Seven/eight-clause exclusion cube, plus disjoint positive padding."""
    z = (3*k+1,3*k+2,3*k+3)
    cube = [tuple(sig[i]*z[i] for i in range(3))
            for sig in ((p,q,r) for p in (1,-1) for q in (1,-1) for r in (1,-1))]
    clauses = cube if unsat else cube[1:]
    padding = max(1, round(k**.25))
    for j in range(padding):
        p = 3*k+4+3*j
        clauses.append((p,p+1,p+2))
    return clauses

def root(k, unsat):
    g = [c for i in range(k) for c in forced_gadget(3*i+1,3*i+2,3*i+3)]
    return g + sat_core(k, unsat)

def to_dimacs(clauses):
    n=max((abs(z) for c in clauses for z in c),default=0)
    return f'p cnf {n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)

def from_dimacs(s):
    lines=s.splitlines()
    if not lines or len(lines[0].split())!=4 or lines[0].split()[:2]!=['p','cnf']:
        raise ValueError('invalid header')
    _,_,sn,sm=lines[0].split(); n=int(sn);m=int(sm)
    cs=[]
    for line in lines[1:]:
        if not line or line.startswith('c '):continue
        ints=[int(x) for x in line.split()]
        if not ints or ints[-1]!=0 or any(abs(t)>n or t==0 for t in ints[:-1]):
            raise ValueError('invalid clause')
        cs.append(tuple(ints[:-1]))
    if len(cs)!=m:raise ValueError('clause-count mismatch')
    return cs

def restrict(clauses, assumptions):
    out=[]
    for c in clauses:
        if any((abs(x) in assumptions and (x>0)==assumptions[abs(x)]) for x in c):
            continue
        new=tuple(x for x in c if abs(x) not in assumptions)
        out.append(new)
    return out

def dense_rename(clauses):
    """Source-name bijection and complete ordinary child serialization."""
    variables=sorted({abs(x) for c in clauses for x in c})
    perm={x:i+1 for i,x in enumerate(variables)}
    return [tuple((1 if x>0 else -1)*perm[abs(x)] for x in c) for c in clauses]

def dp_exact(clauses):
    """Generic Davis-Putnam variable elimination, not a gadget-specific oracle."""
    C={frozenset(c) for c in clauses}
    if frozenset() in C:return False
    names=sorted({abs(x) for c in C for x in c})
    for v in names:
        plus=[c for c in C if v in c];minus=[c for c in C if -v in c]
        rest={c for c in C if v not in c and -v not in c}
        if plus and minus:
            for p in plus:
                for m in minus:
                    res=(p-{v}) | (m-{-v})
                    if any(-z in res for z in res): continue
                    f=frozenset(res)
                    if not f:return False
                    rest.add(f)
        C=rest
    return True

def offspine_gadget_unsat():
    gadget=forced_gadget(1,2,3)
    return not dp_exact(restrict(gadget,{1:False}))

def experiment():
    assert offspine_gadget_unsat()
    records=[]
    assertions=0; stage_calls=0; child_serialized=0; guest_calls=0; read_bits=0; written_bits=0
    for k in (4,16,36,64,100,256,400):
        r=int(k**.5)
        assert r*r==k
        first=k-r
        for unsat in (False,True):
            parent=root(k,unsat)
            assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in parent)
            freq=Counter(abs(x) for c in parent for x in c)
            assert max(freq.values())<=8
            pbits=len(to_dimacs(parent).encode())*8
            pcheck=dp_exact(from_dimacs(to_dimacs(parent)))
            assert pcheck== (not unsat)
            assertions+=3
            child=dense_rename(restrict(parent,{3*i+1:True for i in range(first)}))
            s1=to_dimacs(child);c1=from_dimacs(s1)
            assert len(c1)==len(parent)-4*first
            assert dp_exact(c1)==pcheck
            assertions+=2;stage_calls+=1
            grandchild=dense_rename(restrict(c1,{3*j+1:True for j in range(r)}))
            s2=to_dimacs(grandchild);c2=from_dimacs(s2)
            assert len(c2)==len(sat_core(k,unsat))
            assert dp_exact(c2)==pcheck
            assertions+=2;stage_calls+=1;guest_calls+=1
            for j in range(k):
                gg=forced_gadget(3*j+1,3*j+2,3*j+3)
                assert not dp_exact(restrict(gg,{3*j+1:False}))
                assertions+=1
            b1=len(s1.encode())*8;b2=len(s2.encode())*8
            child_serialized+=2
            read_bits+=pbits+b1+b2
            written_bits+=b1+b2
            records.append({'k':k,'label':'UNSAT' if unsat else 'SAT','parent_bits':pbits,
                            'first_child_bits':b1,'second_child_bits':b2,
                            'clauses':[len(parent),len(c1),len(c2)],
                            'forced_pins_stage1':first,'forced_pins_stage2':r,
                            'local_contradiction_siblings':k,'guest_calls':1,
                            'max_occurrence':max(freq.values()),
                            'DP_parent':pcheck,'DP_child':dp_exact(c1),'DP_grandchild':dp_exact(c2)})
    return {'run_id':'ARC-ADAPTIVE-COMB170','seed':SEED,'mode':'deterministic exact parameter sweep',
            'status':'COMPUTATIONAL finite audit, supporting symbolic restricted theorem',
            'assertions_passed':assertions,'failures':0,
            'stage_invocations':stage_calls,'ordinary_guest_calls':guest_calls,
            'ordinary_children_serialized':child_serialized,
            'declared_serialized_bits_written':written_bits,
            'declared_serialized_bits_read':read_bits,
            'instances':records,
            'limitations':['Davis-Putnam resolves small bounded-occurrence gadgets only',
                           'Python memory and operation counts are not FLMV Turing-machine resources',
                           'Promise family is syntactically easy, not an ARC all-input contraction',
                           'Worst-case off-promise total fallback to A retains the source K exponent']}

if __name__=='__main__':
    obj=experiment()
    print(json.dumps(obj,sort_keys=True,indent=2))
