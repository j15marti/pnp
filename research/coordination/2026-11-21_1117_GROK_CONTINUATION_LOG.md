# Continuation log: T5 resource lower bounds

Timestamp: 2026-11-21 11:17 America/Los_Angeles.

## Status

The exhaustive research handoff at research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md remains the current audited baseline. Unrestricted superpolynomial exact-counting and decision lower bounds for strict #T5 remain OPEN. A P versus NP separation remains OPEN. No new agent reports advancing a universal bridge have been identified since the 10:15 log.

## Literature and external search summary

- Cumulative memory literature: Beame and Kornerup (arXiv:2301.05680) establish general methods converting time-space tradeoff lower bounds into cumulative-memory bounds for classical sequential models and quantum circuits. These are consistent with, but independent of, the project's sole-tape CM theorems for the matching families; no stronger model-free transfer applicable to unrestricted scalar counters appears.
- Knowledge compilation and width parameters: Amarilli, Capelli, Monet, and Senellart (arXiv:1811.02944 and related) and subsequent works on structured Decision-DNNF continue to support exponential lower bounds in treewidth for bounded-degree monotone CNFs, which the handoff applies to high-treewidth independent-set predicates. No results close the gap to unrestricted Boolean circuit size for the encoded Count_N map.
- #CSP dichotomies: Bulatov's work on Mal'tsev polymorphisms and strong balance criteria for #CSP remains the relevant structural classification; the project's fixed symmetric ternary relation C is treated as a specific NP-complete decision problem via the circuit reduction, without new tractability results for exact counting.
- OpenAI math repository (openai/math): Contains formalizations of subexponential algorithms for exact #k-SAT (refuting ETH under the claimed constructions) and related circuit lower-bound consequences. These provide upper-bound context for sparse or bounded-width formulas but do not address the five-valued strict T5 relation, sole-tape resource accounting, or the missing unrestricted bridges. No direct treatment of the project's matching or expander families was located.
- Google and Anthropic organizations: Public code and repository searches yielded no results on strict T5, the specific ternary cycle relation over Z_5, single-tape cumulative-memory lower bounds, or related resource-accounting approaches to exact counting.
- No literature clue was identified that supplies a compulsory information-transfer demand surviving input relocation and arbitrary joint computation, a target-specific conditional pseudoentropy distribution for Count_N, or an unrestricted count-circuit lower bound exceeding the known simulation ceilings (Pippenger-Fischer and distinct-configuration arguments).

## Repository state

Authenticated user: j15marti. The private repository j15marti/pnp holds the handoff, prior coordination logs, agent role definitions, and historical research files. Coordination continues via the research/coordination directory.

## Next recommended actions

The bridge targets enumerated in the handoff Section 24 and reiterated in the 10:15 log remain the appropriate focus:
- Circuit lower-demand or pseudoentropy pair for the encoded count map Count_N.
- Compulsory dynamic information-transfer demand that survives relocation and caching.
- Controlled shortcut-defect analysis for a concrete scalar operation against the typed DLDD completion potential.
- Construction of a decision-sensitive family outside the easy cases already identified.
- Counterexample testing of any new claim against the private-leaf tree, affine/Tseitin systems, complement, forced domains, and input relocation.

All subsequent work must preserve the audited distinctions between the original transport matching family, the later NAND matching family, the separate decision pinning family, and the high-treewidth expander families; between counting and decision; and between restricted representation lower bounds and unrestricted scalar counters.

This log records the search results and status. It advances no mathematical claim.
