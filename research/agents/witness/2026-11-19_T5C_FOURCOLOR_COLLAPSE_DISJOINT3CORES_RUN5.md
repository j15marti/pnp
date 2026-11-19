# Strict T5 witness run 5: four-color collapse and disjoint palette obstructions
2026-11-19 Pacific. **PROVED** exact unpinned palette theorem, **COMPUTATIONALLY VERIFIED** native critical controls, **OPEN** all-input resource theorem and P versus NP.

## Exact source and theorem A (PROVED)
C(x,y,z) accepts directed triangles under R(a,b) iff (b-a)%5 in {1,3}. Its five unordered winning triples are 012,014,034,123,234; precisely 30 of 125 ordered triples pass. Physical clauses have three distinct variable **names**.

For **every finite unpinned strict-C formula** F:
  SAT with <=4 values iff SAT with <=3 values iff primal(F) is graph-3-colorable.
Proof: translate one missing color to 4. Within {0,1,2,3}, the ONLY C-winning triples are 012 and 123. Applying f(0)=0,f(1)=1,f(2)=2,f(3)=0 to the complete witness maps every satisfied original C clause to a permutation of 012. Conversely a proper graph-3-coloring makes every physical clause rainbow 012. All five omitted-color choices times 4^3 triple values were audited: 320 implications, zero failures. The source uniform recoloring costs O(n+m) indexed-RAM time including full C replay and O(n) extra words if the original witness is immutable. Arbitrary pins can block this recoloring.

## Theorem B (PROVED): smallest five-essential SAT formula
F5 = C(v0,v1,v2) & C(v0,v1,v3) & C(v2,v3,v4) is SAT with complete original C witness (0,1,2,4,3), but it has K4 in the primal graph on v0,v1,v2,v3, so no 3-color witness and by theorem A no 4-color witness. At least five names and three clauses are needed: any source of <=4 names cannot use five values, while any <=2 ternary clauses admit a rainbow 3-coloring. Exhaustively checked 1,10,45,120 subsets of sizes 0,1,2,3 on five names: five-essential counts 0,0,0,30. All 30 three-clause examples are isomorphic by S5 relabeling, orbit size 30.

## Theorem C (PROVED): two disjoint no-3 cores force five-color deletion witnesses
If F contains two **clause-index-disjoint** subsets A and B whose individual strict-C formulas have no 3-color witness, then EVERY single physical deletion F-e still contains one intact no-3 core. Therefore every SAT witness of F-e must use all five colors, by theorem A. If F is physically clause-critical UNSAT this applies to every deletion. The theorem certifies palette necessity, NOT full-five-color UNSAT.

## Native critical 25-clause source (independently verified)
From the previous source/proof archive, independently replayed a physically clause-minimal full-C UNSAT source with n=25,m=25, incidence girth 8 and an existing 1046-node full-C GAC refutation (446 branches,600 contradiction leaves). Its 25 complete physical deletion witnesses all passed original C, 625 checks (600 retained TRUE,25 deleted FALSE), each using exactly five colors.
Found two CLAUSE-DISJOINT 3color-UNSAT 5color-SAT cores:
 A=[1,3,5,6,13,20,23,24] has 8 physical clauses,13 names,incidence girth8. Static all-three-color refutation has 61 nodes and 41 contradiction leaves; independent normalized exhaustive test checked 3^10=59049 assignments.
 B=[2,8,10,15,17,18,22] has 7 physical clauses,11 names,incidence girth8. Static refutation has 37 nodes and 25 contradiction leaves; independent exhaustive test checked 3^8=6561 assignments.
Each 3color refutation leaf names a source clause and an already equal-colored pair, and every branch covers all three color choices. Both cores were checked 3color clause-critical, with explicit 3color witnesses after their individual deletions; both are SAT under all-five-color original C. Their variable names can overlap, only physical clause sets are disjoint.
By theorem C these two short refutations, totaling 98 nodes, prove that **every one of the full 25-clause source's 25 deletion witnesses necessarily uses all five colors**. This is stronger than observing that the 25 previously found vectors happened to do so. The earlier 1046-node full-C refutation is separately checked and still required to assert the parent is UNSAT.
Source SHA256 a372c198871f73ec9ebf6665e597f0fae7b3af8613aeae325c07bd6e3ca5bd75; prior full-C static refutation SHA256 2e386cc59ebb1e7c8c4a7f2d418ab23178b6294f9fd7b17b0264ee3ac86b6ef9.

## Fully charged scope and next blocker
The two 98-node palette certificates are cheap to authenticate **once discovered**. Their discovery is not supplied by any uniform polynomial-time algorithm, nor does a three-color contradiction certify five-color UNSAT. General 3color tree search can require exponential time O(3^n(n+m)), linear writable space and exponential proof output. A generic five-color SAT/UNSAT solver still must charge both polarities, failed branches, source scans, certificate verification and entire output. The architecture R<=N^.195 rows, B<=N^.65 blocks, private size<=N^.35 is unproved on arbitrary sources. The local exponent threshold for N^1.33 sequential work stays a<=97/70 from T=N^(.845+.35a). No unrestricted SAT lower bound follows.

The next falsifiable task is a source-uniform short no-3-core recognizer and fully charged five-first witness search on the native girth10 150-variable control, which is not yet physically clause-critical or statically full-C UNSAT-certified.

## Reproducibility and prior literature
Complete archive T5C_Witness_FourColor_Collapse_DisjointCores_20261119.zip includes independent Python 3 standard-library audit, original source and complete witnesses, full prior refutation, both new static 3color proof trees, exact results and SHA256SUMS. No random seed. Archive SHA256 ec15ab33494f10bef6f374ec178ec2dd72e183668e90a442a0bade2bd022e54f.
Prior reviewed witness repository run4 (blob 342efe19a86257b469d8cf86b2fff35a9a52197f), anchored pinned 2SAT run3 (blob beacb7820a25851bed34e840777c8e6040312be5), archived native25 source/proof, and CSP-structure literature (Ganian et al., IJCAI 2020, DOI:10.24963/ijcai.2020/263). No publication-priority claim.

**P versus NP remains OPEN.**
