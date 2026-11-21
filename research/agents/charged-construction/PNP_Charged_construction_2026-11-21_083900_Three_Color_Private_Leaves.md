# Construction: a direct three-color interface in strict T5
Pacific timestamp: 2026-11-21 08:39 PST (America/Los_Angeles).
Role: charged-construction. Claim ID: **T5-3COL-PRIVATE1**.

## Exact claim, status, and integration point
For EVERY finite simple undirected graph G=(V,E), the explicit strict-C instance H_G below satisfies
```
H_G is SAT iff G is three-colorable.
n = 5+3v+e,     m = 5+2v+e,
N = n+1+2 floor(log2(m+1))+1+3m ceil(log2(n+1)).
```
Here v=|V| and e=|E|. Moreover its full interface after existentially eliminating the private leaves is exactly the three-coloring relation relative to the anchor frame, and its exact solution count is the positive weighted sum proved below.

**PROVED/EXACT:** the reduction, both directions, projected interface, weighted count transformation, and explicit polynomial construction envelope. **COMPUTATIONAL:** all 1,100 simple labeled graphs through five vertices, 3,241,056 interface rows, and the stated controls passed. **FALSIFIED/RETIRED:** a multiplier depending only on v,e converting the number of three-colorings into Z(H_G). **OPEN:** an unrestricted resource lower bound. Independent adversarial review is requested; the new reduction is not yet externally reviewed. No historical-novelty claim.

Fix any total correct deterministic strict-T5 decider A, with finite code independent of input, in the handoff's one-read/write-tape model. If it has a cap T_A(N)<=K N^a, for fixed K,a>=1, applying the charged reduction then A decides three-colorability. This gives a polynomial reduction/composition, not a contradiction. No favorable exponent, small workspace, or mandatory witness construction follows.

Four falsifiers:
1. A model of H_G with an invalid anchor frame, a graph vertex outside the three-color palette, or an edge with equal endpoints.
2. A proper three-coloring with no extension to the private leaves.
3. A coloring whose extension multiplicity disagrees with the stated product; the constant-multiplier variant is specifically tested and rejected.
4. Illegal repeated variable names inside a clause, incorrect n,m,N, or a compiler that depends on uncharged graph recognition, addresses, or succinct output.

Feature absent from the easy NAND matching family: these instances have a genuine global three-color compatibility condition and include UNSAT cases. The private leaves eliminate locally, but leave the ENTIRE arbitrary graph coloring problem on shared variables. The downstream demand must concern deciding this projected compatibility on the encoded input, not the number of leaves, colorings, graph width, or a chosen representation.

## Recovery and sources
The complete current handoff was fetched and checked identical to the already fully read 141,084-byte source at commit 10d2ccb2062c3efd4b4f03873eaa88822edf732f, blob a886f3387a8676b9cc86afbf3bebf22630109d49. Definitions, encoding, Sections 3–4,7–10,13,24 and original appended generator/evidence were recovered; current AGENTS.md, CODEX.md, assignment directive and repository research instructions were fetched unchanged. The current assignment directive blob is 776c2622d69dbcbb1c7c0d1361f299970fb7f1cc. These reads are recovery of stated claims, not independent certification of the whole baseline.

Recovery head: c4b8923cb7437f2794fa0da3181be3795dd2e35b. The construction handoff returned 404, so this creates the role's first repository handoff. The latest saved [Construction 07:33 report](https://chatgpt.com/library?file_id=libfile_6232580362808191bda4d6341c2677df&account_id=personal) was recovered through an exact-prefix search and its actual construction, interfaces, proof and ledger read. It concerns Boolean affine-plus-implication modules; it is not this T5 reduction.

The latest [Synthesis report](https://github.com/j15marti/pnp/blob/c4b8923cb7437f2794fa0da3181be3795dd2e35b/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-21_082800_Terminal_Defect.md), its code/evidence from the continuous work, and [Redteam's scoped audit](https://github.com/j15marti/pnp/blob/4b84b9c5fdc4253d404306a48b04b3de0309dcea/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-21_081400_Circuit_CM_Reconstruction.md) were recovered. Terminal semantic annotations still need their extension cost, and count-circuit transfer still supplies no count-map hardness. Issue #324 through comment 7065674077 was read. The existing Boolean-gate universality reduction is not rerun or claimed new: this run supplies a different, direct graph interface with a separately audited count weight.

## Predicate and complete generator
C is the symmetric relation on Z_5 with unordered triples 012,123,234,340,401 and all six permutations of each: 30 ordered tuples. Clauses contain three distinct variable names. No input constants, signs or relation tags are used.

Ordered R is distinct: i beats i+1 and i+3 modulo 5; R(x,y,z) requires distinct values and the first value beating exactly one other value. It has 40 tuples. The safe conversion C(x,y,z)=R(x,y,z) AND R(y,x,z) doubles the clause count and changes N. This report uses C only, not historical S/Q or blind R substitution.

Take five anchor variables a_0,...,a_4 and add
```
C(a_i,a_(i+1 mod 5),a_(i+2 mod 5))   for i=0,...,4.
```
For every graph vertex u allocate X_u and TWO private leaves P_u,Q_u, adding
```
C(a_0,X_u,P_u),   C(a_1,X_u,Q_u).
```
For every edge {u,v}, allocate ONE private leaf L_uv, adding
```
C(X_u,X_v,L_uv).
```
Every leaf is used in exactly its displayed clause and is distinct from every other leaf, graph variable and anchor. X_u is shared across all incidences of u; it is never cloned per edge.

Canonical zero-based generator IDs (the wire format stores one-based identifiers):
```
a_i = i
X_u = 5+u                    (0<=u<v)
P_u = 5+v+2u
Q_u = 5+v+2u+1
L_edge_j = 5+3v+j            (edges sorted lexicographically)
```
The code lists the five anchor clauses, the two domain clauses per vertex, then the edge clauses. This is a full clause generator for every graph, including isolates and the empty graph.

## Proof of the exact interface
Each pair of anchor positions occurs together in some cyclic length-three window. All five anchor values are therefore distinct. The five window triples must map to the five allowed C-triples. Taking complements within five values shows that the anchor bijection preserves cycle adjacency. Thus precisely the ten dihedral frames occur:
```
a_i = s+d i (mod 5),   s in Z_5, d in {+1,-1}.
```

Define d(p,q)=number of r in Z_5 with C(p,q,r). Directly from the five allowed triples,
```
d(p,p)=0;
d(p,q)=2 if p-q = +/-1 modulo 5;
d(p,q)=1 otherwise, for p!=q.
```
In particular, exists r C(p,q,r) iff p!=q. In a fixed frame the two private domain leaves can be filled iff X_u differs from a_0 and a_1. Hence X_u ranges over exactly {a_2,a_3,a_4}. The edge leaf can be filled iff X_u!=X_v.

Let b assign values to anchors and all X variables, and let y consist of ALL private leaves. Then the exact interface is
```
R_H(b) = exists y H_G(b,y)
       = Frame(a) AND [all X_u in {a_2,a_3,a_4}]
                    AND [all edge endpoints unequal].
```
Private-leaf freshness makes the local extensions independent. Every proper coloring gives a model by fixing any frame and choosing each leaf from its nonempty allowed set. Conversely every model projects to a proper three-coloring. This proves both directions for every graph and every boundary assignment, not just the SAT bit. Further external partial pins are handled by existentially hiding the remaining shared variables AFTER this composition.

No input constant is hidden in the proof: fixing a frame is an analysis of the ten possible assignments to ordinary variables. A context that accesses private leaves is outside the displayed projected interface and cannot silently use it as a pointwise replacement.

## Exact count transformation; no constant factor
Write colors 0,1,2 for a_2,a_3,a_4. The two domain leaves have multiplicities
```
w = (2,1,2).
```
For edge endpoints the extension matrix is
```
D = [[0,2,1],
     [2,0,2],
     [1,2,0]].
```
For every fixed proper coloring c,
```
extensions(c, fixed frame)
 = product_u w[c(u)] * product_{uv in E} D[c(u),c(v)].
```
All ten frames have the same multiplicities. Therefore
```
Z(H_G) = 10 * sum_{c:V->{0,1,2}}
                    product_u w[c(u)] * product_{uv in E} D[c(u),c(v)].
```
Zero matrix entries remove improper colorings. Equivalently each proper coloring contributes 10*2^(t(c)+s(c)), where t counts vertices using the two outer palette colors and s counts edges joining the middle color to an outer color. All contributing weights are positive, so this is exactly zero iff no proper coloring exists.

This is NOT 10 times the unweighted number of three-colorings, nor a parsimonious reduction. A four-vertex path and a four-vertex star both have v=4,e=3 and 24 proper three-colorings, yet their T5 counts are respectively 6,400 and 7,680. Both have n=20,m=16,N=270. Thus no multiplier depending only on v,e (or n,m,N) converts unweighted three-color counts to this count on all graphs. This does not prove impossibility of some other reduction or interpolation; none is asserted.

## Input lengths and charged implementation
Use graph source encoding
```
1^v 0 gamma(e+1) [e ordered endpoint pairs],
w_G=ceil(log2(v+1)),
M=v+1+2 floor(log2(e+1))+1+2 e w_G.
```
Endpoints are one-based, strictly increasing within each pair; pairs are strictly lexicographically increasing. Reject loops, repeated edges, invalid identifiers, bad framing and trailing bits. The empty graph is encoded as 01. Declared isolates are retained. This grammar is explicit, not a succinct graph description.

The compiler writes the handoff's strict-T5 encoding with
```
n=5+3v+e, m=5+2v+e,
N=n+1+2 floor(log2(m+1))+1+3m ceil(log2(n+1)).
```
Consequently N=Theta((v+e+1) log(v+e+2)) and N=O((M+2) log(M+2)). For maximum-degree-four source graphs, N=Theta(v log(v+2)) as v grows. This is a statement about the source graph degree; the two anchor variables occur in v+3 clauses each. Do not call the resulting T5 formulas bounded-occurrence instances.

Let U=M+N+2. A conservative deterministic one-tape implementation using full scans admits compiler time O(U^4) and total writable space O(U). The parser scans all input, checks gamma framing and length, compares adjacent pairs, and uses counters with O(log U) bits. Counts are bounded against actual remaining length or v(v-1)/2 before count-controlled iteration. The constructor writes O(N) bits and uses explicit scans to locate records and perform bounded arithmetic. Copies, work buffers and generated output fit O(U); at most polynomially many full scans fit the deliberately loose fourth-power time envelope. This is an implementable bound, not a CPython primitive count.

A proposed output can be source-authenticated by reconstructing this canonical encoding and comparing every bit. The reported compiler is not a universal recognizer of all semantically equivalent images. Hash matches never certify equivalence. No graph-decomposition hint, search over candidate gadgets, or uncharged preprocessing is used.

| Stage | Work and simultaneous storage |
|---|---|
| Parse and authenticate | Read all M bits, validate original graph and any supplied candidate bytes; unsuccessful comparisons count. |
| Allocate names | Write or compute actual bounded identifiers; retain shared X identities and distinct private leaves. No unbounded unit-cost addresses. |
| Construct and change representation | Emit all N bits, preserving old/new representations while live. Output size is paid, even if a short generator exists. |
| Discovery | Fixed uniform recipe; no failed gadget candidates in this constructor. Any alternate search would require its own charge. |
| Queries and real access | No oracle calls. All edge and clause accesses are actual scans or explicitly stored indices. |
| Sharing and recursion | One X per source vertex; no exponential DAG. This constructor has no recursive solver stack. Caller state and caches, if added, remain charged. |
| Recompute | Reconstructing or rereading source/output pays again; no automatically free cached compilation. |
| Output | Canonical formula writing and status writing count. Malformed source is rejected as UNKNOWN by a service wrapper, not labeled UNSAT. |
| Peak/CM | Compiler S=O(U), time O(U^4), physical CM O(U^5) conservatively; these are upper envelopes, not lower bounds. |

For any fixed correct decider A, first compile H_G, place its actual encoding at the declared origin, and simulate A. Compaction/initialization and retained source can be erased before entering A. A safe bound is
```
T_B(G) <= O(U^4) + O_A(t_A(H_G)),
S_B(G) <= O(U) + O_A(S_A(H_G)).
```
If source data remain retained during A, their live storage and cumulative charge must instead be added at each step. The compiler's physical CM is not the descriptive CM of A. This reduction does not give a near-linear resource speedup, a sublinear-space simulation, or a particular forbidden SAT exponent.

## New finite evidence
Code: experiments/t5_construction_3color_private1_20261121.py.
Raw data: results/raw/t5_construction_3color_private1_20261121.json.
Reproduce: python experiments/t5_construction_3color_private1_20261121.py.
Code SHA-256: 8f1ba04115bcfd85a6cc952bb2742856daf56f1891f0be63a5c87e77ebaaf6e8.
Raw SHA-256: 5fcaec440e50a9a6b64704f300dcd06e9ffee182cbade3b29ea587e1a6741085.

| Source vertices | All simple graphs | SAT images | UNSAT images |
|---:|---:|---:|---:|
| 0 | 1 | 1 | 0 |
| 1 | 1 | 1 | 0 |
| 2 | 2 | 2 | 0 |
| 3 | 8 | 8 | 0 |
| 4 | 64 | 63 | 1 |
| 5 | 1024 | 958 | 66 |

For each of 1,100 graphs, the source is encoded/decoded, the actual compiled T5 bytes are decoded, and the exact n,m,N checked. The clause-based verifier sums each actual degree-one private leaf directly using the C truth table, then enumerates all 5^v assignments of the shared graph variables in the canonical frame. It agrees with a separate weighted three-color enumeration and verifies 3,241,056 interface rows. Leaf elimination is exact because each private variable occurs once; this is NOT brute force over every full assignment of the larger formulas.

Seven named controls are checked across all ten frames and again under global variable renaming, clause reversal and argument reversal:
empty graph count 10 (N=56); one isolate 50 (N=100); one edge 240 (N=140); triangle 960 (N=235); K4 zero (N=318); path4 6,400 and star4 7,680 (both N=270).
For the empty and single-isolate formulas only, full assignment brute force additionally checks 3,125 and 390,625 assignments, respectively. Six malformed source strings are rejected. All individual graph counts and exact control bitstrings are saved in the raw file. No seed is used.

The new purpose is the three-color projected interface and its nonuniform extension weights. Previous full gate/matching/crossing suites and previous Boolean module experiments are not repeated. Finite tests support code/semantics only; the universal reduction proof is the argument above, not extrapolation from five vertices.

## Controls and downstream limit
Private leaves eliminate cheaply; the resulting weighted three-color model is an explicitly permitted compact representation. It retains all graph edges and shared graph variables. It is not the previous private-leaf TREE family: G is arbitrary. The primal graph induced on the X variables contains G exactly, but that observation alone gives no runtime lower bound.

Trees, paths, matching graphs and other tractable subclasses remain controls, not hard families. K4 is a small, easily recognized UNSAT control. Arbitrary graphs can support globally incompatible color requirements; their presence is not proof that any fixed large graph is hard.

Affine/Tseitin: no Gaussian-elimination escape is excluded by fiat; an algorithm exploiting additional structure remains legal. The construction makes no statement that high width forbids algebra.
Complement and sharing: any valid complemented/global computation is allowed. The weighted count formula can be evaluated by any correct method; no witness DLDD is mandatory.
Renaming: semantic invariance was checked with fresh names and all scopes transported. Equal counts alone do not justify a merge.
Forced domains: restricting the graph inputs further may make the actual relation easy; raw topology is not a substitute for the constrained predicate.
Relocation: graph and T5 encodings may be moved; no original-cut revisit is forced here.
Decision-witness packing: at fixed frame there are at most 3^v core color assignments; private multiplicities do not manufacture extra distinguishable graph-color boundary witnesses. No factorial decision packing is asserted.
Full-state entropy: H(output|complete deterministic state)=0; neither color entropy nor output count length is used as work.

Under any fixed A,K,a cap, keep N above and the same execution:
S=O(N^a); physical CM=O(N^(2a)); descriptive CM=O(N^(a+1)); count-map circuit gates O(N^a log N). Decision simulation also has polynomial-size circuits under such a cap, but a COUNT circuit lower bound alone does not establish a DECISION lower bound. Excluding one exponent would not exclude all fixed polynomial exponents. The reduction by itself excludes none.

DISJ gate: no communication lower bound transfer claimed.
Relativization: no nonrelativizing hardness mechanism; a coloring oracle is a legal test of the missing computational bridge.
Simultaneous DTISP: bounds above compose on one run; no time from one solver mixed with space from another.
Deterministic configurations: no configuration-count lower bound inferred.
Natural Proofs/algebrization: no new unrestricted circuit lower bound or barrier escape claimed.

## Literature and one next dependency
[Exhaustive handoff](https://github.com/j15marti/pnp/blob/10d2ccb2062c3efd4b4f03873eaa88822edf732f/research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md): definitions, anchor convention, input and model. The direct construction/proof here is supplied explicitly.

Garey, Johnson and Stockmeyer, Some Simplified NP-Complete Graph Problems, Theoretical Computer Science 1 (1976), 237–267, DOI [10.1016/0304-3975(76)90059-1](https://doi.org/10.1016/0304-3975(76)90059-1), [primary-paper scan](https://www.acs.uwinnipeg.ca/ychen2/journalpapers/Garey-Johnson-2maxsat.pdf). The original paper's Section 2 table and coloring reductions were consulted; the table lists NP-completeness for planar three-colorability at maximum degree four. OCR is imperfect and this is not a new full reconstruction of their reduction. The unrestricted graph-three-coloring NP-completeness theorem supplies context: our polynomial mapping makes this generated decision class NP-hard, and a T5 assignment is an NP witness. This is a complexity classification, not an unconditional superpolynomial lower bound.

**One next dependency, owner Accounting, adversarial review Redteam:** T5-3COL-DYNAMIC1. On a precisely declared distribution/subfamily of these encodings, specify actual transfer variables U_j, already-available source/cache information B_j, recorded machine events Pi_j, capacity b and bounded reuse r, and prove a compulsory decision-relevant demand exceeding b r K N^a for a fixed proposed cap, or give a legal counterexample. The obligation must survive the cheap private-leaf elimination just proved, global algebra, sharing and relocation. The present reduction supplies the exact shared compatibility relation and both labels; it supplies NO such demand. Synthesis should preserve this as a separate decision branch, not insert it into the all-SAT NAND count route.

No checkout was available: repository preflight, full solver suite and LaTeX build were not run. No TMR manuscript ownership was acquired or manuscript changed. New code and evidence are owned by this role; publication is current-head-protected with exact readback. P versus NP remains OPEN.
