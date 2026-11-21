# Construction: exact unweighted three-color core
2026-11-21 10:35 PST, America/Los_Angeles.
Named lemma **T5-UNWEIGHTED-3COL1**.

## Result and exact claim
**PROVED/EXACT**, explicit reduction; external independent adversarial review pending. For EVERY finite simple labeled graph G with v vertices and e edges, the strict symmetric-C instance J_G below satisfies
Z_C(J_G)=10 #3COL(G), and J_G is SAT iff G is three-colorable.
Here #3COL counts assignments to three labeled colors, not colorings modulo permutation. Isolated vertices and the empty graph are included. No oracle, primitive pin, negated literal, equality constraint or restricted input domain is used.

Applying the previously proved full-domain equality splitter D gives
Z_C(D(J_G))=10*2^E #3COL(G), E=10+9v+12e,
with maximum variable occurrence five. Both directions of decision equivalence remain explicit. This supplies a NEW family; it does not retroactively make the older H_G reduction unweighted.

**COMPUTATIONAL:** all ten anchor frames, every single-color exclusion table and every restricted edge pair, plus all76 simple graphs on0..4 vertices pass. Expanded split counts use the established equality interface, not brute-force enumeration of expanded assignments. No asymptotic lower bound is inferred.

Downstream demand: compulsory decision-relevant work on the arbitrary three-color core after exact gadget contraction. ONE next dependency, **T5-UNWEIGHTED-CORE-SERVICE1**, owner Accounting, Redteam review and Synthesis tracking. Produce an actual decoded obligation with bounded event reuse for every fixed correct solver, or falsify it. A reduction alone is not a resource lower bound.

## Recovery, model and falsifiers
Current recovery head4c1d7f5ef16531313c82bd7a888fca03edd3f4f3. Fetched the complete current exhaustive handoff, assignment, AGENTS.md, CODEX.md and repository research instructions again; their blobs match the full contents recovered earlier in this continuous session. Baseline blob a886f3387a8676b9cc86afbf3bebf22630109d49,141084 UTF-8 bytes,SHA256 c9a3a0f362c72dfad7548b0cd44723853f105dcdc6a4f9ea5fef4559d3bb2a33. Baseline claims remain under their stated hypotheses, not newly certified. Recovered own09:32 report, complete generator, handoff and relevant issue324 peer claims.

Primary dependencies:
- [Construction equality splitter](https://github.com/j15marti/pnp/blob/8ae69ba65b79af7d3da945293eacb7bbf1ebe2d1/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_093200_Full_Domain_Equality_Split.md), report blob538badc64d1b0ceae21624e33a1daa2e44343d8f; [original code](https://github.com/j15marti/pnp/blob/8ae69ba65b79af7d3da945293eacb7bbf1ebe2d1/experiments/t5_construction_occurrence5_20261121.py), blob8d2586962e55c58408ea25089fc90cd6e22299d9. Its full interface proof and generator were read, not inferred from the handoff.
- Accounting9f6787be1c19431c5848f0cc44f8e3ccd4b4a75c rejects auxiliary orientation entropy as compulsory work.
- Bounds12726183d307127ed4e07103f2eec9324dae7cc9 rejects additive noise that ignores the full multiplier.
- Synthesis4c1d7f5ef16531313c82bd7a888fca03edd3f4f3 accounts for source-dependent full normalization.
- Redteam55805b5b8f8d6a453ddebb029a74b71de5252d07 records same-session reconstruction, not an external independent reviewer. This report likewise makes no external-review claim.

Fix separately ONE correct deterministic strict-C counter or decider A, constants K>0,a>=1 independent of input, and the hypothetical sole-tape cap T_A(N)<=KN^a. The machine has fixed alphabet/control, input/work/output on one tape, paid head motion and all address information. Our compiler is another explicitly charged execution; it cannot supply a missing same-execution lower bound for A.

Four falsifiers:
1. A normalized exclusion gadget has zero or multiple extensions for an allowed endpoint.
2. The edge gadget admits equal colors or gives unequal extension multiplicities.
3. Sharing anchors or private-variable collisions destroy the claimed global tenfold fiber.
4. The occurrence/encoding ledger fails, or gadget multiplicity is promoted into compulsory work despite exact contraction.

C contains every permutation of012,123,234,340,401 over Z5,30 tuples. Every clause uses three distinct variable NAMES. Ordered R is the different40-tuple relation; no historical S/Q substitution. If required, C(x,y,z) becomes R(x,y,z) AND R(y,x,z), preserving assignments/count but doubling clause number and the split occurrence bound toTEN.

## Full clause generator and local proof
Use five anchor variables a_0,...,a_4 with
A = AND_{i=0}^4 C(a_i,a_{i+1},a_{i+2}),
indices modulo5. Its assignments are exactly a_i=s+i or s-i modulo5: every pair of anchor positions shares a clause, hence the five values differ; complementing the allowed triples identifies the preserved five-cycle. There are exactly ten frames.

For k in Z5 and a fresh private P define the TWO-clause exclusion gadget
U_k(X;P) = C(a_k,X,P) AND C(a_{k+2},a_{k+3},P).
For every frame and every value x,
sum_p [U_k(x;p)] = [x != a_k].

It suffices by the frame automorphisms to check k=0 in the identity frame. The second clause permits P in{1,4}. In the first clause:
X=0 has no extension;
X=1,2,3,4 respectively have unique P=4,1,4,1.
This proves the exact interface, not just its existential projection. Index rotation and frame reflection preserve all clauses and cardinalities.

For each graph vertex j create X_j and private P_j,Q_j, and add
U_0(X_j;P_j), U_1(X_j;Q_j).
Thus X_j lies in{a_2,a_3,a_4} and has exactly one pair of auxiliary values for each allowed color. These are four ordinary C-clauses, not a primitive list constraint.

For each graph edge {j,k}, create three private variables L_jk,R_jk,S_jk and add FIVE clauses:
C(X_j,X_k,L_jk),
U_2(L_jk;R_jk), U_4(L_jk;S_jk).
The latter four clauses put L in{a_0,a_1,a_3}, with unique R,S per permitted L. In the identity frame, the possible third colors of C for unordered endpoint pairs are
{2,3}: {1,4}; {2,4}: {3}; {3,4}: {0,2}.
Intersecting with{0,1,3} leaves respectively1,3,0: one value for every unequal pair. Equal endpoints cannot satisfy C. The resulting edge matrix on{2,3,4} is exactly J_3-I_3, with unit off-diagonal weights.

The full instance J_G is the single common frame plus these vertex and edge blocks. All private variables are distinct across blocks; anchors and intended graph endpoints are the only shared names. This is a full generator for every graph, also implemented in the runner.

## Both directions and exact count
Fix one of the ten frames. Map the three labeled graph colors to a_2,a_3,a_4. Every proper coloring uniquely determines each vertex auxiliary pair and each edge triple by the tables above, giving one satisfying extension. Conversely every satisfying assignment places all graph vertices in these three colors and forces unequal endpoints on every edge, hence projects to a proper coloring. Auxiliaries are unique for that projected coloring and frame.

The ten frames are disjoint and exhaustive. Therefore Z_C(J_G)=10 #3COL(G). There is one GLOBAL factor ten, not ten per connected component. For v=e=0 the empty coloring has one assignment and the frame count is ten. An isolated vertex contributes exactly three, as it should. UNSAT produces zero; no witness need exist or be output on UNSAT.

This improves the earlier weighted H_G construction by replacing its private-leaf blocks, not by assuming their old weights disappear. For example path4 and star4 both now give #3COL=24 and Z=240, whereas their old weighted counts differed. The new formula has more clauses; changing construction is paid.

## Bounded occurrence and exact encoding ledger
For J_G:
n_J=5+3v+3e, m_J=5+4v+5e.
Every variable is used. In the equality splitter D, each occurrence gets a distinct copy. Consecutive copies of each source variable are linked by the six-clause Q(U,V) gadget consisting of a five-position frame b_0=U and C(b_4,V,b_1), with four fresh auxiliary names. Q has exact interface2[U=V]. Each internal copy appears once in an original clause, three times as an outgoing U and once as an incoming V, giving degree at most5; private frame variables have degree at most4.

The general splitter has E=3m_J-n_J links, n_B=n_J+5E, m_B=m_J+6E. Therefore this new image B^*_G=D(J_G) has
E=10+9v+12e,
n_B=55+48v+63e,
m_B=65+58v+77e,
Z_C(B^*_G)=10*2^E #3COL(G).
Every target solution projects through equality paths to J_G; every J_G solution has2^E independent frame-orientation lifts. Both SAT and UNSAT are preserved. These orientations are allowed to be contracted and are not compulsory information for A.

For either T5 stage use EXACTLY
N(n,m)=n+2+2floor(log2(m+1))+3m ceil(log2(n+1)),
the unary-n/gamma(m+1)/one-based fixed-ID encoding. Thus N_J=N(n_J,m_J), N_B=N(n_B,m_B), both Theta((v+e+1)log(v+e+2)); N_B=Theta(N_J).

For a graph encoded by unary v, gamma(e+1), and2e endpoint fields of width ceil(log2(v+1)),
M_G=v+2+2floor(log2(e+1))+2e ceil(log2(v+1)).
N_B=O(M_G log(M_G+2)), not uniformly O(M_G): an edgeless graph with many isolates shows the logarithmic growth. Do not compare exponents after silently exchanging M_G,N_J,N_B.

A one-edge graph gives n_J14,m_J18,N_J240,count60; its split image has n_B214,m_B258,N_B6424,E40,count65970697666560. K4 gives n_J35,m_J51,N_J965 and an UNSAT split image n_B625,m_B759,N_B23415,E118. These are executed checks.

For a SAME-length both-label control, use K2,3 and K4 plus an isolate: v5,e6,n_J38,m_J55,N_J1040; n_B673,m_B817,N_B25203,E127. The proper-color counts are30 and0. For K2,3, equal colors on its two-vertex side give3*2^3=24 choices, and different colors give6 more. Hence split counts are300*2^127 and0. This last calculation is symbolic, not an additional expanded enumeration.

Also 3m_B-n_B=14E because all J_G variables are used. Synthesis's header-normalization interface applies with the NEW coefficients above. The normalized quotient is now unweighted #3COL(G), unlike the earlier family. This does not provide a pseudoentropy pair or a hardness proof.

## Lower-bound integration and easy controls
The feature absent from the easy matching family is arbitrary three-color incompatibility with both decision labels, now with exact unit local extension weights. Equality and exclusion/edge contractions recover an arbitrary three-color graph core. There is no reduction to matching-cycle counting established here. Nor is the core claimed hard merely because it has high width.

A subsequent compulsory-progress lemma must identify source-dependent decisions or messages required by EVERY fixed correct solver on this core AFTER contraction and legal algebra/caching/relocation, with a real decoder, charged side information and bounded reuse. It must exceed the appropriate cap in N_B on that same execution. The construction supplies the core and exact reduction, not that obligation.

Trees remain an easy control: a nonempty tree has3*2^{v-1} proper colorings, so its J_G count is30*2^{v-1}. This follows by choosing the root color then one of two colors for each child. Matching/forest cases therefore stay easy. Small forced domains and affine/Tseitin instances retain their own cheap solvers; no universal witness compiler is inferred. Complement, representation changes, caching and renaming remain legitimate. The global equality-orientation factor is retired as a hardness source by Accounting's independence obstruction. Full-state output entropy remains zero. Decision-witness packing is not inferred from ten or2^E multiplicity.

## Complete resource ledger
Let U=M_G+N_J+N_B+2. A fixed uniform scanner validates the graph encoding and distinct legal edges, emits frame/vertex/edge clauses in canonical order, then emits occurrence-copy clauses and six-clause equality links by repeated source scans. O(U^2) logical field visits, O(log U)-bit counters and paid travel across O(U) cells fit the conservative O(U^4) sole-tape time, O(U) simultaneous span, and O(U^5) physical CM envelope. This includes final output layout. It is not a CPython timing claim.

| Stage | Paid treatment |
|---|---|
| Parsing/authentication | Read original graph and all constructed T5 bits; validate IDs, strict clause scopes, duplicate edges and headers. Malformed is rejected/UNKNOWN, not UNSAT. |
| Discovery/failed candidates | The finite gadget search below is research evidence. Deployed compiler uses fixed tables; an arbitrary solver's failed recognition/selection attempts remain charged. |
| Representation changes | Explicit new variables, occurrence maps, fresh private IDs, clause emission and any contraction are paid. No semantic/equality oracle. |
| Queries/accesses/addresses | No external query in the compiler; source rereads, comparisons, head movement, counters and address bits included. |
| Storage/sharing/recompute | One global frame and each physical cached object counted once. Original input, output and buffers coexist. Discarded maps must be recomputed or reread. |
| Witness transport | If requested, choose a frame and the unique local values, then equality orientations; verify all clauses. Finding the source coloring is not supplied by the compiler. |
| Exact output | Write N_B bits and terminator. Count arithmetic for the known multiplier uses O(v+e) value bits and paid operations; no unit-cost huge integers. |
| Descriptive CM | Separate replay bound O(U^4(M_G+log U)); not equated with physical residency. |
| Composed solver | Time includes compiler O(U^4) plus target A on N_B and layout/output costs. Polynomiality is preserved, not each fixed exponent or constant. |

Under the original target cap retain S_A=O(N_B^a), physical CM_A=O(N_B^{2a}), minimum-description CM_A=O(N_B^{a+1}), count-map circuit size O(N_B^a log N_B). No lower demand here exceeds any ceiling; defeating one exponent would not defeat all. A count separation alone would not settle P versus NP.

DISJ: NOT APPLICABLE, no direct sum. Relativization: OPEN for unrestricted separation, no nonrelativizing step. Simultaneous DTISP: PASS for separate compiler/solver ledgers; compulsory violation OPEN. Deterministic configurations: PASS, no state-count lower bound. Natural Proofs/algebrization: no barrier bypass or unrestricted circuit lower-bound theorem.

## Reproducibility and fresh search log
Run:
python experiments/t5_construction_unweighted3col1_20261121.py > results/raw/t5_construction_unweighted3col1_20261121.json

Standalone Python3 runner, assertions enabled, no external dependency or random seed. Code SHA256 d0c1437cca6a8b1de2230514168eccb2f362a5c0434fee28630ec8521eb5e866. The raw file records all ten frame/interface tables and all76 graph cases, including full unsplit clauses/encoding and split clauses for the edge and K4 examples. Graph counts use exact elimination of private auxiliaries followed by enumeration over five-valued vertex tuples, compared against independent enumeration of labeled three-colorings. Split counts use the prior equality theorem and generated degree/size checks, not all5^{n_B} assignments. Finite evidence supplements the general local-table proof.

New experiment reason: the old generator had weights(2,1,2) and unequal edge weights. These are new exclusion/edge gadgets and a changed count transformation. The old equality exhaustive suite and old1100-graph experiment were not rerun. Discovery tested single-anchor private-leaf factors, then factors with an extra anchor-pair clause; the full-domain exclusion row, rather than just its three-color restriction, exposed this construction. No optimal-gadget-size claim.

Fresh queries2026-11-21: “counting CSP gadget unique extension parsimonious graph coloring reduction”; “Dyer Goldberg Jalsenius Richerby bounded degree counting CSP equality simulation 2010”. Read [Dyer et al., STACS2010, Section4](https://drops.dagstuhl.de/storage/00lipics/lipics-vol005-stacs2010/LIPIcs.STACS.2010.2466/LIPIcs.STACS.2010.2466.pdf): their equal-fiber equality simulation and degree accounting concern Boolean languages with pins and approximation-preserving reductions. Those hypotheses do not directly imply this five-color, no-primitive-pin construction. Our exact interface tables provide the needed proof. No external dichotomy or hardness theorem is imported. Search also surfaced parsimonious planar coloring and weighted-CSP articles; their proofs were not inspected/imported.

Fresh official connector query “graph coloring constraint satisfaction counting” under anthropics,openai,xai-org,google-research,google-deepmind:
- Anthropic/xAI: no results returned.
- OpenAI math at4eaee87548250b2682affda7d05d947c05554bae returned a preprint fragment describing one-hot coloring-to-CNF. It is a different encoding; neither the headline complexity claim nor proof was audited or imported.
- Google Research at87e25a5ba04d2c4cf0108f0cec96d648fe2b945a: numbert vocabulary coincidence, rejected.
- DeepMind concordia atd7da4499dd323fc51fce10b38105b3d17fb3651c: narrative word matches, rejected.
Web fallback queries for Anthropic/xAI graph-coloring CSP returned unrelated third-party repositories. Those are not official merely because they use a model/API name.

An additional relevant official search found [Google OR-Tools graph_coloring.cc](https://github.com/google/or-tools/blob/4782dbd0aa85621c8115cf33de1574a2e6757004/ortools/math_opt/samples/cpp/graph_coloring.cc), blob dafb18bc97b4e4d5b46779282ad999b295c056cf. Inspected its one-hot feasibility model and solving routine: exactly one color per vertex, unequal colors per edge. It is not a #T5 counting gadget or a lower bound; no external build/import. Ownership uses the verified-domain/official cross-links already checked in this continuous session: [Anthropic](https://github.com/anthropics), [OpenAI](https://github.com/openai), [xAI](https://x.ai/open-source), [Google Research](https://research.google/pubs/implicit-rate-constrained-optimization-of-non-decomposable-objectives/), [DeepMind](https://deepmind.google/blog/open-sourcing-mujoco/), [Google OR-Tools](https://developers.google.com/optimization). Prior logs avoided redundant deep review; no exhaustive absence/novelty claim.

A bounded repository duplicate query “unique extension color exclusion unweighted” returned older unrelated Boolean lifts, not this exact gadget in the returned set. No local checkout/preflight/LaTeX or external kernel build; no TMR manuscript ownership or edits; no schedule/identity/enabled-state changes.

Return to Accounting, Bounds, Redteam and Synthesis: use the NEW J_G/B^*_G coefficients and unweighted quotient only for this generator. Independently review exact fibers, global frame sharing, counts with isolates, and encoding before promotion. ONE next dependency remains T5-UNWEIGHTED-CORE-SERVICE1. **P versus NP remains OPEN.**
