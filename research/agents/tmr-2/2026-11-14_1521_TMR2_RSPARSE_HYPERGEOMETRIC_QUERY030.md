# TMR-2/030: Hypergeometric r-witness locality for black-box MCSP transformations

**Time:** 2026-11-14 15:21 PST (America/Los_Angeles). **Role:** TMR-2 Information Necessity. **Status:** PROVED/RESTRICTED mathematical argument, independent TMR-4/TMR-5 review OPEN. Native finite tests COMPUTATIONAL. P versus NP OPEN.

## New contribution, distinguished from previous results

This run extends TMR-2/029's exact **singleton** (one satisfying assignment) adaptive oracle argument to an arbitrary **r-sparse satisfying-assignment set**. For deterministic source-independent transformations, even after adaptive global preprocessing, the mean Hamming change in a generated N-bit table has an exact hypergeometric ceiling. This yields a sharp required per-output query count for a proposed zero-UNSAT versus r-witness-SAT to Hamming-Gap-MCSP transformation. A separately verified proper-3-CNF family gives a syntax-aware escape; neither an unrestricted SAT lower bound nor the MCSP magnification premise is established.

Prior-work ledger of ORIGINAL artifacts and their status:

| Source | Existing result and scope |
| --- | --- |
| research/agents/tmr-2/2026-11-14_1417_TMR2_SHARED_ORACLE_PREPROCESS032.md; experiments/tmr/tmr2_shared_oracle032.py; results/raw/tmr/2026-11-14_1417_TMR2_SHARED_ORACLE032_RAW.json | PRIOR global adaptive preprocessing plus independently restarted output routines, singleton r=1, reference-distance bound. Original report/code/raw read, no exact re-execution here. |
| research/agents/tmr-4/2026-11-14_1336_TMR4_ORACLE_LOCALITY_GAP_MASK029.md | PRIOR per-output adaptive oracle locality without global preprocessing, singleton only. |
| research/agents/tmr-5/2026-11-14_1350_TMR5_MCSP_SYNTAX_CERTIFICATE_REVIEW025.md | PRIOR syntax-aware equal-length proper-3-CNF counterexample to unrestricted locality transfer. |
| research/agents/tmr-2/2026-11-14_1123_TMR2_GAP_MCSP_HAMMING_CYLINDER026.md and research/main/2026-10-20_2343_MAIN_QUERY_COVERAGE_FIBER27.md | PRIOR decision-tree YES cylinder counts. Not one-tape time. |
| research/main/2026-10-18_1757_SOURCEQUERY_SYNTHESIS10.md | PRIOR robust source-probe lower bound using different algebraic input distributions; no claimed all-machine transfer. |
| research/agents/tmr-1/2026-11-14_1504_TMR1_PADDING_WINDOW_NEAR_TIGHT029.md; research/agents/tmr-3/2026-11-14_1455_TMR3_TWOWAY_HEADER_NETWORK_BRIDGE029.md; research/agents/tmr-4/2026-11-14_1439_TMR4_POSITIVE_POWER_COMPILER_FIREWALL030.md; research/agents/tmr-5/2026-11-14_1452_TMR5_DUMMY_PADDING_UNIVERSAL_COLLAPSE026.md | PRIOR restricted padding, two-way versus one-way input, and direct-SAT compilation firewalls. No implication modified. |
| research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex; research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex; research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex | Historical crossing, multitape and portfolio barriers in different models. |
| research/agents/tmr-5/2026-11-14_0858_TMR5_GF4_CANCELLATION_MOMENT_TRACE020.md; comments/grok-4.7/2026-10-21/2026-10-21_0013_GROK_REVIEW.tex | Historical compact GF(4), Walsh/moment and semantic-fiber escapes. No unrestricted resource lower bound. |

Older Horn, 2-SAT, XOR/Tseitin Gaussian elimination, bounded treewidth, padding, clause renaming, sharing, cache/recompute, original signed-hypergraph reductions, native-checker counterexamples and abstract-interpretation failures remain preserved, not silently repaired or promoted.

## Exact black-box model

Let source arity be v, source functional domain size M=2^v, and source oracle f from v-bit assignments to {0,1}. Let f_empty be identically zero and f_S be the Boolean function whose 1-set is S, for any subset S of [M]. Let the generated output Y(f) contain N bits, with N=2^n only when interpreted as a *complete* MCSP truth table. Source SAT formula encoding length L is neither M nor N.

A deterministic, source-independent adaptive global preprocessing algorithm P makes at most b oracle evaluations, then retains arbitrary sigma. It has no formula syntax, nonuniform witness advice, or uncharged source-dependent computation. Output coordinate j is computed by a deterministic adaptive L_j making at most q additional oracle evaluations from sigma and j. **Each L_j is independently restarted from the common sigma**: no local transcript or state is shared with other outputs. Computation outside oracle evaluations is entirely unrestricted, so this is *only* a query-cost model, not a time-space bound.

Run P on f_empty. Let Q0 be its set of distinct queried source assignments, b0=|Q0|, B=M-b0, and qprime=min(q,B). Suppose 1<=r<=B. For a target-output Hamming distance d_H, define:

$$
H_{B,r}(q)=1-\frac{\binom{B-qprime}{r}}{\binom Br},
$$

where binomial(a,r)=0 for a<r.

### RSPARSE38-A: Exact hypergeometric locality (PROVED/RESTRICTED, peer review OPEN)

$$
\boxed{
\frac{1}{\binom Br}\sum_{\substack{S\subseteq [M]\setminus Q_0\\ |S|=r}}
\frac{d_H(Y(f_S),Y(f_\emptyset))}{N}
\le H_{B,r}(q).
}
$$

Consequently at least one r-sparse source outside Q0 has relative output distance at most H_{B,r}(q). For r=1 this specializes exactly to TMR-2/029, H_{B,1}(q)=qprime/B.

**Proof.** Every f_S with S disjoint from Q0 gives P the same all-zero reply transcript, hence identical shared state sigma0. Fix output j and list the distinct zero-oracle queries Q_j made by L_j outside Q0. This set has cardinality at most qprime. If S is disjoint from Q_j, the entire adaptive local transcript and output bit are the same on f_S as on f_empty, even if the code branches nonlinearly on its replies. A uniformly selected r-subset of B remaining source positions intersects Q_j with probability

$$
1-\frac{\binom{B-|Q_j|}{r}}{\binom Br}
\le 1-\frac{\binom{B-qprime}{r}}{\binom Br}.
$$

Each output-coordinate disagreement is bounded by this collision indicator. Sum over all j and all r-subsets and divide by N times binomial(B,r). This proves the inequality. QED.

### RSPARSE38-B: Exact conditional Gap-MCSP transfer requirement

For GapMCSP-Ham(n,s,eta), YES is circuit complexity at most s and promised NO is Hamming distance at least eta*N from *every* <=s-gate truth table. If Y(f_empty) is a YES truth table and **every** Y(f_S), |S|=r, is a promised NO instance, the necessary condition is

$$
\boxed{\frac{\binom{B-qprime}{r}}{\binom Br}\le1-\eta.}
$$

By the ordinary union bound, a weaker necessary inequality is q>=eta*B/r. For r=1 the exact condition is q>=eta*B. When r grows, the necessary local query count can be much smaller than the unique-witness condition. This does not establish existence of the hypothesized reduction, does not transfer MCSP thresholds, and says nothing about its physical machine runtime.

### RSPARSE38-C: Sharpness as a reference-distance bound

With no global preprocessing, create one output coordinate for **each q-subset Q of [M]**, and set its bit to OR of the q oracle evaluations indexed by Q. Then N=binomial(M,q). The zero oracle produces all zeros. For each r-subset S, exactly binomial(M-r,q) coordinates remain zero. Thus

$$
\frac{d_H(Y(f_S),Y(f_\emptyset))}{N}
=1-\frac{\binom{M-r}{q}}{\binom Mq}
=1-\frac{\binom{M-q}{r}}{\binom Mr},
$$

exactly meeting the RSPARSE38-A bound. For any b0, the same design over the B unqueried positions gives conditional equality. When q=1 and b0=0, N=M=2^v is a valid power-of-two truth-table length and the reference distance is r/M. For other q, binomial(M,q) is not necessarily a power of two. **The sharpness construction does not guarantee that any nonzero output belongs to the Gap-MCSP promised NO class**, so do not mistake this for a reduction.

## Hostile short proper-3-CNF source

For v>=3 choose y,z as auxiliary variables, and c in {1,...,v-2}. For every forced variable x_i, include the four clauses (x_i OR y OR z), (x_i OR y OR NOT z), (x_i OR NOT y OR z), and (x_i OR NOT y OR NOT z). Every clause contains three distinct variables. There are exactly 4c clauses and 2^(v-c) satisfying assignments. Append the four analogous clauses with NOT x_0, and the formula becomes UNSAT. That contradiction is directly visible from formula syntax, without querying all 2^v assignments. The formulas in this particular hostile control have different encoded lengths, so this is *not* a claim of an equal-length hardness reduction. TMR-5/025 already tested an equal-length syntax escape. Compact algebra, Horn/2-SAT and bounded-treewidth algorithms are additional legitimate hostile examples.

## Primary-source theorem and model matrix

| Primary paper, exact location/version | Exact input, model, threshold, promise/hypothesis | Conclusion and scope |
| --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, **Theorem 1, p.23:3**, https://doi.org/10.4230/LIPIcs.STACS.2021.23 | **Ordinary exact MCSP[2^(mu*n)]**, N=2^n *complete* truth table, deterministic one-way read-only input and one two-way work tape; some sufficiently small fixed positive mu, conditional exclusion from DTIME_1[N^1.01] | P != NP if the **unproved** lower-bound premise holds. Same paper **Theorem 2**, p.23:3, proves randomized two-sided error N^1.99 exclusion for a **different, larger mu close to 1**, not the magnification threshold. |
| Same CHMY paper, Theorem 3, p.23:4 | For every mu>1/2, ordinary MCSP[2^(mu*n)], randomized one-tape oracle machine with short N^o(1) oracle strings, for any oracle | Exclusion from BPTIME_1^O[N^(1+muprime)] for some muprime>0; restricted model, threshold and exponent. |
| McKay, Murray, Williams, STOC 2019, **Theorems 1.2 and 1.3**, pp.2-3, https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf | One-pass **search-MCSP^A** on complete N=2^n table, oracle-gate circuits, s(n)>=n, Sigma_3SAT^A short queries, ~O(s) space, ~O(s^2) update; conditional lower bound for any polynomial-in-s update and space, s time-constructible and A in PH | P != NP under the search-streaming lower-bound premise. Not an ordinary decision-MCSP lower bound. |
| Oliveira and Santhanam, ECCC TR18-139 (2018), https://eccc.weizmann.ac.il/report/2018/139/ | Approximate/average-case decision MCSP with size 2^(sqrt(n)), conditional formula-model lower bounds | Conditional stronger circuit/formula separations; no transfer assumed. |
| Chen et al., ITCS 2020, abstract/introduction, https://doi.org/10.4230/LIPIcs.ITCS.2020.70 | Hardness magnification and locality barriers in specific proof techniques | Context only; no unrestricted theorem imported here. |
| Allender and Hirahara, MFCS 2017, publisher abstract, https://doi.org/10.4230/LIPIcs.MFCS.2017.54 | MCSP/MKTP approximation, some conditional one-way-function conclusions and nonuniform/restricted reductions | No ordinary MCSP NP-completeness claim or threshold-preserving gap transfer. |

These first two primary PDFs were inspected at the printed pages. Other literature is used only within the publisher-verified abstract scope. No oracle, circuit threshold or promise is silently substituted.

## Actual execution and reproducibility

**Native CPython exact source:** experiments/tmr/tmr2_sparse_hypergeo038.py, git blob cde6d9abaebe1924840c503a6f03d1117de45513, SHA256 94a07e8fd31f23506c346fc144287926e8c2d3f20cf4abce48db00de9f9c10fb.

**Immutable native stdout:** results/raw/tmr/2026-11-14_1521_TMR2_RSPARSE_HYPERGEO038_RAW.json, SHA256 7edeb4ac6a27f720c9cb0d03359fa48f70f46235294a22081d0d30971e27694a. Seed 202611141518.

**27,316 assertions, zero failures** in the final native run: 1,104 adaptive parameter configurations, 12,480 r-sparse source executions, 81,223 output-coordinate comparisons, 308 exact sharpness parameter cases, 12,172 full-subset equalities, and 42 proper-3-CNF syntax controls. Initial verifier had a wrong orientation in its sharpness check (binomial(B-q,r) instead of the actual unhit-q-subset count binomial(B-r,q)); that first local run failed. The test was corrected before the final native pass. The mathematical equality uses their corresponding denominators. These executions are semantic finite computations, not a physical one-tape machine or asymptotic proof. No native finite-state-TM compiler was executed.

## Preflight, epistemic status and next target

Current MCSP directive read FIRST and rechecked at SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a. Then Nov13 TMR replacement, AGENTS, CODEX, pnp-research skill, newest five TMR handoffs, issue #3, original TMR/Claude/Grok/legacy work, authentic full proof1 28,714 bytes (blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343), proof2 1,051,196 characters (recovered Git blob 930c5eeddafce656717f28055a7a9a755f44737c), and root main.tex 2,545,859 characters (recovered Git blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34). A local repository preflight script was not executed because no local clone was available; the required current GitHub source files were read. TRACKERS REVIEWED; NO MATERIAL CHANGE. TMR-5 owns root main.tex, which is unchanged.

The gap to an unrestricted P-vs-NP proof is still substantial. A single fixed total uniform deterministic 3-SAT decider A must be handled on *all valid encoded F*, allowing all polynomial space, input rereading, syntax preprocessing, compact algebra and sharing. RSPARSE38 constrains only a source-independent evaluation-oracle architecture with independently restarted local output routines; it yields query counts, not an N^1.01 small-mu ordinary-MCSP one-work-tape lower bound or a superpolynomial 3-SAT time bound.

**Next:** TMR-5 independently audit the hypergeometric denominators, sharpness and actual Gap-MCSP promises. TMR-4 test source-dependent syntax-aware global transformations. TMR-3 charge full output and network transfers, TMR-1 check circuit parameter/exponent thresholds. TMR-2's next target is a genuinely *fully shared adaptive* source-query transducer with charged total-query versus output-work accounting, without assuming a per-output restart.

No scheduled agent created, revived or modified. P versus NP remains **OPEN**.

END_OF_REPORT::TMR2::030::2026-11-14_1521_PST
