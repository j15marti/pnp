# TASK-005 — CRS-PPC bridge theorems

**Status:** OPEN / high priority  
**Source:** `research/explorations/random-challenge/2026-10-01_CRS-PPC-SAT1.md`

## Objective

Determine whether the Causal Random-Snapshot Pointer-Pebbling audit model can be transformed from a solver-relative online game into a fixed problem that constrains every hypothetical polynomial-time static SAT decider.

## Exact proved guards

Do not re-prove or violate:

1. Fresh future IID blocks remain uniform after causal stopping times.
2. Constant-rate true randomness contributes only O(T) fresh bits in T elapsed steps.
3. A causal NDTM can wait for each current formula and guess its witness; it need not predict future G.
4. Polynomially many explicit promised-satisfiable SAT epochs remain polynomially verifiable.
5. If G fully assigns every variable, the remaining task is formula evaluation.
6. Runtime-sensitive epoch starts create solver-relative transcripts.
7. Requiring the exact reference solver transcript is trace simulation, not ordinary SAT.

## Primary theorem targets

### CRS-B — Causal Witness Lower Bound

Construct a SAT-derived challenge relation in which even after the fresh challenge is known, producing a valid stage response forces the same store/track/recompute resource being lower-bounded. Ordinary SAT witness guessing is insufficient.

### CRS-C — Schedule Externalization / Staticization

Remove machine-relative timing while preserving challenge unpredictability and the PPC resource lower bound.

### CRS-D — Fix-the-Transcript with Resource Preservation

Given positive probability of a hard G transcript, fix one transcript and prove preprocessing/random-access cannot collapse the lower bound.

### CRS-E — Static-to-CRS-PPC Compiler

For every arbitrary deterministic static SAT decider A in time n^k, derive a SAME_REALIZATION CRS-PPC strategy with quantitatively controlled preprocessing, state, rereads, recomputation, and sequential work.

### CRS-F — Barrier crossing

Audit the final proposed lower-bound line under semantic-oracle replacement and algebraic-oracle extension. Identify an actual nonrelativizing and nonalgebrizing hinge; randomness/provenance language alone does not count.

## Mandatory controls

- causal NDTM that waits for each current G challenge;
- maximal semantic SAT oracle;
- static full-input visibility;
- pointer jumping / doubling tables;
- preprocessing and memoization;
- INTERP / RECOMP / DEAD / COPY / DELAY;
- Horn, 2-SAT, bounded-treewidth, affine/Tseitin;
- full-assignment degeneracy;
- polynomial-z versus succinct-exponential-z distinction.

## Success criterion

A useful theorem must be solver-independent and stated on a fixed input/model, or come with a proved model-preserving compiler from ordinary static SAT. Machine-relative transcript divergence alone is not sufficient.
