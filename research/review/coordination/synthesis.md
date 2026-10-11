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
