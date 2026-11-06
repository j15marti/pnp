# LSPV-1/434: strict-three-CNF guard / exact affine-hull certificate firewall
**2026-11-05 20:57 PST | Route B lead | PROVED/RESTRICTED (mathematical), COMPUTATIONAL (finite), B3 and P vs NP OPEN.** Independent specialist referee pending. Original R_mix341, five tasks, 2A/3B ownership, weights and schedules unchanged.

## IDEA -> SEARCH -> ITERATE
**Hypothesis:** LSPV-1/432's at-most-r+1 SAT-search-query affine-hull procedure might appear to yield an inexpensive *native* proof of an entailed affine equation. Start with *published* proper signed degree-three Tseitin contradictions and use a guarded strict-3CNF as a falsification control, not a new hard family.

**Falsifiers:** (F1) the guard destroys strict-3 source syntax or SAT projection; (F2) the asserted model-affine hull has additional independent equations; (F3) the even-charge graph incorrectly forces the guard; (F4) extracting the unit using an oracle is miscounted as a historical inference. F1–F3 rejected mathematically and in finite tests; F4 is a live B3 firewall.

Repository audit found the preceding REFEREE330 fully guarded Resolution isometry, LSPV-3/427 strict branch lifting, LSPV-3/387 nonlinear guard interface, LSPV-1/432 affine-model acquisition, and LSPV-2/341 odd-Tseitin mixed shortcut. These are REUSED rather than claimed new. The increment is a proper-width-three auxiliary-aware affine-hull and one-sided-guard source-retraction control.

## Theorem 434.1 (PROVED/RESTRICTED)
Let $F=\bigwedge_{i=1}^{m}(a_i\vee b_i\vee c_i)$ be an UNSAT proper signed 3-CNF on $n$ occurring variables. Make a fresh shared guard $g$ and one fresh private $y_i$ per source clause:
$$
G_3(F)=\bigwedge_{i=1}^{m}
[(g\vee a_i\vee y_i)\wedge(\neg y_i\vee b_i\vee c_i)].
$$
It has exactly $2m$ proper signed three-literal clauses, $n+m+1$ variables, and $6m$ literal occurrences.

For every original assignment $x$,
$$
\exists y\;G_3(F)(g=0,x,y)\iff F(x).
$$
Indeed, the two clauses of block $i$ can both be satisfied iff $a_i\vee b_i\vee c_i$ holds. Since $F$ is UNSAT, every model has $g=1$. Conversely, every original $x$ together with $g=1$ and every $y_i=0$ is a model. Comparing the latter model for all $x$ supplies all $n$ independent original-coordinate differences. For each $i$, choose one $x$ with $b_i\vee c_i=1$, switch only $y_i$ to $1$, and subtract the corresponding all-$y=0$ model. This supplies all $m$ independent auxiliary-coordinate differences. Hence
$$
\boxed{\operatorname{Aff}(\operatorname{Mod}(G_3(F)))=\{(g,x,y):g=1\}.}
$$
Its *complete affine consequence space* has just one independent nontrivial equation, $g=1$. This is a semantic equality, **not** a legal unit-cost R_mix341 source inference.

If the original $F$ is SAT, the same $g=1$ hyperplane is in the affine hull, but there also exists a model with $g=0$. Therefore the model-affine hull is *all* $\mathbb{F}_2^{n+m+1}$ and there is no nontrivial entailed affine equation. These are same-encoding positive and negative controls.

## Theorem 434.2 (PROVED/RESTRICTED strict Resolution, not full mixed)
Let any satisfiable CNF $G$ contain the fresh variable $g$ **only positively** and entail $(g)$. Put $H=G|_{g=0}$, deleting $g$ from all source clauses. In strict oriented binary Resolution with free exact source leaves and one paid node per distinct inferred resolvent, allowing arbitrary shared DAGs,
$$
\boxed{L_{\mathrm{Res}}(G\vdash g)=L_{\mathrm{Res}}(H\vdash\bot).}
$$
A Resolution derivation of $(g)$ cannot pivot on $g$ because no $\neg g$ is a source or derivable. Delete $g$ from all its clauses: every oriented inference remains valid and the conclusion becomes $\bot$, without unrolling shared nodes. Conversely lift each source of any $H$ refutation to its corresponding $G$ source, adding $g$ exactly where it originally occurred. A pivot on any other variable remains a valid strict resolvent. The lifted root is either $\bot$ or $(g)$; the first is impossible since $G$ is satisfiable. Thus the two globally minimized distinct-node costs are equal. This one-sided-source generalization is based on the classical restriction/lifting method and the earlier completely guarded REFEREE330 theorem. No weakening, split, context discharge, new axiom, or semantic oracle is introduced.

**Transfer limit:** This equality compares $G_3(F)\vdash g$ to its *split 3-CNF cofactor* $H$, NOT to the original $F$. The splitting is equisatisfiable, but no polynomial lower-bound-preserving translation of *arbitrary refutations* from $H$ to $F$ has been proved. Do not claim an exponential lower bound for $H$, or for R_mix341.

## Published theorem, encoding and shortcut ledger
- **Urquhart (JACM 1987), Ben-Sasson/Wigderson (JACM 2001):** suitable simple cubic expanding graph $G_h$, $h$ vertices, $3h/2$ original edge variables; four properly signed 3-clauses for each local degree-three parity constraint; odd total charge gives UNSAT; $4h$ clauses and $N=\Theta(h\log h)$ explicit indexed bits. Every **ordinary shared-DAG Resolution** refutation of certain expander sequences has size $2^{\Omega(h)}$. Not an all-machine or full-mixed theorem.
- **Known native mixed escape (LSPV-2/341):** original odd Tseitin sources admit $4h-1$ paid AND3/GF(2) semantic nodes, so a Resolution lower bound cannot simply transfer to R_mix341.
- **Current guarded 3-CNF:** $8h$ clauses, $11h/2+1$ variables, $\Theta(h\log h)$ bits, with an entailed affine unit and an existentially equivalent cofactor. No Res hardness transfer across the clause split is claimed. Finite K4/K33/Cube are controls, not proof of expander hardness.
- **Haken/Cook/Braun:** ordinary PHP Resolution hardness is defeated by Extended Resolution; Braun's 2026 bit-PHP Res($\oplus$) theorem is system-specific, not certified for 3-CNF or historical mixed rules. No system changes are licensed.

## Executed finite tests and resource separation
Standard-library Python independently generated original odd/even K4, K33, Cube sources and split 3-CNF, checked **298,490** assertion groups (all original edge assignments, clause-by-clause local existential equivalence, valid full-dimensional affine spanning witnesses, even-charge $g=0$ models), and built **correctly oriented strict Resolution** proofs of $(g)$ for the odd controls. Its Davis–Putnam strategy is not claimed polynomial.

| graph | original source clauses | guarded strict-3 clauses | total variables | odd/even affine hull rank | exhibited odd paid RES |
|---|---:|---:|---:|---:|---:|
| K4 | 16 | 32 | 23 | 22 / 23 | 47 |
| K33 | 24 | 48 | 34 | 33 / 34 | 99 |
| cube | 32 | 64 | 45 | 44 / 45 | 215 |

An independently implemented Node verifier replayed 32 exact K4 source clauses and all **47 charged strict RES** nodes, checked source SHA-256, true pivots, topological order, g-restricted identical DAG, affine rank and 64 old-input assignments: **2,196 PASS**, six malformed/corrupt controls rejected. The K4 compact JSON inference record is 34,600 bits. This is NOT execution of the still-unauthenticated historical mixed checker.

Host Python producer observed ~1.08 s and max RSS ~96,784 KiB; these are *host measurements*, not a TM time/space theorem. In the ideal minimum, only distinct charged inference nodes count once. In any implemented upper bound, full parsing, source/index/head reads, proof-search failures, transforms, verification, storage, caching, retrieval/recomputation, output and simultaneous peak space must be charged. Route-A materialized child work still obeys $s'\le\max(\rho,\eta,\lambda,\lambda s)$, with $\rho$ covering every local phase.

## Actual searches, project files, limitations
Read governing Nov 2 12:04 handoff; current issue #3 through REFEREE377; AGENTS.md, CODEX.md and skill; original LSPV-2/341 blob c87acd11, LSPV-1/432 and /433 blob 903adccf, LSPV-3/354 and /433, LSPV-5 REFEREE330/374/377, actual GROKPROOF/2026-11-05_1218_PROGRESS.md blob d3183283 and Claude 2026-10-28_1521_ONETAPE-0001 blob 9a5b05d6. Required outside repos: konard/p-vs-np README blob 0e0ec77f plus proofs/complexity/README (finite-machine model); blkph0x/p-vs-np-proof-research README blob f397a774 plus METHOD_INDEX; meelgroup/frat-xor README blob 38a137bc; tanyongkiam/cake_lpr README blob e94f45e9; openai/math README (manuscript catalogue, no direct bridge). Primary-web queries covered proof complexity, Haken, Tseitin, clause splitting, Cook–Reckhow, Braun and Pich/Santhanam (JACM April 2026, self-provability). Direct Google-branded search unavailable. No external GitHub proof implementation or Lean replay was asserted.

Root main.tex blob 593000bbe5b09df6b93fb7453da2ebdf73aeff6b returned **zero readable content bytes**. An ownership-preserving edit could not be verified, so it remains unchanged.

**Remaining OPEN arrows:** exact historical native LOCAL/DEF facet and public/private ports, same-source all-rule mixed normalization or legal counterexample, a superpolynomial $\overline W_{R_{mix341}}$, and the noncircular B3 $\mathrm{SAT}\in P\Rightarrow\overline W_{R_{mix341}}(N)=N^{O(1)}$. P versus NP OPEN.

### References
1. A. Urquhart, *Hard Examples for Resolution* (1987), DOI 10.1145/7531.8928.
2. E. Ben-Sasson and A. Wigderson, *Short Proofs Are Narrow* (2001), DOI 10.1145/375827.375835.
3. S. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution* (1976).
4. K. Braun, *An Exponential Lower Bound for the Bit Pigeonhole Principle in Resolution over Parities*, arXiv:2609.23015 (Sep. 2026).
5. J. Pich and R. Santhanam, *Towards P≠NP from Extended Frege lower bounds*, JACM (2026), DOI 10.1145/3801091.
6. S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems* (1979).
