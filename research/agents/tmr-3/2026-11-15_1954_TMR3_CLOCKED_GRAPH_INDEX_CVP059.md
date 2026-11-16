# TMR-3/059: a genuine computation-graph first-visit edge can encode Circuit Value

November 15, 2026, 19:54 PST. TMR-3 / PNP Time-Space Tradeoffs, Track B.

STATUS: PROVED/EXACT only in the declared fixed, clocked, block-length-one multitape model; external independent mathematical review OPEN. Finite experiments COMPUTATIONAL. P versus NP OPEN.

## Candidate, quantifiers, and falsifiers

C3-ADAPTIVE-GRAPH-INDEXER-059: There exists ONE fixed total deterministic canonical blank-start locally headed multitape machine M and ONE logspace-computable public time j(N) such that the authentic active MARK work-block identifier at j(N), for block width b=1, is P-complete as a Boolean function of original authenticated source x. The authentic first-visit edge (0,j(N)) of that MARK tape encodes the same bit when all other heads are stationary. If a uniform O(log N)-space, polynomial-time original-source-only indexer answers this query on every valid source, then L=P, which is OPEN.

Four precommitted falsifiers: (F1) the authentic CVP encoding or the dual-rail reduction fails; (F2) the purported public query time depends on the CVP answer or the MARK move is not a real paid transition; (F3) hidden clock, input copy, state or source access is free; (F4) the restricted conditional L=P or b=1 theorem is falsely promoted to an unconditional space lower bound or to Williams's b>=log t conversion.

## Primary literature and existing project corpus

R. E. Ladner, The Circuit Value Problem Is Log Space Complete for P (1975), DOI https://doi.org/10.1145/990518.990519; R. R. Williams, Simulating Time With Square-Root Space (STOC 2025), Sections 2-3, DOI https://doi.org/10.1145/3717823.3718225. The previous TMR-3/055 and independent TMR-5/052 source-to-output studies established a P-complete canonical VALUE bit with a public head schedule. The TMR-3/058 frontier theorem in unmerged PR #187 uses an explicit original-source-only active-block generator G as an assumption. The present result attacks this named assumption: the graph-position query itself, not only its work-cell value, can carry P-complete information. TMR-3/057 and TMR-5/055 already provide nonlinear easy-source controls; no priority is claimed for re-proving them.

The governing end-to-end and compatible SAT-compression directives were consulted, as were current AGENTS.md, CODEX.md, the research skill, owner manuscript on the stacked #187 branch, five current handoffs, recent issue #3 entries, and materially relevant original reports and tests. No retired root text proof trackers were read. Local GitHub cloning failed DNS, so repository-wide preflight, native TM microcode and full TeX build were NOT run.

## Original source and exact known completeness transfer

Use the already authenticated CVP source word: unary 1^n0, then n gate records with 2-bit opcode CONST0/CONST1/AND/OR followed by two n-bit one-hot predecessor masks. Nonconstant predecessors are strictly earlier gate indices, duplicate references allowed. Constant gates have zero masks, terminal gate n-1 is output. N=2n^2+3n+1. Invalid words reject. The existing fixed locally headed interpreter A runs on a genuine read-only source with blank work tapes and has T_A=O(n^3 log(n+2)), S_A=O(n+log(n+2)) on the same computation. Its VALUE tape physically stores earlier gate outputs; the evaluator does not receive an answer oracle.

General AND/OR/NOT/constant Circuit Value reduces in logspace to this monotone grammar: maintain positive and negative rails for each original gate; swap rails for NOT; use De Morgan dual AND/OR gates; append an output-copy AND(z,z). A logspace transducer writes unary header, source opcodes and one-hot masks using polynomially many source rereads. The terminal bit f(x) is consequently P-complete. This baseline is a KNOWN THEOREM plus the previously audited restricted compiler, not a new complexity-class separation.

## Charged public-clock and last-movement lemma

For any fixed deterministic total machine A with T_A(N)<=N^d after a harmless fixed constant adjustment, construct a length-only deterministic clock K. It scans source length N and returns the original read-only head left, using O(log N) writable counter cells and content-independent movement. It then performs at least N^(d+2) and at most N^O(d) physical counter transitions. All carries and sweeps are actual paid local-head transitions. Its exact stopping epoch kappa(N) depends only on source length, and is logspace-computable: simulate the fixed logspace, polynomial-time length-only clock with O(log N) counters and a polynomially bounded elapsed-step register, not with CVP advice.

Run A and K as a synchronous product in ONE fixed multitape transition system on disjoint constant-many writable tapes. During each global transition, A executes its ordinary next step and K its own physical counter step. Once A halts, freeze its output bit and heads while the clock continues; the clock is deliberately longer than A's worst case. Source length scanning and subsequent A source input access are sequentially paid on the same single read-only input head. K no longer uses that input head after initialization. No separate machine contributes free time or space.

Add a fresh blank MARK tape, its head held at cell 0 until the public clock stops. At the one genuine paid transition following clock completion, move MARK right if and only if A(x)=1; otherwise stay. At the immediately following paid dummy-read block j(N), MARK is active at block 2 if and only if f(x)=1, and block 1 otherwise (one-indexed blocks, b=1). All other heads are frozen during the postlude, and its fixed public time j(N) depends only on N. Invalid source words are rejected by A but still pass through the complete clock and terminal postlude, yielding a total machine.

Each physical step is one block, hence the machine is automatically block-respecting with b=1. The true MARK block 2 has never been active previously. In the true case this produces the real Williams first-visit edge (0,j(N)) on MARK; in the false case MARK stays in the already active block 1 and no such new-visit edge exists. As other heads are stationary during the postlude, none introduces a spurious first-visit edge at j(N). For all valid CVP sources:

    [MARK block at j(N) = 2]
      = [MARK first-visit edge (0,j(N)) exists]
      = f(x).

Membership in P follows by actually simulating the fixed total polynomial-time M. Hardness follows from the logspace dual-rail source reduction and the logspace construction of the public binary j(N), whose bit length is O(log N). Hence this one fixed authentic source-dependent graph-index predicate, and this specific first-visit predicate, are P-complete. The implication of a polynomial-time logspace source-only graph provider would be L=P, a conditional consequence rather than a proved exclusion. This uses no oracle, nonuniform per-input advice, padded PSPACE reduction or false direction of a SAT reduction.

## Same-physical-execution ledger and limitations

Input-length acquisition and clock initialization: poly(N) paid transitions, O(log N) scratch. Synchronous clock plus genuine CVP evaluator: kappa(N)=N^O(d) physical transitions and peak S_A(N)+O(log N) writable cells, with every frozen A cell retained until clock completion. Terminal MARK move, dummy read, output and halt: O(1) additional paid transitions and MARK cells. The combined original machine has T_M=poly(N), S_M=O(S_A(N)+log N); on this canonical source this is O(sqrt(N)+log N) peak workspace, NOT logspace. Direct full simulation of M is a legal source-only graph-index method at that same polynomial time and polynomial-root space. A hypothetical different logspace indexer is not spliced into the original M's resource bound.

Block width b=1 is a load-bearing qualifier. Nothing here establishes that the P-complete graph edge survives the separate b>=log t Williams block-respecting converter or that arbitrary Tree Evaluation can be computed with less space. The constructed head move demonstrates why the original-source-only G premise in TMR-3/058 must be PROVED for a declared machine class, rather than silently generalized to all work-dependent executions.

## Finite execution evidence

Executed standard-library CPython source revision tmr3-clocked-graph059-v1, deterministic seed 202611151954: 1,977 valid monotone sources, 945 general-circuit dual-rail reductions, 1,015 malformed-source rejections, 12,814 assertions, zero failures. The exact script published source Git blob b40179b9a5145b49f367ac3dc5de6ca0fbd470c6; raw JSON blob d56e0f8f66c69bcff161ead0ae91091800b78041. The code verifies source grammar, positive/negative rails, terminal Boolean outputs, and both MARK end locations. Its public macro-loop event index is explicitly synthetic: no native TM clocked-microtransition schedule, formal source-to-graph converter or P-hardness theorem was experimentally verified. The symbolic construction and class-theoretic transfer are separate. Independent review OPEN.

## Four mandatory verification gates

| Gate | Status and reason |
|---|---|
| DISJ | PASS restricted. No rank-to-runtime transfer. DISJ, Horn, 2-SAT, affine/Gaussian, treewidth, selector, compact DAG and unique-solution shortcuts stay legal. |
| Relativization | NOT APPLICABLE WITH REASON to a separation, none claimed. The P-completeness reduction yields a conditional L=P; nonrelativizing NP bridge, algebrization and Natural Proofs remain OPEN when relevant. |
| Simultaneous DTISP | PASS in the declared original M: clock, A, MARK, source, output counted together. OPEN for any strictly forbidden FLMV/SAT machine. |
| Configuration counting | PASS as an upper-bound consistency check for deterministic total machines T<=2^O(S+log N), never a work lower bound and never transferred automatically to random or quantum computation. |

/341 remains FAIL as a full logical UNSAT authority and /386 remains RESTRICTED. P versus NP remains OPEN.

## One next load-bearing lemma

C3-ADAPTIVE-GRAPH-INDEXER-BGELOG: reconstruct or falsify this source-derived index difficulty under the actual b>=log t converted-machine model, with a public authenticated converted-block query, charged conversion time/space and an honest same-realization ledger. Alternatively identify a structural promise that permits a cheap uniform source-only indexer and prove the promise covers the intended Williams simulation. Neither is assumed.
