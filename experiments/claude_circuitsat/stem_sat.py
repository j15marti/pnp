#!/usr/bin/env python3
"""Validate Lemma (stem conditioning): SAT in O(2^{|S|} m) where S = nodes of out-degree>=2, |S|<=beta.
Compares against brute force on random {AND,OR,NOT} circuits with n inputs."""
import random, itertools, json
def rand_circuit(n,g,rng):
    gates=[]
    for i in range(g):
        k=n+i
        t=rng.choice('ANO'); a=rng.randrange(k); b=rng.randrange(k)
        if t=='N' or a==b: gates.append(('N',a,a))
        else: gates.append((t,a,b))
    return gates
def cone(n,gates):
    g=len(gates); out=n+g-1; used={out}; st=[out]
    while st:
        v=st.pop()
        if v>=n:
            t,a,b=gates[v-n]
            for u in ((a,) if t=='N' else (a,b)):
                if u not in used: used.add(u); st.append(u)
    return used
def brute(n,gates):
    for a in range(1<<n):
        val=[(a>>i)&1 for i in range(n)]
        for t,x,y in gates:
            val.append(1-val[x] if t=='N' else (val[x]&val[y] if t=='A' else val[x]|val[y]))
        if val[-1]: return True
    return False
def stem_sat(n,gates,used):
    outdeg={v:0 for v in used}
    for v in used:
        if v>=n:
            t,a,b=gates[v-n]
            for u in ((a,) if t=='N' else (a,b)): outdeg[u]+=1
    out=n+len(gates)-1
    stems=[v for v in used if v!=out and outdeg[v]>=2]
    beta=sum(outdeg[v]-1 for v in used if v!=out)
    assert len(stems)<=beta
    def tree_ok(assign):
        # each node: set of achievable values given stems fixed (cut) ; non-stem nodes are tree-like
        memo={}
        def ach(v):  # achievable values of v's "own computation" (stem constants not used here)
            if v in memo: return memo[v]
            if v<n: r={0,1}
            else:
                t,a,b=gates[v-n]
                A=use(a)
                if t=='N': r={1-x for x in A}
                else:
                    B=use(b); r=set()
                    for x in A:
                        for y in B: r.add(x&y if t=='A' else x|y)
            memo[v]=r; return r
        def use(u):  # value seen by a consumer
            return {assign[u]} if u in assign else ach(u)
        for s in stems:  # stem's own computation must be able to produce guessed value
            if assign[s] not in ach(s): return False
        return 1 in use(out)
    for bits in itertools.product((0,1),repeat=len(stems)):
        if tree_ok(dict(zip(stems,bits))): return True,len(stems),beta
    return False,len(stems),beta
rng=random.Random(1); bad=0; stats=[]
for trial in range(3000):
    n=rng.randint(2,6); g=rng.randint(2,14)
    gates=rand_circuit(n,g,rng); used=cone(n,gates)
    r,s,b=stem_sat(n,gates,used)
    if r!=brute(n,gates): bad+=1
    stats.append((s,b))
print(json.dumps({'trials':3000,'mismatches':bad,'max_stems':max(s for s,_ in stats),'stems_le_beta_always':all(s<=b for s,b in stats)}))
