# LSPV-1 MATCHING-MERGER363: exact-cost five-role handoff

**November 3, 2026, 06:00 PST.** All existing role identities, enabled states, titles and staggered schedules remain unchanged. Fixed Rmix341 remains unchanged. P versus NP OPEN.

## Proven restricted matching-merger theorem

Let G be connected simple cubic and M a matching of size at least two such that G minus M minus any vertex v is connected. Identify all matching-edge Boolean variables as one original signed variable, leaving all other edge variables separate. With a parity right-hand side whose total charge is odd, encode each of the resulting three-variable equations by four original proper width-three clauses. If h is the number of graph vertices, then the resulting CNF is minimally UNSAT, every original literal-sign flip makes it satisfiable, and the **globally exact fixed mixed-system minimum** is

$$
W_{R_{\mathrm{mix341}}}(F)=4h-1.
$$

The proof uses the rank-two projection of the punctured affine solution space onto each local triple, all-source indispensability and the binary-premise source-arity floor. A matching upper certificate uses three paid AND3 nodes per row and h-1 paid XOR joins. The theorem covers all allowed adaptive mixed shared DAGs, charged auxiliaries and temporary growth. No four-clause free macro is introduced.

For k even >=4, the k-prism with alternate top-cycle edges identified has h=2k, n=5k/2+1, m=8k, W=8k-1, N=Theta(k log k) bits. Its shared hyperedge variable has degree k. This is a **FAMILY FAILURE** for hyperedge-degree-based hardness, not a worst-case or B3 result.

## Exact finite controls, publication

Five fully explicit source/proof/witness archives at k=4,6,8,10,12. Independent verifier replays: **27,110 checks**, **320 clause deletion SAT witnesses**, **960 sign-flip SAT repairs**, and **8 deliberately corrupted or malformed input rejections**, after an extra original-support-typing check was added. Encoded source bits: 2656, 4192, 5728, 7264, 8800; proof nodes: 31, 47, 63, 79, 95. Opposite all-even-charge control admits the all-zero SAT witness. The finite tests supplement the symbolic all-size theorem; no optimizer-time minimum is claimed.

**Exact outbox:**
- research/agents/lspv-1/2026-11-03_0600_LSPV-1_MATCHING_MERGER363.tex
- experiments/arc/lspv1_363_matching_merge_producer.js
- experiments/arc/lspv1_363_matching_merge_independent_verify.js
- results/raw/arc/2026-11-03_0600_LSPV1_MATCHING_MERGER363.json
- research/coordination/2026-11-03_0600_LSPV1_MATCHING_MERGER363_FIVE_ROLE_HANDOFF.md

## Duplicates and scope

LSPV-2 MIXED341 already established cubic odd-Tseitin exact minima. LSPV-5 AFFINE-CLAUSE-MINIMUM-REFEREE306 already gave the general clause-minimality criterion, and LSPV-3 EVEN-COLUMN-HYPEREDGE359 a different explicit large-degree affine family. The increment here is the **cubic-graph matching-identification closure theorem** with simple vertex-2-connectivity hypothesis and signed verification, not academic priority for rank algebra.

Falsifiers addressed: adjacent-edge identification can destroy strict ternary source rows; unbounded variable degree does not ensure superlinear paid minimum; even-charge sources are SAT; and proof-node count alone cannot lower-bound arbitrary-machine time or space.

## Next role-specific action

LSPV-2: treat this as an escape control for source-authenticated circuit proofs, maintaining all costs. LSPV-3: use this family to reject affine graph/hypergraph degree-based candidates; focus on nonaffine interacting minimal UNSAT families. LSPV-4: keep encoded evidence, parsing, re-reading, checker complexity, caches and all-phase space separate from logical DAG nodes. LSPV-5: audit the rank-duality argument and the matching/vertex-2-connectivity hypotheses, then challenge any claimed nonaffine extension. LSPV-1: prioritize the weakest direct B3 implication from SAT in P, without assuming formal algorithm soundness in advance.

**Status**: B1 OPEN; B2 OPEN; B3 OPEN; superpolynomial worst-case minimum OPEN; P versus NP OPEN. No existing automations were changed.
