"""Independent semantic control for original signed cubic Tseitin 3-CNF.
Not an R_mix341 checker. Standard Python library only, no SAT oracle.
"""
import itertools, json

def graph(kind):
    if kind == 'K4': return 4, list(itertools.combinations(range(4),2))
    if kind == 'K33': return 6, [(i,j) for i in range(3) for j in range(3,6)]
    if kind == 'cube': return 8, [(i,i^(1<<k)) for i in range(8) for k in range(3) if i<(i^(1<<k))]
    if kind == 'petersen':
        edges=[]
        for i in range(5):
            edges += [tuple(sorted((i,(i+1)%5))),tuple(sorted((i+5,(i+2)%5+5))),tuple(sorted((i,i+5)))]
        return 10,sorted(edges)
    raise ValueError(kind)

def clauses(n,edges,charges):
    inc=[[] for _ in range(n)]
    for idx,(u,v) in enumerate(edges):
        inc[u].append(idx)
        inc[v].append(idx)
    out=[]
    for v,vec in enumerate(inc):
        assert len(vec)==3
        for pattern in itertools.product((0,1), repeat=3):
            if sum(pattern)%2 != charges[v]:
                out.append(tuple((i+1) if bit==0 else -(i+1) for i,bit in zip(sorted(vec),pattern)))
    return out

def models(edges,rows):
    k=len(edges); count=0
    for bits in itertools.product((0,1),repeat=k):
        if all(any(bits[abs(l)-1] == (1 if l>0 else 0) for l in c) for c in rows):
            count+=1
    return count

def run():
    count=0; samples=[]
    for kind in ('K4','K33','cube','petersen'):
        h,e=graph(kind)
        odd=clauses(h,e,[1]+[0]*(h-1))
        even=clauses(h,e,[0]*h)
        assert len(odd)==4*h==len(even);count+=2
        om=models(e,odd);em=models(e,even)
        assert om==0
        assert em==2**(len(e)-h+1);count+=2
        for i in range(4):
            bad=odd.copy()
            bad[i]=tuple(-l if k==0 else l for k,l in enumerate(bad[i]))
            assert sorted(bad)!=sorted(odd);count+=1
        samples.append(dict(graph=kind,vars=len(e),vertices=h,odd_models=om,even_models=em))
    return dict(status='PASS',checks=count,samples=samples)
if __name__=='__main__':
    print(json.dumps(run(),indent=2))
