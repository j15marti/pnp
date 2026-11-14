# TMR-3/015: a tight finite-head positional-time frontier and a logarithmic-workspace threshold

**Date:** 2026-11-14 02:37 PST (America/Los_Angeles). **Role:** NEW TMR-3 Time-Space Tradeoffs. **Mathematical status:** CANDIDATE/RESTRICTED pending independent TMR-1 or TMR-5 review. **Executed finite evidence:** COMPUTATIONAL. **Unrestricted all-exponent SAT lower bound and P versus NP:** OPEN.

## 1. Precise new claim

Fix a finite deterministic total machine A over immutable L-bit input, read-only original-source cells 1,...,L and endmarkers 0,L+1. Let h>=1 be its fixed number of independently locally moving read-only input heads, b>=0 its fixed number of one-sided, locally moving writable work tapes, Gamma its fixed finite work alphabet with at least two symbols, and Q its fixed finite control. All heads and writable tapes are included in the concrete configuration. Let T_A(x) be actual transitions and S_A(x) the total number of **visited writable work cells** on the SAME halting execution x, summed over all b tapes. Input movement and all work-head transitions count as time; input-head position is an explicit model resource rather than uncharged random access.

**MCF15-A (configuration-time envelope).** For every halting x,

$$
T_A(x)\le |Q|(L+2)^h (S_A(x)+1)^b |\Gamma|^{bS_A(x)}.
\tag{MCF15-A}
$$

Consequently, for any fixed A with S_A(x)=o(log L) along a sequence of growing input lengths, T_A(x) is at most L^{h+o(1)}. If b>=1 and, on an unbounded input sequence, T_A(x)>=(L+2)^{h+epsilon} for fixed epsilon>0, then necessarily

$$
S_A(x)\ge \frac{\epsilon}{b\log|\Gamma|}\log(L+2)
-O_A(\log\log(L+2)).
\tag{MCF15-B}
$$

The logarithm is natural. This is an **inversion of an upper bound on halting-time capacity** conditional on actual long running time, not evidence that long running time is mandatory to decide SAT.

**MCF15-C (matching head-only clock).** For every fixed integer h>=1 there is one uniform finite-state machine D_h, with h independently movable read-only input heads and **zero visited writable cells**, which decides the unbounded restricted language of proper three-literal CNF sign streams over exactly three fixed variables (SAT, UNSAT and MALFORMED), with precise transition count

$$
T_{D_h}(x)=2\sum_{j=1}^{h}(L+1)^j+1
=\Theta_h((L+1)^h),\qquad S_{D_h}(x)=0.
\tag{MCF15-C}
$$

The number of heads h and the finite controller are fixed once, not changed with L. This shows the L^h exponent of (MCF15-A) is attained, up to fixed factors, by a concrete genuine decision computation that pays all physical input-head movements. This restricted three-variable language is **not** unrestricted NP-complete 3-SAT. The deliberate extra scans are semantically inert; their existence does not establish a necessary SAT processing cost.

## 2. Symbolic proof and exact same-execution scope

For a fixed immutable x, every source head has at most L+2 positions. For a one-sided work tape whose head begins at cell zero and moves locally, all visited cells lie in a contiguous initial interval. With S total visited work cells across b tapes, any one work head has at most S+1 possible positions, and the first S visited symbol cells admit at most |Gamma|^S symbol strings. Over b tapes, the coarse product bound is (S+1)^b |Gamma|^{bS}. Multiply by |Q| and (L+2)^h to obtain (MCF15-A).

Two identical complete configurations on the **same fixed source x** cannot both occur on a terminating deterministic trace: after the first recurrence the entire future would repeat, preventing halting. The number of transitions is thus bounded by the number of configurations, with a harmless choice of whether to count the last halting configuration. This is a same-input same-machine statement. No runtime of another machine or workspace from a different input is borrowed.

Taking logarithms of (MCF15-A),

$$
\log T_A(x)\le \log|Q|+h\log(L+2)
+b\log(S+1)+bS\log|\Gamma|.
\tag{MCF15-D}
$$

If S=o(log L), the last two terms are o(log L). For (MCF15-B), if S>(log(L+2))^2 the asserted weaker Omega(log L) bound is immediate. Otherwise log(S+1)=O(loglog L), and rearrangement of (MCF15-D) gives the displayed quantitative inverse. The same work alphabet and same actual writable footprint are used throughout.

**Boundary:** With a one-head, zero-work-tape machine, (MCF15-A) reduces to T_A(x)<=|Q|(L+2). A single input head and zero writable cells cannot execute an arbitrarily high polynomial number of steps before halting. If instead a fixed ordinary one-input-head machine uses b>=1 binary work tapes, executing time L^{1+epsilon} for arbitrarily large L requires Omega(log L) visited writable cells. This is consistent with TMR-1/016's charged O_d(log L) binary-work-tape counter implementation, for each fixed desired polynomial delay degree d.

## 3. Exact sharpness construction

Put q=L+1. Let all h read-only heads H_0,...,H_{h-1} begin at position 0. With h fixed, the following finite nesting is unrolled into an ordinary finite state machine:

- sweep(0): move H_0 right q times and left q times, one physical transition per move.
- sweep(j), j>=1: while H_j lies before the right marker, perform sweep(j-1) once and move H_j right one position. After q repetitions, return H_j left q transitions.

Each nested lower head returns to zero before the next invocation. Thus exact charged movement counts obey

$$
D_0(q)=2q,\qquad
D_j(q)=qD_{j-1}(q)+2q,
\qquad
D_{h-1}(q)=2\sum_{r=1}^{h}q^r.
\tag{MCF15-E}
$$

No writable counter is used: current read-only head positions function as h positional counters, and all their advancement and resetting are paid. Only the fixed nesting level and direction reside in finite control.

During the *first outward* sweep of H_0, parse input bits into successive 3-bit sign masks. Each triple is one proper clause on the **same three fixed Boolean variables** and excludes exactly one of their eight assignments. In constant-size finite control maintain a 3-bit partial triple, a modulo-three phase and an eight-bit forbidden-assignment mask. At the first right marker, classify SAT iff some assignment mask was never forbidden, UNSAT iff all eight were forbidden, and MALFORMED iff a partial triple remains. Retain the correct label during all later movements. After all heads return left, a single halting transition gives (MCF15-C). The status is correct for every bitstring length and unbounded numbers of clauses within this restricted grammar.

For arbitrary fixed correct uniform ordinary 3-SAT A, an h-head model may prepend this *fully charged* odometer and then execute A with its original head(s) and work tapes untouched. This preserves labels on both SAT/UNSAT inputs and malformed strings and adds no visited writable cells, but DOES add h-1 independent read-only heads. The altered model is stated openly, not treated as an ordinary single-source-head equivalence. In particular a proposed memory bound that calls source-head positions 'zero information' is invalid, even though the designated definition of S counts only writable visited cells.

The physical movement state identified by the h head positions, active head index and direction never recurs during this nested controller. The higher positional digits select a unique invocation of each lower sweep, and phase/direction select a unique movement inside it. Thus the construction provides a matching exponent example for the configuration envelope, not a compulsory computational lower bound for the SAT language.

## 4. Executed falsification and independent oracle checks

**Published exact executable:** experiments/tmr/tmr3_multihead_config_frontier015.cjs. **Immutable raw:** results/raw/tmr/2026-11-14_0234_TMR3_MULTIHEAD_CONFIG015_RAW.json. The exact audit function was executed in hosted V8 before publication, then published verbatim and read back. The finite host recursion has fixed depth h and could be unrolled into finite control. Its Set of complete positional/movement states and BigInt arithmetic are host-side verification machinery, NOT resources attributed to D_h.

For each fixed h in {1,2,3,4}, all binary words of lengths 0..8 were exhaustively simulated, together with valid SAT, genuine eight-distinct-mask UNSAT, repetitive-clause, longer and malformed controls. At larger h the length of extra controls was bounded to avoid a large host Set. Each read is from the **current** physical source cell, never a neighboring unvisited cell. An independently implemented set-based three-variable satisfaction oracle classified each word. Every movement and the final halt were counted, every complete movement-state key was unique, and the exact formula (MCF15-C) was checked.

| Check | Actual V8 result |
|---|---:|
| Source/head combinations | 2,071 |
| All charged transitions | 6,700,071 |
| Distinct pre-move positional states | 6,698,000 |
| Current-cell data reads on initial outward scans | 15,249 |
| SAT | 302 |
| UNSAT | 11 |
| MALFORMED | 1,758 |
| Assertion failures | 0 |
| Longest individual trace | 275,121 steps at h=4, L=18 |

Per-head execution: h=1: 521 cases and 9,479 transitions; h=2: 521 and 112,349; h=3: 517 and 836,575; h=4: 512 and 5,741,668.

Separately executed 36 exact BigInt **configuration-envelope inversions**, for illustrative Q=256, Gamma=2, h in {1,2}, b in {1,2}, extra polynomial powers 1..3 and L=2^8, 2^16, 2^32. For h=b=1 and target 2(L+1)^4, the smallest integer S admitted by the *loose inequality* is 14, 36, 83. These are arithmetic results, not an execution of a hypothetical long-running physical TM.

**Failed initial audit attempt:** An earlier version included h=4 and length 66; its host-side Set hit the V8 maximum size and the call failed before publishing any artifact. The revised, actually published audit caps extra longer cases at larger h. The general symbolic theorem does not depend on the finite test range. Native OS Node, independent Python reimplementation, full arbitrary-3SAT machine compiler, project preflight, research-report validator and LaTeX compilation were NOT run. All finite checks remain COMPUTATIONAL.

**Hostile controls:** Gaussian elimination for XOR/Tseitin, Horn, 2-SAT, bounded-treewidth dynamic programming, disjoint products, reencoding, padding, renaming, auxiliary variables, caching, sharing and recomputation are permitted in arbitrary A and do not alter the configuration-count argument. None is proved necessarily slow. They were NOT each executed in this run; the executed semantic decision control was the restricted three-variable sign-stream classifier.

## 5. Primary literature, historical evidence and remaining gap

The new proof is elementary configuration counting and induction, with **no external complexity lower-bound exponent imported**. Scope checks: [1] Hennie, *One-Tape, Off-Line Turing Machine Computations*, Information and Control 8 (1965), 553-578, archival record https://ntrs.nasa.gov/citations/19660041785 (one-tape crossing-sequence model, not arbitrary multitape transfer); [2] Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), 835-865, https://doi.org/10.1145/1101821.1101822 (simultaneous small-space bounded-exponent exclusion for declared random-access SAT model, not arbitrary polynomial workspace); [3] Borodin and Cook, *A Time-Space Tradeoff for Sorting on a General Sequential Model of Computation*, SIAM J. Comput. 11 (1982), 287-297, https://doi.org/10.1137/0211022 (sorting output lower bound, not unrestricted SAT).

Prior work adopted, not reclaimed: LEAD-0030 already showed wrapper-inflated distinct machine configurations; TMR-5/013 already derived the exact multiple-read-only-head positional odometer count; TMR-1/016 separately used one ordinary input head with paid binary writable counters. Original TMR-3/002 and /003 provide a same-execution restricted equality-family crossing tradeoff, already sharp at polynomial strength, not an all-exponent separation. This run adds a **matching finite-head halting-time ceiling** and an explicit conditional logspace inversion. No assumption of mandatory assignment enumeration, a selected proof calculus, algorithm-independent hard family, a free SAT oracle, ETH/SETH, cryptographic hardness, prescribed pebbling DAG or per-length nonuniform programs is made. Relativization, algebrization and natural-proofs barriers are not bypassed by this semantic-neutral configuration result.

For any machine with arbitrary polynomial writable workspace S=L^c, (MCF15-A) allows exponential time and does not rule out polynomial-time SAT. The same-machine fact S_A(x)<=O_A(T_A(x)+1) points in the wrong direction for promoting this upper bound into a necessary SAT lower bound. No part of MCF15 proves there is a valid F requiring superpolynomial T_A(F) for every correct A. All such arrows remain **OPEN**.

**Corpus/read protocol:** Replacement directive was read FIRST and rechecked at Git SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Complete proof1.txt read (28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343). The nonempty complete proof2.txt recovered by authentic Git blob (1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c), not the blank contents response. Complete main.tex recovered by Git blob (2,525,134 characters, SHA d3db01d221df39f096f31237643268132edfcd87). Read AGENTS.md, CODEX.md, repo research skill, latest issue #3 through TMR-1/016, all five handoffs, relevant TMR-3/013/014, TMR-1/016, TMR-2/016, TMR-4/016, TMR-5/013, original historical LEAD-0030 and TMR-3/002/003. Legacy roles superseded; mathematical evidence preserved.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither proof1.txt nor proof2.txt was modified. Root main.tex is left to TMR-5 whole-document synthesis. No scheduled task or agent was created, revived or changed.

**One next target:** Independently verify the fully charged transfer between positional read-only counter heads and a single original input head with O(log L) physical binary writable counters. Then pursue a necessary total decision-time charge rather than a machine-capacity bound, which remains OPEN.

**Publication status:** Exact executable and raw evidence are readback-verified; report publication and handoff verification are to follow before issue #3 coordination.
