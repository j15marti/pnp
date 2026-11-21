# Continuation log: T5 resource lower bounds

Timestamp: 2026-11-21 12:16 America/Los_Angeles.

## Status

The exhaustive research handoff at research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md remains the current audited baseline. Unrestricted superpolynomial exact-counting and decision lower bounds for strict #T5 remain OPEN. A P versus NP separation remains OPEN.

Recent agent activity on 2026-11-21 includes Bounds reports falsifying certain marginal-matched and split-quotient pseudoentropy pairs (e.g., PNP_Charged_bounds_2026-11-21_120300_Marginal_Matched_Pair.md), Synthesis reports on quotient budgets and terminal defects, Construction reports on positive-offset pairs and three-color encodings, Redteam audits of scope contexts and circuit/CM reconstructions, and Discovery reports on extremal-count closure and scope-restricted renaming. These constitute incremental controls and failed candidate bridges rather than a completed universal theorem. No new unrestricted superpolynomial lower bound has been established.

## Literature and external search summary

- Cumulative memory: Beame and Kornerup (arXiv:2301.05680, ICALP 2023, later journal version) provide general methods converting time-space tradeoff lower bounds into cumulative-memory bounds for sequential classical models and quantum circuits. These are consistent with the project's sole-tape matching-family CM theorems but do not supply a model-free transfer to unrestricted scalar counters or close the gap for the encoded Count_N map.
- Knowledge compilation: Amarilli et al. (arXiv:1811.02944) and related structured Decision-DNNF results continue to support the handoff's exponential DNNF/DLDD lower bounds in treewidth for bounded-degree high-treewidth independent-set predicates. No results were located that lower-bound unrestricted Boolean circuit size for the all-input encoded count function.
- #CSP and exact counting: Structural dichotomies (Bulatov et al.) classify tractability for #CSP under polymorphisms; the project's fixed symmetric ternary relation C is NP-complete for decision via the audited circuit reduction, with no new polynomial-time exact-counting algorithm identified for the hard families.
- Pseudoentropy: Vadhan-Zheng characterizations and related chain-rule lower bounds (e.g., Pietrzak-Skorski) remain general; no target-specific conditional pseudoentropy distribution for the strict T5 Count_N map with the required indistinguishability against cap-sized circuits was identified in the literature or public repositories.
- OpenAI math repository: Contains formalizations claiming subexponential exact #k-SAT algorithms (refuting ETH under those constructions) and related Lean developments. These supply upper-bound context for sparse or bounded-width formulas but do not address the five-valued strict T5 relation, sole-tape resource accounting, matching or expander families, or the missing unrestricted bridges.
- Google Research and Anthropic organizations: Public repository and code searches yielded no results on strict T5, the specific ternary cycle relation over Z_5, single-tape cumulative-memory lower bounds, or related resource-accounting approaches to exact counting.
- No literature clue was identified that supplies a compulsory information-transfer demand surviving input relocation and arbitrary joint computation, a suitable target-specific pseudoentropy pair, or an unrestricted count-circuit lower bound exceeding the known simulation ceilings (Pippenger-Fischer and distinct-configuration arguments).

## Repository state

Authenticated user: j15marti. The private repository j15marti/pnp holds the handoff, prior coordination logs (including 08:20, 10:15, and 11:17 PST entries), agent role reports under research/agents/, and historical research files. Coordination continues via the research/coordination directory. Issue #324 remains the coordination point for staggered agent offsets.

## Next recommended actions

The bridge targets enumerated in the handoff Section 24 remain the appropriate focus:
- Circuit lower-demand invariant or computational pseudoentropy pair for the encoded count map Count_N on a suitable distribution or high-treewidth family.
- Compulsory dynamic information-transfer demand that survives input relocation, caching, and arbitrary joint computation.
- Controlled shortcut-defect analysis for a concrete scalar operation against the typed DLDD completion potential, retaining the initial lower bound on high-width graphs.
- Construction of a decision-sensitive family outside the easy matching-cycle and affine/Tseitin cases already identified.
- Independent counterexample testing of any new claim against the private-leaf tree, high-width affine systems, complement, forced domains, memoization, and input relocation.

All subsequent work must preserve the audited distinctions between the original transport matching family, the later NAND matching family, the separate decision pinning family, and the high-treewidth expander families; between counting and decision; between physical and descriptive CM; and between restricted representation lower bounds and unrestricted scalar counters. Finite audits remain computational evidence only.

This log records the search results, recent activity summary, and status. It advances no mathematical claim.
