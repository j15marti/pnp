# LSPV-1/479 | Logarithmic-degree Res(PC) benchmark for the exact split-Tseitin 3-CNF

**November 7, 2026 PST | Route B lead | KNOWN THEOREM application / PROVED-RESTRICTED parameter calculation; COMPUTATIONAL finite controls; P versus NP OPEN.**

**Affected proposed proof tracker node:** [P2-B20], built from [P2-B17], [P2-B18], [P2-B19]. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. [P1-01], [P1-03], [P1-04] remain OPEN. Do not revise historical R_mix341 grammar or unit weights.

## IDEA: precise claim and four falsifiers

**Initial hypothesis:** Pang's *quantitative*, published 2026 preprint degree-size relation can be applied to the SAME established strict proper split-3CNF cubic-expander odd-Tseitin family used in /476-/478 with a growing polynomial-equation degree cap $r=\Theta(\log h)$, not just constant $r$ stated in /477.

Predeclared falsifiers: (F1) the underlying PC degree lower bound belongs to the wrong prime characteristic; (F2) the exact split adds variables/width or changes polynomial axioms so degree transport is unavailable; (F3) the factor $(D/(16n))^{(p-1)r}$ destroys every superpolynomial conclusion at $r=\Theta(\log h)$; (F4) the cited theorem fails for unrestricted DAG-like Res(PC_r), demands a fixed constant $r$, or secretly licenses extensions / native R_mix341 rules.

**ITERATION:** Primary arXiv HTML Theorem 1.1 explicitly bounds *arbitrary DAG-like* syntactic Res(PC_r) and states its hypotheses $D\ge\max\{32(p-1)^2r,8w\}$. Since $D=\Omega(h)$ and $n=11h/2$, (F3) does NOT occur for a sufficiently small constant in front of $\log h$. The revised claim below makes the permissible logarithmic coefficient and the exact weakness of the conclusion explicit. This is an application/quantification of known results, not a novel lower-bound technique.

## Fully scoped mathematical statement

Fix an **odd prime** $p$ and $0<\epsilon<1$. Let $(G_h)$ be a published-type connected cubic constant-edge-expander family with even vertex counts $h$, and choose any odd total charge vector. The original parity-3 CNF $T_h$ has exactly $3h/2$ edge variables and $4h$ signed proper ternary clauses, four forbidding the wrong local parity at each vertex. Its XOR sum is inconsistent, so each $T_h$ is certified UNSAT. Appropriate graph sequences give exponential *ordinary Resolution* size by Urquhart (1987), whereas Buss--Grigoriev--Impagliazzo--Pitassi (2001) gives **ordinary polynomial-calculus degree** $D_{\mathbb F_p}(T_h)\ge c_0h$ for some $c_0=c_0(p,G)>0$ over incompatible odd characteristic. Neither statement is a general SAT-algorithm lower bound.

Apply the exact /476-/477 strict clause split to each original clause
$$
C_i=\ell_{i1}\lor\ell_{i2}\lor\ell_{i3}
$$
as
$$
P_i=\ell_{i1}\lor\ell_{i2}\lor a_i,\qquad Q_i=\ell_{i1}\lor\ell_{i3}\lor\neg a_i.
$$
Write $F_h=S(T_h)$. This has **$n_h=11h/2$ variables, $8h$ proper width-3 clauses and indexed source length $N_h=\Theta(h\log(h+2))$ bits**. /477 [P2-B18] established the exact unrestricted ordinary-PC degree inequality $D_p(T_h)\le D_p(F_h)\le\max\{D_p(T_h),4\}$ with no missing Boolean axiom; therefore $D_p(F_h)\ge c_0h$.

The alternative polarity-normalized $S^+(T_h)$ of /478 [P2-B19] has the SAME variable count/width and also inherits the degree lower bound. It additionally has a polynomial-sparse-PC-certificate projection, but **this property is NOT imported to the old $S(T_h)$**.

Choose any constant $c$ with $0<c<\min(c_0,1)$, and define
$$
\kappa_0=\frac{1-\epsilon}{(p-1)\ln(176/c)},\qquad
r_h=\lfloor\kappa_0\ln h\rfloor.
$$
For sufficiently large $h$ we have $r_h\ge1$. Let $S_h$ be the **minimum node count across ALL permitted shared DAGs** in the DISTINCT syntactic proof system $\operatorname{Res}(\mathrm{PC}_{r_h}/\mathbb F_p)$, with Pang's exact axioms and rules, not historical R_mix341. Its lines are disjunctions of polynomial equations of degree at most $r_h$, with syntactic weakening/contraction, legal linear combination and bounded-degree polynomial multiplication. Original-source clauses and Boolean axioms are authenticated. No free extension-variable, GF(2), semantic equivalence or general branching/discharge rule is inserted.

**Theorem 479.1 (restricted quantitative application, independently derived from cited results):** For all sufficiently large allowed $h$,
$$
\boxed{
S_h\ge\exp\left(\frac{c}{64p^2\kappa_0}\frac{h^{\epsilon}}{\ln h}\right).
}
$$
In particular, for $\epsilon=1/2$ and sufficiently small fixed coefficient $\kappa_0>0$, degree $r_h=\Theta(\log h)$ still forces
$$
S_h\ge\exp\left(\Omega\left(\frac{\sqrt h}{\log h}\right)\right).
$$
This is **superpolynomial but subexponential** as expressed by the obtained bound, and does not assert a sharp minimum or actual machine runtime.

**Proof.** Choose $D=\lfloor ch\rfloor-1$, so ordinary PC cannot derive $1$ in degree $D$, while $D\ge ch/2$ for sufficiently large $h$. As $r_h=O(\log h)$ and width is 3, for sufficiently large $h$,
$$
D\ge\max\{32(p-1)^2r_h,24\}.
$$
By Pang 2026 Theorem 1.1 (preprint, correctness condition explicitly retained), every unrestricted DAG-like $S_h$-node Res(PC_r) refutation satisfies
$$
\ln S_h\ge\frac{D}{32p^2r_h}\left(\frac{D}{16n_h}\right)^{(p-1)r_h}.
$$
Because $n_h=11h/2$,
$$
\frac{D}{16n_h}\ge\frac{c}{176},
\qquad
\left(\frac{c}{176}\right)^{(p-1)r_h}\ge h^{-(1-\epsilon)}.
$$
Thus
$$
\ln S_h\ge\frac{c}{64p^2r_h}h^\epsilon
\ge\frac{c}{64p^2\kappa_0}\frac{h^\epsilon}{\ln h}.
$$
All inequalities preserve their directions; no assumption on proof-tree structure, optimal derivation discovery, or independently optimized branches is made. **QED conditional on correctly scoped primary published lower bounds and the 2026 preprint theorem.**

**One fixed uniform alternative grammar:** Put $\kappa_1=\kappa_0/2$ and declare, for every input with $n$ original variables, $r(n)=\max\{1,\lfloor\kappa_1\ln(n+1)\rfloor\}$. This is a fixed *size-uniform syntactic Res(PC) rule scheme*, determined before the input. For $n=n_h=11h/2$, $\ln(n+1)\le2\ln h$ eventually, so $r(n_h)\le\kappa_0\ln h$ and the same bound applies for large $h$. This is **not** a historical R_mix341 rule set and the logarithmic degree allowance must not be silently added to that fixed calculus.

## Hard-family / known-shortcut / remaining-transfer ledger

| Source | Model, size and known theorem | Permitted shortcut / remaining transfer |
|---|---|---|
| Original odd cubic-expander $T_h$ | $4h$ strict 3-clauses, $3h/2$ vars, indexed $\Theta(h\log h)$; UNSAT by GF(2) charge sum; unrestricted shared-DAG ordinary Resolution $2^{\Omega(h)}$ for suitable expanding graphs (Urquhart/B-S-W); odd-$p$ ordinary PC degree $\Omega(h)$ (B-G-I-P) | GF(2) Gaussian elimination is easy. No all-algorithm hardness. |
| Exact standard split $S(T_h)$ | $8h$ clauses, $11h/2$ vars; Resolution lower bound transported by [P2-B17], all-field PC degree by [P2-B18], present log-degree Res(PC_r) lower bound by Pang | Source reconstruction by $4h$ RES, $3h$ AND3, $(h-1)$ GF(2) gives $8h-1$ **declared-semantic** mixed steps if RES output is admissible as an AND3 input; [P2-L5-412] proves surviving /341 grammar does not determine that accepted-byte edge. |
| Positive-alias $S^+(T_h)$ | Same source sizes and degree; [P2-B19] also p-simulates sparse-PC proof bits with positive monomial aliases | Auxiliary polarity differs from exact standard split. No direct sparse-PC size claim on the former follows from its latter certificate compiler. |
| The fixed $R_{\mathrm{mix341}}$ | Original /341 five declared rules, all unit-paid, every valid shared-DAG derivation | Historical AND3 parent-view byte grammar [P2-D1], all-mixed simulation [P2-C3], superpolynomial mixed lower bound [P2-B1], noncircular B3 [P2-B2] ALL OPEN. |

Haken PHP ordinary Resolution and Cook Extended Resolution remain mandatory *stronger-or-different-system controls*; the current quantitative theorem does not translate them into historical R_mix341. The source-support and shared-DAG accounting controls [P2-D2]/[P2-D3] remain unchanged. The result does not transfer to characteristic two, where parity is an algebraic shortcut. Perfect offline proof choice is allowed throughout each minimum; an implemented search must separately charge all search and verification phases.

## Independent validation and resources

The **exact published V8 script** `experiments/arc/lspv1_479_pang_logdegree_audit.cjs` (blob `2bc87953a883d34ec3cd896b0ad7eaaf3b907ef9`) was executed before publication and read back byte-identically. Its 2,383 assertions passed: 78 eligible sample parameter settings, 66 skipped boundary settings, and exhaustive K4 positive-alias section checks (1,024 odd and 1,024 even) with original odd/even source model counts 0/8. Sample $c=0.05$ and $0.2$ are **illustrative** numbers, never identified with the unknown true published expander-PC constant. Large $h$ in this script checks ONLY floating-point mathematical inequalities, **not** materialized SAT instances or asymptotic hardness.

An independently authored stdlib Python program `lspv1_479_quantitative_independent.py` uses 80-digit Decimal arithmetic and completely separate K4 signed clause generation. Its actual local execution gave 78 eligible settings, 312 quantitative checks and 2,048 K4 section checks PASS, 66 precondition-skips, original odd/even model counts 0/8; measured host seconds and RSS appear in local raw JSON. Full local Python bytes are in the reproducibility archive, not yet a pushed GitHub executable; do not describe the Python as published code.

Resource categories: Ideal $S_h$ counts distinct paid proof DAG nodes; explicit proof bits may be much larger and verifier time follows the concrete Res(PC_r) encoding. The two finite scripts separately incur source generation, parsing/loading, signed truth-table evaluation, logarithms/Decimal high-precision arithmetic, cache/array storage, assertions and output. The experimental wall/RSS values are host measurements, **not native FLMV machine counts**. No actual machine-level proof construction, failed solver search, native R_mix341 checker execution, native tape high-water bound, universal SAT decision algorithm, or actual $h\to\infty$ experiment is claimed.

## SEARCH provenance, duplication, governing files, audit limits

Read both COMPLETE `proof1.txt` and `proof2.txt` at current main (initial blobs `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, `2b9d4e1f5dc083a9bd254af6c260d47d53ac9ace`), issue #3 and latest comments, historical 2026-11-02 five-role handoff, AGENTS.md (`19656af1`), CODEX.md (`754999f5`), project skill (`b8df83a7`), original /341 (`c87acd11`), LSPV-1/476-/478, LSPV-3/475 and LSPV-5/412 current referee/ledger, actual Grok `GROKPROOF/2026-11-07_1119_PROGRESS.md` (`d87fcb3a`) and actual Claude `research/agents/claude/world-ledger/README.md` (`de75a371`). Found earlier fixed-$r$ Pang application in [P2-B18]: extended its **quantitative parameter range** only, not the underlying theorem or a new lower-bound technique. Reused the established 3-CNF source rather than inventing an instance.

Required external repository files reviewed and unchanged relative to the pinned prior review: `konard/p-vs-np/scripts/proof_status.json` (`93b77ed3`), `konard/p-vs-np/proofs/complexity/README.md` (`7ee9a11e`); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` (`18d693ea`), `blkph0x/p-vs-np-proof-research/REVIEW_ADDENDUM.md` (`6a7cc2f8`); `meelgroup/frat-xor/format.md` (`986a21aa`). FRAT-XOR is a DIFFERENT accepted theory proof grammar. Google-branded search was not independently used; web and GitHub queries were used. The authoritative historical checker and repo-scoped preflight were not executed; root `main.tex` returns SHA `68188a24badda635a5983fda1c381cdb694fd497` but zero content, so it must not be edited or claimed reconciled. No third-party manuscript/role region was overwritten.

## Status and next obligation

**PROVED/RESTRICTED APPLICATION**, subject to published source theorems: a *distinct*, explicitly defined bounded-polynomial-equation proof system remains superpolynomially hard even as its allowed equation degree grows logarithmically. This is not a new unconditional general mixed-rule invariant. Historical native grammar [P2-D1], full mixed translation [P2-C3], actual superpolynomial $\overline W_{R_{\rm mix341}}$ [P2-B1], and noncircular B3 [P2-B2] remain OPEN. The immediate target is an invariant that survives native, legally sourced characteristic-two GF(2), AND3, RES, DEF, LOCAL-CONVERT and shared proofs without changing the historical rule grammar. P versus NP remains OPEN.

## References

[1] A. Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), 209–219, DOI 10.1145/7531.8928.

[2] S. R. Buss, D. Grigoriev, R. Impagliazzo, T. Pitassi, *Linear Gaps Between Degrees for the Polynomial Calculus Modulo Distinct Primes*, JCSS 62 (2001), 267–289, https://mathweb.ucsd.edu/~sbuss/ResearchWeb/lineargaps/index.html.

[3] S. Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (2026, **preprint**), Theorem 1.1, https://arxiv.org/abs/2610.00837, HTML primary text verified at arxiv.org/abs/2610.00837.

[4] E. Ben-Sasson, A. Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48 (2001), 149–169, DOI 10.1145/375827.375835.
