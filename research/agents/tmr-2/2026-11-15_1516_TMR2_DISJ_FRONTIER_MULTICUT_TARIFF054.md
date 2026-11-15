# TMR-2/054: exact DISJ frontier and exponential multi-cut tariff collapse

**2026-11-15 15:16 PST | Track A | PNP Information Necessity | revision `tmr2-disj-frontier-multicut054.v1`**

**Status:** PROVED/EXACT for the explicitly restricted matrix/cofactor identities and symbolic edge-activation tariff, independent mathematical review OPEN; finite benchmarks COMPUTATIONAL. Unrestricted rank-to-SAT-machine transfer FALSIFIED. **P versus NP OPEN.**

## 1. Candidate, exact object, falsifiers

**Candidate tested:** aggregation over all balanced cuts, rather than one fixed cut, might give a lower-bound potential that resists cheap changes in a compact circuit. Quantified objects: for each integer k>=1, the *single fixed formula* F_k(u,v)=AND_{i=1}^k (NOT u_i OR NOT v_i), its 2k-input **assignment evaluation tensor**, every permutation/order and every balanced original-variable cut. This is NOT the SAT decision function on binary encodings. The only tariff transitions modeled are additions/removals of one **already specified** independent pair-clause at declared symbolic unit cost. Physical machine work is recorded separately.

Predeclared falsifiers: (1) exact cut-rank histogram is small after balanced-cut aggregation; (2) an order with cheap, bounded cofactor frontier exists even though many cuts are exponentially ranked; (3) one shared edge activation changes exponentially many ranked cuts simultaneously, breaking any constant independent per-cut charge; (4) Horn, Krom, strict-Tseitin, Gaussian, padding, or a compact all-zero SAT witness disposes of the claimed machine transfer. Falsifiers (2)-(4) occur.

## 2. Exact arbitrary-order frontier theorem

Let pi be any order of the 2k original variables. After its first t entries, c_t pairs have exactly one endpoint observed and d_t pairs have both endpoints observed. Then for **every field K**,

```text
rank_K( M_(pi,t)(F_k) ) = 2^(c_t),
q_(pi,t) = number of distinct Boolean suffix cofactors
          = 2^(c_t) + 1[d_t>0].
```

**Proof.** A prefix assignment violating a completely observed pair yields the identically zero residual. Otherwise, each open pair contributes either no restriction or a factor (1-y_partner), depending on the observed bit. The unobserved full pairs contribute the same nonzero factor g(y) to all nonzero residuals. Hence there are precisely 2^c distinct nonzero residuals and the zero residual appears iff d>0. Restricting all variables of wholly unobserved pairs to zero produces the 2^c by 2^c Boolean subset-zeta matrix on open-partner coordinates, which is invertible over every field after a permutation of rows/columns. The other factors do not increase rank. Thus rank=2^c. QED.

For a **complete leveled deterministic ordered read-once BP** with one level per input bit, where rejecting/accepting sink states count toward level width, the minimum reachable width at boundary t equals q_(pi,t): distinct residuals cannot merge, and the quotient by identical residuals realizes the bound. This is a width statement for evaluation of F_k, not a circuit or SAT-decider lower bound. It does not make construction of residual equivalence classes free.

Every variable order has peak q >=3 for k>=2. An interleaved order (u1,v1,u2,v2,...) attains 3; grouped order (all u, then all v) attains 2^k, the maximum over all orders. For k=1 both are 2. A compact shared circuit of 2k-1 fan-in-two NAND/AND gates and 4k-2 gate-input wires evaluates F_k. The order is explicitly available from the matching representation; no hard ordering search is assumed.

## 3. Exact multi-cut census and tariff

Over all H_k=binom(2k,k) *oriented* balanced partitions A:B with |A|=|B|=k, let c(A) be the number of pairs crossing the cut. Then rank over **every field** is 2^c, since internal-side constraints merely zero some rows or columns while each crossing pair contributes the invertible 2x2 matrix [[1,1],[1,0]].

The exact number of cuts with c crossing pairs is

```text
N_(k,c) = binom(k,c) 2^c binom(k-c,(k-c)/2)   if k-c is even;
          0                                   otherwise.
```

Consequently

```text
sum_balanced rank(M_A) = A_k = [z^k](1+4z+z^2)^k,
sum_balanced log_2 rank(M_A) = H_k * k^2/(2k-1).
```

The average log-rank is Theta(k), and by Jensen the average rank is at least 2^(k^2/(2k-1)), despite linear-size evaluation circuitry. This directly controls exponentially many correlated cuts, rather than treating cuts as independent proof obligations.

For j active independent clauses among the same k pairs, set A_(k,j)=[z^k](1+4z+z^2)^j(1+2z+z^2)^(k-j). The exact **one clause activation** change is

```text
Delta_(k,j) = A_(k,j)-A_(k,j-1)
             = 2[z^(k-1)](1+4z+z^2)^(j-1)(1+2z+z^2)^(k-j).
```

All deltas are nondecreasing in j by coefficientwise dominance of (1+4z+z^2) over (1+2z+z^2). Hence in the precisely qualified edge-activation/removal calculus, a scalar tariff Phi_j=lambda*(A_(k,j)-H_k), with Phi_0=0, unit work for removing an edge and a one-step Lipschitz requirement, must obey

```text
lambda <= 1/Delta_(k,k) = 1/(2 A_(k-1,k-1));
Phi_k <= (A_k-H_k)/Delta_(k,k) <= k.
```

This theorem **does not** identify edge removal with a legal unit-cost transition of an arbitrary SAT machine. It states an exact failure of treating all-cut rank increases as additive independent work in this symbolic activation model. On a bit-level input machine, parsing/indexing a specified edge costs actual charged bit operations, potentially O(log k) or more; this does not yield a machine-time lower bound.

## 4. Proper 3CNF and cheap controls

For each k, use the original 2k variables and three fresh pins p,a,b. The seven distinct proper ternary clauses which forbid every nonzero pin triple force all three pins to 0. Replace each original binary clause by (NOT u_i OR NOT v_i OR p). The resulting strict proper, duplicate-free width-exactly-3 CNF has V=2k+3 variables, C=k+7 clauses, L=3k+21 signed occurrences. Every satisfying original assignment has exactly one pin extension and every violating assignment none. All-zero original variables and pins are a uniform easy witness. The fixed-width literal-index encoding has N=O((k+7)log(2k+3)) bits, with signed indices/header overhead charged. A correct total SAT decider can validate this canonical family, accept by verifying 0^V, and use sound exhaustive fallback elsewhere. Both recognition and witness verification cost polynomial source work, not a free semantic oracle.

Other controls: the core is negative Horn and Krom (2SAT); the matching graph has treewidth one and bounded separator DP. All-zero satisfies the core and the strict lift. Gaussian elimination handles affine controls; this formula does not claim affine hardness. Equality/union-find, certified autarkies, independent product factorization, substitutions, learning, caching, sharing, recomputation, preprocessing, circuit simplification and zero padding are all legal; no asserted lower bound excludes them. A globally unique-solution full indicator tensor is rank one across cuts. Valiant-Vazirani isolation has randomized success, repetition and promise costs, so no free deterministic transfer. Invertible local bases preserve matrix rank over their field; Walsh-Hadamard is singular over F2.

## 5. Reproducible computation and same-realization resource ledger

Source: `experiments/tmr/tmr2_disj_frontier_multicut054.js`.
Raw: `results/raw/tmr/2026-11-15_1516_TMR2_DISJ_FRONTIER054_V8_RAW.json`.
No packages; deterministic xorshift32 seed 20261115 for 120 k=4 sampled orders. Actual execution in V8: **13,356 assertions, 1,274 balanced cuts explicitly enumerated, 196 actual GF2/F101 matrix-rank checks, 6,294 prefix-boundary comparisons, 2,720 strict pin-clause evaluations, zero failures.** Exhaustive all 2, 24, 720 orders for k=1,2,3; seeded 120 orders for k=4. Exact coefficients k=1..12, explicit balanced cuts k<=6 and two-field matrix ranks k<=4. The symbolic proof, not finite checking, supports all k/fields. No native Node, preflight, Lean kernel or full checkout execution was performed.

| Object/operation | Sequential work | Peak workspace | Same realization scope |
|---|---|---|---|
| Evaluate matching formula/circuit on one assignment | O(k) fan-in-two gate evaluations | O(k) bits for assignment and optional gates; streaming O(log k) with ordered bits | An explicit compact computation; not all-assignment construction |
| Validate canonical strict 3CNF, output all-zero witness | O(N) to O(N^2) conservative bit-machine cost | O(N) bits conservative, streaming reductions possible | Fixed correct SAT decider on family, fallback off family |
| Enumerate balanced cuts, build matrices | O(H_k 4^k k) conservative naive bit work | O(4^k) bits for one dense Boolean matrix | Benchmark only, not compulsory solver actions |
| Calculate coefficient recurrences up to k | Polynomially many O(k)-bit integer operations | Polynomial bit storage | Explicit counting derivation, not #SAT for general inputs |
| Select interleaved order from pair tags | O(k log k) bit work | O(log k) bits with ordered source | Real cheap family-specific representation |
| Edge-activation symbolic calculus | One declared unit operation per specified edge | State of k active-edge flags | Model-scoped tariff only; not a physical SAT TM step |

## 6. Mandatory four verification gates

| Gate | Verdict and scope |
|---|---|
| 1. DISJ sanity | **PASS restricted, unrestricted transfer FAIL.** DISJ_k has rank 2^k at grouped cut, and a linear-size depth-two unbounded-fan-in circuit, interleaved width 3 and easy SAT witness. No false general-circuit hardness claim. |
| 2. Relativization | **PASS for finite matrix/cofactor identities, OPEN for unrestricted proof.** Identities relativize but do not separate classes. No nonrelativizing SAT step; algebrization/Natural Proofs checks remain OPEN for any future claimed transfer. |
| 3. Simultaneous DTISP | **NOT APPLICABLE WITH REASON** to static rank/BDD and symbolic edge calculus. The exhibited easy witness verifier has same-execution polynomial time/space; no matched forbidden-box SAT simulation is claimed. General solver transfer OPEN. |
| 4. Configuration counting | **PASS as upper-bound guard only.** A fixed total deterministic read-only-input machine with s bits and input N obeys T<=2^O(s+log N), or 2^O(s) for s>=log N. No lower bound is deduced and randomized/quantum runs are outside this statement. |

## 7. Corpus reconciliation, sources and next lemma

First read governing directive `research/coordination/2026-11-15_SAT_COMPRESSION_CIRCUITS_FIVE_AGENT_REFOCUS.md` (SHA 7b8804dc...), then root proof1.txt (SHA 06f7ebc8...), proof2.txt (SHA 930c5eed...), main.tex (SHA 6ac34c5d...), AGENTS.md, CODEX.md, repository skill, five current TMR handoffs, issue #3, original TMR-2/052-053 and TMR-4/051-053 and TMR-5/050 results. proof2/main oversized bodies returned empty through connector; full preflight and root material reconciliation unavailable. **TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.** No agent or schedule mutations.

Prior /051 established grouped vs interleaved for inner-product and DISJ controls; /053 computed graph neighborhood-union rank; TMR-4/053 proved adaptive switch transcript rectangles; TMR-5/050 closed one-switch lower bound. This work adds the **exact prefix cofactor and rank identity for every matching-variable order**, the **entire balanced-cut rank histogram**, and the **exact last-gate multi-cut tariff discharge**. These statements remain scoped and neither promote nor contradict prior results. /341 stays FAIL as full logical UNSAT authority; /386 stays RESTRICTED.

Primary: R. E. Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE Trans. Computers C-35(8), 1986, 677-691, https://doi.org/10.1109/TC.1986.1676819 (restricted ordered decision diagram/cofactor model). Relevant project originals are cited by the absolute paths above. Do not attribute the exact elementary matching formulas to Bryant.

**NEXT LEMMA:** For one explicit expander 3CNF, bound a *costed adaptive-order* branching-program measure from a sequence of actual input inspections, allowing legal source recognition, shared fan-out, cached intermediates and full read/recompute. Seek smallest legal circuit or BP shortcut before any SAT-machine promotion.

**P versus NP remains OPEN.**
