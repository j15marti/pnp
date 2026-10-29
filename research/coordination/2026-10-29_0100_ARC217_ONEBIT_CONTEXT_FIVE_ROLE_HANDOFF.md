# ARC217: Guarded one-bit contextual projection, additive five-role handoff

LSPV-1 Formal Proof Lead, 29 October 2026, 01:00 PDT. The all-input SAT contraction, ARC-EDGE-90, and P versus NP remain **OPEN**. No new agents, task modifications, schedule changes or role reassignment are authorized.

## New proved restricted arrow, independent review pending

For every signed 3CNF `F = AND_j (l1 OR l2 OR l3)`, construct one `g` and per clause fresh `(y1,y2,y3,t)` with binary clauses `(li OR yi)` and XOR3 rows `y1 XOR y2 XOR t = 0`, `t XOR y3 XOR g = 0`. The local existential relation is exactly `g OR clause`; hence `exists x,y,t H_F(g,x,y,t) = g OR SAT(F)`. All `H_F` are explicitly satisfiable at `g=1, y_i=1, t_j=0` for arbitrary `x`. But whether `H_F` has an extension at `g=0` is NP-complete, and entailment of `g=1` is coNP-complete even under the guaranteed-SAT promise. Exact contextual projection to the **one-bit external interface** can be expensive to construct even though the output is one of two constant-size tables. This does not rule out a decision-only shrinker, which outputs YES on all unpinned `H_F`.

Important caveat: the full binary/affine **syntactic overlap** is size `3m`, and the affine nullity of the pinned per-clause parity system is `2m`. This does not contradict ARC215 or ARC216. No new general decision-time lower bound follows.

## Hostile controls

Standard-library Python reproducer with deterministic seed 20261029 passed all checks: 16 local guard/pattern rows, all 256 subsets of the eight 3-variable proper signed clauses, 4096 global assignment/guard rows, 240 random formulas (208 SAT, 32 UNSAT), 480 random guard projections, 15 local witness cases and the independent-consistency false-positive control. The unmodified original `Connected_Interface_Audit.zip` from authenticated ARC215 archive reproduced 4680/7191/139 original counts byte for byte; `results.json` SHA256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`.

## SOURCE/SEARCH provenance

Inspected `j15marti/pnp` root `main.tex`, `AGENTS.md`, `CODEX.md`, pnp-research skill, own ARC213-ARC216 and peer connected-interface work. Search queries: `gaussian xor` in `msoos/cryptominisat`, `projected` and `ONEBIT GUARDED PARITY` in `j15marti/pnp`, global `backbone literal`, `guard satisfiable projection parity`. Read `msoos/cryptominisat/src/gaussian.cpp` blob `7b9d200c1c1d8e344ce0c3109bfc92806a14359b` and `openai/math/.../build/sections/06-recursion.tex` blob `65bf0450f460311b13a11a136db6ada4520cb6f0`. The latter uses one smaller quantum circuit but no polynomial classical oracle constructor. Primary related background: Schaefer STOC 1978 and Fortnow-Santhanam STOC 2008. No kernel-verified proof is claimed.

## Role-specific dependency

LSPV-1: Audit contextual vs decision-only definitions before treating compact summaries as paid constructions. LSPV-2: seek a genuinely constructive circuit summary of the two relations, charging the choice bit. LSPV-3: test a decision-only adaptive one-child successor after fixed points, with polynomial-value rank and two-level hereditary closure. LSPV-4: check native single shared tape, read-only-input multitape, two writable tapes, fixed common-input UTM, and RAM ledgers; never borrow a sequential-head exponent. LSPV-5: independent red team on exact quantifiers, duplicated auxiliary sources, the promised-SAT property and the risk of claiming general hardness from a contextual relation.

All five original scheduled research identities remain unchanged.
