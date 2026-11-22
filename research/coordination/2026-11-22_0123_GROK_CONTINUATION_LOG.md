# Continuation log: T5 resource lower bounds

Timestamp: 2026-11-22 01:23 America/Los_Angeles.

## Status

The exhaustive research handoff at research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md remains the current audited baseline. Unrestricted superpolynomial exact-counting and decision lower bounds for strict #T5 remain OPEN. A P versus NP separation remains OPEN.

No new unrestricted superpolynomial lower bound has been established since the prior 00:19 log. Searches of the private repository, public literature, and organizations including OpenAI, Anthropic, and Google Research / DeepMind yielded no results that close any of the missing bridges identified in the handoff.

## Literature and external search summary

- OpenAI (openai/math) and Anthropic (anthropics/formal-math): The October 2026 deterministic subexponential exact #k-SAT algorithms (OpenAI preprint "The Exponential Time Hypothesis is False", revised 25 October; Anthropic "A 2^{o(n)} Time Algorithm for 3-SAT" with Lean formalization) remain the principal public claims. They apply to Boolean CNF formulas, refute ETH under the stated constructions (with Lean under community examination), and do not address the five-valued strict T5 relation C, the sole-tape model, the matching or expander families, or the project's unrestricted scalar-counter bridges. No transfer yielding a polynomial-time separation for strict #T5 was identified.
- Cumulative memory: Beame and Kornerup (arXiv:2301.05680; ICALP 2023; journal version ACM Trans. Comput. Theory 17(3), Article 20, 2025) remains the principal general reference. Its paradigms convert time-space tradeoffs into cumulative-memory bounds of comparable strength for sequential classical and quantum models. No new applications to the project's sole-tape matching families or model-free transfers to unrestricted scalar counters or the encoded Count_N map appeared.
- Knowledge compilation: Restricted Decision-DNNF fragments continue to be studied (e.g., Calì and Razgon, arXiv:2501.03710 on complexity of restricted fragments; Razgon arXiv:2505.16012 on imbalanced conjunctions). Exponential DNNF/DLDD lower bounds for high-treewidth independent-set predicates (Amarilli et al., Beame–Li–Roy–Suciu) remain in force. No unrestricted Boolean circuit-size lower bound for the all-input encoded count function Count_N exceeding the known simulation ceilings (Pippenger–Fischer O(T log T) and distinct-configuration arguments) was located.
- Google organizations (google, google-research, google-deepmind): No public repositories or code matching strict T5, the ternary cycle relation over ℤ_5, sole-tape cumulative-memory accounting, or related resource lower bounds for exact counting were located beyond general algorithmic libraries and formal-conjectures activity unrelated to this problem.
- Pseudoentropy and information transfer: Vadhan–Zheng characterizations remain available. No target-specific conditional pseudoentropy distribution for the strict T5 Count_N map with the required indistinguishability against all cap-sized circuits was located. No compulsory dynamic information-transfer demand surviving input relocation and arbitrary joint computation appears in the literature.
- No literature clue was identified that supplies a missing bridge for unrestricted superpolynomial exact counting of strict #T5.

## Repository state

Authenticated user: j15marti. The private repository j15marti/pnp holds the handoff, prior coordination logs (including the 00:19 PST entry), and historical research files. Coordination continues via the research/coordination directory.

## Next recommended actions

The bridge targets enumerated in the handoff Section 24 remain the appropriate focus:
- Circuit lower-demand invariant or computational pseudoentropy pair for the encoded count map Count_N on a suitable distribution or high-treewidth family.
- Compulsory dynamic information-transfer demand that survives input relocation, caching, and arbitrary joint computation.
- Controlled shortcut-defect analysis for a concrete scalar operation against the typed DLDD completion potential, retaining the initial lower bound on high-width graphs.
- Construction of a decision-sensitive family outside the easy matching-cycle and affine/Tseitin cases already identified.
- Independent counterexample testing of any new claim against the private-leaf tree, high-width affine systems, complement, forced domains, memoization, and input relocation.

All subsequent work must preserve the audited distinctions between the original transport matching family, the later NAND matching family, the separate decision pinning family, and the high-treewidth expander families; between counting and decision; between physical and descriptive CM; and between restricted representation lower bounds and unrestricted scalar counters. Finite audits remain computational evidence only.

This log records the search results, recent activity summary, and status. It advances no mathematical claim.
