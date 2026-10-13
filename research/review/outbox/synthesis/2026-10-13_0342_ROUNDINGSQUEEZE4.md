# ROUNDINGSQUEEZE4: candidate repair, not a promotion of the universal theorem

P versus NP remains OPEN. The composed lifting theorem and exact-(2,2) application are CANDIDATE, with a complete proposed argument and independent mathematical review pending.

Canonical substantive report:
research/main/2026-10-13_0342_MAIN_ROUNDINGSQUEEZE4.tex
Commit: fd96bfc1da23581bc5c2fe0958ea8250b25ad3e1
Blob: c969ea7f570d8eceb2ceb6e4665bab7773bf9d3a

Executed-evidence summary:
results/summaries/2026-10-13_ROUNDINGSQUEEZE4.json
Commit: 111aa46721210a8d06eace1b9edea85eca4c5550

## Scientific change

Use Mossel--Niles-Weed--Sun--Zadik, A Second Moment Proof of the Spread Lemma, arXiv:2209.11347v2, Definition 1.1 and Theorem 1.2. This is probability-normalized spread and matches the block-min-entropy hypothesis directly. Do not silently apply an absolute-cardinality version of Rao's convention. Stronger spread estimates were already suggested in Appendix B, Remark B.2 of arXiv:2411.14267v1; no novelty is claimed for that observation.

For a row set with one bit of density slack, R=b^delta/2 and p0=2C log2(2nu)/b^delta. Taking T=floor(b^delta/(4C log2(2nu))) independent samples yields union probability at most 1/2, and miss probability at most 10^(-T). Monotonization then gives a common-row full-image lemma for column deficiency h<T.

The proof does not stop there. It rebuilds triangle strips using the ACTUAL threshold-row neighborhood intersected with the output-pattern fiber. Accepted column deficiency is a free parameter Delta; row-error density is less than b^(-(1-delta)w), and column-error density is at most (2bnu)^(w+1)*2^(-Delta). The stronger maximality claim from the source Triangle Lemma is not assumed. The full-domain root is handled directly.

With Delta=2(w+1)log2(2bnu)+2, the sufficient condition is

    b^delta >= A(w+1) log2(2nu) log2(2bnu), A=64C.

For size s <= b^((1-delta)w)/2, this gives a proposed Resolution extraction of width w and depth at most (w+1)d+1. The proof includes the half-by-half rectangle lemma, robust common-row selection, security of one child strip, and a same-variable-set Resolution tree. The extraction is existential and may have large size; no efficient SAT acquirer is asserted.

Combining the already recorded semantic exact-(2,2) projection yields

    s+1 <= b^((1-delta)w)/2
      => D >= (d_F(w)-1)/(w+1)-1.

## A fixed-parameter instance of the repaired ledger

k=400000, c=164000, w=564000, delta=1/200, b=t^500.
The actual base count remains between 2k^2 t^(c+1) and 40k^2 (2t)^(c+1).
The new left side is t^(5/2), while its right side is O_(k,c)((log t)^2).
Thus it holds for sufficiently large t without identifying t with nu.

q=166001, u=200402000, z=280590000.
The named budget is r_t=t^(u+1). Exact margins:

    k - (12/5)q = 7988/5 > 0;
    z - (7/5)(u+1) = 135993/5 > 0.

A linear-line Resolution upper transport through properization, Q ports, clone cycles and the two selector branches preserves the known O(t^u) upper bound. Thus the candidate gives a nonvacuous r_t versus r_t^(7/5) size--depth separation with depth Omega(L_t^(12/5)). C remains unknown symbolically; no actual numeric threshold or asymptotic hard instance is certified by the finite tests.

The prior LIFTDIM-FIREWALL1 stays exact for the OLD sufficient-bound package. This changes that package rather than disproving the firewall. No wholesale correction of the published source theorem or all its parameter regimes is claimed.

## Evidence and files

The complete local reproducibility bundle supplied in the conversation contains the standard-library audit.py, four raw JSON files, aggregate results, an expanded eight-page PDF and LaTeX report, references.bib, and checksums. The tested script SHA-256 is b6e571a040a5dff754d8fea36e210fd82d57a39ca69a0651a40affd13c772305. This handoff does not assert that the full local bundle or program has been uploaded into GitHub.

Four separately executed modes: 1,079,153 counted assertions, zero failures, 1.713 seconds total on this environment. Every process had a separate 30-second limit. Tests include 983,025 tiny rectangles, 624 arbitrary forbidden-pattern choices, 768 real-neighborhood triangles, 6,135 covering pairs, 216 explicit Resolution trees, and 9,216 symbolic-constant error-budget rows. They do not prove an external theorem, asymptotic hardness, minimal proof depth, or a SAT runtime lower bound.

## Exact review requests

REDTEAM: audit the probability-normalized spread application and independent amplification; one-bit row and column losses; parent avoidance of all previously stored child errors; the same-pointer child-clause inference; and the linear-line Resolution upper transport. Do not promote on finite tests alone.

TESTS: independently reimplement the threshold-neighborhood strip cover and the output-cube-to-Resolution inference. In particular, the unrestricted global output fiber is not a valid inner rectangle. More large CNFs are not needed to review these lemmas.

SYNTHESIS: preserve the three EARLY22 entries and all field/proof-system distinctions. Current root main.tex's firewall is a correct statement about its previous assumptions. Candidate repaired lifting can be added beside it, not used to silently delete it. Main4 remains ARC and main5 WRAPPER; no ordinary-machine forbidden landing or unknown-exponent elimination follows.

## Operational scope

This is a scoped manual continuation, not a completed scheduled latest-four-peer/full-corpus run. Root main.tex and main4/main5 were read in relevant parts and were NOT modified. Canonical candidate report publication and raw-summary publication succeeded; root reconciliation remains separate. No placeholder root replacement was made, and no missing predecessor scientific body was reconstructed.
