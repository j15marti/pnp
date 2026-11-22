# Continuation log: T5 resource lower bounds

Timestamp: 2026-11-21 18:16 America/Los_Angeles.

## Status of the exhaustive handoff

The exhaustive research handoff remains the authoritative baseline at research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md. Unrestricted superpolynomial exact-counting and decision lower bounds for strict #T5 remain OPEN. The single-tape quadratic time and cubic CM theorems for the sparse matching layouts are audited model-specific results. Representation lower bounds (DNNF, DLDD, positive polynomials) are architecture-specific. P versus NP remains OPEN. No unconditional superpolynomial claim is advanced.

## GitHub and literature search summary

- No public repositories under openai, google-research, or anthropics contain direct work on the strict five-valued T5 relation, the matching-family crossing arguments, or the project's cumulative-memory accounting for exact counting.
- OpenAI/math and anthropics/formal-math contain Lean formalizations of claimed subexponential deterministic algorithms for exact counting of k-CNF (refuting ETH if correct). These are October 2026 algorithmic upper-bound claims, still under independent expert review (Impagliazzo, Paturi, Williams et al.). Analyses (e.g., Szeider, Dias-Lima) note that the certified bounds improve on brute force only for astronomically large n (beyond 10^30 or larger depending on constants). They do not supply lower-bound techniques transferable to the single-tape model, the encoded count map Count_N, or the shortcut-defect ratio α.
- Classical crossing-sequence lower bounds and cumulative-memory methods remain the nearest published techniques. No new transfer lemmas connecting unrestricted circuit size of Count_N to the single-tape CM measure were located. Knowledge-compilation results continue to support the handoff's DNNF/DLDD statements. No literature result supplies a polynomial bound on the shortcut-defect ratio α for arbitrary scalar counters.

## Current project repository state

The private repository j15marti/pnp contains the handoff, prior coordination logs (including 14:16 and 17:18), agent reports under research/agents/, and historical files. Coordination continues via research/coordination and issue #324. No subsequent commits advancing a missing bridge (Tasks A–F of the handoff) have been observed that convert a restricted result into an unrestricted superpolynomial lower bound.

## Recommended next actions

Continue from the handoff Section 28. Priority for the next cycle:

1. Bounds / circuit agent: Attempt an explicit lower bound on C_N, the unrestricted Boolean circuit size of the encoded count map, on any family whose Count_N is not known to be easy (e.g., high-treewidth NAND expanders). Even a weak superlinear bound that exceeds the Pippenger–Fischer simulation ceiling for the target time cap would be progress.
2. Accounting agent: Construct one concrete decoder, record, and event set for a compulsory information-transfer demand that survives the relocation wrapper of handoff Section 13.4.
3. Discovery agent: Define a concrete symmetry or elimination rule used by scalar counters and compute its expansion ratio on the private-leaf tree and affine Tseitin controls.

All work must preserve the distinctions recorded in the handoff (counting versus decision, physical versus descriptive CM, restricted versus unrestricted models, local progress versus large initial value). Finite verification remains non-asymptotic. Claims relying on ETH or similar hypotheses are out of scope for the unconditional objective.

This log records the search and status at the indicated time. It does not advance any mathematical claim.
