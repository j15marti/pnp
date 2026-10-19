# POSTPROCESSING-FIREWALL6 | 2026-10-20 04:48 Asia/Seoul

**Result.** A compact joint target cannot evade `PUBLIC-SEED-ERASURE-TAX5` merely by compressing or hashing the repeated masked transcripts. Any source-independent deterministic or randomized postprocessing is a Markov kernel and cannot increase total variation. Therefore it preserves the same `Omega(1/alpha)` evidence-sample requirement. The only remaining compact-target escape must directly use additional source information; that is a new `R_k` construction whose acquisition, semantics, output and memory must be charged. **P versus NP remains OPEN.**

## 1. Recovered state

Read governance, current `main2.tex` through `main5.tex`, Compact-History records, the shared fallback Doc, and all commits after `PUBLIC-SEED-ERASURE-TAX5`. No new specialist theorem, code or raw record appeared after that synthesis. The only new repository material was another independent review annotation written into root `main.tex`; root still contains the literal “Full content continues” placeholder and was not edited.

The live frontier was therefore the explicit escape left by the preceding theorem: perhaps `r` weak masked targets could be combined into one short target without paying the repetition tax.

## 2. Falsifiable ideas fixed before literature search

1. **Postprocessing firewall.** If the compact target is computed solely from the public seeds and repeated masked transcripts, data processing should prevent any increase in TV. Falsifier: a source-independent compressor whose output TV exceeds transcript TV.
2. **Direct-access dichotomy.** If a compressor does exceed the transcript information, it must use extra source-dependent information or a different random experiment. Falsifier: exhibit an exact Markov factorization through the old transcripts despite increased TV.
3. **Shared-seed escape.** A short generator could reduce random-seed acquisition, but correlations invalidate the independent product identity. Falsifier for treating this as free: correlated seeds that cancel exposure or break both-promise correctness.

## 3. Primary-source model check

- CHMY's theorem is a randomized one-way-input/one-work-tape lower bound at a fixed larger MCSP threshold. It does not state that arbitrary source-dependent compactors preserve its generator. Primary: <https://doi.org/10.4230/LIPIcs.STACS.2021.23>.
- MMW provides efficient streaming algorithms for resource-bounded compression with short `Sigma_3 SAT` queries under its stated oracle model. It does not provide a generic TV-amplifying compiler or SAT-to-ordinary-MKTP `R_k`. Primary: <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>.
- FLMV remains a deterministic random-access endpoint; a direct source-reading compact target must be costed in that same realization before transfer. Primary: <https://lance.fortnow.com/papers/files/tst.pdf>.
- The total-variation data-processing fact used below is model-independent probability theory, not a computational lower bound.

## 4. Theorem: compact postprocessing cannot restore erased semantics

Let `U_b` be the full transcript distribution generated from source label `b in {0,1}`. It may include all public seeds and all `r` masked outputs. Let `K(v|u)` be any stochastic postprocessor independent of `b`; deterministic compression, hashing, majority circuits and randomized encoders are special cases. Define

`V_b(v)=sum_u U_b(u) K(v|u)`.

**Theorem (established).**

`TV(V_0,V_1) <= TV(U_0,U_1)`.

**Proof.** Using `TV(P,Q)=1/2 sum_x |P(x)-Q(x)|`,

`2 TV(V_0,V_1) = sum_v |sum_u (U_0(u)-U_1(u))K(v|u)|`

`<= sum_u |U_0(u)-U_1(u)| sum_v K(v|u)`

`=2 TV(U_0,U_1)`.

QED.

For the public-seed exposure model from the previous synthesis,

`TV(U_0,U_1)=1-(1-alpha)^r`.

Consequently no transcript-only compact target can enable two-sided error at most `1/3` unless

`1-(1-alpha)^r >= 1/3`.

The `Omega(1/alpha)` repetition/evidence requirement survives arbitrary transcript compression. Compression may reduce serialized length; this theorem alone does **not** prove it needs `Omega(r)` machine time. A fused constructor could share work. But any claim of that kind now needs an explicit same-machine construction and resource proof rather than an information gain from hashing or compression.

### Direct-source-access dichotomy

Suppose a proposed target `C` has TV greater than the full transcript. Then `C` cannot satisfy the Markov chain

`source label -> old transcript -> C`.

It must use additional source-dependent access, a new oracle, different randomness, or different semantics. That is not a postprocessing repair; it is a new reduction. For the main route it must be treated as part of the charged, total, ordinary-MKTP map `R_k`, including both SAT outcomes and witness projection/extension.

## 5. Exact adversarial audit

`experiments/review/2026-10-20_postprocessing_firewall_audit.py` builds a canonical public-exposure distribution with `alpha=1/2` and exhaustively enumerates every Boolean deterministic compressor for `r=1,2,3`.

- `r=1`: 8 compressors over 3 union states; maximum output TV `1/2`.
- `r=2`: 128 compressors over 7 states; maximum output TV `3/4`.
- `r=3`: 32,768 compressors over 15 states; maximum output TV `7/8`.

These equal the uncompressed values `1-2^-r`; none exceeds them. Total: 32,904 compressors and 32,910 exact assertions, zero failures. Raw: `results/raw/synthesis/2026-10-20_0448_POSTPROCESSING_FIREWALL6.json`.

The finite enumeration audits definitions only; the theorem above covers arbitrary finite deterministic or randomized postprocessors.

## 6. Compact-History diagnostic

The same firewall applies to digests of already-generated history samples: hashing or compressing them cannot create missing distinguishing information. A history circuit that directly evaluates the succinct transition is not postprocessing of black-box samples; it is a new explicit algorithm and may fast-forward, as affine/modular controls show. Its construction and evaluation must be charged, and the required shared quantifier remains `exists W forall i`, not `forall i exists W_i`.

## 7. Two-route proof DAG

| Status | Arrow |
|---|---|
| ESTABLISHED | Public-seed TV identity; erasure-amplification tax; TV data-processing firewall; MMW short-query streamer; FLMV matched endpoint. |
| COMPUTATIONAL | 32,904 exhaustive Boolean compressors and 32,910 exact assertions, zero failures. |
| CONDITIONAL | A fused target may reduce serialization or share work, but only under an explicit source-access and machine-cost construction. |
| CANDIDATE | Direct fully charged total `R_k`, or an original-CHMY critical-band construction with proved both-promise semantics and correlated-seed analysis. |
| OPEN | Any direct compact ordinary-MKTP target that uses extra source information; standard-model Ilango replacement; all-input ARC successor; compact diagonal witness premise. |
| RETIRED | Hashing/compressing old masked transcripts as a source of new semantic information; transcript-only compact targets claimed to evade the repetition requirement. |

**Weakest arrow:** the uniform, total, fully charged direct construction `R_k`. The postprocessing escape is now closed; direct source use remains open.

## 8. Role handoff

- **MCSP:** any compact joint target must state whether it is transcript-only. If yes, the TV firewall applies; if no, expose every additional source read and prove both MCSP promises.
- **Universal Solver:** model the compact encoder as a Markov kernel or identify the exact direct-source operation. Report its unknown exponent, target length, output cost and live state.
- **ARC:** charge fused construction rather than just serialized output; test whether shared work actually satisfies the required `a,g,r,eta,lambda` inequalities.
- **Red team:** search for a claimed compressor that secretly reads the source or changes the random experiment; test shared-seed correlations and promise leakage.
- **Synthesis:** admit compact repetition only with a full factorization/access ledger and ordinary-total witness semantics.

No scheduling change was made. Compact History remains supporting diagnostic only. Root `main.tex` was not edited. **P versus NP remains OPEN.**

END_OF_VERIFIED_MAIN::POSTPROCESSING_FIREWALL6::P_VS_NP_OPEN
