#!/usr/bin/env python3
"""MERGEGUARD1: source-matched value merging and exact lift audit.
Python 3.10+, standard library. binary_projection_audit.py is a pinned dependency.
Every production routine except the explicit audit oracles is polynomial.
The 25-second cap applies to each audit batch; cap exits are not NO answers.
Run --batch local, --batch graphs --n 5, --batch general, --batch hardness,
or --batch integration. --out FILE is required. Finite checks are COMPUTATIONAL.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import itertools as it
import json
from pathlib import Path
import random
import time
import binary_projection_audit as bp

SEED=202610140900
DEP='96c54399e26c7268046563eee727383f36ff38e15be8401cbc4c3515230cd75e'
COL=(0,1,2); MERGED=3; ALL=511

def colors(mask): return tuple(c for c in COL if mask>>c&1)

@dataclass
class CSP:
    domains: list[int]
    relations: dict[tuple[int,int],int]
    def __post_init__(self):
        if any(type(m) is not int or not 0<=m<8 for m in self.domains):raise ValueError('invalid domain')
        for (u,v),mask in self.relations.items():
            if type(u) is not int or type(v) is not int or not 0<=u<v<len(self.domains) or type(mask) is not int or not 0<=mask<512:
                raise ValueError('invalid binary relation')
    @property
    def n(self):return len(self.domains)
    def allows(self,u,a,v,b):
        if u>v:u,v,a,b=v,u,b,a
        return bool(self.relations.get((u,v),ALL)>>(3*a+b)&1)
    def accepts(self,t):
        return len(t)==self.n and all(type(c) is int and c in COL and self.domains[v]>>c&1 for v,c in enumerate(t)) and all(mask>>(3*t[u]+t[v])&1 for (u,v),mask in self.relations.items())

def graph(n,edges,masks=None):
    neq=sum(1<<(3*a+b) for a,b in it.product(COL,repeat=2) if a!=b)
    return CSP(list(masks) if masks is not None else [7]*n,{tuple(e):neq for e in edges})

@dataclass
class Merge:
    original: CSP
    pivot: int
    pair: tuple[int,int]
    guards: list[tuple[int,int,int,int]]
    def quotient_domains(self):
        out=[colors(m) for m in self.original.domains]
        out[self.pivot]=tuple(c for c in out[self.pivot] if c not in self.pair)+(MERGED,)
        return out
    def support(self,v,c):
        return tuple(a for a in self.pair if self.original.allows(self.pivot,a,v,c))
    def naive(self,t):
        P=self.original;x=self.pivot
        if len(t)!=P.n or any(c not in d for c,d in zip(t,self.quotient_domains())):return False
        for (u,v),mask in P.relations.items():
            if u!=x and v!=x:
                if not P.allows(u,t[u],v,t[v]):return False
            else:
                y=v if u==x else u
                if t[x]==MERGED:
                    if not self.support(y,t[y]):return False
                elif not P.allows(x,t[x],y,t[y]):return False
        return True
    def repaired(self,t):
        return self.naive(t) and (t[self.pivot]!=MERGED or not any(t[u]==a and t[v]==b for u,a,v,b in self.guards))
    def lift(self,t):
        if not self.repaired(t):return None
        P=self.original;x=self.pivot
        for c in (self.pair if t[x]==MERGED else (t[x],)):
            candidate=list(t);candidate[x]=c
            if P.accepts(candidate):return tuple(candidate)
        raise AssertionError('repaired quotient failed full source lift')

def compile_merge(P:CSP,x:int,pair=(0,1))->Merge:
    if type(x) is not int or not 0<=x<P.n or len(pair)!=2 or pair[0]==pair[1] or any(type(a) is not int or a not in colors(P.domains[x]) for a in pair):
        raise ValueError('invalid merge')
    a,b=pair;guards=[]
    for u,v in it.combinations([i for i in range(P.n) if i!=x],2):
        for c,d in it.product(colors(P.domains[u]),colors(P.domains[v])):
            if not P.allows(u,c,v,d):continue
            su=tuple(z for z in pair if P.allows(x,z,u,c));sv=tuple(z for z in pair if P.allows(x,z,v,d))
            if (su==(a,) and sv==(b,)) or (su==(b,) and sv==(a,)):guards.append((u,c,v,d))
    return Merge(P,x,tuple(pair),guards)

def quotient_image(P,x,pair):
    # Exponential AUDIT oracle only, distinct from compiled guard construction.
    return {tuple(MERGED if i==x and c in pair else c for i,c in enumerate(t))
            for t in it.product(*(colors(m) for m in P.domains)) if P.accepts(t)}

def binary_lift(P:CSP,fibers:list[tuple[int,...]]):
    """One prescribed simultaneous quotient assignment, fiber sizes at most 2."""
    if len(fibers)!=P.n or any(not 1<=len(f)<=2 or len(set(f))!=len(f) or any(c not in colors(P.domains[v]) for c in f) for v,f in enumerate(fibers)):
        raise ValueError('invalid fibers')
    options=[f if len(f)==2 else f*2 for f in fibers];clauses=[]
    for v,f in enumerate(fibers):
        if len(f)==1:clauses.append((2*v,2*v))
    for (u,v) in P.relations:
        for a,b in it.product((0,1),repeat=2):
            if not P.allows(u,options[u][a],v,options[v][b]):clauses.append(((2*u+a)^1,(2*v+b)^1))
    bits=bp.solve_2sat(P.n,clauses)
    if bits is None:return None
    t=tuple(options[v][bits[v]] for v in range(P.n))
    if not P.accepts(t):raise AssertionError('fiber lift did not satisfy original')
    return t

class Audit:
    def __init__(self):self.start=time.monotonic();self.counts=Counter()
    def check(self,ok,label):
        self.counts[label]+=1
        if not ok:raise AssertionError(label)
        if time.monotonic()-self.start>25:raise TimeoutError('split audit batch')

def check_merge(A,P,x,pair):
    M=compile_merge(P,x,pair);oracle=quotient_image(P,x,pair);spurious=[];models=0;lifts=0
    for t in it.product(*M.quotient_domains()):
        expected=t in oracle;naive=M.naive(t);repaired=M.repaired(t)
        A.check(repaired==expected,'exact_repaired_quotient')
        A.check(not expected or naive,'forward_image_in_naive_quotient')
        if repaired:
            w=M.lift(t);A.check(P.accepts(w),'original_source_lift');lifts+=1
        if naive:models+=1
        if naive and not expected:spurious.append(t)
    A.check(bool(M.guards) or not spurious,'local_empty_guard_certificate')
    A.check(len(M.guards)<=9*(P.n-1)*(P.n-2)//2,'quadratic_guard_bound')
    return {'pivot':x,'pair':pair,'guards':M.guards,'image_models':len(oracle),'naive_models':models,
            'spurious_count':len(spurious),'first_spurious':spurious[0] if spurious else None,'lift_count':lifts}

def local_batch(A,start=0,count=4096):
    rows=[]
    # Exhaust every support function D(y)->P({0,1}) for two neighbors.
    for index in range(start,min(4096,start+count)):
        left,right=index//64,index%64
        def relation(code):
            mask=sum(1<<(6+c) for c in COL) # third original color always allowed
            for c in COL:
                support=code>>(2*c)&3
                for a in (0,1):
                    if support>>a&1:mask|=1<<(3*a+c)
            return mask
        r1,r2=relation(left),relation(right)
        for kind,bg in [('full',ALL),('neq',sum(1<<(3*a+b) for a,b in it.product(COL,repeat=2) if a!=b)),('eq',273)]:
            P=CSP([7]*3,{(0,1):r1,(0,2):r2,(1,2):bg})
            row=check_merge(A,P,0,(0,1));rows.append({'support_pair':index,'background':kind,**row})
    return {'support_pairs':min(count,4096-start),'instances':len(rows),'rows':rows}

def graphs_batch(A,n):
    if not 1<=n<=5:raise ValueError('finite exhaustive graph n<=5')
    pairs=list(it.combinations(range(n),2));rows=[]
    for mask in range(1<<len(pairs)):
        es=[e for j,e in enumerate(pairs) if mask>>j&1];P=graph(n,es)
        merge=check_merge(A,P,0,(0,1));full=[t for t in it.product(COL,repeat=n) if P.accepts(t)]
        projected={tuple(int(c==2) for c in t) for t in full};simul=[]
        for z in it.product((0,1),repeat=n):
            fibers=[(2,) if bit else (0,1) for bit in z]
            w=binary_lift(P,fibers)
            A.check((w is not None)==(z in projected),'simultaneous_binary_fiber_exact')
            if w is not None:A.check(tuple(int(c==2) for c in w)==z,'simultaneous_witness_fiber')
            # Independent bipartition test for graph-only explanation.
            chosen={i for i,bit in enumerate(z) if bit};independent=all(not(u in chosen and v in chosen) for u,v in es)
            adj={i:[] for i in range(n) if i not in chosen}
            for u,v in es:
                if u in adj and v in adj:adj[u].append(v);adj[v].append(u)
            lab={};bipartite=True
            for r in adj:
                if r in lab:continue
                lab[r]=0;todo=[r]
                for u in todo:
                    for v in adj[u]:
                        if v not in lab:lab[v]=1-lab[u];todo.append(v)
                        elif lab[v]==lab[u]:bipartite=False
            A.check((z in projected)==(independent and bipartite),'independent_set_bipartite_identity')
            simul.append(int(w is not None))
        rows.append({'edge_mask':mask,'models':len(full),'single_merge':merge,'simultaneous_answers':simul})
    return {'n':n,'graphs':len(rows),'rows':rows}

def general_batch(A):
    rng=random.Random(SEED);rows=[]
    for n in range(2,7):
        for trial in range(45):
            rel={(u,v):rng.randrange(512) for u,v in it.combinations(range(n),2) if rng.random()<.55}
            P=CSP([7]*n,rel);x=rng.randrange(n);pair=tuple(rng.sample(COL,2))
            row=check_merge(A,P,x,pair);full=[t for t in it.product(COL,repeat=n) if P.accepts(t)]
            pairings=[tuple(rng.sample(COL,2)) for _ in range(n)]
            for z in it.product((0,1),repeat=n):
                fibers=[p if not bit else tuple(c for c in COL if c not in p) for p,bit in zip(pairings,z)]
                expected=any(all(t[v] in fibers[v] for v in range(n)) for t in full);w=binary_lift(P,fibers)
                A.check((w is not None)==expected,'general_relation_binary_fiber_exact')
            rows.append({'n':n,'trial':trial,'relations':[[u,v,m] for (u,v),m in rel.items()],**row})
    return {'seed':SEED,'instances':len(rows),'rows':rows}

def hardness_batch(A):
    rows=[]
    for n in range(1,5):
        pairs=list(it.combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            es=[e for j,e in enumerate(pairs) if mask>>j&1];G=graph(n,es)
            source=[t for t in it.product(COL,repeat=n) if G.accepts(t)]
            gadget=list(it.combinations(range(n,n+4),2));P=graph(n+4,es+gadget)
            M=compile_merge(P,n,(0,1));candidates=[]
            # Independent explicit quotient traversal; original UNSAT also checked separately.
            for t in it.product(*M.quotient_domains()):
                if M.naive(t):candidates.append(t)
            original_sat=any(P.accepts(t) for t in it.product(COL,repeat=n+4))
            A.check(not original_sat,'hardness_original_K4_rejects')
            A.check(bool(candidates)==bool(source),'hardness_quotient_equivalence')
            A.check(len(candidates)==6*len(source),'hardness_exact_count')
            A.check(all(not M.repaired(t) for t in candidates),'hardness_every_quotient_witness_spurious')
            rows.append({'n':n,'edge_mask':mask,'source_models':len(source),'quotient_models':len(candidates),
                         'first_spurious':candidates[0] if candidates else None})
    # Satisfiability preservation is strictly weaker than exact witness-image preservation.
    P=graph(3,[(0,1),(0,2)]);M=compile_merge(P,0,(0,1));bad=(MERGED,0,1)
    A.check(M.naive(bad) and not M.repaired(bad) and P.accepts((2,0,1)),'SAT_preservation_not_exact_image')
    # A safe but non-dominance merge: equality constraints on all three pairs.
    P=CSP([7]*3,{e:273 for e in it.combinations(range(3),2)});M=compile_merge(P,0,(0,1))
    A.check(not M.guards and all(M.lift(t) is not None for t in it.product(*M.quotient_domains()) if M.naive(t)), 'safe_contextual_representative')
    for args in [(P,-1,(0,1)),(P,0,(0,0)),(P,0,(0,4))]:
        try:compile_merge(*args)
        except ValueError:A.check(True,'malformed_merge_rejected')
        else:A.check(False,'malformed_merge_rejected')
    return {'source_graphs':len(rows),'rows':rows}

def integration_batch(A):
    import pin_core_audit as pc
    pc.require_dependency();rng=random.Random(SEED+1);rows=[]
    for n in range(1,5):
        pairs=list(it.combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            es=[e for j,e in enumerate(pairs) if mask>>j&1];R=pc.old.reduce_two_trees(n,es);h=R['universe']
            base=[t for t in it.product(COL,repeat=n) if graph(n,es).accepts(t)]
            patterns=[{}]
            if base:
                initial=pc.old.lift_source(R,base[0]);patterns.append({i:initial[i] for i in range(h) if rng.random()<.2})
            patterns += [{i:rng.randrange(3) for i in range(h) if rng.random()<.1} for _ in range(3)]
            details=[]
            for pins in patterns:
                lists,hubs=pc.compress(R,pins);K=bp.project(n,es,lists)
                if not all(hubs) or K.impossible or not K.boundary:continue
                where={v:i for i,v in enumerate(K.boundary)};domains=[7]*len(where);relations={}
                for u,a,v,b in K.forbidden:
                    i,j=where[u],where[v]
                    if i==j:domains[i]&=7^(1<<a)
                    else:relations[(i,j)]=relations.get((i,j),ALL)&(ALL^(1<<(3*a+b)))
                P=CSP(domains,relations);x=next((i for i,m in enumerate(domains) if m.bit_count()>=2),None)
                if x is None:continue
                pair=colors(domains[x])[:2];M=compile_merge(P,x,pair);lifts=0;bad=0
                for t in it.product(*M.quotient_domains()):
                    w=M.lift(t)
                    if M.naive(t) and w is None:bad+=1
                    if w is not None:
                        source=K.lift({v:w[i] for v,i in where.items()});target=pc.lift(R,pins,source,hubs)
                        A.check(pc.old.valid_target(R,target) and all(target[v]==c for v,c in pins.items()),'composed_original_target_witness')
                        lifts+=1
                details.append({'pins':pins,'boundary':K.boundary,'pivot':x,'pair':pair,'guards':M.guards,'lifts':lifts,'spurious':bad})
            rows.append({'n':n,'graph':mask,'cases':details})
    return {'graphs':len(rows),'rows':rows}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--batch',choices=['local','graphs','general','hardness','integration'],required=True)
    p.add_argument('--n',type=int,default=4);p.add_argument('--start',type=int,default=0);p.add_argument('--count',type=int,default=4096);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();A=Audit()
    if hashlib.sha256(Path(bp.__file__).read_bytes()).hexdigest()!=DEP:raise RuntimeError('dependency mismatch')
    result={'run_id':'MERGEGUARD1','status':'COMPUTATIONAL','batch':a.batch,'parameters':vars(a)|{'out':str(a.out)},'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'dependency_sha256':DEP,'timestamp_utc':datetime.now(timezone.utc).isoformat(),'failures':0}
    try:
        if a.batch=='local':result['data']=local_batch(A,a.start,a.count)
        elif a.batch=='graphs':result['data']=graphs_batch(A,a.n)
        elif a.batch=='general':result['data']=general_batch(A)
        elif a.batch=='hardness':result['data']=hardness_batch(A)
        else:result['data']=integration_batch(A)
    except Exception as exc:result['failures']=1;result['error']=repr(exc);raise
    finally:
        result.update(assertions=sum(A.counts.values()),counts=dict(A.counts),elapsed_seconds=time.monotonic()-A.start)
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('batch','assertions','failures','elapsed_seconds')}))
if __name__=='__main__':main()
