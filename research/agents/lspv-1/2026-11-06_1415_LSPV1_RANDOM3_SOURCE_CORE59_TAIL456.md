# LSPV-1/456: A sharpened source-core floor for published random strict-3-CNF

**2026-11-06 14:15 PST | Route B lead | PROVED/RESTRICTED theorem, COMPUTATIONAL controls. P vs NP OPEN.** All original five roles, routes (2A/3B), schedules, native rules and weights preserved.

## IDEA, falsifiers, duplication audit

**Hypothesis.** The exact signed proper random 3-CNF hard family used by Chvátal--Szemerédi and Pang admits a stronger all-rule original-source floor by preserving the without-replacement correction in `binom(n,r)`. Improve existing LSPV-3/443 `n/64` and LSPV-3/457 `n/60` to `n/59`, while retaining every legal algebraic/extension/branch-sharing shortcut. **Falsifiers:** (1) the refined exponential base >=1; (2) the corrected first moment does not go to zero; (3) a sound conservative binary-premise mixed refutation can derive false from satisfiable source ancestry; (4) greedy cores or restricted proof hardness are mistaken for full mixed hardness. The first three are excluded within the exact model; the fourth is a mandatory scope distinction.

Existing LSPV-3/443,457 already establish the method, and LSPV-3/456 already gives a stronger *fragment-restricted* PC-degree/definition-exposure tradeoff. LSPV-3/448 and LSPV-5/367 have already proved pure Resolution branch discharge and nested typed-branch equivalence, so those are not claimed new. This result is only a small certified quantitative improvement of a known Tarsi/union-bound argument. No academic novelty is claimed.

## Exact 3-CNF and established hard family

For integer ambient parameter `n>=3`, sample `m=8n` **indexed, independent-with-replacement** proper width-three signed clauses, uniform among the `8 binom(n,3)` clauses on distinct variable labels in `[n]`. Repetitions are retained as distinct *source indices*. Standard consecutive-ID DIMACS has `N=O(n log(n+2))` encoded bits. The number of *occurring* variables need not equal n (LSPV-3/457 correction).

The formula is UNSAT with probability tending to one because

$$
\mathbb E[\#\mathrm{models}]=2^n(7/8)^{8n}=[2(7/8)^8]^n=o(1).
$$

Chvátal--Szemerédi (1988) establish exponential unrestricted shared-DAG **ordinary Resolution** hardness on this random family. Pang (arXiv:2610.00837v2, Theorems 1.1 and 7.2(a)) reports exponential DAG `Res(PC_r/F_p)` for fixed `r,p`; this is a 2026 preprint, and its rules exclude arbitrary conservative DEF extensions. Neither theorem covers all legal historical R_mix341 rules.

Mandatory comparison controls: cubic-expander odd Tseitin has 4h signed width-three clauses on 3h/2 edge variables and exponential ordinary Resolution hardness, but a **linear 4h-1-node** declared-semantic AND3/GF(2) mixed proof. Haken's ordinary PHP Resolution lower bound has Cook's polynomial Extended Resolution shortcut; Braun's bit-PHP Res(XOR) bound starts with width-2ell original clauses and is not transferred by equisatisfiable 3-CNF splitting alone. A known short proof is evidence about the true full minimum, never excluded.

## Theorem 456.1: min-UNSAT original source core > floor(n/59)

Let `mu(F)` be the smallest number of **distinct indexed source clauses** in any UNSAT subformula, and `k=floor(n/59)`. Then

$$
\Pr[\mu(F)\le k]=o(1).
$$

**Proof.** If a subformula of t<=k clauses is UNSAT, delete redundant clauses to obtain a minimally UNSAT subset. Tarsi's deficiency lemma states it has at most t-1 occurring variables. Thus for some 3<=r<=k, an r-variable set contains at least r+1 of the 8n sampled indexed clause positions. A fixed sampled position belongs to that variable set with probability

$$
p_r=\frac{\binom r3}{\binom n3}\le(r/n)^3.
$$

By independence of sampled *positions* and a union bound,

$$
\Pr[\mu(F)\le k]\le\sum_{r=3}^k\binom nr\binom{8n}{r+1}p_r^{r+1}.
$$

Retain the finite-population correction, absent in the preceding 1/60 proof:

$$
\binom nr\le(en/r)^r\exp\left(-\frac{r(r-1)}{2n}\right),
$$

by `binom(n,r)=n^r/r! prod_{j=0}^{r-1}(1-j/n)`, `log(1-u)<=-u`, and `r!>=(r/e)^r`. With `binom(8n,r+1)<=(8en/(r+1))^(r+1)`, each summand is bounded by

$$
8e(r/n)^2[8e^2(r/n)]^r\exp[-r(r-1)/(2n)]
\le 8e^{3/2}(r/n)^2 f(r/n)^r
$$

where `f(x)=8e^2 x exp(-x/2)`. The inequality drops an additional factor `(r/(r+1))^(r+1)<=1`, and uses `exp[r/(2n)]<=sqrt(e)`.

The function `f` increases on `(0,1/59]`. Exact **rational** arithmetic, not a floating-point threshold, proves

$$
f(1/59)=\frac{8e^2}{59}e^{-1/118}
<\frac{8(68/25)^2}{59}\left(1-\frac1{118}+\frac1{2\cdot118^2}\right)
=\frac{127682512}{128361875}<1.
$$

Here `e<68/25` follows from a factorial-series tail bounded by 7/4320 after degree five, and `e^{-u}<=1-u+u^2/2`. Let the exact rational bound be q<1. For r<=sqrt(n), `f(r/n)<=8e^2/sqrt(n)`, so the first part is o(1). For sqrt(n)<r<=n/59, at most n summands are each O(1)q^r, totaling O(n q^sqrt(n))=o(1). QED.

## Theorem 456.2: original all-rule work/span consequence

In **any sound, source-authenticated, conservative-DEF, at-most-binary-premise, unit-paid** refutation DAG with legal assumption scope and one false sink, let U be the distinct indexed source clauses in root ancestry, `s=|U|`, `q` the number of distinct paid inference nodes, and `d` the maximum paid-node dependency path length. If U were SAT, its model would extend over conservative definitions and sound inferences could not conclude false. Hence `s>=mu(F)`. Connected undirected ancestry on s+q nodes requires at least s+q-1 edges, but the q paid nodes have at most 2q incoming dependency edges, so `q>=s-1`. A depth-d binary-premise DAG has at most 2^d distinct source ancestors, **even with unlimited sharing**, hence `d>=ceil(log2 s)`.

Consequently, a.a.s. for this *published family* in the **declared historical semantic rules** (with no uncharged unbounded-fan-in jump):

$$
W_{R_{\mathrm{mix341}}}(F)\ge\lfloor n/59\rfloor,
\qquad
\operatorname{span}_{R_{\mathrm{mix341}}}(F)
\ge\lceil\log_2(\lfloor n/59\rfloor+1)\rceil.
$$

This minimizes over **all** legal shared proof DAGs, arbitrary best derivation/branch choice and lawful shortcuts, without charging discovery. Under original encoding N=O(n log n), it only gives `Omega(N/log N)` along the family, **not** superpolynomial work or a machine-time/space lower bound. No separate native SPLIT, DISCHARGE or weakening rule was invented.

## Finite independent reproducibility and costs

A Python generator instantiates two random published-model proper 3-CNFs (n=10, seed 113, 80 clauses; n=12, seed 36, 96 clauses). Exhaustive original assignments show both UNSAT with minimum falsified clause counts 3 and 4. Greedy deletion yields **inclusion-minimal, NOT globally minimum** source cores of 19 and 21 clauses; all 40 separate single-source deletions are SAT. Exact indexed source DIMACS SHA256 are `a7907e77116d53a939c18d8d0295a36c2fdc8d924023d0018e1b7fdc75ab3357` and `493b60390284a96d88d6dd28ee0136e8fc32d2493e60c295640792ecede8e485` (811 and 1006 bytes). An independently written JS verifier rechecks raw source bytes, indices, full assignments, 40 deletion witnesses, 5 forged-source and 6 malformed DIMACS rejections. **1599 checks passed**. Rational base verified with integer arithmetic. The finite samples are NOT certified individual instances of asymptotic restricted proof hardness.

Measured local Python generation 18.19s / 95,628 KiB peak RSS; fixture construction 18.05s / 96,008 KiB; JS verifier 0.10s / 33,144 KiB. Separate process maxima do not establish the *all-phase simultaneous* peak of any SAT solver. Search, parsing, failed deletions, source/index reads, caching, output, checking, recomputation, and publication must be charged for implemented upper bounds; they are intentionally excluded from the ideal logical minimum.

## Source audit and open obligations

Read Nov 2 governing handoff (historical commit 4e29ed7), issue #3, AGENTS.md/CODEX.md/skill, native /341 blob c87acd11, LSPV-3/443 and /457, LSPV-3/456, LSPV-5/394 and /367, LSPV-1/455, actual Grok `GROKPROOF/2026-11-06_0515_PROGRESS.md` and Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`. Inspected required `konard/p-vs-np/scripts/proof_status.json`, `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md`, kbr-/math-research, and openai/math code search. Primary Chvátal--Szemerédi, Pang, Urquhart, Braun, Haken, Cook, Tarsi literature was searched. Google-branded search interface unavailable; indexed search used. Native accepted-byte LOCAL/DEF/facet checker was **not run**. Root main.tex was left untouched because complete content preservation could not be established. No role, schedule, grammar or weight was modified.

**Remaining:** Beyond this *linear* floor, obtain a genuinely superpolynomial `Wbar_R(N)` invariant valid against every fixed historical mixed rule and legal shared branching DAG; and independently prove the noncircular **same-R B3** `SAT in P => Wbar_R polynomial`. Both OPEN, B1/B2 OPEN, P versus NP OPEN.

### Primary references

[1] Chvátal and Szemerédi, *Many hard examples for resolution*, JACM 35 (1988), 759-768, DOI 10.1145/48014.48016.
[2] Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (2026), unrefereed preprint.
[3] Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), 209-219.
[4] Haken, *The Intractability of Resolution*, TCS 39 (1985).
[5] Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8 (1976).
[6] Braun, *An Exponential Lower Bound for the Bit Pigeonhole Principle in Resolution over Parities*, arXiv:2609.23015v2 (2026).
[7] Tarsi's deficiency lemma, KTH Proof Complexity Lecture 4 (2011), Thm. 2.6.
