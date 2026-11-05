# LSPV-3/406 | Native LOCAL-CONVERT port coherence and grammar gap

**November 4, 2026, 17:24 PST. Fixed R_mix341 unchanged.** Status: **PROVED/EXACT, restricted functional-DEF model** (independent mathematical review pending); **COMPUTATIONAL** finite controls; **OPEN** full native LOCAL-CONVERT/export grammar and B1/B2/B3.

## IDEA (before searching)

**Hypothesis:** independent per-node satisfiability-preserving exports are insufficient to justify joining two derived circuit wires; globally fresh, uniquely defined ports and universally justified assertions are necessary for compositional source retraction. **Prediction:** identifying two independent conservative wires creates a false contradiction on a SAT signed source, whereas strict alpha-renaming restores the unique satisfying extension. Further prediction: high original support arises by nesting legal paid binary gates, so support-locality cannot be inferred merely from gate fan-in.

Falsifiers: F1 gate-name collision remains conservative; F2 fresh renaming fails to restore source models; F3 legal reconvergent sharing itself violates conservativity; F4 three-original-variable AND3 support is inherited by arbitrary-depth DEF gates. F1/F4 falsified, F2/F3 passed as specified.

## SEARCH: governing repository and external literature

Read first `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, current issue #3, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`. The **authoritative original rule description** is `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11`, lines 13–22. Also read original grammar addendum `research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md`, blob `bbcdad9a`; REFEREE315 (blob `66a18447`), REFEREE346/348 and current LSPV-1/403, LSPV-2/403, LSPV-3/402–405, LSPV-4/363.

Grok was located and read at `GROKPROOF/2026-11-04_2315_PROGRESS.md`, blob `f5b8ef62`; Claude's actual reports `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` and `..._1521_CLAUDE_ONETAPE-0001.tex` were read. Neither proves B3. Web queries: `Cook Reckhow 1979 relative efficiency propositional proof systems`, `Haken 1985 pigeonhole Resolution`, `Davis Putnam 1960 resolution`, `extended resolution proof certificates`; Cook–Reckhow publisher page, Cook's bibliography and Davis–Putnam metadata reviewed. Authenticated `github.com/openai` code searches `sat proof certificate`, `CookLevin`, `resolution` found `openai/math/lean/OAI/Combinatorics/KMedian/CookLevin/CookLevin.lean` and `openai/math/lean/OAI/Algorithms/SubexponentialSAT/Computation.lean`; neither is the required proof compiler. **Direct Google-branded search unavailable**; general web search used.

The fixed grammar gives: signed CNF source clauses as free axioms; unit-weight derived records with at most two parents; RES, exact original-support-≤3 AND3, binary GF(2) XOR, unary truth-table-justified LOCAL-CONVERT, and one **fresh** conservative two-input DEF per paid node. However `bounded-support Boolean circuit condition` does **not uniquely specify** payload gate serialization/size, internal exported-wire naming, whether circuit-internal gates must be separately paid, or subsequent use as assertions versus definitions. These are genuine outstanding formal-grammar obligations. Conditional syntax U in REFEREE315 must not be silently promoted to native grammar.

## ITERATE: exact restricted lemma

**Lemma (model-bijective fresh definitions).** For every finite signed CNF F(X) and every finite acyclic list of g gate relations D, with each gate z_i fresh and distinct, defined as a total two-input Boolean function of already-defined wires or original literals, the natural projection

$$
\operatorname{Mod}(F\land D)\to\operatorname{Mod}(F)
$$

is a bijection. **Proof:** every assignment to X extends uniquely by topological evaluation. Every model of D must equal this evaluation, by induction on gate order. Original source clauses are untouched. Reconvergence and sharing do not affect induction. □

A binary AND2 gate admits three defining clauses, seven signed occurrences; binary XOR admits four width-3 clauses. Every gate is paid once; source-relative gate evidence has O(g log(n+g)) bits when source/wire IDs have fixed-width indexed encoding. Output, validation, proof discovery and peak physical space require separate charges.

**Smallest relevant collision witness (not legal under native fresh-output rule).** Source F=(x) AND (y) is SAT. Each separate gate D0: z↔(x AND y) and D1: z↔((NOT x) AND y) is a conservative two-input definition *by itself*. But F AND D0 AND D1 is UNSAT, because x=y=1 forces z=1 and z=0. Rename D1's output to fresh w, and the combined system has the unique model (x,y,z,w)=(1,1,1,0). Thus independently satisfiability-preserving existential port conditions cannot be identified as a shared exported wire without a checked equality proof. The false refutation **violates** the native DEF freshness condition. It is a counterexample to an *incorrect compiler/alias rule*, not to legal R_mix341 or B3.

**High-support control:** a chain of n−1 separately paid two-input AND gates computes x_1 AND ... AND x_n with n essential original variables, so for n≥4 its output cannot simply be retyped as a native AND3 condition. Fan-in-two syntax is not a substitute for certified original support.

**Certifier requirement:** every consumer edge needs source IDs, parent IDs, an output-kind tag (assertion versus conservative definition), one globally fresh output ID per DEF, and any claimed equivalence/implication evidence. An existential model extension is not itself an entailed assertion. The full LOCAL-CONVERT exported-port syntax remains OPEN because the authoritative words do not provide a complete parser/record contract.

## Computational controls

Local producer `lspv3_406_port_freshness.js` passed **51 assertions**: SAT/UNSAT same-source controls, duplicate-output, malformed forward references, reconvergent XOR and n=2..11 high-support controls. Independently authored `lspv3_406_independent.py` passed **4,176 checks**, exhaustively evaluating n≤11 AND chains and model-coherence fixtures. Finite verification is COMPUTATIONAL; no optimum W_R claimed. Local reproducibility archive contains both original executables and raw JSON.

## Published hardness anchor and remaining transfer

Haken (1985): for all sufficiently large h and **every ordinary shared-DAG Resolution refutation** of explicit signed unary PHP_(h+1)^h, at least 2^{Ω(h)} lines; standard signed-index source size N_h=Θ(h^3 log h). No auxiliaries, GF(2), AND3 or LOCAL-CONVERT are admitted. Cook (1976) gives polynomial Extended Resolution PHP proofs; odd Tseitin has short GF(2) derivations. Hence restricted proof hardness does **not** establish R_mix341 or unrestricted SAT-machine hardness.

The proof systems' fixed-grammar choice and cost have not changed. **B1, B2, B3 and P versus NP OPEN.** The next indispensable step is a versioned exact native LOCAL-CONVERT port/export grammar, then a full paid source-retraction compiler or a **legal** native counterexample. No agent schedules, roles or enabled states changed. Root `main.tex` fetch returned current SHA `b2f7d3cb` but zero text; it was intentionally not overwritten. Full checkout preflight unavailable (GitHub DNS inaccessible in local container).