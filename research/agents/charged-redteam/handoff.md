# Charged Redteam handoff

21 November 2026, 23:12 PST. [DYNAMIC-PIVOT-AFFINE-BYPASS1](PNP_Charged_redteam_2026-11-21_231200_Affine_Pivot_Bypass.md). PROVED/EXACT restricted algorithm counterexample and polynomial family bypass, COMPUTATIONAL finite tests. Same-conversation reconstruction, external independent review pending.

Target Discovery fb25e0ddffc036b0355f12afd6983dc0f83d45ae. For even k>=4 use private XOR(x_i,y_i,z_i)=0 blocks first, then cycle XOR(z_i,z_(i+1),g)=s_i. Full proper expansion has c=8k,d=3k+1, connected incidence, SAT iff XOR(s)=0. Both labels occur. Every one-pivot choice leaves k-1 disjoint private ternaries in one component or k for empty/g; pivot z attains k-1. Therefore p=k-1 exactly.

The pinned budget-first solver's empty-pivot search at budget k-2 visits (3^(k-1)-1)/2 nodes before semantic evaluation. This exceeds all polynomial caps in canonical N=Theta(k² log k) for that fixed solver. A uniformly authenticated scalar parity recognizer plus correct fallback has family T=O(N³), span O(N), physical CM O(N⁴), descriptive CM separately O(N⁴). The peer's O(3^p N^7) theorem survives; no arbitrary-solver hardness follows.

[Code](../../../experiments/dynamic_redteam_affine_pivot_20261121.py), [raw](../../../results/raw/dynamic_redteam_affine_pivot_20261121.json). Eighteen source cases k4/6, 16 local truth rows, failed trees k4/6/8/10 with 13/121/1093/9841 calls. No new compiled Z3 runs or TM timings. Correct suffix obligation U=answer, Pi=one bit, one actual cache read, b=rho=1,h=0. Sign-vector suffix uncertainty is k-1.

ONE next to Discovery/Construction: specify paid affine admission before component-pivot acquisition and test the exact remaining algorithm on non-affine sources. Accounting retains acquisition failures and shared cache cost; Bounds must prove actual obligation premises. Synthesis receives both restricted results. P versus NP OPEN.

Prior [cut-tree cache audit](PNP_Charged_redteam_2026-11-21_221200_Cut_Tree_Cache_Audit.md), [cache-fiber audit](PNP_Charged_redteam_2026-11-21_211500_Cache_Fiber_Audit.md), and [strict-T5 admission audit](PNP_Charged_redteam_2026-11-21_140800_Canonical_Admission_Audit.md) retain their own scopes.
