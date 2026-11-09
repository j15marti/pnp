# LSPV-1/541: exact source-fixed auxiliary-name orbit quotient for paid proof construction

**2026-11-09 11:00 PST | Route B | PROVED/RESTRICTED theorem + COMPUTATIONAL controls | P versus NP OPEN**

**Affected proof-chain proposal:** [P2-L1-541], a restricted positive implementation component for still-OPEN [P2-C3]. Authentication [P2-D1], all-rule minimum [P2-B1], noncircular same-R B3 [P2-B2], and Route A remain OPEN. No inference weight or native grammar is changed.

## IDEA and falsifiers stated before searching

**Candidate.** For a source-fixed proof-construction transition system whose legal rules and native logical weights are equivariant under globally consistent finite permutations of fresh auxiliary variable names, quotienting complete paid-history-aware states by these permutations is an **exact weighted bisimulation**, not merely a cost-underestimating abstraction. It preserves the optimal whole shared refutation DAG cost at every budget, while removing irrelevant large auxiliary-number choices.

F1. A historical native rule examines the **numeric magnitude, relative ordering or encoded length** of an auxiliary identifier, or requires a non-equivariant exposed positional port. Then the symmetry assumption fails and this quotient is not automatically sound.

F2. Independently canonicalizing branch-local nodes instead of **one entire configuration** merges incompatible definitions or assumptions; that is not the quotient claimed here.

F3. Permuting original CNF variable names or original-source clause identifiers loses source authentication. The group must fix the entire original source and all occurrence identities.

F4. Equating equal conclusion labels rather than preserving paid occurrence IDs and all dependency hyperedges can create cycles and incorrectly charge shared subproofs, as demonstrated by LSPV-5/464. That quotient is excluded.

## SEARCH and continuity

Read both root proof trackers, active issue #3 through LSPV-5/465, governing 2026-11-09 abstract-interpretation handoff, AGENTS.md, CODEX.md, research skill, original LSPV-2/341 rule declaration, prior LSPV-1/539-540, LSPV-3/538, LSPV-5/464-465, actual GROKPROOF/2026-11-09_1230_PROGRESS.md, and Claude world-ledger report. Earlier root MAIN /364 and /369 already establish scoped **offline** dependency-preserving renamings and DEF-alpha-normalization; this run does **not** claim that alpha-renaming or nominal symmetry was invented here. The narrower new formal target is an **online weighted transition-level** quotient, global paid-state bisimulation and budgeted lower-bound-transfer condition.

Current repository evidence: konard/p-vs-np README.md (blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95) and scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2) only formalize finite-machine-scoped results; blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5) contains scoped alternative methods, not the native calculus. Relevant format/control files: meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f), tanyongkiam/cake_lpr README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c), MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab), and openai/math README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae). All are evidence, not authority to change R_mix341.

Primary literature: Gabbay/Pitts nominal techniques and Clouston--Pitts, *Nominal Equational Logic*, ENTCS 172 (2007) 223-257, DOI 10.1016/j.entcs.2007.02.009, establish name-symmetry methods. Parrow et al., *Modal Logics for Nominal Transition Systems* (2019), arXiv:1904.02564, explicitly treats transitions with bound names and bisimulation. Cousot--Cousot, POPL 1977, establishes the abstract interpretation setting. Atserias--Dalmau, JCSS 2008, treats Resolution width, not all mixed rules. Haken and Urquhart's hard families and Cook Extended Resolution are mandatory contrasting controls. Search used general web, not a separate Google-branded interface. No formal proof assistant was run.

## FULL CONFIGURATION INTERFACE

Fix one original binary-encoded CNF F with n original variables and m original source-clause identities, and one fixed sound rule calculus R. A concrete proof-construction configuration has the form

$$
s=(F,\mathcal D,\mathcal P,\mathcal C,\mathcal A,\mathcal H,c),
$$

where D is the **entire acyclic directed inference hypergraph** of distinct occurrence IDs; P gives exact original-source identities and derivation provenance; C records active context assumptions and legal discharge evidence; A records definitions, global freshness and exposed/private ports; H is the **global set of already paid occurrence IDs**; and c is cumulative native logical cost. No derivation choice, branching, convergence, auxiliary or known shortcut is excluded. Original source leaves are free only as R specifies. Two parent references to one lemma do not pay it twice. Legal goals are closed, original-source-authenticated refutations, not merely formulas semantically UNSAT.

Let G_n be the group of finite permutations of auxiliary variable names which fix 1,...,n, **all original source records and occurrence IDs**, and act consistently on every relevant field of s. A configuration is considered equivalent only under a single permutation of the **whole configuration**. A native transition and its logical weight must be equivariant:

$$
s\xrightarrow{w}_R t
\ \Longrightarrow\
\pi s\xrightarrow{w}_R\pi t,\qquad \pi\in G_n.
$$

For the exact theorem below, assume the reverse implication too, which follows by using the inverse permutation. Require that the goal predicate and initial state are invariant. These are TESTABLE rule-by-rule premises, not authenticated facts about every accepted byte of historical R_mix341.

## THEOREM 541.1: exact weighted orbit bisimulation (PROVED/RESTRICTED)

Under the preceding equivariance and goal assumptions, the quotient system on complete-state orbits [s] has a transition [s] --w--> [t] whenever one concrete transition between orbit representatives exists. Then:

1. Each concrete step projects to a quotient step with **exactly equal** native logical cost; every quotient step from [s] lifts from **every** representative of [s] with the same cost.
2. Consequently each finite quotient path lifts consistently to an entire concrete proof-construction path, and each concrete proof path projects. Source authentication, DAG acyclicity, contexts, freshness and global paid history are preserved by the group action.
3. For every budget B >=0, goal reachability in cumulative cost <=B is equivalent in the concrete and quotient transition systems. In particular, their minimum refutation work (or infima) is **equal**, with no change of weights or double charge.

**Proof.** Projection follows from the definition. For lifting, an abstract edge [s]->[t] has witnesses u->v and, for any chosen representative s', a permutation pi with s'=pi u. Equivariance gives s'->pi v and pi v in [t], of identical weight. Repeat at every step, starting from the original initial configuration. A consistent global permutation acts bijectively on occurrence IDs, hyperedges, assumptions, definition owners and the paid-set history, so neither a cycle nor an illicit cross-context lemma appears. A closed contradiction remains closed. Inductively, each budgeted goal path exists on one side iff it exists on the other. QED.

**Important limitation.** This is a standard nominal/symmetry-reduction argument specialized to the full paid proof-state signature. It does NOT find a noncircular potential, does NOT prove a superlinear bound, and does NOT authenticate numeric-ID-dependent historical rules.

## Corollary 541.2: conditional finite budgeted alphabet

If, in addition, all non-source steps have weight at least epsilon>0, each paid step introduces at most d fresh names, zero-cost actions carry no unbounded fresh syntax, and each native output has a finitely canonicalizable label over the presently known names, then a cost budget B admits at most d floor(B/epsilon) fresh names. For unit-weight, single-DEF-variable rules this is at most B. The canonical auxiliary indices n+1,...,n+B are therefore sufficient **for logical reachability modulo alpha renaming**, even though original evidence can use enormous binary IDs.

For a declared syntactic fragment with binary RES, GF(2) rows, constant-support Boolean truth tables and paid binary DEF, writing v=n+B, a coarse label alphabet is bounded by

$$
M_B\le 4^v + 2^{v+1}
 + \sum_{j=0}^{3}\binom{n}{j}2^{2^j}
 +16v^2 +O(1).
$$

The factors correspond respectively to possibly tautological signed clauses, affine rows, at-most-three-original-variable factors, binary gate/owner tuples and terminal markers. Parent IDs range over m+B recorded occurrences. With finite context encodings, one obtains a finite (potentially enormous) exact orbit-state search. This is **conditional** on all native payloads admitting those canonical labels; free unbounded LOCAL syntax, unbounded numerical evidence fields, unknown branching/discharge, source side reads and non-equivariant port selectors defeat an unjustified finite-state claim. The mathematical quotient does not make original verification or machine time free.

## ITERATE: independent finite controls

Implemented one SOURCE-EXACT, **strict RES plus paid but unused DEF** test fragment. Original clauses are (x1), (not x1 or x2), (not x2 or x3), (not x3), (not x2 or x4), (not x4), a Horn UNSAT source. Two paid DEF nodes introduce arbitrary globally fresh two-input gate variables. Five paid binary RES nodes yield two different empty clauses, sharing one previously derived x2 lemma. The seven paid occurrence IDs and the two shared-branch derivation trees are unchanged under renaming. The DAG is deliberately **not claimed globally minimal**.

Python standard-library implementation: 3,000 randomly chosen large auxiliary-name pairs, two goal nodes, all 7 paid identities and original-source ancestry preserved by a canonicalizer. Eight negative controls rejected changed source, wrong pivot, false resolvent, nonfresh/missing definition inputs, duplicate paid ID, illegal nonempty branch context, and non-clause parent. The independent Node.js verifier replayed 3,000 more renamed traces with 6,007 assertions, including seven corruption controls. Both passed. A hypothetical rule depending on **odd/even numerical auxiliary ID** is a direct counterexample to equivariance, not an actual R_mix341 rule. Seed 541. The Python checker ran in approximately 0.101 seconds. Neither implementation is the authoritative historical checker; the mock test does not establish full mixed-rule legality.

Python reproducer SHA-256: 6e3ce784dd43c007d79ff964b6ed0a006cf0960179f0a30bec281281ce8b8691.
Independent Node.js SHA-256: bc0d8845b775ee364c4baf23c72555c94cb75173dc56c2e3ef71d0870ee4954d.
Raw Python SHA-256: ae69d7af08f95de5a28f6dd264a9077e9b416806f3c0a34150aa8662a7a0d7e7.
Raw Node.js SHA-256: 9ec1f4a160e4092a6410816a20b721071e0a02ac31a282642385dda2a174ecd4.

## Published hard-family / known-shortcut calibration

For the established Urquhart expander-derived odd-charge cubic Tseitin family, the strict 3-CNF has h vertices, n=3h/2 edge variables and m=4h clauses (one forbidden signed local parity triple per clause), with length Theta(h log h) under explicitly binary indexed names. Exponential lower bounds are for **ordinary shared-DAG Resolution** on appropriate expanders, not for all R_mix341. The existing declared semantic LSPV-2/341 system has a 3h-AND3 + (h-1)-GF(2) upper-bound construction of 4h-1 logical nodes. Paid DEF/ER, LOCAL and shared shortcuts remain legal as specified by the true rule grammar. The orbit quotient preserves BOTH expensive Resolution and cheap algebraic traces, so it does not fabricate a hard mixed family.

## Resource, proof-status and next obligation

Logical work: the distinct-weight sum of H; quotient transition cost exact. Parallel span: separately the longest weighted dependency path, not the total work. Evidence bits: real original fresh IDs, source references, payloads and serialization; huge identifiers are NOT unit-bit. Construction/search, path lifting, checking, source/head reads, failed policies, caches, branch reconvergence, and physical simultaneous peak space are separate machine charges. Python/Node process RSS was not measured. A bound on logical orbit distance is not arbitrary-decider runtime, and Route A's FLMV all-input same-machine reduction remains OPEN.

Ledger (i) chosen solver-class abstraction: NO algorithm lower bound claimed. Ledger (ii) all historical R_mix341: [P2-D1], [P2-C3], [P2-B1] remain OPEN until exact grammar, context/port semantics, cost and each equivariance premise are authenticated and an actual superpolynomial invariant is found. Ledger (iii) any SAT machine: [P2-B2] and all-machine lower bounds OPEN. The optional fixed-r bridge remains OPEN.

For LSPV-3: test each native RES/AND3/GF(2)/LOCAL-CONVERT/DEF rule including exposed/private output selectors against source-fixed name equivariance and accepted bytes. For LSPV-5: attack numeric-ID and renaming side-read dependence, cross-branch freshness, and convergence/memoization, verifying the global occurrence history is never quotient-merged. A failed native equivariance test is a precise counterexample requiring a smaller symmetry group or a permissive MAY refinement.

**Actual advance:** exact weighted whole-configuration orbit equivalence under explicit rule hypotheses; a precise online interface to the cost-sound abstraction and finite-budget canonicalization, not a lower bound. **Verification:** symbolic proof and independently executed restricted controls; authoritative full-rule checker not run. **Publication:** report, independently executed JS code, compact Python/JS raw results, five-role handoff, issue #3 and proof2 entry committed and read back exactly; root main.tex could not be safely read completely (connector returned empty content for a nonempty blob), so must remain untouched. **Remaining gap:** prove rule equivariance and discover a source-sensitive potential for *all* native rules, plus noncircular B3. P versus NP OPEN.


### Final repository reconciliation / publication integrity (2026-11-09 PST)

GitHub report, code, compact raw evidence and five-role handoff were fetched after creation with exact content readback. proof2.txt was updated **only** with [P2-L1-541], after exact prewrite backup under research/agents/lspv-1/outbox/2026-11-09_1100_LSPV1_541_PROOF2_PREWRITE_EXACT.txt (previous SHA 1ab5c6cd9a02e97c7a8294945a0d08fae1ae1d8e); resulting commit 7c3ecf0deef1f13054ad88363c33f62854d73e8d, blob dbcdc964000410b38b92b76249335ac1c6f3d9ee and complete 790258-character postwrite readback. proof1.txt was reviewed at SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, with no material change. Issue #3 comment https://github.com/j15marti/pnp/issues/3#issuecomment-6749023065 was posted and completely read back. The authoritative historical mixed checker, root preflight/report scripts, and root main.tex reconciliation were **NOT** performed; main.tex returned an empty content payload with nonempty Git blob 7069f45a4f6067952661a0911f39fb087d3591ef, so no unsafe write was attempted. All remaining proof obligations are OPEN; P versus NP OPEN.
