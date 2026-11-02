#!/usr/bin/env python3
"""LSPV-2 323: compact self-contained source-signed distributive factorer.
Run from pnp repo root: python experiments/arc/lspv2_323/compact323.py
A restricted architecture, NOT unrestricted minimum gates or a P-vs-NP proof.
"""
from collections import Counter, defaultdict
from itertools import combinations
import ast, json
from pathlib import Path

P9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
N9=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F9=P9+[tuple(-v for v in c) for c in N9]
Y6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
P15=[(1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15)]
N15=[(1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15)]
F15=P15+[tuple(-v for v in c) for c in N15]

def validate(F,n):
    if n<3 or n%3 or 3*len(F)!=4*n:return False
    seen=set();count=Counter()
    for c in F:
        if len(c)!=3 or len({abs(v) for v in c})!=3:return False
        if not all(v>0 for v in c) and not all(v<0 for v in c):return False
        if any(not isinstance(v,int) or isinstance(v,bool) or v==0 or abs(v)>n for v in c):return False
        sig=tuple(sorted(c))
        if sig in seen:return False
        seen.add(sig)
        for v in c:count[abs(v),v>0]+=1
    return all(count[i,True]==count[i,False]==2 for i in range(1,n+1))

def compile(F,n):
    if not validate(F,n):raise ValueError("malformed canonical original")
    incidence=defaultdict(list)
    for j,c in enumerate(F):
        for a,b in combinations(sorted(abs(v) for v in c),2):
            incidence[c[0]>0,a,b].append(j)
    repeated=sorted([(k,ix) for k,ix in incidence.items() if len(ix)==2])
    handled=set();gates=[];outputs=[]
    def add(op,a,b,provenance=()):
        z=n+len(gates)+1
        gates.append((op,a,b,z,tuple(provenance)))
        return z
    for (sign,a,b),ids in repeated:
        i,j=ids
        assert i not in handled and j not in handled
        handled.update((i,j))
        c=next(abs(v) for v in F[i] if abs(v) not in (a,b))
        d=next(abs(v) for v in F[j] if abs(v) not in (a,b))
        p=add("OR" if sign else "AND",a,b,ids)
        q=add("AND" if sign else "OR",c,d,ids)
        outputs.append(add("OR" if sign else "NAND",p,q,ids))
    for j,clause in enumerate(F):
        if j in handled:continue
        a,b,c=map(abs,clause)
        pair=add("OR" if clause[0]>0 else "AND",a,b,(j,))
        outputs.append(add("OR" if clause[0]>0 else "NAND",pair,c,(j,)))
    while len(outputs)>1:
        outputs=[add("AND",outputs[k],outputs[k+1]) if k+1<len(outputs) else outputs[k] for k in range(0,len(outputs),2)]
    assert len(gates)==3*len(F)-1-2*len(repeated)
    return gates,outputs[0],len(repeated)

def evaluate(gates,out,bits):
    values={i+1:bits[i] for i in range(len(bits))}
    for op,a,b,z,_ in gates:
        x,y=values[a],values[b]
        values[z]=int(x or y) if op=="OR" else int(x and y) if op=="AND" else int(not(x and y))
    return values[out]

def source(F,bits):
    return int(all(any(bits[abs(v)-1]==int(v>0) for v in c) for c in F))

def run():
    cases={"Y6":(Y6,6),"F9":(F9,9),"F15":(F15,15)}
    fixture=Path("research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt")
    if fixture.exists():
        text=fixture.read_text()
        U=ast.literal_eval(text[text.index("[["):])
        V=[row[:] for row in U]
        V[2][2],V[44][2]=V[44][2],V[2][2]
        cases.update(U198=(U,198),V198=(V,198))
    results={}
    for name,(F,n) in cases.items():
        gates,out,d=compile(F,n)
        count=0
        for mask in range((1<<n) if n<=15 else 64):
            bits=[(mask>>i)&1 for i in range(n)]
            got=evaluate(gates,out,bits)
            assert got==source(F,bits),(name,mask)
            count+=got
        if n<=15:assert count=={"Y6":20,"F9":70,"F15":1032}[name]
        results[name]={"n":n,"m":len(F),"duplicate_signed_pairs":d,
                       "gates":len(gates),"mixed_width_tseitin_clauses":3*len(gates)+1,
                       "models":count if n<=15 else None}
    p={3:0,5:1,6:0,7:0,8:0}
    G,o,_=compile(F9,9)
    pin_count={}
    for x1 in (0,1):
        ct=0
        for q in range(8):
            a={**p,1:x1,2:q&1,4:(q>>1)&1,9:(q>>2)&1}
            bits=[a[i] for i in range(1,10)]
            ct+=evaluate(G,o,bits)
        pin_count[x1]=ct
    assert pin_count=={0:2,1:0}
    results["same_original_F9_pins"]=pin_count
    results["status"]="restricted exact forward circuit, NOT SAT-decision lower bound"
    print(json.dumps(results,indent=2))

if __name__=="__main__":run()
