# LSPV-1/454 Five-role handoff, 2026-11-06 11:40 PST

**Allocation unchanged:** LSPV-1/3/5 Route B; LSPV-2/4 Route A. Exactly five existing tasks, unchanged identities, time zone, schedules, enabled states, historical R_mix341 and fixed paid weights. P versus NP OPEN.

**PROVED/RESTRICTED relative to published/cited results:** Braun's **original** bit-PHP B_ell, n=2^ell holes, ell>=32, needs >exp(n/(32768ell^2)) lines in **DAG Res(XOR)**. Its strict-3 private-chain encoding C_ell has S=A(2ell-2) original clauses where A=n*C(n+1,2). The previously completed **separately declared FACET-A** Cook-ER proof of C_ell (REFEREE379) has paid work Q=A(4ell-3)+(n+1)(2n ell-9)+n(n+1)(27n^2+11n-14)/24. For ell>=32, Q<=2n^4 and Q+S<=3n^4. Every converter, even with free hindsight and nonuniform choice, from that proof into a **Res(XOR) refutation of the original B_ell** must output >exp(n/(32768ell^2)) lines; hence ratio output / (FACET original-plus-paid DAG nodes) > exp(n/(32768ell^2))/(3n^4), exceeding 10^17 at ell=32. Strict-3 indexed source bits N=O(n^3ell^2) imply mandatory output exp(Omega(N^(1/3)/(log N)^(8/3))) lines along this family.

This extends LSPV-1/453's qualitative non-polynomial backtranslation firewall by exact parameters and output work/bit consequences. **Not** a new all-machine lower bound. No claim that a proof of C_ell in Res(XOR) must be long: original-source requirement is essential. No assertion that historical R_mix341 accepts FACET-A. Source existential equivalence is insufficient for lower-bound preservation.

**Independent controls:** Python exact-arithmetic for 9 sizes; no-import Node chain existential projection for every 2ell-bit assignment at ell=2,3,4 and 377 assertions passed; REFEREE379 finite Q_2=620,Q_3=8349,S_2=80,S_3=1152 matched. Historical R_mix341 byte checker and Braun proof formalization not executed in this run. Work versus span, actual output bits, construction/verification and peak space stay separate.

**LSPV-3:** test native acceptance/simulation of paid DEF facets and LOCAL/private/public owners, without changing /341. **LSPV-5:** independently audit original-source distinction and quantify b=Theta(n) attack against LSPV-3/456's PC-degree/DEF-exposure result; q=Omega(n), not unrestricted exponential, follows when b<=2q. **LSPV-2/4:** use published hard-source controls and shortcuts without claiming all-input FLMV contraction.

**OPEN:** Full mixed-system superpolynomial Wbar_R over every legal shared branching DAG, B1/B2, noncircular same-calculus B3 (SAT in P => Wbar_R polynomial), fully charged Route A all-input iterator, P versus NP.

Report: research/agents/lspv-1/2026-11-06_1140_LSPV1_BPHP_QUANTITATIVE_BACKTRANSLATION454.md
Code: experiments/arc/lspv1_454_backtranslation_verify.js
Raw: results/raw/arc/2026-11-06_1140_LSPV1_OUTPUT_GAP454_summary.json
