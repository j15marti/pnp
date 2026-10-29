# ARC211 LSPV-1 independent audit and sharpness witness

Time: 2026-10-28 20:00 America/Los_Angeles. Scientific state: P versus NP OPEN; no new tasks or schedule changes.

## Source audit

The Library archive `Connected_Interface_Audit.zip` (libfile_a2862f0165b4819195a88d9e896a42a7) was materialized, its `REPORT.tex` and five-page `REPORT.pdf` inspected, and its original `audit.py` rerun. Archived and independently generated `results.json` are byte-identical, SHA-256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`. The exact 4680/7191/139 control counts recur. The statement `k<=4b`, `n<=3b+12bq`, `b+q>=sqrt(n/3)-1/4` is correct with all stated fixed-boundary, disjoint-private-module and per-module syntactic clause-hitting assumptions, but yields no decision-time lower bound.

## New restricted theorem: square-root exponent is tight

For integer r>=2, set b=3r, Y={y_0,...,y_(b-1)}, and k=b private modules, each with b private variables p_(j,i). Build clauses

    C_j^Y = (y_j OR y_(j+1) OR NOT p_(j,0));
    Q_h^Y = (NOT y_(3h) OR NOT y_(3h+1) OR NOT y_(3h+2));
    C_(j,i)^P = (p_(j,i) OR p_(j,i+1) OR NOT p_(j,i+2));
    Q_(j,0)^P = (NOT y_(j+2) OR NOT p_(j,1) OR NOT p_(j,2));
    Q_(j,h)^P = (NOT p_(j,3h) OR NOT p_(j,3h+1) OR NOT p_(j,3h+2)) for 1<=h<r.

All indices are modulo b where needed. These are original literal swaps preserving strict exactly-2-positive/exactly-2-negative occurrence per variable. Every clause has three distinct variables, all signed clauses are unique, the incidence graph is connected, and the original source modules have no cross-module private variables.

The exact per-module minimum private ternary clause-hitting set is r, since the r variables p_(j,3h) hit all clauses without Y, and there are 4r-1 private-only clauses while each private variable occurs at most 4 times. Therefore n=b+b^2=9r^2+3r and b+q=4r=Theta(sqrt(n)). No stronger universal polynomial exponent delta>1/2 follows from just the static bound's hypotheses. The period-3 assignment 110 on Y and on every private module satisfies everything. This is a **tightness counterexample for one syntactic architecture**, not evidence of SAT hardness.

Reproducer (`2026-10-28_2000_ARC211_tight_static_interface_audit.py`) checked r=2,3,4,5,7,10, 2560 source clauses, 4672 exhaustive local hitting subsets at r<=4, and 12 negative source-model controls. All passed. The LaTeX report contains the complete all-r proof.

## Lead dependency chain, unchanged ownership

LSPV-2: test whether moving guard compilation survives introduction of multiple nontrivial private module signatures rather than only a fixed easy cycle; charge full re-entry bits.

LSPV-3: seek a genuine connected strict exact22 SAT/UNSAT matched family with affordable source-authenticated *semantic* local certificates, not a static b=q=O(log N) syntactic cover invalidated by the proven bound.

LSPV-4: account for actual physical construction and source access on single-tape, separate read-only input multitape, two writable tapes and RAM; do not transport restricted crossing exponents without a simulation.

LSPV-5: independently challenge whether k=b, q=r and clause uniqueness hold on this splice for every r; distinguish library-script tests from proof; protect all root-main ownership sentinels.

LSPV-1: the open arrow is a uniform, unconditional, answer-preserving, single-child physical-size shrink on a recursively closed class containing ordinary SAT, or an independently demonstrated same-machine separation. Neither is supplied here. The original one-call OpenAI quantum architecture uses a target-dependent Boolean oracle not classically computed; this remains an analogy only.

No older sound result is retired by this handoff. Reviewer status pending; P versus NP OPEN.