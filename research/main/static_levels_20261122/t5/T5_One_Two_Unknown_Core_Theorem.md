# Independent one- and two-unknown levels in strict symmetric C5

22 November 2026, America/Los_Angeles.

## Scope and status

Each level is a separate static input: a formula and the values still supplied. No earlier execution, cached answer, or sequential-machine history is assumed. The solver must be correct on permitted SAT and UNSAT inputs. The analyst may choose an UNSAT input without giving an UNSAT promise to the solver.

The fixed strict symmetric relation C over D={0,1,2,3,4} permits exactly the permutations of 012, 123, 234, 340, and 401. Clauses have three distinct variable names. It is not the ordered tournament relation R.

The template definition was recovered from research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md, current fetched blob a886f3387a8676b9cc86afbf3bebf22630109d49, section 3.1. The one-unknown bound below is a recovered baseline, also reported in the recent One Unknown Time Space CM conversation. The sharper two-unknown theorem and simultaneous example are this continuation's extension. No historical novelty is claimed for residual supports, minimal unsatisfiable cores, or finite-template intersection arguments.

PROVED/EXACT below: any one-unknown UNSAT residual has a source core of at most two rows; any two-unknown UNSAT residual has one of at most four rows; both bounds are sharp. One fixed globally UNSAT seven-variable, nine-row source realizes minimum core sizes 1,2,4 in three separate static levels, beginning with a complete assignment that violates exactly one row.

COMPUTATIONAL: exhaustive finite-template enumeration verifies the core sizes and counts 12 one-unknown semantic relations and 157 two-unknown relations. The proof of the four-row upper bound is symbolic and does not depend on the enumeration.

## 1. One unknown: exact support and a two-row certificate

For fixed values a,b define U(a,b)={x:C(x,a,b)}. If a=b, this is empty. For distinct a,b the support is one of the five singletons or the five doubletons

    {0,2}, {0,3}, {1,3}, {1,4}, {2,4}.

Write H for this ten-set family. Its doubletons form a five-cycle, hence contain no triangle.

Every nonempty intersection of H-members belongs to H. An intersection of at least one member is therefore either a singleton or doubleton. A surviving doubleton is represented by one source row. A surviving singleton is represented by at most two rows: choose one member containing the point; if it has a second element, choose a member excluding that second element. The intersection of no rows is D.

H has the Helly-2 property: a collection of its members with empty intersection has two disjoint members. To prove it, a singleton in a pairwise-intersecting collection forces all members to contain its point. Otherwise all sets are graph edges. Pairwise-intersecting edges without a common vertex necessarily contain a triangle, which this five-cycle does not have.

Thus the independent one-unknown instance is UNSAT iff either a fully fixed row is false, an incident row has empty support, or two incident rows have disjoint supports. A source certificate uses at most two rows. Two incompatible singleton rows make this sharp.

For reuse in arbitrary pinned contexts, the support has twelve possibilities: D, empty, five singletons, and five doubletons. All are realizable. Every two different supports can be distinguished by a context forcing the unknown to a value in their symmetric difference, because singleton supports are available. Therefore an exact source-free interface needs twelve distinguishable states, or four fixed binary bits. This interface task is stronger than returning the single decision bit. The four bits do not include source positions, addresses, supplied-value lookup, or the work needed to acquire the support.

## 2. Two unknowns: exact compatibility decomposition

Let x,y be the only unknown variables. Every row becomes one of:

1. A true or false constant.
2. A unary support in H (or empty) on x.
3. A unary support in H (or empty) on y.
4. A binary relation M_a={(x,y):C(x,y,a)}, for a fixed value a.

Let S_x and S_y be the intersections of the unary supports. Let J be the set of fixed values occurring in binary rows. Then the entire feasible relation is

    S = (S_x x S_y) intersect (intersection over a in J of M_a),

unless a false constant row has already made it empty. The residual is UNSAT exactly when S is empty. Separate nonempty projections onto x and y are not sufficient; their joint compatibility matters.

Each M_a is the six directed arcs of a four-vertex path. For example M_0 has unordered edges {1,2}, {1,4}, and {3,4}. For distinct a,b, M_a intersect M_b is either empty or exactly two reversed ordered pairs (u,v),(v,u). This follows directly from the unary table: C(x,y,a) and C(x,y,b) require U(x,y) to be the doubleton {a,b}; each permitted doubleton occurs for exactly one unordered pair {x,y}.

## 3. The sharp four-row theorem

Theorem. Every strict-C5 residual with exactly two unknown variables that is UNSAT has an UNSAT subcollection of at most four original rows.

Proof. A false constant or empty unary row is a one-row certificate. If the x-unaries or y-unaries alone conflict, Helly-2 supplies a two-row certificate. Hence assume S_x and S_y are nonempty.

If there are no binary rows, S_x x S_y is nonempty, so the residual is SAT.

If at least two distinct binary rows occur, choose M_a and M_b with a != b. If their intersection is empty, they form a two-row core. Otherwise it has only two candidate ordered pairs. Because the full residual is UNSAT, some additional source row rejects the first pair and some additional source row rejects the second. The chosen two binary rows plus those at most two additional rows are UNSAT. They may be unary or binary. Thus four rows suffice.

It remains to handle exactly one distinct binary relation M_a. Duplicate copies do not change semantics.

If S_x=D, no x-unary row is needed. S_y is represented by at most two y-unary rows, so M_a plus those rows is a core of size at most three.

If S_x is a doubleton, it is represented by one x-unary row. S_y is represented by at most two y-unary rows. Together with M_a this gives at most four rows.

If S_x={p}, at most two x-unary rows force it. When p=a, M_a accepts no pair with x=p, so these at most three rows are already UNSAT. When p != a, the possible y-neighbors are U(p,a), which is itself a member of H. The intersection of U(p,a) with all y-unary supports is empty. Helly-2 supplies either two incompatible y-unaries, already a two-row core, or one y-unary disjoint from U(p,a). In the latter case, use the at most two x-unaries, that one y-unary, and M_a. Again at most four rows suffice. This exhausts the cases. QED.

Sharpness. The four rows

    C(x,a3,a4), C(x,a1,a2), C(x,y,a1), C(x,y,a4)

under supplied values ai=i have supports

    x in {0,2}, x in {0,3}, M_1, M_4.

The unary intersection forces x=0, while M_1 intersect M_4 contains exactly (2,3),(3,2). Therefore all four rows are UNSAT. Delete each row in the displayed order and use, respectively, witnesses (x,y)=(3,2),(2,3),(0,1),(0,2). Each witness satisfies all other rows. Thus the four-row residual is minimally UNSAT and its minimum source core has size four.

## 4. A globally UNSAT source realizing mu_0=1, mu_1=2, mu_2=4

To ensure the original unpinned formula is itself UNSAT, introduce five anchors a0,...,a4 and impose the five ordinary source rows

    C(ai,a(i+1),a(i+2)), i=0,...,4 (indices modulo5).

Add the four rows in the sharpness construction. There are seven variables and nine rows in total.

Every pair of anchor names appears in an anchor row, so any satisfying anchor assignment gives five distinct values. The complement of each permitted triple is an edge of a five-cycle. A bijection preserving all five triples is therefore an automorphism of that five-cycle, hence a rotation or reflection. There are ten anchor frames. The four remaining rows are contradictory in the identity frame, and applying a common rotation or reflection preserves C. They are consequently contradictory in every permitted frame. The original source is globally UNSAT.

Use the full reference assignment

    (a0,a1,a2,a3,a4,x,y)=(0,1,2,3,4,2,3).

All five anchor rows are true. Of the four other rows, only C(x,a1,a2) is false. Thus the fully specified level has minimum source core mu_0=1.

For the independently started one-unknown level, remove only x's value and keep y=3 and ai=i supplied. Two rows reduce to

    C(x,a1,a2): x in {0,3},
    C(x,y,a1): x in {2}.

They conflict. Every individual row has an extension, so mu_1=2.

For the independently started two-unknown level, remove x and y's values and retain only ai=i. The sharp four-row construction applies, so mu_2=4.

No machine is asked to carry information between these levels. This is one mathematical family of separately presented residual instances. The relation among the levels supplies an analysis of how the smallest source obstruction changes, without summing their separate execution costs.

## 5. Distinguishable two-unknown relations

Closing the 25 nonempty atomic residual relations (ten unary relations on each variable and five binary M_a) under intersection gives 157 distinct relations, including the full relation and empty relation. The exhaustive finite computation found this size distribution:

    cardinality 0:1; 1:25; 2:60; 3:10; 4:35; 5:10; 6:5; 10:10; 25:1.

Any two different relations are distinguished by a pinned context forcing a specific pair in their symmetric difference. Thus the finite class has 157 context equivalence classes and requires eight fixed bits for a source-free exact reusable relation summary. A 25-bit truth table is sufficient but not information-minimal for this strict template. Exact one-bit decision is a different output contract.

This count is not needed to prove the source-core theorem. It is an additional exact finite characterization checked by exhaustive closure, not by sampling. It does not prove an eight-bit workspace lower bound for every offline solver that may reread its source.

## 6. The source-core hierarchy has a polynomial ceiling

For a fixed number r of unknown variables, define H_r to be the largest minimum source-core size among UNSAT residual instances with r unknowns. The proved first values are H_0=1, H_1=2, H_2=4.

This does not permit an exponential extrapolation. There are at most

    1 + 10r + 5 binomial(r,2) + binomial(r,3)

distinct nontrivial residual row types. The terms respectively cover an empty row, the ten nonempty unary supports per unknown, the five M_a relations per unordered pair, and the single symmetric C relation per unordered triple. A minimally UNSAT core cannot contain two identical residual row types or a true constant. Also one can select a violated row per one of the 5^r assignments. Hence on an input with m rows,

    minimum source core <= min(m, 5^r,
        1 + 10r + 5 binomial(r,2) + binomial(r,3)).

In particular H_r=O(r^3). This is a bound on source support, not on the number of inference steps or the computational cost needed to establish that the selected rows are incompatible. A stronger unrestricted lower-bound measure must capture that acquisition or inference work.

## 7. Acquisition and the T_q distinction

A small source core is a certificate existence statement. Finding its row positions and evaluating the relevant supplied values can still require input access. Conversely, a source row can reject many candidate assignments at once. Core size is not the number of assignments an unrestricted algorithm must individually enumerate.

For fixed C5 and one or two unknowns, the finite residual relation can be accumulated using a fixed finite transition table, once normalized rows are available. Whether row normalization is O(1), logarithmic, or requires physical tape travel depends on the given input and assignment layout. No exact native time/space/CM optimum is asserted here.

The compact T_q forbidden-region language in the separate report is different. Its input contains a circuit H defining an instance-dependent tournament on q=2B+1 letters, and its question has one unknown x with two ordered-R clauses. The SAT reduction can have exponentially large q in the compact circuit description. One alphabet-valued unknown then packages many Boolean choices. Its lower bounds do not imply that fixed symmetric C5 with one unknown is difficult, and the present finite C5 analysis does not refute that compact-language lower bound. The reduction, encoding length, and simultaneous resource model must be retained before combining the results.

## 8. Validation and provenance

Two inline finite-template runs executed before this standalone audit was assembled. The first enumerated all minimal zero intersections of the 25 atomic residual relations through size six, obtaining size2:75, size3:230, size4:10, size5:0, size6:0. A size-six preliminary bound follows by representing each unary intersection with at most two rows and the binary intersection with at most two rows; the symbolic theorem above improves the universal bound to four. The second run computed the complete closure and its 157 relations. These runs were not rerun merely to generate another identical record.

The standalone script has template, global, and all stages. The new global stage independently checks every one of 5^7 assignments to the nine-row original source, all ten anchor frames, the unique false reference row, the exact minimum cores at all three separate levels, and a satisfying witness for every deletion of one of the four residual rows.

The global stage and its raw output are separate files. The template-stage raw record preserves the results of the earlier executed inline checks. Running the script with --stage all reproduces all checks. This is an executable finite audit, not a formal proof-kernel verification.

## References and related work recovered

1. Current strict source definition: research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md, section3.1; fetched blob a886f3387a8676b9cc86afbf3bebf22630109d49.
2. The recent one-unknown discussion already gave the strict-C5 two-row bound. The separate file /workspace/scratch/d4a6300046d1/T5_Reverse_Unfixing_Core_and_Acquisition_2026-11-22.md was read in full. Its mu_r=r+1 path construction uses ordered R, explicitly defined in its section3; it is not a universal bound for symmetric C.
3. /workspace/scratch/d4a6300046d1/T_q_FLMV_and_CM_Forbidden_Regions_2026-11-22.md, sections1-6, read for its actual compact circuit-defined tournament language and memory hypotheses.
4. Sharma and Velusamy, Characterizing Streaming Decidability of CSPs via Non-Redundancy, ESA2026, https://drops.dagstuhl.de/storage/00lipics/lipics-vol388-esa2026/html/LIPIcs.ESA.2026.131/LIPIcs.ESA.2026.131.html . Theorem1 connects non-redundancy to single-pass streaming space for its shift-allowed CSP model, with a separate positive-Boolean extension. It is relevant context, not a theorem about unrestricted RAM algorithms or an automatic lower bound for positive non-Boolean C5.
5. Dev Gupta, Genc, and O'Sullivan, Explanation in Constraint Satisfaction: A Survey, IJCAI2021, https://ijcai.org/proceedings/2021/0601.pdf . Definitions of minimal conflicts and source unsatisfiable cores; no unrestricted resource lower bound imported.
