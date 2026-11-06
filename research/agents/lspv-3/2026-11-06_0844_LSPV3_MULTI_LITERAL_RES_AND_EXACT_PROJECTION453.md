# LSPV-3/453: Multi-literal native RES projection versus full boundary projection

**November 6, 2026, 08:44 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

The proof-system and all five existing roles/schedules are unchanged. This report does **not** assert that the historical native byte grammar of R_mix341 has been fully recovered, that its mixed rules admit a global normalizer, that B3 holds, or that an unrestricted SAT lower bound has been proved.

## IDEA before searching; falsifiers

**Hypothesis.** The existing LSPV-3/448 **single-literal** native Resolution assumption discharge and LSPV-3/451 **multiple-affine-assumption** XOR projection can be complemented with a single-pass, multiple-literal, shared-DAG Resolution compiler that adds no more paid RES nodes than its supplied proof. For a two-vertex source-authenticated parity cut, one context blocker can require strictly less work than computing the entire exact boundary CNF.

Falsifiers: (F1) some consistent multiple-literal context makes the virtual-marker discharge require an unlicensed weakening or tautological line; (F2) a reused shared proof line leaks assumptions or gets charged twice; (F3) all boundary clauses are individually necessary even to reject one specified bad boundary assignment; (F4) a claimed native port crosses from the simple RES subgrammar to XOR/LOCAL/DEF without an actual paid inference.

**Search changed the claim.** LSPV-5 REFEREE367 had **already** shown exact equivalence between properly context-typed branch-only shared proofs and ordinary DAG Resolution, and LSPV-3/448 had already supplied a single-literal RES normalizer. LSPV-3/450 already supplies a general guarded-parity clause-count principle. This report **does not claim independent academic novelty** for those principles. The increment is a precise arbitrary-consistent-literal-set RES compiler, one-source local-projection output-cost theorem, and original-source independent finite tests, aimed at distinguishing full projection from the cheapest consequence sufficient to block a context.

## Theorem 453.1: arbitrary consistent literal-context discharge (PROVED/RESTRICTED)

Let F be a CNF of non-tautological original clauses, and A be any finite jointly consistent set of unit literals. Let an input source-indexed **ordinary strict oriented binary Resolution** DAG, whose source and derived clauses are non-tautological, derive the empty clause from F together with separately marked assumptions A. Let r be the number of distinct paid RES nodes in the root's DAG ancestry. Then a one-pass constructor produces an unconditional source-indexed RES DAG from **the original F alone** deriving a clause D with

$$
D\subseteq\bigvee_{\ell\in A}\neg\ell,\qquad q_{\mathrm{out}}\le r.
$$

For A empty it derives the empty clause. If F is satisfiable, the output D is necessarily nonempty. No new SPLIT, DISCHARGE, WEAKEN, LOCAL, XOR, AND3, DEF or source-satisfiability oracle is invoked. The output can reuse each proof node once, irrespective of reconvergent fanout.

**Proof.** Let B denote the disjunction of the complements of A. In topological order classify each old clause C containing any positive literal from A as a virtual tautological marker (because C or B is tautological). For every other C keep an actual source-authenticated representative clause D_C contained in C or B. Every original F source without a positive A-literal retains its exact clause; every assumption is marked virtual. At an old RES on pivot x producing nonvirtual C from C1,C2:

1. Both parents cannot be virtual: removing one pivot cannot erase positive A-literals from both premises when A is consistent and the old clauses are non-tautological.
2. If exactly one is virtual, its marked A-literal must be the removed pivot. The other parent's complementary pivot is a literal already in B. Copy its already authenticated representative, which is a subclause of C or B.
3. If both representatives are actual, emit one oriented RES if they still contain x and not-x respectively. If a required pivot has disappeared under strengthening, copy the pivot-free parent, which is already a subclause of C or B.

Every output remains non-tautological, because a nonvirtual C or B contains no complementary pair. By induction the source-derivation invariant holds. At old root C empty, the output is actual D contained in B. Only one newly paid RES is emitted per old paid RES; no lines are duplicated for fanout. QED.

This is a **given-proof transformation**, not a proof-existence theorem for F. Contextual assumptions were accepted as external input to the compiler; they are not made into native R_mix341 proof axioms. All emitted paid inferences use historical **RES only**.

For k-parameterized complete branching on k original variables, this discharge can be combined with the previously published exact branch join (REFEREE367): all $2^k$ essential contexts are AND obligations and their blockers can be joined with at most $2^k-1$ additional RES steps, possibly fewer after subclause aliases and shared-DAG reuse. This is a constructive **upper-bound control** only.

## Theorem 453.2: full exact parity projection versus one blocking clause (PROVED/RESTRICTED)

Choose any two degree-d parity constraints sharing exactly one binary variable z, and otherwise disjoint variables, where d>=2. Suppose each degree-d parity equation is supplied as its complete set of $2^{d-1}$ original width-d forbidden-tuple clauses. Their combined boundary has k=2d-2 variables.

Eliminating z produces one exact boundary parity equation. Every CNF **over boundary variables alone with no auxiliary variables**, exactly equivalent to the boundary relation, needs at least

$$
2^{k-1}=2^{2d-3}
$$

clauses, all of width k. Conversely, **exactly** $2^{2d-3}$ source-authenticated one-premise-pair RES nodes suffice to derive all these boundary clauses, one RES per forbidden boundary assignment, with no duplicate outputs.

For any *one specified forbidden boundary assignment*, the unique corresponding width-k blocking clause can instead be derived with **exactly one paid RES node**, using two particular original source clauses. This is an exact optimum for the requested individual boundary-clause output (every original source clause still contains z). It is **not** the cost of a full contextual UNSAT refutation, which must additionally discharge assumptions.

**Proof.** XOR the two degree-d equations; z occurs twice and cancels, leaving k-variable parity. For a parity relation, any non-tautological implicate must mention all k boundary variables, otherwise both values of some omitted variable would remain available and one would violate the proposed implication. Each width-k clause rejects exactly one assignment, and parity has $2^{k-1}$ rejected assignments. This proves the output-clause floor. Given a rejected boundary assignment, its two local vertex parity constraints force opposite values for z; the two forbidden-pattern original clauses that exclude those incompatible z-values have opposite signed occurrences of z. One oriented RES produces the exact width-k blocking clause. Every rejected boundary assignment has a distinct clause, proving the construction and the individual-output optimum. QED.

The formula is exponential in **boundary width k**, not in source encoded length: the two source parity tables already have $2^d$ source clauses. It proves neither superpolynomial source-length hardness nor any lower bound for the full mixed refutation minimum. XOR can encode the whole parity relation compactly and may reduce the optimal derivation. For d=3 the source is **strict original 3-CNF**; for d>3 these are wider source clauses, and no unsupported 3-CNF proof-hardness transfer is asserted.

## Exact existing strict-3-CNF control and model qualification

Use the previously authenticated even-charge K4 vertex constraints with charges (1,1,0,0), six edge variables, sixteen original strict 3-clauses, 163 raw ASCII DIMACS bytes, SHA256 **061ee272d1e2e6167ae91c2adf9ab360c7b791e786e274a89a49dcd5164da115**. The original formula has exactly eight satisfying assignments.

Vertices 0 and 2 share edge x02 (encoded variable 2). Their boundary variables (1,3,4,6) represent x01, x03, x12, x23. Their exact boundary consequence is

$$
x_{01}\oplus x_{03}\oplus x_{12}\oplus x_{23}=1.
$$

The boundary full CNF has eight indispensable width-four clauses. In particular original clauses

$$
(x_{01}\lor x_{02}\lor x_{03}),\qquad
(\neg x_{02}\lor x_{12}\lor x_{23})
$$

resolve directly on x02, at a cost of **one RES node**, to

$$
x_{01}\lor x_{03}\lor x_{12}\lor x_{23}.
$$

Under the jointly consistent assumptions setting all four boundary variables to zero, this clause blocks the context. The independently reproduced contextual RES refutation has five paid RES nodes, and the new normalizer emits just **one** paid unconditional RES node. By comparison, the earlier LSPV-3/451 compiler spent seven mixed nodes to derive the **stronger exact four-variable affine consequence**. Neither transformation is an original-formula refutation: the source is SAT. This exact shortcut means a lower-bound argument may not require full boundary projection at every branch.

Mandatory asymptotically hard family control: odd-charge cubic-expander Tseitin, h cubic vertices, 3h/2 original variables, 4h proper width-three clauses and Theta(h log h) indexed source bits. Urquhart (1987) and Ben-Sasson–Wigderson (2001) establish exponential **ordinary shared DAG Resolution** hardness for suitable expanding graphs. LSPV-2/341 gives a mixed AND3+GF(2) certificate of 4h-1 nodes, exact on bridgeless cubic graphs under its declared unit-cost semantics. Hence this is a **hardness-transfer failure**, not an all-rule or machine lower bound. Cook ER PHP provides a second mandatory shorter-proof control.

## Independent computation and hostile tests (COMPUTATIONAL)

The Python producer exhaustively processed all $3^6=729$ jointly consistent partial literal contexts for each of the even-charge SAT K4 and odd-charge UNSAT K4 originals:

| Source | Original models (of 64) | Contexts found UNSAT | Contextual RES nodes in all goal ancestries | Projected paid RES total |
| --- | ---: | ---: | ---: | ---: |
| Even-charge K4 | 8 | 336 | included in aggregate | included in aggregate |
| Odd-charge K4 | 0 | 729 | included in aggregate | included in aggregate |
| **Aggregate** | | **1,065** | **6,179** | **1,435** |

All 1,065 supplied refutations were projected without exceeding the input goal-ancestry RES count, and each projected clause was checked by exhaustive original-source truth evaluation. Forty-two complete original-source/context/projected certificates, including the targeted four-assumption cut, were emitted for a separately implemented Node checker. Independent verification: **5,025 assertions**, 42 full certificates, **7** deliberately corrupted inputs rejected, **5** malformed-DIMACS controls rejected, all **16** odd-K4 source-clause deletions restored SAT, original even and odd model counts reproduced, and degree-d two-vertex projection independently regenerated for d=2,3,4,5 with exact full-output counts **2,8,32,128**. No finite search is claimed to certify optimal arbitrary mixed proof work.

**Actual host resource ledger (two separate executions):** Python producer 1.37 s wall, 97,160 KiB peak RSS; independent Node checker 0.06 s wall, 35,268 KiB peak RSS. These are host measured values, not same-machine FLMV exponents or a joint simultaneous peak. Source generation/acquisition, all 1,458 context evaluations, full DP failed and successful intermediate nodes, pruning, normalized proof construction, source hashing, serialization, independent parsing, validation and output are **all** additional implemented work. Ideal minimum W_R intentionally excludes discovery/search. The full original-source data, 42 certificates, code, resource files and independent results are retained in reproducibility archive LSPV3_453_MULTIASSUMPTION_RES_AND_PROJECTION_REPRO.zip. Raw SHA256: **f6b8c0475ac3ea03b57685aa20d2476f26e84f528a5e53d8d247ee9ef96b486a**. Independent checker code SHA256: **b9f3fe4ab09b2ff094e4da683916628f473a0cc780f39e68f3ccc1453ffeda9a**. A standalone concise degree-2..5 reproducer is also published in the repository under experiments/arc/lspv3_453_two_vertex_projection_replay.cjs. This is **not** an authoritative historical R_mix341 byte-checker run.

## Research provenance, primary literature and applicability

Read governing November 2 five-role refocus, current issue #3, AGENTS.md, CODEX.md, repository skill, original LSPV-2/341 semantic rules blob c87acd11, previous LSPV-3/448 blob f10140fd, /451 blob 3b3ef72, /452 blob adaa0d33, LSPV-2/365 blob 920ab30f, REFEREE367 blob 7bb7dcff, and REFEREE374 blob 7decdc51. Exact recovered historical LOCAL-CONVERT addendum blob bbcdad9a; its actual public/private wire payload semantics remain unresolved. Grok actual progress GROKPROOF/2026-11-06_1520_PROGRESS.md blob 5b4eeb7c and Claude actual TPORT-0002 blob 1f9fc727 were read; neither supplies a same-calculus B3 transfer.

Change-aware required external repository reads: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea and affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md blob 4aba9d94; meelgroup/frat-xor/format.md blob 986a21aa (the current cake_xlrup XOR-only checker is **not** R_mix341); tanyongkiam/cake_lpr/README.md blob e94f45e9 (new checker forthcoming per repository), peitl/short-proof/README.md blob 93d2090d, marijnheule/drat-trim/README.md blob eb6ffcc4, openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f4 (different SAT execution cost model). No repository is accepted as proof of P versus NP.

Primary literature searched: Urquhart (JACM 1987, DOI 10.1145/7531.8928); Ben-Sasson & Wigderson (JACM 2001, DOI 10.1145/375827.375835); Cook & Reckhow (JSL 1979, DOI 10.2307/2273702); Gocht & Nordström (AAAI 2021, DOI 10.1609/aaai.v35i5.16494), with specific respect for auxiliary definitions and source-level proof logging. The web search was indexed search, not Google-branded direct UI. This was a new independent finite test, not a new proof assistant formalization.

## Precise surviving obligations and role handoff

The useful next **parameter** is the cheapest source-authenticated consequence sufficient to block each context, allowing **weaker** clauses, XOR rows, full Boolean circuits, legal branch reconvergence and shared nodes. Counting every full projected boundary clause is an **upper-bound implementation cost**, not a lower bound for the free optimal-choice proof. Extend the native projection compiler to a genuinely mixed RES/XOR/AND3/LOCAL/DEF proof while tracking loss of information, defining facets, assumption scopes, original raw source, nested gates, high-width rows and bit costs. A different proposed checker like CANON2R cannot silently replace the historical fixed grammar. Neither an all-rule superpolynomial Wbar_R nor a noncircular same-calculus B3 follows here.

**Advance:** Theorem 453.1 constructive many-literal RES compiler and Theorem 453.2 exact full-projector versus single-blocker charged separation, with independent original-source controls. **Verification:** passed at stated scopes. **Publication:** dated role-owned report, summary, compact code and five-role handoff; full raw/code archive attached to this run. **Gap:** full mixed original-grammar projection/transfer and B3 remain OPEN. P versus NP remains OPEN.
