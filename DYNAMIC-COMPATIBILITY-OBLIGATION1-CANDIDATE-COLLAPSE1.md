DYNAMIC-COMPATIBILITY-OBLIGATION1-CANDIDATE-COLLAPSE1

**Research date:** 26 November 2026, America/Los_Angeles  
**Named dependency:** CHARGED-UNSAT-TRANSPORT1, DYNAMIC-COMPATIBILITY-OBLIGATION1  
**Status:** Candidate obligation collapses. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN. P vs NP OPEN.  
**Review:** Internal construction and obstacle analysis only; no unrestricted superpolynomial claim.

## 1. Literature and repository search

Fresh ECCC inspection (26 November 2026): TR26-344 (complex-analytic lower bounds for Gap Hamming completions), TR26-342 (exhaustive search hard to beat in constant depth for hyperclique and orthogonal vectors), TR26-333 (witness indistinguishability and cryptography), and TR26-341 (Wyner common information NP-hard) do not address single-tape crossing sequences, charged cumulative memory on SAT families, or the compatibility bottleneck after static transport. Organization-scoped searches on OpenAI, Anthropic, Google Research, and DeepMind again yield no charged-model or Hartmanis-style SAT lower-bound work. Hartmanis 1968 remains the classical quadratic barrier for separated equality constructions. Beame–Kornerup cumulative memory supplies general context only.

Repository controls: matching upper bound (41) of CHARGED-UNSAT-TRANSPORT1 and static ceiling Theorem 2 (44) are recovered unchanged. No intervening commit closes DYNAMIC-COMPATIBILITY-OBLIGATION1.

## 2. Attempted proof construction

Candidate dynamic obligation (post-transport):

After the initial left/right map comparison on the permutation (or map) family, introduce a sequence of residual maps \(\rho_1,\rho_2,\ldots,\rho_k\) where each \(\rho_{j+1}\) is an affine shift or permutation of a short description of the previous residual, revealed only after the previous equality bit is known. The claim was that each residual still carries independent \(\Omega(\log r)\) bits of incompressible information that must reside in complete configurations at later crossings, producing an additional \(\Omega(k N^2)\) factor when \(k=\omega(1)\).

The decoder side-information and bounded-reuse conditions of the handoff bounded-reuse lemma were to be satisfied by treating each residual equality as a separate obligation set with reuse bounded by a constant.

## 3. Obstacles and collapse

1. **Joint compressibility.** All residual maps that are deterministic functions of the original input pair \((\pi,\sigma)\) (or \((f,g)\)) can be computed during the single authentication-and-comparison pass already charged in the matching upper bound solver. The equality bits for every residual are thereby obtained and cached before any later “post-transport” stage. No additional compulsory crossings are forced beyond the quadratic already paid.

2. **Paid generation.** If the residuals are generated on the fly by the machine itself, every transition that writes the next residual description, updates the tape, or re-crosses a cut is already included in the whole-run lower bound of the original theorem. The model charges those transitions; they do not constitute free external events. The total remains \(O(N^2)\) when the number of residuals is polynomial, because the family solver simply extends its single comparison loop.

3. **Decoder and reuse.** Any decoder that recovers a residual from a cached equality bit plus a short program for the shift rule has description length \(O(\log N)\). The event reuse bound is vacuously satisfied once the work has already been performed in the initial pass; the obligations are not independent after paid joint preprocessing.

Consequently the candidate fails the requirement that the obligations remain compulsory after static transport can be completed. The construction collapses under the existing matching upper bound.

## 4. Revised scope

The static method is confirmed to saturate only a constant fraction of its own ceiling (consistent with prior ratio computations). No superpolynomial amplification is obtained from residual maps that are functions of the initial separated input. A viable DYNAMIC-COMPATIBILITY-OBLIGATION1 construction must produce obligations whose information is not jointly recoverable from a single paid comparison of the source blocks, or must force the machine to re-materialize incompressible data after the first transport in a way that the charged model cannot cache for free.

## 5. Gates

| Gate | Status |
|---|---|
| Static ceiling | Confirmed; candidate does not exceed it. |
| Matching upper bound | Realized; collapses the candidate. |
| Unrestricted SAT lower bound | Not claimed. |
| P vs NP | OPEN. |

DYNAMIC-COMPATIBILITY-OBLIGATION1 OPEN. P vs NP OPEN.

HEAD at start: 50d59c832b2b6983073cc4f625885125c730b216
