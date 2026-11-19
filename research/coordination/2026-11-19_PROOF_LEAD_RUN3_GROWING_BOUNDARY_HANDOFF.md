# Proof lead coordination handoff, 2026-11-19
**OPEN:** P versus NP. No unrestricted superpolynomial lower bound.

**Main bridge:** source-locally-computable 3-CNF->strict-C reduction, with 15+9v+39m variables and 10+7v+31m native C clauses. Compare to Buss-Williams 2015 published SAT exclusion at (time n^1.34070, space n^0.5), Figure 8.3; Williams 2006 Corollary 2.3 explicitly treats bit-local reductions/3-SAT. **Resource auditor priority:** certify the full published SAT source-encoding->indexed fixed-width 3-CNF->C bit-level model, bounded work and both polarities. If this transfer is certified, the proposed n^1.33/sqrt(n) total strict-C decider is *already excluded* on unrestricted sources; that is not a proof of P!=NP.

**New PROVED adversarial growing-q family:** 7^(q-1) distinct nonempty strict-C projected relations of q shared variables, each defined by <=7(q-1) native clauses with disjoint private pair gadgets. They remain trivially factorable and do **not** imply a machine lower bound. D5 orbits count (5^q+5)/10; explicit R<=N^0.195 rows forces q<=log_5(10N^0.195-5). Growing-q method must handle symbolic sets.

**Verified fixtures:** C=30/125, edge-head inequality all 25 pairs, NAE and OR truth tables all eight cases each; exact seven pair masks and original-C witnesses; q=2..5 projection counts 7,49,343,2401; q=1..5 D5 orbits 1,3,13,63,313; 8-clause critical-core deletion counts 340,340,80,120,460,240,240,600 and complete witnesses replayed with independent predicate.

**Counterexample/FALSIFIED counting shortcut:** after deleting last core clause, one original variable becomes isolated; factorization counts 120 visible-variable solutions but full model count is 600. Charge all original source names even when removed clauses make them unused.

**UNSAT obligation:** FORALL z EXISTS block j FORALL private x_j NOT F_j(z,x_j); index alone is no refutation. Include source access, true/false children, all failures, proof materialization/replay/verification, output and peak workspace. Keep SAT witness search separate. Avoid high-girth/criticality transfer and unproved hardness from modular counts/local consistency.

**Reproduce:** user-facing archive T5C_ProofLead_GrowingBoundary_Run3_20261119.zip, SHA256 6a8aa0c49f0cffe9147804793d633bd24c27ce35d72ee48be2f5c4a379593637, contains lead_audit.py, independent_replay.py, JSON results, REPORT.md and SHA256SUMS. Primary report: research/agents/proof/2026-11-19_RUN3_GROWING_BOUNDARY_RELATION_FIREWALL.md.
