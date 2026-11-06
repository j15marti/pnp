# LSPV-3/439: Bit-PHP to unary-PHP, a conditional ER escape

**2026-11-05 21:32 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL. P vs NP OPEN.**

## Idea, falsifiers, and revision

**Hypothesis:** Published bit pigeonhole lower bounds for unrestricted DAG-like Res($\oplus$) may be defeated by a shared two-input Boolean extension decoder in a stronger calculus. Fix four falsifiers: a nonconservative prefix gate; an incorrectly oriented source-to-collision Resolution step; a required free tautology in the at-least-one proof; or a hidden illegitimate original /341 defining-facet port. The first three were rejected mathematically and by finite independent replay. The fourth remains **OPEN** for historical /341. The proof is explicitly for proposed **FACET-A**, not the authenticated historical parser.

## Mandatory published proper-3-CNF baseline and why it is an upper-bound control

Before choosing bit-PHP, retain the established **Urquhart / Ben-Sasson–Wigderson odd cubic-expander Tseitin family**, which is directly proper 3-CNF: for connected 3-regular expander $G_h$ on $h$ vertices, let edge variables be $x_e$ ($3h/2$ variables); choose charges $\chi_v$ with $\bigoplus_v\chi_v=1$, and encode each local row $\bigoplus_{e\ni v}x_e=\chi_v$ as the four 3-literal clauses forbidden by its opposite-parity assignments ($4h$ clauses, $N=O(h\log h)$ indexed bits). Odd total charge certifies UNSAT. Published ordinary **shared-DAG Resolution** expander bounds are $2^{\Omega(h)}$, not full-calculus or all-machine bounds (Urquhart, JACM 1987; Ben-Sasson and Wigderson, JACM 2001). The **known legal mixed GF(2)/AND3 shortcut** gives the exact historical-semantic minimum $W_{R_{\mathrm{mix341}}}=4h-1$ for bridgeless cubic graphs (LSPV-2/341), so this published directly-3-CNF candidate cannot yield a full-mixed superpolynomial lower bound. This is reused established work, not a new result.

Braun's later bit-PHP is investigated **only as a stronger published Res($\oplus$) lower-bound control and an ER/DEF transfer challenge**; it starts at width $2\ell$ and no hard strict-3-CNF transfer is claimed. This order avoids inventing a new hard family or silently upgrading restricted hardness.

## Exact established family and theorem

Braun, arXiv:2609.23015, revised 2026-10-22, §1.1 and Theorem 1.1, defines $n=2^\ell$ holes, $m=n+1$ pigeons, bits $b_{it}$, and source clauses

$$
C_{ij,a}=\bigvee_{t=1}^\ell[b_{it}\ne a_t]\ \vee\ \bigvee_{t=1}^\ell[b_{jt}\ne a_t],\quad i<j,\ a\in\{0,1\}^\ell.
$$

The formula has $m\ell$ original variables and $n\binom m2$ clauses of width $2\ell$. It is UNSAT by pigeonhole counting. The preprint states and supplies Lean code for a lower bound $>\exp(n/(32768\ell^2))$ for all $\ell\ge32$ in unrestricted **shared-DAG Res($\oplus$)** with arbitrary affine pivots and semantic weakening **but without extension axioms**. It is not a theorem for ER, /341, arbitrary SAT machines, or strict 3-CNF. Independent expert review is not claimed.

## All-size certified-interface construction

**PROVED/RESTRICTED:** In binary Resolution plus globally fresh *paid* two-input AND gates with individually addressable owner-qualified defining facets (proposed FACET-A), define for every pigeon $i$ and prefix $p$ of length at least 2 a shared gate $y_{i,p}=y_{i,p^-}\land[b_{i,|p|}=p_{|p|}]$. Length-one prefixes are signed source-bit literals. Every gate $z=A\land B$ has the three facets $(\neg z\vee A)$, $(\neg z\vee B)$, $(z\vee\neg A\vee\neg B)$, charged by one owner.

The two child third facets resolve on the next bit to give $\neg y_{i,p}\vee y_{i,p0}\vee y_{i,p1}$. Resolve both length-one bridges on the first bit and repeatedly expand the frontier by strict Resolution, yielding the ordinary unary-PHP at-least-one clause $A_i=\bigvee_a y_{i,a}$ **without a free tautology**.

Gate-chain facets also derive $\neg y_{i,a}\vee[b_{it}=a_t]$ for every $t$. Resolve each original source $C_{ij,a}$ on the $2\ell$ opposite bit literals against these authenticated implications, obtaining $B_{ij,a}=\neg y_{i,a}\vee\neg y_{j,a}$. These are exactly the standard unary-PHP collision clauses. The classic Cook/Cook-Reckhow polynomial Extended Resolution PHP refutation then gives a **conditional polynomial ER-size upper bound** for the original bit-PHP family.

Let $D=m(2n-4)$ be paid gate definitions. One explicit shared compiler uses exactly

$$
R=m\left(2n-5+\sum_{d=3}^{\ell}2^d(d-1)\right)+2\ell n\binom m2
$$

paid Resolution nodes for ALL unary premises. $D+R=O(n^3\ell)$. Appending the Cook unary PHP ER construction costs another fixed polynomial $P(n)$, including its own charged definitions and Res steps. This is an upper bound, **not** a globally certified minimum. Worst-case explicit proof evidence has polynomial bit length, with a coarse bound $O(n^4\ell^2\log n)$. Parser, ID lookup, derivation construction, emitted bits, verification, caching, and machine storage remain separate; source-only logical node cost is not time or space.

**Strict 3-CNF:** The published source is width $2\ell$. A standard width-$k$ chain splitting uses $k-2$ strict three-literal clauses and $k-3$ fresh variables per source. Original $C$ can be rederived by $k-3$ strict binary Resolution steps, proving ONLY the polynomial **upper-bound lifting direction** into the strict 3-CNF, with $n\binom m2(2\ell-3)$ added paid nodes. Equisatisfiability alone gives no Res($\oplus$) lower-bound transfer back. No published hard strict-3 transformed family is asserted.

## Checks, corpus, safeguards

Local complete producer and independently authored JavaScript proof verifier checked exact original DIMACS SHA, all original clauses, all defining facets, oriented Resolution DAGs, all unary PHP outputs and seven rejected deliberate corruptions. Small controls, outside $\ell\ge32$: $\ell=2$: 40 sources, 20 DEF, 175 RES, 195 paid, 1,984 independent checks, 25,794-byte typed trace. $\ell=3$: 288 sources, 108 DEF, 1,971 RES, 2,079 paid, 17,352 checks, 254,494-byte trace. These derive **unary premises**, not a complete finite empty-clause certificate. They are not authoritative /341 byte-checker executions. Complete raw traces, Python producer, independent JS replay, resource observations and hashes are in local reproducibility archive `LSPV3_439_BPHP_ER_DECODER_REPRO.zip`; this GitHub record carries the summary and a separate compact checker.

Audited original /341 `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11`, prior LSPV-3/436-438, LSPV-1/434, LSPV-5/REFEREE371, governing handoff, current issue #3, actual Grok `research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex`, and Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`. External `konard/p-vs-np` at `ecedd2b45f1c524d85c00b2da27a9c140025550c` (`proofs/experiments/np_subset_p_proof_attempt.md`) keeps the polynomial SAT machine open; `blkph0x/p-vs-np-proof-research` at `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` (`PROOF_PORTFOLIO_BRIDGE_REPORT.md`) does not certify universal bounded interfaces. FRAT-XOR `format.md` at `18cd6bc17af10a9891c10a846ce966166f9fe0dc` gives typed XOR and clause IDs for another proof system, **not** native /341 syntax. Direct Google-branded search was not executed. Root `main.tex` returned zero readable bytes; no unsafe edit was made.

**Remaining:** Authenticate facet/export/private-wire byte grammar and all-rule translation before claiming this shortcut as a *historical* /341 upper proof; prove or refute superpolynomial full mixed Wbar and noncircular B3. The 2A/3B roles, schedules, weights and ownership are unchanged. P versus NP remains OPEN.

References: [1] Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015 (2026), https://arxiv.org/abs/2609.23015 . [2] Cook & Reckhow, *The relative efficiency of propositional proof systems*, JSL 1979. [3] Buss, *Polynomial size proofs of the propositional pigeonhole principle*, JSL 1987, https://mathweb.ucsd.edu/~sbuss/ResearchWeb/php_PolyFrege/ . [4] Buss, *Quasipolynomial Size Proofs of the Propositional Pigeonhole Principle*, 2015, https://mathweb.ucsd.edu/~sbuss/ResearchWeb/QuasiPolyPHP/ .
