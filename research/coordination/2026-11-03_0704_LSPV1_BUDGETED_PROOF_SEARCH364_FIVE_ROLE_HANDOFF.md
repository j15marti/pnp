# LSPV-1 to five-role handoff: BUDGETED-PROOF-SEARCH364

**November 3, 2026, 07:04 PST. No changes to task IDs, role ownership, schedule, enabled state, calculus or weights. P versus NP OPEN.**

## Scope and mathematical result

Use the same source-authenticated, binary-premise, unit-inference-node mixed calculus Rmix341, including paid signed source-independent VARDEF and authenticated RES/AND3/XOR/LOCAL-CONVERT. Under the explicit bounded-output normal-form proof-evidence hypothesis of LSPV-4 NODE-EVIDENCE-DOMINATION342 (a q-node refutation has a certificate of at most polynomial size in encoded source bits N plus q; checking polynomial), the unary-budget language

$$
\mathcal B_R=\{(\operatorname{enc}(F),1^b):F\text{ valid and }W_R(F)\le b\}
$$

is in NP unconditionally. Therefore, **if SAT is in P**, there is a polynomial-in-(N+b) uniform procedure deciding this language, retrieving an authentic shortest R refutation when one exists in budget b, and independently validating the certificate. Standard Cook-Levin reduction plus SAT search-to-decision self-reduction provides witness bits; binary-searching the integer budget provides exact W_R(F).

**This is a KNOWN THEOREM / project-specific quantitative application, not a new general complexity theorem.** It does not assume that a candidate decider's rejection trace is a sound proof, and it does not derive a polynomial budget from SAT in P. The native printed proof, discovery/search time, verifier cost, input parsing/index access, all-phase peak space and DAG node count are separate.

**Conditional effective-extraction corollary:** SAT in P **and B3 for the same fixed R** imply a P-time total proof-producing SAT solver (SAT assignment, UNSAT charged R-refutation, malformed reject). A polynomial-time independently checked proof-producing solver conversely implies a polynomial worst-case Wbar_R. This does **not** settle B3. Under the antecedent SAT in P, B3 also implies B1 and B2 for *every* correct total algorithm through W_R(F)<=C(N+1)^k; this is a quantifier audit, not a proof of the antecedent or its missing consequence.

## Four falsifiers

1. A binary budget gives time polynomial in log b: **REJECTED**, only polynomial in unary b is proved.
2. Any program's rejecting computation is a valid UNSAT proof: **REJECTED**, only fixed-R verified certificates count.
3. Bare SAT in P supplies the polynomial proof budget: **OPEN/MISSING**; the algorithm can correctly answer NO at every polynomial budget for an UNSAT formula if B3 fails.
4. Finite Resolution optima are full mixed optima: **REJECTED**, experimental optimum claims are Resolution-only.

## Independently executable finite controls

Seven small signed fixtures with exact Resolution costs 0,1,2,3, and 3 SAT controls (model counts 2,1,1); independent exhaustive smaller-budget rejection on each nonzero optimum. Odd/even K4 parity models 0/8; five malformed inputs rejected; three corrupted proof DAGs rejected. Python-free standalone Node producer ran 31 internal checks; separately written Node verifier ran 33; the exact GitHub-readback sources were also re-executed in isolated JS with matching outputs. These finite tests do **not** implement polynomial general SAT nor certify full mixed minima.

- [Formal owned report](../agents/lspv-1/2026-11-03_0704_LSPV-1_BUDGETED_PROOF_SEARCH364.tex)
- [Reproducible producer](../../experiments/arc/lspv1_364_budgeted_min_producer.js)
- [Independent verifier](../../experiments/arc/lspv1_364_budgeted_min_independent_verify.js)
- [Raw cases/proof DAGs](../../results/raw/arc/2026-11-03_0704_LSPV1_BUDGETED_R_PROOF_SEARCH364.json)
- [Independent pass ledger](../../results/raw/arc/2026-11-03_0704_LSPV1_BUDGETED_R_PROOF_SEARCH364_independent.json)

## Allocation and next gaps

LSPV-1: Work on actual B3 antecedent-to-budget implication, not merely this conditional extraction. LSPV-2: Preserve full canonical source/proof checker and budget witness normalization. LSPV-3: Seek a growing nonaffine mixed-hard family; do not use short proof normalization as a lower bound. LSPV-4: Resolve exact arbitrary circuit-valued LOCAL-CONVERT syntax and the all-phase charged acquisition ledger. LSPV-5: Red-team the unary-vs-binary budget, proof-evidence normal form, source checking, and use of conditional SAT algorithm. No other tasks were edited.

Source history: Nov 2 shared directive, issue #3, AGENTS.md, CODEX.md, pnp-research skill, LSPV-1 357/360/361B/362/363, LSPV-4 NODE-EVIDENCE-DOMINATION342 and recent LOCAL-CONVERT controls, LSPV-5 REFEREE314, older FP/FNP search spine. Primary literature Cook--Levin, Cook--Reckhow, Atserias--Müller 2020, Pich--Santhanam 2026; github.com/openai proof checker search provided no adopted implementation. Repository-local complete lint could not run because container cannot resolve GitHub DNS; standalone Node controls and GitHub exact readbacks succeeded.

**Open:** B1/B2/B3, superpolynomial worst-case Wbar_Rmix341, P versus NP.
