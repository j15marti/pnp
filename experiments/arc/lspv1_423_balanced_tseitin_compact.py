"""LSPV-1/423 compact balanced AND3/XOR proof metrics reproducer.
For full source-deletion witnesses and independent verifier see local bundle.
"""
import itertools, math, json

def graphs():
    return {
      'K4': (4,[(i,j) for i in range(4) for j in range(i+1,4)]),
      'K33': (6,[(i,j) for i in range(3) for j in range(3,6)]),
      'cube': (8,[(i,j) for i in range(8) for j in range(i+1,8) if (i^j).bit_count()==1]),
      'Petersen': (10,[(i,(i+1)%5) for i in range(5)]+[(5+i,5+(i+2)%5) for i in range(5)]+[(i,5+i) for i in range(5)])
    }

def proof(h,edges):
    assert len(edges)==3*h//2
    incidence=[set() for _ in range(h)]
    for i,(u,v) in enumerate(edges):incidence[u].add(i);incidence[v].add(i)
    assert all(len(s)==3 for s in incidence)
    charge=[1]+[0]*(h-1)
    source=[]; nodes=[]
    for v in range(h):
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2!=charge[v]:
                source.append(tuple(-(e+1) if b else e+1 for e,b in zip(sorted(incidence[v]),bits)))
    assert len(source)==4*h
    # Balanced four-clause AND3 tree, each pair and final node paid.
    for v in range(h):
        nodes.extend([('AND3',v,1)]*2+[('AND3',v,2)])
    occurrence=3*h
    def xor(group):
        nonlocal occurrence
        if len(group)==1:return set(incidence[group[0]]),charge[group[0]],2
        m=len(group)//2
        a,ab,ad=xor(group[:m]);b,bb,bd=xor(group[m:])
        row=a.symmetric_difference(b)
        occurrence+=len(row)
        nodes.append(('XOR',len(row),max(ad,bd)+1))
        return row,ab^bb,max(ad,bd)+1
    row,rhs,depth=xor(list(range(h)))
    assert row==set() and rhs==1
    assert len(nodes)==4*h-1 and depth==math.ceil(math.log2(4*h))
    assert occurrence<=3*h*(math.ceil(math.log2(h))+1)
    return dict(clauses=len(source),paid_nodes=len(nodes),depth=depth,row_occurrences=occurrence)

if __name__=='__main__':
    print(json.dumps({name:proof(h,e) for name,(h,e) in graphs().items()},indent=2))
