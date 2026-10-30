#!/usr/bin/env python3
"""Weighted exact-SAT-summary scheduling: reproducible restricted theorem/control.

Measured memory is LOGICAL explicit table bits, not Python heap usage.  All source
clauses, indices and output/certificate costs are separately accounted for.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from collections import Counter
import itertools, json, random, hashlib, math, sys

sys.setrecursionlimit(10000)
SEED=1701029
PREFIX='2026-10-29_1724_WEIGHTED_SUMMARY_SCHEDULER170'
HERE=Path(__file__).resolve().parent

@dataclass
class Node:
    s:int
    kids:list['Node']=field(default_factory=list)
    scratch:int=0
    idx:int=-1
    own:tuple[int,...]=()
    bag:tuple[int,...]=()
    clauses:list[tuple[int,...]]=field(default_factory=list)


def count(t):return 1+sum(count(c) for c in t.kids)


def pad_chain(length:int,B:int)->Node:
    assert length>=1 and B>=2 and B&(B-1)==0
    x=Node(s=2)
    for i in range(1,length):x=Node(s=B if i==length-1 else 2,kids=[x])
    if length==1:x.s=B
    return x


def family(h:int,B:int)->Node:
    assert h>=0
    if h==0:return Node(s=2)
    right=family(h-1,B)
    left=pad_chain(count(right),B)
    return Node(s=2,kids=[left,right])


def walk_pre(t:Node):
    yield t
    for c in t.kids:yield from walk_pre(c)


def assign_ids(t:Node):
    for i,v in enumerate(walk_pre(t)):v.idx=i


def data(t:Node):
    if not t.kids:return (t.s,t.s,1,())
    child=[data(c) for c in t.kids]
    num=1+sum(x[2] for x in child)
    M=[]
    if len(child)==1:
        a=child[0]
        return (t.s,max(a[1],a[0]+t.s+t.scratch),num,(0,))
    A,B=child
    ab=max(A[1],A[0]+B[1],A[0]+B[0]+t.s+t.scratch)
    ba=max(B[1],B[0]+A[1],A[0]+B[0]+t.s+t.scratch)
    # More surplus M-s first. At ties either order is optimal.
    order=(0,1) if A[1]-A[0]>=B[1]-B[0] else (1,0)
    assert min(ab,ba)==(ab if order==(0,1) else ba)
    return (t.s,min(ab,ba),num,order)


def order(t:Node, policy:str):
    if len(t.kids)<2:return tuple(range(len(t.kids)))
    if policy=='left':return (0,1)
    if policy=='heavy_count':return (0,1) if count(t.kids[0])>=count(t.kids[1]) else (1,0)
    if policy=='weighted':return data(t)[3]
    raise ValueError(policy)


def theoretical_peak(t:Node,policy:str):
    if not t.kids:return t.s
    peak=[theoretical_peak(c,policy) for c in t.kids]
    if len(t.kids)==1:return max(peak[0],t.kids[0].s+t.s+t.scratch)
    i,j=order(t,policy)
    return max(peak[i],t.kids[i].s+peak[j],sum(c.s for c in t.kids)+t.s+t.scratch)


def brute_min(t:Node):
    if not t.kids:return t.s
    a=[brute_min(c) for c in t.kids]
    if len(t.kids)==1:return max(a[0],t.kids[0].s+t.s+t.scratch)
    x,y=t.kids
    j=x.s+y.s+t.s+t.scratch
    return min(max(a[0],x.s+a[1],j),max(a[1],y.s+a[0],j))


def oracle_all_binary_orders(t:Node):
    # Independent search over all local child orders, no recurrence minimization.
    nodes=[v for v in walk_pre(t) if len(v.kids)==2]
    indices={id(v):i for i,v in enumerate(nodes)}
    if len(nodes)>15:return None
    def evaluate(v,bits):
        if not v.kids:return v.s
        child=[evaluate(x,bits) for x in v.kids]
        if len(v.kids)==1:return max(child[0],v.kids[0].s+v.s+v.scratch)
        b=(bits>>indices[id(v)])&1
        i,j=((0,1) if not b else (1,0))
        return max(child[i],v.kids[i].s+child[j],v.kids[0].s+v.kids[1].s+v.s+v.scratch)
    return min(evaluate(t,bits) for bits in range(1<<len(nodes)))


def make_cnf(t:Node,unsat:bool):
    assign_ids(t)
    nodes=list(walk_pre(t))
    nextvar=1
    for v in nodes:
        width=(v.s.bit_length()-1)
        assert (1<<width)==v.s
        v.own=tuple(range(nextvar,nextvar+width));nextvar+=width
    for v in nodes:
        v.bag=tuple(sorted(set(v.own).union(*(c.own for c in v.kids))))
        v.clauses=[(a,) for a in v.own]
        if v.own:
            for c in v.kids:
                for childvar in c.own:v.clauses.append((v.own[0],childvar))
    if unsat:t.clauses.append((-t.own[0],))
    allclauses=[(v.idx,c) for v in nodes for c in v.clauses]
    # validate ownership and running intersection
    for v in nodes:
        assert all(set(abs(x) for x in c).issubset(set(v.bag)) for c in v.clauses)
        assert all(len(set(abs(x) for x in c))==len(c) for c in v.clauses)
    for x in range(1,nextvar):
        positions=[v.idx for v in nodes if x in v.bag]
        assert len(positions)<=2
        if len(positions)==2:
            owners=[v for v in nodes if x in v.own];assert len(owners)==1
            assert positions==sorted([owners[0].idx,next(v.idx for v in nodes if owners[0] in v.kids)])
    # Check incidence connectivity on the simple positive clauses.
    graph={i:set() for i in range(1,nextvar)}
    for _,cl in allclauses:
        for x in cl:
            for y in cl:
                graph[abs(x)].add(abs(y))
    seen=set();stack=[1]
    while stack:
        v=stack.pop()
        if v in seen:continue
        seen.add(v);stack.extend(graph[v]-seen)
    assert len(seen)==nextvar-1
    return nodes,allclauses,nextvar-1


def evaluate_tables(t:Node,policy:str,stats:Counter):
    live=0;peak=0
    def summary(v:Node):
        nonlocal live,peak
        tables={}
        for i in order(v,policy):
            c=v.kids[i]
            tables[c.idx]=summary(c)
        # Explicit parent output table allocation while child tables remain live.
        live+=v.s+v.scratch
        peak=max(peak,live)
        entrymask=0
        for bits in range(1<<len(v.bag)):
            vals={x:bool((bits>>i)&1) for i,x in enumerate(v.bag)}
            stats['bag_candidates']+=1
            good=True
            for cl in v.clauses:
                stats['source_clause_checks']+=1
                if not any(vals[abs(a)]==(a>0) for a in cl):good=False;break
            if not good:continue
            for c in v.kids:
                idx=sum(int(vals[x])<<i for i,x in enumerate(c.own))
                stats['child_lookups']+=1
                if not (tables[c.idx]>>idx)&1:good=False;break
            if not good:continue
            idx=sum(int(vals[x])<<i for i,x in enumerate(v.own))
            entrymask|=(1<<idx)
        for c in v.kids:live-=c.s
        live-=v.scratch
        stats['table_bits_emitted']+=v.s
        stats['tables_constructed']+=1
        assert live>=0
        return entrymask
    result=summary(t)
    assert live==t.s
    stats['abstract_peak_table_bits']=peak
    return result


def recompute_witness(t:Node,policy:str,stats:Counter):
    # The construction's unit clauses make each true port assignment all-ones.
    # Recompute authenticated child relations while following a chosen root port.
    assignments={}
    def recurse(v:Node,req:tuple[bool,...]):
        child_tables={}
        for c in v.kids:
            child_tables[c.idx]=evaluate_tables(c,policy,stats)
            stats['reconstruction_subtree_replays']+=1
        for bits in range(1<<len(v.bag)):
            stats['reconstruction_candidate_checks']+=1
            vals={x:bool((bits>>j)&1) for j,x in enumerate(v.bag)}
            if tuple(vals[x] for x in v.own)!=req:continue
            if any(not any(vals[abs(a)]==(a>0) for a in cl) for cl in v.clauses):continue
            good=True
            for c in v.kids:
                idx=sum(int(vals[x])<<j for j,x in enumerate(c.own))
                if not (child_tables[c.idx]>>idx)&1:good=False;break
            if not good:continue
            assignments.update({x:vals[x] for x in v.own})
            for c in v.kids:recurse(c,tuple(vals[x] for x in c.own))
            return
        raise AssertionError('no witness reconstruction')
    root_table=evaluate_tables(t,policy,stats)
    first=next((i for i in range(t.s) if ((root_table>>i)&1)),None)
    if first is None:return None
    recurse(t,tuple(bool((first>>i)&1) for i in range(len(t.own))))
    assert len(assignments)==sum(len(v.own) for v in walk_pre(t))
    return assignments


def run():
    rng=random.Random(SEED)
    output={'seed':SEED,'status':{'weighted_tree_lemma':'exact within no-recomputation depth-first whole-subtree schedules',
              'general_sat':'OPEN','memory_units':'abstract explicit table bits, not Python heap'},
            'random_oracle':{},'h_family':[],'connected_source_cnf':[],'counterexamples':[]}
    trials=500;oracle_tests=0;strict=0
    for j in range(trials):
        # arbitrary small unary/binary tree with nonuniform output size
        ts=[Node(s=1<<rng.randrange(0,7),scratch=rng.randrange(0,4)) for i in range(rng.randrange(2,9))]
        while len(ts)>1:
            i=rng.randrange(len(ts));a=ts.pop(i)
            if ts and rng.random()<0.7:
                k=rng.randrange(len(ts));b=ts.pop(k)
                ts.append(Node(s=1<<rng.randrange(0,7),kids=[a,b],scratch=rng.randrange(0,4)))
            else:ts.append(Node(s=1<<rng.randrange(0,7),kids=[a],scratch=rng.randrange(0,4)))
        root=ts[0];opt=data(root)[1]
        assert opt==brute_min(root)
        oracle=oracle_all_binary_orders(root)
        if oracle is not None:assert oracle==opt;oracle_tests+=1
        assert theoretical_peak(root,'weighted')==opt
        if theoretical_peak(root,'left')>opt:strict+=1
    output['random_oracle']={'trees':trials,'exhaustive_schedule_checks':oracle_tests,'left_worse_than_optimum':strict,'mismatches':0}
    for h in range(1,10):
        m=(1<<(h+1))-1
        for B in (4,16,256,1<<(2*(h+1))):
            root=family(h,B)
            assert count(root)==m
            weighted=data(root)[1]
            naive=theoretical_peak(root,'heavy_count')
            predicted=(B+4,h*B+4)
            assert (weighted,naive)==predicted,(h,B,weighted,naive,predicted)
            assert theoretical_peak(root,'left')==naive
            output['h_family'].append({'h':h,'m':m,'B':B,'w':B.bit_length()-1,'optimal_table_bits':weighted,
                                       'nodecount_heavy_table_bits':naive,'ratio':round(naive/weighted,9),
                                       'state_discovery_metadata_upper_bits':4*m*math.ceil(math.log2((m+2)*(B+2)))} )
    for h in (1,2,3):
        for w in (2,3,4):
            for unsat in (False,True):
                root=family(h,1<<w)
                nodes,source,nvars=make_cnf(root,unsat)
                stats1=Counter();stats2=Counter()
                a=evaluate_tables(root,'weighted',stats1)
                b=evaluate_tables(root,'heavy_count',stats2)
                assert a==b
                assert (a==0)==unsat
                assert stats1['abstract_peak_table_bits']==data(root)[1]
                assert stats2['abstract_peak_table_bits']==theoretical_peak(root,'heavy_count')
                if not unsat:
                    rc=Counter();assignment=recompute_witness(root,'weighted',rc)
                    assert assignment and all(any(assignment[abs(l)]==(l>0) for l in cl) for _,cl in source)
                else:rc=Counter();assignment=None
                # Independent simple-unit implication oracle valid for THIS source grammar.
                units={}; conflict=False
                for _,cl in source:
                    if len(cl)==1:
                        x=abs(cl[0]); val=cl[0]>0
                        if x in units and units[x]!=val:conflict=True
                        units[x]=val
                assert conflict==unsat
                output['connected_source_cnf'].append({'h':h,'m':count(root),'w':w,'SAT':not unsat,
                  'variables':nvars,'source_clauses':len(source),'max_bag':max(len(v.bag) for v in nodes),
                  'weighted_peak_table_bits':stats1['abstract_peak_table_bits'],
                  'nodecount_peak_table_bits':stats2['abstract_peak_table_bits'],
                  'bag_assignments_weighted':stats1['bag_candidates'],
                  'bag_assignments_nodecount':stats2['bag_candidates'],
                  'child_lookups':stats1['child_lookups'],
                  'reconstruction_replays':rc['reconstruction_subtree_replays'],
                  'reconstruction_bag_checks':rc['reconstruction_candidate_checks'],
                  'unit_consistency_oracle':not conflict})
    output['counterexamples']=[
       {'claim':'subtree-node-count heavy-first is optimal for nonuniform table bit sizes','status':'FALSIFIED',
        'first_strict_h':2,'first_strict_m':7,'theoretical_family':'M_heavy=h B+4; M_weighted=B+4, B>=2'},
       {'claim':'small bit-length of rank implies polynomial-value rank','status':'FALSIFIED (prior ARC/RANK_SWITCH168)',
        'detail':'2^n remaining steps have n+1-bit encoding but exponentially large numerical value'}]
    raw=json.dumps(output,sort_keys=True,indent=2)+'\n'
    dest=HERE/(PREFIX+'_raw.json');dest.write_text(raw)
    print(json.dumps({'file':str(dest),'sha256':hashlib.sha256(raw.encode()).hexdigest(),
      'oracle_trees':trials,'h_rows':len(output['h_family']),
      'source_cnf_cases':len(output['connected_source_cnf']),'random_strict_cases':strict,
      'max_source_vars':max(r['variables'] for r in output['connected_source_cnf'])},indent=2))

if __name__=='__main__':run()