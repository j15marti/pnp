"""Assemble the exact table for all 188 MU classes from (a) tree_min (DP),
(b) the theorem dag_min >= m-1 for MU formulas, (c) checkpointed stage files
refuting each shorter length L, and (d) the verified k=5 witness."""
import json, sys, collections
sys.argv, args = ['x'], sys.argv[1:]
src = open('research/agents/claude/wbar-exact/min_res.py').read().split('if __name__')[0]
exec(src)
d = json.load(open(args[0]))
stages = [json.loads(l) for l in open(args[1])]
refuted = collections.defaultdict(set)    # (k, L) fully refuted?
cover = collections.defaultdict(list)
for s in stages:
    cover[(s["k"], s["L"])].append(s)
def level_refuted(k, L):
    ss = cover.get((k, L), [])
    if not ss: raise SystemExit(f"missing stage evidence for k={k} L={L}")
    if any(s["found"] for s in ss): return False
    if any(s["slice"] == [0, 1000] and not s.get("slice2") for s in ss): return True
    # union of top slices; slice [0,1] may itself be split at level 2
    top = set()
    for s in ss:
        if not s.get("slice2"):
            top |= set(range(*s["slice"]))
    sub = set()
    for s in ss:
        if s.get("slice2") and s["slice"] == [0, 1]: sub |= set(range(*s["slice2"]))
    full_last = [s for s in ss if not s.get("slice2") and s["nodes"] == 1]
    full_last2 = [s for s in ss if s.get("slice2") and s["nodes"] <= 2]
    if 0 not in top and set(range(44)) <= sub and full_last2: top.add(0)
    return bool(full_last) and set(range(0, max(top) + 1)) <= top
rows = []
for k, f in enumerate(d["formulas"]):
    F = [idx(p, q) for p, q in f["clauses"]]
    m, tm = len(F), tree_min(F)
    if tm == m - 1:
        dm, how = m - 1, "lower bound m-1 meets tree optimum"
    else:
        dm = None
        for L in range(m - 1, tm):
            if not level_refuted(k, L):
                dm, how = L, "proof of this length found; all shorter lengths refuted"; break
        if dm is None:
            dm, how = tm, "all shorter lengths refuted by staged exhaustive search"
    rows.append({"k": k, "m": m, "orbit": f["orbit_size"], "tree_min": tm, "dag_min": dm, "how": how})
if rows[5]["dag_min"] != 8:
    raise SystemExit("k=5 inconsistency")
json.dump(rows, open(args[2], "w"), indent=0)
by_m = collections.defaultdict(list)
for r in rows: by_m[r["m"]].append(r)
print("m  classes labelled  max_dag  max_tree  #dag<tree")
for m in sorted(by_m):
    R = by_m[m]
    print(m, len(R), sum(r["orbit"] for r in R), max(r["dag_min"] for r in R),
          max(r["tree_min"] for r in R), sum(r["dag_min"] < r["tree_min"] for r in R))
print("overall max dag:", max(r["dag_min"] for r in rows), [ (r["k"], r["m"]) for r in rows if r["dag_min"] == max(x["dag_min"] for x in rows)])
print("dag-tree gaps:", [(r["k"], r["m"], r["tree_min"], r["dag_min"]) for r in rows if r["dag_min"] < r["tree_min"]])
print("excess over m-1 (dag):", collections.Counter(r["dag_min"] - (r["m"] - 1) for r in rows))
print("hardest clauses:", d["formulas"][7]["clauses"], "orbit", d["formulas"][7]["orbit_size"])
