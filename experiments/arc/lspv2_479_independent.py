"""Independent finite controls; NOT a Kleene fixed-point execution."""
import itertools,json
edges=[(a,b) for a in range(4) for b in range(a+1,4)]
checks=0;sat=0;unsat=0
for charge in range(16):
    clauses=[]
    for v in range(4):
        incident=[j for j,(a,b) in enumerate(edges) if v in (a,b)]
        for bits in itertools.product([0,1],repeat=3):
            if sum(bits)%2!=((charge>>v)&1):
                clauses.append(tuple((j+1) if bits[i]==0 else -(j+1) for i,j in enumerate(incident)))
    assert len(clauses)==16;checks+=1
    sat_now=False
    for vals in itertools.product([False,True],repeat=6):
        if all(any(vals[abs(l)-1]==(l>0) for l in c) for c in clauses):
            sat_now=True;break
    assert sat_now==(charge.bit_count()%2==0);checks+=1
    sat+=sat_now;unsat+=not sat_now
for k in range(5):
    for n in range(1,18):
        lower=(n+1)**(k+2)
        assert lower>(n+1)**k;checks+=1
        for h in [None,1,4,9,20]:
            actual=h is not None and h<=n
            steps=lower if actual else 0
            assert (steps>(n+1)**k)==actual;checks+=1
print(json.dumps(dict(status='PASS',checks=checks,sat=int(sat),unsat=int(unsat),scope='finite independent arithmetic and K4 controls only'),indent=2))
