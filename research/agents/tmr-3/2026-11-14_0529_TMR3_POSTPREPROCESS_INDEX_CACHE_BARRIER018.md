# TMR-3/018: post-preprocessing INDEX port has a quantitative retained-state versus source-retrieval barrier

**Pacific timestamp:** 2026-11-14 05:29 PST, America/Los_Angeles.
**Role:** TMR-3, new time-space tradeoffs.
**Mathematical status:** CANDIDATE/RESTRICTED, complete direct argument awaiting independent TMR-5/TMR-1 audit.
**Finite experiment:** COMPUTATIONAL.
**Unrestricted 3-SAT superpolynomial processing lower bound:** OPEN.

## 1. Exact model and claim

Fix ONE finite deterministic machine A, with q finite control states, h fixed ordinary locally moving writable work tapes (including every index, cache, stack and buffer), and finite alphabets of at most g symbols each, g>=2. A has one original read-only input tape containing x in {0,1}^L between physical endmarkers. All head movements, reads, writes and output are charged physical transitions. All work tapes start blank at their fixed origins. A must be total for all binary x and all valid later query indices.

This is a deliberately **restricted two-phase source-bit-query service**, NOT a general 3-SAT decider. First, A may preprocess the input for an arbitrarily long time, reread it, rearrange or algebraically compress it, and retain any work-tape representation. The query index p is NOT known in preprocessing. At the phase boundary A's original input head is restored to the left endmarker, and at most s *distinct writable cells have been visited*, uniformly over all length-L source strings. Its control, work contents, work-head positions and visited footprints may all depend on x. Next, a binary encoding of p in {1,...,L} is supplied on a separate read-only query tape, with every access charged. The query phase must output exactly x_p for EVERY pair (x,p), may reread all original source cells and use arbitrary recomputation, and its clock counts every transition including output. The query tape never gives any x-dependent information.

Let

$$
M_A(s)=q(2s+3)^{3h}g^s,\qquad b_A(s)=\lfloor\log_2 M_A(s)\rfloor.
$$

**TMR3-IC18, restricted same-machine lower bound.** For any L>b_A(s), there exist a source x of exactly L bits and a valid query p, for the SAME machine A and after its actual preprocessing on x, such that

$$
T_A^{\mathrm{query}}(x,p)\ \ge\ L-b_A(s).
\tag{IC18}
$$

In particular, if s=s(L)=o(L) is an all-input pre-query visited-workspace budget for this fixed machine, then

$$
\max_{x\in\{0,1\}^L,\ 1\le p\le L}
T_A^{\mathrm{query}}(x,p)\ge (1-o(1))L.
$$

No restriction is placed on how many preprocessing transitions the same machine spends, and that cost is not treated as free in the combined runtime. For the witnessing input, the complete physical cost is at least the actual preprocessing time on that same x plus the right-hand side of (IC18).

## 2. Complete proof

Every work-tape cell ever visited lies in a contiguous interval around that tape's fixed origin, because heads move only one cell per transition. If at most s cells total are visited across h tapes, each tape's visited interval, work-head position and boundary descriptors admit at most (2s+3)^3 possibilities. The visited contents across all tapes admit at most g^s choices, and the finite control has q possibilities. Consequently the total number of distinct COMPLETE post-preprocessing work configurations, including all work heads and visited boundaries, is at most M_A(s). The original source head is fixed at position zero by the interface; the query tape contains no source-dependent data before p is given. These are overcounts, not assumptions about which compression scheme A chooses.

Set m=b_A(s)+1 and r=L-m>=0. Fix the first r source bits to zero. The 2^m possible remaining suffixes exceed M_A(s), so there are distinct length-L sources x,y with identical first r bits and **identical complete retained post-preprocessing configuration**. They differ in at least one suffix coordinate.

After the same query p at any coordinate where x and y differ is supplied, couple the two deterministic query executions step by step. The query tape, program, writable tapes, heads, control and every source cell in positions 0 through r are identical. Until the first access to an original-source cell past r, the two complete computations must have exactly the same transitions, including cache use, source rereads, recomputation, output and potential halting. They cannot both halt with the same answer, since their required outputs x_p and y_p differ. Thus a distinguishing access to some differing suffix cell must occur. Reaching any suffix cell from the original source head at physical position zero requires at least r+1=L-b_A(s) locally moving transitions. This proves (IC18). The first distinguishing cell need not itself be p, since arbitrary algebraic inference from another differing cell is allowed.

The argument uses one fixed A on two same-length inputs, not two algorithms or two independently chosen hard instances. It does NOT use a selected SAT proof system or an assignment enumeration assumption. For fixed q,h,g, log_2 M_A(s)=s log_2 g+O_A(log(s+2)), so s=o(L) gives the displayed asymptotic statement. QED, subject to independent review of the complete configuration overcount.

## 3. Quantifier and transfer audit

This excludes exactly the simultaneous port pairs in which **all** length-L pre-query runs have s=o(L) writable visited cells AND **all** source/index queries finish in o(L) transitions. It does NOT exclude even a linear-time 3-SAT solver, nor a polynomial-time solver with S=Theta(L), nor any arbitrary polynomial workspace S=O(L^k). The same-machine S<=O(T) observation cannot bridge this gap; it allows S=Theta(L) or larger under polynomial time.

The interface itself supplies p only AFTER preprocessing and explicitly resets the original source head. A normal 3-SAT decider receives no such adversarial query and may decide SAT without reconstructing any requested source bit. Its computation can interleave acquisition and algebraic work before terminal output. The proof therefore supplies no unrestricted-machine SAT processing lower bound. If the source head is allowed to remain parked at an input-dependent location after preprocessing, its position must be added to the retained-state count (an O(log L) information correction) and the physical distance argument must be changed; (IC18) is NOT stated for that alternate interface.

For comparison, TMR-3/017's R=L+2 complete cache incurs Theta(L) visited cache cells and then permits locally aligned, moving virtual input heads to read without further original-source rereads. It violates the s=o(L) premise exactly as expected. If an absolute p is supplied independently, moving a locally moving cache-work head to its address is also charged; (IC18) does not promise constant-time indexed lookup at s=Theta(L). TMR-3/017's moving-window O(L+(T+1)(1+L/R)) upper simulation is a distinct constructed simulator, not a lower bound on A itself. In its implementation, lazy window-base updates at reload rather than mandatory binary-address updates on every simulated move are necessary for O(1) ordinary cached steps; this is a compiler obligation, not a new lower bound.

## 4. Executed evidence and hostile controls

**Published exact hosted-V8 code:** experiments/tmr/tmr3_postprep_index_cache018.cjs.
**Published immutable raw JSON:** results/raw/tmr/2026-11-14_0529_TMR3_INDEX_CACHE018_RAW.json.
The exact source and raw files were independently read back from GitHub main after writes.

The executed finite audit used lengths L=5..14, budgets 0<=s<=min(6,L-2), and three representation styles: literal prefix retention, striped XOR parity, and an interleaved nonlinear XOR sketch. For every (L,s,representation), it enumerated 2^(s+1) source suffixes sharing a fixed prefix, found a genuine retained-state collision, identified a differing suffix query and checked physically sequential source-position reach with the head incremented before each current-cell observation. It also tested injective full-copy storage with s=L, and reproduced the original TMR-2/019 valid-label nine-variable 3CNF forcing/pivot one-bit neighbors by brute force on all 512 assignments, including the exact 203+16m length and a single changed encoded sign bit.

| Executed check | Count |
|---|---:|
| (L,s,sketch) cases | 192 |
| Exact retained-state collision witnesses | 192 |
| Tracked source-head prefix movements | 1,359 |
| Full-copy injective string checks | 2,046 |
| SAT source-family controls | 5 |
| Single-bit valid SAT-to-UNSAT neighbors | 31 |
| Assertions failed | 0 |

A **separately authored native CPython** finite collision test ran locally in one short chunk: 192 witnesses, maximum differing query index 14, zero assertion failures. It is local-only and NOT represented as shared published code. Neither emulator is a physically compiled arbitrary Turing machine and its sketch-construction host-language arithmetic is NOT fully charged machine code. Finite evidence is COMPUTATIONAL; the all-length assertion depends on the combinatorial proof above.

Horn, 2-SAT, GF(2) Gaussian elimination, bounded treewidth, products, auxiliary variables, reordering and shared computations remain allowable inside arbitrary preprocessor A because the theorem counts complete retained configurations without stipulating what they mean. These specialized SAT algorithms were NOT individually benchmarked here. Query-index arrival after preprocessing is a real access-model restriction, not a theorem about arbitrary 3-SAT computations.

## 5. Primary literature and previous ORIGINAL project scope

1. A. C.-C. Yao (1979), Some complexity questions related to distributive computing, STOC 1979, 209-213, https://doi.org/10.1145/800135.804414 . The original primary model charges transmitted bits in two-party communication; our complete-state collision follows the deterministic one-way INDEX pigeonhole idea but has a NEW explicitly charged locally moving original-source head. We do not import a one-way lower bound as a theorem about SAT.
2. L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas (2005), Time-space lower bounds for satisfiability, JACM 52(6), 835-865, https://doi.org/10.1145/1101821.1101822 . Its primary abstract establishes exclusion of T=n^c, S=n^d for c below the golden ratio and a corresponding sufficiently small d>0 on deterministic random-access Turing machines, not all polynomial workspaces; no FLMV bound is invoked to prove (IC18).
3. J.-W. Hong, H. T. Kung (1981), I/O complexity: the red-blue pebble game, STOC, 326-333, https://doi.org/10.1145/800076.802486 . Its original model tracks I/O under a prescribed computation graph; no prescribed DAG is imposed on our machine.
4. A. Borodin, S. Cook (1982), A time-space tradeoff for sorting on a general sequential model of computation, SIAM J. Computing 11(2), 287-297, https://doi.org/10.1137/0211022 . The primary abstract's TS=Omega(N^2/log N) is for sorting N integers, NOT 3-SAT or our query interface.
5. Prior original TMR-3/002, research/agents/tmr-3/2026-11-13_1434_TMR3_TWOWAY_CROSSING_TRADEOFF002.md, and TMR-3/008, research/agents/tmr-3/2026-11-13_1935_TMR3_BATCH_LOCALITY_TRADEOFF008.md: same-execution input-cut TS products on exact equality 3CNF encodings with ONE sequential input head. They reach polynomial, geometry-dependent bounds, not any all-polynomial SAT exclusion.
6. TMR-3/017 and TMR-5/015: the former gives an achievable whole-cache/partial-cache simulation upper frontier; the latter independently identified an off-current-cell test defect in earlier TMR-3/016 and corrected the physical source fetch. This run does not reuse that defective trace.

Original LSPV/ARC/FLMV tracker evidence and the LSPV-5/523 authentic accepted literal-order counterexample remain historical restricted evidence. No accepted path is removed and no status is promoted by this experiment.

## 6. Repository preflight, statuses and next obligation

First recovered the current TMR replacement directive (Git SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4). BOTH proof trackers reviewed: proof1.txt 28,714 chars, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt recovered via exact Git blob, 1,051,196 chars, SHA 930c5eeddafce656717f28055a7a9a755f44737c, NOT the misleading blank fetch_file content. Canonical root main.tex recovered completely via Git blob, 2,533,636 chars, SHA 867c9b7512a51d59a50c479e81dda6c65615026f. Also read AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, latest issue #3 comments through TMR-2/019, all five newest TMR handoffs and original TMR-3/002,/008,/017, TMR-5/015, TMR-2/019, and primary source pages. Rechecked directive before shared writes. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex unmodified; TMR-5 owns manuscript synthesis. No tasks or schedules altered.

**Peer requests:** TMR-5 check the exact full-configuration count and coupled pre-query witness, and try cache-dependent hard queries with compact XOR/GF(2) states; TMR-1 audit the requirement to reset the original input head and the externally delayed index; TMR-2 seek a genuine SAT-vs-UNSAT analogue rather than an optional source-bit query; TMR-4 build the all-transition abstraction for this two-phase interface without inventing free query oracles.

**One next target:** Either prove a universal charged reduction making an unavoidable semantic SAT distinction simulate this delayed INDEX interface for all correct A, OR produce an explicit correct SAT machine that invalidates that reduction through early global invariants, interleaving or full caching. This arrow is OPEN. No general superpolynomial bound has been established.

END_OF_REPORT::TMR-3::018::2026-11-14_0529_PST
