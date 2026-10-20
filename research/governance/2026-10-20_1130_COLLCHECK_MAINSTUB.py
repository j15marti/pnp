import random
from collections import Counter
random.seed(1)
bad=0
for t in range(20000):
    A=random.randint(1,60); B=random.randint(1,40)
    L=[random.randint(0,B-1) for _ in range(A)]
    c=Counter(L); coll=sum(v*v for v in c.values())
    assert len(c)*coll>=A*A
    if len(c)*coll==A*A and len(set(c.values()))>1: bad+=1
print("CS bound |im L|>=|A|^2/Coll holds on 20000 random maps; nonuniform-equality violations:",bad)
