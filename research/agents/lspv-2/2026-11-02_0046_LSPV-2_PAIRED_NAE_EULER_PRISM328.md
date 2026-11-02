# LSPV-2 PAIRED-NAE-EULER-PRISM328 (2026-11-02 00:46 PST)

**PROVED/EXACT on a recognized restricted canonical sublanguage; independently COMPUTATIONAL; all-input P vs NP OPEN.** Target only valid duplicate-free proper Döcker monotone 3-SAT-(2,2) ORIGINALS, rejecting malformed strings. Preserve all five tasks/ownership/schedules. This SAT special case is **already known in Döcker 2019** and the cubic edge-quasi-coloring in Bacsó et al. 2019; no general novelty claim.

## Exact constructive original-source theorem

Suppose every positive source triple of a valid canonical original F has its exact all-negative complement. The q=2n/3 paired supports give a loopless cubic multigraph whose vertices are the q positive source clause IDs, and whose n original-variable-labeled edges join the two positive occurrences of each variable.

For each connected cubic component of v vertices, pair its vertices arbitrarily and add v/2 artificial edges, exactly one incident to each vertex. The augmented connected graph is 4-regular with 2v edges. Construct an Euler circuit and cyclically alternate two edge colors. Every vertex has augmented color degrees (2,2); removing its artificial edge leaves (1,2) or (2,1). Assign original x_i the color of its original dual edge. Both colors occur in every positive triple, so that positive clause AND its complementary negative clause hold. The output is a **complete original-clause-checked SAT witness**, with polynomial source recognition, graph construction, Euler traversal and output; no free SAT-label or representative oracle. Disconnected originals also work. Nonpaired canonical originals return UNRESOLVED to the fully charged general fallback, never UNSAT.

This is an alternate constructive certificate for a *known satisfiable subclass*, not a solution of arbitrary M22-SAT. The explicit source-recognition and Euler algorithm are linear word work after indexing, O(n log n) bits including source/graph/index/tour/witness on standard explicit encodings. Sequential tape/head movements may add polynomial overhead.

## Same-original exact forward circuit and transfer

The paired source clauses on support (a,b,c) equal NAE3(a,b,c), implemented by 3 fan-in-two XOR/OR gates: (a XOR b) OR (b XOR c). A binary AND tree over q blocks has exactly **g=4q-1=8n/3-1** gates within this declared disjoint-block architecture. Its output-one biconditional Tseitin representation has **14q-2 clauses** and **38q-6 literal records** and a unique forward trace per original assignment. Tseitin is NOT a canonical child. This is not an unrestricted minimum or decision lower bound.

Connected k-prism canonical originals, k>=3, have n=3k, m=4k. Source-indexed prism recognition yields a four-state boundary transfer in order 00,01,10,11:

```
M = [[1,1,1,2],[1,0,2,1],[1,2,0,1],[2,1,1,1]]
```

The exact number of original SAT assignments is **trace(M^k)**. Its characteristic polynomial is (lambda+1)(lambda+2)(lambda^2-5lambda+2), giving counts k=3,4,5,6,8,12: **86, 450, 1942, 9074, 187714, 81166050**. The first three are independently exhaustively enumerated against original source CNF; an independent finite closed-walk computation confirms k<=6. Source recognition/graph search, boundary synthesis and big-integer matrix operations are paid. A four-state continuation quotient on this recognized family does not imply universal semantic compression or hardness.

## Independently checked both-label controls

Z6_NAE: n=6, 8 source clauses, 18 models and 15 forward gates. **Same ORIGINAL** pins (x4,x5,x6)=(0,0,0) give zero completions with a complete eight-leaf original-clause falsification cover; changing only x4 to 1 gives three completions and a checked witness. Disconnected Z6+Z6: valid canonical, 324 models. F9/Y6/F15 are canonical but not complement-paired and are correctly rejected by this terminal; their complete original model counts 70/20/1032 and inherited 28/19/48-gate circuits were independently replayed. Same-original F9 SAT2/UNSAT0 and F15 SAT2/UNSAT0 pin controls have full eight-leaf/64-leaf original-clause covers. U198 and V198 are rejected by the restricted recognizer; a fresh independent U198 source refutation replay made 384 boundary queries, 19488 DPLL nodes, 6099608 source-literal probes, no survivors; a V198 source witness was checked against all 264 original clauses.

**Independent checks:** 3,263,627 no-producer-import checks of canonical grammar, Euler circuits, every clause, source versus gate evaluation, exact matrix and pinned covers; plus 14,832 independent Tseitin unique-trace checks; 180 renaming/clause-order/sign controls and 12 malformed serialized rejections. For n=198 forward checks are sampled, not exhaustive.

**Paid direct-versus-circuit SAT:** common UP-DPLL original source versus Tseitin literal visits: Z6 SAT 55/2037, Z6 UNSAT 61/1947, F9 SAT 74/5012 and UNSAT 56/4431, F15 SAT 313/19562 and UNSAT 338/16309, PRISM3 root 270/5974. Tseitin counts exclude additional positive acquisition/compilation cost. Host word/probe counts are not native FLMV transitions. This *falsifies* any inference that smaller forward gate count automatically means lower decision work.

**Fully charged all-input gap:** sum grammar, original bit/head/index reads, pair recognition, unsuccessful policies, switching, gate/Tseitin compilation, semantic quotient acquisition/equality, proof and GE, cache/replay, child/output/bit access, all DELAY/COPY/RECOMP guest work and recursively evaluated successors; peak space counts all co-live original/index/ancestor/cache/child/proof/guest writable configurations. Euler terminal emits no child, but general fallbacks can be exponential. No uniform all-input polynomial total work, arbitrary A->Phi(A) hereditary power-short contraction, or strict SAME-MACHINE numerical FLMV transfer is proved. Both P=NP and P!=NP OPEN.

## Duplication/literature

Döcker 2019 [original target and known paired-NAE satisfiability](https://arxiv.org/abs/1912.08032); Bacsó et al. 2019 [cubic edge-quasi-coloring](https://doi.org/10.1007/s00373-019-02063-w); Dhawan 2024 [constructive Shannon multigraph coloring](https://doi.org/10.1137/1.9781611977912.77); Bollig and Wegener 2000 [OBDD minima](https://doi.org/10.1006/jcss.2000.1733); Fortnow-Lipton-van Melkebeek-Viglas 2005 [FLMV](https://doi.org/10.1145/1101821.1101822). Project duplications: LSPV2 326 (Z6/NAE pairing), 327 (cubic signed graphs), LSPV3 boundary keys; verified five-role handoff and issue #3. GitHub project search and separate github.com/openai SAT/OBDD code search recorded; openai search returned no relevant excerpts and does not establish novelty.

Complete producer, no-import verifier, full raw, matrix, source/circuit fixtures, full mathematical report and integrity manifest are retained in the run's user-facing reproducibility archive. Root main.tex must not be overwritten if authenticated blob contents are empty.
