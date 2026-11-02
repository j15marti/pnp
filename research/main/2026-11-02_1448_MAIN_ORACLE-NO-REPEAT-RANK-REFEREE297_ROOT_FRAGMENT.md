% BEGIN LSPV5 ORACLE-NO-REPEAT-RANK-REFEREE297 EXEC
\textbf{Newest noisy-oracle no-repeat referee (REFEREE297).}
For a unique satisfying assignment and independent effective correct-bit
probability \(q\), order all assignments by successive product-weighted
sampling without replacement.  Exponential-clock analysis gives the exact
expected target rank
\[
 1+\sum_{d=1}^n{n\choose d}
 \frac{((1-q)/q)^d}{1+((1-q)/q)^d}
\]
and the bounds
\[
 \frac{q^{-n}+1}{2}\le \mathbb E R\le q^{-n}.
\]
Thus never repeating an assignment improves iid witness sampling by at most a
factor of two; every fixed \(q<1\), including \(99.5\%\), remains exponential.
Polynomial expected rank needs \(q=1-O(\log n/n)\), plus polynomial paid
acquisition of witness-correlated advice.  UNSAT has no correct witness bits.
The unit-CNF controls show source-aware propagation and Resolution can be
linear/one-node even when blind sampling is exponential, so this is a
\textbf{PROVED/EXACT SAMPLING THEOREM}, not a \(W_R\) lower bound or B3.
Report:
\path{research/main/2026-11-02_1448_MAIN_ORACLE-NO-REPEAT-RANK-REFEREE297.md}.
B1, global B2, B3 and P versus NP remain \OPEN.
% END LSPV5 ORACLE-NO-REPEAT-RANK-REFEREE297 EXEC

