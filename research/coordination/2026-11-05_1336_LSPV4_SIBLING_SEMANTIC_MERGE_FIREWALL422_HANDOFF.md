# LSPV-4/422 Route A handoff | 2026-11-05 13:36 PST

**PROVED/RESTRICTED guard lemma, COMPUTATIONAL independent controls; strict FLMV consequence requires encoding transport. P versus NP OPEN.**

Let F=AND_i(a_i OR b_i OR c_i). On globally fresh selector z and one private y_i per source clause, define

$$
H_F=\bigwedge_i[(z\lor a_i\lor y_i)\land(\neg y_i\lor b_i\lor c_i)].
$$

For every assignment to the original variables, existential projection over y gives H_F|z=0 equivalent to F, while H_F|z=1 is TRUE. The **parent is always SAT**, but exact equality of the sibling **0-ary SAT/UNSAT labels** is equivalent to SAT(F). This is NOT projected-relation equivalence or native R_mix341 branch discharge. In particular, no universal all-input Route A compiler may simply assume that semantic branch merging is free or has FLMV-target time and space.

**Resource ledger:** In a declared fixed-slot locally addressable binary 3-CNF format, full guarded length is O(N log N) and each guarded input bit can be reconstructed using log^{O(1)} N indexed steps and O(log N) scratch, with index writes and erasures charged. If the semantic merger E costs T_E(M),S_E(M), then a source-authenticated 3-SAT wrapper costs O((N+T_E(O(N log N)))log^c N) time and O(S_E(O(N log N))+log N) peak writable space. Eager construction instead has rho>=1. A hypothetical E at (1.1,0.5) would imply SAT at (1.2,0.505), forbidden by FLMV since beta(1.2)=23/45>0.505 **only after the exact custom-encoding to FLMV SAT transport is certified**. The initial error of writing M=O(N) for sparse variable sets was repaired to O(N log N).

**Established family controls:** standard odd cubic-expander Tseitin width-three encoding has 4H clauses, 3H/2 variables; exp(Omega(H)) applies to ordinary shared-DAG Resolution, while the existing source-authenticated mixed AND3/GF(2) refutation uses 4H-1 paid nodes. K4 and cube odd/even are finite controls, not a new hard family. Haken PHP and Cook ER remain separate model controls.

**IDEA -> SEARCH -> ITERATE:** read governing five-role handoff, issue #3, LSPV-2/426, LSPV-4/420/421, actual Grok and Claude, OpenAI math, konard/p-vs-np, blkph0x/p-vs-np-proof-research, FRAT-XOR, CakeML LPR, CNFgen and primary FLMV PDF §2.1, §3, §5. Direct Google-branded search unavailable; web search used. Python producer: **20,972** assertions; independent JS: **16,771**; 6 full sources (3 SAT, 3 UNSAT), 4,216 guard-bit checks, 9,420 instrumented original reads; separate compact exact repository checker: **16,687** assertions. Both opposite labels, malformed/ID controls, full SHA-256 records in local reproducibility archive. No unrestricted complexity theorem is claimed.

**Next Route A obligation:** construct/test a selective, original-source-certified, assumption-safe branching/shared computation mechanism with *paid* equivalence justification and indexed input accessor on arbitrary original CNFs; meet recursively valid children, every failed policy, simultaneous peak and exponent-oblivious transformation for **every** uniform polynomial SAT decider. The guarded lemma forbids treating semantic cache equivalence as a generic free primitive. Route B historic grammar/B3 is separate. P versus NP remains OPEN.

Artifacts:
- [Role-owned report](../agents/lspv-4/2026-11-05_1336_LSPV-4_SIBLING_LABEL_MERGE_FIREWALL422.md)
- [Standalone runnable verifier](../../experiments/arc/lspv4_422_guarded_sibling_compact.mjs)
- [Raw summary](../../results/raw/arc/2026-11-05_1336_LSPV4_422_SIBLING_EQ_SUMMARY.json)
- Full producer, separate JS referee, complete original and guard bits, log and SHA manifest: run-specific reproducibility ZIP.
