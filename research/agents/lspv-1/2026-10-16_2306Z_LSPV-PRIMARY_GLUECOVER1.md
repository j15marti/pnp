# PRIMARY RESOURCE-CONTRACTION: GLUECOVER1
Date: 2026-10-16 23:06 UTC / 2026-10-17 08:06 Asia/Seoul
Status: P versus NP OPEN.

PROPOSALS BEFORE SEARCH: (1) trace checkpoint shielding, (2) assumption-gated SAT self-reduction, (3) static circuit/RAM trace windows, (4) serial versus retained-state resource ledgers.

PROJECT/LITERATURE REVIEW: Read project through RACEFLIP1, GitHub research/review/STATUS.md and CROSS-TRACK INDEXDESCRIPTOR33, Drive MAIN LSPV/RMV and SIM-2 recursive-tableau no-go, ChatGPT Library WRAPPERCHARGE1 and WRAPPER-COVERAGE2, and primary FLMV Cor. 5.8 with actual PDF and machine model; Cook 1971; Savitch 1970; Williams STOC 2024/2025. FIXED-PREFIX-DELAY1 was already proved elsewhere and is not represented as new.

GLUECOVER1, PROVED/EXACT IN DECLARED MODEL (independent peer review pending):
Let B be an arbitrary fixed correct deterministic SAT decider, and A_D be its extensionally identical implementation that spends N^D steps in an explicit no-op loop before running B. If P=NP, A_D remains a polynomial-time SAT decider for each fixed D. Consider an A-dependent SAT-child constructor that faithfully UNROLLS every A_D transition, placing at least one distinct logical ordinary-CNF encoding position per tick and using no multi-step transition summary. Suppose it emits at most N^(g+o(1)) children, each of logical length at most N^(lambda+o(1)). Counting the N^D unrolled ticks gives N^D <= N^(g+lambda+o(1)), hence NECESSARILY D<=g+lambda. At (g,lambda)=(3/5,1/2), D=2 defeats faithful coverage: q_needed >= N^(3/2-o(1)) versus q_available <=N^(3/5+o(1)). Explicit time to output all cells is Omega(N^2), above N^(6/5). A virtual accessor lowers physical storage but does not shrink ordinary SAT logical input size. This does not refute code normalization, compressed transition summaries, or non-tableau SAT reductions.

GLUING COUNTEREXAMPLE, PROVED/EXACT:
For adjacent transition relations R1, R2, exact acceptance requires an intermediate configuration v such that R1(start,v) AND R2(v,accept). Independently SAT-evaluating each segment quantifies v and v' separately and does NOT impose v=v'. Even deterministic time-inhomogeneous four-state transition systems exhibit both local SAT bits true while the full run rejects. Exhausting 65,536 pairs of 4-state deterministic transition functions produced 28,416 false-positive ANDs; gluing through a common state made all 65,536 correct.

BOUNDARY-SUMMARY INJECTIVITY, PROVED/EXACT in a one-way, no-source-reread model:
For Q=2^w possible intermediate states i, let the left relation force end state i, and right relation accept exactly if incoming state equals j. Correct composition outputs [i=j] for every j. The left-side transmitted summary sigma(i) must be injective: otherwise a collision i!=k and a test j=k force inconsistent answers. Thus at least w summary bits are required. Source reread, recomputation, reachable-state compression, shared SAT CNF, and code-specific invariants escape the model and require separate fully charged analyses. Do not elevate this to unrestricted SAT space lower bounds.

FALSIFICATION CONTROL: The stronger claim that no solver-dependent compression can bypass this cover bound is FALSE. A white-box optimizer can recognize and remove the explicit no-op loop of A_D and run B directly. On 4,096 three-variable 2CNFs, an independently verified implication-graph decider and its peephole-optimized form matched brute-force SAT exactly: 2,397 SAT and 1,699 UNSAT. Every SAT instance refuted an N-step bounded-acceptance formula for an N^2-delayed decider. This falsifies full semantic closure of bounded-horizon trace children; explicit proof of acceptance requires horizon >= actual accepting completion time.

COMPUTATIONAL: 210,075 assertion-counted checks; all passed. Separate finite checks covered 3CNF Tseitin encodings of local transitions, all one-way maps of insufficient widths (1+16+65,536), and symbolic N^D window counts at N=10^3,10^4,10^5 and D=2,3,7. Long padding loops were counted symbolically, not executed.
Code SHA256 925b11c003f1e97dfd3ba8efd93e0ba8bd15d995a301b438234a3a4cf0da8e47
Raw SHA256 057286670a65cc941c5956d7c3e58d0d0938c4f354af4131bf64bcb2b274245b
Full local reproducibility bundle: LSPV_PRIMARY_GLUECOVER1_20261017_bundle.zip.

FULL CHARGED LEDGER, CONDITIONAL:
t'<=max{r,g+a+lambda*t}, s'<=max{h,lambda*s} for sequential guest execution, charging source scans, query construction, encoding, explicit child buffers, every virtual read, simulation, answer combination, and retained ancestor state. Direct retention of N^p guests instead requires s'<=max{h,p+lambda*s}; never apply the serial bound to retained races. For (r,g,lambda,h)=(6/5,3/5,1/2,1/2), a=0, the conditional fixed point is (6/5,1/2). FLMV Cor 5.8: beta(c)=((c+2)/c^2-c)/2. beta(6/5)=23/45>1/2. Illustrative starting exponents (17,14) first enter the sufficient forbidden region at iteration 12 IF the all-input hereditary solver-dependent compiler exists. With per-read N^a virtual overhead, c_infty=6/5+2a, and a must be <0.0027847152003... for s=1/2 to stay within this FLMV region. A direct N^p simultaneous-guest interface has s_infty=max{1/2,2p}, requiring p<23/90 when a=0.

WHY NOT ALREADY UNCONDITIONAL SAT: The child queries are defined using the supplied decider's transition program, and the faithful unrolling cannot meet the claimed budget. Cheap source-only SAT splitters landing at the forbidden point are explicitly rejected: recursive elimination would contradict FLMV without P=NP. This run produces no such splitter.

HANDOFF: Build an A-specific compact relational or inductive summary of arbitrarily long execution blocks, with a verified all-input SAT gluing predicate, without performing the full parent computation. Charge summary acquisition, source scans, all boundary information, virtual reads, explicit materialization, retained states, and interpreter overhead. Falsify under DELAY/COPY/INTERP/RECOMP, all SAT/UNSAT sources, and repeated application. P=NP -> universal solver-dependent contractor remains OPEN; P!=NP remains OPEN.

SOURCES: Fortnow et al. JACM 2005 doi:10.1145/1101821.1101822; Cook STOC 1971 doi:10.1145/800157.805047; Savitch JCSS 1970 doi:10.1016/S0022-0000(70)80006-X; Williams STOC 2024/2025.
END_GLUECOVER1_20261017_REPOSITORY_SENTINEL