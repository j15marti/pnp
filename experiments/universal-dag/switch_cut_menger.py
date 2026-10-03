from math import comb
from itertools import combinations

# SWITCH-CUT-MENGER3
# Topology-independent passive monotone contact lower bound for D(n,8).

def U8(n):
    return (comb(n,3)
            +268*comb(n,4)
            +3030*comb(n,5)
            +7800*comb(n,6)
            +5040*comb(n,7))

def tau8(n):
    M=8*comb(n,3)
    U=U8(n)
    d=0
    while comb(M-d,8)>U:
        d+=1
    return M,U,d

def d4_conflict_graph():
    C=[(T,p) for T in combinations(range(4),3) for p in range(8)]
    def conflict(c1,c2):
        T1,p1=c1; T2,p2=c2
        i1={v:i for i,v in enumerate(T1)}
        i2={v:i for i,v in enumerate(T2)}
        return all(((p1>>i1[v])&1)==((p2>>i2[v])&1)
                   for v in set(T1)&set(T2))
    E=[(i,j) for i in range(32) for j in range(i+1,32)
       if conflict(C[i],C[j])]
    adj=[0]*32
    for u,v in E:
        adj[u]|=1<<v
        adj[v]|=1<<u
    return E,adj

def unique_conflict_witness_count():
    E,adj=d4_conflict_graph()
    def find(u,v):
        seed=[u,v]
        forbidden=(1<<u)|(1<<v)|adj[u]|adj[v]
        cand=[w for w in range(32) if not ((forbidden>>w)&1)]
        def rec(start,left,arr):
            if left==0:
                return arr.copy()
            for ii in range(start,len(cand)):
                w=cand[ii]
                if all(not ((adj[w]>>z)&1) for z in arr):
                    arr.append(w)
                    out=rec(ii+1,left-1,arr)
                    if out is not None:
                        return out
                    arr.pop()
            return None
        r=rec(0,6,[])
        return seed+r if r else None
    good=0
    for u,v in E:
        S=find(u,v)
        assert S is not None
        c=sum(1 for a,b in combinations(S,2) if (adj[a]>>b)&1)
        assert c==1
        good+=1
    return len(E),good

if __name__=="__main__":
    print("n,M,U8,tau,contact_lower,endpoint_upper,gap")
    for n in range(4,13):
        M,U,t=tau8(n)
        print(n,M,U,t,2*t,2*M-16,(2*M-16)-2*t,sep=",")

    E,good=unique_conflict_witness_count()
    print("D4 unique-conflict pair witnesses",good,"of",E)

    assert 6**17 > 49*24**8

    print("STATUS")
    print("For passive monotone contact schemes computing D(n,8) on the exact-weight-8 promise:")
    print("every s-t cut uses at least tau distinct clause labels;")
    print("Menger gives at least tau edge-disjoint s-t paths;")
    print("every path needs at least two controlled contacts;")
    print("therefore C_contact >= 2*tau.")
    print("For all n>=4, tau>M/2, so one-occurrence C=M is impossible.")
    print("Asymptotically tau=M-O(n^(7/8)), hence C_contact>=2M-O(n^(7/8)).")
    print("This is a restricted passive monotone-contact lower bound, not a SAT time lower bound.")
