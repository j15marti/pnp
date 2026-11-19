# Strict-C critical-graphs: Hajós witness transport and treewidth firewall
2026-11-19 America/Los_Angeles. Status PROVED structural theorems; COMPUTATIONALLY VERIFIED exhaustive deletions; FALSIFIED growing-girth claim for this family; OPEN unrestricted P vs NP.

## Exact model
D=Z5, R(a,b) iff (b-a) mod 5 is in {1,3}. C(h,u,v) is the cyclic directed triangle, with either orientation, and accepts 30 of 125 ordered triples. Every original clause has distinct variable names; only co-occurrence enforces unequal values. Fresh private head h_e per edge of graph G gives `exists h_e C(h_e,u,v) iff u!=v`. Thus the full C source is UNSAT iff G is non-5-colorable, and clause-minimal UNSAT iff G is edge-minimal non-5-colorable. Historical Q, P, and S evidence was not reused as C.

## Exact Hajós theorem with deletion witnesses
Let G1,G2 be edge-minimal non-5-colorable graphs. Select edges ab in G1 and cd in G2; identify a=c=w, delete ab and cd, and add bd. Every proper five-coloring of G1-ab must give a=b (else G1 is colored); every proper coloring of G2-cd must give c=d. Hence the join J cannot be 5-colored. For deletion of bd, align the roots of colorings of G1-ab and G2-cd. For a retained edge f in G1-ab, combine a coloring of G1-f (a!=b because ab is present) and a coloring of G2-cd (c=d) after aligning a=c, so b!=d. Symmetrically for f in G2-cd. Therefore J is edge-minimal non-5-colorable and each deletion witness is constructible without a coloring oracle. Lift to strict C by assigning completing private heads to the retained unequal endpoint pairs and any head to the designated equal pair. The designated deleted original C clause then evaluates FALSE and every retained C clause TRUE.

Girth(J) >= min(girth(G1),girth(G2)): any mixed cycle consists of two selected-edge replacement paths of lengths at least g1-1,g2-1 plus connector bd, for length at least g1+g2-1. Private-head C incidence girth equals 2*girth(J), whereas C primal graph contains triangles.

Construct a tree decomposition of J from the child decompositions by adding bag {w,b,d} and attaching to child bags covering the selected edges. This gives tw(J) <= max(tw(G1),tw(G2),2). Append leaf bags {h_e,u,v} for each C head, so strict C primal tw is also <= max(tw(G1),tw(G2),2). Similar Hajós bounded-treewidth observations appear in Xie (2026), arXiv:2609.14865. No novelty claim for classical Hajós theory.

## Explicit source and numerical replay
Base G0 = Mycielski^3(C5), with 47 graph vertices and 236 edges; chi=6, edge-critical, graph girth 4. Construct balanced joins of t copies, t=1,2,4,8. Exact formulas: graph vertices 46t+1; edges 235t+1; private-head strict C variables 281t+2 and C clauses 235t+1. Incidence girth 8. Explicit original C primal tree decompositions have verified width <=21 at all tested sizes, matching the constructive bound for every t.

| t | strict-C variables | clauses | complete deletion witnesses | independently replayed C clauses | TD width bound |
|---|---:|---:|---:|---:|---:|
| 1 | 283 | 236 | 236 | 55,696 | 21 |
| 2 | 564 | 471 | 471 | 221,841 | 21 |
| 4 | 1,126 | 941 | 941 | 885,481 | 21 |
| 8 | 2,250 | 1,881 | 1,881 | 3,538,161 | 21 |
| total | | | 3,529 | 4,701,179 | |

All 4,697,650 retained-clause evaluations were TRUE, and all 3,529 designated deleted original C clauses were FALSE. Every complete deletion witness, every original source clause and the width-21 decomposition was independently replayed. The separate replay uses (a-b)^2+(b-c)^2+(c-a)^2 == 1 modulo 5, confirmed equivalent to the original strict C over all 125 ordered color triples. Deterministic run label 2026111903; no random seed, SAT oracle or free polarity. Input and witness JSONL.GZ, scripts, exact raw JSON, output ledgers and SHA-256 manifest are in conversation-local archive T5C_Hajos_Critical_Width_Firewall_20261119.zip. The complete local package is not uploaded to GitHub.

## Falsifier and new obligation
Base G0 contains 2,080 four-cycles; two explicit edge-disjoint four-cycles survive deleting any single selected base edge. Hence these balanced joins retain graph girth four and C incidence girth eight regardless of size. The universal assertion that Hajós joins *never* increase girth is false: joining two K3's produces a C5 of girth five; independent 3-critical test passed. A K6+K6 join has 11 vertices, 29 edges, girth three and 29 verified 5-color deletion witnesses.

For any 6-critical graph, minimum degree >=5. The published girth-treewidth bound of Chandran and Subramanian (JCTB 93:23-32, 2005) implies tw=Omega(4^floor((g-1)/2)/(g+1)) for girth g. Consequently growing C incidence girth in edge-critical private-head source graphs forces unbounded treewidth. Fixed-base bounded-width Hajós inflation is not a path to increasing girth. Growing girth and width remain *structural* requirements, not machine-time lower bounds.

## Resources, scopes and remaining gap
The balanced materialized generator and full verifier account for recursive child-color calls, private-head completion lookups, strict-C predicate checks, source records and full deletion witness output. All 3,529 witnesses required 5,624,248 output color symbols and 11,690,062 plain JSONL text bytes before gzip; exhaustive full-ledger output alone has an Omega(N^2) printing bound, not computational hardness. CPython main traced-heap peak 1,376,817 bytes (reproducibility measurement, not a RAM lower bound). A recognizable canonical family has a cheap construction-refutation certificate and bounded-width DP. Its shared assignment space has 5^(46t+1) rows and Theta(N) blocks, violating the separate N^.195 row and N^.65 block budgets. No arbitrary CNF specialist, n^1.33/sqrt(N) result, or P-vs-NP lower bound follows.

Next exact target: efficiently produce source-certified growing-incidence-girth **critical** strict-C graphs and all original-clause deletion witnesses, without relying on fixed-width shortcuts. The prior LPS q=89,257 sources establish high-girth UNSAT graph encodings but critical cores and complete deletion ledgers remain ungenerated. Obtain those, or a smaller alternative, before making hardness assertions.

## Bibliography
1. Jensen TR, Royle GF. Hajós constructions of critical graphs. J Graph Theory 1999;30:37-50. doi:10.1002/(SICI)1097-0118(199901)30:1<37::AID-JGT5>3.0.CO;2-V.
2. Xie Y. Nullstellensatz degree under Hajós joins and vertex identifications. arXiv:2609.14865 (2026). https://arxiv.org/abs/2609.14865.
3. Chandran LS, Subramanian CR. Girth and Treewidth. J Combin Theory B 2005;93:23-32. doi:10.1016/j.jctb.2004.05.004.
4. Mycielski J. Sur le coloriage des graphs. Colloq Math 1955;3:161-162.
5. Previous project: research/agents/critical-graphs/2026-11-19_LPS73_GIRTH_SOURCE_K6_LIFT_FALSIFIER.md. User's strict research PDF independently reviewed; exact-title strict research ZIP could not be accessed in this run.

No existing schedule, manuscript or agent ownership changed. P versus NP OPEN.