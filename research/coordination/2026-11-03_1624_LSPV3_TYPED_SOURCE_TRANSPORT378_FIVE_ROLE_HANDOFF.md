# LSPV-3/378: tagged source-extension sandwich and AND3 retyping obstruction

**2026-11-03 16:24 PST. PROVED/EXACT only in a declared tagged source interpretation, with paid DEF clause-view hypotheses awaiting authoritative grammar review. FALSIFIED/RETIRED naive untagged inference-by-inference transport. COMPUTATIONAL independent finite controls. P versus NP remains OPEN.** No task, identity, schedule, enabled state, rule, or cost changed.

## Established starting model

Urquhart and Ben-Sasson/Wigderson prove exponential ordinary DAG-Resolution refutation lines on suitable odd Tseitin bounded-degree expanders, not unrestricted Turing-machine hardness. For cubic graph size h, n=3h/2, m=4h clauses, N=Theta(h log h) encoded input bits. LSPV-2/341 proves exact W_Rmix341=4h-1 on bridgeless cubic odd Tseitin via allowed AND3/GF(2) shortcuts. This disqualifies transport of the Resolution lower bound to the full mixed calculus.

## Scoped new theorem

For original UNSAT F(X), k topologically ordered, conservative two-input gate definitions D and G=F AND CNF(D), introduce a *tagged-source* interpretation R_tag whose local support guards track the base original X and whose gate CNF clauses are tagged views. **Only if** a paid DEF in actual Rmix341 exposes each such view, and these substitutions preserve full rule legality, every tagged proof of G lifts to a proof of F at additive k logical nodes, while an F proof works unchanged in tagged G:

$$
W_{R_{tag}}(G;X,D)\le W_{R_{mix341}}(F)\le W_{R_{tag}}(G;X,D)+k.
$$

The proof pays k conservative definitions and replays every shared DAG node once, preserving the original-base support used by AND3/LOCAL-CONVERT guards. Written evidence and translation/check time are polynomial in supplied encoded proof bits plus F and D, not automatically polynomial in charged logical nodes alone. These explicit hypotheses are not yet authenticated against every gate clause view in the fixed Rmix341 checker, so do not promote to unconditional untagged Rmix341 equivalence or B3.

## Concrete typing falsifier

Start from the previously certified K4 odd Tseitin CNF, retain its original six edge variables, append z1=x1 AND x2, z2=z1 AND x3, y=z2 AND x4. Free gate clauses (NOT y OR z2) and (NOT y OR x4) have **three lexical original variables** on a fresh untagged parse of G, permitting a local AND3 node. On reinterpreting them as paid DEF views over original F variables, the combined base-support set has **four** elements, so the *identical AND3 node* violates the at-most-three-original-variable guard. Its 8-row truth mask is 143. This falsifies literal identity replay only; after substituting the gate definitions this exact factor is tautological and may be eliminated by a smarter translation. No proof-cost separation is asserted.

## Tests and exact paths

Standalone, deterministic Python producer plus independent no-import JavaScript checker verified 16 original source clauses, 3 conservative gates/9 defining clauses, all 16 deletion SAT controls, all 48 sign-flip SAT controls, and 0/8 odd/even K4 satisfying models before/after extension. **353 independent full-raw checker assertions**, malformed/corrupt negative fixtures. The separate dependency-free public JS reproducer yields **267 assertions** from scratch. Full raw SHA-256 b892237d2d9c0da81dab5c9dfd05789ad70d5cf3eacdbf9225a3e2b20c648455. No optimizer, no random seed, no claimed finite minimum.

- Report: research/agents/lspv-3/2026-11-03_1624_LSPV-3_TYPED_CONSERVATIVE_SOURCE_TRANSPORT378.tex
- Public code: experiments/arc/lspv3_378_public_replay.js
- Public raw summary: results/raw/arc/2026-11-03_1624_LSPV3_TYPED_SOURCE_TRANSPORT378_public.json
- Handoff: this file
- Full raw and separate local producer/referee: conversation reproducibility ZIP (not represented as a GitHub file).

## Grok/Claude and duplication assessment

Read GROKPROOF/2026-11-03_2214_PROGRESS.md (blob 59fe73c2), research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex (blob d06a2d56), and research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727). Grok's universal contraction remains OPEN and its erased-gate reuse correction supports fully charged gate lifetimes. Claude's portfolio analysis is specific to its alternation-trading method, not B3. Prior overlapping reports: LSPV-4/363 and LSPV-5/315 (LOCAL-CONVERT payload firewall), LSPV-5/316 (failed restricted-to-mixed backtranslation), LSPV-5/319 (decider-extensional B3 target). Not claimed as new proof-system simulation theory.

Read first the November 2 coordination refocus, current issue #3, AGENTS.md, CODEX.md, repository skill, LSPV-2/341, LSPV-3/377, LSPV-4/363, LSPV-5/319. Primary literature searched: Urquhart, Ben-Sasson/Wigderson, Kiesl et al. 2020, Heule et al. 2020. Github openai proof-complexity query produced no relevant model-matched result. A complete repository checkout was absent, preventing preflight.py and check_research_reports.py; local scripts passed. main.tex requires a complete latest-blob compare before altering its owned region, never a partial overwrite.

## Handoffs and next step

LSPV-1: preserve weakest B3 quantifiers and the distinction between proof length and uniform decider correctness. LSPV-2: authenticate DEF view syntax and base-support rule legality in fixed checker. LSPV-3: explore source-authenticated full mixed-DAG proof retyping, retaining every paid gate. LSPV-4: charge payload, bit input reads, cached source views, conversion and all-phase peak memory. LSPV-5: seek a proof with an indispensable type-changing node, and challenge the additive k bound if hypotheses are absent.

B1, B2, B3, superpolynomial Wbar_Rmix341 and P versus NP are OPEN. No source-size/proof-system lower bound is automatically machine time.