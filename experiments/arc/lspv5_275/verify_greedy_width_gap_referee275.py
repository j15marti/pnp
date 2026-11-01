#!/usr/bin/env python3
"""No-producer-import verifier for LSPV-5 REFEREE275."""
from collections import Counter
from itertools import combinations, permutations, product
import json
import pathlib
import sys

P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=P+tuple(tuple(-v for v in c) for c in N)
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-v for v in c) for c in N15)
NUM=Counter()

def ck(x,msg):
    NUM['assertions']+=1
    if not x:raise AssertionError(msg)

def grammar(G,n):
    if n%3 or 3*len(G)!=4*n:return False
    q=Counter(); seen=set()
    for c in G:
        if len(c)!=3 or len(set(map(abs,c)))!=3:return False
        if any(not 1<=abs(x)<=n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        z=tuple(sorted(c))
        if z in seen:return False
        seen.add(z);q.update(c)
    return all(q[v]==q[-v]==2 for v in range(1,n+1))

def good(G,a):return all(any(a[abs(x)]==int(x>0) for x in c) for c in G)

def count(G,n,p):
    free=[v for v in range(1,n+1) if v not in p]
    return sum(good(G,{**p,**dict(zip(free,b))}) for b in product((0,1),repeat=len(free)))

def graph(G,p):
    scopes=[]
    for j,c in enumerate(G,1):
        if any(abs(x) in p and p[abs(x)]==int(x>0) for x in c):continue
        s=tuple(sorted(abs(x) for x in c if abs(x) not in p))
        ck(bool(s),'no immediate empty source clause')
        scopes.append((j,s))
    a={v:set() for _,s in scopes for v in s}
    for _,s in scopes:
        for u,v in combinations(s,2):a[u].add(v);a[v].add(u)
    return scopes,a

def elim(a,x):
    b={v:set(a[v])-{x} for v in a if v!=x}; ns=tuple(a[x])
    for u,v in combinations(ns,2):b[u].add(v);b[v].add(u)
    return b

def width(a,order):
    a={v:set(z) for v,z in a.items()}; w=0; rows=[]
    for x in order:
        z=1+len(a[x]); w=max(w,z);rows.append((x,z,tuple(sorted(a[x]))));a=elim(a,x)
    return w,rows

def greedy(a):
    a={v:set(z) for v,z in a.items()};o=[]
    while a:
        x=min(a,key=lambda v:(1+len(a[v]),v));o.append(x);a=elim(a,x)
    return tuple(o)

def minor(a,B):
    def conn(S):
        seen={next(iter(S))}
        while True:
            z=seen|{v for u in seen for v in a[u]&S}
            if z==seen:return z==S
            seen=z
    return all(conn(S) for S in B) and all(any(v in a[u] for u in B[i] for v in B[j]) for i in range(5) for j in range(i+1,5))

def main():
    path=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else 'results/raw/arc/2026-11-01_1548_LSPV5_GREEDY_WIDTH_GAP_REFEREE275_raw.json')
    R=json.loads(path.read_text())
    ck(R['status']=='PASS' and R['P_vs_NP']=='OPEN','status firewall')
    ck(grammar(F,9) and grammar(Y,6) and grammar(F15,15),'canonical sources')
    p={5:0,7:0}; scopes,a=graph(F,p)
    ck(count(F,9,{})==70 and count(F,9,p)==13,'F9 source counts')
    ck([[j,list(s)] for j,s in scopes]==[[z['clause_id'],z['scope']] for z in R['counterexample']['source_scopes']],'source scope provenance')
    go=greedy(a);gw,grows=width(a,go)
    ck(go==(1,2,3,4,6,8,9) and gw==6,'greedy width six')
    all_orders=0;best=99;best_order=None
    for order in permutations(sorted(a)):
        all_orders+=1;w,_=width(a,order)
        if w<best:best=w;best_order=order
    NUM['orders_checked']=all_orders
    ck(best==5,'exact exhaustive optimum five')
    ck(width(a,(3,2,1,4,6,8,9))[0]==5,'claimed optimal order')
    ck(R['counterexample']['cap5_greedy_status']=='UNRESOLVED' and R['counterexample']['cap5_optimal_order_status']=='SAT','cap-five consequence')
    B=[{1,3},{4},{6},{8},{9}]
    ck(minor(a,B),'explicit K5 minor lower certificate')
    after=elim(a,1)
    ck(all(len(after[v])==5 for v in after),'first greedy fill is K6')
    f9s={5:0,6:1,7:0,8:0,9:1}; f9u={1:1,3:0,5:1,6:0,7:0,8:0}
    s15=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))
    u15=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
    ck((count(F,9,f9s),count(F,9,f9u),count(F15,15,s15),count(F15,15,u15),count(Y,6,{}))==(3,0,2,0,20),'same-source both labels')
    leaf=0
    free=[v for v in range(1,10) if v not in f9u]
    for bits in product((0,1),repeat=len(free)):
        a0={**f9u,**dict(zip(free,bits))}
        ck(any(not any(a0[abs(x)]==int(x>0) for x in c) for c in F),'complete original-clause UNSAT leaf')
        leaf+=1
    NUM['F9_UNSAT_leaves']=leaf
    su=0
    for i,j in combinations(range(12),2):
        for s,t in product((0,1),repeat=2):
            d={};ok=True
            for c,b in ((F[i],s),(F[j],t)):
                for l in c:
                    want=int(l>0) if b else int(l<0);v=abs(l)
                    if v in d and d[v]!=want:ok=False
                    d[v]=want
            same=any(l in F[j] for l in F[i]);opp=any(-l in F[j] for l in F[i])
            ck(ok==(not opp if s==t else not same),'S/U mode')
            su+=1
    NUM['SU_modes']=su
    bad=[Y[:-1],Y+Y[:1],Y[:2]+((1,1,2),)+Y[3:],Y[:2]+((1,-2,3),)+Y[3:],Y[:2]+((0,2,3),)+Y[3:],Y[:2]+((1,2,7),)+Y[3:]]
    for z in bad:ck(not grammar(z,6),'malformed rejection')
    w=R['resource_scope']['wrappers']
    ck(w['DELAY']['native_steps']==4096 and w['DELAY']['logical_endpoint_xor']==0,'DELAY')
    ck(w['COPY']['shadow_writes']==128 and w['COPY']['logical_endpoint_xor']==0,'COPY')
    ck(w['RECOMP']['source_literal_reads']==36 and w['RECOMP']['retained_clause_status_bits']==0,'RECOMP')
    ck(w['changed_then_restored']['adjacent_physical_changes']==2 and w['changed_then_restored']['endpoint_delta']==0,'restore XOR')
    out={'verifier':'no_producer_import_REFEREE275','status':'PASS','checks':dict(NUM),
         'exact_optimum_closed_width':best,'first_best_order':list(best_order),
         'U198_V198':'inherited, not used in theorem','native_FLMV_trace':False,'P_vs_NP':'OPEN'}
    text=json.dumps(out,indent=2,sort_keys=True)+'\n'
    if len(sys.argv)>2:pathlib.Path(sys.argv[2]).write_text(text)
    print(text,end='')

if __name__=='__main__':main()
