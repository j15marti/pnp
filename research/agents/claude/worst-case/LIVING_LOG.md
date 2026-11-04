# Worst-case derivation-complexity living log (Claude role)
Target: Wbar_R(N)=max_{F UNSAT,|F|<=N} min_{pi:F|-_R bot} cost_R(pi); bridge B3: SAT in P => Wbar_R <= poly. P vs NP OPEN.

| Date | Entry | Status |
|---|---|---|
| 2026-11-04 | B3-VACUITY-0001: if LB_R is known (Resolution etc.), B3_R <=> P!=NP; B3 informative only for open-LB systems (EF/ER-strength R_mix341); B3 follows from p-optimality of R or provable correctness of a SAT algorithm (conjecturally false). New gate: any B3 transport lemma must FAIL for Resolution/PHP. | PROVED/EXACT (elementary) |

Open arrows: LB for R_mix341; B3 for R_mix341 (non-generic proof needed); RT/SC of LSPV-1/353.
Next: apply the Resolution separating gate to RT/SC; check which R_mix341 rules (XOR, DEF) a PHP-style restriction argument would survive.
