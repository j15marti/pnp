# ARC216, five-role additive handoff

Timestamp: 2026-10-29 00:00 PDT. LSPV-1 Formal Proof Lead. Independent review pending. P versus NP and ARC-EDGE-90 OPEN. No task changes.

## Mathematical status

PROVED/RESTRICTED: For any explicitly encoded mixed instance of 2CNF plus GF(2) affine constraints, eliminate variables private to each subsystem by paid 2CNF resolution and Gaussian elimination. Let Z be the syntactic overlap, b=|Z|. The exact projected affine system A_Z has nullity r=b-rank(A_Z) when consistent; a deterministic all-input solver enumerates all 2^r affine solutions and tests projected 2CNF. Total native runtime is poly(N)*(1+2^r), and simultaneous peak space is polynomial in N. If r=O(log N), the specified mixed class is in P even when b is much larger than log N. All source processing, pivot discovery, failed trials, row operations, candidate evaluation, and output are charged. This is standard parameterization logic, not an all-SAT compressor.

FALSIFIED: Gaussian basis substitution generally retains the ordinary 2CNF language. A clause (z OR w) with row z XOR u XOR v=0 becomes (u XOR v) OR w. Three satisfying assignments (0,1,0), (1,0,0), (0,0,1) have falsifying majority (0,0,0), incompatible with any 2CNF existential projection.

HOSTILE GENERAL CASE: The ARC213 exact signed 3SAT gadget for m clauses has b=3m, affine rank=m and r=2m, independently of SAT versus UNSAT. Thus there is no general small-nullity certificate from this reduction. The all-eight-clauses UNSAT control checks all 65536 affine candidates in the enumerator.

COMPUTATIONAL: 720 brute-force random mixed instances (141 SAT and 579 UNSAT), 4554 pointwise projected assignments, 5 gadget controls, 5 small-nullity and 2 high-nullity controls, plus a majority falsifier. The unchanged original `Connected_Interface_Audit.zip` audit reproduced exactly: 4680 boundary subsets, 7191 local checks and 139 SAT comparisons, SHA-256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`. No finite test is promoted into a theorem.

## Dependency requests to existing five roles

LSPV-1: Prove or disprove a fully charged progress measure that decreases after the ARC215 zero-private-variable fixed point, allowing polynomial complete states. LSPV-2: Test an actual representation-changing circuit reentry that beats its AFFINE-RESOLVENT-FIXEDPOINT216 physical-length orbit. LSPV-3: Seek a uniformly constructible moving exact summary whose affine nullity is logarithmic or whose polynomial-value rank decreases on every SAT and UNSAT input. LSPV-4: Referee native one-tape, read-only-input multitape, fully writable two-tape, fixed-UTM and indexed-RAM costs, without cross-model exponent borrowing. LSPV-5: Attack the majority-closure proof, hidden source access, incorrect SAT-side selection, and any unsupported universal small-r assertion.

## Original sources inspected

`j15marti/pnp/research/agents/lspv-1/2026-10-28_2337_LSPV-1_ARC215_TWO_LANGUAGE_EXACT_INTERFACE_PROJECTION.tex` blob `707ee1cba0b357deee08b21635090cbe8c2d7888`; `msoos/cryptominisat/src/gaussian.cpp` blob `7b9d200c1c1d8e344ce0c3109bfc92806a14359b`; `openai/math/preprints/Polynomial-Time-Unitary-Synthesis-from-a-Boolean-Oracle-October-5-2026/build/sections/06-recursion.tex` blob `65bf0450f460311b13a11a136db6ada4520cb6f0`; original Schaefer (STOC 1978). Targeted GitHub queries were `xor gaussian elimination 2sat`, `parity xor cnf encoding tseitin`, and `AFFINE-RESOLVENT-FIXEDPOINT216`. OpenAI constructs a programmable skeleton, not a polynomial classical oracle constructor.

OPEN: All-input hereditary answer-preserving polynomial SAT contraction or a full polynomial-value rank algorithm, and any same-machine ARC/FLMV contradiction. All role ownership and existing schedules preserved.