#!/usr/bin/env python3
"""TMR-3/076: complete exact T5 CSP count, strong-2-cover incidence accelerator.

Input format: ASCII 'n m' followed by exactly n declared vertex labels
0..n-1, then exactly m ordered endpoint pairs. Each explicit vertex
ensures n<=source length; duplicates ignored, loops give 0.
The count is for the original graph, including each separate private sink.
No uncharged oracle, alternate semantics, or external dependencies.
"""
from __future__ import annotations
import argparse
import itertools
import json
import random
import sys
from hashlib import sha256
from pathlib import Path

REVISION = "tmr3-t5-strong2cover076-v1"
BEATS = {1, 3}

def weight(a, b, c):
    return sum(all(((z-v) % 5) in BEATS for v in (a,b,c)) for z in range(5))

def parse(source):
    words = source.split()
    if len(words)<2 or not words[0].isascii() or not words[1].isascii() or not words[0].isdecimal() or not words[1].isdecimal():
        raise ValueError("invalid header")
    n,m = map(int,words[:2])
    if n<0 or m<0 or n>len(words)-2 or m>len(words)-2 or len(words)!=2+n+2*m:
        raise ValueError("invalid declarations or number of endpoints")
    for i in range(n):
        token=words[2+i]
        if not token.isascii() or not token.isdecimal() or int(token)!=i:
            raise ValueError("invalid declared vertex name")
    arcs=set()
    for j in range(m):
        a,b = words[2+n+2*j:4+n+2*j]
        if not a.isascii() or not b.isascii() or not a.isdecimal() or not b.isdecimal():
            raise ValueError("invalid endpoint token")
        u,v=int(a),int(b)
        if not (0<=u<n and 0<=v<n):
            raise ValueError("invalid vertex id")
        arcs.add((u,v))
    return n,sorted(arcs)

def serialize(n,arcs):
    return " ".join([str(n),str(len(arcs))]+[str(i) for i in range(n)]+[str(v) for edge in arcs for v in edge])

def recognize_triple(n,arcs):
    # Returns hubs, per-sink triples, or None. Isolates count as hubs.
    indeg=[[] for _ in range(n)]
    outdeg=[[] for _ in range(n)]
    for u,v in arcs:
        indeg[v].append(u);outdeg[u].append(v)
    hubs=[i for i in range(n) if not indeg[i]]
    hubset=set(hubs)
    triples=[]
    for v in range(n):
        if v in hubset: continue
        if len(indeg[v])!=3 or outdeg[v] or any(u not in hubset for u in indeg[v]):
            return None
        triples.append(tuple(sorted(indeg[v])))
    # If arc comes from a hub with indegree0, all accounted.
    return hubs,triples

def strong_cover(triples,k):
    # Exact minimum 2-hitting set. Exhaustive parameter search is charged.
    unique=sorted(set(triples))
    visited=0
    def dfs(mask,limit):
        nonlocal visited
        visited+=1
        defect=None
        for tri in unique:
            if sum((mask>>x)&1 for x in tri)<2:
                defect=tri
                break
        if defect is None: return mask
        rem=[x for x in defect if not ((mask>>x)&1)]
        needed=2-sum((mask>>x)&1 for x in defect)
        if mask.bit_count()+needed>limit: return None
        for take in itertools.combinations(rem,needed):
            plus=sum(1<<v for v in take)
            ans=dfs(mask|plus,limit)
            if ans is not None: return ans
        return None
    for t in range(k+1):
        ans=dfs(0,t)
        if ans is not None:
            assert ans.bit_count()==t
            return [i for i in range(k) if (ans>>i)&1],visited
    raise AssertionError("full cover must exist")

def incidence_count(n,arcs):
    rec=recognize_triple(n,arcs)
    if rec is None:
        raise ValueError("not incidence family")
    hubs,triples0=rec
    remap={v:i for i,v in enumerate(hubs)}
    triples=[tuple(remap[v] for v in e) for e in triples0]
    k=len(hubs)
    cover,nodes=strong_cover(triples,k)
    cset=set(cover)
    outsiders=[v for v in range(k) if v not in cset]
    total=0
    assignments=0
    for colors in itertools.product(range(5),repeat=len(cover)):
        assignments+=1
        given=dict(zip(cover,colors))
        local={v:[1]*5 for v in outsiders}
        factor=1
        for tri in triples:
            others=[v for v in tri if v not in cset]
            if len(others)==0:
                factor*=weight(*(given[v] for v in tri))
            elif len(others)==1:
                v=others[0]
                two=[given[u] for u in tri if u in cset]
                for color in range(5):
                    local[v][color]*=weight(two[0],two[1],color)
            else:
                raise AssertionError("invalid strong cover")
            if factor==0:break
        if factor:
            for v in outsiders:
                factor*=sum(local[v])
                if factor==0:break
        total+=factor
    return total,{'cover':len(cover),'search_nodes':nodes,'color_assignments':assignments, 'hub_count':k,'private_sinks':len(triples)}

def forest_count(n,arcs):
    # Fallback exact binary-edge spanning-forest assignments, root0 per component.
    neighbors=[[] for _ in range(n)]
    for u,v in arcs:
        neighbors[u].append((v,1))
        neighbors[v].append((u,-1))
    assigned=[None]*n
    components=0
    order=[]
    for r in range(n):
        if assigned[r] is not None: continue
        components+=1
        assigned[r]=0
        queue=[r]
        for v in queue:
            for w,d in neighbors[v]:
                if assigned[w] is None:
                    assigned[w]=0
                    order.append((v,w,d))
                    queue.append(w)
    rooted=0
    def dfs(i):
        nonlocal rooted
        if i==len(order):
            rooted+=all((assigned[v]-assigned[u])%5 in BEATS for u,v in arcs)
            return
        p,v,d=order[i]
        for q in (1,3):
            assigned[v]=(assigned[p]+d*q)%5
            dfs(i+1)
        assigned[v]=0
    dfs(0)
    return rooted*pow(5,components)

def brute(n,arcs):
    out=0
    for colors in itertools.product(range(5),repeat=n):
        if all((colors[v]-colors[u])%5 in BEATS for u,v in arcs):out+=1
    return out

def solve(source):
    n,arcs=parse(source)
    arcset=set(arcs)
    if any(u==v or (v,u) in arcset for u,v in arcs):
        return 0,'rejected-infeasible',{}
    rec=recognize_triple(n,arcs)
    if rec is not None:
        count,meta=incidence_count(n,arcs)
        return count,'strong2cover',meta
    return forest_count(n,arcs),'forest-fallback',{}

def dense_three_anchor_family(k):
    """Each outside hub joins all 3 unordered anchor pairs; min degree >=3."""
    if k < 4: raise ValueError("requires at least four hubs")
    arcs=[];triples=[]
    for v in range(3,k):
        for a,b in ((0,1),(0,2),(1,2)):
            sink=k+len(triples)
            triples.append((a,b,v))
            arcs.extend(((a,sink),(b,sink),(v,sink)))
    return k+len(triples),arcs,triples

def is_module_prime(n,arcs):
    """Slow exhaustive independent structural witness for k=5,6 only."""
    E=set(arcs)
    for mask in range(1,(1<<n)-1):
        if mask.bit_count()<=1:continue
        vs=[u for u in range(n) if mask>>u&1]
        v=vs[0]
        if all(all((((v,w) in E)==((x,w) in E)) and (((w,v) in E)==((w,x) in E)) for x in vs[1:]) for w in range(n) if not (mask>>w&1)):
            return False
    return True

def run_audit():
    rng=random.Random(202611171954)
    checks=0
    paths={'strong2cover':0,'forest-fallback':0, 'rejected-infeasible':0}
    for n in range(0,7):
        for _ in range(32):
            arcs=[(i,j) for i in range(n) for j in range(n) if i!=j and rng.random()<0.18]
            x,how,meta=solve(serialize(n,arcs))
            y=brute(n,arcs)
            assert x==y,(n,arcs,how,x,y)
            checks+=1;paths[how]+=1
    # Random incidence templates with k<=5, up to 5 sinks for exhaustive original-graph check.
    for k in range(3,6):
        trip=list(itertools.combinations(range(k),3))
        for _ in range(120):
            used=[t for t in trip if rng.random()<0.32]
            used=used[:5]
            arcs=[(v,k+i) for i,t in enumerate(used) for v in t]
            n=k+len(used)
            x,how,meta=solve(serialize(n,arcs))
            assert how=='strong2cover'
            ref=brute(n,arcs) if n<=7 else slow_reference(k,used)
            assert x==ref,(k,used,x,ref)
            checks+=1;paths[how]+=1
    # Symbolic sunflower exact count, including 3-color legitimate hub assignments.
    sunflowers={}
    for k in [4,5,6,7,10,30,100]:
        used=[(0,1,j) for j in range(2,k)]
        arcs=[(v,k+i) for i,t in enumerate(used) for v in t]
        value,how,meta=solve(serialize(k+len(used),arcs))
        expected=5*pow(4,k-2)+10*pow(2,k-2)
        assert value==expected,(k,value,expected)
        assert meta['cover']==2
        sunflowers[k]={'count':str(value),'digits':len(str(value)),'cover':2,'vertices':k+len(used),'arcs':len(arcs)}
        checks+=1;paths[how]+=1
    # Dense connected prime cores: h=n, cycle rank 5k-17, still cover 3.
    dense={}
    for k in (5,6,7,9,20,40):
        n,arcs,tri=dense_three_anchor_family(k)
        z,how,meta=solve(serialize(n,arcs))
        expected=5*pow(10,k-3)+30*pow(3,k-3)
        assert z==expected and meta['cover']==3
        assert len(arcs)-n+1==5*k-17
        deg=[0]*n
        for u,v in arcs:deg[u]+=1;deg[v]+=1
        assert min(deg)>=3
        if k<=7:assert z==slow_reference(k,tri)
        if k in (5,6):assert is_module_prime(n,arcs)
        dense[k]={'count':str(z),'digits':len(str(z)),'n':n,'m':len(arcs),'cycle_rank':len(arcs)-n+1,'strong_cover':3}
        paths[how]+=1;checks+=1
    for bad in ['','1','abc 0' ,'3 1 0','3 1 -1 2','3 1 0 3','0 1 0 0','3 0 0']:
        try: solve(bad)
        except ValueError: checks+=1
        else: raise AssertionError(('bad parsed',bad))
    cases=[('opposed',2,[(0,1),(1,0)]),('selfloop',1,[(0,0)]),('isolated',6,[])]
    for name,n,arcs in cases:
        v,_,_=solve(serialize(n,arcs))
        assert v==brute(n,arcs);checks+=1
    return {'revision':REVISION,'seed':202611171954,'checks':checks,'failures':0, 'paths':paths,'sunflowers':sunflowers, 'dense_prime':dense, 'tests':'random arbitrary graphs; incidence random; brute force; sunflower closed form; malformed; loop and opposed arc; isolates'}

def slow_reference(k,triples):
    total=0
    for colors in itertools.product(range(5),repeat=k):
        prod=1
        for tri in triples:
            prod*=weight(*(colors[v] for v in tri))
            if prod==0: break
        total+=prod
    return total

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--audit',action='store_true')
    args=parser.parse_args()
    if args.audit:
        print(json.dumps(run_audit(),sort_keys=True,separators=(',',':')))
    else:
        s=sys.stdin.read()
        try:
            value,method,info=solve(s)
        except ValueError as e:
            print(json.dumps({'error':str(e)}));sys.exit(2)
        print(json.dumps({'count':str(value),'satisfiable':value>0,'method':method,'info':info},sort_keys=True))
