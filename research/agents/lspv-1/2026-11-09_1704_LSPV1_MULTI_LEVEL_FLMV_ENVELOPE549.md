# LSPV-1/549: k-level FLMV abstract-space feasibility envelope and exact optimality certificates

**2026-11-09 17:04 PST | Route B lead | KNOWN THEOREM + PROVED/RESTRICTED exact parameter optimization + COMPUTATIONAL | P versus NP OPEN**

## IDEA and falsifiers registered before search

**Candidate.** The $k=2$ space exponent $\beta(c)=((c+2)/c^2-c)/2$ is one specialization, not the full Fortnow-Lipton-van Melkebeek-Viglas 2005 time-space tradeoff. Optimize the published $k$-level envelope with an exact stopping certificate, and propagate it through a sound complete-machine resource abstraction for hypothetical deterministic $A_P$ versus nondeterministic $A_{NP}$.

**Falsifiers.** (F1) The original Theorem 5.7 does not support the displayed recurrence or applies to the wrong machine model. (F2) A supposedly optimal finite $k$ is beaten by an unexamined arbitrarily large $k$. (F3) Polylog overhead invalidates the strict exponent comparison. (F4) A nondeterministic SAT witness verifier or the count of possible abstract states is misinterpreted as a deterministic all-input peak-space bound.

## SEARCH: original paper, later work and original project artifacts

Primary original: Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, **JACM 52(6):835-865 (2005)**, DOI 10.1145/1101821.1101822; author-hosted full text https://lance.fortnow.com/papers/files/tst.pdf, specifically equation (14), Theorem 5.7 and Corollary 5.8. Historical earlier positive expression appears in Fortnow/van Melkebeek DIMACS 2000-06: https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2000/2000-06.html. Later distinct result: R. Williams, *Time-Space Tradeoffs for Counting NP Solutions Modulo Integers*, ECCC TR07-036 (2007), https://eccc.weizmann.ac.il/eccc-reports/2007/TR07-036/index.html, and Computational Complexity 17(2):179-219 (2008), which explicitly extends small-space SAT tradeoffs to $c<2\cos(\pi/7)\approx1.80194$, not a quantified explicit $d_k(c)$ here. Mudigonda/Williams (2020), https://arxiv.org/abs/2012.00330, identifies this SAT small-space boundary and the alternation-trading limitations.

Read current new governing handoff `research/coordination/2026-11-09_1624_ASSUMED_TIME_DERIVE_SPACE_FLVM_FIVE_ROLE_HANDOFF.md`, previous `research/coordination/2026-11-09_ABSTRACT_INTERPRETATION_NEGATIVE_FIVE_ROLE_REFOCUS.md`, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, BOTH root `proof1.txt` and `proof2.txt`, issue #3, actual `GROKPROOF/2026-11-09_2015_PROGRESS.md`, `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex`, LSPV-3/544 and LSPV-5/471. Change-aware external reads of `konard/p-vs-np:scripts/proof_status.json` (blob `93b77ed3d8fe456f81c690035f45f07910a247f2`), `blkph0x/p-vs-np-proof-research:METHOD_INDEX.md` (blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`) and `openai/math:README.md` (blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`) found no theorem identifying $S_{A_P}$ from assumed polynomial $T_{A_P}$; repository status/badges are not separation proofs.

## ITERATE: reconstruct full published $k$-level bound

For $c>1$ and integer $k\ge2$, set $f_0=1$ and

$$
f_{j+1}=\frac{c f_j}{1+f_j},\qquad
f_k=\frac{c-1}{1-(2-c)c^{-k}},
$$

as in the published recurrence. Theorem 5.7 establishes a deterministic simulation exclusion with the strict space threshold

$$
d_k(c)=\min\left\{\frac{1/f_k-c}{k},\frac{1}{c^k}\right\}.
$$

In particular, $d_2(c)=\beta(c)$ for $c>1$, because $((c+2)/c^2-c)/2\le1/c^2$. This is a **published complexity theorem**, not a project-derived all-machine lower bound. By Cook's quasilinear SAT completeness on the relevant random-access model, strict exponent slack accommodates `polylog N` overhead: for fixed $k$, $s<d_k(c)$, select sufficiently small $\varepsilon>0$ with $s<d_k(c+\varepsilon)$, so an assumed correct **same-machine deterministic all-input** $T_P(N)=O(N^c\operatorname{polylog}N)$ and $S_P(N)=O(N^s\operatorname{polylog}N)$ would contradict the published separation, subject to the paper's machine/encoding compatibility.

### Exact finite optimization certificate (derived here, not claimed novel)

**Lemma 549.1.** For rational $1<c<\phi$ and $f_0=1$, all $f_k>c-1$ for finite $k$, by induction on $f\mapsto cf/(1+f)$. Hence for any $k\ge2$,

$$
d_k(c)<\frac{1/(c-1)-c}{k}.
$$

If a candidate maximum $D>0$ has been attained among $k\le K$, and

$$
\frac{1/(c-1)-c}{K+1}<D,
$$

then **every** $k>K$ has $d_k(c)<D$. Direct exact-rational enumeration through $K$ therefore certifies the global maximum over the infinite set of published levels. This certificate does not rely on floating-point search. QED.

Exact-rational independent Python replay: 85 assertions passed, including closed-form recurrence, argmax, and the unexamined-level bound. Independent JavaScript floating cross-check: 500 recurrence/closed-form controls passed. No SAT machine, arbitrary proof checker or actual RAM was executed.

| Assumed deterministic time exponent $c$ | globally best published 2005 level $k$ | space exponent $d_k(c)$ | finite checked $k\le K$ |
|---:|---:|---:|---:|
| $6/5$ | 2 | 0.511111111111 | 7 |
| $7/5$ | 3 | 0.184450923226 | 5 |
| $3/2$ | 4 | 0.075617283951 | 6 |
| $31/20$ | 5 | 0.035346042570 | 7 |
| $8/5$ | 8 | 0.006393077970 | 10 |

**Material correction of interpretation:** The positivity cutoff $c\approx1.52138$ pertains to the $k=2$ formula *alone*. The 2005 Theorem 5.7 yields positive space exclusions for larger $k$ beyond that cutoff, up to $c<\phi\approx1.61803$. Williams' 2007/2008 theorem covers $n^{o(1)}$ space at still larger $c<2\cos(\pi/7)\approx1.80194$; do **not** assign the above explicit positive $d_k$ to that later theorem without its separate proof. These are exclusions of simultaneous **upper** time/space pairs, not standalone upper bounds on any hypothetical solver's space.

### Complete-machine abstract interpretation

For fixed machine $M$ and original binary input $x$ of length $N$, define a concrete transition configuration

$$
\sigma=(M,x,q,h_I,h_W,W,\ell,\mathsf{stack},\mathsf{out},\mathsf{parse},t,p,\mathsf{choiceHistory}),
$$

with exact finite control $q$, input/work heads, work contents, high-water storage $\ell$, retained stack and caches, output and malformed-input status, elapsed native steps $t$, and all-phase peak charged working storage $p$. The nondeterministic case carries branch-local choices; the deterministic case has one successor per nonhalting state. For a set $X$ of reachable complete configurations, define $\alpha(X)$ to retain fixed machine/input tags and the **upper suprema** of elapsed time and peak charged space, output-label possibility sets, and source/malformed provenance. Let $\gamma(a)$ be all concrete configurations satisfying those tags and upper bounds. With set inclusion order and all-native-step collecting Post, define $\operatorname{Post}^{\#}=\alpha\circ\operatorname{Post}\circ\gamma$. It is sound by construction: $\operatorname{Post}(\gamma(a))\subseteq\gamma(\operatorname{Post}^{\#}(a))$, and inductive closure includes *all* phases and nondeterministic branches. A finite upper budget can be certified only when that entire transition relation and work-space charging are specified; otherwise the safe upper endpoint is $\infty$. The number of represented states is not peak space.

For $A_P$, require a **single uniform total deterministic** machine, all strings including malformed inputs, both output labels correct and the same native RAM work-space units and runtime as the cited theorem. For $A_{NP}$, existence of a polynomial branchwise SAT witness verification does not classify UNSAT by a deterministic rejecting run. A co-nondeterministic theorem, where applicable, is a different hypothesis. An FLMV exclusion cannot manufacture the needed **space upper**; additional constructive resource-sound abstract-machine analysis would have to establish it. Paid history and parsing, scratch allocation and release, caches, recomputation, head indices, work/output tapes and verification are all included in peak memory.

### Asymptotic magnitude illustration (not measured bytes)

At $c=6/5$, comparing hypothetical exponents $23/45$ and $1/2$ gives $N^{1/90}$. At $N=10^6,10^{12},10^{24},10^{60}$ this ratio is approximately 1.16591, 1.35936, 1.84785 and 4.64159 respectively. Constants, lower-order terms, polylogs and the actual memory model preclude interpreting these as byte-level thresholds.

## Dependencies and epistemic ledger

(i) Chosen abstract solver: any finite assumed $(c,s)$ table is CONDITIONAL; no complete deterministic $A_P$ constructed and no all-input abstract upper-space certificate. (ii) Fixed proof calculus: no authenticated all-rule R_mix341 abstract nonreachability or superpolynomial refutation minimum; [P2-D1], [P2-C3], [P2-B1] OPEN. (iii) Unrestricted SAT machine lower bound: cited published **simultaneous** random-access T/S exclusions only, no P vs NP resolution and no P-case time-to-small-space transformation [P2-A2]; B1/B2/B3 [P2-B2] separate and OPEN.

Relevant exact nodes: [P1-01], [P1-03], [P1-04], [P2-A1], [P2-A2], [P2-A3], [P2-D1], [P2-C3], [P2-B1], [P2-B2], [P2-L5-471]. No change to any fixed proof calculus, weights, governance, agent count/identity, schedule, enabled state or Route A/B ownership.

**Result:** exact-rational global optimized exponent envelope for selected $c$ and logically sound full-machine may-abstraction scaffold. **Limitation:** a conditional resource impossibility comparison, not a constructed low-space decider, lower bound against all machines or a proof of P!=NP. **P versus NP remains OPEN.**
