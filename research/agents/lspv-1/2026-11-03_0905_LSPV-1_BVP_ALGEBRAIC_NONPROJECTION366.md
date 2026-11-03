# LSPV-1 366: Alekseev BVP reverse-transfer firewall

**November 3, 2026, 09:05 PST.** P versus NP remains **OPEN**. **PROVED/EXACT**, conditional only on an established external proof-size theorem and the already proved project carry-CNF upper bound: a polynomial-output proof backtranslation from the Boolean carry-CNF to the original algebraic Binary Value Principle is impossible, even nonuniformly. **COMPUTATIONAL:** 1,264 independent source/Resolution replay assertion groups. External mathematical review is pending.

## One preselected calculus and cost

Use unchanged $R_{\mathrm{mix341}}$, with authenticated zero-cost original CNF clauses; unit cost for each genuine strict binary Resolution, exact local AND3, GF(2) XOR, LOCAL-CONVERT and conservative signed fresh two-input VARDEF node, with sharing charged once. Let

$$
W_R(F)=\min_{\pi:F\vdash_R\bot}|\pi_{\mathrm{derived}}|,\qquad
\overline W_R(N)=\max_{F\ {\rm valid\ UNSAT},\ |\operatorname{enc}(F)|\le N}W_R(F).
$$

$N$ counts encoded bits. The fixed calculus and the definition of B1, B2, B3 have not changed.

## Established lower-bound starting point

**KNOWN THEOREM [1, Theorem 1.1]:** For the original algebraic system

$$
P_n:\qquad 1+\sum_{i=1}^n 2^{i-1}x_i=0,\qquad x_i^2-x_i=0\quad (1\le i\le n),
$$

over the rational field, every refutation in Alekseev's algebraic Ext-PC-with-extension-and-square-root calculus has **bit size** at least $2^{cn}$ for some $c>0$ and all sufficiently large $n$. The algebraic input uses $O(n^2)$ encoded bits, including binary coefficients. The published paper explicitly states that this algebraic source is not the standard arithmetization of any polynomial-size CNF, and its lower bound does **not** establish a Frege or Extended Frege lower bound on CNF formulas. Source [1] was inspected at the original paper, pages 4 to 5, including the statement and warning.

**PRIOR PROJECT EXACT THEOREM [2, LSPV-3 354, November 2, 2026, 22:24 PST]:** The faithfully equisatisfiable Boolean ripple-carry CNF $B_n$, with $2n+1$ variables and $5n+2$ source clauses, satisfies

$$
W_{R_{\mathrm{mix341}}}(B_n)=2n+1.
$$

Its initial carry is $c_1=1$, its overflow is pinned $c_{n+1}=0$, and each stage uses clauses

$$
(x_i\vee\neg c_i),\quad(\neg x_i\vee c_i),\quad
(\neg c_{i+1}\vee x_i),\quad(\neg c_{i+1}\vee c_i),\quad
(\neg x_i\vee\neg c_i\vee c_{i+1}).
$$

Resolve the first and fifth on $x_i$ to derive $(\neg c_i\vee c_{i+1})$, then propagate $c_i$ to $c_{i+1}$ by Resolution; repeat and contradict the terminal negative unit. This uses $2n+1$ genuine paid RES nodes. The prior report independently proved $2n+2$ indispensable source clauses, giving the global minimum for **all** rules in this exact mixed calculus. Source and a pivot-only proof have $O(n\log(n+2))$ encoded bits. No novelty or priority is claimed for that prior construction.

## New quantified no-backtranslation theorem

**PROVED/EXACT (known theorem plus prior project proof):** For every nonnegative polynomial $p$, there exists $n_p$ such that for every $n\ge n_p$ and every Ext-PC-with-extension-and-square-root refutation $\rho$ of the **original algebraic** $P_n$,

$$
|\rho|_{\mathrm{bits}}>
p\bigl(|P_n|_{\mathrm{bits}}+
|\operatorname{enc}(B_n)|_{\mathrm{bits}}+
|\pi_n|_{\mathrm{bits}}+1\bigr),
$$

where $\pi_n$ is the existing authenticated $O(n\log n)$-bit Resolution refutation of $B_n$.

**Proof.** The argument of $p$ is $O(n^2)$, so its value is $n^{O_p(1)}$. Alekseev's lower bound is $2^{cn}$ for all sufficiently large $n$, exceeding any polynomial. This rules out a uniform, nonuniform, or even computationally unbounded transformation producing a polynomial-bit refutation of $P_n$ from those short Boolean proofs: the required small target proof simply does not exist.

**Important direction:** The known polynomial simulation of Extended Frege by the algebraic extension calculus applies to the arithmetization of the *given CNF clauses*. It may yield a short algebraic proof of $\operatorname{Arith}(B_n)$ from the short ER proof of $B_n$, **not** a short proof of the different algebraic input $P_n$. A purported polynomial-output backtranslation from $\operatorname{Arith}(B_n)$ to $P_n$ is therefore the precise missing and disproved step. Equisatisfiability does not supply a proof-cost isomorphism. This is a mathematical prohibition on one transfer, **not** a general CNF-SAT lower bound.

## Exact falsifiers and controls

F1: BVP's exponential rational-algebraic bit lower bound transfers unchanged to the fixed mixed calculus on natural carry-CNF. **FALSIFIED**, by the already proved global minimum $2n+1$.

F2: A polynomial-bit backwards proof translation might still exist without any algorithmic uniformity requirement. **FALSIFIED**, by the all-polynomials theorem above.

F3: An upper bound $T_A(M)\le M^{K+o(1)}$ can be multiplied as a per-query **lower** bound $\Omega(M^K)$. **FALSIFIED** as an inference. The actual Grok 2026-11-03 12:17 UTC note makes that error; peers LSPV-2 and LSPV-4 independently flagged it. This does not refute FLMV.

F4: Algebraic immunity one characterizes affine Boolean functions. **FALSIFIED**: $f(x_1,x_2)=x_1x_2$ is nonlinear, while $(1+x_1)f=0$ modulo $x_i^2=x_i$. The claim appears in the actual Claude 2026-09-30 0266 review; it cannot justify a Gaussian shortcut.

**COMPUTATIONAL:** This run independently reconstructed the existing source and Resolution proof at $n=1,2,3,4,8,16,32,64$. All $5n+2$ source clauses and $2n+1$ strict-pivot steps checked, with $2n+2$ deletion witnesses, paired SAT controls obtained by negating the initial or terminal unit, malformed-clause and corrupt-pivot rejection. The independent no-import JS runner completed **1,264 checks**; even/odd K4 parity controls have 8/0 models. These finite checks neither establish Alekseev's asymptotic theorem nor new proof minima. The program generates a reproducible signed source and proof, and the raw records give exact $n$-wise costs. Proof discovery, bit evidence, checking and machine time/space are distinct from logical-node cost.

## Grok and Claude file audit

The actual repository folders were located through repository code search: root GROKPROOF/, research/agents/grok/, and research/agents/claude/. Read GROKPROOF/2026-11-03_1217_PROGRESS.md (blob acf9fbee) and GROKPROOF/2026-11-03_1518_PROGRESS.md (blob 234fc189): the universal all-input fully charged ARC contraction remains OPEN, and the 12:17 query-cost lemma reverses a bound. Neither proves B3. Read research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex (blob b7150bb9), research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727), research/agents/claude/onetape/README.md (blob 6255025f), and research/agents/claude/2026-09-30_CLAUDE-0266_review.tex (blob 694c1c81). TPORT's barrier is confined to its alternation-trading rule set, ONETAPE's time-space bound assumes sequential input access, and the 0266 algebraic-immunity assertion has the explicit counterexample above. These reviews do not close the proof transfer.

Reviewed the complete current Nov 2 12:04 shared directive, issue #3 through Nov 3 08:48 PST, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md; LSPV-1 365, LSPV-2 HAKEN-ER2-NONPROJECTION364 and MIXED-RES-TRANSFER365, LSPV-3 BVP354 and BOUNDED-INTERFACE367, LSPV-4 GROK-QUERY-EXPONENT364 and LSPV-5 REFEREE316. BVP bitblasting is explicitly duplicated from LSPV-3 354; Haken-to-ER2 no-projection is explicitly duplicated from LSPV-2 364. Primary source queries included Alekseev 2026 Ext-PC BVP, Haken 1985 PHP, Pich-Santhanam 2026 EF witnessing and Cook-Reckhow. A search of github.com/openai for Resolution proof, SAT certificate and Extended Resolution predominantly returned unrelated geometry or subexponential SAT code; no checker was adopted.

## Cost and remaining transfer

Logical minimum: $2n+1$ distinct RES nodes on $B_n$; encoded proof size $O(n\log n)$ bits; actual algorithm/output/checker/source/index/head work is separately charged. All-phase peak space, cache and ancestor storage have not been converted to a native-machine FLMV lower bound, with the corrected envelope $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$ and $\rho$ accounting for every phase.

B1, B2, B3, the superpolynomial worst-case $\overline W_{R_{\mathrm{mix341}}}$ bound, and P versus NP remain **OPEN**. The new theorem excludes one incorrect backwards transfer from a strong published algebraic lower bound. The weakest sufficient next obligation remains **B3 for the same preselected R**, derived from bare SAT in P without presupposing polynomial refutations or a chosen algorithm's formal correctness certificate. Independently test known hard families against every fixed mixed rule, rather than generating new formulas.

## References

[1] Y. Alekseev, *A Lower Bound for Polynomial Calculus with Extension Rule*, Theory of Computing 22 (2026), Article 4, Theorem 1.1, DOI 10.4086/toc.2026.v022a004.

[2] j15marti/pnp, research/agents/lspv-3/2026-11-02_2224_LSPV-3_BVP_BITBLAST_COLLAPSE354.tex, verified global exact $2n+1$ cost.

[3] S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, Journal of Symbolic Logic 44 (1979), 36-50.

[4] A. Haken, *The Intractability of Resolution*, Theoretical Computer Science 39 (1985), 297-308.

[5] J. Pich and R. Santhanam, *Towards P≠NP from Extended Frege Lower Bounds*, JACM 73(2) (2026).
