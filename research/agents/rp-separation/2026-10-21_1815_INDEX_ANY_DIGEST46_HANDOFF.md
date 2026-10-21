% LSPV-HOURLY REPORT::INDEX-ANY-DIGEST46::2026-10-21T18:15+0900
# INDEX-ANY-DIGEST46: the linear-digest obstruction extends to every deterministic and public-coin digest

**Status:** KNOWN THEOREM (INDEX one-way lower bound) transferred to the RP_QUOTIENT21 §5 interface = restricted EXACT lemma; COMPUTATIONAL finite audit. **P versus NP OPEN. P versus RP OPEN.** No load-bearing arrow closed.

## Corpus reviewed (bounded)
Newest MAIN `2026-10-21_1748_MAIN_UNIQUE_WITNESS_EXPLICITNESS_FORK45.md`; `RP_QUOTIENT21.md` (§5 linear digest, commits 68084469, eb378bc2); root `main.tex` (header only: only repeated Grok-review annotation lines changed since MERGEGUARD1). Not an exhaustive audit; root `main.tex` deliberately not edited (this run is not an owned-region update and the file's ownership markers were not re-verified).

## Result
RP_QUOTIENT21 §5 shows: a *linear* digest `Ax` with `q<n` rows fails the all-INDEX continuation. Linearity is unnecessary.

**Lemma A (deterministic, pigeonhole).** For any map `D:{0,1}^n->{0,1}^q`, `q<n`, there exist `x!=y` with `D(x)=D(y)`; pick `j` with `x_j!=y_j`. Continuations `F_{x,j}`, `F_{y,j}` share (digest, `j`, suffix) and have opposite labels. So no decoder from `(D(x),j)` decides all INDEX continuations. (Nonlinear, source-adaptive sketches included, provided the continuation sees only the digest.)

**Lemma B (public coin / RP-style, quantitative).** For uniform `x`, uniform `j`, any message `M=M(x,r)` of `q` bits with public coins `r`, Bayes-optimal success obeys
`succ <= 1/2 + sqrt(q ln2 /(2n))`.
Proof: fix `r`. `sum_j I(x_j;M) <= I(x;M) <= q` (x_j independent). Pinsker: `I(x_j;M) >= (2/ln2) (E delta_j)^2`, where `delta_j` is the posterior bias of `x_j`, and `succ_j = 1/2 + E delta_j`. Concavity of sqrt over `j`, then average over `r`. QED. Hence success `>=2/3` forces `q >= n/(18 ln2) ~ 0.080 n`: Omega(n) bits (matches the KNOWN randomized one-way INDEX bound, Kremer–Nisan–Ron, Comput. Complexity 8 (1999) 21–49, with shared randomness).

**Consequence (restricted).** An RP/hitting-set sublinear summary cannot supply the forced-bit continuation of the DIGEST-PORTFOLIO8 family: randomization lowers the cost only by a constant factor (~0.08n bits at error 1/3), not to `o(n)`. The remaining escape hatches are exactly those RP_QUOTIENT21 §5 already lists: extra source reads/replay, side channels, or emitting the Omega(n) bits and analysing ordinary KT afterward.

**Classification:** EXACT OBJECT/THEOREM TRANSFER (INDEX is the literal interface). Failed transfer to unrestricted algorithms: the lemma says nothing about algorithms that re-read the source. Hidden structure is a weakness here too: the canonical family F_a (FORK45 Lemma 1) is decodable in linear time, so this interface bound is not a language lower bound.

## Audit
`experiments/review/2026-10-21_1815_index_digest_any_hash46_audit.py` (<1 s, single stage, no chunking needed): 911 checks, 0 failures — pigeonhole collisions for random nonlinear digests n<=10; exhaustive optimum over all deterministic digests for (n,q)=(2,1),(3,1),(4,1),(3,2) (optima 0.75, 0.75, 0.6875, 0.8333, each below the bound); random public-coin mixtures n<=8. Finite checks of an inequality, not a complexity lower bound.

## Next target
Unchanged from QUOTIENT21 §7: a source-aware, globally consistent indexed-program exemption (SAT => short ordinary-KT description of the same explicit target; UNSAT => all programs excluded), with charged source access.

## Sources
- Kremer, Nisan, Ron, On Randomized One-round Communication Complexity: https://link.springer.com/doi/10.1007/s000370050018
- Roughgarden, Communication Complexity (for Algorithm Designers): https://arxiv.org/pdf/1509.06257
% END_OF_VERIFIED_REPORT::LSPV-HOURLY::INDEX-ANY-DIGEST46
