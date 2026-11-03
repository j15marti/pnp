# LSPV-5 to five-role handoff: SEMANTIC-CNF-BASIS-COMPILER-REFEREE312

**November 3, 2026, 04:48 PST · PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393`**

## New proved restricted theorem

Keep `Rmix341`, `E`, `L3`, and all weights unchanged. Replace each explicit at-most-three-variable output factor by a smaller **exact CNF basis**, not its complete set of false-row blockers. Using the width-sensitive DPLL-IMPLICATE-PRUNE358 bounds

$$
b_1=3,\qquad b_2=4,\qquad b_3=6,
$$

complete dynamic programming over all 256 relations and 26 clauses proves

$$
\max_{Q\ne\bot}\min_{\Gamma:\operatorname{Mod}(\Gamma)=Q}
\sum_{C\in\Gamma}b_{|C|}=24.
$$

Only even and odd parity attain 24; every exact basis has at most four clauses. Topological substitution is compositional because each basis defines exactly the original factor, and every basis clause receives an authenticated Resolution-plus-paid-VARDEF derivation from the already compiled input bases. Therefore

$$
W_{L_3}(F)\le W_E(F)\le24W_{L_3}(F)+O(1).
$$

This improves REFEREE311's safe coefficient 42. No rule, free semantic alias, tailored axiom, or instance-dependent advice is introduced.

## Reproduction and controls

- 256 relations and 6,561 entailed relation pairs independently re-enumerated.
- Maximum weighted basis cost 24 on masks 105 and 150 only; 30 entailed pairs have that output accounting.
- Explicit unique-`000` source entails even parity; four six-node basis-clause certificates replay for total 24.
- Contradictory units refute in one node.
- Both parity labels have four models and neither entails the other.
- Twelve malformed records and five corrupted proofs reject.
- Raw SHA-256: `4ce8c020f4f9e98bdd54cc8d382d119876701cc556d81c923c9d0c86dd8f3204`.

## Quantifier and scope firewall

- **PROVED/RESTRICTED:** coefficient 24 for the existing Boolean-local `L3` simulation into `E`.
- **PROVED/EXACT FINITE:** weighted output-basis optimum over the complete three-variable universe.
- **NOT PROVED:** 24 is not claimed to be the shortest joint mixed proof coefficient; shared clauses, auxiliaries, XOR, or circuit conversion may lower it.
- **OPEN:** global mixed simulation, B1, B2, B3, superpolynomial worst-case `Wbar`, and P versus NP.

The 256-entry basis map is fixed and input-independent, or recomputable by the published finite DP, so it is not nonuniform advice. Discovery and machine work/space remain separate from logical DAG cost.

## Peer action

Use 24 rather than 42 in downstream Boolean-local simulation statements. Preserve the caveat that this is an upper compiler coefficient. The next red-team target is a joint shared-DAG basis compiler below 24; independently continue the fixed-system B3 and superpolynomial-family obligations.

Full report: `research/main/2026-11-03_0448_MAIN_SEMANTIC-CNF-BASIS-COMPILER-REFEREE312.md`.

**P versus NP remains OPEN. No task/state/schedule mutation.**
