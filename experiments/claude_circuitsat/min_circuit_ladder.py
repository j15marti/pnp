"""Exact minimum fan-in-2 circuit size over the full B2 basis, n<=3, by BFS over
sets of computed truth tables (inputs free, constants excluded).  Wires = 2*gates
(each gate has two input wires, fan-out free).  Chunked: n=2 and n=3 depth<=BOUND."""
import json, sys, time, itertools
n = int(sys.argv[1]); BOUND = int(sys.argv[2])
M = (1 << (1 << n)) - 1
ins = []
for i in range(n):
    t = 0
    for a in range(1 << n):
        if (a >> i) & 1: t |= 1 << a
    ins.append(t)
ops = [lambda a,b,o=o: sum(((o>>(2*((a>>k)&1)+((b>>k)&1)))&1)<<k for k in range(1<<n)) for o in range(16)]
# faster: precompute via bit tricks
def gate(a,b,o):
    r = 0
    if o&1:  r |= ~a & ~b
    if o&2:  r |= ~a & b
    if o&4:  r |= a & ~b
    if o&8:  r |= a & b
    return r & M
best = {}   # function -> min gates
base = frozenset(ins)
for f in list(ins)+[0,M]: best.setdefault(f,0)
frontier = {base}
seen = {base}
t0 = time.time()
for d in range(1, BOUND+1):
    nxt = set()
    for S in frontier:
        L = sorted(S)
        for a,b in itertools.combinations(L,2):
            for o in range(1,15):
                f = gate(a,b,o)
                if f in S or f in (0,M): continue
                T = S | {f}
                if T in seen: continue
                seen.add(T); nxt.add(T)
                best.setdefault(f,d)
    frontier = nxt
    print(f"depth {d} states {len(nxt)} funcs {len(best)}/{1<<(1<<n)} t={time.time()-t0:.1f}", file=sys.stderr)
    if time.time()-t0 > 20: print("time cap", file=sys.stderr); BOUND=d; break
hist = {}
for f,g in best.items(): hist[g] = hist.get(g,0)+1
names = {}
if n==3:
    pop = lambda f: bin(f).count("1")
    names = {"AND3":ins[0]&ins[1]&ins[2],"OR3":ins[0]|ins[1]|ins[2],"XOR3":ins[0]^ins[1]^ins[2],
             "MAJ3":(ins[0]&ins[1])|(ins[0]&ins[2])|(ins[1]&ins[2]),"MUX":(ins[0]&ins[1])|(~ins[0]&ins[2])&M}
res = {"n":n,"depth_bound_completed":BOUND,"num_functions_found":len(best),"total":1<<(1<<n),
       "histogram_gates":hist,"named":{k:best.get(v,f">{BOUND}") for k,v in names.items()}}
print(json.dumps(res))
