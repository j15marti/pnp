# Claude hourly routine: roABP width of an explicit IPS_LIN' certificate for random UNSAT 3-CNF

Run: 2026-11-19 ~07:20-08:00 UTC (scheduled routine; not one of the five TMR identities). Branch `ccr-8d8a5ce7-6ignvf`,
base `origin/main` 32dfff68 merged with predecessor routine branch `ccr-8d8a5ce7-39wor1` (8154bcc6).
No TMR manuscript edited (AGENTS.md ownership). Retired trackers proof*.txt not read. P versus NP remains OPEN.

## 0. Source check

The Google Doc `1b2SYjJJ...` ("P vs. NP Proof Attempts") has modifiedTime 2026-11-02T17:46:59Z, so it has not changed since the predecessor
audit (`research/agents/claude/2026-11-19_0712_CLAUDE_GDOC_RANK_CLAIM_AUDIT.md`, on branch 39wor1). That audit was not repeated.
New OpenAI/Google GitHub search hit: `openai/math` `lean/ComparatorChallenges/SubexponentialSAT.{lean,json}`, which has challenge theorem
`OAI.Algorithms.SubexponentialSAT.SqrtLogSpace.exact_count_and_sat` with supporting modules `Sparsify.lean`, `Sunflower.lean`, `Encoding.lean` and
`SubexpDenseRowTableBound.lean`. These are formalized SAT/#SAT **upper bounds** (sparsification-style). They are possibly relevant to TMR-1 as a pinned formal
algorithm statement, but they give no lower bound. The file contents could not be read (`gh api repos/openai/math/contents` returned 403, because the repo is
outside the session scope). The exact statement is UNVERIFIED. The google-deepmind/google-research searches for "proof complexity", roABP and
"ideal proof system" returned nothing new.

## 1. Dependency advanced

This run takes the next lemma named by the predecessor run (its section 7): does the full-rank (2^{n/2}) functional bound for one aggregated axiom 1/f
transfer to roABP-IPS_LIN' refutations of CNFs? This is the load-bearing arrow in the doc's route IIB (IPS functional lower bounds for SAT).

Model: the CNF F = C_1..C_m on x in {0,1}^n, with clause axioms f_j(x) = prod over literals of [literal false] (multilinear). The certificate is
P(x,y) = sum_j g_j(x) y_j with multilinear g_j and sum_j g_j f_j = 1 on the cube (IPS_LIN' modulo the Boolean axioms). roABP variable order is x_pi(1..n)
then y_1..y_m. By Nisan's characterization (KNOWN THEOREM), the minimum roABP width at the x-cut k equals the rank of the coefficient matrix. For
multilinear polynomials this equals the rank over Q of the cube evaluation matrix M_k[a,(b,j)] = g_j(a,b). Widths at the y-cuts are <= m+1.

Candidate tested: the explicit certificate g_j = [C_j is the first falsified clause] (clause order fixed).

Falsifiers stated before running:
- F1: the width is >= 2^{n/2} (as large as the single-axiom 1/f bound) for every order tried, which would support transfer.
- F2: the width is far below 2^{n/2} for some natural order, so transfer is not automatic.
- F3: a provable exponential upper bound on this certificate exists that does not reflect its actual rank (bound vs. rank gap).

## 2. Evidence (COMPUTATIONAL, finite n; exact ranks)

Instances are uniform random 3-CNF with m = round(6n) clauses (rng = numpy default_rng(10000 n + seed)). Every reported instance was checked UNSAT by full
enumeration; SAT draws were skipped and recorded (n=20 seed 0, n=22 seed 2). The rank is computed mod p = 2^31-1 on the integer Gram matrix (a lower bound on
rank over Q) and cross-checked by float rank. The two agreed in every case.

Stage A: `experiments/claude/cnf_ipslin_roabp_width.py`, raw `results/raw/2026-11-19_CLAUDE_IPSLIN_ROABP_WIDTH_raw.json`, 274 s total (each instance < 60 s).
This covers all x-cuts for n = 8..18, seeds 0-2, natural and BFS variable orders, with given and sorted-by-last-variable clause orders.
- Given (random) clause order: the max width exceeds 2^{n/2} at n=8..14 and is near 2^{n/2} at n = 16-18 (n=18: 296-693 vs 512).
- Sorted clause order: max width 14-35 for n <= 12, 34-45 at n=14, 40-53 at n=16 and 40-81 at n=18 (against 512).

Stage B: `experiments/claude/cnf_ipslin_residual_scaling.py`, raw `..._RESIDUAL_SCALING_raw.json`, 25 s. It proves an exact decomposition bound (PROVED,
elementary). For the sorted order, all prefix-internal clauses precede the crossing clauses. A prefix that falsifies an internal clause therefore has a
constant row, while a surviving prefix's row is determined by its residual set of unsatisfied crossing clauses. So W_k <= i_k + S_k. At the middle cut,
S_k grows exponentially (ratio 6: about 90 at n=16 and 7.7e3 to 7.1e4 at n=40; ratio 4.26: up to 2.1e5 at n=40).

Stage C: `experiments/claude/cnf_ipslin_midcut_rank.py`, raw `..._MIDCUT_RANK_raw.json`, 77 s. This gives the exact rank at the middle cuts with the sorted
order:

| n | 2^{n/2} | middle-cut rank (seeds) | distinct rows |
|---|---|---|---|
| 16 | 256 | 49, 46, 36 | 52, 54, 37 |
| 18 | 512 | 35, 76, 48 | 38, 117, 67 |
| 20 | 1024 | 55, 90, 42 | 67, 135, 55 |
| 22 | 2048 | 63, 73, 150 | 88, 110, 262 |
| 24 | 4096 | 101, 96, 55, 83 | 149, 147, 70, 120 |

Stage A's raw file was produced before a cosmetic `if __name__ == "__main__"` guard was added; the computation is unchanged.

## 3. Conclusions

COMPUTATIONAL (n <= 24, ratio 6): F2 holds. Clause order matters a lot. With clauses sorted by last variable, the explicit first-falsified certificate
has roABP width 36-150 (about 0.3-1.1 m) at the middle cut. That is 10-40x below the 2^{n/2} that the single-axiom 1/f functional bound forces. The
aggregated full-rank bound therefore does **not** transfer to CNF refutations by aggregation in this range, which sharpens the predecessor's F3. The
widths grow slowly but do not decide asymptotics.

F3 holds: the provable upper bound i_k + S_k is exponential while the measured rank is far smaller, so neither the bound nor the number of distinct
subfunctions is evidence of an exponential width lower bound.

OPEN: (i) the asymptotic growth of this certificate's width; (ii) the minimum over **all** certificates and orders. That minimum is the actual
roABP-IPS_LIN' refutation size question for random 3-CNF. Any lower bound must hold for every certificate, and none is computed here. Before any claim,
check the literature: Forbes-Shpilka-Tzameret-Wigderson (roABP-IPS functional lower bounds, subset-sum axioms), Govindasamy-Hakoniemi-Tzameret,
Hakoniemi-Limaye-Tzameret 2024 (lifting toward CNF lower bounds). Whether roABP-IPS CNF lower bounds for random 3-CNF are known was not verified this run.

Gates for the candidate "width of the first-falsified certificate is a SAT lower bound". DISJ: NOT APPLICABLE as stated (this is a proof-size measure,
not an algorithm bound). Relativization: NOT APPLICABLE (a static algebraic proof system). Simultaneous DTISP: NOT APPLICABLE. Deterministic
configuration counting: NOT APPLICABLE. No runtime claim is made from rank (AGENTS.md). Even a 2^{Omega(n)} roABP-IPS lower bound would be a
proof-complexity result in a restricted system, not a SAT time lower bound.

## 4. Next load-bearing lemma

Find a computable **lower bound** valid for all IPS_LIN' certificates at a fixed cut. A candidate: for each prefix a, the restriction F|_a is a CNF on
the suffix, and any certificate restricts to a certificate of F|_a. A rank lower bound should therefore follow from the number of linearly independent
"residual refutation spaces" {(g_j(a,.))_j : sum_j g_j(a,.) f_j(a,.) = 1}, which are affine spaces. Bound from below the minimum rank of a choice of one
point per affine space (a min-rank completion problem) on small n, and compare with the 36-150 upper bounds above.

Validation actually run: the three scripts above. No independent review. No manuscript or peer file was modified.
