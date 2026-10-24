#!/usr/bin/env python3
"""Strict signed exact-(2,2) torus controls; stdlib only, source-coherent.
Run from j15marti/pnp root:
 python research/agents/lspv-2/2026-10-24_1412_TORUS_EXACT22_FRONTIER116_minirepro.py
No SAT lower bound, no all-input contraction.
"""
import ast, math, json, collections, hashlib, random, sys
from pathlib import Path
SOURCE=Path("research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt")
WITNESS_HEX="6c2144363530a3925c8aa38509469054a0d2a359a0d2951a7"

def load():
    text="\n".join(l for l in SOURCE.read_text().splitlines() if not l.startswith("#"))
    U=ast.literal_eval(text)
    V=[row[:] for row in U]
    assert U[3]==[-2,-3,-194] and U[13]==[3,9,10] and U[254]==[1,33,65]
    V[3][1]=3; V[13][0]=-3
    w=int(WITNESS_HEX,16)
    assert len(U)==264 and max(abs(x) for row in U for x in row)==198
    assert satisfied(V,[(w>>i)&1 for i in range(198)])
    return U,V,[(w>>i)&1 for i in range(198)]

def satisfied(F,bits):
    return all(any((l>0)==bool(bits[abs(l)-1]) for l in row) for row in F)

def grid(h):
    assert h>=6 and h%3==0
    nx=h*h; M=2*nx
    C=[]
    for r in range(h):
      for c in range(h):
        x=r*h+c+1
        C.append([x,r*h+(c+1)%h+1,nx+2*(r*h+c)+1])
        C.append([-x,-((r+1)%h*h+c+1),nx+2*(r*h+c)+2])
    for shift,sign in [(0,1),(1,-1),(2,-1)]:
      for k in range(0,M,3):
        C.append([sign*(nx+((shift+k+i)%M)+1) for i in range(3)])
    assert len(C)==4*nx
    bits=[1]*nx+[(j%2) for j in range(M)]
    assert satisfied(C,bits)
    return C,bits

def build(h,label,U,V,original_bits):
    G,gb=grid(h)
    C=[row[:] for row in (V if label=="SAT" else U)]
    G=[[((1 if l>0 else -1)*(198+abs(l))) for l in row] for row in G]
    z=198+h*h+1
    assert C[254]==[1,33,65] and G[0][2]==z
    C[254][1]=z; G[0][2]=33
    F=C+G
    if label=="SAT": assert satisfied(F,original_bits+gb)
    else: assert F[:254]==U[:254]
    return F

def graph_and_grammar(F,n):
    count=collections.defaultdict(lambda:[0,0]);seen=set()
    parent=list(range(n+1))
    def root(x):
      while parent[x]!=x:
        parent[x]=parent[parent[x]]
        x=parent[x]
      return x
    def join(x,y):
      x,y=root(x),root(y)
      if x!=y: parent[x]=y
    for row in F:
      assert len(row)==3 and len({abs(l) for l in row})==3
      key=tuple(sorted(row));assert key not in seen;seen.add(key)
      for l in row:
        assert 1<=abs(l)<=n
        count[abs(l)][int(l<0)]+=1
      a,b,c=map(abs,row);join(a,b);join(b,c)
    assert len(count)==n and all(v==[2,2] for v in count.values())
    assert len({root(x) for x in range(1,n+1)})==1
    # A complementary pair has same signed literals except one opposite pivot.
    seen=set(seen)
    for row in F:
      for j,l in enumerate(row):
        cp=row[:];cp[j]=-l
        assert tuple(sorted(cp)) not in seen
    return len(count)

def random_edge_frontier(h,seed):
    # This is only a finite test of the all-orders theorem.
    E=[]
    for r in range(h):
      for c in range(h):
        v=r*h+c
        E.append((v,r*h+(c+1)%h))
        E.append((v,(r+1)%h*h+c))
    random.Random(seed).shuffle(E)
    E1=set(range(len(E)//2))
    A=set();B=set()
    for j,(u,v) in enumerate(E):
      (A if j in E1 else B).update((u,v))
    return len(A&B)

def run(sizes):
    U,V,w=load()
    rows=[]
    for h in sizes:
      n=198+3*h*h;m=264+4*h*h
      SAT=build(h,"SAT",U,V,w)
      UNSAT=build(h,"UNSAT",U,V,w)
      for F in (SAT,UNSAT):assert graph_and_grammar(F,n)==n
      assert len(SAT)==len(UNSAT)==m and m*3==n*4
      delta=[(i,j,SAT[i][j],UNSAT[i][j]) for i in range(m) for j in range(3)
             if SAT[i][j]!=UNSAT[i][j]]
      assert len(delta)==2 and {abs(d[2]) for d in delta}=={3}
      low=math.ceil(h/2)
      if h<=48:
        for seed in range(20):
          assert random_edge_frontier(h,20261024+seed)>=low
      word=(64*(n+m+1)-1).bit_length()
      N=(4*m+2)*word
      rows.append({"h":h,"n":n,"m":m,"N_bits":N,
                   "min_any_order_live_source_bound":low,"connected":True,
                   "strict_exact22":True,"matching_cardinality_fails":m>n,
                   "SAT_source_hash":hashlib.sha256(str(SAT).encode()).hexdigest(),
                   "UNSAT_source_hash":hashlib.sha256(str(UNSAT).encode()).hexdigest(),
                   "changed_sign_fields":delta})
    print(json.dumps({"run":"TORUS-EXACT22-FRONTIER116",
                      "SAT_proof":"full V witness replay",
                      "UNSAT_proof":"unchanged source U[:254], see DOECKER-CORE-CERT61 independent verifier",
                      "controls":rows,"assertion_failures":0},indent=2))
if __name__=="__main__":
    run([int(x) for x in sys.argv[1:]] if len(sys.argv)>1 else [6,12,24,48,96])
