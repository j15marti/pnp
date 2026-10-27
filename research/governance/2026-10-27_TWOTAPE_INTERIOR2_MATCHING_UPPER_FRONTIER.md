# TWOTAPE-INTERIOR2: Constructive saturation of the two-writable-tape write-space interior (2026-10-27)

**Status:** all-size CONSTRUCTIVE upper-bound proofs on one calibrated framed exact signed 2P2N proper-3CNF DISJOINTNESS promise, exhaustively/independently finite-tested. The **matching lower-bound interpretation is CONDITIONAL** on the earlier TWOTAPE-JOINT1 crossing/event theorem, independent mathematical referee STILL PENDING. **P vs NP OPEN**. This handoff adds to current LSPV roles; do not activate or reschedule paused agents.

## New theorem: finite-control two fully writable tapes, tape 2 never written

For m variable-disjoint copies of the source W1 two-bit exact22 switch H(a_i,b_i), prepend B<=m fixed satisfiable H(0,0) calibration modules and frame A modules | fixed gap | B modules. The chosen framing punctuation is public and independent of control bits; V=15(m+B), M=20(m+B), input bit length N=Theta(m log m) and UNSAT iff OR_i(a_i AND b_i). The source W1 has model counts (00,01,10,11)=(772,272,272,0). All input formulas are proper, clause-distinct, exact 2 positive/2 negative occurrences per variable.

A SINGLE uniform, finite-control two-writable-tape TM with a detectable LEFT END on tape2 achieves for all m,B and all 2^(2m) control pairs:
  S2 <= B+1,  D2 = 0,  D1 <= 2 floor(m/B),
  T=O(N*m),   R1=O(m).
It keeps tape2 entirely BLANK, representing j in {1,...,B} by head2's physical position. At each j it navigates Alice and Bob's actual signed literal text by j source module delimiters; then scans B fixed satisfiable calibration modules to test whether j=B, restoring j by reverse movement. Upon completing one B-sized block it changes ONE Alice separator and ONE Bob separator on tape1 from '/' to '#'. NO per-bit write is needed. Every head movement, source read, transition call and actual tape1 change is charged. The only program-side case splits test the two scanned symbols plus fixed finite control; Python m/B are INPUT GENERATOR/AUDIT parameters and not consulted by run. Parsing the framed CNF module delimiters is part of this DECLARED promise input grammar, NOT native unframed DIMACS. It is a global two-tape PROMISE DECIDER, not a SAT decider on all formulas.

A simpler variant uses a one-time tape2 @ sentinel at head position B (D2=1), and passed a larger independent test grid. The stronger D2=0 version was also audited at the actual clause-sign parser level.

## Fast endpoint: optimize input-head reversals

A second SINGLE uniform two-writable-tape TM scans each B-module batch forward on actual framed exact22 clause records, writes/erases up to B cached signs on tape2 and marks each processed module's trailing ';' on tape1:
  S2<=B+2, D1<=2m, D2<=2m+1,
  T=O(N ceil(m/B)), R1=O(ceil(m/B)).
The marker must be placed on each module's TRAILING clause semicolon, not its leading '/', otherwise a naive implementation incurs O(m) input-head reversals merely to reread signs. This improved version explicitly avoids per-module reversals.

## Closed model-specific phase diagram, CONDITIONAL on TWOTAPE-JOINT1 lower bounds

For B=m^(alpha+o(1)), 0<=alpha<=1, write/space/time/reversal exponent tuples attainable:
  sparse unchanged tape2: (s2,d,t,r)=(alpha,1-alpha,2,1);
  buffered forward:        (s2,d,t,r)=(alpha,1,2-alpha,1-alpha).
TWOTAPE-JOINT1 claims necessary:
  t+s2>=2, r+s2>=1, d+s2>=1,
  d<1 => t>=2 and r>=1
(all on one two-writable-tape machine, D=D1+D2, physical counters).
Combining these with the new upper algorithms gives, on this CALIBRATED EASY PROMISE for 0<=s2<=1:
  if d+s2<1: IMPOSSIBLE under project lower bound;
  if d<1 and d+s2>=1: attainable minimal (t,r)=(2,1);
  if d>=1: attainable minimal (t,r)=(2-s2,1-s2).
Input-reading time t>=1 supplies extension for s2>=1.
This closes the previously OPEN **INTERIOR WRITE-SPACE UPPER CONSTRUCTION for the declared calibrated family**, without closing any ordinary-SAT or RAM lower-bound problem. Lower theorem must pass external mathematical referee first. No contradiction to P=NP.

## Explicit RAM escape, audited on SAME exact22 gadget

Re-encode the same clauses with fixed-width binary variable IDs L=ceil(log2(15(m+B)+1)), record length C=3L+6. Alice and Bob module record widths are 1+2C, so their control sign positions are affine functions of module index i. An indexed-input word RAM checks both signs with at most 2m random sign probes and O(logN) work/address bits; deriving m,B,L from a single source pass costs O(N) further bit work. This avoids tape head transport entirely. Exhaustive 6372 selector/structure cases, 37848 indexed sign probes. Thus the new *tape* frontier is NOT RAM-native; the residual semantic obstruction is still open.

## Reproducibility and exact status

Files available to user as TWOTAPE_INTERIOR2_research.zip and TWOTAPE_INTERIOR2_report.pdf:
- sparse_write_two_tape.py: 6460 selector finite simulations, 32124 assertions;
- UniformCalibratedTape2Machine (same script): 31014 runs, 92976 assertions;
- exact22_calibration_bridge.py: 6372 proper exact22 clause/semantic module cases;
- framed_exact22_machine.py: 1279 finite-state actual source-sign comparisons, 3810 assertions;
- framed_no_work_writes.py: 1279 FINITE-STATE proper exact22 framed cases, 5062 assertions, NO TAPE2 WRITES;
- framed_batch_machine.py: 1279 basic+1288 forward scans, 8890 assertions, includes input-head reversal charges;
- indexed_RAM_control.py: 6372 fixed-width exact22 source-index cases, 37848 probes;
- original verified W1 gadget script, raw per-run statistics, plots, formal note and 6-page rendered PDF.

All Python scripts in package are self-contained with prior_exact22_gadget.py; no project path dependency. Counts represent finite validation, not mathematical proof of lower bounds. Source case semantics is verified by strict signed occurrences and fixed independently enumerated 15-var gadget model counts. Framing assumes fixed delimiter alphabet and a detectable end of work tape.

**Key attack to pursue:** prove/falsify TWOTAPE-JOINT1's native splicing and BOTH-TAPES change-event lemma; check mutation of input tape1 and simultaneous tape changes. If verified, the interior frontier on our easy framed promise is RESOLVED, so do not waste cycles searching for a stronger transport lower bound on that same promise. Redirect to *RAM-native connected SAT semantic* restrictions or a no-framing source compiler with all costs. In particular, any conjecture claiming a required write per compared sign is FALSIFIED by this construction.

## Five existing research agents (additive assignments, preserve enabled state)
LSPV-1: certify matching lower+upper statement with correct globally sound/promise program quantifiers; no P!=NP transfer.
LSPV-2: independently code finite-state delimiter parser and T,S,D,R resource bounds and vary dummy-calibration grammar; test true unframed signed CNF.
LSPV-3: distinguish witness construction from sound SAT acceptance; test true connected modules and whether any semantic hardness survives the RAM escape.
LSPV-4: prove or falsify TWOTAPE-JOINT1 event-code lower bound, especially mutated tape1, program selection and offset encoding; check full matching t/r frontier.
LSPV-5: aggressively break the two real clause-level machines (head2 origin, hidden counters, marker collision, loss of parse validity after mutation, source-program nonuniformity, simultaneous writes), and the conditional optimality claim. P versus NP OPEN.

References: earlier project TWOTAPE-JOINT1 https://github.com/j15marti/pnp/blob/main/research/governance/2026-10-27_TWOTAPE_JOINT1_BOTH_WRITABLE.md ; Hennie & Stearns, JACM 1966 DOI:10.1145/321356.321362; Vitanyi, JCSS 1984 DOI:10.1016/0022-0000(84)90001-1.
