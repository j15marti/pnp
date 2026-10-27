# TWOTAPE-JOINT1: native joint lower bounds for TWO FULLY WRITABLE Turing-machine tapes
Date 2026-10-27. STATUS: New proof derivation, independently cross-checked by explicit 2-tape simulation, formal external referee pending. P vs NP OPEN. Additive handoff for five existing LSPV research agents; preserve schedules and roles.

## IMPORTANT correction from earlier WRITE-TIGHT2

WRITE-TIGHT2 had ONE READ-ONLY input tape and k writable work tapes, so its D counted exclusively the work-tape changes. The present physical model has EXACTLY TWO independently movable READ/WRITE tape heads, finite fixed state/alphabet, input formula initially on tape 1, tape 2 initially all blank; each tape has one sequential head. Thus tape 1 may change its symbols.

A FALSE extension is to claim (D2+1)(S2+1) log(S2+2)=Omega(N/logN) where only tape-2 symbol changes D2 count. A finite-control promise comparator with a writable input tape MARKS each Alice and Bob symbol as processed, makes D1=2m,D2=0,S2=1, halts in O(Nm) steps and crosses a fixed middle cut 2m times with only TWO distinct crossing labels. The earlier no-change-epoch argument fails because tape 1's contents change. Do not reuse it.

## Exact22 source and correct complete crossing

Our independently checked 15-variable/20 proper clause exact 2P2N gadget H(a,b) has SAT model counts 772,272,272,0 and UNSAT(H(a,b))=a AND b. m disjoint copies, ordered 2m A-variable clauses | 16m fixed clauses | 2m B-variable clauses, give F_m(a,b) with N=Theta(m logm), invariant central tape-1 region G=Theta(N), and UNSAT=OR_i(a_i AND b_i). There are 2^m satisfiable fooling inputs F_m(a,NOT a). For distinct a,a', at least one crossed combination is UNSAT.

At any fixed tape-1 middle cut, for ONE globally sound accepting algorithm/program, the FULL crossing sequence includes the finite control, direction, all tape-2 contents and head2 position. It must be injective among accepted fooling inputs, even when tape1 may be WRITTEN: left and right tape1 work evolution splices locally and the shared tape2 state agrees at cut crossings. Short-program UTM portfolios with b<=O(logN) prefix bits can be grouped by p; no program may accept any UNSAT input. RAW witness printers without verified soundness do NOT qualify.

## Native two-writable-tape necessary finite inequalities

Let T be actual transitions, H1,H2 head movements, R1 reversals of head1, S2 ALL tape2 cells visited (including blank), D1,D2 actual changed symbols on tape1/2 (formal same-value writes excluded), D=D1+D2. For uniform worst-case ceilings on accepted fooling inputs and fixed machine q, there exists fixed constant cU so:

(1) m <= b + ceil(log2 G) + cU (S2+2)(1+H1/G) [snapshot low-crossing cut].
(2) m <= b + cU (S2+2)(R1+1) [fixed cut, direction reversals].
(3) m <= b + cU (D1+D2+1)(S2+2)log2(S2+2) [new BOTH-TAPES change-epoch log].

Proof for (3): one chronicle at fixed cut records W1 marker for each tape1 actual symbol change WITHOUT tape1 address, W2(tape2 position, new symbol) for every tape2 actual change, and CROSS(state,dir, tape2 head location) at cut. Replay W2 updates to reconstruct tape2 contents at each CROSS. W1 markers split the run into <=D1+D2+1 epochs with BOTH TAPE CONTENTS unchanged. Within each epoch repeating the same state, crossing direction, and head2 position at a fixed cut repeats FULL machine configuration and would loop. Therefore <=O(S2+2) crossings per epoch; each event is O(log S2) bits. Equal event codes force equal full crossing transcripts, hence one wrong UNSAT mixed acceptance by splice.

Exponent boundaries for T=N^{t+o(1)},S2=N^{s2+o(1)},R1+1=N^{r+o(1)},D+1=N^{d+o(1)}:
    t+s2>=2,    r+s2>=1,    d+s2>=1.
The coordinate S1 need not appear: tape1 writable cells lie spatially on ONE side of the cut. It is incorrect to count their contents as shared input-boundary storage. S2 is the globally accessible channel.

## New movement-aware "f" joint inequality

At a per-run cut with C<=H1/G crossings, record W1, W2 and CROSS events. Encode tape2 head position at each event by a self-delimiting SIGNED DELTA from previous event, rather than absolute location. Their total absolute displacement <=H2. Let L=D1+D2+1+ceil(H1/G). By Jensen and a standard integer code, the entire ordered event code has <=cU*L*[1+log2(2+H2/L)] bits. Each code reconstructs tape2 full crossing history; include p and cut index.

(4) m <= b + ceil(log2 G) + cU*L*[1+log2(2+H2/L)],   L=D+1+ceil(H1/G).

With Hj<=T, G=Theta(N), m=Theta(N/logN), a concrete fully joint necessary relation is:
    (D+1+T/N)*[1+log2(2+T/(D+1+T/N))] = Omega(N/logN).
No unproved f-function is inserted; the factor follows from encoding actual sequential head displacement.

Corollaries: for every fixed epsilon>0, a deterministic machine using D=O(N^{1-epsilon}) actual changes and polynomial T must use T,H1=Omega(N^2/log^2N) and R1=Omega(N/log^2N). Equivalently d<1 => t>=2 and r>=1. If T=O(N), then D=Omega(m/loglogN) with H2<=T; if additionally H2=O(m), D=Omega(m), matched by buffering on this easy promise.

## Three native algorithmic controls, ALL inputs on the promise

A) Tape1 marker-only, no tape2 writes or moves: D1<=2m,D2=0,S2=1,H2=0,T=O(Nm). Shows D2-only theorem false.
B) Tape2 full buffer: D1=0,D2<=m,S2=m+1,H2=O(m),T=O(N),R1=0. Saturates linear-time+linear-second-head-travel write lower bound.
C) Tape1 in-place marking + tape2 B-cell batch buffer: D1<=2m,D2<=2m+1,S2=B+1,T=O(N ceil(m/B)+B). Thus s2=alpha,t=2-alpha,d=1 endpoints/slices attainable on promised family. The simulator takes capacity B as explicit input; charged finite-control construction of arbitrary B(N) has a separate small arithmetic/setup obligation, so do not overclaim full transition-level uniformity.

A previous zero-write unary head-position counter uses D1=D2=0,S2=m,T=O(Nm); exact origin-marker assumptions are in WRITE-TIGHT2.

## Finite independent replay controls PASSED

In user research deliverable TWOTAPE_JOINT1_complete_sources.zip and 4-page TWOTAPE_JOINT1_report.pdf: 10,920 exhaustive mark/buffer runs, 16,356 batched comparisons, 1,364 exact22 CNF selector cases tested by both basic two-tape algorithms (2,728 cases), 252 selected-cut WRITE+CROSS event replay checks, all-invariant-gap-cut crossing-history injectivity checks, 14 simultaneous BOTH-TAPES-change and head-crossing controls. Replayed complete tape2 contents at each cut crossing and checked tape2 event delta travel <= actual H2. Explicit m=6 hostile machine: D1=12,D2=0,S2=1,T=720, 12 crossings of middle cut but just 2 distinct labels.

These finite tests are falsifiers and construction validations; asymptotic validity relies on the proof, still independent formal referee pending.

## STRICT limitations and agent tasks
- Neither this result nor its predecessors proves ANY RAM-native superpolynomial SAT lower bound. P != NP OPEN. An extra independently movable input head, uncharged output tape/head, address-mode memory access, growing state/alphabet, uncharged preloaded tape2 advice, or native source oracle breaks assumptions.
- One globally sound full-SAT decider or globally sound short UTM portfolio is required. Promise-specific comparator is used only as saturation/counterexample, NOT presented as full SAT decider.
- LSPV-1: audit same-machine universal common-input p,c event code and all exponents; check no shortcut to arbitrary native RAM.
- LSPV-2: reconstruct explicit two-writable 2P2N sign switch, check false D2-only claim, independently implement finite-control B initialization and more efficient batching.
- LSPV-3: compare proof/certificate boundary transport with tape1 mutable, beware free witness verification and program selection.
- LSPV-4: attack signed-delta Jensen encoding, event ordering, no-change epoch counting for BOTH writable tapes, constants and exact b.
- LSPV-5: falsify splicing under tape1 self-modification, advise second input head/output head counterexample, and challenge T=O(N),H2=O(m)=>D=Omega(m).
- Keep the other active roles and schedules unchanged. Do not assert that the frontier d+s2=1 is tight in the interior; it remains OPEN even with generous polynomial time.

Background: Hennie and Stearns, JACM 1966 https://doi.org/10.1145/321356.321362 ; Vitanyi, JCSS 1984 https://doi.org/10.1016/0022-0000(84)90001-1 ; Jonathan Katz lecture crossing sequences https://www.cs.umd.edu/~jkatz/complexity/f05/lower_bounds.pdf . Vitanyi's work confirms recording the other storage tape in crossing states; it does not establish the present symbolic write-count refinements, which are new project derivations pending referee.
