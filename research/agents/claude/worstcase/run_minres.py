import sys, json, random, time
import minres, minres_sat
n = int(sys.argv[1]); seed = int(sys.argv[2]); budget = float(sys.argv[3])
rng = random.Random(seed); t0 = time.time(); rows = []
for cl in minres.sample_mus(n, rng):
    if time.time() - t0 > budget: break
    w = minres_sat.min_refutation(cl, n, deadline=t0 + budget)
    rows.append({"m": len(cl), "clauses": cl, "min_res": w})
done = [r["min_res"] for r in rows if r["min_res"]]
print(json.dumps({"n": n, "seed": seed, "instances": len(rows), "solved": len(done), "max": max(done) if done else None,
  "hist": {str(k): done.count(k) for k in sorted(set(done))}}))
json.dump(rows, open(f"minres_n{n}_s{seed}.json", "w"))
