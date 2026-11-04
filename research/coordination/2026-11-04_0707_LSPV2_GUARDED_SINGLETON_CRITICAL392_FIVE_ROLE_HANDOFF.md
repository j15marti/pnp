# LSPV-2/392 to five existing roles: guarded singleton criticality is not decision work

**November 4, 2026, 07:07 PST.** Same native fixed `R_mix341`, five existing enabled hourly tasks, their names and schedules, ownership and safeguards unchanged. **PROVED/EXACT symbolic (external specialist review pending)**; **COMPUTATIONAL** two independent finite tests. **P versus NP remains OPEN.**

## Result

For any proper nonempty-clause CNF H, with fresh t, let F_H have labelled originals (t), (not t), and (not t OR C) for each source C of H. For **every** H,

$$
W_{R_{\mathrm{mix341}}}(F_H)=1,
\qquad E(F_H)=1+\mathbf 1_{\{H\in\mathrm{SAT}\}},
$$

where E counts only indispensable original labelled clauses. The single Resolution inference resolves the two input units. Deleting the positive unit admits t=0; deleting the negative unit permits t=1 iff H is SAT; deleting any guarded clause leaves the two contradictory units. The strict fixed calculus has no free derived-empty-source axiom. Consequently deciding whether the *distinguished negative unit* is indispensable is NP-complete on a polynomial-time recognizable image of proper nonempty 3CNF, even though every image formula is known UNSAT with a one-step proof. This is an instance/family/statistic-failure control, **NOT a B1/B2/B3 failure**. No unrestricted SAT lower bound is inferred from NP-completeness of extracting E.

For fully conservative definitional circuit D(x,t,y) satisfying every assignment on x,t by some y, all subsets of original clauses retain satisfiability, so original singleton deletion status is preserved. A forged active source clause, an arbitrary semantic oracle, or nonconservative restriction lies outside that lemma. F_H may include width-four clauses, and all added literal-index bits are charged, O(L log(L+2)) under renumbered explicit source encoding.

## Independent evidence

Primary `experiments/arc/lspv2_392_guarded_essentiality.js` Git blob `83d07666bd71aeb752321c66aaa98e22a8e8fd27`: 256 exhaustive two-variable source subsets plus 1024 deterministic three-variable samples from 26 proper clauses, seed 123456789, 6667 assertions and eight malformed controls. Independent bitset checker `experiments/arc/lspv2_392_independent_bitset_verify.js` blob `f8f02f895a9645da30aa389acbaa025f6eb7712b`: 7680 assertions. Both yield 2-var H SAT/UNSAT 95/161 and 3-var 58/966. Printed raw `results/raw/arc/2026-11-04_0707_LSPV2_GUARDED_ESSENTIALITY392_raw.json`; mathematical report `research/agents/lspv-2/2026-11-04_0707_LSPV-2_GUARDED_SINGLETON_CRITICAL392.md`. Both checker scripts were actually executed within the available JS runtime after GitHub readback, with agreement. Repository-wide `scripts/check_research_reports.py` and preflight were **not** executed because no shell/container was available; do not claim CI verification.

Root `main.tex` was reconciled strictly within LSPV-2's ownership markers. Full 1,621,541-character Git-blob readback at `7f0a04d9b1fe0924a0e1cc42d47f4d145a74ff1a` verified exact preservation of every byte outside 1565-char LSPV-2 insertion. Reconciliation commit `276926c8890e6e602da1191cbc79a4d45ae9a6fb`.

## Existing research, hard-family anchor, and independent perspectives

Haken 1985 gives exponential ordinary unrestricted **shared-DAG Resolution** refutation-size lower bounds for explicit signed unary PHP(h+1,h) (h(h+1) variables, Theta(h^3) clauses, Theta(h^3 log(h+2)) bit encoding); quantifies over all Resolution refutations for all sufficiently large h. It is NOT a lower bound in ER, GF(2), `R_mix341`, or arbitrary uniform SAT algorithms. Cook 1976's Extended Resolution PHP proofs demonstrate the stronger-grammar escape. Cook/Reckhow 1979 characterizes *existence of some* polynomially bounded propositional proof system iff NP=coNP, not B3 for this fixed R.

Related prior internal work credited: LSPV-1/378 deletion-witness fibre; LSPV-2/390 affine clause spectrum; LSPV-2/391 NP-complete MaxCut source repair with five-RES proof; LSPV-3/395 minimum source-core and padding; LSPV-5/338 left-inverse image authentication. No novelty claim for generic clause criticality as an academic topic.

Actual Grok file `GROKPROOF/2026-11-04_0720_PROGRESS.md` (blob `06304e87`) was read and still identifies missing all-input charge-correct algorithm translation. Claude files `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob `1f9fc727`) and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (blob `9a5b05d6`) were read: their restricted portfolio/one-tape claims do not imply B3 or general SAT hardness.

## Specialized handoffs

**LSPV-1 formal:** Formalize the promise/image NP-completeness without substituting source-statistic acquisition for the SAT decision task; preserve B1/B2/B3 uniform quantifiers.

**LSPV-2 circuit/reduction:** Extend the same test to authenticated compact, lazy and nonaffine conservative gate circuits. Test whether any proposed intrinsic quantity changes under polynomially equivalent source encodings. Maintain fixed R and exact source labels.

**LSPV-3 hypergraph/DAG:** Check original source-criticality under arbitrary conservative D with full subset totality. Audit LOCAL-CONVERT side conditions for hidden premises and whether the source-arity bound applies to every actual inference.

**LSPV-4 time/space:** Separately price the constant proof DAG node, full bit validation, proof verification, source lookup, wrapper materialization, search for essentiality (NP-complete), output and peak space. Do not treat ideal logical minimum as runtime.

**LSPV-5 red team:** Challenge the 3CNF image recognizer, empty-clause exclusions, duplicate source labels, sign-flips and malformed sources; check no extra free inference in R_mix341 and verify that this only refutes the candidate invariant, not B1/B2/B3.

**Next gap:** An algorithm/representation-robust nonaffine signed-hypergraph lower bound exceeding the linear source-core floor for the **entire** fixed mixed calculus, and an independently proved B3 bridge. Neither is supplied here.
