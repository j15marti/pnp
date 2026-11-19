# Red-team coordination handoff: canonical SA3 tables fail SA4 extension on a SAT tree (2026-11-19)

**PROVED:** For strict-C F=C(a,b,c)&C(a,d,e) with five distinct names, the exact run-6 universal SA3 pseudomarginals cannot extend to a four-variable marginal on (a,b,c,d). They require mu_abd(0,2,3)=20/750>0, yet mu_abc support forces c=1 for a=0,b=2 and mu_acd(0,1,3)=0. A nonnegative 4-way distribution would imply 20/750<=0. This is an explicit 0-1-coefficient event inequality, not a numerical solver observation.

**Do not overclaim:** F has 180 SAT assignments, with full strict-C witness (0,1,2,1,2); SA4 on this F is feasible. The existing universal SA3 feasibility theorem remains true. Only automatic extension of its particular table is falsified.

**Independent checks:** 30/125 original C; 125/125 alternate predicate agreement; 4 normalized SA3 triple tables; 300 pair-marginal checks; native25 25 deletion witnesses (600/600 retained clauses, 25/25 deleted clauses failing), incidence girth 8; its threefold incidence cover 75/75 clauses SAT, connected, girth 8. No random seeds. Reproducibility archive T5C_RedTeam_SA3_Forest_Nonextendibility_20261119.zip SHA256 8a9919b73260c6b2df8dc193884b29e7b922ae2f719354674e295086c97dc4f6.

**Next blocker:** exact SA4 native25 primal/dual computation with certificate acquisition and read-only versus writable space charged; do not infer unrestricted SAT lower bounds from local consistency limitations. Full report: research/agents/redteam-new/2026-11-19_SA3_SA4_FOREST_EXTENSION_COUNTEREXAMPLE.md.
