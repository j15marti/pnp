# LSPV-2 PROOF-PAYLOAD-ARITY-COLLAPSE347
**November 2, 2026, 6:15 p.m. PST. Status: PROVED/EXACT for the diagnostic extension; COMPUTATIONAL finite controls; P versus NP OPEN.**

## Why this is a diagnostic, not a new common calculus
Keep the already fixed Rmix341 unchanged. Consider separately Rcover347 = Rmix341 plus exactly one **named diagnostic** inference ENUM_ARITY, which has k>=2 explicit authenticated original-clause premises and one certificate row j[a] per complete assignment a to the declared n variables. Each row identifies one premise clause falsified by that assignment. The verifier independently checks every row, rejecting malformed sources or certificates. The logical cost is max(1,k-1), matching the prior arity-weight convention. All certificate bytes, source reads and checking time are measured separately. The diagnostic rule is deliberately **not adopted** by any agent as an Rmix341 primitive: it contains potentially exponential data and is not an ordinary bounded-local inference.

## Theorem (all-input, exact in this diagnostic system)
Let mu(F) be the size of a smallest UNSAT subformula of any general CNF F, with mu(F)>=2. Then

    W_Rcover347(F) = mu(F)-1.

**Lower bound:** In any sound conservative contradiction DAG, the original-source ancestry must contain an UNSAT subset, at least mu(F) original clauses. On the connected ancestry graph with s sources, q paid inference nodes and E named premise edges, E>=s+q-1. Since every node weight is at least k_v-1, W>=E-q>=s-1>=mu(F)-1. This allows shared subproofs, temporary growth and charged auxiliary definitions.

**Upper bound:** Select a minimum UNSAT core with freely granted optimal hindsight. Every assignment falsifies at least one of its mu clauses. Write their indices in the 2^n-row ENUM certificate and cite all mu clauses as explicit premises. Its one weighted inference costs mu-1. All rows can be checked directly with no hidden answer oracle, though potentially exponentially much evidence.

**Corollary:** For a reasonable encoded CNF with m<=N clauses, the diagnostic system has Wbar_Rcover347(N)<=N, so it cannot support superpolynomial worst-case *logical node-weight* hardness. This proves NOTHING about superpolynomial Wbar_Rmix341, because Rmix341 does not contain ENUM_ARITY. In particular G342 has diagnostic optimum 5, whereas the prior declared VARDEF-only mixed optimum was 6. Do not transfer either minimum across calculi.

## Verification/representation charge
A canonical fixed-width row encoding requires 2^n ceil(log2(mu)) data bits, plus source identifiers and framing. The deliberately explicit verifier reads all 2^n indices and checks one signed original clause per row (at most 2^n max |C_j| literal evaluations), with source parsing and authentication separately charged. It is polynomial in **written proof length**, not necessarily input length. A host program materializing rows uses exponential storage and incurs an all-phase space peak; streaming can change space but does not make evidence or checking free. A fan-in-two AND circuit of m-1 gates does not prove its output constant zero without such checked justification.

Independently checked finite fixtures (JS producer, separate no-import Python referee, **790 assertions**):

| original | vars n | m | mu | exact diagnostic W | rows | literal checks | JSON certificate bytes |
|---|---:|---:|---:|---:|---:|---:|---:|
| G342 | 4 | 6 | 6 | 5 | 16 | 36 | 97 |
| Horn7 | 7 | 8 | 8 | 7 | 128 | 191 | 325 |
| BPHP2 | 3 | 6 | 6 | 5 | 8 | 16 | 81 |
| odd K4 Tseitin | 6 | 16 | 16 | 15 | 64 | 192 | 232 |
| equality4 with opposite units | 4 | 8 | 5 | 4 | 16 | 27 | 95 |
| unit clash | 1 | 2 | 2 | 1 | 2 | 2 | 61 |

All core deletions and individual sign flips were SAT, as predicted by clause minimality. Same-source or same-shape opposite-label controls: even K4 has 8 models; G342 occurrence flip, Horn final-unit flip, and equality final-unit flip each have 1 model and reject ENUM cover. Twelve malformed source strings and six corrupt row certificates rejected. The independent verifier initially detected a BPHP fixture clause-order mismatch; corrected before accepting 790 assertions. Generator is limited to n<=10,m<=16 for finite tests; theorem is not.

## Falsifiers and status
1. Arity-weighting alone prevents huge certificate macros from collapsing all-input shortest weighted proofs: **FALSIFIED** for the explicit diagnostic system.
2. A source-factor AND circuit is itself an UNSAT proof once all clauses are merged: **FALSIFIED** unless a paid zero-function justification is supplied.
3. The G342 exact mixed-six bound survives any larger system: **FALSIFIED** for diagnostic Rcover347; any source-factor DEF without ENUM remains **OPEN**.

**Search:** Primary Cook–Reckhow (1979), Peitl–Szeider (2021); GitHub project searches for Rmix341, G342 and DEF source-factor ambiguity; github.com/openai/openai-cookbook search returned only an unrelated formal-logic notebook, not a comparable implementation. These elementary model limitations are not claimed novel. Research corpus: authenticated full worst-case five-role handoff, issue #3, AGENTS, CODEX, pnp-research skill, LSPV-2 346, LSPV-3 344/346, LSPV-5 REFEREE300. Direct web to private handoff 404; connector succeeded. Local clone failed DNS. Root main.tex authenticated fetch returned zero bytes despite a nonempty SHA, so ownership-only reconciliation was **not attempted**; never overwrite this partial fetch.

**Next step:** obtain a single complete executable definition/checker for Rmix341 source-factor DEF (no free false gate), then seek growing hard families against all its rules and independently prove B3 for that same preselected calculus. Existing schedules, IDs, statuses unchanged. P versus NP OPEN.

**References:** Cook and Reckhow (1979), The Relative Efficiency of Propositional Proof Systems, JSL 44, 36–50; Peitl and Szeider (2021), Finding the Hardest Formulas for Resolution, JAIR 72, 69–97. Complete locally verified reproducer, referee, raw proof rows and SHA256 manifest are in LSPV2_PROOF_PAYLOAD_ARITY_COLLAPSE347_2026-11-02.zip.
## Verified publication postscript (same run)

The first authenticated GitHub `fetch_file(main.tex)` returned empty content despite its valid nonempty blob SHA. Rather than overwrite that partial result, I used the exact SHA with `fetch_blob`, obtaining the full **1,316,475-byte** prior root. An optimistic-SHA `update_file` inserted the result **only after** `% BEGIN LSPV-2 OWNED`, leaving the prefix, suffix and every byte outside the owned region unchanged. Complete `fetch_blob` readback confirmed exact content equality on the resulting **1,318,319-byte** root. **Verified root commit:** `3aaa11d351d27a6e7909d3245eb9f333038fc00f`; verified new blob SHA `89eb623b7b2b20cc80d203d4a531eb89abb8a671`. Thus the earlier root-fetch failure was recovered safely, and ownership-only reconciliation is complete. The published compact JS was also re-executed from exact GitHub readback inside an isolated JavaScript evaluator and reproduced all six minimum costs, row-check counts, and all four SAT-label counts. Existing task identities and scheduling were not changed.
