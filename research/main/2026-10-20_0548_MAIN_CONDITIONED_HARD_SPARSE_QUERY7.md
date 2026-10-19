# CONDITIONED-HARD-SPARSE-QUERY7 | 2026-10-20 05:48 Asia/Seoul

**Result.** The direct-source escape left by `POSTPROCESSING-FIREWALL6` also has a quantitative barrier in a precise bit-query model. Against a zero YES source and a uniformly random `k`-sparse source conditioned to have circuit complexity greater than `s`, every randomized construction using at most `q` adaptive source-bit probes and otherwise source-independent side information has output total variation at most

`1 - C(N-k,q)/C(N,q) + eta`,

where `eta <= 2^L/C(N,k)` and `L` upper-bounds the circuit-description length. Thus bounded error needs this quantity at least `1/3`. This is an exact restricted-model theorem, not a CHMY transport, SAT-to-MKTP reduction, or unrestricted machine lower bound. **P versus NP remains OPEN.**

## 1. Recovered state

The required governance, continuity protocol, Compact-History addendum, current `main2.tex` through `main5.tex`, shared Google continuity log, and all new commits after `POSTPROCESSING-FIREWALL6` were read. The only new specialist evidence was REDTEAM24's machine-readable record `results/raw/separation/2026-10-20_0536_REDTEAM24_SOURCE_QUERY_TAX_MIN.json`. It states the unconditioned sparse-source hit bound and a finite `N=1024,k=64,s=4` control. No complete REDTEAM24 report or executable was published at recovery time.

Root `main.tex` was not edited. The Google fallback log's newest visible entry was REDTEAM23; GitHub was available, so no fallback append was needed.

## 2. Falsifiable ideas fixed before literature search

1. **Hard-promise conditioning repair.** Transfer the uniform sparse-source query bound to actual MCSP-NO sources by conditioning away size-`s` circuits. Falsifier: conditioning can increase output TV by more than the discarded easy mass `eta`.
2. **Adaptive zero-path coupling.** Until the first source `1` is found, every adaptive query follows exactly its zero-source path. Falsifier: a decision tree whose no-hit probability is below the hypergeometric value for `q` distinct probes.
3. **Two-stage access ledger.** Transcript-only processing has the previous data-processing firewall; direct source access pays the present query tax. Falsifier: a factorization using neither old transcripts nor charged source probes but still increasing label TV.
4. **Universal-solver separation.** A fastest-correct solver can optimize the downstream decision, but cannot retroactively create label information absent from the constructed target. Falsifier: a source-independent downstream solver whose acceptance gap exceeds input TV.

## 3. Primary-source check

- CHMY proves a randomized two-sided lower bound for MCSP at a fixed larger threshold on a one-tape machine with a one-way read-only input tape. It does not supply the source-query reduction below or a threshold descent. <https://doi.org/10.4230/LIPIcs.STACS.2021.23>
- MMW Theorem 4.2 gives an `O(N p(N))`-time, `O(p(N))`-space MKTP streamer with `O(p(N))`-length `Sigma_3 SAT` queries for `p(N)>=log N`. It consumes an existing truth table and does not construct a SAT-to-MKTP target. <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>
- OPS is a nonuniform GapMCSP hardness-magnification endpoint; the present adaptive bit-query statement is not its hypothesis. <https://theoryofcomputing.org/articles/v017a011/>
- Hutter's universal solver competes only with programs accompanied by correctness and runtime proofs and retains program/proof-dependent overhead; it does not uniformly bound the unknown MMW exponent. <https://arxiv.org/abs/cs/0206022>
- Ilango's current SAT-to-MCSP result is random-oracle-relative, not a deterministic standard-model replacement for `R_k`. <https://eccc.weizmann.ac.il/report/2023/165/>
- FLMV is a deterministic random-access time-space endpoint. A bit-query lemma cannot be promoted to that endpoint without a same-machine construction and full resource accounting. <https://lance.fortnow.com/papers/files/tst.pdf>

Levin/Hutter search and Blum speedup remain portfolio diagnostics: they do not provide the missing total SAT-to-MKTP construction or an all-input ARC successor. Easy-witness/Compact-History reasoning still assumes the open shared circuit `exists W forall i`; the present full truth-table source distribution does not prove compactness for an explicit succinct transition.

## 4. Theorem: hard sparse sources retain the adaptive query tax

Let `N=2^n`. Let `Z=0^N`. Let `U_k` be uniform over the `C(N,k)` Boolean strings of Hamming weight exactly `k`. Let `H_s` be the subset having circuit complexity greater than `s` in the fixed AND/OR/NOT circuit model, and let `F` be uniform over `U_k` conditioned on `H_s`.

If circuits of size at most `s` have descriptions of length at most

`L = s(2 + 2 ceil(log2(n+s))) + ceil(log2(n+s))`,

then the easy fraction satisfies

`eta := Pr_{X~U_k}[X notin H_s] <= 2^L/C(N,k)`.

Consider any randomized procedure `A` with arbitrary side information independent of the source and its label. `A` may make at most `q` adaptive bit probes to its source and then output anything. For `q<=N-k`,

**Theorem (established, restricted model).**

`TV(A(Z),A(F)) <= h_q + eta`,

where

`h_q = 1 - C(N-k,q)/C(N,q)`.

For `q>N-k`, use the trivial bound one.

**Proof.** Couple both executions with the same internal randomness and side information. On the zero source every answer is zero, fixing a zero-answer query path. Against a uniform `k`-subset, the two executions remain identical until that path hits the support. Repeated probes only decrease the hit probability; `q` distinct probes attain exactly `h_q`. Hence coupling gives `TV(A(Z),A(U_k))<=h_q`. Also `TV(U_k,F)=eta`, and data processing plus the triangle inequality gives `TV(A(Z),A(F))<=h_q+eta`. QED.

The unconditioned bound is tight: probe `q` distinct coordinates and output the hit flag.

If a downstream decision has two-sided error at most `1/3` on the two source distributions, its acceptance gap is at least `1/3`. Therefore necessarily

`h_q + eta >= 1/3`.

When `k=o(N)` and `eta=o(1)`, this forces `q=Omega(N/k)`. For `s=N^mu` and `k=N^(1-kappa)` with `0<kappa<1-mu`, circuit counting makes `eta` negligible and the restricted construction needs `Omega(N^kappa)` source probes.

## 5. Exact adversarial audit

`experiments/review/2026-10-20_conditioned_sparse_query_audit.py` performed:

- exhaustive checks of every zero-answer query sequence, including repeated coordinates, for `2<=N<=8` and `q<=4`;
- exact conditioning checks after deleting up to three arbitrary sparse supports;
- exact reproduction of REDTEAM24's named point `N=1024,k=64,s=4,L=44`.

Results: 61,582 query-sequence checks, 684 conditioning checks, 62,405 assertions total, zero failures. At the named point `log2 eta <= -297.1039485`; the bounds are `0.3217310` at `q=6` and `0.3643727` at `q=7`, so seven probes are necessary for a `1/3` TV gap.

The enumeration audits the finite identities; the coupling-and-conditioning proof is general.

## 6. Scope and strongest falsifier

The theorem closes only the **few direct bit probes plus source-independent side information** escape. It does not charge a source-aware preprocessor that already read many bits, a word-RAM primitive reading packed words, correlated semantic access, or a different ordinary-total reduction. All such access must be exposed and charged in the actual machine model.

The strongest falsifier is explicit: a preprocessor can scan the source, choose a nonzero coordinate, and hand the target constructor that coordinate and bit. It defeats the source-independent-side-information premise, but pays the scan/read cost. Proving that this cost ruins the desired exponents in the actual `R_k` or CHMY machine remains OPEN.

Compact-History is unaffected: a random hard sparse truth table is not a succinct explicit transition. Modular increment still fast-forwards, and `forall i exists W_i` still does not imply `exists W forall i`.

## 7. Two-route proof DAG

| Status | Arrow |
|---|---|
| ESTABLISHED | Sparse-source adaptive query bound; hard-promise conditioning cost `eta`; transcript data-processing firewall; MMW short-query streamer; FLMV matched endpoint. |
| COMPUTATIONAL | 62,405 exact assertions, zero failures; named `q=7` threshold reproduced. |
| CONDITIONAL | Polynomial query tax transfers to construction time only after source access is implemented and charged in the matched machine. |
| CANDIDATE | Apply the theorem to an explicit source port of a proposed CHMY/ordinary-KT target, with all other side information proved source-independent. |
| OPEN | Total deterministic standard-model `R_k`; source-aware compact target; all-input ARC successor; shared Compact-History witness; control of the MMW solver exponent by a certified portfolio. |
| RETIRED | Transcript-only hashing/compression; claims that a few adaptive bit probes evade sparse-source erasure without paying conditioning or access cost. |

**Weakest arrow:** a uniform, total, fully charged ordinary-MKTP construction `R_k`. The new theorem constrains one access pattern; it does not build that arrow.

## 8. Narrow role allocation

- **MCSP (:00):** instantiate `q`, `k`, `eta`, and all side information for one actual CHMY source-injection candidate; prove the side information is source-independent or expose its reads.
- **Universal Solver (:12):** place target acquisition before portfolio search and show whether proof-certified selection changes only downstream exponent `C` or also performs charged source reads.
- **ARC (:24):** test whether a source-aware preprocessor satisfying the query bound can meet `a+g<=3/5`, `lambda<=1/2`, and `eta_space<=1/2` on every input; a sparse distribution alone is insufficient.
- **Red team (:36):** attack the independence premise with correlated advice and packed-word access; state every pre-read and recompute the TV bound after conditioning.
- **Synthesis (:48):** admit direct-access repairs only with a source-access ledger and matched machine; keep Compact-History supporting-only.

No schedule was changed. Root `main.tex` was not edited. **P versus NP remains OPEN.**

END_OF_VERIFIED_MAIN::CONDITIONED_HARD_SPARSE_QUERY7::P_VS_NP_OPEN
