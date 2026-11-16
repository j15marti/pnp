# TMR-3/065: canonical checkpoint reconstruction without storing the future-live frontier

November 16, 2026, Pacific. Track B / TMR-3 / PNP Time-Space Tradeoffs.
Status: PROVED/EXACT in the declared fixed finite-state one-write model, independent mathematical review OPEN; executable evidence COMPUTATIONAL. P versus NP OPEN.

## Candidate, quantifiers, falsifiers, and integration

Named dependency C3-PINNED-CONVERTER-FRONTIER-REPAIR, alternative to retaining W complete work blocks in /063. For EVERY fixed finite Q,R and deterministic tables delta:Q x {0,1}->Q, omega:Q x {0,1}->{0,1}, rho:R x {0,1}->R, out:R->{0,1}, EVERY even b>=2 and EVERY authentic payload y in {0,1}^{b^3}, construct the blank-start four-work-tape boomerang with a genuinely written finite-state-transduced PATH and a read-only reverse pass. Show uniform source-only access to all canonical work-cell bits at arbitrary times; integrate that provider with authentic public graph indices and a complete sequential output evaluator. Falsifiers fixed before source review: F1 source-prefix replay fails to reconstruct a written symbol; F2 public head/clock phases or boundary alignment fail; F3 source rereads, indices, retention, caches or Q requests are unpaid; F4 a chronological restricted evaluator is falsely called a generic Cook-Mertz speedup. The original Williams paper is [1], and /064 is the specific physical controller.

## Fixed authentic program and graph

Valid source x=1^(b-1)0 y has N=b+b^3 bits, even b>=2, |y|=M=b^3. An actual sequential parser checks header, payload length and trailing characters, rejecting malformed encodings. The fixed machine has three physically bounded bouncing-clock tapes and one initially blank PATH tape. It bootstraps in b steps, runs M outbound steps, b turnaround steps, M return steps and b terminal steps. In the outbound pass q_(k+1)=delta(q_k,y_k) and actual work cell PATH[k] receives v_k=omega(q_k,y_k). Return physically reads PATH[M-1],...,PATH[0] and accumulates r<-rho(r,v), finally outputs out(r). All finite tables are fixed in the machine's finite control, not input-dependent advice. All work-block crossings occur at multiples of b and source acquisition is paid.

The movement word is PUBLIC, input-value independent and has exactly one candidate K=1. Put m=b^2 and B=t/b=2m+3, t=2M+3b. The three clock heads are always in block 0. PATH is at block z(3,j)=0 for j=0; j-1 for 1<=j<=m; m for j=m+1; 2m+1-j for m+2<=j<=2m+1; and 0 at j=2m+2. The authentic frontier is exactly W=m+3, regardless of omega or rho, since the same m written PATH blocks are revisited. At even b>=12, b>=ceil(log2 t) and b=Theta(t^(1/3)). High W persists when the graph is unique.

## Canonical provider theorem, proved in the restricted model

Let tau be the count of COMPLETED physical steps, 0<=tau<=t, and a>=0 be a PATH cell. The exact count of completed outbound writes is w(tau)=min(M,max(0,tau-b)). Define v_a by scanning the ORIGINAL payload from its first bit through y_a with a fixed q-register and the genuine delta/omega tables. Then the work-tape content is

  PATH(tau,a)= v_a if 0<=a<w(tau); BLANK otherwise.

Clock tapes have only their real bootstrap endpoint symbols. Their head positions are source-independent and calculated by a bounded counter simulation or exact half-sweep arithmetic. Source-head position and PATH position are determined by phase counters. A finite-control checkpoint r(tau), if requested, can be reconstructed by folding rho over the actually completed reverse reads, replaying each relevant v_a. No physically preloaded checkpoint is claimed.

Proof: induction on outbound writes gives the true q_k from the original-source prefix and the true unique work-cell write v_k. No PATH cell is later overwritten. The pre-write blank and post-write bit formula is therefore exact for every tau and a. The clock/graph schedule is independent of y. Induction through reverse reads then proves that rho receives exactly the true cell values and produces out(r_M), for both Boolean labels. Source grammar rejection is performed before service access.

A conventional local-input-head bit-machine spends O(N polylog N) worst-case time and O(log N) auxiliary workspace per arbitrary PATH work-bit query: this includes source-head restoration, prefix scanning and O(log N)-bit address counters. Clock content and head-position queries are similarly logarithmic-space, and can use O(t polylog N) time by direct public movement replay. A generic requested finite-control checkpoint is obtainable in O(N^2 polylog N) time and O(log N) space, because up to M reverse read values may each require a prefix replay. A full b-bit node value may be streamed with O(log N) additional provider space; materialization must charge a real O(b)-bit buffer.

## One SAME-EXECUTION complete virtual output simulator

Authenticate once, retaining b and N as O(log N)-bit counters; generate the one candidate graph on demand with exactly Q_G=4B stage-index calls, not an uncharged B-entry table; replay the outbound transducer logically without allocating PATH; during return request exactly Q_V=M actual canonical PATH bits in reverse order, updating the finite r-register; compare real stage blocks with the public movement schedule and emit the result. The scans, candidate discovery, Q, source-head seeks, counters, phase switches, retained state, output and malformed-input handling are performed on ONE standard deterministic sequential two-way-read-only-input machine.

The disjoint charged work partitions give

  T_virtual = O((N+Q_G+Q_V N+t) polylog(N+2)) = O(N^2 polylog N),
  S_virtual = O(log(N+2)),

where Q_G=4(2b^2+3), Q_V=b^3 and t=2b^3+3b. Arbitrary additional adaptive Q work-bit requests add O(Q N polylog N) time and O(log(N+Q+2)) workspace. Other graph-edge queries may cost O(B polylog N) per query to check prior visits. The reference original machine instead has T_original=Theta(N), S_original=M+1+3b=Theta(N) physically visited writable cells. These are separate honest realizations; no best-of-two resource splicing.

This is a COMPLETE restricted blank-start source -> graph -> canonical value provider -> chronological evaluator -> output chain, and a counterexample to treating high physical W as a universal content-storage necessity. It is NOT an improved generic NONASSOCIATIVE Tree Evaluation algorithm. Direct source-aware shortcuts remain legal and might be faster. The missing general HPV converter, arbitrary work-dependent last-writer service and improved Tree Evaluation stay OPEN.

## Actually executed independent finite audit

Standard-library CPython 3.13.5, revision tmr3-invertible-write-once065-v1, seed 202611160624, executed TWICE with byte-identical raw JSON: 96 valid source/controller cases, at b=2,4,6,8,10,12 and four FIXED transducer rules COPY, PREFIX_AND, PREFIX_XOR and NONLINEAR; 12,290 canonical checkpoint bit comparisons; 296 malformed controls; 120,042 assertions and ZERO failures. The audit checks genuine transduced reference arrays, sampled finite-control checkpoints, public head/block positions, clock endpoint symbols, exact W, Q_G=4B, Q_V=M, and terminal both-label outputs. Small widths below b=12 are structural tests only.

Actually executed source SHA256 76352ad9798669dfa34d2d5a1ad980b5e16fecc5ec249b3bd7a039e6ba0135ec; Git blob 68750c928e6e7031e62b50b7ef1d203a27ba68f6. Raw SHA256 7858ba24ec4f312d5f0d664c9f1b43cbeffb5814ce20d30ea4e17f7765bbe2a1; Git blob d7210978ddeb0034545438e9beaa921ede25fcde. The harness uses indexed Python strings and materialized reference arrays; the logarithmic bit-machine ledger is a symbolic proof, NOT measured Python workspace. The independent audit does not compile the full native physical transition table, the literal HPV converter or Cook-Mertz. External math review OPEN. Repository clone failed because github.com DNS was unresolved; repo preflight NOT run.

## Four gates and safeguards

DISJ sanity: PASS restricted, no rank-to-work inference. Relativization: NOT APPLICABLE WITH REASON to a separation, none claimed; BGS, algebrization and Natural Proofs remain open downstream audits. Simultaneous DTISP: PASS for each fully charged original and virtual whole machine separately; unrestricted SAT forbidden-pair transfer OPEN. Configuration counting: PASS as deterministic halting-run upper-bound consistency only; not a work lower bound or automatic randomized/quantum claim. All Horn, 2-SAT, affine/Gaussian, bounded-treewidth, equality, autarky, product, padding, auxiliary, unique-solution, selector, field/local-basis, charged isolation, compact-circuit, caching and source replay controls remain legal. Circuit-to-CNF growth, majority ties and quantum error models are not used here. /341 FAIL as full UNSAT authority; /386 RESTRICTED. P versus NP OPEN.

## ONE next load-bearing lemma

C3-GENERAL-LAST-WRITER-ORACLE: for a PINNED general HPV/Williams converter with arbitrary work-dependent overwrites, derive a charged source-reachable last-writer or recursively reconstructed value-bit provider that services ALL adaptive Q nonassociative tree queries without restoring the Wb materialized cache, with a genuinely improved evaluator and correct same-machine total time/peak space. This restricted transducer construction does not establish it.

References: [1] R. R. Williams, Simulating Time With Square-Root Space, arXiv:2502.17779v1, Section 3.2, https://arxiv.org/html/2502.17779v1, primary HTML inspected November 16 2026. [2] Cook and Mertz, Tree Evaluation Is in Space O(log n log log n), STOC 2024, Theorem 7 as quoted in Williams. [3] TMR-3/063 and /064, original restricted reports in stacked unmerged PRs #210 and #215.
