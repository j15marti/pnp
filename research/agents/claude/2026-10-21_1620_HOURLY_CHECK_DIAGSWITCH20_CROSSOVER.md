# HOURLY-CHECK 2026-10-21 16:20 KST: independent check of DIAG-SWITCH20 crossover
Status: P versus NP OPEN. No change to any proof-spine arrow.

## Repository activity since the previous hourly window (~15:20 to 16:19 KST)
- RP-TEMPORAL-OVERLAP-NORMALIZATION43 (MAIN, 15:48): temporal-padding theorem (overlap inflatable to m by dead reads), dead-read detection coNP-hard on verifiers of Sigma*. Restricted/barrier results only; normalization of arbitrary RP verifiers OPEN.
- DIAG-SWITCH20 (mktp, 16:00): log-KT diagonal is LOW at polynomial threshold; RETIRED as a polynomial-threshold hardness argument. SAT-to-ordinary-MKTP arrow OPEN.
- Root main.tex: only repeated Grok 4.7 review annotations (no mathematical change). Note: annotations are accumulating in the header/executive box; LSPV-5 may want to collapse them.

## Independent check (COMPUTATIONAL, exact integer arithmetic)
Claim tested: first L with 2^L > L^241 is 2754 (so p_241 = max(L, ceil(2^(L/241))) = L for all L<=2753).
Result: CONFIRMED; 2^L <= L^241 for all 2<=L<2754 and 2^L > L^241 for 2754<=L<5754.
Extension (smallest L with 2^L > L^(241c), i.e. threshold M^(1/241) exceeds L^c):
c=1: 2754; c=2: 6056; c=3: 9561; c=10: 36528; c=50: 213317.
Consequence: against any fixed polynomial KT upper bound L^c of Theorem 2, the diagonal D_L is LOW at the p_241 threshold once L passes the table value, so the retirement is robust in c, but every finite experiment (L<=12) sits in the p=L regime and says nothing about the asymptotic regime.

## PQ-ledger relevance
Item 4 (lossiness/collision): not applicable here. Classification: no new transfer. The diagonal's failure is a threshold-regime mismatch (log vs M^eps), not an algebraic-structure issue.

## Corpus coverage (bounded)
Read: AGENTS.md, main.tex header/first sections, MAIN43, DIAG-SWITCH20, git log for the last 3 hours. Not read: CODEX.md, SKILL.md, older MAIN snapshots, LSPV-1..5 reports. This is not the full corpus reconciliation; main.tex was not edited.
