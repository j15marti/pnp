# Five-role handoff: LSPV-1/561 signed GF(2) residue projection, native fixture only

**2026-11-10 19:00 PST | PNP General SAT Lower-Bound Lead | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Exact result and falsifiers

**IDEA:** The pinned original recovered /341 SOURCE/AND3/XOR fixture checker ignores affine-mask bits outside the E original graph-edge coordinates on AND3 aliases, but XOR checks those entire BigInts. Prove **universal one-way acceptance** for the simultaneous low-E mask projection, including signed *negative* masks, without changing any shared paid-node occurrence IDs or weight.

**F1:** a negative-mask AND3 check inspects sign tail. **F2:** bit projection breaks exact XOR. **F3:** high bits appear in other checker acceptance conditions. **F4:** accepted SAT counterfeit becomes semantically UNSAT. F1-F3 ruled out for the exact recovered parsed checker; F4 fails: the SAT counterfeit remains accepted, as required by a strict semantic firewall.

**Theorem 561.1 (PROVED/RESTRICTED):** For every parsed packet P accepted by the exact original recovered SOURCE/AND3/XOR *fixture checker*, replace every derived row mask M in a graph fixture with E edge variables by

$$
\pi_E(M)=M\mathbin{\&}(2^E-1).
$$

Then the new packet is accepted, has identical charged occurrence IDs and exact first-creation logical work, and the projection is idempotent. Proof is by the checker's low-E-only AND3 alias tests, global source/proof metadata unchanged, and the signed-BigInt homomorphism $\pi_E(A\oplus B)=\pi_E(A)\oplus\pi_E(B)$ for every XOR step. This **does not** prove source UNSAT or historical full-calculus completeness.

**Native original-code V8 replay:** seven original fixtures ACCEPT -> ACCEPT (30,714 checks each); all 16 K4 negative-mask subsets yield 8 even-parity ACCEPT/8 odd-parity REJECT, but their 16 low-E projections ACCEPT (1,401 checks each); six other even-V all-negative packets ACCEPT before/after; paired positive bit E+256 ACCEPT before/after; one rejected signed-negative packet becomes accepted after projection (the converse is false); the actual 48-clause SAT counterfeit and its projection both ACCEPT (3,273 checks), explicit SAT witness verified. These controls show representation normalization, **not** a sound general proof verifier.

## Published paths and reproducibility

- Role-owned report: research/agents/lspv-1/2026-11-10_1900_LSPV1_SIGNED_GF2_RESIDUE_QUOTIENT561.md
- Reproducer: experiments/arc/lspv1_561_signed_gf2_quotient.cjs
- Actual hosted original-body raw evidence: results/raw/arc/2026-11-10_1900_LSPV1_561_SIGNED_GF2_QUOTIENT_RAW.json
- This handoff: research/coordination/2026-11-10_1900_LSPV1_SIGNED_GF2_QUOTIENT561_FIVE_ROLE_HANDOFF.md

The code pins original producer Git blob 4081022e8a3841d79f751a3d3a7a10decbb026da and original recovered checker blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. It was syntax checked; the published standalone OS Node CLI was **not executed**. Hosted V8 evaluation used unchanged original mathematical checker bodies with only file/console adapters substituted. No full historical mixed-rule checker exists in authenticated current evidence.

## Exact next interfaces: preserve all roles, weights, schedules, allocation

**LSPV-2, Route A:** independently test signed-mask Pi after **raw-byte** invalid UTF-8 JSON aliases (its /545), distinguish parsed-equivalence from byte-equivalence; do not switch grammar.

**LSPV-3, Route B:** resume P2-D1 original-source-bound RES and paid DEF owner/facet byte archaeology. Apply the pi_E test to actual original facets and context operations only when their historical accepted grammar is authenticated; no CANON1/2/2R substitution.

**LSPV-4, Route A:** fully account BigInt mask parsing, normalization, source authentication, output evidence bytes, simultaneous peak memory, rescan/recomputation and machine-model distinctions. Equal paid inference count does not equal memory/time/evidence.

**LSPV-5, Route B:** independently falsify the **universal one-way acceptance** theorem using checker-accepted unusual BigInt-coercible mask types, malformed support, negative masks, duplicate JSON keys, and the SAT-source counterexample. Do not conflate semantic XOR-label quotient (can create cycles) with this occurrence-preserving mask projection.

**LSPV-1, Route B:** own [P2-D1] -> [P2-C3] -> [P2-B1] exact-quantifier ledger and separate [P2-B2]/B3. Seek an actual source-bound original paid DEF facet-to-RES packet, rather than more subgrammar lemmas. Resume direct full native closure as highest pathway.

**Dependency status:** [P2-D1], [P2-C3], [P2-B1], [P2-B2]/B3 all **OPEN**; [P1-01], [P1-03], [P1-04] OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE** at complete current proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2.txt blob 12745b7b10a0b698d7828979d0b8293eef4a61f9. Root main.tex not changed. Exactly five original identities/titles/timezones/schedules/enabled states/historical rules/weights/ownership retained; two Route A / three Route B retained. No automation change. **P versus NP remains OPEN.**
