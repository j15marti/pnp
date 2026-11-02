#!/usr/bin/env python3
"""LSPV-4 SWAP-PROMISE-COFACTOR334, stdlib, deterministic.
Exhaustively validates every same-sign Z6 copy swap and a source-pinned F9.
This reports finite computation, not a P-vs-NP result.
"""
import json
from collections import Counter
Z=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
def shifted(F,d):
    return tuple(tuple((1 if v>0 else -1)*(abs(v)+d) for v in c) for c in F)
def valid(F,n):
    if n<3 or n%3 or len(F)!=4*n//3:return False
    cnt=Counter();seen=set()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3 or any(type(x)!=int or x==0 or abs(x)>n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key);cnt.update(c)
    return all(cnt[i]==cnt[-i]==2 for i in range(1,n+1))
def sat(F,a):
    return all(any(((a>>(abs(x)-1))&1)==int(x>0) for x in c) for c in F)
def swap(F,i,k,j,l):
    H=[list(c) for c in F]
    assert H[i][k]*H[j][l]>0
    H[i][k],H[j][l]=H[j][l],H[i][k]
    return tuple(map(tuple,H))
def connected(F,n):
    N=[set() for _ in range(n)]
    for c in F:
        ids=[abs(v)-1 for v in c]
        for u in ids:N[u].update(ids)
    seen={0};stack=[0]
    while stack:
        for u in N[stack.pop()]-seen:seen.add(u);stack.append(u)
    return len(seen)==n
def mask(F,n):
    return sum(1<<a for a in range(1<<n) if sat(F,a))
def prof(c,p):
    W=[[0,0],[0,0]];rest=Z[:c]+Z[c+1:]
    for a in range(64):
        if not sat(rest,a):continue
        u=int(((a>>(abs(Z[c][p])-1))&1)==int(Z[c][p]>0))
        A=int(any(((a>>(abs(v)-1))&1)==int(v>0) for k,v in enumerate(Z[c]) if k!=p))
        W[u][A]+=1
    return W
def bilinear(W):
    b=q=both=0
    for u in range(2):
      for A in range(2):
       for v in range(2):
        for B in range(2):
         k=W[u][A]*W[v][B]
         old=(u or A) and (v or B)
         new=(v or A) and (u or B)
         b+=k*bool(old);q+=k*bool(new);both+=k*bool(old and new)
    return (b,q,both,b-both,q-both)
def main():
    assert valid(Z,6) and valid(F9,9)
    assert sum(sat(F9,a) for a in range(512))==70
    base=Z+shifted(Z,6);assert valid(base,12)
    original=mask(base,12);assert original.bit_count()==324
    hist=Counter();profiles=set();tested=0
    for polarity in (1,-1):
      for i in range(8):
       if (Z[i][0]>0)!=(polarity>0):continue
       for k in range(3):
        W=prof(i,k);profiles.add(tuple(W[0]+W[1]))
        for j in range(8,16):
         if (base[j][0]>0)!=(polarity>0):continue
         for l in range(3):
          H=swap(base,i,k,j,l)
          assert valid(H,12) and connected(H,12)
          M=mask(H,12)
          vals=(original.bit_count(),M.bit_count(),(original&M).bit_count(),
                (original&~M).bit_count(),(M&~original).bit_count())
          assert vals==bilinear(W)
          hist[vals]+=1;tested+=1
    assert tested==288 and hist==Counter({(324,318,270,54,48):288})
    assert profiles=={(4,9,3,6)}
    B=swap(base,1,1,8,0);mB=mask(B,12)
    z=mask(Z,6);counts=[0]*5
    for a in range(1<<18):
        g=bool((z>>(a&63))&1)
        p=g and bool((original>>(a>>6))&1)
        q=g and bool((mB>>(a>>6))&1)
        for k,flag in enumerate((p,q,p and q,p and not q,q and not p)):counts[k]+=flag
    assert counts==[5832,5724,4860,972,864]
    pin=[sum(sat(F9,a) and all(((a>>(i-1))&1)==v for i,v in ((1,b),(2,0),(3,0),(6,1)))
             for a in range(512)) for b in (0,1)]
    assert pin==[1,0]
    F21=F9+shifted(Z,9)+shifted(Z,15);S21=swap(F21,13,1,20,0)
    assert valid(F21,21) and valid(S21,21)
    bad=[base+(base[0],),base[:-1],((-1,2,3),)+base[1:],((1,1,3),)+base[1:],((1,2,13),)+base[1:],((0,2,3),)+base[1:],((True,2,3),)+base[1:]]
    assert all(not valid(x,12) for x in bad)
    return {'run':'LSPV4_SWAP_PROMISE_COFACTOR334','swaps':tested,
      'profile':[[4,9],[3,6]],'twelve_variable_stats':[324,318,270,54,48],
      'eighteen_variable_stats':counts,'eighteen_variable_rows':262144,
      'F9_models':70,'F9_pin_SAT_UNSAT':pin,'F9_Z6x2_models':[22680,22260],
      'malformed_rejected':len(bad),'private_forward_gates_Z6x2':47,
      'semantic_inequivalence_formula':'R1 & R2 & (u XOR v) & (A XOR B)',
      'native_FLMV_trace':'NOT_OBTAINED','P_vs_NP':'OPEN'}
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
