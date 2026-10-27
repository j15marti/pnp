"""Wire-by-wire ladder for Circuit-SAT (ClaudeCircuitSAT.tex). Runtime << 30s.
Circuits: n inputs, g fan-in-2 gates (AND/OR with optional negation on each wire).
For each circuit, a wire is 'critical' if rerouting it to constant 0 or 1 changes satisfiability.
Reports, per (n,g): #circuits, max critical wires, max wires, and whether some circuit has all wires critical.
"""
import itertools, json
def sat(n, gates, out, override=None):
    # gates: list of (op, (src_a,neg_a),(src_b,neg_b)); src index <n inputs, else gate n+i
    for x in range(1<<n):
        val=[(x>>i)&1 for i in range(n)]
        for gi,(op,a,b) in enumerate(gates):
            def rd(k,w):
                if override and override[0]==(gi,k): return override[1]
                s,ng=w; return val[s]^ng
            va,vb=rd(0,a),rd(1,b)
            val.append(va&vb if op==0 else va|vb)
        if val[out]: return True
    return False
def circuits(n,g):
    def rec(gates):
        k=len(gates)
        if k==g: yield list(gates); return
        wires=[(s,ng) for s in range(n+k) for ng in (0,1)]
        for op in (0,1):
            for a in wires:
                for b in wires:
                    if b<a: continue
                    gates.append((op,a,b)); yield from rec(gates); gates.pop()
    yield from rec([])
res={}
for n in range(1,4):
    for g in range(1,4):
        if g>=3 and n==3 and g>2: pass
        cnt=0; best=0; allcrit=False; maxw=2*g
        for gates in circuits(n,g):
            out=n+g-1
            # require every gate to feed forward to output (no dead gates)
            used={out}
            for gi in range(g-1,-1,-1):
                if n+gi in used:
                    used.add(gates[gi][1][0]); used.add(gates[gi][2][0])
            if any(n+gi not in used for gi in range(g)): continue
            cnt+=1
            base=sat(n,gates,out)
            crit=sum(1 for gi in range(g) for k in (0,1)
                     if any(sat(n,gates,out,((gi,k),c))!=base for c in (0,1)))
            best=max(best,crit)
            if crit==maxw: allcrit=True
        res[f"n={n},g={g}"]=dict(circuits=cnt,max_critical=best,wires=maxw,all_critical_exists=allcrit)
        print(n,g,res[f"n={n},g={g}"],flush=True)
json.dump(res,open("results/raw/claude_circuitsat/wire_ladder.json","w"),indent=1)
