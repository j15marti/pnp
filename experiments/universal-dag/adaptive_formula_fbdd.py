from functools import lru_cache
from itertools import combinations, product
from collections import defaultdict
import random

def clause_cover(n, vars_, signs):
    m = 0
    for a in range(1 << n):
        if all(((a >> v) & 1) != s for v, s in zip(vars_, signs)):
            m |= 1 << a
    return m

def family_2sat3():
    C=[]
    for i,j in combinations(range(3),2):
        for si,sj in product((0,1), repeat=2):
            C.append(clause_cover(3,(i,j),(si,sj)))
    return C,3

def family_horn3():
    C=[]
    for i in range(3):
        C.append(clause_cover(3,(i,),(1,)))
    for i in range(3):
        for j in range(3):
            if i!=j:
                C.append(clause_cover(3,(i,j),(0,1)))
    for i in range(3):
        C.append(clause_cover(3,(i,),(0,)))
    return C,3

def family_xor3():
    C=[]
    for row in range(1,8):
        for rhs in (0,1):
            m=0
            for x in range(8):
                if (((row & x).bit_count() & 1) != rhs):
                    m |= 1 << x
            C.append(m)
    return C,3

def family_chain4():
    C=[]
    for T in ((0,1,2),(1,2,3)):
        for s in product((0,1), repeat=3):
            C.append(clause_cover(4,T,s))
    return C,4

def family_3sat4():
    C=[]
    for omit in range(4):
        T=tuple(v for v in range(4) if v != omit)
        for s in product((0,1), repeat=3):
            C.append(clause_cover(4,T,s))
    return C,4

def canonical_signature(U,R,covers,n):
    if U == 0:
        return ("UNSAT",)
    clauses=[]
    for a in range(1 << n):
        if (U >> a) & 1:
            m=0
            x=R
            while x:
                l=x & -x
                i=l.bit_length()-1
                x-=l
                if (covers[i] >> a) & 1:
                    m |= l
            if m == 0:
                return ("SAT",)
            clauses.append(m)
    clauses=sorted(set(clauses), key=lambda z:(z.bit_count(),z))
    out=[]
    for m in clauses:
        if not any((q & m) == q for q in out):
            out.append(m)
    return tuple(out)

def restrict_state(U,R,i,val,covers):
    R &= ~(1 << i)
    if val:
        U &= ~covers[i]
    return U,R

def exact_adaptive_depth(covers,n):
    M=len(covers)
    FULL=(1 << (1 << n))-1
    root=canonical_signature(FULL,(1<<M)-1,covers,n)
    rep={root:(FULL,(1<<M)-1)}
    memo={}
    terminal={("SAT",),("UNSAT",)}
    def rec(sig):
        if sig in terminal: return 0
        if sig in memo: return memo[sig]
        U,R=rep[sig]
        union=0
        for m in sig: union |= m
        vars_=[i for i in range(M) if (union >> i) & 1]
        best=10**9
        for i in vars_:
            ds=[]
            for val in (0,1):
                U2,R2=restrict_state(U,R,i,val,covers)
                s2=canonical_signature(U2,R2,covers,n)
                if s2 not in terminal and s2 not in rep:
                    rep[s2]=(U2,R2)
                ds.append(0 if s2 in terminal else rec(s2))
            best=min(best,1+max(ds))
        memo[sig]=best
        return best
    return rec(root)

def adaptive_from_base(covers,n,base_order,window=2):
    M=len(covers)
    FULL=(1 << (1 << n))-1
    pos={v:i for i,v in enumerate(base_order)}
    terminal={("SAT",),("UNSAT",)}
    root=canonical_signature(FULL,(1<<M)-1,covers,n)
    rep={root:(FULL,(1<<M)-1)}
    choice={}
    children={}
    stack=[root]
    def vars_in(sig):
        u=0
        for m in sig: u |= m
        return [i for i in range(M) if (u >> i) & 1]
    while stack:
        sig=stack.pop()
        if sig in terminal or sig in choice: continue
        U,R=rep[sig]
        vars_=sorted(vars_in(sig), key=lambda i:pos[i])
        cand=vars_[:min(window,len(vars_))]
        scored=[]
        for i in cand:
            ch=[]
            lens=[]
            for val in (0,1):
                U2,R2=restrict_state(U,R,i,val,covers)
                s2=canonical_signature(U2,R2,covers,n)
                ch.append((s2,(U2,R2)))
                lens.append(0 if s2 in terminal else len(s2))
            scored.append(((max(lens),sum(lens),pos[i]),i,ch))
        _,i,ch=min(scored)
        choice[sig]=i
        children[sig]=(ch[0][0],ch[1][0])
        for s2,ur in ch:
            if s2 not in terminal and s2 not in rep:
                rep[s2]=ur
                stack.append(s2)
    @lru_cache(None)
    def depth(sig):
        if sig in terminal: return 0
        return 1+max(depth(children[sig][0]),depth(children[sig][1]))
    return root,choice,children,depth(root)

def chain_lookahead_fbdd(covers,n):
    M=len(covers)
    FULL=(1 << (1 << n))-1
    terminal=("SAT","UNSAT")
    @lru_cache(None)
    def norm(U,R):
        if U==0: return ("UNSAT",0,0)
        rr=0
        union=0
        x=R
        while x:
            l=x & -x
            i=l.bit_length()-1
            x-=l
            ci=covers[i] & U
            if ci:
                rr |= l
                union |= ci
        if U & ~union: return ("SAT",0,0)
        return ("NODE",U,rr)
    choice={}
    def rough(U,R):
        s=norm(U,R)
        return 0 if s[0]!="NODE" else s[1].bit_count()*s[2].bit_count()
    root=norm(FULL,(1<<M)-1)
    stack=[root]
    while stack:
        st=stack.pop()
        if st[0]!="NODE": continue
        U,R=st[1],st[2]
        if (U,R) in choice: continue
        vars_=[i for i in range(M) if (R>>i)&1]
        def key(i):
            R2=R & ~(1<<i)
            return (max(rough(U,R2),rough(U & ~covers[i],R2)),
                    rough(U,R2)+rough(U & ~covers[i],R2),i)
        i=min(vars_,key=key)
        choice[(U,R)]=i
        R2=R & ~(1<<i)
        stack.append(norm(U,R2))
        stack.append(norm(U & ~covers[i],R2))
    return root,choice,norm

def eval_chain(root,choice,norm,covers,mask):
    st=root
    while st[0]=="NODE":
        U,R=st[1],st[2]
        i=choice[(U,R)]
        R2=R & ~(1<<i)
        U2=U & ~covers[i] if ((mask>>i)&1) else U
        st=norm(U2,R2)
    return st[0]=="SAT"

def direct_sat(covers,n,mask):
    U=(1 << (1 << n))-1
    for i,c in enumerate(covers):
        if (mask>>i)&1:
            U &= ~c
    return U != 0

def main():
    fams={
        "2SAT3":family_2sat3(),
        "HORN3_GRAPH":family_horn3(),
        "XOR3_ALL_EQ":family_xor3(),
        "CHAIN4_TWO_TRIPLES":family_chain4(),
    }
    base_orders={
        "2SAT3":[11,10,7,6,3,2,9,8,5,4,1,0],
        "HORN3_GRAPH":[11,10,9,8,5,4,7,6,3,2,1,0],
        "XOR3_ALL_EQ":[13,12,10,8,7,4,3,1,11,9,6,5,2,0],
    }
    print("exact adaptive depths")
    for name,(C,n) in fams.items():
        print(name, exact_adaptive_depth(C,n))

    C,n=fams["CHAIN4_TWO_TRIPLES"]
    root,ch,norm=chain_lookahead_fbdd(C,n)
    print("CHAIN4 nodes",len(ch))
    bad=0
    for x in range(1<<16):
        if eval_chain(root,ch,norm,C,x) != direct_sat(C,n,x):
            bad+=1
            break
    print("CHAIN4 exhaustive mismatches",bad)

    C,n=family_3sat4()
    sign_major=[0,8,16,24,1,9,17,25,2,10,18,26,3,11,19,27,
                4,12,20,28,5,13,21,29,6,14,22,30,7,15,23,31]
    root,ch,children,dep=adaptive_from_base(C,n,sign_major,window=2)
    print("3SAT4 adaptive nodes",len(ch),"constructed depth",dep)
    rng=random.Random(20261003)
    bad=0
    for _ in range(1_000_000):
        x=rng.getrandbits(32)
        s=root
        while s not in (("SAT",),("UNSAT",)):
            i=ch[s]
            s=children[s][(x>>i)&1]
        if (s==("SAT",)) != direct_sat(C,n,x):
            bad+=1
            break
    print("3SAT4 seeded random mismatches",bad)
    print("Rivest-Vuillemin separately proves exact deterministic query depth 32:")
    print("32 clause variables = 2^5, transitive Q4-edge action, nonconstant invariant predicate.")

if __name__=="__main__":
    main()
