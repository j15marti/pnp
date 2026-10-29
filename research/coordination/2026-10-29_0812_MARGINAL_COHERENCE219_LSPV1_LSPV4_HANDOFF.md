# LSPV-2 MARGINAL-COHERENCE219
29 October 2026. PROVED/EXACT restricted, independent review pending. P vs NP OPEN.

A two-state signed puncture splice has modules E={(0,0),(1,1)}, X={(0,1),(1,0)}, and B={(0,0)}. All X yields connected UNSAT U_k; changing any one X to E yields connected SAT S_{k,j}. For every k>=1: n=7k+9, m=9k+13, proper 3CNF, maximum variable incidence five, identical unsigned scopes, identical per-variable signed incidence and identical individual one-port marginals. Exactly four sign bits differ. NOT strict exact-(2,2).

Indexed bit-probe promise P_k={U_k,S_{k,j}: j in [k]}: worst-case Q_+=Q_-=k for the same deterministic program. It is input acquisition only, not post-acquisition hardness. A complete authenticating syntactic recognizer outputs one 54-bit YES or 340-bit NO ordinary 3CNF child. For k>=4 this is <=N^(3/4), with direct bounded bases. This is a restricted easy class, not a general SAT contraction.

COMPUTATIONAL: 131072 exhaustive assignments k=1, 47042 independent DPLL calls k<=8, nine sizes through k=64, 44 malformed one-bit controls, bit-precise output and same-source-profile verifications, identical rerun JSON. Library Connected_Interface_Audit.zip rerun passed exactly 4680 boundary subsets, 7191 local searches, 139 SAT comparisons. Its static coverage bound is not a time lower bound.

Duplication: LSPV-3 GUARDED90 had NP-hard singleton projection, LSPV-3 AFFINE147 had five-occurrence affine profile reduction, LSPV-5 MARGINAL-PARITY192 had parity marginal failure. The present scoped two-port splice and exact answer-side k-query result are the additions. Original LSPV-2 SIGNED-PUNCTURE-PROFILE218 remains valid.

The complete expanded LaTeX, Python, raw JSON, bibliography and PDF are in this run's downloadable reproducibility package. GitHub concise report is a self-contained mathematical proof; experimental Python and raw must be separately synchronized if GitHub upload is blocked. Root ownership safeguards unchanged.