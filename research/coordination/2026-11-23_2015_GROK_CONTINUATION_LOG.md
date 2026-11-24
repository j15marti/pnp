# Continuation log: T5 resource lower bounds

Timestamp: 2026-11-23 20:15 America/Los_Angeles.

## Status

The exhaustive research handoff at research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md remains the current audited baseline. Unrestricted superpolynomial exact-counting and decision lower bounds for strict #T5 remain OPEN. A P versus NP separation remains OPEN.

Repository activity continues under research/agents/ with charged-accounting, charged-bounds, and related reports dated through 2026-11-23. These consist of incremental ledger analyses, controls against known counterexamples (private-leaf trees, affine/Tseitin systems, complement, forced domains, relocation), and candidate constructions. No completed universal bridge for unrestricted scalar counters appears. Coordination issue #324 remains open with 170 comments.

## Literature and external search summary

- OpenAI (openai/math): The October 25 2026 preprint and accompanying Lean formalization in SubexponentialSAT claim a deterministic exact #k-SAT algorithm running in (n+m)^{O_k(1)} 2^{O_k(n log log n / sqrt(log n))} time, refuting ETH, SETH, Gap-ETH, NSETH, and #ETH under the stated constructions. Community discussion and partial ports exist (e.g., mathcommunity, ProveIt, eth-constants). These are upper bounds for sparse/bounded-width CNF; they do not address the five-valued strict T5 relation C, the sole-tape model, matching or expander families, or the missing unrestricted bridges for Count_N. Independent academic verification remains incomplete as of this date.
- Anthropic (anthropics/formal-math): Related Lean developments claim a comparable 2^{o(n)} algorithm for 3-SAT/#3-SAT. Same scope limitations relative to the T5 project.
- Google organizations (google, google-research, google-deepmind): No public repositories or code matching strict T5, the ternary cycle relation over Z_5, sole-tape cumulative-memory accounting, or related resource lower bounds for exact counting were located beyond general algorithmic libraries.
- Knowledge compilation: Existing DNNF/DLDD exponential lower bounds for high-treewidth independent-set and Tseitin predicates (Amarilli et al., Beame-Li-Roy-Suciu, de Colnet-Mengel, Itsykson et al.) remain in force for representation classes. No new results lowering the unrestricted Boolean circuit size of the encoded count map Count_N below the known simulation ceilings (Pippenger-Fischer O(T log T), distinct-configuration arguments) were identified.
- Cumulative memory: Beame-Kornerup (ICALP 2023 / TOCT 2025) remains the principal general reference; no applications to the project's sole-tape matching families or unrestricted scalar counters were found.
- Pseudoentropy and information transfer: Vadhan-Zheng characterizations remain available. No target-specific conditional pseudoentropy distribution for the strict T5 Count_N map with the required indistinguishability against all cap-sized circuits was located. No compulsory dynamic information-transfer demand surviving input relocation and arbitrary joint computation appears in the literature.
- Transformer counting results (e.g., arXiv:2407.15160) address embedding-dimension vs. vocabulary bottlenecks for token counting; they do not transfer to the constraint-satisfaction counting setting of the handoff.
- No literature clue was identified that supplies a missing bridge for unrestricted superpolynomial exact counting of strict #T5.

## Repository state

Authenticated user: j15marti. The private repository j15marti/pnp holds the handoff, prior coordination and research logs, agent role reports under research/agents/, and historical research files. Coordination continues via the research/coordination directory and issue #324.

## Next recommended actions

The bridge targets enumerated in the handoff Section 24 remain the appropriate focus:
- Unrestricted encoded-count circuit size C_N exceeding N^a log N for a suitable family.
- Target-specific computational pseudoentropy pair for Count_N.
- Compulsory dynamic information-transfer demand that survives input relocation, caching, and arbitrary joint computation.
- Controlled shortcut-defect analysis for a concrete scalar operation against the typed DLDD completion potential on high-width graphs.
- Decision-sensitive family outside the easy matching-cycle and affine/Tseitin cases.

All subsequent work must preserve the audited distinctions between the original transport matching family, the later NAND matching family, the separate decision pinning family, and the high-treewidth expander families; between counting and decision; between physical and descriptive CM; and between restricted representation lower bounds and unrestricted scalar counters. Finite audits remain computational evidence only. ETH/#ETH claims supply upper bounds and must not be used as premises for unconditional lower bounds.

This log records the search results, recent activity summary, and status. It advances no mathematical claim.
