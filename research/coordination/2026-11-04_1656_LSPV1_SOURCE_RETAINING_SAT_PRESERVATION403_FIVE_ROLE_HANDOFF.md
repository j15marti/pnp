# LSPV-1/403 five-role handoff: source-retaining SAT-preservation firewall

**November 4, 2026, 16:56 PST, America/Los_Angeles.** Existing LSPV-1 specialist, same task ID `6ad6f02da1bc8191bfd844daded8e1ec`. **Status:** PROVED/EXACT symbolic theorem in a declared restricted class of polynomial-clocked SAT preprocessors, independent specialist review pending. B1/B2/B3, unrestricted mixed-calculus minimum lower bounds, and P versus NP remain **OPEN**. Do not change the fixed `R_mix341` grammar, rules, weights, tasks, schedules or enabled states.

## IDEA -> SEARCH -> ITERATE

**IDEA and falsifiers.** Ask whether global SAT-preservation of an arbitrary claimed representation switch is automatically computable from its source code even after all original signed CNF clauses are retained and only two fresh contradictory unit clauses can be appended. Attack with (1) an alleged universal checker of restricted transducers, (2) source copying as a supposed soundness certificate, (3) delayed halting beyond finite test cutoff and (4) malformed/SAT/UNSAT opposite-label controls.

**SEARCH.** Read the authoritative 2026-11-02 five-role refocus (Git blob `033b54b8`), current issue #3, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, REFEREE344/345/347/348, LSPV-1/402, LSPV-2/403, `GROKPROOF/2026-11-04_2315_PROGRESS.md` (blob `f5b8ef62`), and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (blob `9a5b05d6`). Neither Grok nor Claude establishes B3. Older `research/review/reports/redteam/2026-10-11_1736_RT-0015.tex` (blob `7258f5a9`) already showed no computable complete extensional canonicalizer for polynomial-clocked programs, so new classification is an intentionally narrower exact-source-copying CNF specialization rather than a newly discovered Rice theorem. Primary literature consulted: Haken 1985 (ordinary Resolution PHP), Cook 1976 (ER PHP), Cook--Reckhow 1979 (exact-target proof systems), Hoyrup ICALP 2016 (subrecursive program properties). General-web actual queries included "Rice theorem equivalence of total polynomial-time functions", "equivalence of clocked polynomial transducers", "compiler semantic preservation undecidability", "Cook Reckhow propositional proof systems". Direct branded Google search was not available and was not claimed. OpenAI GitHub scoped queries "CookLevin" and "proof verifier" found `openai/math/lean/OAI/Combinatorics/KMedian/CookLevin/CookLevin.lean` (blob `1e23a159`), not a B3 compiler.

**ITERATE: PROVED/EXACT in its stated model.** Let `T_P(F)` copy every original clause exactly and either append no clause or append fresh `(z),(-z)` if an explicitly polynomial-clocked predicate `P(F)` accepts. Malformed inputs are unchanged. Then the program-index set
```
GOOD = {P : for every binary input x, SAT(T_P(x)) = SAT(x)}
```
is **Pi^0_1-complete**. Membership: enumerate inputs and use terminating exhaustive SAT checks to enumerate failures. Hardness: for arbitrary `M,w`, let `P_{M,w}` activate only on canonical SAT sources `U_n=(x1)&...&(xn)` if `M(w)` halts within `n` steps. It is one fixed uniform polynomial-time program per `M,w`. It preserves all labels exactly if `M(w)` never halts, and maps some SAT `U_n` to UNSAT if it halts. Hence NONHALT many-one reduces to GOOD.

The simple **source-retention firewall** is that `UNSAT(F) => UNSAT(T_P(F))` holds, but `UNSAT(T_P(F)) => UNSAT(F)` fails for SAT inputs with appended contradictory units. Thus source copying and fully charged polynomial runtime alone are not sound back-retraction certificates.

**Failure and repair in finite testing.** An initial SAT control `[[1],[2]]` was itself the canonical trigger `U_2`. Replaced by genuinely noncanonical SAT `[[1],[3]]`. A deterministic Python producer passed 750 checks on 108 threshold cases, eight SAT/UNSAT controls (including Horn, 2SAT and even/odd K4 Tseitin), and seven malformed arrays. An independent JavaScript verifier passed 561 checks. Finite tests are COMPUTATIONAL, not proof of the Pi^0_1 statement. Each Python invocation was short and deterministic.

**Exact hard-family scope.** Haken: `exists c,h0 for all h>=h0 for all authentic ordinary shared-DAG Resolution refutations pi of unary PHP_{h+1}^h: |pi|>=2^(c*h)`. Signed binary-index input length `N_h=Theta(h^3 log h)`. This theorem excludes Extended Resolution, Res(XOR), GF(2), paid definitions, LOCAL-CONVERT and unrestricted SAT algorithms. Cook 1976 gives polynomial ER proofs. The transducers here are not legal `R_mix341` rules and do not alter its paid-node minimum.

## Published artifacts

- Formal symbolic report: `research/agents/lspv-1/2026-11-04_1656_LSPV-1_SOURCE_RETAINING_SAT_PRESERVATION403.tex`, initial publication commit `7ac73d8815971f785729dc2d9f3548e9224766dd`.
- Deterministic Python producer: `experiments/arc/lspv1_403_sat_preprocessor.py`, commit `fa9fa62a3e67dfcae2b4cacf3526d13ca5153315`.
- Independent JavaScript verifier: `experiments/arc/lspv1_403_independent_verify.js`, commit `f7204cfc8c427d3b1ed4be283d91eeb93474372a`.
- Raw 108-case results: `results/raw/arc/2026-11-04_1656_LSPV1_SOURCE_RETAINING_SAT_PRESERVATION403_raw.json`, commit `691967fdee20de086ebab7ab0bbb42f923d1fda7`.
- This handoff: `research/coordination/2026-11-04_1656_LSPV1_SOURCE_RETAINING_SAT_PRESERVATION403_FIVE_ROLE_HANDOFF.md`. Readback status separately recorded.

## Unmodified specialist roles and next targeted audits

**LSPV-1:** Audit Pi^0_1 quantifiers, fixed clock and exact-source retraction; seek weakest noncircular B3 for `R_mix341`.

**LSPV-2:** Implement rule-by-rule source-sound LOCAL-CONVERT witness and compact XOR/ER countercontrols; do not mistake a general preprocessor for a native inference rule.

**LSPV-3:** Examine clause-ID and provenance signed-hypergraph DAG source equivalence with auxiliary exports, including the counterexample `SAT(F), UNSAT(T_P(F))`.

**LSPV-4:** Independently charge source copying, fresh-index discovery, bounded simulation, output bits, verification and all-phase peak space; distinguish program-index decidability from one-input executable cost and FLMV.

**LSPV-5:** Red-team Pi^0_1 membership/hardness and strict parser, ensure no overclaim of a full mixed-calculus restriction; assess the existing RT-0015 duplication and prior REFEREE348.

**Publication safeguards.** Root `main.tex` was refetched from GitHub with a valid blob SHA `d859ad9bce9f6adc2744f30d7655117a255fa966` but **zero returned content**. Therefore its full approximately 1.6 MB original could not be preserved by a safe edit. No root overwrite attempted; this report and handoff are the documented fallback. A direct raw GitHub fetch from the container failed DNS, so test validation is local plus GitHub connector readback rather than claiming a raw download test. Predecessor REFEREE348 was a substantive readback-verified Markdown write, but lacked a literal report sentinel; future predecessor reports should retain the required sentinel. No task mutations occurred.

**Next obligation:** Authenticate the actual `LOCAL-CONVERT` exported-wire, support and definition rules and prove a source-sound polynomial compiler in the unchanged fixed calculus. B1, B2, B3, superpolynomial `Wbar_Rmix341`, and P versus NP remain **OPEN**.
