# TMR-3/067: polynomial-depth genuine overwrites with a logarithmic-space canonical provider

November 17, 2026, 11:24 PST. TMR-3 / PNP Time-Space Tradeoffs, Track B.

**Status:** PROVED/EXACT for an explicit restricted affine ping-pong computation and its source-derived virtual value identities, pending independent mathematics and native-TM review. Separate finite program: COMPUTATIONAL. General Williams/HPV conversion, general source-access provider, height-sublinear nonassociative Tree Evaluation, and P versus NP remain OPEN.

## Exact pipeline and candidate

Named dependency: **C3-POLYNOMIAL-CAUSAL-DEPTH-REPLAY067**, a constructive extension of the C3-CAUSAL-DEPTH-CERTIFIER target after TMR-3/066. The /066 recursive 2-branch evaluator is efficient because depth k=O(log N). This run asks whether logarithmic causal depth is NECESSARY for a cheap authentic work-bit provider when genuine overwrites, large physical live frontier, and public movement blocks all occur together.

Claim: there is ONE fixed total blank-start locally headed deterministic multitape program M, which, for every sufficiently large power of two b and every authenticated source x=1^(b-1)0 y with |y|=M_cells=b^3, executes R=M_cells-1 genuine two-tape overwrite layers of depth Theta(N). Yet a uniform original-source-only provider returns EVERY reachable data-tape bit at every completed time using O(log N) space and polynomial time. A single fully charged virtual machine outputs the exact final bit with O(N^2 polylog N) time and O(log N) space. Its evaluator exploits GF(2) linearity, NOT a general-purpose nonassociative Tree Evaluation speedup.

Falsifiers established before primary-source review: (F1) the update accidentally uses a just-written rather than completed old-layer value; (F2) a head crosses a b-cell boundary at an inadmissible time, or source validation is free; (F3) Lucas/submask reconstruction fails at zero boundaries or for intermediate overwritten cells; (F4) total Q, source seeks, head indices, live state or output is omitted, or a restricted affine procedure is advertised as a general arbitrary-TM/NP result.

## Authentic source and physical machine

Valid inputs have b a sufficiently large power of two, header 1^(b-1)0 and exactly b^3 binary payload bits y_0,...,y_(M_cells-1), total N=b+b^3. A total parser checks the header, b, length, terminal endmarker and trailing data before initializing the simulation; malformed words reject. Use a fixed b-cell phase-clock and a fixed number of O(log N)-cell counter tapes; all original work tapes begin blank. Input-content differences do not affect the schedule for valid same-length words. Source scanning, clock initialization and validation must be scheduled with charged local head movements. The standard /066 alignment construction delays source-head block crossings until b-boundaries and can pad a valid-source prefix to a public length-only duration; no advice or preloaded checkpoint is present.

A forward seed writes y_i on tape A at cell i. Each successive round ell=1,...,R reads the PREVIOUS COMPLETE layer on the alternating source tape, and overwrites the opposite destination tape in the forward direction. A single control bit p remembers the preceding OLD source-tape bit. At cell i, read a=V_i^(ell-1), write a XOR p, and set p=a (with p=0 at i=0). Both data heads travel together. Reverse return traversals perform NO writes and reset p at the start of each forward layer. The exact source-independent logical rule is

    V_i^(0)=y_i, V_i^(ell)=V_i^(ell-1) XOR V_(i-1)^(ell-1),
    where V_(-1)^(ell-1)=0.

The seed and each overwrite stage traverse M_cells positions forward and M_cells back. Starting aligned at a b-block boundary, the forward traversal takes M_cells steps. Pause b-1 steps at the far endpoint; the first leftward crossing then takes place on a multiple-of-b transition. Reverse travel takes M_cells steps, ending at position zero; one final pause aligns the next forward sweep. Thus a stage takes exactly D=2*M_cells+b transitions and EVERY crossing of either long data tape lies at an integer multiple of b. A fixed unary tally on a separate work tape can mark and count M_cells-1 layers, advancing at an aligned stage transition and reading a public seed-installed endpoint; its visited cells add O(M_cells) to the physical space and its block crossings obey the same phase rule. A binary counter with fixed b-step stage slack is another implementation. Both are fully charged, never treated as finite-control unbounded arithmetic.

The valid-source prefix may be padded by a uniform public clock to leave all heads at the required positions and the elapsed time a multiple of b. The following exact D-stage equations describe the post-authentication core, not the native transition count of an uncompiled parser. The original complete run has T_original=Theta(M_cells^2) up to fixed polynomial-log initialization overhead and S_original=Theta(M_cells)=Theta(N) visited cells. Since log T_original=O(log b) and b grows, it is block-respecting with b >= ceil(log2 T_original) for sufficiently large b. The movement word is public, K=1; after seed the M_cells/b=b^2 blocks of the first data tape are future-live. The genuine causal dependency chain from V_i^(R) back through V_i^(R-1),...,V_i^(0) has depth R=Theta(N), irrespective of semantic cancellation.

The physical machine's output bit is the last cell of the final layer V_(M_cells-1)^(R). It is not an arbitrary proof oracle output.

## Exact affine reconstruction theorem

Let S be the zero-boundary left shift on F_2^(M_cells), (Sv)_i=v_(i-1) for i>=1, (Sv)_0=0. Then the physical recurrence gives

    V^(ell) = (I+S)^ell y.

In characteristic two, (I+S)^(2^h)=I+S^(2^h). With ell's binary digits ell_h,

    (I+S)^ell = product over h with ell_h=1 of (I+S^(2^h)).

Consequently for every 0<=ell<=R and 0<=i<M_cells,

    V_i^(ell) = XOR_{0<=j<=min(ell,i), (j AND ell)=j} y_(i-j).

This is Lucas's parity-of-binomial-coefficients identity, proved directly by the displayed Frobenius factorization. No precomputed long state or algebraic coefficient table is required. A uniform provider enumerates j in binary, tests the subset condition in O(log N) bits and seeks the actual read-only source head to y_(i-j), paying up to O(N) local moves per term. At most ell+1<=M_cells terms occur. Thus every canonical layer-cell request costs O(N^2 polylog N) time and O(log N) writable space.

For an arbitrary completed physical time tau and tape h=A/B, source-independent phase arithmetic selects the latest ell of the correct parity whose forward step for cell i is finished. Before any write the symbol is BLANK; otherwise the above formula returns the authentic current bit. In a post-validation core clock with stages of length D and write to i at t_ell(i)=ell*D+i+1, the latest eligible ell is at most min(R, floor((tau-i-1)/D)), reduced by one if its tape parity is wrong. For a physical time in the validation prefix, that tape is blank. Thus the interface handles partial overwrite sweeps and not just completed layers. It also returns the write/blank flag, not merely zero for a blank tape.

## One complete virtual source-to-output execution

One sequential deterministic virtual machine (not a network) validates the source and retains b,M_cells,R,D in O(log N) bits. It issues public head/block queries for every relevant time block, Q_G=p B where p is the fixed total tape count and B=ceil(T_original/b)=O(N^2 polylogN/b). It generates each query address and tape block from arithmetic on phase, layer, local head offset and public clock state in polylog bit operations; no B-bit word is materialized. It then evaluates the final authentic output by the displayed Lucas sum for ell=R and i=M_cells-1, using exactly Q_V=2^popcount(R)=M_cells original-source bit queries since M_cells is a power of two and R=M_cells-1. For any additional Q arbitrary adaptive completed-time checkpoint-bit requests, the same provider supplies them at an added O(Q N^2 polylog N) time, O(log(N+Q)) indexed-state space, provided the query stream is supplied sequentially.

Partition the actual machine's work into disjoint phases: source validation O(N polylogN) or a conservative O(N^2 polylogN) public parser clock; graph-stage arithmetic O(p B polylogN); source-seeking and XOR for Q_V=M_cells real bit requests O(Q_V N polylogN); output and final validation O(polylogN). All are paid on the SAME execution, with no tape-block materialization, no uncharged checkpoint and no recursive ancestor stack. The resulting simultaneous upper bounds are

    T_virtual = O(N^2 polylog N),  S_virtual = O(log N).

The terminal bit equals XOR_i y_i for R=M_cells-1, which is an explicit lawful direct shortcut; this example cannot prove any work lower bound. The stronger interface statement is that EVERY intermediate overwritten data-bit has a cheap provider, not just that parity is easy. A whole b-bit block still requires b output bits or a physical b-bit buffer. Arbitrary nonaffine updates, work-dependent head schedules, and an improved evaluator for arbitrary nonassociative trees remain OPEN.

## Hostage Negotiator relationship

Reviewed Hostage_Negotiator.pdf (71 pages) and PNP_Hostage_Review_and_Agent_Restart_2026-11-17.md. The document's source-grounded certificate versus small-evaluator EXISTENCE distinction is retained. This restricted affine provider is explicitly BUILT, not inferred from global consistency, uniqueness, fresh query counts, or an unproved short-description compression theorem. Its query algebra is not a general information-necessity or SAT lower-bound potential. The correct affine output-relevance control is r(A;B)=rank([A;B])-rank(A), but this paper makes no assertion that independent source queries necessarily reduce semantic target ambiguity.

## Reproduction, gates and scope

Executed exact CPython source revision tmr3-affine-overwrite067-v1, seed 202611171124, twice with byte-identical raw JSON. Exhaustive all 256 sources at b=2; 28 pseudorandom b=4 sources with all layer/cell tests; 3 pseudorandom b=8 sources with sampled layer/cell tests. 287 valid sources, 1,148 malformed controls, 21,525 last-writer checkpoint queries, 67,648 verified boundary crossings, 136,470 public graph query checks, 986,256 enumerated Lucas terms, 312,140 assertions, zero failures. The Python interpreter DOES materialize full arrays to validate semantics and is NOT the claimed low-space TM. Only the core controller, not a full native parser/clock finite transition table, was microtraced. No literal HPV implementation or independent external mathematics review. A GitHub-connected source read was used because a local repository checkout failed DNS; repository preflight was not executed.

Code: experiments/tmr/tmr3_affine_overwrite067.py
Raw: results/raw/tmr/2026-11-17_1124_TMR3_AFFINE_OVERWRITE067_PY_RAW.json
Source SHA256: 9c72ee36809410b743242fc8035675dfef4a42b944d56e68334644cb4b6d6b9e
Raw SHA256: 0614e4dd73595e91a25bc45fe1d41da95f167f19c3c1865e28f1867c3f4b0679

Four gates:
* DISJ sanity: PASS restricted. This is a positive affine upper algorithm; direct parity and compact source methods remain legal, no rank-to-work claim.
* Relativization: NOT APPLICABLE WITH REASON to a separation, none asserted. Any NP-level BGS/algebrization/Natural Proofs bridge remains OPEN.
* Simultaneous DTISP: PASS for the explicitly separate original and virtual machines, with their own actual T and peak S. A forbidden-region SAT transfer remains OPEN.
* Deterministic configuration counting: PASS as upper-bound consistency only, never a runtime lower bound or automatic randomized/quantum claim.

No uncharged isolation, auxiliary-variable counting, circuit-to-CNF or majority/quantum transfer is used. Applicable Horn, 2-SAT, affine, treewidth, selector, unique-solution, field/local basis, products, padding, caching, compact and recomputation controls remain legal. /341 FAIL as full UNSAT authority; /386 RESTRICTED. P versus NP remains OPEN.

## One next load-bearing lemma

**C3-NONAFFINE-LONG-DEPTH-TRANSFER:** identify a source-authenticated, polynomial-time and sublinear-space representation of genuinely nonlinear, polynomial-causal-depth overwrite computations, or find a precise fixed-class obstruction robust to source replay and legal algebraic compression. Any proposed generic Williams/HPV transfer must supply a fixed compiler, complete graph/node access and a genuinely improved nonassociative TreeEval evaluator with a single matched query/time/space ledger. This restricted affine argument does not supply them.

Original references: Ryan Williams, *Simulating Time With Square-Root Space*, arXiv:2502.17779v1 (2025), sections 2-3; Lucas's theorem (1878), also a direct corollary of Frobenius in characteristic two; TMR-3/066 original report and implementation.
