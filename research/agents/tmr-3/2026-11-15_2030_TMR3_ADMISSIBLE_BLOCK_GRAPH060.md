# TMR-3/060: admissible-block graph hardness and the conversion-preservation distinction

2026-11-15 20:30 PST. TMR-3 / PNP Time-Space Tradeoffs, Track B.

## Result and status

**PROVED/EXACT, restricted constructive normal form; independent mathematical review OPEN.** There is one fixed total, blank-start, locally headed deterministic multitape machine with a P-complete authentic first-visit graph-edge predicate, at admissible block width b >= ceil(log2 t) and in fact b = Theta(t^(1/3)). The clocks, source processing, marker trajectory, and output are charged on one execution.

**Important qualification:** this constructs an explicit already block-respecting realization of the CVP-based mechanism. It does NOT prove that an unspecified implementation of the Hopcroft-Paul-Valiant (HPV) folded-copy compiler preserves the particular marker in TMR-3/059. Williams's Lemma 2.1 is an existence/equivalent-output statement, not a trace-preservation contract. Literal transport of the old marked edge through a pinned HPV compiler remains OPEN. The universal claim that every equivalent compiler must preserve it is false: a semantically unused marker tape can be omitted.

The named dependency is **C3-ADAPTIVE-GRAPH-INDEXER-BGELOG**. The new theorem closes the existence-of-hard-authentic-indices gap at legal b for the whole block-respecting target class. It does not close the general low-space provider/evaluator construction.

## Candidate and four falsifiers, before primary-source search

Candidate: preserve an answer-dependent first visit by replacing the width-one marker with a publicly aligned terminal sweep in a fully charged block-respecting realization.

F1: an equivalent converter need not preserve a named head, block, or time. F2: the query index or alignment may depend on the circuit's answer. F3: clock initialization, the full source evaluator, visited cells, or source-head movements may be hidden. F4: b=1, b>=log t, one chosen representation, and every equivalent representation may be conflated. These checks are all retained in the result's scope.

## Primary-source reconstruction

Williams [1], Lemma 2.1, supplies an equivalent O(t)-time block-respecting machine for log t <= b <= t; Section 3.2 defines the authentic graph's previous-access and first-visit edges. Its inexpensive edge tests are GIVEN the movement word, not a procedure that recovers that word from the original source.

HPV [2], page 333, uses a bouncing clock and reversed neighboring-block copies. The paper explicitly leaves the copying/marking details to the reader. Therefore no unique literal converter or physical-head projection can be recovered from that statement alone. The present argument uses their block-respecting definition and Williams's actual graph definition, not a purported execution of unspecified compiler microcode.

Ladner's Circuit Value P-completeness [3] is the baseline hardness fact. The one-hot monotone encoding and dual-rail conversion from /055 and /059 are retained with their original scope. No novel priority is claimed for encoding an output in a head position.

## Exact source and real evaluator

A valid source x has unary 1^n0, followed by n gate records. Each record has a two-bit code for constant 0, constant 1, AND, or OR, and two n-bit predecessor masks. Constants have zero masks; nonconstants have exactly one selected predecessor in each mask, strictly earlier than the gate. The last gate is output. N=2n^2+3n+1. Invalid binary strings have f(x)=0.

A total fixed local-head evaluator A first validates the header and total length before allocating the VALUE prefix. It rescans source records as needed, uses one n-cell VALUE tape, physically scans it to obtain each predecessor, and writes the gate result. One may implement it with O(n N log(N+2)+N log(N+2)) time on valid inputs, O(N^2 log(N+2)) as a loose all-input envelope, and O(n+log(N+2)) workspace on valid inputs. Malformed size headers are rejected before any oversized allocation. These bounds are below C0(N+d)^3 for a fixed C0. Each individual work head stays within the first N+d cells for a sufficiently large fixed d; counters may be put on separate constant-many tapes.

The source language is P-complete: replace each general circuit gate by positive/negative monotone rails, use De Morgan duals and rail swapping, copy the true output to the final gate, then print the one-hot records with logspace counters and source rescans. The increase in encoded length is polynomial and both Boolean labels are preserved.

## Explicit blank-start block-respecting construction

Fix an even constant C >= 2 larger than the evaluator's cubic-time constant. Fix d >= 8 large enough that 2^b >= (C+4)b^3 for every b >= d. Such a fixed d is computable by finite search, since 2^b/b^3 increases for b>=8. Put b(N)=N+d.

The machine has A's fixed tapes, three additional clock tapes, and a fresh MARK tape. All work tapes start blank; all heads start at zero.

**Bootstrap, exactly b steps.** Sweep the original N-bit source and then d blank positions. On all three clock tapes put a left endpoint at cell 0 and a right endpoint at cell b-1. The first b-1 steps move right; the last writes the endpoint and stays. The endmarker plus a fixed d-state suffix counter determines the endpoint; the machine does not need a free N or b oracle. The original source head and clock heads remain inside their first b-cell blocks. MARK remains at zero.

**Clocked evaluation, exactly C b^3 steps.** Each clock has a direction bit in finite control. When enabled it moves one cell in that direction if possible. At an endpoint facing outward it holds for one step, reverses direction, and emits a pulse. Thus a half-sweep takes exactly b enabled steps, not b-1. Enable clock 1 at every transition, clock 2 only on clock-1 pulses, and clock 3 only on clock-2 pulses. A clock-3 pulse occurs after exactly b^3 physical transitions. Stop the epoch after C such pulses, where C is a fixed finite-control constant.

Run A synchronously on separate tapes during the same epoch, paying its return to the original source's start, parsing, all reads, gate evaluation, and output-bit retention. Once A finishes, freeze its tapes and retain f(x) in finite control while the clocks continue. C was chosen so it always finishes. This is one fixed multitape product transition system, not three processors or an oracle. Since C is even, all three clock heads are at their right endpoints after the epoch.

**Alignment, exactly b steps.** Freeze A and clocks 2 and 3. Let clock 1 perform one half-sweep to its left endpoint. MARK is still zero.

**Marker sweep, exactly b steps.** On the next rightward half-sweep, move MARK right on each of the first b-1 steps. On the final endpoint-hold step move MARK right iff f(x)=1, and otherwise stay. Thus it ends at b-1+f(x). The only possible tape-block crossing is this final move at global time C b^3+3b, an integer multiple of b.

**Read/output, one step.** Read the final MARK cell and halt with answer f(x). This begins time block

    j(N) = C b(N)^2 + 4.

Every other tape head always stays inside its first block. This includes the original input head, all work-value and counter heads, and all clocks. Hence the ENTIRE blank-start execution, including bootstrap and authentication, is block-respecting, not merely its suffix.

The exact whole-machine time and simultaneous workspace are

    t(N) = C b(N)^3 + 3b(N) + 1,
    S(N) = 3b + (b+f(x)) + O(n+log(N+2)) = Theta(N).

The marker visited-cell term is b on NO and b+1 on YES. Frozen A storage remains charged. Time is partitioned into bootstrap, synchronous product, alignment, sweep, and read. A's concurrent steps are not added again to the product's elapsed time. The choice of d guarantees b>=ceil(log2 t), and b=Theta(t^(1/3)). This intentional clock padding establishes a normal form, not a time-space improvement or a hardness amplification.

## Authentic graph-edge theorem

Use Williams's one-indexed tape blocks. Let m be MARK's tape ID. At the start of time block j(N), its active block is 2 exactly when f(x)=1. Block 2 has never previously been read on MARK; all preceding MARK reads were in block 1. Thus

    ((m,0,2),(1,j(N))) is an authentic first-visit edge
        iff block(m,j(N))=2
        iff f(x)=1.

The source node (m,0,2) is the initially blank second MARK block. The target (1,j) is a genuine final-time node; the definition permits any target tape ID. Chronological edges are separate and do not erase this distinction.

Both b(N) and j(N) are computable in O(log N) workspace with actual input scanning and binary arithmetic. The reduction prints the unchanged authenticated source and an O(log N)-bit query index. Membership of the edge language in P follows from full simulation (or directly from A). Hardness follows from the logspace CVP compiler. It is therefore P-complete.

Consequently a uniform O(log N)-workspace, polynomial-time source-only provider answering these authentic graph queries on every source would imply L=P. This is NOT a proved exclusion, a superlogarithmic lower bound, or a reason to rule out a T^(1/3)-space evaluator.

## What is and is not transported through conversion

The new machine already satisfies the source's exact block-respecting definition. Identity normalization, with one idle tape added if the precise tape count is wanted, is a valid witness to Lemma 2.1 for this machine. Equivalently, a uniform normalizer may recognize this one fixed program and use identity, and use HPV on other programs. This proves existence inside the actual eligible target class.

It does not assert that the predecessor /059 program under a particular unimplemented folded-copy compiler has the same distinguished edge. A simple falsifier to mere coarsening is 0 and 1 lying in the same b-cell block for every b>=2: the old one-cell marker is not preserved by replacing width one with b. Furthermore, because MARK does not determine acceptance, an equivalent compiler can omit that tape. Even state reconstruction or a graph-preservation property must be explicitly declared, not inferred from equivalent output.

No claim is made for every admissible b(N), especially b=Theta(log t) with input spread over many blocks. No claim is made that general graph recovery is intrinsically necessary: guessed schedules, validation, oblivious normalization with paid overhead, and joint evaluation remain legal.

**Matched normalization control.** Define M0 by changing only the final conditional MARK crossing to a stay. Keep the same source evaluator, clocks, bootstrap, alignment, b-1 unconditional marker moves, dummy read and output f(x). M0 has exactly the same t(N), b(N), correct answer and all but at most one visited writable cell. Every head now stays in block 1 on every source. Its authentic block graph is length-only, and the queried second-block first-visit edge is always absent. Thus even an equally timed, equally scoped, block-respecting equivalent machine can erase the hard edge. The information remains in node values. This is a symbolic counter-construction, not a claim that the native M0 transition table was tested.

## Four-gate table and end-to-end ledger

| Gate | Verdict |
|---|---|
| DISJ sanity | PASS restricted. No assignment-rank or general SAT lower bound. Easy Horn, affine, 2-SAT, treewidth, compact and selector controls remain legal. |
| Relativization | NOT APPLICABLE WITH REASON to a separation: none is asserted. This is an ordinary-machine P-completeness reduction and conditional implication. No nonrelativizing NP step, algebrization or Natural Proofs claim. |
| Simultaneous DTISP | PASS for the explicit one-machine cubic-clock construction. The logarithmic provider is hypothetical and separate. Generic improved Tree Evaluation and strict SAT forbidden-region transfer remain OPEN. |
| Configuration counting | PASS as upper-bound consistency only: polynomial time with Theta(N) visited storage is compatible with 2^O(S+log N). No random/quantum inference. |

The pipeline is authenticated source -> actual blank-start A/clock/marker machine -> actual Williams graph -> one specified query -> conditional L=P consequence. It is a counterexample to silently assuming cheap authentic graph recovery for ALL normalized machines, not a completed provider -> improved evaluator pipeline. /341 remains FAIL as a full logical UNSAT authority; /386 remains RESTRICTED; P versus NP OPEN.

## Finite evidence, corpus reconciliation and limits

The separate deterministic Python audit revision tmr3-admissible-block-marker060-v1, seed 202611152040, was executed twice with byte-identical JSON: 3,279,441 assertions, zero failures, 150 local clock/postlude controller cases, 768 authenticated monotone circuit sources, 775 malformed controls, and 16 equal-length opposite-label pairs. Controller widths were 2..24, even round constants 2 and 4, with varied ready-signal times. Clock-head movement and every marker block crossing were checked transition by transition. Some small controller tests intentionally do not meet the asymptotic b>=log t side condition; legal-width source diagnostics are separate.

The CVP result and parser are checked separately from the clock. The harness injects the evaluator's completion signal within the deadline. Test constant C=2 is NOT a certified constant for a native compiled A. No native complete-CVP transition table, literal HPV converter, generic Cook-Mertz evaluation, independent mathematical review, or full repository preflight was executed. The local git checkout attempt failed DNS. A local LaTeX compilation is recorded separately only if actually run.

Reviewed: current end-to-end directive, current AGENTS/CODEX/skill, main3 on main and complete draft /059 manuscript at blob 5ed28350bf84b60d7c5d0e2dff30d28f65881196, all five current compact handoffs, relevant main4/main5 material, recent issue #3 entries, original /059 report/source, and primary Williams/HPV papers including PDF screenshots. Earlier /054-/059 proofs are preserved verbatim in the archived predecessor manuscript rather than silently overwritten or promoted. Retired text trackers and schedules are untouched. The new manuscript is reorganized around the active normal-form theorem and its exact limits; older results remain cited and recoverable.

**Next dependency:** fix the particular converter intended by the improved simulation and prove a usable index-generation promise OR replace authentic-graph recovery by a paid guessed-graph verification interface, with an explicit total evaluator query bound. The present existence theorem does not certify that narrower interface. Do not spend another cycle merely varying the marker clock.

## References

[1] R. R. Williams. Simulating Time With Square-Root Space. STOC 2025; arXiv:2502.17779v1, Lemma 2.1 and Section 3.2. https://arxiv.org/html/2502.17779v1

[2] J. Hopcroft, W. Paul, L. Valiant. On Time Versus Space. JACM 24(2), 332-337, 1977, especially p.333. https://doi.org/10.1145/322003.322015

[3] R. E. Ladner. The Circuit Value Problem Is Log Space Complete for P. SIGACT News 7(1), 18-20, 1975. https://doi.org/10.1145/990518.990519
