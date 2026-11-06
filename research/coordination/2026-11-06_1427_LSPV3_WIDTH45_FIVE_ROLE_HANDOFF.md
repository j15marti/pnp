# LSPV-3/459 five-role handoff | November 6, 2026 14:27 PST

**PROVED/RESTRICTED and COMPUTATIONAL; P vs NP OPEN.** Start from the already published Chvátal–Szemerédi/Pang iid strict-three-CNF distribution with m=8n indexed source clauses. Previous LSPV-3/458 proved second-generation **width<=3 throughout** RES is absent with probability 1-O(1/n). That restriction cannot be generalized: legal *first* width-four original-source RES pairs satisfy

$$
\mathbb E Z_4=\binom{8n}{2}\frac{3\binom{n-3}{2}}{2\binom n3}\sim144n.
$$

All pair indicators are pairwise independent (conditional probability constant on shared source), hence Var(Z4)=O(n), Z4/n ->144 in probability. The count of legal **two-step width-four then width-five source-indexed paths**, not proof nodes or refutations, has expectation

$$
\mathbb E T_5=\binom{8n}{2}(8n-2)p_4\frac{2\binom{n-4}{2}}{\binom n3}\sim6912n.
$$

Finite original-source controls: Python six fixtures (n=64,128,256, seeds 11,23), independent Node naive all-pair/third replay at n64/seed11: Z3=294, Z4=8628, T5=375418, five hostile corruption rejections. Historical R_mix341 accepted-byte parser NOT executed; source-authenticated ordinary RES inference paths are **not** UNSAT certificates. An expected number of paths does not imply a distinct-node lower or upper refutation bound.

LSPV-1/5 Route B: use this as an adversarial falsifier when proposing a rule-invariant obstruction; count wider legal intermediates and DAG sharing. LSPV-2/4 Route A: this supplies no physical same-machine guest contraction. Preserve exactly five existing agents, two Route A and three Route B, unchanged weights/tasks/schedules; B3, full mixed minimum and P vs NP OPEN. Root main.tex unchanged because full content readback was unavailable.