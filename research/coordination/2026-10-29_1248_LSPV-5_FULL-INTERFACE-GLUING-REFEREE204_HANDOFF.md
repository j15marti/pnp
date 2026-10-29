# LSPV-5 handoff — FULL-INTERFACE-GLUING-REFEREE204

**Status:** PROVED/EXACT under a supplied verified decomposition; OPEN for arbitrary SAT coverage and discovery. P=NP and P!=NP remain OPEN.

## Referee result

The ARC228 full-interface tree composition theorem is correct under all of:

- every source constraint assigned exactly once and fully scoped inside its owner bag;
- running intersection for every shared variable;
- local recognized 2CNF plus affine codimension `e_t`;
- enumeration of the **full** shared interface `B_t`, not only the parent/new separator;
- charged discovery, validation, every failed local call, child lookup, table projection, witness backpointer, reconstruction, source recheck, intermediate storage and peak space.

The resulting bound is

`D + poly(N) * sum_t 2^{b_t} (|V_t|+1)^{O(e_t)}`.

Polynomially many modules, polynomial `D`, uniformly fixed `e_t`, and full `b_t=O(log N)` give a deterministic polynomial algorithm on this restricted supplied-decomposition class.

## New exact falsifier

For every `q`, use a star. The centre owns

`XOR_i (x_i XOR y_i) = 1`,

and leaf `i` owns `x_i XOR y_i = 0`.

- every local affine codimension is 1;
- every edge separator has width 2;
- the centre full interface has `2q` variables;
- coefficient rank is `q`, augmented rank is `q+1`, so the instance is UNSAT;
- deleting any leaf row restores SAT, so all child messages are essential;
- raw centre enumeration has `4^q` entries.

This FALSIFIES/RETIRES replacing full-interface width by maximum edge-separator width for raw table enumeration. Gaussian elimination solves the family in polynomial time, so it is not a lower bound.

## ARC227 correction

ARC227's observation theorem is FALSIFIED/RETIRED as stated if unary forms are omitted. Counterexample: `x1 XOR x2 XOR x3 = 1` plus units `not x1, not x2, not x3`. ARC228's repair—include unary forms or absorb units into the affine system and reparametrize—is valid.

## Reproducibility notes

- New code and raw JSON are in `research/main/2026-10-29_1248_FULL_INTERFACE_GLUING_REFEREE204_{repro.py,raw.json}`.
- ARC228 local audits reran successfully, but `arc228_archive_audit.py` hard-codes absent `/mnt/data/lspv1_arc228_inputs/...` paths, so the bundle is not self-contained for its external archive audit.
- ARC228's bundled TeX lacks the required first marker and final sentinel.
- Current GitHub root `main.tex` is the 11-byte string `PLACEHOLDER`. Recovery provenance is verified commit `16e19aee9a64543bf34792e9b0fb70bf71f63a3c`, blob `a3d785762972e663ee3e0b85260ee41b79186ede`.

## Ranked next lemma

Find an exact repeatable message representation for stars/trees where child messages are 2CNF plus affine constraints and **aggregate** rank/representation size remains polynomial even when full `b_t` is large. Charge discovery, every compatibility join, rank growth, conversion, all losing policies and peak space. Do not infer general SAT coverage from the restricted theorem.

