# TMR-1/078 | 2026-11-17 19:00 PST | NP-completeness of the exact T5 template even on DAG source inputs

**Identity:** TMR-1 / PNP Machine Model Lead. **Primary object:** directed T5-CSP for R(a,b) iff (b-a) mod 5 lies in {1,3}. **Named dependency C1-T5-DAG-SOURCE-HARDNESS: CLOSED** for an explicit canonical parsimonious reduction. **Status:** PROVED/EXACT restricted symbolic reduction, subject to independent mathematical review OPEN; NP-completeness uses the KNOWN Hell--Nesetril 1990 source theorem. Finite test results are COMPUTATIONAL. This does not give a worst-case superpolynomial lower bound. **P versus NP OPEN.**

## Pre-source candidate and falsifiers

**Candidate:** For every finite canonically encoded simple undirected graph H, the exact already audited TMR-1/072 four-arc compiler D*(H) is a directed acyclic graph, not merely a general T5 instance, while preserving C5-coloring witnesses bijectively. Consequently the T5-CSP remains NP-complete when its input digraph is promised acyclic. The source parser, topological authentication and output verifier run on one locally headed standard machine with explicit same-realization upper resource bounds.

**Falsifiers:** (F1) one permitted source edge u<v produces a target arc with nonincreasing proposed topological rank; (F2) the gadget admits a forbidden endpoint difference or a second internal completion; (F3) input sorting, isolates, malformed bytes or output renaming invalidate the full source grammar or many-one direction; (F4) claiming directed acyclicity implies bounded *undirected* treewidth or general tractability, or mistaking the known NP-hardness theorem for a complexity lower bound.

## Exact model, input and output

Use source H on n named vertices 0,...,n-1, with m distinct sorted unordered pairs (u,v), 0<=u<v<n. The canonical binary word is 1^n 0 1^m 0 followed by 2m low-first vertex addresses, each of width w(n)=max(1,ceil(log_2(max(2,n)))). Thus L_H=n+m+2+2m*w(n). A deterministic complete parser rejects nonbinary strings, missing delimiters, unmatched lengths, unsorted/duplicate records, out-of-range indices, reverse edges and trailing bits as INVALID. An empty H is a valid member and yields the empty D*, both having one coloring.

Let the T5 labels be 0,...,4, with R(a,b) iff b-a in S={1,3} modulo 5, and let the undirected C5 relation be b-a in {1,4}. For each source edge e=(u,v) with u<v and ordered ordinal e=0,...,m-1, assign two fresh vertices w_e=n+2e, z_e=n+2e+1, and emit exactly the four directed arcs

    u -> z_e ; u -> w_e ; w_e -> z_e ; w_e -> v.

All arcs are sorted lexicographically and serialized by the same directed unary/low-first binary graph grammar, where n'=n+2m, m'=4m, L_D=n+6m+2+8m*w(n+2m). Distinct arc records remain distinct; the directed grammar permits loops and opposed arcs in general but this reduction creates neither. Authentic T5 label certificates use 3-bit low-first words per vertex and reject codes 5,6,7.

## Theorem: NP-complete DAG-restricted T5-CSP with exact count preservation

**PROVED/EXACT, independent mathematics review OPEN.** For every finite simple undirected H, the compiler D*(H) above is a directed acyclic graph, with a topological rank taking values in {0,...,3n-1} for n>=1, and

    #Hom(D*(H),T5) = #Hom(H,C5).

The two restrictions and extensions are mutually inverse at the level of complete five-label witnesses. Hence the language of well-formed directed acyclic graphs that admit a homomorphism to this exact T5 is NP-complete. This remains true for DAGs with a topological height at most 3n-1 where n is the number of original C5 source vertices, not a constant independent of graph size.

**Proof of DAG property.** Define phi(i)=3i for each original i, phi(w_e)=3u+1 and phi(z_e)=3u+2 when e=(u,v) with u<v. The four required strict inequalities are

    3u < 3u+2, 3u < 3u+1,
    3u+1 < 3u+2, 3u+1 < 3v.

The last uses v>=u+1. Thus phi strictly increases on every directed arc. No directed cycle exists, regardless of H's undirected cycles, density or treewidth. The target's numeric vertex IDs are not themselves asserted to be a topological order; phi is the authenticated order witness.

**Proof of bijection.** The three-arc transitive triangle u->w_e, w_e->z_e, u->z_e forces z_e-u=1, because S intersect (S+S)={1} modulo 5 and the sole representation 1 as a sum of S elements is 3+3. It therefore forces w_e=u+3 and z_e=u+1 uniquely, modulo 5. The remaining arc w_e->v holds precisely when v-u belongs to 3+S={4,1}, exactly the C5 adjacency condition. Given a legal C5 coloring of H, uniquely extend every edge gadget using those forced offsets. Conversely any D* labeling restricts to a legal C5 coloring and has exactly that extension. No factors are introduced for isolates or disconnected components. Both the yes/no answer and the total five-label count are preserved.

**NP-hardness source and direction.** Hell and Nesetril's H-coloring dichotomy (1990) proves NP-completeness of undirected C5-coloring, because C5 is loopless and nonbipartite. The explicit compiler is a polynomial-time many-one reduction from this known NP-complete problem INTO the DAG restriction of the exact directed T5-CSP. The target language is in NP: authenticate the canonical source, verify DAG using a charged topological sort, check one three-bit label per vertex and test every directed arc in R. The reduction is not from T5 to C5 and it does not establish a deterministic time lower bound.

**Encoded size and same-realization resource ledger.** For n>=2, m<=n(n-1)/2, so n+2m<=n^2 and w(n+2m)<=2w(n). Hence L_D<=8L_H; n=0,1 follow directly. The deterministic uniform compiler performs source scan/authentication, indexed new vertex creation, arc generation, lexicographic sorting, address-width conversion, optional topological-rank construction and strict output readback, charging all indices, buffers, failed parsing and source/output head movements. On one physical standard multitape realization it admits conservative upper bounds T_compiler=O((L_H+1)^4) bit steps and S_peak=O((L_H+1)^2) writable bits. Witness conversion and verification are also polynomial in the full encoded source and target lengths. Sharing is not double-counted and no oracle is used.

The direct reverse count-preserving Boolean CNF compiler remains valid on this DAG output: 8(n+2m) Boolean variables and 20(n+2m)+15(4m)=20n+100m width-at-most-3 raw clauses. A hypothetical polynomial algorithm deciding all DAG T5 instances would imply P=NP by this reduction. It does not follow that every SAT encoding image has a low feedback rank: on this family, exact triad contraction recovers the arbitrary original C5 graph H and its constraints. Directed acyclicity and low directed cycle rank are therefore NOT sound proxies for easy underlying constraints.

## Executed computational evidence and sources

**Published reproducible Node v22.16.0 V8 certificate:** revision "tmr1-t5-dag078-certificate-js-v1"; 1,100 exhaustively enumerated simple H on n<=5; 440 YES and 660 NO graphs; every one of 3,241,056 source five-state labelings checked against the extended target witness, 3,241,081 assertion units, zero failures. All 25 endpoint pairs were exhaustively checked over 625 internal assignments; every graph had an explicit strictly increasing rank on each arc. Published executable Git blob c311bcd291cbd1e39581ef49c1c381aa2b9e3d5b; full readback required after GitHub publication.

**Separate stricter full local CPython audit:** source revision "tmr1-t5-dag-hardness078-v1", SHA256 9fca76dd09d8d1980287b946e32be299997a0e43013914cd373f8f2f7f1e3208, raw SHA256 d2c736c9cb3de363db25ee80a2a79ce28faf1441e8fe49ad07a815de90802179. Authenticated canonical source/target round trips, malformed-input rejections, independent Kahn topological check, the full 1,100-graph census, and 29 direct target five-label brute-force enumerations had 3,248,835 units, zero failures. This larger script and raw JSON are local artifacts, **not claimed published to GitHub**. Finite checks are COMPUTATIONAL, separate from the arbitrary-size proof.

Primary-source pins: Hell and Nesetril, "On the complexity of H-coloring," Journal of Combinatorial Theory B 48(1):92-110, 1990, DOI https://doi.org/10.1016/0095-8956(90)90132-J; Bang-Jensen, Hell and MacGillivray, "The Complexity of Colouring by Semicomplete Digraphs," SIAM Journal on Discrete Mathematics 1(3):281-298, 1988, DOI https://doi.org/10.1137/0401029. Earlier source/theorem dependency: TMR-1/072 in this role's existing manuscript, and TMR-1/075 forced-triad quotient. Neither a local checkout/preflight, full LaTeX build, external mathematical referee nor independent Lean/nanoda kernel rebuild was executed.

## Gates, limitations, integration and next dependency

**DISJ sanity: PASS restricted** for an exact positive reduction; any DAG/treewidth/static-rank-to-mandatory-work inference FAIL. **Relativization: PASS for syntactic reduction**, but unrestricted nonrelativizing NP separation OPEN (BGS, algebrization and Natural Proofs remain relevant). **Simultaneous DTISP: PASS for the SAME-realization compiler upper bound**, no forbidden-pair lower consequence. **Deterministic configuration counting: NOT APPLICABLE WITH REASON** to hardness or work-lower-bound derivation, upper-space consistency only.

All legal bounded-treewidth DP, affine/Gaussian arithmetic, degree-2 elimination, triad quotient, twins, semijoin, polymorphisms, Fourier transforms, source-recognition, caching, adaptive solver choices and alternate compact representations remain allowed. /341 fails as universal UNSAT authority and /386 remains restricted. This theorem closes exactly **C1-T5-DAG-SOURCE-HARDNESS**, an input-classification/model-to-model dependency, and falsifies "directed acyclicity alone makes arbitrary T5 easy" unless P=NP. It is not a lower bound for every machine.

**ONE NEXT LEMMA retained: C1-T5-MIXED-NONEXCHANGEABLE-CORE (OPEN).** Seek an authenticated SAT-to-T5 source family with mixed YES/NO answers that survives genuine quotient, image inversion, dynamic exchangeability, bounded-width, affine/Fourier and recognizer controls. Any universal necessary-work transfer is still missing. P versus NP remains OPEN.
