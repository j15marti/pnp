% LSPV-2 REPORT::TREEWIDTH-MINOR-GATE275::2026-10-31T08:12:00-07:00
# TREEWIDTH-MINOR-GATE275: full-interface width survives a Horn/Krom forest split

**31 October 2026, 08:12 PDT. Role: LSPV-2, Circuit & Reduction Builder.**
**Status:** PROVED/EXACT restricted graph lemma (mathematical peer review pending); COMPUTATIONAL independently checked finite experiments; arbitrary-A ARC and P versus NP OPEN.

## Corpus and priority
Read the 2026-10-30 09:48 universal-parameterized governance redirect, Universal Parameterized FLMV Contract1, AFFINE-SMALLBIAS-DESCENT-GATE2, CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1, root main.tex, AGENTS/CODEX/pnp-research skill and issue #3. Reused HORN-KROM-FOREST-INTERFACE274's *same source* transformation and three-resolution-step original-clause recovery. Cross-checked LSPV-3 GATE276, LSPV-5 REFEREE243, Schaefer 1978, Samer/Szeider 2010 and FLMV JACM 2005. Neither the preexisting affine theorem nor a treewidth obstruction proves arbitrary SAT hardness.

## Exact theorem, proof and four falsifiers
Let F be an ordered proper signed three-CNF with primal graph P(F) and width w. For every original clause C_j=(ell_j1 OR ell_j2 OR ell_j3), make private occurrence variables y_jk, the negative Horn clause H_j=(NOT y_j1 OR NOT y_j2 OR NOT y_j3), and Krom links (ell_jk OR y_jk) AND (NOT ell_jk OR NOT y_jk). Denote the conjunction T(F)=H AND K. The links uniquely enforce y_jk=NOT ell_jk(x), so for every original coherent x, exists y T(F)(x,y) iff F(x). Original source clauses are recovered by three ordinary resolution steps, and original SAT witnesses and UNSAT refutations lift.

**Proved restricted graph lemma:**
tw(P(H)) <= 2, tw(P(K)) <= 1, but
tw(P(F)) <= tw(P(T(F))) <= max(tw(P(F)),5).
Thus tw(P(T(F)))=tw(P(F)) whenever source width >=5.

**Proof:** Contract the distinct occurrence-link edges x_i--y_jk in P(T(F)). The Horn y-triangles contract to the exact original clause triangles, giving P(F) as a graph minor. For the reverse inequality, take a source width-w tree decomposition. Each three-variable clause support is a clique and lies in some bag. Attach to that bag a new leaf with its three original variables and its three private y variables. All graph edges are covered, the running-intersection property holds, and new bags have six vertices. Treewidth minor monotonicity and this explicit decomposition give the bounds.

**F1 falsified:** individually small component width does not bound the conjunction width. **F2 falsified:** signed occurrence splitting does not reduce effective source-primal width. **F3 falsified:** constant-factor shorter ordinary SAT children need not meet physical M<=sqrt(N). **F4 falsified as a purported universal lower bound:** high-width all-positive instances have instantly verified all-TRUE witnesses; high-width UNSAT mates have an eight-clause resolution core. Width is policy-specific, not a universal SAT lower bound.

## Same-source signed controls and computation
37 original formulas: 25 SAT, 12 UNSAT; 71,787 independent checker assertions PASSED and four deliberate certificate mutations rejected. For 3,899 original-clause pairs, all SS/SU/US/UU local extreme modes were verified; 1,283 original signed occurrences and their S/U inverses; 189 coherent flip transitions with four-count clause states; every eligible original-to-transformed assignment equivalence tested exhaustively for n<=7. The transformed resolution DAGs contain 1,350 source-indexed steps; all twelve source UNSAT decisions have exact refutation roots. A separate independent verifier checks all proof parents, pivots, and resolvents.

Paired YES/NO sources with identical unsigned clause supports and complete K_7 primal graph both yield exactly tw(T(F))=tw(F)=6 while tw(H)=2 and tw(K)=1. Both parents have physical N=21,712 bits, children M=2,776 YES or M=2,872 NO. Neither satisfies M<=sqrt(N). All 37 tested outputs failed this physical threshold.

The demonstrated state-dependent controller performs paid endpoint verification, then Krom, Horn, dual-Horn, certified XOR/GF(2), exact computed treewidth DP, and complete DPLL fallback: 12 endpoint, four Krom, two XOR, five width-DP, fourteen fallback cases. Crucially, optimum treewidth was *computed* with an exponential subset algorithm, not supplied for free.

## Resource ledger and limitation
Per-case raw data record input-character/literal reads, graph construction and adjacency probes, 1,048 treewidth-subset states, 3,244 elimination candidates, 53,808 graph probes, 107 policy recognitions, 96 failed policy switches, retained buckets, original/child physical characters, proof construction, reconstruction, source/child witnesses, 1,904 *offline* verification assignments, and observed host peak allocations. The controller measured 74,343 selected Python event proxies plus 44,685 construction/provenance proxies; baseline UP-DPLL visited 180 nodes and 5,795 literals. The different event counters are not machine-instruction comparable; no performance advantage or native FLMV time/space accounting has been established. Python explicitly retained sources, proof DAGs, and children. Guest A was not invoked.

On the no-padding dense original-clause family, the extracted original child has M=Theta(N) physical length. A compulsory call to arbitrary delayed correct SAT guest A_D on this child costs Omega(N^D), incompatible with the desired universal lambda=1/2 exponent coefficient for this particular compiler. It does not disprove any alternative compiler.

FLMV Theorem 5.7 has d*(241/200)=11642479/23232400>1/2. The proposed joint recurrence K'<=max(11/10,3/5+K/2), L'<=max(1/2,L/2) remains CONDITIONAL. No all-input hereditary A->Phi(A), budgeted power-short emitter, native matched indexed-TM implementation, or general strict-(2,2) indexed accessor exists here. P=NP and P!=NP remain OPEN.

## Reproducibility and handoff
Full producer, prior authenticated proof-DAG primitives, independently authored verifier, raw JSON and complete signed-source controls, standalone four-page TeX/PDF proof, BibTeX and SHA-256 manifest were verified locally and uploaded to persistent Library:
 /P-vs-NP/LSPV2_TREEWIDTH_MINOR_GATE275_2026-10-31.zip
Raw JSON SHA-256: a7a17bab50df8f098adf7427f5b990ae3da9d73397d4eafa5e38b55bbdbc1708.
The compact independent program in experiments/arc verifies the matched YES/NO minor theorem without repository dependencies. Next: implement a *fully charged, directly indexed, physically budgeted auxiliary-CNF full-interface DP emitter*, with discovery and source-to-child correctness certified under DELAY/COPY controls. Preserve exactly five existing roles, schedules and status.

Primary sources: Schaefer, STOC 1978, DOI 10.1145/800133.804350; Samer & Szeider, JDA 2010, DOI 10.1016/j.jda.2009.06.002; Fortnow et al., JACM 2005, DOI 10.1145/1101821.1101822; Davis & Putnam, JACM 1960, DOI 10.1145/321033.321034.

% END_OF_VERIFIED_REPORT::LSPV-2::TREEWIDTH-MINOR-GATE275