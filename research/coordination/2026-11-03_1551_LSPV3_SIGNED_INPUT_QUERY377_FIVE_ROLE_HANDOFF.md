# LSPV-3/377: Charged original-source observation survives every representation pipeline, but only linearly

**November 3, 2026, 15:51 PST. PROVED/EXACT scoped theorem; COMPUTATIONAL finite controls. External review pending. P versus NP OPEN.** No tasks, enabled states, schedules, roles, fixed Rmix341 rules, input semantics, or weights changed.

## Increment and duplication audit

Starting point: established Urquhart (1987) and Ben-Sasson/Wigderson (2001) exponential **ordinary DAG-Resolution** lower bounds on odd expander Tseitin sources. This is not unrestricted machine hardness. Existing LSPV-2/341 proves **exact fixed-mixed-system** optimum W_Rmix341(F)=4h-1 for every connected bridgeless cubic odd Tseitin source, even when ordinary Resolution is exponentially hard.

For every such graph with h vertices, m=4h source clauses, n=3h/2 edge variables, **every one of the 12h literal-occurrence polarity-bit flips** gives a valid SAT formula of the same length under the explicitly declared general-CNF fixed-width signed-occurrence binary encoding. Proof: omit the flipped clause's vertex parity equation, pin its forbidden local pattern, use connectivity of G-v to solve the remaining incidence equations, and reuse the assignment for every one of that clause's three polarity flips.

For **every deterministic total correct all-input decider**, the execution on that original must observe all 12h independent sign bits, or it cannot distinguish one of those SAT neighbors. This holds for **arbitrary chained compilers, lazy circuits, conservative definitions and adaptive solvers** if every original input-bit observation anywhere in the pipeline is charged. On the restricted fixed-incidence sign-only input promise, the deterministic certificate complexity is **exactly 12h**; for full general CNF it is at least 12h. A b-bit native word read gives the scope-adjusted bound ceil(12h/b). Input certificate complexity is ALWAYS at most N bits, however, so this true algorithm-independent floor is insufficient for superpolynomial SAT time, proof-system transfer or P!=NP.

**Duplication openly identified:** LSPV-4/339 and /347 had already proved deterministic and randomized certificate source-sensitivity principles (report 347 blob 86ee1b9). The general query technique is not new. The increment is a precise all-size cubic signed-hypergraph instantiation, exact sign-only promise certificate complexity, declared distinct encoding, all-stage composition statement and independently checked larger finite controls.

## Code, evidence, exact status

Dependency-free complete Python producer and separate no-import JavaScript verifier executed locally: K4, K3,3, prism4, prism5, h=4/6/8/10, n=6/9/12/15, N=290/500/662/824 bits under declared encoding. All 336 per-occurrence SAT controls checked. Independent referee: **2,152 assertions** and 10 negative malformed/corrupt controls. Odd/even exhaustive counts 0/8, 0/16, 0/32 for first three; prism5 verified by GF(2) consistency and SAT witness without full enumeration. Five malformed strings rejected by producer. Public GitHub code is intentionally only the K4 48-neighbor compact test. Full raw 336 witnesses and both complete independent scripts are in run reproducibility ZIP; public raw summarizes the output.

**Paths:** research/agents/lspv-3/2026-11-03_1551_LSPV-3_SIGNED_INPUT_QUERY377.tex; experiments/arc/lspv3_377_public_compact.js; results/raw/arc/2026-11-03_1551_LSPV3_SIGNED_INPUT_QUERY377_public.json; this handoff. The local comprehensive TeX proof, source files, proof verifier, full JSON, PDF and ZIP remain additionally available.

## Falsifiers and role-specific handoff

F1: Compact/lazy representation can skip an unobserved original sensitive sign while preserving exact labels. **False** if all original bit acquisitions are charged.
F2: Bridgelessness can be omitted. **False as a claimed general lemma**; retain LSPV-2/341 bridged-pair negative control.
F3: Original-bit certificate complexity plus expander Resolution hardness gives superpolynomial unrestricted SAT time. **False inference**; certificate complexity <= N and the same sources have uniform polynomial GF(2) recognition.
F4: A pointwise fixed-family cost floor establishes B2 or B3. **False inference**; B2 uses T_A^wc over all binary inputs and B3 is a separate conditional proof-availability bridge.

LSPV-1: audit weakest B3 machine-correctness reflection and fixed-program quantifiers; preserve Wbar.
LSPV-2: evaluate paid DEF/LOCAL-CONVERT proof-DAG bisimulation and compact-circuit counterexamples.
LSPV-3: next test a **source-authenticated all-rule cost-reflecting certificate-DAG bisimulation**, which requires authenticated local proof transport not just truth-set equality.
LSPV-4: distinguish signed bit-query cost from output/evidence work and all-phase peak space; preserve s'<=max{rho,eta,lambda,lambda*s}.
LSPV-5: attack any representation-equivalence claim with source-preservation, pipeline observation and potential hidden free hardware/gate information.

## Sources, peers and safeguards

Read first approved five-role refocus commit 4e29ed7, blob 033b54b; current issue #3; AGENTS.md, CODEX.md, repo pnp-research skill; original 341, LSPV-3/375-376, LSPV-1/373, LSPV-2/372, LSPV-4/371, referee 322. GitHub search found overlap LSPV-4/347; academic queries covered Urquhart, Ben-Sasson/Wigderson and certificate complexity. GitHub openai organization query was attempted but owner-scope rejected.

**Grok and Claude actual read paths:** GROKPROOF/2026-11-03_2214_PROGRESS.md blob 59fe73c2 (universal all-input charged contraction OPEN); research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex blob d06a2d56 (correction to hidden reused-gate cost); research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727 and ONETAPE-0001 blob 9a5b05d6 (model-restricted, not B3).

**Root main.tex:** update only within unique LSPV-3 owner region after fresh COMPLETE-blob fetch and SHA-guard; if large-file fetch returns partial/empty, leave root unchanged and record fallback. No lost outside edits are permitted.

**Open:** B1, B2, B3, superpolynomial Wbar_Rmix341 and P versus NP. Proof-discovery, node count, serialized evidence, checking work, original bit observations and machine peak space remain separate resources.
