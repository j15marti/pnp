# LSPV-4/397: Guarded Horn-Consequence Firewall and Proof-Carrying Subformula Repair

**November 4, 2026, America/Los_Angeles, afternoon PST.** **PROVED/EXACT** for the stated complexity reduction, already established as the guarded-projection mechanism in LSPV-4/388; **PROVED/RESTRICTED** for the new concrete signed-Resolution Horn-subformula repair; **COMPUTATIONAL** finite controls. **OPEN** B1/B2/B3, full `R_mix341` transfer, mixed superpolynomial minimum, P versus NP. No changes to fixed rules/weights, five roles, ownership or hourly schedules.

## IDEA before searching
Grok's `GROKPROOF/2026-11-04_2315_PROGRESS.md` proposes extracting Horn/2-SAT/XOR consequences `G` and verifying `UNSAT(F and not G)` using only polynomial-time Horn/2-SAT/XOR solvers. Falsifiable prediction: tractability of `G` alone does **not** make the entailment query tractable when `F` is arbitrary 3-CNF. A correct repair is to prove `G` from an authenticated **tractable subformula** of `F` and emit a locally checked Resolution trace, or else explicitly certify that the whole validation formula is in a tractable class.

Falsifiers: (1) SAT original H induces an invalid claimed unit; (2) UNSAT H induces a valid unit although guarded F itself remains SAT; (3) a Horn unit consequence is accepted by a solver without checking full F; (4) malformed signed clauses, illegal Resolution pivots, and odd/even affine Tseitin controls.

## SEARCH, sources, duplication and exact provenance
Read controlling `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`; issue #3; `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`; original system `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11`); `GROKPROOF/2026-11-04_2315_PROGRESS.md` (blob `f5b8ef62`); Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob `1f9fc727`); LSPV-3/402 (blob `4b301395`) and LSPV-4/393 and /396. The guarded-unit coNP-completeness theorem was **already** proved in `research/agents/lspv-4/2026-11-04_0736_LSPV-4_PROJECTED_CONVERSION_QUANTIFIER_FIREWALL388.md`; no novelty is claimed for that core reduction. LSPV-1/399 already corrected Grok's unrelated strict exponent mistake; not reproved here.

Primary references checked: Haken (1985), *The Intractability of Resolution*, TCS 39:297–308, DOI 10.1016/0304-3975(85)90144-6; Cook & Reckhow (1979), *Relative Efficiency of Propositional Proof Systems*, JSL 44:36–50; Dowling & Gallier (1984), *Linear-Time Algorithms for Testing the Satisfiability of Propositional Horn Formulae*, JLP 1(3):267–284, DOI 10.1016/0743-1066(84)90014-1; Krajicek (2012), *A Note on SAT Algorithms and Proof Complexity*, IPL 112:490–493, https://www.karlin.mff.cuni.cz/~krajicek/sat.pdf. The latter specifically conditions computational lower-bound transfers on short **formal reflection proofs**. Actual web searches: `propositional proof systems feasible reflection principle polynomially bounded extended Frege`; `CNF implication checking Horn consequence coNP complete implication single literal guarded SAT`; `Horn satisfiability unit propagation linear time Dowling Gallier`. Direct Google-branded interface unavailable; used general web search, without claiming separate Google results. GitHub searches in `openai` for `SAT proof checker`, `ExecCNFWidthCorrectness`, `SAT certificate`; read `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFWidthCorrectness.lean` (blob `1944f3fc`). It proves a bounded-width executable driver's behavior but not a certificate transfer to `R_mix341`. Grok and Claude do not establish B3.

## PROVED/EXACT: unit consequent remains coNP-complete
For arbitrary proper 3-CNF H(Y), choose fresh guard x and per-clause fresh y_C. For C=(a or b or c), define two proper width-three clauses

$$
(\neg x\lor a\lor y_C)\;\land\;(\neg y_C\lor b\lor c).
$$

Let F_H be their conjunction and G=(not x), a **unit clause simultaneously Horn, 2-CNF and affine**. Every F_H is SAT: set x=0, all y_C=0. But the residual at x=1 is existentially equivalent to H. Hence

$$
F_H\models (\neg x)\iff H\text{ is UNSAT}.
$$

Non-entailment has a polynomial assignment witness, so deciding entailment of a **one-literal Horn/2SAT/affine conclusion** from an arbitrary proper width-three source is coNP-complete, **even on the promise that the source F is SAT**. This is a standard guarded-reduction consequence (project /388), not a lower bound against all algorithms. Any validator merely classifying G as tractable and then running a Horn/2SAT/XOR algorithm on general F and not G has no proven correctness.

The finite producer additionally uses a source with single-/two-literal clauses; a fresh-sign splitting gadget makes each guarded clause a **proper width-three** clause and preserves this identity, with all source clauses authenticated.

## PROVED/RESTRICTED: sound and charged Horn-subformula repair
Fix one valid ordinary signed CNF F, with each original clause address authenticated. Let S be the conjunction of **exactly those original clauses** with at most one positive literal. Thus F implies S. Apply unit propagation to S. Every unit consequence or empty contradiction is accompanied by genuine strict binary RES inference nodes, with signed source references and pivots checked against F. Thus each emitted consequent D satisfies F entails D, and a derived empty clause is a valid Rmix341 refutation. If no such inference is available report UNRESOLVED. No semantic oracle is invoked; **completeness for arbitrary CNF is not claimed**. A falsely claimed arbitrary single-literal implication from F_H is not emitted without a derivation.

The straightforward producer parses all of F, may buffer source and proof, and scans all selected clauses at most O(N) times; with each source clause of width at most N, O(N^3) clauses/literal inspections plus up to O(N^2) proof nodes give a conservative polynomial-time bound O(N^4) including naïve set manipulation, and O(N^3 log(N+2)) proof-buffer bits as a coarse upper bound. Explicit proof serialization and re-verification cost extra polynomial work. In the actual host implementation both source and proof are buffered. These are declared *upper* bounds, not the FLMV same-machine sublinear-space profile. Discovery/strategy selection (one syntactic scan), failed trials, source-index lookups, simultaneous live arrays, output, verification and malformed rejection are charged. Perfect minimum proof discovery is not asserted.

## ITERATE: failed implementation, repair and independent tests
The first producer incorrectly continued when a source Horn clause had **zero** remaining unset literals after propagation, returning PARTIAL on F=(a) and (not a or b) and (not b). This was a real unsound/incomplete implementation error, not an accepted result. Repaired it to RES-eliminate *all* falsified source literals and emit the empty-clause node, and to avoid redundant derivations of already-known units. Reran all controls and a separately implemented JavaScript referee.

For all 256 nonempty-clause subsets of the eight non-tautological signed clauses on two variables, precisely 95 are SAT and 161 UNSAT. Their proper 3-CNF guarded sources are **all 256 SAT**, and `F and x` has a model exactly for the 95 SAT originals. Producer: **1,572 assertions**, ten malformed controls rejected, positive Horn entailment and complete Horn UNSAT contradiction certificate checked, and odd/even K4 Tseitin yielded 0/8 assignments. Independent no-import JavaScript referee: **1,549 checks**, independently exhausts all 256 guarded instances, truth assignments, signed Resolution nodes and parity controls. Finite checks do not establish asymptotic machine hardness.

## Established hardness model and missing transfer
Unary PHP with h+1 pigeons/h holes has h(h+1) variables, (h+1)+h*binom(h+1,2) clauses, explicit binary indexed signed input N_h=Theta(h^3 log h). Haken (1985): some fixed c>0 and h0, for **all** h>=h0 and **every** ordinary shared-DAG Resolution refutation, at least 2^(c h) proof lines. The theorem excludes GF(2), extension variables, LOCAL-CONVERT, and arbitrary uniform machine algorithms. Cook's polynomial Extended Resolution PHP construction is mandatory countercontrol. Odd expander Tseitin can be ordinary-Resolution hard yet has a linear 4h-1 mixed proof in fixed Rmix341; no proof-cost lower bound for the full mixed system follows.

For the **same fixed** system Rmix341, the central obligation remains B3:

$$
\mathrm{SAT}\in P\;\Longrightarrow\;\overline W_{R_{\mathrm{mix341}}}(N)=N^{O(1)}.
$$

B1, B2, B3, a superpolynomial worst-case mixed minimum, and P versus NP remain OPEN. The repair only certifies a sound restricted local source-deduction procedure, not an all-input fast solver or proof-system hardness transfer.

## Reproducibility and ownership
Producer `experiments/arc/lspv4_397_guarded_horn_firewall.py`; independent referee `experiments/arc/lspv4_397_independent_verify.js`; raw result `results/raw/arc/2026-11-04_1536_LSPV4_397_guarded_horn_raw.json`; role handoff `research/coordination/2026-11-04_1536_LSPV4_GUARDED_HORN_FIREWALL397_HANDOFF.md`. Code hashes locally: producer SHA256 `8efcceae3e99c0df4cdea18911dab33ee81e09f062919b512dec32008d15827e`, referee `48276659f2110750e642d1b9f54671d1a42dfdc20ada8676329fe38f53a1c9be`. Root `main.tex` unchanged unless a fresh, full, conflict-safe authorized-marker reconciliation succeeds; no tasks modified.

References: [1] Haken, TCS 39 (1985), 297–308. [2] Cook, SIGACT News 8(4) (1976), 28–32. [3] Cook and Reckhow, JSL 44 (1979), 36–50. [4] Dowling and Gallier, JLP 1(3) (1984), 267–284. [5] Krajicek, IPL 112 (2012), 490–493.
