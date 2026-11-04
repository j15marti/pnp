#!/usr/bin/env python3
"""LSPV-2/391: exact graph-to-affine-CNF repair-distance controls."""
import itertools, json

def clauses(n, edges):
    out=[]
    for u,v in list(edges)+[(n,n+1),(n+1,n+2),(n,n+2)]:
        out.extend([(u+1,v+1), (-(u+1),-(v+1))])
    return out

def satisfied(c,mask):
    return any(bool(mask&(1<<(abs(l)-1)))==(l>0) for l in c)

def cut(n, edges):
    return max((sum(((x>>u)&1)!=((x>>v)&1) for u,v in edges) for x in range(1<<n)),default=0)

def minbad(n, cs):
    return min(sum(not satisfied(c,x) for c in cs) for x in range(1<<n))

def resolve(a,b,p):
    if not ((p in a and -p in b) or (-p in a and p in b)):
        raise ValueError("invalid pivot")
    return tuple(sorted((set(a)|set(b))-{p,-p}))

def proof(n=0):
    a,b,c=n+1,n+2,n+3
    cs=clauses(n,[])
    steps=[(0,3,b),(6,5,a),(1,4,a),(8,2,b),(7,9,c)]
    refs=list(cs); out=[]
    for l,r,p in steps:
        refs.append(resolve(refs[l],refs[r],p))
        out.append(dict(left=l,right=r,pivot=p,conclusion=list(refs[-1])))
    assert not refs[-1]
    return dict(clauses=[list(v) for v in cs],steps=out,final=[])

def main():
    checks=0; graphs=0; hist={}; examples=[]
    for n in range(1,6):
        pairs=list(itertools.combinations(range(n),2))
        for g in range(1<<len(pairs)):
            edges=[e for i,e in enumerate(pairs) if g>>i&1]
            cs=clauses(n,edges)
            val=minbad(n+3,cs)
            mc=cut(n,edges)
            assert val==len(edges)-mc+1
            checks+=1
            full=edges+[(n,n+1),(n+1,n+2),(n,n+2)]
            for x in range(1<<(n+3)):
                bad=sum(not satisfied(c,x) for c in cs)
                mono=sum(((x>>u)&1)==((x>>v)&1) for u,v in full)
                assert bad==mono
                checks+=1
            graphs+=1; hist[str(val)]=hist.get(str(val),0)+1
            if n==5 and g in (0,31,100,1023):
                examples.append(dict(n=n,edges=edges,maxcut=mc,min_deletions=val,source_clauses=len(cs)))
        assert not proof(n)["final"];checks+=1
    for r in range(1,4):
        edges=[]
        for j in range(r):
            i=3*j;edges.extend([(i,i+1),(i+1,i+2),(i,i+2)])
        assert minbad(3*r+3,clauses(3*r,edges))==r+1
        checks+=1
    for n in range(1,6):
        eq=[(u+1,-v-1) for u,v in [(n,n+1),(n+1,n+2),(n,n+2)]]
        assert all(satisfied(c,0) for c in eq)
        checks+=1
    try: resolve((1,2),(-2,-3),1)
    except ValueError: checks+=1
    else: raise AssertionError("corrupted pivot accepted")
    obj=dict(id="LSPV2-391",status="COMPUTATIONAL, plus separate all-size symbolic theorem",
      graph_universe="all simple labelled graphs with n=1..5",
      graphs_checked=graphs,assignment_clause_checks=checks,distance_histogram=hist,
      examples=examples,triangle_strict_resolution_certificate=proof(),
      disjoint_triangles_tested=3,malformed_proof_rejections=1)
    print(json.dumps(obj,sort_keys=True,separators=(",",":")))
if __name__=="__main__":main()
