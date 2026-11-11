# LSPV-4/536: Native archived /386 active nested-owner chains, cost-once accounting and exact dead-facet deletion

**2026-11-10 23:45 PST | PNP Time-Space Resource Auditor | historical Route A retained | PROVED/RESTRICTED (symbolic construction in the archived /386 grammar) + COMPUTATIONAL (original checker replay). P versus NP OPEN.**

## Candidate theorem and falsifiers, before testing

**Candidate:** On the original guarded K4 source, the *actual archived* `/386` verifier accepts a parametrized chain of **active**, not unused, paid nested extension owners. Every additional owner can be passed into and out of strict Resolution ancestry, adding exactly one distinct paid DEF owner, two paid RES inferences, three free defining-facet records, and five chronological records. A source- and owner-preserving deletion of the one unneeded facet per owner decreases representation size but does not increase paid logical work.

F1: two-or-more chained gate owners violate the *actual* original declaration/freshness rule or a signed facet. F2: the first accepted chain is only a dead metadata extension whose paid owners do not occur in sink ancestry. F3: a parent index, pivot, owner, original source clause or payment count can be changed without rejection. F4: deletion of dead facets breaks the complete CLI, silently drops a live dependency or charges a shared owner repeatedly. Eight positive parameter values, original-body replay, exhaustive finite original-source model evaluation, an independently computed ancestry/depth ledger, and eleven new corruptions address these falsifiers. All four failed within the exact declared scope.

## Exact historical authority and precedence

The original mathematical mixed-calculus declaration is `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (Git blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`). It declares the intended native unit-paid RES, AND3, GF(2), LOCAL-CONVERT and conservative paid definitions, **but no single complete five-rule accepted-byte dispatcher has been recovered**. The original archived /341 checker `experiments/arc/lspv2_341_independent_verify.js` (blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`) is a distinct SOURCE/AND3/XOR fixture verifier and is not used as the authority for this theorem. The authoritative *restricted* checker used below is **the unchanged archived /386** `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`.

**Prior art explicitly preserved:** LSPV-3/561 published the accepted one-owner 50-paid guarded K4 seed (`d0fa96a155672f8f6a6a3428eacafa15e79b9e88`). LSPV-3/563 published and tested **the k=1 two-owner case** at 53 paid, which this run reproduced before generalizing. LSPV-4/535 already distinguished free facets from paid owners, found checker CLI/core mismatch, and sliced irrelevant facets. This run's distinct result is a *constructive nested owner chain of arbitrary tested length, every owner active in a sink-ancestral strict RES path, with exact count-once work/span/reference formulas and full-CLI-valid deletion of one dead facet per owner*. LSPV-2/549 showed that two different checkers accepting the same JSON object do not authenticate a cross-language inference. LSPV-2/550 documented a globally semantic MAY abstraction cost collapse, and LSPV-3/554 documented the invalid operational-ACCEPT vs semantic-UNSAT identification for the separate /341 checker.

Both root trackers were read (`proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, `proof2.txt` preflight blob `b148b8e9270f5911c4f9daa5df1d8e182ea22a2a`), together with issue #3 and its current tail comments, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, all material /539 through /549 role evidence, LSPV-2/550, LSPV-3/561-563, LSPV-4/524-535 and current coordination handoffs. The repository directories, main.tex blob `efad5ac1bb75fce04945256b09341830becba9d4`, relevant tasks and historical owner markers were surveyed. No actual full R_mix341 mixed dispatcher was discovered. **Corpus correction:** the k=1 nested construction is explicitly credited to /563 rather than treated as new.

## Theorem 536.1: accepted nested paid owner chain, exact logical cost

Let `P_0` be the exact accepted archived guarded K4 certificate with 17 original signed SOURCE records, paid owner `g_0=(0,8,1,2)` for `z_0=x_1 AND x_2`, three zero-extra-charge facets and 49 paid RES nodes. Its derived clause at original chronological index 20 is

```text
C_0 = [-2, 3, -7, -8].
```

For each positive integer `i<=k`, declare a new paid owner `g_i=(i,8+i,7+i,-3)`, or semantically

```text
z_i = z_(i-1) AND (NOT x_3),
where z_i is wire 8+i and z_0 is wire 8.
```

The original `views(z_i,z_(i-1),-3)` returns exactly these three signed facets, sorted canonically by absolute literal and then sign:

```text
[z_(i-1), -z_i]         (forward facet)
[-3, -z_i]             (unused facet)
[3, -z_(i-1), z_i]    (backward facet)
```

All owners are entered into the original declaration bank in order. Insert these 3k facet records before the old `C_0` record. Define `C_i=[-2,3,-7,-z_i]`. First insert k strict forward RES records

```text
RES([z_(i-1),-z_i], C_(i-1); pivot=z_(i-1)) = C_i.
```

Then insert k reverse RES records in the order `i=k,k-1,...,1`:

```text
RES([3,-z_(i-1),z_i], C_i; pivot=z_i) = C_(i-1).
```

The duplicate literal `3` is removed by the original `key` canonicalization; `C_0` is recovered exactly. Redirect all former uses of original `C_0` to the newly paid returned `C_0` and shift all other chronological indices. There is no new original source clause and the terminal empty clause is unchanged. By induction, the two signed RES steps per owner are exact legal resolvents, all gate inputs refer only to original variables or previously declared fresh outputs, and every chronological parent precedes its consumer. The original source is unchanged.

For each admissible k that fits the finite JavaScript safe-integer identifier grammar and physically representable JSON input, the original /386 mathematical core and complete standalone checker execute the same successful checks. Its exact ledgers are:

$$
\boxed{W_{386}(k)=49+2k+(1+k)=50+3k}
$$

$$
\boxed{R_{386}(k)=2(49+2k)=98+4k}
$$

$$
\boxed{N_{\mathrm{records}}(k)=17+(3+3k)+(49+2k)=69+5k.}
$$

There are `1+k` **distinct paid owners**, `3+3k` zero-extra-paid facet records, and `2+2k` facet records in the terminal strict-RES ancestry. All `1+k` owners are transitive dependencies of the terminal, as checked independently through facet owners and definition-input dependencies; the original 17 signed SOURCE records remain ancestors. The number of sink-ancestor *records* is `68+4k`.

**Proof of count-once:** The charge belongs to the unique gate owner declaration, not to each of its three views or its multiple later references. Every new RES has its own chronological record and costs one. A shared preceding proof node is never re-created merely because its index occurs in another parent list. Therefore the displayed W counts the 49+2k distinct RES plus 1+k distinct owners exactly once. Any abstraction charging one paid unit per DEF facet instead would assign `W#=W+(3+3k)`, which is **strictly larger** than this authentic concrete charge and violates the required `W#<=W` path polarity.

The source is UNSAT by independently checking all `2^7=128` signed guarded assignments. This construction **does not prove** the existence of a large minimum refutation cost; the added detours are deliberately redundant.

## Theorem 536.2: cost-safe CLI-compatible live-owner facet normalization

In `P_k`, the second facet `[-3,-z_i]` of every owner (`i=0,...,k`) is never used as a RES parent. Remove these exactly `k+1` records, consistently reindex remaining RES parents, and update only the mechanical `summary.def_views` and `summary.live_records` counts. Keep **all** `k+1` paid gate owners, both still-used facets per owner, all RES nodes, original source and original terminal.

The result `Q_k` satisfies

$$
\boxed{N_{\mathrm{records}}(Q_k)=68+4k, \quad W(Q_k)=50+3k=W(P_k).}
$$

Every removed record has zero additional logical work, and no remaining RES parent uses it. Its gate owner is retained because its other facets and next owner's signed input depend on it. The original complete CLI's known nonempty-gate self-test still has at least one owner, so it accepts both `P_k` and `Q_k`. This is an exact *family-specific* backward slice and represents a cost-nonincreasing concrete normalization. It is **not** a universal all-rule CEGAR or a theorem that all original CLI proofs can be sliced in this manner.

## Source-body replay, hostile controls and evidence

The unmodified original archived /386 JavaScript checker source was loaded into an isolated V8 execution, using only virtual input-file contents, a console capture and an output-digest stub. The original `checkProof` and its **eleven bundled hostile mutation checks** were executed without modification. For `k=0,1,2,3,4,8,16,32`, all **eight full** and all **eight facet-sliced** packets were accepted. The original-source model checker found zero satisfying assignments among the 128 guard/edge assignments. Independent ancestry/owner-closure and gate-aware depth computations passed.

| k | Full bytes | Sliced bytes | Paid W | Records full/sliced | Active owners | Gate-aware span |
|--:|--:|--:|--:|--:|--:|--:|
| 0 | 4,143 | 4,095 | 50 | 69/68 | 1 | 10 |
| 1 | 4,421 | 4,324 | 53 | 74/72 | 2 | 12 |
| 2 | 4,705 | 4,558 | 56 | 79/76 | 3 | 14 |
| 4 | 5,284 | 5,037 | 62 | 89/84 | 5 | 18 |
| 8 | 6,449 | 5,994 | 74 | 109/100 | 9 | 26 |
| 16 | 8,846 | 7,960 | 98 | 149/132 | 17 | 42 |
| 32 | 13,611 | 11,913 | 146 | 229/196 | 33 | 74 |

The **eleven further hostile changes** all rejected under the unmodified checker: owner order reversal, duplicate owner ID, duplicate output wire, incorrect nested input, malformed signed facet, negative pivot where positive required, understated paid-total field, changed original SOURCE clause, forward parent reference, corrupted contradiction and deletion of a required gate owner. For the k=4 full packet, the original checker asserted 5,623 times, with the sliced packet at 5,413; these are checks in the JS verification code, **not physical elapsed time**. For k=32, assertion counts were 14,583 and 13,197. The bundled 11 CLI controls passed for all 16 positive packets.

The exact reproducibility inputs, source hash pins, original-checker invocation, all family constructors, hostile mutation tests, and dead-facet slicer are in `experiments/arc/lspv4_536_native_nested_owner_chain.cjs`. Its syntax was parsed successfully in hosted V8, but the published script itself was **not executed as a native operating-system Node process**. Its built-in Node VM/checker, cryptographic hashes, and raw stdout should be rerun in a full checkout. Actual process high-water RAM, physical processor time and host allocation sizes were not measured. The hosted replay used an output-only digest stub; neither its result nor the assertion count is a SHA-256 verification.

Raw observed V8 ledger: `results/raw/arc/2026-11-10_2345_LSPV4_536_NATIVE_NESTED_OWNER_CHAIN_RAW.json`.

## Resource semantics, abstraction obligations and cost firewall

| Operation or resource | Authentic /386 logical tariff | Mandatory evidence and application resources | Other machine resources |
|---|---|---|---|
| SOURCE | 0 | Signed canonical clause, occurrence/vertex identity, parents empty, original guarded K4 source match | Parse/compare, source retrieval and retention; real byte cost, not inferred from W |
| Paid DEF owner | 1 per unique declaration `id` and fresh output wire | Full owner tuple `[id,z,a,b]`; safe-int IDs, globally fresh output, declared-earlier inputs, guard exclusion | Parse and store gate bank; nested lookups; gate dependency depth; emit no duplicate charge |
| Defining facet | 0 extra, never 1 | Signed sorted clause exactly in a gate's three defining views; empty parent list and owner pointer | Nonzero serialized bytes, validation, retrieval and live retention; may delete unused facet safely only when no references |
| Strict RES | 1 per distinct RES record | Two earlier parent indices, oriented signed pivot and exact tautology-free canonical resolvent | Parent retrieval, set-union/sort and comparison; cache/recompute/retention physical costs separate from proof DAG paid identities |
| GF(2), AND3, LOCAL-CONVERT, branching, contexts, discharge, weakening, joins, deletion, private/exported wires | **UNAUTHENTICATED IN THIS CHECKER** | No accepted `/386` opcode has authenticated the historical full-rule cost/byte grammar | Must remain conservative MAY cases for any proposed whole-Rmix lower bound |
| Reference applications and work space | No separately authenticated per-reference *logical* tariff | Exactly `98+4k` directed RES-parent applications; serialized decimal IDs contribute bytes | The checker `known` retains `69+5k` complete clause arrays, an implementation upper-space behavior, **not a universal space lower bound** |
| Span | Depends on execution assumptions | In the model with one paid unit per gate declaration along prior-owner edges and one per RES, zero extra for facets, the sink dependency depth is exactly `10+2k` | A different parent-only depth convention may differ by a constant; neither equals measured parallel verification time |

**Concrete-step inclusion and goal polarity:** For the explicitly generated `/386` paths, the abstraction that copies every SOURCE/DEF/RES record, signed pivot, chronological parent relation, owner first-use identity and original guarded source produces an abstract path of the *same* paid work `50+3k`, ending in the same empty clause. The verified dead-facet slice has equal paid W and remains CLI-accepted. A per-facet paid abstraction produces a larger cost than a legal concrete path, demonstrating a concrete violation of abstract-cost soundness. No theorem is claimed that one can map **all** full-historical Rmix traces with no greater cost.

**Representation and recomputation:** The compact JSON sizes are actual serialized **ASCII packet** lengths for this family; a sparse affine row, giant identifier, invalid UTF-8 alias, or branch join could change another checker representation or host cost, and the current /386 operation set has no GF(2) row grammar. Retaining all rows in `known` consumes memory growing with record count; a read-only indexed rescanning verifier can use a different time/space tradeoff but is not proved here for this entire original JSON parser. Source, certificate and shared-node evaluation occur on different resource measures. `W_R` denotes an ideal minimum over genuine legal source-authenticated refutations, not the cost of discovering the displayed padded certificate or the time of checking it.

**Mandatory countercontrols:** The exact /341 XOR/GF(2) shortcuts remain valid separately and may beat any RES-focused lower-bound candidate; /386's 47-RES core certificate from LSPV-1/564 removes this *entire* gate detour (although its original complete CLI rejects the zero-gate record due to the self-test artifact found in /535). Learned lemmas across compatible branches, retention/recomputation schedules, very large identifiers, affine compression and zero-cost closures all remain legal hazards to transferring a bound to the missing full historical calculus. No nonnegative additive decomposition lower bound is asserted without a formally proved disjoint paid-identity partition.

**Cross-domain and barriers:** Cook and Reckhow's proof-system definition is directly relevant to the need for an exact sound checker, but does not prove a historical parser. Nordström's pebbling/simulation literature is a **structural analogy** for sharing and retention, not a same-model transfer to arbitrary Rmix logical work. Hardware fanout/memory routing costs are an **analogy only**, since no physical VLSI layout or machine model is mapped. The representation-facet vs owner distinction is similar to structured proof logging, but external FRAT/LRAT/DRAT syntax is **not an Rmix accepted-byte authority**. The result does not address relativization, algebrization or Natural Proofs separation barriers because it asserts no circuit lower bound or unconditional SAT time lower bound.

## Status, files, handoff

**[P2-D1] OPEN:** New authentic archived /386 signed chain family, not a complete one-checker five-rule `R_mix341` grammar. **[P2-C3] OPEN:** Family-specific exact paid-owner/free-view projection and cost-safe slice, not an all-rule cost-sound abstraction. **[P2-B1] OPEN:** Deliberate lengthened refutations provide **upper-bound** controls only. **[P2-B2/B3] OPEN separately:** no SAT-in-P-to-fixed-R compiler. **P versus NP OPEN.**

**Proof trackers:** Reviewed both. A new scoped [P2-L4-536] entry is warranted under proof2 because the k-dependent accepted-byte /386 witness and exact normalizer are a material extension of /563 and /535; proof1 remains unchanged. Root `main.tex` must be reconciled **inside LSPV-4 ownership markers only**. No existing task identity, title, schedule, timezone, historical fixed rule weight, two Route A/three Route B allocation or ownership boundary is to be changed.

**Next decisive target:** authenticate a **single checker** whose actual accepted byte grammar connects a signed /386 RES/DEF facet to an AND3 or GF(2)/LOCAL-CONVERT operation, then audit real shared-identity first-use cost and source/goal preservation. A two-checker polyglot or a typed *reference* completer is not enough.

### Primary references

[1] Cook SA, Reckhow RA. The Relative Efficiency of Propositional Proof Systems. *Journal of Symbolic Logic*. 1979;44:36-50. DOI: 10.2307/2273702.

[2] Nordström J. Pebble Games, Proof Complexity, and Time-Space Trade-offs. *Logical Methods in Computer Science*. 2013;9(3:15). DOI: 10.2168/LMCS-9(3:15)2013.

[3] Heule MJH, Kiesl B, Biere A. Strong Extension-Free Proof Systems. *Journal of Automated Reasoning*. 2020;64:533-554. DOI: 10.1007/s10817-019-09516-0.
