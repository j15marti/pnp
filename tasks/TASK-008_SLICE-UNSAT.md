# TASK-008: SLICE-UNSAT monotone lower-bound branch

**Status:** OPEN  
**Priority:** HIGH  
**Created:** 2026-10-04

## Goal

Determine whether a computationally hard fixed-weight slice of clause-presence (UNSAT_{3,n}) admits a superpolynomial monotone-circuit lower bound, so that Valiant's slice-function theorem can transfer the result to unrestricted Boolean circuits.

## Load-bearing target

For (N=8\binom n3), define the monotone slice function (U_{n,t}) that agrees with clause-presence (UNSAT_{3,n}) on (|z|=t), is 0 below the layer, and 1 above it.

Prove for an explicitly hard slice (t=t(n)):

[
C_{mon}(U_{n,t})=N^{\omega(1)}.
]

## First deliverables

1. Exact statement and proof-hypothesis audit of Valiant's slice theorem.
2. Exact padding/hardness lemma for a fixed clause-count slice.
3. Reconstruction of the known full-cube monotone lower bound for (UNSAT_{3,n}).
4. Identification of the first proof step that fails on the Hamming slice.
5. Attempted repair using the current chain/correlation/clean-core decomposition.
6. Hostile tests against easy fixed-weight slices, Horn/2-SAT, Tseitin/parity, bounded treewidth, padding, and independent products.

## Guard

Do not infer slice hardness from full-cube monotone hardness. Do not claim a (P\neq NP) consequence unless both the slice hardness transfer and the superpolynomial monotone lower bound are proved.

Detailed plan:
`research/explorations/monotone-slice/2026-10-04_SLICE-UNSAT_PLAN.md`
