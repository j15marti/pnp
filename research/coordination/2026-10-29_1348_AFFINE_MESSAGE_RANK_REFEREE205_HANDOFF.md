# LSPV-5 handoff — AFFINE-MESSAGE-RANK-REFEREE205

Status: **PROVED/EXACT (restricted)** for the theorem below; **FALSIFIED/RETIRED** for the per-edge-rank shortcut; finite controls **COMPUTATIONAL**; general SAT coverage and both P=NP/P≠NP **OPEN**.

## Proved theorem

On a polynomial-time discovered and verified running-intersection module tree with source-once ownership, compile each exact child message that is bijunctive into parent 2CNF and each exact child message that is affine into parent affine equations. If

- `S_t` is the parent separator,
- `A_t` is the original parent affine matrix,
- `M_t` is the set of all embedded affine child-message rows, and
- `E_t = rank([A_t;M_t])`,

then exact bottom-up decision and witness reconstruction take

`D + poly(N) Σ_t [2^{|S_t|} (|V_t|+1)^{O(E_t)} + 2^{|S_t|} poly(|S_t|+1)]`.

Thus polynomially many modules, polynomial discovery/verification, logarithmic separators, and uniformly bounded **aggregate embedded rank** give a polynomial algorithm on this supplied-decomposition class.

## Specific falsifier

For `h` disjoint width-three child separators, let child `j` send `a_j xor b_j xor c_j = 1`, while the center owns the XOR of all triples equal to `beta`. Every child message has affine codimension one, but their aggregate embedded rank is `h`. The star is SAT iff `beta = h mod 2`; in the mismatch case every child row is essential to UNSAT. Therefore bounded affine codimension per edge does **not** preserve bounded parent codimension.

The family is pure affine and easy by Gaussian elimination. It is an accounting counterexample, not a lower bound.

## Referee conclusions

- ARC229's exact bijunctive-message closure is valid under authenticated ownership, full scope containment, running intersection, and exact table construction.
- HYBRID-BAD-MESSAGE228's exceptional-union composition is valid with its full union parameter charged.
- Affine absorption is complementary: it replaces union enumeration by aggregate-rank accounting only when the resulting rank is controlled.
- CONNECTED-AND-CONNECTOR231 was inspected, but its fixed 15-variable guard table was not independently replayed in this run.

## Artifacts

- `research/main/2026-10-29_1348_MAIN_AFFINE-MESSAGE-RANK-REFEREE205.tex`
- `research/main/2026-10-29_1348_AFFINE_MESSAGE_RANK_REFEREE205_repro.py`
- `research/main/2026-10-29_1348_AFFINE_MESSAGE_RANK_REFEREE205_raw.json`

All finite assertions passed: 278 exhaustive relations through arity 3; 800 affine cosets; 430 rejected one-point mutations; 500 random 2CNF projections; 16 parity-star instances through `h=64`; 600 mixed-rank checks; duplicate affine-message controls through 64 copies.

## Next lemma

Prove coverage for one precisely defined hereditary connected strict22 subclass: polynomially discover and verify a running-intersection tree with `|S_t|=O(log N)`, every exact child message bijunctive or affine, and `E_t=O(1)`, charging all failed decompositions and all controller work.
