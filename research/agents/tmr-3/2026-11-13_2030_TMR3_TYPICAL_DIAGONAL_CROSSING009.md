# TMR-3/009: typical-input strengthening of the batched crossing tradeoff

**Date:** November 13, 2026, 20:30 PST (America/Los_Angeles).  
**Repository:** j15marti/pnp, main. **Role:** TMR-3 Time-Space Tradeoffs.  
**Scientific status:** New *distributional implication* PROVED/RESTRICTED **conditional on the still-CANDIDATE TMR-3/008 complete-crossing code and injectivity lemmas**. Original source-splice checks are COMPUTATIONAL. No unrestricted 3-SAT processing lower bound; P versus NP OPEN.

## 1. New result and exact quantifiers

Continue with the **exact** binary proper 3-CNF batched equality family $E_{n,m}(a,b)$ of TMR-3/008, for $1\le m\le n$ and $a,b\in\{0,1\}^n$. The unary header, ordered clause grammar, all sign and ID fields, and exact input length are unchanged:

$$
w=\max(1,\lceil\log_2(5n)\rceil),\qquad
g=12(w+1),\qquad
L=13n+2+2ng.
$$

Fix ONE correct total uniform deterministic multitape decider $A$ with ONE adjacent-moving read-only binary source head, finitely many locally moving writable tapes, a fixed control/alphabet, and no free input-indexed jumps. Let $T_A(F)$ be the actual transitions and $S_A(F)$ all peak visited writable cells of this **same run**, including buffers, parsing, cache, work indices, preprocessing, recomputation, output, and every input reread. No space bound is assumed.

**TMR3-TYPICAL9, conditional theorem.** Suppose the full-configuration crossing-code lemmas CODE and splice injectivity from the original TMR-3/008 report hold with its fixed machine-dependent $d_A>0$. For all $n\ge m\ge16$, with $a$ drawn uniformly from $\{0,1\}^n$, put $F_a=E_{n,m}(a,a)$ and $q=\lfloor m/2\rfloor$. Define

$$
K=\left\lfloor\frac nm\right\rfloor(qg-1).
$$

Then

$$
\Pr_a\!\left[
T_A(F_a)\bigl(S_A(F_a)+1\bigr)
\ge \frac{Lm}{512d_A}\right]
\ \ge\
1-\min\left\{1,\ K\,2^{-q/2}\right\}.
\tag{TYPICAL9}
$$

The right side is useful even when $m$ is moderately less than the explicit sufficient threshold. In particular, for $m\ge8\log_2 L+8$ the success probability is at least $1-1/L$. Thus for sufficiently broad batches **almost every diagonal SAT source** satisfies a same-machine time-space transport product; TMR-3/008 had only shown that *some* diagonal source does.

This does NOT upgrade TMR-3/008's still-unreviewed premises into an independently proved physical-machine theorem. It does NOT hold as written for indexed-input or two-source-head machines, generic 3-CNF encodings, or all polynomial-time exponents.

## 2. Derivation with exact same-execution charges

**Step 1: source cuts and opposite-label splicing.** Consider only full batches. In each batch choose the $qg-1$ source-bit boundaries strictly inside the portion of the first-bank string that begins after the first $q$ completed first-bank four-clause blocks. All $q$ corresponding second-bank blocks occur to the right of every cut. Fix all other equality bits. At each selected cut $c$, varying the $q$ paired bits produces $2^q$ accepting diagonals. Splicing the left of one with the right of a different one produces the **literal canonical** $E_{n,m}(a,b)$ with unequal paired bits, hence UNSAT. This is a valid both-label fooling set without changing the number, names, ordering, or grammar of any other clause.

**Step 2: full crossing codes, not a chosen solver transcript.** On an accepting diagonal, the unique locally moving input head must reach its final second-bank forcing block. Otherwise a same-length opposite-sign final-block input is unseen and would be incorrectly accepted. Therefore it crosses every chosen cut at least once. For each cut $c$, let $r_c(a)$ count its actual crossings, and let $\ell_c(a)$ be the prefix-free binary encoding of the complete ordered crossing configurations, with full writable tape contents, all work head positions, controller state and crossing directions. By the exact original CODE assumption,

$$
\ell_c(a)\le d_A\,r_c(a)\bigl(S_A(F_a)+1\bigr).
$$

Matching complete crossing records for two different $q$-bit choices permit a deterministic accepting splice on an UNSAT source, contradicting both-label correctness. Thus the codes are injective on the conditioned $2^q$ diagonals. Their prefix-free coding gives

$$
\Pr_a[\ell_c(a)<q/2]\le2^{-q/2}.
$$

Here the conditional probability bound holds for **every fixed assignment** of bits outside the relevant $q$ choices, so it holds after averaging over all $a$. It does not assume per-cut hard instances coincide.

**Step 3: uniform union bound across all cuts.** There are $K$ distinct selected boundaries and $K\le L$. The probability that even one has code length below $q/2$ is at most $K2^{-q/2}$. On the complementary event, all selected cuts on **the same actual computation $A(F_a)$** obey

$$
r_c(a)(S_A(F_a)+1)\ge\frac{q}{2d_A}.
$$

A local input-head move crosses at most one boundary, so $\sum_{c}r_c(a)\le T_A(F_a)$. Therefore

$$
T_A(F_a)(S_A(F_a)+1)
\ge\frac{Kq}{2d_A}.
$$

For $m\ge16$, $q\ge m/4$, and with $g\ge24$, $L\le4ng$. Since $\lfloor n/m\rfloor\ge n/(2m)$ and $qg-1\ge qg/2$,

$$
K\ge\frac{nqg}{4m},\qquad
\frac{Kq}{2d_A}\ge\frac{ngq^2}{8d_Am}
\ge\frac{ngm}{128d_A}\ge\frac{Lm}{512d_A}.
$$

For $m\ge8\log_2 L+8$, $q/2\ge2\log_2L+3/2$ and $K2^{-q/2}<1/L$. This proves the **conditional** distributional statement. Every time/space factor is from the same machine, input and execution.

## 3. Native finite audits and source-level negative controls

The independently authored native Node v22.16.0 outbox program at local path /mnt/data/tmr3_20261113_2024/tmr3_batch_typicality009.cjs ran successfully with zero assertions. It covered 195 canonical two-label source/ordering tests, 29,488 exact parsed source splices, including 27,416 genuine unequal-pair UNSAT hybrids, 2,072 equal-pair SAT hybrids, and complete source lengths up to 77,058 bits. Its source and raw local SHA-256 values are recorded below. A **separately written** compact reproduction ran directly in hosted V8, and is the exact published GitHub executable and raw output: 195 canonical parser cases, 29,488 source splices, 27,416 unequal pairs and zero failures.

Numerical union-bound examples from the actual compact V8 run for $n=256$, $L=77{,}058$:

| Batch $m$ | $q$ | Selected cuts $K$ | $1-K2^{-q/2}$ (clipped below at 0) |
|---:|---:|---:|---:|
| 64 | 32 | 18,428 | 0.7188110352 |
| 128 | 64 | 18,430 | 0.9999957089 |
| 256 | 128 | 18,431 | 0.999999999999999 |

These are *algebraic probability lower bounds*, **not** empirical probabilities over physical TM runs. Actual native/V8 executions only confirm clause grammar, source cuts/splices, arithmetic and code behavior. They do not simulate A's complete crossing configurations, prove their injectivity as a physical implementation, or measure all of A's transitions. No full SAT fallback or LaTeX compiler was run.

Native outbox SHA-256 (not GitHub artifacts): source **cee90a28a4f9669c5e81dd14702d3b8272ca3eb19a4157418105f5e4fde283f4**, raw **7b4c7d349fab908abc37842e38ec70ddc166189602d6d15ba5f7111fcf59dda9**. The native outbox began with a failed assertion for $m=1$: the test incorrectly counted candidate cuts where the selected-cut set was intentionally empty. It was repaired and fully rerun; this was a test-harness counting error, not discarded source evidence.

**Readback-verified GitHub artifacts:**
- Executable: experiments/tmr/tmr3_typical_diagonal009.cjs, blob 5296e5beeeb59a1c3a78e163a6cb637eb330f6d0.
- Raw data: results/raw/tmr/2026-11-13_2030_TMR3_TYPICAL_DIAGONAL009_RAW.json, blob 0eb9438f916e16151fa8d4a5c3a0bab7307c860d.

## 4. Hostile controls and an upper-bound wording repair

TMR-3/008's claimed upper $T_D=O(L\lceil m/r\rceil)$, $S_D=O(r+\log L)$ on **all** canonical $E_{n,m}(a,b)$ survives *if* the fast path distinguishes two predicates: (i) failure of canonical grammar/identifiers, which invokes a paid exhaustive fallback; and (ii) an authenticated $a_i\ne b_i$, which sets an UNSAT flag and continues authenticating the complete source before returning UNSAT **directly**. The 008 prose says "On ANY mismatch ... invoke ... exhaustive" and is misleading if read as including semantic pair inequalities: a literal exhaustive-enumeration fallback on every valid unequal pair would take $2^{5n}$ assignment rounds on canonical UNSAT sources. The original published 008 executable already distinguishes these outcomes, returning \`member:true,sat:false\` for canonical unequal pairs. **Correction requested: change this wording only; do not treat the original scoped lower product as falsified.**

The one-head transport lower bound is still destroyed by reordering to $m=1$ (TMR-3/007), by adding a second independently moving source head or indexed access, and by moving to a solver with enough polynomial work space to cache full batches. Horn/2-SAT, affine/GF(2) Tseitin, bounded-treewidth, disjoint product, and compact-circuit strategies remain compatible with cheap processing on special instances; no theorem requiring their enumeration was assumed. Our test did not run generic implementations of these solvers.

This strengthens the *distribution of hard inputs inside one restricted source geometry*, not the time exponent. On $m=\Theta(n^\alpha)$, $L=\Theta(n\log n)$, even the new typical-input result forces only $T(S+1)=\Omega(Lm)$, excluding simultaneous exponent pairs $k+s<1+\alpha$ there. It cannot rule out arbitrary polynomial workspace or every polynomial time exponent; $S\le O(T)$ on the same machine yields no stronger conclusion than compulsory $T=\Omega(L)$ source traversal.

## 5. Historical corpus, primary sources, dependencies and next target

The original TMR-3/008 report, executable and raw data, TMR-3/002 and /007, LSPV-5/167 crossing-averaging predecessor, TMR-2/010 and TMR-5/007 source/fast-path controls, newest five TMR handoffs, replacement directive, issue #3, AGENTS.md, CODEX.md and the repository pnp skill were inspected. Root proof1.txt read fully (28,714 chars, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343); root proof2.txt recovered via the authentic Git blob rather than treating the empty contents-API body as the stored file (1,051,196 chars, SHA 930c5eeddafce656717f28055a7a9a755f44737c); root main.tex likewise recovered by Git blob (2,504,241 chars, SHA 103435a5c6ff2b02e2b975e7c00d37476d66b064).

**Sources and scope.**
1. F. C. Hennie, *One-Tape, Off-Line Turing Machine Computations*, Information and Control 8 (1965), 553-578; 1965 original crossing-sequence context, not a claimed arbitrary multitape SAT bound. [NASA conference record](https://ntrs.nasa.gov/citations/19660035639).
2. L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6) (2005), 835-865, [publisher primary abstract](https://doi.org/10.1145/1101821.1101822). Explicit random-access TM model, with some SAT $n^c$ vs $n^d$ exclusions for $c$ below the golden ratio and suitably small positive $d$. Neither this paper nor our one-head argument excludes arbitrary polynomial workspace.
3. A. Borodin and S. Cook, *A Time-Space Tradeoff for Sorting on a General Sequential Model of Computation*, SIAM J Comput 11(2) (1982), 287-297, [publisher primary abstract](https://doi.org/10.1137/0211022). Its task is sorting, not SAT.
4. Project's original specific cut proof, [TMR-3/008](../../agents/tmr-3/2026-11-13_1935_TMR3_BATCH_LOCALITY_TRADEOFF008.md), remains **CANDIDATE** pending independent physical crossing-code review; the new theorem is a conditional corollary, not an independent promotion of that parent.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The P=NP and P!=NP chain nodes remain OPEN. Root main.tex was not edited; TMR-5 owns synthesis and the new distributional statement should stay conditional until its underlying crossing lemma is independently reviewed. No scheduled tasks were created, revived or modified.

**Next single target:** TMR-5 should independently reconstruct the prefix-free full-configuration crossing record (including all work-head positions and total binary serialization bound $\ell_c\le d_A r_c(S+1)$) and audit the all-cuts conditional fooling-set splices. A genuine post-acquisition processing bound invariant under favorable ordering, two input heads/INDEX, algebraic reduction, caching, recomputation and arbitrary polynomial workspace remains OPEN.

END_OF_REPORT::TMR3::TYPICAL_DIAGONAL009::2026-11-13_2030_PST
