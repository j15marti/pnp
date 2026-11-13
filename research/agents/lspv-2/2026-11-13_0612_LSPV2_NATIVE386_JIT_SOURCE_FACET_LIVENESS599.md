# LSPV-2/599: Pointwise-optimal just-in-time SOURCE and DEF-root retention in archived native `/386`

**November 13, 2026, 06:12 PST | LSPV-2 SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED (storage-schedule theorem) + COMPUTATIONAL (actual original-checker OS replay). P versus NP OPEN.**

## Candidate and four falsifiers

**Candidate.** In the exact original `/386` restricted SOURCE/paid-AND2-owner/free-DEF-facet/strict-signed-RES accepted-byte language, for a **fixed paid RES occurrence DAG and fixed chronological RES order**, move each mandatory original SOURCE or zero-additional-payment DEF root to immediately before its **first RES consumer**, emitting otherwise unused roots before all paid deductions. This produces a native accepted certificate with unchanged W, signed SOURCE, once-paid owner identity, RES graph and span. In a separately stated offline one-emission/no-recomputation last-use storage model, it is pointwise optimal for the number of retained SOURCE/DEF root clauses at every RES checkpoint, not merely a helpful greedy heuristic.

The predeclared falsifiers were: **F1**, the unchanged archived checker rejects an actually generated JIT certificate; **F2**, delaying a root to first use introduces a forward reference or loses an original mandatory SOURCE/DEF occurrence; **F3**, an alternative legal root order with the same paid RES order and a single emission per root has smaller live root inventory at a RES checkpoint; **F4**, forged signed SOURCE, future parent, underpayment or an unsupported opcode survives the original checker. All four failed for the stated restricted model and executed inputs. F3 is excluded by the interval lower-bound proof, not by finite sampling.

## Recovered authority and preexisting results

The unchanged original archived `/386` executable is `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`, SHA-256 `22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113`. It checks signed guarded cubic Tseitin original SOURCE occurrences, globally once-paid conservative AND2 owner definitions, free defining facets, and strict oriented binary RES. It **does not** check AND3, GF(2), LOCAL-CONVERT, branches, contexts, weakening/discharge, joins, deletions or private/exported wire transformations. The distinct original `/341` fixture checker does not supply those omitted transitions; even dual acceptance cannot authenticate cross-rule composition.

The independently provided external signed original SOURCE file was `results/raw/arc/574_k01_SIGNED_SOURCE.cnf`, SHA-256 `3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c`, 17 exact occurrence clauses. The four seed packets and original checker are unchanged files preserved in LSPV-2/598's evidence archive. The separate LSPV-2/599 replayer reconstructs and compares all SOURCE multiset members to this independent input before exercising the original checker. This external binder is **not** built into original `/386`.

**Prior work not reclaimed:** LSPV-1/566 established full original `/386` topological proof-record normal-form legality and fixed W, including SOURCE-first; LSPV-3/574 established source-fixed whole-DAG rescheduling and cycle-action controls; LSPV-4/545 provided exact fresh-result liveness for paid RES results in a specified execution model; LSPV-4/555 compared a source-prefix to a late-source source-area proxy for a parametric family; LSPV-2/597 showed paid RES schedule-dependent peak retention; LSPV-2/598 demonstrated concrete accepted late SOURCE/DEF chronology. The **new** limited contribution is a pointwise necessary-and-sufficient root liveness lower envelope for every fixed RES order, and native accepted-byte transformation/quantitative checks for both W29 and W32, including actual free DEF facets. This does not establish global memory optimality, a full online algorithm, or a lower bound for R_mix341.

## Theorem 599.1: root-liveness envelope, exact for fixed RES order

Let $P$ be an ordinary parsed packet accepted by the archived `/386` mathematical proof body, with $m$ paid RES occurrence records in a fixed order $d_1,\ldots,d_m$, and with a finite collection $R_0$ of parentless mandatory SOURCE and allowed DEF-facet records. Hold fixed all paid RES identities, signed clauses, chronological RES parent dependency edges, all root-parent edges, all global paid-owner declarations, and the final empty RES record. Require every root record to be emitted exactly once; after emission a root's clause must be retained through its last RES use and cannot be reloaded, recomputed or reconstructed for free. Every root used as a RES parent must appear before its first use. Unused mandatory roots must still be emitted somewhere in the certificate. Root storage is sampled just before each RES record, including its required premises. This is an **offline certificate-execution** storage convention; it does not charge source acquisition, parsing, or physical checker RAM.

For each used root $r$, write

$$
f(r)=\min\{j:r\text{ is an immediate parent of }d_j\},\qquad
\ell(r)=\max\{j:r\text{ is an immediate parent of }d_j\}.
$$

The unavoidable live-root envelope at RES checkpoint $j$ is

$$
\boxed{\quad L_0(j)=\bigl|\{r\in R_0:f(r)\le j\le\ell(r)\}\bigr|.\quad}
$$

Define $J(P)$ by placing unused SOURCE/DEF roots before $d_1$ and each used SOURCE/DEF root immediately before $d_{f(r)}$, retaining original relative RES order and consistently remapping all chronological integer parent indices. Then, for every $j=1,\ldots,m$:

$$
\boxed{\quad \mathrm{LiveRoot}_{J(P)}(j)=L_0(j)\le\mathrm{LiveRoot}_{Q}(j)\quad}
$$

for every other legal root-rescheduling $Q$ satisfying the stated same-proof, one-emission and retention conditions. The derived RES live intervals depend only on the fixed RES order, so in this explicit model $J(P)$ also minimizes **each combined root-plus-RES slot count**, the maximum of those checkpoint counts and their sum. If other changes are allowed, such as RES reordering, clause recomputation, in-place reuse, or physically different storage representations, this optimum claim does not apply.

**Proof.** Every use of $r$ by $d_{f(r)}$ requires an earlier root emission. By the no-recomputation assumption, every checkpoint through $d_{\ell(r)}$ requires retaining that same root clause. Hence every legal $Q$ has $r$ resident at every $j\in[f(r),\ell(r)]$, giving the universal lower bound $L_0(j)$. The constructed $J(P)$ emits $r$ directly before $d_{f(r)}$ and releases it immediately after $d_{\ell(r)}$, attaining equality. Unused original SOURCE/DEF records have no RES consumer and are emitted in a separate zero-paid prefix, then reclaimed under the declared ideal execution model, without contributing to any RES checkpoint. All SOURCE/DEF records are parentless in this checker, and their validity depends on the immutable graph/charges or globally predeclared paid owner, not on the proof chronology. Every RES retains its original two parent identities, signed literals, pivot and resolvent; after rebasing, all parents are earlier. Thus the checker mathematical core accepts the remapping. Global owner bank, record counts, payments and last empty clause remain unchanged, and the unchanged complete CLI's existing negative-control preconditions remain true because the owner bank and terminal pivot were not changed. Therefore every originally full-CLI-accepted ordinary packet in this restricted model remains accepted; $W=N_{\mathrm{RES}}+|D|$ and RES dependency span are equal. For a fixed RES order, a RES result's last consumer ordinal is also fixed, so its live interval is the same in all compared schedules. Adding this identical derived-result count to the root envelope proves the combined-checkpoint statement. QED.

**Resource qualification:** The word *live* means retained clause payload under the declared one-emission/last-use model. The original checker actually retains `known[]` records in memory; this theorem does **not** demonstrate reduced checker process peak RSS or a fully charged FLMV machine-space bound. Certificate bytes can even increase because chronological decimal parent indices change. Source authentication, proof construction, preprocessing, available scheduling information, failed search, and output bytes remain separate charged resources.

## Executed exact accepted-byte evidence

All packets were written as UTF-8 JSON plus LF and submitted via separate real Node.js operating-system subprocesses to the **unchanged original `/386` checker**. The checker also runs its original embedded corruption tests for each accepted packet. A clearly labeled independent **reference** replayer validates the external signed SOURCE clauses, keeps exact root identities and every parent/pivot, checks signed RES DAG identity through canonicalized references, computes interval lower bounds, and compares the root count at *every* RES checkpoint. It is not a substitute for the original checker.

| Original source/proof | SOURCE + DEF roots | Paid RES | W | Span | SOURCE-first peak roots / total slots | JIT peak roots / total slots | SOURCE-first root area / all-slot area | JIT root area / all-slot area |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Guarded odd K4, W29 | 17 + 0 | 28 | 29 | 7 | 17 / 18 | **3 / 10** | 213 / 357 | **35 / 179** |
| Guarded odd K4, W32 | 17 + 2 | 31 | 32 | 8 | 19 / 20 | **3 / 10** | 272 / 423 | **38 / 189** |

For W29, 27/28 RES checkpoints strictly improve retained root count relative to SOURCE-first; for W32, 29/31 improve. The pointwise root envelopes are exactly attained, with area 35 and 38, respectively. Prior /598 lazy schedules already attained the same envelopes, consistent with the theorem. Consequently the run does **not** claim a novel W29/W32 proof cost or that the optimal envelopes were unknown; it supplies a general fixed-RES-order optimality statement for this explicitly charged storage model and systematic native replay.

A total of **12/12 positive original-CLI packets ACCEPTED** (two W29 and two W32 seeds, each tested in input/SOURCE-first/JIT form), with 4/4 deliberate hostile corruptions **REJECTED** (forged original signed SOURCE, future RES parent, false paid summary, unsupported AND3 opcode). The 12 positives completed 43,872 original-checker positive assertion groups (W29 has 3,542 per packet; W32 3,770). Checksums are recorded for every packet; all four test groups have separate actual original-checker execution verdicts. No randomized inputs. Tests require Node.js 22 or compatible modern Node runtime for `structuredClone` and built-in crypto.

Actual full executable: `experiments/arc/lspv2_599_jit_root_schedule.cjs` (local SHA-256 `57198ee3c917161c701d37a3ecf8e2b092fcc021a98ad8607844faa6b85d3398`).
Machine-readable raw: `results/raw/arc/2026-11-13_0612_LSPV2_599_JIT_ROOT_SCHEDULING_RAW.json` (local SHA-256 `c9266de6b29499bfbcd1694dabe295a6685147b1c888f9f7784275c742bf7f7d`).
Direct byte witnesses for JIT W29/W32 and their SOURCE-first comparators are additionally archived; four corrupt inputs retained in the evidence ZIP. Reproduction usage is specified at the top of the full executable; the evidence ZIP preserves its original checker, signed CNF and four input seeds.

## Corpus and primary sources

**CORPUS REVIEWED:** root proof1.txt blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343` read in full; root proof2.txt current blob `930c5eeddafce656717f28055a7a9a755f44737c` recovered through direct blob access after the contents API returned an empty body for this ~1 MB file; issue #3 and its latest research comments; AGENTS.md, CODEX.md, pnp-research SKILL.md; original archived `/341` and `/386` checkers and producer; current LSPV-2/598 five-role handoff and actual /539, /575, /582, /598 reports; LSPV-1/566 and /590; LSPV-3/574; LSPV-4/545 and /555; the native mixed-source underdetermination referee LSPV-5/412; original external source and original-CLI W29/W32 packets. Root `main.tex` current blob `01d55d5bd3306de3166a33da4f9cc76d846125ac` recovered via direct blob API. The required cross-calculus primary format comparator `meelgroup/frat-xor/format.md` explicitly distinguishes clause and XOR ID types; it is **not** historical R_mix341 authority. Other required comparator repos `tanyongkiam/cake_lpr`, `peitl/short-proof`, `konard/p-vs-np`, `blkph0x/p-vs-np-proof-research` and associated existing project receipts were consulted for context only, not imported into a checker.

**PRIMARY LITERATURE:** Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50, DOI 10.2307/2273702; Cousot and Cousot, *Abstract Interpretation*, POPL (1977), DOI 10.1145/512950.512973; Ben-Sasson and Nordström, *Understanding Space in Proof Complexity*, JACM/related proof-space publications; Clarke et al., *Counterexample-Guided Abstraction Refinement*, CAV 2000, DOI 10.1007/10722167_15. These provide motivation and auditing methods. None asserts the checker-specific interval lemma or authenticates missing mixed accepted-byte grammar.

**DUPLICATION / CONTRADICTION AUDIT:** Source-first cost normal form is an existing LSPV-1/566 result and remains correct for W; source-first is not generally storage-optimal. LSPV-4/555 already established beneficial late-source area on a special family, and LSPV-2/598 already executed both late SOURCE and free DEF schedules. The result here narrows the missing quantitative resource condition for a fixed RES schedule but is not a new P2-C3 full-calculus alpha/gamma. We adopt the original `/386` parser, LSPV-1/566 normal-form legality and LSPV-4/545 last-use resource convention. We reject full-calculus transfer and reject any claim that modelled slot savings imply reduced physical checker RAM or a machine-space lower bound. No prior proved theorem is retired by this result.

**WHAT CHANGED RELATIVE TO ROOT MAIN:** A newly explicit, model-scoped pointwise exact envelope for SOURCE and DEF-root liveness, checked against exact original-CLI byte packets; this is restricted incremental evidence for [P2-C3], not closure. Existing status OPEN remains correct.

## Open obligations and concise role handoff

- **[P2-D1] OPEN:** Historical authoritative complete R_mix341 parser/checker for all source-authenticated mixed operations remains missing. `/341` and `/386` are distinct siblings; no source-bound RES-to-AND3 or paid DEF-to-LOCAL-CONVERT verified under one original checker.
- **[P2-C3] OPEN:** No global alpha/gamma over full concrete configurations, contexts, fresh/private/exported wires, branching, discharge, joins, deletions and hidden shared paid identities. New theorem covers a fixed RES-order root-retention subproblem only.
- **[P2-B1] OPEN:** No all-rule superpolynomial minimum lower bound, since the full calculus and legal shortcuts are not authenticated.
- **[P2-B2/B3] OPEN:** No noncircular SAT-in-P-to-polynomial-cost proof bridge in the identical fixed historical calculus.
- **[P1-01], [P1-03], [P1-04] OPEN:** No all-input fully charged polynomial-time deterministic SAT decider.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both root trackers are preserved without padding or partial overwrite. Root `main.tex` may be updated only strictly inside LSPV-2's balanced ownership markers with current complete blob + optimistic-concurrency SHA and full outside-region readback. Exactly the original five existing identities and historical TWO Route A/THREE Route B labels are preserved. No automations were modified.

**Next decisive target:** Obtain one authoritative single original checker accepting an externally source-bound mixed RES-to-AND3 or DEF-to-LOCAL-CONVERT record, plus a rejected corrupted signed-port control. Extend pointwise root storage to proper contexts only after all context transitions and discharge/joins are authenticated. Unknown rule classes remain conservative MAY paths.

**P versus NP remains OPEN.**