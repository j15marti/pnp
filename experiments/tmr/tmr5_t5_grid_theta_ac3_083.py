#!/usr/bin/env python3
"""TMR-5/083: identical underlying bounded-degree high-treewidth T5 DAGs,
exact counts 5 vs 0, and generic one-variable AC-3 propagation.
Every numerical result is independently recomputed from actual input arcs.
"""
from collections import Counter,deque
import json,hashlib
S=(1,3)
def R(a,b):return ((b-a)%5) in S

def module_witness(reverse=False):
    # external endpoints u,v, internals a,b
    e=[('u','a'),('a','b'),('b','v'),('u','v')]
    if reverse:e=[(v,u) for u,v in e]
    table={}
    for u in range(5):
        for v in range(5):
            choices=[(a,b) for a in range(5) for b in range(5)
                if all(R(dict(u=u,v=v,a=a,b=b)[x],dict(u=u,v=v,a=a,b=b)[y]) for x,y in e)]
            assert len(choices)==(1 if (v-u)%5==(2 if reverse else 3) else 0)
            table[(u,v)]=choices
    return table

def make_grid_theta(L,h,kind):
    assert L>=2 and h>=5 and kind in ('YES','NO')
    s=('grid',0,0);t=('t',)
    base=set([('grid',i,j) for i in range(L) for j in range(L)]+[t]);macro=[]
    for i in range(L):
        for j in range(L):
            v=('grid',i,j)
            if i+1<L:macro.append((v,('grid',i+1,j),False))
            if j+1<L:macro.append((v,('grid',i,j+1),False))
    cycle_nodes=set((s,t))
    for k in range(2):
        path=[s]+[('path',k,z) for z in range(1,h)]+[t]
        cycle_nodes.update(path)
        base.update(path)
        for step,(u,v) in enumerate(zip(path[:-1],path[1:]),start=1):
            reverse=(step==2) if kind=='YES' else (k==1 and step in (2,4))
            macro.append((u,v,reverse))
    vertices=set(base);arcs=[]
    for j,(u,v,reverse) in enumerate(macro):
        a=('a',j);b=('b',j);vertices.update([a,b])
        pattern=[(u,a),(a,b),(b,v),(u,v)]
        if reverse:pattern=[(y,x) for x,y in pattern]
        arcs.extend(pattern)
    assert len(macro)==2*L*(L-1)+2*h
    assert len(base)==L*L+2*h-1
    assert len(vertices)==5*L*L-4*L+6*h-1
    assert len(arcs)==8*L*(L-1)+8*h
    return vertices,arcs,base,macro,cycle_nodes

def graph_stats(vertices,arcs):
    indeg=Counter(v for _,v in arcs);outdeg=Counter(u for u,_ in arcs)
    values=Counter((indeg[v],outdeg[v]) for v in vertices)
    max_degree=max(indeg[v]+outdeg[v] for v in vertices)
    # raw bipartiteness, no special graph libraries
    neighbors={v:set() for v in vertices}
    for u,v in arcs:
        neighbors[u].add(v);neighbors[v].add(u)
    parts={}
    for root in vertices:
        if root in parts:continue
        parts[root]=0;q=deque([root])
        while q:
            v=q.popleft()
            for w in neighbors[v]:
                if w in parts:
                    assert parts[w]!=parts[v]
                else:parts[w]=1-parts[v];q.append(w)
    assert len(set(parts.values()))==2
    # Directed acyclicity
    deg={v:indeg[v] for v in vertices}
    out={v:[] for v in vertices}
    for u,v in arcs:out[u].append(v)
    q=deque([v for v in vertices if deg[v]==0]);seen=0
    while q:
        u=q.popleft();seen+=1
        for v in out[u]:
            deg[v]-=1
            if deg[v]==0:q.append(v)
    assert seen==len(vertices)
    return {"indeg_outdeg":sorted((list(k),n) for k,n in values.items()),"max_degree":max_degree,"undirected_edges":set(frozenset((u,v)) for u,v in arcs)}

def linear_solve(base,macro):
    neighbors={v:[] for v in base}
    for u,v,rev in macro:
        diff=2 if rev else 3
        neighbors[u].append((v,diff));neighbors[v].append((u,-diff))
    x={};count_components=0
    for root in base:
        if root in x:continue
        count_components+=1;x[root]=0
        q=[root]
        while q:
            u=q.pop()
            for v,diff in neighbors[u]:
                new=(x[u]+diff)%5
                if v in x:
                    if x[v]!=new:return 0,None
                else:x[v]=new;q.append(v)
    return 5**count_components,x

def ac3(vertices,arcs,pin):
    # generic T5 binary CSP engine, no knowledge of modules, grid, theta or labels
    ordered=sorted(vertices)
    adj={v:[] for v in ordered}
    for u,v in arcs:
        adj[u].append((v,1));adj[v].append((u,-1))
    for v in ordered:adj[v].sort()
    dom={v:set(range(5)) for v in ordered}
    dom[pin]={0}
    q=deque((u,v,d) for u in ordered for v,d in adj[u]);revisions=0
    while q:
        u,v,d=q.popleft();revisions+=1
        prune={a for a in dom[u] if not any((R(a,b) if d==1 else R(b,a)) for b in dom[v])}
        if prune:
            dom[u]-=prune
            if not dom[u]:return False,revisions,False
            for w,back_sign in adj[u]:
                if w!=v:q.append((w,u,-back_sign))
    singleton=all(len(s)==1 for s in dom.values())
    if singleton:
        assert all(R(next(iter(dom[u])),next(iter(dom[v]))) for u,v in arcs)
    return True,revisions,singleton


def raw_csp_backtrack_count(vertices,arcs):
    """Complete generic binary CSP solver, independent of rigid-module algebra."""
    vs=sorted(vertices)
    adj={v:[] for v in vs}
    for u,v in arcs:
        adj[u].append((v,1));adj[v].append((u,-1))
    for v in vs:adj[v].sort()
    nodes=[0]
    def propagate(dom):
        queue=deque((u,v,sgn) for u in vs for v,sgn in adj[u])
        while queue:
            u,v,sgn=queue.popleft()
            bad={a for a in dom[u] if not any(R(a,b) if sgn==1 else R(b,a) for b in dom[v])}
            if bad:
                dom[u].difference_update(bad)
                if not dom[u]:return False
                for w,back in adj[u]:
                    if w!=v:queue.append((w,u,-back))
        return True
    def search(dom):
        nodes[0]+=1
        if not propagate(dom):return 0
        todo=[v for v in vs if len(dom[v])>1]
        if not todo:return 1
        v=min(todo,key=lambda w:len(dom[w]))
        count=0
        for a in sorted(dom[v]):
            dd={w:set(d) for w,d in dom.items()}
            dd[v]={a}
            count+=search(dd)
        return count
    return search({v:set(range(5)) for v in vs}),nodes[0]

def deletion_controls(L,h):
    vertices,arcs,base,macro,cycle_nodes=make_grid_theta(L,h,'NO')
    checked=0
    for v in cycle_nodes:
        induced=[(u,w) for u,w in arcs if u!=v and w!=v]
        other=vertices-{v}
        # Independent generic full CSP AC-3/backtracking, no gadget awareness.
        total,nodes=raw_csp_backtrack_count(other,induced)
        assert total>0,(L,h,v,total,nodes)
        checked+=1
    return checked

def run():
    module_witness(False);module_witness(True)
    # Independent ordinary AC3 propagation from each of the four gadget positions.
    standalone={"u","a","b","v"}
    for rev in (False,True):
        module=[("u","a"),("a","b"),("b","v"),("u","v")]
        if rev:module=[(v,u) for u,v in module]
        for pin in standalone:
            ok,_,single=ac3(standalone,module,pin)
            assert ok and single,(rev,pin)
    result={"module_endpoint_pairs":50,"singleton_module_anchor_controls":8,"pairs":[],"deletion_controls":0}
    for L,h in [(3,5),(4,5),(5,5),(6,6),(7,7),(9,9),(12,12)]:
        pair={}
        for k in ('YES','NO'):
            vertices,arcs,base,macro,cycle_nodes=make_grid_theta(L,h,k)
            stats=graph_stats(vertices,arcs)
            answer,assignment=linear_solve(base,macro)
            assert answer==(5 if k=='YES' else 0)
            if assignment is not None:
                full=dict(assignment)
                for j,(u,v,rev) in enumerate(macro):
                    full[('a',j)]=(full[u]+(-1 if rev else 1))%5
                    full[('b',j)]=(full[u]+(-2 if rev else 2))%5
                assert len(full)==len(vertices)
                assert all(R(full[u],full[v]) for u,v in arcs)
            # demonstrate generic arc-consistency without source recognition.
            pin=('grid',0,0)
            ac_ok,ac_steps,all_singleton=ac3(vertices,arcs,pin)
            assert (ac_ok,all_singleton)==((k=='YES'),(k=='YES')),(L,h,k,ac_ok,all_singleton)
            pair[k]={"vertices":len(vertices),"arcs":len(arcs),"count":answer,
                "max_degree":stats['max_degree'],"directed_degree_multiset":stats['indeg_outdeg'],
                "ac3_rooted_success":ac_ok,"ac3_all_singleton":all_singleton,"ac3_revisions":ac_steps,
                "undirected_edges":stats['undirected_edges']}
        for attr in ('vertices','arcs','max_degree','directed_degree_multiset','undirected_edges'):
            assert pair['YES'][attr]==pair['NO'][attr],(L,h,attr)
        assert pair['YES']['max_degree']<=8
        undirected_edge_count=len(pair['YES']['undirected_edges'])
        result['pairs'].append({"grid_side":L,"path_length":h,
          "vertices":pair['YES']['vertices'],"arcs":pair['YES']['arcs'],
          "edges_underlying":undirected_edge_count,"max_total_degree":pair['YES']['max_degree'],
          "same_underlying":True,"same_directed_degree_multiset":True,
          "yes_count":5,"no_count":0,"yes_root_AC3":pair['YES']['ac3_revisions'],
          "no_root_AC3":pair['NO']['ac3_revisions']})
    for L,h in [(3,5),(4,5)]:result['deletion_controls']+=deletion_controls(L,h)
    result['all_vertex_anchor_controls']=0
    for L,h in [(3,5),(4,5)]:
        for kind in ('YES','NO'):
            vertices,arcs,_,_,_=make_grid_theta(L,h,kind)
            for anchor in sorted(vertices):
                ok,_,single=ac3(vertices,arcs,anchor)
                assert (ok,single)==((kind=='YES'),(kind=='YES')),(L,h,kind,anchor)
                result['all_vertex_anchor_controls']+=1
    return result

if __name__=='__main__':
    r=run()
    raw=json.dumps(r,sort_keys=True,indent=2)+'\n'
    open('/mnt/data/tmr5_082/tmr5_083_affine_raw.json','w').write(raw)
    print('validated',len(r['pairs']),'pairs,',r['deletion_controls'],'vertex deletions')
    for q in r['pairs']:
        print(q['grid_side'],q['path_length'],q['vertices'],q['arcs'],q['yes_count'],q['no_count'],q['yes_root_AC3'],q['no_root_AC3'])
    print('RAW_SHA256',hashlib.sha256(raw.encode()).hexdigest())
