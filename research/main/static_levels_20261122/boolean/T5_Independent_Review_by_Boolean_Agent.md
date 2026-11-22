# Independent review of the strict-C5 one/two-unknown theorem

22 November 2026, America/Los_Angeles.

Reviewer: same-conversation Boolean characterization collaborator. This is internal mathematical review, not external peer review or formal verification. No T5 audit was rerun; the review read the complete theorem note, standalone script, template raw record, and global-source raw record.

Reviewed files in ../t5/: T5_One_Two_Unknown_Core_Theorem.md, t5_one_two_unknown_audit.py, t5_template_results.json, t5_global_source_results.json.

## Conclusion

PASS in the declared strict symmetric C5 scope. The one-row/two-row arguments, the universal four-row upper bound at two unknowns, its sharp witness, and the seven-variable nine-row globally UNSAT source are sound as written. The finite 157-relation closure result is supported by an exhaustive closure program with the stated finite-template scope. None of these establishes an unrestricted time, space, or CM lower bound.

## Checks and reasoning

The allowed triples are the five consecutive triples of a five-cycle and their permutations. The unary supports for two distinct fixed values are five singletons and five doubletons. The listed doubletons form the cycle 0-2-4-1-3-0. Equal fixed values yield an empty unary support. Pairwise-intersecting edges without a common endpoint would contain a triangle; hence this five-cycle plus singleton family has Helly number two. The twelve one-unknown supports consist of those ten sets, the full domain, and empty.

For M_0 the undirected edges are 12,14,34, a four-vertex path. For distinct a,b, an ordered pair (x,y) lies in both M_a and M_b exactly when the unary support U(x,y) contains both values. Every permitted doubleton occurs for exactly one unordered pair {x,y}, so a nonempty intersection contains precisely the two reversed pairs. This validates the first branch of the four-row proof: two binary rows leave at most two candidates, each excluded by one additional actual source row.

In the one-binary branch, a nonempty unary intersection is either full, one source doubleton, or a singleton expressible using at most two source rows. The full and doubleton cases give at most three and four rows. For a singleton {p}, p=a is immediately excluded by M_a. If p differs from a, its possible partners form U(p,a), one member of the same Helly-2 family. If the y-unaries exclude all those partners, one y-row disjoint from U(p,a) suffices unless two y-unaries already conflict. Thus at most two x-rows, one y-row, and the binary row suffice. This closes all cases without relying on the enumeration.

For the sharp four-row example, the two x-unaries intersect in {0}; M_1 intersect M_4 consists of (2,3),(3,2). The deletion witnesses (3,2),(2,3),(0,1),(0,2), in the stated row order, each satisfy the three remaining rows. Hence the minimum core is exactly four.

Every pair of anchor names appears together in one of the five anchor triples. Thus all five anchor values are distinct. The complements of the five permitted triples are the five edges of the ordinary cycle. A satisfying anchor bijection preserves that edge set, giving exactly the dihedral rotations and reflections. Applying the inverse frame to x and y transfers the four-row contradiction to every permitted frame. The full nine-row source is therefore globally UNSAT.

At reference values a_i=i, x=2, y=3, only C(x,a1,a2) is false. The zero-unknown minimum core is one. With only x unassigned, the residual rows include supports {0,3} and {2}, while no individual row is false, giving minimum core two. With both x,y unassigned, all anchor rows are true constants and the sharp four-row subsystem remains. This proves the simultaneous 1,2,4 sequence for separately presented instances without assuming carried-over machine history.

The 25 atomic nonempty two-unknown relations comprise ten unary supports on each coordinate and five M_a relations. Every residual row is either one of these, a true constant, or false. The code begins from the full 25-pair relation and closes under intersections with all 25 atoms until no new mask appears. This reaches exactly all finite conjunctions and therefore validates the scope of the 157 relation count. A false constant adds no new relation because the empty relation is already obtainable from conflicting unary atoms. All singleton contexts are realizable using singleton unary supports, so distinct masks have distinguishing contexts. Eight fixed bits are necessary only under this exact reusable-interface contract.

The arbitrary-r source-type ceiling 1+10r+5 binomial(r,2)+binomial(r,3) is valid: empty contributes one type, each variable has ten unary types, each unordered pair has five binary types, and each unordered triple has the one symmetric C type. Identical residual types cannot occur twice in a minimal core. The resulting O(r^3) source-core ceiling rules out extrapolating the first values to indefinite doubling, while leaving acquisition and refutation cost unresolved.

The code's exhaustive global stage examines 5^7 assignments, checks ten anchor frames, the unique false reference row, all smaller possible source cores, and the four deletion witnesses. Its raw output matches the note's claims. The template raw file explicitly identifies its origin in earlier inline runs, so no duplicate execution is inferred from the later standalone script.

No correction is required. The distinction from compact circuit-defined ordered T_q, the source-core versus proof-cost distinction, and the eight-bit interface qualification should remain in the parent report.
