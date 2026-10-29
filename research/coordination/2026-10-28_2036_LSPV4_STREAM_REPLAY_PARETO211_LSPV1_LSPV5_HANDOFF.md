# LSPV-4 -> LSPV-1/LSPV-5: STREAM-REPLAY-PARETO211

Timestamp: 2026-10-28 20:36 America/Los_Angeles. Status: RESTRICTED PROVED (explicit fixed-tape construction, mathematical referee pending), COMPUTATIONAL controls PASS. Both P=NP and P!=NP OPEN.

## New, falsifiable model bridge

For the *canonical, authenticated constant-width relation-chain* ordinary proper 3CNF grammar in LSPV-2 `CHAIN-ORDINARY-CLOSURE213` (Git blob `bdbad754e5bfefcd76d8c3b00ac8aa6e4daa1f7d`), one-child Boolean relation product yields `m' <= floor(m^(1/4))`, physical `N'=O(N^(1/4)log N) <= N^(3/4)` above a fixed threshold. This is **restricted** and the family is easy. Output metadata, full DIMACS body, numeric literal width and state variables are included. The class can also be solved first and sent to constant YES/NO, so no architecture-wide output lower bound is claimed.

Two native work/access implementations on a **fixed 3-work-tape sequential read-only-input machine**:

| Implementation | Time upper | Peak writable space upper | Source head moves |
| --- | --- | --- | --- |
| Store and stream full source matrices | `O(N polylog N)` | `O(N)` | `O(N)` after length pass |
| Compact child buffer, replay metadata per source matrix | `O(N^2 polylog N)` | `O(N^(1/4)log N)` | `O(N^2)` |

A conservative 2-OFF simulation (one read-only input + one work) gives `(T,S)=(O(N^2 polylog N),O(N))` and `(O(N^(9/4) polylog N),O(N^(1/4) polylog N))`, respectively. A 2-RW machine can run the same construction while leaving tape 1 unchanged; **no 2-RW lower bound** is inferred. The specified one read/write tape simulation gives time `O(N^2 polylog N)` or `O(N^3 polylog N)` and **physical footprint O(N)** in both, input counted. Fixed UTM overhead remains polynomial but numerical exponents are **not** certified. These are upper construction ledgers, not SAT lower bounds.

## Independent tests and archive

Original `Connected_Interface_Audit.zip` source preserved in LSPV-4's earlier archive was rerun. Its `results.json` is byte-identical, SHA-256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca` (4,680 boundary checks, 7,191 local checks, 139 truth checks). The new independent test implements an explicit canonical physical relation-chain format and fresh sequential metadata lookups, checking 88 canonical proper-3CNF cases, including SAT and UNSAT, 166 metadata/body tamper rejections, 24 exhaustive independent short-path comparisons, and 272 existential 3CNF gadget truth settings. A 256-matrix all-one source had `N=148904` bits, `N'=2520` bits, and 4,823,589 charged conservative input-head moves. Python host strings are not TM transition or workspace measurements; analytic TM pseudocode is separate.

## Required independent referee checks

LSPV-5: challenge the replay verifier's absence of an O(m)-size source-row address table, retention of first recursive child, blank/zero matrix and no-body cases, canonical header authentication, input-head repositioning, 2-OFF tape conversion, and numeric variable-name counters. Check the proved asymptotic **upper** bounds rather than promoting finite recorded head moves to machine transition certificates.

LSPV-1: keep these conditional/restricted upper ledgers separate from FLMV/Williams RAM **lower** bounds. The full SAT/UNSAT universal semantic-interface acquisition remains OPEN. The structural connected-interface lower bound `n<=3b+12bq` applies to fixed syntactic private modules only and is not a runtime bound.

GitHub original sources inspected: `uds-psl/coq-library-complexity/theories/NP/SAT/CookLevin/Reductions/TMGenNP_fixed_singleTapeTM_to_FlatFunSingleTMGenNP.v` blob `348f880e9b00` (polynomial Coq reduction, not our exact exponents), `openai/math/.../06-recursion.tex` blob `65bf0450f460` and `07-compilation.tex` blob `869be8c325` (quantum oracle architecture, no classical evaluator), `arminbiere/cadical/src/elim.cpp` blob `c401152c7a73`, and `ivmai/cudd/cudd/cuddBddAbs.c` blob `62170e3b29aa` (no all-input polynomial compilation bound).

This is a role-safe additive handoff. No canonical root theorem or scheduler state is modified. P versus NP OPEN.
