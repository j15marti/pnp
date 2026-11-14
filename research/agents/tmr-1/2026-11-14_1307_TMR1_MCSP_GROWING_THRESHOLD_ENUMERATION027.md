# TMR-1/027: Growing-threshold MCSP upper bound on one physical work tape

**Pacific timestamp:** 2026-11-14 13:07 PST (America/Los_Angeles). **Owner:** TMR-1 Machine Model Lead. **Status:** PROVED/RESTRICTED elementary constructive upper bound, TMR-3/TMR-5 independent physical-model review OPEN. Finite testing COMPUTATIONAL. P versus NP OPEN.

## Preflight, original-work ledger and novelty

Read FIRST the 2026-11-14 MCSP five-agent directive (Git blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a), then the 2026-11-13 replacement directive, AGENTS.md, CODEX.md, the repository pnp-research skill, latest issue #3 through TMR-5/024, and all TMR handoffs. Root proof1.txt recovered completely (28,714 chars); proof2.txt (1,051,196 chars, original blob 930c5eeddafce656717f28055a7a9a755f44737c) and canonical main.tex (2,545,859 chars, blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34) recovered through Git blobs, not considered empty when the Contents API returned blank bodies.

| Original artifacts reviewed | Prior finding/status |
| --- | --- |
| research/agents/tmr-4/2026-11-14_1243_TMR4_LENGTH_BLIND_FIXED_GATE_COFACTOR028.md and original Python/raw | Fixed-gate length-blind streaming, restricted; cannot maintain newly admitted growing-gate candidates using only pruned flags |
| research/agents/tmr-5/2026-11-14_1259_TMR5_BOUNDED_ENVELOPE_REVIEW024.md and original Python/raw | Independent favorable constant-S envelope review; bounded varying thresholds, not unbounded s(n) |
| research/agents/tmr-2/2026-11-14_1221_TMR2_ODOMETER_CODE_CERTIFICATE027.md | Zero-gate O(N log N) one-tape decision, high YES query depth does not imply high computational processing cost |
| research/agents/tmr-1/2026-11-14_1200_TMR1_MCSP_GATE_SPECTRUM_RESOLUTION026.md; 2026-11-14_1010_TMR1_MCSP_EXACT_PADDING_EXPONENT_FIREWALL024.md | Earlier additive circuit-size shells, exact dummy padding, threshold mismatch |
| research/agents/tmr-3/2026-11-14_1228_TMR3_MCSP_MOBILE_HEADER_FUSION027.md | Annotated-source single-tape simulation and full-output-only buffering obstruction |
| research/agents/tmr-4/2026-11-14_1142_TMR4_GAPMCSP_AFFINE_KERNEL_CYLINDER027.md; research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex | Restricted fixed affine sketch collisions; no arbitrary decision lower bound |
| research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex; 2026-10-28_1326_CLAUDE_TPORT-0001.tex; 2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex; research/agents/lspv-2/2026-11-01_0515_LSPV-2_STREAMED_WALSH_OVERLAP297.tex; research/agents/mktp/2026-10-21_1810_RP_MKTP_FORK22.md | Historical restricted tape/portfolio/Walsh/MKTP controls; no arbitrary SAT model transfer |
| research/main/2026-10-18_ASYMPTOTIC_CONE5.md; research/agents/threshold-descent/2026-10-18_1204_THRES_ENTROPY1.tex | Previous padding exponent and circuit-description warnings |

**New to the recent MCSP team:** a quantitative upper-bound construction in the exact one-work-tape/one-way-input model for an **unbounded** gate threshold \(s(n)=\Theta(n/\log n)\), with explicit time exponent, instead of merely a fixed gate cap. This is elementary exhaustive circuit enumeration and is not claimed as a new discovery in complexity theory. It is not a lower bound.

## Circuit and machine definitions

Write \(n\) for Boolean arity, \(N=2^n\) for the complete explicit input truth-table length, and \(L\) for an independent succinct SAT encoding length. Gate basis: binary AND/OR, unary NOT, free constants, free input wires and fanout; all AND/OR/NOT gates are counted, including shared gates. Let \(CC_n(f)\) be minimum gate count. Ordinary exact MCSP[s] decides \(CC_n(f)\le s(n)\) on every complete table, not a promise version.

Use ONE fixed uniform finite-control deterministic machine for all n, with one **one-way read-only input tape**, exactly one **two-way read/write work tape**, a single work head and finite alphabet. No advance length header, second work tape, oracle, advice, unit-cost unbounded words or free random access. Charge every transition, input advance, scratch, tag, tape movement, rerun, preprocessing and malformed-input check. Reject lengths that are not positive powers of two, with a fixed convention for n=1.

## SLOWTHRESH30 theorem and proof

**Claim (PROVED/RESTRICTED symbolic construction, independent tape audit pending).** If \(s(n)\) is a nonnegative integer computable from n in time \(\operatorname{poly}(n+s(n))\) by a fixed finite routine, ordinary MCSP[s] is decidable on that machine within

$$
T(N)\le N\,D(n,s(n))\operatorname{poly}(n+s(n)+1)
         +N\operatorname{poly}(n+1),
$$

with \(O(N\operatorname{poly}(n+s(n)+1))\) visited writable cells, where

$$
D(n,s)=(s+1)(n+s+2)[3(n+s+2)^2]^s.
$$

In particular, for fixed rational \(\kappa>0\), let

$$
s_\kappa(n)=\left\lfloor\frac{\kappa n}{\lceil\log_2(n+1)\rceil}\right\rfloor,\qquad n\ge2.
$$

Then

$$
\boxed{T(N)\le N^{1+2\kappa+o(1)}}.
$$

For each fixed \(0<\kappa<0.005\), the SAME uniform machine lies in \(\mathrm{DTIME}_1[N^{1.01}]\); for computable \(s(n)=o(n/\log n)\), the analogous construction has \(T=N^{1+o(1)}\). All statements concern EXPLICIT full truth tables.

**Proof, with each interface charged.** First copy every one-way input symbol into an append-only record on the ONE work tape, storing its source bit plus a self-delimited binary index i. A single mobile binary counter next to the writing head generates the next index; copying, incrementing and formatting it on a finite alphabet takes a fixed polynomial in \(\log(i+2)\) moves per input bit. At the endmarker, calculate N from the counter, reject if N is not a power of two, and obtain n. This costs \(N\operatorname{poly}(n)\) transitions, uses \(O(Nn)\) tape cells, and never rewinds the read-only input.

Next enumerate all syntactic DAG circuits with 0 through s(n) gates, each gate chosen from NOT/AND/OR with predecessor pointers among at most n+s+2 wires, plus a selected output. The number of descriptions is at most D(n,s). For EACH candidate make a complete sequential pass over the stored indexed records. Evaluate the gate program on the record's binary assignment and compare with its saved input bit. Accept iff one candidate agrees at all N records. This proves correctness for BOTH decision labels on every source table, not merely an approximation promise.

A one-work-tape implementation of each pass carries the candidate description, gate registers and temporary binary index in a **mobile finite-alphabet scratch block** adjacent to the current source record. Moving a scratch block of \(m=O(n+s\log(n+s+2))\) cells past an immutable \(O(n)\)-cell source record, evaluating a circuit, and updating the comparison flag can all be compiled into a fixed finite-head routine using \(\operatorname{poly}(m+n)\) adjacent operations, preserving the source record. After each pass return to the list origin in \(O(N\operatorname{poly}(m+n))\) moves. Gate enumeration and construction are also charged. There are at most D candidates, so total time is \(N D\operatorname{poly}(n+s)+N\operatorname{poly}(n)\). This is an existence-level explicit compiler, not a compiled transition-table run. Its unspecified polynomial overhead is harmless for the exponent claimed when s=O(n/log n).

For \(s=\lfloor\kappa n/\lceil\log_2(n+1)\rceil\rfloor\), since \(\log_2(n+s+2)=(1+o(1))\log_2n\),

$$
\log_2D(n,s)=\log_2((s+1)(n+s+2))+
s(\log_2 3+2\log_2(n+s+2))
\le(2\kappa+o(1))n.
$$

Every polynomial in n+s is \(2^{o(n)}\). With \(N=2^n\) the stated \(N^{1+2\kappa+o(1)}\) follows. The strict inequality \(2\kappa<0.01\) absorbs all asymptotic slack for an \(N^{1.01}\) bound. No practical crossover n or exact low-order constants are asserted. The method may use \(O(N\log N)\) work cells and does not give a poly(s)-space update algorithm.

## Primary-source theorem matrix and separation firewall

| Source and exact statement | Model and input measure, hypotheses and conclusion | Current gap |
| --- | --- | --- |
| CHMY, STACS 2021, Theorem 1, p23:3 [1] | Ordinary exact decision MCSP[\(2^{\mu_1n}\)] on full N=2^n bits; deterministic one-way input + exactly one two-way work tape; nonmembership in \(\mathrm{DTIME}_1[N^{1.01}]\) for some sufficiently small fixed \(\mu_1>0\) implies \(P\ne NP\) | This premise is OPEN; our s(n) is dramatically smaller than \(N^{\mu_1}\) |
| CHMY, Theorem 2, p23:3 [1] | Randomized two-sided error, same input/tape interface, ordinary MCSP[\(2^{\mu_2n}\)] at a distinct larger \(\mu_2>\mu_1\): unconditional nonmembership in \(\mathrm{BPTIME}_1[N^{1.99}]\) | Stronger exponent at wrong circuit-size threshold |
| CHMY, Theorem 3, p23:4 [1] | Restricted short \(N^{o(1)}\)-length oracle-query computation at \(\mu>1/2\) | Does not exclude every oracle/query model |
| McKay-Murray-Williams, STOC 2019, Thm. 1.2/1.3, p2 [2] | **Search**-MCSP of A-oracle circuits, time-constructible \(s(n)\ge n\); \(\Sigma_3SAT^A\) oracle of query length \(\widetilde O(s)\), \(\widetilde O(s^2)\) streaming update, \(\widetilde O(s)\) space. Under specified no-poly(s) streaming premise, \(P\ne NP\) | This construction is ordinary **decision**, stores \(N\) bits, and has no oracle; cannot be substituted for search streaming |
| Oliveira-Pich-Santhanam, CCC 2019 [3]; Atserias-Müller arXiv:2503.24061v2 Thm.27 [4] | Different approximation promises and circuit models; the Atserias-Müller P-uniform premise concludes \(P\ne NP^{\oplus P}\) | No ordinary MCSP/GAP/MKTP or nonuniform transfer is asserted |

The TMR-1 result is a **counterexample** to claims that every positive unbounded gate threshold already requires superlinear exponent 1.01 on one work tape, but does not affect CHMY's power-of-N threshold. The known CHMY high-threshold lower bound and hypothetical charge-sound both-label threshold reduction remain separate. Required high-to-low map [OPEN] -> matching small-\(\mu\) lower bound [OPEN] -> separation [CONDITIONAL]. Ordinary MCSP NP-completeness is not assumed. There is no SAT solver here: a concise L-bit CNF does NOT give its \(N=2^n\) truth table for free.

## Reproducible finite evidence, hostile controls and next target

**Executed native CPython**, script experiments/tmr/tmr1_slowthreshold030.py, SHA256 03e7554f228d4654eeec71d91072f56c4ecdb7b32f9b242424fa211a9401c4fd, with seed 20261114. Raw JSON results/raw/tmr/2026-11-14_1307_TMR1_SLOWTHRESH030_RAW.json, SHA256 f13b7809c330e067ce0fe4dd8dd266b8981d3588e6b6a324627f53e791dcc855. Checked all 828 n=1,2,3 full-table/threshold combinations for s=0,1,2, nine independently expected exact circuit function-count controls, 36 malformed lengths and ten finite count-bound checks: **884 assertions, zero failures**. At n=3 the distinct circuit functions for s=0/1/2 were 5/14/40. The test is a semantic indexed-record proxy, NOT a native one-head tape execution. The symbolic proof, not these finite tests, establishes the asymptotic statement.

Free constants, projections, NOT/AND/OR, gate sharing, all n<=3 tables, malformed lengths, counter/index tags and source rereading restrictions were addressed. Other SAT controls (Horn, 2-SAT, XOR/Gaussian elimination, bounded-treewidth DP, products, sharing, renaming, padding, auxiliary variables, cache/recompute) remain permitted unrestricted-machine escape strategies, not tested as alleged hard SAT families.

**Peer request:** TMR-3 and TMR-5 audit the concrete one-physical-tape mobile block, in particular preserving every indexed record and the EOF test; TMR-2 audit the query/processing distinction; TMR-4 test dynamic unbounded cofactor flags versus this stored-input baseline. TMR-1 next pursue a genuinely resource-preserving \(s=N^\mu\) threshold bridge rather than treating a tiny-s upper bound as magnification progress.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex unchanged under TMR-5 ownership. No schedules modified. P versus NP OPEN.

## References

[1] Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Theorems 1–3, pp.23:3–23:4. https://doi.org/10.4230/LIPIcs.STACS.2021.23

[2] McKay, Murray, Williams, STOC 2019, Theorems 1.2–1.3, p.2. https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf

[3] Oliveira, Pich, Santhanam, CCC 2019. https://doi.org/10.4230/LIPIcs.CCC.2019.27

[4] Atserias, Müller, arXiv:2503.24061v2 (2025). https://arxiv.org/abs/2503.24061
