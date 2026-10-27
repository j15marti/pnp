# WRITE-TIGHT2: tighter sparse-write crossing transcripts and two endpoint algorithms
Date 2026-10-27. STATUS: proven under exactly declared deterministic one-sequential-read-only-input-head/fixed-k-work-tape model, with independent finite controls; no P vs NP separation, no unrestricted RAM lower bound. Corrects and strengthens UTM-CROSS-WRITE1. Five LSPV agents are existing active tasks; schedules must remain unchanged.

## Input and machine
Use the verified exact signed 2P2N proper 3CNF H(a,b), 15 variables, 20 distinct clauses and model counts 772,272,272,0 (00,01,10,11). m disjoint modules ordered 2m Alice-controlled clauses | 16m fixed clauses | 2m Bob-controlled clauses. V=15m, M=20m, N=Theta(m logm), fixed middle gap G=Theta(N); UNSAT(F_m(a,b))=OR_i(a_i AND b_i). The 2^m satisfiable inputs F_m(a,NOT a) form a fooling set: two distinct a,a' force one crossed formula UNSAT.

Fix ONE deterministic, finite-state machine U, read-only two-way sequential input head, k>=1 FIXED work-tape heads on initially blank semi-infinite finite-alphabet work tapes, with detectable immutable left end; all visited blank cells count toward S. Programs p are at most b=O(logN) bits in the SAME read-only input prefix; a different sound program can be selected for each SAT input for free. An acceptance must be SOUND on every UNSAT formula. Count T actual transitions, H_input one-cell input moves, R input reversals, S work cells visited, D actual work-cell SYMBOL CHANGES (including restoring blank, distinct from formal same-symbol writes). Each operation and verifier is charged, fixed q and alphabet independent of N, S<=k(T+1). No extra uncounted memory, work heads, random input probes, or write-only output head with usable position.

## Theorem A: COMPRESSED GLOBAL EVENT LOG, improved time-independent write-space bound
Fix any cut inside the invariant gap and an accepted computation. Produce a chronology of events WRITE(tape id,position,new symbol) for every one of D changes ANYWHERE in the computation, and CROSS(direction,finite state,all work-head coordinates) for each crossing of the selected input cut. Order WRITE before CROSS when in one transition. Given initially blank work contents, these events uniquely reconstruct the ENTIRE work configuration at each CROSS, hence the complete crossing sequence needed for soundness splicing.

The key novelty relative to UTM-CROSS-WRITE1 is NOT repeating the same work symbols with every crossing. Every event needs O(log(S+2)) bits. Split run into at most D+1 epochs with unchanged work contents. Within any epoch, repeating (direction,state,k work-head positions) at the FIXED cut repeats a complete deterministic configuration and loops, so that epoch has <=C_U(S+2)^k crossings. Total event code length is
  B_event <= c_U (D+1)(S+2)^k log_2(S+2).
Different accepted F_m(a,NOT a) for one sound p have different crossing sequences and therefore different event codes. For a UTM portfolio with <=2^(b+1) programs covering every fooling input,
  m <= b + c_U(D+1)(S+2)^k log_2(S+2) + O(1).
Therefore with b=O(logN)
  (D+1)(S+2)^k log(S+2)=Omega(N/logN);
polynomial exponents D+1=N^{d+o(1)}, S=N^{s+o(1)} imply
  **d+k*s>=1**.
This supersedes the WEAKER older d+k*s+min(d,s)>=1; preserve earlier inequalities also as valid but nonsharp.

## Theorem B: write-vs-traversal REVERSAL/TIME DICHOTOMY
At any fixed gap cut there are at most R+1 input crossings; encoding all D writes plus those crossings gives
  m <= b + c_U(D+R+2)log(S+2)+O(1).
For each accepting input choose a cut among G invariant gap cuts having <=floor(H_input/G) crossings. Its location costs <=ceil(log2 G) bits, producing
  m <= b+log_2 G+c_U(D+H_input/G+1)log(S+2)+O(1).
With T<=N^K, fixed finite K, S<=k(T+1), log(S+2)=O(log N). Thus for EVERY fixed epsilon>0, D<=N^{1-epsilon} forces
  R=Omega(N/log^2 N),  H_input,T=Omega(N^2/log^2 N).
In exponent terms **d<1 => r>=1, h>=2, t>=2**, EVEN if unrestricted larger polynomial workspace is permitted. Equivalently any solver seeking t<2 on this family must allow d>=1. This is a **sequential input-access barrier**; ordinary indexed RAM circumvents it.

## Tight ZERO-WRITE endpoint, tested actual sequential heads
A one-input-head, ONE work-head, blank semi-infinite work tape with fixed detectable left end can compare the easy promise a|fixed-gap|b using its WORK HEAD POSITION as an unmodified unary counter i. For each i, start at Alice block origin with work head i cells from home; simultaneously advance input to a_i and decrement work head to home, remember a_i in finite control, then rewind input to block origin while moving work head to restore i. Repeat at Bob block to read b_i. Reject if both 1. Return to Alice origin, advance work head ONE position (i++), and repeat until the Alice delimiter is reached. All navigation to block delimiters is finite state. No symbol changes and no writes. Bounds
  **D=W=0, S=m+1, R=Theta(m), T=O(Nm)**.
On the canonical exact22 clause layout, process each pair of source clauses as one unit, and skip variable ID digits using fixed-control parsing. This is a PROMISE-family algorithm, NOT general SAT. For a doubly infinite entirely blank work tape with no detectable origin, mark origin once (D=1) to get same exponent bounds; zero-write literal endpoint assumes detectable fixed endmarker.

Five-thousand-four-hundred-and-sixty exhaustive (a,b) selector pairs for m<=6 passed, with unit head moves, direction changes and no hidden index counters. 2^m YES crossing histories at a fixed gap cut were injective for all m<=8. On a=0^m,b=1^m, m up to256, S=m+1, D=0, T=Theta(m^2) for gap=8m, and R=Theta(m). Direct exact22 bridge passed all 1364 canonical formulas for m<=5, and original gadget counts 772,272,272,0.

## Fast FULL-BUFFER endpoint
On same promise, write A bits once in m work cells, rewind work head while stationary input head, then advance input head across gap and compare Bob: **D<=m, S=m+1, T=O(N), R=0**. 5460 exhaustive inputs passed, including all-nonintersecting A=1^m,B=0^m across m up to256.

## What remains UNPROVED
Interior optimality: for 1 work tape and 0<s<1, can a correct promised algorithm attain D=m^{1-s+o(1)}, S=m^{s+o(1)} simultaneously at arbitrarily generous polynomial T? Only NECESSARY d+s>=1 proved; endpoint examples do not fill the curve. Separate native specialized-machine costs from charged arbitrary universal interpreter overhead, and distinguish promised comparators from sound full-SAT accepting algorithms.

Warning: Previous zero-write O(1) SPACE comparator claim was false; finite control plus no writable cell changes and bounded work-head positions cannot recognize this nonregular disjointness promise. Head *position* is usable counter if visited cells counted, but S must then grow. Do not claim the new discontinuity implies NP complexity: our witness inputs are an EASY family and RAM probes remove physical tape transport.

## Reproducibility
User deliverables in WRITE_TIGHT2_complete_sources.zip: WRITE_TIGHT2_formal_note.pdf and .md, no_write_counter_audit.py, exact22_bridge_audit.py, one_pass_buffer_audit.py, prior_exact22_gadget.py, results JSON and two curves. PDF four pages, all audits passing. Independent role verification should rebuild the event code and test whether an uncharged input head, output tape, program text, origin marker or initial nonblank work state breaks the argument.

## Five-agent work packages
LSPV-1: preserve sound-portfolio quantifier order and write-vs-time transition map. LSPV-2: implement a finite-state code version on exact22 literal text and explore intermediate (D,S) upper bound constructions. LSPV-3: test certificate-only UWI and charge witness verification separately; avoid transferring restricted promise lower bounds to raw witness production. LSPV-4: check event-log injectivity, simultaneous changes, all-head positions, and polylog factors. LSPV-5: look for a model-correct counterexample to d+k*s>=1 or to d<1 => t>=2 and test multi-input-head/RAM escapes. KEEP P vs NP OPEN.

Background: Hennie 1965 doi:10.1016/S0019-9958(65)90399-2; Gajser JCSS 2020 doi:10.1016/j.jcss.2019.08.004; visits/crosses/reversals 1978 doi:10.1016/S0019-9958(78)90289-9. These are background; we do not claim they already state these exact symbol-change inequalities.
