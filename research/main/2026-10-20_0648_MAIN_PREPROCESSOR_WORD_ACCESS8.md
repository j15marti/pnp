# PREPROCESSOR-WORD-ACCESS8 | 2026-10-20 06:48 Asia/Seoul

**Result.** Splitting source access among preprocessing, target construction, and a universal solver does not evade `CONDITIONED-HARD-SPARSE-QUERY7`. In a precise block-access model, only the union of source coordinates touched on the zero-answer execution matters. If `A` adaptive accesses each reveal at most `w` named source bits, arbitrary phase composition and downstream computation have total variation at most

`1 - C(N-u,k)/C(N,k) + eta`, where `u <= min(N,wA)`.

For negligible `eta`, sparse support `k=o(N)`, and `wA=o(N)`, constant distinguishing advantage requires `A=Omega(N/(wk))`. On a standard logarithmic-word abstraction this is `Omega(N/(k log N))` word accesses. This is a restricted information/access theorem, not a one-tape or unrestricted SAT lower bound. **P versus NP remains OPEN.**

## 1. Recovered state

Read the governance audit, continuity protocol, Compact-History addendum, current `main2.tex` through `main5.tex`, the shared Google continuity log, the previous `CONDITIONED-HARD-SPARSE-QUERY7` theorem and REDTEAM24 raw record, and every repository commit after the preceding synthesis. No new :00/:12/:24/:36 scientific artifact appeared. The only new commit was an independent review at 06:11 KST; it preserved the open status and modified unsafe root `main.tex`, which was not edited here.

The shared fallback document remained unchanged after REDTEAM23. GitHub was available, so no fallback append was required.

## 2. Falsifiable ideas fixed before literature search

1. **Phase-composition conservation.** Concatenate preprocessor and constructor probes; their separate labels should not change the zero-path coupling. Falsifier: a two-phase adaptive strategy whose hit probability exceeds that of its total touched-coordinate union.
2. **Packed-word repair.** Replace one-bit probes by accesses revealing at most `w` named coordinates. Falsifier: a legal word access exposing information about untouched source coordinates.
3. **Universal-race ledger.** Portfolio candidates may interleave, but all source coordinates read before termination must be charged to the actual execution. Falsifier: a fastest-correct race whose output depends on a source bit no executed candidate accessed.
4. **Semantic-access boundary.** Global hashes, algebraic summaries, or succinct transition syntax are not `w`-coordinate accesses unless their construction cost is separately supplied. Falsifier: implement such a primitive in the declared machine using fewer touched coordinates than its specification reads.

## 3. Primary-source model check

- CHMY's proved lower bound is for randomized two-sided MCSP at a fixed larger threshold on a one-tape machine with an additional one-way read-only input tape. The theorem below does not model its full scan or establish threshold descent. <https://doi.org/10.4230/LIPIcs.STACS.2021.23>
- MMW's search-MCSP streamer reads the truth table in successive blocks, maintains a circuit consistent with the prefix, and invokes short `Sigma_3 SAT` queries. Its Theorem 1.3 requires both polynomial-in-`s` space and update time. This source-consumption algorithm is not a SAT-to-MKTP target constructor. <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>
- OPS is a distinct nonuniform GapMCSP magnification hypothesis. <https://theoryofcomputing.org/articles/v017a011/>
- Hutter's universal solver schedules programs with proofs of correctness and runtime bounds; it does not make their input accesses free or establish a uniform bound on the winning exponent. <https://arxiv.org/abs/cs/0206022>
- Ilango remains random-oracle-relative, and FLMV remains a deterministic random-access simultaneous time-space endpoint. Neither supplies the missing model transfer.

Levin search, Blum speedup, and easy-witness results remain diagnostics. None turns the restricted access theorem into the total deterministic standard-model `R_k`, and none proves the shared Compact-History witness premise.

## 4. Theorem: touched-coordinate conservation across phases

Let `Z=0^N`. Let `U_k` be uniform over weight-`k` Boolean strings. Let `F` be `U_k` conditioned to circuit complexity greater than `s`, with discarded easy mass

`eta <= 2^L/C(N,k)`.

Consider any randomized pipeline with source-independent initial side information and any number of named phases: preprocessing, target construction, portfolio scheduling, decoding, and final decision. Across the actual execution it makes at most `A` adaptive source accesses. Each access names a set of at most `w` source coordinates and returns their bits. All later computation is unrestricted but receives no additional source information.

Let `u` be the number of distinct coordinates touched along the all-zero execution for fixed internal randomness. Then `u<=min(N,wA)`.

**Theorem (established, restricted model).**

`TV(Pipeline(Z), Pipeline(F))`

`<= 1 - C(N-u,k)/C(N,k) + eta`

`<= 1 - C(N-min(N,wA),k)/C(N,k) + eta`.

**Proof.** Couple the executions using identical internal randomness and side information. Until an accessed block intersects the random support, every returned bit is zero, so every phase transition and future access is exactly the one on the zero execution. The executions can diverge only if the random `k`-support intersects the union of the zero-path blocks. A fixed union of size `u` is avoided with probability `C(N-u,k)/C(N,k)`. Coupling bounds TV by the complementary hit probability. Conditioning from `U_k` to hard sources changes TV by at most `eta`; the triangle inequality completes the proof. Arbitrary postprocessing cannot increase TV. QED.

The phase split is irrelevant: `r` preprocessing accesses and `q` constructor/portfolio accesses obey the same bound with `A=r+q`. Parallel simulation also receives no free reads; charge the union of coordinates touched by all candidates actually executed before termination.

For two-sided error at most `1/3`, TV must be at least `1/3`. Hence the right side must reach `1/3`. When `k=o(N)`, `eta=o(1)`, and `wA=o(N)`, this forces `A=Omega(N/(wk))`.

## 5. Exact audit

`experiments/review/2026-10-20_preprocessor_word_access_audit.py` exhaustively enumerated every sequence of blocks of size at most two for `2<=N<=8` and up to three accesses, including repeats and overlap. For every support size it checked that the observed hit probability never exceeded the bound from `wA`. It also checked all 45 splits of totals zero through eight between preprocessing and construction.

Results: 97,138 block sequences, 704,658 exact assertions, zero failures.

Named control: `N=65536`, `k=256`, `s=16`, `w=16`, `L=197`, and `log2 eta<=-2214.2842`. Six word accesses give bound `0.3134028<1/3`; seven give `0.3551446>1/3`. Thus seven 16-bit source accesses are necessary in this instance.

Finite enumeration audits the definitions; the coupling proof covers all finite adaptive phase pipelines in the stated model.

## 6. Strongest falsifier and scope

The strongest escape is a primitive returning a global source-dependent summary—such as a hash, parity, algebraic sketch, or succinct semantic feature—while being charged as one small access. That primitive violates the `w` named-coordinate interface unless its own source reads are included. A proof may use it only after giving a machine implementation and charging acquisition, construction, storage, and replay.

MMW's actual streamer reads the full source and therefore lies outside the intended low-access regime; the present theorem does not contradict it. CHMY's one-way input head may scan all `N` cells, so its time cost and generator structure must be analyzed directly. ARC still requires an all-input hereditary successor, not a distributional sparse-source argument.

Compact-History remains supporting-only. Explicit modular increment supplies semantic transition syntax and can fast-forward; it is not a truth-table block-access algorithm. The open quantifier is still one shared `exists W forall i`, not separate `forall i exists W_i` witnesses.

## 7. Two-route proof DAG

| Status | Arrow |
|---|---|
| ESTABLISHED | Transcript data-processing firewall; adaptive hard-sparse bit-query tax; phase-composed block-access conservation; MMW streaming theorem; FLMV endpoint. |
| COMPUTATIONAL | 97,138 block sequences and 704,658 exact assertions, zero failures. |
| CONDITIONAL | Converting the word-access count into matched machine time requires an explicit implementation and word-width convention. |
| CANDIDATE | Apply the bound to a concrete source port of a proposed total ordinary-MKTP target with every global summary expanded into its accesses. |
| OPEN | Deterministic standard-model `R_k`; vanishing threshold with `p_k>=log M`; no-side-table totalization; bounded universal-solver exponent; all-input ARC successor; Compact-History shared witness. |
| RETIRED | Hiding source acquisition in a separate preprocessor, portfolio candidate, or packed word without charging all touched coordinates. |

**Weakest arrow:** the uniform, total, fully charged standard-model `R_k`. The new theorem strengthens its access ledger but does not construct it.

## 8. Narrow role allocation

- **MCSP (:00):** give one actual CHMY source-injection candidate an explicit block-access ledger; distinguish full sequential scan from local generator access.
- **Universal Solver (:12):** sum the touched-coordinate union across every candidate run before the winner is certified; report proof search and input acquisition separately from exponent `C`.
- **ARC (:24):** test whether any global summary used by a contractor can be computed within `a+g<=3/5` and live space `<=1/2` on every input.
- **Red team (:36):** propose a global-summary primitive, implement it in the declared machine, and charge every source coordinate or word it consumes.
- **Synthesis (:48):** reject phase-separated access ledgers; require a single execution-wide union and same-machine time/space/output record.

No schedule was changed. Root `main.tex` was not edited. **P versus NP remains OPEN.**

END_OF_VERIFIED_MAIN::PREPROCESSOR_WORD_ACCESS8::P_VS_NP_OPEN
