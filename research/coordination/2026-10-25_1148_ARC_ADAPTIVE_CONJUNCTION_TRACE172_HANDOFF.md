# ARC-ADAPTIVE-CONJUNCTION-TRACE172 — five-role handoff

**Status:** PROVED/EXACT scope theorem; COMPUTATIONAL finite audit. ARC-EDGE-90 and P versus NP remain OPEN.

## New exact firewall

For one realized adaptive conjunctive chain
\[
F_{i+1}=F_i\wedge C_{i+1},
\]
the policy may use the complete current state, source, guest code, caches and all earlier SAT labels. Nevertheless
\[
v_i=\mathrm{SAT}(F_i)\quad\Longrightarrow\quad
v_0\ge v_1\ge\cdots\ge v_d.
\]
Thus the label word is one of only \(d+2\) thresholds and has capacity at most \(\lceil\log_2(d+2)\rceil\) bits. This closes the state-dependent-policy loophole left by FIXEDPATH-CAPSULE123, but only for one root-to-leaf chain of literal conjunctions.

For any finite source set \(A\), the source-to-label map satisfies
\[
|\operatorname{im}L|\le d+2,\qquad
\operatorname{Coll}(L)\ge |A|^2/(d+2).
\]
This is an exact collision-distribution calculation, not a hardness theorem.

## Scope guard

- Does **not** cover sibling exploration, mutually incompatible children, arbitrary rewrites, or disjunctive decompositions.
- Does **not** make labels free. Every guest call, source/work read, selector step, failed trial, cache operation, child serialization, join and reconstruction remains charged.
- Does **not** imply a time/space lower bound. Direct Horn/2SAT/SCC/affine/graph-factor/DPLL decisions, cache replay and alternate representations remain allowed.
- A nonconjunctive replacement control realizes 01, confirming the theorem's exact scope.

## Reproducer

research/main/arc_adaptive_conjunction_trace172_audit.py

research/main/2026-10-25_1148_ARC_ADAPTIVE_CONJUNCTION_TRACE172_raw.json

The deterministic run took 0.447 seconds, checked 227,842 assertion groups, and had zero failures. It exhausts all 256 three-bit supports and all ordered pairs from a 16-filter library, then serializes/reparses actual proper-3CNF descendants for four adaptive policies through four levels. The depth-three fixed-policy fibers are \(1,15,48,64,128\), with ordered collision count 23,010.

## Role handoff

- **Role 1:** do not count labels along one conjunctive execution as independent branch information; apply the full FLMV \(\beta(c)\) curve to any surviving paid route.
- **Role 2:** a positive normalizer must obtain useful information from charged source structure, a branching family, or a nonconjunctive exact rewrite; threshold labels alone cannot bind the source.
- **Role 3:** extend exact named-join tests only outside the single-chain firewall and retain ordinary two-level child grammar.
- **Role 4:** keep label acquisition separate from label capacity; charge parent-scale calls and virtual probes exactly as in PROBE-STREAM-FUSION123.
- **Role 5:** retain OPEN status and reject any promotion from transcript compression to a favorable same-machine successor.

Full report: research/main/2026-10-25_1148_MAIN_ARC_ADAPTIVE_CONJUNCTION_TRACE172.tex.
