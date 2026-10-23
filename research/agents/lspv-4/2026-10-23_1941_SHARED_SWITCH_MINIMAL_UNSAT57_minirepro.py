#!/usr/bin/env python3
"""Reproducer of LSPV-4 SHARED-SWITCH-MINIMAL-UNSAT57; Python stdlib only."""
import itertools, json
def source(q,sigma):
    assert q>=3 and len(sigma)==q
    s,t,y,z=q+1,q+2,q+3,q+4
    out=[]
    for i,bi in enumerate(sigma):
        a=i+1; b=(i+1)%q+1
        pair=((a,b),(-a,-b)) if bi else ((-a,b),(a,-b))
        out.extend([(s,*p) for p in pair])
    out.extend([(-s,t,y),(-s,t,-y),(-s,-t,z),(-s,-t,-z)])
    return q+4,out
def sat(clauses,a):
    return all(any(a[abs(x)-1]==(x>0) for x in c) for c in clauses)
def count(n,clauses):
    return sum(sat(clauses,a) for a in itertools.product((False,True),repeat=n))
def resolution(q,sigma):
    assert sum(sigma)%2==1
    n,cs=source(q,sigma)
    nodes=[frozenset(c) for c in cs];steps=[]
    def add(l,r,p):
        assert p in nodes[l] and -p in nodes[r]
        x=(nodes[l]-{p})|(nodes[r]-{-p})
        nodes.append(frozenset(x)); steps.append((l,r,p))
        return len(nodes)-1
    k=2*q
    r1=add(k,k+1,q+3)
    r2=add(k+2,k+3,q+4)
    ns=add(r1,r2,q+2)
    assert nodes[ns]==frozenset({-(q+1)})
    edge_ids=[add(i,ns,q+1) for i in range(2*q)]
    def chosen(i,value):
        a=i+1; b=(i+1)%q+1
        nxt=value^sigma[i]
        wanted=frozenset({-a if value else a,b if nxt else -b})
        return next(j for j in edge_ids[2*i:2*i+2] if nodes[j]==wanted)
    units=[]
    for init in (0,1):
        v=init;cur=None
        for i in range(q):
            j=chosen(i,v)
            if cur is None:cur=j
            else:cur=add(cur,j,i+1 if v else -(i+1))
            v^=sigma[i]
        units.append(cur)
    assert nodes[units[0]]==frozenset({1})
    assert nodes[units[1]]==frozenset({-1})
    end=add(units[0],units[1],1)
    assert not nodes[end] and len(steps)==4*q+2
    return len(steps)
def main():
    d={"cases":0,"deleted_clauses_checked":0,"single_field_flips":0,"resolution_proofs":0}
    for q in (3,4,5):
        for bits in itertools.product((0,1),repeat=q):
            n,cs=source(q,bits)
            parity=sum(bits)%2
            assert n==q+4 and len(cs)==2*q+4
            assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in cs)
            lits={x for c in cs for x in c}
            assert all(j in lits and -j in lits for j in range(1,n+1))
            assert count(n,cs)==(0 if parity else 16)
            for j in range(len(cs)):
                expected=(8 if parity else 16) if j<2*q else ((0 if parity else 16)+2**(q+1))
                assert count(n,cs[:j]+cs[j+1:])==expected
                d["deleted_clauses_checked"]+=1
            for i in range(q):
                alt=list(bits);alt[i]^=1
                _,flipped=source(q,alt)
                changes=[(j,h) for j,(a,b) in enumerate(zip(cs,flipped)) for h,(x,y) in enumerate(zip(a,b)) if x!=y]
                assert changes==[(2*i,1),(2*i+1,1)]
                d["single_field_flips"]+=1
            if parity:
                assert resolution(q,bits)==4*q+2
                d["resolution_proofs"]+=1
            d["cases"]+=1
    for q in (16,64,256):
        v=[0]*q;v[0]=1
        assert resolution(q,v)==4*q+2
        d["resolution_proofs"]+=1
    assert d=={"cases":56,"deleted_clauses_checked":720,"single_field_flips":248,"resolution_proofs":31}
    print(json.dumps({"label":"COMPUTATIONAL","failures":0,"counts":d},sort_keys=True))
if __name__=="__main__":main()
