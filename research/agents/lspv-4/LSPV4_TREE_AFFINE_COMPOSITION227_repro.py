#!/usr/bin/env python3
"""Dependency-free, auditable GF(2)^e / 2SAT and tree-interface experiment.

Core recursive solver specializes Brakensiek/Gopi/Guruswami 2019 Algorithm 5.2
for the additive group (F2)^e.  Its allowed syndrome set remains an affine
subspace; every failed first route that leads to a second route increases the
allowed-set dimension.  SCC normalization is charged explicitly.
"""
import collections
import itertools
import json
import math
import random
import sys
from pathlib import Path

RUN_ID = "TREE-AFFINE-COMPOSITION227"
SEED = 20261029

def evaluate(clauses, equations, assignment):
    return (all(any((assignment[abs(l)-1] == int(l > 0)) for l in clause) for clause in clauses)
            and all((sum(assignment[i] for i in support) & 1) == rhs for support, rhs in equations))

def brute(n, clauses, eqs):
    for bits in itertools.product((0,1), repeat=n):
        if evaluate(clauses, eqs, bits):
            return list(bits)
    return None

def reduce_basis(vectors):
    pivots = {}
    for v in vectors:
        w = v
        while w:
            p = w.bit_length()-1
            if p in pivots: w ^= pivots[p]
            else:
                pivots[p] = w
                break
    return tuple(pivots[p] for p in sorted(pivots, reverse=True))

def in_span(v, basis):
    w = v
    for a in basis:
        p = a.bit_length()-1
        if w & (1 << p): w ^= a
    return w == 0

class Syndrome:
    def __init__(self, offset, basis=()):
        self.offset = offset
        self.basis = reduce_basis(basis)
    def shift(self, v):
        return Syndrome(self.offset ^ v, self.basis)
    def expand(self, v):
        if in_span(v,self.basis): return self
        return Syndrome(self.offset, self.basis+(v,))
    def contains(self, v):
        return in_span(v^self.offset,self.basis)
    @property
    def dimension(self): return len(self.basis)

class Stats:
    def __init__(self):
        self.calls = self.fail_first = self.right_attempts = self.max_depth = 0
        self.sccs = self.graph_arcs = 0
    def to_json(self): return dict(self.__dict__)

def solve_xor2sat(n, clauses, equations, stats=None):
    """Return a model or None. clauses use signed 1-based vars, equations (support indices, rhs)."""
    if stats is None: stats = Stats()
    coeffs = [0]*n
    for row,(support,rhs) in enumerate(equations):
        for i in support:
            coeffs[i] ^= (1<<row)
    target = sum((rhs & 1)<<row for row,(_,rhs) in enumerate(equations))
    node = lambda lit: 2*(abs(lit)-1)+(1 if lit>0 else 0)
    arcs = [set() for _ in range(2*n)]
    for c in clauses:
        if len(c)==0: return None
        if len(c)>2: raise ValueError('width exceeds 2')
        if len(c)==1: a=b=c[0]
        else: a,b=c
        arcs[node(-a)].add(node(b))
        arcs[node(-b)].add(node(a))
    rev = [set() for _ in range(2*n)]
    for u,neighbors in enumerate(arcs):
        for v in neighbors: rev[v].add(u)
    visited=set(); order=[]
    for v in range(2*n):
        if v in visited: continue
        stack=[(v,False)]
        while stack:
            z,done=stack.pop()
            if done:
                order.append(z); continue
            if z in visited: continue
            visited.add(z); stack.append((z,True))
            stack.extend((w,False) for w in sorted(arcs[z]) if w not in visited)
    comp=[-1]*(2*n); members=[]
    for v in reversed(order):
        if comp[v]>=0: continue
        c=len(members); stack=[v]; comp[v]=c; mem=[]
        while stack:
            z=stack.pop(); mem.append(z)
            for w in rev[z]:
                if comp[w]<0: comp[w]=c; stack.append(w)
        members.append(mem)
    stats.sccs += len(members)
    if any(comp[2*i]==comp[2*i+1] for i in range(n)): return None
    complement={c:comp[members[c][0]^1] for c in range(len(members))}
    assert all(complement[complement[c]]==c for c in complement)
    cnode={}; count=0
    for c in range(len(members)):
        if c in cnode: continue
        other=complement[c]; cnode[c]=2*count+1; cnode[other]=2*count
        count+=1
    weights=[[0,0] for _ in range(count)]
    original=[]
    for i in range(n):
        v=cnode[comp[2*i+1]]; q=v//2; val=v&1
        weights[q][val] ^= coeffs[i]
        original.append((q,val))
    dag = [set() for _ in range(2*count)]; rdag=[set() for _ in range(2*count)]
    for u,vs in enumerate(arcs):
        for v in vs:
            p=cnode[comp[u]]; q=cnode[comp[v]]
            if p!=q: dag[p].add(q); rdag[q].add(p)
    stats.graph_arcs += sum(map(len,dag))
    initial = frozenset(range(2*count))
    def recurse(alive, allowed, depth):
        stats.calls+=1; stats.max_depth=max(stats.max_depth,depth)
        if not alive: return {} if allowed.contains(0) else None
        sinks=[y for y in sorted(alive) if not any(v in alive for v in dag[y])]
        assert sinks, 'quotient graph is not acyclic'
        y=sinks[0]; q=y//2; truevalue=y&1
        after_true=alive-{y,y^1}
        yes=recurse(after_true,allowed.shift(weights[q][truevalue]),depth+1)
        if yes is not None:
            yes[q]=truevalue
            return yes
        stats.fail_first+=1
        ancestors={y}; queue=[y]
        for z in queue:
            for p in rdag[z]:
                if p in alive and p not in ancestors:
                    ancestors.add(p); queue.append(p)
        complements={z^1 for z in ancestors}
        if ancestors & complements: return None
        fixed={}
        for z in ancestors:
            v=1-(z&1); qz=z//2
            if qz in fixed: assert fixed[qz]==v
            fixed[qz]=v
        fixed_delta=0
        for qz,v in fixed.items(): fixed_delta ^= weights[qz][v]
        s0=allowed.shift(fixed_delta)
        flip_delta=weights[q][truevalue]^weights[q][1-truevalue]
        s2=s0.expand(flip_delta)
        if s2.dimension==s0.dimension: return None
        stats.right_attempts+=1
        remaining=alive-ancestors-complements
        rest=recurse(remaining,s2,depth+1)
        if rest is None: return None
        remainder=0
        for qz,v in rest.items(): remainder ^= weights[qz][v]
        if s0.contains(remainder):
            fixed[q]=1-truevalue
        else:
            assert s0.shift(flip_delta).contains(remainder)
            fixed[q]=truevalue
        rest.update(fixed)
        return rest
    result=recurse(initial,Syndrome(target),0)
    if result is None: return None
    solution=[result[q] if val==1 else 1-result[q] for q,val in original]
    assert evaluate(clauses,equations,solution), 'reconstructed witness failed'
    return solution

def tree_validate(modules, parent):
    nt=len(modules)
    assert len(parent)==nt and parent[0]==-1
    assert all(0<=parent[i]<i for i in range(1,nt))
    adj=[set() for _ in range(nt)]
    for t in range(1,nt): adj[t].add(parent[t]);adj[parent[t]].add(t)
    universe=set().union(*(set(m['bag']) for m in modules))
    for m in modules:
        bag=set(m['bag'])
        for c in m['clauses']:
            assert all(abs(l)-1 in bag for l in c), 'constraint outside owner bag'
        for supp,rhs in m['equations']:
            assert set(supp)<=bag, 'affine constraint outside owner bag'
    for x in universe:
        holders={t for t,m in enumerate(modules) if x in m['bag']}
        discovered={min(holders)}; queue=list(discovered)
        for t in queue:
            for child in adj[t]&holders:
                if child not in discovered:
                    discovered.add(child);queue.append(child)
        if discovered!=holders:
            raise ValueError(f'REJECT running-intersection violation variable {x}')
    return True

def tree_solve(modules,parent,validate=True):
    if validate: tree_validate(modules,parent)
    n=max((x for m in modules for x in m['bag']),default=-1)+1
    occurrences=collections.Counter(x for m in modules for x in m['bag'])
    interfaces=[tuple(sorted(x for x in m['bag'] if occurrences[x]>1)) for m in modules]
    children=[[] for _ in modules]
    for i in range(1,len(modules)): children[parent[i]].append(i)
    lookup={}; rows={}; calls=0; peak_table_entries=0
    for t in reversed(range(len(modules))):
        interface=interfaces[t]; rows[t]={}
        for bits in itertools.product((0,1),repeat=len(interface)):
            choice=dict(zip(interface,bits))
            okay=True
            for child in children[t]:
                sep=tuple(sorted(set(modules[t]['bag'])&set(modules[child]['bag'])))
                key=tuple(choice[x] for x in sep)
                if key not in lookup[child]: okay=False;break
            if not okay: continue
            chosen_clauses=modules[t]['clauses']+[tuple((x+1) if v else -(x+1) for x,v in [(x,bit)]) for x,bit in choice.items()]
            witness=solve_xor2sat(n,chosen_clauses,modules[t]['equations'])
            calls+=1
            if witness is not None: rows[t][bits]=witness
        sep=tuple(sorted(set(modules[t]['bag'])&set(modules[parent[t]]['bag']))) if t else ()
        lookup[t]={}
        for bits in rows[t]:
            choice=dict(zip(interface,bits))
            k=tuple(choice[x] for x in sep)
            if k not in lookup[t]: lookup[t][k]=bits
        peak_table_entries=max(peak_table_entries,sum(map(len,rows.values())))
    if () not in lookup[0]: return None,{'local_calls':calls,'table_entries':sum(map(len,rows.values())),'peak_entries':peak_table_entries,'interfaces':list(map(len,interfaces))}
    if not validate:
        # Report only the unsafe Boolean table result, not a fabricated global witness.
        return ['SPURIOUS_LOCAL_SAT'],{'local_calls':calls,'table_entries':sum(map(len,rows.values())),'peak_entries':peak_table_entries,'interfaces':list(map(len,interfaces))}
    global_assignment={}
    def reconstruct(t,bits):
        witness=rows[t][bits]
        for x in modules[t]['bag']:
            if x in global_assignment: assert global_assignment[x]==witness[x]
            else:global_assignment[x]=witness[x]
        for child in children[t]:
            sep=tuple(sorted(set(modules[t]['bag'])&set(modules[child]['bag'])))
            childbits=lookup[child][tuple(global_assignment[x] for x in sep)]
            reconstruct(child,childbits)
    reconstruct(0,lookup[0][()])
    result=[global_assignment.get(i,0) for i in range(n)]
    for m in modules:
        assert evaluate(m['clauses'],m['equations'],result)
    return result,{'local_calls':calls,'table_entries':sum(map(len,rows.values())),'peak_entries':peak_table_entries,'interfaces':list(map(len,interfaces))}

def random_module(rng,bag,ntwo=3,nxor=2,planted=None):
    cl=[];eq=[]
    for _ in range(ntwo):
        sel=rng.sample(bag,rng.randrange(1,min(2,len(bag))+1))
        signs=[rng.choice([-1,1]) for x in sel]
        if planted is not None and not any(planted[x]==int(sign>0) for x,sign in zip(sel,signs)):
            signs[0]=1 if planted[sel[0]] else -1
        cl.append(tuple((x+1)*sign for x,sign in zip(sel,signs)))
    for _ in range(nxor):
        sel=tuple(sorted(rng.sample(bag,rng.randrange(1,len(bag)+1))))
        eq.append((sel,(sum(planted[x] for x in sel)&1) if planted is not None else rng.randrange(2)))
    return {'bag':tuple(bag),'clauses':cl,'equations':eq}

def strict22_six():
    n=6
    cls=[(i+1,((i+1)%n)+1,-(((i+2)%n)+1)) for i in range(n)]
    cls.extend([(-1,-2,-3),(-4,-5,-6)])
    return cls

def run():
    rng=random.Random(SEED)
    totals=collections.Counter(); max_scc=0; max_calls=0; max_right=0
    for n in range(1,9):
        for e in range(4):
            for rep in range(80):
                clauses=[]; equations=[]
                for _ in range(rng.randrange(0,3*n+1)):
                    size=rng.randrange(1,min(n,2)+1)
                    vs=rng.sample(range(1,n+1),size)
                    clauses.append(tuple(v*rng.choice((-1,1)) for v in vs))
                for _ in range(e):
                    k=rng.randrange(n+1)
                    support=tuple(sorted(rng.sample(range(n),k)))
                    equations.append((support,rng.randrange(2)))
                oracle=brute(n,clauses,equations)
                stats=Stats(); result=solve_xor2sat(n,clauses,equations,stats)
                assert (oracle is None)==(result is None),(n,e,clauses,equations,oracle,result)
                if result is not None: assert evaluate(clauses,equations,result)
                totals['local_cases']+=1
                totals['local_SAT' if oracle is not None else 'local_UNSAT']+=1
                max_scc=max(max_scc,stats.sccs)
                max_calls=max(max_calls,stats.calls)
                max_right=max(max_right,stats.right_attempts)
    tree_examples=[]
    for rep in range(300):
        planted=[rng.randrange(2) for _ in range(5)] if rep%2==0 else None
        modules=[random_module(rng,[0,1,2],planted=planted),
                 random_module(rng,[0,2,3],planted=planted),
                 random_module(rng,[0,3,4],planted=planted)]
        sol,ledger=tree_solve(modules,[-1,0,1])
        oracle=brute(5,[c for m in modules for c in m['clauses']],
                     [eq for m in modules for eq in m['equations']])
        assert (sol is None)==(oracle is None),(rep,modules,sol,oracle)
        totals['tree_cases']+=1
        totals['tree_SAT' if oracle is not None else 'tree_UNSAT']+=1
        if rep<6: tree_examples.append({'result':'SAT' if oracle is not None else 'UNSAT',**ledger})
    bad=[{'bag':(0,1),'clauses':[(1,)],'equations':[]},
         {'bag':(1,2),'clauses':[],'equations':[]},
         {'bag':(0,2),'clauses':[(-1,)],'equations':[]}]
    rejected=False
    try: tree_solve(bad,[-1,0,1],validate=True)
    except ValueError: rejected=True
    assert rejected
    unsafe,unsafeledger=tree_solve(bad,[-1,0,1],validate=False)
    assert unsafe is not None and brute(3,[(1,),(-1,)],[]) is None
    cls=strict22_six()
    counts=collections.Counter(l for clause in cls for l in clause)
    for i in range(1,7): assert counts[i]==counts[-i]==2
    neighbors={i:set() for i in range(1,7)}
    for c in cls:
        for x in c:
            for y in c:
                if abs(x)!=abs(y): neighbors[abs(x)].add(abs(y))
    assert all(len(ns)==4 for ns in neighbors.values())
    orig_sat=brute(6,cls,[])
    assert orig_sat is not None
    for value in (0,1):
        restricted=[]
        for c in cls:
            if any((abs(l)==1 and (l>0)==bool(value)) for l in c): continue
            restricted.append(tuple(l for l in c if abs(l)!=1))
        assert all(len(c)>=2 for c in restricted)
        assert len(set(abs(l) for c in restricted for l in c))==5
        totals['strict22_root_children']+=1
    assert 2*(6-1)**2>6**2
    output={
      'run_id':RUN_ID,'seed':SEED,
      'counts':dict(totals),
      'max_local_solver_calls':max_calls,'max_right_expansions':max_right,
      'max_scc_components_observed':max_scc,
      'tree_examples':tree_examples,
      'running_intersection_violation':{'correct_global':'UNSAT','unsafe_tree':'SAT','validated_tree':'REJECTED','unsafe_ledger':unsafeledger},
      'strict22_n6':{'n':6,'m':len(cls),'signed_occurrences':'2+2 per variable',
         'primal_minimum_degree':min(map(len,neighbors.values())),'forced_bag_lower_bound':5,
         'witness':orig_sat,'two_child_p2_mass':2*(6-1)**2,'root_p2_mass':6**2},
      'verification':'random mixed cases exhaustively compared; n6 graph is a symbolic min-degree/treewidth witness'
    }
    raw=Path(__file__).with_name('LSPV4_TREE_AFFINE_COMPOSITION227_raw.json')
    raw.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    print(json.dumps(output,indent=2,sort_keys=True))

if __name__=='__main__': run()
