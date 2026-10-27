#!/usr/bin/env python3
"""ARC-OUTPUT-LEDGER190: standalone reproduction, Python standard library.
No physical TM timing measurement and no unrestricted SAT lower bound.
"""
from collections import Counter
from hashlib import sha256
from math import ceil, log2
from itertools import product
import json

W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),
    (-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),
    (1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),
    (-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),
    (4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
Y=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),
   (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
checks=0
def check(x,msg):
    global checks
    checks+=1
    if not x: raise AssertionError(msg)
def valid(F,n):
    pos,neg=Counter(),Counter()
    seen=set()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3: return False
        if any(abs(x)<1 or abs(x)>n for x in c): return False
        key=tuple(sorted(c))
        if key in seen: return False
        seen.add(key)
        for x in c: (pos if x>0 else neg)[abs(x)]+=1
    return all(pos[i]==2 and neg[i]==2 for i in range(1,n+1))
def models(F,n):
    cnt=0
    for a in range(1<<n):
        if all(any((((a>>(abs(x)-1))&1)==(x>0)) for x in c) for c in F):
            cnt+=1
    return cnt
def copies(F,n,r):
    return [tuple((1 if x>0 else -1)*(abs(x)+j*n) for x in c)
            for j in range(r) for c in F]
def bits(n,m):
    w=n.bit_length()
    b=max(32,m.bit_length())
    return 8+2*b+m*(3*(w+1)+1)
def stream_hash(F,n,r,limit=3000000):
    nn,mm=n*r,len(F)*r
    w,b=nn.bit_length(),max(32,mm.bit_length())
    length=bits(nn,mm)
    if length>limit: return {"mode":"exact length, not emitted","bits":length}
    h=sha256()
    header=("10101100"+format(nn,"0%db"%b)+format(mm,"0%db"%b)).encode()
    h.update(header)
    emitted=len(header)
    for j in range(r):
        for c in F:
            for x in c:
                token=(("1" if x>0 else "0")+
                      format(j*n+abs(x),"0%db"%w)).encode()
                h.update(token);emitted+=len(token)
            h.update(b"0");emitted+=1
    check(emitted==length,"exact streamed bits")
    return {"mode":"physically emitted and hashed","bits":emitted,"sha256":h.hexdigest()}
def main():
    A=[list(x) for x in W1]
    for ci,li in [(6,0),(11,0)]:
        check(abs(A[ci][li])==4,"A sign location")
        A[ci][li]=-A[ci][li]
    A=[tuple(x) for x in A]
    seeds=[("W1_UNSAT",W1,15,0),("W1_A_SAT",A,15,272),
           ("Y_MONO_SAT",Y,6,20)]
    physical=[]
    nested=[]
    for tag,F,n,expected in seeds:
        check(valid(F,n),tag+" proper signed 2P2N")
        check(models(F,n)==expected,tag+" model count")
        if tag=="Y_MONO_SAT":
            check(all(all(x>0 for x in c) or all(x<0 for x in c) for c in F),
                  "clause monotonicity")
        N=bits(n,len(F))
        for r in [1,2,8,N]:
            check(3*len(F)*r==4*n*r,"incidence balance")
            if r<=8:
                G=copies(F,n,r)
                check(valid(G,n*r),"actual first-level proper 2P2N")
            info=stream_hash(F,n,r)
            check(info["bits"]==bits(n*r,len(F)*r),"output bit length")
            physical.append({"source":tag,"N":N,"r":r,"L":info["bits"],
               "SAT_input_and_output":expected>0,**info})
        for r1,r2 in [(2,2),(2,3)]:
            G=copies(F,n,r1)
            H=copies(G,n*r1,r2)
            check(valid(G,n*r1),"actual level one")
            check(valid(H,n*r1*r2),"actual level two")
            check(len(H)==len(F)*r1*r2,"two-level clause count")
            nested.append({"source":tag,"r1":r1,"r2":r2,
                           "N":N,"L1":bits(n*r1,len(F)*r1),
                           "L2":bits(n*r1*r2,len(F)*r1*r2),
                           "SAT":expected>0})
    scaling=[]
    for q in [1,2,4,8,16,32,64]:
        N=bits(15*q,20*q)
        L=bits(15*q*N,20*q*N)
        check(L>=N*N//2,"quadratic output floor")
        scaling.append({"q":q,"N":N,"r":N,"L":L,
                        "L_over_N2":L/(N*N)})
    transfer=[]
    for ta in [10,11,14,18,20,30]:
        for sa in [0,1,5,10,20]:
            t,s=ta/10,sa/10
            check(t+max(1,s)>=2,"one-tape inequality vacuous")
            check(t+max(1,s)+s>=2,"one-input-head product vacuous")
            check(t+s>=1,"reversal consequence vacuous")
            transfer.append({"t":t,"s":s})
    data={"run":"ARC-OUTPUT-LEDGER190","assertions":checks,"failures":0,
          "base_counts":{"W1":0,"W1_A":272,"Y":20},
          "physical":physical,"nested":nested,"scaling":scaling,
          "transfer_grid":transfer,
          "limits":["No physical Turing-machine transition experiment",
                    "Semantic product proof gives large-instance labels",
                    "Output-port and one-shared-tape conventions intentionally differ"]}
    print(json.dumps(data,indent=2))
if __name__=="__main__":main()
