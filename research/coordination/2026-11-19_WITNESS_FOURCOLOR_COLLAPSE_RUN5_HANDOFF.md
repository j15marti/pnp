# Witness specialist run 5, strict-C palette necessity and physical deletion controls
2026-11-19 Pacific. P vs NP OPEN.

**PROVED:** For every **unpinned** original strict-C formula F, SAT using at most four values iff SAT using three values iff the primal graph is graph-3-colorable. After translation to missing color 4, the only accepted color triples in {0,1,2,3} are 012 and 123; fold 3->0 globally. Original C induced-table verified 320/320. Arbitrary fixed-color pins do NOT preserve this fold.

**Minimal five-essential SAT fixture:** C(v0,v1,v2), C(v0,v1,v3), C(v2,v3,v4), complete SAT vector (0,1,2,4,3). Primal graph contains K4; minimum n=5,m=3. Exhaustive all 120 triple-clause sets on five names found 30 five-essential, all isomorphic.

**Source-certified critical control:** Native n25 m25 incidence-girth8 full-C UNSAT source, existing 1046-node source-authenticated proof independently replayed (446 branches,600 leaves). Replayed all 25 physical deletion witnesses and 625 original-C values (600 retained TRUE,25 deleted FALSE). All 25 witnesses use all five colors **necessarily**, not just by a chosen search heuristic, due two CLAUSE-DISJOINT three-color UNSAT cores:
 A=[1,3,5,6,13,20,23,24], n=13,m=8,girth8, a static 61-node three-color proof tree and separate 59049-assignment exact audit.
 B=[2,8,10,15,17,18,22], n=11,m=7,girth8, a static 37-node proof and separate 6561-assignment audit.
Each core is physically clause-critical for **three-color** UNSAT with 3color deletion witnesses, and each is five-color SAT. Their variables may overlap; physical clause records do not. Deleting ANY parent clause preserves an entire no-3 core; the collapse theorem therefore excludes 4 colors too. The combined static no-3 proof has 98 nodes. Neither core is full-C UNSAT.

**Resource firewall:** This does not give a uniform cheap core discoverer, general full-C witness solver, or source-independent lower bound. The recoloring is O(n+m) given an existing <=4 witness. Generic no-3 search can use exponential time and proof size. All preprocessing, source access, proof acquisition, both SAT/UNSAT children, failed branches, replay, output and peak live space remain charged in any claimed N^1.33/N^.5 result. No verified arbitrary-C R<=N^.195 / B<=N^.65 / p<=N^.35 decomposition exists.

**Next concrete experiment:** On native150 girth10, find disjoint small three-color UNSAT cores **without advance knowledge**, fully charge the search and test whether a five-first SAT witness strategy wins on H-e. Native150 currently is not physically clause-critical and lacks a standalone static full-C refutation.

**Reproduce:** Archive T5C_Witness_FourColor_Collapse_DisjointCores_20261119.zip, SHA256 ec15ab33494f10bef6f374ec178ec2dd72e183668e90a442a0bade2bd022e54f. Includes Python3 audit, full physical source and existing 1046-node proof, 25 deletion witnesses, both new 3color proof trees, result JSON and SHA256 manifest. No randomness. Full report research/agents/witness/2026-11-19_T5C_FOURCOLOR_COLLAPSE_DISJOINT3CORES_RUN5.md.
