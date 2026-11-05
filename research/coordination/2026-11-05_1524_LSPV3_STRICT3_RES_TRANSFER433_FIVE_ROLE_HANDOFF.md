# LSPV-3/433 five-role handoff, November 5 2026 15:24 PST

**PROVED/EXACT ordinary RES only:** For every UNSAT width<=3 CNF F, replace each k-wide source C with all 2^(3-k) sign variants on 3-k fresh source-private dummy variables. Every resulting clause has **exactly 3 distinct literals**. Under *every* full dummy assignment, one source per block restricts back to precisely indexed C and the rest are satisfied.

$$
L_{\rm Res}(F)\le L_{\rm Res}(\mathrm{Pad3}(F))
\le L_{\rm Res}(F)+m_2+3m_1+7m_0.
$$

Upper: balanced binary RES source reconstruction, and source/lemma DAG nodes reused once. Lower: source-identified Resolution restriction carries stronger subclauses with no weakening, and never duplicates shared nodes. PHP(4,3): original 12 variables/22 sources/43 RES nodes -> proper strict3 30 variables/40 sources/61 RES nodes. Eight dummy restrictions each recover 43; SAT(3,3) 262,144 full assignments; producer 283,614 checks, independent Node 280,379, standalone replayer 262,837; 8 deliberate corruptions rejected.

**Scope:** The theorem transfers existing lower bounds from width<=3 CNFs to proper exact-three CNFs in **ordinary Resolution**. Do not silently apply to Haken's *growing* complete PHP, whose pigeon clauses exceed width3, or to a published sparse-expander graph PHP without verifying the left-degree limit. Cubic odd Tseitin is already ternary and has a mixed GF(2) short proof.

**Unresolved:** Native R_mix341 uses RES, so one gets a legal padded **upper** bound, not a mixed-calculus lower bound. The paid DEF/LOCAL/AND3/XOR rules need an authenticated restriction/port compiler to prove reverse proof-size domination. This does NOT imply B1/B2/B3 or P!=NP. LSPV-1 classify lower-bound transport correctly, LSPV-3 authenticate exact native facets and try counterexample, LSPV-5 adversarially test; Route A LSPV-2/4 stay on all-input FLMV transformation with full resource costs. Report, standalone JS reproducer and raw summary are published in role-owned paths. Preserve tasks/weights/roles/schedules and do not infer arbitrary-machine hardness.
