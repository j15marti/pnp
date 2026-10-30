#!/usr/bin/env python3
"""Independent compact reproducer for LSPV-2 POLICY-ENTRY-GATE253.
Standard library only. Focus: source-indexed entry projection and sharp
width thresholds. Full 476-line experiment and raw data are in run ZIP.
"""
from itertools import product
def sat(F,a):
    return all(any(a[abs(l)] == (l>0) for l in c) for c in F)
def restrict(F,beta):
    return [tuple(l for l in c if abs(l) not in beta)
            for c in F if not any(abs(l) in beta and beta[abs(l)] == (l>0) for l in c)]
def belongs(F,k):
    if k=='horn':return all(sum(l>0 for l in c)<=1 for c in F)
    if k=='dual':return all(sum(l<0 for l in c)<=1 for c in F)
    return all(len(c)<=2 for c in F)
def entry(F,B,k):
    B=set(B);out=[]
    for j,c in enumerate(F,1):
        D=tuple(l for l in c if abs(l) in B)
        R=tuple(l for l in c if abs(l) not in B)
        bad=({'horn':sum(l>0 for l in R)>1,
              'dual':sum(l<0 for l in R)>1,
              'krom':len(R)>2})[k]
        if bad:out.append((j,D))
    return out
def models(Q,B):
    B=sorted(B)
    for vals in product((False,True),repeat=len(B)):
        a=dict(zip(B,vals))
        if all(any(a[abs(l)] == (l>0) for l in c) for j,c in Q):
            yield a
def check(F,B,k):
    Q=entry(F,B,k)
    for vals in product((False,True),repeat=len(B)):
        a=dict(zip(sorted(B),vals))
        lhs=belongs(restrict(F,a),k)
        rhs=all(any(a[abs(l)] == (l>0) for l in c) for j,c in Q)
        assert lhs==rhs,(F,B,k,a,Q)
    return Q
def parity3():
    out=[]
    for bits in product((False,True),repeat=3):
        out.append(tuple(v if b else -v for v,b in zip((1,2,3),bits)))
    return out
def main():
    H=parity3()
    Hsat=H[1:]
    controls=[H,Hsat,[(1,2,3),(-3,)],[(1,2,3),(1,2,-3)]]
    verified=0
    for F in controls:
        n=3
        for bits in product((False,True),repeat=3):
            a={i+1:bits[i] for i in range(3)}
            assert isinstance(sat(F,a),bool)
        for mask in product((False,True),repeat=3):
            B=[i+1 for i,b in enumerate(mask) if b]
            for kind in ('horn','dual','krom'):
                Q=check(F,B,kind)
                assert all(len(c)<=1 for _,c in Q)
                verified+=1
    # A proper H can be UNSAT while every constructed parent is SAT.
    for H0 in (H,Hsat):
        n=3;B=set(range(1,n+1))
        for kind,outside in [('horn',(4,5)),('dual',(-4,-5)),('krom',(4,5,6))]:
            F=[tuple(outside)+tuple(c) for c in H0]
            Q=entry(F,B,kind)
            assert [c for _,c in Q]==H0
            a={i:False for i in B}
            a.update({abs(l):l>0 for l in outside})
            assert sat(F,a)
            assert bool(list(models(Q,B)))==any(
                sat(H0,dict(zip(range(1,4),bits)))
                for bits in product((False,True),repeat=3))
            verified+=1
    # Failure of a fixed-B class-selection test is NOT original UNSAT.
    F=[(1,2,3),(1,2,-3)]
    assert list(models(entry(F,{3},'horn'),{3}))==[]
    assert sat(F,{1:True,2:False,3:False})
    # Failure of the one selected Horn cofactor is NOT original UNSAT.
    F=[(1,2,3),(-3,)]
    assert list(models(entry(F,{3},'horn'),{3}))==[{3:True}]
    assert not sat(F,{1:True,2:False,3:True})
    assert sat(F,{1:True,2:False,3:False})
    print({'status':'PASS','cases':verified,'source_indexed_policy_projections':True,
           'full_experiment':'see run ZIP; 67 SAT/UNSAT controls'})
if __name__=='__main__':main()
