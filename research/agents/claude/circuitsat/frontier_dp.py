"""CSAT-0002: frontier-DP Circuit-SAT in O(m*2^k) time, k = max live wires.
Verified against brute force on random circuits; also counts distinct residual
functions (Myhill-Nerode classes) for the 'secret mask' family: 2^k classes."""
import random, itertools, json
def rand_circuit(n, m, rng):
    # gates: (op, a, b) referencing node ids < current; nodes 0..n-1 inputs
    gates=[]
    for i in range(m):
        cur=n+i
        a=rng.randrange(cur); b=rng.randrange(cur)
        gates.append((rng.choice(['and','or','xor','nand']),a,b))
    return gates
OPS={'and':lambda x,y:x&y,'or':lambda x,y:x|y,'xor':lambda x,y:x^y,'nand':1}
def ev(op,x,y):
    return 1-(x&y) if op=='nand' else OPS[op](x,y)
def brute(n,gates):
    for x in itertools.product([0,1],repeat=n):
        v=list(x)
        for op,a,b in gates: v.append(ev(op,v[a],v[b]))
        if v[-1]: return True
    return False
def frontier_dp(n,gates):
    """Process nodes in index order. live[t] = nodes <= t still needed later (or output).
    State = set of assignments to live nodes consistent with some input prefix."""
    N=n+len(gates); last=N-1
    lastuse=[-1]*N
    for i,(op,a,b) in enumerate(gates):
        lastuse[a]=max(lastuse[a],n+i); lastuse[b]=max(lastuse[b],n+i)
    lastuse[last]=N
    live=[]; states={()}; maxlive=0
    for t in range(N):
        new=set()
        if t<n:
            for s in states:
                for bit in (0,1): new.add(s+(bit,))
            live.append(t)
        else:
            op,a,b=gates[t-n]; ia=live.index(a); ib=live.index(b)
            for s in states: new.add(s+(ev(op,s[ia],s[ib]),))
            live.append(t)
        # drop dead
        keep=[i for i,v in enumerate(live) if lastuse[v]>t or v==last]
        new={tuple(s[i] for i in keep) for s in new}
        live=[live[i] for i in keep]; states=new; maxlive=max(maxlive,len(live)+1)
    return any(s[live.index(last)] for s in states), maxlive
rng=random.Random(1); ok=0; mk=0
for trial in range(300):
    n=rng.randint(2,7); m=rng.randint(1,14)
    g=rand_circuit(n,m,rng)
    r,k=frontier_dp(n,g); assert r==brute(n,g); ok+=1; mk=max(mk,k)
# Myhill-Nerode family: inputs x1..xk loaded to frontier, suffix computes [x==s]
def residual_classes(k):
    funcs=set()
    for s in itertools.product([0,1],repeat=k):
        funcs.add(tuple(int(x==s) for x in itertools.product([0,1],repeat=k)))
    return len(funcs)
out={"random_trials_agree":ok,"max_frontier_seen":mk,"residual_classes":{k:residual_classes(k) for k in range(1,9)}}
print(json.dumps(out)); open(__file__.replace('.py','_results.json'),'w').write(json.dumps(out,indent=1))
