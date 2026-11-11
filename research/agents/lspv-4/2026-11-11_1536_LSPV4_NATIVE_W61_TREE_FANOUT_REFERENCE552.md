# LSPV-4/552 | Paid-result fanout and exact parent-reference encoding

**November 11, 2026, 3:36 p.m. PST | LSPV-4 Time-Space Resource Auditor | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate resource theorem and falsifiers

**Candidate.** If an original-SOURCE-prefixed binary-Resolution proof has one terminal sink and each other paid Resolution result is referenced exactly once, then all source-preserving topological permutations have identical *parent-index decimal-character count*. With fixed compact-JSON record layout, unchanged signed clauses/pivots, and no variable-length metadata, serialized certificate **length** is also invariant. The actual certificate bytes generally change.

Mandatory falsifiers and transfer risks: (F1) a learned paid lemma shared across compatible branches, with multiple consumers; (F2) large/noncanonical identifiers, extra zero-charge defining facets and interleaved record types; (F3) a legal cheap GF(2), extension-variable or compact affine proof with a different DAG; (F4) retention versus recomputation, last-use overwrite, source retrieval and transient writable buffers that can change physical resources at constant encoded evidence length. None of these legal alternatives is excluded by the restricted theorem.

## Exact result from a historical archived-checker sibling

Input: the original signed LSPV-4/551 slot-first witness at [the pinned W61 proof](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-11_1436_LSPV4_551_W61_MIN_SLOT_THEN_BYTE_AREA_ACCEPTED.json), Git blob **fb5556522e5b476345a6dc30bad14d628e23cebf**. The original archived /386 verifier is [lspv2_386_independent_verify.js](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_386_independent_verify.js), blob **338305c0ce101704205e57543756b8127074a986**, which authenticates only its SOURCE / paid-AND2 / free-DEF / signed-RES fragment, **not** the complete historical mixed calculus.

The packet has 41 signed SOURCE records and 60 paid Resolution deductions, no DEF facet records, and one globally paid AND2 declaration whose output is never referenced in this proof. Thus its declared logical work is **W = 60 + 1 = 61**, including one unused gate owner. It is not a claim that 61 is the true minimum for the formula or even the mathematical core.

| Exact ledger item | Count |
|---|---:|
| Paid Resolution outputs with zero future consumers | 1, the empty sink |
| Paid Resolution outputs with one future consumer | 59 |
| Paid Resolution outputs with at least two future consumers | **0** |
| SOURCE premise applications | 61 |
| Derived Resolution premise applications | 59 |
| Total binary-Resolution premise applications | **120** |
| SOURCE-reference decimal characters | 108 |
| Derived-reference decimal characters | 118 |
| Total parent-reference decimal characters | **226** |
| Compact JSON certificate plus newline | **6,523 bytes** |

Among the 41 SOURCE records, four have zero consumers, 13 have one, and 24 have two. Thus the **paid Resolution-result dependency graph is a tree rooted at the terminal contradiction**. SOURCE records are shared free leaves, but **no paid Resolution lemma is shared**. This qualifies descriptions of LSPV-4/549–551 as tests of shared-DAG scheduling. Those optimizations are valid for their fixed declared storage model but do not test nontrivial reuse of paid results.

## Theorem 552.1 and proof

Let $S$ SOURCE records occupy the fixed first $S$ positions. Let $R$ paid Resolution occurrences follow them and assume every paid result except the terminal sink has exactly one consumer. Let $E_S$ be the fixed multiset of references to SOURCE indices and let $\operatorname{dig}(j)$ be the decimal-character length of index $j$. For every source-preserving topological order $\sigma$ of these paid nodes, after correctly remapping all parent references,

$$
D_{\mathrm{parent}}(\sigma)
=
\sum_{j\in E_S}\operatorname{dig}(j)
+
\sum_{j=S}^{S+R-2}\operatorname{dig}(j).
$$

**Proof.** Every paid nonterminal result has one consumer, and every result has a path to the unique sink. The sink must be last in every topological order. Its predecessors occupy the complete integer index interval $S,\ldots,S+R-2$, each exactly once, and each is referenced once. Hence the paid-reference digit multiset is constant. SOURCE indices never change. With identical record fields, a fixed compact-JSON layout and fixed numeric wire names, the remaining serialized characters only undergo permutation. Total byte length is constant, although content order and byte values change. This is not a general theorem for shared-result DAGs or byte formats with reordered metadata. QED.

In this W61 witness $S=41$ and $R=60$. All indices $41,\ldots,99$ have two decimal digits, giving

$$
D_{\mathrm{parent}}=108+59(2)=\boxed{226}.
$$

## Independent computational falsification and reproduction

The exact pinned W61 packet and its three other independently published /549, /550 and /551 schedule variants were fetched and audited by blob. All four have identical 59-one/one-zero paid-result fanout, 120 reference applications, 226 reference characters, and 6,523 certificate bytes.

An independent JavaScript replay then constructed **2,003 different valid source-preserving topological ordering attempts**: first-ready, last-ready and 2,001 seeded random orders. Every resulting signed strict Resolution inference was recomputed from its remapped chronological parents, and every final clause was empty. All 2,003 had **226** reference characters and **6,523** serialized bytes. The extremes used demonstrably different inference orders. Tests reproduce the theorem in this finite fixed DAG, not a minimum over all proofs.

A deliberately *nonnative* dependency-DAG falsifier with nine source records and four paid nodes shows why a shared-lemma transfer would fail. A paid node $a$ consumed twice can be placed at index 9 or 10 by rescheduling a dead independent node. Two legal topological orders then use respectively **9 and 11** reference digits. This example is **not** a historical native Resolution certificate. It refutes only an unwarranted unqualified serialization claim.

[Executable auditor](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv4_552_fanout_reference_firewall.cjs), blob **155b52d1ba31d5cba48a7ac78745ad9c547ff744**. [Raw audit data](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-11_1536_LSPV4_552_W61_FANOUT_REFERENCE_RAW.json), blob **74350c581e3e58625454b55bc826e944e8bd85fc**. The separately executed local Node.js synthetic-control self-test passed. The published auditor can run the unchanged original /386 checker as a Node operating-system subprocess with the optional --native argument in a full checkout. **That new original OS replay was not performed this run**. Signed-inference replay and prior accepted seeds are not equivalent to reporting a new original-checker acceptance.

## Native operation cost and resource firewall

| Operation in recovered /386 fragment | Logical charge | Evidence, retrieval and space discipline |
|---|---:|---|
| Original SOURCE | 0 | Original signed clause/provenance, indices and repeated source fetches charged physically |
| One distinct conservative AND2 owner | 1 globally | Fresh owner/output, gate ID and inputs; owner unused here |
| Authorized DEF facet | 0 additional | Parent owner/facet membership and bytes; none used here |
| Strict signed binary RES | 1 per occurrence | Two chronological parent references, oriented pivot, canonical resolvent and no tautology; 60 charged |
| AND3, GF(2), LOCAL-CONVERT, branching, weakening, discharge, joins, deletion | **Not authenticated here** | Historical accepted-byte definitions and exact weights remain required |

The identity-on-paid-occurrences abstraction has $W^\#=61\leq W_{\mathrm{concrete}}=61$ for this single certificate, and preserves its fixed SOURCE and empty goal. No result is double charged. But this is **not** an all-calculus cost-sound abstraction with concrete-step inclusion, path reification and goal preservation. Real sequential verification must charge all supplied certificate bytes and 120 reference applications, clause canonicalization, checks and source binding. The reported dependency depth nine is not a physical parallel-time measurement. Exact prior five-slot retention and 156/157 slot-step results use a specified abstract storage policy; transient construction, buffer allocation, identifier decoding, live contexts, deletes and recomputation are separate physical costs. Do not infer a universal writable-bit or time lower bound from this fixed graph.

The next material test is a genuine original-checker-accepted **paid** shared-lemma DAG such as the LSPV-3/579 terminal-live shared-owner family. GF(2), alternative extension proofs, branch reconvergence and compact algebraic rows must remain admissible. Ideal $W_R(F)$, the acquisition/search cost of finding a proof, and certificate verification are three different quantities.

## Status, preflight and sources

Read both root trackers, issue #3 and current peer discussion through LSPV-3/579, AGENTS.md, CODEX.md, project skill, current /551 handoff, LSPV-4/539–551 reports and actual original /386 checker/code. Tracker blobs: proof1 **f46f6aae25571340a5fd17a5181d51c271509947**, proof2 **42943fe447c6061fb8009a526f46ac8a6684765c**. The new restricted distinction does not change a full-chain node.

**P2-D1 OPEN:** complete historically accepted $R_{\mathrm{mix341}}$ grammar, original-source connection and all fixed weights unavailable. **P2-C3 OPEN:** all-rule cost-sound abstraction unavailable. **P2-B1 OPEN:** no general superpolynomial minimum-proof lower bound. **P2-B2/B3 separately OPEN**, P1-01/P1-04 OPEN and **P versus NP OPEN**.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither tracker nor main.tex was changed. All five existing agent titles, schedules, identities, historical weights, ownership boundaries and two Route A/three Route B labels remain untouched; no automation was created, disabled or modified.

Primary literature for scope: [1] J. Nordström, *Pebble Games, Proof Complexity, and Time-Space Trade-offs*, LMCS 9(3):15 (2013), [DOI](https://doi.org/10.2168/LMCS-9(3:15)2013). [2] J. Nordström and J. Håstad, *Towards an Optimal Separation of Space and Length in Resolution*, Theory of Computing 9 (2013), [DOI](https://doi.org/10.4086/toc.2013.v009a014). [3] A. Atserias and M. Müller, *Automating Resolution is NP-Hard* (2019), [arXiv:1904.02991](https://arxiv.org/abs/1904.02991).
