#!/usr/bin/env python3
"""ANDTREE-MITER362 independently checks full strict Resolution pivots and gate sources.
Run from repository root: python experiments/arc/lspv2_362_andtree_checker.py
"""
import json,subprocess
G="experiments/arc/lspv2_362_andtree_miter_public.js"
def canon(a):
    if type(a)!=list or any(type(x)!=int or x==0 for x in a) or any(-x in a for x in a):raise ValueError("bad clause")
    return tuple(sorted(set(a),key=lambda x:(abs(x),x)))
def get(n):
    command="const m=require('./"+G+"');console.log(JSON.stringify(m.produce("+str(n)+")))"
    return json.loads(subprocess.check_output(["node","-e",command],text=True))
def replay(d):
    n=d["n"];src=d["source"];pr=d["proof"];p=d["rootA"];q=d["rootB"]
    if len(src)!=6*n-4 or len(pr)!=8*n-9 or d["variables"]!=3*n-2:raise ValueError("bad counts")
    if any(len(a)!=len(set(a)) for a in src):raise ValueError("duplicate source")
    clauses=list(map(canon,src))
    for k in range(2*(n-1)):
        a,b,c=clauses[3*k:3*k+3]
        out_candidates=[x for x in a if x<0 and x in b]
        if len(out_candidates)!=1:raise ValueError("gate")
        out=-out_candidates[0]
        children=[x for x in a if x>0]+[x for x in b if x>0]
        if len(children)!=2 or len(set(children))!=2 or out<=max(children):raise ValueError("gate order")
        if c!=canon([out,-children[0],-children[1]]):raise ValueError("gate truth")
    if clauses[-2:]!=[canon([p,q]),canon([-p,-q])]:raise ValueError("miter")
    for i,z in enumerate(pr):
        a,b=z["parents"];pivot=z["pivot"]
        if type(a)!=int or type(b)!=int or not(0<=a<len(src)+i and 0<=b<len(src)+i):raise ValueError("parents")
        l,r=clauses[a],clauses[b]
        if pivot not in l or -pivot not in r:raise ValueError("pivot")
        v=canon([x for x in l if x!=pivot]+[x for x in r if x!=-pivot])
        if v!=canon(z["cl"]):raise ValueError("not resolvent")
        clauses.append(v)
    if d["empty"]!=len(clauses)-1 or clauses[-1]!=():raise ValueError("not UNSAT")
    if n<=5:
        def sat(cs):
            for mask in range(1<<d["variables"]):
                if all(any(bool(mask & (1<<(abs(x)-1)))==(x>0) for x in c) for c in cs):return True
            return False
        if sat(src):raise ValueError("SAT")
        for j in range(len(src)):
            if not sat(src[:j]+src[j+1:]):raise ValueError("nonessential")
    return len(pr)+(len(src) if n<=5 else 0)
def main():
    totals=0
    for n in [2,3,4,5,6,8,12,16]:
        d=get(n);count=replay(d);totals+=count
        bad=json.loads(json.dumps(d));bad["proof"][-1]["pivot"]=99999
        try:replay(bad);raise AssertionError("accepted corrupt proof")
        except ValueError:pass
        bad=json.loads(json.dumps(d));bad["source"][0]=[99999]
        try:replay(bad);raise AssertionError("accepted corrupt source")
        except ValueError:pass
        print(n,len(d["source"]),len(d["proof"]),count,"PASS")
    print("assertions",totals,"negative_controls",16)
if __name__=="__main__":main()
