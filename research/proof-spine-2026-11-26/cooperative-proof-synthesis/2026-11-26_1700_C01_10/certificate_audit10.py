"""Independent exhaustive audit of the two-sided / least-core theorem.
No dependencies. All systems are abstract GF(2) evaluation controls.
"""
import itertools as it
import random
import json

def span(vectors):
    s={0}
    for v in vectors: s |= {x^v for x in s}
    return s

def rank(S): return len(S).bit_length()-1

def subsets(I):
    I=list(I)
    for mask in range(1<<len(I)):
        yield {i for j,i in enumerate(I) if mask>>j&1}

def value(x,v): return (x&v).bit_count()&1

def core(P,H,I,W):
    base=span(list(W)+[v for i in H for v in P[i]])
    best=None; keep=None
    for J in subsets(I-H):
        s=span(list(base)+[v for i in J for v in P[i]])
        d=rank(s)-rank(base)-len(J)
        if best is None or d<best: best=d;keep=J.copy()
        elif d==best: keep &= J
    return keep|H

def run():
    rng=random.Random(2611261002)
    stats=dict(systems=0,cuts=0,extensions=0,global_dominance=0,strict_joint=0)
    for trial in range(300):
        n=rng.randrange(2,6); m=rng.randrange(1,8)
        P=[];Q=[];H=set();I=set(range(m))
        for i in range(m):
            a,b=rng.sample(range(1,1<<n),2);P.append((a,b))
            words=list(it.product((0,1),repeat=2));bad=rng.choice(words)
            if rng.randrange(4)==0:
                Q.append({rng.choice(words)});H.add(i)
            else: Q.append(set(words)-{bad})
        def U(J):return span(v for i in J for v in P[i])
        def models(J):return [x for x in range(1<<n) if all(tuple(value(x,v) for v in P[i]) in Q[i] for i in J)]
        def projection(M,S):return {tuple(value(x,v) for v in sorted(S)) for x in M}
        C=core(P,H,I,{0});actual=models(I)
        assert projection(actual,U(C))==projection(models(C),U(C))
        for j in range(m+1):
            L=set(range(j));R=I-L;W=U(L)&U(R)
            A=core(P,H&L,L,W);B=core(P,H&R,R,W)
            E=U(A)&W;F=U(B)&W;Z=E&F
            assert C<=A|B;stats['global_dominance']+=1
            assert Z==U(A)&U(B)
            assert bool(projection(models(L),Z)&projection(models(R),Z))==bool(actual)
            assert projection(actual,U(A|B))==projection(models(A|B),U(A|B))
            stats['extensions']+=len(models(A|B));stats['cuts']+=1
            stats['strict_joint']+=rank(Z)<min(rank(E),rank(F))
            l=L&C;r=R&C;w=U(l)&U(r)
            assert core(P,H&l,l,w)==l and core(P,H&r,r,w)==r
        stats['systems']+=1
    print(json.dumps(stats,sort_keys=True))
if __name__=='__main__':run()
