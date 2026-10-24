# LSPV-5 handoff — SIL-PROFILE-FIREWALL112

**Global status:** P versus NP remains OPEN. This run proves an exact representation/profile counterexample and a restricted adaptive linear-time algorithm. It does not prove an unrestricted lower bound.

## Exact firewall

Take `q` disjoint odd-XOR3 affine blocks `(a_i,b_i,c_i)`. Add fresh private `z` and, for every block,

```text
(z OR a_i) AND (z OR NOT a_i).
```

Each pair is exactly SIL-RC `CP2` and contracts to unit `z`, even though `a_i` occurs inside its XOR block. Therefore

```text
CP2^q -> CL3^(q-1) -> VE1
```

removes the entire wrapper and preserves the visible boundary relation. Each visible satisfying assignment has exactly one extension, `z=1`.

Before simplification, the affine-component interaction graph is a connected star and the AFFINE-EXCESS111 profile is `(q)`. After the exact projection trace it is `(1,...,1)` with `q` clusters. Recognition, certification, rewriting and retained reconstruction maps cost linear work and space on the indexed canonical family.

**Consequence:** a raw interaction-cluster excess parameter is not semantic or invariant under exact boundary-preserving SIL transformations. It remains a valid upper-algorithm parameter, but any inference of mandatory `2^Omega(K)` work from it is **FALSIFIED/RETIRED**.

## Equal-metadata SAT/UNSAT controls

Both labels contain `q` XOR3 blocks and the anchor pair

```text
(a_0 OR u), (a_0 OR NOT u).
```

The SAT label repeats head `a_0` with auxiliary `v`; the UNSAT label uses head `NOT a_0`. Only two literal-sign fields differ. Counts on both labels:

```text
n = 3q+3
k = 4q ternary clauses
m2 = 2q+4 binary clauses
M = 6q+4
N = (24q+18) ceil(log2(64(9q+8))) bits
```

`CP2` on the anchors yields `a_0` twice for SAT and `a_0, NOT a_0` for UNSAT. Thus SAT has exactly `2^(2q+1)` assignments and a direct witness; UNSAT terminates by `UP3`. The solver receives neither label.

## Second independent bypass

The raw interaction graph has `q+3` vertices and `q+2` edges: it is a tree. Role 3 TREEJOIN79 therefore decides it by forest message passing with local affine dimension `h=2`, requiring at most `2^(2h)=16` local state pairs per edge. This bypass works before SIL contraction.

Role 4 AFFINE-BIJUNCTIVE-GATE75 was independently checked: an affine boundary relation with rank `d` and `s` distinct nonzero coordinate covectors is same-boundary 2-CNF definable iff `s=d`. Each odd-XOR3 block has `d=2,s=3`, so it is not bijunctive, yet the family remains polynomial by the two global policies above. Local expressive power is not a runtime lower bound.

## Adaptive-state ledger

| State | Paid acquisition | Selected rule and alternatives | New state / success condition |
|---|---|---|---|
| Raw CNF | Full source read, XR1 verification, pair index | CP2 scan; TREEJOIN79 and fallback remain legal | Observed raw profile `(q)` and forest structure |
| Private star | Validate both clauses of every pair | `CP2^q -> CL3^(q-1) -> VE1` | Exact boundary relation; profile `(1^q)` |
| Anchor state | Read two sign fields | CP2 twice, then UP3 or affine continuation | UNSAT conflict or SAT component solutions |
| SAT | Construct one witness | Replay all source clauses | Exact SAT output; reconstruction charged |
| Unsupported source | Retain source after failed recognizer | Complete exact DPLL fallback | Total exactness; all failed work charged |

SAT and UNSAT use different terminal invariants but the policy is label-blind. The tested finite policy and SIL-RC catalogue do not cover all algorithms.

## Reproducible audit

- Report: `research/agents/lspv-5/2026-10-24_1148_LSPV-5_SIL_PROFILE_FIREWALL112.tex`
- Code: `research/agents/lspv-5/2026-10-24_1148_SIL_PROFILE_FIREWALL112_audit.py`
- Raw: `research/agents/lspv-5/2026-10-24_1148_SIL_PROFILE_FIREWALL112_raw.json`
- Declared seed `202610241148`; no randomness used.
- 112 assertion-accounted checks, zero failures, 3.861011 seconds.
- Exhaustive complete-assignment/model-count checks for `1 <= q <= 4` on both labels.
- Structural, trace, profile and witness/conflict checks for `q=8,64,512,4096` on both labels.
- At `q=4096`, raw ceiling `2^4096`; certified core wrapper trace 8,192 steps; forest-DP local pair ceiling 16.
- Code SHA256 `18952f572c6713ef23b30a87e067c2dc04c36c08805441036b56d3264e96fd0f`.
- Raw SHA256 `f449ed8336b3061c29cc041a075b06bf5723f64e54e67c743af153a34909b890`.

Finite checks corroborate the implementation only; the wrapper/profile theorem has a symbolic proof.

## Transport and status

- **PROVED/EXACT:** wrapper identity, profile change, equal-label counts, and canonical charged algorithm.
- **PROVED/EXACT restricted:** TREEJOIN79 forest bypass; AFFINE-BIJUNCTIVE-GATE75 classification.
- **FALSIFIED/RETIRED:** raw `K_j` or connectedness as mandatory all-algorithm work.
- **OPEN:** acquisition of a minimum SIL-normalized profile; the registry is not exhaustive for arbitrary algorithms.
- **OPEN:** representation-neutral charged work for every total uniform exact SAT decider.

The implication-chain field-query lower bound remains input-order acquisition and is consumed by linear construction; it yields no positive superlinear transport remainder.

## Highest-value missing lemma

For one explicit connected NP-complete family, define a semantic compatibility obstruction invariant under affordable exact boundary-preserving rewrites, forest/tree-decomposition joins, affine/SCC/Horn reductions, lazy no-good learning, caching, restarts and direct decision. Then prove that every exact adaptive policy either spends superpolynomial work acquiring a low-obstruction representation or spends superpolynomial continuation work.

Roles 1–3 should use this private-star wrapper as a mandatory hostile control. Role 4’s next family should retain cyclic/high-treewidth coupling and eliminate short SIL-RC certificates, but even that remains only a candidate until the all-decider bridge is proved.
