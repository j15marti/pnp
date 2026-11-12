# LSPV-1/594: Historical /341 verifier is not closed under locally valid paid-node insertion

**12 November 2026, 08:31 PST | General SAT Lower-Bound Lead | historical Route B**  
**Status: PROVED/RESTRICTED pinned-checker theorem + COMPUTATIONAL original-body hosted-V8 replay. P versus NP OPEN.**

## Candidate, quantifiers, falsifiers

**Candidate:** The recovered original /341 verifier, even restricted to its genuinely implemented SOURCE/AND3/XOR instructions, does not define a proof language closed under locally valid unused paid-AND3 insertion. Consequently its full-packet acceptance cannot be equated with an inductive native inference transition system for P2-C3. This is a statement about the *actual pinned verifier*, not the unrecovered full historical R_mix341 calculus.

Fix the exact historical checker Git blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0** and accepted seven-fixture packet blob **fe27fe1011d0021e721ccaeb747ed58da65d7464**. For every fixture F with h vertices and its accepted proof P, select a SOURCE-parent AND3 node p and insert before the last sink a fresh-id exact copy p' of p, with all parent references and computed truth table unchanged. Then (i) p' passes the checker's local AND3 rule; (ii) all original proof nodes, source occurrences, ancestry and terminal contradiction remain unchanged; and (iii) the unmodified complete verifier rejects P' solely because the proof length increased from 4h-1 to 4h.

Precise falsifiers: **F1** at least one baseline fixture fails the original checker. **F2** the inserted clone is not locally a legal AND3 or alters a parent, source or sink. **F3** the historical checker accepts the padded packet. **F4** the rejection arises from an inference failure other than the pinned global proof-length assertion. All four were excluded in seven original-body hosted-V8 controls; direct checker source inspection proves the structural cause.

## Exact nonclosure theorem

**Theorem 594.1 (pinned-/341 locally valid padding nonclosure).** Let C_341 denote exactly the archived independently executed verifier in the pinned Git blob, and let f be any C_341-accepted fixture with h vertices, at least one AND3 node p with two original SOURCE-factor parents, and a final XOR contradiction. Assume p has no side effects other than adding its fresh result identifier, as is true in the pinned code. Form f' by inserting, strictly before the sink, one fresh-identifier clone of p with identical parents, kind, support, table and optional affine alias. Then:

1. Every original source clause, original paid-node definition, original paid-node identity, original parent edge and final sink in f persists unchanged in f'.
2. The newly inserted node satisfies every local AND3 parent, support, truth-table and optional-affine-alias condition used by C_341. It costs one additional paid AND3 node in a *hypothetical* prefix-local transition system.
3. The literal complete checker C_341 rejects f' because it tests f'.proof.length === 4h-1 before iterating through the proof, whereas f'.proof.length = 4h.

**Proof.** The source factor map is constructed from the same original clause set. The cloned node takes the same two earlier SOURCE-factor parents as p, with the same support, table and optional row, so its conjunction truth table and typed local checks are identical. Its newly chosen identifier does not occur in the original SOURCE or inference maps. Insertion occurs before the last XOR sink, so all previous references still resolve by identifier and all original source ancestors remain ancestors of the unchanged terminal contradiction. The independent checker explicitly asserts \`f.proof.length===4*V-1\` before its per-inference loop. P has exactly 4h-1 paid proof records, so P' has exactly 4h and fails that assertion. No semantic inference violation is required. QED.

**Corollary 594.2 (transition-system boundary).** The accepted-byte language of this archived verifier is not extension-closed under otherwise locally valid unused paid deductions, and does not define the full prefix transition relation required for an optimal-whole-shared-DAG cost objective. In particular a per-step CEGAR refinement cannot take C_341's final acceptance predicate as a substitute for step-local legality. A sound model must separately encode the local inference relation and terminal global wrapper checks, retaining all genuine native operations when the authoritative mixed checker becomes available.

The corollary does **not** establish that padding is legal in the declared historical R_mix341, which has not been fully authenticated. It does not claim every prefix is accepted or that the global check should be disabled. It does not close any asymptotic lower bound.

## Independent original-body verification

Fetched the exact checker and input bytes from the GitHub repository. Extracted the original \`verify\` function *without rewriting its test body* and executed it in hosted V8. The unmodified baseline accepted all seven fixtures with **30,714 assertion checks**. Seven padded variants were rejected, each with the exact error \`Verifier: proof candidate length\`.

| Fixture | h | Original paid nodes | Padded paid nodes | Original verifier |
| --- | ---: | ---: | ---: | --- |
| K4 | 4 | 15 | 16 | REJECT |
| K3,3 | 6 | 23 | 24 | REJECT |
| Cube | 8 | 31 | 32 | REJECT |
| Petersen | 10 | 39 | 40 | REJECT |
| Prism6 | 12 | 47 | 48 | REJECT |
| Prism16 | 32 | 127 | 128 | REJECT |
| Bridge-K4x2 | 10 | 39 | 40 | REJECT |

Wrong truth-table, duplicate-parent, and corrupted-sink controls were all rejected by the original verifier with **different** diagnostic errors, confirming that the padding failure is the length guard. A separate independent bit-assignment evaluation of the duplicated AND3 table and source support passed all seven fixtures. The source, original paid DAG and terminal XOR sink were not altered.

**Execution limitation:** the original checker function ran in hosted V8 with its file I/O wrapper omitted. The new standalone Node OS-subprocess reproducer has been committed, but its OS execution was not separately performed in this run. No claim of new original-Node subprocess evidence is made.

Evidence:
- Reproducer: \`experiments/arc/lspv1_594_native341_padding_nonclosure.cjs\`.
- Immutable hosted raw: \`results/raw/arc/2026-11-12_0831_LSPV1_594_NATIVE341_PADDING_NONCLOSURE_HOSTED_RAW.json\`.
- Historical verifier: \`experiments/arc/lspv2_341_independent_verify.js\` (Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0).
- Historical packet: \`results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json\` (Git blob fe27fe1011d0021e721ccaeb747ed58da65d7464).

## Dependency and barrier audit

**P2-D1 OPEN.** This is one newly explicit *negative* operational property of the source-authenticated /341 fixture verifier, not recovery of historical RES, LOCAL-CONVERT, DEF, branching, contexts, weakening, joins or discharge. The distinct archived /386 checker remains noncomposable. LSPV-5/413 already proved the restricted two-tag dispatch; /594 adds a **structural nonclosure counterexample** even within those recognized tags.

**P2-C3 OPEN.** A complete native concrete state must track the entire shared proof DAG, original SOURCE identity, paid IDs and exact weights, definition/facet freshness, contexts, assumption discharge and final wrapper obligations. The raw checker predicate is a terminal property, not an all-transition relation. Any abstract transition must overapproximate all *legal native steps*, with a potential satisfying all edge inequalities; dropping padded legal paths or unknown operations would be unsound. For the seven fixture packets, cloned node overhead is one unit of logical work, not zero; evidence bytes, checker runtime, actual time, span and peak space are separate.

**P2-B1 OPEN.** The source family is a parity-controlled test family, not a superpolynomial-hard mixed-family witness. Source-essentiality and the exact 4h-1 fixture size do not imply minimum whole-DAG work when other valid proof structures are freely selectable. The checker can reject a redundant node without implying that a full native calculus forbids it.

**P2-B2/B3 OPEN and separate.** Nothing here establishes an all-algorithm cost transfer. LSPV-1/592's conditional Extended-Resolution strength audit remains a separate control.

**Prior corpus reconciliation.** Read both root trackers, issue #3 and latest peer updates, AGENTS.md, CODEX.md, the project research skill, LSPV-1/539/544/549 and /592-593, LSPV-2/549/576, LSPV-3/549/590, LSPV-4/563, LSPV-5/413/505 and current five-role handoffs; surveyed the complete current repository tree. The exact global proof-length guard was *already present and publicly known in the historical checker*; novelty claimed here is solely the formally stated closure obstruction and seven-fixture negative test, not discovery of the guard or full checker grammar. Main historical source artifacts, Grok/Claude and external FRAT-XOR checkers were not substituted for native authority.

**Primary literature.** Cook and Reckhow, "The Relative Efficiency of Propositional Proof Systems", *J. Symbolic Logic* 44 (1979), DOI 10.2307/2273702, distinguishes proof-system semantics from particular presentations. Cousot and Cousot, "Abstract Interpretation", *POPL* (1977), DOI 10.1145/512950.512973, requires a sound abstract semantics of an actual transition system. Ben-Sasson and Wigderson, "Short Proofs Are Narrow", *JACM* 48 (2001), DOI 10.1145/375827.375835, concerns ordinary Resolution and supplies no all-rule native lower bound. None authenticates missing mixed-rule bytes.

**Barriers:** No relativization or Natural-Proofs conclusion is advanced. A restricted checker-nonclosure theorem transfers no complexity-theoretic hardness to arbitrary SAT algorithms. Code/execution evidence concerns the exact recovered /341 fixture checker only.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Leave P2-D1, P2-C3, P2-B1 and P2-B2/B3 OPEN. The only possible manuscript insertion belongs inside LSPV-1's uniquely marked region, preserving all other content by full-current SHA and exact readback.

**Next:** independently run the exact pinned Node CLI reproducer, then locate an original externally source-bound *single dispatcher* accepting a true RES->AND3 or DEF->LOCAL-CONVERT inference and reject its corrupted variants.
