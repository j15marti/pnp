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
