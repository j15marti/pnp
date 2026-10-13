#!/usr/bin/env python3
"""Explicit proper-3CNF -> exact-(2,2) compiler and checked projections.

Mathematical conventions: clauses are tuples of nonzero signed integers;
Boolean 1 means true. Projection maps a target variable to an original positive
variable ID or to Boolean zero. No SAT oracle is used by the compiler.
Q is copied verbatim from the PC22_TRANSFER1 reproducibility package, itself
attributed there to CLAUDE-0021 / LBO3SAT-0031.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Iterable

Clause = tuple[int, ...]
CNF = list[Clause]
W1: CNF = [(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
 (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),
 (-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),
 (-3,12,15),(-5,-12,15),(-1,13,14)]
Q: CNF = W1[:7] + W1[8:]
PORTS = (1,7,13)

@dataclass
class Compiled:
    source: CNF
    balanced: CNF
    clauses: CNF
    source_n: int
    balanced_n: int
    n: int
    padding_gadgets: int
    R: int
    projection: dict[int,int]
    clone_to_balanced: dict[int,int]
    kinds: list[tuple[str,int]]


def check_proper(cnf: CNF, width: int = 3) -> int:
    if not cnf:
        raise ValueError('Use a fixed satisfiable output for the empty formula; nonempty domain here.')
    seen=set(); variables=set()
    for c in cnf:
        if len(c)!=width or any(not isinstance(x,int) or x==0 for x in c):
            raise ValueError('Each clause must have exactly the requested number of nonzero literals.')
        if len(set(map(abs,c)))!=width:
            raise ValueError('Repeated/complementary variable within a clause.')
        key=tuple(sorted(c))
        if key in seen: raise ValueError('Duplicate clause.')
        seen.add(key); variables.update(map(abs,c))
    n=max(variables)
    if variables != set(range(1,n+1)):
        raise ValueError('Use dense active variable IDs 1..n.')
    return n


def pad7(lit: int, first: int) -> CNF:
    """One signed occurrence of lit, five new exactly-(2,2) auxiliaries.
    Setting all auxiliaries to zero satisfies all seven clauses for either lit.
    """
    a,b,c,d,e=range(first,first+5)
    if abs(lit) in (a,b,c,d,e): raise ValueError('Auxiliary IDs must be fresh.')
    return [(lit,-a,-b),(a,c,-d),(a,d,-e),(b,e,-c),
            (b,-d,-e),(-a,c,d),(-b,-c,e)]


def balance(source: CNF) -> tuple[CNF,int,int]:
    n=check_proper(source)
    counts=Counter(l for c in source for l in c)
    out=list(source); next_var=n+1; gadgets=0
    for x in range(1,n+1):
        r=max(counts[x],counts[-x],2)
        for lit,deficit in ((x,r-counts[x]),(-x,r-counts[-x])):
            for _ in range(deficit):
                out.extend(pad7(lit,next_var)); next_var+=5; gadgets+=1
    return out,next_var-1,gadgets


def compile22(source: CNF) -> Compiled:
    n=check_proper(source)
    bal,nb,gadgets=balance(source)
    positions=defaultdict(lambda:{1:[],-1:[]})
    for i,c in enumerate(bal):
        for j,l in enumerate(c): positions[abs(l)][1 if l>0 else -1].append((i,j))
    out=[list(c) for c in bal]; clone_map={}; cycles=[]; offset=0
    for x in range(1,nb+1):
        pos=positions[x]; r=len(pos[1])
        if r!=len(pos[-1]) or r<2: raise AssertionError('Unbalanced intermediate.')
        ids=list(range(offset+1,offset+r+1)); offset+=r
        for j,z in enumerate(ids):
            clone_map[z]=x
            for sign in (1,-1):
                ci,cj=pos[sign][j]; out[ci][cj]=sign*z
        cycles.extend((ids[j],ids[(j+1)%r]) for j in range(r))
    R=offset
    if R%3: raise AssertionError('R must be a multiple of three.')
    kinds=[('source',i) if i<len(source) else ('balance',i) for i in range(len(bal))]
    for j,(u,v) in enumerate(cycles):
        q,p=divmod(j,3); out.append([-u,v,R+15*q+PORTS[p]])
        kinds.append(('implication',clone_map[u]))
    for q in range(R//3):
        for c in Q:
            out.append([(R+15*q+abs(l))*(1 if l>0 else -1) for l in c])
            kinds.append(('Q',q))
    projection={z:x if x<=n else 0 for z,x in clone_map.items()}
    projection.update({z:0 for z in range(R+1,6*R+1)})
    return Compiled(source,bal,[tuple(c) for c in out],n,nb,6*R,gadgets,R,
                    projection,clone_map,kinds)


def eval_cnf(cnf: CNF, values: dict[int,int]) -> bool:
    return all(any(values[abs(l)]==int(l>0) for l in c) for c in cnf)


def lift(comp: Compiled, values: dict[int,int]) -> dict[int,int]:
    return {z:values[x] if x else 0 for z,x in comp.projection.items()}


def properize23(cnf: CNF) -> tuple[CNF,dict[int,int]]:
    """Proper width-2/3 source -> proper width-3, with a constant restriction.
    Each binary D becomes D OR z and D OR not z. Existing 3-clauses first.
    """
    variables={abs(l) for c in cnf for l in c}
    if not variables: raise ValueError('Nonempty source required.')
    n=max(variables)
    if variables!=set(range(1,n+1)): raise ValueError('Dense source IDs required.')
    if any(len(c) not in (2,3) or len(set(map(abs,c)))!=len(c) for c in cnf):
        raise ValueError('Only proper binary/ternary clauses supported.')
    if len(set(tuple(sorted(c)) for c in cnf))!=len(cnf): raise ValueError('Duplicate input clauses.')
    out=[tuple(c) for c in cnf if len(c)==3]; mapping={i:i for i in range(1,n+1)}
    z=n
    for c in cnf:
        if len(c)==2:
            z+=1; out.extend([tuple(c)+(z,),tuple(c)+(-z,)]); mapping[z]=0
    return out,mapping


def colouring_cnf(vertices: int, edges: Iterable[tuple[int,int]]) -> CNF:
    es=sorted({tuple(sorted(e)) for e in edges})
    if any(u<0 or v>=vertices or u==v for u,v in es): raise ValueError('Simple graph required.')
    def x(v:int,k:int)->int: return 3*v+k+1
    out=[tuple(x(v,k) for k in range(3)) for v in range(vertices)]
    for v in range(vertices):
        for a in range(3):
            for b in range(a+1,3): out.append((-x(v,a),-x(v,b)))
    for u,v in es:
        for k in range(3): out.append((-x(u,k),-x(v,k)))
    return out


# Tiny explicit-polynomial kernel. Exponents are NOT silently multilinearized.
Poly=dict[tuple[int,...],int]
def add(p:Poly,q:Poly,scale:int=1)->Poly:
    out=dict(p)
    for m,c in q.items(): out[m]=out.get(m,0)+scale*c
    return {m:c for m,c in out.items() if c}
def mul(p:Poly,q:Poly)->Poly:
    out={}
    for m,c in p.items():
        for n,d in q.items():
            k=tuple(sorted(m+n)); out[k]=out.get(k,0)+c*d
    return {m:c for m,c in out.items() if c}
def clause_poly(c:Clause)->Poly:
    p={():1}
    for l in c: p=mul(p,{():1,(l,):-1} if l>0 else {(-l,):1})
    return p
def subst(p:Poly,mapping:dict[int,int])->Poly:
    out={}
    for m,c in p.items():
        v=tuple(sorted(mapping[x] for x in m))
        if 0 in v: continue
        out[v]=out.get(v,0)+c
    return {m:c for m,c in out.items() if c}
def reduced_mod(p:Poly,prime:int)->Poly:
    return {m:c%prime for m,c in p.items() if c%prime}
