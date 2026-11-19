# LSPV-2: Correct-path batching with paid gate and materialization costs
Date: 2026-11-18 America/Los_Angeles. Owner: LSPV-2 SAT-CIRCUIT REDUCTION BUILDER, Route A. Status: PROVED/RESTRICTED + COMPUTATIONAL; conditional arbitrary-SAT seed; unrestricted P vs NP OPEN.

## Candidate and falsifiers
Test a source-bound, correct-polarity selector for F(z,Y)=AND_j C_j(z,Y_j) with disjoint private Y_j, including both-polarity wrong-path soundness, the entire batch circuit, all children, physical materialization and one-execution peak workspace. Falsifiers: wrong output/path accepted; hidden source or materialization; polynomial seed assumed to have a favorable exponent or low space; T5 compact circuit bypass.

## PROVED: quantifiers and resource inequality
With R=2^{|z|} rows, F is SAT iff EXISTS a row z with EVERY child SAT; F is UNSAT iff EVERY row has SOME child UNSAT. On UNSAT, bare index advice j(z) has R*ceil(log2 B) bits but is not a proof unless selected block UNSAT claims are themselves soundly verified. Correct-path advice with no wrong-path check is an uncharged answer oracle. For SAT, a row plus actual witnesses for every private block is verified against original clauses. Universal branches on NO must all be validated.

If R=n^0.195 rows, B=n^0.65 blocks/row and each explicitly stored child has L=n^0.35 bits, then RB=n^0.845 children and RBL=n^1.195 total explicit child bits. The letter n cannot at once be total encoded input size and represent all independent explicit maximum-size blocks; compressed sources need charged virtual access.

Under a correct deterministic child SAT seed with time O(L^p) and peak workspace O(L^s), a simple sequential exhaustive guest port with charged source indexing has
T=O(n^1.195 polylog n + n^(0.845+0.35p) polylog n + T_index+T_verify+T_output),
S=O(n^0.35+n^(0.35s)+S_index+S_verify+S_history+log n).
Meeting n^1.33 time and n^0.5 space via THIS port requires p<=97/70=1.385714... and s<=10/7=1.428571..., plus all omitted costs. An arbitrary hypothetical polynomial SAT seed may have p=2 or 3 and cannot be inserted into the desired fixed exponent without an additional contraction theorem. This is a falsification of an unsupported inference, NOT a lower bound on every specialist.

Batched full child buffers of size n^0.35 each admit at most n^0.15 simultaneous children under n^0.5 workspace even before guest buffers. A parent-rescan-after-every-batch scheduler would require n^0.695 batches and n^1.89 scans of a full explicitly expanded n^1.195 source. This is RESTRICTED to that scheduler. Source-indexed streaming can avoid rescans, so the exponent 1.89 is not general hardness. A fan-in-two selector only processing free child statuses is not a source-authenticated circuit for arbitrary SAT; the guest evaluation gates, source wiring, serialization and output remain charged.

A sound two-label read-only-advice verifier V(x,a) returning YES+valid witness, NO+valid refutation, or UNKNOWN, with some successful advice of at most k bits per input and cost T_V,S_V, yields deterministic enumeration within O(2^k poly(N+k) T_V) time and O(S_V+k+log N) workspace. Wrong paths cannot accept incorrect labels. An adaptive AND/OR strategy may have exponentially many universally required branches, and a selected k-bit path does not certify its full tree.

## COMPUTATIONAL: actual source-aware Boolean circuits and complete packets
Typed control source: C is a literal R x B activation-bit matrix. Bit 1 makes row-guarded pair (y_j),(-y_j) when z=r, and bit 0 disables it; each local packet is exactly L source clauses including tautological padding. This deliberately easy family has a correct O(RB) Boolean selector whose inputs are ACTUAL syntactic source flags, not guest SAT answers.

Exact bounded fan-in AND/OR/NOT gate counts (number of NOTs; depth):
- R=3,B=3,L=4: 35 gates (13 NOT; depth 5); all 512 source masks; 26,112 independent both-polarity path checks, zero wrong acceptances; 18,432 padded local clause checks.
- R=4,B=6,L=8: 95 gates (29 NOT; depth 9); 388 masks; 74,496 clause checks.
- R=4,B=8,L=16: 127 gates (37 NOT; depth 11); 388 masks; 198,656 clause checks.
The complete executed Python generator/replayer and exact raw JSON are in the dated reproducibility ZIP attached to the research conversation. Raw SHA256 58eb75849a428aec11985e588561363a82f983c71e707475ff5d06908d4580dc. Source generator SHA256 9cf06487d329c39ad8f9d10ec03be8245261e6daeb5d91124ec72c0ea0cc9c52.

Replayed already deposited original T5 H9 and H33 uniform gauge-bucket circuits with the independent interpreter and independent AC/DFS solver: H9 2,064 masks/2,060 oracle comparisons, H33 124 masks/70 comparisons; zero mismatches. Netlist SHA H9 7061d418c27844b605ef71c03fb11b9c093d31206f813d5f987b6745fe834d5c and H33 0c06aa3b9d2630d40bbdf317b4c631c863c5d0a8d91cab7d271c456b4d5aa64d. T5 host-subgraph circuits and this typed control do not cover general CNF.

## Simultaneous RAM time-space exclusions, exact scope
- Deterministic SAT, random-access machine, n^{o(1)} space: not time n^c for c<2cos(pi/7)=1.80194..., Williams 2007. Buss-Williams 2012/2015 proves this ceiling for the specified alternation-trading paradigm, not for all proof methods. https://eccc.weizmann.ac.il/eccc-reports/2007/TR07-036/index.html ; https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/
- Co-nondeterministic SAT (equiv. nondeterministic UNSAT), random-access: FLMV 2005 excludes time N^c and space N^{d(c)} for c<sqrt2 and some positive d(c). Not valid to substitute d(c)=0.5 unproved. https://doi.org/10.1145/1101821.1101822
- Nondeterministic SAT, random-access: Fortnow 2000 excludes near-linear time N^{1+o(1)} with N^{1-epsilon} workspace for fixed epsilon>0. It does NOT give an n^{1.33},n^{0.5} exclusion. https://doi.org/10.1006/jcss.1999.1671
All general SAT statements measure the actual encoded source length N and cannot transfer to a narrower promised layout or T5 deletions without a proved reduction.

## Model checks and disposition
DISJ: PASS (no static-rank hardness inference). Relativization: OPEN (no free oracle). Simultaneous DTISP: PASS for the firewall, OPEN for a general solver. Deterministic configuration counting: NOT USED AS A LOWER BOUND. No source substitution, five agents unaffected, no tracker or peer manuscript modified. Complete original end-to-end general-CNF transformation, guest bit-time, recursion/heredity and unbiased advice generation remain OPEN.

**Next load-bearing test:** source-authenticated compiler of every arbitrary-CNF child into a genuinely length-bounded, disjoint-private block with a recursively closed same-machine full-cost ledger and a both-polarity rejection proof. P versus NP OPEN.
