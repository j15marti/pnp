# Source audit: openai/ten-proofs permanent formula lower bound, and its ceiling for the SAT pipeline

2026-11-19, independent Claude scheduled routine (not a TMR owner; no TMR manuscript was edited).
P versus NP remains OPEN. Nothing in this report promotes any SAT lower bound.

## Source (pinned)

openai/ten-proofs, commit 94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6, file Permanent.lean (27,563 lines),
Lean leanprover/lean4:v4.32.0 + mathlib. formalization.yaml reports sorry_count 0 and axioms
{propext, Classical.choice, Quot.sound}. Comparator challenge ComparatorChallenges/C_PermanentFormulaLowerBound.lean
states the two target theorems. **Kernel build and Comparator check were NOT executed here** (no Lean toolchain
in this container; a mathlib build would far exceed the 30 s stage budget). I read the challenge statement and
the top-level proof skeleton (lines 27197-27560), not all 27k lines.

KNOWN THEOREM (formalized upstream, not kernel-checked by us). For n >= 32 and every division-free formula f over C
in the n^2 entries with eval f = per_n: n^4/(128 log2 n) <= variableLeaves f. With division (Valid formulas, no division
by zero), the constant is 192. Here N = n^2 input variables, so the bound is N^2/(64 log2 N).
Model: algebraic formulas (fan-out 1) over C computing per_n as a polynomial (not as a function on {0,1}^N); only
variable leaves are counted; constants are free.

Proof skeleton (as read). Take ell = clog2 n, m = n - 2 ell. Partition the n^2 entries into n * (n/(2 ell)) disjoint
"cyclic diagonal" blocks of 2 ell entries forming a matching. (i) Coefficient lemma: the coefficients of per_n viewed as
a polynomial in a matching block's variables have transcendence degree >= m^2 over C (needs m <= 2^ell, 2 ell < m).
(ii) Skeleton lemma: TD <= 4 * (leaves in block) - 2 (6 with division). (iii) Summation gives n^4 <= 32 (2 ell) leaves.
This is the Kalorkoti/Nechiporuk block method with blocks of size Theta(log n), instead of single variables
(Kalorkoti 1985 gave Omega(n^3) = N^{1.5}).

## Independent finite reproduction of step (i)  [COMPUTATIONAL]

experiments/claude/perm_block_td_20261119.py (SHA256 in commit), raw results/raw/claude/2026-11-19_perm_block_td.json.
For each subset S of the 2 ell marked matching entries, the coefficient P_S is the permanent of the matrix with rows and
columns of S deleted and the other marked entries zeroed. The Jacobian of {P_S} with respect to the unmarked variables,
at a random integer point, has rank mod p = 1000003 that is a SOUND lower bound on the TD over C
(rank mod p <= rank over Q <= generic rank; Jacobian criterion in characteristic 0). Gradients come from a vectorized Ryser
formula, validated against brute-force minor permanents for n = 3,4,5 (0 mismatches). Seeds 2026111901/2026111902.

| ell | m | n | coefficients 2^(2 ell) | lemma claims m^2 | certified rank | hypotheses of (i) |
|---|---|---|---|---|---|---|
| 2 | 3 | 7 | 16 | 9 | 16 | no |
| 2 | 4 | 8 | 16 | 16 | 16 | no |
| 3 | 7 | 13 | 64 | 49 | 64 | yes |
| 3 | 8 | 14 | 64 | 64 | 64 | yes |

Both seeds agree. All coefficients are algebraically independent in these cases: the TD saturates its trivial
ceiling 2^(2 ell). Finite evidence only; n >= 32 (2^10 coefficients, 32x32 permanents) was not tested.

## PROVED (elementary; mine; not independently reviewed): technique ceiling

Lemma. Let g be any multilinear polynomial in N variables. Any bound obtained as
sum_i TD_i / 4 over a partition of the variables into disjoint blocks B_i, with TD_i the coefficient transcendence degree
of g in block B_i, is at most N^2 / (4 floor(log2 N)) (for N >= 4).

Proof. g has at most 2^{|B_i|} coefficients as a polynomial in B_i, and they lie in C(other variables), so
TD_i <= min(2^{b_i}, N - b_i) <= min(2^{b_i}, N) with b_i = |B_i|. Hence sum_i TD_i <= sum_i b_i * h(b_i), where
h(b) = min(2^b, N)/b. For 1 <= b <= floor(log2 N), 2^b/b is nondecreasing for b >= 1 (2,2,8/3,...) so h(b) <= 2^L/L <= N/L with
L = floor(log2 N); for b > L, h(b) <= N/b < N/L. Summing, sum_i TD_i <= N * N/L. Divide by 4. QED.

Consequences. (a) The formalized N^2/(64 log2 N) bound is within a constant factor (asymptotically 16) of what this
method can ever give, for per or for ANY multilinear target, including arithmetizations of #3SAT. The finite table shows
the slack is in the counting/skeleton constants, not in step (i). (b) The method cannot reach N^{2+eps}, so it cannot give
superpolynomial algebraic formula bounds or touch VP vs VNP; same N^2/log N barrier as Boolean Nechiporuk.

## Candidate and falsifiers for the project's SAT pipeline

CANDIDATE examined: "the ten-proofs permanent bound supplies a load-bearing lower-bound link for an NP-complete SAT
problem in a TMR pipeline". Falsifiers checked:
F1 (ceiling) - FALSIFIES any superquadratic extension of the method: lemma above.
F2 (model/direction) - FALSIFIES direct Boolean transfer: a fast Boolean SAT or #SAT algorithm does not yield a small
algebraic formula over C for per_n (Valiant's projections go from per to other VNP families; Burgisser's transfer goes from
VP = VNP over finite fields to Boolean collapses, not from Boolean algorithms to C-formulas). No reduction in the required
direction is known.
F3 (field) - OPEN: whether step (i) holds in characteristic 2, where per = det and det has n^{O(log n)} formulas; any
Boolean-flavoured use would need it and would at best give a polynomial bound.
F4 (measure) - the result counts formula leaves only; it says nothing about circuits, branching programs, time or space,
so it does not touch the strict-C row-cover or DTISP (1.3407, 0.5) chains currently in issue #3.

Status: KNOWN THEOREM (upstream formalization, our kernel check UNEXECUTED) for the stated algebraic-formula model;
RESTRICTED/NOT TRANSFERABLE as a SAT lower-bound link. Integration point: TMR-1 Track C source-verification ledger
(formal statement pinned, axioms recorded) and TMR-5 ranked synthesis (as a hostile ceiling control for any
"block transcendence/rank" invariant proposed by TMR-2/TMR-4).

Gates. DISJ: NOT APPLICABLE (no communication model). Relativization: NOT APPLICABLE (fixed polynomial, no oracle
machines). Simultaneous DTISP: NOT APPLICABLE (no machine model; F4). Deterministic configuration counting:
NOT APPLICABLE. Algebraic natural proofs (Forbes-Shpilka-Volk; Grochow-Kumar-Saks-Saraf): not an obstacle at polynomial
size, and the ceiling lemma is a stronger, method-specific barrier. Algebrization: NOT APPLICABLE.

## Corpus survey this run

Linked Google Doc "Dual Proof Attempts for P = NP and P != NP" (62.6 kB): read the introduction, summary table, sections
2.1-2.2 in full and the synthesis/works-cited tail; sections 2.3-3.3 were read only by heading. It is a survey of
holographic, tensor-network, IPS, GCT and hardness-magnification breakdowns; no new executable construction for the
current strict-C chain. GitHub search: openai/ten-proofs (new to this repo; audited above), openai/lean-gym,
openai/NavierStokesAndEuler, google-deepmind/formal-conjectures (not yet audited; candidate next source for formalized
complexity conjecture statements). Searches for SAT/complexity code under google, google-deepmind returned no new
relevant repositories.

## One next lemma

Determine whether step (i) (block coefficient TD >= m^2 for matching blocks) holds over GF(2) or GF(p) for small p, with
the Jacobian criterion replaced by a characteristic-free algebraic-independence certificate; this decides whether the
method has any finite-field (and hence Burgisser-adjacent) content at all.
