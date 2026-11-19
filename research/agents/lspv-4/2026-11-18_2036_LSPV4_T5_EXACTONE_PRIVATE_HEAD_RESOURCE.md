# LSPV-4: T5 exact-one Q private-head criticality and all-deletion resource audit

Date: 2026-11-18 20:36 PST (America/Los_Angeles). Role: PNP Time-Space Resource Auditor, historical Route A. Classification: PROVED/EXACT restricted theorems; COMPUTATIONAL original-constraint checks; CONDITIONAL other-algorithm transfer; OPEN unrestricted P versus NP.

## Pre-search candidate and falsifiers

Candidate: for each finite simple graph J=(U,E), with Q(x,y,z)=R(x,y) XOR R(x,z) and R(a,b) iff (b-a) mod5 in {1,3}, introduce one distinct private head h_e and Q(h_e,u,v) for each edge e={u,v}. L(J) is SAT exactly when J is 5-colorable. For an intrinsically critical UNSAT source, all single-clause SAT deletion witnesses can be found with a shared, advice-free endpoint enumeration and exact original-source Q verification. Falsifiers: equal symbols/ties, reused heads, wrongly transferring binary-R source UNSAT, uncharged candidate acquisition/output or overclaiming a high-girth/unrestricted lower bound.

## Theorem 1: exact reduction, multiplicities and P comparison

For any endpoint letters a,b, the five private head choices satisfying Q(h,a,b) number w((b-a) mod5)=[0,4,2,2,4]. This was independently checked over all 125 value triples: 60 Q successes versus 20 P(x,y,z)=R(x,y)&R(x,z), intersection zero, including ties. Thus L(J) SAT iff J admits a proper 5-coloring. Each such coloring can be lifted by choosing the least valid private head for every edge, and every Q witness projects to a proper coloring. Counts are generally NOT preserved:

    #Q(L(J)) = sum_{proper 5-colorings c} product_{e={u,v}} w((c(v)-c(u)) mod5).

On the SAME ordered clauses P(h_e,u,v), the universal assignment endpoints=1, private heads=0 satisfies P for every J, including Q-UNSAT examples. This falsifies any interpretation of Q as a P relaxation.

## Theorem 2: intrinsically critical, arbitrarily high incidence-girth Q sources

If J is connected and edge-minimal non-5-colorable, L(J) is connected, Q-UNSAT and clause-minimal: deleting every single original Q clause yields SAT. If graph J has finite girth g, the clause-variable BIPARTITE INCIDENCE graph of L(J) has girth 2g; private heads are leaves. Erdős' high-girth/high-chromatic theorem, followed by deleting edges while retaining non-5-colorability and discarding isolates, supplies a connected edge-minimal 6-chromatic J_g with girth >g for every finite g. Thus Q has arbitrarily high INCIDENCE-girth intrinsically clause-critical sources. This is existential: no polynomial-time generator or critical-promise hardness follows. In the ordinary primal graph of each ternary Q source a clause creates a triangle, so high PRIMAL girth is NOT established. The older directed binary-R T5 edge-critical high-girth promise is a DISTINCT object and is not transferred.

## Theorem 3: advice-free simultaneous witness harvest

For an endpoint labeling c, let Bad(c)={e={u,v}:c(u)=c(v)}. For every edge e, L(J)-Q_e is SAT exactly when some c has Bad(c) subseteq {e}. If L(J) is UNSAT then Bad(c) cannot be empty; hence the necessary and sufficient condition is Bad(c)={e}. For edge-critical J all edges have such a coloring.

A uniform algorithm authenticates the actual source records, canonical IDs, distinct named triple variables, one fresh head per edge and no head used as a target; otherwise it rejects the restricted-specialist input as OUT-OF-SCOPE rather than issuing a false label. It constructs J, fixes one endpoint color 0 using exact T5 fivefold rotation symmetry, enumerates all 5^(u-1) normalized endpoint colorings, examines all edges stopping at a second bad edge, and for each previously unwitnessed single-bad edge e constructs all private head labels by testing 0..4, verifies the full ORIGINAL Q source with clause e omitted, writes the complete (e,witness) record to a write-only stream, and marks e seen. If an e is missing, it reports missing witnesses, never guesses them. All candidate/failed trials and source checks are charged.

Canonical word RAM, O(log(N+u+m))-bit words, N encoded input bytes read-only, m edge/head clauses, u endpoint vertices, complete witness stream write-only:

    T_RAM = O(N + m*5^(u-1) + m*(u+m)).
    S_live = O((u+m)*log(N+u+m)) writable bits.

All m output witnesses may contain Theta(m*(u+m)) symbols, counted in time and external output but not silently retained as writable RAM. A physically materialized source requires N additional stored bytes. Self-reduction from a decision-only graph-color solver, preprocessing, indexing, cache, rejected guesses, verification and output all add to the same execution. Converting these word-RAM costs to exact bit/TM time can add polylogs. A speculative graph 5-coloring solver B can replace enumeration ONLY if its actual fully charged search, source access and memory are substituted. No superpolynomial lower bound is derived.

## Independent finite evidence

Standalone CPython script revision t5_lspv4_exactone_resource_v1, deterministic seed 20261118: 201 assertions passed. Five parity-feasible Q clauses (a,b,c),(a,b,d),(b,a,c),(b,c,d),(c,a,d) are Q-UNSAT by 5^4 exhaustive enumeration; deletion counts exactly [10,40,10,30,25]. Two abstract strict 4-vertex tournament orientations meet their XOR equations, showing parity alone insufficient. An odd target triangle for ONE shared head is also parity-UNSAT, even though the endpoints are 5-colorable.

K6 private-head Q lift: 6 endpoints, 15 private heads, 15 original Q clauses. Original Q UNSAT. Every one of 15 clause deletions has 120 endpoint colorings and exactly 120*5*2^21=1,258,291,200 complete Q assignments. The SAME-SOURCE P lift is SAT. The independent harvest script authenticated canonical 142-byte original Q source (SHA256 0cf0f8c3e50b1d8ee5a93ba7ab38785fc287ffcf7f37ef253d7a94224b2b0716), explored 3,125 normalized endpoint colorings, performed 28,314 equalities, emitted 15 full original-clause-verified deleted-edge witnesses, with 353 private-head candidate checks and 210 original Q clause verification checks. JSONL output SHA256 e6c2d18aa4fd2976f3236053710eb706bf9582362ce303c53ea7cd8d252cb687.

70 matched Q/P random/planted scopes, 193,750 complete assignments enumerated per language, 397,635 Q and 234,685 P original clause tests: random Q SAT 23/30, P SAT 0/30; planted-Q Q SAT 20/20, P SAT 2/20; planted-P P SAT 20/20, Q SAT 7/20. This is a seed-controlled finite sample, not a complexity statement. Original older 9-vertex/11-arc and 33-vertex/44-arc oriented R-T5 critical sources, when mapped to DIFFERENT Q fresh-head sources on their undirected edges, both yielded direct Q witnesses (DSATUR 10 and 34 nodes, original Q verification 11 and 44 clauses). Original 33-vertex R UNSAT not freshly reproved.

A reused-head guard Q(h,a,b),Q(h,b,c),Q(h,c,a) is UNSAT, although the endpoint triangle is properly five-colorable. The fresh-head condition must be checked. Experiment Python tracemalloc and symbolic slot counts are not physical machine lower bounds; the declared same-machine bound is analytical.

## Time-space polarity and barrier gates

Buss-Williams (2015), verified primary Figure 8.2/8.3, excludes general SAT in the specified DTISP(n^1.34070,n^0.5) random-access model (n^{o(1)} exponent convention). Thus a uniform general-SAT deterministic (1.33,.5) decider in that model is already excluded; earlier FLMV (2005) weaker deterministic/conondeterministic curves do not override it. None of these exclusions transfers automatically to exact Q critical promise inputs without a resource-preserving reduction. Free polarity, nondeterministic SAT witness, existential UNSAT proof, and all-branch coverage are distinct. The separate row/block n^.195/.65/.35 source layout is not shown to coincide with this graph lift.

DISJ: PASS as a restricted semantic reduction, no lower bound. Relativization: PASS warning; methods relativize. DTISP: PASS guard, no contradictory all-SAT claim. Deterministic configurations: NOT USED as runtime lower bound. Algebrization/Natural Proofs: no unrestricted promotion. OPEN: high-primal-girth Q, uniform critical-family generation, critical-promise NP-hardness, reused-head global realizability, binary R transfer, and all-algorithm SAT witness lower bounds.

## Reproducibility and ownership

Full dated mathematical report, two executable standalone scripts, raw exact JSON and K6 verified witness stream are available in user-facing local archive T5_EXACTONE_LSPV4_RESOURCE_AUDIT_20261118.zip. SHA256 of final main exhaustive script 290242bc830c1a6d596672e4cfd038481fbc1dee86f74aad1d7cce7f4cbcafbb, harvest script cc3a3575adbf26a4f1d85f782eb8a13f0f7a5b8b6ff86651a9dbf087c9528201. The original automated checkout preflight was not executed (no authenticated checkout). No foreign TMR living manuscript, old proof trackers, agents, states or schedules changed. Independent peer proof review OPEN. Manuscript ownership unchanged.

References: Erdős high girth/chromatic theorem https://doi.org/10.1002/jgt.1017 ; Krivelevich critical graphs https://doi.org/10.37236/1342 ; Buss-Williams https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf ; FLMV https://doi.org/10.1145/1101821.1101822 . Original local and peer corpus: LSPV-4/1936 block cube cover, LSPV-1/626 guard coverage, cross-track balanced60 (different relation).

Next: source-authenticate global T5 realizability with shared/reused heads beyond parity and degree tests; run cached elimination/width and algebraic controls with the same word-RAM ledger. P versus NP OPEN.
