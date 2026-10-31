#!/usr/bin/env python3
"""Standalone compact reproducer of source-only cube-blocker resolution.
No external packages. Full 28-case producer and raw proof DAG are in the ZIP archive.
"""
import itertools, json

def solve(F, cube):
    F=[tuple(C) for C in F]
    proof=[{'kind':'source','source':j,'clause':list(C)} for j,C in enumerate(F)]
    variables=sorted({abs(x) for C in F})
    def conflict(a):
        for j,C in enumerate(F):
            if all(abs(l) in a and a[abs(l)]!=(l>0) for l in C):
                return j
        return None
    def search(a):
        j=conflict(a)
        if j is not None: return False,j,None
        if all(any(abs(l) in a and a[abs(l)]==(l>0) for l in C) for C in F):
            return True,None,{v:a.get(v,False) for v in variables}
        x=next(v for v in variables if v not in a)
        a[x]=False;left=search(a);a.pop(x)
        if left[0]: return left
        if x not in proof[left[1]]['clause']: return left
        a[x]=True;right=search(a);a.pop(x)
        if right[0]: return right
        if -x not in proof[right[1]]['clause']: return right
        A=set(proof[left[1]]['clause']);B=set(proof[right[1]]['clause'])
        R=sorted((A-{x})|(B-{-x}),key=lambda z:(abs(z),z<0))
        assert not (set(R)&{-v for v in R})
        proof.append({'kind':'resolve','left':left[1],'right':right[1],
                      'pivot':x,'clause':R})
        return False,len(proof)-1,None
    good,root,witness=search(dict(cube))
    if not good:
        D=proof[root]['clause']
        assert all(abs(l) in cube and cube[abs(l)]!=(l>0) for l in D)
    else: D=None
    for j,p in enumerate(proof):
        if p['kind']=='source':
            assert p['clause']==list(F[p['source']])
        else:
            A=set(proof[p['left']]['clause'])
            B=set(proof[p['right']]['clause'])
            x=p['pivot']
            assert p['left']<j and p['right']<j and x in A and -x in B
            assert set(p['clause'])==(A-{x})|(B-{-x})
    for bits in itertools.product((False,True),repeat=len(variables)):
        a=dict(zip(variables,bits))
        f=all(any(a[abs(l)]==(l>0) for l in C) for C in F)
        if f and D is not None:
            assert any(a[abs(l)]==(l>0) for l in D)
        if f and all(a[k]==v for k,v in cube.items()):
            assert good
    return {'source_sat_under_cube':good,'source_clause_blocker':D,
            'resolution_steps':sum(p['kind']=='resolve' for p in proof),
            'witness':witness}

def clause(bits):
    return [i if b==0 else -i for i,b in enumerate(bits,1)]
F7=[clause(b) for b in itertools.product((0,1),repeat=3) if b!=(1,1,1)]
F8=[clause(b) for b in itertools.product((0,1),repeat=3)]
cases={'conditional_SAT_parent':([(1,2),(1,-2)],{1:False}),
       'renamed_SAT_parent':([(-1,-2),(-1,2)],{1:True}),
       'F7_unique_SAT_parent':(F7,{1:False}),
       'F8_UNSAT_parent':(F8,{})}
out={name:solve(F,cube) for name,(F,cube) in cases.items()}
assert out['conditional_SAT_parent']['source_clause_blocker']==[1]
assert out['renamed_SAT_parent']['source_clause_blocker']==[-1]
assert out['F7_unique_SAT_parent']['source_clause_blocker']==[1]
assert out['F8_UNSAT_parent']['source_clause_blocker']==[]
print(json.dumps({'status':'PASS','cases':out},indent=2))
