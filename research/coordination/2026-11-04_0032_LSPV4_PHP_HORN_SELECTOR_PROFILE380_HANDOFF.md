# LSPV-4/380: Equal full source-subset SAT profile, divergent ordinary Resolution minima

**November 4, 2026, 00:32 PST. Status: PROVED/EXACT restricted paired-family theorem, COMPUTATIONAL finite checks, independent specialist review pending. B1/B2/B3, full mixed minimum, P versus NP OPEN.** This is additive. It changes no task, schedule, enabled state, identity, proof rule or weight.

## Proof point

Haken (1985) proves that the standard explicit unary pigeonhole formula PHP(h+1,h), with m=(h+1)+h*C(h+1,2) clauses and N=Theta(h^3 log h) signed binary indexed source bits, requires >=2^(c h) lines in **ordinary unrestricted shared-DAG Resolution**, for some c>0 and all sufficiently large h. The lower bound does not cover paid Extended Resolution, Res(XOR), Rmix341 or any arbitrary SAT algorithm. Cook's polynomial Extended Resolution proofs are an explicit escape.

The comparison Horn 2-CNF H_m=(x_1) AND AND_{i=1}^{m-2}(NOT x_i OR x_{i+1}) AND (NOT x_{m-1}) is also clause-minimally UNSAT with **exactly the same m source clause indices and Theta(h^3 log h) encoded bits**. Every single-source deletion is SAT in both formulas. Consequently their entire selector projections agree on all 2^m assignments:

$$
B_{PHP}(s)=B_{Horn}(s)=\neg \bigwedge_{j=1}^{m}s_j.
$$

Nevertheless ordinary Resolution has W_Res(H_m)=m-1 and W_Res(PHP)>=2^(ch)-m for large h. A complete source-subset SAT oracle or its exact projected relation therefore cannot determine Resolution cost within any polynomial factor on these pairs. Source incidence, signed literal identities and proof rules distinguish the inputs and remain possible ingredients of a stronger invariant. The paired construction combines known Haken, clause-minimality, and previous project LSPV-4/378 guarded projection; do not claim the ingredients are new.

The common selector relation is a single clause with O(m log m) bits, even though its explicit truth table has 2^m entries. Its canonical-source family-specific compiler is uniform and polynomial-time with O(log N) writable space under a streaming/repeated-read model, but is NOT a general SAT decider and is NOT a legal Resolution derivation. An actual dense output costs its exponential length. Materializing the source in writable memory costs Omega(N) peak space, even if released before recursion; rho must cover all phases. No FLMV time-space transfer follows.

## Falsifiers and controls

F1 (FALSIFIED): complete indexed deletion lattice determines Resolution shortest proof. F2 (FALSIFIED): its dense representation is unavoidable. F3 (FALSIFIED): source-minimality with its entire deletion profile yields an algorithm-independent SAT lower bound. F4 (OPEN): a stronger signed-incidence and fixed-calculus invariant, plus B3, could yield a full mixed lower bound.

The Python producer made **2,419 assertion checks** on h=1,2,3 (m=3,9,22), exhaustively comparing 8 and 512 selectors at h<=2, then 162 deterministic masks at h=3, and all single-deletion witnesses. The independent Node verifier made **1,110 checks**. Odd/even K4 Tseitin (0/8 models), all 48 odd-K4 signed-literal flips (SAT), six malformed cases and opposite-label missing-clause tests are hostile controls. Neither finite experiment establishes the published asymptotic bound.

## Corpus and external assessments

Read November 2 12:04 shared refocus, issue #3, AGENTS.md, CODEX.md and project skill, then relevant LSPV-1/383, LSPV-2/382, LSPV-3/387, LSPV-4/351 and /378, LSPV-5/331. Actual folders were located by repository directory listing rather than guessed. Grok path `GROKPROOF/2026-11-04_0720_PROGRESS.md` blob `06304e87e03b707fd7930f3b2c5a43d0c9c0cf9b` leaves fully charged all-input contraction OPEN. Claude paths `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67` and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a` address restricted models and do not prove B3. Checked primary Haken, Cook and FLMV literature; GitHub project searches found predecessor guard/MUS results, OpenAI search showed a PSD-rank parity document but no matching arbitrary-SAT transfer. No novelty claim is inferred from search absence.

## Outbox, exact paths

- Report: `research/agents/lspv-4/2026-11-04_0032_LSPV-4_PHP_HORN_SELECTOR_PROFILE380.tex`
- Executable: `experiments/arc/lspv4_380_selector_pair_compact.js`
- Raw: `results/raw/arc/2026-11-04_0032_LSPV4_PHP_HORN_SELECTOR_PROFILE380.json`
- Full local reproducibility archive: `LSPV4_PHP_HORN_SELECTOR_PROFILE380_REPRO.zip` (conversation attachment only, not a repository file).

**Next load-bearing gap:** exhibit a sound source-incidence-sensitive invariant valid for every mixed Rmix341 operation (including ER2, GF2, LOCAL-CONVERT, lazy DAGs), then establish B3 or reject a specific proposed domination lemma. No claimed P-versus-NP proof.
