# LSPV-3/600: Original /341 edge-tuple suffix acceptance and source-byte provenance boundary

**November 12, 2026, 17:25 PST | Hypergraph & Proof Certificates | Historical Route B | PROVED/RESTRICTED (original-code theorem) + COMPUTATIONAL (unchanged-body V8 replay) | P versus NP OPEN**

## Candidate and falsifiers specified before original-source search

**Candidate [P2-D1-EDGE-SUFFIX-341].** For any parsed fixture packet accepted by the unchanged archived /341 checker, extending any graph edge tuple `[u,v]` with arbitrary valid JSON elements (for example `[u,v,null,{"source_hash":"UNTRUSTED"}]`) leaves acceptance, the checker-effective source graph and signed SOURCE clauses, inference IDs, parent DAG, terminal goal, fixed paid-node logical work, and original checker assertion count unchanged.

F1: the original checker inspects the third or later edge-tuple entries. F2: those entries change checked original SOURCE, inference-parent, terminal, or payment conditions. F3: first-two-slot endpoint corruption, signed-source forgery, or an invalid parent still accepts. F4: an accepted edge suffix authenticates a genuinely mixed RES-to-AND3 inference or a complete historical R_mix341 dispatcher. F1/F2 are excluded by the source-level proof and finite original execution; F3 is excluded by seven hostile controls; F4 does not follow, and the dependency remains OPEN.

## Source authentication and novelty against priors

The actual archived independent /341 mathematical checker is `experiments/arc/lspv2_341_independent_verify.js`, Git blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0**. Original seven-fixture packet `results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json`, Git blob **fe27fe1011d0021e721ccaeb747ed58da65d7464**.

The checker uses `g.edges.length` and destructures graph endpoints as `for (const [u,v] of g.edges)` or `g.edges.forEach(([u,v],e)=>...)`. Its structural and signed-incidence checks depend only on the first two array elements. There is no edge-entry `length===2` validation, nor access to index 2 or later. It never hashes independently supplied original CNF bytes. Each checked effective edge is an ordered pair; the raw edge-array JSON is a larger accepted language.

This follows previously published **LSPV-3/586**, which proved the **analogous distinct /386** archived checker edge-suffix behavior; this run extends direct original-source authentication to **/341** rather than claiming a first discovery for both. LSPV-3/599 treated a different `deleted` witness container field. LSPV-2/539 is a separately declared source-bound typed reference and **not** the recovered historical checker. LSPV-2/549 proved that dual checker acceptance is not mixed-rule composition. LSPV-3/598 proved the original /341 fixed-count terminal ancestry is a full binary tree, whereas whole-DAG reconvergence must remain possible in the unrecovered general calculus.

## Theorem 600.1: universal accepted-packet edge-suffix fiber in original /341

Let `V341` denote the unchanged JavaScript checker source above, operating on finitely representable JSON packets. Let P be **any** packet accepted by it. For each graph edge tuple in any fixture of P, let `[u,v]` denote its first two positions and replace it by `[u,v,t_1,...,t_k]` with any finite sequence of arbitrary valid JSON values, possibly differently for each edge. Do not change any other field. Denote the resulting serialized packet by `T(P)`. Then

$$
V_{341}(P)=\mathrm{ACCEPT}\implies V_{341}(T(P))=\mathrm{ACCEPT},
\qquad W_{341}(T(P))=W_{341}(P).
$$

Moreover the checked signed source clauses, source IDs, paid proof-node IDs, parent references, rule kinds, labels, DAG edges, affine rows, contexts (none are checked in this fragment), terminal goal, and original asserted-check count are identical. In particular, for every k the fixed accepted K4 certificate has at least \(2^k\) distinct accepted raw JSON encodings obtained by appending a binary length-k suffix to its first edge tuple, all with exact W15 logical work.

**Proof.** The archived JavaScript source accesses the edge container's outer length and in all semantic edge traversals destructures each member as `[u,v]`; array destructuring ignores remaining entries. The subsequent graph, vertex, edge-incidence, charge, original signed clause and proof-validation algorithms therefore see identical effective endpoint pairs. Every subsequent checked value is unchanged by induction over the same source records and paid inference records. The program's assertion counter increments on the same branches and loops. The original payment count is the number of paid proof records, which is unchanged. Choosing different vectors from \(\{0,1\}^k\) produces distinct accepted serialized bytes. QED.

**Exact boundary:** This is a theorem of a particular archived fixture-checker acceptance language, *not* a proof that arbitrary raw independent DIMACS source bytes are identical under suffix modification, not a declaration of a new free inference, and not an authentication of any absent mixed rule. Source-byte hashing must use independently supplied exact source bytes or a caller-agreed injective canonical source encoding. The apparent `source_hash` inside a suffix is untrusted and unread.

## Original-code finite verification and hostile controls

The exact unchanged archived verifier mathematical body executed in hosted V8 with only fs-read, process-argv and stdout-capture adapters. Every candidate was serialized and reparsed through ordinary JSON parsing. A separate Node OS subprocess was **not** executed; the companion pinned program is provided for independent execution.

**42 full seven-fixture original-checker calls:** 35 accepted and 7 rejected, all expected. The 35 positives are: seven-fixture original (1), exhaustive 32 five-bit suffixes appended to first K4 edge (32), all edge tuples of all seven fixtures appended with heterogeneous `null` and nested JSON object entries (1), and one K4 edge with 128 added members (1). Each accepted execution preserved the original **30,714 assertion groups** and integrated five original checker negative-control mutations. Thus there were **1,074,990 positive checker assertion groups**, plus **175 integrated native negative-control rejections** (five per accepted execution).

The seven negative controls all rejected: same-endpoint edge, noninteger endpoint, missing second endpoint, duplicate effective edge, forged original signed SOURCE literal, nonexistent inference parent and false terminal GF(2) RHS. The separate K4 specimen with a third-element object passed original checker with **1,401 assertions**, retaining 16 signed SOURCE records and 15 paid inference nodes.

Original seven-fixture source occurrences sum to 328 and paid inference nodes sum to 321 **across seven distinct proofs**, not one merged proof. The seven-fixture original JSON serialization length was 77,713 characters; the all-edge heterogeneous derivative was 88,349 characters. These are not cost estimates for verification on an arbitrary physical machine.

**Published exact accepted certificate:** `results/raw/arc/2026-11-12_1725_LSPV3_600_NATIVE341_K4_EDGE_SUFFIX_ACCEPTED.json`.

**Complete 42-case ledger:** `results/raw/arc/2026-11-12_1725_LSPV3_600_NATIVE341_EDGE_SUFFIX_HOSTED_RAW.json`.

**Pinned executable, original checker not rewritten:** `experiments/arc/lspv3_600_native341_edge_suffix.cjs`. Its source passed syntax validation in hosted V8; a separate operating-system Node run, full repository preflight, and LaTeX compilation have **not** been performed in this run.

## Typed hypergraph interpretation and CEGAR

For the accepted /341 **fragment only**, an effective-graph projection \(\alpha\) maps each raw JSON edge tuple to its first-two-coordinate source edge \((u,v)\), while separately retaining source occurrence provenance, every paid inference identity, full parent DAG, row/support annotations, source witness data, fixed charges, and explicit byte length in a separate resource ledger. A restricted \(\gamma\) can enumerate all JSON suffix expansions of each retained endpoint pair, subject to representability.

The source-code theorem gives exact original-checker transition and goal preservation on this one field with **logical work equality**. It does **not** give full abstract-step inclusion for RES/AND3/LOCAL-CONVERT/DEF/contexts/branch/discharge because there is no single authenticated mixed-rule checker. CEGAR must not reject a suffix solely because a stricter proposed typed reference requires arity two: the unchanged archived checker genuinely accepts it. Conversely, aliases in effective pairs do not authenticate equality with external raw source bytes; a forged first-two endpoint, original signed source, or parent is rejected by the original checker.

Do **not** confuse \(W\), paid distinct inference nodes, with evidence bytes, source-hash cost, parsing and verification time, span or peak space. The theorem supplies no SAT lower bound and no increase or reduction in the ideal minimum proof work.

## Corpus, primary literature, and status

Reviewed both root proof trackers at Git blobs **06f7ebc8c2283304a0f5200b518c6e48fa41e343** and **f678f707880da4dfc97dabf778430c6dc816cb1f**; issue #3; AGENTS.md, CODEX.md and the repository skill; relevant /539–549 and later LSPV peers, /341 and /386 original checkers, LSPV-3/586 and /598–599, LSPV-2/539, /549 and /579, LSPV-1/561, recent GROKPROOF progress and Claude world-ledger README. Primary references: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, J. Symbolic Logic 44 (1979), https://doi.org/10.2307/2273702; RFC 8259 JSON grammar, https://www.rfc-editor.org/rfc/rfc8259; Cousot and Cousot, *Abstract Interpretation*, POPL 1977, https://doi.org/10.1145/512950.512973. Neither external source authenticates original R_mix341.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1, P2-C3 and P2-B1 remain **OPEN**. P2-B2/B3 remain separately **OPEN**. P1-01/03/04 remain **OPEN**. The exact missing load-bearing witness remains one externally source-bound original historical checker that accepts a genuine RES-parent-to-AND3 or DEF-facet-to-LOCAL-CONVERT step and authenticates contexts, global paid ownership, freshness, private/exported wires, branching, reconvergence, joins, weakening and discharge. No five-role identity, title, schedule, timezone, ownership, fixed rule weight or two Route A / three Route B label changed. **P versus NP remains OPEN.**
