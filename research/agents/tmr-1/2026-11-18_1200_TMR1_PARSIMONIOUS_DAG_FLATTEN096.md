# TMR-1/096: Parsimonious 28-bit-factor flattening of arbitrary T5-CSP into four-layer DAGs

**Owner:** TMR-1 / PNP Machine Model Lead. **Date:** 2026-11-18 12:00 PST.
**Status:** New arbitrary-size elementary theorem and independently executed finite computational certificate. Independent peer review, full living-manuscript build and formal kernel replay remain OPEN. **P versus NP OPEN.**

## Theorem C1-T5-FOURLAYER-DAG-096

Fix the five-state tournament T5 on Z5, where R(x,y)=1 precisely if y-x mod 5 lies in {1,3}. For any finite input directed constraint graph G=(V,E), including directed self-loops, opposed arcs, isolates and the empty instance, construct a directed acyclic graph D(G) with the following properties.

Let n=|V|, m=|E|, k be the number of source vertices incident to at least one arc (whether as source or target), and i=n-k. Then:

1. D(G) has exactly N=i+4k=n+3k vertices and M=m+5k arcs.
2. Every arc goes from a strictly lower to a strictly higher member of four fixed vertex layers 0,1,2,3. Hence D(G) is acyclic and every directed path has at most three arcs.
3. There is an **explicit bijection of satisfying witnesses**, including a unique extension in one direction:
   #Hom(D(G),T5) = #Hom(G,T5).
4. Under the owned canonical self-delimiting bit encoding with source length L=n+m+2+2m*w(n), w(t)=max(1,ceil(log2(max(2,t)))), the complete output bitstream has L'=N+M+2+2M*w(N) <= **28 L** for every valid source. All output constraints are distinct, sorted, and loop-free.
5. The reduction and both directions of witness conversion are constructible in deterministic polynomial time and polynomial writable space on a single sequential binary machine. These are explicit upper bounds, not time/space lower bounds.

Therefore T5-homomorphism remains NP-complete when the **input** is restricted to four-layer directed acyclic graphs of maximum directed-path length three. Exact T5 solution counting remains #P-complete for that restricted family under the standard counting reductions inherited from the original problem. This theorem is not a proof that P differs from NP.

## Equality gadget, with exactly one satisfying extension

Introduce terminals p,q and internal variables a,b with five constraints:

    p -> a,  p -> b,  q -> a,  q -> b,  a -> b.

For fixed terminal colors x,y in Z5, define

    E(x,y) = sum_{a,b in Z5} R(x,a)R(x,b)R(y,a)R(y,b)R(a,b).

The theorem is **E(x,y) = 1 if x=y, and 0 otherwise**. Indeed each color x beats precisely x+1 and x+3. When x=y, a,b must be distinct and comprise those two outneighbors. Only a=x+3, b=x+1 satisfies a->b because (x+1)-(x+3)=-2=3 mod 5. When x!=y, the two outneighbor sets have intersection of size at most one. Because R(a,b) excludes equality, no permitted (a,b) exists. The outneighbor-intersection matrix RR^T has first row [2,0,1,1,0], and all other rows are cyclic shifts, which independently proves the required bound.

This is a primitive-positive definition of equality with **unique witnesses** over the bare beat relation, not an extra allowed predicate or a cost-free oracle. The gadget alone is a four-layer-compatible DAG, and all five arcs are charged in the reduction.

## Constructive flattening of an arbitrary instance

For every original vertex v that is incident to at least one edge, introduce four distinct vertices p_v, q_v, a_v, b_v. Give them layers 0,1,2,3, respectively, and place the five gadget edges p_v->a_v, p_v->b_v, q_v->a_v, q_v->b_v, a_v->b_v. For each original arc (u,v), add the single cross-edge p_u->q_v. Every isolated source vertex stays as a single isolated output vertex; this is essential for the uniform 28-fold bit bound and preserves its five possible colors without any additional extensions.

If an original assignment is x_v, the **unique** output extension is

    p_v = q_v = x_v;
    a_v = x_v + 3 mod 5;
    b_v = x_v + 1 mod 5.

For isolates, retain x_v. Every cross-edge p_u->q_v now evaluates to R(x_u,x_v), exactly the original constraint. Conversely every satisfying target labeling obeys p_v=q_v=x_v by the equality lemma, so reading those labels recovers a valid original witness. This is a two-sided bijection, not merely equisatisfiability. If a source arc is a self-loop (v,v), the target has p_v->q_v, which contradicts the equality gadget, so valid self-loop sources become UNSAT **loop-free** four-layer DAGs. Opposed arcs and disconnected components likewise require no exceptions.

Arcs p_u->q_v go from layer 0 to 1; all gadget arcs go from layer 0 to 2 or 3, layer 1 to 2 or 3, or layer 2 to 3. Thus the longest directed path is at most 3 despite the full NP-completeness of the family. Acyclicity of the **input digraph** cannot by itself establish easy T5 coloring. Undirected treewidth of the flattened graph can still grow.

## Exact canonical source and output bit accounting

The owned canonical format uses unary vertex/edge counts 1^n 0 1^m 0, followed by m lexicographically strictly increasing arcs, each endpoint a low-first fixed-width w(n)-bit vertex index. Invalid headers, lengths, bounds, nonbinary symbols or unsorted/duplicate arcs are malformed, not source promises. There is no restriction against valid self-loops or opposing arcs. Witnesses are 3n low-first bits encoding values 0..4; 5..7 are invalid.

Canonical target numbering places either a single isolate or the four vertices (p,q,a,b) consecutively for each original vertex in input order, then sorts every target arc. Put k<=min(n,2m). The exact output bit length is

    L'=n+8k+m+2+2(m+5k)*w(n+3k).

Because N=n+3k<=4n for n>=1, w(N)<=w(n)+2. Since k<=2m,

    L' <= n+61m+22m*w(n)+2
       <= 28*(n+m+2+2m*w(n)) = 28 L.

The last inequality follows from 61+22w<=28(1+2w) for every w>=1. If n=0, the only valid source has m=0 and both encodings have length 2. If m=0 and n>=1 then k=0 and D(G)=G, with L'=L exactly. This avoids isolate-induced superconstant bit overhead while keeping full counting parsimony.

A malformed source word maps to the fixed contradictory four-vertex DAG consisting of one equality gadget plus p->q, with N=4, M=6 and length 36 bits. Its unsatisfiability is certified by the equality lemma. Consequently the reduction can be made total with an affine bound |f(s)| <= 28(|s|+2). Parsing, incidence marking, numbering, sorting, serialization, SHA-256 audit metadata, and witness translation are all charged on the **same sequential bit-machine realization**. Conservative simultaneous upper bounds are T=O((L+1)^4) and writable S=O((L+1)^2). These overheads forbid pretending the reduction is free, or transferring an exact fine-grained time exponent without charging it.

The SHA-256 example in the raw audit permits byte-integrity comparison of two canonical example encodings. A digest alone does not cryptographically authenticate authorship or input provenance without a trusted signer or trusted manifest; it is not treated as such.

## Exact Boolean translation and implications

Compose this reduction with the already proved /095 zero-auxiliary strict 3-CNF compiler. Since D(G) is loop-free, the composed CNF has

    B=3N=3n+9k Boolean variables;
    K=3N+5M=3n+34k+5m strict three-distinct-literal clauses.

Every original T5 labeling corresponds to exactly one satisfying Boolean assignment. The exact Boolean bitstream length, using the /095 serialization, is

    L_3CNF = B+2+K*(6+3*w(B)).

The direct /095 compiler is smaller for ordinary T5 instances; the DAG composition has a different purpose and must not be sold as an algorithmic improvement.

Primary literature establishes NP-completeness of general T5-homomorphism: T5 is semicomplete and contains multiple directed cycles, including A->B->C->A and A->D->E->A (Bang-Jensen, Hell, MacGillivray 1988). The /089 explicit reduction from undirected C5-colorability supplies a second route from the Hell-Nesetril 1990 theorem. Counting hardness follows from Dyer-Greenhill 2000 (including 2004 corrigendum) together with that explicit /089 counting relation and the new parsimonious flattening. These classification inputs are cited rather than silently inferred from resemblance to Boolean SAT.

A polynomial-time algorithm for **every four-layer DAG** input would imply a polynomial-time algorithm for arbitrary T5-CSP and thus P=NP. A polynomial-time algorithm for a smaller structured subclass does not. A proved worst-case lower bound for the four-layer DAG restriction would automatically be a lower bound for general T5, but no such superpolynomial bound is known or claimed. No theorem here rules out algebraic, Fourier, Gaussian, consistency, treewidth, quotient, or other efficient algorithms on special input families.

## Exact computational audit and unresolved safeguards

Full locally executed, dependency-free Node.js verifier:
experiments/tmr/tmr1_t5_dag096_certificate.js (local full verifier; linked separately as a conversation attachment).
Public independent short certificate:
experiments/tmr/tmr1_t5_dag096_public.js.
Repository raw full-run audit:
results/raw/tmr/2026-11-18_TMR1_DAG_FLATTEN096_RAW.json.

**Full local run:** 16,999,357 assertions, 659 directed graphs, 144,411 source assignments, 5,085,031 fully enumerated target assignments, 5,445,861 parameterized encoded-length cases, zero failures. It checked the 25 exact gadget terminal pairs, all loop-permitted digraphs through 3 vertices, deterministic 4-vertex samples, source/target bit roundtrips, malformed source rejection, full direct target counts through source n=2, acyclic layers, witness reconstruction and a fixed NO instance. **Public independent replay:** 1,455,857 assertions, 531 directed graphs, 64,411 source assignments, 5,085,031 full target assignments, zero failures.

These are finite **COMPUTATIONAL** tests. The arbitrary-size theorem is separately proved above. No Lean kernel, whole-manuscript build, independent referee or externally repeated full verifier is claimed. P versus NP remains OPEN.

## Primary references

[1] Bang-Jensen J, Hell P, MacGillivray G. The Complexity of Colouring by Semicomplete Digraphs. SIAM J Discrete Math 1988;1(3):281-298. https://doi.org/10.1137/0401029

[2] Hell P, Nesetril J. On the complexity of H-coloring. J Combin Theory B 1990;48(1):92-110. https://doi.org/10.1016/0095-8956(90)90132-J

[3] Dyer M, Greenhill C. The complexity of counting graph homomorphisms. Random Struct Algorithms 2000;17:260-289. https://doi.org/10.1002/1098-2418(200010/12)17:3/4%3C260::AID-RSA5%3E3.0.CO;2-W

[4] Dyer M, Greenhill C. Corrigendum: The complexity of counting graph homomorphisms. Random Struct Algorithms 2004;25:346-352. https://doi.org/10.1002/rsa.20036

**Handoff:** Update only owned living main1 and compact handoff; byte-exact archive previous /095 handoff; append this proof-obligation executable and raw audit under owned paths; issue #3 and draft PR #197 remain the permitted workflow. Preserve identity, title, enabled state, hourly schedule and every scientific safeguard. No new or immediately rerun agents.
