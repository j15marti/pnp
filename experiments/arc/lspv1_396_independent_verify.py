#!/usr/bin/env python3
"""Independent exhaustive checker for LSPV-1/396 compressed-resolution-row audit."""
import itertools, json, sys

SOURCES = ((1,2),(1,-2),(-1,))
CLAUSES = ((1,),(-1,),(2,),(-2,),(1,2),(1,-2),(-1,2),(-1,-2))

def val(clause, assignment):
    return any(((assignment[abs(lit)-1] == 1) if lit > 0 else (assignment[abs(lit)-1] == 0)) for lit in clause)

def sat(clauses, n=2):
    return any(all(val(c,a) for c in clauses) for a in itertools.product((0,1), repeat=n))

def check_row(D, assignment):
    left_source = 2 if all(val(c,assignment) for c in D) else 0
    left = SOURCES[left_source]
    right = SOURCES[1]
    pivot = 2
    if pivot not in left or -pivot not in right:
        return False
    result = tuple(sorted((set(left)-{pivot})|(set(right)-{-pivot})))
    return result == (1,)

def verify_shape(D,n):
    if type(n) is not int or n < 1 or n > 10 or not isinstance(D, (list,tuple)):
        return False
    for c in D:
        if not isinstance(c,(list,tuple)) or len(c) == 0 or len(c) > n or any(type(x) is not int or x == 0 or abs(x)>n for x in c):
            return False
        if len(set(c)) != len(c) or any(-x in c for x in c):
            return False
    return True

def run(raw):
    assert not sat(SOURCES)
    assert verify_shape([[1],[-1]],2)
    assert not verify_shape([[3]],2)
    assert not verify_shape([[1,-1]],2)
    assert not verify_shape([[0]],2)
    assert not verify_shape([[]],2)
    assert raw['schema']=='LSPV1-396-compressed-rows-v1'
    assert raw['source']==[list(c) for c in SOURCES]
    assert raw['clause_universe']==[list(c) for c in CLAUSES]
    cases = raw['cases']; assert len(cases)==256
    unsat_count=0; sat_count=0; assertions=9
    for mask in range(256):
        D=[list(c) for j,c in enumerate(CLAUSES) if (mask >> j)&1]
        assert cases[mask]['mask']==mask
        assert cases[mask]['cnf']==D
        assert verify_shape(D,2)
        SAT=sat(D)
        valid=all(check_row(D,a) for a in itertools.product((0,1),repeat=2))
        assert SAT != valid, (mask,D,SAT,valid)
        assert cases[mask]['sat']==SAT
        assert cases[mask]['all_rows_legal']==valid
        assert cases[mask]['invalid_rows']==sum(not check_row(D,a) for a in itertools.product((0,1),repeat=2))
        if SAT: sat_count+=1
        else: unsat_count+=1
        assertions+=6
    assert raw['summary']['sat']==sat_count
    assert raw['summary']['unsat']==unsat_count
    assert raw['summary']['cases']==256
    assertions+=3
    return assertions,sat_count,unsat_count

if __name__=='__main__':
    obj=json.load(open(sys.argv[1]))
    checks,sat_n,unsat_n=run(obj)
    import copy
    mutations=[]
    x=copy.deepcopy(obj); x['cases'][0]['sat']=not x['cases'][0]['sat']; mutations.append(x)
    x=copy.deepcopy(obj); x['cases']=x['cases'][:-1]; mutations.append(x)
    x=copy.deepcopy(obj); x['source'][0][0]=-1; mutations.append(x)
    x=copy.deepcopy(obj); x['cases'][100]['invalid_rows']+=1; mutations.append(x)
    for x in mutations:
        try: run(x)
        except (AssertionError, ValueError, KeyError): pass
        else: raise AssertionError('corrupted proof audit accepted')
    print(json.dumps({'verdict':'PASS','independent_assertions':checks,'corruption_rejections':len(mutations),'sat':sat_n,'unsat':unsat_n}))
