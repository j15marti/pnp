from itertools import product, combinations
from functools import lru_cache
from collections import Counter, defaultdict
import random

SEED=20261127

def gate(p,u,v):
    return [(-p,u),(-p,v),(p,-u,-v)]

def compile_cnf(F,n):
    G=[]; keys=[]; groups=[]
    for i,C in enumerate(F):
        l1,l2,l3=(tuple(C)+(C[-1],)*3)[:3]
        a,b,c=-l1,-l2,l3
        u,v,s,t=range(n+4*i+1,n+4*i+5)
        start=len(G)
        G+=gate(a,u,s)+gate(b,v,t)+gate(c,u,v)
        keys.extend([start,start+3,start+8])
        groups.append((a,b,c,u,v,s,t))
    return G,n+4*len(F),keys,groups

def lit(x,A): return bool(A[abs(x)])==(x>0)
def sat(F,A): return all(any(lit(x,A) for x in C) for C in F)

def extension(A,groups):
    B=dict(A)
    for a,b,c,u,v,s,t in groups:
        A1,B1,C1=(int(lit(x,A)) for x in (a,b,c))
        B.update({u:A1|C1,v:B1|C1,s:A1,t:B1})
    return B

def cnf_masks(F):
    return tuple(sorted(set((sum(1<<(x-1) for x in set(C) if x>0),sum(1<<(-x-1) for x in set(C) if x<0)) for C in F if not any(-x in C for x in C))))

def restrict_masks(F,bit,val):
    if val: return tuple(sorted(set((p,q&~bit) for p,q in F if not p&bit)))
    return tuple(sorted(set((p&~bit,q) for p,q in F if not q&bit)))

@lru_cache(None)
def opt(F):
    if (0,0) in F:return 1,0
    if not F:raise ValueError('SAT')
    allbits=0
    for p,q in F:allbits|=p|q
    L=10**30;D=10**9
    while allbits:
        b=allbits&-allbits;allbits^=b
        x=opt(restrict_masks(F,b,0));y=opt(restrict_masks(F,b,1))
        L=min(L,x[0]+y[0]);D=min(D,1+max(x[1],y[1]))
    return L,D

def optimum(F,n,unfix=None):
    R=cnf_masks(F)
    if unfix is not None:
        for i in range(unfix,n):R=restrict_masks(R,1<<i,0)
    result=opt(R);return result

def bits(F,n):return n+2*len(F)+2+(n.bit_length()+2)*sum(map(len,F))

def witness_checks(F,n,G,keys,groups):
    # Exact exhaustive enumeration of source assignments; construct and check all deletion witnesses.
    witnesses={};yes=0
    for vals in product((0,1),repeat=n):
        A=dict(zip(range(1,n+1),vals));bad=[i for i,C in enumerate(F) if not sat([C],A)]
        B=extension(A,groups)
        assert sat(G,B)==(not bad)
        if not bad:yes+=1
        if len(bad)==1:
            i=bad[0];a,b,c,u,v,s,t=groups[i]
            for k,delta in zip(keys[3*i:3*i+3],({u:0,s:1,v:1,t:1},{u:1,s:1,v:0,t:1},{u:1,s:1,v:1,t:1})):
                H=B|delta
                assert [j for j,C in enumerate(G) if not sat([C],H)]==[k]
                witnesses[k]=H
    return yes,len(witnesses)

def recover(F):
    # History-free exact existential projection on private components.
    counts=Counter(abs(x) for C in F for x in C)
    phase={j for j,d in counts.items() if d%3==0}
    private=set(counts)-phase;adj={j:set() for j in private}
    for C in F:
        P={abs(x) for x in C}&private
        for j in P:adj[j]|=P-{j}
    comps=[];rem=set(private)
    while rem:
        Q=[rem.pop()];S=set(Q)
        for x in Q:
            for y in adj[x]&rem:rem.remove(y);S.add(y);Q.append(y)
        comps.append(S)
    out=[]
    for S in comps:
        C=[c for c in F if any(abs(x) in S for x in c)]
        B=sorted({abs(x) for c in C for x in c}-S)
        if len(S)>4 or len(B)>3:return None
        V=sorted(S)
        for a in product((0,1),repeat=len(B)):
            A=dict(zip(B,a))
            if not any(sat(C,A|dict(zip(V,z))) for z in product((0,1),repeat=len(V))):
                out.append(tuple(-x if y else x for x,y in zip(B,a)))
    out.extend(c for c in F if all(abs(x) in phase for x in c))
    return out,phase

def sat_over(F,V):
    return any(sat(F,dict(zip(V,a))) for a in product((0,1),repeat=len(V)))

def general_projection(A):
    # AND-output image is the Horn fixed-point family of coverage closure.
    covers=defaultdict(list)
    for i,S in enumerate(A):
        for x in S:covers[x].append(i)
    H=set()
    for i,S in enumerate(A):
        for J in product(*(covers[x] for x in sorted(S))):
            if i not in J:H.add((frozenset(J),i))
    return H

def main():
    rng=random.Random(SEED)
    F0=[(1,),(-1,)];F1=[(1,2),(-1,2),(-2,)];F2=[(1,2),(-1,2),(1,-2),(-1,-2)]
    for F,n in [(F0,1),(F1,2),(F2,2)]:
        G,v,K,Q=compile_cnf(F,n);core=[G[i] for i in K]
        yes,w=witness_checks(F,n,G,K,Q);assert yes==0 and w==3*len(F)
        base=optimum(F,n);co=optimum(core,v)
        assert co[0]==3*len(F) and base[0]==len(F)
        # Direct full DP on first two; third uses proved leaf bounds, not exhaustive DP.
        full=optimum(G,v) if len(F)<4 else None
        if full:assert full[0]==3*len(F)
        print('base',n,len(F),'full n,m,N',v,len(G),bits(G,v),'core n,m,N',n+2*len(F),len(core), (n+2*len(F))+2*len(core)+2+((n+2*len(F)).bit_length()+2)*sum(map(len,core)), 'base L,D',base,'core L,D',co,'full L,D',full,'indispensable',w,flush=True)
        opt.cache_clear()
    G,v,K,Q=compile_cnf(F0,1)
    print('reverse full unit',[(j,optimum(G,v,j)) for j in range(v+1)],flush=True);opt.cache_clear()
    # Verify general coverage lemma independently, enumerate both sides for random hypergraphs.
    tests=0;clauses=0
    for _ in range(120):
        A=[set(rng.sample(range(5),rng.randint(1,3))) for j in range(6)]
        H=general_projection(A);clauses+=len(H)
        actual={tuple(int(all(z[x] for x in S)) for S in A) for z in product((0,1),repeat=5)}
        predicted={p for p in product((0,1),repeat=6) if all(not all(p[j] for j in J) or p[i] for J,i in H)}
        assert actual==predicted;tests+=64
    print('coverage hypergraphs',120,'output words',tests,'Horn clauses',clauses,flush=True)
    # Renamed/complemented direct CNF. Both labels, exact projected truth table checked.
    labels=Counter();comparisons=0
    for _ in range(120):
        F=list(F2)
        if rng.randrange(2):del F[rng.randrange(len(F))]
        G,v,K,Q=compile_cnf(F,2);P=list(range(1,v+1));rng.shuffle(P);sgn=[rng.choice((-1,1)) for j in P]
        def rename(x):return (1 if x>0 else -1)*sgn[abs(x)-1]*P[abs(x)-1]
        G=[tuple(map(rename,C)) for C in G];rng.shuffle(G)
        R,V=recover(G);assert V==set(P[:2]);Fnew=[tuple(map(rename,C)) for C in F]
        for z in product((0,1),repeat=2):
            A=dict(zip(sorted(V),z));assert sat(R,A)==sat(Fnew,A);comparisons+=1
        labels[sat_over(R,sorted(V))]+=1
    print('history-free cases NO YES',labels[False],labels[True],'phase words',comparisons,flush=True)
    # Prior run's K4 base and overlapping selector result (direct independent optimizer).
    edges=list(combinations(range(4),2));F=[]
    for i in range(4):
        E=[j+1 for j,e in enumerate(edges) if i in e]
        for a in product((0,1),repeat=3):
            if sum(a)%2!=int(i==0):F.append(tuple(-x if y else x for x,y in zip(E,a)))
    assert optimum(F,6)==(28,5)
    G=[C+tuple(-x if y else x for x,y in zip((7,8),a)) for C in F for a in product((0,1),repeat=2)]
    assert optimum(G,8)==(112,7)
    print('prior K4 base/lift',optimum(F,6),optimum(G,8),flush=True)

if __name__=='__main__':main()

def gf2(rows):
    piv={}
    for m,b in rows:
        while m:
            j=m.bit_length()-1
            if j not in piv:piv[j]=(m,b);break
            u,c=piv[j];m^=u;b^=c
        if not m and b:return False
    return True

def parity_decide(F):
    R=defaultdict(set)
    for C in F:
        if len(C)!=3:return None
        V=tuple(sorted(map(abs,C)));R[V].add(tuple(int(-j in C) for j in V))
    rows=[];defects=[]
    for V,S in R.items():
        A=set(product((0,1),repeat=3))-S
        if len(A)==4 and len({sum(z)%2 for z in A})==1:
            rows.append((sum(1<<(j-1) for j in V),sum(next(iter(A)))%2))
        else:defects.append((V,A))
    if len(defects)>1:return None
    if not defects:return gf2(rows)
    V,A=defects[0]
    return any(gf2(rows+[(1<<(j-1),a) for j,a in zip(V,z)]) for z in A)

def larger_controls():
    rng=random.Random(SEED+1);labels=Counter()
    for h in (3,4,8,16,32):
        E=[(r*h+i,r*h+(i+1)%h) for r in range(2) for i in range(h)]+[(i,h+i) for i in range(h)]
        n=len(E)
        for mode in ('odd','even','delete'):
            F=[]
            for i in range(2*h):
                V=[j+1 for j,e in enumerate(E) if i in e]
                for z in product((0,1),repeat=3):
                    if sum(z)%2!=int(i==0 and mode!='even'):F.append(tuple(-j if a else j for j,a in zip(V,z)))
            if mode=='delete':del F[rng.randrange(len(F))]
            G,v,K,Q=compile_cnf(F,n);P=list(range(1,v+1));rng.shuffle(P);sgn=[rng.choice((-1,1)) for _ in P]
            def rename(x):return (1 if x>0 else -1)*sgn[abs(x)-1]*P[abs(x)-1]
            G=[tuple(map(rename,C)) for C in G];rng.shuffle(G)
            R,V=recover(G);assert V==set(P[:n]);assert parity_decide(R)==(mode!='odd')
            labels[mode]+=1
            if mode=='odd':print('compiled prism',h,'n,m,N',v,len(G),bits(G,v),flush=True)
    print('larger parity projection controls',dict(labels),flush=True)

if __name__=='__main__':larger_controls()
