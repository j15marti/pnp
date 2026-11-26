"""Genuine raw-source regional target mask tests. Never use full-source signed
identities at targets where they need not hold."""
from parity import *

def run():
    rng=random.Random(261127);T,n=mixed_ring(3);auth(T,n);stats=C.Counter()
    for j in range(100):
        S=sorted(rng.sample(range(len(T)),rng.randint(1,8)))
        R=[tuple((i,1) for i in S if T[i][c]==v) for c in range(3) for v in range(n)]
        R=[row for row in R if row];P=prepare(R);stats['regions']+=1
        if P is None:stats['OPEN']+=1;continue
        W=[dict(zip(S,w)) for w in I.product((0,1),repeat=len(S))]
        def occupancy(w):return [sum(w[v]==b for v,b in row) for row in R]
        valid=[w for w in W if max(occupancy(w),default=0)<=1]
        for i in range(10):
            t=occupancy(rng.choice(valid)) if i%2 else [rng.randrange(2) for row in R]
            pins={v:rng.randrange(2) for v in S if rng.randrange(5)==0}
            expected=any(occupancy(w)==t and all(w[v]==b for v,b in pins.items()) for w in W)
            status,x,opt=evaluate(R,P,t,pins);assert (status=='YES')==expected
            stats['queries']+=1;stats[status]+=1
    return dict(stats)
if __name__=='__main__':print(json.dumps(run()))
