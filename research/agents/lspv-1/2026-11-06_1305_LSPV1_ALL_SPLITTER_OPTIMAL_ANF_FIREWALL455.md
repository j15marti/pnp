# LSPV-1/455: exact degree and ANF size of all proper-3CNF splitter sections

**2026-11-06 13:05 PST, Route B; PROVED/RESTRICTED, specialist review pending.** Finite tests COMPUTATIONAL. Historical native R_mix341 grammar, mixed lower bound, B1/B2/B3, and P versus NP OPEN. Roles, schedules, rules, weights unchanged.

## Hypothesis / falsifiers / prior-art audit

Extend LSPV-1/454's first-splitter affine obstruction to *every* private splitter of a standard long-clause 3CNF reduction. Four falsifiers: a smaller middle degree, failure of simultaneous optimal sections, smaller mixed ANF support, and illicit promotion to general mixed proof hardness. First three excluded by proof; fourth rejected by an O(k)-gate upper control.

Reviewed Nov 2 five-role handoff (blob c3889a3e514ddbd747150dcb68607013a3b2d154), issue #3, AGENTS.md, CODEX.md, pnp-research skill, LSPV-1/453-454, GROKPROOF/2026-11-06_0515_PROGRESS.md, Claude TPORT-0002, LSPV-5 REFEREE315, and LSPV-3/457's issue comment. Grok/Claude actual files were read. A guessed LSPV-3/457 file path returned 404. Current root main.tex partial fetch returned empty content (blob 8a440b7d81dbfe300470c7c097c7165802b1067a); no root edit. Searches for exact all-splitter degree/ANF result found no indexed match, but novelty is NOT claimed. Primary Braun and Pang papers reviewed. Required repositories: konard/p-vs-np README blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95, scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f. These are not proofs into the historical calculus.

## Exact theorem (clause-local, not an all-rule refutation lower bound)

Let $k\ge4$, with distinct *literal-truth* coordinates $a_1,\ldots,a_k$. The standard proper width-three chain for $C_k=\bigvee_{i=1}^ka_i$ is

$$
T_k=(a_1\vee a_2\vee y_1)\wedge
\bigwedge_{j=2}^{k-3}(\neg y_{j-1}\vee a_{j+1}\vee y_j)
\wedge(\neg y_{k-3}\vee a_{k-1}\vee a_k).
$$

It has $k-2$ clauses and $k-3$ private variables. A complete *local Skolem section* $f=(f_1,\ldots,f_{k-3})$ must satisfy $T_k(a,f(a))$ for **every** $a\ne0^k$, with each $f_j$ a Boolean function of all original literal coordinates. For position $j$, set $p=j+1$, $s=k-p$, $P=(a_1,\ldots,a_p)$, $S=(a_{p+1},\ldots,a_k)$.

**Theorem 455.1 (exact and tight).** For every complete section,

$$
\deg_{\mathrm{ANF}}f_j\ge\min(p,s),\qquad
\operatorname{ANFterms}(f_j)\ge\min(2^p,2^s-1).
$$

A *single* section simultaneously attains both bounds for all $j$:

$$
f_j(P,S)=
\begin{cases}
\prod_{i=1}^{p}(1+a_i),&p<s,\\
1+\prod_{i=p+1}^{k}(1+a_i),&p\ge s.
\end{cases}
$$

Therefore the minimum possible maximum ANF degree over the entire private splitter chain is $\lfloor k/2\rfloor$.

**Proof.** When $P=0,S\ne0$, the first and intervening clauses force $y_j=1$. When $P\ne0,S=0$, putting $y_j=1$ propagates to the last splitter and falsifies the last clause, so $y_j=0$. When both blocks are nonzero either $y_j$ value has some extension. Let $c=f_j(0,0)$. If $c=1$, the restricted ANF $f_j(P,0)$ is the zero-point indicator $\prod_{i\le p}(1+a_i)$, with degree $p$ and $2^p$ monomials. If $c=0$, $f_j(0,S)$ is OR$(S)=1+\prod_{i>p}(1+a_i)$, with degree $s$ and $2^s-1$ monomials. A restriction setting variables to zero cannot increase ANF degree or monomial count. This proves the bounds, regardless of arbitrary cross-block monomials. The exhibited section chooses prefix-zero indicators until the midpoint and suffix-OR indicators afterwards. All clauses on each side hold; at the single transition, a violation would force $a=0$, excluded by $C_k(a)=1$. Both bounds are simultaneously attained. QED.

All *coordinate*-admissible polynomials additionally have an exact description: either baseline above, plus a multilinear polynomial every monomial of which meets both $P$ and $S$. Arbitrary per-coordinate choices need not be globally consistent; the given switching section is consistent.

## Existing certified-hard family and transfer qualification

Braun's original bit-PHP has $n=2^\ell$ holes, $n+1$ pigeons, $A=n\binom{n+1}{2}$ width-$2\ell$ clauses. The private-chain conversion gives $A(2\ell-2)$ proper 3CNF clauses, $(n+1)\ell+A(2\ell-3)$ original-and-private variables, and at most $O(A\ell\log(A\ell+2))$ source bits with consecutive IDs. The center splitter ($j=\ell-1$) of **each original wide clause** requires ANF degree at least $\ell$ and at least $2^\ell-1=n-1$ monomials in any *clause-local* section. Braun's published exponential bound is for unrestricted shared-DAG Res($\oplus$) on original bit-PHP, with **no arbitrary definitional extension axioms**. Neither equisatisfiability nor this polynomial-section lower bound preserves it into historical R_mix341. A linear-size signed Boolean-gate circuit computes the displayed full section, so general circuit-definitional shortcuts must remain available as candidate upper bounds and legally simulated/charged if used.

Pang's Res(PC_r/F_p) theorem concerns a specified bounded polynomial degree $r$, not arbitrary paid extensions. Cook ER PHP proofs are a mandatory known shortcut. The minimum Skolem-output fan-in-two Boolean circuit depth is at least $\lceil\log_2\ell\rceil$ for the middle output, by degree doubling, but this is NOT computational or all-rule proof-work hardness.

## Verification, resource and next obligations

Python exact GF(2) rank: widths 4..14, 66 splitter coordinates, 293 degree-threshold tests, 81,650 processed rows; 32,741 full satisfying original assignments passed with simultaneous sections, 21 corrupt forced-bit controls rejected. Odd/even K4 Tseitin original proper 3CNFs: 0/8 models, 16/16 single-clause-deletion SAT controls, five malformed DIMACS rejected. Independent Node checker: widths through 13, 55 coordinates, 35,346 checks, 55 hostile forced-coordinate controls rejected. Finite runtime Python ~3.72 s; tracemalloc Python-managed peak 769,635 bytes (not RSS). Distinguish this exhaustive *search/checking* resource ledger from the ideal polynomial representation degree and from logical proof weight.

**Next:** authenticate exactly historical LOCAL-CONVERT/AND3/GF(2) paid-definition interface, then test full polynomial proof-level simulation of Braun's *proper-3CNF encoding* against all legal mixed DAG shortcuts. Separately OPEN: superpolynomial worst-case mixed minimum and noncircular $\mathrm{SAT}\in P\Rightarrow\overline W_{R_{\mathrm{mix341}}}\in N^{O(1)}$. No arbitrary-machine lower bound. P vs NP OPEN.

## Primary sources

Braun, 2026, https://arxiv.org/abs/2609.23015, Section 1/Theorem 1.1 (arXiv HTML consulted); Pang, 2026, https://arxiv.org/abs/2610.00837, Section 1; Cook, 1976, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*. Historical LSPV-1/454 already proves the first-splitter $\deg\ge2$ case.
