# Grok continuation log: strict T5 resource lower bounds

Timestamp: 2026-11-22 19:14 America/Los_Angeles.

## Searches performed this cycle

- Authenticated as j15marti. Confirmed private repository j15marti/pnp holds the exhaustive handoff (research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md), prior Grok logs (including 2026-11-22_1317), and recent status notes on CM forbidden regions and T5/T_q extensions.
- Code search within the repository and across GitHub for strict T5, cumulative memory, and related terms returned only project-internal results.
- Organization searches (openai/math, anthropics/formal-math, google-research): located the October 2026 AI-generated manuscripts claiming deterministic subexponential exact #k-SAT algorithms (OpenAI: (n+m)^{O_k(1)} 2^{n/(log n)^{1/2+o(1)}} with Lean formalization of a weaker bound; Anthropic: 2^{O(n log log n / \sqrt log n)} with Lean 4 kernel-checked formalization). No work on the five-valued strict T5 relation C or the project's matching-family constructions.
- Literature searches: confirmed Beame–Kornerup ICALP 2023 cumulative-memory lower bounds (generic conversion of time-space tradeoffs); classical one-tape crossing-sequence results; DNNF/DLDD exponential lower bounds for high-treewidth independent-set and Tseitin predicates remain representation-specific. No unrestricted superpolynomial lower bound for the encoded Count_N map of general strict #T5 or #SAT.

## Key findings

The OpenAI and Anthropic October 2026 preprints (with accompanying Lean developments) claim algorithms that would refute ETH (and related hypotheses) by counting k-CNF solutions in subexponential time. Independent expert review (including Impagliazzo, Paturi, Williams) is ongoing as of this date. The claimed bounds are galactic: crossover points where they improve on exhaustive search or best known algorithms require astronomically large n (e.g., >2^{131071} in one analysis). The manuscripts note that the speedup does not transfer through arbitrary polynomial reductions. These are algorithmic upper bounds only; they supply no technique for the project's missing bridges (unrestricted Count_N circuit size, compulsory dynamic information transfer, shortcut-defect control, etc.).

Recent project notes (CM_Forbidden_Region_Status_2026-11-22.md, Additional_T5_Tq_Forbidden_Regions_2026-11-22.md) establish scoped polynomial CM and simultaneous time-workspace exclusions via FLMV/Williams transfers and streaming arguments on pin gadgets, all under explicit model assumptions. They do not yield superpolynomial separations or unrestricted lower bounds.

## Status relative to the handoff

The exhaustive research handoff remains the authoritative baseline. Unrestricted superpolynomial exact-counting and decision lower bounds for strict #T5 remain OPEN. Model-specific single-tape T=\Omega(N^{2}) and CM=\Omega(N^{3}) for sparse matching layouts are retained as audited project theorems. Representation lower bounds (DNNF, DLDD, positive polynomials) are architecture-specific. P versus NP remains OPEN. No unconditional superpolynomial claim is advanced.

The claimed ETH refutations, even if verified, remove a common conditional-hardness premise but do not resolve the unrestricted scalar-counter case or produce a polynomial-size unrestricted circuit for Count_N on hard families.

## Next concrete tasks (priority unchanged)

1. Bounds / circuit: seek any explicit lower bound on C_N (unrestricted Boolean circuit size of the encoded count map) exceeding the Pippenger–Fischer simulation ceiling for a target polynomial cap, on a family not known to be easy (high-treewidth NAND expanders). Check against affine/Tseitin controls.
2. Accounting: construct one concrete compulsory information-transfer demand (decoder, record, event set, reuse factor) that survives the relocation wrapper of handoff Section 13.4.
3. Discovery: define one concrete scalar-counter operation (symmetry quotient, elimination rule, or algebraic transform) and compute its expansion ratio on the private-leaf tree and affine Tseitin examples.

All work must preserve the distinctions recorded in the handoff (symmetric C vs ordered R, transport vs NAND matching, count vs decision, witness predicate vs count map, etc.). Finite verification remains non-asymptotic. Claims relying on ETH or similar hypotheses are out of scope for the unconditional objective.

This log is an additive research record. It does not promote any theorem.
