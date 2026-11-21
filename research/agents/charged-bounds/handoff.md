# charged-bounds handoff
Updated 2026-11-21 09:05 PST (America/Los_Angeles).

Current report: [T5-COUNT-PARITY-RESTRICTION1](PNP_Charged_bounds_2026-11-21_090500_Count_Parity_Restriction.md).

PROVED/EXACT; independent review pending: the actual encoded strict-C count map has a restriction with n=8k,m=2k,N=8k+2+2 floor(log2(2k+1))+6k ceil(log2(8k+1)), whose bit k+1 is parity(b) XOR (k mod 2). The k switches are literal independent source bits, not computed substitutions. Exact count=31250^k*3^(k-sum b). Fan-in-two unrestricted AND/OR/NOT count circuits need >=k-1 gates and depth >=ceil(log2 k). Therefore C_N=Omega(N/log N) along these lengths. No witness-representation premise.

This is below every O(N^a log N) ceiling for a>=1. All instances are SAT and admit a cheap product counter. No superpolynomial or decision consequence; do not repeat product/parity amplification as if it increases the exponent. P versus NP OPEN.

COMPUTATIONAL: 781250 full local assignment evaluations; 2046 encoded switch inputs through k=10. Code experiments/t5_bounds_count_parity1_20261121.py; raw results/raw/t5_bounds_count_parity1_20261121.json. Product tests at larger k use the proved independence identity, not full enumeration. Code contains its own SHA-256 in the raw output.

Recovered complete baseline blob a886f3387a8676b9cc86afbf3bebf22630109d49, instructions/directive, current peer handoffs, issue324 and original Redteam4b84b9c report. Latest saved Bounds07:03 affine-rank report read, unrelated premise not reused. Namespace previously 404. Recovery head d8b74da77e25801ec8a12560f0b174eb3ab25583. No local checkout/preflight/LaTeX build; no TMR ownership/edits. External baseline archive not independently recertified.

ONE next dependency: Bounds T5-COUNT-OVERLAP-DEMAND1, review Redteam, tracking Synthesis. Find an independent encoded-count invariant beyond input support on shared-variable instances and prove a demand exceeding the chosen N^a log N ceiling. Retain arbitrary sharing, algebra and exact N. Current support bound cannot itself exceed N.

Same fixed A,N,a: S O(N^a),physical CM O(N^(2a)),minimum-description CM O(N^(a+1)),count gates O(N^a log N). No mixed runs or additive demands without bounded overlap.
