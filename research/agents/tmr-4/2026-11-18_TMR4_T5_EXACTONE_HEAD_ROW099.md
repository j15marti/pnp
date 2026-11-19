# TMR-4/099: exact head-component quotient for T5 exact-one rows

**Date:** 18 November 2026 (Pacific). **Role:** TMR-4 / PNP Cost-Sound Abstraction. **Status:** PROVED/EXACT for the restricted identities below, COMPUTATIONAL for finite tests, OPEN for unrestricted source-decision lower bounds and P versus NP. Draft stacked on /098; no ownership, agent state or schedule changed.

## Original source and exact scope

A source is an explicit list of clauses Q(h,u,v) on original variables taking values in Z5, with pairwise distinct variable **names** in a clause. Equal assigned values are allowed. R(a,b)=1 exactly when (b-a mod5) is 1 or 3; Q(h,u,v)=R(h,u) XOR R(h,v). In particular, NOT R(h,u) includes ties. The parent source archive T5_Exact_One_Experiments_2026-11-18.zip establishes 60 accepted triples out of 125, against the older AND rule's 20/125, with disjoint accepted sets.

## PROVED/EXACT: head-component fiber factorization

For each first variable h, build undirected follower graph H_h, with edge {u,v} for each clause Q(h,u,v). An odd cycle in H_h is an authentic UNSAT certificate. Otherwise choose a deterministic bipartition (L_C,U_C) for each nontrivial connected component C of H_h. Fix a source-authenticated protected interface Z. Retain S consisting of all heads, protected variables, and every follower used with more than one head. Other follower vertices occur only in one H_h and can be eliminated *after* accounting for their extension multiplicity. Unprotected isolated variables contribute five values each.

For a fixed retained labeling α:S→Z5 and component C, define the factor
\[
F_C(\alpha)=
\sum_{e\in\{0,1\}}
\Bigl(\prod_{v\in L_C\cap S}[R(\alpha(h),\alpha(v))=e]\Bigr)
\Bigl(\prod_{v\in U_C\cap S}[R(\alpha(h),\alpha(v))=1-e]\Bigr)
(2^e3^{1-e})^{|L_C\setminus S|}
(2^{1-e}3^e)^{|U_C\setminus S|}.
\]
Here every bracket is a 0/1 indicator, not an advice bit. If i original variables are isolated and unprotected, the exact number of accepting original extensions of α is A(α)=5^i∏_C F_C(α). Exactly 5^(n-|S|)-A(α) original extensions reject. Summing A(α) over all five-letter α gives the full accepting count and its complement gives the full rejecting count.

**Proof.** Each follower edge requires opposite win bits relative to h, so all valid win-bit assignments of a connected bipartite component are the two partition orientations. For a given orientation, every eliminated follower has exactly two winning or three nonwinning letter choices, independent of every other component. Retained followers impose indicator checks. The two orientations yield disjoint full-letter assignment sets because each component contains an edge. No eliminated vertex occurs in two factors. Multiply independent extension cardinalities, then sum retained assignments. Pointwise labels for eliminated variables are NOT stored in the quotient, and no polynomial-width pointwise FBDD is inferred.

For private-disjoint rows r sharing z, the exact row summary is A_r(z), obtained by summing retained nonshared variables. Thus #F=Σ_z∏_r A_r(z). This is an exact evaluator, not a freely materialized table. Any incomplete UNSAT proof for even one z cannot be promoted to a full all-z refutation.

## Rotation quotient and SAME_REALIZATION costs

Global color translation α(v)↦α(v)+t mod5 preserves every Q clause. The extension count A(α) is translation invariant. If S is nonempty, fix one retained symbol to A and multiply the sum by five. This reduces 5^|S| retained tuples to 5^(|S|-1), a constant factor, not a polynomial-time uniform algorithm.

Build follower graphs by charged input reading, deduplication, BFS and bipartiteness testing. The deterministic sorted implementation charges O(m log m) source processing; a standard hash-adjacency implementation costs O(n+m) expected RAM operations for parsing/graph work, with all actual input bytes and malformed controls paid. Each queried α examines up to two orientations per component, scans at most O(m) follower occurrences, performs arbitrary-precision integer products on O(n)-bit counts, and accumulates the exact result. A safe bit-time envelope is poly(L+n+m)·5^|S|. Retaining the explicit graphs takes O((n+m)log(n+m)+L) bits plus O(n) for counters and assignments; this is a program-level bound rather than measured Python RSS. Streaming can trade paid rereads against storage. The exact source enumeration and all failing attempts remain charged.

For n^0.195 rows and n^0.65 blocks of size n^0.35, the parent per-fixed-z n^(0.845+0.35d+o(1)) seed bound still requires a sufficiently small d, paid indexing, and a separate all-z join. This factor theorem supplies no universal bound on |S| or shared z and therefore no (n^1.33,n^0.5 polylog n) algorithm.

## New finite two-row obstruction

Shared variables a,b,c,d, private p for row 1 and q for row 2:
- row 1: Q(a,b,c), Q(a,b,d), Q(a,b,p)
- row 2: Q(b,a,c), Q(b,c,d), Q(c,a,d), Q(c,a,q)

Each row individually has positive extension counts for 150 and 50 of the 625 shared z values, respectively; their supports have empty intersection. Complete six-variable source enumeration and exact factored row join both return zero. Deleting Q(a,b,c) yields exactly 60 satisfying six-variable assignments, agreed on independently. No free choice of one globally false row exists.

New executable controls (separate from the archived 2,320 + 600-run datasets): ten structural fixtures exhaustively enumerated in original five-letter semantics and compared with factor counts and orbit-normalized counts; 25 fixed-head/follower conditional fibers; all 625 two-row interface values; and a distinct letter-string verifier of ten full counts and the row deletion. All comparisons passed. Archive's independent control additionally revalidated all 236 deletion witnesses and 55,696 clause checks of the 283-variable finite fixture. Python traced allocation is explicitly not a mathematical peak RAM claim. Local evidence bundle includes code, JSON outcomes, SHA-256 manifest and this report.

## PROVED/EXACT corollary: unbounded incidence-girth critical UNSAT existence

For every fixed integer g there exists a clause-deletion-minimal UNSAT Q source with fresh private heads, no UNSAT subformula with at most g clauses, every per-head parity check feasible, and incidence girth >2g.

**Proof.** Erdős's 1959 high-girth/high-chromatic existence theorem yields a graph H with girth >g and chromatic number at least six. Choose an edge-minimal subgraph H' still not 5-colorable. Then H' is 6-chromatic and every single-edge deletion is 5-colorable. Replace every edge {u,v} with Q(h_uv,u,v), with fresh h_uv. The exact identity ∃h Q(h,u,v) iff u≠v makes the whole source UNSAT but every clause deletion SAT, with a full witness obtained by extending the corresponding 5-coloring. Any ≤g edges form a forest, hence a 2-colorable graph, and so their associated clauses are SAT. Private heads have degree one in the variable-clause incidence graph; every original cycle of length ℓ induces one of length 2ℓ, proving incidence girth >2g. This is an **existential family**, not a polynomial-time generator or an all-algorithm time lower bound. The archived Mycielski control has only fixed incidence girth 8, not this unbounded-girth property.

## Falsifiers and verification gates

Falsifiers: (1) odd H_h cycles permit source-local UNSAT; (2) dropping 2/3 multiplicities makes existential projections nonparsimonious; (3) independent per-head parity bits need not have any global T5-letter realization; (4) no bounded-clause obstruction list detects every high-girth critical UNSAT source.

DISJ: PASS as a cheap-source and nonlocality sanity check, not an algorithmic lower bound. Relativization: OPEN for unrestricted separation. Simultaneous DTISP: OPEN at the target resource pair. Deterministic configurations: PASS as upper-bound consistency only; no time lower bound. No algebrization or Natural-Proofs bypass is claimed.

Independent mathematical review, source-to-physical-TM replay and a uniformly compact complete strategy remain OPEN.

**Next dependency D4-T5-ROW-GLOBAL-REALIZABILITY-100:** source-discoverable, complete global five-letter joins after parity and private-follower contraction, tested on high-girth critical controls, with paid construction, failed branches, verifier, 5^q enumeration or proved symbolic replacement, output and SAME_REALIZATION peak storage. **P versus NP remains OPEN.**

### References
1. Erdős, P. Graph theory and probability. Canadian J. Mathematics 11 (1959), 34–38. Also proved in Diestel, Graph Theory, Chapter 11: https://www.math.uni-hamburg.de/home/diestel/books/graph.theory/preview/Ch11.pdf
2. Osthus, D., Prömel, H. J., Taraz, A. Almost all graphs with high girth and suitable density have high chromatic number. J. Graph Theory 37 (2001), 220–226. https://doi.org/10.1002/jgt.1017
3. Garey, M. R., Johnson, D. S., Stockmeyer, L. Some simplified NP-complete graph problems. Theor. Comput. Sci. 1 (1976), 237–267. https://doi.org/10.1016/0304-3975(76)90059-1
