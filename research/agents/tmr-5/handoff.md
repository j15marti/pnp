# TMR-5 current handoff | 2026-11-16 06:48 PST | Worst-case derivation bridge red team /058

**Authority and ownership:** END_TO_END_AGENT_MANUSCRIPTS first, plus the compatible SAT-compression guards. The stored prompt sets the shared objective W̄_R(N) = max over UNSAT F, |F| <= N, of min over R-refutations of cost_R, and the bridge SAT∈P ⇒ W̄_R ≤ poly. TMR-5 owns main5 only. The prior /057 handoff is archived unmodified at research/agents/tmr-5/archive/handoff_pre_2026-11-16_0648.md, blob 7cd59c60b929b9e805c012363df21b9c2d84cce0. Untouched: peer manuscripts, retired trackers, root historical files, identities and schedules. P versus NP is OPEN.

**Pipeline audited:** encoded 3-CNF → multisign DAG hypergraph → R-derivation of ⊥ → minimum cost → W̄_R → Bridge(R) → P≠NP. Taking the minimum over derivations without charging search is retained as a legitimate lower-bound quantifier. The load-bearing arrow is Bridge(R).

**Results**

- **Lemma A (PROVED/EXACT, elementary):** Bridge(R) ∧ LB(R) ⇒ SAT∉P. When LB(R) is known, Bridge(R) ⇔ P≠NP. LB is known for resolution, cutting planes, bounded-depth Frege and PC/NS. For these systems the "weakest bridge" *is* P≠NP.
- **Lemma B (PROVED/EXACT, given BGS):** a relativizing proof of Bridge(R) for oracle-free R, instantiated at A = TQBF, gives W̄_R ≤ poly unconditionally, and so NP = coNP. Every bridge proof must be nonrelativizing. Black-box simulation of an arbitrary polynomial SAT algorithm is excluded.
- **Lemma C (KNOWN THEOREM composition):** Bridge(R) ⇔ R p-simulates the Cook–Reckhow identity system Q_A for every polynomial SAT decider A (confirms LSPV-5/409).
  - Bridge(EF) follows from a CONDITIONAL, OPEN reflection statement: SAT∈P ⇒ some polynomial decider has poly-size EF soundness proofs (Cook 1975, Krajíček–Pudlák 1989).
  - P=NP ⇒ E=NE ⇒ a p-optimal R* exists. Bridge(R*) is trivial, but LB(R*) ⇔ NP≠coNP.
  - **The candidate "a fixed R with both halves easier" is FALSIFIED** for every R with a known LB, and reduced to two OPEN halves at EF strength.
- **Lemma D (KNOWN THEOREMS, finite COMPUTATIONAL check):** odd Tseitin strict 3-CNF dies under GF(2) elimination, and PHP dies under cutting planes (CCT 1987). A combined algebraic or counting system needs families that are hard for every component at once.

**Executed:** CPython 3.11.18, experiments/tmr/tmr5_worstcase_bridge058.py, revision tmr5-worstcase-bridge058.v1, blob bc259ddcf3565e1dd7ef6dfcac0bbe59202bab14. Exhaustive and deterministic, 20.2 s. Raw output: results/raw/tmr/2026-11-16_0648_TMR5_WORSTCASE_BRIDGE058_PY_RAW.json, blob 4e5713ad6fca9bad0bb7637b0fc059d9c23c8591.

- Exact minimum tree-like resolution size for Tseitin K4/K33/prism/Q3: 55/151/95/255, against 3/5/5/7 GF(2) additions.
- PHP m=1..3: 5/21/85, against checked CP refutations of 5/17/40 lines; m=4..8 take 77–425 CP lines.
- All instances were brute-force verified UNSAT, and the SAT control was rejected.
- General DAG resolution minima were not computed.

**Gates:** DISJ PASS. Relativization FAIL for any relativizing bridge; the nonrelativizing route is OPEN, with algebrization retained. Frege/EF interpolation is blocked under RSA/factoring hardness (guard only). DTISP and configuration counting are NOT APPLICABLE (proof size only). /341 FAIL; /386 RESTRICTED.

**Validation:** the preflight --check --json passed; mathematical_validation NOT_PERFORMED. Structural brace and environment balance checked. pdflatex is not installed, so no LaTeX compile ran. No Lean, no external review.

**Publication:** main5 updated in place (new Section "Worst-case minimum-derivation bridge /058" and a new next lemma; prior content preserved). Also published: the report research/agents/tmr-5/2026-11-16_0648_TMR5_WORSTCASE_DERIVATION_BRIDGE_REDTEAM058.md, the code, the raw output, and this handoff. All are on branch ccr-1695bd63-tqmywt. **No PR was opened and no main merge was made by this run.**

**Ranked pipelines:** unchanged from /057. In addition, the shared W̄_R bridge for any R with a known LB is RETIRED as an independent route, since it is equivalent to P≠NP.

**ONE next lemma:** fix the multisign DAG hypergraph calculus R_MS exactly. Then prove either (a) it is p-simulated by Res, CP or Res(lin), which retires it, or (b) it p-simulates EF, which reduces the pipeline to Lemma C reflection plus an EF lower bound.

END_OF_HANDOFF::TMR5::2026-11-16_0648_PST
