# LSPV-4/564: Exact transient-peak versus cumulative-retention frontier for one native-/386 shared Resolution DAG

**November 12, 2026, 08:38 PST. PNP Time-Space Resource Auditor, historical Route A.**

**PROVED/RESTRICTED exact finite-DAG recurrence; COMPUTATIONAL independently reproduced in Python and Node; independent external review pending. P versus NP OPEN.**

## One candidate theorem and four falsifiers

**Candidate.** For the signed original-source, 35-Resolution-node fixed proof DAG of LSPV-4/560, with exactly four derived-result registers, no recomputation and permitted nonexpanding last-use overwrite, there is a strict tradeoff between (i) peak simultaneous retained canonical-clause payload during a deduction and (ii) cumulative post-step retained clause-byte area. A scalar lower bound in one resource cannot be claimed for the other resource without a same-realization schedule.

- **F1, cheaper peak:** a legal complete topological schedule has transient payload peak at most 44 canonical clause bytes. **Falsified** by exact exhaustive 44-byte reachability (1,171 nonterminal order ideals, 2,480 admitted edges); first feasible peak is 45.
- **F2, simultaneous minima:** a schedule with transient peak 45 also achieves the unconstrained cumulative area minimum 885 clause-byte steps. **Falsified**: the exact cap-45 minimum is 958; minimum 885 first becomes feasible at cap 51.
- **F3, invalid signed/native reconstruction:** a witness changes the original signed SOURCE, paid owner, defining facets, pivot or inference identities or introduces an illegal forward parent. **Rejected by independently replaying all 35 exact signed Resolution steps**, with fixed original SOURCE and gate objects. The three *new reordered packets* **were subsequently run through the unchanged original /386 checker as a Node v22.16.0 operating-system process**. Each was ACCEPTED with 3,915 checker assertions and eleven bundled adversarial rejection controls. Exact Git blob hashes of the original checker, source and three regenerated packets matched the published repository blobs before executing the CLI. See the separate immutable original-OS replay evidence below.
- **F4, a valid alternate proof or compact/recomputed calculation beats the fixed-DAG frontier.** **Admitted**: the theorem does not constrain other proof DAGs, Gaussian-elimination/GF(2) shortcuts, fresh extension variables, learned branch lemmas, recomputation or physical representation choices. The same original signed source already has a cheaper W29 proof and a restricted tree-like W28 witness (LSPV-2/576); this is a deliberate falsification control for universal extrapolation.

## Exact object and model

The source- and owner-identical packet is [LSPV-4/560's W38 accepted artifact](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_0436_LSPV4_560_W38_ACCEPTED.json), blob `6b72c961c2db19be87a0936361c467ef3445f4e2`. The unchanged archived-/386 checker is [`experiments/arc/lspv2_386_independent_verify.js`](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_386_independent_verify.js), original Git blob `338305c0ce101704205e57543756b8127074a986`.

This certificate has 17 mandatory signed original SOURCE clauses, six genuine free AND2 defining facets, 35 paid strict signed Resolution records, and **three globally paid conservative AND2 owners**. All 35 RES identities, 70 parent references (35 from paid RES and 35 from SOURCE/DEF), and 3 owners remain unchanged in all three constructed schedules. Logical charge is **W=35+3=38**. The fixed paid-only dependency depth is **13** inferences (SOURCE/facet input treated as depth zero). Owners are paid once globally, not once per facet or fanout consumer.

Let `D` be the executed subset of the 35 paid RES identities, `L(D)={u in D: some paid successor of u is outside D}`, and `b(u)=len(JSON.stringify(C_u))`, the exact canonical signed-clause-array payload length. An eligible ready deduction `v` can use a last-use paid parent register only if that parent has no successor outside `D union {v}` and `b(parent)>=b(v)`. In that case its clause payload is overwritten *after both premises are read*. Otherwise the output must first coexist with live parents in a fresh register.

For every ready `v`, define the transient register count and byte-payload demand:

```
R(D,v)=|L(D)| + (0 if eligible_nonexpanding_overwrite else 1)
M(D,v)=sum_{u in L(D)} b(u) + (0 if eligible_nonexpanding_overwrite else b(v))
```

For one no-recomputation schedule of 35 steps, **peak** `M*=max_v M(D,v)` and **post-step retention** `A=sum(poststep resident clause bytes)`. The final empty clause `[]` contributes its 2-byte canonical payload at the final post-step checkpoint, following LSPV-4/563's corrected common convention. SOURCE and DEF facets are read-only inputs and not charged as derived-result registers.

For a fixed peak cap `P` and four-result-slot capacity, compute exact `A_P=min A` across every ready order by an order-ideal dynamic program with exact parent availability and overwrite conditions. The recurrence is a complete shortest-path search in a finite DAG of execution subsets. The state cost is the cumulative `sum b(L(D))`, with terminal +2, and tie break is cumulative live-slot area, terminal +1. Reachability failure proves infeasibility **only in the declared restricted schedule model**.

## Exact independently replicated frontier

| Max transient canonical clause bytes | Reachable? | Minimum post-step byte area | Post-step slot area at that byte optimum |
|---:|:---:|---:|---:|
| 44 | No | n/a | n/a |
| 45 | Yes | **958** | 87 |
| 46, 47, 48, 49 | Yes | **958** | 87 |
| 50 | Yes | **927** | 87 |
| 51 and higher | Yes | **885** | 83 |

At 45 bytes, the exact area overhead relative to the 51-byte area optimum is **73/885 = 8.25%**, while the minimum transient payload peak drops by **6/51 = 11.76%**. Thus both extrema are attainable for the **same signed inference DAG and logical W38**, but **not in the same topological order**.

The two independent implementations agree on all nine tested caps and exact values, including **1,171 nonterminal visited subsets / 2,480 allowed edges** at cap 44, **1,202 / 2,541** at cap 45, **2,478 / 5,587** at cap 50, **3,370 / 7,861** at cap 51, and **6,887 / 18,789** at cap 1,000. The last recovers LSPV-4/563's exact 885-byte no-recomputation post-step minimum. State counters exclude the successful terminal subset.

Three newly serialized full signed certificates retain identical source, owners and paid inferences: [P45](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_0838_LSPV4_564_P45_W38_NATIVE386_CERT.json), [P50](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_0838_LSPV4_564_P50_W38_NATIVE386_CERT.json), [P51](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_0838_LSPV4_564_P51_W38_NATIVE386_CERT.json). Each is 3,640 UTF-8 bytes including the final newline. All paid RES original identities and signed resolvents were replayed, with chronological renumbering of both parent references. These are both **signed-step-validated and original-checker-ACCEPTED** packets. Independent local Node OS CLI replay of each exact published Git blob passed all eleven bundled hostile mutations, 3,915 checker assertions each.

## Exact resource ledger and limitations

| Operation in authenticated /386 fragment | Fixed paid logical cost | Evidence/application/verification | Resident and peak memory |
|---|---:|---|---|
| SOURCE | zero paid inference | 17 explicit signed clauses, provenance and source-index verification, retrieval costs | read-only input in abstract register model; real parser stores more |
| Conservative AND2 owner | one globally per declared owner | 3 owner declarations; wire namespace, declaration and validation costs | owner objects and lookup space excluded from the proxy |
| Defining facet | zero additional paid units | 6 genuine facet records, checks, references and retrieval | available as read-only records in proxy |
| Strict RES | one per executed inference, here 35 | two parent lookups per deduction, signed pivot, canonical resolvent, comparison and verification | up to four live-derived slots; transient byte demand counted in above metric |
| Shared result reference | no second charge for an existing paid inference | each actual application/retrieval still costs time and encoded index bits | producer remains live until last consumer or is explicitly recomputed at fresh logical charge |
| Delete/last-use overwrite | no additional logical inference | array writing, scratch, free-list bookkeeping and memory allocator costs not zero in an actual machine | nonexpanding overwrite is allowed only when parent no longer needed |
| AND3, GF(2), LOCAL-CONVERT, branching, joins, context/assumption discharge, exported/private wires | **not jointly authenticated with /386** | **do not import or invent historical weights** | all must be admitted as potential cheaper alternative paths in full R_mix341 |

The four slots and 45/51 clause bytes are **only an abstract resident signed-clause-payload model**, not actual process RSS, verifier bit-space, sequential proof-discovery time or general SAT lower bounds. In an actual /386 checker, the whole JSON is parsed, complete `dat.records` and `known[]` are held, the eleven bundled adversarial controls run, and temporary clause computation consumes additional memory. Even a streaming verifier must charge input bytes, reference digits, canonicalization, copying/recomputation, read-only source access, extra temporary output and all concurrent peak buffers. Source-external inference references are not counted as paid RES successors in the order-ideal state.

A cumulative resource may be minimized by a different execution than its peak. An abstraction claiming componentwise cost-nonincreasing simulation therefore cannot combine the 45-byte peak from one schedule with the 885-byte cumulative area from another and call that vector a realizable single-path witness. It may safely underapproximate both for a lower-bound *relaxation*, but cannot infer physical realizability from such a synthetic vector. This complements the epoch-aware recomputation firewall /563 and the cross-cone owner accounting /540.

## Provenance, corpus and primary literature

Root `proof1.txt` blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`, full `proof2.txt` blob `ba4d1c0faf9acbce836ffc5e16740b197e4c7bbe`, issue #3 including later LSPV-1/593, `AGENTS.md`, `CODEX.md`, project skill, original /386 checker, LSPV-4/539–549, /560–563, and relevant peers LSPV-2/576, LSPV-3/589–590, LSPV-5/505 were surveyed. Prior LSPV-4/558–563 had established slot extrema, recomputation-area extrema and common post-step convention; **this run newly establishes the exact finite nonrecomputed peak/area frontier and three signed-step-replayed source-identical certificates**. LSPV-1/593 and LSPV-5/505 additionally repair separate original /386 full-CLI wrapper scope issues; those are not assumed absent here. No prior theorem about mixed R_mix341 physical space was found.

Direct references: Jakob Nordström, [*Pebble Games, Proof Complexity, and Time-Space Trade-offs*](https://doi.org/10.2168/LMCS-9(3:15)2013), *LMCS* 9(3), 2013; Nordström and Håstad, [*Towards an Optimal Separation of Space and Length in Resolution*](https://doi.org/10.4086/toc.2013.v009a014), *Theory of Computing* 9 (2013); Cousot and Cousot, [*Abstract Interpretation: A Unified Lattice Model*](https://doi.org/10.1145/512950.512973), POPL 1977. These support model distinctions but do **not** prove this new finite numeric result. Pebbling is a structurally useful theorem-transfer model for the declared fixed paid-RES DAG, but a universal physical-machine/circuit lower bound transfer is **not established**.

## Reproduction and handoff

Standalone Python [`experiments/arc/lspv4_564_native386_peak_area_frontier.py`](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv4_564_native386_peak_area_frontier.py) searches complete finite order ideals, checks signed RES chronology against the source artifact when run in the repository root and offers explicit `--replay` for the unchanged archived Node OS CLI. A **separate original-checker Node OS replay was executed successfully** with the exact archived checker blob and all three exact regenerated certificate blobs. The published script's optional `--replay` mode is available for a further checkout replication. Independent Node [`experiments/arc/lspv4_564_independent_frontier.cjs`](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv4_564_independent_frontier.cjs) uses a different recursive memoized reachability implementation. Immutable [frontier evidence](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_0838_LSPV4_564_PEAK_AREA_FRONTIER_RAW.json) and [original-Node-OS checker acceptance evidence](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_0838_LSPV4_564_ORIGINAL_NODE_OS_REPLAY_RAW.json) includes exhaustive cap-state counts and complete witness orders. Deterministic exhaustive, no random seeds.

**Affected but OPEN**: P2-D1, P2-C3, P2-B1; P2-B2/P2-B3 separate and OPEN. P1-01/P1-03/P1-04 OPEN. No material load-bearing tracker status change: **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Fixed-rule mixed native calculus remains unauthenticated, and the evidence is not a general SAT lower bound. P versus NP OPEN.

**Next:** add explicit per-reference application/decoded-index bits and simultaneous scratch to *each same-schedule* vector; then test whether peak/area tradeoffs survive cost-sound recomputation and, only when authenticated, native mixed GF(2)/AND3 alternatives. Root `main.tex` has been reconciled within LSPV-4 ownership markers only, with exact full-content readback and preservation of every other specialist's content; the OS replay addendum is included. Git blob `97c1677a01a0b0cfeb0f31b0e8152962b08d6bc8`.
