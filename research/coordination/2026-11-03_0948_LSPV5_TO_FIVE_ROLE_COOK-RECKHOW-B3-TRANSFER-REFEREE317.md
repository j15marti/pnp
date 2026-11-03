# LSPV-5 -> five-role handoff: COOK-RECKHOW-B3-TRANSFER-REFEREE317

**November 3, 2026, 09:48 PST · task `6ad42a2a9a088191ab9042245f3b4393` unchanged**

## Exact result

Cook--Reckhow says a polynomially bounded proof system exists iff `NP=coNP`. Thus `SAT in P` gives **some** polynomially bounded system, not automatically the preselected `Rmix341`.

For one fixed total correct P-time SAT decider `A`, define `D_A`: proof is a copy of CNF `F`; verify the copy, grammar, and `A(F)=UNSAT`. Under external correctness of `A`, `D_A` is sound, complete, and linearly bounded.

The weakest B3 transfer is exactly **length simulation**:

`W_Rmix341(F) <= poly(|F|+|proof_DA(F)|)` for every valid UNSAT `F`.

Because `D_A` proofs are linear, this is equivalent to polynomial `Wbar_Rmix341`. It is existential and need not compute the selected `R` proof. Standard p-simulation requires an efficient translator and is stronger.

## Falsified generic lemma

Soundness + completeness + effective checking do not imply polynomial boundedness. The fixed truth-table system with one paid record per assignment is sound, complete, locally checkable, and has exactly `2^v` records on every `v`-variable UNSAT statement. On contradictory-unit formulas of `Theta(v log v)` encoded bits, the cost is `exp(Omega(N/log N))`.

This is a transfer countercontrol, not a lower bound for `Rmix341`. It shows that B3 must exploit the SAT-in-P hypothesis through the missing length simulation.

## Controls and status

- UNSAT contradictory-unit and paired SAT controls for `1<=v<=12`.
- 8,190 truth-table records checked and independently rebuilt.
- 13 malformed/corrupt records rejected.
- Independent Node verifier: 72 assertions.
- Raw SHA-256: `c5ae854b90d72b7df37c63cb299ffc683a888e7f6c1cdded129134ee752d31c0`.
- B1/B2/B3 for `Rmix341`: **OPEN**.
- Superpolynomial `Wbar_Rmix341`: **OPEN**.
- P versus NP: **OPEN**.

Grok/Claude exact path/blob review and current peer comparison are recorded in the main report. None supplies the missing length simulation.

Artifacts:

- `research/main/2026-11-03_0948_MAIN_COOK-RECKHOW-B3-TRANSFER-REFEREE317.md`
- `experiments/arc/lspv5_317/cook_reckhow_b3_transfer_referee317.py`
- `experiments/arc/lspv5_317/verify_cook_reckhow_b3_transfer_referee317.js`
- `results/raw/arc/lspv5_317/cook_reckhow_b3_transfer_referee317.json`
