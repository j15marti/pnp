"""Exact minimum fan-in-2 circuit size (gates, wires) over all 16 binary gates
for every Boolean function on n<=3 inputs. Runs in a few seconds.
Circuit = DAG; size counts gates; wires = 2*gates (every gate fan-in 2;
wires into the output are free, inputs are free, constants allowed as gate args)."""
import itertools, json, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    ins=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    base=set(ins)|{0,M}
    ops=[lambda x,y,t=t:sum((((t>>(2*((x>>a)&1)+((y>>a)&1)))&1)<<a) for a in range(N)) for t in range(16)]
    best={f:0 for f in base}
    # level-by-level: functions computable with <=k gates via sets of circuit "states"
    # states = frozenset of available functions; BFS on states (n<=3 small)
    start=frozenset(base); seen={start}; front=[start]; k=0
    size={f:0 for f in base}
    while front and len(size)<(1<<N):
        k+=1; nxt=[]
        for st in front:
            L=list(st)
            for x,y in itertools.combinations_with_replacement(L,2):
                for op in ops:
                    g=op(x,y)
                    if g in st: continue
                    ns=st|{g}
                    if ns not in seen:
                        seen.add(ns); nxt.append(ns)
                        if g not in size: size[g]=k
        front=nxt
    return size
out={}
for n in (1,2,3):
    s=run(n)
    hist={}
    for f,k in s.items(): hist[k]=hist.get(k,0)+1
    N=1<<n
    # unique-satisfier functions (needle): popcount==1
    needle=max(k for f,k in s.items() if bin(f).count('1')==1)
    needle_min=min(k for f,k in s.items() if bin(f).count('1')==1)
    out[n]={"hist":dict(sorted(hist.items())),"max_gates":max(s.values()),
            "needle_gates_min":needle_min,"needle_gates_max":needle}
    print(n,out[n],flush=True)
json.dump(out,open("minwires_results.json","w"),indent=1)
