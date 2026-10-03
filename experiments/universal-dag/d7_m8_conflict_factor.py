from itertools import combinations
from collections import Counter

# D(7,8) exact-cover and factored conflict-circuit verifier.
# Deterministic, exhaustive for the exact-cover count and all 39,060 clause pairs.
# Gate basis: fan-in-2 AND/OR plus unary NOT. The reported SAT circuit uses no final NOT.

def clause_system(n):
    triples=list(combinations(range(n),3))
    clauses=[]
    contains=[[] for _ in range(1<<n)]
    for T in triples:
        for pat in range(8):
            mask=0
            req={v:(pat>>j)&1 for j,v in enumerate(T)}
            for a in range(1<<n):
                if all(((a>>v)&1)==req[v] for v in T):
                    mask |= 1<<a
            ci=len(clauses)
            clauses.append((T,pat,req,mask))
            for a in range(1<<n):
                if (mask>>a)&1:
                    contains[a].append(ci)
    return triples,clauses,contains

def exact_cover_count(n):
    triples,clauses,contains=clause_system(n)
    FULL=(1<<(1<<n))-1
    count=0
    support=Counter()
    multprof=Counter()
    def rec(cov,chosen):
        nonlocal count
        if cov==FULL:
            if len(chosen)==8:
                count+=1
                used=set()
                tc=Counter()
                for ci in chosen:
                    T=clauses[ci][0]
                    used.update(T)
                    tc[T]+=1
                support[len(used)]+=1
                multprof[tuple(sorted(tc.values()))]+=1
            return
        if len(chosen)>=8:
            return
        rem=(~cov)&FULL
        a=(rem & -rem).bit_length()-1
        for ci in contains[a]:
            m=clauses[ci][3]
            if m&cov:
                continue
            chosen.append(ci)
            rec(cov|m,chosen)
            chosen.pop()
    rec(0,[])
    return count,support,multprof

def verify_conflict_factorization():
    n=7
    triples,clauses,_=clause_system(n)
    mismatches=0
    by_intersection=Counter()
    E=0
    for i,j in combinations(range(len(clauses)),2):
        Ti,pi,ri,mi=clauses[i]
        Tj,pj,rj,mj=clauses[j]
        exact=bool(mi & mj)
        I=set(Ti)&set(Tj)
        if len(I)==0:
            factored=True
        elif len(I)==1:
            v=next(iter(I))
            factored=(ri[v]==rj[v])
        elif len(I)==2:
            factored=all(ri[v]==rj[v] for v in I)
        else:
            factored=False
        mismatches += int(exact!=factored)
        if exact:
            E+=1
            by_intersection[len(I)]+=1
    return len(clauses),E,by_intersection,mismatches

# Explicit biclique cover certificates.
K0_CERT=[
("012","456"),("013","2456"),("014","256"),("015","246"),("016","245"),
("023","1456"),("024","156"),("025","146"),("026","145"),("034","1256"),
("035","1246"),("036","1245"),("045","126"),("046","125"),("056","124"),
("123","0456"),("134","0256"),("135","0246"),("136","0245"),
("234","0156"),("235","0146"),("236","0145"),("345","0126"),
("346","0125"),("356","0124")
]
K1_CERT=[
("012","345"),("013","245"),("024","135"),("025","134"),
("034","125"),("035","124"),("0145","23")
]

def verify_biclique_certificates():
    # k0 conflict graph KG(7,3)
    trip7=list(combinations(range(7),3))
    target0={tuple(sorted((i,j))) for i in range(len(trip7))
             for j in range(i+1,len(trip7))
             if set(trip7[i]).isdisjoint(trip7[j])}
    cov0=set(); cost0=0
    for As,Bs in K0_CERT:
        A=set(map(int,As)); B=set(map(int,Bs))
        L=[i for i,T in enumerate(trip7) if set(T)<=A]
        R=[i for i,T in enumerate(trip7) if set(T)<=B]
        cost0 += len(L)+len(R)
        cov0 |= {tuple(sorted((i,j))) for i in L for j in R}

    # k1 local graph KG(6,2)
    edge6=list(combinations(range(6),2))
    target1={tuple(sorted((i,j))) for i in range(len(edge6))
             for j in range(i+1,len(edge6))
             if set(edge6[i]).isdisjoint(edge6[j])}
    cov1=set(); cost1=0
    for As,Bs in K1_CERT:
        A=set(map(int,As)); B=set(map(int,Bs))
        L=[i for i,e in enumerate(edge6) if set(e)<=A]
        R=[i for i,e in enumerate(edge6) if set(e)<=B]
        cost1 += len(L)+len(R)
        cov1 |= {tuple(sorted((i,j))) for i in L for j in R}

    return cov0==target0,cost0-1,cov1==target1,cost1-1

if __name__=="__main__":
    seq=[]
    for n in range(3,8):
        c,s,m=exact_cover_count(n)
        seq.append(c)
        print("exact_cover_count",n,c)
        if n==7:
            print("support_counts",dict(sorted(s.items())))
            print("triple_multiplicity_profiles",dict(sorted(m.items())))
    V,E,byI,mm=verify_conflict_factorization()
    print("clause_vertices",V)
    print("conflict_edges",E)
    print("conflict_edges_by_intersection",dict(sorted(byI.items())))
    print("pair_factorization_mismatches",mm)
    k0ok,k0g,k1ok,k1g=verify_biclique_certificates()
    print("k0_certificate_ok",k0ok,"k0_gates",k0g)
    print("k1_certificate_ok",k1ok,"k1_gates_per_variable_sign",k1g)

    # Gate accounting:
    # Per variable triple: 12 OR2 edge groups + 6 OR4 halfcube groups + 1 OR8 occupancy = 19.
    prep=35*19
    k0=k0g
    # 7 shared variables x 2 signs, each local KG(6,2) conflict detector, plus OR14.
    k1=14*k1g + 13
    # 21 shared variable pairs x 4 shared sign patterns.
    # Each has 5 signals and threshold >=2 can be implemented in 10 gates; OR84 costs 83.
    k2=84*10 + 83
    final_or=2
    total=prep+k0+k1+k2+final_or
    print("gate_prep",prep)
    print("gate_k0",k0)
    print("gate_k1",k1)
    print("gate_k2",k2)
    print("gate_final_or",final_or)
    print("SAT_circuit_upper_bound",total)
