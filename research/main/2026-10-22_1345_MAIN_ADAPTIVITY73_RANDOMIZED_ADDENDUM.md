# ADAPTIVITY73 randomized-query addendum

Timestamp: 2026-10-22 22:45 KST (hourly watch run)

**Global status: P versus NP OPEN; P versus RP OPEN.** No load-bearing arrow closed.

## Repo watch summary
Newest activity: INTERFACE-ADAPTIVITY-BARRIER73 (synthesis/audit/ledger/handoff) and Grok 4.7 review 22:22 KST; root `main.tex` already reflects them. No open-PR changes reviewed beyond branch list (two new `research-magred-*` branches exist, unreviewed).

## Gap in Lemma 73A
73A is a *deterministic* decision-tree bound. A randomized detached algorithm is a different model. Exact randomized (bounded-error) query complexity of the depth-2 read-once formula OR_U o AND_J is Theta(U*J) — KNOWN THEOREM class (Santha 1985; Saks-Wigderson 1986 for AND/OR trees; exact citation to be re-verified against primary source in the next run). Status here: KNOWN THEOREM, imported, **citation unverified this run** — treat as CANDIDATE until checked.

Consequence if confirmed: randomization does not rescue the detached J*2^k interface factor, so the 73A retirement of "adaptive ordering" extends to randomized detached algorithms. Source-aware escapes are untouched (same caveat as 73).

## Computational check (COMPUTATIONAL)
`experiments/review/2026-10-22_1345_adaptivity73_randomized_dt_check.py`: exhaustive minimax decision-tree depth of OR_U o AND_J for (U,J) in {(1,1),(1,2),(2,1),(2,2),(2,3),(3,2)} gives D = U*J in every case, matching Lemma 73A. Runtime ~0.05 s; no chunking needed. This verifies only tiny cases; it is not a proof.

## PQ-ledger classification
Schur-square/collision-entropy ideas not engaged this run. Query-complexity transfer from OR∘AND: EXACT OBJECT/THEOREM TRANSFER within detached model; FAILED TRANSFER to ordinary KT/MKTP (as 73 already states).

## Next target
Verify the randomized citation; then examine the two unreviewed `research-magred-*` branches for duplicate/contradictory claims.

% END_OF_VERIFIED_REPORT::ADAPTIVITY73-RAND::2026-10-22_1345
