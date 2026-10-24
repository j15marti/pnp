# SIL-RC 0.1: Local CNF Reduction Classification

SIL-RC::0.1::2026-10-24

Status: PROPOSED DERIVED-ALIAS REGISTRY. This document does not change canonical SIL semantics, root main.tex, any task, or any schedule. The purpose is compact communication of known and recovered pattern simplifications, not a new SAT lower bound.

## 1. Naming and semantic contract

A rule ID consists of two mnemonic letters followed by a positive integer: CP2, VE3, EQ4, SP1. Lower numbers identify simpler cases within a family, not a global hardness ordering, runtime bound, or mandatory solver pipeline. Issued IDs must not be renumbered. Record parameter values separately.

SIL's original module semantics are G(I)=exists U F(I,U), with an ordered boundary I and internal variables U. The usual replacement contract is exists U F(I,U) equivalent to exists U' F'(I,U'). The outside context may share only I. Original source-variable identities and all cross-module occurrences must remain coherent.

Preservation modes:

- E: exact logical equivalence on the stated visible signature. A gate/XOR/cardinality relation can be the target representation.
- P: exact existential boundary preservation. Internal variables may be eliminated or fresh private auxiliaries introduced. Include reconstruction.
- S: whole-formula equisatisfiability only by default. This is not an arbitrary-context SIL replacement. A stronger boundary claim needs its own proof.
- CTX: equivalence only under an explicitly retained context and its dependency certificate.

Scope is independent of mode: a constant-size motif, full occurrence neighborhood, implication path, graph/module, or proof schema. Small displayed syntax does not imply cheap discovery or a small dependency footprint.

## 2. Catalogue

Notation: A and B denote disjunctions, possibly empty; l denotes a literal; x denotes a pivot variable. TRUE is the empty conjunction and FALSE the empty clause. A side condition referring to all occurrences means the entire current occurrence environment, not just the displayed clauses.

### CL: Clause cleanup

| Code | Pattern or operation | Mode / main guard |
|---|---|---|
| CL1 | (l OR l OR A) -> (l OR A) | E; same signed source literal |
| CL2 | (l OR NOT l OR A) -> TRUE | E; complementary pair in the same clause |
| CL3 | C AND C -> C | E; retain occurrence provenance separately for DeltaSIL |
| CL4 | FALSE AND F -> FALSE | E; actual empty clause, not an unread record |
| CL5 | Constant folding: FALSE OR A -> A; TRUE OR A -> TRUE; TRUE AND F -> F | E; constants must be certified |

### UP: Unit propagation and probing

| Code | Pattern or operation | Mode / main guard |
|---|---|---|
| UP1 | l AND (l OR A) -> l | E; keep the unit or equivalent fixed-coordinate trail |
| UP2 | l AND (NOT l OR A) -> l AND A | E; keep the unit/assignment |
| UP3 | l AND NOT l -> FALSE | E; units belong to the same context |
| UP4 | Repeat UP1/UP2, preserving fixed assignments and conflict provenance | E; BCP closure |
| UP5 | UP(F AND l)=FALSE implies NOT l; propagate it | E; failed-literal probing, charge the failed trial |
| UP6 | Derive l in both x and NOT x branches, discharge assumptions, then add l | E; two checked consequences |

### SS: Subsumption and strengthening

| Code | Pattern or operation | Mode / main guard |
|---|---|---|
| SS1 | A AND (A OR B) -> A | E; signed-literal subset test |
| SS2 | (x OR A) AND (NOT x OR A OR B) -> (x OR A) AND (A OR B) | E; self-subsuming resolution |
| SS3 | Replace C by a derived D subset C | E; clause vivification with a valid implication trace |
| SS4 | F0 AND C -> F0 when F0 entails C | E; implied-clause deletion, including asymmetric-tautology/RUP checks; no circular use of C |
| SS5 | Hidden-subsumption elimination | E; licensed hidden-literal closure plus a deletion-entailment certificate |
| SS6 | Asymmetric-subsumption elimination | E; licensed asymmetric-literal closure plus a deletion-entailment certificate |

### CP: Complementary-pattern contraction

| Code | Pattern or operation | Mode / main guard |
|---|---|---|
| CP1 | (a OR x) AND (a OR NOT x) -> a | E; two binaries become one unit |
| CP2 | (A OR x) AND (A OR NOT x) -> A | E; identical tail A, which omits x; valid even if x occurs elsewhere |
| CP3 | All 2^t polarity variants (A OR signed(x1,...,xt)) -> A | E; complete polarity cube, not a subset |

CP3 includes the four-clause FORCE(l;a,b) -> l identity. Missing even one required clause invalidates that contraction in general.

### VE: Existential variable elimination

| Code | Pattern or operation | Mode / main guard |
|---|---|---|
| VE1 | A private degree-one variable satisfies its sole clause; delete that clause | P; no omitted occurrences, pivot not on boundary |
| VE2 | Set a private pure literal true and delete all clauses it satisfies | P; complete polarity check |
| VE3 | exists x [(x OR A) AND (NOT x OR B)] -> A OR B | P; the two parents are all x-containing clauses |
| VE4 | VE3 where A OR B is tautological -> TRUE | P; private-pivot cancellation |
| VE5 | General Davis-Putnam elimination: replace all positive/negative pivot parents by all non-tautological resolvents | P; full occurrence environment and reconstruction |
| VE6 | Bounded variable elimination | P; apply VE5 only within an explicit output-size/work budget |
| VE7 | Exact 2-CNF projection onto a declared boundary X | P; SCC/reachability or elimination certificate; at most 2|X|^2 distinct unit/binary clauses for nonempty X, or FALSE |

VE5 can increase size and width. VE6 is an admission policy, not a stronger equivalence theorem. A pivot with one occurrence of one sign is a singular-DP specialization of VE5, not a new primitive.

### EQ: Equality and SCC quotients

| Code | Pattern or operation | Mode / main guard |
|---|---|---|
| EQ1 | (NOT x OR y) AND (x OR NOT y) -> EQ(x,y) | E; visible ports remain related |
| EQ2 | (x OR y) AND (NOT x OR NOT y) -> NEQ(x,y) | E; signed equality |
| EQ3 | Contract a private EQ/NEQ chain to its endpoint relation | P; parity of NEQ links determines the relation |
| EQ4 | Merge mutually implied literals using an implication-graph SCC | P; update all occurrences and retain maps for exposed ports |
| EQ5 | x and NOT x in the same implication SCC -> FALSE | E; retain both directed paths as a certificate |

### IM: Implication simplification

| Code | Pattern or operation | Mode / main guard |
|---|---|---|
| IM1 | From a->b and b->c, learn a->c | E; parents remain unless separately proved redundant |
| IM2 | Delete a binary clause with an alternate implication path | E; search with the candidate clause and both its edges removed |
| IM3 | If retained context proves a->b, replace (a OR b OR D) by (b OR D) | E; hidden literal elimination |
| IM4 | Hyper-binary resolution: (A OR l1 OR ... OR lt) plus all (NOT li OR b) entails A OR b | E; for binary output, |A|<=1; learning need not shrink immediately |
| IM5 | Hidden tautology elimination | E; licensed hidden-literal closure certifies the deletion, without circular support |

### GT: Functional gates

| Code | Pattern or operation | Mode / main guard |
|---|---|---|
| GT1 | AND gate: (-z OR a), (-z OR b), (z OR -a OR -b) -> z iff a AND b | E; all defining clauses present |
| GT2 | OR gate: (z OR -a), (z OR -b), (-z OR a OR b) -> z iff a OR b | E; NAND/NOR are signed-output variants |
| GT3 | Four-clause ITE gate -> z=ITE(s,a,b) | E; coherent selector and source inputs |
| GT4 | Six-clause majority gate -> z=MAJ3(a,b,c) | E; complete definition |
| GT5 | Delete an unused private output and its total functional definition | P; no external output uses |
| GT6 | Merge duplicate functional outputs | P; prove identical functions, update fan-outs, and preserve boundary equality if either output is exposed |

The GT3 clauses are (-s OR -a OR z), (-s OR a OR -z), (s OR -b OR z), (s OR b OR -z). GT4 has (-a OR -b OR z), (-a OR -c OR z), (-b OR -c OR z), (a OR b OR -z), (a OR c OR -z), (b OR c OR -z). Hash equality alone is not a GT6 proof. Gate extraction is a representation change, not permission to forget a shared output.

### XR: XOR and affine relations

| Code | Pattern or operation | Mode / main guard |
|---|---|---|
| XR1 | A complete parity-forbidding CNF block -> XOR(X)=b | E; includes four-clause XOR3 and functional XOR gates |
| XR2 | Invertible row XOR, duplicate-row removal, and 0=0/0=1 simplification | E; keep one parent while replacing the other by its XOR |
| XR3 | exists y [(a XOR y=p) AND (y XOR b=q)] -> a XOR b=p XOR q | P; y private and fully scoped |
| XR4 | Gaussian elimination to an exact affine boundary summary | P; do not omit non-affine clauses sharing eliminated variables |

### BC: Blocked and covered redundancy

| Code | Pattern or operation | Mode / main guard |
|---|---|---|
| BC1 | Blocked-clause elimination | S; one pivot literal has only tautological resolvents against its entire opposite-occurrence environment |
| BC2 | Hidden blocked-clause elimination, HBCE | S; hidden-literal closure and blocking proof |
| BC3 | Asymmetric blocked-clause elimination, ABCE | S; asymmetric-literal closure and blocking proof |
| BC4 | Covered-clause elimination, CCE, with HCCE/ACCE variants | S; covered-addition trace and blocked endpoint |
| BC5 | Set-blocked clause elimination | S; nonempty blocking set and every required neighborhood check |
| BC6 | Semantic/super-blocked clause elimination | S; full local repair obligation; not assumed cheap to discover |

For BC5, a nonempty L subset C blocks C if (C minus L) union complement(L) union D is tautological for every D containing a complement of a literal of L. BC6 uses the semantic/super-blocking definitions in the cited paper. These families generally change models. Boundary-safe use requires an additional projection argument, such as a private blocked pivot with reconstruction that fixes all boundary coordinates.

### FA: Factoring and cardinality recoding

| Code | Pattern or operation | Mode / main guard |
|---|---|---|
| FA1 | Rectangular factoring: AND_ij(Ai OR Bj) iff exists z [AND_i(Ai OR z) AND AND_j(Bj OR NOT z)] | P; z fresh, full rectangle present; pq clauses become p+q |
| FA2 | Complete negative binary clique -> AMO(X) | E; all pairs present |
| FA3 | Positive covering clause plus AMO(X) -> exactly-one(X) | E; same variable set |
| FA4 | Cardinality relation <-> certified auxiliary counter encoding | P; preserve original-variable relation, not necessarily full model counts |
| FA5 | (OR X) AND (OR NOT X) -> NAE(X) | E; same distinct source variables, t>=2 |

FA1 is a bounded-variable-addition schema. It is admitted only if the declared size objective improves; a 2x2 rectangle does not reduce clause count and adds a variable. The 2026 graph-theoretic BVA paper is a current supporting source, not a reason to equate compactness with hardness or solver speed.

### AU: Autarky elimination

| Code | Pattern or operation | Mode / main guard |
|---|---|---|
| AU1 | A partial assignment satisfying every clause it touches permits deleting those clauses | S; all occurrences checked; P if assigned variables are private and the lift fixes boundary |
| AU2 | Matching-autarky specialization | S; matching must yield an assignment passing the actual AU1 check |

Discovery is not free. A satisfying assignment for one isolated-looking subset is not an autarky if it damages another touched clause.

### DC: Decomposition and exact summaries

| Code | Pattern or operation | Mode / main guard |
|---|---|---|
| DC1 | Variable-disjoint factors -> SIL tensor/product | E; true source-variable disjointness |
| DC2 | A closed private component -> its exact TRUE/FALSE result | P; component decision must actually be performed and charged |
| DC3 | Exact separator join of child boundary relations | P; every shared source lies in the separator |
| DC4 | Closed 2-SAT/Horn/dual-Horn component decision | P; a nonempty boundary needs a relation, not one SAT bit |
| DC5 | Bounded module -> a smaller exact truth-table-equivalent representative | P; explicit size bound and exhaustive/equivalence certificate; no claim a smaller representative always exists |

DC3 does not combine independent child SAT bits when the children share variables. DC4 does not assert that every Horn projection is small. DC5 is an extensibility mechanism for new finite motifs, not an efficient unbounded complete SAT simplifier.

### SP: Recovered project macros

| Code | Pattern or operation | Mode / main guard |
|---|---|---|
| SP1 | SIL double-coincidence, four ternaries -> one ternary | P; boundary (x,a,b), private y,z |
| SP2 | CANCEL-JOIN69 eight-clause module -> two binaries | P; boundary (a,a_next,b,c), private x,y,z |
| SP3 | Context-certified pruning | CTX; retain the context proving the reduced boundary relation |

SP1 is the existing SIL section-16 identity:

exists y,z [(x OR y OR z) AND (x OR NOT y OR NOT z) AND (NOT y OR z OR a) AND (y OR NOT z OR b)] iff (x OR a OR b).

SP2 is the module

(a_next OR b OR x), (a_next OR b OR NOT x),
(NOT a OR c OR y), (NOT a OR c OR NOT y),
(NOT b OR x OR z), (NOT b OR NOT x OR NOT z),
(NOT c OR y OR z), (NOT c OR NOT y OR NOT z).

After existentially hiding x,y,z its exact replacement is (a_next OR b) AND (NOT a OR c). The proof is CP2 twice, then VE4 twice. A valid lift is z=0, x=y=1. Neither macro licenses merging independent copies of a shared source.

### PR: Proof-certified schemas

| Code | Pattern or operation | Mode / main guard |
|---|---|---|
| PR1 | RUP/implication-certified clause learning or deletion | E; adding C uses F entails C; deleting C must prove it from F without C |
| PR2 | RAT-certified redundancy addition/deletion | S; pivot and all resolvent obligations checked against the correct remaining formula |

These are proof-supported general schemas, not small recognizable motifs. A proof of UNSAT is not automatically a small relation summary. A fresh variable or model-changing step needs its own boundary/reconstruction record.

## 3. Required instance record

Every application carries: rule ID; source occurrence IDs; ordered boundary; internal variables before/after; substitution; preservation mode; retained context dependencies; complete side-condition certificate; proof trace; witness lift; model-count/extension information; source reads; discovery cost; proof-check cost; rewrite/output cost; peak simultaneous space; size before/after; and status.

Suggested compact log:

CP2 pivot=x clauses=[c17,c18] boundary=[a,b] mode=E cert=p12
VE3 pivot=u clauses=[c4,c9] boundary=[a,b,c] mode=P occurrences=complete lift=L7

These are proposed log aliases, not claims that an existing parser accepts new commands. They can be represented as annotations to SIL's existing cnf/project/meet/join/summarize_C operations.

## 4. Important limits

1. The catalogue is broad and extensible, not a claim to enumerate every possible or published rewrite. Each schema covers infinitely many variable-renamed and size-parameterized instances.
2. For b ordered boundary variables, an exact projected truth vector has 2^b bits. There are 16 binary, 256 ternary, and 65,536 quaternary relations. Matching these tables classifies bounded modules, not solver difficulty. Hidden-variable enumeration and canonicalization remain charged.
3. E and P do not automatically preserve DeltaSIL occurrence-deletion relations. A duplicate-clause deletion preserves ordinary models but can change the result of deleting a named occurrence later.
4. Projection does not generally preserve full witness counts or unique extension. SP1's hidden extension counts for boundary rows 000 through 111 are 0,1,1,2,2,3,3,4.
5. Proper-3CNF and exact occurrence quotas are not automatically preserved by simplification. Recompute grammar membership or charge a recoding.
6. An adaptive policy may select any currently certified rule from observed state. IDs are not a fixed order. Failed tests, switches, discarded work, caches and replay are included in the cost ledger. The finite rule list is not coverage of every SAT algorithm.
7. Ordinary resolution only learns a consequence. Replacing both parents by the resolvent requires VE3/VE5's full private-pivot existential conditions.
8. P versus NP is unchanged by this nomenclature or by finite tests.

## 5. Independent bounded audit

The accompanying local standard-library verifier made 2,793 assertion-accounted checks with zero failures. It checked selected elementary schemas, full DP projection on seeded small formulas, gate truth tables, parity blocks, rectangular factoring, the exact SP1/SP2 projected relations and reconstruction, 586 blocked-clause deletion instances, and explicit side-condition counterexamples.

The counterexamples reject incomplete polarity cubes, incomplete XOR blocks, omitted pivot occurrences, erased boundary units, ordinary-SAT versus DeltaSIL confusion, model-count preservation after projection, width-preservation assumptions, dropping both resolution parents without projection, and dropping a contextual assumption.

Four small adaptive controls cover SAT and UNSAT paths, complementary contraction, propagation, a charged VE6 trial, and a bounded complete truth-table fallback. Counters are abstract source/literal events, not exact RAM instruction counts or Python RSS. Advanced HBCE/ABCE/CCE/set/super-blocking/RAT matchers are catalogued, not implemented by this auditor.

Audit seed: 20261024. Full machine-readable catalogue and runnable audit are supplied in the conversation's downloadable bundle; this repository document does not falsely assert those local files are available to another runtime. This catalogue itself must be read back before publication is reported as verified.

## 6. Sources and prior-name crosswalk

- Canonical SIL grammar, fetched document headed version 1.4.0: https://docs.google.com/document/d/1gh6-ywWpijJHVGO794r3j2hFouZBVT8Im5vwNPORxyI/edit . Sections 2,5,6,9,13,16 supply boundary semantics, S0/S1/S2 distinctions and SP1.
- Een and Biere (2005), Effective Preprocessing in SAT Through Variable and Clause Elimination: https://cca.informatik.uni-freiburg.de/papers/EenBiere-SAT05.pdf . VE, subsumption, SSR and gate extraction.
- Heule, Jarvisalo and Biere (2010), Clause Elimination Procedures for CNF Formulas: https://www.cs.cmu.edu/~mheule/publications/LPAR17.pdf . Hidden/asymmetric subsumption, tautology and blocked variants.
- Heule, Jarvisalo and Biere (2011), Efficient CNF Simplification Based on Binary Implication Graphs: doi:10.1007/978-3-642-21581-0_17 . EQ/IM.
- Jarvisalo, Heule and Biere (2012), Inprocessing Rules: https://www.cs.cmu.edu/~mheule/publications/rules.pdf . Proof, redundancy and reconstruction distinctions.
- Li et al. (2020), Clause Vivification by Unit Propagation in CDCL SAT Solvers: https://doi.org/10.1016/j.artint.2019.103197 . SS3.
- Kiesl, Seidl, Tompits and Biere (2018), Local Redundancy in SAT: Generalizations of Blocked Clauses: https://arxiv.org/html/1702.05527 . BC1, BC5, BC6.
- Heule, Jarvisalo and Biere (2010), Covered Clause Elimination: https://arxiv.org/abs/1011.5202 . BC4.
- Manthey, Heule and Biere (2012), Automated Reencoding of Boolean Formulas: https://research.jku.at/en/publications/automated-reencoding-of-boolean-formulas/ . FA1.
- Przybocki, Subercaseaux and Heule (2026), Automated Reencoding Meets Graph Theory: https://arxiv.org/html/2603.27774 . Current BVA structural perspective.
- Soos (2012), Enhanced Gaussian Elimination in DPLL-based SAT Solvers: https://easychair.org/publications/paper/j1D . XR.
- Sinz (2005), Towards an Optimal CNF Encoding of Boolean Cardinality Constraints: doi:10.1007/11564751_73; author source https://www.carstensinz.de/software.html . FA2-FA5.
- Kullmann (2000), Investigations on Autark Assignments: doi:10.1016/S0166-218X(00)00262-6; Kullmann and Marques-Silva (2015), https://arxiv.org/abs/1505.02371 . AU.
- Aspvall, Plass and Tarjan (1979): doi:10.1016/0020-0190(79)90002-4 . SCC and Krom background.
- Dowling and Gallier (1984): doi:10.1016/0743-1066(84)90014-1 . Bottom-up Horn forward chaining.
- Project CANCEL-JOIN69: research/agents/lspv-2/2026-10-24_0812_LSPV-2_CANCEL_JOIN69.tex . SP2 and VE4 application.

Prior SIL normalization names map to these aliases: N_prod -> DC1; N_aff -> XR4; N_impl -> EQ4/VE7; N_Horn -> DC4 for closed decision or separately certified nonempty-boundary summaries; N_tw -> DC3 with a supplied, charged decomposition; N_local -> the appropriate certified motif. BOOL remains a derived rewrite medium, not a replacement for SIL semantics.

END_OF_SIL_RC_CATALOGUE::0.1::70_RULES
