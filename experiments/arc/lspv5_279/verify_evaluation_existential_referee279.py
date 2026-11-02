#!/usr/bin/env python3
"""Independent no-import verifier for REFEREE279."""
from __future__ import annotations
import argparse,itertools,json

P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
M=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))

def value(x):
    return int(all(any((x>>(v-1))&1 for v in c) for c in P) and
               all(any(not((x>>(v-1))&1) for v in c) for c in M))

def residual(table,S,a):
    rest=[i for i in range(9) if not ((S>>i)&1)]
    return tuple(table[a|sum(((b>>k)&1)<<i for k,i in enumerate(rest))]
                 for b in range(1<<len(rest)))

def level_cost(table,S,i):
    pv=[j for j in range(9) if (S>>j)&1]; seen=set()
    for z in range(1<<len(pv)):
        a=sum(((z>>k)&1)<<j for k,j in enumerate(pv))
        low=residual(table,S|1<<i,a); high=residual(table,S|1<<i,a|1<<i)
        if low!=high:seen.add((low,high))
    return len(seen)

def size(table,order):
    S=0;z=0
    for v in order:z+=level_cost(table,S,v-1);S|=1<<(v-1)
    return z

def depth(table):
    memo={}
    def go(mask,bits):
        key=(mask,bits)
        if key in memo:return memo[key]
        vals={table[x] for x in range(512) if x&mask==bits}
        if len(vals)==1:memo[key]=0;return 0
        ans=1+min(max(go(mask|1<<i,bits),go(mask|1<<i,bits|1<<i))
                  for i in range(9) if not ((mask>>i)&1))
        memo[key]=ans;return ans
    return go(0,0),len(memo)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("raw");a=ap.parse_args()
    r=json.load(open(a.raw)); checks=0; table=tuple(value(x) for x in range(512))
    assert sum(table)==70;checks+=512
    assert size(table,tuple(range(1,10)))==66;checks+=1
    assert size(table,tuple(r["obdd"]["minimum_order"]))==52;checks+=1
    assert size(table,tuple(r["obdd"]["maximum_order"]))==80;checks+=1
    d,states=depth(table);assert d==9==r["decision_tree"]["D_evaluate"];checks+=states
    # Every rejecting assignment is certified by one falsified 3-clause.
    for x,v in enumerate(table):
        if not v:
            assert any(all(((x>>(q-1))&1)==0 for q in c) for c in P) or any(
                all(((x>>(q-1))&1)==1 for q in c) for c in M)
            checks+=1
    # Recheck the same-original 6-pin SAT/UNSAT pair directly.
    for first,expected in ((0,2),(1,0)):
        z=0
        for x2,x4,x9 in itertools.product((0,1),repeat=3):
            x=(first<<0)|(x2<<1)|(0<<2)|(x4<<3)|(1<<4)|(0<<5)|(0<<6)|(0<<7)|(x9<<8)
            z+=table[x]
        assert z==expected;checks+=8
    assert r["P_vs_NP"]=="OPEN" and "no all-input polynomial controller" in r["limitations"];checks+=2
    print(json.dumps({"status":"PASS","independent_assertion_groups":checks,
      "decision_states":states,"F9_models":sum(table),"P_vs_NP":"OPEN"},indent=2))
if __name__=="__main__":main()
