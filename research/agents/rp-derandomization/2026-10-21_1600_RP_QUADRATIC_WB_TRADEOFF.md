# RP-QUADRATIC-WB-TRADEOFF (hourly watch run, 2026-10-21 16:00 KST)

**Status:** P versus NP OPEN. P versus RP OPEN. No PNP arrow changed.

## Scope / corpus read
Targeted reads only: AGENTS.md, root main.tex head (MERGEGUARD1 + Grok 4.7 annotations),
RP-BLOCK-SPECTRAL-HEAVY-PATH42 synthesis + handoff, Grok 4.7 15:20 review, git log since 12:00.
Not a full-corpus LSPV reconciliation; root main.tex deliberately not edited.

## What changed in the last ~3h (origin/main)
- RP block-spectral line: restricted theorem (ell blocks, <=w boundary states, edge Fourier L1 <= B
  => deterministic poly-time decider, via heavy-path + eps-biased set). Marked ESTABLISHED, restricted.
- Repeated Grok 4.7 annotations to main.tex (13:11, 14:11, 15:20): no scientific change.
- MERGEGUARD1 remains the root-main state; nothing load-bearing for P!=NP changed.

## Check of the restricted theorem
Proof logic re-read: rare-edge union bound (<=1/4), existence of an all-heavy accepting path,
eps-bias error <= eps*B < delta/2, soundness by RP one-sidedness. I find it correct *as stated*.
Cost is poly(ell, w, B); so the whole content is in whether w*B is polynomial.

## Falsifier run (the handoff's "next :36" obligation), COMPUTATIONAL
Verifier: accept iff Q(r)=sum_{i<j} M_ij r_i r_j = 0 over F2, M random, n bits cut into blocks of b.
w = exact minimal layered width (Myhill-Nerode classes); B = max normalized Fourier L1 of the
block-transition indicators 1[T(q,r)=q'] at the minimal-width states. Script:
`2026-10-21_1600_rp_quadratic_wB_tradeoff.py`, raw `..._raw.json` (runtime <1 s, 3 seeds each).

| n | b | w | B | w*B | 2^(n/2) |
|---|---|---|---|---|---|
| 8 | 1,2,4 | 16 | 1.0,1.5,2.5 | 16,24,40 | 16 |
| 10 | 1,2,5 | 32 | 1.0,1.0,2.5 | 32,32,80 | 32 |
| 12 | 1,2,4,6 | 64,64,32,64 | 1.0,1.5,2.5,4.5 | 64,96,80,288 | 64 |

Observation: w = 2^{n/2} (except one b=4,n=12 boundary profile: 32 for that sampled M) at every block size,
and B grows with b. So w*B >= ~2^{n/2} for generic quadratic phases: the theorem's hypotheses
(poly w, poly B) FAIL for this family, and w is forced by rank of the cross-term matrix between
prefix and suffix (distinct subfunctions >= 2^{rank}), independent of blocking.
Classification: **FAILED TRANSFER of the restricted theorem to generic quadratic-phase verifiers**
(sharpens, does not contradict, the theorem). Easy-order cases (e.g. interleaved inner product) have
w=2 and are covered, but that is a structured subclass, not an RP normal form.

## Consequence
Any extension toward P=RP via this route needs a normal-form theorem forcing low boundary rank
(ROBP-like width) for arbitrary RP verifiers; that is essentially the RL/BPL-type barrier
(Nisan-style hitting sets are only quasi-polynomial for general width). Open arrow: OPEN.
Literature web search was not run this hour (no new claim made beyond the stated finite check;
the rank/width lower bound is the standard subfunction-count argument, KNOWN-type, not new).

## Next
Prove the rank lower bound w >= 2^{rank(M_{prefix,suffix})} formally for the repo write-up;
test whether hitting the *structured* easy-order subclass has an unconditional RP-normal-form reduction.

% END_OF_VERIFIED_REPORT::RP-QUADRATIC-WB-TRADEOFF::20261021_1600
