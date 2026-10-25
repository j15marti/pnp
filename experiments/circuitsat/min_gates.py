"""Exact minimum B2 (all 2-input gates) circuit size for every Boolean function on n<=3 inputs.
BFS over sets of computed functions (truth tables), deduped. Runtime ~ seconds."""
import itertools, json, sys
n = int(sys.argv[1]) if len(sys.argv)>1 else 3
N = 1<<n; MASK=(1<<N)-1
def var(i): return sum(1<<x for x in range(N) if (x>>i)&1)
inputs=[var(i) for i in range(n)]
# nontrivial binary gates: truth tables g(a,b) for 4-bit g, excluding constants/projections/negated projections
gates=[g for g in range(16) if g not in (0,15,0b1100,0b0011,0b1010,0b0101)]
def ap(g,a,b):
    r=0
    if g&1: r|=~a&~b
    if g&2: r|=a&~b
    if g&4: r|=~a&b
    if g&8: r|=a&b
    return r&MASK
base=frozenset(inputs)
best={}  # function -> min gates
def trivial(f): return f in (0,MASK) or f in inputs or (~f&MASK) in inputs
for f in range(1<<N):
    if trivial(f): best[f]=0
level={base}; k=0
while len(best)<(1<<N):
    k+=1; nxt=set()
    for S in level:
        L=sorted(S)
        for a,b in itertools.combinations(L,2):
            for g in gates:
                h=ap(g,a,b)
                if h in S: continue
                nxt.add(S|{h})
    for S in nxt:
        for h in S:
            for f in (h,~h&MASK):   # output negation free in B2 (absorbed into last gate)
                best.setdefault(f,k)
    level=nxt; print("level",k,"states",len(nxt),"covered",len(best),file=sys.stderr)
from collections import Counter
dist=Counter(best.values())
print(json.dumps({"n":n,"max_gates":max(best.values()),"distribution":dict(sorted(dist.items())),
 "xor_n":best[ __import__('functools').reduce(lambda a,b:a^b,inputs)],
 "and_n":best[__import__('functools').reduce(lambda a,b:a&b,inputs)],
 "maj_or_threshold":None}))
