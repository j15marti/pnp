#!/usr/bin/env python3
"""BINARYPROJ1: exact elimination of <=2-color interiors into pair nogoods.
Standard library, Python 3.10+. The projection/lift are polynomial algorithms.
Only the explicitly named test oracles enumerate assignments. Each audit
invocation has a 25-second cooperative cap; split ranges instead of extending it.
Example: python binary_projection_audit.py --batch graphs --n 5 --start 0 --count 256 --out out.json
"""
from __future__ import annotations
import argparse
from collections import Counter, deque
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import itertools as it
import json
from pathlib import Path
import random
import time

COLORS = (0, 1, 2)
SEED = 202610140840

def validate(n: int, edges: list[tuple[int,int]], masks: list[int]) -> None:
    if type(n) is not int or n < 0 or len(masks) != n:
        raise ValueError('invalid explicit vertex count/list count')
    if any(type(m) is not int or not 0 <= m <= 7 for m in masks):
        raise ValueError('color lists must be three-bit masks')
    if any(not isinstance(e, (list, tuple)) or len(e) != 2 for e in edges):
        raise ValueError('edge pairs required')
    if any(type(u) is not int or type(v) is not int or not 0 <= u < v < n for u,v in edges):
        raise ValueError('invalid canonical edge')
    if len({tuple(e) for e in edges}) != len(edges):
        raise ValueError('duplicate edge')

def implication_graph(b: int, clauses: list[tuple[int,int]]) -> list[list[int]]:
    # Literal 2*i+a means Boolean variable i has value a; complement is xor 1.
    adj = [set() for _ in range(2*b)]
    for p,q in clauses:
        adj[p^1].add(q); adj[q^1].add(p)
    return [sorted(x) for x in adj]

def solve_2sat(b: int, clauses: list[tuple[int,int]], units=()) -> list[int] | None:
    """Iterative Kosaraju, independent of the projection reachability code."""
    adj=implication_graph(b, clauses+[(p,p) for p in units]); rev=[[] for _ in adj]
    for u,ns in enumerate(adj):
        for v in ns: rev[v].append(u)
    seen=set(); finish=[]
    for r in range(2*b):
        if r in seen: continue
        seen.add(r); stack=[(r,0)]
        while stack:
            u,j=stack[-1]
            if j==len(adj[u]): finish.append(u);stack.pop();continue
            v=adj[u][j];stack[-1]=(u,j+1)
            if v not in seen: seen.add(v);stack.append((v,0))
    comp=[-1]*(2*b); k=0
    for r in reversed(finish):
        if comp[r]>=0: continue
        comp[r]=k; todo=[r]
        while todo:
            u=todo.pop()
            for v in rev[u]:
                if comp[v]<0:comp[v]=k;todo.append(v)
        k+=1
    if any(comp[2*i]==comp[2*i+1] for i in range(b)): return None
    answer=[int(comp[2*i+1]>comp[2*i]) for i in range(b)]
    def true(p): return answer[p//2]==p%2
    if not all(true(p) or true(q) for p,q in clauses) or not all(true(p) for p in units):
        raise AssertionError('SCC witness failed original Boolean formula')
    return answer

def reachability(adj):
    result=[]
    for r in range(len(adj)):
        seen={r};todo=[r]
        for u in todo:
            for v in adj[u]:
                if v not in seen:seen.add(v);todo.append(v)
        result.append(sum(1<<u for u in seen))
    return result

def path_between(adj,s,t):
    parent={s:None};todo=deque([s])
    while todo and t not in parent:
        u=todo.popleft()
        for v in adj[u]:
            if v not in parent:parent[v]=u;todo.append(v)
    if t not in parent:raise AssertionError('missing claimed path')
    out=[];v=t
    while v is not None:out.append(v);v=parent[v]
    return list(reversed(out))

@dataclass
class Kernel:
    n: int
    edges: list[tuple[int,int]]
    masks: list[int]
    boundary: list[int]
    interior: list[int]
    choices: list[tuple[int,int]]
    clauses: list[tuple[int,int]]
    requirements: dict[tuple[int,int],set[int]]
    forbidden: dict[tuple[int,int,int,int],dict]
    impossible: bool
    metrics: dict

    def accepts(self, coloring: dict[int,int]) -> bool:
        if set(coloring)!=set(self.boundary) or any(type(c) is not int or c not in COLORS for c in coloring.values()):
            raise ValueError('a complete boundary coloring is required')
        return not self.impossible and not any(coloring[u]==a and coloring[v]==b for u,a,v,b in self.forbidden)

    def lift(self, boundary_colors: dict[int,int]) -> tuple[int,...] | None:
        if not self.accepts(boundary_colors):return None
        units=sorted(set().union(*(self.requirements[(u,c)] for u,c in boundary_colors.items()))) if boundary_colors else []
        bits=solve_2sat(len(self.interior),self.clauses,units)
        if bits is None:raise AssertionError('accepted projected point did not lift')
        out=[-1]*self.n
        for u,c in boundary_colors.items():out[u]=c
        for i,v in enumerate(self.interior):out[v]=self.choices[i][bits[i]]
        if not all(self.masks[v]&(1<<out[v]) for v in range(self.n)) or not all(out[u]!=out[v] for u,v in self.edges):
            raise AssertionError('lift failed original list coloring')
        return tuple(out)

    def certificate_ok(self,key,record):
        u,a,v,b=key
        if record['kind']=='edge':return u!=v and (min(u,v),max(u,v)) in self.edges and a==b
        l,m=record['left_literal'],record['right_literal'];path=record['path']
        adj=implication_graph(len(self.interior),self.clauses)
        return (l in self.requirements[(u,a)] and m in self.requirements[(v,b)] and
                path[0]==l and path[-1]==(m^1) and all(y in adj[x] for x,y in zip(path,path[1:])))


def project(n: int, edges: list[tuple[int,int]], masks: list[int]) -> Kernel:
    validate(n,edges,masks);edges=[tuple(e) for e in edges]
    U=[v for v,m in enumerate(masks) if m==7];B=[v for v,m in enumerate(masks) if m!=7]
    req={(u,c):set() for u in U for c in COLORS};where={v:i for i,v in enumerate(B)}
    choices=[];clauses=[];forbidden={}
    if 0 in masks:return Kernel(n,edges,masks,U,B,[],[],req,{},True,{'empty_list':True})
    for i,v in enumerate(B):
        available=tuple(c for c in COLORS if masks[v]&(1<<c))
        if len(available)==1:
            available=available*2;clauses.append((2*i,2*i))  # use option zero
        choices.append(available)
    for u,v in edges:
        if u in where and v in where:
            i,j=where[u],where[v]
            for a,b in it.product((0,1),repeat=2):
                if choices[i][a]==choices[j][b]:clauses.append(((2*i+a)^1,(2*j+b)^1))
        elif u not in where and v not in where:
            for c in COLORS:forbidden[(u,c,v,c)]={'kind':'edge'}
        else:
            guard,inside=(u,v) if u not in where else (v,u);j=where[inside]
            for a,c in enumerate(choices[j]):req[(guard,c)].add((2*j+a)^1)
    adj=implication_graph(len(B),clauses);reach=reachability(adj)
    impossible=any((reach[2*i]>>(2*i+1))&1 and (reach[2*i+1]>>(2*i))&1 for i in range(len(B)))
    if not impossible:
        guards=sorted(req)
        for i,g in enumerate(guards):
            for h in guards[i:]:
                if g[0]==h[0] and g!=h:continue  # incompatible equality flags cannot co-occur
                key=(*g,*h)
                if key in forbidden:continue
                witness=next(((l,m) for l in sorted(req[g]) for m in sorted(req[h]) if (reach[l]>>(m^1))&1),None)
                if witness is not None:
                    l,m=witness
                    forbidden[key]={'kind':'path','left_literal':l,'right_literal':m,'path':path_between(adj,l,m^1)}
    metrics={'boundary_vertices':len(U),'interior_vertices':len(B),'base_clauses':len(clauses),
             'implication_arcs':sum(map(len,adj)),'reachability_bits_capacity':4*len(B)**2,
             'unary_nogoods':sum(k[0]==k[2] for k in forbidden),'binary_nogoods':sum(k[0]!=k[2] for k in forbidden)}
    return Kernel(n,edges,masks,U,B,choices,clauses,req,forbidden,impossible,metrics)

class Audit:
    def __init__(self):self.start=time.monotonic();self.counts=Counter()
    def check(self,ok,label):
        self.counts[label]+=1
        if not ok:raise AssertionError(label)
        if time.monotonic()-self.start>25:raise TimeoutError('split audit: 25-second cooperative deadline')

def oracle_models(n,edges,masks):
    return [c for c in it.product(COLORS,repeat=n) if all(masks[v]&(1<<c[v]) for v in range(n)) and all(c[u]!=c[v] for u,v in edges)]

def audit_instance(A,n,edges,masks):
    K=project(n,edges,masks);models=oracle_models(n,edges,masks)
    projected={tuple(c[u] for u in K.boundary) for c in models};positive=0
    for values in it.product(COLORS,repeat=len(K.boundary)):
        env=dict(zip(K.boundary,values));truth=values in projected
        A.check(K.accepts(env)==truth,'exact_full_boundary_projection')
        if truth:
            w=K.lift(env);A.check(w in models,'original_witness_lift');positive+=1
    for k,c in K.forbidden.items():A.check(K.certificate_ok(k,c),'nogood_path_or_edge_certificate')
    k=len(K.boundary);A.check(len(K.forbidden)<=3*k+9*k*(k-1)//2,'quadratic_output_bound')
    return {'masks':masks,'models':len(models),'projected_models':len(projected),'lifts':positive,
            'impossible_base':K.impossible,'metrics':K.metrics}

def exhaustive(A,n):
    if not 0<=n<=3:raise ValueError('full list-mask audit is n<=3')
    pairs=list(it.combinations(range(n),2));rows=[]
    for bits in range(1<<len(pairs)):
        es=[e for j,e in enumerate(pairs) if bits>>j&1]
        for masks in it.product(range(8),repeat=n):
            rows.append({'graph':bits,**audit_instance(A,n,es,list(masks))})
    return {'n':n,'cases':len(rows),'rows':rows}

def graphs(A,n,start,count):
    if not 1<=n<=5:raise ValueError('finite graph audit n<=5')
    pairs=list(it.combinations(range(n),2));stop=min(1<<len(pairs),start+count);rng=random.Random(SEED+n+start);rows=[]
    for bits in range(start,stop):
        es=[e for j,e in enumerate(pairs) if bits>>j&1]
        palettes=[[7]*n,[3]*n,[5]*n,[6]*n]
        palettes += [[rng.choice((1,2,3,4,5,6,7,7,7)) for _ in range(n)] for _ in range(8)]
        rows.append({'graph':bits,'cases':[audit_instance(A,n,es,m) for m in palettes]})
    return {'n':n,'start':start,'graphs':len(rows),'cases':12*len(rows),'seed':SEED+n+start,'rows':rows}

def local(A):
    K=project(3,[(0,2),(1,2)],[7,7,3]);bad=[]
    for a,b in it.product(COLORS,repeat=2):
        expected=(a,b) not in ((0,1),(1,0))
        A.check(K.accepts({0:a,1:b})==expected,'path_requires_general_pair_relation')
        if not expected:bad.append((a,b))
    # Neither no edge nor an inequality edge on two full-domain vertices represents this relation.
    A.check(len(bad)==2 and K.accepts({0:0,1:0}),'same_vertex_graph_language_not_closed')
    # The argument cannot extend to a hidden THREE-choice center: all pairs project fully.
    rainbow=[c for c in it.product(COLORS,repeat=3) if len(set(c))<=2]
    for keep in it.combinations(range(3),2):A.check(len({tuple(c[i] for i in keep) for c in rainbow})==9,'three_choice_center_pairwise_escape')
    A.check(len(rainbow)==21,'three_choice_center_not_full')
    # Long binary path: length L parity determines endpoint obstruction, with k=2 fixed.
    large=[]
    for length in (2,3,8,9,32,33,128,129):
        n=length+1;edges=[(i,i+1) for i in range(length)];masks=[3]*n;masks[0]=masks[-1]=7
        P=project(n,edges,masks)
        for a,b in it.product(COLORS,repeat=2):
            # Internal vertices use only 0,1. When both ends use 0,1, they must obey path parity.
            truth=a==2 or b==2 or ((a==b)==(length%2==0))
            A.check(P.accepts({0:a,n-1:b})==truth,'long_binary_chain_exact_parity')
            if truth:A.check(P.lift({0:a,n-1:b}) is not None,'long_chain_lift')
        A.check(len(P.forbidden)==2,'long_interior_constant_boundary_output')
        large.append({'length':length,'metrics':P.metrics,'nogoods':[list(k) for k in P.forbidden]})
    # Full three-choice domains can remain easy with unbounded k.
    for n in (8,32,128):
        split=n//2;es=[(u,v) for u in range(split) for v in range(split,n)]
        P=project(n,es,[7]*n);c={v:int(v>=split) for v in range(n)}
        A.check(P.accepts(c) and P.lift(c) is not None,'large_k_bipartite_easy_control')
    # Intrinsic 2-SAT obstruction must not be missed when boundary is empty.
    P=project(3,[(0,1),(0,2),(1,2)],[3]*3)
    A.check(P.impossible and not P.accepts({}),'unsat_binary_base')
    for args in ((2,[(0,2)],[7,7]),(2,[(0,1),(0,1)],[7,7]),(1,[],[True]),(1,[],[8])):
        try:project(*args)
        except ValueError:A.check(True,'malformed_input_rejected')
        else:A.check(False,'malformed_input_rejected')
    return {'local_forbidden':bad,'long_paths':large}

def integration(A,source_dir):
    """The exact prior PINCORE source is supplied as a pinned dependency, not advice."""
    import sys
    sys.path.insert(0,str(Path(source_dir).resolve()))
    import pin_core_audit as pc
    pc.require_dependency()
    if hashlib.sha256(Path(pc.__file__).read_bytes()).hexdigest()!='82bef7428c6ae9c53bff13f0525a4954c3ffada96a6da3b0392160cb70004fb9':
        raise RuntimeError('PINCORE revision mismatch')
    rng=random.Random(SEED);rows=[]
    for n in range(1,5):
        pairs=list(it.combinations(range(n),2))
        for bits in range(1<<len(pairs)):
            es=[e for j,e in enumerate(pairs) if bits>>j&1];R=pc.old.reduce_two_trees(n,es);h=R['universe']
            dec=pc.recover(pc.old.encode_pair(R));A.check(dec is not None,'integration_exact_decoder')
            source_models=oracle_models(n,es,[7]*n)
            patterns=[{}]+[{v:rng.randrange(3) for v in range(h) if rng.random()<.2} for _ in range(5)]
            if source_models:
                w=pc.lift_source(R,source_models[0]) if hasattr(pc,'lift_source') else pc.old.lift_source(R,source_models[0])
                patterns.append({v:w[v] for v in range(h) if rng.random()<.5})
            cases=[]
            for pins in patterns:
                masks,hubs=pc.compress(R,pins);K=project(n,es,masks)
                feasible=[]
                for values in it.product(COLORS,repeat=len(K.boundary)):
                    env=dict(zip(K.boundary,values))
                    if all(hubs) and K.accepts(env):
                        c=K.lift(env);w=pc.lift(R,pins,c,hubs)
                        A.check(pc.old.valid_target(R,w) and all(w[v]==z for v,z in pins.items()),'complete_target_pins_and_edges')
                        feasible.append(c)
                # Independent target solver accesses only original target graph/pins.
                w,_=pc.pinned_search(h,pc.union_edges(R),pins)
                A.check(bool(feasible)==(w is not None),'independent_target_projection_composition')
                cases.append({'pins':pins,'masks':masks,'hub_masks':hubs,'k':len(K.boundary),'yes':bool(feasible)})
            rows.append({'n':n,'graph':bits,'cases':cases})
    return {'graphs':len(rows),'rows':rows}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--batch',choices=['local','exhaustive','graphs','integration'],required=True)
    p.add_argument('--n',type=int,default=3);p.add_argument('--start',type=int,default=0);p.add_argument('--count',type=int,default=256)
    p.add_argument('--source-dir',type=Path);p.add_argument('--out',type=Path,required=True);args=p.parse_args();A=Audit()
    result={'run_id':'BINARYPROJ1','status':'COMPUTATIONAL','batch':args.batch,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'timestamp_utc':datetime.now(timezone.utc).isoformat(),'parameters':{k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},'failures':0}
    try:
        if args.batch=='local':result['data']=local(A)
        elif args.batch=='exhaustive':result['data']=exhaustive(A,args.n)
        elif args.batch=='graphs':result['data']=graphs(A,args.n,args.start,args.count)
        elif args.source_dir is None:raise ValueError('--source-dir required for integration')
        else:result['data']=integration(A,args.source_dir)
    except Exception as exc:result['failures']=1;result['error']=repr(exc);raise
    finally:
        result.update(assertions=sum(A.counts.values()),counts=dict(A.counts),elapsed_seconds=time.monotonic()-A.start)
        args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('batch','assertions','failures','elapsed_seconds')}))
if __name__=='__main__':main()
