#!/usr/bin/env python3
"""GATE302 self-contained canonical source generator and certificate reproducer.
Full producer, no-import independent verifier, raw S/U matrix and trials are
in the companion downloadable reproducibility archive. Python 3 stdlib only.
"""
import json, collections, itertools

def source(r):
    assert r>=4 and r%2==0
    def vertex(i,j,p): return (i%r*r+j%r)*4+p
    edge=[];lookup={}
    def add(a,b):
        pair=tuple(sorted((a,b)))
        assert pair not in lookup
        lookup[pair]=len(edge)+1
        edge.append(pair)
        return len(edge)
    ring={};north={}
    for i in range(r):
        for j in range(r):
            for p in range(4):
                ring[i,j,p]=add(vertex(i,j,p),vertex(i,j,(p+1)%4))
    for i in range(r):
        for j in range(r):
            north[(i+1)%r,j]=add(vertex(i,j,2),vertex(i+1,j,0))
            add(vertex(i,j,1),vertex(i,j+1,3))
    incidence=[[] for _ in range(4*r*r)]
    for e,(a,b) in enumerate(edge,1):
        incidence[a].append(e);incidence[b].append(e)
    assert all(len(z)==3 for z in incidence)
    positive=[set(z) for z in incidence]
    negative=[set(z) for z in incidence]
    for i in range(r):
        for j in range(r//2):
            a=vertex(i,j,0)
            b=vertex(i,j+r//2,0)
            ea=north[i,j];eb=north[i,j+r//2]
            positive[a].remove(ea);positive[a].add(eb)
            positive[b].remove(eb);positive[b].add(ea)
    clauses=[tuple(sorted(z)) for z in positive]
    clauses +=[tuple(-e for e in sorted(z)) for z in negative]
    return edge,incidence,clauses

def grammar(n,clauses):
    if 3*len(clauses)!=4*n:return False
    counts=collections.Counter();seen=set()
    for c in clauses:
        if len(c)!=3 or len(set(map(abs,c)))!=3:return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        if any(abs(x)>n or x==0 for x in c):return False
        if tuple(sorted(c)) in seen:return False
        seen.add(tuple(sorted(c)))
        for lit in c:counts[lit]+=1
    return all(counts[i]==counts[-i]==2 for i in range(1,n+1))

def recognize(n,clauses):
    """No use of source vertex labels or witness indices; rename-invariant."""
    if not grammar(n,clauses):return None
    neg=[tuple(-x for x in c) for c in clauses if c[0]<0]
    pos=[tuple(c) for c in clauses if c[0]>0]
    occurrences=collections.defaultdict(list)
    for v,c in enumerate(neg):
        for e in c:occurrences[e].append(v)
    if len(occurrences)!=n or any(len(a)!=2 or a[0]==a[1] for a in occurrences.values()):return None
    ends={e:tuple(a) for e,a in occurrences.items()}
    V=len(neg);neighbors=[set() for _ in range(V)]
    for a,b in ends.values():neighbors[a].add(b);neighbors[b].add(a)
    if any(len(z)!=3 for z in neighbors):return None
    cycles=set()
    for a in range(V):
        for b in neighbors[a]:
            for c in neighbors[b]-{a}:
                for d in neighbors[c]-{a,b}:
                    if a in neighbors[d]:cycles.add(tuple(sorted((a,b,c,d))))
    if 4*len(cycles)!=V:return None
    block={}
    for cycle in cycles:
        for v in cycle:
            if v in block:return None
            block[v]=cycle
    if len(block)!=V:return None
    internal={e for e,(a,b) in ends.items() if block[a]==block[b]}
    if len(internal)!=V:return None
    adj=[{} for _ in range(V)]
    for e in internal:
        a,b=ends[e];adj[a][b]=e;adj[b][a]=e
    if any(len(a)!=2 for a in adj):return None
    for c in pos:
        z=[e for e in c if e in internal]
        if len(z)!=2 or not(set(ends[z[0]]) & set(ends[z[1]])):return None
    matching=set()
    for cyc in cycles:
        a=min(cyc);b=min(adj[a])
        c,d=tuple(set(cyc)-{a,b})
        if d not in adj[c]:return None
        matching.update((adj[a][b],adj[c][d]))
    if not all(any((lit>0 and lit in matching) or
                   (lit<0 and -lit not in matching) for lit in c)
               for c in clauses):return None
    return matching

def cube(edge,incidence,clauses,r):
    # external horizontal edge E(0,0) to W(0,1)
    u=1;v=7
    e=next(e for e,(a,b) in enumerate(edge,1) if set((a,b))=={u,v})
    pin={x:0 for x in incidence[u] if x!=e}
    pin.update({x:1 for x in incidence[v] if x!=e})
    assert len(pin)==4
    open_clauses=[]
    for j,c in enumerate(clauses):
        if any((lit>0 and pin.get(lit)==1) or
               (lit<0 and pin.get(-lit)==0) for lit in c):continue
        remaining=[lit for lit in c if abs(lit) not in pin]
        assert remaining
        open_clauses.append((j,remaining))
    ids=[(j,c[0]) for j,c in open_clauses if len(c)==1]
    assert any(lit==e for _,lit in ids)
    assert any(lit==-e for _,lit in ids)
    return {'pins':pin,'pivot':e,'unit_source_ids':ids,
            'source_resolution_proof':[[e],[-e],[]]}

def hist(C,ones):
    h=[0]*4
    for c in C:
        t=sum((x>0 and x in ones) or (x<0 and -x not in ones) for x in c)
        h[t]+=1
    return h

def main():
    rows=[]
    for r in (4,6,8,12):
        edges,inc,C=source(r)
        n=len(edges);m=len(C)
        assert grammar(n,C)
        w=recognize(n,C);assert w is not None
        assert hist(C,w)==[0,m//2,m//2,0]
        assert hist(C,set(range(1,n+1))-w)==[0,m//2,m//2,0]
        q=cube(edges,inc,C,r)
        P={frozenset(c) for c in C if c[0]>0}
        Q={frozenset(-x for x in c) for c in C if c[0]<0}
        assert len(P-Q)==len(Q-P)==r*r
        rows.append({'r':r,'n':n,'m':m,'delta_root':2*n-m,
                     'unpaired_per_sign':r*r,
                     'treewidth_lower_bound':(r-2)/2,
                     'SAT_matching_weight':len(w),
                     'SAT_histogram':hist(C,w),
                     'UNSAT_cube':q,
                     'SOURCE_VALID':True})
    print(json.dumps(rows,indent=2))
if __name__=='__main__': main()
