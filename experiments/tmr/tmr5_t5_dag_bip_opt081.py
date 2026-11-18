#!/usr/bin/env python3
"""Independent TMR-5/081: smallest unpinned DAG+bipartite C5-in-T5 edge gadget.
Fully enumerate ALL simple oriented sources on n<=5, <=4 distinct arcs,
with fixed ordered terminals 0,1; separately audit witnesses for three
known 4/5-arc edge gadgets. Python 3 standard library only.
"""
import itertools
import json
from collections import Counter

VERSION = 'tmr5-t5-dag-bip-opt081-v1'
MOD = 5
TARGET = frozenset((1,4))

def beat(a,b):
    return (b-a)%MOD in (1,3)

def bipartite(n, es):
    adj=[set() for _ in range(n)]
    for u,v in es:
        adj[u].add(v); adj[v].add(u)
    c=[-1]*n
    for root in range(n):
        if c[root]>=0:continue
        c[root]=0; todo=[root]
        while todo:
            u=todo.pop()
            for v in adj[u]:
                if c[v]<0:c[v]=1-c[u];todo.append(v)
                elif c[v]==c[u]:return False
    return True

def is_dag(n, es):
    ins=[0]*n
    out=[[] for _ in range(n)]
    for u,v in es:ins[v]+=1;out[u].append(v)
    todo=[x for x in range(n) if ins[x]==0]; i=0; removed=0
    while i<len(todo):
        u=todo[i];i+=1;removed+=1
        for v in out[u]:
            ins[v]-=1
            if ins[v]==0:todo.append(v)
    return removed==n

def count_for_endpoints(n, arcs, a, b):
    ans=0
    for tail in itertools.product(range(5),repeat=n-2):
        lab=(a,b)+tail
        if all(beat(lab[u],lab[v]) for u,v in arcs): ans+=1
    return ans

def relation(n,arcs):
    return tuple(d for d in range(5) if count_for_endpoints(n,arcs,0,d)>0)

def audit_gadget(tag,n,arcs,mult):
    assert is_dag(n,arcs)==mult['dag']
    assert bipartite(n,arcs)==mult['bip']
    assert len(arcs)==mult['m']
    counts=[[count_for_endpoints(n,arcs,a,b) for b in range(5)] for a in range(5)]
    for a in range(5):
        for b in range(5):
            assert counts[a][b]==(mult['ext'] if (b-a)%5 in TARGET else 0), (tag,a,b,counts[a][b])
    return {'name':tag, 'n':n, 'arcs':list(map(list,arcs)), 'dag':mult['dag'], 'underlying_bipartite':mult['bip'], 'endpoint_extension_count':mult['ext'], 'endpoint_pairs_checked':25}

def main():
    # For every simple oriented source with <=4 distinct arcs and <=5 vertices,
    # terminals are 0,1 by arbitrary renaming. Others unpinned.
    tally=Counter()
    supports=Counter()
    graph_checked=0
    witness_counts=0
    witnesses=[]
    cyclic_four_arc=[]
    for n in range(2,6):
        undir=list(itertools.combinations(range(n),2))
        for k in range(0,5):
            if k>len(undir):continue
            for picked in itertools.combinations(undir,k):
                if not bipartite(n,picked):
                    tally['underlying_nonbipartite']+=2**k
                    continue
                for choices in itertools.product((0,1),repeat=k):
                    arcs=tuple((v,u) if c else (u,v) for (u,v),c in zip(picked,choices))
                    if not is_dag(n,arcs):
                        tally['cyclic_orientations']+=1
                        if k==4 and set(relation(n,arcs))==TARGET:
                            cyclic_four_arc.append((n,arcs))
                        continue
                    graph_checked+=1
                    r=relation(n,arcs)
                    witness_counts+=5
                    supports[','.join(map(str,r))]+=1
                    if set(r)==TARGET:
                        witnesses.append({'n':n,'arcs':list(map(list,arcs))})
    assert witnesses==[], f'BAD lower bound: {witnesses[:4]}'
    assert len(cyclic_four_arc)==8, cyclic_four_arc
    assert all(n in (4,5) for n,arcs in cyclic_four_arc)
    gadgets=[
      audit_gadget('directed_4cycle_072',4,((0,2),(2,1),(1,3),(3,0)),{'dag':False,'bip':True,'m':4,'ext':2}),
      audit_gadget('directed_4arc_triangle_073',4,((0,2),(0,3),(3,2),(3,1)),{'dag':True,'bip':False,'m':4,'ext':1}),
      audit_gadget('dag_bipartite_5arc_080',5,((0,2),(2,3),(3,4),(0,4),(4,1)),{'dag':True,'bip':True,'m':5,'ext':1}),
    ]
    summary={'version':VERSION,'theorem':'No unpinned loopless simple oriented DAG with bipartite underlying graph and <=4 arcs pp-defines undirected C5 adjacency via two terminals. Five arcs suffice.',
      'enumeration':{'max_vertices':5,'max_arcs':4,'labelled_terminal_pair':[0,1], 'eligible_dag_bipartite_sources':graph_checked,'endpoint_differences_tested':witness_counts, 'pruning':dict(tally), 'relation_support_histogram':dict(sorted(supports.items())), 'false_counterexamples':len(witnesses),'non_DAG_four_arc_C5_realizations':len(cyclic_four_arc)},
      'gadget_audits':gadgets,'assertion_failures':0}
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=='__main__':main()
