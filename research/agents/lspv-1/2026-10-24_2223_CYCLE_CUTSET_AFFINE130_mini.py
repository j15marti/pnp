#!/usr/bin/env python3
"""CYCLE-CUTSET-AFFINE130: independent small control, Python stdlib."""
from itertools import product
from random import Random

def local_ok(block, assignment):
    xs, clauses, row, rhs = block
    return all(any(assignment[abs(l)] == int(l>0) for l in c)
               for c in clauses) and sum(assignment[x] for x in row)%2 == rhs

def global_brute(blocks):
    xs = sorted(set().union(*(set(b[0]) for b in blocks)))
    for bits in product((0,1), repeat=len(xs)):
        a=dict(zip(xs,bits))
        if all(local_ok(b,a) for b in blocks): return True
    return False

def cutset_decide(blocks, edges):
    B=len(blocks); uf=list(range(B)); tree=[]; chords=[]
    def find(x):
        while uf[x]!=x:
            uf[x]=uf[uf[x]]; x=uf[x]
        return x
    for u,v,x in edges:
        p,q=find(u),find(v)
        if p==q: chords.append(x)
        else: uf[p]=q; tree.append((u,v,x))
    assert len(tree)==B-1 and len(chords)==len(edges)-B+1
    adj=[[] for _ in blocks]
    for u,v,x in tree:
        adj[u].append((v,x));adj[v].append((u,x))
    parent=[-1]*B; incoming=[None]*B; order=[0]
    for u in order:
        for v,x in adj[u]:
            if v==parent[u]: continue
            assert v not in order
            parent[v]=u; incoming[v]=x;order.append(v)
    children=[[] for _ in blocks]
    for v in range(1,B):
        children[parent[v]].append((v,incoming[v]))
    for bits in product((0,1),repeat=len(chords)):
        fixed=dict(zip(chords,bits)); messages=[set() for _ in blocks]
        for u in reversed(order):
            b=blocks[u]
            for pin in ((None,) if u==0 else (0,1)):
                for row in product((0,1),repeat=len(b[0])):
                    a=dict(zip(b[0],row))
                    if any(a[x]!=z for x,z in fixed.items() if x in a):continue
                    if pin is not None and a[incoming[u]]!=pin:continue
                    if local_ok(b,a) and all(a[x] in messages[v] for v,x in children[u]):
                        messages[u].add(pin);break
        if None in messages[0]:return True
    return False

def complete_bipartite(r, odd):
    B=2*r;edges=[];owned=[[] for _ in range(B)]
    for u in range(r):
        for j in range(r):
            x=len(edges)+1
            edges.append((u,r+j,x))
            owned[u].append(x);owned[r+j].append(x)
    blocks=[(tuple(v),tuple(),tuple(v),int(odd and i==0))
            for i,v in enumerate(owned)]
    return blocks,edges

def main():
    rng=Random(202610241330); checks=0
    for r in (2,3,4,8,16):
        for odd in (False,True):
            blocks,edges=complete_bipartite(r,odd)
            k=len(edges)-len(blocks)+1
            assert k==(r-1)**2;checks+=1
            assert (sum(b[3] for b in blocks)%2==0)==(not odd);checks+=1
            if r<=3:
                assert cutset_decide(blocks,edges)==global_brute(blocks)==(not odd)
                checks+=1
            if r<=4:
                count=0
                for values in product((0,1),repeat=r*r):
                    a={x+1:values[x] for x in range(r*r)}
                    count+=all(local_ok(b,a) for b in blocks)
                assert count==(2**k if not odd else 0);checks+=1
    for B in (3,4,5):
        for k in range(min(3,(B-1)*(B-2)//2)+1):
            base={(i-1,i) for i in range(1,B)}
            extras=[(i,j) for i in range(B) for j in range(i+1,B)
                    if (i,j) not in base]
            rng.shuffle(extras)
            pairs=sorted(base.union(extras[:k]))
            edges=[];owned=[[] for _ in range(B)]
            for u,v in pairs:
                x=len(edges)+1
                edges.append((u,v,x));owned[u].append(x);owned[v].append(x)
            for i in range(B):owned[i].append(len(edges)+i+1)
            for label in ('sat','unsat'):
                truth={x:rng.randrange(2) for x in set().union(*map(set,owned))}
                blocks=[]
                for vs in owned:
                    row=tuple(x for x in vs if rng.randrange(2))
                    rhs=(sum(truth[x] for x in row)%2 if label=='sat'
                         else rng.randrange(2))
                    clauses=[]
                    for _ in range(2):
                        v=rng.choice(vs);lit=v if rng.randrange(2) else -v
                        if label=='sat':lit=v if truth[v] else -v
                        clauses.append((lit,))
                    blocks.append((tuple(vs),tuple(clauses),row,rhs))
                if label=='unsat':
                    u,v,x=edges[0]
                    for i,lit in ((u,-x),(v,x)):
                        vs,clauses,row,rhs=blocks[i]
                        blocks[i]=(vs,clauses+((lit,),),row,rhs)
                assert cutset_decide(blocks,edges)==global_brute(blocks)==(label=='sat')
                checks+=1
    print({'checks':checks,'failures':0,'seed':202610241330,
           'scope':'finite explicit block networks only','P_vs_NP':'OPEN'})

if __name__ == '__main__':
    main()
