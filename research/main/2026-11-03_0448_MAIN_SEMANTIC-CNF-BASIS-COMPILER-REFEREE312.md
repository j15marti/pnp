# SEMANTIC-CNF-BASIS-COMPILER-REFEREE312

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 04:48 PST**

**Status:** PROVED/RESTRICTED computer-assisted local simulation theorem; COMPUTATIONAL exhaustive finite classification and independent proof replay; B1, B2, B3, a superpolynomial worst-case minimum, and P versus NP remain OPEN. No task identity, title, enabled state, ownership, schedule, calculus, or weight changed.

## Exact obstruction and result

REFEREE311 reduced the Boolean-local `L3`-to-`E` compiler coefficient from 48 to 42 by observing that a satisfiable source cannot entail the false eight-blocker factor. That still compiled every false truth-table row as a separate complete blocker. The exact obstruction tested here is:

> Does the compiler really need the complete blocker CNF, or may it replace each explicit factor by a smaller exact CNF basis without breaking downstream factor semantics or hiding computation?

Keep the preselected `Rmix341` unchanged. Let `E` be its strict non-tautological binary Resolution plus paid, conservative, source-independent signed two-input `VARDEF` fragment. Let `L3` be the already declared subgrammar whose additional `AND3` and `LOCAL-CONVERT` inputs and outputs are exact Boolean factors or clauses on a common support of at most three named variables. Source clauses are free; each distinct Resolution, definition, or other paid inference node has unit weight; shared DAG nodes count once. Optimizer discovery is excluded from the logical minimum and reported separately.

### Computer-assisted finite basis lemma

Assign these safe compilation weights to a nonempty clause according to its width:

$$
b_1=3,\qquad b_2=4,\qquad b_3=6.
$$

They are the `k=3` consequences of DPLL-IMPLICATE-PRUNE358:

$$
B(3,s)=2^{3-s}-1+3\max\{s-1,0\}.
$$

For each nonfalse relation `Q` on three variables, minimize the total weight of an auxiliary-free, non-tautological CNF whose model set is exactly `Q`. Complete dynamic programming over all 26 possible nonempty clauses and all 256 relations gives

$$
\max_{Q\ne\bot}\ \min_{\Gamma:\operatorname{Mod}(\Gamma)=Q}
\sum_{C\in\Gamma} b_{|C|}=24.
$$

The maximum is attained only by the two parity relations, masks 105 and 150. Every exact basis has at most four clauses. The two parity functions require four width-three clauses: every proper projection is complete, so no width-one or width-two clause is an implicate, and each width-three clause excludes only one wrong-parity row. Thus their weighted auxiliary-free basis cost is exactly

$$
4\cdot6=24.
$$

The false factor is handled by an early contradiction at cost at most seven, not by a CNF basis of output blockers.

### Theorem: coefficient 24

For every general UNSAT CNF,

$$
W_{L_3}(F)\le W_E(F)\le24W_{L_3}(F)+O(1).
$$

**Proof.** Choose a legal shared `L3` derivation and process its nodes topologically. Reproduce its source clauses, strict Resolution nodes, and paid source-independent definitions. For every explicit local factor label `Q`, use the fixed exact basis `Gamma_Q` certified above rather than all complete blockers.

Inductively, the already compiled input bases define exactly the input factors, so their conjunction `S` has exactly the local predecessor semantics. If `S` is unsatisfiable, DPLL-IMPLICATE-PRUNE358 derives contradiction within seven paid nodes and the global refutation terminates. Otherwise every clause in `Gamma_Q` is a genuine consequence of satisfiable `S`; the same theorem derives it exactly at cost at most `b_s`, where `s` is its width. Summing over the chosen basis costs at most 24. Globally fresh extension names are used for every compiler call. Because `Gamma_Q` is semantically equivalent to `Q`, every downstream local inference sees the same relation; this is an inductive representation substitution, not strengthening, weakening, or a free semantic axiom. All pre-existing DAG references point to authenticated compiled clauses.

The compiler is uniform. The domain has exactly 256 factor tables, so the basis map can be computed by the published fixed dynamic program or stored as a single finite, input-independent table in the compiler code. It is not advice depending on formula size, instance identity, or SAT label. The lower inequality follows because `E` is a subgrammar of `L3`. QED.

The coefficient 24 is exact for the **declared output-only weighted-basis optimization**. It is not asserted to be the shortest full mixed proof coefficient: cross-clause DAG sharing, auxiliary encodings, global XOR, or circuit-valued conversion may improve it further.

## Four falsifiers and dispositions

1. **Canonical complete blockers are mandatory factor syntax.** FALSIFIED for the simulation: an exact CNF basis preserves the complete model relation and composes inductively through later local nodes.
2. **Basis selection is hidden nonuniform advice.** REJECTED. The same 256-entry map or fixed finite dynamic program is used for every input and size; every output factor label is already an explicit eight-row object.
3. **A smaller basis silently strengthens the output.** REJECTED. The verifier checks that the conjunction of basis clauses has exactly, not merely a subset of, the requested truth-table mask.
4. **Parity has a cheaper narrow-clause basis.** FALSIFIED in the auxiliary-free output representation: both parity labels have complete proper projections and require four width-three clauses. This does not exclude a cheaper shared or auxiliary proof in the full calculus.

## Exhaustive audit and encoded DAG controls

The producer and separately written no-import Node verifier independently enumerated:

- all 26 nonempty non-tautological clauses on three names;
- all 256 Boolean relations;
- all 6,561 entailed relation pairs `S subset Q`;
- every exact-basis intersection state and weighted optimum; and
- the two parity maxima and 30 entailed pairs whose output-basis accounting is 24.

The relation-cost histogram is:

| Weighted cost | Relations |
|---:|---:|
| 0 | 1 |
| 3 | 6 |
| 4 | 12 |
| 6 | 20 |
| 7 | 25 |
| 8 | 54 |
| 9 | 8 |
| 10 | 24 |
| 11 | 12 |
| 12 | 52 |
| 14 | 24 |
| 18 | 16 |
| 24 | 2 |

An explicit nontrivial DAG control uses the nine binary clauses whose unique model is `000`. This source entails even parity. Each of the four exact parity-basis clauses is derived from an actual falsified binary source clause using two fresh paid definitions and four strict Resolution nodes. The verifier replayed all 24 paid nodes, checking source provenance, definition freshness and signed clause slots, parent availability, pivots, and outputs. A separate contradictory-unit source resolves to the empty clause in one paid node.

Both-label controls independently confirm masks 105 and 150, four models each, neither entailing the other, and weighted basis cost 24 for both. Twelve malformed records and five deliberately corrupted proofs were rejected.

Final raw SHA-256:

`4ce8c020f4f9e98bdd54cc8d382d119876701cc556d81c923c9d0c86dd8f3204`

## Correct bridge classification

| Obligation | Disposition | Reason |
|---|---|---|
| B1 pointwise | OPEN | A constant-overhead local-rule compiler is not a translation from every total correct SAT decider. |
| B2 worst-case | OPEN | No claim relates every decider's worst-case runtime to the maximum fixed-calculus proof cost. |
| B3 weakest conditional bridge | OPEN | `SAT in P` still does not prove polynomial boundedness for the same preselected `Rmix341`; the new theorem covers only `L3`. |

The result is a restricted proof-system simulation and a further family/representation shortcut. It is neither a proof lower bound nor evidence that every hard family is easy. It does not infer correctness from a machine trace.

## Work, space, and encoding ledger

| Phase | Measured record |
|---|---:|
| Python producer wall time | 0.009824654 s |
| Python producer peak host RSS | 10,496 KiB |
| Node verifier wall time | 0.040291271 s |
| Node verifier peak host RSS | 47,668 KiB |
| Producer source bytes | 11,564 |
| Verifier source bytes | 9,303 |
| Raw JSON bytes | 75,466 |

These are host implementation observations, not Turing-machine or FLMV space bounds. The finite basis optimizer and source selection are discovery/compiler work, not inference-node cost. A scheduled implementation must still charge parsing, factor-table access, lookup or DP, clause emission, fresh-name allocation, proof validation, source/index/head reads, caches, serialization, and all simultaneously live records. The all-phase envelope remains

$$
s'\le\max\{\rho,\eta,\lambda,\lambda s\}.
$$

## Literature and repository review

- McCluskey, [Minimization of Boolean Functions](https://doi.org/10.1002/j.1538-7305.1956.tb03835.x), gives the classical finite Boolean minimization setting. The present weighted CNF dual is a fixed three-variable exhaustive calculation, not a novelty claim for Boolean minimization.
- Čepek, Kučera, and Savický, [Boolean functions with a simple certificate for CNF complexity](https://doi.org/10.1016/j.dam.2011.05.013), study minimum CNF size through implicate covers.
- Emdin, Kulikov, Mihajlin, and Slezkin, [CNF Encodings of Parity](https://doi.org/10.4230/LIPIcs.MFCS.2022.47), record the general auxiliary-free parity clause requirement and the effect of auxiliary variables.
- Kiesl et al., [Simulating Strong Practical Proof Systems with Extended Resolution](https://doi.org/10.1007/s10817-020-09554-z), is relevant precedent for requiring explicit proof transformations rather than semantic equivalence oracles.

Project GitHub searches reviewed LOCAL-TRUTHTABLE-ER2-COMPILER359, CONSTANT-CHARGE-WEAKENING360, DPLL-IMPLICATE-PRUNE358, REFEREE310/311, the 04:12 XOR local-projection result, the 04:12 ER2 reflection-normalization result, and the 04:31 orthogonal-snake family failure. The LSPV-1 reflection equivalence remains explicitly conditional and does not establish B3. Searches in `github.com/openai` for exact CNF minimizers and proof checkers returned no applicable implementation; absence is not evidence of novelty.

## Artifacts and next exact gap

- Producer: `experiments/arc/lspv5_312/semantic_cnf_basis_compiler_referee312.py`
- Independent verifier: `experiments/arc/lspv5_312/verify_semantic_cnf_basis_compiler_referee312.js`
- Raw ledger: `results/raw/arc/lspv5_312/semantic_cnf_basis_compiler_referee312.json`
- Five-role handoff: `research/coordination/2026-11-03_0448_LSPV5_TO_FIVE_ROLE_SEMANTIC-CNF-BASIS-COMPILER-REFEREE312.md`

Next: optimize joint authenticated derivations of an entire basis, allowing shared intermediate clauses and conservative auxiliaries, to test whether 24 falls further. Separately, the decisive gaps remain a mixed-rule-resistant superpolynomial family and B3 for the same fixed calculus.

**P versus NP remains OPEN.**

