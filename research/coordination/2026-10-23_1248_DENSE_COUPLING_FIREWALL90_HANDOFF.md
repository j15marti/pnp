# DENSE-COUPLING-FIREWALL90 handoff

**Status:** P versus NP OPEN. PROVED/EXACT only in the declared graph/CNF and deterministic query models; COMPUTATIONAL audit is finite.

## New theorem

For `t >= 4`, start with `K_{t,t}` on parts `A,B`. Add either the star edges `a0a1,a0a2,a0a3` (SAT) or the triangle `a0a1,a1a2,a2a0` (UNSAT). The two inputs have identical metadata, source treewidth exactly `t`, one-hot-CNF primal treewidth in `[t,3t+2]`, and opposite 3-colorability labels. Yet canonical recognition and decision take `O(t^2)=O(N/w)` word time and `O(log N)` auxiliary bits.

This retires dense coupling, unbounded treewidth, large syntactic residual, or many local compatibility edges as standalone lower-bound measures.

## Independent checks

- Role-4 chain: exact `q` deterministic orientation-field queries on the all-one input; only `Omega(N/w)` word acquisition under the declared fixed-width encoding.
- Role-4 odd wheels: independently checked matched SAT/UNSAT controls and every positive-block deletion witness for odd `h=5..31`.
- Leaf/forest padding preserves 3-colorability and is linearly stripped, so it does not amplify the chain bound.
- Transport inequality has no positive asymptotic remainder when `L_old=Omega(q)` but materialization or recognition costs `Theta(q)`.
- Role-2 refinement incorporated: exact ternary/2-CNF projection compiler is `O(k(n+m)+k^2)` word time, improving the earlier `O(k^2(n+m))` construction; kernel size remains at most `k+18k^2` clauses.

## Audit

`experiments/review/dense_coupling_firewall90_audit.py` produced 545 assertions, 398 exact 3-color searches, 26 dense instances, 26 decomposition checks, 78 padding controls, and 266 wheel deletion witnesses, with zero failures. Raw result: `results/raw/review/DENSE_COUPLING_FIREWALL90_raw.json`.

## Transport ledger

Only
`T_new^{<=}(g(q)) >= (L_old(q)-R(q)-H(q))/(Q(q) tau(q))`
is justified, with a positive numerator. Direct inclusion preserves order but does not amplify it. Here construction/recognition consumes the linear source bound.

## Roles 1--3 hostile control

Any proposed obstruction must distinguish a source-nonrecognizable NP-complete family after charging source acquisition and compatibility discovery. It must survive the dense matched pair, odd wheels, leaf padding, SCC/affine/treewidth DP, caching, learned constraints, and decide-first normalization.

## Highest-value missing lemma

A representation-independent charged semantic compression-or-continuation theorem covering **every** total uniform deterministic exact decider for one fixed NP-complete encoding, with an independently defined `r_A(F)` and hard inputs satisfying `r_A(F)/log N -> infinity`. Every universal arrow remains OPEN.
