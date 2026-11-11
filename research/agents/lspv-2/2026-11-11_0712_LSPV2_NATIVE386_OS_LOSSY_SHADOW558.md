# LSPV-2/558: Original /386 full-CLI lossy UTF-8 SOURCE shadows

**2026-11-11 07:12 PST | SAT-Circuit Reduction Builder | historical Route A retained | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## Candidate and four falsifiers

Candidate: The unchanged historical archived /386 original checker will accept two *distinct malformed UTF-8 byte strings* with the same decoded terminal-live signed SOURCE/DEF/Resolution proof when the first SOURCE clause property c contains a malformed string and the last c gives the authentic source clause. Verify using **complete original OS Node subprocesses**, including eleven built-in hostile controls, not a replacement checker.

F1: Node JSON.parse(Buffer) rejects invalid UTF-8. F2: duplicate keys are rejected or use first-wins. F3: original source, paid owner, Resolution or full-CLI mutation tests reject the repaired parsed proof. F4: reversing the duplicate values or damaging the winning opcode still accepts. Original executions falsified F1-F3 and rejected all four F4 corruptions.

## Authority, prior work, and boundary

Original archived checker, Git blob **338305c0ce101704205e57543756b8127074a986**, path experiments/arc/lspv2_386_independent_verify.js. Original accepted terminal-live guarded odd-K4 certificate, Git blob **aeeb555c4dcf7f510a9a501c8afc609b629a9298**, path results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json. Both Git blobs are verified by the new executable before tests. The seed contains 17 signed SOURCE records, three separately paid AND2 owners, four free DEF facets, 30 paid Resolution records, 51 records overall, W=33.

Novelty is limited: LSPV-2/540 already exposed duplicate keys in the /341 fixture checker; /545 exposed invalid UTF-8 in that distinct /341 SOURCE identity system; /557 exposed ASCII duplicate key shadowing in the /386 mathematical checker core. /558 combines ill-formed-UTF8, winning signed SOURCE c shadow and **complete unchanged original /386 OS CLI validation**, not just a hosted mathematical function. No novelty is claimed for JavaScript replacement decoding.

## Theorem 558.1: Original /386 full-CLI decoded-object equivalence (restricted)

Let D be Node Buffer UTF-8 replacement decoding, J the original JSON.parse, and C386 the unchanged one-input original CLI including its eleven cloned-corruption checks. Whenever J(D(b)) and J(D(b')) produce identical parsed proof objects, the original CLI's accept/reject outcomes and, on acceptance, logical charges coincide:

$$
J(D(b))=J(D(b'))\ \Longrightarrow\
C_{386}(b)=C_{386}(b'),\quad W_{386}(b)=W_{386}(b').
$$

Proof: Inspect the exact original program. After JSON.parse(Buffer), the original checkProof and the eleven structuredClone corruptions read only the parsed object. The original filename and SHA-256 are printed after verification but do not feed into acceptance. Equal parsed objects thus undergo identical source, gate, facet, signed pivot, chronological dependency and summary tests. This is a program-specific accepted-byte theorem, not an assertion of historical mixed R_mix341 completeness or cost equality for reading/decoding/certificate bits/construction/span/peak space.

From the 3,213-byte authentic certificate, replace the first active SOURCE clause property with a string holding the single raw byte 0x80 or 0x81, followed by a second same-decoded-name c containing the original signed clause [1,2,3,-7]. Both replacement-mode decodings map the invalid octet to U+FFFD. The two **3,221-byte packets** therefore differ as bytes but have exactly the same parsed proof. Both were accepted by the original full CLI at W=33, while strict TextDecoder('utf-8',{fatal:true}) rejects both. This is a concrete counterexample to any reference parser that unconditionally excludes non-strict UTF-8 from its exact accepted-byte domain. Reversing the duplicate or corrupting the winning SOURCE operation rejects.

## Computational evidence

Real operating-system Node v22.16.0 subprocesses invoked the **unchanged original checker** for 19 byte-exact packets: **11 accepted, 8 rejected, 19/19 expected**. Successful executions each completed 3,509 original checker assertions, totaling **38,599 assertions** and **121 original bundled corrupted-certificate checks**. All accepted packets have 17 authentic source records, three paid gate owners, 30 strict Resolution steps, 51 total records and W=33. Odd K4 parity is UNSAT (zero odd-charge models) with eight even-charge control models.

Positive cases include baseline, bad-first/good-last SOURCE/DEF/pivot duplicates, Unicode escaped active SOURCE/DEF/RES opcodes, SOURCE clause property and terminal pivot property, and two byte-distinct malformed-UTF8 SOURCE shadows. Negative cases include wrong-last SOURCE/DEF/pivot, malformed SOURCE opcode, two wrong-last invalid UTF-8 variants and two malformed winning SOURCE opcodes.

Executable: experiments/arc/lspv2_558_native386_os_utf8_shadow.cjs. Full hexadecimal 19-packet corpus: results/raw/arc/2026-11-11_0712_LSPV2_558_ACCEPTED_BYTE_CORPUS.json. OS decision/SHA-256 manifest: results/raw/arc/2026-11-11_0712_LSPV2_558_NATIVE_OS_RESULTS.json.

Accepted invalid-byte SHA-256:
- 0x80: 5e9bcaed9cbfd2d5eed861644f22c3bf3566fc2506e6f1e23af182e9d7103ae4
- 0x81: ca5ff619066d9995e70e2667cc5d4c91d576baa9be5addef4a3a2d03d87737cf

Both have parsed-object SHA-256 f9aaafae511397762b655acf9d4c0c6595414733f36f3e225d2d20da560fc7dd. Distinguish native *logical* W from certificate-byte size and original CLI parsing work.

## Preflight and literature

Read both root proof trackers (proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; proof2.txt blob 7db80e8b55a7f5c348fbb2ed8decd3ceaa2657f3), issue #3 and latest peer comments, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, latest five-role handoffs, actual relevant LSPV-2/539-557 reports, LSPV-1/570-571, LSPV-4/543 and LSPV-5/488R1. Searched source-authenticated historical checker files and external SAT certificate interfaces for the complete mixed dispatcher; not found.

Primary references: Cook-Reckhow (1979), DOI [10.2307/2273702](https://doi.org/10.2307/2273702); Cousot-Cousot (1977), DOI [10.1145/512950.512973](https://doi.org/10.1145/512950.512973); Clarke et al. (CAV 2000), DOI [10.1007/10722167_15](https://doi.org/10.1007/10722167_15); Baek-Carneiro-Heule FRAT (2021), [arXiv:2109.09665](https://arxiv.org/abs/2109.09665); original [drat-trim](https://github.com/marijnheule/drat-trim). None authenticates the lost mixed-calculus syntax or transfers a restricted proof bound to general SAT computation.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1 full grammar, P2-C3 full alpha/gamma, P2-B1 superpolynomial all-rule lower bound and separate B2/B3 SAT bridge remain OPEN. P1-01/P1-03/P1-04 remain OPEN. The five existing agents, original weights, identities, Pacific Time schedules, ownership boundaries, TWO Route A/THREE Route B assignments remain unchanged. The /386 original sibling checker is not misidentified as the lost full R_mix341 authority.

Next target: authenticate a genuine single-checker cross-rule RES-to-AND3 or DEF-to-LOCAL-CONVERT port, with a positive original accepted-byte packet and corrupted-port rejects. P versus NP remains OPEN.
