#!/usr/bin/env python3
"""CORRELATIONELIM1. Exact correlation-preserving elimination and tree controls.
Python 3.10+, standard library only. Each audit batch has a 25-second cap.
Algorithms have no fixed size cap; exhaustive audits have explicit small bounds.
Examples:
 python correlation_elimination_audit.py --batch local --out local.json
 python correlation_elimination_audit.py --batch graphs --n 5 --out graphs5.json
 python correlation_elimination_audit.py --batch trees --max-height 8 --out trees.json
All operation counters describe this implementation, never all algorithms.
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
import time

COLORS = (0, 1, 2)
SEED = 202610140615  # No random sampling used by this program.

class Audit:
    def __init__(self):
        self.start = time.monotonic()
        self.counts = Counter()
    def check(self, condition, label):
        self.counts[label] += 1
        if not condition:
            raise AssertionError(label)
        if time.monotonic()-self.start > 25:
            raise TimeoutError('25-second audit cap; split the batch')

def validate_graph(n, edges):
    if type(n) is not int or n < 1:
        raise ValueError('positive explicit vertex count required')
    if any(type(e) is not tuple or len(e) != 2 for e in edges):
        raise ValueError('edge pairs required')
    if any(type(u) is not int or type(v) is not int or not 0 <= u < v < n for u,v in edges):
        raise ValueError('invalid endpoints or noncanonical simple edge')
    if len(set(edges)) != len(edges):
        raise ValueError('duplicate edge')

def is_coloring(c, edges):
    return all(x in COLORS for x in c) and all(c[u] != c[v] for u,v in edges)

@dataclass(frozen=True)
class Factor:
    scope: tuple[int, ...]
    allowed: frozenset[tuple[int, ...]]
    def accepts(self, assignment):
        return tuple(assignment[v] for v in self.scope) in self.allowed

@dataclass
class Step:
    variable: int
    boundary: tuple[int, ...]
    supports: dict[tuple[int, ...], int]
    tested: int

def graph_factors(n, edges):
    validate_graph(n, edges)
    return [Factor((u,v), frozenset((a,b) for a in COLORS for b in COLORS if a != b)) for u,v in edges]

def min_fill_order(n, edges):
    graph = [set() for _ in range(n)]
    for u,v in edges:
        graph[u].add(v); graph[v].add(u)
    remaining = set(range(n)); order=[]
    while remaining:
        def score(v):
            s=graph[v] & remaining
            return (sum(b not in graph[a] for a,b in it.combinations(s,2)), len(s), v)
        v=min(remaining,key=score); order.append(v)
        nbrs=graph[v] & remaining
        for a,b in it.combinations(nbrs,2):
            graph[a].add(b); graph[b].add(a)
        remaining.remove(v)
    return order

def eliminate(n, edges, order, check_state=None):
    """Exact tabular bucket elimination, all support masks retained for lifting.
    check_state, when supplied, is an audit callback, not part of the algorithm.
    """
    factors=graph_factors(n,edges)
    if len(order)!=n or set(order)!=set(range(n)) or any(type(v) is not int for v in order):
        raise ValueError('order must be a permutation')
    steps=[]; remaining=list(range(n)); metric=Counter()
    metric['initial_allowed_rows']=6*len(edges)
    for v in order:
        bucket=[f for f in factors if v in f.scope]
        factors=[f for f in factors if v not in f.scope]
        boundary=tuple(sorted(set().union(*(set(f.scope) for f in bucket))-{v})) if bucket else ()
        support={}; allowed=set(); tested=0
        for values in it.product(COLORS,repeat=len(boundary)):
            env=dict(zip(boundary,values)); mask=0
            for color in COLORS:
                env[v]=color; tested+=1
                # All factors in one bucket are tested on the SAME assignment.
                if all(f.accepts(env) for f in bucket):
                    mask |= 1 << color
            support[values]=mask
            if mask:
                allowed.add(values)
        factors.append(Factor(boundary,frozenset(allowed)))
        steps.append(Step(v,boundary,support,tested))
        remaining.remove(v)
        metric['candidate_tests']+=tested
        metric['retained_support_rows']+=len(support)
        metric['max_boundary']=max(metric['max_boundary'],len(boundary))
        metric['peak_active_allowed_rows']=max(metric['peak_active_allowed_rows'],sum(len(f.allowed) for f in factors))
        metric['peak_support_rows']=max(metric['peak_support_rows'],len(support))
        if check_state is not None:
            check_state(tuple(remaining),factors)
    sat=all(() in f.allowed for f in factors)
    witness=None
    if sat:
        env={}
        for step in reversed(steps):
            key=tuple(env[x] for x in step.boundary)
            mask=step.supports[key]
            if not mask:
                raise AssertionError('reverse support vanished')
            env[step.variable]=(mask & -mask).bit_length()-1
        witness=tuple(env[v] for v in range(n))
        if not is_coloring(witness,edges):
            raise AssertionError('lifted witness failed original graph')
    return sat,witness,dict(metric)

def star_rule(neighbors):
    """Nonempty missing-color set; evaluates with a three-bit occurrence mask."""
    seen=0
    for c in neighbors:
        if c not in COLORS:
            raise ValueError('color outside domain')
        seen |= 1 << c
    return seen != 7

def no_rainbow(a,b,c):
    return a==b or a==c or b==c

def mul4(a,b):
    # Independent four-element field, modulus X^2+X+1, elements 0..3.
    p=0
    while b:
        if b&1: p ^= a
        b >>= 1; a <<= 1
        if a&4: a ^= 7
    return p

def local_batch(A):
    star_rows=[]
    for d in range(0,9):
        count=0
        for colors in it.product(COLORS,repeat=d):
            extensions=[c for c in COLORS if all(c!=x for x in colors)]
            exact=star_rule(colors)
            triples=all(no_rainbow(*t) for t in it.combinations(colors,3))
            A.check(exact==bool(extensions)==triples,'star_exact_projection')
            if exact:
                c=next(x for x in COLORS if x not in colors)
                A.check(all(c!=x for x in colors),'star_reconstruction')
                count+=1
        expected=1 if d==0 else 3*(2**d)-3
        A.check(count==expected,'star_exact_count')
        star_rows.append({'degree':d,'accepted':count,'total':3**d,'orbit_count':1 if d==0 else 2**(d-1)})
    R3={t for t in it.product(COLORS,repeat=3) if no_rainbow(*t)}
    for omitted in range(3):
        A.check(len({t[:omitted]+t[omitted+1:] for t in R3})==9,'R3_pair_projection_full')
    for a,b,c in it.product((1,2,3),repeat=3):
        delta=mul4(mul4(a^b,a^c),b^c)
        A.check((delta==0)==no_rainbow(a,b,c),'F4_vandermonde_R3')
    R4=set(); forbidden=[]
    for a,b,c,d in it.product(COLORS,repeat=4):
        projected=any(no_rainbow(y,a,b) and y!=c and y!=d for y in COLORS)
        original=any(x!=a and x!=b and x!=y and y!=c and y!=d for x,y in it.product(COLORS,repeat=2))
        condition=not(a!=b and c!=d and {a,b}=={c,d})
        A.check(projected==original==condition,'double_star_exact_relation')
        if projected: R4.add((a,b,c,d))
        else: forbidden.append((a,b,c,d))
    A.check(len(R4)==69,'R4_69_of_81')
    for omitted in range(4):
        A.check(len({t[:omitted]+t[omitted+1:] for t in R4})==27,'R4_triple_projection_full')
    for n,answer in ((3,True),(4,False)):
        edges=list(it.combinations(range(n),2))
        got,w,stats=eliminate(n,edges,list(range(n)))
        A.check(got==answer,'K3_K4_exact_elimination')
    # Large formulas calculated symbolically, not represented as giant tables.
    for d in (16,32,64,128,1024):
        A.check(star_rule([0]*(d-1)+[1]),'large_compact_star_accept')
        A.check(not star_rule([0]*(d-2)+[1,2]),'large_compact_star_reject')
        star_rows.append({'degree':d,'accepted_formula':str(3*(2**d)-3),'orbit_count_formula':str(2**(d-1)),'compact_occurrence_mask_bits':3,'compact_input_reads':d})
    return {'stars':star_rows,'R3_allowed':len(R3),'R4_allowed':len(R4),'R4_forbidden':forbidden}

def graphs_batch(A,n):
    if not 1<=n<=5: raise ValueError('split exhaustive graph tests at n<=5')
    pairs=list(it.combinations(range(n),2)); records=[]
    for mask in range(1<<len(pairs)):
        edges=[e for j,e in enumerate(pairs) if (mask>>j)&1]
        oracle=[t for t in it.product(COLORS,repeat=n) if is_coloring(t,edges)]
        def compare(remaining,factors):
            expected={tuple(t[v] for v in remaining) for t in oracle}
            got=set()
            for values in it.product(COLORS,repeat=len(remaining)):
                env=dict(zip(remaining,values))
                if all(f.accepts(env) for f in factors): got.add(values)
            A.check(got==expected,'every_intermediate_exact_projection')
        row={'mask':mask,'models':len(oracle),'orders':[]}
        for name,order in [('natural',list(range(n))),('reverse',list(reversed(range(n)))),('min_fill',min_fill_order(n,edges))]:
            got,w,stats=eliminate(n,edges,order,compare)
            A.check(got==bool(oracle),'graph_exact_decision')
            A.check(w is None or w in oracle,'original_witness_reconstruction')
            if w is not None:
                # ROOTGLUE1 carrier: two triangle-cycle bits per source vertex.
                z=sum((c+1)<<(2*v) for v,c in enumerate(w))
                x=sum(7<<(3*j) for j in range(2*n) if (z>>j)&1)
                carrier_edges=[]
                for j in range(2*n):
                    carrier_edges.extend(((3*j,3*j+1),(3*j+1,3*j+2),(3*j,3*j+2)))
                carrier_edges.extend((3*j+1,3*(j+1)) for j in range(2*n-1))
                charges=[0]*(6*n)
                for i,(u,v) in enumerate(carrier_edges):
                    charges[u]^=(x>>i)&1; charges[v]^=(x>>i)&1
                projected=sum(((x>>(3*j+2))&1)<<j for j in range(2*n))
                A.check(not any(charges) and projected==z,'complete_Tseitin_witness_lift')
            row['orders'].append({'name':name,'order':order,'witness':w,'metrics':stats})
        records.append(row)
    return {'n':n,'graphs':len(records),'YES':sum(r['models']>0 for r in records),'NO':sum(r['models']==0 for r in records),'records':records}

def forcing_tree(height):
    """Two full binary forcing trees, roots joined and forced to color zero."""
    if type(height) is not int or height<0: raise ValueError('nonnegative height required')
    edges=[]; pins={}; next_id=0
    def make(h,color):
        nonlocal next_id
        v=next_id; next_id+=1
        if h==0: pins[v]=1<<color
        else:
            for child_color in COLORS:
                if child_color!=color:
                    u=make(h-1,child_color); edges.append(tuple(sorted((v,u))))
        return v
    r=make(height,0); s=make(height,0); edges.append(tuple(sorted((r,s))))
    return next_id,sorted(edges),pins

def orient_tree(n,edges):
    validate_graph(n,edges)
    if len(edges)!=n-1: raise ValueError('tree needs n-1 edges')
    adj=[[] for _ in range(n)]
    for u,v in edges: adj[u].append(v); adj[v].append(u)
    parent=[-2]*n; parent[0]=-1; order=[0]
    for v in order:
        for u in adj[v]:
            if u==parent[v]:continue
            if parent[u]!=-2:raise ValueError('cycle')
            parent[u]=v;order.append(u)
    if len(order)!=n:raise ValueError('disconnected')
    return parent,order

def tree_extend(n,edges,domains):
    parent,order=orient_tree(n,edges)
    for v,mask in domains.items():
        if type(v) is not int or not 0<=v<n or type(mask) is not int or not 0<=mask<8:
            raise ValueError('invalid domain')
    feasible=[domains.get(v,7) for v in range(n)]
    for v in reversed(order[1:]):
        # Child colors are nonempty and differ from parent color.
        m=feasible[v]
        support=sum((1<<c) for c in COLORS if m & (7 ^ (1<<c)))
        feasible[parent[v]] &= support
    if not feasible[0]:return None
    colors=[-1]*n
    colors[0]=(feasible[0]&-feasible[0]).bit_length()-1
    for v in order[1:]:
        m=feasible[v] & (7 ^ (1<<colors[parent[v]]))
        if not m:raise AssertionError('DP reconstruction failed')
        colors[v]=(m&-m).bit_length()-1
    return tuple(colors)

class TreeCircuit:
    """Quantifier-free Boolean DAG on three allowed-color bits per boundary.
    Every node is constant, input, two-input AND, or two-input OR.
    """
    def __init__(self,n,edges,boundary):
        parent,order=orient_tree(n,edges)
        boundary=set(boundary)
        if any(type(v) is not int or not 0<=v<n for v in boundary):raise ValueError('bad boundary')
        self.nodes=[('const',0),('const',1)]
        self.inputs={}
        def inp(v,c):
            k=len(self.nodes);self.nodes.append(('input',v,c));self.inputs[(v,c)]=k;return k
        def gate(op,a,b):
            if a==b:return a
            if op=='and':
                if a==0 or b==0:return 0
                if a==1:return b
                if b==1:return a
            if op=='or':
                if a==1 or b==1:return 1
                if a==0:return b
                if b==0:return a
            k=len(self.nodes);self.nodes.append((op,a,b));return k
        feasible=[[inp(v,c) if v in boundary else 1 for c in COLORS] for v in range(n)]
        for v in reversed(order[1:]):
            for c in COLORS:
                other=[a for a in COLORS if a!=c]
                support=gate('or',feasible[v][other[0]],feasible[v][other[1]])
                p=parent[v];feasible[p][c]=gate('and',feasible[p][c],support)
        self.output=gate('or',gate('or',feasible[0][0],feasible[0][1]),feasible[0][2])
    def evaluate(self,domains):
        values=[]
        for node in self.nodes:
            if node[0]=='const':v=bool(node[1])
            elif node[0]=='input':v=bool(domains.get(node[1],7)&(1<<node[2]))
            elif node[0]=='and':v=values[node[1]] and values[node[2]]
            elif node[0]=='or':v=values[node[1]] or values[node[2]]
            else:raise AssertionError('invalid gate')
            values.append(v)
        return values[self.output]
    @property
    def gate_count(self):return sum(t[0] in ('and','or') for t in self.nodes)

def tree_all_colorings(n,edges):
    """Exhaustive audit oracle only, not part of the linear algorithm."""
    parent,order=orient_tree(n,edges);c=[-1]*n
    def visit(i):
        if i==n:yield tuple(c);return
        v=order[i]
        for a in COLORS:
            if parent[v]<0 or a!=c[parent[v]]:
                c[v]=a;yield from visit(i+1)
    yield from visit(0)

def trees_batch(A,max_height):
    if not 0<=max_height<=8:raise ValueError('checkpoint heights above 8')
    rows=[]
    for h in range(max_height+1):
        n,edges,pins=forcing_tree(h);boundary=sorted(pins);b=len(boundary)
        C=TreeCircuit(n,edges,boundary)
        A.check(n==2*b-2 and b==2**(h+1),'forcing_tree_size')
        A.check(tree_extend(n,edges,pins) is None,'full_boundary_obstruction')
        A.check(not C.evaluate(pins),'circuit_rejects_obstruction')
        A.check(C.gate_count<=6*(n-1)+2,'linear_gate_budget')
        restored=[]
        for removed in boundary:
            partial=dict(pins);del partial[removed]
            witness=tree_extend(n,edges,partial)
            A.check(witness is not None,'each_proper_projection_extends')
            A.check(is_coloring(witness,edges) and all(m&(1<<witness[v]) for v,m in partial.items()),'partial_pin_original_witness')
            A.check(C.evaluate(partial),'circuit_accepts_relaxed_boundary')
            restored.append(witness[removed])
        exact_count=None
        if h<=2:
            oracle={tuple(c[v] for v in boundary) for c in tree_all_colorings(n,edges)}
            exact_count=len(oracle)
            A.check(exact_count == 3**b-3*2**(b-2),'trivalent_exact_count')
            for omitted in range(b):
                projected={t[:omitted]+t[omitted+1:] for t in oracle}
                A.check(len(projected)==3**(b-1),'all_proper_boundary_projections_full')
            for colors in it.product(COLORS,repeat=b):
                domains={v:1<<c for v,c in zip(boundary,colors)}
                w=tree_extend(n,edges,domains)
                answer=colors in oracle
                A.check((w is not None)==answer==C.evaluate(domains),'full_boundary_truth_table_vs_bruteforce')
                A.check(w is None or is_coloring(w,edges),'full_boundary_witness_check')
        rows.append({'height':h,'vertices':n,'edges':len(edges),'boundary':boundary,'pin_masks':[pins[v] for v in boundary],'restored_colors':restored,'input_nodes':len(C.inputs),'boolean_gates':C.gate_count,'all_nodes':len(C.nodes),'truth_table_rows':3**b,'extendable_boundary_count_if_exhaustive':exact_count})
    for b in (3,5,6,7,9,10,17,33,65):
        n=2; edges=[(0,1)]
        for _ in range(b-2):
            u=next(v if a==0 else a for a,v in edges if a==0 or v==0)
            edges.remove(tuple(sorted((0,u))))
            edges.extend([tuple(sorted((0,n))),tuple(sorted((u,n))),(n,n+1)])
            n+=2
        edges=sorted(edges)
        parent,order=orient_tree(n,edges)
        children=[[] for _ in range(n)]
        for v in order[1:]:children[parent[v]].append(v)
        pins={0:1}; desired={children[0][0]:0}
        for v in order[1:]:
            color=desired[v]
            if not children[v]:pins[v]=1<<color
            else:
                others=[c for c in COLORS if c!=color]
                for u,c in zip(children[v],others):desired[u]=c
        C=TreeCircuit(n,edges,pins)
        A.check(len(pins)==b and n==2*b-2,'arbitrary_boundary_tree_size')
        A.check(tree_extend(n,edges,pins) is None and not C.evaluate(pins),'arbitrary_boundary_obstruction')
        for removed in pins:
            partial={v:m for v,m in pins.items() if v!=removed}
            w=tree_extend(n,edges,partial)
            A.check(w is not None and is_coloring(w,edges) and all(m&(1<<w[v]) for v,m in partial.items()),'arbitrary_boundary_relaxed_witness')
            A.check(C.evaluate(partial),'arbitrary_boundary_relaxed_circuit')
        A.check(C.gate_count<=6*(n-1)+2,'arbitrary_boundary_linear_gates')
        rows.append({'height':None,'shape':'caterpillar','vertices':n,'boundary':sorted(pins),'pin_masks':[pins[v] for v in sorted(pins)],'boolean_gates':C.gate_count,'all_nodes':len(C.nodes),'input_nodes':len(C.inputs),'truth_table_rows':3**b})
    for n,edges in [(3,[(0,1),(0,1)]),(3,[(0,1)]),(3,[(0,1),(1,3)])]:
        try:tree_extend(n,edges,{})
        except ValueError:A.check(True,'malformed_tree_rejected')
        else:A.check(False,'malformed_tree_rejected')
    return {'trees':rows,'max_height':max_height}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--batch',choices=['local','graphs','trees'],required=True)
    p.add_argument('--n',type=int,default=4)
    p.add_argument('--max-height',type=int,default=8)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();A=Audit()
    result={'run_id':'CORRELATIONELIM1','status':'COMPUTATIONAL','batch':args.batch,'seed':SEED,'randomness':'none','timestamp_utc':datetime.now(timezone.utc).isoformat(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'failures':0}
    try:
        if args.batch=='local':result['data']=local_batch(A)
        elif args.batch=='graphs':result['data']=graphs_batch(A,args.n)
        else:result['data']=trees_batch(A,args.max_height)
    except Exception as exc:
        result['failures']=1;result['error']=repr(exc);raise
    finally:
        result['assertions']=sum(A.counts.values());result['counts']=dict(A.counts)
        result['elapsed_seconds']=time.monotonic()-A.start
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('batch','assertions','failures','elapsed_seconds')}))

if __name__=='__main__':main()
