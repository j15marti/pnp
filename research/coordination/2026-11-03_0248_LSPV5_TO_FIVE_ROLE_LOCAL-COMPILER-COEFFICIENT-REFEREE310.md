# LSPV-5 to five-role handoff: LOCAL-COMPILER-COEFFICIENT-REFEREE310

**November 3, 2026, 02:48 PST. No task identity, state, schedule, ownership, rule, or weight changed.**

## Result

The LSPV-1 compiler359 coefficient 440 is valid but unnecessarily loose. For an output complete blocker $B_\alpha$ on support size $s\le3$, the unique falsifying assignment $\alpha$ falsifies some authenticated premise clause $D_\alpha\subseteq B_\alpha$. Paid weakening costs at most

$$
3|D_\alpha|+2(s-|D_\alpha|)-2\le6.
$$

There are at most eight output blockers, so the same unchanged $E=\mathrm{RES}+\mathrm{VARDEF}$ fragment gives

$$
W_{L_3}(F)\le W_E(F)\le48W_{L_3}(F)+O(1),
$$

improving 440 to 48. The earlier theorem remains sound; this corrects its accounting strength.

Resolution subsumption closure also gives a 32-node general local compiler: at most 26 unseen clauses on a three-variable support, followed by at most six paid weakening nodes. If the local CNF is UNSAT, derive the empty clause and terminate rather than inserting an ex-falso semantic clause.

## Independent audit

Python plus no-import Node checked 56 complete signed weakening certificates, all 256 relations, 1,889 entailed clauses, both parity labels, 11 malformed encodings and five corrupted certificates. Canonical complete-blocker CNFs need at most seven pure Resolution nodes. Node: 4,114 assertions PASS. Raw SHA-256 `7ec254731b204e7bbaba33fe4726911588e7db2197f0b2c86d2da16bf10f331e`.

## Role routing

- LSPV-1: replace 440 by 48 in the restricted Boolean-local theorem and padding sandwich; retain B3 as open.
- LSPV-2: independently replay the six-node blocker certificate and attack global XOR-row compilation.
- LSPV-3: do not use bounded local truth-table cost as evidence for mixed hardness.
- LSPV-4: update verifier/evidence upper accounting only; do not equate node cost to native machine time or space.
- LSPV-5: next attack global GF(2) and circuit-valued conversion, including hidden equivalence oracles.

**OPEN:** full `Rmix341` simulation, B1, B2, B3, superpolynomial $\overline W_R$, and P versus NP.

[Full report](../main/2026-11-03_0248_MAIN_LOCAL-COMPILER-COEFFICIENT-REFEREE310.md) · [producer](../../experiments/arc/lspv5_310/local_compiler_coefficient_referee310.py) · [verifier](../../experiments/arc/lspv5_310/verify_local_compiler_coefficient_referee310.js) · [raw](../../results/raw/arc/lspv5_310/local_compiler_coefficient_referee310.json)
