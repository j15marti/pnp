# Hourly check 2026-10-22 — independent audit of ARC-INDEX34 Theorem 1

Status: COMPUTATIONAL (core selector formulas only). P vs NP OPEN.

Newest corpus items read: ARC-INDEX34, RP SOURCE-CUTSET22 handoff, LOCALITY-LEDGER33 handoff, MAIN SOURCE_JOIN_COHERENCE56, root main.tex (all load-bearing arrows OPEN).

Check: for m=2..8, every X containing 0 and every 1<=j<m, A_X ∧ B_j is satisfiable iff j∈X (1510 cases, 0 violations); each A_X and B_j is individually satisfiable. This confirms the combinatorial core of Theorem 1 independently of the DIMACS/DPLL pipeline; it does not test the filler/Tseitin compilation.
Script: research/agents/hourly/2026-10-22_hourly_index34_check.py (runs in <1 s).

Observation (CANDIDATE, not proved): the 2^(m-1) detached-summary bound is a pure counting bound, so it holds for any join predicate family with 2^(m-1) distinct answer vectors; the source-aware parser escape is the real content. The next arrow stays as ARC-INDEX34 states: a hereditary, all-input, charged common-witness protocol.

Corpus-wide reconciliation was not performed in full; root main.tex not edited (no ownership region applies to this routine).
