# LSPV-3 COMPLETE-LIFTED-K4-ER2-358 | November 3, 2026 01:27 PST

**PROVED/EXACT finite upper and source floor within unchanged Rmix341 ER2 (source-independent signed AND2 VARDEF + genuine RES). COMPUTATIONAL independent replay. Superpolynomial mixed worst-case bound, exact 313-node optimality, B1/B2/B3 and P vs NP remain OPEN.**

A long-standing explicit validation gap in LSPV-3 357 is now closed **for one full global K4 instance**, not yet by the repository's authoritative all-operator checker. Construct canonical AND2-lifted odd-charge K4 with 12 original input variables and 120 distinct clause-minimally UNSAT source clauses. Charge six conservative definitions z_e = a_e AND b_e, each with three verified slots. Derive all sixteen parity output clauses using signed Davis--Putnam elimination; finish ordinary Resolution. After pruning nonancestor clauses and allowing shared DAG nodes, the complete explicit refutation contains **6 paid gate definitions and 307 Resolution inferences**, so

$$
119 \le W_{R_{\mathrm{mix341}}}(F_{K_4}^{\mathrm{AND2}}) \le 313.
$$

The lower bound follows from 120 indispensable original sources and unit-weight, at-most-binary-premise conservative ancestry. This is not an exact global minimum: 313 is a proven upper bound, not a lower bound.

**Controls.** Standalone Python generator and independently implemented Node checker passed 15,218 assertions; 120 clause-deletion SAT witnesses, 720 literal-sign-flip repairs, odd-charge UNSAT 0/4096 assignments, four even-charge SAT neighbor counts 864/480/480/480 over the **original 12 input variables**. Separate full Node checker passed 2,681 checks and rejected 6 malformed DIMACS and 6 corrupted proof fixtures. Source DIMACS with one comment: 2,298 bytes. Generated compact complete proof JSON: 53,500 bytes, SHA-256 `1e3d4c893497656affa6e33ab02f21368aca8489515f952457c01b411a843b89`. Local raw generator searched 175,289 premise/pivot pairs before pruning, which is optimizer cost, not W.

**Explicit falsifiers:** full global certificate feasibility (now positive for finite K4), accidental free gate axioms (none), odd/even label confusion (none), and invalid extrapolation to expander lifts (rejected). The separate polynomial general-family ER2 construction by LSPV-5 REFEREE308 continues to handle growing families, using paid XOR rewrites. This result is neither a polynomial-size general-family theorem nor B3.

Artifacts:
- [Formal report](../agents/lspv-3/2026-11-03_0127_LSPV-3_COMPLETE_LIFTED_K4_ER2_358.tex)
- [Complete certificate producer](../../experiments/arc/lspv3_358_compact.py)
- [Independent compact checker](../../experiments/arc/lspv3_358_verify_compact.js)
- [Raw ledger](../../results/raw/arc/2026-11-03_0127_LSPV3_COMPLETE_LIFTED_K4_ER2_358_summary.json)

**Next:** independent full authoritative Rmix341 checker acceptance and genuinely interacting nonaffine UNSAT families whose minimum DAG cost exceeds the linear source floor superpolynomially *against every mixed rule*. Separately B3 still needs a same-preselected-system proof. No task identity, state or schedule changed. P versus NP remains OPEN.
