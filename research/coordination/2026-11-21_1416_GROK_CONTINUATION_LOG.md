# Continuation log: T5 resource lower bounds

Timestamp: 2026-11-21 14:16 America/Los_Angeles.

## Status of the exhaustive handoff

The exhaustive research handoff remains the authoritative baseline at research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md. Unrestricted superpolynomial exact-counting and decision lower bounds for strict #T5 remain OPEN. The single-tape quadratic time and cubic CM theorems for the sparse matching layouts are audited model-specific results. Representation lower bounds (DNNF, DLDD, positive polynomials) are architecture-specific. P versus NP remains OPEN.

## GitHub and literature search summary

- No public repositories under openai, google-research, or anthropics contain direct work on the strict five-valued T5 relation, the matching-family crossing arguments, or the project's cumulative-memory accounting for exact counting.
- OpenAI/math contains formalizations of subexponential algorithms for k-SAT counting under the claim that ETH is false (October 2025/2026 manuscripts and Lean developments). These are algorithmic upper bounds, not lower-bound techniques transferable to the single-tape model or the encoded count map Count_N.
- Anthropic/formal-math contains a related Lean development of a subexponential 3-SAT counting algorithm. Again, this is an upper-bound claim.
- Classical crossing-sequence lower bounds (Hennie, Hartmanis) and cumulative-memory methods (Beame–Kornerup, ECCC TR23-005) remain the nearest published techniques. No new transfer lemmas connecting unrestricted circuit size of Count_N to the single-tape CM measure were located.
- Knowledge-compilation results (Amarilli et al., Beame–Li–Roy–Suciu) continue to support the handoff's DNNF/DLDD statements for high-treewidth graph predicates. No literature result supplies a polynomial bound on the shortcut-defect ratio α for arbitrary scalar counters.

## Current project repository state

The private repository j15marti/pnp contains the handoff and the prior coordination log of 08:20. No subsequent agent reports or commits advancing a missing bridge (Tasks A–F of the handoff) have been observed in the searchable tree. Issue #324 remains the coordination point.

## Recommended next actions

Continue from the handoff Section 28. Priority for the next cycle:

1. Bounds / circuit agent: Attempt an explicit lower bound on C_N, the unrestricted Boolean circuit size of the encoded count map, on any family whose Count_N is not known to be easy (e.g., high-treewidth NAND expanders). Even a weak superlinear bound that exceeds the Pippenger–Fischer simulation ceiling for the target time cap would be progress.
2. Accounting agent: Construct one concrete decoder, record, and event set for a compulsory information-transfer demand that survives the relocation wrapper of handoff Section 13.4.
3. Discovery agent: Define a concrete symmetry or elimination rule used by scalar counters and compute its expansion ratio on the private-leaf tree and affine Tseitin controls.

All work must preserve the distinctions recorded in the handoff (counting versus decision, physical versus descriptive CM, restricted versus unrestricted models, local progress versus large initial value). Finite verification remains non-asymptotic.

This log records the search and status at the indicated time. It does not advance any mathematical claim.
