# TMR-3/010: exponential-moment aggregation removes the cut-count penalty

**Date:** November 13, 2026, 21:20 PST (America/Los_Angeles).  
**Repository and role:** j15marti/pnp main, TMR-3 Time-Space Tradeoffs.  
**Status:** The new tail inequality is PROVED/EXACT as a combinatorial lemma. Its specialized one-head 3-SAT crossing consequence is **CONDITIONAL/RESTRICTED** on the still-CANDIDATE physical crossing-code/splice premises of TMR-3/008. Numerical audits are **COMPUTATIONAL**. General 3-SAT all-exponent lower bound and P versus NP remain **OPEN**.

## 1. Precisely scoped new mathematical advance

The preceding TMR-3/009 applied a union bound to K source cuts, giving error at most $K2^{-q/2}$ for the desired same-realization product. This requires large batches to make the estimate useful. **We can remove the entire factor K, while retaining exactly the same product threshold**, using an exponential moment followed by Jensen/AM-GM and Markov instead of demanding that every cut is simultaneously long.

**Lemma TMR3-EM10 (prefix-free aggregate tail).** Let $X$ be uniform on a set of size $2^q$. For each $1\le c\le K$, suppose $z_c(X)$ is the length of a binary prefix-free code whose codewords are distinct as X varies, with arbitrary dependence between codebooks, non-identical lengths, and arbitrary correlation of the K lengths under the common X. Then for any $0<\delta<1$,

$$
\Pr_X\left[
\sum_{c=1}^{K} z_c(X)
<
K\bigl(q-\log_2(1/\delta)\bigr)
\right]\le\delta.
\tag{EM10}
$$

The statement also holds if each codebook depends on additional random variables W, provided conditional on every W relevant to that codebook, X supplies q independent uniform symbols and the codewords remain distinct and prefix-free. Different cuts may condition on *different* coordinates of a larger common random vector, as long as this conditional property holds for each cut.

**Proof.** Kraft gives $\sum_{x}2^{-z_c(x)}\le1$. Thus for each c,
$$
\mathbb E[2^{q-z_c(X)}]\le1.
$$
Define $Y(X)=K^{-1}\sum_c2^{q-z_c(X)}$. Then $\mathbb E Y\le1$. Convexity of $t\mapsto2^t$ implies
$$
Y(X)\ge2^{q-K^{-1}\sum_c z_c(X)}.
$$
If the event in EM10 occurs, $Y(X)>1/\delta$. Markov gives $\Pr(Y>1/\delta)\le\delta$. In the conditional variant, first take expectation conditional on the nonvarying outside coordinates for each c, then average. **No independence between source cuts is assumed**, and no maximum over different executions is summed. QED.

**Important limitation:** Prefix-freeness or an equivalent Kraft inequality is essential to this proof. Mere injectivity of a variable-length raw bit string does not guarantee $\sum2^{-\ell}\le1$.

## 2. Application to the original exact 3-CNF batched equality sources

Preserve the exact grammar and assumptions of TMR-3/008 and /009:
$$
w=\max(1,\lceil\log_2(5n)\rceil),\quad
g=12(w+1),\quad
L=13n+2+2ng,
$$
$$
n\ge m\ge16,\quad q=\lfloor m/2\rfloor,\quad
K=\lfloor n/m\rfloor(qg-1),\quad F_a=E_{n,m}(a,a).
$$

A is ONE fixed finite total all-input-correct deterministic multitape 3-SAT decider, with one adjacent-moving read-only input head, finitely many locally moving writable tapes, fixed alphabet/control, physical read charges, and unrestricted but paid writable workspace $S_A(F)$ and transitions $T_A(F)$. The original TMR-3/008 CODE and legal-SAT/UNSAT splice-injectivity premises imply that at every selected cut c, the full crossing record has a prefix-free code of length $\ell_c(a)$ with

$$
\ell_c(a)\le d_A r_c(a)(S_A(F_a)+1),
$$

where $r_c(a)$ is the *actual* crossing count. For a uniform full vector a, condition separately at each cut on all outside variables; its q completed left-bank variables are independently uniform and form an exact both-label fooling set of size $2^q$. Thus the conditional Kraft inequality applies at each c, even though each cut uses a different q-subvector.

Sum over ALL cuts on the SAME execution and use $\sum_c r_c(a)\le T_A(F_a)$:

$$
\boxed{\Pr_a\left[
T_A(F_a)(S_A(F_a)+1)
\ge \frac{K}{d_A}\bigl(q-\log_2(1/\delta)\bigr)
\right]\ge1-\delta.}
\tag{TMR3-EM10-SAT}
$$

When the right-side threshold is negative, the assertion is vacuous but valid. In particular set $\delta=2^{-q/2}$. Using the exact same algebraic estimate $Kq/(2d_A)\ge Lm/(512d_A)$ from TMR-3/009:

$$
\boxed{
\Pr_a\left[T_A(F_a)(S_A(F_a)+1)\ge\frac{Lm}{512d_A}\right]
\ge1-2^{-q/2}.}
\tag{EM10-STRONG}
$$

This retains the previous product constant while improving the previous failure probability bound from $\min(1,K2^{-q/2})$ to $2^{-q/2}$. For $m\ge16$, $q\ge8$, the probability is at least $15/16$ uniformly in n. For $m\ge4\log_2 L+2$ it is at least $1-1/L$ (the old sufficient condition was $m\ge8\log_2L+8$). With $m=\Omega(\log\log L)$ the probability can approach one at inverse-polylogarithmic error.

**This remains a same-input source-transport time-space product, not a compulsory SAT reasoning bound.** A single fixed correct machine serves all input lengths. The selected a depends on A and may vary with n,m. No separate worst-case input witnesses are combined.

## 3. Exact numerical implications and original hostile controls

For $n=256$, $L=77,058$ encoded bits:

| m | q | K | Previous error bound | New error bound |
|---:|---:|---:|---:|---:|
| 16 | 8 | 18,416 | 1 | 0.0625 |
| 32 | 16 | 18,424 | 1 | 0.00390625 |
| 64 | 32 | 18,428 | 0.28118896484375 | 0.0000152587890625 |
| 128 | 64 | 18,430 | 0.00000429106876 | 0.00000000023283064 |
| 256 | 128 | 18,431 | 0.0000000000000009991465 | 0.00000000000000000005421 |

The mathematical probability bound is not an empirical distribution of actual Turing-machine computations.

**COMPUTATIONAL execution:** Directly evaluated the exact function subsequently published as a standalone Node-compatible script using hosted V8. Seed `0x3A9C2701`; 504 distinct $(q,K,\mathrm{trial})$ cases, 5,292 complete prefix-free codebooks, 36,576 full-vector assignments, 3,024 exhaustive probability-tail checks over $\delta=2^{-1},\ldots,2^{-6}$; zero tail violations and zero exponential-moment violations. The independently constructed negative control uses an INJECTIVE but NOT prefix-free collection of raw strings of lengths $0,1,\ldots,q$ at $q=4$, circulantly rearranged over K=16 cuts. Every source has average length 2.375, so the purported $\delta=1/2$ bound $\Pr[\bar\ell<3]\le1/2$ fails with observed probability one. Its Kraft sum is 4.0625, not one. This verifies that prefix-freeness is a load-bearing hypothesis rather than an aesthetic code choice.

Source: `experiments/tmr/tmr3_aggregate_kraft010.cjs`. Raw deterministic counters: `results/raw/tmr/2026-11-13_2120_TMR3_AGGREGATE_KRAFT010_RAW.json`. These finite checks test aggregate prefix-code arithmetic and the negative control, **not** physical Turing-machine crossing states, an all-input SAT decider, or a superpolynomial result. No OS-native Node execution, full physical machine simulator, repo preflight or LaTeX compilation was performed in this connector-only run.

## 4. Dependency, historical reconciliation, model-transfer firewall

**Original artifacts read:** TMR-3/008 and /009 original mathematical reports, TMR-3/002 full crossing model, TMR-3/007 clause-reordering falsifier, TMR-2/010 two-label streaming mask countermodel, TMR-5/008 source-observation ceiling, TMR-1/011 head-origin theorem, original historical LSPV-5/167 crossing-average proof and LSPV-1/197 all-cuts distribution argument. LSPV-5/167 established a related expectation-based common-input argument on a different exact22 family. LSPV-1/197 established a union-based high-density theorem for a proof-interpreter model, not the present exponential-moment *aggregate code-length* tail. This run does not claim to invent crossing sequences or the Kraft inequality. The precise delta-tail improvement over TMR-3/009 is the new scoped item.

**Primary literature independently checked:** F. C. Hennie, `Crossing sequences and off-line Turing machine computations` (1965), [NASA original bibliographic entry](https://ntrs.nasa.gov/citations/19660035639), classical sequential crossing context, not a 3-SAT arbitrary-access theorem. Fortnow, Lipton, van Melkebeek, Viglas, `Time-space lower bounds for satisfiability`, JACM 52(6), 835-865 (2005), [ACM original](https://doi.org/10.1145/1101821.1101822), a random-access TM *small-space* exclusion for $c<\varphi$ and suitably small d, not arbitrary polynomial workspace. Borodin and Cook, `A Time-Space Tradeoff for Sorting on a General Sequential Model of Computation`, SIAM J Comput 11(2), 287-297 (1982), [publisher original](https://doi.org/10.1137/0211022), concerns sorting rather than unrestricted 3-SAT. These citations contextualize the access-model boundary; EM10 itself is proved above.

**Hostile alternate algorithms and representations:** m=1 exact clause interleaving admits $T=O(L),S=O(\log L)$ on the same unordered CNF; two independent physical input heads and charged INDEX circumvent the one-head cut separation; caching full batches obtains polynomial resource pairs; a source-copying implementation can trade O(L) work cells for O(L) input acquisition; XOR/Tseitin Gaussian elimination, 2-SAT, Horn, bounded-treewidth DP, disjoint products, compact circuits, sharing, padding, auxiliary variables and recomputation are not excluded. No algorithm is compelled to execute the prescribed source crossings on an arbitrary alternate encoding.

**Exponent firewall:** If $m=\Theta(n^\alpha)$, $0<\alpha\le1$, the product is only $\Omega_A(L^{1+\alpha}/(\log L)^\alpha)$ at the specified high probability. It excludes simultaneous polynomial exponent pairs $k+s<1+\alpha$ on these inputs; it does not exclude arbitrarily large polynomial workspace/time exponents. Using $S\le O(T)$ on this SAME machine yields $T=\Omega(\sqrt{Lm})$, weaker than mandatory $\Omega(L)$ traversal at maximal m. The unrestricted all-exponent separation remains OPEN. No ETH, SETH, cryptographic assumption, oracle or per-length algorithm minimization was invoked.

**Corpus and tracker status:** Replacement directive read first (SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4); root proof1.txt fully read (28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), proof2.txt recovered through authentic Git blob (1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c), main.tex recovered via Git blob (2,507,300 characters, SHA c0d657568af18ed0a2d17843b8ef0e6c11ac6327). AGENTS.md, CODEX.md, skill, all five role handoffs and issue #3 through TMR-1/011 reviewed. Original historical assigned identities are superseded but evidence preserved. **TRACKERS REVIEWED; NO MATERIAL CHANGE** to either root proof chain. The current `main.tex` contains balanced TMR owner regions but is left unchanged: TMR-5 owns whole-document synthesis; no increase in proof status is warranted by a conditional tail improvement. No scheduled task was modified.

**New status:** EM10 aggregate prefix-free tail is exact mathematics; EM10-SAT remains **CONDITIONAL/RESTRICTED** until another role independently proves the TMR-3/008 crossing-code all-transition splice premises. Its quantitative conclusion by itself is polynomial-strength and encoding-access restricted.

**Next single target for TMR-5 and TMR-1:** independently reconstruct the full physical crossing-configuration serializability, prove or disprove the splice injectivity for the authenticated same-length opposite-label hybrids, then evaluate the new EM10 strengthened tail. A true representation-independent processing bottleneck that survives indexed access, arbitrary polynomial workspace and compact algebra remains **OPEN**.

END_OF_REPORT::TMR3::AGGREGATE_KRAFT010::2026-11-13_2120_PST
