"""Reproducible nonlinear shared-wire Tseitin experiments. Python stdlib only."""
from itertools import product, combinations
from functools import lru_cache
from collections import defaultdict
import random

# Clause literals signed 1-based integers. A cell fixes physical bits to falsify clause.
def lift(F):
    G=[]
    for C in F:
        cells=[]
        for lit in C:
            a,b=2*abs(lit)-1,2*abs(lit)
            cells.append([(a,),(-a,b)] if lit>0 else [(-a,-b)])
        G.extend(tuple(x for block in blocks for x in block) for blocks in product(*cells))
    return G

def tseitin(edges, charges):
    F=[]
    for v,b in enumerate(charges):
        es=[i+1 for i,e in enumerate(edges) if v in e]
        for z in product((0,1),repeat=len(es)):
            if sum(z)%2 != b: F.append(tuple(-i if bit else i for i,bit in zip(es,z)))
    return F

def prism(h):
    return sorted({tuple(sorted(e)) for e in [(r*h+i,r*h+(i+1)%h) for r in (0,1) for i in range(h)]+[(i,h+i) for i in range(h)]})

def ok(F, x):
    return all(any(bool(x[abs(l)-1])==(l>0) for l in C) for C in F)

def encoded_size(F,n):
    # unary n,m, width, then (w-bit ID,sign) per literal
    return n+2*len(F)+2+(n.bit_length()+2)*sum(map(len,F))

def restrict(F,i,b):
    yes=i if b else -i
    return tuple(sorted(set(tuple(l for l in C if l!=-yes) for C in F if yes not in C)))

@lru_cache(None)
def opt(F):
    if () in F: return (1,0)
    if not F: return (float('inf'),float('inf'))
    bestL=bestD=float('inf')
    for i in sorted({abs(l) for C in F for l in C}):
        a,b=opt(restrict(F,i,0)),opt(restrict(F,i,1))
        bestL=min(bestL,a[0]+b[0]); bestD=min(bestD,1+max(a[1],b[1]))
    return bestL,bestD

def canon(F):return tuple(sorted(set(tuple(sorted(C)) for C in F)))

@lru_cache(None)
def and_weighted(F):
    # Exact lift leaf count by the random-one-free restriction theorem.
    if () in F:return 1
    if not F:return float('inf')
    return min(2*and_weighted(restrict(F,i,0))+and_weighted(restrict(F,i,1))
               for i in {abs(l) for C in F for l in C})

def brute(F,n):
    return next((x for x in product((0,1),repeat=n) if ok(F,x)),None)

def gf2(rows,n):
    # Return witness or independently checked linear inconsistency certificate.
    basis={}
    for j,(a,b) in enumerate(rows):
        p=1<<j
        while a:
            k=a.bit_length()-1
            if k not in basis:
                basis[k]=(a,b,p); break
            aa,bb,pp=basis[k]; a^=aa;b^=bb;p^=pp
        if not a and b:
            aa=bb=0
            for i,(r,s) in enumerate(rows):
                if p>>i&1: aa^=r;bb^=s
            assert aa==0 and bb==1
            return None
    x=0
    for k,(a,b,p) in sorted(basis.items()):
        if (a&x).bit_count()%2 != b:x|=1<<k
    assert all((a&x).bit_count()%2==b for a,b in rows)
    return x

def recover(F,n):
    """Exact partial decider. None=unsupported; False=UNSAT; tuple=SAT witness."""
    adj=[{i} for i in range(1,n+1)]
    for C in F:
        vs=set(map(abs,C))
        if not vs:return False
        for i in vs:adj[i-1].update(vs)
    twins=defaultdict(list)
    for i,a in enumerate(adj,1):twins[frozenset(a)].append(i)
    pairs=list(twins.values())
    if any(len(p)!=2 for p in pairs):return None
    owner={i:j for j,p in enumerate(pairs) for i in p}
    groups=defaultdict(list)
    for C in F:
        key=tuple(sorted({owner[abs(l)] for l in C}))
        if len(key)!=3:return None
        groups[key].append(C)
    if any(sum(j in key for key in groups)!=2 for j in range(len(pairs))):return None
    keys=list(groups)
    # Local table 1 means forbidden; 4-state variable per recovered pair.
    words=list(product(range(4),repeat=3))
    tables=[]; facts=[]
    for key in keys:
        T={}
        for z in words:
            x={i:(t>>k)&1 for j,t in zip(key,z) for k,i in enumerate(pairs[j])}
            T[z]=int(not all(any(bool(x[abs(l)])==(l>0) for l in C) for C in groups[key]))
        tables.append(T); base=T[0,0,0]; fs=[]
        for k in range(3):
            fs.append(tuple(T[tuple(t if j==k else 0 for j in range(3))]^base for t in range(4)))
        facts.append((base,fs) if all(len(set(f))==2 for f in fs) and all(T[z]==(base^fs[0][z[0]]^fs[1][z[1]]^fs[2][z[2]]) for z in words) else None)
    # Try no exception and every possible one-table exception. All accepted decompositions are exact.
    for exc in [-1]+list(range(len(keys))):
        functions={};rows=[];good=True
        for k,key in enumerate(keys):
            if k==exc:continue
            if facts[k] is None:good=False;break
            b,fs=facts[k]
            for j,f in zip(key,fs):
                if j in functions and functions[j]!=f:good=False;break
                functions[j]=f
            if not good:break
            rows.append((sum(1<<j for j in key),b))
        if not good or len(functions)!=len(pairs):continue
        choices=[()] if exc<0 else [z for z in words if not tables[exc][z]]
        for z in choices:
            pins={} if exc<0 else dict(zip(keys[exc],z))
            rr=rows+[(1<<j,functions[j][t]) for j,t in pins.items()]
            y=gf2(rr,len(pairs))
            if y is None:continue
            x=[0]*n
            for j,p in enumerate(pairs):
                t=pins[j] if j in pins else functions[j].index((y>>j)&1)
                for k,i in enumerate(p):x[i-1]=(t>>k)&1
            assert ok(F,x)
            return tuple(x)
        return False
    return None

def transform(F,n,rng):
    p=list(range(1,n+1));rng.shuffle(p);p=[i*rng.choice([-1,1]) for i in p]
    out=[tuple(p[abs(l)-1]*(1 if l>0 else -1) for l in C) for C in F]
    rng.shuffle(out);return out

def no_complement(F):
    S={frozenset(C) for C in F}
    return all((C-{l})|{-l} not in S for C in S for l in C)

def main():
    rng=random.Random(20261127)
    K4=list(combinations(range(4),2));tri=[(0,1),(1,2),(0,2)]
    tests=[('unit',[(1,),(-1,)],1),('split',[(1,2),(1,-2),(-1,)],2),('triangle',tseitin(tri,[1,0,0]),3),('K4',tseitin(K4,[1,0,0,0]),6)]
    for name,F,n in tests:
        G=lift(F); L,D=opt(canon(F)); Lg,Dg=opt(canon(G))
        assert (Lg,Dg)==(and_weighted(canon(F)),2*D)
        assert brute(G,2*n) is None
        assert all(brute(G[:i]+G[i+1:],2*n) is not None for i in range(len(G)))
        print('DP',name,'base',n,len(F),L,D,'lift',2*n,len(G),sum(map(len,G)),encoded_size(G,2*n),Lg,Dg,'DAG_lb',len(G)-1,'weighted',and_weighted(canon(F)))
        if name=='triangle':
            reverse=[]
            for k in range(2*n+1):
                H=canon(G)
                for i in range(k+1,2*n+1): H=restrict(H,i,0)
                reverse.append(opt(H))
            print('REVERSE triangle',reverse)
        opt.cache_clear()
    # Prior control: one private selector per clause on unit/split/triangle/K4 (direct DP small, restriction identity for K4 not tested here).
    for name,F,n in tests[:3]:
        H=[C+(s*(n+j+1),) for j,C in enumerate(F) for s in (1,-1)]
        l,d=opt(canon(F)); h,k=opt(canon(H)); assert (h,k)==(2*l,d+1)
        print('PRIOR selector control',name,(l,d),(h,k));opt.cache_clear()
    # Repeated minimally UNSAT clause splitting: direct DP against weighted theorem.
    for trial in range(24):
        F=[(1,),(-1,)]; n=1
        for _ in range(rng.randrange(1,5)):
            i=rng.randrange(len(F));C=F.pop(i);n+=1;F.extend([C+(n,),C+(-n,)])
        # Complement variables to test asymmetrical AND weights.
        F=transform(F,n,rng);G=lift(F)
        L,D=opt(canon(G)); assert (L,D)==(and_weighted(canon(F)),2*opt(canon(F))[1])
        opt.cache_clear();and_weighted.cache_clear()
    print('WEIGHTED independent clause-split controls',24)
    # Every deletion of K4 is checked by hidden solver and brute already above.
    G=lift(tseitin(K4,[1,0,0,0]));assert no_complement(G)
    for i in range(len(G)):
        H=transform(G[:i]+G[i+1:],12,rng); assert isinstance(recover(H,12),tuple)
    print('ALL K4 single-deletion hidden recovery',len(G))
    counts=defaultdict(int)
    for h in (3,4,8,16,32):
        edges=prism(h);v=2*h;n=2*len(edges)
        F=tseitin(edges,[1]+[0]*(v-1));G=lift(F)
        assert len(G)==13*v+1 and sum(map(len,G))==66*v+3 and no_complement(G)
        print('SCALE',v,n,len(G),sum(map(len,G)),encoded_size(G,n))
        for rep in range(4):
            for kind in ('odd','even','delete'):
                if kind=='even':H=lift(tseitin(edges,[0]*v))
                elif kind=='delete':
                    i=rng.randrange(len(G));H=G[:i]+G[i+1:]
                else:H=G
                H=transform(H,n,rng);r=recover(H,n)
                assert r is not None and (r is False)==(kind=='odd')
                counts[kind]+=1
    print('HIDDEN',dict(counts),'total',sum(counts.values()))
    # Check truth-table affine hull on physical six bits via exclusion of nonzero linear forms.
    for b in (0,1):
        S=[x for x in product((0,1),repeat=6) if sum(x[i]*x[i+1] for i in (0,2,4))%2==b]
        assert all(len({sum(x[i] for i in range(6) if mask>>i&1)%2 for x in S})==2 for mask in range(1,64))
        assert all(len({(x[i],x[j]) for x in S})==4 for i,j in combinations(range(6),2))
        print('LOCAL',b,'allowed',len(S),'affine_rank',6,'full_binary_projections',15)
    print('PASS')
if __name__=='__main__':main()
