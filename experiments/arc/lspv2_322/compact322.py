#!/usr/bin/env python3
"""LSPV-2 322 compact self-contained signed-pair optimizer for canonical M22 inputs.
Run: python experiments/arc/lspv2_322/compact322.py
The complete charged producer and independent verifiers are in the run archive.
No SAT-label oracle, no P-vs-NP proof, no external dependencies.
"""
from collections import Counter, defaultdict
from itertools import combinations, product
import ast, json
from pathlib import Path

F9_P = [(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
F9_N = [(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F9 = F9_P + [tuple(-i for i in c) for c in F9_N]
Y6 = [(1,2,3),(1,4,5),(2,4,6),(3,5,6),
      (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
P15 = [(1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
       (6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15)]
N15 = [(1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),
       (4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15)]
F15 = P15 + [tuple(-i for i in c) for c in N15]

def valid(F,n):
    if n<3 or n%3 or len(F)*3!=4*n:return False
    p=Counter();seen=set()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if any(x==0 or abs(x)>n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        sig=tuple(sorted(c))
        if sig in seen:return False
        seen.add(sig)
        for x in c:p[abs(x),x>0]+=1
    return all(p[i,True]==p[i,False]==2 for i in range(1,n+1))

def pair_options(c):
    op="OR" if c[0]>0 else "AND"
    return [(op,)+p for p in combinations(sorted(abs(x) for x in c),2)]

def exact_pairs(F):
    # Every signed pair is in at most two clauses; repeat-pair edges are
    # disjoint by exact signed variable degree 2. Sorting is paid.
    occ=defaultdict(list)
    for j,c in enumerate(F):
        for p in pair_options(c):occ[p].append(j)
    repeat=sorted(p for p,ids in occ.items() if len(ids)==2)
    matched=set()
    for p in repeat:
        ids=occ[p]
        assert len(ids)==2 and all(j not in matched for j in ids)
        matched.update(ids)
    selected=repeat+[pair_options(c)[0] for j,c in enumerate(F) if j not in matched]
    assert len(selected)==len(F)-len(repeat)
    return selected,len(repeat)

def compile_source(F,n):
    if not valid(F,n):raise ValueError("malformed canonical original")
    pairs,d=exact_pairs(F)
    gates=[];pairids={}
    def add(op,a,b):
        g=n+len(gates)+1
        gates.append((op,a,b,g))
        return g
    for op,a,b in pairs:pairids[op,a,b]=add(op,a,b)
    clause_gates=[]
    for c in F:
        pair=next(p for p in pair_options(c) if p in pairids)
        last=next(abs(x) for x in c if abs(x) not in pair[1:])
        clause_gates.append(add("OR" if c[0]>0 else "NAND",
                                pairids[pair],last))
    layer=clause_gates
    while len(layer)>1:
        layer=[add("AND",layer[i],layer[i+1]) if i+1<len(layer) else layer[i]
               for i in range(0,len(layer),2)]
    assert len(gates)==3*len(F)-1-d
    return gates,layer[0],d

def eval_circuit(gates,n,out,a):
    vals={i:a[i] for i in range(1,n+1)}
    for op,x,y,z in gates:
        A,B=vals[x],vals[y]
        vals[z]=int(A or B) if op=="OR" else (A&B if op=="AND" else 1-(A&B))
    return vals[out]

def eval_source(F,a):
    return int(all(any(a[abs(x)]==int(x>0) for x in c) for c in F))

def tseitin(gates,out):
    clauses=[]
    for op,a,b,z in gates:
        if op=="OR":clauses.extend([(-z,a,b),(z,-a),(z,-b)])
        elif op=="AND":clauses.extend([(z,-a,-b),(-z,a),(-z,b)])
        else:clauses.extend([(-z,-a,-b),(z,a),(z,b)])
    return clauses+[(out,)]

def run():
    cases=[("Y6",Y6,6),("F9",F9,9),("F15",F15,15)]
    root=Path(__file__).resolve().parents[3]
    fixture=root/"research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt"
    if fixture.exists():
        text=fixture.read_text()
        U=ast.literal_eval(text[text.index("[["):])
        V=[c[:] for c in U]
        V[2][2],V[44][2]=V[44][2],V[2][2]
        cases += [("U198",U,198),("V198",V,198)]
    out={}
    for name,F,n in cases:
        G,o,d=compile_source(F,n)
        assert len(tseitin(G,o))==3*len(G)+1
        models=0
        for bits in range(1<<n if n<=15 else 64):
            a={i+1:(bits>>i)&1 for i in range(n)}
            assert eval_circuit(G,n,o,a)==eval_source(F,a)
            models+=eval_source(F,a)
        out[name]={"n":n,"m":len(F),"signed_repeated_pairs":d,
                   "gates":len(G),"tseitin_clauses":3*len(G)+1,
                   "models_exhaustive_if_n_at_most_15":models if n<=15 else None}
    pbad={1:1,3:0,5:1,6:0,7:0,8:0}
    counts={}
    for lab,p in (("UNSAT",pbad),("SAT",{**pbad,1:0})):
        count=0
        for bits in range(8):
            a={**p,2:bits&1,4:(bits>>1)&1,9:(bits>>2)&1}
            count+=eval_source(F9,a)
        counts[lab]=count
    assert counts=={"UNSAT":0,"SAT":2}
    for bad in (F9[:-1],F9+[F9[0]],[(1,-5,6)]+F9[1:]):
        assert not valid(bad,9)
    out["F9_same_original_pins"]=counts
    out["status"]="PASS, restricted exact circuit architecture; P versus NP OPEN"
    print(json.dumps(out,indent=2))
if __name__=="__main__":run()
