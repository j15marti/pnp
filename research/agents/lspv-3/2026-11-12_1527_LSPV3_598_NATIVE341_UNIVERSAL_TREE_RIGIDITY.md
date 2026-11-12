% LSPV-3 REPORT::598::2026-11-12 15:27 PST
# LSPV-3/598: Universal arborescence rigidity of every accepted original /341 fixture

**2026-11-12 15:27 PST | LSPV-3 Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED source-code theorem + COMPUTATIONAL original-checker replay | P versus NP OPEN.**

## Single P2-D1/P2-C3 candidate and precise falsifiers

**Candidate, fixed before replay:** Not merely the well-typed or mathematically sound examples, but **every** JSON packet accepted by the unchanged original archived /341 SOURCE/AND3/XOR fixture checker has, within **each** fixture, a terminal ancestor graph that is a rooted full binary tree: every SOURCE occurrence and every paid inference is terminal-live, and no SOURCE or paid record has two consumers. This is an exact *acceptance-language* restriction and does not apply to the unlocated full historical R_mix341 grammar.

- **F1:** A genuinely original-checker-accepted packet has an inference or source with consumer count greater than one.
- **F2:** A genuinely accepted packet contains a terminal-dead paid inference while retaining all original sources.
- **F3:** Parser irregularities such as object terminal IDs, string supports, or an accepted SAT-source packet break the asserted tree conclusion.
- **F4:** An altered packet that doubles a parent, introduces a dead paid record, reuses a source, or removes a source is accepted under the original checker despite the arborescence argument.

F1-F3 were absent in the tested corpus; F4 was rejected in all six hostile mutations. **The universal result below is proved directly from the original checker source, not inferred from these finite tests.**

## Source authentication, corpus, and precedence

Read both root trackers (proof1.txt blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2.txt blob f678f707880da4dfc97dabf778430c6dc816cb1f), issue #3 and latest comments, AGENTS.md, CODEX.md, the required pnp-research skill, and the current LSPV-3/597 handoff. Reviewed the exact archived /341 verifier JS blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0**, historical 7-fixture packet blob **fe27fe1011d0021e721ccaeb747ed58da65d7464**, and the separate /386 checker blob **338305c0ce101704205e57543756b8127074a986**. Reviewed materially relevant LSPV-1/469, LSPV-4/525, LSPV-3/491, /582, /590, /594, /596, /597, LSPV-2/549 and /583, LSPV-5/511, and source reports from the /539-549 period. Also reviewed GROKPROOF/2026-11-12_0917_PROGRESS.md and the Claude world-ledger README. No recovered full historical mixed-rule dispatcher was found in these materials.

**Prior art carefully separated:** LSPV-1/469 already proved the m-1 binary-ancestry tree-rigidity implication for a *declared semantic calculus*, assuming soundness and indispensable sources. LSPV-4/525 already showed that the recovered /341 fixture checker rejects explicitly longer, valid shared XOR detours that a **different typed reference checker** accepts. LSPV-3/491 already authenticated a balanced tree fixture. **The incremental claim here is narrower in calculus but stronger in quantifier domain:** it is a source-code theorem for **all accepted original /341 parsed packets**, including malformed nonsemantic certificates, without assuming mathematical soundness, source indispensability, a well-typed identifier schema or a separately invented proof grammar. This is not a new general graph-theoretic lemma or proof-system lower bound.

Primary literature checked: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), DOI 10.2307/2273702; Cousot and Cousot, *Abstract Interpretation*, POPL (1977), DOI 10.1145/512950.512973; de Colnet and Mengel, *Characterizing Tseitin-formulas with short regular resolution refutations*, arXiv:2103.09609 (2021). None identifies this archived parser or transfers its property to all algorithms. External FRAT-XOR/XLRUP and CakeLPR formats are distinct from the missing historical R_mix341 parser.

## Theorem 598.1 (original /341 accepted-byte terminal tree)

For **every** finite JSON byte packet b for which the *unchanged complete* archived /341 checker accepts, and for every fixture f in the parsed packet, let S_f be the set of original SOURCE records and D_f the set of inference records. Define a directed dependency edge from each inference to each of its two ordered parents, identifying nodes by the exact JavaScript Map keys produced by the original JSON.parse. Then:

1. The last inference is the unique terminal root. Its ancestor graph contains **every** source and **every** inference.
2. Every nonterminal node, whether SOURCE or paid, appears **exactly once** as a parent of a paid inference. The root has no consumers.
3. The underlying undirected dependency graph is a tree. In particular there is **no reconvergence, paid-node re-use, shared-source fanout or terminal-dead paid node** in any original /341 accepted fixture.
4. The checker-enforced inference count is exactly |D_f|=|S_f|-1=4|V_f|-1. This counts records. It is not an authenticated global mixed-rule minimum.

**Proof from executable source.** The original checker creates a Map for each source identifier and checks source-ID uniqueness (source lines 58-74). It requires precisely m=4V source records and r=4V-1 proof records (lines 59, 76). For each inference it requires two present, distinct, earlier parents and a fresh inference ID (lines 77-79, 106). These conditions guarantee a finite chronological DAG with two distinct parent edges per paid node, even for weird accepted primitive/object terminal identifiers. It chooses the last proof record as root, recursively marks all ancestors, and requires every source to be marked (lines 108-111).

Let r_* be the number of inference nodes in the root-ancestor graph. All m sources lie in this graph. Every one of its r_* inferences contributes exactly two parent edges, and no ancestor edge leaves the graph. The undirected ancestor graph is connected and has m+r_* vertices and 2r_* edges, so

$$
2r_* \ge m+r_*-1,\qquad r_* \ge m-1.
$$

But r_* <= r=m-1. Hence r_*=r: **every** inference is an ancestor. The entire graph has m+r=2m-1 vertices and 2r=2m-2 edges. Since it is connected, it is an undirected tree (parallel/duplicate edges are excluded by distinct parents and unique Map identities). Every non-root node lies on the unique path to the root, and therefore has exactly one consumer. This proof does not invoke local clause correctness, parity charge typing, CNF satisfiability, validity of affine annotations, or even an external original-source hash. QED.

**Consequence for CEGAR and abstraction scope:** A purported *original-/341-only* cheap abstract terminal path containing genuine source or paid-node reconvergence cannot have an accepted concrete preimage. Its removal may be justified by the above checker-specific invariant with rank, source, parent identity and terminal ancestry retained. Conversely, applying this restriction to **historical full R_mix341** is UNSOUND as a transfer: the full grammar is not authenticated, and other declared legal derivations with extra work, paid definitions, resolution, exported/private wires, contexts, or sharing may exist. The separately authenticated /386 grammar already permits paid shared DAGs, and a semantic /539 typed reference accepts longer shared XOR detours. Keep full-calculus sharing as MAY, not excluded.

## Authenticated execution, measurements and hostile controls

Ran the **entire unchanged archived checker function body** in hosted V8 against actual JSON bytes fetched from GitHub, with only fs/process/console I/O adapters. This executes the original built-in malformed-CNF and five corruption controls on every accepted packet. Separately traversed the exact parsed identity graph using JavaScript Maps and exact source/parent keys, not a structural-string canonicalizer.

- **8/8** original-checker packets accepted, containing **20** separately checked proof fixtures.
- **71,706** total positive original-checker assertion groups.
- **20/20** accepted fixture dependency graphs satisfy complete terminal ancestry, paid count m-1, tree edges 2(m-1), fanout 1 for each non-root node and root fanout 0.
- Included the seven original graphs, transported source-charge, reversed AND3 support coordinates, terminal object-ID, object summary, all seven support-string peer packets, noncanonical SAT-source charge packet, and array-mask certificate. The SAT-source checker acceptance is a previously known **unsoundness defect** but does **not** invalidate this purely syntactic arborescence invariant.
- **6/6** hostiles rejected by the original checker: duplicate parent, extra terminal-dead inference (length), deleted inference (length), reused source reference (incorrect conjunction), reused derived reference (XOR types), and missing original SOURCE (clause count).

These are **20 finite corpus witnesses, not a proof of universal soundness or a large-class lower bound**. The symbolic source-code proof establishes the universal accepted-packet property. The standalone Node.js script was written, parsed for syntax and published, but **was not executed as an OS subprocess** in this run; hosted V8 original-body replays were executed. No filesystem-wide preflight, repository checkout, independent OS process timing, LaTeX build, evidence-bit complexity theorem, physical peak-space measure, or machine-time lower bound was completed.

## Fixed work versus resource and historical model boundaries

The /341 packet has r=m-1 binary paid inference **records** and no sharing; that count does not authenticate the wider fixed weight vector or any minimum over arbitrary legal R_mix341 proofs. Actual accepted JSON bytes, source retrieval, proof serialization, input parsing, checker time, critical-path span and peak working memory are different quantities. A cost-sound abstract interpreter must continue to assign each unique paid node its original unit charge, not charge every reference and not infer a lower bound on machine time from m-1 record count.

This tree result **removes one potential false positive when testing a recovered sibling parser**, but it does **not** advance the missing historical cross-rule authentication needed for P2-D1 closure. Any claim that this result proves reconvergence illegal in full R_mix341 is **FALSIFIED/RETIRED AS AN INFERENCE**, not a theorem about the historical rules.

**[P2-D1] OPEN:** full historical SOURCE/RES/AND3/GF(2)/LOCAL-CONVERT/DEF/branch/discharge/joins grammar and native externally source-bound mixed checker still missing. **[P2-C3] OPEN:** exact full-calculus concrete-step-inclusive and cost-no-greater abstraction not proved. **[P2-B1] OPEN:** no all-rule superpolynomial SAT minimum. **[P2-B2/B3] OPEN separately. [P1-01/03/04] OPEN. P versus NP OPEN.**

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both root trackers are current and require no change from this restricted source-code theorem. The five existing role identities, titles, Pacific schedules, existing two Route A / three Route B allocation, ownership regions, historical fixed weights and enabled states were not modified.

## Reproduction artifacts and five-role handoff

- Replayer: experiments/arc/lspv3_598_native341_tree_rigidity.cjs
- Complete raw ledger of input blob hashes, original-checker assertions, 20 tree audits, and six hostile diagnostics: results/raw/arc/2026-11-12_1527_LSPV3_598_NATIVE341_TREE_RIGIDITY_RAW.json
- Five-role handoff: research/coordination/2026-11-12_1527_LSPV3_NATIVE341_TREE_RIGIDITY598_FIVE_ROLE_HANDOFF.md

Next decisive source-authentication target remains an **original single-file historical R_mix341 checker** accepting one externally original-source-bound actual RES -> AND3 or paid DEF-facet -> LOCAL-CONVERT inference with global paid ownership and hostile source/parent mutations. No replacement parser or polyglot pair of sibling checkers can satisfy that obligation.

% END_OF_VERIFIED_REPORT::LSPV-3::598
