# LSPV-3/572: exact source-fixed cycle-space symmetry of the original archived /386 certificate checker

**2026-11-11 08:24 PST | Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED symbolic theorem plus COMPUTATIONAL unchanged-original-checker hosted-V8 replay. P versus NP OPEN.**

## IDEA: candidate and four pre-search falsifiers

**Single candidate [P2-D1 -> P2-C3]:** Unlike the vertex automorphisms of LSPV-3/571 and the source-changing edge gauge transformations of LSPV-3/565, a **cycle-space edge-sign flip** acts on accepted SOURCE/paid-DEF/Resolution certificates while keeping the complete original signed clause multiset, original source *vertex tags*, in-band source graph/charge/guard, global paid-owner IDs and logical work unchanged. For connected G, there are exactly 2^(|E|-|V|+1) such transformations. This applies only to the authentically recovered /386 sublanguage, **not** the missing complete historical R_mix341 grammar.

F1. A nonzero even-incidence edge flip breaks an original SOURCE, a nested DEF facet or strict Resolution pivot and the unchanged checker rejects.

F2. An odd-incidence edge flip, with graph/charge spec fixed, is accepted by the original checker.

F3. The positive transformations modify a signed original SOURCE multiset, paid gate-output identity, original-source provenance tag or count-once W.

F4. A positive proof accepted by the mathematical core fails the original complete CLI's extra model-count/negative-test phase.

All four were falsified for the complete 64-mask K4 differential. The symbolic proof supplies the stated core-level theorem for every accepted /386 packet, with the full-CLI qualification below.

## Source/corpus authenticity and search

Read both complete root trackers: proof1.txt Git blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2.txt Git blob 7db80e8b55a7f5c348fbb2ed8decd3ceaa2657f3. Their P1-01/03/04 and P2-D1/C3/B1/B2/B3 statuses remain OPEN. Read current issue #3 and recent LSPV-1/574, LSPV-2/559, LSPV-4/544 and LSPV-5/489 comment evidence, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, current five-role handoffs, actual original /341 and /386 source, the authentic LSPV-3/563 nested-owner seed and LSPV-3/565, /570 and /571 reports. Checked peer LSPV-2/538, /549, LSPV-1/573 and GROKPROOF 2026-11-11 07:20, plus targeted repo searches for prior cycle-kernel /386 stabilizer work. In contrast to earlier /565 and /571, the present group acts **without source charges changing, edge labels moving or source provenance tags being permuted**. No earlier source-fixed kernel-group exhaustive original-CLI witness was found in the relevant searched corpus.

Immutable original checker: experiments/arc/lspv2_386_independent_verify.js, Git blob **338305c0ce101704205e57543756b8127074a986**. Immutable accepted 74-record seed: results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json, Git blob **08aa169b5db49b2ddd1cb5a9b6890fcc3b790916**. Distinct recovered /341 fixture checker: experiments/arc/lspv2_341_independent_verify.js, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. Neither archived checker supplies the complete R_mix341 RES/AND3/GF(2)/LOCAL-CONVERT/DEF/branch/discharge grammar.

Primary literature independently searched: Cook and Reckhow (1979), *The relative efficiency of propositional proof systems*, J. Symbolic Logic 44, 36-50, DOI 10.2307/2273702; Cousot and Cousot (1977), POPL, DOI 10.1145/512950.512973; Clarke, Grumberg, Jha, Lu and Veith (2000), CAV, DOI 10.1007/10722167_15. External [FRAT-XOR](https://github.com/meelgroup/frat-xor/blob/main/format.md) and [cake_lpr](https://github.com/tanyongkiam/cake_lpr) are separate checker formats; their syntaxes cannot be imported into /386 or R_mix341. Cycle-space linear algebra is a direct exact symmetry theorem in this recovered checker; abstract interpretation and CEGAR supply the formal method, not the missing full historical rule authentication.

## Theorem 572.1: exact original-source stabilizer (PROVED/RESTRICTED)

Let P be a *parsed*, accepted original /386 checker packet whose in-band fixed source specification s=(h,E,b,g) is a connected simple cubic graph G=(V,E), binary odd vertex charge b, and guard g. Let B be its vertex-edge incidence matrix over GF(2). Select any f in ker B, where f is a bit vector indexed by the **original edge variables**, not the globally fresh auxiliary output wires. Define T_f on each signed original edge literal x_e by sign negation exactly if f_e=1; preserve all nonoriginal gate and guard literals. Apply T_f consistently to **every** signed SOURCE/DEF/RES clause, every paid gate's two signed inputs, and every RES pivot; canonical-sort every resulting signed clause using the original checker's comparator. Preserve source vertex tags, exact spec, source IDs, gate/definition IDs and output wires, parent indices, entire record order, cost summary, and terminal empty clause.

Then the original /386 mathematical core accepts T_f(P); its original signed SOURCE *multiset with provenance tags* is exactly the same as P's, and

    W_386(T_f(P)) = W_386(P) = (# RES records) + (# globally paid gate definitions).

The transformations compose by xor of their bit vectors and have inverses equal to themselves; on fixed spec the legal edge-flip group has cardinality 2^(|E|-|V|+1). The full shared proof DAG (including whole-DAG reconvergence and all repeated references to one paid owner) and logical work remain identical.

**Converse for this transport.** If f is not in ker B, at some vertex v the number of flipped incident edges is odd. Every original SOURCE clause at v forbids one local assignment of parity opposite to b_v. Under T_f its forbidden assignment changes parity and is *not* one of the source clauses permitted at vertex v. Since every accepted packet contains all four original clauses at every vertex and source tags are held fixed, its first transformed SOURCE at that vertex fails the checker's exact expected-source test. Therefore the checker rejects T_f(P) when Bf != 0. This is a classification of this particular **fixed-spec, fixed-tag, comprehensive sign-flip transport**, not of every arbitrary accepted certificate.

**Proof of forward direction.** At v, complementing selected incident edge bits shifts local parity by (Bf)_v=0, so it permutes the four forbidden local assignments within the same vertex's four original SOURCE clauses. All original SOURCE vertex provenance stays correct and the complete signed original clause multiset is fixed. The paid definition D(z,a,b) has free defining facets (-z OR a), (-z OR b), (z OR -a OR -b); signed literal sign-complementation maps all three facets to the facets of D(z,T_f(a),T_f(b)), without changing z or its owner. For any strict Resolution with signed complementary pivot p, transporting both parents and T_f(p) transports the exact signed resolvent; canonical sorting commutes with transport at the set level. Topological induction over original record positions preserves every check and the terminal empty clause. Since gate IDs, gate count and RES record identities do not change, W is exactly invariant. The source and cost results follow. The kernel dimension is |E|-rank_GF2(B)=|E|-|V|+1 by connected incidence-matrix rank. QED.

**Precise scope qualification:** Original /386 complete CLI includes synthetic negative controls in addition to the mathematical checkProof core. Some very large packets involving its hard-coded +999999 pivot corruption sentinel may behave nonextensionally (LSPV-1/571). The general theorem concerns its mathematical core; all 64 K4 packets below were executed against the **complete** original CLI.

## Theorem 572.2: source-retracting exact-cost orbit abstraction (PROVED/RESTRICTED)

For the parsed, correctly typed original /386 SOURCE/DEF/RES fragment, define concrete state C to retain the entire source specification and provenance, all live signed clause nodes, the complete shared record DAG, gate declarations and globally fresh output identities, chronological parents, paid owner identities, and fixed original-source closure. The group K=ker B acts on this state as above. Define alpha(C) to be the orbit [C]_K (implemented by the lexicographically least **canonical parsed** representative), and gamma([C]_K) to be all its concrete orbit members. Then SOURCE insertion from its authenticated local source set, true free DEF-facet insertion and signed RES insertion are K-equivariant. Their quotient transformers are well-defined and satisfy exact concrete-step correspondence:

    Post(gamma(A)) = gamma(Post_sharp(A))

for the group-closed subset of those transitions, and W_sharp([C])=W(C). This is an exact-cost, source-preserving subdomain with terminal-goal preservation and no charge for choosing the best proof. It is **not** the all-rule alpha/gamma requested by P2-C3: byte-level malformed JSON aliases, external DIMACS-byte binding, branching contexts, weakening, deletion, exported/private wire interfaces, LOCAL-CONVERT, AND3, XOR and all unknown native transitions require their own authenticated treatment or conservative MAY overapproximation. The orbit is an exact quotient of a *parsed* typed fragment, not automatically a quotient of raw UTF-8 accepted-byte lexemes.

## Original-checker exhaustive accepted-byte differential

The K4 source has four vertices and six original edge variables. Its incidence rank is 3, so the predicted kernel has 2^3=8 members. Exhaustively enumerated **all 64** edge sign-flip masks with the same 74-record nested-owner seed:

- Exactly **8/64 ACCEPTED** by the complete unchanged original /386 checker, at decimal mask indices **0, 11, 21, 30, 38, 45, 51, 56**.
- Exactly **56/64 REJECTED**, and these are precisely the 56 masks with at least one odd-incidence vertex. All rejects have original-checker SOURCE errors.
- Every accepted packet preserves the exact in-band spec, original signed SOURCE multiset with **unchanged** source vertex tags, gate owner IDs, nested DEF dependencies, 74 shared records, 17 SOURCE, six free DEF facets, 51 paid RES and two paid owners.
- Every accepted packet pays **W=53**, passes **4,663** original CLI assertions including **11** built-in negative controls; eight positive executions entail 37,304 assertion groups and 88 internal negative-control runs.
- Six extra deliberately malformed packets are **6/6 rejected**: SOURCE literal change, wrong SOURCE vertex tag, incomplete nested DEF-input transport, incomplete RES pivot transport, duplicate paid output wire and underpaid summary.
- An independently computed Python GF(2) enumeration of the six K4 edges returned the same eight masks.
- A concrete nonidentity **4,440-byte** certificate for mask 11 was published. Its original and transformed signed SOURCE *sets* coincide, while individual record clause bytes are allowed to be permuted within a provenance class.

**Execution authority:** The unchanged complete original /386 checker body executed for every tested packet in hosted V8 with filesystem/console, digest-only, and structuredClone adapters. The native cryptographic digest in hosted output was diagnostic-stubbed, *not* authenticated. The newly published, separately executable Node.js driver pins both genuine Git blob SHAs and invokes the unchanged checker via genuine OS Node subprocess for each packet, but **that new driver has not been independently executed as an OS process in this run**. Original checker acceptance is therefore a hosted-original-body result, not a claim of native OS replay. Raw results distinguish these two paths.

Code: experiments/arc/lspv3_572_386_fixed_source_cycle_space.cjs

Original-checker hosted raw: results/raw/arc/2026-11-11_0824_LSPV3_572_CYCLE_SPACE_HOSTED_V8_RAW.json

Exact accepted packet: results/raw/arc/2026-11-11_0824_LSPV3_572_FIXED_SOURCE_CYCLE11_ACCEPTED_PACKET.json

The independent OS driver, if run with --write-raw on a checkout, additionally writes results/raw/arc/2026-11-11_0824_LSPV3_572_CYCLE_SPACE_NATIVE_OS_RAW.json. No such OS output file is claimed to exist in this run.

## CEGAR interpretation, metrics and required handoff

A proposed coarse abstraction that admits an arbitrary independent original-edge sign flip as a fixed-source symmetry falsely declares 56 of 64 K4 packets valid. Each is an **abstractly spurious path** because the authoritative checker rejects it on SOURCE provenance. Refine by retaining the componentwise boundary syndrome Bf. The proof of soundness is exactly the kernel characterization above. Conversely all eight accepted cycle flips are real legal source-preserving paths and cannot be discarded merely to strengthen a prospective lower-bound invariant. This CEGAR result applies **only** to this native /386 fragment. It neither licenses a mixed-rule transition nor bounds arbitrary SAT proof search.

Resources remain separate: logical work W=53; the concrete mask-11 accepted file is 4,440 UTF-8 bytes; 4,663 original assertion groups per accepted CLI check. Ideal span, physical elapsed time, peak workspace, proof acquisition/discovery, source/index acquisition and total machine cost are not measured, and none is inferred from W. Shared subproof nodes and DEF owners are each charged once, no hidden branching/search overhead is attached to the free ideal minimum.

## CORPUS REVIEWED / duplication and contradiction audit / root-MAIN delta

**Adopted:** Original code, pinned seed, source-signed/provenance validation, exact owner-paid and RES-fixed tariffs, LSPV-3/565 charge-gauge algebra, LSPV-3/570 edge renaming, LSPV-3/571 source-fixed graph automorphism, LSPV-2/549 two-checker noncomposition and LSPV-1/573 SAT-side polyglot warning.

**New compared with /565 /571:** the full **fixed-original-source, fixed-source-provenance** edge-sign stabilizer is the cycle space ker B, with exact iff characterization and 64/64 original-checker differential including all nested paid gate owners. Vertex automorphisms can move SOURCE vertex tags; these cycle flips leave tags and source graph unchanged. The /565 gauge normally changes charges/source; here it is restricted to the nontrivial kernel and the iff boundary is authenticated.

**Rejected or retired:** treating any noncycle edge flip as a free source automorphism; using /341 and /386 as one mixed checker; or charging repeated paid-owner reference twice. No prior valid theorem was retired. The existing root MAIN contains older restricted transformations and no verified complete historical mixed grammar. This adds a specialized exact-cost quotient without closing or silently strengthening P2-D1/C3/B1.

**Publication / manuscript exception:** root main.tex's current Git blob can be read via fetch_blob (about 2.0 million UTF-8 characters), but the direct fetch_file path including ranged requests has returned empty content. Safe update is permitted **only inside the LSPV-3 OWNED region, using current SHA and full readback**; if such a write fails, do not overwrite the manuscript. Root trackers require **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No completed P=NP or P!=NP chain arrow has changed status.

**Next P2-D1 task:** locate a true single **historically source-bound** native checker executing actual RES-parent -> AND3 or paid DEF/facet -> LOCAL-CONVERT/GF(2) and then subject its exact bytes to typed-source, global-freshness, assumption/context and cost-sound CEGAR tests. Keep P2-D1, P2-C3, P2-B1 and P2-B2/B3 separately OPEN. All five existing agents, titles, schedules, historic weights, ownership boundaries and TWO Route A / THREE Route B assignments remain unchanged. **P versus NP OPEN.**
