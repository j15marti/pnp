# PNP Charged Construction — full-domain equality and occurrence-five decision reduction

2026-11-21 09:32 PST (America/Los_Angeles). Role: Charged Construction.
Recovery/publication base: `d18f513e02a053db9d30ee7172ee516834c152d3`.

## Exact target and result

**T5-FULL-EQUALITY-SPLIT1 — PROVED/EXACT, self-contained construction proof; independent adversarial review pending.** There is one deterministic uniform compiler D such that, for every well-formed strict symmetric-C input F with n declared variables, m clauses and u variables that occur in clauses, D(F) is another strict-C input, every variable occurs in at most five clauses, and
$$
E=3m-u,\qquad n'=n+15m-5u,\qquad m'=19m-6u,\qquad Z_C(D(F))=2^E Z_C(F).
$$
These quantifiers include empty formulas, unused declared variables, repeated clauses, arbitrary clause order and arbitrary source variable names. Each source clause has three distinct variable names. Every source assignment has exactly 2^E extensions if it satisfies F, and zero otherwise. Consequently SAT and UNSAT are both preserved. Malformed strings are rejected as malformed, never labeled UNSAT.

The fixed compiler, its resource envelope, and the quantified solver are distinct: fix any deterministic total correct target solver A and any constants K>0, a>=1 with T_A(M)<=K M^a in the declared bit-cost model. This report proves a reduction usable by that same A; it supplies **no lower bound** on A. The sole-tape implementation described below has fixed alphabet and charged input/output storage. The reference Python generator establishes syntax/semantics, not a measured sole-tape step count.

The new implication is that the previous arbitrary-graph three-color decision interface survives a constant occurrence bound without introducing primitive equality, constants or per-clause relation tags. A correct reduction alone is not a compulsory-progress lemma. **The unrestricted resource separation and P versus NP remain OPEN.**

One next dependency: **T5-BOUNDED-3COL-DYNAMIC1**, owner Accounting, independent audit requested from Redteam, tracked by Synthesis. Its obligations must survive equality contraction and private-leaf elimination.

Four concrete falsifiers selected for this construction:

1. An unequal pair of endpoint colors has a satisfying equality-gadget extension, or two equal colors have different extension multiplicities.
2. A legal source assignment fails to lift, a target assignment projects to a nonsolution, or unused variables/repeated clauses change the claimed multiplier.
3. Any generated variable has occurrence above five, or an encoded n', m', N' differs from the stated ledger.
4. A claimed compulsory demand counts the inserted equality paths as unavoidable separate work even though exact local contraction recovers the original instance. This falsifies that proposed hardness use, not the reduction.

## Recovery and source revision

Read the complete current handoff (141084 UTF-8 bytes; SHA-256 `c9a3a0f362c72dfad7548b0cd44723853f105dcdc6a4f9ea5fef4559d3bb2a33`), current assignment, AGENTS.md, CODEX.md and the repository PNP research instructions. They were recovered again unchanged in this continuous workspace; the complete baseline reading from the preceding run remains available. The baseline is audited only under its stated hypotheses, not recertified here.

Recovered the full current Construction handoff (blob `57b1c810df0bf0467da3316c0b6b5d573fdf67fb`), [08:39 original report](https://github.com/j15marti/pnp/blob/358200a519d8cd27b33a02a12bb1b6b7db24a825/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_083900_Three_Color_Private_Leaves.md), its original [generator](https://github.com/j15marti/pnp/blob/358200a519d8cd27b33a02a12bb1b6b7db24a825/experiments/t5_construction_3color_private1_20261121.py) and [raw evidence](https://github.com/j15marti/pnp/blob/358200a519d8cd27b33a02a12bb1b6b7db24a825/results/raw/t5_construction_3color_private1_20261121.json). That report explicitly left anchor degree unbounded; this run addresses that limitation. Its 1100-graph experiment was not rerun. The present graph controls test the new compiler.

Read current [issue #324](https://github.com/j15marti/pnp/issues/324), including Accounting's selector-capacity result at `fd693f40c606be2453db0440504cdfd7de49ff89`, Discovery's fixed-depth nested-renaming result at `3f1f2846496f68ba414cc2c8169da3cc60ec6352`, Redteam's parity audit at `2c1f76d1188f30aa396b8330ee93a67f9ea0ab7e`, and Synthesis's [quotient-budget report](https://github.com/j15marti/pnp/blob/d18f513e02a053db9d30ee7172ee516834c152d3/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-21_092400_Quotient_Budget_Bridge.md). None supplies the missing decision-progress premise. No peer or TMR manuscript is modified.

Repository keyword search `full domain equality occurrence` returned historical bounded-occurrence/projection work, not a matching strict-C result in the bounded returned set. This is not a novelty claim or an exhaustive historical nonexistence claim.

## Relation and exact encoding

C is symmetric on Z_5. Its allowed unordered triples are 012,123,234,340,401; all six permutations are allowed, for 30 tuples. Clauses use distinct variable names; variables initially have full domain Z_5. No input pin, NOT, equality or other relation is used.

The ordered tournament relation R has 40 tuples and is different. We use no historical S/Q substitution. If an R implementation is desired, replace each C(x,y,z) by R(x,y,z) and R(y,x,z), exactly as in handoff section 3. This preserves assignments and count but doubles clauses and the occurrence bound becomes **ten**, not five. The degree-five assertion is exclusively for C.

The source and target both use
$$
1^n0\ \gamma(m+1)\ [m\text{ ordered triples of one-based IDs}],\quad
w=\lceil\log_2(n+1)\rceil,\quad
N=n+2+2\lfloor\log_2(m+1)\rfloor+3mw.
$$
Target N' is the identical expression with n',m',w'. Empty n=m=0 has N=2. Argument order is retained by the encoder even though C is symmetric.

In general n',m'=O(n+m), and **N'=O(N log(N+2))**. Do not replace this with O(N) for arbitrary sources: repeat a fixed three-variable clause m times; source N=Theta(m), while this compiler has n',m'=Theta(m), hence N'=Theta(m log m). Duplicate removal is a legal optional shortcut, not part of D's count formula. The special graph image below has N'=Theta(N).

## Gadget and complete proof

For distinct external names U,V and four private names b_1,...,b_4, put b_0=U and use exactly
$$
Q(U,V;\mathbf b)=
\bigwedge_{i=0}^4 C(b_i,b_{i+1},b_{i+2})\ \land C(b_4,V,b_1),
$$
where frame indices are modulo five. In order, these are
$$
C(U,b_1,b_2), C(b_1,b_2,b_3), C(b_2,b_3,b_4),
C(b_3,b_4,U), C(b_4,U,b_1), C(b_4,V,b_1).
$$
This is the full clause list.

Every pair of frame positions occurs together in at least one frame clause: distances one and two exhaust pairs on a five-cycle. Therefore b_0,...,b_4 are all distinct. They are a permutation of Z_5. The complements of the five allowed triples are exactly the five adjacent pairs of the color cycle. Taking complements in a frame permutation shows it preserves that cycle. Its assignments are exactly b_i=s+i or b_i=s-i modulo five, for s in Z_5. Conversely these ten assignments satisfy every frame clause.

For any such frame, the pair (b_4,b_1) has exactly one legal third color, b_0: normalize to (4,1), whose only allowed triple is 401, then apply the frame automorphism. The last clause forces V=U. Fixing U leaves precisely the two orientations of the frame. Thus for all x,y in Z_5,
$$
\sum_{\mathbf b\in Z_5^4} [Q(x,y;\mathbf b)]=2[x=y].
$$
No color is privileged and there is no forced endpoint domain. U occurs three times, V once, b_1 and b_4 four times, and b_2,b_3 three times.

To construct D(F), scan source occurrences in clause/argument order. Make a fresh occurrence copy for each of the L=3m positions and replace the source clauses by those copies. Preserve one free variable for each of the n-u unused source variables. For each used source variable x with copies x_1,...,x_d in occurrence order, append Q(x_j,x_{j+1}) for j=1,...,d-1, using four new private variables per link. There are E=sum_x(d_x-1)=L-u links. This is the complete generator; executable code additionally fixes all integer IDs and serialization order.

The transformed original clauses use each occurrence copy once. An internal path copy occurs as U in at most one link and V in at most one link, so its total degree is at most 1+3+1=5. Auxiliaries have degree at most four. Unused variables have degree zero. Therefore all degrees are bounded by five. Counts of variables and clauses are
$$
n'=L+(n-u)+4(L-u)=n+15m-5u,\qquad
m'=m+6(L-u)=19m-6u.
$$
These equations also hold when m=0.

A satisfying source assignment assigns the same source value to every copy and to its retained unused variable. Each link has two extensions, independently because its four auxiliaries are fresh, giving exactly 2^E targets. Conversely any target solution forces each copy path to a single value; project it to the corresponding source variable, and preserve each unused value. Every original clause is then satisfied. These maps prove both directions of decision equivalence and the exact fiber cardinality. Zero models stays zero. Counting is not used as a substitute for the decision proof.

## Explicit decision-sensitive family

Let G be any finite simple graph with v vertices and e edges. Use the previous construction H_G: five frame anchors a_i; one X_j and private P_j,Q_j per vertex; one private L_jk per edge; clauses
$$
\bigwedge_{i=0}^4 C(a_i,a_{i+1},a_{i+2}),\quad
C(a_0,X_j,P_j), C(a_1,X_j,Q_j),\quad
C(X_j,X_k,L_{jk}).
$$
The full generator is included in the new code, not just a reference to an oracle.

At a normalized frame the private-vertex projection permits exactly X_j in {2,3,4}, with extension weights (2,1,2). The edge projection permits exactly unequal colors, with weights
$$
W=\begin{pmatrix}0&2&1\\2&0&2\\1&2&0\end{pmatrix}.
$$
These facts follow by listing the five allowed unordered triples. Thus H_G is SAT iff G is three-colorable; every proper coloring lifts and every satisfying assignment projects to a proper coloring. The new family B_G=D(H_G) has the same decision equivalence, via the proven projection/lift.

All variables of H_G are used. Substitution gives
$$
E=10+3v+2e,\quad n_B=55+18v+11e,\quad m_B=65+20v+13e.
$$
With the fixed T5 encoding, N_B is exactly the n_B,m_B formula above. Both N_H and N_B are Theta((v+e+1) log(v+e+2)), so N_B=Theta(N_H). If G itself is encoded by unary v, gamma(e+1), and 2e one-based width-ceil(log_2(v+1)) endpoint fields, its length is
$$
M_G=v+2+2\lfloor\log_2(e+1)\rfloor+2e\lceil\log_2(v+1)\rceil.
$$
Graph authentication checks simple distinct sorted edges and valid endpoints. In particular isolated vertices can make N_B=Theta(M_G log M_G); do not silently identify these encodings.

The exact count is
$$
Z_C(B_G)=2^{10+3v+2e}\cdot10
\sum_{\text{proper }c:V\to\{2,3,4\}}
\prod_j w(c(j))\prod_{jk\in E}W(c(j),c(k)).
$$
It is not a constant multiple, depending only on v,e, of the unweighted number of graph colorings. Path4 and star4 retain their unequal weighted counts. This run does not reverse the earlier falsification.

The feature absent from the easy matching family is arbitrary three-color compatibility with both SAT and UNSAT images, now despite bounded occurrence. Exact equality contraction followed by private-leaf summation returns the arbitrary graph core. That operation is permitted and gives no exponential demand. A later compulsory-progress lemma would have to concern decision-relevant compatibility **after** these contractions, not the number of copies, orientations, represented witnesses or inserted clauses. No argument here rules out an algebraic, cached or compact evaluator for that core.

## Complete resource ledger

Use U=N+N'+2 (or U=M_G+N_H+N_B+2 for the composed graph reduction). The following is one conservative uniform **sole-tape** implementation envelope, not a performance claim for CPython.

A scanner can avoid an n-entry address table. It first authenticates all source bits and counts u by scanning the source once per declared variable. It computes n',m',E using binary counters. It writes the header and the transformed original clauses, whose copy IDs are their occurrence ranks. For each source variable it scans occurrences in order, retaining only the preceding occurrence rank, and emits the six clauses of each next link. Reserve the unused-variable IDs before the auxiliary interval; unused variables need no clause records. A counter allocates four fresh IDs per link. The whole source, generated output and finitely many counters occupy O(U) cells. At most O(U^2) logical field visits suffice; comparing/updating O(log U)-bit counters using sweeps across O(U) occupied cells is covered by O(U^4) physical steps. This intentionally loose bound includes writing and relocating the final output into the target solver's input layout.

| Component on this one compiler execution | Paid bound or treatment |
|---|---|
| Original input and source authentication | Read and validate actual bits; O(U) resident input/output cells; malformed input distinct from UNSAT |
| Discover used variables and copy chains | Repeated source scans and occurrence ranks, O(U^2) logical field visits; no equality oracle |
| Failed candidates / parameter search | No runtime candidate search or failed solver calls; fixed six-clause gadget is part of the program |
| Counters, addresses, arithmetic precision | O(log U) bits per counter and actual tape travel; allocation IDs are not unit-cost unbounded integers |
| Representation conversion and adaptive switches | One deterministic conversion, no adaptive portfolio; all emitting, copying and layout changes inside O(U^4) |
| Queries and real accesses | Zero external/semantic oracle queries; source rereads and destination writes are included |
| Retention, sharing and recomputation | O(U) occupied cells; original bits and output counted once, reread work paid; no sum over imagined interfaces |
| Output and verification | Exactly N' bits; a further full decode/syntax check fits the envelope; hashes are integrity checks only |
| Compiler time, peak physical S, physical CM | O(U^4), O(U), O(U^5), respectively, on the described single run |
| Minimum-description CM | Separately bounded by O(U^4(N+log U)) for reconstructible deterministic configurations; not equated to physical CM |

The graph-to-H stage can use the same scan/output envelope; composing the two fixed compilers stays within O(U^4) for this U. A source SAT witness lifts by choosing either frame orientation per link; a target witness projects by reading occurrence copies. If witnesses are requested, their actual O(n') entries, source rereads and verification are paid within the polynomial envelope. The decision solver need output only one label and is not required to construct that witness.

For a fixed target solver A under T_A(N')<=K(N')^a, the composed source solver runs D, then the same A on the generated target, then returns its decision bit or divides its exact count by 2^E. Counts have O(n') binary bits. Division by 2^E is a bit shift with exact divisibility on this image; even a simple tape implementation costs O(U^2). Overall time is O(U^4)+T_A(N'), peak space O(U+S_A), and physical CM is at most O(U^5)+O(T_A(N')(U+S_A)). These upper bounds concern the specified composition, not a mixture of executions. The theorem does not preserve exponent a: the compiler and changed encoding must be charged.

On the target input itself, the handoff cap ceilings remain S_A=O((N')^a), physical CM_A=O((N')^(2a)), minimum-description CM_A=O((N')^(a+1)), and count-map circuit size O((N')^a log N'), under its input-charge/model assumptions. Here none is exceeded. On an original encoded input use its own N and the composed runtime; never compare one regime's lower demand with the other's ceiling. Excluding a single fixed exponent would not exclude every polynomial exponent.

## Reproducible evidence

Run from repository root:

```sh
python experiments/t5_construction_occurrence5_20261121.py > results/raw/t5_construction_occurrence5_20261121.json
```

Code SHA-256: `830f2bf2a15a6282017701f527c6cea082a4d83360865aefd3a593a089b37cfb`.
No seed; deterministic exhaustive finite checks. The executed stage completed in under one second in this workspace. It is not a measured complexity lower bound.

The program exhausts all 15625 assignments to the six gadget variables (25 endpoint pairs, 625 auxiliary tuples each), obtaining exactly 2I_5. It enumerates all 3125 frame assignments, finding exactly ten. It checks all 16 subsets of the four possible clauses on four variables, plus zero-variable, unused-variable, duplicate, attained-degree-five, six graph and two renaming/reordering controls: **28 cases**. It checks all 125 tuples under color reflection, rejects five malformed bitstrings, and checks complete encoding round trips and degree/size formulas.

Target counts are obtained by exact local elimination and contraction, **not full enumeration of the expanded formula**. The verifier reads each actual six-clause block, computes its endpoint matrix, checks scalar identity and fresh private support, contracts it, and verifies the recovered source syntax up to its explicit map. Small source counts are independently enumerated; graph source counts sum their actual private-clause extensions. Consequently these tests corroborate the composition without pretending to perform 5^(n') assignments. The report's symbolic proof, not the finite list, establishes the universal statement.

| Source | N_H or N | n' | m' | N' | E | Source count | Target count |
|---|---:|---:|---:|---:|---:|---:|---:|
| duplicate single clause | 19 | 18 | 20 | 328 | 3 | 30 | 240 |
| empty graph image | 56 | 55 | 65 | 1239 | 10 | 10 | 10240 |
| edge image | 140 | 102 | 118 | 2594 | 18 | 240 | 62914560 |
| triangle image | 235 | 142 | 164 | 4094 | 25 | 960 | 32212254720 |
| K4 image | 318 | 193 | 223 | 5561 | 34 | 0 | 0 |
| path4 image | 270 | 160 | 184 | 4592 | 28 | 6400 | 1717986918400 |
| star4 image | 270 | 160 | 184 | 4592 | 28 | 7680 | 2061584302080 |

The raw JSON includes full source and target clause lists, target bitstrings, equality matrices, maps, exact integers and code/input hashes. Hash equality is not used as a semantic merge argument. The source/target count assertions are explicit exact integers, not UNKNOWN masquerading as UNSAT.

## Controls and model-transfer gates

- **Matching cycles / affine and Tseitin:** splitting applies equally to easy matching or affine-encoded sources. Equality contraction returns those sources, so their cheap global algorithms survive. No forced separate processing of 2^E extensions; those extensions have the scalar formula 2^E.
- **Private-leaf tree:** path4 and star4 remain tree controls after contraction/leaf elimination. Bounded-width dynamic programming is permitted. Their enlarged encodings do not make them hard; their proposed hardness role is rejected.
- **Forced domains:** Q permits every endpoint color; it forces only equality. H_G's palette restrictions are explicitly constructed by C-clauses and private leaves. Easy pinned/forced source instances stay easy after contraction. Degree-five does not remove this control.
- **Sharing, caching, renaming and relocation:** one shared source variable becomes a syntactic path, but a solver may merge it back after checking the local semantics. Source/argument/clause permutations preserve the count identity. Relocating data or changing layout is legal and paid; no fixed-cut revisit premise is assumed. A branch result may be cached once and reused.
- **Complement:** color reflection x->-x mod5 preserves C; the finite test checks every tuple. Arbitrary five-color permutations are not asserted to be relation automorphisms, and Boolean complement is not silently installed as a primitive.
- **Decision-witness / full-state entropy:** K4 produces UNSAT while triangle produces SAT. Decision equivalence is proved both ways without requiring a decision solver to enumerate witnesses. Complete deterministic state determines the eventual answer; H(answer | complete state)=0. Auxiliary solution entropy does not measure remaining computation.
- **DISJ sanity — NOT APPLICABLE to the construction as a communication lower bound; OPEN for the downstream dynamic claim.** No communication protocol or compulsory cut demand is inferred.
- **Relativization — PASS for the syntactic reduction; OPEN as a separation gate.** It is a direct finite gadget identity and introduces no nonrelativizing lower-bound step.
- **Simultaneous DTISP — PASS for the one described compiler/composed execution; OPEN for any excluding lower bound.** Physical and descriptive CM are separately labeled.
- **Deterministic configurations — PASS as an accounting upper-bound safeguard.** No state-count lower bound is asserted. Algebrization and Natural Proofs supply no resolved barrier here; neither is bypassed by an equality gadget.

The expanded equality family itself collapses to a cheap scalar factor times its source. It is retained as a normalization tool/control and **FALSIFIED/RETIRED as an independent source of compulsory hardness**. The arbitrary graph core's unrestricted hardness remains OPEN rather than being inferred from its width or representation.

## Fresh literature and official-repository search log

Searches performed 2026-11-21 during this run, bounded to the equality/occurrence dependency. Earlier search logs were consulted to avoid re-auditing unrelated broad theorem claims.

**Primary literature.** Query: `bounded degree counting constraint satisfaction equality Dyer Goldberg Jerrum`. Read Dyer, Goldberg, Jalsenius and Richerby, *The Complexity of Approximating Bounded-Degree Boolean #CSP*, STACS 2010, pp.323–334, [publisher PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol005-stacs2010/LIPIcs.STACS.2010.2466/LIPIcs.STACS.2010.2466.pdf), especially section 4, p.329, equality simulation and Proposition 4.1. Their definition requires equal extension multiplicities on the two Boolean values and controls port degree so each port can be used once more. Their stated reduction is approximation preserving and permits unary pins. This motivates the extension-count/port-degree checks, but is not a theorem about five-valued pin-free C. Our exact five-valued identity is proved above; no Boolean classification or approximate-hardness conclusion is imported. The paper's affine and degree-two discussions reinforce the need not to infer hardness from bounded degree alone. Publisher version was read; arXiv 0907.2663 and 1001.4987 appeared in search, but were not separately reviewed.

**Official ownership.** [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai) organization pages show verified corporate domains. [x.ai/open-source](https://x.ai/open-source) links xai-org/grok-build directly. A [Google Research publication](https://research.google/pubs/implicit-rate-constrained-optimization-of-non-decomposable-objectives/) explicitly links google-research/google-research. [Google DeepMind's MuJoCo announcement](https://deepmind.google/blog/open-sourcing-mujoco/) links the repository and redirects to google-deepmind/mujoco. [Google's OR-Tools site](https://developers.google.com/optimization) links google/or-tools. Thus ownership was checked through domains and official cross-links, not product-like names.

| Organization and fresh query | Retrieved source/revision and relevance |
|---|---|
| Anthropic, web `site:github.com/anthropics formal math equality SAT` (also bounded-occurrence wording) | formal-math ETH README/statement hits; no strict five-color equality gadget in the returned hits. Prior inspected pin `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` is prior context, not a newly verified kernel build. Broad ETH headlines are not used as established theorems. |
| OpenAI, web `site:github.com/openai math constraint satisfaction equality` | math/preprints games/constraint-label results and comparator statement hits. No applicable strict-C degree-five implementation in returned hits. Prior README pin `4eaee87548250b2682affda7d05d947c05554bae` is prior context only. No theorem imported from snippets. |
| xAI, GitHub org xai-org query `SAT equality constraints` | grok-build `crates/codegen/xai-grok-tools/src/types/requirements.rs`, search pin `2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8`; returned fragment compares tool parameter values. Rejected as unrelated to CSP equality simulation; whole repository not audited. |
| Google Research, GitHub org google-research same query | google-research `gift/tasks/domain_mapping_utils.py` and vocabulary hit, search pin `87e25a5ba04d2c4cf0108f0cec96d648fe2b945a`; pairwise tensor equality/Sinkhorn constraints are not a finite-domain gadget theorem. |
| Google DeepMind, GitHub org google-deepmind same query | mujoco doc/changelog.rst and doc/mjx.rst, search pin `7a587a978699cd60d2466117aeba559492ea05b3`; mechanical equality constraints do not simulate C. Rejected scope, no proof imported. |
| Google, web `site:github.com/google constraint programming OR-Tools SAT equality` | Read `ortools/sat/README.md` on stable, ref `100f66e6242ab8bf8d32feb8f3bf086db66ae2b5`. CP-SAT table constraints, presolve and solution checking are useful reproducibility alternatives; no unrestricted lower-bound theorem. Not installed or executed. The small gadget is exhaustively checked by the supplied standalone code instead. |

Connected keyword coverage returned noisy unrelated hits; web fallback was used for literature, Anthropic/OpenAI and OR-Tools. No access failure was used to invent a source. These are bounded search findings, not assertions that the organizations have no relevant research. No new external formal kernel, CP-SAT or literature theorem build was executed.

## Status and next dependency

| Claim | Status and review |
|---|---|
| Full-domain six-clause equality with exactly two extensions | PROVED/EXACT here, COMPUTATIONAL 25-pair corroboration; independent review pending |
| Universal occurrence-five reduction with exact multiplier and encoding | PROVED/EXACT here; independent review pending |
| Graph decision equivalence and weighted count after splitting | PROVED/EXACT composition; original construction source pinned above |
| 28 finite compiler/control cases | COMPUTATIONAL, reproducible; not an asymptotic lower-bound test |
| Added equality paths force large computational work | FALSIFIED/RETIRED as a hardness inference by exact contraction |
| Compulsory decision demand beyond a fixed polynomial cap | OPEN |
| P versus NP | OPEN |

**Next: Accounting's T5-BOUNDED-3COL-DYNAMIC1.** For a specified distribution of B_G and arbitrary fixed correct A under T<=K(N_B)^a, identify actual decoded obligations with explicit side information, event capacity and bounded reuse **after** allowed contraction and algebra. Prove a total demand exceeding b r K(N_B)^a, or provide a legal solver/control invalidating the obligation. Redteam should first independently reconstruct the six-clause interface, degree count, unused-variable case and N-versus-N' distinction. Synthesis should retain the decision branch separately from orbit-quotient pseudoentropy.

No local checkout was available, so repository preflight was not run; connected full-file recovery and source pins were used. No LaTeX manuscript build or proof-assistant verification was run. No schedules, roles, enabled states, peer files or TMR ownership were changed.

