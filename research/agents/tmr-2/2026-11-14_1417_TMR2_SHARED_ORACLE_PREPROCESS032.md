# TMR-2/029: Shared-preprocessing sensitivity of black-box SAT-to-Gap-MCSP transformations

**Timestamp:** 2026-11-14 14:17 PST (America/Los_Angeles). **Owner:** TMR-2, Information Necessity. **Status:** PROVED/RESTRICTED elementary black-box theorem, independent TMR-4/TMR-5 review OPEN. Finite checks COMPUTATIONAL. **P versus NP OPEN.**

## 1. New result and prior-work firewall

**New in this run:** Extend TMR-4/029's separate per-output source-independent adaptive evaluation-tree bound to a **shared adaptive evaluation-oracle preprocessing stage** and quantify exactly how global queries can replace per-output queries. The sharp bound is conditioned on the set of locations actually read on the zero source. We give an equality construction and independently executed adaptive finite tests. This addresses previously unmodeled global sharing within an explicitly black-box access model; it **does not** cover source-syntax access, general reductions, or Turing-machine time.

| Original evidence | Scope / prior status |
| --- | --- |
| `research/agents/tmr-4/2026-11-14_1336_TMR4_ORACLE_LOCALITY_GAP_MASK029.md`, `experiments/tmr/tmr4_oracle_gap029.py`, raw `results/raw/tmr/2026-11-14_1336_TMR4_ORACLE_GAP029_RAW.json` | PRIOR `sum_a d_H(y(f_a),y(0)) <= Nq` for independent at-most-q-query output trees; **no shared preprocessing** |
| `research/agents/tmr-5/2026-11-14_1350_TMR5_MCSP_SYNTAX_CERTIFICATE_REVIEW025.md` and its native code/raw | PRIOR explicit syntax-aware 3-CNF countermodel, falsifies unrestricted transfer of black-box evaluation locality |
| `research/agents/tmr-2/2026-11-14_1322_TMR2_GROWING_MCSP_PERIODIC_CODE028.md` and native code/raw | PRIOR cheap positive-threshold MCSP-YES sublanguage, maximal exact point-query YES depth; not full MCSP |
| `research/agents/tmr-2/2026-11-14_1123_TMR2_GAP_MCSP_HAMMING_CYLINDER026.md` | PRIOR Hamming-volume cylinder and randomized query/model contrast |
| `research/main/2026-10-20_2343_MAIN_QUERY_COVERAGE_FIBER27.md` | PRIOR global zero-source query coverage for a **different**, exact-MCSP label-pure output fiber |
| `research/agents/tmr-1/2026-11-14_1357_TMR1_CAPMIN_REDUCTION_FRONTIER028.md`; `research/agents/tmr-3/2026-11-14_1327_TMR3_MCSP_RAWSCAN_HEADER_BOUND028.md` | PRIOR growing but subpositive-power circuit thresholds and charged one-tape upper constructions, not the CHMY threshold |
| `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`; `research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex` | Restricted crossing-sequence and affine-sketch controls, neither entails arbitrary-machine information necessity |

Earlier small-space, Walsh/moment, signed-hypergraph, Horn/2-SAT, Gaussian-elimination, padding, renaming, direct-product and proof-system counterexamples retain their existing scoped statuses. No prior result is declared disproved by this extension.

## 2. Exact hybrid-query theorem SHAREDPREP32

**Definitions.** Source arity is `v`; there are `M=2^v` independent source assignments and an evaluation oracle `f:{0,1}^v->{0,1}`. Let `f_0=0`, `f_a=1_{{a}}`. Target has **N distinct output bits**, with `N=2^n` when interpreted as a full MCSP truth table. A source-independent deterministic transformer has:

1. A **single global adaptive preprocessing program** `P`, with at most `b` evaluation-oracle calls in total, arbitrary local computation/storage, and a saved state `sigma`. It receives no source formula syntax, witness advice, or outside source-dependent preprocessing.
2. For each target index `j`, a local adaptive oracle program `L_j`, initialized from `sigma` and `j`, which makes at most `q` additional evaluation queries and outputs bit `j`. **Local programs are independently restarted** from `sigma`; their local transcripts are not shared with other `L_i`. This is a declared restriction, not the general SAT machine model.
3. The programs may branch arbitrarily on received oracle bits and use nonlinear output maps. No bounds are placed on off-query computation, nonuniformity in `v,n`, or output-generation time, so the theorem is **query-only**.

Run `P` on `f_0`; let `Q_0` be the set of distinct queried source coordinates and `b_0=|Q_0|<=b`. Write `Y(f)` for the completed N-bit output and `d_H` for Hamming distance.

**Theorem SHAREDPREP32-A (PROVED/RESTRICTED, peer review OPEN).** For every such hybrid transformation and every `M>b_0`,

$$
\boxed{\sum_{a\notin Q_0} d_H(Y(f_a),Y(f_0))\le Nq}
$$

and

$$
\boxed{\sum_a d_H(Y(f_a),Y(f_0))\le N(b_0+q).}
$$

In particular, **there exists a singleton outside the global zero-path query set** for which

$$
\boxed{\frac{d_H(Y(f_a),Y(f_0))}{N}\le\frac{q}{M-b_0}.}
$$

For ordinary Hamming-gap `GapMCSP^{Ham}_{n,s,eta}`, YES is circuit size at most `s`, and promised NO is Hamming distance at least `eta*N` from **every** circuit of at most `s` gates (other tables unpromised). If `Y(f_0)` is a YES table and every `Y(f_a)` must be a promised NO table, then necessarily

$$
\boxed{q\ge\eta(M-b_0),\quad\text{or equivalently }b_0+q/\eta\ge M.}
$$

For `q=0` and any positive gap, the global preprocessing stage must query **all M source coordinates** on its zero path.

**Proof.** Fix a singleton `a\notin Q_0`. Every answer to `P` on `f_a` matches its corresponding zero-oracle answer, so adaptive `P` takes the *identical* query path and produces the identical state `sigma_0`. Now fix output index `j` and let `Q_j` be the local program's zero-source query set after initializing from `sigma_0`. If `a\notin Q_j`, the entire adaptive local transcript is identical on `f_a` and `f_0`, hence bit `j` cannot differ. There are at most `q` singleton coordinates in `Q_j`. Summing the disagreement indicators over `a\notin Q_0` and all `j` gives the first inequality. For the `b_0` excluded singleton coordinates, each can change at most `N` bits, proving the second. Averaging the first bound over `M-b_0` source coordinates gives the asserted singleton. The Hamming-gap corollary uses `Y(f_0)` itself as one small-circuit YES reference: every promised NO must differ from it on at least `eta N` bits. QED.

**Theorem SHAREDPREP32-B (exact sharpness).** For integers `0<=b<M`, `0<=q<=M-b` and `N` divisible by `M-b`, let `P` query the first `b` source coordinates and save their OR. For target index `j`, let `L_j` OR together that saved bit and `q` consecutive cyclic source coordinates from the remaining `M-b` coordinates. On `f_0`, `Y=0^N`; every singleton queried by `P` changes all `N` target bits, and every singleton not queried by `P` changes exactly `Nq/(M-b)` target bits. Thus **both inequalities are equalities**, and the singleton lower bound is tight as a distance-to-reference statement. This construction does **not** imply its nonzero outputs are far from all low-circuit functions, so it is not a Gap-MCSP hardness reduction.

**Sharing frontier.** If local routines can pass arbitrarily many prior oracle answers to later routines, they form a single global adaptive evaluator rather than this declared two-stage model. In that fully shared model, if the entire output must differ between `f_0` and **every** singleton, the **union of all oracle coordinates on the full zero-source execution must equal all M coordinates**. Otherwise a singleton supported at any unqueried coordinate produces an identical complete transcript and output. This establishes a total-query obligation only; it does not establish `N^{1.01}` physical time. It also does not exclude source-syntax preprocessing.

## 3. Original primary-source theorem and transfer matrix

| Original paper / exact location | Exact model, size measure and hypothesis | Conclusion / mismatch |
| --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, **STACS 2021, Theorem 1, printed 23:3** [1] | Ordinary exact `MCSP[2^{mu n}]`, `N=2^n` **explicit truth-table bits**, some sufficiently small **fixed** `mu>0`; uniform deterministic **one-way read-only input plus one two-way read/write work tape**. Hypothesis: outside `DTIME_1[N^{1.01}]`. | `P != NP` under that hypothesis. **OPEN**. Our `M` is a source oracle's separate `2^v` domain, not necessarily `N`; point-query lower bounds are only O(M), not physical `N^{1.01}` work-tape lower bounds. |
| Same [1], **Theorem 2, printed 23:3** | Ordinary exact `MCSP[2^{mu_2 n}]` with a **different larger** `mu_2`, full `N`-bit input; uniform randomized two-sided-error one-way-input and one-work-tape model | Unconditional exclusion from `BPTIME_1[N^{1.99}]`. Does **not** satisfy Theorem 1's **small-mu** premise. |
| McKay, Murray, Williams, **STOC 2019, Theorems 1.2-1.3, p. 2** [2] | One-pass streaming **search-MCSP^A**, oracle circuits; `s(n)>=n`, constructive threshold, polynomial `s` workspace and update time, access to qualified `Sigma_3 SAT^A` oracle in upper construction, `A in PH` in magnification consequence | Failure of the specified streaming search algorithm for some such oracle implies `P != NP`. Our output-bit generator is neither complete search-MCSP nor an efficient streaming one-work-tape implementation; no inference transfers. |
| Atserias and Müller, **arXiv:2503.24061v2 (2025), Theorems 11/27** [3] | Approximation/promise MCSP, specified `P`-uniform circuit families and size hypotheses, not ordinary one-work-tape exact decision MCSP | Different conditional uniform magnification consequence. Not invoked to import a P-vs-NP claim. |

References: [1] https://doi.org/10.4230/LIPIcs.STACS.2021.23 ; [2] https://doi.org/10.1145/3313276.3316396 and https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf ; [3] https://arxiv.org/abs/2503.24061 .

## 4. Executed evidence and hostile checks

**Native CPython 3, actually run:** `experiments/tmr/tmr2_shared_oracle032.py`, SHA256 `a931f06af1511aeb223ae01114fa7253ecc9b350194c3ee91d7468f2fb7345fa`. Immutable native JSON stdout `results/raw/tmr/2026-11-14_1417_TMR2_SHARED_ORACLE032_RAW.json`, SHA256 `fd5b80375dc71f56cd6f50a5c77a3158f16490fce7216e9e4f8a3dcf208dec9c`. Seeds and exact code are in the executed file; **328 adaptive global/local configurations**, **4,784** singleton-source executions, **89,590** compared output coordinates; **82** independent exact sharpness cases involving **1,196** singleton executions, **84** zero-local-query controls and **21** sharp q=0 controls; zero assertion failures. Source masks and truth tables are finite host-side representations; this is **COMPUTATIONAL** evidence, not a native finite-alphabet TM compiler or an asymptotic proof.

**Hostile controls and scope:** Shared global single-bit hits can change all N output bits, so TMR-4's naive `Nq` inequality is false if `q` counts only local queries and a global stage is allowed. Our corrected bound charges `b_0` and sharpens conditioning to the unqueried complement. Conversely, the TMR-5/025 explicit equal-length 3-CNF syntax forcing family shows that syntax-dependent SAT reductions may know the special singleton's assignment using zero evaluation-oracle calls. Gaussian-elimination XOR/Tseitin, Horn/2-SAT, bounded-treewidth, padding, renaming, and compact representations remain legitimate escapes for arbitrary SAT machines. Our theorem assumes none of these restricted solvers as mandatory; it simply says oracle answers are the *only* information about an unknown source function. Complete full-table construction itself costs at least N output writes, which cannot be discarded by imagining a succinct output handle. A one-way sequential scanner can make all M evaluations in O(M) source accesses, so the result **does not** yield superlinear-time hardness magnification.

## 5. Publication, open arrow, next peer review

Preflight read the November 14 MCSP directive first, followed by November 13 replacement, both full root proof trackers (including authentic 1,051,196-character `proof2.txt` blob), complete 2,545,859-character canonical `main.tex` blob, latest issue #3, `AGENTS.md`, `CODEX.md`, research skill, all five newest TMR handoffs and relevant original TMR-4 code/raw, Claude ONETAPE, threshold affine-kernel and FIBER27 controls. Root trackers remain **OPEN**, with **NO MATERIAL CHANGE**, and `main.tex` remains TMR-5-owned.

**Exact outstanding transfer:** Replace the source-independent evaluation-oracle-only hypothesis by a theorem covering every correct uniform deterministic SAT decider that can read formula syntax, adaptively reread complete inputs, share preprocessing, and use arbitrary compact or algebraic representations; then derive an actual one-way-input/one-work-tape `N^{1.01}` lower bound on **ordinary** `MCSP[N^mu]` at the required small fixed `mu`. Neither transfer has been proved.

**Peer request:** TMR-4 independently inspect the conditioned `M-b_0` denominator and counterexample for uncharged shared preprocessing; TMR-5 independently implement exact sharpness and audit source-independence, full sharing and target Gap-MCSP promises. TMR-1 check CHMY threshold; TMR-3 review oracle-query versus physical one-tape charge. Do not promote to root trackers or canonical `main.tex` until peer-reviewed. No tasks changed. **P versus NP remains OPEN.**
