# TMR-5/009: independent multihead MAY review and a sharp correlated-code obstruction

**Date:** 2026-11-13 21:55 PST (America/Los_Angeles). **Role:** TMR-5 Machine Bottleneck Redteam and synthesis. **Repository:** j15marti/pnp, main.

**Verdicts:** (1) TMR-4/012's exact multiple-local-head MAY interval theorem receives an independent favorable mathematical review at **PROVED/RESTRICTED** scope, limited to its declared source/head abstraction and charged physical access. (2) A new explicit correlated prefix-free code construction TMR5-KS9 proves the **K-independent probability tail in TMR-3/010 is essentially sharp from its marginal Kraft hypotheses alone**. This new mathematical construction is **CANDIDATE pending TMR-3 independent review**; its finite instances are **COMPUTATIONAL**. (3) TMR-3/010's actual 3-SAT crossing consequence remains **CONDITIONAL/RESTRICTED** on TMR-3/008's unreviewed physical crossing-code and legal-splice premises. No representation-independent superpolynomial 3-SAT lower bound has been proved. **P versus NP OPEN**.

## 1. Independent review of TMR-4/012

Let one fixed total correct deterministic multitape 3-SAT decider have $h\ge1$ physically local, read-only input heads at data positions $H=(p_1,\ldots,p_h)$, each observing its pre-move coordinate and moving by at most one coordinate per charged transition. It has arbitrary charged work tapes, fixed finite alphabet/control and serves all lengths. For fixed source $x$ of encoded binary length $L$ and independently certified same-length opposite-label valid sources $y_i$, put $D_i=\{j:x_j\ne(y_i)_j\}\ne\varnothing$. The MAY state $(H,V)$ retains heads and observed source coordinates; it does not retain work-tape states.

For every unhit support $D_i\cap V=\varnothing$, choose head-containing intervals $I_j=[a_j,b_j]$ with $a_j\le p_j\le b_j$ whose union hits every unhit support. Then the independently reviewed exact remaining shortest-path distance is

$$
\Psi(H,V)=
\begin{cases}
0,&D_i\cap V\ne\varnothing\text{ for all }i,\\[3pt]
1+\displaystyle\min_{\{I_j\}}\max_{1\le j\le h}
\left((b_j-a_j)+\min(p_j-a_j,b_j-p_j)\right),&\text{otherwise}.
\end{cases}
$$

**Independent proof of shortest path:** Any goal-reaching path must read one position of each unhit support. On each head's actual local walk, the visited pre-move read positions have extrema $a_j,b_j$ and its start is $p_j$. Its number of physical movements before the last extreme read is at least $(b_j-a_j)+\min(p_j-a_j,b_j-p_j)$; the last read consumes an additional paid transition. Concurrent head movements imply the path costs at least $1+\max_j c_j$. Conversely, for a minimizing collection of covering intervals, each head travels first to its nearer endpoint and then across to the other endpoint, reading that final endpoint on a paid transition. Heads run concurrently and idle when finished. Thus the path of the stated cost exists in the MAY graph. Initial observation set $V$ may be arbitrary; no one-pass assumption is used.

**Every-transition simulation and both labels:** Relate every concrete configuration to its actual source-head coordinates and cumulative observed input positions. Each real transition has a cost-one abstract edge moving the heads as the real transition does and observing its actual pre-move source positions; all work-state changes, copying, rereading, compact algebra and recomputation are conservatively forgotten. The initial states relate with $V=\varnothing$. If a concrete SAT or UNSAT terminal did not hit some $D_i$, running the identical deterministic program on opposite-label $y_i$ would reproduce every scanned symbol and full work configuration and halt with the same answer, contradicting both-label total correctness. Hence both terminal labels have enabled cost-zero abstract goal edges. As $\Psi$ is the exact goal distance, **every** paid edge satisfies $\Psi(u)\le1+\Psi(v)$, zero-cost stutters preserve it, zero-cost terminal edges start at $\Psi=0$, and $\Psi(\mathrm{goal})=0$. Therefore $\Psi(H_0,\varnothing)\le T_A(x)$ on the SAME execution.

**Scope and ceiling:** One head can scan the complete source, so $\Psi(H_0,\varnothing)\le L+\lfloor(L-1)/2\rfloor=O(L)$ for data-cell starts. This is a ceiling on an overly permissive abstraction's provable *lower bound*, not an upper bound on actual SAT runtime. Extra heads may reduce this cost: $L=11$ with endpoint singleton supports has exact distance 16 from one center-start head, 11 from two left-start heads, and 1 from opposite-end heads. Zero-cost indexed jumps are outside the model. All arbitrary polynomial writable workspace remains allowed. **Verdict: PROVED/RESTRICTED after independent review**, not an unrestricted processing lower bound.

**Independent native computation:** A fresh Python implementation (not the peer source) separately enumerated shortest paths by BFS and interval covers, including arbitrary already-observed $V$, for 224 seeded small configurations with one to three heads; every equality passed. It checked 8,816 separately generated paid edges for the all-edge potential inequality, plus the three endpoint hostile controls, with zero failures. Independently inspected peer's original report, exact published Python source and raw result; these independent runs do **not** claim native execution of the peer's exact program or physical instruction-level TM simulations. Local-only verifier and raw evidence remain in the run outbox; the new publicly published executable below instead tests the separate correlated-code theorem.

## 2. New TMR5-KS9: marginal Kraft tails do not concentrate with more cuts

**Statement and precise setting.** TMR-3/010 proves for $K$ prefix-free injective codebooks on uniform $X\in\{0,1\}^q$ the aggregate inequality

$$
\Pr\left[\frac1K\sum_{c=1}^{K}\ell_c(X)
<q-\log_2(1/\delta)\right]\le\delta,
\qquad 0<\delta<1.
$$

This combinatorial lemma is correct. However, its **marginal Kraft and prefix-free hypotheses alone** cannot improve $\delta$ to an error vanishing with $K$. For arbitrarily large $q$ and arbitrary $K\ge1$, explicit perfectly correlated **valid prefix-free** codebooks make the left-hand probability arbitrarily close to $\delta$.

**Constructive proof.** Fix integers $q>t\ge1$, put $\ell=q-t$, $M=2^\ell-1$, and use the $2^q$ possible values $x=0,\ldots,2^q-1$. Fix the reserved binary prefix $u=1^\ell$ and the following complete injective binary codebook:

$$
c(x)=
\begin{cases}
\operatorname{bin}_{\ell}(x),&0\le x<M,\\
u\,\Vert\,\operatorname{bin}_q(x-M),&M\le x<2^q.
\end{cases}
$$

All $M$ short words have length $\ell$ and exclude the reserved prefix $u$. All other codewords begin with $u$ and have distinct $q$-bit suffixes. Since there are $2^q-M\le2^q$ long words, the suffixes exist. No short word prefixes a long one; all words within each length class are distinct. **The code is prefix-free and injective**, with Kraft sum

$$
\kappa=\frac{2^\ell-1}{2^\ell}
+\frac{2^q-2^\ell+1}{2^{\ell+q}}
=1-\frac{2^\ell-1}{2^{\ell+q}}<1.
$$

For any $K$, take **identical** codebooks $c_1=\cdots=c_K=c$. This is allowed in the aggregate lemma, which does not assume independence across cuts. Choose

$$
\delta_{q,t}=2^{-t}(1+2^{-q})\in(0,1).
$$

The threshold becomes $q-\log_2(1/\delta_{q,t})=\ell+\log_2(1+2^{-q})$, strictly between $\ell$ and $\ell+1$. Thus the failure event is **exactly** the $M$ short codewords on every cut, with probability

$$
p_{q,t}=\frac{M}{2^q}=2^{-t}-2^{-q}.
$$

It does not change with $K$ at all. At any fixed $t$,

$$
\frac{p_{q,t}}{\delta_{q,t}}
=\frac{1-2^{t-q}}{1+2^{-q}}\longrightarrow1
\qquad(q\longrightarrow\infty).
$$

Therefore no bound $o_K(\delta)$ or exponentially decreasing function of $K$ follows **solely** from marginal prefix-free coding and Kraft. This **does not refute** TMR-3/010; it shows its current coefficient and lack of $K$-concentration are nearly optimal. A stronger result would need new structural *joint* constraints on the physical crossing codes, beyond per-cut conditional injectivity. Nothing here proves that these abstract correlated codebooks are physically realizable as transcripts of one fixed SAT machine.

**Native and independent computational evidence:** The exact newly published Node.js source was executed both in hosted V8 and natively under Node 22.16.0, with the same Git blob SHA and identical results: 60 explicitly generated prefix-free codebooks, 196,276 adjacent sorted-word prefix comparisons, 240 $K\in\{1,4,64,4096\}$ tail checks, zero failures. Independently written native Python 3.13.5 performed 60 codebook construction / prefix-free checks and 240 $K$ comparisons, also zero failures. At $q=14,t=3,K=4096$, $\delta=0.1250076294$, actual tail probability $0.1249389648$, ratio $0.9994507171$. Finite tests are **COMPUTATIONAL**, whereas the asymptotic statement is supported by the explicit symbolic construction and proof, pending TMR-3 review.

Public code: [TMR-5/009 verifier](https://github.com/j15marti/pnp/blob/main/experiments/tmr/tmr5_correlated_prefix009.cjs). Public immutable results: [raw JSON](https://github.com/j15marti/pnp/blob/main/results/raw/tmr/2026-11-13_2155_TMR5_CORRELATED_PREFIX009_RAW.json). Independent Python is **local-only** and not represented as a GitHub publication.

## 3. Dependency synthesis, adversarial controls, and next arrow

**TMR-1/011:** the arbitrary-origin single-head source-transport theorem is independently reviewed by TMR-4/012 and specializes from the now-reviewed multihead identity. Fixed finite total program, exact binary input length and same-machine cost remain mandatory.

**TMR-2/011:** the $5r$ SAT and 24-bit UNSAT **promise sign-bit certificate** claims in the 8-mask family remain restricted, and their native enumerations do not imply compulsory memory retention or reasoning time. TMR-2/010's authenticated two-label compact mask classifier is a polynomial structural countermodel.

**TMR-3/008 and /010:** the aggregate Kraft theorem survives; the new correlated-code example kills any future attempt to obtain $K$-dependent concentration from marginal prefix-free bounds alone. The physical crossing-code injectivity and all-transition splice must still be independently authenticated before a physical time-space claim is promoted. Even if authenticated, $T(S+1)=\Omega(Lm)$ only excludes limited simultaneous exponents, not all polynomial time/space pairs.

**TMR-4/012:** the all-edge MAY potential is now independently checked at PROVED/RESTRICTED scope, and its $O(L)$ shortest-path ceiling means certificate multiplicity cannot force superlinear processing in this abstraction. A cheap abstract scan is not necessarily a cheap real computation. A genuine cheap real computation is never erased as a spurious abstract path.

**All-input controls:** The current results admit Horn/2-SAT polynomial solvers, GF(2) Gaussian elimination on XOR/Tseitin, bounded-treewidth DP, disjoint products, sharing, padding, variable renaming and auxiliary variables, input rereads, caching and recomputation. The code construction is about arbitrary prefix-free lists, **not** about random-access models, free advice, uncharged table construction or a SAT oracle. It assumes no ETH/SETH or cryptographic hardness. Known relativization, algebrization and natural-proofs obstacles do not themselves disprove the target.

**Exact objective remains OPEN:**

$$
\forall A\text{ fixed total uniform correct SAT decider}\quad
\forall k\ge1\quad\forall C>0\quad\forall L_0\quad
\exists F\text{ valid},\ |F|\ge L_0:\ 
T_A(F)>C(|F|+1)^k.
$$

Neither a small-space restriction nor a bound on one fixed exponent establishes this. A full polynomial 3-SAT algorithm is also a legitimate endpoint.

**Next target for TMR-3:** Independently prove (or furnish a complete counterexample to) the exact physical crossing-configuration splice and variable-length prefix serialization of TMR-3/008 for its authentic grammar and one-head model. Then seek any genuinely new *joint* constraint on different crossing codes, not a marginal Kraft repetition. **Next global target:** a cost-sound full-program processing potential remaining nontrivial after reading the input, allowing arbitrary polynomial workspace and all valid representations.

## 4. Corpus, source scope, and publication protocol

Read the authoritative 2026-11-13 12:49 PST TMR directive first, then recovered complete root proof1 (28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and proof2 (authentic Git blob 1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c), main.tex (authentic Git blob 2,507,300 characters, SHA c0d657568af18ed0a2d17843b8ef0e6c11ac6327), issue #3 through TMR-4/012, AGENTS.md, CODEX.md, repo pnp-research SKILL.md, all five current TMR handoffs, original TMR-4/012 report/code/data, TMR-3/008 and /010 original reports/code/data, TMR-2/011 original report, and TMR-5/008. Root AGENTS/CODEX old LSPV allocation is superseded, verified historical evidence is not. Readback/rechecked the superseding directive before shared writes.

Primary literature independently checked for *correct scope*: [Cousot and Cousot 1977, POPL abstract interpretation](https://doi.org/10.1145/512950.512973) establishes conservative abstract-execution methodology, not our interval identity. [Buhrman and de Wolf 2002, decision-tree and certificate survey](https://doi.org/10.1016/S0304-3975(01)00144-X) concerns input-query and certificate notions, not unrestricted processing. [Fortnow, Lipton, van Melkebeek and Viglas 2005, JACM](https://doi.org/10.1145/1101821.1101822) excludes certain time/space exponent pairs on random-access models, not all polynomial workspace. [McMillan 1956, IEEE](https://doi.org/10.1109/TIT.1956.1056818) supplies the classical code-length inequality background, not the new explicit correlated construction.

**Tracker decision:** TRACKERS REVIEWED; NO MATERIAL CHANGE to proof1.txt or proof2.txt. Their unrestricted proof arrows remain OPEN. New claims are placed in role report/handoff and canonical manuscript synthesis without reconstructing either tracker. No scheduled tasks or agents were created, revived or modified. Repository preflight script and instruction-level general SAT TM simulation were **not executed**; peer's original exact Python was inspected but not natively run in this run. Native Node is the exact published new verifier, and independent native Python checks are local-only.

END_OF_REPORT::TMR5::KRAFT_SHARPNESS_AND_MULTIHEAD009::2026-11-13_2155_PST
