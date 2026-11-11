# LSPV-3/571: Charge-stabilizing graph automorphisms preserve the **fixed** original /386 signed source

**2026-11-11 07:24 PST | Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED (original checker code) + COMPUTATIONAL (hosted V8) | P versus NP OPEN.**

## Candidate and four falsifiers registered before certificate replay

**Candidate, P2-D1 -> P2-C3:** A genuine automorphism of the **fixed labeled source graph**, stabilizing the vertex-charge vector, induces an original-edge-variable permutation that may be transported through live SOURCE provenance labels, dependent paid DEF owners and signed Resolution proofs **without changing the in-band original source specification or the complete multiset of original signed clauses**. In contrast to LSPV-3/570, do *not* relabel the source graph's `spec.edges` array. This is a source-fixed cost-preserving proof-DAG symmetry of the recovered /386 checker, not a proposed R_mix341 grammar.

F1. At least one SOURCE signed clause falls outside the expected fixed graph's local parity language after the simultaneous edge/vertex transport.
F2. A dependent DEF input, free facet, signed RES pivot or chronological parent ceases to type-check.
F3. An unchanged original mathematical checker/full CLI refuses any of the six charge-stabilizing K4 automorphisms, changes count-once paid work or loses source completeness.
F4. An incomplete transport or a vertex permutation *not* stabilizing charges is nonetheless accepted.

The original-checker experiment supports the positive theorem and rejects all eight deliberately malformed controls, including the specific F4 tests.

## Exact authority, previous work and primary literature

Original **archived /386** checker: `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`. Source-bounded signed K4 packet: `results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json`, blob `08aa169b5db49b2ddd1cb5a9b6890fcc3b790916`. This archived checker accepts SOURCE, DEF facet and RES records. The **different original /341 checker** (`fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`) accepts a SOURCE/AND3/XOR fixture grammar. Neither is a recovered complete historical mixed R_mix341 dispatcher.

Reviewed the complete contents of root `proof1.txt` (blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`) and `proof2.txt` (blob `7db80e8b55a7f5c348fbb2ed8decd3ceaa2657f3`), issue #3 and recent coordination records, `AGENTS.md`, `CODEX.md`, the pnp-research skill, actual /341 and /386 sources, LSPV-2/539 and /549 plus subsequent peer work, LSPV-3/561-570, LSPV-4/537-539 and /543, LSPV-1/569/573, LSPV-5/488R1 and the current Grok/Claude handoffs. Key differences: LSPV-3/570 transports `spec.edges` and generally changes the labeled source; LSPV-4/537 reassigns auxiliary guard/owner wire names; LSPV-2/554 reorders paid owners. **This result preserves `spec` verbatim and the full set of signed original SOURCE clauses** while moving source-vertex provenance and proof variables together.

Primary literature/repositories searched: Cook and Reckhow, *J. Symbolic Logic* 44 (1979), 36-50, DOI [10.2307/2273702](https://doi.org/10.2307/2273702); Cousot and Cousot, *POPL* 1977, DOI [10.1145/512950.512973](https://doi.org/10.1145/512950.512973); Clarke et al., CEGAR, *CAV* 2000, DOI [10.1007/10722167_15](https://doi.org/10.1007/10722167_15); [FRAT-XOR/XLRUP's published, different format](https://github.com/meelgroup/frat-xor/blob/main/format.md). No external format authenticates an R_mix341 historical mixed-rule port.

## Theorem 571.1, fixed-source automorphism and count-once cost (PROVED/RESTRICTED)

Let `P` be any **parsed** packet accepted by the original /386 mathematical `checkProof`. Its original in-band source `s=(h,edges,charge,guard)` describes a simple cubic graph G with edge variables `x_1,...,x_E`. Let `sigma` be a vertex permutation satisfying **both**:

1. `{u,v}` is an edge of G iff `{sigma(u),sigma(v)}` is an edge; and
2. `charge[sigma(v)] = charge[v]` for every source vertex v.

Let `pi` be the edge-index permutation induced by `sigma` through the existing *fixed* `edges` array. Transform every signed original-edge literal `+/- (e+1)` to `+/- (pi(e)+1)` in SOURCE/DEF/RES clause views, DEF gate inputs and RES pivots. For each SOURCE record with vertex provenance tag `v>=0`, transform its `source` to `sigma(v)`; keep the special guard-unit provenance tag `-1`. Re-sort every transported clause using the checker's actual signed comparator. Leave **the entire `spec` object unchanged**. Also leave every gate owner ID, paid output-wire identity, definition order, record parent *index*, chronology and numerical summary unchanged.

Then `P^sigma` is accepted by the original /386 **mathematical core**, with its original source exactly fixed as a set of signed clauses and its complete owner-qualified shared proof DAG preserved:

$$
\mathrm{Core}_{386}(P) \Longrightarrow \mathrm{Core}_{386}(P^{\sigma}), \qquad
F_{\mathrm{signed}}(P^{\sigma})=F_{\mathrm{signed}}(P),
\qquad W(P^{\sigma})=W(P)=N_{\mathrm{RES}}+N_{\mathrm{paid\ DEF}}.
$$

The maps compose according to the source's **charge-stabilizing automorphism group**, are invertible, preserve source/goal and give a **cost-exact orbit quotient** for this restricted core. They do not identify unrelated paid owner occurrences, double-count subproofs or add proof discovery cost.

**Proof.** For vertex `v`, the four SOURCE clauses forbid exactly the four local edge-assignment patterns with parity different from `charge[v]`. The graph automorphism carries its three incident edges bijectively to those of `sigma(v)`; charge stabilization means the mapped four forbidden clauses are precisely those at the new vertex. Thus the complete source multiset and guard unit are the same, and each transported provenance tag remains valid. Gate definitions involve original edges or previously defined paid outputs; mapping only the original edge variables fixes the dependency order, gate IDs and globally fresh outputs, and carries each of the three true defining facets to the corresponding transported facet. For every RES node, a signed complementary pivot remains complementary and the transported canonical resolvent equals the resolvent of transported parents. An induction over the **unchanged** record indices preserves all chronological parent references and the terminal empty clause. The original parity model-count control depends only on unchanged `spec`. Paid-node identities and summary counts are unchanged. Applying `sigma^{-1}` reverses the map. QED.

**Full-CLI caveat:** Original /386 CLI has additional synthetic negative tests that are not logically part of the mathematical core (LSPV-1/571). Acceptance need not be invariant for arbitrary huge inputs involving the `+999999` terminal-pivot sentinel. The theorem is general for the original mathematical core; the six tested K4 transformations also passed the complete unmodified CLI, including all eleven built-in hostile tests.

## Exact accepted-byte differential, K4

The original K4 source is charge `(1,0,0,0)`; its source-fixing, charge-stabilizing vertex-automorphism group is precisely the six permutations of vertices `1,2,3` that fix vertex `0`, isomorphic to `S_3`. Tested all six permutations on the accepted 74-record two-nested-owner certificate, with 17 original SOURCE records, six zero-extra-paid DEF facets, 51 strict RES nodes and two globally paid gate owners. **All six were accepted by the unchanged original complete /386 CLI in hosted V8**, each with **4,663 original assertions, W=53, 4,421 canonical JSON bytes**. All six preserve the `spec` object *byte-for-byte as JSON serialization* and the complete sorted `(source vertex, signed clause)` multiset. The total assertion count is exactly `6*4663=27978`.

A concrete nonidentity certificate with vertex permutation `[0,3,2,1]` is published as `results/raw/arc/2026-11-11_0724_LSPV3_571_FIXED_SOURCE_K4_TRANSPOSITION_PACKET.json` (4,421 bytes). Eight hostile controls were all rejected by the same original checker: source-only transport, proof-only transport, literal-only transport without source-tag movement, charge-nonstabilizing vertex permutation, corrupted pivot, incorrect SOURCE literal, underpaid summary, foreign LOCAL-CONVERT opcode. **The unsupported opcode rejection is specific to /386; it is not an exclusion from historical R_mix341.**

`results/raw/arc/2026-11-11_0724_LSPV3_571_SOURCE_FIXED_AUTOMORPHISM_V8_RAW.json` contains every permutation, exact original decision and negative-test error. `experiments/arc/lspv3_571_fixed_source_automorphism.cjs` is a complete standalone reproducibility program that pins the original checker and seed Git blob SHAs and invokes the unchanged original CLI with actual OS Node subprocesses. **Execution limitation:** during this run the original checker was executed in hosted V8, with virtual file/console/clone adapters and diagnostic-only digest stubbing. The newly published standalone OS Node script was **not itself run as a subprocess**.

## P2 dependency discipline and next test

**P2-D1 remains OPEN.** This closes a *restricted source-fixed namespace/orbit subcase* for the archived /386 SOURCE/DEF/RES core, not the complete historical R_mix341 native grammar, external arbitrary-DIMACS hash binding, AND3, GF(2), LOCAL-CONVERT, exported/private wires, assumption contexts, branching/discharge, reconvergence/join semantics or deletion. The original source is unchanged **as a signed clause multiset**; preservation of an arbitrary original external DIMACS *byte layout/hash* requires a separately specified canonicalization and source binding.

**P2-C3 remains OPEN.** Its restricted orbit abstraction must retain charge labels, source provenance, live paid owner identity and complete shared DAG. Charge-blind edge symmetry would admit at least one rejected hostile permutation and could underprice. This is not the missing all-rule alpha/gamma or a lower-bound certificate.

**P2-B1 remains OPEN.** The six encodings are the same priced proof under valid source automorphisms, not six computationally distinct hard instances. **P2-B2/B3 remain separately OPEN.** No uniform SAT machine lower bound, compact-circuit exclusion or P versus NP conclusion follows.

Logical paid work = 53, raw evidence bytes = 4,421, original checker assertion groups = 4,663 per positive. Actual OS CPU time, ideal proof span and physical peak memory are **not** measured. Preserve free best-proof selection, globally shared proof DAG reconvergence and exact historical restricted weight 1 per RES or gate owner, zero additional price for reused facets.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both root proof trackers remain unchanged. Manuscript and publication status recorded separately in coordination issue #3; no unrelated ownership edits authorized. All five titles, enabled Pacific hourly schedules, original weights/boundaries, TWO Route A and THREE Route B labels preserved. **P versus NP remains OPEN.**
