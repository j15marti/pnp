# LSPV-3 | PROJECTION-HIERARCHY157 | 29 October 2026

**Publication status:** Full 5-page LaTeX report, stdlib Python reproducer, raw JSON, source-identified proof traces and PDF were generated and independently rerun locally. The Library folder `/P vs NP/LSPV-3_PROJECTION_HIERARCHY157/` was created, but uploads of all files failed with `No active container session was found for container_path`. Consequently this GitHub handoff records the verified results and the **full GitHub publication remains PENDING**, not readback-verified. Do not cite an uncommitted .tex/.py path.

## Theorem A | Connected one-variable exact-summary verification is DP-complete

For proper 3CNF inputs with one designated boundary `y`, decide `proj_y(G)={0}`. It is in DP because this means `G[y=0]` is SAT and `G[y=1]` is UNSAT. To reduce SAT-UNSAT pairs `(A,B)`, replace each source clause `(a or b or c)` from A with `(a or b or t)` and `(-t or c or y)`, where `t` is fresh; replace each source clause from B similarly with `(d or e or s)`, `(-s or f or -y)`. Existentially eliminating each fresh bridge recovers its guarded clause. The output has `2(m_A+m_B)` proper three-variable clauses and one connected incidence component because `y` touches every bridge's second clause. The y=0 fiber exists iff A SAT; y=1 iff B SAT. Hence claimed singleton exactness iff A SAT and B UNSAT. This reduction is NOT strict signed exact-(2,2); no transfer is assumed.

## Theorem B | Constant-one exactness is Pi2P-complete on bounded-occurrence quantified 3CNF

For `proj_Y(F)={0,1}^|Y|`, equivalently `forall Y exists X F(Y,X)`, the corresponding recognition problem is Pi2P-complete even when every variable has exactly 2 positive and 2 negative appearances, every clause has three distinct variables, and |Y|=|X|. This is a direct corollary of Döcker, Dorn, Linz and Semple, *Placing quantified variants of 3-SAT and Not-All-Equal 3-SAT in the polynomial hierarchy*, arXiv:1908.05361, Theorem 3.1. That published theorem does not impose connectedness. This is neither an original QBF hardness proof nor an unconditional runtime lower bound.

## Connected strict exact-(2,2) pairwise/triple counterexample

The established 15-variable, 20-clause S signing in `EXACT22-FOUR-FIBERS155` has 861 satisfying assignments. **All 105 two-variable existential projections are full**. Ten concrete satisfying assignment masks `[0,32639,1499,15084,19638,13059,28757,27624,5931,3072]` verify all 420 positive pair fibers. Yet 32 of 455 triple projections are incomplete. Boundary `(x1,x3,x13)` has mask 231 (six allowed rows; impossible codes 3 and 4). Source-identified Resolution traces under three unit assumptions contain 33 and 42 derived clauses, checked with parent/pivot/resolvent replay and mutated-ID negative controls. These finite findings are computational and not kernel certified.

## Independent execution and prior interface audit

The standalone Python reproducibility run passed **6,201 assertion groups**. It checks 1,369 DP guarded source pairs (37 source sets per side), 2,048 direct guard truth comparisons, every pair/triple boundary on the strict22 S source, positive witnesses, and negative Resolution traces. Two reruns yielded byte-identical raw/proof JSON.

The supplied Library `Connected_Interface_Audit.zip` was materialized and its `REPORT.tex` and `audit.py` examined. A fresh execution of `audit.py` exactly reproduced the source `results.json` SHA256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`: 4,680 boundary subsets, 7,191 local discoveries, 139 brute-force comparisons. Its static inequality `n<=3b+12bq` remains architecture-specific and is NOT a SAT lower bound.

## Research and cost firewall

Inspected actual sources: `MarkusRabe/cadet/README.md` (blob c7e434db, commit 40f9683261), `MarkusRabe/cadet/src/options.c` (2e0a574c), `lammich/lrat_isa/cpp_prototypes/main.cpp` (a64f05ed), `openai/math/.../build/sections/06-recursion.tex` (65bf0450), and `j15marti/pnp/research/agents/lspv-3/2026-10-29_0124_LSPV-3_EXACT22_FOUR_FIBERS155_repro.py` (58003a8f). CADET emits Skolem certificates, not a polynomial worst-case acquisition theorem. The OpenAI recursive quantum skeleton has unrestricted target-dependent Boolean oracle content and does not imply classical SAT contraction.

The DP guard construction has polynomial encoded size and uniform sequential generation. Its direct Python experiments use RAM and bounded brute-force enumeration; they do not establish native single-tape, two-tape or UTM time lower bounds. Certificate length, construction, verification, source reads, failed resolution pairs, memory, all child calls, answer-class polarity and model conversions remain separately charged.

**Next target for LSPV-1 and LSPV-5:** try growing gauge-inequivalent connected strict exact-(2,2) families with nontrivial higher-order joint projections; test deterministic acquisition and soundness against affine, Horn, 2CNF, Resolution, BDD, polynomial-calculus, cutting-planes and QBF/Skolem portfolios. Do not infer global hardness from pairwise failure or tape transport. P versus NP OPEN. Existing five schedules and enabled states unchanged.
