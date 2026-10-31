#!/usr/bin/env python3
"""ARC-AMORTIZED-INDEX282: small standalone exact source and FLMV ledger checks.
Requires U_source.json from the linked full reproducibility ZIP in same directory.
This is an abstract finite-tape witness, not an end-to-end FLMV SAT solver.
"""
from fractions import Fraction
from pathlib import Path
from itertools import product
from collections import Counter
import json

Y = ((1,2,3),(1,4,5),(2,4,6),(3,5,6),
     (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
V_WITNESS = (
"010110111001100010001111000101011110010101001111010001001011010000110010000100001001010111010000111010101010001101001010010010110001100011111001010101011011001110000100000001110110111000101100100001"
)
def count(clause, a):
    return sum((a[abs(x)-1] == 1) == (x>0) for x in clause)
def sat(F, a):
    return all(count(C,a)>0 for C in F)
def valid(F):
    n=max(abs(x) for C in F for x in C)
    m=len(F)
    signed=Counter(x for C in F for x in C)
    assert 3*m==4*n and n%3==0
    assert len({tuple(sorted(C)) for C in F})==m
    assert all(len(C)==3 and len({abs(x) for x in C})==3 and
               (all(x>0 for x in C) or all(x<0 for x in C)) for C in F)
    assert all(signed[i]==signed[-i]==2 for i in range(1,n+1))
    return n,m
def dpll(F):
    F=tuple(tuple(c) for c in F)
    counters=Counter()
    def recurse(Cs):
        counters["nodes"]+=1
        while True:
            if () in Cs:return False
            if not Cs:return True
            unit=next((c[0] for c in Cs if len(c)==1),None)
            if unit is None:break
            Cs=tuple(tuple(x for x in c if x!=-unit) for c in Cs if unit not in c)
        branch=min(Cs,key=len)[0]
        for lit in (branch,-branch):
            child=tuple(tuple(x for x in c if x!=-lit) for c in Cs if lit not in c)
            if recurse(child):return True
        return False
    return recurse(F),dict(counters)
def certify_U(F):
    boundary=[F[0],F[1]]
    nodes=[]
    for j in range(6):
        block=F[2+42*j:2+42*(j+1)]
        lo,hi=32*j+1,32*(j+1)
        local=[tuple(z for z in C if lo<=abs(z)<=hi) for C in block]
        yes,stats=dpll(local)
        assert not yes
        nodes.append(stats["nodes"])
        boundary.append(tuple(sorted({z for C in block for z in C if abs(z)>192})))
    for b in product([0,1],repeat=6):
        full=[0]*192+list(b)
        assert any(count(C,full)==0 for C in boundary)
    return nodes
def exact_bytes(n):
    m=4*n//3
    header=len(("p cnf %d %d\n"%(n,m)).encode("ascii"))
    return header+5*m+2*n+4*sum(len(str(j)) for j in range(1,n+1))
def source_bytes(F):
    n,m=valid(F)
    return len(("p cnf %d %d\n"%(n,m) +
                "".join(" ".join(map(str,C))+" 0\n" for C in F)).encode("ascii"))
def index_jump_trace(h):
    idx=[0]*(h+1); head=0; Q=E=D=T=0
    for j in range(h):
        assert idx[head]==0
        idx[head]=1; head+=1
        Q+=1;D+=1;T+=1
    address=sum(v<<j for j,v in enumerate(idx))
    erased=sum(idx);idx[:]=[0]*(h+1)
    E+=erased;D+=erased;T+=1
    T+=1 # read blank, whether source byte or not
    for _ in range(h):head-=1;T+=1
    assert head==0
    T+=1 # indexed jump back to address zero (blank index)
    assert D==2*Q==2*E and D<=2*T and not any(idx)
    return dict(h=h,initial_index_ones=0,total_native_primitive_events=T,
                Q_direct=Q,E_erased=E,adjacent_physical_XOR=D,
                endpoint_physical_XOR=0,single_erase_step_XOR=h,
                far_input_address=address)
def flmv(c):
    f=Fraction(1); ds=[]
    for k in range(1,4):
        f=c*f/(1+f)
        ds.append(min((1/f-c)/k,c**(-k)))
    assert ds[1]>ds[0] and ds[1]>ds[2] and ds[1]>c**(-4)
    return str(ds[1])
def main():
    assert sum(sat(Y,b) for b in product([0,1],repeat=6))==20
    assert source_bytes(Y)==exact_bytes(6)==86
    ufile=Path(__file__).parent/"U_source.json"
    if not ufile.exists():
        raise FileNotFoundError("Place U_source.json from the ARC282 complete ZIP beside this file.")
    U=[tuple(C) for C in json.loads(ufile.read_text())]
    V=[list(C) for C in U]
    V[1][0],V[7][0]=V[7][0],V[1][0]
    V=[tuple(C) for C in V]
    assert valid(U)==valid(V)==(198,264)
    assert source_bytes(U)==source_bytes(V)==exact_bytes(198)==3674
    unsat_nodes=certify_U(U)
    assert len(V_WITNESS)==198 and sat(V,[int(v) for v in V_WITNESS])
    for F in (Y,U,V):
        n,m=valid(F)
        for e in (0,1):
            base=[e]*n;cs=[count(C,base) for C in F]
            state=base+[v for t in cs for v in (t&1,(t>>1)&1,int(t>0))]
            for j in range(n):
                b=base[:];b[j]^=1
                ts=[count(C,b) for C in F]
                new=b+[v for t in ts for v in (t&1,(t>>1)&1,int(t>0))]
                assert sum(x!=y for x,y in zip(state,new))==7
    assert flmv(Fraction(6,5))=="23/45"
    assert flmv(Fraction(241,200))=="11642479/23232400"
    print(json.dumps({"status":"PASS","both_labels":"U198 UNSAT, V198 SAT",
                      "U_local_refutation_nodes":unsat_nodes,"Y_models":20,
                      "source_bytes":{"Y6":86,"U198":3674,"V198":3674},
                      "atomic_index_traces":[index_jump_trace(h) for h in [1,2,4,8,16,32,64]],
                      "flmv_d_star":{"6/5":"23/45","241/200":"11642479/23232400"},
                      "proof_status":"restricted exact; P versus NP OPEN"},indent=2))
if __name__=="__main__":main()
