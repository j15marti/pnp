# LSPV-4/388: The quantified-projection validation firewall

**November 4, 2026, 07:36 PST | PNP Time-Space Resource Auditor**

**Status:** PROVED/EXACT for the mathematical reductions from known quantified-SAT results; finite checks COMPUTATIONAL; independent specialist review PENDING. B1/B2/B3, superpolynomial minimum cost for unchanged R_mix341, and P versus NP OPEN.

## Source and exact theorem

Start from Haken (1985): the standard unary pigeonhole CNF for h+1 pigeons and h holes has (h+1)+h*binom(h+1,2) clauses, conventional binary signed-literal encoding size N_h=Theta(h^3 log(h+2)), and every **ordinary shared-DAG Resolution** refutation has at least 2^(c h) lines for some c>0 and all sufficiently large h. The quantifier is over all Resolution DAG proofs, not all SAT algorithms. Cook's polynomial Extended Resolution proofs and the mixed GF(2) shortcut on odd Tseitin remain mandatory countercontrols.

The unchanged R_mix341 is specified in `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb): free original clauses, unit-paid binary RES, constant-three-original-variable AND3, binary XOR rows, explicit local truth-table LOCAL-CONVERT and unit-paid conservative two-input DEF. **It does not include an arbitrary existential-hidden-CNF conversion**. The following is a hostile proposed rule model, not a legal new R_mix341 rule.

Let J(X,Y) be an explicitly encoded signed 3CNF, where X comprises u public bits and Y comprises e hidden bits. Define the projected boundary $$B_J(x)=1\iff\exists y:J(x,y)=1.$$ Let R(X) be an explicitly given Boolean circuit and ask whether $$\forall x\;(B_J(x)=R(x)).$$

**Theorem 388.1:** This exact implicit-projection equality problem is Pi_2^P-complete under polynomial many-one reductions, even with R(X)=TRUE. Membership: failure has either x,y satisfying J and falsifying R, or x satisfying R with all y falsifying J; the union is Sigma_2^P. Hardness: R=TRUE makes the question precisely $$\forall X\exists Y\;J(X,Y),$$ the known Pi_2^P-complete forall-exists quantified 3SAT problem (Döcker, Dorn, Linz and Semple, 2019). The reduction is a linear-output copy plus constant target. No oracle or nonuniform advice.

**Theorem 388.2 (one public bit):** Given any CNF H(Y), set $$J_H(x,Y)=\bigwedge_{C\in H}(\neg x\lor C).$$ Then B(0)=1 and B(1)=SAT(H). Hence the one-literal target R(x)=NOT x is exactly equal to B iff H is UNSAT. The equality question is coNP-complete on this syntactically recognizable guard image: a failure witness is an H satisfying assignment. Likewise, projected equality to FALSE for general J is coNP-complete. This sharpens the earlier guarded-boundary identity; not claimed academically novel.

**CORRECT LIMITATION:** When there are at most three original support variables and no arbitrary existential witnesses, an explicit truth-table entailment is at most eight cases. If an arbitrary constant-fed circuit is embedded, gate acquisition costs polynomial time (CVP-hardness may be relevant), but no Pi_2 conclusion follows from the fixed original R syntax. Conservative DEF gate variables extend uniquely; they cannot be silently interpreted as arbitrary existential choices.

## Fully charged T/S

For M input bits, u public and e hidden variables, exhaustive double-loop evaluation on indexed read-only input gives conservative native-machine upper bounds $$T=O(2^{u+e}(M+1)^3),\quad S=O(u+e+\log(M+2))$$ writable bits, including parsing, source queries, address heads and loop counters. This is NOT square-root space when u+e is linear in M. The Python implementation uses host memory and is not a native-space benchmark. Materializing a dense boundary needs 2^u output bits; writing an explicit Skolem map needs e*2^u bits. Neither is compulsory if a compact circuit, lazy evaluator or recomputation is used. A short output relation does not make its semantic equivalence cheap. A rejecting decider trace does not certify program correctness.

## Four falsifiers and controls

1. One-bit boundary always has constant acquisition cost: FALSIFIED for arbitrary hidden H; exact relation checking is coNP-complete.
2. Compact output TRUE always admits cheap independent semantic validation: FALSIFIED for unbounded public X with existential Y; Pi_2^P-complete.
3. A unit-paid existential semantic jump is already legal R_mix341 LOCAL-CONVERT: FALSE. The fixed actual rule has constant-original-support local entailment and conservative paid definitions.
4. Dense-table output is compulsory and its size lower bounds every algorithm: FALSE. Compact targets, sharing, and lazy source access remain valid alternatives.

**Finite controls:** producer checked 1,031 well-formed signed CNFs in two independent enumeration orders and 31,337 assertion/check groups, rejected 10 malformed records. An exhaustive 256-formula two-variable hidden-H guard test classified 95 SAT and 161 UNSAT H, with exact projected relation NOT x iff UNSAT. Four hand-chosen both-label cases passed. Independent Node verifier reconstructed all 256 guards plus 12 relation fixtures: 530 checks. Initial public-assignment bit-order mismatch detected and repaired before publication; results are for corrected code. These numbers are not evidence of an asymptotic lower bound.

## Project and outside review

Reviewed latest issue #3 (including peer results through LSPV-2/392), AGENTS.md, CODEX.md, pnp-research skill, LSPV-2/341, LSPV-2/392, LSPV-4/386; relevant LSPV-1/391 and LSPV-3/395 handoffs. Located **GROKPROOF/2026-11-04_1518_PROGRESS.md** blob 4e2bb9d941295f620a64e078117d29244caf4fba, **research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex** blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67, and **research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex** blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a. Their assertions concern conditional ARC contraction and restricted alternation-trading/sequential-input models. None proves B3.

Literature/search queries: "forall exists quantified 3CNF Pi2 complete QSAT2 QBF CNF", "Haken 1985 exponential resolution pigeonhole extended resolution Cook", project and OpenAI GitHub SAT proof implementations. We do not claim a failed search proves novelty.

**Bridge:** B1 is a pointwise statement for every fixed uniform total decider and UNSAT input; B2 uses the maximum run time over *all* inputs <=N of each decider; B3 is SAT in P implying polynomial worst-case Wbar for the SAME preselected R_mix341. This complexity classification does not prove or disprove any of them.

Next target: a complete typed, effectively and polynomially verified certificate grammar for actual R_mix341 LOCAL-CONVERT/DEF under all source conditions, followed separately by a valid B3 simulation. P versus NP remains OPEN.

## References
[1] Haken, *The Intractability of Resolution*, TCS 39 (1985), 297-308, https://doi.org/10.1016/0304-3975(85)90144-6 .
[2] Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976), 28-32.
[3] Döcker, Dorn, Linz, Semple, *Placing quantified variants of 3-SAT and Not-All-Equal 3-SAT in the polynomial hierarchy*, 2019, https://arxiv.org/abs/1908.05361 .
[4] Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36-50.

Related code: `experiments/arc/lspv4_388_projection_audit.py`, independent verifier `experiments/arc/lspv4_388_independent_verify.js`, raw `results/raw/arc/2026-11-04_0736_LSPV4_PROJECTED_CONVERSION388.json`. No task/schedule/rule/weight mutation.