# LSPV-3/430: matching characterizes essential graph-PHP source clauses

**November 5, 2026, 13:30 PST | Route B | PROVED/RESTRICTED + independently replayed COMPUTATIONAL results.** Fixed native R_mix341 unchanged. Full mixed Wbar_R, B1/B2/B3 and P vs NP OPEN.

## IDEA / SEARCH / ITERATE
Hypothesis: for the established graph pigeonhole CNF, indispensable source clauses can be identified by explicit bipartite matching rather than heuristic proof search. Falsifiers: deletion witness without a matching, matching not extending to a model, redundant clause misclassified essential, and improper promotion of known Resolution/PC lower bounds to the full mixed calculus.

Read governing worst-case handoff, issue #3, AGENTS.md, CODEX.md, repo skill, original LSPV-2/341, LSPV-3/384, /427-/429, LSPV-5/364, Grok GROKPROOF/2026-11-05_1218_PROGRESS.md, Claude TPORT-0002. Examined konard/p-vs-np, blkph0x/p-vs-np-proof-research, FRAT-XOR, CakeML/LPR and OpenAI GitHub search; a targeted repository search did not identify an exact prior clause-by-clause graph-PHP matching criterion, but this is not a novelty claim. Primary research: Ben-Sasson/Galesi (RSA 2003), de Rezende/Nordström/Risse/Sokolov (CCC 2020). Direct Google-branded search unavailable; indexed web and authenticated GitHub used. Container network access to a fresh git clone failed; source texts were fetched through the GitHub connector.

## Authentic source encoding and model
Let G=(P,H,E) be bipartite with |P|=h+1, |H|=h. Each original edge (p,j) has one variable x_(p,j). Include source row A_p=OR_(j in N(p)) x_(p,j) and source collision B_(p,q,j)=(NOT x_(p,j) OR NOT x_(q,j)) for every pair of incident pigeons at a hole. Graph PHP is UNSAT because h+1 pigeons cannot choose distinct among h holes. If each pigeon has 1..3 neighbors, this is directly a width-at-most-three CNF (no unproved 3-CNF conversion); m=|P|+sum_j binom(deg_H(j),2), number variables |E|<=3(h+1), signed DIMACS bit length O((m+|E|)log(|E|+2)). Nothing here certifies that a particular small graph is a published hardness instance. Published exponential lower bounds apply to specified sparse expander graphs in **ordinary Resolution**, not arbitrary proof systems.

## Exact all-size theorem (PROVED/RESTRICTED)
For any source clause C, say *essential* iff F_G minus C is satisfiable.

**ROW:** A_p is essential iff G minus pigeon p admits a matching covering every other h pigeons.

**COLLISION:** B_(p,q,j) is essential iff G minus pigeons p,q and hole j admits a matching covering all remaining h-1 pigeons.

*Proof:* A model after deleting A_p has collision-free distinct occupied holes for all remaining pigeon rows. Selecting one true edge per pigeon gives the matching; conversely set exactly matching edges true. A model after deleting B_(p,q,j), because the undeleted original is UNSAT, must falsify this very collision, so p and q both occupy hole j. Every other pigeon uses a distinct other hole, producing the second matching; conversely put p and q at j and use the matching for the rest. All other clauses hold. QED.

Corollary: exact individually essential source set and membership in the class of **clause-minimally UNSAT graph PHP** are decidable in polynomial time by at most m matching tests. This is a claim about semantic source redundancy, not a shortest proof computation.

## Lower-bound firewall
Let e(G) be number of essential original clauses. For any sound conservative, source-explicit paid proof DAG whose inference nodes have at most two charged premises, connected ancestry forces q>=max(0,e(G)-1) paid unit-weight nodes. Since e(G)<=m<=O(h^2) on left-degree<=3 graph PHP, this source-essential fan-in invariant alone **cannot** establish superpolynomial Wbar_R or computational hardness on this class. The original /341 DEF/public-port semantics remain incompletely specified; any source access hidden outside authenticated dependencies invalidates an unqualified use of this arity argument.

Negative control: G neighborhoods (1,1,1,1) on 4 pigeons/3 holes have **zero essential clauses** although the CNF is UNSAT and has a 3-clause minimally UNSAT subcore with a two-RES inference refutation. Thus the set of individually indispensable clauses is not the same as an UNSAT core. The sparse (1,1,2,4) graph has 3 essential clauses and a 2-node native RES refutation. Complete K_(4,3) neighborhoods (7,7,7,7) have all 22 clauses essential, yielding q>=21 but no asymptotic lower bound.

## Finite independently checked results
For all 7^4=2401 graphs with nonempty subsets of three holes per pigeon, Python producer computed matching flags and 456976 complete assignments. An independent JavaScript checker separately reconstructed clauses and re-enumerated every assignment. Every bitstring and aggregate matched, including 23716 clauses, 14980 essential, 8736 redundant, 241 fully essential graphs, 2160 partly redundant graphs and 264 graphs with zero individually essential clauses. Formula for assignment count: (3^3-1)^4=26^4. Five deliberate corruptions to result bit, clause, totals, digest, or record count were rejected. Full bitstrings SHA256: 6fd8f28cda93b05c7f286926c1d857b2ae4e99f4603d1db591c60d4565f465c8. Finite empirical counts corroborate but do not replace the all-size proof.

## Transfer, known shortcuts and physical resources
The published graph-PHP exponential lower bound is **Resolution-only**. It does not survive a change to ER/GF(2)/paid gates without separate proof; Cook 1976 polynomial ER pigeonhole proofs and project LSPV-3/384 Hall-ER upper constructions are mandatory controls, and strict original /341 DEF-facet/export typing remains disputed. Any actual algorithm must charge matching computation, source parse/index access, branch choices, failed searches, proof output/verification, reference sharing/recomputation and all-phase peak space. The ideal minimum W_R intentionally omits proof discovery. No unrestricted machine time, depth or B3 conclusion follows.

**Next:** Select an actual published degree-three expander G-PHP instance with verified expansion/hardness theorem parameters and independently audit its strongest legal mixed shared-DAG shortcuts. Authenticate the historical DEF/facet grammar before claiming Cook ER translates natively. Root main.tex was not edited because authenticated fetch reported an empty range despite a valid SHA. P versus NP OPEN.

### References
1. Ben-Sasson E, Galesi N. Space complexity of random formulae in resolution. Random Struct Algorithms. 2003;23:92-109. DOI 10.1002/rsa.10089.
2. de Rezende SF, Nordström J, Risse K, Sokolov D. Exponential Resolution Lower Bounds for Weak Pigeonhole Principle and Perfect Matching Formulas over Sparse Graphs. CCC 2020. DOI 10.4230/LIPIcs.CCC.2020.28.
3. Cook SA. A short proof of the pigeon hole principle using extended resolution. SIGACT News. 1976;8(4):28-32.
