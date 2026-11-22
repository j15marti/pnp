# Continuation log: T5 resource lower bounds

Timestamp: 2026-11-22 08:21 America/Los_Angeles.

## Status

The exhaustive research handoff at research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md remains the current audited baseline. Unrestricted superpolynomial exact-counting and decision lower bounds for strict #T5 remain OPEN. A P versus NP separation remains OPEN.

No new unrestricted superpolynomial lower bound has been established since the prior 07:22 log. Incremental agent reports continue under research/agents/ (charged-accounting, charged-bounds, etc.), advancing controls, falsifying candidate residual portfolios and shortcut ratios, and refining decoders, but none closes a missing universal bridge from the handoff Section 24.

## Literature and external search summary

- OpenAI (openai/math) and Anthropic (anthropics/formal-math): The October 2026 subexponential deterministic exact-counting algorithms for k-CNF (form 2^{O(n log log n / sqrt(log n))}, with Lean formalizations claiming ETH false) remain the principal related public results. They apply to Boolean CNF and do not transfer to the sole-tape sparse matching families, high-treewidth NAND/expander families, or the unrestricted encoded Count_N map for the five-valued strict T5 relation. Independent expert review continues; the algorithms are galactic for practical n and do not resolve P versus NP. No new updates identified in this cycle.
- Cumulative memory: Beame and Kornerup (ACM Trans. Comput. Theory 17(3), Article 20, 2025; DOI 10.1145/3728715; ICALP 2023 preliminary) remains the principal general reference converting time-space tradeoffs into matching-strength CM bounds for classical and quantum models. No new sole-tape or CSP-specific applications to exact counting of restricted five-valued templates were identified.
- Knowledge compilation and circuits: No new unrestricted Boolean circuit-size lower bound for the all-input Count_N function of the encoded strict T5 instances. Restricted DNNF/DLDD exponential lower bounds for high-treewidth independent-set and Tseitin predicates continue to hold via prior published results (Amarilli et al., Beame-Li-Roy-Suciu, de Colnet-Mengel, Itsykson et al.). No literature result supplies a polynomial bound on the shortcut-defect ratio α for arbitrary scalar counters.
- Google organizations (google, google-research, google-deepmind): No public matches for the strict five-valued T5 cycle relation over Z_5, sole-tape cumulative-memory accounting, matching-family crossing arguments, or related exact-counting resource lower bounds. (Public "T5" results continue to refer predominantly to the text-to-text transformer or unrelated cryptographic/graph-theoretic objects.)
- Pseudoentropy, information transfer, and circuit completion: No target-specific conditional pseudoentropy distribution for the strict T5 Count_N map that is indistinguishable to all cap-sized circuits, nor a compulsory dynamic information-transfer demand that survives input relocation (handoff Section 13.4), caching, and arbitrary joint computation, was located. The unrestricted Boolean completion potential for Count_N retains the local substitution property but still lacks a large initial value.
- No literature clue was identified that supplies a missing bridge for unrestricted superpolynomial exact counting of strict #T5 or a decision-sensitive superpolynomial tradeoff.

## Repository state

Authenticated user: j15marti. The private repository j15marti/pnp holds the handoff, prior coordination logs (most recent prior: 2026-11-22_0722), and continuing agent activity under research/agents/. Coordination continues via the research/coordination directory. Issue #324 remains the active assignment tracker for the staggered charged agents.

## Next recommended actions

The bridge targets enumerated in the handoff Section 24 remain the appropriate focus for the next cycle:
- Bounds/circuit agent: Attempt an explicit lower bound on C_N (unrestricted Boolean circuit size of the encoded count map) for a high-treewidth NAND/expander family under the explicit bit encoding, or construct a concrete pseudoentropy pair indistinguishable against circuits of size O(N^a log N).
- Accounting agent: Construct one concrete decoder, record, event set, and reuse factor for a compulsory information-transfer demand that survives the relocation wrapper.
- Discovery/construction agents: Define a concrete symmetry, elimination, or algebraic transform used by scalar counters; compute its expansion ratio α on the private-leaf tree and affine Tseitin controls while retaining the typed DLDD initial lower bound on high-width graphs.
- All agents: Independently test any candidate lemma against the private-leaf tree, high-width affine systems, complement, forced domains, memoization, variable renaming, and input relocation. Record refuted candidates explicitly.

All subsequent work must preserve the audited distinctions between the original transport matching family, the later NAND matching family, the separate decision pinning family, and the high-treewidth expander families; between counting and decision; between physical and descriptive CM; and between restricted representation lower bounds and unrestricted scalar counters. Finite audits remain computational evidence only. Claims relying on ETH, SETH, or similar hypotheses remain out of scope for the unconditional objective.

This log records the search results, recent activity summary, and status at the indicated time. It advances no mathematical claim.
