"""Independent checks (no code shared with min_res.py's search):
1. every enumerated formula is exact-3 and minimally unsatisfiable;
2. orbit sizes sum to the labelled count and each orbit size divides 384;
3. the DAG witness for the sharing-gap formula is a valid resolution refutation
   of the stated length, rechecked from scratch;
4. every recorded (tree_min, dag_min) satisfies m-1 <= dag_min <= tree_min."""
import json, sys, itertools
n = 4
data = json.load(open(sys.argv[1]))
rows = [json.loads(l) for l in open(sys.argv[2])]
stages = [json.loads(l) for l in open(sys.argv[3])]
def lits(p, q): return frozenset([v + 1 for v in range(n) if p >> v & 1] + [-(v + 1) for v in range(n) if q >> v & 1])
def sat(cls):
    for bits in itertools.product((False, True), repeat=n):
        if all(any((l > 0) == bits[abs(l) - 1] for l in c) for c in cls): return True
    return False
ok = True
for f in data["formulas"]:
    cls = [lits(p, q) for p, q in f["clauses"]]
    ok &= all(len(c) == 3 for c in cls) and not sat(cls)
    ok &= all(sat(cls[:i] + cls[i + 1:]) for i in range(len(cls)))
    ok &= 384 % f["orbit_size"] == 0
ok &= sum(f["orbit_size"] for f in data["formulas"]) == data["mu_labelled"]
print("enumeration checks:", ok)
bad = [r for r in rows if not (r["m"] - 1 <= r["dag_min"] <= r["tree_min"])]
print("sandwich m-1 <= dag <= tree:", not bad, "rows:", len(rows))
w = json.load(open(sys.argv[4]))
cls = [lits(p, q) for p, q in data["formulas"][w["k"]]["clauses"]]
have = set(cls); steps = 0
for (p, q) in w["derived"]:
    c = lits(p, q)
    found = False
    for a in have:
        for b in have:
            for v in a:
                if -v in b:
                    r = (a - {v}) | (b - {-v})
                    if r == c and not any(-x in r for x in r): found = True
    assert found, ("unjustified", sorted(c))
    have.add(c); steps += 1
print("witness valid:", frozenset() in have, "length:", steps)
