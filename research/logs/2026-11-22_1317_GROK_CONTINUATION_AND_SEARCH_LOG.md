# Grok continuation log: strict T5 resource lower bounds

Timestamp: 2026-11-22 13:17 America/Los_Angeles.

## Searches performed this cycle

- Authenticated GitHub user: j15marti. Located repository j15marti/pnp containing the exhaustive handoff, prior coordination logs, and research files.
- Code search across GitHub for strict T5, cumulative memory, crossing sequences: results limited to the pnp repository itself.
- Organization searches (openai, anthropics, google-research): no direct work on the five-valued strict T5 relation or the project's matching-family crossing / CM accounting.
- Literature: recent preprints on counting CSP dichotomies, DNNF lower bounds for high-treewidth formulas, treewidth-parameterized counting algorithms under #SETH, and the October 2026 OpenAI/Anthropic claims of subexponential deterministic exact #k-SAT algorithms.

## Key findings

OpenAI (openai/math preprint 25 October 2026) and Anthropic (anthropics/formal-math/eth, Claude-credited manuscript) both present deterministic algorithms claiming to count satisfying assignments of k-CNF formulas in time 2^{O(n log log n / \sqrt log n)} · poly_k(n, m). Both are accompanied by Lean 4 formalizations (kernel-checked under standard axioms). These are algorithmic upper bounds. Independent expert review remains ongoing. The bounds are galactic; practical improvement over brute force occurs only for astronomically large n. The manuscripts explicitly note that the speedup does not transfer through arbitrary polynomial reductions to all of NP.

No literature or public repository supplies an unrestricted superpolynomial lower bound for the encoded count map Count_N of general strict T5 (or #SAT). DNNF/DLDD exponential lower bounds for high-treewidth independent-set and Tseitin predicates remain representation-specific. Beame–Kornerup cumulative-memory results convert certain time-space tradeoffs into CM bounds of matching strength, but do not resolve the unrestricted scalar-counter case. Classical one-tape crossing-sequence quadratic lower bounds are consistent with the project's audited matching-family theorems.

## Status relative to the handoff

The exhaustive research handoff (research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md) remains the authoritative baseline. Unrestricted superpolynomial exact-counting and decision lower bounds for strict #T5 remain OPEN. Model-specific single-tape T = \Omega(N^{2}) and CM = \Omega(N^{3}) for the sparse matching layouts are retained as audited project theorems. Representation lower bounds are architecture-specific. P versus NP remains OPEN. No unconditional superpolynomial claim is advanced.

The ETH-refutation claims, if correct, remove a common conditional-hardness premise but supply no lower-bound technique for the project's missing bridges (Tasks A–F). In particular, they do not produce a polynomial-size unrestricted circuit for Count_N on high-treewidth families, nor do they bound the shortcut-defect ratio \alpha for arbitrary scalar counters.

## Next concrete tasks (unchanged priority)

1. Bounds / circuit: seek any explicit lower bound on C_N (unrestricted Boolean circuit size of the encoded count map) exceeding the Pippenger–Fischer simulation ceiling for a target polynomial cap, on a family not known to be easy (high-treewidth NAND expanders). Check against affine/Tseitin controls.
2. Accounting: construct one concrete compulsory information-transfer demand (decoder, record, event set, reuse factor) that survives the relocation wrapper of handoff Section 13.4.
3. Discovery: define one concrete scalar-counter operation (symmetry quotient, elimination rule, or algebraic transform) and compute its expansion ratio on the private-leaf tree and affine Tseitin examples.

All work must preserve the distinctions recorded in the handoff. Finite verification remains non-asymptotic. Claims relying on ETH or similar hypotheses are out of scope for the unconditional objective.

This log is an additive research record. It does not promote any theorem.
