# LSPV-2/500: Two trusted trace anchors for shared child-SAT computation

**2026-11-08 11:20 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Exact proof-chain IDs:** [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04]; cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2], all OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both root trackers were read completely: initial full proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2.txt blob d897a6e16ccac7b3ef7f2598df69559f4bda71fa; peer proof2 was later seen at blob 18ae5b871650a419f191a8e556a73059aac5cc75. No tracker edit is justified by this restricted computational-sharing control.

## IDEA and falsifiers

LSPV-2/432 previously PROVED the single-anchor actual input-read-footprint lemma. Here we test a bounded portfolio of *multiple* trusted anchors to preserve shared computed SAT labels across alternating branches. This does not assume a source splitter. Falsifiers: (F1) same-length children agreeing on recorded guest-read bits but having different outputs; (F2) a cache hit leaking through a hidden assumption context or different input length; (F3) appended ternary clauses invalidating the odd K4 original signed 3-CNF core or its syntax; (F4) cache comparisons/storage exceeding the planned FLMV time/space exponents. F1 is excluded by deterministic transition induction, F2 requires full-context child bytes and exact length, F3 is excluded by odd-charge parity and explicitly valid fixed-width suffix; F4 is excluded only under the *explicit missing* paid indexed virtual-child premise with h polylogarithmically many anchors. No all-input decomposition is constructed.

## SEARCH and provenance

Read both complete root trackers, current coordination issue #3, governing five-role handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob c3889a3e514ddbd747150dcb68607013a3b2d154), AGENTS.md (19656af102604d5f0a721d548cf2e4e72a063561), CODEX.md (754999f50de93cdb693ed37bc8110d31e9e698ef), .codex/skills/pnp-research/SKILL.md (b8df83a7b0b1428f349b0e02ce1387d979e8db7f), LSPV-2/430, /432, /441, /484, /497, /499 and peer LSPV-4/495. Grok actual GROKPROOF/2026-11-08_1130_PROGRESS.md blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70; Claude actual research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67. The earlier single-anchor lemma is adopted, *not claimed new*.

External original files read: konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 (finite-machine P subset NP only); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (scoped methods, no P/NP proof); MassimoLauria/cnfgen cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (Tseitin generator); berkeley-abc/abc README.md blob 88a9d1a316dd9751acade746de315fd1e6e6c362 (separate circuit control); openai/math CONTENTS.md blob 7e1ed90ac5a666f1bbecb22027387c4ad79e9d03 (no universal transfer). Public web search used; no separate Google-branded search. Local GitHub DNS unavailable, so authenticated GitHub reads/writes are used.

Primary research: Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, DOI 10.1145/1101821.1101822; Urquhart 1987 and Ben-Sasson/Wigderson 2001 for *ordinary shared-DAG Resolution* exponential lower bounds on expanding odd Tseitin sources, NOT on all SAT algorithms or R_mix341.

## Theorem 500.1: trusted multi-anchor reuse, PROVED/RESTRICTED

Fix a total deterministic binary-input machine A with SAT, UNSAT and MALFORMED outputs. An internally trusted anchor record contains the complete input length, every distinct actual read-only input address and its bit observed during one completed execution on x, and the final output label. For any y of identical length agreeing with x at all recorded addresses, the entire run of A(y) is identical to A(x), including output and guest resources. **Proof:** induction on transitions. Initial state/length agree; work/INDEX head positions agree at each step, and all read-only guest input bits agree at every observed address, forcing the same successor configuration and the same eventual halt. An arbitrary portfolio may reuse *any* matching anchor; two matching anchors must output the same label because deterministic A(y) has a unique result.

This is sound only for complete encoded child inputs that include every premise, original-source assumption and branch restriction relevant to a child SAT query. An unencoded branch-local fact cannot be cached as an unconditional global lemma. Untrusted *external* asserted traces require a paid replay or separate sound proof; matching a fabricated record to a string is not itself a certificate of correctness. This theorem does not introduce a SPLIT, DISCHARGE, weakening or any other rule into R_mix341.

## Theorem 500.2: explicitly conditional same-machine resource ledger

Assume an *already available* correct all-input source constructor emits q<=N^(3/5+o(1)) complete context-authenticated child SAT inputs of L<=N^(1/2+o(1)) bits, sequentially, with all source parsing, child-bit generation, join/discharge, output, failed searches, INDEX writes/restarts and reference costs within N^(11/10+o(1)) total local work and N^(1/2+o(1)) all-phase local peak. Assume guest simulation, instrumentation, reads, tape resets and cache comparisons each require N^o(1) native overhead. Guest A itself has time L^(t+o(1)), space L^(s+o(1)). Store h=O(polylog N) recent trusted anchors, at most L observed (address,bit) pairs each; deduplicate with one temporary L-bit bitmap. Each retained anchor uses <=L(ceil(log2(L+1))+1)+O(log L) evidence bits. Test at most hL addresses per child. At most u<=q real guest calls execute.

Then for this conditional *stage*, including full simultaneous retained and guest workspace, the envelopes are

$$
T_{\mathrm{stage}}(N)\le N^{11/10+o(1)}+O(qhL N^{o(1)})+uL^{t+o(1)}
\le N^{\max\{11/10,\;3/5+t/2\}+o(1)},
$$

$$
S_{\mathrm{stage}}(N)\le N^{\max\{1/2,\;s/2\}+o(1)}.
$$

The upper bound is unchanged in the worst case because u can equal q. No source-only splitter, recursively iterable compiler, virtual-port native FLMV interpreter or general P algorithm follows. Logical work is u guest completions plus q-u cache reuses and their paid comparisons, not a new refutation proof system; R_mix341 inference nodes and certificate evidence bits are not applicable.

## ITERATE: original signed 3-CNF and computational falsifiers

Take standard cubic K4 odd-charge Tseitin: six edge variables, four proper signed 3-clauses per vertex, 16 clauses; odd total charge is UNSAT. Two different original signed UNSAT cores C0 and C1 put odd charge at different vertices. They are distinct, and each of 16 original clauses is indispensable (deleting it makes the formula SAT). This is a finite semantic fixture, NOT a growing hard-family certification.

Independent reference guest encoding: 8-bit magic 10110101, six-bit variable count n, 12-bit clause count m and m ternary clauses of three (sign, ceil(log2 n)-bit zero-based variable-ID) literals. All suffix records are valid when n=16 because every four-bit ID names a variable; repeated literals and tautologies are allowed in general CNF. The total deterministic three-label guest recognizes the two original 16-clause odd K4 prefixes and returns UNSAT without reading the arbitrary suffix, otherwise parses all clauses and uses exhaustive SAT testing, rejecting malformed. **This guest is exponential, not a polynomial-time SAT algorithm.** Under the conditional SAT-in-P hypothesis one could replace its exhaustive fallback with a polynomial solver, but that hypothesis is unproved.

Generate 128 children, each 2906 encoded bits (192 clauses), alternating C0/C1 with 176 varying ternary clauses. Each completed special-prefix guest read footprint has exactly 266 addresses, header 26 plus core 240. Two independently authored hosted implementations agree: no cache 128 guest calls; one most-recent anchor 128 calls; two anchors **2 guest calls and 126 exact reuses**, because the alternating cores have incompatible read prefixes. The two retained anchor records occupy 6948 bits under explicit sparse address/bit coding, but the two-anchor method makes 35,884 paid comparisons; it is not free. The synthetic 1000-step post-core arithmetic workload is a cost control, not SAT hardness.

Python reference: 558 assertions PASS, including original SAT/UNSAT, 32 one-clause deletion witnesses and five malformed controls. Independent Node/V8: 101,230 assertions PASS, two-core sharing plus four fabricated external-trace rejection checks using full replay. Smaller standalone published Node control: 645 checks PASS, same 128/128/2 guest-call counts. Host arrays and input copies are not a native FLMV workspace test. Neither native FLMV finite-state machine nor historical R_mix341 checker ran.

## Remaining open dependencies and publication safety

[P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. The decisive missing step is the uniform, solver-dependent, exponent-oblivious, recursively iterable, all-input A->Phi(A) with fully charged same-machine contraction. The cache is merely a legal candidate shared-computation upper control when such a child constructor is supplied. Root main.tex fetched at blob 68188a24badda635a5983fda1c381cdb694fd497 returned zero readable characters, so it was not edited. Existing five agent identities, ownership, schedules, enabled states, two-Route-A/three-Route-B allocation, and historical R_mix341 grammar/weights unchanged. **P versus NP remains OPEN.**
