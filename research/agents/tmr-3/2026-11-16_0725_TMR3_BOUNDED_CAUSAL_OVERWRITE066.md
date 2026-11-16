# TMR-3/066: source-reachable last-writer reconstruction across genuine overwrites

November 16, 2026, 07:25 PST. TMR-3 / PNP Time-Space Tradeoffs, Track B.

**STATUS:** PROVED/EXACT only for the declared bounded-causal-depth, source-authenticated ping-pong machine family, independent mathematical review OPEN. The finite reference program is COMPUTATIONAL. The complete general Williams/HPV checkpoint provider, height-sublinear generic TreeEval and P versus NP remain OPEN.

## Candidate, quantified scope and four falsifiers (set before primary-source review)

**C3-BOUNDED-CAUSAL-OVERWRITE066**, a restricted closure of the /065 **C3-GENERAL-LAST-WRITER-ORACLE** dependency. There exists a fixed deterministic, finite-alphabet, locally headed multitape machine M implementing the rule F(a,p,z)=(a AND p) XOR z, such that for every sufficiently large b=2^k (k>=1), every genuine source x=1^(b-1)0 y with M_cells=b^3, and every canonical completed time tau, tape identity and cell, a uniform original-source-only algorithm determines the actual last-written work-cell value with polynomial time and O(log^2 N) writable bits. The end-to-end virtual machine computes the SAME terminal parity output by recursively evaluating the authentic, source-indexed, nonassociative dependency tree at depth k. It does not simulate an arbitrary HPV-converted program.

F1: the updated work-cell value depends on an old cell which was already overwritten in the same pass, destroying bounded causal depth. F2: some source/work-tape crossing occurs off a b-step boundary, or input authentication/turning hides movement. F3: a claimed O(log^2 N) virtual bound omits recursive frames, addresses, physical source seeks, Q, clock/graph queries, rejected malformed inputs or output. F4: the shallow special tree is falsely promoted to a generic height-sublinear TreeEval, a polynomial-time generic Williams simulation, or an NP lower bound.

## Authentic source, complete physical computation and resource ledger

Let b=2^k, M_cells=b^3, N=b+M_cells. Valid source is exactly (b-1) ones, delimiter zero, and M_cells payload bits y_0,...,y_{M_cells-1}. Check the unary header, power-of-two b, length b^3 and absence of trailing symbols before running the processing phase; malformed sources reject. Input content is read-only, all work tapes begin blank, and every transition has locally moving heads. A fixed number of auxiliary counter tapes and one bounded b-cell clock tape control phase. Their peak used lengths are O(log N) and b respectively; no full source copy or checkpoint is provided.

After a charged forward seed scan, tape A physically stores V^(0)_i=y_i. Then perform k genuine overwrite sweeps, alternately reading the preceding complete layer on tape A/B and writing the other tape. For odd layers scan from right to left, for even layers from left to right. At each cell the machine reads OLD value a and holds in finite control the previously read OLD value p of the adjacent cell in sweep direction (zero at the scan boundary). In that SAME transition it writes the new value F(a,p,y_i), updating the finite register p<-a. Thus no just-written value is reused as a predecessor within the same pass. At the LAST update sweep the machine XORs each new output into a single finite-control parity register and outputs that bit, after a paid terminal halt.

Each scan touches exactly M_cells cells, with one locally headed transition per cell; both data tape heads move together. Forward scans step onto cell M_cells immediately after processing the final data bit, at a b-step boundary. Before a reverse scan, the heads wait at M_cells until the next b boundary, then move left to M_cells-1 at that boundary, paying b transitions for the entire turnaround. Reverse scans end by staying on the distinguished first cell 0, so the next forward scan starts there at an aligned boundary. Every data-tape crossing is therefore at an integer multiple of b. The read-only original source head follows the same scan on its payload offset b, so its crossings are aligned too. Source authentication uses a b-cell bouncing clock and O(log N)-bit position/length counters; a crossing after a variable-cost counter update is postponed to the next clock boundary, costing at most b extra transitions per source block. This covers the read-only source head, not merely the two work heads. The initial b-symbol header traversal crosses into payload precisely at the first b boundary. All fixed control/counter heads remain inside their initial work block once b exceeds a fixed constant.

The core controller uses (k+1)M_cells + b ceil(k/2) transitions for the seed and k overwrites, excluding constant terminal/output overhead; source validation, alignment and returning the input head to the payload are O(N polylog N) time and O(log N) live counter bits. Thus one genuine physical execution has
  T_original=O(N polylog N), S_original=Theta(M_cells)=Theta(N) visited writable cells.
The b clock and both M_cells-length data tapes are counted in S_original. There are constant-many heads and b>=ceil(log2 T_original) for all sufficiently large powers of two b, since log T_original=O(log b) and b grows faster than log b. The genuine public movement graph has exactly one source-independent candidate, K=1. At the cut after seed and before the first overwrite all b^2 data blocks on A must be reread: its future-live block frontier W is Omega(b^2); at most 2b^2+O(1) distinct data/clock block identities can be future-live. Hence W=Theta(b^2) despite the compact canonical provider.

## Exact local-write dependency and source-only last-writer theorem

For 0<=i<M_cells define V^(0)_i=y_i. For each 1<=ell<=k let d_ell=+1 for odd ell and -1 for even ell (the preceding cell in scan order). With V^(ell-1) out of range interpreted as zero, define

  V^(ell)_i = F(V^(ell-1)_i, V^(ell-1)_(i+d_ell), y_i).

The induction over physical sweeps is exact: reading OLD cells from the opposite data tape, retaining just the last OLD bit, prevents within-layer dependencies; the written new cell is precisely V^(ell)_i. Every Boolean update can depend nonlinearly on two earlier work values. It is not a finite-state one-write streaming transducer as in /065.

For any completed time tau, tape h in {A,B} and position i, calculate which sweeps on h have completed their WRITE at position i by public phase arithmetic: the ell-th sweep begins at source-independent time s_ell, has direction determined by parity ell, and visits i after i+1 steps in a forward sweep or M_cells-i steps in a reverse sweep. Select the **largest** ell with matching tape parity and tau>=s_ell+visit_offset_ell(i). If none exists, the canonical bit is BLANK; otherwise compute V^(ell)_i recursively from the source. The query never receives a guessed, arbitrary preloaded checkpoint. Original time before seed includes the charged known-length validation/aligning prefix; only validated sources reach service.

One recursive request V^(ell)_i performs at most 2^(ell+1)-1 value-node calls, each involving one source-symbol lookup and O(log N)-bit frame indices. The complete bounded-depth tree has a stack of at most k+1 frames, with two child results retained by each frame. Each source lookup on a locally moving read-only input head can be performed with an O(N)-move seek, and all binary arithmetic and switching cost polylog N per call. Consequently

  T_value(ell) = O(2^ell N polylog N),
  S_value(ell) = O((ell+1)log N) <= O(log^2 N).

The same source-derived method answers any adaptive query about a canonical completed work-tape bit; a requested whole b-bit tape block must be streamed or materialized with an honest additional O(b)-bit buffer. A finite-control checkpoint at tau can be recomputed by replaying the bounded-depth written values in chronological order; this may require polynomially many repeated requests, not a free state oracle.

## One charged virtual output execution

A single deterministic locally headed virtual machine authenticates x, produces the actual one-candidate graph's pB block labels on demand, uses the last-writer recursion for final layer cells i=0,...,M_cells-1, XORs each returned real bit into one writable parity bit and emits the original machine's result. This is an actual restricted nonassociative tree-evaluation implementation, not an invocation of a nonexistent improved generic Cook-Mertz evaluator.

With p a fixed number of tapes, B=ceil(T_original/b), the graph interface is called Q_G=pB times. Each source-length-only graph-index call may be conservatively implemented by replaying the public phase schedule in O(T_original polylog N) time and O(log N) scratch, including source-head positions and auxiliary clock. There are at most

  Q_V <= M_cells(2^(k+1)-1) <= 2 M_cells b

actual recursive value-node invocations for the complete output. With no checkpoint cache, the disjoint time budget is

  T_virtual = O( N polylog N [authenticate] + Q_G T_original polylog N [graph] + Q_V N polylog N [value, address, source seek] + M_cells polylog N [XOR/output] ).

Since T_original=O(N polylog N), B=O(N polylog N/b), k=log2 b and 2^k=b, this simplifies conservatively to

  T_virtual=O(N^2 b polylog N)=O(N^(7/3) polylog N),
  S_virtual=O(log^2 N).

Peak space counts the full recursive frame stack, the source-cursor and restored positions, source authentication counters, current graph generation, clock/phase address counters, two child bits, all control and output simultaneously. The source is never cached in writable memory, no physical checkpoints are allocated, and total work is sequential. The virtual and original bounds refer to separate fully charged executions; no resources are spliced.

The tree is only of causal depth k=Theta(log N). Its O(k log N) ordinary DFS stack is **not** an improvement of the arbitrary-height nonassociative TreeEval result in Cook--Mertz, nor an all-machine t^(1/3) simulation. Sharing/caching/direct source-aware evaluation could be cheaper and remains legal. The restriction of b to large powers of two is a genuine scope restriction; finite small-b tests validate control semantics, not the asymptotic block-width inequality.

## Original sources and current alternative

[1] Williams, *Simulating Time With Square-Root Space*, STOC 2025, arXiv:2502.17779v1, Section 2 block-respecting definition and Section 3.2 computation graphs, https://arxiv.org/html/2502.17779v1. His Lemma 2.1 is equivalent-output, not fixed-trace preservation. The Section 3.2 algorithm guesses movements and uses FAIL; this report gives no general replacement.

[2] Cook and Mertz, *Tree Evaluation Is in Space O(log n log log n)*, STOC 2024 / SIAM J Comput 2025, DOI https://doi.org/10.1137/24M1690126, standard variable-height bound quoted by Williams.

[3] Asadi and Cleve, *Polynomial-Time Almost Log-Space Tree Evaluation by Catalytic Pebbling*, arXiv:2604.02606, April 3 2026, https://arxiv.org/abs/2604.02606. Theorem 1 provides n^(1/epsilon+O(1)) time and ~O(log^(1+epsilon)n) catalytic bits for an explicitly represented size-n tree. For a Williams implicit tree with up to (2p)^B nodes, this n-polynomial runtime can be exp(O(B)): it cannot be silently treated as polynomial in the original time-t source. Catalytic physical storage must count toward peak space.

[4] TMR-3/065 original one-write source-replay theorem and exact evidence, branch research/tmr3-canonical-workvalue-replay065-20261116; the present result repairs its overwrite restriction only at bounded causal depth.

## Executed evidence and review status

Standard-library CPython original source revision tmr3-bounded-causal-overwrite066-v1, deterministic seed 202611160725, ran TWICE byte-identically. 300 valid test sources (256 exhaustive b=2 payloads plus deterministic b=4,8,16 instances), 1,200 malformed controls, 73,984 canonical completed-time tape-bit comparisons, 210,082 recursive value-node invocations, 192,942 assertions, ZERO failures. Local byte-identical raw SHA256 3a4106534e0e4861dd8256215887a20ed2f99ddf191a133603180a37075b1880; original complete source SHA256 798de9d0980c4c59cd86f0b81548cf3f8883525775e9888be0534f5437793ae4. The controller checks real writes, bounded head trajectories, crossing step congruence, last-writer selection, and output both labels. Python uses materialized reference arrays and indexed source bits, not physical logspace memory. Full native source authentication/clock transition tables, an actual HPV converter, generic Cook-Mertz implementation, independent mathematical review and full repository preflight have NOT been executed; no claim otherwise.

Code: experiments/tmr/tmr3_bounded_causal_overwrite066.py. Raw: results/raw/tmr/2026-11-16_0725_TMR3_BOUNDED_OVERWRITE066_PY_RAW.json. Living paper: main3_PNP_TIME_SPACE_TRADEOFFS.tex.

## Four gates and hostile controls

| Gate | Verdict |
|---|---|
| DISJ sanity | PASS RESTRICTED. No rank to general SAT work inference. The machine may compute an easy function. Horn/2SAT/affine/Gaussian/treewidth/equality/autarky/product/selector/unique-solution/compact/auxiliary controls remain legal. |
| Relativization | NOT APPLICABLE WITH REASON to a separation (none). BGS, algebrization and Natural Proofs remain OPEN for any downstream NP claim. |
| Simultaneous DTISP | PASS for each separately specified full physical/virtual machine with paid source, graph, Q and buffers; generic polynomial-time forbidden-region transfer OPEN. |
| Configuration counting | PASS as deterministic upper-bound consistency only, never a work lower bound or automatic randomized/quantum claim. |

No randomized isolation or field change is used; majority ties, quantum error model and circuit-to-CNF blowup are inapplicable to this restricted algorithm, but stay mandatory for any later transfer. /341 FAIL as full UNSAT authority; /386 RESTRICTED. P versus NP remains OPEN.

## ONE next load-bearing lemma

**C3-CAUSAL-DEPTH-CERTIFIER:** for a specified general block-respecting compiler, give a polynomial-time, O(polylog t)-space *source-authenticated* certificate/algorithm that bounds causal last-writer depth by O(log t), or produce the smallest authentic adaptive overwrite counterexample. All graph/node queries, rejected proposals, source rereads and same-run total resources must be charged. The present explicit family supplies a positive model but no coverage or verifier for arbitrary converted computations.
