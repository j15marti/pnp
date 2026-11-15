# TMR-5/029: Polynomial-output MCSP-NO streaming control and transfer red team

**November 14, 2026, 17:50 PST, America/Los_Angeles.** Role TMR-5, Machine Bottleneck Redteam and Synthesis. **Status:** POLYREPEAT048 elementary symbolic **CANDIDATE/RESTRICTED**, independent TMR-1/TMR-4 mathematical review OPEN; finite native execution COMPUTATIONAL. **P versus NP OPEN.**

## What is genuinely new

TMR-4/033 (STREAMSHARE047) refuted multiplying worst-index complexity by the truth-table length when the generator's source already contains the whole N-bit target table (L=N). This report supplies a strictly stronger adversarial family: **for every fixed 0<mu<1**, a fixed uniform source-to-table streaming transducer takes a source of length **L=o(N)**, produces a target table of **polynomial length N=poly(L)** having ordinary MCSP NO complexity, and still uses **O(N)** charged time. Restarting a suitable indexed evaluator for every output position instead uses **Omega(NL)** source-bit reads. The counterexample directly narrows any attempt to repair the L=N objection merely by imposing polynomial output length or sublinear source length.

This is not an explicit efficiently recognizable family of MCSP NO strings: the source x is existentially high-circuit-complexity and supplied as input. No MCSP decision solver or SAT-to-MCSP reduction follows.

## Exact lemma POLYREPEAT048

Fix an arbitrary rational or real constant 0<mu<1. Choose and fix an integer q>=1 such that

$$
\beta=\frac{q}{q+1}>\mu.
$$

For each m>=1 set

$$
h=qm,\quad L=2^{h},\quad M=2^m,\quad n=(q+1)m,\quad
N=2^n=LM=L^{1+1/q}.
$$

Let x be the complete L-bit truth table of an h-input Boolean function g. Define the n-input Boolean function

$$
Y_x(u,v)=g(v),\qquad u\in\{0,1\}^m,\quad v\in\{0,1\}^{h}.
$$

Its explicit N-bit truth table consists of M identical consecutive copies of x. Under ordinary fan-in-two AND/OR/NOT gate count with free constants and unrestricted fanout,

$$
CC_{n}(Y_x)=CC_{h}(g).
$$

**Proof of equality:** Ignoring u gives the upper bound. Conversely, substitute the all-zero m-bit input for u in any n-input circuit for Y; the resulting h-input circuit still computes g with no more gates. No promise or hidden oracle is involved.

Let s=floor(N^mu). The standard elementary circuit-description count, for s>=1, is bounded by

$$
D(h,s)=(s+1)(h+s+2)[3(h+s+2)^2]^s.
$$

Since s<=L^{mu/beta} with mu/beta<1,

$$
\log_2D(h,s)=O(s\log(h+s))=o(L).
$$

For all sufficiently large m, D(h,s)<2^L, so some x has CC_h(g)>s. Every such x generates an **ordinary MCSP[s] NO** N-bit table Y_x, with NO requiring exact circuit size strictly greater than s. This is a counting existence claim, not a uniform procedure for finding x.

There is one fixed deterministic, finite-alphabet, **one-way read-only source input plus one locally moving two-way work tape and charged sequential output stream** transducer G_q, independent of x and m, which generates Y_x from x in **O(N)** physical transitions and O(L) peak writable work cells. The fixed program may depend on q but not on input length or the high-complexity source x.

**Charged implementation:** First copy x once, bit-by-bit, onto one finite-alphabet tape track in O(L) operations, preserving the left boundary. Determine h=log_2 L on the valid power-of-two lengths by h full sweeps of the L-cell counter track: each sweep retains every second still-active marker, and a short unary tally records the number of sweeps. These take O(Lh) movements, allow all input rereads and head reversals to be counted, and do not alter the data track. The fixed q divides the sweep tally, giving m=h/q. Construct M=2^m unary repetition markers by m doubling stages, with O(M+Lh) additional local moves including travel to the data region. Then mark one repetition marker per round and sweep the retained L data symbols from left to right, outputting one bit per cell, with a paid work-head rewind and marker update each round. M rounds cost O(ML+M^2), which is O(ML) since M<=L. Total

$$
T_{G_q}(x)=O_q(Lh+ML)=O_q(N)
$$

because for fixed q, h=Theta(log L) and M=L^{1/q} eventually dominates log L. Source bit reads are L; output writes are exactly N. Memory is O(L+M). For lengths not of the declared form the same program can halt with a fixed fallback label/output; no length-indexed advice is installed.

A separate fixed indexed transducer E_q(x,i) can parse n=(q+1)m bits of index i, extract the low h bits interpreted as j=i mod L, and scan the **source from its left origin** through x_j. On all lengths in this family, independently restarting E_q over every target index incurs exactly

$$
Q_{\rm restarted}=\sum_{i=0}^{N-1}(i\bmod L+1)=\frac{N(L+1)}2
$$

charged source reads, or Omega(NL) physical steps. The shared G_q requires only O(N) elapsed transitions. This is an explicit failure of any generic rule that multiplies the worst indexed bit-generation time by N to lower-bound **all** full-output generators. The comparison uses different declared algorithms to **refute an asserted universal implication**, not to transfer a time lower bound from one machine to another.

The stream processor does not evaluate CC_h(g), decide MCSP, or know which x are NO. It copies easy and hard x identically. This preserves the established LOCALPF045 bound on the circuit complexity of quickly **indexed** functions, and leaves hardness of ordinary MCSP **decision** untouched.

## Input, threshold and model firewalls

- Source encoding length is L bits, input arity of its Boolean function is h=log_2 L. Target input arity is n=(q+1)m, full target truth table length N=2^n. None is an arbitrary 3-CNF encoding length; in a future SAT application that source length must be denoted separately.
- Threshold s=floor(N^mu), mu fixed. If beta>mu, the counting margin is strict; at equality this argument gives no conclusion. The existential x may depend on m and need not be efficiently findable. The **transducer program G_q does not**.
- The target y is a NO instance for exact ordinary MCSP. No statement about Gap-MCSP, MKTP, partial/succinct MCSP, or low-threshold SAT reductions is transferred.
- Input access is local, one-way and charged; one single writable work tape stores x and unary markers on finite tracks. A write-only output stream has a charged output operation per bit. A separate read/write output tape is not secretly free.
- In the native experiment the work-head sweeping and L log L halving are **semantic charged proxies**, not an assembled finite-state Turing-machine executable. The all-length finite-state construction described above is a symbolic implementation argument subject to peer review.

## Independent audit of peer chains and dependency map

| Candidate arrow | Original evidence/status | Exact verdict after this run |
|---|---|---|
| TMR-1/031 LOCALPF045: local-head prefix and Pippenger-Fischer indexed circuit O(t log t) | research/agents/tmr-1/2026-11-14_1704_TMR1_LOCAL_PREFIX_PF_COMPOSITION031.md, CANDIDATE/RESTRICTED | **Not falsified.** Our high-CC repeated outputs have worst-index source traversal Omega(L), consistent with the indexed lower bound. Any new full-output inference requires a separate sharing lemma, now refuted even when L=o(N). |
| TMR-2/032 exact expected sparse-oracle minimax | research/agents/tmr-2/2026-11-14_1720_TMR2_EXPECTED_QUERY_MINIMAX032.md, PROVED/RESTRICTED pending review | The oracle theorem concerns distinguishing sparse supports by bit evaluations, not producing or classifying repeated hard tables. It supplies no post-input MCSP computation cost. No conflicting numerical bound found. |
| TMR-3/032 one-way MCSP prefix ingress | research/agents/tmr-3/2026-11-14_1728_TMR3_RANDOM_ONEWAY_PREFIX_INGRESS032.md, PROVED/RESTRICTED pending review | Linear input-ingress in explicit MCSP is compatible with O(N) whole-table **output**. It does not yield N^1.01 at small mu; sequential-ingress version of NETFRONT39's e<0.99 corridor is vacuous as TMR-3/032 states. |
| TMR-4/033 STREAMSHARE047 | research/agents/tmr-4/2026-11-14_1732_TMR4_STREAMING_OUTPUT_AMORTIZATION_FIREWALL033.md, PROVED/RESTRICTED pending review | **Strengthened** from L=N to L=o(N), N=poly(L), for any fixed mu<1, without a new decision or SAT implication. Counting and restrictions independently rederived. |
| TMR-5/028 source-query tail and local-head circuits | research/agents/tmr-5/2026-11-14_1650_TMR5_LOCALHEAD_AND_SPARSE_TAIL_AUDIT028.md, PROVED/RESTRICTED pending review | Consistent at their respective **query** and **indexed-circuit** scopes. Neither yields unrestricted 3-SAT machine time. |
| Earlier Claude ONETAPE/TPORT/DIRECTPRODUCT, affine Walsh, LSPV checker and Grok ARC | Original paths in the ledger below | Remain historical restricted evidence and falsifiers. No genuine source-compression or transfer theorem was promoted. |

**Retired inference:** "If the output is ordinary MCSP NO and has polynomial length N=poly(L) with L=o(N), its uniform full-output generation must cost Omega(N times a worst-index cost)." POLYREPEAT048 supplies a fixed-program countermodel. The stronger conclusion for the special case L=N was already retired by TMR-4/033; this report closes the obvious attempted repair based solely on input/output length disparity. This does **not** retire a stronger independently proved SAT-label-preserving reduction bound.

The strongest surviving conditional complexity chain, with every step scoped, is

$$
\mathrm{MCSP}[2^{\mu_1 n}]\notin \mathrm{DTIME}_1[N^{1.01}]
\quad\Longrightarrow\quad P\ne NP
$$

for the particular small existential mu_1 from Cheraghchi et al. The implication is published, while the antecedent is still **OPEN**. A known randomized N^{1.99} lower bound uses a different, larger mu_2. Restricted source-ingress, output-copy, indexed-compilation and network-simulation claims do not fill the antecedent.

An independent attempted SAT route would additionally need a **fully charged, both-label, uniform** reduction from 3-CNF of bit length L_sat to the exact MCSP variant with target length N=poly(L_sat), plus a justified decision-time lower-bound transfer. No such general bridge has been established here.

## Primary-source theorem matrix

| Original source, version, location | Exact model, threshold, input measure, hypotheses, result | Use and limitation |
|---|---|---|
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Theorem 1, printed p.23:3 [1] | Ordinary exact MCSP on N=2^n truth-table bits, circuit cap 2^{mu_1 n} for some **small** mu_1>0; deterministic one **two-way work tape** plus **one-way read-only input**. **Conditional:** not in DTIME_1[N^{1.01}] implies P != NP. | Unproved antecedent. Cannot substitute a query or full-output-generation lower bound. |
| Same paper, Theorem 2, p.23:3 [1] | Same explicit ordinary MCSP problem family but a **different larger** cap 2^{mu_2 n}, mu_2 close to 1, bounded-error **randomized** one-way-input/one-work-tape model. Proven MCSP not in BPTIME_1[N^{1.99}]. | Does not instantiate Theorem 1 at mu_1. |
| McKay, Murray, Williams, STOC 2019, Theorems 1.2 and 1.3, printed p.2 [2] | **Search-MCSP^A[s(n)]**, truth-table input N=2^n, time-constructible s(n)>=n, with poly-hierarchy oracle A. Thm 1.2 gives one-pass streaming search using nearly-linear in s space and nearly-quadratic update time with short Sigma_3SAT^A queries; Thm 1.3 states that failure of a poly(s)-space and poly(s)-update streamer for some A in PH implies P != NP. | Not the ordinary decision-MCSP theorem without a separate proof. |
| Pippenger, Fischer, JACM 1979, Theorem 4, printed p.379 [3] | O(h log h) combinational-network cost to simulate h steps of a fixed finite-alphabet one-dimensional-tape machine. | Background for LOCALPF045. No indexed-to-shared time lower-bound implication follows. Publisher/PDF text verified; PDF screenshot returned 403 and was not treated as visual confirmation. |
| Elementary gate-counting and restriction lemma, proof in this report | Finite fan-in-two gates, fixed q and mu<q/(q+1), source L=2^{qm}, target N=L^{1+1/q}. Existential NO sources; fixed G_q outputs replicated table in O(N) time. | CANDIDATE/RESTRICTED independent peer audit OPEN. No hardness assumption, no NP-hardness assertion. |

References: [1] https://doi.org/10.4230/LIPIcs.STACS.2021.23 (publisher PDF Theorems 1/2 visually checked, p.23:3); [2] https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf (original accepted PDF Theorems 1.2/1.3 visually checked, p.2); [3] https://doi.org/10.1145/322123.322138 and https://www.ccs.neu.edu/home/viola/classes/papers/PippengerF-Oblivious.pdf .

## Original-work ledger and hostile controls

- TMR-1/031 original report and native Python: research/agents/tmr-1/2026-11-14_1704_TMR1_LOCAL_PREFIX_PF_COMPOSITION031.md, experiments/tmr/tmr1_localpf_prefix045.py, original raw JSON. Distinguish fixed indexed evaluator E from shared generator G.
- TMR-2/032 original report, code, raw: research/agents/tmr-2/2026-11-14_1720_TMR2_EXPECTED_QUERY_MINIMAX032.md, experiments/tmr/tmr2_expected_sparse_query046.py, results/raw/tmr/2026-11-14_1720_TMR2_EXPECTED_SPARSE_QUERY046_RAW.json.
- TMR-3/032 original report, code, raw: research/agents/tmr-3/2026-11-14_1728_TMR3_RANDOM_ONEWAY_PREFIX_INGRESS032.md, experiments/tmr/tmr3_oneway_prefix046.js, results/raw/tmr/2026-11-14_1728_TMR3_ONEWAY_PREFIX046_RAW.json.
- TMR-4/033 original report, code, raw: research/agents/tmr-4/2026-11-14_1732_TMR4_STREAMING_OUTPUT_AMORTIZATION_FIREWALL033.md, experiments/tmr/tmr4_stream_share_gap047.js, results/raw/tmr/2026-11-14_1732_TMR4_STREAMSHARE047_RAW.json.
- TMR-5/028 original report and native source: research/agents/tmr-5/2026-11-14_1650_TMR5_LOCALHEAD_AND_SPARSE_TAIL_AUDIT028.md, experiments/tmr/tmr5_locality_tail_audit044.py.
- Historical original research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex, research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex, research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex; none is an unrestricted SAT lower bound.
- Compact-algebra controls: research/agents/tmr-2/2026-11-14_0823_TMR2_MAXSAT_WALSH_SIGN_ROBUSTNESS022.md; LSPV accepted SAT-source checker falsifier research/agents/lspv-3/2026-11-13_0727_LSPV3_615_HASH_BINDING_SOUNDNESS_COUNTEREXAMPLE.md; historical GROKPROOF/2026-10-31_0522_GROK_PROGRESS.md. Horn, 2-SAT, GF(2) Gaussian elimination, bounded treewidth, shared products, padding, renaming and auxiliary variables are not claimed hard by this copying construction. Easy all-zero/all-one source controls were executed.

## Executed reproducibility and publication status

**Native CPython on the model's working container:** exact source experiments/tmr/tmr5_polyreplication_audit048.py, immutable stdout results/raw/tmr/2026-11-14_1750_TMR5_POLYREPEAT048_RAW.json. **206 assertions, zero failures**, six (q,m) finite exact at-most-two-gate source classifications, source restriction tests, charged work-sweep/source-read/output-write counts, seven exact-rational exponent windows, and zero/one easy controls. The simulator models charged scans and halving passes, NOT a compiled Turing machine. Source SHA256 f43ae4a7a23e77c59d8a973ac560667cc843f0d262eeb00caf2173b976528250; raw SHA256 c786585b4101280cf1a57fa74c7cf7d505632a141f9f090e105f454c17a42b12. Exact native Git blob source 309f50c759d5df054866fa7b3ee94021c1919482, raw ad8a97a677ef7667164e098eca65a7e2ca0ceeb3. Finite evidence COMPUTATIONAL.

Preflight: current Nov14 MCSP directive read FIRST, SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a. Read Nov13 replacement, root proof1.txt full 28,714 characters SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, recovered **entire** authentic proof2.txt Git blob 1,051,196 characters SHA 930c5eeddafce656717f28055a7a9a755f44737c, and recovered entire canonical main.tex Git blob 2,545,859 characters SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. Also AGENTS.md/CODEX.md/repo skill, issue #3 through TMR-4/033, newest five TMR handoffs and cited original peer/Claude/Grok/LSPV work reviewed.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root main.tex rewrite: the new construction is deliberately CANDIDATE/RESTRICTED pending independent TMR-1/TMR-4 review, and does not close any P-vs-NP load-bearing arrow. No agent schedule or task modified.

**Peer requests:** TMR-1 check the single fixed local-tape G_q implementation, power-of-two length recovery and threshold quantifiers; TMR-4 check exact restriction preservation, NO-table counting, and the distinction from a both-label SAT reduction. TMR-2/3 check that input-ingress lower bounds cannot be used as post-ingress work. **Next falsification target:** demand an MCSP **decision** invariant, rather than a high-circuit-output generation invariant, that survives source x supplied on a short tape, arbitrary input rereads and compact algebra. Independently test any such invariant against fully paid one-tape simulations at the small CHMY mu_1 threshold.

END_OF_REPORT::TMR5::029::2026-11-14_1750_PST
