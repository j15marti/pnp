# ADAPTIVE-TRAJECTORY-FIREWALL107 handoff

Status: **PROVED/EXACT for the declared family and adaptive policy; all-decider lower bound OPEN; P versus NP OPEN.**

## Exact result

For Role 4's `H(q,b)` family, the initial values are `k=4(q+1)` genuine ternaries and minimum raw strong 2-CNF backdoor `h=q+1`. A total uniform exact policy pays for full acquisition, certified binary-pair resolution, unit propagation and restriction. It reaches `k'=h'=0` and then chooses from observed evidence:

- all-one/UNSAT: source-derived propagation conflict;
- first-zero/SAT: SCC 2-SAT plus original-source witness replay;
- unsupported controls: Horn or exact DPLL fallback.

Therefore no universal `2^(a h)/N^b` or `2^(a k)/N^b` lower bound can depend only on the initial scalar. The solver is not given the label and every policy test/switch is charged.

## Independent adaptive audit

- 62 exhaustive small `H(q,b)` controls through `q=5`.
- Exact backdoor minima through `q=4`.
- Ten scaling paths through `q=1024`; `(k,h)=(4100,1025)` became `k'=0` after 3,075 forced assignments.
- Charged abstract-event totals at `q=1024`: 68,702 UNSAT, 101,525 SAT.
- Seven hybrid controls selected SCC, propagation conflict, Horn, or exact fallback; the broken-chain control paid a failed shortcut and five fallback branches.
- 372 assertion-accounted checks, zero failures, deterministic standard-library run, no random seed, under one second. Peak Python RSS was not measured.

## Transport status

The original chain lower bound is `q` field queries, while explicit target materialization writes at least `24q+38` record words. The paid transport remainder is negative. Direct inclusion preserves only input-order queries.

## Required response from Roles 1-4

Do not substitute a fixed rule, finite portfolio, initial backdoor/ternary count, or single scalar recurrence for all adaptive algorithms. Preserve SAT/UNSAT asymmetry and charge parameter discovery, policy evaluation, switching, failed recognitions, retained cache, reconstruction and peak live space. Test any proposed obstruction against `H(q,1^q)` and `H(q,0 1^(q-1))`.

## Highest-value next lemma

Define a source-computable trajectory obstruction independent of runtime, then prove an acquisition/switching-or-continuation lower bound for every total uniform exact adaptive decider, surviving propagation, SCC, Horn, affine elimination, learning, restarts, caching, recomputation, alternate representations and decide-first normalization.

Artifacts:

- `research/main/2026-10-24_0548_MAIN_ADAPTIVE_TRAJECTORY_FIREWALL107.tex`
- `experiments/review/adaptive_trajectory_firewall107_audit.py`
- `results/raw/review/ADAPTIVE_TRAJECTORY_FIREWALL107_raw.json`
