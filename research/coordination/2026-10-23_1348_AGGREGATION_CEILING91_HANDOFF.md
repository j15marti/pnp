# AGGREGATION-CEILING91 handoff

**Global status:** P versus NP remains OPEN.

## Exact new rung

Take `p` disjoint fixed-width implication chains, each with `q` orientation fields. Let `s_j` be the SAT label of chain `j`, and combine the labels with any full binary read-once AND/OR tree `A`.

There is a guarded width-at-most-three CNF `G_{A,p,q}` with

- `n = pq + 3p - 1` variables;
- `m = 1 + 2 I_AND + I_OR + p(q+2)` clauses;
- `SAT(G) = A(s_1,...,s_p)` exactly.

Short clauses convert to ordinary proper 3CNF with constant overhead.

The source predicate has full multilinear degree `pq`, so its exact deterministic orientation-field decision-tree complexity is

`D = pq`.

This is a genuine multiplicative direct-sum/query result, but the encoded input also contains `pq` independent fields. Hence `D = Theta(N/log N)`: acquisition order only.

## Transport consequence

Materializing the target requires `R = Theta(pq+p)` record writes. Therefore

`T_new^{<=}(g) >= (L_old-R-H)/(Q tau)`

has no proved positive asymptotic remainder when `L_old=pq`. Direct inclusion preserves the same field bound but does not amplify its order.

## Time and space

- One chain: linear SCC time.
- `p` disjoint chains: exact `pq` worst-case fields; sequential component processing permits workspace reuse.
- Guarded canonical family: `O(pq+p)` source recognition/evaluation and conservative `O(p+q)` working words.
- Proper-3CNF conversion: `Theta(pq+p)` output records.
- Exponential generic branching is an upper bound, not mandatory work.

## Audit

`experiments/review/aggregation_ceiling91_audit.py` checked 37,926 exact CNF/source semantic instances, 31 exact decision-tree depths, 31 full-degree coefficients, and 151,848 total assertions with zero failures. Raw output is `results/raw/review/AGGREGATION_CEILING91_raw.json`.

## Roles 1--3 integration

Independent products, disjoint components, and guarded selectors can now be retired as superlinear amplification mechanisms: they only fill the explicit-input query ceiling. The first plausible arrow is a **post-acquisition shared-compatibility theorem** for one fixed NP-complete encoding. It must force every uniform exact decider either to pay superpolynomial charged compression/verification cost or superpolynomial continuation, while surviving the certified 2-CNF projection kernel, SCC/Horn/affine/treewidth algorithms, caching, source recognition, semantic oracles, and decide-first normalization.

Every universal implication remains OPEN.
