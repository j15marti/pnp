# LSPV-2/547: Source-bound minimal mixed RES/AND3/XOR reference certificate

**November 10, 2026, 20:12 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## IDEA, falsifiers and exact boundary

Construct a seven-paid-inference proof on a fixed independently authenticated signed proper 3-CNF using four Resolution inferences, two truth-table AND3 inferences accepting RES-derived clause parents, and one XOR inference. Provide a replayable reference accepted-byte corpus and do not mistake it for a native historical R_mix341 certificate. Registered falsifiers: F1 incorrect pivot or resolvent; F2 false AND3 factor or GF(2) alias; F3 tampered independent source, dependencies, hashes or paid identities; F4 alternative TAGGED parent rule or unimplemented historical operation erroneously rejected rather than recorded MAY.

**Historical authority:** The original declaration is LSPV-2/341, file research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. Original producer blob 4081022e8a3841d79f751a3d3a7a10decbb026da and checker blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. This recovered checker processes only SOURCE/AND3/XOR fixtures and has no RES dispatcher. Consequently the new REF547 grammar is **NOT the authoritative native grammar**. The historical RES-to-AND3 parent type and byte spelling remain unidentified.

## Theorem 547.1, PROVED/RESTRICTED: a mixed seven-node optimum under the separate EXTENSIONAL grammar

Fix the distinct reference grammar admitting exact binary complementary-pivot Resolution, exact AND3 of two earlier Boolean conditions with combined support at most three original variables, and exact binary GF(2) addition of authenticated rows; RES-derived clauses count as conditions. Every new derived identity has logical weight one, and source occurrences cost zero.

The external source is the signed full cube over x1,x2,x3, consisting of the eight distinct clauses from all sign patterns in lexical order (+,+,+), (+,+,-), (+,-,+), (+,-,-), (-,+,+), (-,+,-), (-,-,+), (-,-,-). The exact full DIMACS text is present in the raw ledger. Its byte length is **86** and SHA-256 is **a2f85326956ed24023d756dc4b0c205657cec886e8cf405083437b2b820cb719**.

Using source IDs s0,...,s7 in that order, construct these exact steps:

1. d0 = RES(s0,s1,3) = (x1 OR x2).
2. d1 = RES(s2,s3,3) = (x1 OR NOT x2).
3. d2 = AND3(d0,d1) = factor x1, affine row mask 1, RHS 1.
4. d3 = RES(s4,s5,3) = (NOT x1 OR x2).
5. d4 = RES(s6,s7,3) = (NOT x1 OR NOT x2).
6. d5 = AND3(d3,d4) = factor NOT x1, affine row mask 1, RHS 0.
7. d6 = XOR(d2,d5) = 0=1.

The two AND3 support sets are {1,2}; exact 4-entry local truth tables, with variable 1 as the least-significant bit, are integers 10 and 5. The contradiction has **7 distinct paid nodes**, 4 RES + 2 AND3 + 1 XOR, logical critical span 3, and an **863-ASCII-byte** reference JSON packet. All eight source occurrences are ancestors of the final sink.

Each of the eight original assignments falsifies exactly one clause. The source is UNSAT and every individual source is essential, since deleting it makes its uniquely excluded assignment satisfying. By the existing project source/arity argument (LSPV-1/469, LSPV-4/524), for m=8 essential free source roots and q distinct paid nodes with indegree at most two, connected sink ancestry requires at least m+q-1 edge incidences but provides at most 2q, hence q>=m-1=7. This example attains the bound **within the stated sound grammar**. It is neither a new general proof-complexity lower bound nor a universal SAT algorithm lower bound. It does not apply if free multi-parent rules or source-independent axioms are admitted.

**Novelty audit:** LSPV-3/556 already used this exact eight-clause input and proved a seven-RES proof; LSPV-3/434 previously gave a different 13-node semantic RES-to-AND3/XOR refutation; LSPV-5/412 already proved competing EXTENSIONAL/TAGGED parent grammars agree on native fixtures. This run adds the *specific seven-node heterogeneous RES/AND3/XOR positive control and differential byte-exact replayer*. No claimed novelty for the shared binary-arity lemma, source family or grammar ambiguity.

## Concrete/abstract resource polarity

The restricted reference concrete configuration includes externally pinned source bytes and digest, current packet bytes, parser position, typed clauses/factors/affine rows, full ordered shared dependency map, distinct paid-ID first-creation set, empty active context and owner/wire maps, charged logical cost and terminal status. The reference alpha retains exact typed source identities, provenance, first-creation paid identities and parent edges while forgetting only permitted untrusted lexical representation. Gamma consists of exact concrete encodings conforming to that typed projection. Every verified RES, AND3 or XOR transition maps to its exact typed abstract successor at the same unit logical charge. A shared parent lookup does not charge its prior node again. Checked 0=1 sinks remain represented.

This correspondence holds **only for the explicitly written reference grammar**. For historical unknown DEF, defining facets, LOCAL-CONVERT, fresh/exported/private wires, branching, assumptions, weakening, discharge, joins and deletions, the conservative abstract effect is a TOP/MAY successor with logical cost floor zero. These paths can conceal valid shortcuts, so P2-C3 and all full-calculus nonreachability/lower-bound obligations remain OPEN. The unknown transitions are not silently declared illegal. No physical memory lower bound is inferred from logical node count or certificate bytes.

## ITERATE: test and CEGAR ledger

Published runnable code: experiments/arc/lspv2_547_mixed_cube_reference_replayer.cjs.
Raw 20-case, exact serialized-JSON corpus: results/raw/arc/2026-11-10_2012_LSPV2_547_MIXED_CUBE_REFERENCE_RAW.json.

The available V8 runtime passed **20 controls**: one exact mixed positive, ten hostile rejections (bad RES pivot/conclusion, bad AND3 table, false affine annotation, bad XOR sink, source substitution, SHA substitution, duplicate paid identity, missing parent, missing source occurrence), one TAGGED parent-policy MAY and eight unavailable native-opcode MAY states. Independently executed Python Boolean enumeration checked all eight complete assignments, all eight deletion witnesses, 32 RES, 16 AND3 and eight XOR assignment evaluations. The Python control file is supplied separately as a reproducibility artifact.

An intentionally corrupted first resolvent was permitted by a coarse unverified-semantic MAY abstraction with projected cost floor zero. Typed concrete replay rejects it. CEGAR refinement adds exact signed pivot and resolvent equality and removes that spurious path while retaining the genuine seven-step certificate. This is local refinement for the separate reference grammar, not a full historical CEGAR proof. Under the separately proposed TAGGED semantics the first RES-to-AND3 step remains MAY rather than an authenticated rejection.

Source bytes, certificate bits, proof acquisition time, verification/construction time, ideal critical span and peak simultaneously live work storage are **separate resources**. No OS Node execution of the original mixed checker occurred because it is unavailable; no native mixed accepted-byte result is claimed. V8 generated the exact packet ledger and tested the separate reference algorithm.

## Primary literature and independent source survey

Cook and Reckhow, Journal of Symbolic Logic 44 (1979), 36-50, DOI https://doi.org/10.2307/2273702 ; Cousot and Cousot, POPL 1977, DOI https://doi.org/10.1145/512950.512973 ; D'Silva, Haller and Kroening, Abstract Conflict Driven Learning, POPL 2013, DOI https://doi.org/10.1145/2429069.2429087 . These motivate exact proof-language semantics and sound overapproximation but do not specify R_mix341. Inspected source repositories: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f. None authenticates the absent dispatcher.

Governing files reviewed: full proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; full proof2.txt blob 75f5fb4e9ee8c74d7f6d5f6d0a62b756c6f1aca5; issue #3 with 1,603 comments; AGENTS.md, CODEX.md, pnp-research skill, November 9 and November 10 five-role handoffs, relevant LSPV reports 539-549/peers/559/562 and later source/space controls. No P1-01/P1-03/P1-04 or P2-D1/P2-C3/P2-B1/P2-B2/B3 theorem status changed.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Historical weights, roles, ownership boundaries, 2 Route A/3 Route B labels, enabled states and schedules are unchanged. P versus NP OPEN.

**Next essential evidence:** Obtain an actual historical full-rule checker and an accepted source-bound RES-to-AND3 byte packet, or preserve the grammar as unknown. Do not elevate the reference packet to historical authority.
