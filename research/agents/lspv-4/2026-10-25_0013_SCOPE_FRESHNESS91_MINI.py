#!/usr/bin/env python3
"""Independent compact reproducer of SCOPE-FRESHNESS-VALIDATION91.
All claims are restricted to explicit finite tests and a supplied scoped grammar.
No FLMV TM step count or general SAT lower bound is measured.
"""
from itertools import combinations, product
from math import comb, ceil, log2
import json

checks=0
def test(x,why="check"):
    global checks
    checks+=1
    if not x: raise AssertionError(why)

def block(i,a,b):
    return [('O',i),('O',a),('O',b),('K',(i,a,b)),('C',b),('C',a),('C',i)]

def half(q,S,second=False):
    offset=q//2 if second else 0
    names=sorted(set(range(1,q+1))-set(S)) if second else sorted(S)
    return sum((block(i,q+2*(offset+j)+1,q+2*(offset+j)+2)
                for j,i in enumerate(names)),[])

def grammar(E,n,m):
    live=set();old=set();count=0;wid=0
    for typ,payload in E:
        if typ=='O':
            if payload in old or payload in live: return False,wid
            live.add(payload);old.add(payload);wid=max(wid,len(live))
        elif typ=='C':
            if payload not in live:return False,wid
            live.remove(payload)
        else:
            count+=1
            if len({abs(x) for x in payload})!=3 or not all(abs(x) in live for x in payload):
                return False,wid
    return not live and old==set(range(1,n+1)) and count==m,wid

def pin(v,a,b,sgn):
    E=[('O',v),('O',a),('O',b)]
    E += [('K',(sgn*v,sa*a,sb*b)) for sa,sb in product((1,-1),repeat=2)]
    return E+[('C',b),('C',a),('C',v)]

def frontier_models(E):
    active=[];tab={():1}
    for op,arg in E:
        nxt={}
        if op=='O':
            test(arg not in active,"local named overlap")
            for tup,k in tab.items():
                for bit in (0,1):nxt[tup+(bit,)]=nxt.get(tup+(bit,),0)+k
            active.append(arg)
        elif op=='K':
            ids=[active.index(abs(t)) for t in arg]
            for tup,k in tab.items():
                if any(tup[i]==(t>0) for t,i in zip(arg,ids)):nxt[tup]=nxt.get(tup,0)+k
        else:
            i=active.index(arg)
            for tup,k in tab.items():
                key=tup[:i]+tup[i+1:];nxt[key]=nxt.get(key,0)+k
            active.pop(i)
        tab=nxt
    test(not active)
    return tab.get((),0)

def ordinary_models(E,n):
    cls=[v for kind,v in E if kind=='K']
    return sum(all(any((a[abs(x)-1]==1)==(x>0) for x in clause)
                   for clause in cls) for a in product((0,1),repeat=n))

rows=[]
for q in (2,4,6,8):
    subsets=list(combinations(range(1,q+1),q//2))
    for S in subsets:
        suffix=half(q,S,True)
        for Sp in subsets:
            E=half(q,Sp)+suffix
            valid,width=grammar(E,3*q,q)
            test(valid==(S==Sp),"fooling pair")
            if valid:test(width==3,"matched width")
    e=half(q,subsets[0])+half(q,subsets[0],True)
    test(frontier_models(e)==7**q,"7^q models")
    rows.append({"q":q,"distinguishable_prefix_states":comb(q,q//2),
                 "log2_states":log2(comb(q,q//2)),"valid":len(subsets),
                 "invalid":len(subsets)*(len(subsets)-1)})
good=pin(1,3,4,1)+pin(2,5,6,-1)
bad=pin(1,3,4,1)+pin(1,5,6,-1)
test(grammar(good,6,8)[0])
test(not grammar(bad,6,8)[0])
gg,gb=frontier_models(good),frontier_models(bad)
og,ob=ordinary_models(good,6),ordinary_models(bad,6)
test((gg,gb,og,ob)==(16,16,16,0),"reopen changes ordinary SAT")
h=ceil(log2(64*(6+8+1)))
test((2+4*len(good))*h==820)
print(json.dumps({"run":"SCOPE-FRESHNESS91-MINI","status":"PASS",
 "checks":checks,"width":3,"rows":rows,
 "ordinary_models":[og,ob],"unvalidated_local_DP_models":[gg,gb],
 "matched_bits":820},sort_keys=True))
