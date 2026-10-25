"""Wire ledger + exact probe-sensitivity for the paired-literal AND circuit family P_n.
P_n: variables x_1..x_n; output = AND of 2n literal wires, wire (i,b) reads x_i with
polarity bit s_{i,b}. SAT iff s_{i,0}==s_{i,1} for all i. Instance = bit string of 2n polarities.
Runtime: seconds (n<=5)."""
import itertools, json
def sat(s,n): return all(s[2*i]==s[2*i+1] for i in range(n))
def wires(n):  # n inputs, 2n literal wires, AND tree of 2n leaves has 2n-1 fan-in-2 gates, 2(2n-1) gate-input wires
    return {"inputs":n,"literal_wires":2*n,"and_gates":2*n-1,"gate_input_wires":2*(2*n-1)}
out={}
for n in range(1,6):
    N=2*n; base=tuple([0]*N); assert sat(base,n)
    sens=sum(1 for j in range(N) if not sat(base[:j]+(1,)+base[j+1:],n))
    # exact deterministic probe complexity by minimax over decision trees for small N
    from functools import lru_cache
    @lru_cache(None)
    def D(known):  # known: tuple of None/0/1
        vals=[sat(s,n) for s in itertools.product(*[(k,) if k is not None else (0,1) for k in known])]
        if all(vals) or not any(vals): return 0
        best=99
        for j,k in enumerate(known):
            if k is None:
                best=min(best,1+max(D(known[:j]+(b,)+known[j+1:]) for b in (0,1)))
        return best
    d=D(tuple([None]*N)) if N<=8 else None
    out[n]=dict(wires(n),sensitivity_at_all_plus=sens,exact_det_probe_complexity=d)
json.dump(out,open("results/raw/claude_circuitsat/ladder_results.json","w"),indent=1)
print(json.dumps(out))
