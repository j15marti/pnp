COREGRAPH53 | 2026-10-17 05:48 UTC / 14:48 KST | P versus NP OPEN.

PROPOSE BEFORE SEARCH: (A1) A-specific predecision checkpoint compression; (A2) semantic dependency slicing; (B1) reused-predicate graph vertex-cover factoring; (B2) explicit biclique-cover compression.

SEARCH: Primary Liu ICALP 2018 Algorithm 4; Fortnow-Lipton-van Melkebeek-Viglas JACM 2005 Corollary 5.8; Konig matching/vertex cover. Latest repository reports read: GUARDDIVERSITY52, SEMANTICEDGE1, CERTSLICE1, HUBSUNFLOWER49, SHAREDRESERVOIR1, RANKDROP-FACTOR1, GLUECOVER1, SEMQUOTIENT38.

BUILD, PROVED/EXACT in restricted predicate graph model, independent review pending: For any graph G=(V,E), vertex cover C, predicates P_v and N(W) the neighbor set,
AND_{uv in E}(P_u OR P_v) = OR_{T subset C}[AND_{v in T} P_v AND AND_{w in N(C minus T)} P_w].
Proof: in any satisfying evaluation choose T as the true predicates in C; every neighbor of a false C predicate must be true. Conversely each edge meets C and is satisfied by its true endpoint or by a mandated neighbor. If each P_v is a clause of width at most 3, all at most 2^|C| residual branches remain at-most-3CNF, with O(2^|C| poly(N)) total generation and polynomial workspace. For bipartite G choose min vertex cover C in polynomial time, |C|=maximum matching m. If every edge comes from (P_u OR y_e) AND (P_v OR NOT y_e) with a fresh degree-two mediator and width(P)<=2, existential elimination and witness reconstruction are exact. For m disjoint edges 2^m positive-predicate DNF terms are necessary; this is NOT a SAT lower bound. Provided biclique cover of b pieces yields 2^b branches; complete shared reservoir has b=1.

TESTS: 528 matching/cover and 528 branch-size checks, 13,628 pointwise formula checks, 22,861 witness checks, 1,600 brute mediator checks, all pass. Script SHA256 de7a49f5b72028a8adc39efcb1f2e1d955d4f07263757f08c006bff8814765ec, seed 202610170548. Necessary-premise failures: same-sign mediators, reused mediators, third mediator occurrence.

PROOF DAG A: P=NP -> polynomial SAT A [ESTABLISHED]; A -> all-input recursively iterable fully charged SAT contraction [OPEN]; favorable recurrence -> forbidden FLMV joint time-space endpoint [ESTABLISHED conditional]. NEXT A: predecision A-specific factored checkpoint SAT child constructor with exact gluing and charged access.

PROOF DAG B: Liu BR/DLS and scoped local gains [ESTABLISHED]; COREGRAPH53 template factoring [EXACT SCOPED]; full globally amortized 38-type improved deterministic 3SAT base [OPEN]. NEXT B: globally charge 2^m / 2^b factor branches against signed characteristic gain, preserving stopping/overshoot, all original clauses, no duplicated petals.

RETIRED: timing/hash padding races, status-only oracle adaptation, UWI common-input as assumed, untransported proof-system bounds, representation explosion as runtime.

ROOT main.tex still has an omitted-body placeholder and unbalanced ownership markers. No root update. Full local report and runnable evidence bundle preserved for publication recovery.
END_COREGRAPH53_STATUS_READBACK