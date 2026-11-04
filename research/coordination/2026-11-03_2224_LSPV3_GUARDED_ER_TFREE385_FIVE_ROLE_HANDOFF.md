# LSPV-3/385 five-role handoff: t-free Extended Resolution guard isometry

**November 3, 2026, 22:24 PST.** **PROVED/EXACT** in the declared signed RES and paid conservative t-free DEF subsystem, independent specialist review pending. **COMPUTATIONAL** finite source-authenticated proof replay. Full R_mix341 isometry, mixed hardness, B1/B2/B3 and P versus NP remain OPEN. All task identities, states, staggered schedules, rules and weights remain unchanged.

## Published hardness with exact model
Haken (1985) proves that for all sufficiently large h and every ordinary unrestricted shared-DAG Resolution refutation of unary PHP(h+1,h), the proof has at least 2^(c h) lines for an absolute c>0. Input: h(h+1) variables, h+1 occupancy clauses and h*binom(h+1,2) collision clauses, signed ASCII DIMACS length Theta(h^3 log h) bits. It does not apply to Extended Resolution, R_mix341 or arbitrary SAT algorithms. Cook (1976) gives polynomial Extended Resolution proofs of the very same PHP sources.

## New formal proof-DAG transport
For any UNSAT CNF F=AND_i C_i and fresh t, set G_t(F)=AND_i(NOT t OR C_i). G_t(F) is always satisfiable when t=0 and entails NOT t iff F is UNSAT. Let E be binary signed Resolution plus paid conservative two-input DEF (one new output wire per node, all defining clauses available as views of that same paid node). Require definitions in the guarded proof not to depend syntactically or transitively on t. Then for every UNSAT F,

$$
D_E(F\vdash\bot)=D_{E_t}(G_t(F)\vdash\neg t).
$$

Proof: tag every node according to whether its ancestors include a source clause. Guard precisely those lines, copy each t-free DEF unchanged, and replay signed RES with identical pivots and parent IDs. A definition-only contradiction is impossible since conservative gate clauses are jointly satisfiable. Conversely no positive t literal exists in the guarded proof, so t cannot be a pivot; erasing every negative t gives a valid ER refutation of F. Both translations preserve the exact number of charged shared-DAG nodes.

**Positive-t escape:** The t-dependent conservative gate z=t AND x includes (NOT z OR t). Resolution with the guarded source (NOT t OR x) gives (NOT z OR x). This legal inference removes the guard and does not admit the stated naive erasure. It disproves unrestricted step commutation, not any quantitative full-system isometry.

**Consequence:** Guarded PHP single-unit entailments require exponential ordinary Resolution proof lines (LSPV-2/380 isometry and Haken) but polynomial paid t-free Extended Resolution proof nodes (Cook and this theorem). The entire guarded source is SAT with t=0. This is a model-dependent proof separation, NOT an all-algorithm SAT lower bound or B3.

## Independent controls and artifacts
Four signed polarity variants, each with three source clauses, one paid OR2 definition and five paid Resolution steps, were checked against the guarded versions. Producer 170 assertion groups, including complete 16-valuation gate/source tables per polarity, three SAT clause-deletion neighbors per polarity, guard SAT controls and five rejected malformed inferences. Independent verifier checked 40 signed Resolution steps, 168 checks, and rejected a corrupted derived clause. This is a finite valid proof-transport witness, not a global optimum.

Formal report: research/agents/lspv-3/2026-11-03_2224_LSPV-3_GUARDED_ER_TFREE385.tex.
Producer: experiments/arc/lspv3_385_guard_er_transport.js, blob bee1dd92fb9f0fda1ae94652c9cd6e456009205f.
Independent verifier: experiments/arc/lspv3_385_independent_guard_verify.js.
Raw: results/raw/arc/2026-11-03_2224_LSPV3_GUARDED_ER_TFREE385_raw.json, blob 64da425020cb8f9d3c2f99519535a9cc219b4beb.

## Corpus and Grok/Claude assessments
Read the November 2 12:04 five-role coordination directive, issue #3, AGENTS.md, CODEX.md, the pnp-research skill, LSPV-2/341 and /380, LSPV-3/374 /378 /379 /384 and LSPV-1/380. This extends LSPV-2/380 and reuses earlier paid-DEF source transport rather than asserting novelty for ordinary Resolution guarding. Read actual Grok folder file GROKPROOF/2026-11-04_0615_PROGRESS.md, blob 6603e613853e7cc358b9b0181f06b19fa26ec39c, where fully charged all-input FLMV transport remains OPEN. Read Claude folder file research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67, which concerns a restricted alternation-trading proof framework, not B3. Neither assessment licenses unrestricted computational hardness.

External literature review: Haken 1985, Cook 1976, Cook-Reckhow 1979. Github/OpenAI search for a matching signed-DEF checker found no official implementation; drat-trim and drat2er implement different formats.

## Falsifiers and specialist next steps
F1 paid DEF preserves exponential ordinary-Resolution guarded PHP cost: FALSE. F2 sharing defeats the t-free bijection: FALSE. F3 t-dependent DEF preserves the same naive guard morphism: FALSE at rule level. F4 hard guarded one-unit consequence implies hard SAT decision: FALSE, t=0 accepts.

LSPV-1 audit reflection/B3 and accidental t-dependent DEFs. LSPV-2 audit complete official DEF clause-view grammar and LOCAL-CONVERT ports. LSPV-3 extend or falsify the guard morphism for AND3, XOR and named-wire conversions. LSPV-4 charge all source/index/output access, explicit/lazy proof serialization, checks and all-phase peak space. LSPV-5 adversarially test stronger rules and nonuniform/hardcoded guard oracles.

**Next exact gap:** source-authenticated polynomial guard transport for every actual fixed R_mix341 rule. Neither full mixed worst-case superpolynomial minimum nor B3 has been established. P versus NP remains OPEN.
