import itertools, json

def gf2_rank(mat):
    if not mat: return 0
    A=[row[:] for row in mat]; m=len(A); n=len(A[0]); r=0
    for c in range(n):
        p=next((i for i in range(r,m) if A[i][c]),None)
        if p is None: continue
        A[r],A[p]=A[p],A[r]
        for i in range(m):
            if i!=r and A[i][c]:
                A[i]=[x^y for x,y in zip(A[i],A[r])]
        r+=1
    return r

def gauge_matrix(edges,n):
    rows=[]
    for u,v,w in edges:
        a=[0]*n; a[u]^=1; a[w]^=1
        b=[0]*n; b[v]^=1; b[w]^=1
        rows += [a,b]
    return rows

def components(edges):
    verts=set(sum(([u,v,w] for u,v,w in edges),[]))
    if not verts: return 0,0
    adj={v:set() for v in verts}
    for e in edges:
        for x in e:
            adj[x].update(y for y in e if y!=x)
    seen=set(); c=0
    for v in verts:
        if v in seen: continue
        c+=1; stack=[v]; seen.add(v)
        while stack:
            x=stack.pop()
            for y in adj[x]:
                if y not in seen: seen.add(y); stack.append(y)
    return len(verts),c

rows=[]; assertions=0
for n in range(3,6):
    all_edges=list(itertools.combinations(range(n),3))
    for mask in range(1,1<<len(all_edges)):
        edges=[all_edges[i] for i in range(len(all_edges)) if mask>>i&1]
        v,c=components(edges); m=len(edges)
        rank=gf2_rank(gauge_matrix(edges,n))
        assertions+=1
        assert rank==v-c,(n,edges,rank,v-c)
        deficiency=2*m-rank
        assertions+=1
        assert deficiency==2*m-v+c
        rows.append((n,m,v,c,rank,deficiency))
summary={
  'status':'COMPUTATIONAL',
  'n_range':[3,5],
  'hypergraphs_tested':len(rows),
  'assertions':assertions,
  'rank_discrepancies':0,
  'deficiency_discrepancies':0,
  'deficiency_hist':{}
}
for *_,d in rows:
    summary['deficiency_hist'][str(d)]=summary['deficiency_hist'].get(str(d),0)+1
print(json.dumps(summary,indent=2,sort_keys=True))
