# TMR-2/027: Code-distance certificate theorem and faster one-tape zero-gate MCSP

**Pacific timestamp:** November 14, 2026, 12:21 PST. **Role:** TMR-2, Information Necessity. **Status:** PROVED/RESTRICTED elementary symbolic results, pending TMR-1/TMR-5 independent review; finite evidence COMPUTATIONAL; P versus NP OPEN. No schedules modified.

## 1. Preflight, original evidence, and new contribution

Read FIRST research/coordination/2026-11-14_MCSP_FIVE_AGENT_REVIEW.md (Git blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a), then the November 13 TMR replacement directive, AGENTS.md, CODEX.md, the pnp-research skill, all five TMR handoffs, latest issue #3, proof1.txt, proof2.txt, and root main.tex. The ordinary file endpoint supplied SHA but an empty body for proof2 and main.tex; retrieving the underlying Git blobs recovered all 1,051,196 and 2,545,859 characters, respectively. Proof1 had 28,714 characters. Exact blobs: proof1 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 930c5eeddafce656717f28055a7a9a755f44737c; main.tex 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34.

**Prior art, not newly claimed:**

| Original repository artifact | Scope |
| --- | --- |
| research/agents/tmr-2/2026-11-14_1123_TMR2_GAP_MCSP_HAMMING_CYLINDER026.md | Already proved the Hamming-cylinder YES query lower bound and exact depth 3N/4+1 for threshold zero, eta=1/4. |
| research/agents/tmr-5/2026-11-14_1155_TMR5_AFFINE_VS_NONLINEAR_STREAMING_REVIEW023.md and experiments/tmr/tmr5_zero_gate_stream028.py | Already gave a uniform length-blind one-way-input, one-work-tape MCSP[0] algorithm with O(log N) cells and O(N log^2 N) time. |
| research/agents/tmr-4/2026-11-14_1142_TMR4_GAPMCSP_AFFINE_KERNEL_CYLINDER027.md and research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex | Fixed source-independent GF(2)-affine sketches need high rank; does not bind nonlinear source-adaptive streaming summaries. |
| research/main/2026-10-20_2343_MAIN_QUERY_COVERAGE_FIBER27.md | Historical exact-MCSP sparse-query coverage theorem, distinct from the present general code-distance result. |
| research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex and research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex | Original restricted crossing-sequence, nondeterminism and portfolio facts; no automatic arbitrary-SAT transfer. |
| TMR-1/026, TMR-3/026, TMR-4/027, TMR-5/023 original reports | Circuit-threshold gaps, ordered-output padding retention, affine collision and a fast nonlinear decision control. |

**New relative to this corpus:** a general minimum-code-distance characterization of the exact deterministic YES query depth for *every* Hamming radius up to one quarter of the truth table in zero-gate Gap-MCSP, and an independent improved **O(N log N)** one-work-tape **physical-time upper bound**, by co-locating counter bits and projection-match flags. Neither proves a lower bound for the positive, growing circuit threshold in the CHMY magnification theorem.

## 2. CODEDIST27: an exact point-query theorem

Let C be a nonempty set of N-bit binary strings, with minimum pairwise Hamming distance d, and fix an integer r>=1 satisfying 2r<=d. Consider the promise problem YES=C; NO={y : d_H(y,C)>=r}. Strings at distance 1,...,r-1 are unpromised. One point query reads one arbitrary bit coordinate; off-query computation and memory are unrestricted.

**Theorem CODEDIST27 (PROVED/RESTRICTED).** Every deterministic adaptive exact promise decider queries at least N-r+1 distinct coordinates on **each** YES input before accepting. A decision tree with exactly N-r+1 coordinate queries on all promised inputs exists, provided that the finite C is available for comparison. The latter is a query-model existence result, not an efficient uniform algorithm for arbitrary supplied C.

**Lower-bound proof.** If an accepting transcript for x in C queries q<=N-r distinct positions, choose r unqueried positions and flip x there to obtain y. Deterministic adaptivity yields the identical accepting transcript. But d_H(y,x)=r, and for every other c in C, the triangle inequality yields d_H(y,c)>=d_H(x,c)-r>=d-r>=r. Therefore y is a promised NO, a contradiction.

**Matching query algorithm.** Query any fixed N-r+1 positions Q, and accept iff some c in C agrees with the observed bits. Every YES input matches. Every input that matches differs from some c on at most r-1 unobserved coordinates and so cannot be promised NO. Otherwise reject. Hence both promised labels are correct.

In a fan-in-two AND/OR/NOT circuit basis with free constants and positive input wires, NOT gates charged, the N=2^n truth tables computed with zero gates are exactly the two constants and n positive coordinate projections. At n>=2, distinct such truth tables have Hamming distance at least N/2. Consequently, for **every** 0<eta<=1/4 and r=ceil(eta N), the exact deterministic YES decision-tree query complexity of eta-Gap-MCSP[0] is

$$
q_{\mathrm{YES}}(N,\eta)=N-\lceil\eta N\rceil+1.
$$

The previous TMR-2/026 result at eta=1/4 is the special case 3N/4+1; the full radius parameterization and code lemma are the new extension. The result is NOT a one-work-tape runtime bound. A complete scan of N input bits is legal.

## 3. ODOMETER27: explicit uniform one-work-tape improvement

**Theorem ODOMETER27 (PROVED/RESTRICTED, independent review requested).** One fixed deterministic finite-control machine decides ordinary exact MCSP[0] for all valid N=2^n-bit truth tables, n>=1, and rejects malformed lengths, on an input interface consisting of one **one-way read-only input tape** and one **two-way read/write work tape**, with no advance n/N header, in O(N log N) transitions and O(log N) visited work cells. Therefore it also correctly decides the zero-gate eta-Gap-MCSP promise for every eta>0. Its code is finite and identical for every input length.

**Locally realizable invariant.** Before source symbol x_j, the work tape contains an adjacent array of cells B_i=(b_i,a_i) for binary counter bits i, where b_i=bit_i(j) and

$$
a_i=1\iff \forall k<j,\ x_k=\operatorname{bit}_i(k).
$$

Two prefix flags all0 and all1 are held in finite control. Initialize one work cell B_0=(0,1) and both flags true. Read the next source symbol v into finite control, advance the input head, and update the two flags.

On a single left-to-right work-tape sweep, with a one-bit carry c initialized to one, update for every cell:

$$
a_i\leftarrow a_i\wedge[v=b_i^{old}],\quad
b_i\leftarrow b_i^{old}\oplus c,\quad
c\leftarrow c\wedge b_i^{old}.
$$

If the carry persists beyond the last cell, append a new highest counter-bit cell (1,all0), with all0 already updated for the current symbol. This new bit first becomes nonzero at position 2^i; it was zero at all prior source indices, so the initialized projection-match flag is correct. Return the work-tape head to the leftmost cell in one sweep. Each cell is one symbol of a four-element work alphabet; the current source bit, carry and two prefix flags are finite control. Every work-head move and symbol update is a fixed number of machine steps; the current array has O(log(j+2)) cells. Thus the same fixed machine uses O(log(j+2)) operations for source symbol j, and summing gives O(N log N) time with O(log N) peak workspace.

On the right endmarker, scan the binary length counter and require a power of two >=2. At valid length N=2^n, the highest counter bit i=n was introduced only **after** the Nth input symbol; its projection-match flag must be excluded. Accept iff all0, all1, or one of flags a_0,...,a_(n-1) is true. This exactly recognizes all zero-gate tables. All nonpower-of-two lengths are rejected as malformed. The input can be revisited in a more general machine, but this construction does not reread it.

**Hostile conclusion:** Deterministic YES query lower bounds near N and fixed-affine rank Omega(N) do not imply either Omega(N) *workspace* or an N^(1+epsilon) physical decision-time lower bound for arbitrary one-way one-work-tape deciders. This new code gives a nonlinear compact summary and a near-linear physical decision algorithm for s=0. It does not contradict the source-independent affine impossibility, which has different quantifiers, nor the ordered *full-output* transducer bounds. In particular it does **not** address s=N^mu for any positive mu or prove an N^1.01 algorithm for those positive thresholds.

## 4. Reproducibility and hostile controls

**Actually executed native CPython**, 3.44 seconds, published source experiments/tmr/tmr2_odometer_stream027.py, SHA256 of published-source matching local executable 667bea8c98b18cb1a092ec774931504294d9834562036e33f442add7757d60de. Published raw results results/raw/tmr/2026-11-14_1221_TMR2_ODOMETER_CODE027_RAW.json; exact original raw SHA256 8c94a1c4baa2627bb31807f2c300147670d25aa8215bc52302a6912443047767. The published script was independently rerun in native Python after matching its Git blob to the local source with one blank-line normalization; its JSON output was byte-identical to the recorded raw JSON.

65,812 complete truth tables checked exhaustively for n=1,2,3,4, including 18 YES and 65,794 NO. In addition: 192 random larger truth tables at N=32/64/128, 40 malformed lengths, 38 YES/radius certificate cases, 15,292 adversarial r-bit flips, and every full truth table at each of the seven (n,r) query-acceptance checks for n=2,3,4 and 1<=r<=N/4; zero assertion failures. Work-tape invariants were independently compared with direct projection semantics. At N=16 the proxy uses a maximum of 5 writable data cells and records at most 208 local-transition accounting units. These are finite COMPUTATIONAL checks, **not** proof of asymptotic claims or an execution of a compiled native formal Turing machine.

Controls considered: nonlinear compact summaries (realized), constant/projection circuits and charged NOT, unpromised near-code inputs, malformed lengths, all valid sizes, full decision outputs versus full table outputs, arbitrary input rereading, caching, GF(2)/Gaussian elimination on XOR/Tseitin, Horn, 2-SAT, bounded-treewidth, renaming, sharing and disjoint products. The latter easy SAT subclasses are not claimed to be hard.

## 5. Primary theorem table and precise missing separation arrow

| Primary source / location | Exact problem and input measure | Model, threshold, premise and conclusion |
| --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Theorem 1, printed p.23:3, https://doi.org/10.4230/LIPIcs.STACS.2021.23 | Ordinary exact MCSP with full truth-table length N=2^n, size 2^(mu_1 n). | For **some sufficiently small fixed mu_1>0**, a lower bound excluding uniform deterministic DTIME_1[N^1.01] (one-way read-only input, one two-way work tape) implies **P!=NP**. Our s=0 upper bound is a different language. |
| Same, Theorem 2, printed p.23:3 | Ordinary exact MCSP at size 2^(mu_2 n), with mu_2>mu_1. | Unconditional exclusion of bounded-error randomized one-way-input one-work-tape BPTIME_1[N^1.99]. Different circuit threshold, not a premise for Theorem 1. |
| McKay, Murray, Williams, STOC 2019, Theorems 1.2/1.3, original https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf, pp.1-2 | N=2^n-bit **one-pass search-MCSP^A**, oracle-enhanced circuits, size s(n)>=n. | Theorem 1.2 constructs streaming with tilde-O(s^2) update time, tilde-O(s) space, and small Sigma_3SAT^A oracle calls. Theorem 1.3 says impossibility of any poly(s)-update, poly(s)-space algorithm for some time-constructible s and A in PH implies P!=NP. Neither applies to s=0 decision MCSP. |
| Oliveira, Pich, Santhanam, Theory of Computing 17(11), 2021, https://doi.org/10.4086/toc.2021.v017a011 | Gap-MCSP and Gap-MKtP families with theorem-specific circuit-size/approximation promises and N=2^n length. | Circuit/formula magnification results in their stated **nonuniform** models; no Gap-to-ordinary or s=0-to-s=N^mu transfer used here. |
| Chen, Hirahara, Oliveira, Pich, Rajgopal, Santhanam, ITCS 2020 / JACM 2022, https://doi.org/10.4230/LIPIcs.ITCS.2020.70 | Local-oracle circuit/formula models, locality and natural-proofs barriers. | Describes why localizable methods may not cross certain magnification frontiers. It does not forbid all new nonlocal methods or imply a tape-time lower bound. |

In particular, N=2^n is the explicit MCSP table length and n its input arity, whereas L is the encoded 3-CNF input length. The unrestricted P!=NP machine target remains: for each fixed uniform correct total deterministic multitape SAT decider A and every integer k>=1, C>0 and L0, there must be some valid F with |F|>=L0 and T_A(F)>C(|F|+1)^k. Nothing here rules out a single polynomial-time machine for general 3-SAT.

**Open load-bearing arrow:** show unavoidable **post-acquisition time** for exact positive-small-mu MCSP in CHMY's precise one-way-input/one-work-tape model, exceeding N^1.01, or give a fully resource-charged exact both-label threshold-transfer reduction satisfying the distinct mu values. The present upper bound and exact-query characterization do not supply this.

**Peer-review request:** TMR-5 verify the coupled-counter sweep and the high-bit endmarker exclusion; TMR-1 audit all radius, label and positive-threshold quantifiers; TMR-3 independently check O(log N) head travel per input bit. **Next TMR-2 target:** search for an exact source-dependent compact representative at s>=1 or growing s, and try to falsify it with a legally cheap uniform algorithm before proposing universal post-scan time obligations. TRACKERS REVIEWED; NO MATERIAL CHANGE. Canonical main.tex and all scheduled tasks unchanged.
