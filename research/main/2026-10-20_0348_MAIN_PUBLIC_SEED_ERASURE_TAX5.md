# PUBLIC-SEED-ERASURE-TAX5 | 2026-10-20 03:48 Asia/Seoul

**Result.** The latest threshold and red-team artifacts combine into an exact semantic/resource no-go for the modified public-seed, fixed-port CHMY-like construction. Masking that suppresses source exposure to probability `alpha` forces independent semantic recovery to use `Omega(1/alpha)` copies. Thus making exposure polynomially small creates a polynomial output/time tax unless a new compressed joint target theorem is supplied. This retires redundant fixed-port source injection as an exponent-improving mechanism; it does not attack the original CHMY generator or close ordinary-MKTP totalization. **P versus NP remains OPEN.**

## 1. Recovered state

Read the verified governance, `main2.tex` through `main5.tex`, Compact-History records, fallback Doc, `SHORT-QUERY-QUARANTINE3`, `AMPLIFY-FIX-SELECTOR4`, and new exact artifacts:

- **MCSP / MULTIPORT-MASK-FLOOR3:** for the modified recurrence with the same source XORed into a fixed set of additive ports, source exposure is within a factor two of the latest-port survival probability. Repeating fixed ports cannot buy an additional exponential erasure factor. Exhaustive audit: 1,013 port sets, 348,502 mask states, 377,626 recurrence/frontier assertions, plus 2,100 affine fast-forward checks; zero failures.
- **ARC / COMPACT-HISTORY-GATE1:** the conditional recurrence `t'<=max{r,a+g+lambda t}`, `s'<=max{eta,lambda s}` requires `r<=11/10`, `a+g<=3/5`, `lambda<=1/2`, `eta<=1/2` for the proposed `(6/5,1/2)` fixed point. No all-input iterable contractor establishes them. Compact-witness search has an unknown polynomial exponent.
- **REDTEAM22:** exact public-seed joint-output TV values `1/16,1/8,1/16,3/16,3/16` for five tested port sets, each too small for one-copy two-sided `2/3` classification. The model is explicitly a modified recursion, not original CHMY.
- No newer verified universal-solver body was found; the last established status remains that certified fastest-program racing preserves an unknown competitor exponent.

Root `main.tex` now has blob `526ab047415edafd6dbcb50cebc9b4fd630be710` and still contains a literal “Full content continues” placeholder. It was not edited.

## 2. Falsifiable integrations proposed before source search

1. **Exact public-seed TV identity.** For a deterministic public-seed transformation, joint source-pair TV equals the probability that the two outputs differ. Falsifier: hidden private randomness, nonidentical seed measures, or a nondeterministic target map.
2. **Erasure-amplification tax.** Independent copies with one-copy exposure `alpha` have TV exactly `1-(1-alpha)^r`; two-sided `2/3` recovery therefore needs `r=Omega(1/alpha)`. Falsifier: a coupled/compressed target carrying more information than the listed copies.
3. **Descent cancellation test.** If masking obtains `alpha=N^{-kappa}`, explicitly serializing the necessary copies costs `Omega(N^kappa)` target blocks, which must be charged before importing any one-tape or FLMV endpoint. Falsifier: construct one ordinary total target instance of sub-repetition length with a proved witness-preserving decoder.

## 3. Primary-source model check

- CHMY proves a nearly quadratic randomized lower bound at a fixed large MCSP threshold on a one-way read-only input plus one-work-tape model. The modified public-source ports analyzed here are not part of that theorem. Primary: <https://doi.org/10.4230/LIPIcs.STACS.2021.23> and <https://eccc.weizmann.ac.il/report/2020/103/>.
- OPS concerns nonuniform GapMCSP/GapMKtP circuit magnification with quantified small thresholds, not public-seed TV recovery. Primary: <https://theoryofcomputing.org/articles/v017a011/>.
- MMW's MKTP streaming result uses short `Sigma_3 SAT` queries; it does not supply the missing SAT-to-total-MKTP construction. Primary: <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>.
- FLMV is a deterministic random-access time-space lower bound. Serialized repeated outputs, seed generation, and live state must be present in the same machine ledger. Primary: <https://pages.cs.wisc.edu/~dieter/Research/sat-ts.html>.
- Ilango remains random-oracle-relative and therefore does not fill this deterministic public-seed interface. Primary: <https://doi.org/10.1137/24M1652568>.

## 4. New theorem: public-seed erasure tax

Let `Z` be public randomness with the same distribution for two source strings `f0,f1`. Let `Phi_Z` be deterministic after `Z` is fixed, and define

`P_b = distribution of (Z,Phi_Z(f_b))`, for `b in {0,1}`.

Put `alpha=Pr_Z[Phi_Z(f0) != Phi_Z(f1)]`.

**Theorem 1 (exact TV identity).** `TV(P_0,P_1)=alpha`.

**Proof.** Conditioned on each public seed `z`, both distributions put their equal mass on one point. If the outputs coincide, their conditional contribution to TV is zero; if they differ, it is the full seed mass. Summing over seeds gives exactly `alpha`. QED.

For `r` independent copies, the same argument gives

`TV(P_0^r,P_1^r)=1-(1-alpha)^r <= r alpha`.

Any classifier whose error on each source is at most `1/3` has equal-prior average error at most `1/3`. The optimal equal-prior error is `(1-TV)/2`, so necessarily `TV>=1/3`. Hence

`1-(1-alpha)^r >= 1/3`.

In particular, `r alpha>=1/3`, and more exactly

`r >= ceil(log(2/3)/log(1-alpha))`.

This is an information statement about the declared public-seed outputs, not an unrestricted runtime lower bound.

## 5. Applying MULTIPORT-MASK-FLOOR3

In the modified fixed-port recursion,

`Phi_Z(f)=B_Z XOR (Q_J(Z) AND f)`.

For `Delta=f0 XOR f1` supported on `S`, Theorem 1 gives

`alpha=Pr_Z[Q_J(Z) AND Delta != 0] <= |S| p^t`,

where `t` is the number of masks following the latest source port and every relevant layer marginal is at most `p`. Therefore any independent-copy recovery with both source errors at most `1/3` must satisfy

`1-(1-|S|p^t)^r >= 1/3`

whenever `|S|p^t<1`.

For unbiased masks, choose a constant-density support `|S|=delta N`. Circuit counting supplies some truth table supported on `S` with circuit complexity above `N^mu` for every fixed `mu<1`, while `f0=0` is a source YES instance. If `t=(1+kappa)log_2 N`, then

`alpha <= delta N^{-kappa}` and `r=Omega(N^kappa)`.

Thus deeper public masking cannot simultaneously claim polynomial source erasure and free constant-copy semantic recovery. A route may still survive by constructing a compact single target that combines the copies, but that requires a new ordinary-target encoding, witness projection/extension, and charged decoder theorem.

## 6. Exact audit

`experiments/review/2026-10-20_public_seed_erasure_tax_audit.py` used exact fractions. REDTEAM22's five one-copy TV values require respectively `7,4,7,2,2` independent copies merely to reach TV `1/3`. For the control `delta=1/8`, `N=64`, the upper bounds `alpha<=1/(8N^kappa)` require at least 208 copies for `kappa=1` and 13,287 for `kappa=2`. Thirty-nine exact minimality and union-bound assertions passed with zero failures. Raw: `results/raw/synthesis/2026-10-20_0348_PUBLIC_SEED_ERASURE_TAX5.json`.

Finite checks validate arithmetic only. The TV and repetition statements are proved symbolically above.

## 7. Proof DAG

| Status | Arrow |
|---|---|
| ESTABLISHED | MULTIPORT-MASK-FLOOR3 in its modified fixed-port independent-layer model; exact public-seed TV identity and erasure tax; MMW short-query streamer; FLMV matched deterministic endpoint. |
| COMPUTATIONAL | 39 new exact TV/repetition controls; predecessor 1,013 port-set and 163,840 REDTEAM22 identity checks, zero failures. |
| CONDITIONAL | A source-combining total target could evade explicit repetition only if its encoding, witness semantics, construction, and decoding are proved and fully charged. ARC recurrence enters its fixed point only under the stated unbuilt contractor inequalities. |
| CANDIDATE | Uniform charged `R_k` to ordinary MKTP/KT followed by short-query inlining; or a genuine CHMY source-specific critical-band construction using the original private generator. |
| OPEN | Ordinary totalization; standard-model Ilango replacement; source-monochromatic semantics; vanishing parameter; compressed repetition target; all-input ARC successor. |
| RETIRED | Redundant fixed additive ports as an extra exponential erasure mechanism; public-seed single-copy classification below TV `1/3`; black-box history hardness transferred to explicit affine transitions. |

**Weakest arrow:** unchanged—uniform, total, fully charged `R_k`. The new result is valuable because it removes a tempting but quantitatively self-canceling CHMY repair.

## 8. Role handoff

- **MCSP:** stop adding the same source to more fixed public ports. Attack the remaining critical band only through the original generator's actual private randomness/two-coordinate properties, or build a compressed ordinary target for repetitions.
- **Universal Solver:** price a selector/compressor acting on `r` copies. Report target length, proof search, unknown exponent, output time, workspace, and every full-source call.
- **ARC:** insert the `r=Omega(1/alpha)` acquisition/output tax into `a,g,r,eta,lambda`; reject a contractor if repetitions destroy `a+g<=3/5` or output materialization violates space.
- **Red team:** test coupled seeds, adaptive port choice, nonlinear source embeddings, and compact joint-target claims. Preserve the private-generator distinction.
- **Synthesis:** promote no CHMY descent unless both promises and the serialized/compressed repetition ledger survive in the source theorem's machine model.

The two-route allocation remains unchanged. Compact History remains a diagnostic. **P versus NP remains OPEN.**

END_OF_VERIFIED_MAIN::PUBLIC_SEED_ERASURE_TAX5::P_VS_NP_OPEN
