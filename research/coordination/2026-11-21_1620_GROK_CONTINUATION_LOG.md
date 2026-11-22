# Continuation log: T5 resource lower bounds

Timestamp: 2026-11-21 16:20 America/Los_Angeles.

## Status

The exhaustive research handoff at research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md remains the current audited baseline. Unrestricted superpolynomial exact-counting and decision lower bounds for strict #T5 remain OPEN. A P versus NP separation remains OPEN.

No new unrestricted superpolynomial lower bound has been established since the prior 13:15 log. Agent activity continues to produce incremental controls, failed candidate bridges, and scope audits rather than a completed universal theorem.

## Literature and external search summary

- Cumulative memory lower bounds: The Beame–Kornerup framework (arXiv:2301.05680; ICALP 2023; ACM TOCT 2025) remains the principal general reference converting time-space tradeoffs into cumulative-memory bounds. It is compatible with the project's sole-tape matching-family results but supplies no model-free transfer to unrestricted scalar counters or the encoded Count_N map. Recent journal version confirms the classical and quantum paradigms.
- Knowledge compilation and representation: Recent work on restricted Decision-DNNF fragments (e.g., Razgon arXiv:2505.16012 on imbalanced conjunctions) continues to examine structured variants relative to treewidth. Distributed compilation frameworks for d-DNNF (arXiv:2607.13642) address scalability but do not alter the exponential lower bounds for high-treewidth independent-set predicates. The handoff's DNNF/DLDD exponential lower bounds, derived from Amarilli et al. and Beame–Li–Roy–Suciu, remain supported; no unrestricted Boolean circuit-size lower bound for the all-input encoded count function has appeared.
- #CSP and exact counting: Structural dichotomies for #CSP continue to classify tractability via polymorphisms. The fixed symmetric ternary relation C is NP-complete for decision by the audited Boolean-circuit reduction; no new polynomial-time exact-counting algorithm for the hard matching or expander families was identified. OpenAI (openai/math) and Anthropic (anthropics/formal-math/eth) preprints claim subexponential exact #k-SAT algorithms (refuting ETH under those constructions) with Lean formalizations; these provide upper-bound context for sparse or bounded-width formulas but do not address the five-valued strict T5 relation, sole-tape resource accounting, the matching or expander families, or the missing unrestricted bridges. Follow-up repositories (e.g., eth-hamiltonicity, NotETHSimplified, eth-constants) refine constants or extend to related counting problems under the same assumptions.
- Pseudoentropy: General characterizations (Vadhan–Zheng and related chain-rule results) remain available. No target-specific conditional pseudoentropy distribution for the strict T5 Count_N map, with the required indistinguishability against cap-sized circuits, was located.
- Google Research and Anthropic organizations: Public repository and code searches yielded no results on strict T5, the specific ternary cycle relation over ℤ_5, single-tape cumulative-memory lower bounds, or related resource-accounting approaches to exact counting beyond the ETH-related formalizations noted above.
- No literature clue was identified that supplies a compulsory information-transfer demand surviving input relocation and arbitrary joint computation, a suitable target-specific pseudoentropy pair, or an unrestricted count-circuit lower bound exceeding the known simulation ceilings (Pippenger–Fischer and distinct-configuration arguments).

## Repository state

Authenticated user: j15marti. The private repository j15marti/pnp holds the handoff, prior coordination logs (including the 13:15 PST entry), agent role reports under research/agents/, and historical research files. Coordination continues via the research/coordination directory.

## Next recommended actions

The bridge targets enumerated in the handoff Section 24 remain the appropriate focus:
- Circuit lower-demand invariant or computational pseudoentropy pair for the encoded count map Count_N on a suitable distribution or high-treewidth family.
- Compulsory dynamic information-transfer demand that survives input relocation, caching, and arbitrary joint computation.
- Controlled shortcut-defect analysis for a concrete scalar operation against the typed DLDD completion potential, retaining the initial lower bound on high-width graphs.
- Construction of a decision-sensitive family outside the easy matching-cycle and affine/Tseitin cases already identified.
- Independent counterexample testing of any new claim against the private-leaf tree, high-width affine systems, complement, forced domains, memoization, and input relocation.

All subsequent work must preserve the audited distinctions between the original transport matching family, the later NAND matching family, the separate decision pinning family, and the high-treewidth expander families; between counting and decision; between physical and descriptive CM; and between restricted representation lower bounds and unrestricted scalar counters. Finite audits remain computational evidence only.

This log records the search results, recent activity summary, and status. It advances no mathematical claim.
