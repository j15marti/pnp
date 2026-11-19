# Strict-C witness run 4, independently auditable coordination handoff (2026-11-19)

**PROVED restricted algorithm.** For canonical C=directed T5 triangle (30/125 tuples), find an anchor a minimizing r(a), the number of distinct variable names in clauses not containing a, in deterministic O(n+m) indexed-RAM time. For active names h and directed co-occurrence count c(a,x), r(a)=h-1-sum_{x!=a}[c(a,x)=d(x)]. Two stable radix-counting sorts handle all 6m directed pairs. k exceptional clauses imply r<=3k.

Branch over all assignments to U_a; physical exception failures are source-replayed, while successful exceptional assignments reduce to a **fully pinned common-anchor** strict-C subsource, already solved exactly by 2SAT. SAT yields a full verified original-C vector; UNSAT outputs one checkable original-source certificate for **every** branch, with no polarity oracle. Time O((n+m)5^r), peak writable O(n+m) words; output/certificate time is included. For unpinned inputs D5 symmetry cuts 5^r rows to K_r=(5^r+5)/10; pinned branches do not get unauthorized symmetry reduction. Optional leaf cap returns UNKNOWN, not UNSAT.

**Reproduced:** 1,494 solver/certificate checks, 44,242 rows, 493 SAT/1000 UNSAT/1 intentional UNKNOWN, zero errors. Exhaustive 1042 unpinned sources (n<=5), 440 seeded pinned instances (n<=6), 1384 separately brute-checked anchor optima, 8 corrupted proofs rejected. Original native25 critical source's 25 deletion witnesses pass 625 C evaluations. Independently compiled C++ DPLL gives SAT on all native25 H-e in 9-104 search nodes, and exhaustive UNSAT in 205 nodes for H.

**Firewall:** The high-incidence-girth critical native25 source has min r=23 on n=25; direct D5 proof-stream requires 1,192,092,895,507,813 rows, even though finite DPLL readily finds witnesses. Previous native150 girth10 candidate has min r=149 on n=150. Backdoor parameter not small in hard controls. No universal SAT complexity conclusion.

**Conditional target:** If shared-row/block architecture and free-of-global-indexing assumptions are independently proved, and each N^.35 local block misses a common anchor in at most lambda log_5 N clauses, row-block scan is N^(1.195+3lambda+o(1)); lambda<=0.045 fits 1.33. Full-source scan per row and block is N^1.845, not admissible.

**Next challenge:** non-anchor strong backdoor or separator amenable to uniform low-workspace discovery on native25/native150; independently verify proof acquisition costs and original C clauses. This is a tractability theorem, **not P vs NP proof**.

Details and reproducibility: `research/agents/witness/2026-11-19_T5C_MINIMAL_EXCEPTION_ANCHOR_D5_STREAM_RUN4.md`; full code, source fixtures, proof transcripts, independent verifier and hashes are in the conversation artifact `T5C_Minimal_Apex_Backdoor_Stream_Run4_20261119.zip`. Seed 202611190640.
