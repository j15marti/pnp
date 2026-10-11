# SYNTHESIS current run 2026-10-11

## SYNTHESIS-0014 — log-succinct resource trilemma (2026-10-11T20:45:32Z)

**Status:** core publication pending readback. **P versus NP remains OPEN.**

- **PROVED/EXACT, independent review pending:** `LOG-SUCCINCT-RESOURCE-EQUIV1`.
- **FALSIFIED/RETIRED as an intermediate route:** `LOG-SUCCINCT-RESOURCE-AS-INTERMEDIATE1` and conditional witness/resource incompressibility.
- **COMPUTATIONAL:** 28,187 exact finite checks, zero failures, 0.180 seconds.
- **Single OPEN target:** `SOURCE-PASS-ACCESS1` with externally fixed predecision semantics, bit-local access, hereditary coverage, arbitrary-exponent elimination, complete charging, and one model-matched forbidden realization.

Report: `research/review/reports/synthesis/2026-10-11_2045_SYNTHESIS-0014.tex`.
Historical MAIN: `research/main/2026-10-11_2045_MAIN_SYNTHESIS-0014.tex`.

---

# SYNTHESIS current run 2026-10-11

## SYNTHESIS-0012 — quotient covariance has no invariant middle (2026-10-11T18:48:00Z)

**Status:** VERIFIED by exact GitHub readback. **P versus NP remains OPEN.**

- **PROVED/EXACT, prior corpus:** connected covariance up to an equivalence relation makes the quotient class source-only; every equivalence-respecting resource also factors through the source.
- **PROVED/EXACT:** under a fixed unconditional endpoint exclusion SAT not in G, the complete typed compiler implication is equivalent to SAT not in P.
- **FALSIFIED/RETIRED:** `TYPED-COMPILER-AS-INTERMEDIATE1`; the compiler itself remains OPEN and separation-strength.
- **COMPUTATIONAL:** 1,353,627 graph labelings, 1,536 semantic wrapper checks, affine/easy-family/encoding controls, zero failures.
- **Single OPEN target:** `SOURCE-PASS-ACCESS1` — one predecision, bit-local, hereditary, fully charged source pass with no current-scale or fallback unknown-exponent term.

Report: `research/review/reports/synthesis/2026-10-11_1848_SYNTHESIS-0012.tex`.
Historical MAIN: `research/main/2026-10-11_1848_MAIN_SYNTHESIS-0012.tex`.

---

# SYNTHESIS current run 2026-10-11

## SYNTHESIS-0010 — local-reduction port dichotomy (2026-10-11T16:48:00Z)

**Status:** VERIFIED and published. **P versus NP remains OPEN.**

`LOCAL-REDUCTION-PORT-DICHOTOMY1` reconciles MODELBRIDGE-0014, LB-0014, TESTS-0009, and RT-0014. Parent-owned bounded-fanout emission uses only forward child labels. Target-owned exact fanout certification or complete parent enumeration has a linear child-query lower bound per target. Reverse incidence is therefore neither automatically available nor generically required.

Retired: `GENERIC-REVERSE-PORT-NECESSITY1` and the unqualified `CHILD-LOCALITY-IMPLIES-FANOUT-CERT1`.

Open supporting target: `JMV-TO-H22-STREAM1`, including direct on-demand exact Monotone 3-SAT-(2,2) encoding, address translation, uniqueness, witness maps, quasilinear output, polylog bit time, and logarithmic workspace.

Open load-bearing target: an exponent-independent, fully charged, predecision, hereditary transformation from every hypothetical polynomial SAT decider to the FLMV-forbidden time-space realization. The local reduction does not supply this bootstrap or a nonrelativizing hinge.

Audit: 10,432 circuits, 450,339 edge comparisons, zero failures; completed in 0.329 seconds.

Report: `research/review/reports/synthesis/2026-10-11_1648_SYNTHESIS-0010.tex`.

---

# UNIVERSAL_CORE_SYNTHESIS coordination

## SYNTHESIS-0013 — 2026-10-11T19:48:00Z

**Status:** verified and published. **P versus NP remains OPEN.**

**PROVED/EXACT modulo KNOWN THEOREM:** `LAYER-BALANCED-H22-ISLAND1`.
The SAT formula `P_(ell+22)` and UNSAT formula `P_ell disjoint-union U` have
the same `(n,m,m+,m-,N)` for every `ell>=1`.

**FALSIFIED/RETIRED:** `COFINAL-ANSWER-BALANCE-REPAIR1`. Same-layer answer
diversity does not repair pointwise all-decider necessity.

**OPEN single target:** `SOURCE-PASS-ACCESS1` with worst-case existential
inputs and all acquisition/access/replay/output/time/space costs in one
SAME_REALIZATION.

Report: `research/review/reports/synthesis/2026-10-11_1948_SYNTHESIS-0013.tex`.

## SYNTHESIS-0009 — 2026-10-11T15:48:00Z

**Status:** VERIFIED, pending independent review. **P versus NP remains OPEN.**

**PROVED/EXACT:** `OFFLINE-INDEX-SPACE-GATE1` for the materialized TESTS-0008 realization. If output length is `M=N^(q+o(1))` and the same execution stores a `Theta(M)` index, composed workspace exponent is `q`, not `q/2`.

**FALSIFIED/RETIRED:** `OFFLINE-INDEX-CLOSES-LOCAL-COOK1`. Correct explicit offline indexing is not an on-demand, simultaneous-space local reduction. Full inverse incidence is not necessary for the fixed tagged second leg.

**OPEN single target:** `JMV-PORT-LOCALITY1`: compute the concrete first-leg forward occurrence/port label in polylogarithmic time and logarithmic workspace without materialization. The arbitrary-algorithm transfer and P versus NP remain OPEN.

Report: `research/review/reports/synthesis/2026-10-11_1548_SYNTHESIS-0009.tex`.

# UNIVERSAL_CORE_SYNTHESIS coordination

## SYNTHESIS-0008 — 2026-10-11T14:48:00Z

**Status:** VERIFIED, pending independent review. **P versus NP remains OPEN.**

**PROVED/EXACT:** `RECOGNIZABLE-ISLAND-BARRIER1`. A uniformly recognizable constant-answer island admits a recognize-first exact wrapper with only the recognizer cost on every island member.

**FALSIFIED/RETIRED:** `STRUCTURAL-POINTWISE-NECESSITY1` in its unqualified form. The theorem does not refute worst-case `forall A exists F` lower bounds.

**OPEN single target:** `LOCAL-COOK-MONOTONE22STAR1`, the bit-local first leg from the exact FLMV source to Monotone 3-Sat*-(2,2). The arbitrary-exponent bootstrap, barrier crossings, UCORE-TIME1, and P versus NP remain OPEN.

Report: `research/review/reports/synthesis/2026-10-11_1448_SYNTHESIS-0008.tex`.
Code: `experiments/review/recognizable_island_quantifier_audit.py`.
Raw result: `results/raw/review/2026-10-11_recognizable_island_quantifier.json`.

## SYNTHESIS-0001 — 2026-10-11T05:52:00Z

**Status:** VERIFIED. **P versus NP remains OPEN.**

**PROVED/EXACT:** `PINNING-NOCONTRACT1`. For the recurrence `C_(t+1)=max(r,eta+lambda C_t)`, every standard explicit pinning child retains the source and therefore has `lambda=1`. Hence `C_t>=K` for every depth; pinning cannot eliminate an arbitrary polynomial SAT exponent.

**FALSIFIED/RETIRED:** `PINNING-CONTRACTION1` and any promotion treating source-retaining pinning calls as strict-shrink descendants or charging their separate work to the original one-bit execution without a proved service.

**OPEN unified target:** `UCORE-CONTRACT1`. Construct one source-first, fully charged, hereditary ordinary-CNF successor with `lambda<1` on every input, including the canonical Monotone 3-SAT-(2,2) core, and land its closed time/space recurrence inside a model-matched unconditional forbidden region.

Peer handoffs:

- MODEL_BRIDGE: EDGE-EXTRACT1 is useful only if a richer service yields `lambda<1`.
- TESTS: attack strict-shrink services with batching, reread, affine, and compact representations.
- REDTEAM: reject children retaining the whole source and direct-sum imports without a compiler.
- PROOF_MAP: require a same-execution compiler that also proves strict source-scale contraction.
- COST_CERTIFICATES: close reset, access, verifier, and child-representation costs in the same recurrence.

Report: `research/review/reports/synthesis/2026-10-11_0552_SYNTHESIS-0001.tex`.
Code: `experiments/review/universal_core_synthesis_gate.py`.
Raw result: `results/raw/review/2026-10-11_universal_core_synthesis_gate.json`.
## SYNTHESIS-0002 — 2026-10-11T06:48:00Z

**Status:** VERIFIED, pending independent red-team review. **P versus NP remains OPEN.**

**PROVED/EXACT:** `DECIDE-GUARD-CONTRACT1`. For every total deterministic decider A and every polynomial source functional q, a uniform guard wrapper can make q decoder-causally indispensable and emit an equivalent constant-size proper 3-CNF successor (lambda=0). The wrapper first runs A, so its charged local exponent r is at least A's unknown exponent K; `C_(t+1)=max(r,eta+lambda C_t)>=K`.

**FALSIFIED/RETIRED:** `CAUSAL-STRICT-SUCCESSOR-IMPLIES-K-ELIMINATION1`, including decide-then-emit contractions. Causal use, exact equivalence, heredity, and strict child size do not substitute for a K-independent constructor bound.

**OPEN unified target:** `PREDECISION-CONTRACT1`. Produce the strict, locally addressable ordinary-CNF successor within one K-independent charged bound before any current-scale decision work, close hereditary time/space recurrence, and enter the same-model FLMV forbidden region.

Peer handoffs:

- MODEL_BRIDGE: bind acquisition completion before current-scale decision work; test inlining invariance.
- TESTS: measure constructor and child costs separately under decide-then-emit and RECOMP wrappers.
- REDTEAM: reject any strict successor whose local exponent inherits K or whose predecision guard is merely syntactic.
- PROOF_MAP: force the representation before the answer is known and preserve FLMV access.
- COST_CERTIFICATES: charge constructor, reset, serialization, access, recursion, and output jointly.

Report: `research/review/reports/synthesis/2026-10-11_0648_SYNTHESIS-0002.tex`.
Code: `experiments/review/guarded_constant_successor_audit.py`.
Raw result: `results/raw/review/2026-10-11_guarded_constant_successor_audit.json`.

## SYNTHESIS-0003 — 2026-10-11T07:48:00Z

**Status:** VERIFIED locally, pending independent readback. **P versus NP remains OPEN.**

**PROVED/EXACT:** `TW-DP-UPPER-NOT-LOWER1`. With `x=k-(tw(F)+1)`, `2^(k-x)` is the maximum Boolean assignment count for one supplied primal-treewidth bag. It is a DP interface scale, not an all-decider lower bound.

**FALSIFIED/RETIRED:** `TREEWIDTH-2K2X-LOWER1`. Dense Horn SAT/UNSAT families and a tautological-clause wrapper have primal graph `K_n` and nominal scale `2^n` but linear-time or trivial decisions.

**OPEN unified target:** `TW-MESSAGE-FORCING1`: a K-independent predecision same-execution compiler from every uniform deterministic SAT decider on canonical Monotone 3-SAT-(2,2) to a charged separator-message protocol, followed by an unconditional model-matched lower bound. Source-program replay `Q=enc(F)` is an explicit adversary.

Peer handoffs:

- MODEL_BRIDGE: force a specific separator protocol in the same execution; test source replay and semantic bypasses.
- TESTS: carry dense Horn, DEAD tautology, 2SAT, affine, COPY, and permutation controls with all stages charged.
- REDTEAM: reject `2^(k-x)` when it is only table capacity, reachable-state count, or explicit-output length.
- PROOF_MAP: keep treewidth DP as a representation upper bound and SETH optimality as conditional.
- LOWER_BOUND/COST_CERTIFICATES: seek joint evaluation bounds immune to source reread and preserve arbitrary exponent K.

Report: `research/review/reports/synthesis/2026-10-11_0748_SYNTHESIS-0003.tex`.
Code: `experiments/review/treewidth_2k2x_synthesis_audit.py`.
Raw result: `results/raw/review/2026-10-11_treewidth_2k2x_synthesis_audit.json`.


## SYNTHESIS-0004 — 2026-10-11T09:48:00Z

**Status:** VERIFIED report pending publication log. **P versus NP remains OPEN.**

- **PROVED/EXACT:** the declared two-clause balanced connector has `k=0 mod 3`; `k=0` is disconnected and `k=3` is impossible under clause uniqueness.
- **COMPUTATIONAL:** exhaustive `k=6` search covered 1,417,800 positive hypergraphs and both negative orbits; 150 semantic hits, zero connected hits.
- **FALSIFIED/RETIRED:** balance as a general obstruction to exact monotone clause simulation, by Döcker's known enforcer.
- **OPEN:** `k>=9`, global connected balanced pin lift, `DAG-COMPILER1`, `UCORE-TIME1`, and P versus NP.

Peer handoffs:

- TESTS/REDTEAM: independently reimplement the `k=6` orbit/enumeration certificate before theorem promotion.
- LOWER_BOUND/MODEL_BRIDGE: do not treat connector size or minimal DAG size as arbitrary-machine work without `DAG-COMPILER1`.
- PROOF_MAP: encode the `k=9` search with symmetry breaking and checkable projection/connectivity certificates in sub-30-second chunks.
- LSPV-5: retain OPEN status; this is a construction-search floor, not a separation.

Report: `research/review/reports/synthesis/2026-10-11_0948_SYNTHESIS-0004.tex`.
Code: `experiments/review/two_clause_connector_k6_audit.py`.
Raw result: `results/raw/review/2026-10-11_two_clause_connector_k6.json`.

## SYNTHESIS-0006 — 2026-10-11T12:48:00Z

**Status:** VERIFIED, pending independent review. **P versus NP remains OPEN.**

**PROVED/EXACT:** `SOURCE-ONLY-RECURSIVE-ENDPOINT-EQUIV1`. A fully charged hereditary source-only successor with `(r,p,h,v)` closes to one depth-first SAT decider with `C=max{1,r,(v-h)/(1-h)}` and `P=max{p,h}`; any endpoint decider gives the terminal converse.

**FALSIFIED/RETIRED:** `SOURCE-ONLY-IS-INTERMEDIATE1`. A source-only favorable contract in a forbidden region is already the endpoint algorithm, not a weaker consequence of an arbitrary polynomial implementation.

**OPEN unified target:** `A-RELATIVE-FRACTIONAL-BOOTSTRAP1`. Transform every assumed uniform polynomial SAT decider into a recursively replaceable strictly-smaller-instance realization with a fixed favorable full ledger, no current-scale/fallback `K` term, and a same-machine endpoint transfer.

Peer handoffs:

- MODEL_BRIDGE: specify the exact uniform map `A -> S_A` or a wrapper/oracle counterexample.
- LOWER_BOUND: reject source-only/external objects as same-execution obligations; audit DIRECT, RECOMP, affine, and maximal-oracle replacements.
- TESTS/COST_CERTIFICATES: measure recursive call replacement, generator access, replay, serialization, reconstruction, and retained ancestors.
- REDTEAM: reject any `N^(1-o(1))` parent call, answer-dependent child selection, or mixed-machine time/space pair.
- LSPV-5/PROOF_MAP: keep the bootstrap, endpoint transfer, nonrelativization, nonalgebrization, UCORE-TIME1, and P versus NP OPEN.

Report: `research/review/reports/synthesis/2026-10-11_1248_SYNTHESIS-0006.tex`.
Code: `experiments/review/source_only_recursive_endpoint_audit.py`.
Raw result: `results/raw/review/2026-10-11_source_only_recursive_endpoint.json`.
## SYNTHESIS-0007 — 2026-10-11T13:48:00Z

**PROVED/EXACT pending independent review:** `CLEANCORE-FLMV-TRANSFER-BUDGET1`. A reduction with target-length exponent `q`, setup `a`, per-bit overhead `alpha`, and workspace `b` sends target exponents `(c,p)` to `C=max{1,a,qc+alpha}`, `P=max{b,qp}`. For `(6/5,1/2)` with ideal other costs the sharp FLMV budget is `q<1.003836695566892...`.

**FALSIFIED/RETIRED:** `POLYNOMIAL-NP-REDUCTION-SUFFICES1`. NP-completeness alone does not transfer a quantitative time-space endpoint.

**OPEN unified clean-core target:** `LOCAL-H22-FLMV-TRANSFER1`: verify a general-source, canonical, bit-local, same-model reduction with `M=N^(1+o(1))`, fully charged setup/access and compatible peak workspace. `NONVACUOUS-INTENSIONAL-BOOTSTRAP1` remains separately OPEN after RT-0011.

Report: `research/review/reports/synthesis/2026-10-11_1348_SYNTHESIS-0007.tex`.
Code: `experiments/review/clean_core_flmv_transfer_budget_audit.py`.
Raw result: `results/raw/review/2026-10-11_clean_core_flmv_transfer_budget.json`.
P versus NP remains OPEN.
