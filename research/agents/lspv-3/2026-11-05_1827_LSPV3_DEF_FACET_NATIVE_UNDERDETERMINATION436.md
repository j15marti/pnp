# LSPV-3/436: Original R_mix341 DEF-facet grammar is not uniquely determined

**November 5, 2026, 18:27 PST | Route B | PROVED/EXACT for TWO DEFINED COMPLETIONS, COMPUTATIONAL finite replay; historical authority OPEN.** No claim that these two completions are the original byte parser, that their minima differ, or that P versus NP is solved.

## Idea, falsifiers, evidence, revision

**Hypothesis (stated before search):** The original printed R_mix341 semantic specification permits two sound, refutationally complete, effective byte grammars differing on whether the individually indexed clauses of one paid binary DEF are externally accessible as Resolution premises. Falsifiers: (1) original /341 already specifies a unique indexed facet syntax; (2) either grammar is unsound or incomplete; (3) the witness uses an invalid source, forged DEF, invalid pivot, or dead facets; (4) the difference disappears after source authentication.

**Original source inspected:** research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. It fixes free original CNF axioms, unit-weight binary RES, bounded-support exact AND3, GF(2), paid LOCAL-CONVERT, and one paid conservative two-input DEF. All defining relations belong to that node and later uses reference its owner. It does **not** fix an exact facet selector or a byte serialization.

**Prior-work firewall:** LSPV-5/374, research/main/2026-11-05_1748_MAIN_CANON2R-LOCAL-RESTORATION-NORMALIZER-REFEREE374.md (blob 7decdc51aa3b188aa0204e45c069d1a25fdd1b96), already proves a <=11q whole-proof normalization and actually accepts LSPV-3/435's 11-node trace in a *proposed frozen CANON2R checker*. This run does not reprove that result or promote CANON2R to historical authority. The revised contribution is a typed acceptance-fork witness all of whose DEF facets and original clauses contribute to false.

## Two sound complete effective grammars, precisely distinguished

Both systems retain the printed sound RES, AND3, GF(2), LOCAL and charged conservative DEF semantics and ordinary Resolution refutational completeness. Both check finite source DIMACS, topological nodes, fresh DEF outputs, typed references, oriented Resolution, and actual truth of local gate relations. **FACET-A** additionally lets a RES clause parent reference {def: chargedOwner, facet: k} for k=0,1,2,3. The four clauses are implied by the charged DEF relation, not new free source axioms. **GATE-B** allows the paid gate to be referenced as a whole local relation but has no clause facet selector. Both are sound: every source model extends uniquely through definitions; DEF facets in A hold on every such extension; all remaining rules preserve consequence. Both are refutationally complete since unrestricted RES remains. GATE-B simply restricts one view type.

For z=a AND b, FACET-A indexes

$$
(a\vee b\vee\neg z),\quad
(a\vee\neg b\vee\neg z),\quad
(\neg a\vee b\vee\neg z),\quad
(\neg a\vee\neg b\vee z).
$$

Their conjunction is exactly z=a AND b. The displayed historical prose does not determine whether this owner-qualified view is directly addressable. These are TWO PROPOSED TYPED COMPLETIONS, NOT two original-source-authenticated historical parsers.

## Exact strict-three-CNF source

The focused diagnostic starts with minimally UNSAT (a), (b), (NOT a OR NOT b) and applies the previously established exact signed-padding construction /433. It does **not** claim a new proof-hard family. All ten original clauses have exactly three distinct variables, and the source raw DIMACS is 104 ASCII bytes:

    p cnf 7 10
    1 3 4 0
    1 3 -4 0
    1 -3 4 0
    1 -3 -4 0
    2 5 6 0
    2 5 -6 0
    2 -5 6 0
    2 -5 -6 0
    -1 -2 7 0
    -1 -2 -7 0

Seven paid RES steps recover (a), (b), (NOT a OR NOT b). One charged fresh DEF establishes z=8=a AND b. From the **four owner-qualified facets**, seven more paid RES steps derive: (a OR NOT z), (b OR NOT z), (NOT b OR NOT z), (NOT z), (NOT b OR z), (z), and empty. Every facet index 0,1,2,3 is in the final proof ancestry; every one of the ten original source clauses contributes. FACET-A accepts the 15-node certificate; GATE-B rejects an indexed facet reference by its declared grammar, while accepting a distinct nine-node RES-only proof of the identical source. The two systems therefore have different **certificate languages**, not a proved separation in W_R.

All ten original clauses are independently indispensable. The source-ancestry/fan-in bound q>=m-1, and the matching 9-RES proof, give **exact global unit-node minimum W=9 in both completions** (and under the printed binary-premise semantic rules). A 15-node proof is deliberately used to distinguish the accepted *proof language*, not to establish optimality.

## Independent verification / cost ledger

Local full Python producer/checker: experiments/arc/lspv3_436_facet_ambiguity.py in the local reproducibility archive; separate Node implementation in that archive: lspv3_436_independent.js. The latter passed 342 assertions. Both replay all 128 source assignments, ten clause-deletion SAT controls, all 15 topological proof nodes, exact four-facet truth relation, and final ancestry. Six deliberately corrupted documents were rejected (wrong final clause, pivot, gate truth, facet index, malformed source, wrong parent). A common 9-node proof succeeds without DEF facets. GitHub's compact standalone executable is experiments/arc/lspv3_436_facet_grammar_fork.js; it independently builds the same 15-node witness and checks the A/B acceptance fork. Neither program executes an **authoritative historical** R_mix341 parser.

Unit-node work=15: one DEF plus 14 RES; 28 RES premise references, five uses of four distinct facet indices, ten original source leaves, unit-weight critical-path span=5. The full compact typed proof is 1,442 JSON bytes; the original DIMACS is 104 bytes. On the local Linux tool runtime the producer measured 0.69 seconds/96,684 KiB peak RSS; the independent Node verifier 0.03 seconds/24,692 KiB. These are observations, not asymptotic machine bounds. Source reads, parsing, truth-table computation, conversions, allocation, output and checks are charged by these implemented runs, with ideal derivation selection intentionally free only in W_R.

## Established-family and hardness-transfer ledger

| Family | Exact formula, size, proved bound and model | Shortcut and missing transfer |
| --- | --- | --- |
| Cubic odd-Tseitin on suitable simple bridgeless expander with h vertices | n=3h/2 edge variables; each odd/even degree-three vertex constraint has four signed width-3 blocking clauses, total m=4h. Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001): exponential **ordinary DAG Resolution** length. | Earlier project /341 proved a **linear mixed semantic** minimum 4h-1 by AND3 and GF(2); not hard for all mixed rules. |
| Graph-PHP on sparse expanders (de Rezende, Nordström, Risse, Sokolov, CCC 2020; journal TheoretiCS 2025) | One assignment variable per bipartite graph edge; each pigeon at-least-one clause plus binary collisions for pigeon pairs sharing a hole. Certain expander families have exponential **ordinary Resolution** length. A degree-three bound is NOT assumed for all the published graphs. | Cook/Buss ER/Frege shortcuts and restriction must be examined; strict-3 padding preserves the previous **Resolution** lower bound only when source width<=3. All-mixed backtranslation OPEN. |
| Focused padded 10-clause control this run | Exactly ten width-three clauses over seven source variables, all individually essential. | W=9 exact in both defined completions; A/B distinguish certificate *acceptance*, not proof hardness. |

Primary literature searches also reviewed Raz/Tzameret and Part/Tzameret Res(lin): characteristic-zero subset-sum lower bounds are not GF(2) 3-CNF lower bounds. Proof-checker sources read: meelgroup/frat-xor/format.md blob 986a21aa (theory steps need checker), tanyongkiam/cake_lpr/README.md blob e94f45e9 (verified checker, different language), peitl/short-proof/README.md blob 93d2090d (ordinary Resolution minima), openai/math/README.md blob cc5b0a03 (mixed formalization status). Both NEW repositories inspected with pinned heads: konard/p-vs-np ec edd2b45f1c524d85c00b2da27a9c140025550c, proofs/complexity/README.md blob 7ee9a11e and proofs/experiments/README.md blob 4c8752aa (explicit finite-machine, incomplete proof attempts); blkph0x/p-vs-np-proof-research 7dedc73f758dfbdc072e7aa29dfc08505761ebd5, METHOD_INDEX.md blob 18d693ea and RESIDUAL_EQUIVALENCE_BARRIER_REPORT.md blob 46413596 (exact residual-equivalence coNP-completeness, no free equivalence oracle). Project tree/head fa0d10959a11fa0c4d5e0e5a4be0e34bf729749d at research review. Actual Grok progress GROKPROOF/2026-11-06_0215_PROGRESS.md (blob eae7e6c), Claude TPORT README (blob d1290822) and ONETAPE README (blob 6255025f) consulted. Current issue #3 and governing 2026-11-02 handoff (blob c3889a3e) read. Indexed web search used; Google-branded interface unavailable; container git DNS failed.

**Precise next obligation:** locate authoritative archived /341 grammar/checker for facet owner syntax, LOCAL output types, global freshness, exported/private ports, and branch assumptions. Only an actual historical implementation or authoritative specification can settle which completion is historical. Neither the conditional CANON2R normalization nor this grammar fork supplies a noncircular same-R B3, or a superpolynomial Wbar_R family. B1, B2, B3 and P versus NP remain OPEN.

**Publication safeguard:** Root main.tex at blob 593000bbe5b09df6b93fb7453da2ebdf73aeff6b returned zero readable characters via authenticated fetch, so it is unchanged. No task, schedule, owner region, inference rule or weight was changed.
