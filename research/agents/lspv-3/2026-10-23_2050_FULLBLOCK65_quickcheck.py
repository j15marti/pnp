#!/usr/bin/env python3
"""FULLBLOCK65, concise reproducibility check. Python standard library only.
Companion full DPLL audit and fixed-record raw JSON are in the local research bundle.
"""
import itertools, json, math

def source(q, b):
    n = 0
    clauses = []
    pivots = []
    def fresh():
        nonlocal n
        n += 1
        return n
    def add(*ls):
        assert len(ls) == 3 and len({abs(x) for x in ls}) == 3
        clauses.append(ls)
    def force(l):
        a, v = fresh(), fresh()
        for s, t in itertools.product((1,-1),repeat=2):
            add(l,s*a,t*v)
    def two(a,v):
        p = fresh()
        add(a,v,p)
        add(a,v,-p)
    def AND(a,v):
        o=fresh()
        two(-o,a)
        two(-o,v)
        add(o,-a,-v)
        return o
    def OR(a,v):
        o=fresh()
        two(o,-a)
        two(o,-v)
        add(-o,a,v)
        return o
    z=fresh()
    force(-z)
    c1=c2=c3=z
    for bit in b:
        x,u,v=fresh(),fresh(),fresh()
        force(-u)
        force(-v)
        pivots.append(len(clauses))
        add(x if bit else -x,u,v)
        h2,h3=AND(c1,x),AND(c2,x)
        c1,c2,c3=OR(c1,x),OR(c2,h2),OR(c3,h3)
    force(c2)
    force(-c3)
    return n,clauses,pivots

def bits(n,clauses):
    m=len(clauses)
    w=math.ceil(math.log2(64*(n+m+1)))
    words=[n,m]
    for row in clauses:
        words.append(3)
        words.extend(abs(t)+(1<<(w-1) if t<0 else 0) for t in row)
    return ''.join(format(x,'0%db'%w) for x in words),w

def check():
    results=[]
    for q in range(2,9):
        n0,c0,pv0=source(q,(0,)*q)
        s0,w=bits(n0,c0)
        pivot_bits={i:(2+4*pv0[i]+1)*w for i in range(q)}
        sat=unsat=0
        for b in itertools.product((0,1),repeat=q):
            n,c,p=source(q,b)
            assert (n,len(c),p)==(n0,len(c0),pv0)
            s,w2=bits(n,c)
            assert len(s)==len(s0) and w==w2
            changed={i for i,(a,t) in enumerate(zip(s0,s)) if a!=t}
            assert changed=={pivot_bits[i] for i,x in enumerate(b) if x}
            (sat if sum(b)==2 else unsat)  # classification below
            if sum(b)==2:
                sat+=1
            else:
                unsat+=1
        assert sat==q*(q-1)//2
        assert sat+unsat==(1<<q)
        # Difference hypergraph on 0^q is all pairs of selector positions.
        opposite=[{i,j} for i in range(q) for j in range(i+1,q)]
        best=min(
            len(Q) for k in range(q+1)
            for T in itertools.combinations(range(q),k)
            for Q in [set(T)]
            if all(Q.intersection(E) for E in opposite)
        ) if q<=7 else q-1
        assert best==q-1
        results.append(dict(q=q,n=n0,m=len(c0),N=len(s0),
                            sat=sat,unsat=unsat,single_flip=0,
                            full_difference=best))
    return results

if __name__=="__main__":
    print(json.dumps(check(),indent=2,sort_keys=True))
