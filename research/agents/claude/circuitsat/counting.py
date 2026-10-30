"""Shannon counting: smallest g such that #circuits(g gates) < 2^(2^n); then some
n-variable function needs >= g+1 gates (B2, fan-in 2).  #circuits(g) <= (n+g) * prod_{i=1..g} 16 (n+i-1)^2 / g!  is NOT used;
we use the weaker but trivially valid bound without /g!  and also the version with /g! (valid because
topological relabellings of a circuit with all gates reachable give g! distinct encodings... see tex remark; reported separately)."""
import math, json
out = {}
for n in range(1, 13):
    lim = 2 ** n  # log2 of number of functions
    lg = math.log2(n)  # placeholder
    s = 0.0; g = 0
    while True:
        g += 1
        s += 4 + 2 * math.log2(n + g - 1)
        if s + math.log2(n + g) < lim:  # circuits with g gates (output any node) fewer than functions
            lower = g + 1
        else:
            break
    out[n] = {"log2_functions": lim, "gates_lower_bound_some_function": g if g>1 else 1}
    # recompute cleanly: largest g with count<funcs  => need >= g+1
    s = 0.0; best = 0
    for gg in range(1, 10 ** 6):
        s += 4 + 2 * math.log2(n + gg - 1)
        if s + math.log2(n + gg) < lim: best = gg
        else: break
    out[n] = {"log2_functions": lim, "some_function_needs_at_least_gates": best + 1, "wires": 2 * (best + 1)}
json.dump(out, open("counting_results.json", "w"), indent=1)
for n, v in out.items(): print(n, v)
