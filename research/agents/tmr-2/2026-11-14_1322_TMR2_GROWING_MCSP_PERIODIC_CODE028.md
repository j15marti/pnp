# TMR-2/028: A growing-threshold MCSP YES code with maximal query depth and sub-1.01 one-tape recognition

**Date:** 2026-11-14 13:22 PST (America/Los_Angeles). **Role:** TMR-2, Information Necessity. **Status:** elementary symbolic **PROVED/RESTRICTED candidate pending independent review**; tests **COMPUTATIONAL**. **P versus NP remains OPEN.**

## 1. Preflight, prior-work ledger, novelty

Read FIRST research/coordination/2026-11-14_MCSP_FIVE_AGENT_REVIEW.md on main, blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a. Then reviewed the 2026-11-13 TMR replacement directive, AGENTS.md, CODEX.md, pnp-research skill, all five current TMR handoffs, latest issue #3 through TMR-5/024, proof1.txt, proof2.txt and canonical main.tex. Root proof1 has 28,714 characters (SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343). Large-file Git contents reads were empty; Git blob reads recovered complete proof2 (1,051,196 characters; SHA 930c5eeddafce656717f28055a7a755f44737c) and main.tex (2,545,859; SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34). No tracker or main.tex edit is justified.

| Original path | Status and distinction |
| --- | --- |
| research/agents/tmr-2/2026-11-14_1221_TMR2_ODOMETER_CODE_CERTIFICATE027.md and experiments/tmr/tmr2_odometer_stream027.py | **PRIOR:** exact minimum-distance/query theorem and length-blind one-tape MCSP[0] O(N log N) algorithm. Neither covers growing thresholds. |
| research/agents/tmr-4/2026-11-14_1243_TMR4_LENGTH_BLIND_FIXED_GATE_COFACTOR028.md and experiments/tmr/tmr4_fixed_gate_stream028.py | **PRIOR:** fixed-gate cofactor inheritance, finite semantic-mask tests, not unrestricted growing-threshold MCSP. |
| research/agents/tmr-5/2026-11-14_1259_TMR5_BOUNDED_ENVELOPE_REVIEW024.md and experiments/tmr/tmr5_bounded_envelope029.py | **PRIOR:** bounded gate-cap schedules, independent semantic audit, not growing circuit threshold. |
| research/agents/tmr-4/2026-11-14_1142_TMR4_GAPMCSP_AFFINE_KERNEL_CYLINDER027.md and research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex | **PRIOR:** source-independent affine sketch lower bounds, not nonlinear adaptive computation lower bounds. |
| research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex and 2026-10-28_1326_CLAUDE_TPORT-0001.tex | **PRIOR:** one-tape crossing sequences, nondeterministic limitation and restricted portfolio resource barriers. |
| research/agents/tmr-1/2026-11-14_1200_TMR1_MCSP_GATE_SPECTRUM_RESOLUTION026.md and research/agents/tmr-3/2026-11-14_1228_TMR3_MCSP_MOBILE_HEADER_FUSION027.md | **PRIOR:** padding/threshold mismatch and one-tape header construction caveats; no SAT or general MCSP transfer. |

**Genuinely new relative to these reports:** exhibit an explicit growing-circuit-size MCSP YES *subclass*, of size exponentially large in a positive power of N, whose exact deterministic YES coordinate-query depth is the maximum possible N, but which has a fixed uniform **length-blind one-way-input plus one-work-tape** both-label recognition algorithm in O(N^1.005) time. This is a rigorous countermodel to inferring a CHMY time lower bound from candidate multiplicity, maximal query depth, and positive growing MCSP circuit-size membership **alone**. Periodicity recognition itself is standard and no general scientific priority claim is made for the language.

## 2. Exact construction, circuit size and information theorem

Let n>=1 denote circuit input arity and N=2^n the full truth-table length. This is not a 3-CNF source encoding length L. Fix a rational number 0<nu<1/100, e.g. nu=1/200. Set

$$
h=\lfloor \nu n\rfloor,\qquad k=2^h,\qquad
\mathcal C_{\nu,n}=\{x\in\{0,1\}^N:x_j=x_{j\bmod k}\ \text{for every }0\le j<N\}.
$$

Index assignments by binary integers; the h low-order variables change inside each length-k block. The language consists of all strings obtained by repeating an arbitrary k-bit block N/k times.

**PERIODCODE28-A (elementary restricted facts):**

1. Exactly 2^k words lie in C at each n. The minimum pairwise Hamming distance is d=N/k. A difference in one of k pattern positions repeats N/k times.
2. Every word in C is a complete truth table for an n-input Boolean function with a fan-in-two AND/OR/NOT circuit of at most 3(k-1)+h gates, with free constants and input wires and unrestricted sharing: form a complete depth-h multiplexer tree, using two AND gates and one OR for each of its k-1 internal multiplexers, with the h input negations shared, and set the k leaves to the source pattern. Therefore, for any fixed mu>nu, eventually

$$
\mathcal C_{\nu,n}\subseteq \mathrm{MCSP}[\lfloor N^\mu\rfloor]_{\mathrm{YES}}.
$$

This is a **one-direction inclusion only**, not an all-label reduction.
3. Every exact deterministic adaptive **coordinate-query** decider for the language C must read all N distinct coordinates on **every YES word**. If an accepting transcript omits one coordinate j, flipping that bit yields a NO word because N/k>=2 repeated occurrences of the same residue formerly agreed, while the deterministic transcript is unchanged. Reading N coordinates suffices in the unrestricted off-query computation model.
4. For the **different, explicit distance-promise problem** YES=C and NO={z:dist(z,C)>=r}, 1<=r<=N/(2k), the exact deterministic YES-coordinate-query complexity is N-r+1 by the already established TMR-2/027 CODEDIST27 theorem. This is an instantiation, not a newly claimed general coding theorem.

Consequently |C|=2^{Theta(N^nu)} for fixed nu>0; its YES codeword multiplicity is enormous, yet its exact coordinate-query depth is N. These facts do not control post-input computation on a single tape.

## 3. Uniform one-physical-tape upper bound with charged input

**PERIODCODE28-B (symbolic restricted recognition construction, peer-review OPEN):** For each fixed rational 0<nu<1/100, there is one finite uniform total deterministic machine, with one **one-way read-only input** and exactly one **two-way read/write finite-alphabet work tape**, no input-length header or advice, that decides the full C language (both YES and NO) and rejects malformed non-power-of-two lengths with

$$
T(N)=O(N\log N+Nk)=O(N^{1+\nu}),\qquad S(N)=O(N).
$$

Construction with all charged work:

1. Copy the input's N bits sequentially onto the work tape with a left marker, one work symbol per source bit, O(N) transitions. This deliberately uses N writable cells. No free second input copy or random access.
2. At EOF, use a fixed spare marker track and O(log N) full forward-and-return sweeps to halve the number of marked data cells on each sweep. Reject a non-singleton odd count. This recognizes N=2^n, and a unary sweep counter produces n. A fixed finite modular counter for the denominator of nu determines h; a marker segment is doubled h times to locate the first k=2^h cells. O(N log N) transitions, counting scratch marks/reversals. No unbounded-word unit-cost operation.
3. Copy the first k data bits to a template track on those same k physical cells. For each next k-bit source block, move the whole length-k template **on the same tape** right by k positions, compare its k bits with the unmodified raw data track, and reject on any mismatch. A one-position shift processes template bits right-to-left, requiring O(k) head moves/writes, so a k-position shift costs O(k^2). There are N/k-1 blocks. Their total cost is O(Nk). The implementation uses only a fixed finite alphabet with tracks (data bit, template bit/blank, length-marker) and on-tape markers/counters; it never rereads the input.

Because k=2^{floor(nu n)} is between N^nu/2 and N^nu, log N=O(k), and time is O(N^{1+nu}). The source copy and length detection are charged, the program is identical at every length, and arbitrary NO patterns also terminate within this time. For nu=1/200 the bound is O(N^1.005), strictly below N^1.01. The N-space bound is allowed by the CHMY one-work-tape model.

**Evidence limitation:** the published Python uses a locally charged moving-head, finite-track *proxy* for storage, halving and all template movements; Python loop indices and arithmetic orchestrate the proxy, and there is no native compiled finite transition-table execution. The uniform finite-control compiler is argued symbolically. Hence retain PROVED/RESTRICTED as candidate and request independent one-tape audit.

## 4. A precise failed implication, and why P versus NP is still open

The following combination is realizable for *the same explicitly constructed language*, at any fixed positive mu>nu:

$$
|\mathcal C_{\nu,n}|=2^{\Theta(N^\nu)},\quad
q_{\mathrm{YES}}(\mathcal C_{\nu,n})=N,\quad
\mathcal C_{\nu,n}\subseteq\mathrm{MCSP}[N^\mu]_{\mathrm{YES}},\quad
T_{\mathcal C}(N)=O(N^{1+\nu}).
$$

Thus **superpolynomially many growing-threshold MCSP YES instances, maximal deterministic point-query depth, and a circuit-complexity size bound do not alone imply one-tape time N^1.01 lower bounds**. A nonenumerative source-dependent comparison of repeated blocks defeats that inference. The literal per-candidate-flag method would have at least 2^k flags for this subclass, but the problem can be decided without enumerating members.

Critical limitation: the C complement contains both small-circuit functions outside C and high-circuit functions. The periodicity decider does NOT decide ordinary MCSP, does NOT preserve its NO label, and cannot be used as an ordinary MCSP threshold reduction. This is not an upper bound or lower bound for full MCSP[N^mu]. Nor is it a lower bound on arbitrary deterministic SAT machines: the required target quantifies over one fixed correct total multitape 3-SAT decider A for ALL source lengths L, every k0>=1, C>0,L0, and some long valid F. No arrow toward that target is closed.

**CHMY exact outstanding arrow:** Cheraghchi et al. STACS 2021 Theorem 1 requires ordinary full-table MCSP[2^{mu n}] **not** in deterministic one-way-read-only-input/one-work-tape O(N^1.01) time for a particular small fixed positive mu; that would imply P!=NP. CHMY Theorem 2 proves a much stronger randomized lower-bound exponent 1.99 only at a **different, larger threshold**, so it cannot be substituted. The code's mu can be arbitrarily small, but it is still only a YES subclass.

## 5. Primary-source theorem/version matrix

| Primary location | Exact input measure, problem, model, threshold, premise, conclusion |
| --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, STACS 2021 [publisher PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol187-stacs2021/LIPIcs.STACS.2021.23/LIPIcs.STACS.2021.23.pdf), **Theorem 1, p. 23:3** | Exact ordinary MCSP on full truth table N=2^n, threshold 2^{mu n} for some sufficiently small positive mu; deterministic one-way read-only input plus one two-way work tape, O(N^1.01) time exclusion as hypothesis, concludes P!=NP. Premise OPEN. |
| Same paper, **Theorem 2, p. 23:3** | Exact ordinary MCSP on full N-bit table with different large positive mu close to 1; randomized two-sided error one-way-input one-work-tape, unconditionally excludes BPTIME_1[N^1.99]. Not the threshold of Theorem 1. |
| Same paper, **Theorem 3, p. 23:4** | For each 1/2<mu<1, oracle randomized one-way-input one-work-tape, all oracle query lengths N^{o(1)}; excludes N^{1+mu'} for some mu'>0. Restricted short-oracle-query barrier, not general tape-time impossibility. |
| McKay, Murray, Williams, *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*, STOC 2019 [original manuscript](https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf), **Theorems 1.2 and 1.3 pp.2-3** | N=2^n-bit **search-MCSP^A**, s(n)>=n, oracle-enhanced circuit outputs, streaming oracle-assisted upper bound, and conditional magnification for some A in PH. Different output/promise/model, no transfer used. |

No ETH/SETH/cryptographic premise, no false ordinary-MCSP NP-completeness assumption, no Gap-to-ordinary, MKTP-to-MCSP, partial/succinct-to-explicit, or SAT-to-truth-table free expansion.

## 6. Actual tests, peer request and next target

**Actually executed native CPython** in one bounded invocation, deterministic seed 20261114: source experiments/tmr/tmr2_periodic_code028.py, raw results results/raw/tmr/2026-11-14_1322_TMR2_PERIODIC_CODE028_RAW.json. Code SHA256 37dd60c73a19128b7c1f5766a1f40659e58504ff78da502f824c3d9abdbcd455; raw SHA256 7fbfe34fd6ca7a5baea8bac607f7deb586ace3948bddf4de45a5f962cd7890be. 2,367 charged physical-head proxy examples, 8,189,818 head/cell operation units, 78,834 single-position template shifts, 2,920 adversarial Hamming flip controls, 39 malformed lengths, 21 exact minimum-distance controls, 5,368 recorded check groups, **zero assertion failures**. Complete all-table tests for N<=8 in three denominator schedules; exhaustive codewords where k<=8; seeded positives/negatives and random inputs through N=128. Finite cases only; the n>=200 asymptotic range for nu=1/200 was not executed. This is COMPUTATIONAL evidence, not an asymptotic test.

Hostile controls: both labels of C, alternate nonperiodic *low-circuit* functions, malformed lengths, all one-bit neighbor flips, binary source length, paid work head and input copy, multiple circuits sharing the same compact periodic form. Horn, XOR/Tseitin with Gaussian elimination, 2-SAT, bounded treewidth, products, variable renaming, auxiliary variables and source-adaptive nonlinear computations remain viable shortcuts, not excluded by this construction.

**Peer-review request:** TMR-3 audit the claimed O(N log N+Nk) physical tape compiler with no extra work tape or length header. TMR-1 check exact 3(k-1)+h multiplexer count and mu>nu threshold constants. TMR-5 independently falsify or verify one-head template movement and ensure no both-label MCSP transfer leaks into the conclusion. **Next TMR-2 target:** representation-independent *post-acquisition* processing for **the whole** small-positive-mu ordinary MCSP language that survives periodic/structured YES controls, adaptive compact summaries, input rereads and fully charged reductions.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex unchanged. No scheduled tasks modified. P versus NP remains OPEN.

END_OF_REPORT::TMR2::028::2026-11-14_1322_PST
