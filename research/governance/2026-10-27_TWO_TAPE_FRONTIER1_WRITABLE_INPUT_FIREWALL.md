# TWO-TAPE-FRONTIER1 | two writable tapes vs one read-only input + one work tape
Date 2026-10-27. Additive governance handoff for existing five active LSPV research agents; no P!=NP separation and no agent-schedule change. This is a derived new model-specific theorem requiring INDEPENDENT referee review. The compact source-only selector simulator is not a full SAT decision machine.

## Input/source contract
Take our previously verified signed exact-(2P,2N) proper 3SAT 15-var/20-clause AND gadget H(a,b), with satisfying-assignment counts (00,01,10,11)=(772,272,272,0). Concatenate m disjoint gadgets, arrange 2m Alice-controlled clauses | 16m fixed clauses | 2m Bob-controlled clauses. N=Theta(m logm), fixed GAP length G=Theta(N), and UNSAT(F_m(a,b))=OR_i(a_i AND b_i). For all a, F_m(a,NOT a) is SAT; for distinct a,a', at least one crossed formula is UNSAT, so sound accepting runs must have distinct complete crossing histories at every gap cut. Uniform UTM program-prefix portfolio b=O(logN) accepted soundly may be included, with universal transitions charged.

## Two different TWO-TAPE models

2-OFF: one TWO-WAY READ-ONLY sequential input head plus one initially blank read/write work tape/head. The earlier independently refereed WRITE-TIGHT2 establishes t+s>=2, r+s>=1, d2+s>=1, and d2<1=>t>=2,r>=1, for polynomial exponent ceilings. s=visited work cells, d2=actual changes to that work tape.

2-RW: the STANDARD model of TWO INDEPENDENT READ/WRITE TAPES, each one head. Input initially on tape1; tape2 initially blank. S2 is AUXILIARY tape2 visited-cell footprint, excluding tape1, and is NOT standard total writable-space (which is at least N). D1,D2 count actual changed symbols on the corresponding tapes; Dtotal=D1+D2. Both heads may move in one charged transition.

## Derived TWO-RW lower bounds, mathematical red-team pending

A complete cut crossing configuration includes fixed control, crossing direction, and ENTIRE tape2 state, encoding O(S2+1) bits. The same soundness splice works on a writable tape1 because left and right tape1 modifications remain local to their respective parts. This gives for same-machine ceilings:
  (R1+1)(S2+1)=Omega(N/logN),
  H1(S2+1)=Omega(N^2/logN),
  T(S2+1)=Omega(N^2/logN).
For polynomial exponent ceilings: r+s2>=1, h+s2>=2, t+s2>=2.

NEW two-writable TOTAL-change theorem:
  (D1+D2+1)(S2+1)log(S2+2)=Omega(N/logN),
  dtotal+s2>=1.
Proof: for each accepted run/cut chronologically log (i) unlabelled W1 token for EACH actual TAPE1 change, (ii) W2(tape2-position,new-symbol) for EACH TAPE2 change, (iii) CROSS(direction,state,tape2-head-position). W1 positions are unnecessary for reconstructing TAPE2 contents at CROSS; W1 tokens delimit epochs with unchanged TAPE1 contents. In an epoch in which NEITHER tape changes, identical state,direction,tape2-head coordinate at same tape1 cut repeats the complete configuration and would loop. Thus <=O(S2+1) CROSS events per epoch, <=Dtotal+1 epochs, <=O((Dtotal+1)(S2+1)) events total, each O(log(S2+2)) bits. Equal event codes imply equal complete tape2 crossing histories and an unsound mixed-input acceptance. Counting 2^m distinct sound YES inputs minus b selected-program bits yields the bound. This holds for all running times, one fixed finite-alphabet deterministic two-tape machine, provided there is no other memory-bearing head and each actual change on EITHER tape is counted.

IMPORTANT FALSE TRANSFER: D2+s2>=1 alone is FALSE for standard two R/W tapes: simply ignore tape2 and use any correct one-tape SAT algorithm, with D2=0 and S2=O(1) and enough time. Tape1 overwrites are the omitted resource.

NEW independent work-tape-only time/write dichotomy which survives ALL tape1 modifications: omit W1 from the event chronicle entirely, encode only W2 and CROSS. At every cut, equal codes still imply equal whole tape2 configurations and unsound splicing. The event length is O((D2+R1+1)log(S2+2)), and choosing a minimally crossed gap cut adds only logG bits:
  m<=b+O((D2+R1+1)log(S2+2)),
  m<=b+logG+O((D2+H1/G+1)log(S2+2)).
For polynomial T and b=O(logN), exponent d2<1 IMPLIES r>=1,h>=2,t>=2, EVEN IF D1 IS UNBOUNDED. Thus the standard two-RW jointly excluded resource set includes
  t+s2<2 OR r+s2<1 OR dtotal+s2<1 OR (d2<1 AND t<2) OR (d2<1 AND r<1).
These are necessary model-specific conditions, not an existence or superpoly hardness theorem.

NEW M1 SINGLE-TAPE COROLLARY: with no tape2, the same no-change epoch proof has O(1) gap crossings per epoch, hence D1=Omega(m)=Omega(N/logN) actual tape1 symbol changes for some SAT YES input of ANY sound one-tape decider, independent of its allotted time. The standard single-tape mark+sweep promise comparator writes 2m marks and attains this bound up to constants.

## NEW INTERIOR UPPER CONSTRUCTION FOR TWO WRITABLE TAPES

On a GROUPED INPUT SERIALIZATION of the exact22 subfamily, add VALUE-INDEPENDENT group delimiters every B modules inside Alice's and Bob's controlled clause lists, leaving all clauses and their interpretations unchanged. A native fixed finite-state TWO-RW comparator changes only the active group delimiters on tape1 and uses the blank tape2 HEAD POSITION as an unmodified unary within-group index j. With single-cell head moves, the controller locates each marked group, decrements tape2 head as it scans j module records, carries one A bit in finite control, restores the index by rewinding, then compares the corresponding Bob bit. Upon finishing a group it moves both marker positions to their next group and resets the unary index. Initial group delimiters and group size are in the FIXED input serialization, not an uncharged input-dependent strategy oracle.

S2<=B+1, D1<=4 ceil(m/B), D2=0, T=O(mN), R1=O(m). For B=ceil(m^alpha), 0<alpha<1, this gives
  (s2,dtotal,t,r,d2)=(alpha,1-alpha,2,1,0)
and hence SATURATES the NEW total-change boundary dtotal+s2=1 on this EASY GROUPED PROMISE family for ALL interior exponents alpha. It DOES NOT fill the independently open 2-OFF interior, because off-line input cannot bear these markers; and this is NOT a full SAT solver.

On 2-RW with NO bound on tape1 writes, the PROMISE time-exponent envelope for fixed s2 in [0,1] is also matched:
  d2<1 => t_min=2 (one-tape mark+sweep ignoring tape2);
  d2>=1 => t_min=2-s2 (standard block-buffer multi-pass comparator using O(m) work changes).
Always add t>=1. The characterization is FOR THE PROMISE and native declared model ONLY. Efficient full SAT remains OPEN.

## Finite head-level verification
Standalone simulator TWO_TAPE_FRONTIER1/two_rw_marker_counter_audit.py: 6372 EXHAUSTIVE (m,B,a,b) promised selector cases, all m=1..5 and B=1..m; 1364 separate one-tape marker-sweep cases; 19 complement-family crossing-injectivity controls for m<=7; examples through m=256. No discrepancies. At m=256,B=16: selector length=2596, T=1,420,053, S2=17, D1=64, D2=0, input reversals=1122; Dtotal*S2=1088~4m. This is a grouped SELECTOR PROXY; finite-state parsing into complete proper CNF clause text is described mathematically, but has NOT been separately audited at literal-transition level. Full source zip and note are supplied to the user; GitHub text handoff only, unless scripts uploaded separately.

## Historical model calibrations
Hennie-Stearns (JACM 1966): a fixed arbitrary k-tape T-time machine can be simulated by TWO CONVENTIONAL WRITABLE TAPES in O(T logT), with constants depending on the source machine. Does not give this bound for 2-OFF. Maass-Schnitger-Szemeredi (STOC 1987): a particular linear-time P language on TWO writable WORK tapes requires Omega(n logn/loglogn) on one-work-tape off-line machines. Separate work-space and total-space conventions. Any 2-RW FULL SAT polynomial-time decider would imply P=NP, but none of the new restricted frontier results excludes all finite polynomials. Indexed RAM bypasses tape1 gap transport.

## Independent agent falsifiers
LSPV-1: formalize the two-RW sparse event code, sound acceptor portfolio b and same-machine native TM/UTM quantifiers.
LSPV-2: port the grouped selector algorithm to FULL exact22 clause text, finite-state parser and normal lexical blank lines; test interior B~m^alpha on true TM symbols and both tape write counters.
LSPV-3: test two-RW write budget under candidate-only UWI witness generation and confirm unavoidable verification polarity; cross-check affine-interface projections.
LSPV-4: independently prove or break ALL-time dtotal+s2>=1 with unlabelled W1 events and separate write-vs-traversal result using only W2. Model-mismatch countercontrols.
LSPV-5: search counterexamples via first-tape scratch beyond input, erased/replaced delimiters, work-head position, simultaneous tape changes, third output/input head, nonuniform descriptions; independently audit claims of sharp interior frontier. Maintain P vs NP OPEN, no schedule changes or new agents.

REFERENCES: Hennie and Stearns https://www.cs.toronto.edu/tss/files/papers/HennieStearns66.pdf ; Maass/Schnitger/Szemeredi https://doi.org/10.1145/28395.28406 ; Santhanam https://doi.org/10.1016/S0020-0190(00)00227-1 ; prior project WRITE-TIGHT2 and BINARY_WORK-SAT4.
