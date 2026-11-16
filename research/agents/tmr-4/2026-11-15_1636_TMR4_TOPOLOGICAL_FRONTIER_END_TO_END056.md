# TMR-4/056 | 2026-11-15 16:36 PST | Authenticated topological live-frontier compiler

Status: **PROVED/EXACT, RESTRICTED** for the declared layout-equipped shared Boolean DAG model, independent mathematical review **OPEN**. Executed finite audit: **COMPUTATIONAL**. Unrestricted circuit/SAT hardness and P versus NP **OPEN**.

## Candidate, quantifiers, pipeline and pre-search falsifiers

Named dependency **D4-UNRESTRICTED-CONVERSION**, strengthened/closed for the **topologically scheduled live-frontier subclass**, not for all ordinary circuits.

For every finite shared fan-in-two Boolean gate DAG C over n>=1 original input bits and g>=0 gates, with an authenticated topological schedule pi listing all n inputs and all g gates exactly once, first token x0, each gate after both of its source wires, and one designated output source, let w(pi) be the maximum number of *distinct* previously evaluated nonconstant wire IDs that still have any future gate-use or the designated terminal output-use. One wire is charged once regardless of fan-out. Output is a designated pseudo-use after the last schedule token. Source encoding includes the schedule; it is not discovered for free.

Claim: a uniform compiler constructs a fixed-public-order, n-stage shared gate register program with exactly w(pi) persistent bit slots (unused slots permitted) and gate count at most g plus stage outputs of at most nw wire references; its complete materialized leveled OBDD has at most n*2^w distinct internal nodes, preserves the original Boolean answer for every x, and counts exactly the original #satisfying assignments when paths are counted with *edge multiplicity*. Every original gate execution is simulated in the matching stage; the compiler's physical construction/storage is charged.

The targeted falsifiers were (i) DISJ grouped-rank 2^k with a linear-size interleaved circuit and small live frontier, (ii) shared outputs used multiple times, possibly retired before their last real use, (iii) lost path multiplicities at merged OBDD states, and (iv) malformed/non-topological or duplicated source records. Additional controls include EQ, affine XOR parity, unused/dead records and input-order changes. No candidate lower bound on arbitrary circuit size is posited.

Pipeline: canonical encoded circuit+schedule+original input x -> complete parser/authenticator -> last-use and live-frontier computation -> gate-preserving stage register compiler -> reachable-state complete OBDD (both binary arcs at every layer) -> input evaluation and integer path-count DP -> bit f_C(x), integer #C, rank/retained-width implication.

## Exact model and live sets

The input lists n, gate records (unique ID g_i, two references a,b to constants 0/1, original input IDs or earlier gates, and one of 16 binary truth-table codes), a topological schedule pi of length M=n+g, and a designated output ID. Referenced inputs must precede any consuming gate; gates may share inputs and their own previously computed gate values freely. Duplicates, cyclic/forward edges, missing source bits, missing/duplicate schedule vertices, invalid opcodes and missing outputs are rejected. The current exact serialized test source uses JSON records; a physical implementation additionally validates the full encoded length/syntax and pointer ranges, charged below. The source input x is a separate read-only binary word.

Write last(v) for the greatest schedule position of an actual gate consuming v, or position M for the designated output (if it is v), whichever is greater. If v has no later use set last(v)=-1. At the end of step t, let
L_t={v: position(v)<=t<last(v)}.
Define w=max_t |L_t|. Constants are hardwired, not retained. Input introductions in pi induce a fixed public permutation rho. A stage begins at an input introduction and ends immediately before the next one (or at schedule end). Because the first token is x0, these n stages partition pi.

For stage i, the inputs are bit x_(rho(i)) and the live wires from the preceding stage boundary. Its **shared combinational gate DAG** contains exactly the original gate records in that schedule segment, preserving their fan-out, truth tables and repeated operands. Its next persistent-register vector is precisely the list of live wires at the end of the segment. Slot maps are computed by the authenticated compiler and hardwired into its produced stage records. The output bit is a slot at final stage (or the hardwired constant). All stages have a uniform w-bit register envelope by zero padding, not by adding new independent information.

## Theorem 1: exact all-step simulation and quantitative transfer

For every valid (C,pi) of width w and every x in {0,1}^n, the register program evaluates every original source gate exactly once within its stage, with identical values. At every original schedule step t, the original and stage-local valuation agree on each wire computed in that stage, and at each stage boundary the persistent bits equal the original live-wire values. Both terminal output labels agree. Proof: induction in pi order; for input introduction read the same original bit, for a gate both predecessors have either a stage-local value or a previous live-register slot because any predecessor with this future use has last-use >= t and cannot have been discarded. Apply the same two-input truth table, update live slots only after their final consumer. At the final output pseudo-use, the output value remains available. This proves initial correspondence, all-step coverage, and terminal correspondence without unfolding or double-counting fan-out.

The stage program is fixed order rho and reads each input exactly once. Enumerate reachable inter-stage w-bit registers, use the two actual stage successor maps for each reachable register, share identical (layer, register) states and retain **both** outgoing arcs even if they reach the same target. It yields V<=n*2^w distinct nonterminal nodes. Every x determines exactly one complete length-n path. Counting accepting paths with their multiplicities therefore gives #C, not merely the number of terminal or residual nodes.

For every prefix cut of rho, the suffix function is completely determined by the preceding stage's live values, so its Boolean assignment matrix has at most 2^k distinct rows when k is that boundary's live width. Over **every field K**:
rank_K(M_prefix,suffix(f_C)) <= 2^k <= 2^w.
Thus any **provided** topological evaluation schedule of live width w for this circuit must have w>=ceil(log2 rank_K(M_prefix,suffix)) for each rho-prefix. This is a lower bound on that schedule's live-wire width, not on the number of gates, unrestricted source-circuit complexity, or all-algorithm machine work.

## Output and SAME_REALIZATION resource ledger

Let M=n+g, L be the complete source encoding bit length, and w the measured frontier width. All parsing, topological authentication, last-use scan and computation of boundary sets can be performed by a fixed deterministic multitape machine with conservative repeated sequential scans. Stage records have g original binary gate records once, plus at most n*w persistent-slot references and O(n) input selectors. Their bit length is bounded by
B=O((g+n*w+n)*ceil(log2(M+w+2)))+O(L)
including all stage headers/addresses, repeated constant references, and generated slot maps. The **source gate DAG is not duplicated by the physical stage compiler**; it remains a shared object.

The materialized complete OBDD has at most V=n*2^w nodes and 2V arcs, and each node record uses O(w+log(n+V+2)) bits. For exact #C counting, store an integer of at most n+1 bits per retained state; the sum of all state counts is at most 2^n. The original input head, if rho is not physical tape order, incurs at most O(n^2) local moves, charged.

Define D=1+L+B+O(V*(w+n+log(n+V+2))) in **bits**. One deliberately inefficient but uniform conventional deterministic multitape execution first parses/compiles, then builds the entire OBDD by exhaustive reachable-state expansion, evaluates the x path, performs exact integer path-count DP, and emits f_C(x) and #C, in
T_total=O(D^5+n^2), S_peak=O(D).
This bound counts source acquisition, source and output storage, gate evaluations, representation discovery from the **supplied** schedule, table scans/address arithmetic, failed canonical-input checks, full stage DAG temporary buffers, fan-out, both arcs, path multiplicities, exact (n+1)-bit integer additions, local tape heads and output. D may be exponential in w; no polynomial-time unrestricted compilation is claimed. If w=O(log L), all bounds are polynomial in L, and the output count still requires at most n+1 bits. A source-only schedule evaluator instead has w retained value bits plus O(log L) addresses and up to O(g) temporary stage gates; these are not silently identified with total physical machine workspace. A search over alternate schedules, if performed, costs additional time and space and is **not** included as a free optimization. No network parallel-span bound is used.

## Independent finite verification and controls

Actual hosted V8 run of **exact committed revision** tmr4-frontier056.v2, seed 20261115, checked 112 valid layout/circuit pairs, 2,594 complete original assignments, 15,594 stage gate executions, 1,812 compiled target branch transitions, 972 exact finite-field rank checks (GF(2), GF(101)), 112 full integer path-count comparisons, four malformed rejections, 130,922 assertions, **zero unexpected failures**. Cases include DISJ and EQ grouped/interleaved for k=1..4, parity 1..6, and 90 deterministic seeded shared-gate circuits. All source, stage and target Boolean outputs matched. An earlier exploratory v1 run did not include integer path counts and is not the publication basis. Node CLI, whole-repository preflight and LaTeX compilation were not executed during this run; checkout unavailable due github.com DNS resolution.

DISJ_3 grouped schedule has a larger live frontier than its legal interleaved schedule. Its assignment matrix on grouped x:y remains rank 8 while the interleaved circuit and OBDD are O(k), so **the theorem survives without a general circuit hardness transfer**. The rank bound uses the *prefix of the actual order rho*, never substitutes an arbitrary grouped cut into an interleaved prefix theorem. EQ has an analogous schedule distinction; XOR/parity retains its cheap affine evaluation. Horn, 2-SAT, bounded-treewidth, Gaussian, autarky, products, padding, alternative encodings, unique solutions, true reuse/rereads by broader machines and compact algebra remain legal controls. This construction is deterministic, Boolean and exact, not a majority or quantum assertion; local basis changes are not used. /341 remains FAIL for full logical UNSAT, /386 RESTRICTED.

## Four gates

| Gate | Verdict | Exact scope and reason |
| --- | --- | --- |
| DISJ sanity | PASS restricted | legal interleaved O(k) path is represented; no inference from grouped rank to all circuits |
| Relativization | PASS restricted; OPEN unrestricted | syntactic construction relativizes and proves no P-vs-NP separation; nonrelativizing NP bridge, algebrization and Natural Proofs issues remain OPEN |
| Simultaneous DTISP | PASS for same-run ledger; OPEN for hierarchy transfer | one actual compiler/evaluator carries T_total and S_peak, neither meets a forbidden FLMV region |
| Deterministic configuration counting | PASS as upper-bound guard | the bound T<=2^O(S+log N) applies to total fixed deterministic read-only-input machines, not a work lower bound or a probabilistic/quantum simulation |

## Original sources and relation to peer work

Wegener, *Branching Programs and Binary Decision Diagrams* (SIAM, 2000), Chapters 2/3, https://doi.org/10.1137/1.9780898719789 , baseline Boolean circuit and OBDD definitions. De Colnet, Ordyniak and Szeider, *OBDDs, SDDs, and circuits of bounded width: Completeness matters* (Artificial Intelligence 2025), https://doi.org/10.1016/j.artint.2025.104458 , cautions that width equivalence must distinguish **complete** OBDDs. Razgon, *On oblivious branching programs with bounded repetition ...* (arXiv:1510.02951, 2015), https://arxiv.org/abs/1510.02951 , matching/pathwidth caveats. Baker, Gill and Solovay, https://doi.org/10.1137/0204037 , relativization barrier.

TMR-4/055 is the exact prior restricted register-to-FBDD compiler, main4_PNP_COST_SOUND_ABSTRACTION.tex, source Git blob cd711193fd36b1a3bd6a60ddc35eb2168d47dd65. This report **closes its named missing source conversion only for supplied topological layouts**, connecting an actual ordinary shared Boolean gate DAG to that register class. TMR-4 pending draft PR #158 concerns a distinct *fixed bipartition signal hypercut* method and is neither silently merged nor overwritten. TMR-1/055 and TMR-2/055 focus respectively on count-preserving wire-CNF and genuine source exact-counting shortcuts, which are compatible but not needed to infer this restricted width implication. The TMR-3/054 draft and TMR-5/051 physical source-head results impose no general proof transfer here.

## Reproducibility

Revision: tmr4-frontier056.v2. Seed 20261115 (LCG arithmetic, fully deterministic). Valid circuits use IDs x_i/g_i, gate truth-table op in [0,15] indexed as bit 2a+b, canonical schedule order and designated output. Full executed audit:
experiments/tmr/tmr4_frontier_circuit_e2e056.js
Immutable raw results:
results/raw/tmr/2026-11-15_1636_TMR4_FRONTIER_E2E056_V8_RAW.json

**Next ONE load-bearing lemma D4-CROSS-ORDER:** either construct and fully charge a uniform decomposition finder that produces an O(log L) or otherwise useful live-frontier schedule for a nontrivial structural circuit family **without supplied advice**, or furnish a compact circuit family disproving the claimed width/switch bound. No tensor static-rank-to-unrestricted-circuit inference, no P vs NP separation. Independent mathematical peer review OPEN.
