# TMR-3/064: one public authentic movement word can have a \quadratic live-block frontier

November 16, 2026, 05:04 PST. TMR-3 / PNP Time-Space Tradeoffs, Track B.
**PROVED/EXACT, restricted explicit machine and arithmetic, external independent mathematical review OPEN.** Finite tests COMPUTATIONAL. P versus NP OPEN.

## Candidate, quantifiers, falsifiers, and integration point

The named dependency is **C3-CANDIDATE-COVERAGE-UNDER-A-PINNED-CONVERTER**, specifically the unproved inference that a small source-indexable candidate set in TMR-3/063 should also give a small authentic future-live frontier. For EVERY sufficiently large even integer b and EVERY payload y of length b^3, construct ONE fixed deterministic blank-start locally headed machine M, with four writable tapes and one read-only original-source head, whose *entire valid-source run* is b-block-respecting. Its sole authentic movement candidate has a source-independent logspace indexing procedure, while its future-live work-block frontier is exactly b^2+3. This is an identity-normalization falsifier of automatic low width, not a theorem about a pinned folded-copy HPV compiler or an arbitrary representation.

Precommitted falsifiers: F1 a head crosses a physical b-block between time-block boundaries; F2 source-length authentication, clock writes, return reads, or input/head movements are free; F3 the maximum future-live count fails to measure distinct (tape ID, block ID) identities or is inflated by repeated visits to a single block; F4 a fixed architecture's cache width is promoted to an unavoidable workspace lower bound despite source replay, parity streaming, semantic compression, or another legal compiler.

The full selected pipeline remains: authentic input -> paid parser -> fixed block-respecting machine -> actual unique movement word and block graph -> charged candidate provider -> /063 width prefilter and chronological canonical evaluator -> exact Boolean output. This run falsifies the automatic-small-frontier arrow *before* the /063 verifier is called. Its conditional verifier theorem remains intact.

## Authentic source grammar and complete program

An authentic source is `x=1^(b-1) 0 y`, with even b>=2 and y in {0,1}^{b^3}; its total bit length is N=b+b^3. The fixed program rejects malformed prefixes, odd b, early end of payload and trailing input before accepting. A read-only input head discovers b by advancing over the actual prefix. During exactly b bootstrap transitions the three fresh clock heads move from cell zero to cell b-1, where right endpoint symbols are written. Left endpoints and all non-endpoint clock cells are also physically initialized. The first b-1 prefix bits are ones; the b-th is the delimiter zero. A one-bit finite-control parity of prefix length rejects odd b. No b-dependent transition table or preloaded checkpoint is used.

Each clock is a finite-control bouncing head on the interval [0,b-1]. An enabled head moves one step unless facing outward at an endpoint, where it stays, reverses and emits a pulse. One half-sweep requires exactly b enabled transitions. Clock 1 is enabled every outbound/reverse transition; clock 2 only on clock-1 pulses and clock 3 only on clock-2 pulses. A clock-3 pulse therefore marks precisely b^3 paid transitions. Even b ensures the first two heads are at their right endpoints after the first cubic epoch.

The PATH tape is initially blank. During exactly b^3 outbound transitions M reads the actual next payload bit y_k, writes it into PATH cell k and advances PATH right by one cell. At every b-th step PATH crosses to the next physical block, and never crosses earlier. The read-only input head advances one cell per bit; its first post-payload read verifies the endmarker and rejects extra bytes.

During b turnaround transitions clock 1 moves from its right endpoint to the left while clocks 2/3 stay fixed; PATH stays at cell b^3 on the first b-1 transitions and crosses left to cell b^3-1 on the last. During the next b^3 transitions the three clocks resume; PATH reads every genuinely written cell in reverse order, maintains a one-bit XOR accumulator in finite control, moves left after each read except the last, and stops at cell zero on the second cubic pulse. Finally M spends b paid stationary terminal transitions and emits its actual XOR output. The source grammar and physical controller are fixed, uniform and total. For all authentic sources,
\[
 M(x)=\bigoplus_{k=0}^{b^3-1} y_k.
\]
Malformed inputs are rejected, not classified UNSAT by a missing graph.

## Exact block schedule and frontier theorem

Put m=b^2 and let time blocks j be zero-indexed. Total duration is
\[
 t=b+b^3+b+b^3+b=2b^3+3b,\q\quad B=t/b=2m+3.
\]
The PATH active-block index is:
\[
 z(j)=\begin{cases}
 0,&j=0,\\
 j-1,&1\le j\le m,\\
 m,&j=m+1,\\
 2m+1-j,&m+2\le j\le 2m+1,\\
 0,&j=2m+2.
 \end{cases}
\]
Each of the three clock-tape heads remains in its physical block zero for every time block. The exact movement word is therefore **one public candidate** g_b, independent of y. The candidate index (tape, stage)->block is calculable with O(log N) writable bits from authenticated b and O(polylog N) binary arithmetic. With a locally moving read-only input head, rescan/restore makes per-query time at most O(N polylog N), fully charged. No full B-entry table is stored.

For a candidate c define the TMR-3/063 cut frontier F_j(c) to contain each distinct (work-tape ID, block ID) active by j and active again after j. At the cut just after outbound stage j=m, the PATH has visited m distinct blocks 0,...,m-1, and reverse traversal will revisit every one. The three distinct CLOCK tape/block identities remain live too. Therefore
\[
 |F_m(g_b)|=m+3.
\]
No cut contains more than m PATH blocks that are both past and future active: block m is only a turnaround visit, never revisited. Hence the exact maximum is
\[
 \boxed{K=1,\quad W=w(g_b)=b^2+3
       =\Theta(B)=\Theta(t^{2/3}).}
\]
At all even b>=12, 2^b>=2b^3+3b (check b=12, then exponential-to-cubic ratio increases), so b>=ceil(log_2 t) and b=\Theta(t^{1/3}). This holds in precisely the admissible block-width range of the restricted /063 interface. The proof uses *active physical tape blocks*, not a static cut rank or a forced set of semantic dependencies.

In particular the materialized-block dictionary of /063 would have a worst-case budget (W+p)b=\Theta(b^3)=\Theta(t) on this family, even though K=1 and the candidate provider is inexpensive. Repeated original-source bits really are written to b^3 visited PATH cells. No claim is made that all correct deciders must retain them.

## Full same-execution time/space/query ledger

The original physical machine has p=4 work tapes; its three clocks use 3b visited cells and PATH visits b^3+1, with fixed finite control. Its actual simultaneous time and space are
\[
 T_M=2b^3+3b=\Theta(N),\quad
 S_M=b^3+1+3b=\Theta(N)
\]
where read-only input is not counted as writable work tape. Input source bit acquisition and every cell move are included in T_M. The step partitions (bootstrap, outbound, turnaround, return, terminal) are disjoint. There are m outward, one turnaround, and m-1 return physical cross-block moves, 2m total.

For one candidate G's indices need O(log N) work and at most O(N polylog N) source-head time per query; screening /063 has Q_G=O(pB^3) calls, which is polynomial but its forced cache width bound becomes linear in t. Graph-edge queries may be synthesized from the same stage-index service with charged scans. Arbitrary checkpoint-value requests may require source replay. The original M's physical cells are never erased by describing a virtual sketch. No polynomial-time lower bound is inferred.

A direct independent authentic-source parser streaming XOR of y achieves T=O(N polylog N), S_peak=O(log N) on one different physical execution and rejects malformed words. This valid compact alternative proves the high physical frontier is **not** representation-independent hardness and cannot establish SAT lower bounds.

## Finite executable evidence, exact provenance

Standard-library CPython 3.13.5 executable `experiments/tmr/tmr3_boomerang_frontier064.py`, revision `tmr3-boomerang-frontier064-v1`, deterministic seed 202611160504. Two executions produced byte-identical raw JSON: 56 valid sources (eight cases at each even b=2,4,6,8,10,12,14), 30 malformed controls, 605,350 instrumented checks, zero failures. The tested local transitions include 3 bounded clock heads, actual source reads/writes, outward/return PATH positions, each time-block boundary and full past/future block-set frontier. The finite small-b diagnostic cases below b=12 are not claimed to satisfy b>=log t. Source SHA256 7baa92171b5a7efb923b01abd3bd828ecb6e475d371f2928d8b3d67f3e51b1cb; raw SHA256 6541322fc38c60d787a1c8269f0de6471d3ff3db947600617efce65b4ab94a14. Python microtrace is for this particular controller, not a native general multi-tape compiler, a literal HPV folded-copy conversion, or a Cook--Mertz implementation. External mathematical review OPEN.

Raw path `results/raw/tmr/2026-11-16_0504_TMR3_BOOMERANG_FRONTIER064_PY_RAW.json`. GitHub publication/readback and LaTeX build statuses are recorded separately, not inferred from test success. A local full-repository checkout is unavailable because git ls-remote could not resolve github.com; project preflight was not run.

## Four gates and guardrails

| Gate | Verdict |
|---|---|
| DISJ sanity | PASS restricted. Only a physical-width property is asserted; DISJ, affine parity, Horn, 2-SAT, treewidth, equality, autarky, compact programs and shared-cache shortcuts are legal. |
| Relativization | NOT APPLICABLE WITH REASON to a separation: none is claimed. No nonrelativizing NP premise, algebrization or Natural Proofs result is asserted. |
| Simultaneous DTISP | PASS for the exact original M and separately declared streaming direct algorithm; generic low-width /063 premise and FLMV forbidden pair remain OPEN. |
| Deterministic configuration counting | PASS as an upper-bound consistency control only; t=\Theta(N), s=\Theta(N), no randomized/quantum transfer. |

Local-basis changes, field characteristic, charged randomized isolation, uniqueness/selector projection, exact counting semantics, circuit-to-CNF wire blowup, majority ties, quantum error models, and product/padding/auxiliary operations do not enter this physical theorem. They remain explicit guards for any downstream SAT/circuit theorem. Historical /341 stays FAIL as full UNSAT authority; /386 RESTRICTED.

## One next load-bearing dependency

**C3-PINNED-CONVERTER-FRONTIER-REPAIR:** choose and implement one specific general HPV/Williams block-respecting converter, and either prove a nontrivial bound on its actual authentic frontiers together with polynomial source-derived candidate coverage, or replace physical-block retention with a sound charged value-compression/reconstruction interface supporting Q adaptive nonassociative Tree Evaluation queries. Count conversion, provider, Q, replay, output, time and peak space for the same machine. The identity construction here falsifies only an automatic small-W conclusion from block respect and K=1.

Sources: [1] R. R. Williams, *Simulating Time With Square-Root Space*, arXiv:2502.17779v1, Sec. 3.2, https://arxiv.org/html/2502.17779v1. [2] Cook and Mertz, *Tree Evaluation Is in Space O(log n log log n)*, STOC 2024, DOI:10.1145/3618260.3649664. Prior original project /063 is on unmerged draft PR #210. P versus NP remains OPEN.
