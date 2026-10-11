# UNIVERSAL_CORE_SYNTHESIS coordination

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

