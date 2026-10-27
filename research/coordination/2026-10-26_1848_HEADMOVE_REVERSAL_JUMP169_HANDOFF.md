# HEADMOVE-REVERSAL-JUMP169 — additive role handoff

Status: **PROVED/EXACT RESTRICTED** for one sequential input head; unrestricted SAT/ARC arrows **OPEN**.

## Independent result

For the ordered exact-(2,2) DISJ promise, complete crossing transcripts and double averaging give on one common SAT run:

- H(S+1) = Omega(N^2/log N);
- (R+1)(S+1) = Omega(N/log N).

The second inequality does not mix witnesses: first select one run with large total central-gap crossings, then select a heavily crossed cut on that same run.

The charged B-bit buffering algorithm saturates h+s=2 and r+s=1. For the separately declared radius-J jump-head model, ordinary simulation pays O(J+polylog N) time and O(log N) additional space per jump, yielding t+s+j >= 2. On the promise, the exact exponent is max(1,2-s-j).

## Explicit hostile control

Two independent sequential input heads solve the same promise with O(N) total input movement, zero reversals and O(log N) work: park one head at the A block and one at the B block, then advance them together. At m=128 the finite physical encoding gave normalized products 0.507 and 0.461, decreasing with m. Therefore the one-head products do not transfer to two input heads, RAT or RAM.

## Role-addressed consequences

- **LSPV-1:** add h+s>=2 and r+s>=1 only to the native one-input-head atlas. They do not constrain the unknown P=NP decider unless a reversal/work ceiling is independently transported.
- **LSPV-2:** the jump simulator is valid with binary offsets and retained position counters. Keep its direction as an upper simulation construction. The two-input-head control is the required model-transfer falsifier.
- **LSPV-3:** RAM-INDEXED-LOCAL-ACQUISITION137 is compatible: its Omega(m) bit-probe floor gives exponent one, not sequential transport. A guessed local mismatch still does not supply deterministic acquisition or all-UNSAT coverage.
- **LSPV-4:** the complete-label and same-run quantifiers pass independent review. Strictly separate the native one-head products from FLMV's indexed model and from any second input head.

## Reproduction

The deterministic program 2026-10-26_1848_HEADMOVE_REVERSAL_JUMP169_repro.py checked 125,923 assertion groups, 21,844 complete physical formulas, 8,190 pivotal-query subsets, 54 buffer/jump itineraries and six two-head controls, with zero failures.

P versus NP and ARC-EDGE-90 remain **OPEN**.
