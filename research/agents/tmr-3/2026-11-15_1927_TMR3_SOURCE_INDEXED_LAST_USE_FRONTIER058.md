# TMR-3/058: A fully charged source-indexed last-use frontier evaluator

**November 15, 2026, 19:27 PST. Track B, C3-PUBLIC-SCHEDULE-FRONTIER.**
**PROVED/EXACT restricted model, independent mathematical review OPEN.** The executable evidence is COMPUTATIONAL. No general Williams space improvement or P-versus-NP proof.

## Candidate and falsifiers
The target is the authentic source -> published/verified source-only schedule -> true block/cell values -> chronological nonassociative frontier evaluator -> correct accept/reject bit. The candidate states that future-live access width w, plus a fully charged source-only schedule G, permits a complete simulator with O(wb) retained block values rather than retaining the entire computation history.

F1: a discarded work block reappears later; test exact future visits. F2: a purported public schedule depends on unobserved intermediate work bits; the theorem explicitly excludes this case. F3: generator calls or input-head restoration are counted for one machine but omitted from the claimed time bound; every call is charged. F4: a supposed lower bound uses the costs of our particular evaluator to exclude legal two-register shortcuts; no such exclusion is asserted.

## Theorem: genuine source-indexed block-respecting simulator
For one fixed deterministic finite-alphabet p-work-tape machine starting with blank work tapes, let an authenticated input x (length N) have B genuine time blocks of b transitions. Assume one original-source-only uniform G(x,h,j), using at most g writable bits and tau paid steps including local input-head seeks, returns the true active b-cell block on tape h during block j, for every source x in the declared domain. The input parser costs A(N) time and uses s_A(N) peak writable bits. This is a constructive hypothesis about the actual execution, not a guessed graph provided for free.

Let F_j be the set of (tape,block) addresses appearing among both blocks 1..j and blocks j+1..B, and w=max_j |F_j|. One uniform total sequential simulator for that family has simultaneous resources
\[
S=O(s_A(N)+(w+p)(b+\log(B+2))+g+\log(N+B+2)),
\]
\[
T=O(A(N)+pB^2(\tau+1)+Bp(w+p)(b+\log(B+2))+Bb).
\]
It reads and validates the original source, obtains all active block labels from G, loads actual previously stored content or blanks, executes all b genuine local transitions per block, and scans later G labels before keeping or discarding each touched block. By induction every retained cell and control state equals the genuine blank-start computation. After each block only the previously seen, future-needed blocks remain, at most w; at most p transient live block buffers are additional. The time expression pays at most pB² full source-generator calls, all sequential table scans, authentic transitions, input-head restoration, exact output and validation. The proof does not assume associative node functions.

This is an elementary last-use/pebbling construction given a source-indexable schedule. It is a restricted chronological DAG evaluator, **not** a new universal Cook-Mertz Tree Evaluation algorithm. For arbitrary Williams computations, G can depend on uncomputed work values, and w need not be small. The theorem cannot be used to claim arbitrary cube-root space or a DTISP forbidden region.

## Concrete blank-start nonlinear source-to-output construction
The total canonical grammar is unary 1^B, separator 0, and B payload bits x. Malformed inputs are rejected, N=2B+1. One fixed finite-control work-tape program reads x_j and, if x_j=1, performs a true read-only work-head bounce at cells j-1,j-2,j-1. It then genuinely accesses cells j-1,j-2,j-1,j by unit/zero moves, captures old a at j-2 and p at j-1, and writes c_j=(p AND a) XOR x_j at j; the initial missing cells are blank. All head movements are locally legal. In particular c_1=x_1 and c_2=x_2, so the j=3 AND depends on two independently variable previously written symbols. Thus the operation is not affine even though the schedule is reconstructible from source bits.

The true trace has H=4B+3 popcount(x) work visits and B+2 distinct accessed work cells. Its source-only indexed generator takes O(N) paid bit time and O(log N) workspace per query. Exact last-use frontier width is at most 2 for every x. The virtual table simulator issues at most H(H+1)/2 source-indexed generator calls, and completes both labels with O(NH²)=O(N³) time and O(log N) writable space, charging all lookahead accesses, old-value readbacks, counters, original-source rescans and output. The original physical work tape visits Theta(B) cells. A direct two-register streaming algorithm is cheaper and remains allowed. This particular control is a **cell-time** trace; it is not claimed to instantiate the b≥log t Williams conversion.

## Four mandatory gates
| Gate | Verdict and reason |
|---|---|
| DISJ sanity | PASS restricted: no static cut-rank to general-circuit or SAT-machine lower bound |
| Relativization | NOT APPLICABLE WITH REASON: no separation; hypothetical nonrelativizing NP step remains OPEN |
| Simultaneous DTISP | PASS for this same simulator's time and peak space; strict FLMV / all-SAT transfer OPEN |
| Configuration count | PASS upper-bound consistency only, T≤2^{O(S+log N)} for total deterministic machines |

Algebrization and Natural Proofs are not used in this restricted construction. All compact, affine, Horn, DISJ, 2-SAT, treewidth, unique-solution, selector, padding, caching and recomputation paths remain admissible. Historical /341 FAIL as full UNSAT authority, /386 RESTRICTED.

## Exact computational evidence and provenance
Standard-library CPython 3.13.5 revision tmr3-source-frontier058-py-v2, no random seed; two byte-identical runs. Exhaustive B=1..7 plus 19 deterministic B=8 controls: **273 authentic source words, 9,286 paid work visits, 7,050 true predecessor edges, 45,289 assertions, zero failures**. Each original work-head step, schedule query, cache contents and exact past/future intersection were compared on all tested sources; malformed inputs and a missing-old-cell negative control included. The Python verifier uses full traces as a reference model and is not a measured logspace implementation.

Current original TMR-3/057 report, stacked drafts #164/#169/#174/#180, current five peer handoffs/manuscript sections, source protocol and Williams STOC 2025 Sections 2-3 were reviewed. Root main3 on main is an older seed, so the current draft branch manuscript was used as the conflict-safe baseline. Local repository checkout, full preflight, LaTeX build, native finite-transition table compilation, and independent mathematical review not executed.

**One next lemma:** C3-ADAPTIVE-GRAPH-INDEXER. For the genuine general Williams block-respecting conversion, construct or falsify a fully charged canonical block-identifier provider even where head movements depend on previously written work bits. Bound its query volume, sequential cost and peak space simultaneously before composing with a nonassociative evaluator. General P versus NP remains OPEN.

References:
[1] R. Ryan Williams, Simulating Time With Square-Root Space, STOC 2025, https://arxiv.org/html/2502.17779 .
[2] J. Cook and I. Mertz, Tree Evaluation Is in Space O(log n log log n), STOC 2024, SIAM J. Comput. 2025, https://doi.org/10.1137/24M1690126 .
