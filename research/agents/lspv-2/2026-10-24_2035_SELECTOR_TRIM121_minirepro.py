#!/usr/bin/env python3
"""SELECTOR-TRIM121: exact nonempty-selector model, standard-library reproducer.
Usage: python SELECTOR_TRIM121_minirepro.py [DOECKER61_original_source.txt]
For the complete 556-case hybrid audit, see the packaged extended audit.
"""
import ast, collections, itertools, json, math, pathlib, random, sys
SEED=202610240435
R=random.Random(SEED)

def encode(F):
    occ=collections.defaultdict(lambda:[[],[]]); O=[]
    for j,c in enumerate(F):
        assert len(c)==3 and len(set(map(abs,c)))==3
        tri=tuple(3*j+k+1 for k in range(3));O.append(tri)
        for k,l in enumerate(c):occ[abs(l)][int(l<0)].append(tri[k])
    E=[(-p,-q) for x in sorted(occ) for p in occ[x][0] for q in occ[x][1]]
    out=list(O)
    for i,(a,b) in enumerate(E,1):
        z=3*len(F)+i
        out.extend(((a,b,z),(a,b,-z)))
    return O,E,out

def solve(cs):
    nodes=0
    def visit(A):
        nonlocal nodes
        nodes+=1
        A=dict(A)
        while 1:
            unit=None; score=collections.Counter()
            for c in cs:
                remaining=[];sat=False
                for l in c:
                    v=A.get(abs(l))
                    if v is None:remaining.append(l);score[abs(l)]+=1
                    elif v==(l>0):sat=True;break
                if sat:continue
                if not remaining:return None
                if len(remaining)==1:unit=remaining[0];break
            if unit is None:
                if not score:return A
                x=score.most_common(1)[0][0]
                for b in (True,False):
                    Z=dict(A);Z[x]=b
                    r=visit(Z)
                    if r is not None:return r
                return None
            A[abs(unit)]=unit>0
    return visit({}),nodes

def brute(F,n):
    return next((a for a in itertools.product((False,True),repeat=n)
        if all(any(a[abs(l)-1]==(l>0) for l in c) for c in F)),None)

def reconstructed(F,Y):
    A={}
    for j,c in enumerate(F):
        assert any(Y.get(3*j+k+1,False) for k in range(3))
        for k,l in enumerate(c):
            if Y.get(3*j+k+1,False):
                if abs(l) in A:assert A[abs(l)]==(l>0)
                A[abs(l)]=l>0
    return all(any(A.get(abs(l),False)==(l>0) for l in c) for c in F)

def main():
    count=collections.Counter()
    allc=[tuple((j+1)*v for j,v in enumerate(s))
        for s in itertools.product((-1,1),repeat=3)]
    tests=[[allc[j] for j in range(8) if mask>>j&1] for mask in range(256)]
    for n in (4,5,6):
        for _ in range(60):
            length=R.randint(n+4,4*n+7);f=[];seen=set()
            while len(f)<length:
                v=R.sample(range(1,n+1),3)
                c=tuple(sorted((i if R.getrandbits(1) else -i for i in v),key=abs))
                if c not in seen:seen.add(c);f.append(c)
            tests.append(f)
    for F in tests:
        n=max((abs(l) for c in F for l in c),default=0)
        O,E,G=encode(F)
        v,num=solve(O+E)
        a=brute(F,n)
        assert (v is None)==(a is None)
        if v is not None:assert reconstructed(F,v)
        assert len(G)==len(F)+2*len(E)
        assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in G)
        for av,bv,z in itertools.product((False,True),repeat=3):
            assert (av or bv)==((av or bv or z) and (av or bv or not z))
        count['SAT' if v is not None else 'UNSAT']+=1
        count['DPLL_nodes']+=num
    if len(sys.argv)>1:
        t=pathlib.Path(sys.argv[1]).read_text()
        F=ast.literal_eval(t[t.index('[['):])
        n=max(abs(l) for c in F for l in c);m=len(F)
        q=collections.Counter((abs(l),l>0) for c in F for l in c)
        assert n==198 and m==264
        assert all(q[x,sg]==2 for x in range(1,n+1) for sg in (True,False))
        O,E,G=encode(F)
        assert len(E)==4*n==3*m and len(G)==7*m
        assert len({abs(l) for c in G for l in c})==6*m
        w=lambda nv,mv:math.ceil(math.log2(64*(nv+mv+1)))
        new=(4*len(G)+2)*w(6*m,7*m)
        old=(4*16*m+2)*w(9*m,16*m)
        assert (new,old)==(133092,321062)
        print(json.dumps({'strict_benchmark':{'n':n,'m':m,
            'conflicts':len(E),'new_proper_clauses':len(G),
            'output_bits':new,'prior_bits':old}}))
    print(json.dumps({'run':'SELECTOR-TRIM121','seed':SEED,'counts':dict(count),
        'checks_failed':0,'ARC_edge':'OPEN'},sort_keys=True))
if __name__=='__main__':main()
