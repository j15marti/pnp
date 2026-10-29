# ARC215 LSPV-1 coordinated research handoff, 2026-10-28 23:37 PDT

**Role:** LSPV-1 Formal Proof Lead. **Scientific status:** PROVED/RESTRICTED (well-known closure methods, exact joint theorem); COMPUTATIONAL (finite hostile tests); FALSIFIED (automatic hereditary shrink of this projection-only compiler); OPEN (unrestricted single-child SAT contraction, all-input source-authenticated UNSAT certificates, ARC-EDGE-90 and P versus NP). Independent mathematical review pending. No schedule/task modification.

## PROPOSE, SEARCH, BUILD

Missing arrow: an unconditional deterministic, sound for both SAT and UNSAT, fully charged, answer-oblivious single-child contraction with recursive closure on a class containing ordinary SAT, or a polynomial-value decreasing rank and polynomial complete states. Four falsifiable mechanisms, fixed prior to source search: (M1) 2CNF private-variable elimination retains 2CNF; (M2) GF(2) private-variable elimination retains bounded affine rank; (M3) their shared-variable projection automatically power-shrinks on repeated application; (M4) logarithmic overlap permits polynomial decision. M1/M2 exact, M3 false generally at level 2, M4 exact under named overlap hypothesis.

GitHub queries: `2sat xor gauss`, `pathwidth dynamic programming parity xor`, `gauss_jordan` scoped to `msoos/cryptominisat`, and `program` scoped to `openai/math`; source inspected: `msoos/cryptominisat/src/propengine.cpp` blob `5e685596b4194e8818a9b3664fbdc95a3b1b5719` (XOR watchers, `gauss_jordan_elim`, conflict logic); `msoos/cryptominisat/README.md` blob `7636988713ee16802b84fb1cdf688ea8f87da70e`; `openai/math/preprints/Polynomial-Time-Unitary-Synthesis-from-a-Boolean-Oracle-October-5-2026/build/sections/06-recursion.tex` blob `65bf0450f460311b13a11a136db6ada4520cb6f0` (one smaller quantum call, no classical target-oracle evaluator). Mathematical primary sources: Schaefer 1978 Boolean CSP dichotomy; Eén and Biere 2005 variable elimination. Source-level implementations are NOT machine-verified theorems or universal polynomial SAT solvers. Reused LSPV-1 ARC213 and LSPV-2 AFFINE-RESOLVENT-FIXEDPOINT216 without relabeling them as new.

## Exact theorem and structural failure

For a mixed problem with a 2CNF component C on variables Z union X and an affine component A on variables Z union Y, where X,Y,Z disjoint and b=|Z|, syntactic discovery and deterministic Davis-Putnam/Gaussian projection construct explicit `C_Z AND A_Z` on Z such that for EVERY z, `(exists x,y C(x,z) AND A(y,z)) <=> C_Z(z) AND A_Z(z)`. The physical encoded child is `O(b^2 log(b+2))` bits, even if the parent is large. This is a restricted construction, not a solution of mixed SAT. If b <= N^{1/2-epsilon} it yields one power-short child, but DOES NOT imply second-level contraction. If b=O(log N), enumeration of 2^b boundary assignments is polynomial and fully charged. The ARC213 mixed NP-hard encoding has linear shared overlap, so neither restriction applies.

Hostile recurrence: choose shared core `(AND_i (z_i OR z_(i+1))) AND (AND_i (z_i=1))`; add private 2CNF pads `(z_i OR u) AND (NOT z_i OR NOT u)` and affine pads `z_i XOR v=0`. The pads are tautological under existential projection; the first explicit projection removes them, and the next projection fixes the growing core exactly. A mirrored UNSAT core uses `(z_i=0)` rows instead. The family refutes universal hereditary contraction for this exact fixed compiler, not P=NP or general semantic methods.

## Independent evidence

User Library `Connected_Interface_Audit.zip` found at `/P vs NP/Connected_Interface_Audit.zip`; original `audit.py` rerun unchanged. Produced archived `results.json` byte-for-byte, SHA256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`: 4,680 boundary subsets, 7,191 local discovery checks, 139 brute force comparisons; 130 sampled strict exact22 variants SAT. Its inequality `k<=4b, n<=3b+12bq` applies ONLY to its static architecture and is not a runtime bound. The proof is not kernel-verified.

ARC215 Python reproducer independently checks 1,200 random mixed problems (129 SAT, 1,071 UNSAT), 60 signed ARC213-like gadget instances, two ternary-XOR interaction cases (SAT/UNSAT), four padding/fixed-point cases (b=3,5,9,17), 1,266 total cases. In each small case the COMPLETE boundary relation agrees with brute-force source projection, separately for 2CNF, affine, and mixed. Four physical (parent,child,second) byte triples: (1527,60,60), (2641,88,88), (4869,144,144), (9769,280,280). All tests passed. Experimental checks are finite and do not establish asymptotics.

## One-realization resource and model ledger

The report contains generous native upper bounds for the compiler: indexed RAM T<=N^{6+o(1)}, S<=N^{3+o(1)}; fixed-k read-only-input multitape T<=N^{9+o(1)}, S<=N^{3+o(1)}; conservative one shared read/write tape simulation T<=N^{12+o(1)}, footprint <=N^{3+o(1)} including input, observing t_single <= t_multi+max(1,s_multi). Fully writable two-tape is a distinct native model; fixed UTM includes a program and interpreter. These are compiler upper bounds, not decision lower bounds. Charge syntactic scan, source authentication, generated resolvents, matrix pivots, output, failed branches and peak simultaneous storage. Enumeration of 2^b when used is not free.

## Coordinated next tasks, no new tasks or schedule changes

- **LSPV-1 at :00:** seek noncircular all-input interface discovery and a second-level successor on the projected shared core; maintain proof DAG with explicit time/space exponents.
- **LSPV-2 at :12:** search for a provably contracting alternative to resolution/affine private elimination that survives both its affine-resolvent fixed point and the present shared-core fixed point; track physical Tseitin reentry size.
- **LSPV-3 at :24:** test source-authenticated discovery of a moving interface on both answer classes, including the exact mixed hardness gadget, charging any failure or oracle/access bits.
- **LSPV-4 at :36:** independently transport ONE concrete constructor over single tape, read-only-input multitape, two fully writable tapes and indexed RAM with simultaneous peak space, no exponent mixing or crossing-transfer.
- **LSPV-5 at :48:** red-team first/second hereditary closure and counterexamples, verify that parser and output sizes are physical, source-authenticated and not using the truth bit, and referee independent proof arrows.

Do not modify agent schedules, task identities, ownership, peer regions or false claims of general P versus NP separation. **P versus NP OPEN.**
