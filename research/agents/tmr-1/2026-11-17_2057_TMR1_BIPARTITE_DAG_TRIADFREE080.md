# TMR-1/080: Parsimonious NP-completeness on bipartite triangle-free DAG T5 instances
Date: 2026-11-17 20:57 PST. Identity: TMR-1 / PNP Machine Model Lead.
Status: PROVED/EXACT reduction with independent mathematical review OPEN; NP-completeness KNOWN from Hell-Nešetřil plus this exact reduction; finite tests COMPUTATIONAL. P versus NP OPEN. Draft branch publication, not a main merge.

## Named dependency C1-T5-TRIADFREE-ACYCLIC-BIPARTITE-HARDNESS080
Candidate fixed BEFORE source/corpus audit: Every canonical finite simple undirected H has a parsimonious five-arc H->D(H) reduction into an underlying-bipartite, triangle-free, directed-acyclic T5-CSP source, with constant-factor canonical binary length. This explicitly falsifies the proposal that an all-input solver can rely on lack of directed cycles, forced triangles, or bipartiteness ALONE to obtain polynomial time.

Potential falsifiers: (1) a wrong endpoint relation or multiple internal completions; (2) identification of auxiliaries across edges or loss of original labels; (3) a directed cycle/undirected odd cycle introduced by shared endpoints; (4) failing total source authentication, bit-length bound or malformed-source handling. All resolved below.

## Exact fixed-template source and gadget
The fixed target has alphabet Z5 and R(x,y) iff y-x modulo 5 is in S={1,3}. C5 is the *undirected* five-cycle with adjacency differences {1,4}, not the target directed tournament. Source H has n vertices 0,...,n-1 and m strictly sorted distinct edges {u,v}, u<v.

For each edge e=(u,v), create three private vertices a_e=n+3e, b_e=a_e+1, c_e=a_e+2; add exactly five directed arcs:
  u->a_e, a_e->b_e, b_e->c_e, u->c_e, c_e->v.
The first four arcs specify a directed three-step path u->a->b->c plus u->c. Their constraints imply c-u belongs both to S and 3S; 3S has sum multiset [0:3,1:0,2:3,3:1,4:1]. Thus S intersect 3S={3}. The *only* realization of 3 as a sum of three members of S is 1+1+1 modulo 5. Consequently c=u+3, a=u+1, b=u+2, uniquely. The last arc c->v is satisfied iff v-u modulo 5 belongs to 3+S={4,1}. This is exactly undirected C5 adjacency.

For any fixed endpoint assignment, the gadget has exactly one extension iff the endpoints are C5 adjacent, and zero otherwise. All auxiliaries are private. Restriction of any T5 coloring to the original n vertices is a C5 coloring; every C5 coloring has the unique extension a_e=u+1,b_e=u+2,c_e=u+3 for every e. Hence for all H, including isolated vertices and n=m=0,
    #Hom(D(H),T5) = #Hom(H,C5)
and YES iff YES. This is a witness-level bijection (parsimonious reduction), unlike /071's 2^m factor.

## Strong structural restrictions and proof
The target *input graph* D(H) has n+3m vertices and 5m arcs. A topological rank is phi(u)=4u for every old vertex u and phi(a_e)=4u+1, phi(b_e)=4u+2, phi(c_e)=4u+3 for e={u,v}, u<v. Every arc increases phi, because phi(v)>=4u+4. Thus D(H) is a DAG despite possibly cyclic undirected H. It is underlying-bipartite with partition (all old vertices and each b_e) versus (all a_e and c_e). Every arc crosses the partition. In particular, the underlying graph has no triangle and the forced-transitive-triad preprocessor /075 cannot contract a single triangle in D(H).

The underlying graph may contain 4-cycles, so the result does NOT establish high girth or small treewidth. The quotient under a *triangle-only* contraction has k=n+3m, e=5m, c=c_H and rho=e-k+c=2m-n+c_H, where c_H includes original isolates. For m=0, rho=0. It can be linear or superlinear. This is not a mandatory-work lower bound, since legal global C5 source-aware and other algorithms remain admissible.

Hell and Nešetřil (1990), On the complexity of H-coloring, Journal of Combinatorial Theory B 48:92-110, DOI https://doi.org/10.1016/0095-8956(90)90132-J, proves NP-completeness for irreflexive nonbipartite fixed undirected H, including C5. Therefore the just-proved polynomial reduction establishes NP-hardness for T5-CSP even on the above simultaneously DAG, underlying-bipartite, triangle-free promise class. Membership in NP follows from n_D five-symbol certificates and direct arc checking. No assumption about Boolean 3SAT is needed for this classification.

## Authenticated canonical bit and exact output
On a finite simple undirected H encode 1^n 0 1^m 0 followed by m pairs (u,v) sorted lexicographically with u<v<n, each address in w(n)=max(1,ceil(log2 max(2,n))) low-first bits; exact L_H=n+m+2+2m*w(n). The target writes the same headers and all 5m directed arcs in lexicographic order using w_D=w(n+3m), with exact length
    L_D = n+8m+2+10m*w_D.
Because m<=n(n-1)/2, for n>=2, n+3m<=n+3n(n-1)/2 <= 2^(3w(n)); n=0,1 are immediate, so w_D<=3w(n) and L_D<=15 L_H. Three low-first bits per original five-state witness symbol give length 3n or 3(n+3m), with encodings 5,6,7 rejected.

A full parser checks alphabet, unary headers, exact length, range, strict sorting, duplicate edges, no loops and u<v. Invalid input strings are mapped, for a total Karp many-one function, to the fixed unsatisfiable D(K3): twelve vertices, fifteen arcs, a DAG and underlying-bipartite. K3 has no C5 homomorphism, since C5 has no triangle. The constant factor bound is for canonical valid inputs; arbitrary malformed words satisfy additive O(L+1) bounds under the fallback. A conventional sequential compiler (no preloaded witness) charges parsing, validation, building fresh addresses, sorting five arcs per edge, serialization, full verifier access and output. Conservative simultaneous T<=O((L+1)^4), writable S_peak<=O((L+1)^2) bits on one bit machine. Exact implementation costs are upper bounds, not lower bounds.

Prior /071 functional reverse T5->width-at-most-three CNF compiler takes N directed vertices and M arcs to 8N Boolean variables and 20N+15M clauses with unique extension. Applied here it gives exactly 8n+24m variables and 20n+135m clauses, preserving C5 coloring count. The total compiler remains polynomial time and space and is sourced from a canonical authentic input. Any subexponential or polynomial T5 solver transfers to C5/Boolean SAT only with the specific reduction blowup accounted. A lower bound against one T5 algorithm, graph encoding or quotient does NOT imply a lower bound against all Boolean SAT algorithms. An unconditional all-machine superpolynomial T5 bound would, by NP-completeness and polynomial reductions, imply P!=NP; none is proved here.

## Executed finite COMPUTATIONAL verification
Revision tmr1-t5-bipartite-dag-triadfree080-js-v2, no random seed (exhaustive). The V8 code checked all 25 endpoint pairs by all 125 internal assignments, all 1,100 labeled simple H with 0<=n<=5, all 3,241,056 original five-color assignments, 81,326 satisfying witness extensions, DAG ranks/bipartitions, exact canonical lengths, malformed inputs and unsatisfiable K3 control. The graph-level full target counts are reconstructed from independently brute-forced 25 local tables, NOT by enumeration over 5^(n+3m) labelings. Actual result:
{
  "revision": "tmr1-t5-bipartite-dag-triadfree080-js-v2",
  "gadgetEndpointCounts": [
    0,
    1,
    0,
    0,
    1
  ],
  "gadgetAssignmentsChecked": 3125,
  "undirectedGraphs": 1100,
  "sourceLabelingsChecked": 3241056,
  "yesGraphs": 440,
  "noGraphs": 660,
  "satisfyingWitnessesValidated": 81326,
  "malformedRejections": 8,
  "assertions": 200728,
  "failures": 0,
  "scope": "finite checks; theorem symbolic",
  "notes": "Each graph count uses factorization of private gadgets, not full 5^(n+3m) target enumeration",
  "bitRatioBoundValidCanonicalInputs": 15
}
No unexpected failures. Both this finite run and the published self-contained V8/Node source are COMPUTATIONAL; arbitrary-size soundness follows from the separate symbolic proof above. The exact standalone source string is published and can be executed as node experiments/tmr/tmr1_t5_bipartite_dag080.js. No local Git checkout, repository preflight, complete LaTeX build, Lean/nanoda kernel or independent mathematical peer review was executed.

## Named integration point and honest barriers
This joins /071's T5 gadget semantics with /078's DAG-hardness in a *single* stronger construction, removing both directed cycles and all forced triangles. It refutes treating no directed cycles, no transitive triangle or underlying bipartiteness as a sufficient all-input tractability criterion. It does NOT prove that /075 quotienting or /079 Fourier flow is hard on the image; each remains correct and the quotient feedback rank is only a parameter, not resource necessity. The actual residual C5 NP-hardness is an encoding-level property. Legal alternative representations, graph decompositions, polymorphisms, CSP solvers, Gaussian algebra, Fourier, caching and source-aware preprocessing remain live.

Gates: DISJ PASS for this source-specific positive reduction; no rank-to-work inference. Relativization PASS for the explicit finite compiler, general nonrelativizing NP lower-bound bridge OPEN; algebrization/Natural Proofs unaffected. Simultaneous DTISP PASS for *upper* polynomial time and polynomial peak space belonging to the same sequential compiler; unrestricted forbidden resource pair OPEN. Configuration counting NOT APPLICABLE AS A LOWER BOUND, and its usual deterministic configuration *upper* bound retained. Horn/2SAT/affine/treewidth/equality/autarky/product/padding/auxiliary/selector/unique-solution/local-basis/field/charged-isolation controls remain applicable and unexcluded. /341 FAIL general UNSAT, /386 RESTRICTED. E^NP consequences do not promote to NP separation.

ONE NEXT dependency: C1-T5-TRIADFREE-MIXED-CORE-ALGORITHM-AUDIT: compare the /075 quotient, /079 integer flow, TMR-4 vertex-cover/MDD and TMR-3 separator algorithms on actual H->D(H) images for mixed C5 YES/NO graphs, preserving authentic source costs, and locate a precisely stated step not already bypassed by a cheap representation. Even a resistant finite family is not an all-algorithms lower bound.

## Evidence paths
Owner manuscript main1_PNP_MACHINE_MODEL_LEAD.tex; report research/agents/tmr-1/2026-11-17_2057_TMR1_BIPARTITE_DAG_TRIADFREE080.md; self-contained verifier experiments/tmr/tmr1_t5_bipartite_dag080.js; immutable result results/raw/tmr/2026-11-17_2057_TMR1_T5_BIPARTITE_DAG080_V8_RAW.json; role handoff research/agents/tmr-1/handoff.md. All are on branch tmr1-20261115-independent-lean060, PR #197, until separately merged.
