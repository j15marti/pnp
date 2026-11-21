# charged-synthesis handoff
Updated 2026-11-21 09:24 PST.

Current report: [T5-QUOTIENT-BUDGET1](PNP_Charged_synthesis_2026-11-21_092400_Quotient_Budget_Bridge.md).
Recovery head 2c1f76d1188f30aa396b8330ee93a67f9ea0ab7e; mandatory baseline unchanged a886f3387a8676b9cc86afbf3bebf22630109d49.

PROVED/EXACT scoped interface, independent adversarial review pending: for m>=1 strict C, lattice-supported fake counts and their /10 quotients have identical conditional Shannon/average min-entropy. Multiplication/division by ten cost O(N) circuit gates and transport distinguishing advantages with additive budget loss. Same-domain raw/quotient count complexities differ by O(N). Conditional pseudoentropy-to-count lower demand B-O(N); its target-specific indistinguishability premise remains OPEN.

FALSIFIED/RETIRED only support+entropy sufficiency: one clause n=3,m=1,N=13,count30, fake uniform {30,40}, entropy1, residue advantage0 but equality advantage1/2. Off-lattice {30,31} loses entropy under floor division; m=0,n=1,count5 is outside the orbit premise.

COMPUTATIONAL: 8190 arithmetic words,1039 nonempty C-clause sets on 3..5 variables,63 rational vectors,504 transported tests. New code experiments/t5_synthesis_quotient_budget1_20261121.py and results/raw/t5_synthesis_quotient_budget1_20261121.json. Not machine timing/asymptotic evidence.

Reconciliation: Construction 358200a supplies exact 3COL decision interface and WEIGHTED count, not dynamic work; Accounting fd693f4 charges actual selector information, no compulsory demand; Discovery 3f1f284 extends typed views for FIXED d only; Bounds orbit filter is necessary not sufficient; Redteam 2c1f76d independently confirms Bounds 81c887a's Omega(N/log N) count demand, which excludes no cap. Prior terminal-closure ledger c4b8923 remains applicable. Separate witness, count-map and decision branches retained in report graph.

Same A,K,a,N: S O(N^a), physical CM O(N^(2a)), description CM O(N^(a+1)), count gates O(N^a log N). No added overlapping demands. Physical normalization wrapper O(T_A+N^2) is not exact cap-exponent preservation for a<2.

ONE next dependency: Bounds T5-QUOTIENT-PAIR1, Redteam adversarial review, Synthesis tracking. Specify actual X,V, entropy and indistinguishability beyond chosen cap; residue support and random perturbation alone fail. New report awaits independent review. Other role tasks preserved.
Fresh primary-literature and official repository searches logged; no external algorithm theorem imported. No checkout/preflight/LaTeX build, no TMR ownership/edit. P versus NP OPEN.
