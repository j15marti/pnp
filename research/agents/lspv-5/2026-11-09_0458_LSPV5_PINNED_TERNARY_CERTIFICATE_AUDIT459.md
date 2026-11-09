# LSPV-5/459: independent audit of the pinned ternary-path Resolution certificate

**2026-11-09 04:58 PST | Route B independent red team | PROVED/RESTRICTED audit + COMPUTATIONAL replay. P versus NP OPEN.**

This run audits peer node **[P2-L3-532]**. It changes no tracker status. Load-bearing nodes **[P2-D1]**, **[P2-C3]**, **[P2-B1]**, and **[P2-B2]** remain OPEN; previous LSPV-5 node **[P2-L5-458]** is unchanged. Route-A nodes **[P1-01]**, **[P1-03]**, and **[P1-04]** remain OPEN.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis.** The weakest proposed B3 bridge still hides a reflection premise: a locally valid rejecting machine trace does not become an $R_{mix341}$ refutation unless the fixed calculus proves the traced machine correct on every SAT input.

**Predeclared falsifiers.** (F1) the authenticated historical grammar contains a generic reflection rule with a polynomial simulation; (F2) a peer artifact constructs accepted bytes for every polynomial SAT decider with source binding and proved polynomial cost; (F3) a primary theorem supplies that simulation for this exact fixed calculus; (F4) the project already proved the same obstruction, so the proposed advance is duplicate.

**Search changed the target.** F4 fired. The exact trace/reflection obstruction is already developed in `research/main/2026-11-04_2048_MAIN_FRESH-WIRE-PROVENANCE-B3-REFLECTION-FIREWALL-REFEREE353.md` and `research/main/2026-11-07_0455_MAIN_B3_IDENTITY_SIMULATION_REFEREE409.md`. This run does not relabel it as progress. The revised, falsifiable target was to independently authenticate the newly published ordinary-Resolution certificate [P2-L3-532], reject malformed variants, and test whether its claimed linear upper control survives reconstruction from the original strict 3-CNF source.

## Continuity and search record

Read both full trackers: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; final `proof2.txt` blob `7549db233db857f131811ab80ac4de6ab620fcab` (the latter includes [P2-L3-532] and peer [P2-L4-519]). Read current issue #3 metadata; comment enumeration failed with `Transport closed` on the 1,470-comment thread and is reported rather than disguised. Read the 2026-11-02 governing five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, the current knot/link handoff blob `0289edb73d1e38492f0693844667be59d4152785`, AGENTS.md blob `4ae902888754d0b06ba4ce1aaeca0657a92b46a9`, CODEX.md blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, the research instructions and protocol, peer LSPV-3/532 report blob `03be13610552668d2f92183dca3e8c6ef4316904`, peer generator blob `1ffb5122a29a61cf98a1e158162dda055355a560`, peer raw blob `fe4ab8c1eeb042e3ed6dfae2b059feca515b3bcd`, and LSPV-4/519 report blob `d0daf3a10a06cc966db2328f16b4a056ef5514db`.

Actual external assessment files read: `GROKPROOF/2026-11-09_1230_PROGRESS.md` blob `0ee19c6b2fdf92b64427ab737fe563346779c828` and `research/agents/claude/world-ledger/README.md` blob `de75a371ce3143a4495e6892df7fb04794a6b708`. Neither supplies an $R_{mix341}$ normalization or B3 bridge.

Change-aware required-repository heads were unchanged: `konard/p-vs-np` `ecedd2b45f1c524d85c00b2da27a9c140025550c`; `blkph0x/p-vs-np-proof-research` `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; `meelgroup/frat-xor` `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; `tanyongkiam/cake_lpr` `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`; `MassimoLauria/cnfgen` `24e633bdbed0d0998493bee99c42faf480c7dc96`; `openai/math` `4eaee87548250b2682affda7d05d947c05554bae`. Targeted GitHub search found CNFgen's actual Tseitin generator at `cnfgen/families/tseitin.py`; the konard query was rate-limited (HTTP 429), and the other targeted exact-term searches returned no relevant fixed-calculus result. No separate Google-branded engine was available; general web search was used and logged.

Primary controls read at source: Haken, *The intractability of resolution* (1985), DOI `10.1016/0304-3975(85)90144-6`, for pigeonhole ordinary-Resolution hardness; Cook-Reckhow, *The Relative Efficiency of Propositional Proof Systems* (1979), DOI `10.2307/2273702`, for proof-system relativity; and Itsykson-Riazanov-Smirnov, *Tight Bounds for Tseitin Formulas* (SAT 2022), DOI `10.4230/LIPIcs.SAT.2022.6`, for treewidth-sensitive regular-Resolution bounds. These are model-specific controls, not full-mixed-calculus results.

## Independent theorem audit

For $k\ge1$, peer [P2-L3-532] uses $2k+1$ ternary one-hot groups on a signed modular-three path. Its original source contains one positive ALO per group, the 18 wrong-charge proper ternary clauses per path vertex, and four proper ternary clauses for each of $k+2$ boundary-pin gadgets. The exact counts reconstructed independently are

$$
n=8k+7,\qquad m=(2k+1)+18k+4(k+2)=24k+9.
$$

The verifier does not trust peer tags or clauses. It reconstructs every expected signed source clause from $k$, requires dense unique source IDs, distinct noncomplementary literals in every original width-three clause, and checks every Resolution node against earlier parent IDs with the published orientation $p\in A$, $-p\in B$. It then recomputes the resolvent, rejects tautologies, checks the terminal empty clause, source ancestry, and dependency depth.

All seven published controls $k\in\{1,2,3,4,5,8,12\}$ passed exactly:

$$
W_{exhibited}=9k+3,\quad references=18k+6,\quad span=4k+1,\quad source\ ancestors=7k+6.
$$

The $7k+6$ ancestors are the union of $4(k+2)$ pin facets, $3(k-1)$ propagation sources, and one final forbidden row. Shared parents are charged once; no branch-local context, split rule, weakening, or discharge is used. This is a valid source-authenticated ordinary-Resolution DAG in the implemented schema.

Six adversarial mutations per instance were rejected: reversed pivot, forward/self reference, forged final clause, altered source literal, false empty-node pointer, and duplicate source ID, for **42/42 rejections**. For each instance, independently deleting the first facet of the final pin gadget admitted the closed-form satisfying assignment in which every edge takes residue zero and all pin auxiliaries are false. Thus the test is not succeeding on an already-unsound source.

The run's independent verifier completed seven instances and all corruptions in 0.66 host seconds. At $k=12$ it checked 103 variables, 297 original clauses, 111 paid Resolution nodes, 222 references, span 49, and 90 distinct source ancestors. The Python verifier is 6,906 bytes; raw output is 1,963 bytes. These host measurements include interpreter overhead, are not minimum proofs, and do not establish native $R_{mix341}$ byte acceptance.

## Revised claim and classification

**PROVED/RESTRICTED confirmation.** The peer certificate is internally correct under its explicit ordinary-Resolution schema. It gives a linear upper bound for this source-pinned path family. It also confirms that the exponential no-auxiliary *flat representation* of the unpinned boundary relation [P2-L3-530] is not a proof-work lower bound after source pins are supplied: legal Resolution can propagate one state and ignore most source clauses.

**Not proved.** The audit does not establish shortest proof size, acceptance by the still-open historical mixed byte grammar [P2-D1], a simulation of all mixed rules [P2-C3], any superpolynomial $\overline W_R$ lower bound [P2-B1], or B3 [P2-B2]. It is a **family upper control / family-failure classification**, not a B1 or B2 counterexample and not hardness against all algorithms. Haken's pigeonhole lower bound and expander Tseitin controls remain restricted to their stated systems; Cook extended proof mechanisms and algebraic shortcuts remain mandatory controls.

## Publication and trackers

Artifacts: `experiments/review/lspv5_459_pinned_path_trace_audit.py`; raw `results/raw/arc/2026-11-09_0458_LSPV5_459_PINNED_PATH_AUDIT_RAW.json`; handoff `research/coordination/2026-11-09_0458_LSPV5_PINNED_PATH_AUDIT459_HANDOFF.md`; issue outbox `outbox/2026-11-09_0458_LSPV5_459_ISSUE3_OUTBOX.md`.

Local preflight failed because this partial scratch checkout lacks root `main.tex`, AGENTS.md, CODEX.md, and the repository skill file; the authoritative remote versions were read directly. The remote root `main.tex` remains unreadable as a complete nonempty blob, so it was not edited. Historical grammar, weights, agents, IDs, titles, schedules, enabled states, and two-Route-A/three-Route-B allocation are unchanged.

**TRACKERS REVIEWED; NO MATERIAL CHANGE**

Actual advance: an independent source reconstruction, full Resolution replay, exact DAG accounting, 42 hostile rejections, and seven deletion witnesses confirm [P2-L3-532] without expanding its scope. Precise remaining gap: authenticate the complete fixed $R_{mix341}$ grammar and prove either a lower bound surviving every legal mixed shortcut or a noncircular same-calculus B3 bridge. P versus NP remains OPEN.
