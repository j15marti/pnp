# LSPV-3/573: Source-slot-fixed cycle action in the original /386 checker

**2026-11-11 09:24 PST | LSPV-3 Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED theorem + COMPUTATIONAL original-body hosted-V8 replay | P versus NP OPEN.**

## IDEA: candidate and four falsifiers

Candidate [P2-D1 -> P2-C3]: LSPV-3/572 established a cycle-space sign flip preserving the provenance-tagged signed original SOURCE *multiset* in the archived /386 checker, but it changed individual SOURCE records at their original positions. For a complete SOURCE-prefix certificate, simultaneously permute every reference into that prefix according to which original signed SOURCE clause the flip produces. This should preserve **each individual original signed SOURCE record in its original slot**, including its source tag and exact serialized fields, while retaining legitimate transformed nested DEF and strict Resolution inferences at unchanged logical cost.

Four falsifiers:
1. F1: a cycle mask has no within-vertex signed SOURCE-slot bijection;
2. F2: the full unchanged /386 checker rejects a remapped native RES or DEF step;
3. F3: any remapped accepted packet changes an ordered original SOURCE record or external frozen SOURCE-prefix fingerprint;
4. F4: the transformation introduces a forward parent, changes paid-owner identity or count-once work, or fails to compose as a group.

All four failed on the eight applicable original K4 masks. The other 56 noncycle masks have no compatible SOURCE-slot bijection in this construction, which is not a general impossibility of alternative proofs.

## Authority, corpus and primary references

The authority is the unchanged historical archived /386 SOURCE/paid-DEF-facet/strict-RES checker at experiments/arc/lspv2_386_independent_verify.js, Git blob **338305c0ce101704205e57543756b8127074a986**. The authentic nested-owner K4 seed is results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json, Git blob **08aa169b5db49b2ddd1cb5a9b6890fcc3b790916**. The different original /341 fixture checker, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0, has no RES/DEF dispatcher and does not establish a combined R_mix341 parser.

Read both proof trackers, current issue #3, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, root MAIN owned region, related historical handoffs and real original source, LSPV-3/539 and /561-/572, LSPV-2/539-/549 and /552, LSPV-1/541 and /573, LSPV-4/538, LSPV-5/412 and /488R1, GROKPROOF/2026-11-11_0720_PROGRESS.md and the Claude world-ledger README. Targeted original-repository searches for a /386 SOURCE-slot cycle permutation with reference rewiring did not surface an earlier theorem. The established /565 source-changing gauge, /572 SOURCE-*multiset*-fixed orbit, and /541 globally fresh auxiliary naming bisimulation are adopted, not presented as novel.

Primary methodological sources: Cousot and Cousot, Abstract Interpretation, POPL 1977, DOI 10.1145/512950.512973; Clarke et al., Counterexample-Guided Abstraction Refinement, CAV 2000, DOI 10.1007/10722167_15; Cook and Reckhow, The Relative Efficiency of Propositional Proof Systems, JSL 1979, DOI 10.2307/2273702. The explicit clause/step namespaces in https://github.com/meelgroup/frat-xor/blob/main/format.md are useful comparison evidence, **not** a native R_mix341 specification. The new exact theorem relies on the recovered original checker body, not on a transferred external format.

## Theorem 573.1: exact fixed SOURCE-slot native action

Let P be any *parsed* packet accepted by the **mathematical core** of the pinned original /386 checker, with the additional precondition that all 4h+1 original SOURCE records form a chronological prefix of its records. Its source is a connected cubic graph G=(V,E), binary odd charge b, a fixed guard g, four distinct signed guarded SOURCE clauses for each vertex, plus the guard unit. Let B be the GF(2) vertex-edge incidence matrix and K=ker(B).

For any f in K, tau_f complements the sign of precisely the original edge literals e where f_e=1. It fixes all fresh DEF outputs, the guard, source labels, owner IDs and record IDs. Since Bf=0, each vertex's four forbidden source assignments are permuted amongst themselves. Thus for every original SOURCE ordinal i there exists one unique SOURCE ordinal s_f(i) of the same source vertex such that its clause is exactly tau_f(C_i). Set s_f of the guard row to itself.

Define U_f(P) as follows:

1. Copy **every SOURCE record at the exact old ordinal position**, unaltered, including signed literals, source tag and parents.
2. Complement original-edge signs in all later DEF and RES clauses, signed paid-definition inputs and RES pivots, canonicalizing clauses by the exact native comparator. Do not modify outputs or paid owner IDs.
3. In each later record, replace a parent reference i into the SOURCE prefix by s_f(i). Leave non-SOURCE parents unchanged.

Then the original /386 **mathematical checker** accepts U_f(P); all original SOURCE record objects are literally identical at each original ordinal, and the complete chronological shared proof DAG, globally paid owner set and exact count-once logical work are preserved:

\[
\forall i<4h+1:\ U_f(P).records[i]=P.records[i],\qquad
W_{386}(U_f(P))=W_{386}(P)=N_{\rm RES}+N_{\rm paid\ DEF}.
\]

Furthermore,

\[
U_f(U_g(P))=U_{f\oplus g}(P),\quad U_f^2(P)=P,\quad
|K|=2^{|E|-|V|+1}.
\]

The last cardinality uses connectedness. For f not in K, the local forbidden-parity class changes at some vertex, so the required provenance-preserving SOURCE-slot bijection does not exist under this construction.

**Proof.** The incidence kernel condition means that the number of complemented incident edges at every vertex is even. Hence the four forbidden local patterns, indexed by signed clauses and source vertex, are carried bijectively into the same four patterns. This constructs a within-vertex permutation s_f, whose compositions correspond to xor of masks. The original SOURCE prefix remains valid and unmodified. A later record originally depending on SOURCE i now references its genuine sign-transformed clause at s_f(i), still earlier than every non-SOURCE record by the prefix precondition. For every true defining DEF facet, complementing signed original inputs and their facet literals preserves the exact Boolean gate definition with the same output and paid owner. For every strict RES step, complementing both signed parent clauses and its complementary pivot produces exactly the correspondingly transformed resolvent. Topological induction through all derived records preserves all native legality tests, including reconvergence and repeated use of any paid ancestor. The terminal empty clause is unchanged. The record/owner sets are fixed, so W is unchanged; the group identities follow from signed-literal involution and source-permutation composition. QED.

**Qualification:** The original full CLI has synthetic negative tests and other nonextensional checks; the theorem is unconditional only for its mathematical checker, while the finite examples below were run through the complete original CLI. Source-prefix is a specific precondition, not a universal assertion about /386 accepted packets. Fixing an *external* original SOURCE ordinal fingerprint is a **new comparison firewall**, not a historical requirement proved for either recovered checker. Nothing here authenticates RES-to-AND3, LOCAL-CONVERT, GF(2) or assumption discharge inside full R_mix341.

## Theorem 573.2: exact-cost restricted source-retracting quotient

Take a concrete *post-SOURCE* /386 configuration carrying an immutable ordered original SOURCE prefix, all later typed clauses, full shared DAG edges, original source provenance, globally paid owner IDs, fresh wire definitions and cost. The group K acts through U_f on this **whole configuration**, never through independent branch canonicalization. Let alpha map a configuration to its K-orbit and gamma expand an abstract orbit back to its complete concrete members. Because actual derived DEF-facet and strict RES steps commute with U_f, their orbit transformer satisfies

\[
\operatorname{Post}(\gamma(A))=\gamma(\operatorname{Post}^{\#}(A)),
\qquad W^{\#}(\alpha(C))=W(C).
\]

Thus the quotient preserves refutation goal and ideal minimum cost exactly for this restricted post-SOURCE sublanguage, with paid subproofs and paid gate owners counted once. It neither adds discovery/search cost nor claims physical execution time. The action does not cover the entire historical calculus or raw JSON aliasing, context discharge, branching, exported/private ports, deletion, weakening, arbitrary source-order packets or externally source-hashed input semantics. Such transitions must be explicitly authenticated or MAY-overapproximated rather than excluded.

## Original-checker experiment and falsification

The source is K4 with h=4 and six edge variables, 17 original SOURCE records including guard, six free DEF facets, two globally paid nested definitions, 51 RES records, 74 total records and W=53.

| Verification | Observed |
|---|---|
| Edge masks scanned | 64 |
| Native SOURCE-slot bijections | 8 |
| Complete original /386 CLI accepts | **8/8** |
| Noncycle masks lacking the bijection | 56 |
| Exact SOURCE records unchanged | **17/17 for each accepted packet** |
| Group-pair composition controls | **64/64** |
| Original assertion groups per accepted packet | **4,663** |
| Built-in checker negative controls per accepted packet | 11 |
| Additional corrupted certificates rejected | **6/6** |

Accepted masks: 0, 11, 21, 30, 38, 45, 51 and 56. The genuine accepted mask-11 packet is **4,439 UTF-8 bytes** compared with the original 4,421 bytes, and twelve derived records have altered SOURCE-parent references. The increase of 18 bytes concerns evidence representation, **not** logical W.

The six originally rejected hostiles respectively altered a SOURCE-parent index, a signed RES pivot, a genuine signed DEF facet, paid summary, paid gate output freshness and an original SOURCE literal. A seventh adversarial case swapped two SOURCE record positions with all necessary parent pointers updated. The **original /386 checker ACCEPTED** it at W=53, while the stronger externally pinned ordered-SOURCE-slot firewall REJECTED it. This is the exact distinction between historical acceptance and proposed stronger source identity. The old /572 transformed packets are legal for original /386 but generally fail that stronger firewall; the current conjugated accepted packets pass it.

**Execution authority:** The complete unchanged original checker BODY was executed in hosted V8 on all eight positives, six negatives and one accepted source-slot-swap comparison, with filesystem, console, structuredClone and noncryptographic diagnostic-digest adapters. The new native-OS Node subprocess runner is published and syntax-parsed, but **not OS-executed in this run**. No hosted diagnostic digest is claimed to be SHA-256; the immutable Git blobs and full SOURCE object comparisons are the present provenance controls.

**Reproducible artifacts:**
- Reproducer: experiments/arc/lspv3_573_source_slot_fixed_cycle.cjs, Git blob 7788879f35576d5ffd3bf6317bc5d6b29deea5d9.
- Exact accepted 4,439-byte certificate: results/raw/arc/2026-11-11_0924_LSPV3_573_FIXED_SOURCE_SLOT_CYCLE11_PACKET.json, Git blob f15e8fced19f1b245e860101b6093e0da8124555.
- Complete 64-mask original-body ledger: results/raw/arc/2026-11-11_0924_LSPV3_573_SOURCE_SLOT_64_V8_RAW.json, Git blob 7836e0fce2ccd34c6c6d1bdbd3c0bf62572aa761.

Logical work W=53, evidence bytes 4,439, source/definition/RES count and original assertion groups are separate. Actual OS machine time, checker peak space, physical span and proof acquisition/discovery work are **not measured**. An ideal freely selected optimum incurs no extra discovery charge.

## Corpus reconciliation, proof obligations and next target

**CORPUS REVIEWED / DUPLICATION / CONTRADICTION / ROOT-MAIN DELTA:** Prior /572 fixed the SOURCE multiset but explicitly *did not* preserve the original signed clause at each position. The new result fixes the exact SOURCE record at every ordinal while changing downstream references through a mathematically required permutation. General alpha-normalization (/541) and separate parser fixes are preserved, not retired. It would overstate either theorem to call the entire historical R_mix341 native calculus authenticated. No prior valid result is withdrawn.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt Git blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2.txt blob d79f9fa101127412aeca2c807353e1d0dbfc262b were inspected. [P2-D1], [P2-C3], [P2-B1] and [P2-B2/B3] remain **OPEN**, as do [P1-01/03/04]. No P-versus-NP implication or unrestricted SAT lower bound is established.

**Next:** Locate an actual historical **single source-bound mixed-rule dispatcher** and genuine accepted RES-parent-to-AND3 or DEF-facet-to-LOCAL-CONVERT/GF(2) certificate, then test source ordinal identity, typed DAG ownership, global freshness and assumption-aware reuse under one consistent native parser. All five existing agent titles, identities, schedules, America/Los_Angeles timezone, historic weights, ownership regions and TWO Route A/THREE Route B labels are unchanged. No automations were created or edited. **P versus NP remains OPEN.**
