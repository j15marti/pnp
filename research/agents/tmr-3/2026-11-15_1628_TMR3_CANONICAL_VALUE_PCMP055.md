# TMR-3/055: P-complete canonical work values with public work-head movements

**2026-11-15 16:28 PST | TMR-3 / PNP Time-Space Tradeoffs | Track B**

**Status:** PROVED/EXACT within a specified deterministic blank-start circuit-value service, independent mathematical review OPEN. Classical circuit-value P-completeness is a KNOWN THEOREM. The concrete two-way interface and conditional corollary are project-specific. Finite checks are COMPUTATIONAL. No generic Tree Evaluation space improvement, P != L, SAT lower bound, or P versus NP proof is asserted. P versus NP remains OPEN.

## 1. Candidate, end-to-end target, and falsifiers

**Named dependency C3-VALUE-PROVIDER:** authentic encoded circuit source -> total parser -> fixed deterministic machine with blank work tapes and genuinely revisited gate values -> a publicly generated VALUE-head movement schedule -> canonical terminal work-bit query -> correct Boolean output -> complexity-theoretic provider condition.

Candidate: the complete movement schedule for a *particular writable value tape* can be computable from input length alone, while predicting even its one terminal work bit remains P-complete. An all-input **logarithmic-space**, polynomial-time replacement for this source-to-work-value service would imply L=P. This is a conditional barrier, not an unconditional workspace lower bound.

Precommitted falsifiers: (F1) output accidentally encoded directly or reduction not logspace; (F2) secret data-dependent VALUE-head position; (F3) preloaded checkpoint or uncharged source and work reads; (F4) unjustified inference P != L or all-head Williams graph obliviousness.

## 2. Fixed authenticated original source and physical service

For n>=1 the source word consists of unary 1^n0 followed by n topologically ordered monotone gate records. Each record has a 2-bit opcode (00/01 constants, 10 AND, 11 OR) and two n-bit one-hot operand masks. Constant masks are zero. Each nonconstant mask selects exactly one prior gate; the two operands may coincide. Gate n is the output. Its exact length is

    N = (n+1)+n(2+2n) = 2n^2+3n+1.

A single uniform parser checks the entire original binary word, its header, length, masks and earlier-gate condition, rejecting malformed words. A locally moving input head can rescan any row at cost O(N); a fixed number of counters of O(log n) bits suffice. No persistent gate-record table is required.

The fixed machine M starts with blank writable tapes. Its VALUE tape has n actual writable cells, initially blank denoting zero. For j=0,...,n-1, it physically returns VALUE's head to zero, sweeps every cell 0..n-1 and reads the previous genuine work symbols, captures the two operands selected by the current original-source masks, then moves to cell j and writes the gate's computed Boolean value. Every source row is reacquired through real local input-head movements, with masks read synchronously during the VALUE sweep. Its last written VALUE[n-1] is the output.

**Theorem 055-A.** On every valid source this machine's terminal bit is the circuit value, and the entire VALUE-head macro itinerary at stage j depends only on (n,j), not on gates, source data or prior work values. For the specified scans it makes exactly

    VALUE reads Q=n^2,
    VALUE writes W=n,
    VALUE head movements H=2n^2-3n+1.

**Proof.** Induct on stage j. Both operands refer only to earlier gates and are captured from true previously written cells on the complete sweep, so the write at j stores the exact gate value. All earlier cells remain correct. The terminal cell is therefore the designated output. At stage zero the head moves 2n-2 cells. For j>=1 it returns j-1 cells to zero, sweeps n-1 cells, and moves n-1-j cells to j: 2n-3 moves per stage. Summing yields the identity. The route depends only on (n,j). QED.

A conventional fixed finite-alphabet, constant-tape interpreter with the declared parser uses

    source-head movements <= 2nN+2N,
    T_M = O(n^3 log(n+2)),
    S_peak = O(n+log(n+2)) writable cells/bits.

The upper bounds charge parser and authentication, source seeking, gate-mask scans, data sweeps, both captured bits, scratch/index counters, writes and output on ONE execution. The VALUE array is n live work cells. The *entire* multihead movement trace is not claimed oblivious: only the specifically identified VALUE head has the public macro schedule. Physical native transition-table compilation and a source-head microtrace are not executed; the bounds follow from ordinary sequential tape scans/counters, not from a Python heap measurement.

## 3. Known P-completeness transfers through this exact interface

**Theorem 055-B.** The total language CANONICAL-VALUE, consisting of authenticated source words whose final VALUE cell is 1, is P-complete under uniform logspace many-one reductions.

**Proof.** Membership is given by Theorem 055-A. The topologically ordered Circuit Value Problem is P-complete under logspace reductions [1,2]. Reduce any general ordered circuit by dual-rail monotone translation: maintain a true and false wire for every gate; constants create both rails, NOT swaps them, AND pairs true rails with AND and false rails with OR, and OR does the reverse. A swapped rail is implemented by legal AND(z,z) copy gates. The resulting monotonically ordered gate program has at most 2g+1 gates for an original g-gate circuit; append an identity copy of the final true output as the last gate. The transducer emits its unary gate count and each one-hot mask position by O(log g) counters and input rescans. The output length O(g^2) is polynomial and the reduction does not evaluate the original circuit. The new final bit equals the old output on every instance. Hence this service is P-hard and, with P membership, P-complete. QED.

**Conditional corollary.** A uniform O(log N)-writable-space, polynomial-time virtual provider answering the canonical terminal VALUE bit for all authenticated sources would place the P-complete language in L, hence prove L=P. This consequence is OPEN. It is **not** an unconditional superlogarithmic lower bound; a provider using O(T^(1/3)) space could still be possible. The original interpreter consumes O(n) physically real work cells and can always compute the output by the paid ordinary evaluation.

For every n, all source words have the same VALUE-head schedule; the n-stage constant-zero and constant-one instances even have opposing terminal bits with that identical schedule. **Therefore graph labels alone cannot stand in for missing work-cell values.**

## 4. Precise integration and limitations

TMR-3/054 draft PR #164 already provides a complete, but restricted, fixed-state streaming graph-label provider and associative comb evaluator with Q=B leaf queries. TMR-5/051 merged PR #165 additionally closes that model's ordered-query sequential-source-head conversion. These chains do not supply arbitrary mutable, multiply revisited work-cell values. Here the movement problem has been made extremely easy, yet the canonical VALUE bit still represents arbitrary shared-DAG Circuit Value.

This advances/falsifies the **free C3-VALUE-PROVIDER inference** from cheap graph-position schedules to cheap work-value answers. It does not invalidate arbitrary honest reconstruction, alternative compact algebra, caching, or extra time/space. It does not construct a general, nonassociative Tree Evaluation evaluator: the circuit is a shared DAG and unfolding can duplicate gates. Both the actual adaptive TreeEval query count and the simultaneous cost of a generic provider/evaluator remain OPEN.

## 5. Four verification gates

| Gate | Verdict | Exact scope |
|---|---|---|
| DISJ sanity | PASS restricted | This proof is about source-authenticated circuit evaluation, not static assignment rank. DISJ, Horn, 2SAT, affine/Gaussian, bounded-treewidth, equality, unique-solution, selector projection, padding and compact circuits remain legitimate cheap inputs. |
| Relativization | NOT APPLICABLE WITH REASON | No P-vs-NP separation; conditional L=P consequence is not a claim to have established L!=P. No Natural Proofs/algebrization assertion is used. |
| Simultaneous DTISP | PASS for fixed canonical service, OPEN unrestricted | The same fixed machine has T=O(n^3 log n), S=O(n); there is no matched forbidden-region SAT machine or generic TreeEval improvement. |
| Configuration counting | PASS upper-bound guard | Deterministic bound T<=2^O(S+log N) is consistent with the implementation, not inverted to a work lower bound; no quantum/randomized extension. |

Historical /341 is FAIL as a complete logical UNSAT authority; /386 remains RESTRICTED. No semantic-shortcut or representation cost is asserted necessary for arbitrary algorithms.

## 6. Executable evidence and corpus

Published CPython source revision \`tmr3-canonical-cvp055-v1\`, deterministic seed 20261115, two byte-identical executions. 1,152 valid monotone sources, 1,120 general AND/OR/NOT-to-dual-rail conversions, 8 invalid sources rejected, 12,596 assertions and zero failures. Checks include exact input length, source authentication, output, intermediate values, data reads/writes/movements, source-independent head itineraries and opposite-output controls. The Python instrumented runner logs traces and is NOT a measured low-space native Turing-machine implementation. P-hardness comes from the symbolic reduction plus established CVP theorem, not finite testing.

Reviewed: governing end-to-end directive first; compatible A/B/C scientific directive; AGENTS.md, CODEX.md, current repository skill, all five peer manuscripts and handoffs, issue #3, original /054 unmerged report and /051 merged review, primary Williams and CVP sources. No retired text proof trackers read or written. Local checkout and full repository preflight unavailable due GitHub DNS; new manuscript is based on PR #164's full owner text rather than overwriting the older main-branch seed. No Lean/kernel/native TM microcode run.

Owned root manuscript is \`main3_PNP_TIME_SPACE_TRADEOFFS.tex\`, updated IN PLACE on the dependent branch. Detailed report here, source \`experiments/tmr/tmr3_canonical_cvp055.py\`, raw \`results/raw/tmr/2026-11-15_1628_TMR3_CANONICAL_CVP055_PY_RAW.json\`. Exact publication and review status require branch readback, not a claimed merge. Independent math peer review remains OPEN.

**One next lemma:** implement a source-authenticated canonical work-bit provider for an explicit NONASSOCIATIVE Tree Evaluation node family with arbitrary adaptive Q and fully charged sequential time, query-source/work access, and peak writable space on the SAME blank-start machine. The P-completeness result neither proves this impossible nor supplies its implementation.

### References

[1] R. E. Ladner (1975), *The Circuit Value Problem Is Log Space Complete for P*, SIGACT News 7(1), 18-20. https://doi.org/10.1145/990518.990519

[2] R. Greenlaw, H. J. Hoover, W. L. Ruzzo (1995), *Limits to Parallel Computation: P-Completeness Theory*, Oxford University Press, Chapter 6. https://academic.oup.com/book/41695/chapter-abstract/353938389

[3] R. R. Williams (2025), *Simulating Time With Square-Root Space*, STOC 2025, Sec. 2-3. https://doi.org/10.1145/3717823.3718225

[4] J. Cook and I. Mertz, *Tree Evaluation Is in Space O(log n log log n)*, STOC 2024. https://doi.org/10.1145/3618260.3649664
