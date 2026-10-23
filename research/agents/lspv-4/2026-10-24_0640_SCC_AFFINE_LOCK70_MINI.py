#!/usr/bin/env python3
"""Independent finite checks for LSPV-4 SCC_AFFINE_LOCK70. Standard library."""
from itertools import product
from functools import lru_cache
import json

def xor_cnf(x,y,z,rhs):
    return [tuple(-v if bit else v for v,bit in zip((x,y,z),bits))
            for bits in product((0,1),repeat=3) if sum(bits)%2!=rhs]

def build(q,b):
    z=list(range(1,q+2));a,beta,c,d=range(q+2,q+6)
    local=[tuple(range(q+6+3*i,q+9+3*i)) for i in range(q+1)]
    n=4*q+8
    F=[(-a,beta),(-beta,a)]
    F += [(-z[i-1],z[i] if bit else -z[i]) for i,bit in enumerate(b,1)]
    E=[((a,c,z[0]),1),((a,c,z[q]),0),((a,d,z[0]),1),
       ((beta,c,d),0),((c,z[0],z[q]),1)]
    for i,(u,v,w) in enumerate(local):
        E += [((z[i],u,v),0),((z[i],u,w),0),((u,v,w),0)]
    for row,rhs in E:F.extend(xor_cnf(*row,rhs))
    assert n==max(abs(l) for cl in F for l in cl)
    return n,F,E,{'z':z,'a':a,'beta':beta,'c':c,'d':d,'local':local}

def gf_rank(rows):
    pivots={}
    for vars_ in rows:
        v=0
        for x in vars_:v^=1<<(x-1)
        while v:
            p=v.bit_length()-1
            if p not in pivots:pivots[p]=v;break
            v^=pivots[p]
    return len(pivots)

def exact_hit(F):
    support=frozenset(frozenset(map(abs,c)) for c in F if len(c)==3)
    @lru_cache(None)
    def recurse(s):
        if not s:return 0
        clause=next(iter(s))
        return 1+min(recurse(frozenset(c for c in s if x not in c)) for x in clause)
    return recurse(support)

def check(F,assign):
    return all(any(bool(assign[abs(l)])==(l>0) for l in c) for c in F)

def dpll(F):
    def rec(cs,partial):
        left=[]
        for c in cs:
            if any(abs(l) in partial and partial[abs(l)]==(l>0) for l in c):continue
            d=tuple(l for l in c if abs(l) not in partial)
            if not d:return False
            left.append(d)
        if not left:return True
        lit=next((c[0] for c in left if len(c)==1),None)
        if lit is not None:
            return rec(left,{**partial,abs(lit):lit>0})
        lit=min(left,key=len)[0]
        return rec(left,{**partial,abs(lit):True}) or rec(left,{**partial,abs(lit):False})
    return rec(F,{})

def main():
    tests=0;rows=[]
    for q in range(1,6):
        for b in product((0,1),repeat=q):
            n,F,E,v=build(q,b)
            assert n==4*q+8 and len(F)==13*q+34
            assert sum(len(c)==3 for c in F)==12*q+32
            assert sum(len(c)==2 for c in F)==q+2
            assert gf_rank([s for s,r in E])==3*q+8
            assert gf_rank([s for s,r in E]+[(v['a'],v['beta'])])==3*q+9
            if q<=4:assert exact_hit(F)==q+3
            expected=(0 in b)
            if expected:
                first=b.index(0)+1
                assign={v['z'][i]:i<first for i in range(q+1)}
                for x in ('a','beta','c','d'):assign[v[x]]=False
                for i,(u,x,y) in enumerate(v['local']):
                    assign[u]=False;assign[x]=assign[v['z'][i]]
                    assign[y]=assign[v['z'][i]]
                assert check(F,assign)
            if q<=3:assert dpll(F)==expected
            tests+=9
            if b in [(1,)*q,(1,)*(q-1)+(0,)]:
                rows.append({'q':q,'b':''.join(map(str,b)),'SAT':expected,
                             'n':n,'clauses':len(F),'k':12*q+32,'h':q+3})
    print(json.dumps({'checked_orientation_instances':62,
                      'assertion_groups':tests,'failures':0,'sample':rows},indent=2))
if __name__=='__main__':main()
