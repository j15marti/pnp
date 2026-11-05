# LSPV-1/420 | Five-role handoff | November 5, 2026, 08:09 PST

**IDEA → SEARCH → ITERATE completed.** New **PROVED/RESTRICTED** theorem concerns a *finite program-index safety audit*, not a proof of B3 or a native-combined-R lower bound. B1, B2, B3, the full mixed worst-case superpolynomial bound and P versus NP are **OPEN**.

## Finding

For polynomial-clock program descriptions A and unary horizon 1^L, define SafeReject(A,L) to mean that no valid SAT source F of at most L encoded bytes, accompanied by an assignment satisfying F, is erroneously classified UNSAT by A. This problem is in coNP. Reduce 3UNSAT G on n variables by embedding G in the program and using visibly SAT, canonical, distinct, proper 2-CNF sentinels S_w = conjunction over i of (z OR literal_i(w_i)). Each sentinel is SAT by z=1, has O(n log n) encoded bytes and encodes w. The program rejects precisely if G(w) holds. Then SafeReject(A_G,L_n) iff G UNSAT. This is coNP-complete even when every possible bad rejection occurs only on visibly SAT sentinel sources.

**Stronger conditional variant:** Suppose SAT is in P with one correct P-time decider D. Let B_G use the above special sentinel behavior and use D on every nonsentinel source. Every B_G is now complete for rejecting actual UNSAT inputs; finite rejection soundness is still equivalent to G UNSAT. The program code varies with G. Under SAT in P, coNP=P, so do not infer a superpolynomial runtime from this coNP classification. This cannot refute B3 or replace an independently justified one-decider reflection theorem.

## What changed in the iteration

The initial construction A_G was not complete for UNSAT. The revised B_G uses D outside the proven-SAT sentinel family to meet the one-sided completeness promise central to LSPV-1/419, without assuming any correctness proof for D or existence of R certificates. This isolates the extra assumption: an unconditional SAT-in-P-to-native proof-size transfer for one fixed suitable decider is still missing.

## Evidence and source review

All 256 signed 2-variable source subsets: 95 SAT, 161 UNSAT. All 256 full-clause 3-variable subsets: 255 SAT, one UNSAT. Python produced 13,338 checks, 21 malicious/malformed controls, 3072 SAT sentinel cases and 1152 demonstrable false rejections on SAT program data. An independent Node implementation produced 6,687 checks. Zero randomness.

Read governing Nov. 2 /1204, issue #3, all 12,598 GitHub tree entries, AGENTS.md, CODEX.md, repo skill, original mixed /341, LSPV-1 /418 and branch /419, LSPV-2/419, LSPV-3/424, LSPV-4/415, REFEREE361 and 364, actual GROKPROOF 2026-11-05_1428_PROGRESS.md and Claude tport README, and all of github.com/openai math Lean ExecCNFNodeSearchCosts. Primary Cook–Reckhow 1979, Haken 1985, Cook ER PHP 1976 and Pich–Santhanam ECCC 2023. No relevant all-input B3 compiler found. Direct Google-branded search unavailable; indexed web used. Bounded model checking supplies only a finite-safety analogy.

Haken's exponential PHP result is ordinary DAG Resolution, *not* the full unchanged paid ER/AND3/GF(2)/LOCAL calculus, and Cook ER PHP plus affine Tseitin are required escape controls. The original native grammar remains unsettled. The new result does not consume or update rule weights or task settings.

## Immutable artifact paths (GitHub readback checked)

- Formal role report: research/agents/lspv-1/2026-11-05_0809_LSPV-1_FINITE_ONE_SIDED_REJECTION_AUDIT420.tex
- Python producer: experiments/arc/lspv1_420_finite_one_sided_audit.py
- Independent Node verifier: experiments/arc/lspv1_420_independent.mjs
- Raw exhaustive record: results/raw/arc/2026-11-05_0809_LSPV1_FINITE_AUDIT420_raw.json
- This coordination handoff: research/coordination/2026-11-05_0809_LSPV1_FINITE_ONE_SIDED_AUDIT420_FIVE_ROLE_HANDOFF.md

Reproduce in a normal repo checkout by running the Python producer, moving its generated experiments/arc/raw420.json to the canonical raw path for independent replay, and then node experiments/arc/lspv1_420_independent.mjs results/raw/arc/2026-11-05_0809_LSPV1_FINITE_AUDIT420_raw.json. Additional *full* versioned local files remain conversation attachments.

**main.tex governance fallback:** GitHub fetch_file of root main.tex returned SHA 1b8a7d9a1514b06c96501849a7902b7aa3dae2a1, but only an empty content field; repo tree records a very large document. A safe full-old/new blob comparison is impossible in this interface. Leave root unchanged and ask LSPV-5 to reconcile the LSPV-1 region once complete contents are obtainable, rather than overwriting or editing other roles.

## Separate specialist requests

LSPV-2/3: continue forensic historical native LOCAL/DEF-facet exported-wire grammar and general typed polynomial proof-to-proof compiler or a *legal* native counterexample. Retain exact source and sparse high-width affine masks. LSPV-4: keep source/index/output/peak-space charges separate from paid nodes and use a byte-injective sparse ID parser. LSPV-5: attack the claim that program-index finite coNP audits affect B3 for one fixed correct SAT decider, and independently review the reduction's SAT sentinel witnesses and common polynomial clock. LSPV-1: find the noncircular one-decider native reflection transfer without assuming formalized rejection soundness. **P versus NP OPEN.**
