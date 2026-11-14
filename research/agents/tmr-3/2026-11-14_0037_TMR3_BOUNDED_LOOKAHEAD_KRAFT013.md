# TMR-3/013: bounded future dependence restores quantitative Kraft concentration

**Date:** 2026-11-14 00:37 PST (America/Los_Angeles). **Role:** NEW TMR-3, Time-Space Tradeoffs, j15marti/pnp main. **Mathematical status:** CANDIDATE pending independent TMR-5 or TMR-2 review, with a complete proof below. **Finite execution:** COMPUTATIONAL. **Unrestricted 3-SAT lower bound:** OPEN.

## 1. Precise new lemma: a quantitative middle ground between causal and fully conditioned codebooks

Prior TMR-3/010 proves a K-free lower-tail inequality for individually conditionally prefix-free crossing codes. TMR-3/012 constructs *independent disjoint* q-bit free blocks with globally correlated lengths because each codebook can depend on all future blocks. Simply claiming disjoint sources create independent crossing lengths is FALSIFIED by that construction.

**TMR3-LA13 theorem (bounded-lookahead Kraft/Hölder inequality, CANDIDATE).** Let $X_1,\ldots,X_K$ be mutually independent uniform binary strings with lengths $q_i\ge1$. Fix an integer $r\ge0$, put $d=r+1$, and let each binary codeword $c_i$ be a deterministic function ONLY of $(X_1,\ldots,X_{\min(K,i+r)})$. For every fixed choice of those arguments except $X_i$, require $x_i\mapsto c_i$ to be injective and prefix-free on all $2^{q_i}$ possible $x_i$. Write $\ell_i=|c_i|$. Then, for every $b>0$,

$$
\boxed{
\Pr\left[\sum_{i=1}^{K}\ell_i
<\sum_{i=1}^{K}q_i-b\right]\le 2^{-b/d}.
}
\tag{LA13}
$$

For equal $q_i=q$ and any $0<\delta<1$, substituting $b=K\log_2(1/\delta)$ yields

$$
\boxed{
\Pr\left[\frac1K\sum_{i=1}^K\ell_i
<q-\log_2(1/\delta)\right]
\le \delta^{K/(r+1)}.
}
\tag{LA13-equal}
$$

In particular $r=0$ gives the strong $\delta^K$ tail, while $r=K-1$ reduces to the sharp existing $\delta$ tail. The claim allows *arbitrary dependence on the entire past*, adaptive codebooks, and repeated/shared information. It does NOT assert that actual two-way SAT crossing records satisfy a bounded future horizon.

### Complete proof

Set $Y_i=2^{q_i-\ell_i}$ and $\mathcal F_j=\sigma(X_1,\ldots,X_j)$. Conditional on $\mathcal F_{i-1}$ and on all future variables used by $c_i$, the value $X_i$ remains independent uniform. The prefix-free assumption and Kraft's inequality give

$$
\mathbb E[Y_i\mid\mathcal F_{i-1},X_{i+1},\ldots,X_{\min(K,i+r)}]
=\sum_{x_i\in\{0,1\}^{q_i}}2^{-|c_i(x_i;\text{fixed outside})|}
\le1.
$$

Averaging over the unobserved future proves $\mathbb E[Y_i\mid\mathcal F_{i-1}]\le1$.

Partition indices into the $d=r+1$ residue classes modulo $d$. In each class, successive indices $i<j$ satisfy $j\ge i+d$, hence $Y_i$ is measurable with respect to $\mathcal F_{i+r}\subseteq\mathcal F_{j-1}$. Multiplication and the conditional expectation inequality, iterated from the last index backward, imply

$$
\mathbb E[P_a]\le1,\qquad
P_a=\prod_{\substack{i\in\{1,\ldots,K\}\\i\equiv a\pmod d}}Y_i
$$

for every residue class $a$; empty classes have $P_a=1$. By generalized Hölder,

$$
\mathbb E\left[\left(\prod_{i=1}^K Y_i\right)^{1/d}\right]
=\mathbb E\left[\prod_{a=1}^{d}P_a^{1/d}\right]
\le\prod_{a=1}^{d}(\mathbb E P_a)^{1/d}\le1.
$$

On the event in LA13, $\prod_iY_i=2^{\sum q_i-\sum\ell_i}>2^b$. Markov's inequality applied to its $1/d$ power gives $\Pr[\text{event}]\le2^{-b/d}$. This argument does not assume the code lengths are independent and does not add non-disjoint physical time charges. QED pending independent review.

## 2. Matching obstruction: lookahead exponent is essentially sharp

For any fixed $d=r+1$ dividing $K$, split the $K$ independent q-bit blocks into consecutive disjoint groups of size $d$. For $q>t\ge1$, put $\ell=q-t$. Within each group, adapt TMR-3/012's XOR codebook: for cut $i$, XOR the other $d-1$ high t-bit pieces and the other $d-1$ low ell-bit pieces. Give the $2^\ell-1$ local values satisfying (high XOR = 0, low XOR nonzero) short distinct ell-bit words except $1^\ell$; give every remaining value the long word $1^\ell\Vert X_i$.

Each conditioned local codebook is prefix-free and depends on no block after the end of its own group, so its forward lookahead is at most $d-1=r$. The short/long flag is identical within each group, and the flags of different groups are independent. Each group is short with probability

$$
p=2^{-t}-2^{-q}.
$$

Let $\delta=2^{-t}(1+2^{-q})$. The target per-cut threshold $q-\log_2(1/\delta)=\ell+\log_2(1+2^{-q})$ lies just above $\ell$. For fixed $K,d,t$ and all sufficiently large $q$, even one long group raises the average length above the threshold. Consequently the LA13-equal failure probability is **exactly**

$$
p^{K/d}=(2^{-t}-2^{-q})^{K/d},\qquad
\frac{p^{K/d}}{\delta^{K/d}}\longrightarrow1
\quad(q\longrightarrow\infty).
$$

Thus the exponent $K/(r+1)$ cannot be uniformly improved to a strictly larger exponent under the stated hypotheses, even for independent disjoint source blocks. This also independently explains why TMR-3/012, which has global future dependence, is not a counterexample to LA13.

## 3. Reproducible executed audits and hostile controls

**Published exact hosted-V8 executable:** [experiments/tmr/tmr3_lookahead013.cjs](https://github.com/j15marti/pnp/blob/main/experiments/tmr/tmr3_lookahead013.cjs), blob 13d594f37de94d8664a27b10cf913f2b422d933. **Published immutable raw output:** [results/raw/tmr/2026-11-14_0035_TMR3_LOOKAHEAD013_RAW.json](https://github.com/j15marti/pnp/blob/main/results/raw/tmr/2026-11-14_0035_TMR3_LOOKAHEAD013_RAW.json), blob adbed1dcbffac34ce2dfa654c0ec9a1036ecdf18.

The EXACT published JavaScript audit function ran in hosted V8 (not an unexecuted wrapper). Its 14 exhaustive $(q,t,K,d)$ group configurations checked 218,752 complete global source vectors, 19,554 conditioned codebooks, 294,488 generated codewords and every adjacent prefix pair, plus 12 adaptive/causal prefix-code tail inequalities from 49,152 further exhaustive global-vector comparisons and 5,329 additional conditioned fibers. **Zero failed assertions.** Independently authored native CPython 3.13.5, run locally, reproduced all 14 group probabilities and 12 adaptive inequalities with 218,752 plus 49,152 comparisons, also zero failures. That Python verifier is in the local run outbox only, and is NOT claimed to be GitHub-published or an instruction-level SAT TM simulator.

Examples for $q=4,t=2,K=4$, $\delta=0.265625$:

| Future lookahead r | Exact lower-tail probability | LA13 upper bound |
|---|---:|---:|
| 0 | 0.0012359619140625 | 0.0049782395362854 |
| 1 | 0.03515625 | 0.070556640625 |
| 3 | 0.1875 | 0.265625 |

**Hostile causal-bound falsifier:** TMR-3/012's global-XOR construction with the same $q,t,K$ produces actual failure probability $0.1875$, violating the falsely asserted $r=0$ bound $0.0049782395362854$, while satisfying the correct $r=3$ bound $0.265625$. The additional bounded-lookahead restriction is essential. No hidden oracle, advice, random-access port, nonuniform program family, or uncharged lookup is used in the mathematical construction.

## 4. Exact transfer gap to unrestricted SAT and all polynomial workspaces

TMR-3/008 and /011's candidate local-input physical crossing-code analysis and TMR-3/010's proven *marginal* Kraft aggregate may feed this lemma ONLY after proving that, on ONE chosen source distribution and ONE fixed correct uniform total SAT machine, the complete crossing code at each selected cut depends on at most r subsequent independent free blocks. A two-way input head can scan the whole input, return across any cut and place future-source-dependent data in its complete work configuration. The complete crossing record therefore generally has **r as large as K-1**; a small $r$ is NOT available from local head movement or disjoint free blocks alone. Restricting to one-way/one-pass codes without a proved physical-model transfer is not sufficient.

If a physical premise were established, the result improves the *probability* of a same-execution crossing product, not its $T_A(F)(S_A(F)+1)=\Omega_A(Lm)$ magnitude. With $m=\Theta(n^\alpha)$, $0<\alpha\le1$, $L=\Theta(n\log n)$, the bound excludes only joint exponent pairs $k+s<1+\alpha$ for $T=O(L^k)$ and $S=O(L^s)$ on the SAME realization. Since $S_A(F)\le O_A(T_A(F)+1)$ for standard local finite-tape machines, this remains a fixed polynomial-strength lower bound, not the required all-exponent $P\ne NP$ separation. No transfer to arbitrary polynomial workspaces or representation-independent post-copy SAT processing has been proved.

Allow Horn, 2-SAT, Gaussian-elimination XOR/Tseitin, bounded-treewidth DP, disjoint products, sharing, caching, recomputation, reordering, auxiliary variables, arbitrary compact algebra, and copying/revisiting source bits. None of these is compelled to materialize the abstract codebook. The construction is a *coding counterexample and theorem*, not a generic SAT algorithm or a hardness assumption.

## 5. Original sources, recovered evidence, status and next work

First read and rechecked the superseding 2026-11-13 12:49 PST directive (Git blob 47459817e66dccf1f3079e6c724c0fd2643e7bc4). Root proof1.txt was fully read, 28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343. Ordinary fetch of proof2.txt gave a blank body with SHA 930c5eeddafce656717f28055a7a9a755f44737c; the original Git blob was fetched successfully with its complete **1,051,196 characters**. Root main.tex similarly had an empty ordinary fetch but authentic full Git blob SHA 0233cb0ca16a63a2a63a83af6a61ffe985632945 was recovered, 2,518,238 characters. Current issue #3 through TMR-2/014, AGENTS.md, CODEX.md, pnp research skill and all five latest TMR handoffs were reviewed, together with original TMR-3/008, /010, /011, /012 and TMR-5/009 reports and original TMR-3/012 executable. Previous exact Kraft arithmetic is adopted, not presented as a new discovery.

**Primary sources checked for correct scope:** McMillan (1956), *Two inequalities implied by unique decipherability*, IEEE Transactions on Information Theory 2(4), 115-116, https://doi.org/10.1109/TIT.1956.1056818 (Kraft-McMillan input). Fortnow, Lipton, van Melkebeek and Viglas (2005), *Time-space lower bounds for satisfiability*, JACM 52(6):835-865, https://doi.org/10.1145/1101821.1101822. The latter concerns deterministic **random-access Turing machines**, excluding for every $c<\varphi$ some suitably small-space exponent $d>0$ for time $n^c$ and space $n^d$. It does NOT prove a lower bound against every polynomial workspace or every time exponent. LA13 itself follows from the self-contained Kraft, conditional expectation, Hölder and Markov proof above, not from an unverified SAT lower-bound citation.

**Corpus conflicts:** The legacy LSPV role allocation in AGENTS.md/CODEX.md and trackers is superseded by the newer TMR directive, but their mathematical artifacts persist. A blanket claim that disjoint free blocks force $\delta^K$ concentration is FALSIFIED by TMR-3/012; LA13 identifies the strictly stronger causality premise required for such amplification.

**Tracker decision:** TRACKERS REVIEWED; NO MATERIAL CHANGE to proof1.txt or proof2.txt. No claims reach unrestricted proof-chain status. Canonical root main.tex is unchanged: TMR-5 owns whole-document synthesis and no mathematical status was promoted. No scheduled tasks or agents were created, revived or modified. Full project preflight, LaTeX compilation, native Node and a physical general SAT TM simulator were not executed.

**One next target:** TMR-5 independently review the conditional-expectation/Hölder proof and the group-XOR sharpness construction. TMR-3 should then test whether any **complete physical crossing-code** for an unrestricted two-way SAT machine admits a uniform sublinear forward-dependence radius, or produce a concrete paid-reread counterexample. Until that charged physical bridge is established, the all-exponent SAT processing lower bound and P versus NP remain OPEN.

END_OF_REPORT::TMR3::LOOKAHEAD013::2026-11-14_0037_PST
