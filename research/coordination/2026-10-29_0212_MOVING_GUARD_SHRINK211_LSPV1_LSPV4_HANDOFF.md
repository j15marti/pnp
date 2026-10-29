# LSPV-2 additive handoff: MOVING-GUARD-SHRINK211

Timestamp: 2026-10-29 02:12 UTC. Status: RESTRICTED PROVED/EXACT, independent review pending. P vs NP OPEN.

## What was independently audited

Library `Connected_Interface_Audit.zip`, ID `libfile_a2862f0165b4819195a88d9e896a42a7`: REPORT.tex / REPORT.pdf visually inspected, audit.py reran, results.json matched byte-for-byte: 4,680 boundary cases, 7,191 discovery checks, 139 brute comparisons. Its static exact22 coverage lemma is algebraically valid under stated module/partition assumptions: `k <= 4b`, `n <= 3b+12bq`, `b+q >= sqrt(n/3)-1/4`, and for `b=0`, `q >= n/3`. This says nothing about unrestricted SAT time.

## New one-child result

A closed, syntactically recognized annotated ordinary-3CNF class has at least one proper clause on each consecutive triple and a four-variable end guard. Eliminate all but sqrt(r) suffix variables; use exact 16-pattern guard DP, serialize guard back into ordinary proper3CNF via <=16 fresh auxiliaries / <=32 clauses, and renumber. The projected formula is exactly equivalent as a function of the remaining variables and remains in the same class. Physical size is O(sqrt(r) log r); with a paid bounded-frontier fallback in finite small cases, output <= N^(19/20) above a fixed threshold. The fallback calls no SAT oracle; the entire class is already decidable in polynomial time. Both SAT and UNSAT controls pass. This does NOT give a contraction for all SAT and does NOT strengthen either side of P vs NP.

## High-value next targets

LSPV-1: test whether any all-input answer-preserving, not function-preserving, replacement can discover a suitable small moving/hierarchical separator with paid preprocessing and no free answer bit. LSPV-4: audit any claimed FLMV transfer against native indexed-input machine and physical child-length budgets; the restricted one-child recurrence is not itself an ARC contradiction. Continue uniform inverse Rank/Select source-header and alias accounting with no stored occurrence table.

GitHub search and source inspected: `arminbiere/cadical/src/elimfast.cpp` blob `0d6c00897acb6fe73c8cb4028e2c9bb309683535`, `crillab/d4/preproc/Forgetting.cc` `8f00f7397b70cb18dc24f3488722be372343b1c4`, `berkeley-abc/abc/src/bdd/cudd/cuddBddAbs.c` `e2345617c1e56bbc7bcbb3c06002cfb975dd4fe7`, `openai/math` recursion `65bf0450f460` and compilation `869be8c325`; these provide implementation architectures, no universal SAT shrinker.

Main.tex currently lacks LSPV-2 ownership markers and includes a comment that its prior full body is elided; preserve root untouched and request marker reconciliation, not a blind overwrite. Schedules and all other roles unchanged.
