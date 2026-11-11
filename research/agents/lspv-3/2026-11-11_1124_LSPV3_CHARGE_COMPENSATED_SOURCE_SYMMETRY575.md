# LSPV-3/575: Source-fixed charge-compensated graph automorphisms in the original archived /386 checker

**2026-11-11 11:24 PST | Hypergraph & Proof Certificates | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate and falsifiers stated before investigation

**Candidate [P2-D1 -> P2-C3]:** Source-preserving symmetries of a cubic signed Tseitin proof are not limited to independently charge-stabilizing vertex automorphisms and cycle-space edge sign flips. A charge-changing graph automorphism can become legal when an edge flip compensates the moved charge. A complete source-preserving shared-DAG transformation may therefore be larger than the two previously authenticated orbits LSPV-3/571 and /574.

F1: A graph automorphism moving the charged vertex cannot have any bit-flip solution that preserves the original signed SOURCE multiset. F2: the unchanged archived original /386 checker rejects an otherwise correct jointly transformed proof despite source bijection. F3: the transformation loses source identities, chronological parent typing, paid owner identities, free defining facets, or exact fixed count-once W. F4: the claimed combined transformations fail closure under composition or the original checker accepts hostile incorrect parent/pivot/source/freshness/payment mutations. All four falsifiers failed on the K4 test. They remain important controls for generalization to any unlocated full mixed dispatcher.

## Theorem 575.1: exact charged-source signed-automorphism lift

Let G=(V,E) be a **connected simple cubic graph** with edge-variable identifiers, incidence matrix B over GF(2), and fixed odd binary vertex charge b. Let sigma be **any** graph automorphism, not necessarily fixing b. For each original edge e, let its literal be transformed by a signed permutation to the sigma(e) edge variable, complemented iff f_e=1.

This substitution preserves the entire signed original 4-clause parity-CNF packet at every original source vertex, up to source-vertex relocation, if and only if

$$
 (Bf)_v = b_v \oplus b_{\sigma(v)}\quad\text{for all }v.
$$

For every sigma the right-hand side has even total parity, hence lies in im(B). There are exactly 2^{|E|-|V|+1} such masks f. The full group H_b of source-fixed signed graph automorphisms fits into an exact extension

$$
 1\longrightarrow \ker B\longrightarrow H_b\longrightarrow \mathrm{Aut}(G)\longrightarrow 1,
 \qquad |H_b|=|\mathrm{Aut}(G)|2^{|E|-|V|+1}.
$$

This statement concerns signed substitution symmetries, **not** the historical verifier's full accepted-byte grammar. For graphs with multiple components, lifting additionally requires the automorphism preserve their total charge parities; the connected case needs no extra condition.

**Proof.** Under the signed substitution, an original vertex equation with right side b_v becomes an equation at sigma(v) with right side b_v xor (Bf)_v. Equality with the fixed target source requires the displayed condition, and this is sufficient because the four forbidden local signed clauses encode exactly that affine equation. The even-parity criterion is necessary and sufficient for membership in im(B) on a connected graph. Rank(B)=|V|-1 gives the number of lifts. For successive actions (sigma,f) then (tau,g), their signed edge maps compose as (tau∘sigma,h), h_e=f_e xor g_{sigma(e)}, proving closure and inverses. QED.

## Corollary 575.2: exact count-once shared-DAG transform in authenticated /386 fragment

Let P be any parsed accepted original /386 mathematical-core SOURCE/paid-AND2/free-DEF-facet/strict-RES proof, with every original SOURCE occurrence. Normalize all SOURCE nodes before derived nodes if needed (existing LSPV-3/574 result). Preserve the original SOURCE record objects in their relative order. For every (sigma,f) in H_b, transform non-SOURCE signed clauses and pivots, paid definition inputs, and redirect each SOURCE-parent edge to the unique fixed SOURCE occurrence obtained by transforming that antecedent and its vertex provenance. All derived-to-derived parent edges and globally paid owner identities remain unchanged. Every RES resolvent, true DEF facet, freshness check, original SOURCE-completeness check and terminal empty sink remain valid, and

$$
 W_{386}(T_{\sigma,f}(P))=W_{386}(P)=N_{\mathrm{RES}}+N_{\mathrm{paid\ DEF}}.
$$

The complete /386 command-line wrapper has additional synthetic corruption-test constraints; the native K4 experiments below satisfy them, but the corollary is stated universally only for the mathematical core. Full historical R_mix341 cost-sound online alpha/gamma for AND3, GF(2), LOCAL-CONVERT, branching, discharge, exported/private wires, weakening, joins, deletion and learning remains OPEN.

## Authoritative-checker accepted-byte witness and CEGAR

Pinned unchanged original archived /386 checker Git blob `338305c0ce101704205e57543756b8127074a986` and source-authenticated seed blob `08aa169b5db49b2ddd1cb5a9b6890fcc3b790916`. The genuine original checker body was replayed in hosted V8, with only Node I/O and the **printed** SHA diagnostic adapted. All 192 permutations of the K4 proof (24 vertex automorphisms times 8 compensated masks each) were ACCEPTED with **4,663 assertions each** and the original eleven built-in negative controls. All 192 full accepted packets are distinct, preserve the 17 signed SOURCE records *object for object and ordinal for ordinal*, preserve two paid owner identities, 6 free facets, 51 paid RES nodes, all 74 proof records, and W=53.

Of the 192 accepted transformations, **144 move the charged vertex** and require a compensating non-cycle mask. The simplest witness is sigma=[1,0,2,3], f=1 (complement edge #1 while swapping vertices 0 and 1). It changes no original SOURCE records and remains accepted by the original checker. A proposed abstraction restricted to Aut(G,b) x ker B has only 6 x 8 = 48 members and would silently omit these 144 genuine legal source-fixed transformations. CEGAR must retain these paths. The paired source transformation is not interchangeable with a naked charge-moving permutation.

All **36,864 ordered group-pair composition parameter tests** stayed in the admissible set; these are independent algebraic checks, not 36,864 original-checker invocations. Six hostile accepted-byte mutations were rejected by the original checker: incorrect pivot, forged SOURCE, future parent, underpayment, fake AND3 opcode and colliding paid wire. The valid 192 and hostile six are exhaustive within the specified 24 x 64 K4 signed-permutation search, not an exhaustive search of arbitrary proofs. The published standalone Node.js OS subprocess reproducer is syntax-checked, **not executed as an OS program in this run**. The raw hosted-V8 diagnostic SHA is a placeholder, not a real certificate hash.

## Source binding, corpus and duplication audit

**CORPUS REVIEWED:** Both root proof trackers (proof1 blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; proof2 startup blob d5f13bbd71f28d4a7e1e73d2d588f28f4b58427d), current issue #3, AGENTS.md, CODEX.md, the pnp-research skill, original /341 checker blob fcb7d4ced8f922de14c0bd a16263a8cc7853e8e0 (without space), the original /386 checker, the original /341 /341 producer, actual LSPV-2/539 and /549 sibling-checker noncomposition report, LSPV-3/565–574, LSPV-1/577–578, LSPV-2/561–562, LSPV-4/547, LSPV-5/492, original Grok research and Claude world-ledger materials. External primary sources are Cook and Reckhow, JSL 44 (1979) 36–50, DOI 10.2307/2273702; Cousot and Cousot, POPL 1977, DOI 10.1145/512950.512973; Clarke et al., CAV 2000, DOI 10.1007/10722167_15. These are analogues and methodology, not authority for R_mix341 bytes.

**DUPLICATION / CONTRADICTION AUDIT:** LSPV-3/565 handled charge changes requiring source rewrite; /570 edge renaming; /571 only b-stabilizing graph automorphisms; /572–574 cycle-space transformations fixing source and resolving arbitrary SOURCE chronology. Their existing proofs are adopted. **New:** the admissible mixed charge-compensated signed automorphism group is 192, quadrupling the previously tested 48 subgroup, with 144 authentic new cross-charge source-fixed certificates and a group-composition audit. The exact historical R_mix341 single mixed-rule checker remains absent; sibling /341 and /386 checkers do not compose. No arbitrary-algorithm, native all-rule W lower bound or SAT decision-time consequence is claimed.

**WHAT CHANGED RELATIVE TO ROOT MAIN:** a stronger, cost-exact, source-fixed *completed-certificate* orbit for a restricted original checker. It is not an online cost-lower-bound transformer. **ADOPTED:** /571 and /574 source-first reattachment and count-once W; **REJECTED:** treating source-fixed symmetries as Aut(G,b) times ker B only; **RETIRED:** no existing theorem, no material tracker status change.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Exact affected OPEN IDs P2-D1 -> P2-C3 -> P2-B1; P2-B2/B3 kept separate. P1-01/03/04 OPEN. Ideal free optimal proof selection, complete DAG reconvergence and assumption-aware lemma reuse are unaffected. W, evidence bits, acquisition/runtime, span and peak memory remain separate.

## Sources and next falsifier

1. [Cook and Reckhow 1979](https://doi.org/10.2307/2273702), propositional proof-system cost model, no historical parser.
2. [Cousot and Cousot 1977](https://doi.org/10.1145/512950.512973), abstract transition soundness, no native step costs.
3. [Clarke et al. 2000](https://doi.org/10.1007/10722167_15), CEGAR and spurious-path refinement, no proof system lower bound.
4. [Original /386 verifier](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_386_independent_verify.js); [distinct original /341 checker](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_341_independent_verify.js).

**Next:** LSPV-2 byte-interface audit and LSPV-5 adversarial OS replay of this 192-case corpus; LSPV-4 separate cost/source ledger; LSPV-1 theorem quantifiers. The top target is still an *original single-dispatcher R_mix341* accepted packet with RES->AND3 or DEF-facet->LOCAL-CONVERT/GF(2), an independent original-source hash, original fixed weights, all branch scopes and wire interfaces. P2-D1, P2-C3, P2-B1 and separate B2/B3 OPEN. **P versus NP remains OPEN.**
