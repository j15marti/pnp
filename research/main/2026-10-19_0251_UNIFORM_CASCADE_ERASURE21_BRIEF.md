# UNIFORM-CASCADE-ERASURE21 (2026-10-19 02:51 KST)
Status: Scoped exact theorem, independent audit pending. P versus NP OPEN.

For full-rank block-parity maps R1:F2^N->F2^b1 and R2:F2^b1->F2^b2 (b2<b1), choose sparse right inverses H,J and source X=HJ(U_b2). Every source table has weight <=b2 and circuit size O(b2 log N). Stage one distinguishes X from uniform with TV=1-2^(b2-b1), yet R2R1(X) and R2R1(U_N) are both exactly uniform. Online balanced pair encoding (r, r XOR v) keeps each uniform baseline *exactly* uniform without fixing the issue.

Finite exhaustive audit: N=16,b1=8,b2=4. Stage-one TV=15/16; stage-two TV=0, both before and after balanced encoding. 65,536 second-stage cases checked, 0 failures.

This toy source is NOT CHMY's PRG. First-stage range support plus a uniform-to-uniform interface is insufficient to justify cofinal advantage. CHMY-specific typed advantage preservation and a jointly uniform NP/PH label are OPEN. Next lemma CHMY-ADVANTAGE-INVARIANT22. See local complete report/code/JSON. P versus NP OPEN.
