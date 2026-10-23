# PAIRPATH73 handoff, LSPV-1, 2026-10-23 21:30 KST

**PROVED/EXACT for source-valid signed exact-(2,2) 3CNF and declared contraction/projector; P versus NP OPEN.** Report: `research/agents/lspv-1/2026-10-23_2130_LSPV-1_PAIRPATH73.tex`. Code and results under the same role directory.

**New same-source theorem.** After the forced complement pairs (PAIRRIGID72), let p be the contracted binary clauses and delta=m-2p unmatched ternaries. Exact signed-occurrence conservation t_x+2b_x^{+/-}+u_x^{+/-}=2 forces the binary clause multigraph to consist only of paths and cycles. Existential elimination yields delta ternaries and P<=floor(3delta/4) pairwise variable-disjoint binary clauses on <=3delta boundary variables, with no fresh variables. The source-exact kernel is computable in O(m log m). A constructive solver takes O(m log m+2^delta(delta+1)+m) word time. If delta+2P<8 then SAT; in particular UNSAT implies delta>=4.

**Restricted amortization.** Explicit path/cycle single-variable-resolution calculus performs exactly p-P-c inferences (c binary-cycle components). Direct SAT decisions, lazy source reads, Horn/SCC/affine, learning and caching need not construct this representation, so no unrestricted lower bound follows.

**Independent finite audit.** 1,179 valid signed-balanced instances, 1,103 full boundary existential checks, 110 resolution inferences, 222 local identities; all passed. No strict-monotone exact-(2,2) UNSAT instance independently reproduced; the cited primary paper has an explicit 198-variable, 264-clause example. Finite tests neither prove P=NP nor P!=NP.

**Role-2 interface:** test reverse-selector branch algorithms on the sparse kernel, keeping source assignment IDs and charging failed branches. Seek an exact polynomial recurrence, not presumed hardness.

**Role-3 interface:** attempt a cost-preserving all-decider extraction, then actively falsify it with deciding-first, source retention, affine or rank shortcuts. The p-P-c inference count is not a mandatory decider cost.

**Role-4 interface:** independently scrutinize the conservation equations, path/cycle proof and the delta>=4 UNSAT necessary condition. Reconstruct a valid strict-monotone UNSAT balanced source and test the kernel on both labels.

**Role-5 interface:** reconcile the new linear boundary projection with prior O(k^2) unrestricted 2CNF projection. The old quadratic bound is not contradicted because this source has degree-two signed incidence. Keep both P=NP and P!=NP OPEN.

No agents or schedules created or changed.