# Discovery: flat authenticated renaming has bounded closed defect
Pacific timestamp: 2026-11-21 08:59 PST (America/Los_Angeles).
Named lemma: **T5-FLAT-RENAME1**, a restricted instance of Synthesis's T5-NAND-CLOSED-DEFECT1.

**PROVED/EXACT, restricted architecture:** a scalar counter using native DLDD operations plus flat renaming of explicitly constructed, authenticated DLDD templates has cumulative extension cost O((W+v+1)^2), including its final target-resolving action. A renamed view may reuse a count without copying its diagram physically. The theorem charges building the base and authenticating the map, and bounds the diagram that could be obtained by expansion.
**COMPUTATIONAL:** 2,688 permutation/template checks, 175,616 Boolean semantic evaluations, and 40 rejected invalid cases pass.
**OPEN:** an analogous polynomial defect bound for arbitrary scalar counters, or even unrestricted recursive template reuse. Independent adversarial review is requested, not received. This is not a new unrestricted counting or decision lower bound.

## Exact target, quantifiers and falsifiers

For every fixed deterministic correct counter A in the architecture below, every valid input x in its declared strict-C NAND-graph image, and its actual finite execution of charged primitive work W=T_A(x), let v be the number of normalized Boolean graph variables. There is a constant c_A independent of x such that
```
R_F(empty) <= sum_j kappa_j <= c_A (W+v+1)^2,
Delta_c = sum_j [kappa_j-c q_j]_+ <= c_A (W+v+1)^2
```
for a disjoint partition into charged actions q_j>=1, including final resolution of F=f_G. The lemma also applies to other Boolean source classes with the same authenticated architecture; this broader statement is a representation simulation, not a hardness assertion.

The machine model is the handoff's fixed finite-control/finite-alphabet sole read/write tape, charged input, head positions and output. No free oracle, externally supplied template, advice, or source store is granted. A may choose orders, parameters, decomposition, candidates and cache policy adaptively. Arbitrary global methods are legitimate algorithms, but are covered by THIS theorem only if their resolutions meet the declared rules. An algorithm can be correct outside this input image by an explicitly paid fallback; no global polynomial bound is assumed from that.

Fix K,a>=1 independently of x when comparing W<=K N^a. There is no changing exponent or padding regime hidden in the statement.

Four concrete falsifiers:
1. A valid flat-view execution whose copied base requires more than one renamed copy per distinct view, despite memoizing old-node IDs.
2. A bijective source map that passes exact authentication but changes the predicate/count, including declared unused variables.
3. A final output accepted as a resolved target although it has no derivation by native operations or the declared flat rule.
4. An accepted base containing an unmaterialized lazy view, or a size-dependent template loaded without charging its creation/access.

Items 3–4 violate the proposed architecture and must be rejected by an implementation; silently permitting them would invalidate this theorem's application. They are explicit scope checks, not reasons to reject legitimate algorithms from the unrestricted problem.

## Recovery and dependency

Recovery began at 358200a519d8cd27b33a02a12bb1b6b7db24a825 and includes Accounting publication fd693f40c606be2453db0440504cdfd7de49ff89. The complete handoff was already read in this continuous work; a fresh complete fetch is byte-identical, blob a886f3387a8676b9cc86afbf3bebf22630109d49, to baseline 10d2ccb2062c3efd4b4f03873eaa88822edf732f. AGENTS.md, CODEX.md, repository research instructions and the current assignment directive were recovered unchanged. The new Discovery handoff returned 404, so this run creates its own.

A fresh prefix search recovered the latest [Discovery 07:53 selector-resolution report](https://chatgpt.com/library?file_id=libfile_7f7b5aa9cdb4819185bb4520b81d2b6d&account_id=personal). Its actual content and earlier evidence were recovered: the L+3m forward resolution lift concerns a different source interface and gives no scalar-to-DLDD compiler. That experiment is not repeated.

The immediate dependency is [Synthesis T5-TERMINAL-DEFECT1, c4b8923](https://github.com/j15marti/pnp/blob/c4b8923cb7437f2794fa0da3181be3795dd2e35b/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-21_082800_Terminal_Defect.md). Its report, code/raw evidence and handoff were recovered in this continuous work: R_0<=r_end+sum kappa, and adding the root costs exactly r_end. The [original Parameterized Aggregate Progress, Section 7](https://chatgpt.com/library?file_id=libfile_6b014b0aaa8c81919e054356c46107c6&account_id=personal) was read directly, including its semantic-annotation convention. This run bounds one specific shortcut and closes the target within that architecture; it does not require the original arbitrary counter to output a diagram.

Relevant peer restrictions: Construction 358200a supplies a separate decision-sensitive three-color interface and weighted count; it is not the NAND family here. Accounting fd693f4 requires real selector/timing/address charges, so discovery/access metadata are not free. Redteam 4b84b9c preserves same-execution circuit/CM accounting and still lacks an independent count-map lower demand. Issue #324 was read through those publications. No peer has independently reviewed this new lemma.

## Strict-C input and normalized interface

C consists of all permutations of 012,123,234,340,401, exactly 30 ordered tuples. Every clause uses three distinct variable names, initially all with domain Z_5; no input constants or signs. Ordered R has 40 tuples and is a different problem. No S/Q result is used.

For a simple bipartite graph G=(L,R,E), the baseline NAND source has five anchor variables a_0,...,a_4 and the five cyclic clauses C(a_i,a_(i+1),a_(i+2)), indices modulo five. Add C(a_0,a_1,X_u) for each left u, C(a_0,a_4,Y_z) for each right z, and C(a_0,X_u,Y_z) for each edge uz. Thus
```
n=v+5, m=5+v+e, w=ceil(log2(n+1)),
N=n+1+2 floor(log2(m+1))+1+3mw.
```
For each of the ten anchor frames, left values are a_2/a_4 and right values a_3/a_1. Selecting a_2 on the left or a_3 on the right gives Boolean variables; precisely the pair of selected endpoints is forbidden. The normalized witness predicate is
```
F=f_G=AND_(uz in E) NOT(x_u AND y_z),   #C(source)=10 #F.
```
Declared isolates remain in scope and contribute their factors of two. The exact interface is R_A(b)=exists y A(b,y); fixing the frame and interpreting graph variables as above yields F(b), with no independently chosen assignments for different edges. Source recognition, frame/extraction justification, and the final multiplication by ten are charged. The fixed C pair table directly verifies the stated three allowed edge pairs; this known gadget is context, not a rerun of its earlier full assignment experiment.

This family is always SAT. Its witness lower bounds support a restricted EXACT-COUNTING architecture analysis only. They do not make its decision problem hard and do not replace Construction's separate three-color decision path.

## The declared architecture and authenticated shortcut

A native record is a constant/literal, a decision on a variable absent from both child diagrams, a NOT, or a binary Boolean operator whose child diagrams have disjoint mentioned-variable sets. Each record has explicit named scope, child IDs and exact count/probability information. No overlapping binary operation is admitted merely because its counts happen to match. Count arithmetic and all scope verification are paid. Explicit records form actual DAGs; reuse follows their identities.

An ordinary base template B_i is an explicitly materialized DLDD with s_i nodes, a declared scope S_i, an authenticated source predicate g_i and a computed exact count Z_i. Its nodes contain NO lazy renaming references. It has been built and checked during this execution from native records; no unverified equivalence certificate or hardwired size-dependent diagram is assumed. Constant many fixed-program records can be absorbed into c_A. Reconstructed/deleted records cost again. Let S_max=max_i s_i over the run. Explicit construction and the free O(v) initial literal convention give
```
S_max <= c_A (W+v+1).
```

The ONE new shortcut, FLAT-RENAME, takes:
- an ordinary base B_i and its typed source g_i;
- an explicit bijection pi:S_i -> S' onto a declared target scope;
- authenticated target source h with exact syntactic equality h=pi(g_i), under a fixed transparent source normalization.

It returns the scalar Z_i and a typed semantic view of pi(g_i). The physical view may retain only the base ID, pi, source references and count. It need not physically construct s_i copied nodes. All map discovery, failed maps, source reads, bijectivity checks, record creation, accesses and count output are included in W.

A concrete verifier for graph NAND sources checks every declared name, exact edge list and any explicit pins; compares the mapped sorted lists with full data equality; and checks the scope including isolates. For strict-C whole-source isomorphism, it also maps/checks anchors, left/right domain clauses and all actual C triples. Predicate-level normalized graph maps require the already authenticated normalization derivation; a raw-C isomorphism is never inferred from a Boolean count alone. The executable controls below test the normalized Boolean interface, not a new raw-C parser.

Given a candidate map and source records of total bit length L, direct repeated scans, comparisons and sorting give a conservative O((L+1)^4) one-tape verification bound with O(L+1) stored bits. This does not bound FINDING the map: enumeration or another algorithm pays its actual time, including failed candidates. No polynomial graph-isomorphism discovery theorem is assumed. Hash equality alone cannot pass the verifier.

A view of a view is allowed only after explicitly composing its maps back to the same ordinary base; this composition is charged. A native combination containing views may be used normally with typed children. It may NOT be renamed wholesale as a new base until it has actually been expanded/materialized and that work charged. This is the flatness restriction. Parameter choices, branching orders and choice among eligible bases remain arbitrary and adaptive.

The final scalar is accepted as resolved F only when the native/view derivation is tied to the actual target relation. Opaque scalar answers obtained by an additional rule are outside the proved architecture, even if correct. Such rules are legal unrestricted computation and would require their own defect analysis.

## Proof, including cumulative cost and terminal closure

**One view.** Traverse its ordinary base in topological order and memoize one copied ID per original node. Replace every variable label z by pi(z), retain operator labels, and connect copied parents to copied children. Bijection preserves the absence of decision variables below decisions and preserves disjointness at binary nodes. Induction gives the predicate pi(g_i). Each original node is copied at most once; common children remain common. Thus this typed view has extension cost at most s_i (up to the fixed constant-node convention), regardless of how often its handle is subsequently used. This construction does not assume that the copier is run free by A.

A bijection of declared assignment spaces proves equality of exact counts; free-variable multiplicities agree. A short scalar value by itself proves neither this predicate identity nor the existence of a legal view.

**Whole run.** Refine actions so that each native output has constant extension cost and each successful view has the bound just proved. Multioutput actions can instead use their joint expansion; charging them separately only weakens this upper bound. The architecture charges at least one primitive step per emitted record and a fixed finite number of records per step, so the number H of native outputs and J of successful view events are each O_A(W). The costs of failed search, parsing, arithmetic, switches and all other work occur in the same disjoint partition; those actions add no relation handle unless a declared rule justifies one.

Then
```
sum_j kappa_j <= c_A H + sum_(view events j) s_base(j)
              <= c_A W + c_A W S_max
              <= c'_A (W+v+1)^2.
```
This is an upper bound on proof extension costs, not a sum of alleged independent lower demands. Copies shared within a view are counted once; repeat reference to an existing named view has extension cost zero. Deleting a physical base/cache entry never gives free access; a subsequent copy must have a retained base or pay reconstruction. Native operations need their typed children. The loose bound remains valid if an identical view is deleted and later re-created, because that is another charged event.

Apply the original substitution lemma action by action. Deletions can increase the remaining completion cost, so they cannot invalidate R_0<=sum kappa for a trace whose final target is resolved. Every final resolution is a native action or an authenticated view, hence is already included. There is no uncharged semantic root insertion. Consequently R_0<=sum kappa and Delta_c<=sum kappa for every fixed c>=0. This proves the two stated bounds.

Equivalently, one can expand each distinct view once into an ordinary DLDD and retain the outer native DAG. If its outer native node count is R and its distinct views use bases of sizes s_i, the expanded DAG has at most R+sum_views s_i+O(v) nodes. An old-node-to-new-node table preserves sharing. This gives a uniform polynomial-size expansion GIVEN the authenticated trace and bases. It is not a polynomial algorithm for discovering that trace from the original source.

For a fully explicit implementation, the expanded serialization length is O((v+R+sum s_i+1) log(v+W+2)). Ordinary finite-list scans and topological copying produce it in polynomial time and storage in that length plus the supplied trace length. These are separate extraction costs, not charged back as if A had actually allocated the expanded DAG.

## Consequence for the restricted cap, and the unrestricted gap

Let L(F) be any independently established ordinary DLDD node lower bound for the SAME fixed witness F. The proved expansion gives
```
L(F) <= c_A (W+v+1)^2.
```
This is the exact reduction in the exponent incurred by the new rule. Under W<=K N^a, v<=N and a>=1, L(F)=O_A,K(N^(2a)) is necessary for this architecture.

Conditionally plugging in the handoff's bounded-degree graph premise L(f_G)>=2^(lambda_Delta sqrt(tw(G))) yields W+v+1 >= c 2^((lambda_Delta/2) sqrt(tw(G))). Equivalently a polynomial cap implies tw(G)=O_A,K,Delta(a^2 log^2 N) along the same input encoding. The graph-family lower-bound premise is retained from the baseline, not independently recertified by this run. No upper bound in a parameter has been inverted into a lower bound.

Primary source [Beame–Li–Roy–Suciu, 2017](https://homes.cs.washington.edu/~beame/papers/numsat-journal.pdf), Definition 2.4 and Theorem 3.1, was read directly. It specifies the DLDD model and its quasipolynomial FBDD simulation. Our copying proof uses the definition, not an unrestricted lower bound from that paper. Nodes in that theorem are representation size, not encoded T5 input length N.

The missing unrestricted implication remains: every arbitrary scalar counting method would have to admit a similarly charged, polynomial-defect explanation. Flat explicit templates do not establish that. Affine/Tseitin controls already prohibit a generic scalar-to-witness compiler. No unrestricted count-map circuit lower bound has been proved; no decision P-versus-NP consequence follows.

## Resource ledger on the same execution

| Item | Charge/limitation |
|---|---|
| Input and authentication | N source bits, all parsing, exact source/target comparison, scope and relation normalization; no free named-graph oracle. |
| Discovery and failures | Actual strategy/order/parameter selection, template search and every rejected mapping in W; supplied short map does not include its discovery. |
| Base construction | Actual explicit nodes, wires, bit-lengths, count/probability arithmetic, child lookup and verification; size <= O_A(W+v+1). |
| View creation | Explicit base reference, named bijection, source records and scalar count; map and addresses are real data. |
| Evaluation | Existing exact count reused only after authentication; native DLDD probabilities/counts evaluated with exact integer arithmetic, O(v)-bit values under uniform Boolean assignments. |
| Sharing/retention | Retain actual templates, maps and live count data once per identity; distinct renamed scopes are distinct views. Proof expansion sharing is not free physical memory for A. |
| Deletion/recomputation | Access to an erased record requires reconstruction or another legitimate source, with its entire cost. |
| Output | Boolean count up to 2^v, T5 count up to 5^n; write all result bits and any requested evidence. Invalid certificates yield UNKNOWN, never UNSAT. |
| Peak simultaneous physical space | Source, bases, maps, call state, counters and outputs coexist. Same A with W<=K N^a has S=O_A(N^a) under the charged-input convention; the virtual O(W^2) diagram is not asserted to be live. |
| Physical versus descriptive CM | Retain physical CM O(N^(2a)) and minimum-description CM O(N^(a+1)) separately. No code-length-to-physical-storage substitution. |
| Count-map circuit ceiling | O(N^a log N), as in the baseline; distinct from this fixed-instance witness expansion. |
| Research computation | Python finite checks of Boolean sources and explicit copying; no measured bit-machine runtime, peak heap bound or asymptotic experiment. |

The polynomial copying algorithm does not supply a fast generator for templates. Conversely, if a purported scalar shortcut has no explicit authenticated base, it cannot invoke this bound by naming one that exists nonuniformly.

## Tests and controls tied to this rule

Reproduce:
```
python experiments/t5_discovery_flat_rename1_20261121.py
```
Raw evidence: results/raw/t5_discovery_flat_rename1_20261121.json.
Code SHA-256: ea861c90b47cdacdc09d7d51e76ffe3ff537ba9ee636315e3fbfe6c7d336b676.
Raw SHA-256: 93325457f0ef7eef7a5128f6e5ee539eac3f286093c5ce525375ff4db20fb74c.

Eight explicit sources: matching, four-cycle, five-vertex private-leaf tree, K2,3, forced K2,3, even parity, inconsistent parity, and a declared free scope. For each, two branching orders and both polarities were tested. Every permutation of the four/five declared names was checked. The base generator explicitly enumerates assignments; its expensive discovery is recorded, not replaced by the tiny output count. A mapped base is copied with memoized old-node IDs, referenced seven further times without more copies, and combined with a second disjoint copy using AND/OR/XOR/equivalence. All joint truth tables are checked. Exact source comparison rejects nonbijections and modified source constraints; overlapping nonconstant binary children are rejected. The experiment is deterministic, no seed.

The results are 2,688 permutation checks, 175,616 semantic evaluations and 40 invalid-case rejections. Raw rows include base sizes, counts, discovery leaf evaluations, copied-node visits and actual expanded-node counts. Finite checks support implementation mechanics; the all-input bound follows from the proof above.

Complement is a native NOT, with its true representation cost included. The private-leaf tree returns count 13, not a hard-family claim. Forced K2,3 returns one; inconsistent parity returns zero; free scope returns 16 despite a constant diagram, verifying declared-scope factors. These affine controls use small examples and do not retest the published high-width obstruction: a Gaussian-only solution of a high-width affine system remains an allowed escape outside this explicit-base architecture. Renaming/sharing are the new tested rule. Relocation changes actual access work but not copying semantics; no fixed cut is used. Decision-witness packing is not invoked. The all-SAT NAND scope is explicit.

DISJ gate: NOT APPLICABLE, no communication lower bound imported. Relativization gate: OPEN for unrestricted promotion; this structural simulation supplies no nonrelativizing hardness. Simultaneous DTISP gate: PASS for bookkeeping, no new forbidden region. Deterministic-configuration gate: PASS, no state-count runtime inference. Natural Proofs/algebrization: NOT APPLICABLE to this representation-copying lemma; no general circuit lower bound is asserted.

## One next dependency

**Owner Discovery; adversarial review Redteam; track in Synthesis: T5-NESTED-RENAME1.** Permit a renamed template whose ordinary outer DAG itself contains lazy renamed subtemplates, without requiring full materialization. Either bound its CLOSED cumulative defect in terms of actual encoded records/maps and work, or produce an in-class family with superpolynomial expansion. The certificate must track original-variable scopes and actual shared identities; a repeated occurrence is not automatically repeated physical work. Do not assume a general recursive grammar expands polynomially.

This is a strict follow-up to the proved flat case, not an assertion that nested reuse is already a counterexample. The unrestricted bridge remains OPEN even if another restricted closure theorem succeeds.

No TMR manuscript ownership acquired or file edited. No checkout/preflight or LaTeX build was available/run. Publication uses the owned report, compact handoff, executable code and raw evidence with a current-head lease and exact readback. P versus NP remains OPEN.

