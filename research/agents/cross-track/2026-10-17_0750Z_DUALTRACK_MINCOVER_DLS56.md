# DUAL-TRACK MINCOVER-DLS56
Date: 2026-10-17
Status: P versus NP OPEN.

## PROPOSE COMBINATIONS

Track A:
1. Replace complete semantic minimization by sound, incomplete, syntax-certified solver-specific slicing.
2. Require any successful contractor to inspect intensional program structure, since answer-only SAT access is eliminable and complete marked-deletion recognition is blocked by SEMANTICNONHALT1.
3. Treat TETRAFOLDGAP1 as a warning: multiplicity of fold classes is not work unless acquisition/coverage is charged.

Track B:
1. Strengthen COREGRAPH53 by replacing its 2^|C| vertex-cover subset expansion with the canonical minimal-vertex-cover DNF.
2. Charge each forced type-1-chain literal directly in Liu's DLS factor.
3. Use the resulting weighted minimal-cover polynomial to decide when graph factoring is genuinely favorable, and route unfavorable sparse graphs back to hypermatching/high-incidence branching.

## SEARCH / PRIOR WORK CHECK

Primary sources checked:
- S. Cliff Liu, ICALP 2018 / arXiv:1804.07901, chain covering-code DLS framework.
- S. Tsukiyama, M. Ide, H. Ariyoshi, I. Shirakawa, SIAM J. Comput. 6(3), 1977, DOI 10.1137/0206036: all maximal independent sets can be generated in output-polynomial total time and O(n+m) space. Complements are minimal vertex covers.
- Fortnow, Lipton, van Melkebeek, Viglas, JACM 2005: Track A forbidden-region endpoint remains available only after the missing contractor.
- Weiser 1981 and Necula POPL 1997 were checked as conceptual precedents for sound incomplete slicing / proof-carrying verification; neither supplies the missing SAT contraction theorem.

Project predecessors checked: COREGRAPH53, BICLIQUE-LEDGER55, HUBBRANCH_COORDGUARD54, SEMANTICNONHALT1, TETRAFOLDGAP1, and current main2 clean-core ledger.

## BUILD: MINCOVER-DLS56

Let G=(V,E). Associate to each v one Boolean predicate P_v. Define

    H_G = AND_{uv in E} (P_u OR P_v).

Let MVC(G) be the inclusion-minimal vertex covers of G.

### Theorem 1: canonical minimal-cover DNF

    H_G = OR_{C in MVC(G)} AND_{v in C} P_v.

Proof. If a term indexed by C holds, every edge meets C, so H_G holds. Conversely, under any satisfying evaluation, the set T={v:P_v=1} is a vertex cover. Every finite vertex cover contains an inclusion-minimal vertex cover C subseteq T, so the corresponding term holds.

Moreover this DNF is forced among exact DNFs whose terms are conjunctions of positive predicates P_v. For the satisfying assignment whose true set is exactly a minimal cover C, some exact positive term S must satisfy S subseteq C; soundness requires S itself to be a vertex cover, hence minimality forces S=C. Thus every minimal cover is required.

### Theorem 2: Liu-DLS weighted factor criterion, scoped

Assume:
- each graph vertex v denotes one fixed signed literal on a distinct positive type-1 chain;
- all selected type-1 chains are variable-disjoint;
- all original CNF clauses remain checked by the terminal SAT search.

For an unforced type-1 chain, lambda=3/7 and its local DLS cost is 7/3.

Forcing one designated literal true has local DLS cost:
- 16/9 if the designated literal is positive, ratio (16/9)/(7/3)=16/21;
- 5/3 if it is negative, ratio (5/3)/(7/3)=5/7 < 16/21.

Set alpha=16/21. In the branch indexed by C, the DLS cost is therefore at most alpha^|C| times the independent-chain baseline. Hence the total positive-factor DLS cost is at most

    Z_G(alpha) = SUM_{C in MVC(G)} alpha^|C|

times the baseline.

Thus Z_G(16/21)<1 certifies a strict DLS improvement in this scoped terminal model.

Because minimal vertex covers are complements of maximal independent sets, Tsukiyama et al. give output-polynomial enumeration with polynomial delay/overhead per branch and O(n+m) graph workspace. Therefore replacing COREGRAPH53's 2^|C| subset expansion by MVC enumeration does not hide exponential work beyond the branches themselves.

### Corollaries

1. Complete bipartite K_{q,p}:
   MVCs are exactly the two sides, so
       Z = alpha^q + alpha^p.
   This recovers BICLIQUE-LEDGER55 exactly.

2. Star K_{1,p}:
       Z = alpha + alpha^p.
   The first strict improvement occurs at p=6.

3. Clique K_r:
       Z = r alpha^(r-1).
   The first strict improvement occurs at r=10.

4. Disjoint union:
       Z_{G1 union G2} = Z_{G1} Z_{G2}.
   Therefore disjoint favorable components multiply without double counting.

5. Sparse path control:
   Z(P_n)>1 for n=2,...,12 in the exact audit. Positive-predicate factorization is therefore not the right mechanism for path-like sparse structure; route it to hypermatching / local correlation instead.

### Exact audit

Exhaustive over every simple graph through 6 vertices:
- 33,867 graphs;
- 2,131,018 graph-assignment equivalence checks;
- 149,446 minimal-cover necessity checks;
- zero failures.

The audit verifies the Boolean identity and irredundancy, not Liu's asymptotic algorithm.

## DECISION / ALLOCATION

Track A:
SEMANTICNONHALT1 and TETRAFOLDGAP1 jointly argue against complete semantic deletion and raw fold enumeration. Redirect to INTENSIONAL, SOUND-INCOMPLETE, PROOF-CARRYING transformations: local syntactic rewrites or checkpoint summaries whose safety certificate is cheap to verify and whose aggregate effect provably creates ordinary SAT children of size N^(lambda+o(1)), lambda<1. The missing theorem remains a hereditary all-input A -> Phi(A) contraction. P versus NP remains OPEN.

Track B:
Adopt MINCOVER-DLS56 as the canonical graph-factoring ledger. Stop enumerating arbitrary vertex-cover subsets when minimal covers suffice. Use:
- Z_G(16/21)<1 => factor by minimal covers;
- sparse/spread graphs => hypermatching / direct correlated blocks;
- high-incidence graphs => HUBBRANCH / LOCALPATTERN branching.
Highest-value next lemma: integrate these three choices into one provenance-aware Liu Algorithm 4 recurrence and prove a strict global base below 1.3279235672158634... with the corrected chain catalogue and stop/overshoot accounting.

## PROOF DAG

Track A:
P=NP -> polynomial SAT decider A [ESTABLISHED]
A -> fully charged hereditary smaller-instance contractor [OPEN]
contractor recurrence -> (6/5,1/2) neighborhood [CONDITIONAL/ESTABLISHED ALGEBRA]
FLMV forbids endpoint [KNOWN THEOREM]

Track B:
Liu BR/DLS [KNOWN THEOREM]
local pruning/correlation/mediator gains [SCOPED EXACT]
MINCOVER-DLS56 [SCOPED EXACT]
global integrated recurrence below Liu base [OPEN]

RETIRED / DO NOT REPEAT WITHOUT NEW THEOREM:
timing/hash races; answer-only oracle necessity; complete semantic deletion; trace-length/fold multiplicity as hardness; multiplying overlapping motifs; assuming UWI common-input obstruction; untransported Resolution/CP/PC/SoS bounds.

END_MINCOVER_DLS56_READBACK
