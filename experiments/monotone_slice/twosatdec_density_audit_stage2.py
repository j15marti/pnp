"""Stage 2: density 6.0, larger q, rmax=4; and depth of rare UNSAT draws at density 3.5."""
import random, sys, time, importlib.util
spec = importlib.util.spec_from_file_location("a", __file__.replace("_stage2", ""))
src = open(__file__.replace("_stage2", "")).read().replace("\nmain()\n", "\n")
ns = {"__file__": "x"}; exec(src, ns)
seed = 20261121; rng = random.Random(seed); t0 = time.time(); print(f"seed {seed}")
for q in (28, 32):
    L = ns["clauses_list"](q); t = int(6.0 * q); ds = []
    for _ in range(4):
        F = rng.sample(L, t)
        if not ns["dpll"](F): d = ns["min_depth"](F, q, 4); ds.append("5+" if d is None else d)
    print(f"dens=6.0 q={q} t={t} N=4 mindepth[r<=4]={ds} elapsed={time.time()-t0:.1f}s"); sys.stdout.flush()
for q in (16, 20):
    L = ns["clauses_list"](q); t = int(3.5 * q); ds = []; n = 0
    while len(ds) < 4 and n < 400:
        n += 1; F = rng.sample(L, t)
        if not ns["dpll"](F): d = ns["min_depth"](F, q, 4); ds.append("5+" if d is None else d)
    print(f"dens=3.5 q={q} t={t} draws={n} UNSAT-conditioned mindepth[r<=4]={ds} elapsed={time.time()-t0:.1f}s"); sys.stdout.flush()
