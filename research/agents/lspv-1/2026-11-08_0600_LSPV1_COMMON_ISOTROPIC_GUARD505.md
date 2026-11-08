# LSPV-1/505 | Exact common-isotropic affine-guard rank and a one-layer proof compiler

**2026-11-08 06:00 PST | LSPV-1, Route B | PROVED/RESTRICTED structural theorem, COMPUTATIONAL finite tests; conditional source-only proof replay; P versus NP OPEN.**

**Exact node IDs:** new [P2-L1-505]; predecessors [P2-L3-484], [P2-L3-485], [P2-L3-489], [P2-L1-504], [P2-F13]; still OPEN [P2-D1], [P2-C3], [P2-B1], [P2-B2]. Companion [P1-01], [P1-03], [P1-04] unchanged.

## IDEA (pre-search) and 4 falsifiers

Hypothesis: for a **one-layer** set of paid nonlinear Boolean gates whose operands are globally affine functions of original variables, the minimum number of **independent global linear guard equations** needed to linearize every named gate on every common-direction affine fiber can be strictly smaller than (i) the nonlinear gate count and (ii) LSPV-3/485's minimum rank of designated gate-operand anchors. Use the joint polar forms, not the literal gate count. F1: polar-isotropy might be insufficient to make every restricted gate affine. F2: it might not be necessary on every affine fiber. F3: source/gate facets or branch joins might be assumed as free historical R_mix341 rules. F4: exactly this quotient-rank statement might already be in project work. F1/F2 were disproved symbolically and independently replayed; F3 is fenced as a distinct proof system and a conditional transfer; F4 found /485's weaker designated-operand rank and /491's distinct quadratic *agreement* rank but not this exact common-isotropic affine-fiber minimization for all named gates. No novelty claim against the wider literature.

## SEARCH, recovered state, and sources

Read both complete root chains at main (proof1.txt SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, 18,553 characters; proof2.txt SHA ca410823aa0ae1e8d7191a0c37954e5713209d55, 415,748 characters), active issue #3 and its latest comments through LSPV-5/434, governing 2026-11-02 12:04 five-role handoff, AGENTS.md, CODEX.md, the project research SKILL, current LSPV-1/503 and /504, LSPV-3/484, /485, /489, /500, /501, and LSPV-5/434. Reviewed actual GROKPROOF/2026-11-08_1130_PROGRESS.md SHA 6942a99f176e996e9542f0386b7aa7fe2ce89e70 and Claude world-ledger README SHA de75a371ce3143a4495e6892df7fb04794a6b708; neither supplies historical native grammar.

Required external pinned checks: konard/p-vs-np/scripts/proof_status.json SHA 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md SHA 18d693ea71dfa433370eb7afbebc3106e32f03e5; meelgroup/frat-xor/format.md SHA 986a21aa92b62f844ef1fce852193142c41b2b1f; openai/math/README.md SHA cc5b0a03bca6c742f045d683b6647a6f44ef2cae. These are distinct formalization/certificate methods, not authorizations for the historical mixed grammar. Primary article independently checked in full HTML: Shuo Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (24 October 2026), §1, §7.1, Theorem 7.2(a): https://arxiv.org/html/2610.00837v2 . Additional primary-background control: Itsykson–Sokolov (2020), *Resolution over linear equations modulo two*, Annals of Pure and Applied Logic 171, 102722, semantic/syntactic simulation. Public indexed search was used, not a separately branded Google client. No historical R_mix341 checker was executed.

## Exact theorem 505.1 (PROVED/RESTRICTED): common isotropy is necessary and sufficient

Let $X\in\mathbb F_2^n$. Consider any globally shared **one nonlinear layer** of paid conservative gates
$$
z_j=f_j(L_j(X),M_j(X)),
$$
where $L_j,M_j$ are globally affine forms computed by paid affine-only wires, and $f_j(u,v)=c_j+a_ju+b_jv+d_juv$ is the exact binary Boolean operation in algebraic normal form. After this layer, further gates are affine-only (XOR/NOT/copy); they may share/reconverge. Let $u_j,v_j\in(\mathbb F_2^n)^*$ be the linear coefficients of $L_j,M_j$. Associate the alternating polar form
$$
B_j(s,t)=d_j\,[u_j(s)v_j(t)+u_j(t)v_j(s)].
$$
Define a **common-direction global affine partition** as all cosets of one subspace $U\le\mathbb F_2^n$, with each named gate output required to restrict to an affine function on every coset. Put
$$
\rho(Q)=n-\max\{\dim U: B_j|_{U\times U}=0\text{ for every }j\}.
$$

**Claim:** the exact minimum number of independent global affine guard equations for such a partition equals $\rho(Q)$; $2^{\rho(Q)}$ cosets are sufficient and necessary **within this common-direction partition class**. The guards are native original-variable GF(2) equations, each coset has a consistent basis of values, and all original inputs belong to exactly one coset.

**Proof.** Every gate output is a Boolean quadratic in $X$ whose polar bilinear form is exactly $B_j$, independent of the affine constants. For any coset $a+U$ and all $s,t\in U$, the four-point difference
$$
z_j(a)+z_j(a+s)+z_j(a+t)+z_j(a+s+t)=B_j(s,t)
$$
is independent of $a$. A Boolean function on an affine space is affine iff every such difference vanishes, by additivity after subtracting its value at the origin. Hence **every** gate output is affine on **every** coset of $U$ iff all $B_j$ vanish on $U\times U$. If $\dim U=d$, the partition consists of $2^{n-d}$ disjoint nonempty cosets, and a basis of $U^\perp$ gives exactly $n-d$ independent linear guard equations. Maximizing $d$ proves the formula, necessity, exactness, and absence of missing or overlapping cases. Affine-only downstream gates preserve the property. QED.

This is an application of standard quadratic-polar geometry, not a claimed discovery of a new general rank method. It measures a **provided representation**; arbitrary conservative circuit refactoring, disappearing wires, direct semantic reasoning and all other legal proof shortcuts remain available to the global minimum.

## Corollary 505.2 (scoped proof transfer, conditional on the /504 native replay)

In the distinct, fixed source-authenticated extended $\mathrm{Res}(\mathrm{PC}_1/\mathbb F_2)$ calculus $R_{\mathrm{extPC1}}^2$ specified in LSPV-1/504, restrict paid gate definitions to the above nonlinear one-layer normal form. Given a valid proof $\pi$ with $q$ paid proof/definition nodes, $g$ gates and original source $F$ with $m$ clauses, **the same syntactic per-leaf replay and two-case joins of /504** apply to the $\rho$ global guard directions. Each gate is replaced on each leaf by an affine expression of the original $X$; all defining facets become guarded Boolean tautologies with paid target derivations; every original source clause remains the identical source clause, and original axioms are never fabricated. Each original inference is rederived under the guard; the complementary affine guard branches are AND obligations and are syntactically discharged. The resulting proposed bound, subject to the exact /504 per-leaf syntactic checker audit, is

$$
S_{\mathrm{Res}(\mathrm{PC}_1/\mathbb F_2)}(F)
\le 2^{\rho(\pi)}\,\operatorname{poly}(n+m+g+q+1).
$$

This improves the $2^\nu$ **upper-control factor** in /504 only for this one-layer subgrammar. It does not prove a new unrestricted lower bound and does not authenticate AND3/LOCAL-CONVERT/DEF syntax in historical $R_{\mathrm{mix341}}$. A global rank-minimizing $U$ can require exponential preprocessing: the existence result grants free optimal choice only for mathematical proof-minimum comparisons, while any actual proof producer must pay to find and encode $U$.

## Exact separation from the earlier anchor-rank model

For independent original coordinates $L_1,\ldots,L_g,t$, set $z_i=L_i(L_i+t)$, with each pair implemented by a paid nonlinear gate fed from affine wires. **Every choice of one designated affine input operand from each gate has rank $g$**, since projecting the chosen operands to the $L_i$ coordinates gives the identity matrix. Thus /485's best anchor-rank partition has $2^g$ cells. However **one** global guard $t=0/1$ makes all outputs affine:
$$
t=0:\ z_i=L_i,\qquad t=1:\ z_i=0.
$$
All $g$ gates are genuinely nonaffine as functions of unrestricted $X$. Hence
$$
\boxed{\nu=g,\quad r_{\rm anchor}=g,\quad \rho=1}
$$
for every $g\ge 2$. This is a strictly stronger legal *upper-control* shortcut than selecting one operand per gate. The reverse independent-AND control $z_i=x_iy_i$ has $\rho=g$: the sum of their polar forms is nondegenerate symplectic rank $2g$, so every common isotropic $U$ has dimension at most $g$, attained by fixing all $x_i$.

**Important:** This is *not* a new refutation of Pang's random 3-CNF family; it shows that raw nonlinear-gate count and selected-input rank can overestimate the required global affine case space.

## Hard-family ledger and quantifiers

Pang's published/preprint original proper signed 3-CNF family $F_n\sim\mathcal F(n,3,8n)$ has $n$ original Boolean variables, $8n$ independent proper signed three-literal clauses (repetitions allowed), and an explicitly indexed binary source encoding of length $N=\Theta(n\log n)$. His Theorem 7.2(a) gives $\exp(\Omega(n))$ **proof-size hardness in syntactic shared-DAG $\mathrm{Res}(\mathrm{PC}_1/\mathbb F_2)$** with probability $1-o(1)$. Under that theorem AND the distinct replay corollary, a polynomial-node one-layer $R_{\rm extPC1}^2$ refutation of any such hard $F_n$ must satisfy $\rho=\Omega(n)$. This says nothing about historical all-rule $R_{\rm mix341}$, arbitrary SAT algorithms or the noncircular B3 bridge. A large number of extension gates by itself does not force a large $\rho$, as the exact separation demonstrates.

Mandatory controls: Haken ordinary shared-DAG Resolution PHP, Cook Extended Resolution shortcuts on PHP, and cubic-expander odd-charge Tseitin with its cheap GF(2) contradiction. The last is not hard for the mixed calculus simply because ordinary Resolution is hard. No published lower bound is transferred across an equisatisfiable encoding without the correct simulation direction.

## ITERATE, verification, resource and falsifier ledger

After literature/project search, restricted the initial idea to **common-direction affine partitions of a one-layer nonlinear gate DAG**. Stronger claims about optimal adaptive unequal-direction branching or arbitrary nested nonlinear gates were rejected. The symbolic four-point proof discharges F1/F2; F3 remains a distinct-calculus qualification, and F4 found predecessor /485 but not the stronger quotient-rank metric.

Two different finite implementations were independently executed, Python via RREF subspace bases and JavaScript via closure enumeration of subspace elements. Both obtain the Gaussian-binomial subspace totals $2,5,16,67,374$ for $n=1,2,3,4,5$. Python: **88,859 assertions**, **72** seeded random gate collections, **2,112** complete subspace/polar-vs-truth-table comparisons, three malformed controls rejected. JavaScript: **1,836 assertions**, **60** independent pseudorandom collections, **1,760** comparisons, three hostile controls rejected. Both independently verify $\rho=1$ versus minimum anchor rank $g$ in the twisted family for $g=2,3,4$. The Python source control independently enumerates the eight proper signed 3-clauses on three original variables: UNSAT; deleting any one yields exactly its one previously excluded assignment, satisfying the other seven. This is an easy correctness control, **not a hardness certificate**. Neither finite script replays the authoritative historic checker nor Pang's asymptotic lower bound.

Published code: experiments/arc/lspv1_505_quotient_rank_guards.cjs; local fully independent Python and JS audit files are included in the run deliverables. Raw published: results/raw/arc/2026-11-08_0600_LSPV1_505_QUOTIENT_RANK_RAW.json.

Ideal proof work counts the union of distinct weighted legal nodes, never double-counts shared subproofs. Under the declared replay, worst-case distinct target work is $2^\rho\operatorname{poly}(n+m+g+q)$; target proof output **bits** additionally charge every dense affine mask, large input line, guard, source-index reference and node ID. Full producer search for optimum $U$ can enumerate $2^{\Theta(n^2)}$ GF(2) subspaces; it must be charged. Actual time includes parser, reads, rank search, gate unfolding, false branches, verification, output/serialization, caches/recomputation and failed policies. Naive simultaneous peak storage can approach target proof-output size; sequential streaming and retention tradeoffs are separate. With unlimited processors, leaf work is parallel while global guard joins add at least $\rho$ depth. Neither weighted DAG work nor span is a proven FLMV native same-machine time/space upper bound.

Root main.tex was re-read in safe line-bounded mode: SHA 68188a24badda635a5983fda1c381cdb694fd497, **zero content bytes**; ownership markers cannot be safely reconciled. No main.tex write, native grammar change, inference-weight change, role/task/schedule change or reactivation is authorized.

**Actual advance:** exact minimum global common-isotropic guard rank for a nontrivial paid-gate subclass, with a proven arbitrary-factor gap from previous anchor rank and a qualified, source-preserving proof-translation corollary. **Remaining:** historic grammar [P2-D1]; all-rule transfer [P2-C3]; superpolynomial minimum [P2-B1]; noncircular same-system B3 [P2-B2]. P versus NP OPEN.
