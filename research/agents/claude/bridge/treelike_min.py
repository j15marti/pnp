#!/usr/bin/env python3
"""Exact minimum tree-like Resolution refutation size (= min decision-tree
size for the falsified-clause search problem) for small UNSAT CNFs.
Memoised over partial assignments. Runs well under 30 s for the listed cases.
Tree-like size counts leaves (= #derivation nodes of a tree refutation + 1 style
convention: size(F)=1 if some clause falsified, else min_x size(F|x=0)+size(F|x=1)).
Usage: python3 treelike_min.py
"""
import itertools, json, sys
from functools import lru_cache

def php(h):  # h+1 pigeons, h holes; var p(i,j)=1+i*h+j
    v=lambda i,j:1+i*h+j
    cl=[[v(i,j) for j in range(h)] for i in range(h+1)]
    for j in range(h):
        for a in range(h+1):
            for b in range(a+1,h+1): cl.append([-v(a,j),-v(b,j)])
    return h*(h+1),cl

def tseitin_Kn(n):  # complete graph K_n, odd charge on vertex 0 -> UNSAT
    edges=list(itertools.combinations(range(n),2)); ev={e:i+1 for i,e in enumerate(edges)}
    cl=[]
    for u in range(n):
        inc=[ev[e] for e in edges if u in e]
        par=1 if u==0 else 0
        for signs in itertools.product([0,1],repeat=len(inc)):
            if sum(signs)%2!=par:  # forbid assignments with wrong parity
                cl.append([ -x if s else x for x,s in zip(inc,signs)])
    return len(edges),cl

def min_tree(nv,cl):
    cl=[tuple(c) for c in cl]
    @lru_cache(None)
    def go(asg):  # asg: tuple of 0 unset,1 true,-1 false
        live=[]
        for c in cl:
            sat=False; rest=[]
            for l in c:
                a=asg[abs(l)-1]
                if a==0: rest.append(l)
                elif (a>0)==(l>0): sat=True;break
            if sat: continue
            if not rest: return 1
            live.append(rest)
        # branch on a variable in a shortest live clause (complete & optimal over all vars below)
        vs=sorted({abs(l) for c in live for l in c})
        best=10**9
        for x in vs:
            a0=list(asg);a0[x-1]=-1;a1=list(asg);a1[x-1]=1
            r=go(tuple(a0))
            if r>=best: continue
            r+=go(tuple(a1))
            best=min(best,r)
        return best
    return go(tuple([0]*nv))

if __name__=="__main__":
    out={}
    for h in (1,2,3):
        nv,cl=php(h); out[f"PHP_{h+1}^{h}"]=dict(vars=nv,clauses=len(cl),min_tree_leaves=min_tree(nv,cl))
    for n in (3,4,5):
        nv,cl=tseitin_Kn(n); out[f"Tseitin_K{n}"]=dict(vars=nv,clauses=len(cl),min_tree_leaves=min_tree(nv,cl))
    print(json.dumps(out,indent=1))
