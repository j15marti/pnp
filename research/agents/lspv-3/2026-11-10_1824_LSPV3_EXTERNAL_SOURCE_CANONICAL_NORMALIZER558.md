# LSPV-3/558: Polynomial-size proof-independent canonical regeneration for guarded original-source cubic fixtures

**2026-11-10 18:24 PST | Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED constructive bound + COMPUTATIONAL original-code replays | P versus NP OPEN**

## IDEA -> SEARCH -> ITERATE: candidate and falsifiers

**Candidate tied to [P2-D1] -> [P2-C3].** Strengthen LSPV-1/560's already established guarded source-driven equality-of-paid-cost reconstruction by removing reliance on the *input packet's* derived proof, arbitrary identifier spellings, retained untrusted metadata, and original deletion-witness payload. Supply a separate immutable original DIMACS source, graph/incidence metadata and strictly numeric odd charges. Regenerate all original-source records, deletion witnesses, AND3 and XOR records from these authenticated inputs. Prove a polynomial bound on **the emitted full checker packet's evidence bytes** independently of the original packet length, while retaining the precise native 4V-1 **logical paid-node count**. This remains a separate restricted fixture operation, not the full five-rule calculus.

F1: an accepted packet's ill-typed proof supports or unbounded metadata are needed for canonical inference reconstruction. **FALSIFIED:** seven original fixtures were rebuilt after discarding the entire paid proof and adding 40,000 untrusted metadata bytes; each canonical packet was accepted by the pinned checker. F2: source replacement or string-number charges remain legal inputs to the guarded constructor. **FALSIFIED:** each of seven altered external sources and seven string-charge controls were rejected; the previously published accepted SAT-source forged packet LSPV-3/557 is rejected at G2. F3: a bridge graph defeats the deletion-witness reconstruction or essentiality count. **FALSIFIED in the bridge control:** an original bridge graph reconstructed with 36 essential of 40 clauses and accepted with 39 paid nodes. F4: physical packet size must scale with arbitrary untrusted original metadata. **FALSIFIED:** the builder emits only canonical graph, source, proof and independently recomputed witnesses, and its output-size theorem is independent of ignored input metadata.

## PRECEDENCE AND SOURCE REVIEW

The actual original mathematical declaration [4], Git blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`, defines free SOURCE and unit-paid RES, AND3, GF(2), LOCAL-CONVERT and conservative two-input DEF. The pinned recovered checker is only the original SOURCE/AND3/XOR specialized **fixture** checker `experiments/arc/lspv2_341_independent_verify.js`, blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. Its original producer is `experiments/arc/lspv2_341_mixed_tseitin_min_dag.js`, blob `4081022e8a3841d79f751a3d3a7a10decbb026da`. No authoritative accepted-byte implementation of full RES, LOCAL-CONVERT, paid DEF/facets or branching/discharge was found; this work does NOT invent such an implementation.

**Direct antecedent:** LSPV-1/560 [5] already proved equal-cost **source-driven** replacement for guarded parsed packets while retaining existing metadata and deletion-witness records. The present constructive improvement is to *regenerate and size-bound the entire resulting certificate*, including deletion witnesses, with a separately stored K4 external DIMACS file. It adds an independently reproducible source-bound and full-packet-sized result, NOT a new lower bound or a universal normalization theorem. The /557 SAT-source checker exploit and /545 malformed UTF-8 alias are retained as hostile controls, not imported as legal proof rules.

Primary literature: Cook–Reckhow [1] requires keeping proof length and polynomial validation separate from uncharged logical inference counts. Cousot–Cousot [2] supplies concrete/abstract sound simulation discipline. D'Silva–Haller–Kroening [3] concerns abstract satisfaction, not proof-cost lower bounds. Targeted original repository reviews of `konard/p-vs-np/scripts/proof_status.json` (blob `93b77ed3d8fe456f81c690035f45f07910a247f2`), `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` (blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`) and `meelgroup/frat-xor/format.md` (blob `986a21aa92b62f844ef1fce852193142c41b2b1f`) find other proof representations, not the missing historical R_mix341 mixed-rule byte grammar. Both root trackers, issue #3, AGENTS.md, CODEX.md, project skill, current role handoffs, LSPV-3/549–557, LSPV-1/559–560, LSPV-2/539–545 and LSPV-5/479–480 were reviewed.

## Theorem 558.1 (PROVED/RESTRICTED): proof-independent canonical full-packet regeneration

Let a separately supplied, immutable, proper signed original 3-CNF `F` contain exactly `4V` clauses, over the `E=3V/2` edge variables of a witnessed connected simple cubic graph `G`. Let every clause carry an authenticated vertex assignment and have exactly that vertex's three incident original edge variables, with the four distinct local forbidden patterns at vertex v being exactly the four parity assignments opposite a **numeric** charge `chi_v in {0,1}`. Assume `xor_v chi_v = 1`. These conditions are the source/graph/charge guards G0–G2 of LSPV-1/560, with an **independent literal-for-literal external DIMACS binding**.

There is a uniform deterministic algorithm `Canon(F,G,chi)` that does **not inspect any offered paid proof DAG**, labels its source records canonically by original source index, constructs:
 
* exactly three two-parent truth-table AND3 inferences for each vertex to conjoin its four source clauses;
* an exact in-range GF(2) row on each resulting vertex factor;
* exactly V-1 two-parent XOR inferences reducing all vertex rows to `0=1`;
* all `4V` source-deletion witnesses, using deterministic GF(2) elimination after pinning the three edges falsifying the deleted source clause (or `null` when no completion exists);
* a valid all-zero even-charge witness, a normalized graph record and fresh canonical paid IDs.

The resulting source-bound packet has exactly

$$
W(\mathrm{Canon})=3V+(V-1)=4V-1
$$

**distinct paid creations** and is accepted by the exact pinned original specialized checker. It proves the independently supplied F is UNSAT. Its *entire output*, including explicit deletion witnesses and every retained affine mask, has

$$
|\mathrm{enc}(\mathrm{Canon})|=O(V^2+V\log V)=O(V^2)
$$

bytes for canonical decimal index encodings, and is constructed in polynomial time and space in `V` and input bit length. In particular, if `N=|F|` is the independent input's binary length, `V=O(N)`, so the emitted certificate is `O(N^2)` bytes. The output bound has **no dependence on arbitrary source-irrelevant fields, long original IDs, malformed UTF-8 aliases or untrusted paid-proof bodies** of an offered checker-accepted packet. It is NOT a byte-preserving rewrite or a claim that the logical work count pays validation, construction, memory, or output bytes.

**Proof.** Parsing and comparing F's complete signed literal sequence against the supplied graph/vertex incidence authenticates every original clause independently of offered derived nodes. Each local 3-variable truth table is exactly the source clause's Boolean condition. The three AND3 conjunctions produce the conjunction of all four original vertex clauses, which is precisely parity `xor_{e incident(v)} x_e = chi_v`. The check is exhaustive on eight local assignments. Each original graph edge occurs in exactly two vertex equations; XORing the V rows cancels every edge coefficient and leaves RHS `xor_v chi_v=1`, hence `0=1`. These are the exact conditions tested by the pinned recovered checker for the reconstructed records, including canonical freshness, topological two-parent references, source ancestry and its mandatory `4V-1` count.

For each source clause C at vertex v, the falsifying incident-edge assignment is fixed. Gaussian elimination solves the remaining `V-1` vertex parity equations with those three pins. A solution is an assignment satisfying all other original source clauses while falsifying C; if the reduced system is inconsistent, no such witness exists and `null` is correct. The independently computed essential count equals the count of nonnull witnesses. The all-zero vector witnesses the even-zero-charge control. There are O(V) clause records, O(V) paid records and O(V) GF(2) row masks, each mask encoding at most O(V) edge bits; the 4V deletion witnesses each contain at most E=O(V) bits. Hence O(V^2) evidence bytes plus O(V log V) indices. Gaussian elimination is polynomial; no SAT oracle is used. QED.

**Scope limitation:** This is not a proof-size lower bound or an all-rule R_mix341 normal form. Output length is bounded for the new packet, not necessarily for the old accepted input or for every legal proof under the unknown full calculus. Any general abstract transformer must still admit all genuinely legal mixed rules as MAY transitions pending source authentication.

## Executed V8 audit and hostile controls

The original producer and original checker bodies were fetched at their pinned Git blobs and run in the connected V8 runtime with only `fs.readFileSync` and `console.log` adapted for input/output. The published standalone Node script was not separately executed in an operating-system subprocess. The K4 source was read from the separately persisted 163-byte file `results/raw/arc/2026-11-10_1824_LSPV3_558_K4_EXTERNAL.cnf` (Git blob `ccca1078ce4a64707447b70d4fe10749f80361cd`); the other six test cases used original-fixture-derived source serializations. This is an exact test qualification, not a claim that all seven inputs came from separately archived DIMACS files.

| Graph | V | Canonical output bytes | Paid W | Original checker assertions |
| :--- | ---: | ---: | ---: | ---: |
| K4 | 4 | 3,600 | 15 | 1,401 |
| K3,3 | 6 | 5,316 | 23 | 2,255 |
| Cube | 8 | 7,115 | 31 | 3,237 |
| Petersen | 10 | 8,991 | 39 | 4,347 |
| Prism6 | 12 | 10,918 | 47 | 5,583 |
| Prism16 | 32 | 33,240 | 127 | 25,003 |
| Bridge-K4x2 | 10 | 8,932 | 39 | 4,176 |

**Seven canonical accepts and 46,002 successful original-body assertions.** Each of seven malformed independent-source controls and seven string-charge controls was rejected; each deliberately corrupted offered paid proof was ignored and reconstructed canonically; adding 40,000 irrelevant input metadata bytes did not affect accepted output. The previously accepted LSPV-3/557 SAT-source counterfeit was rejected by the strict G2 numeric charge guard. These tests verify this finite application and the source-level proof; they do not test a full native checker.

Reproducer: `experiments/arc/lspv3_558_external_source_canonical.cjs` (Git blob `621df0b937c97ba2e46c8a517e7f8ec1c6199600`). Raw: `results/raw/arc/2026-11-10_1824_LSPV3_558_CANONICAL_SOURCE_NORMALIZER_RAW.json` (Git blob `2d11c38a7127cf51546ef5cd616991fe862eadc9`). Every record can be reconstructed without consulting an offered paid proof. Native host memory and actual indexed-machine space were not measured.

## Abstract interpretation and CEGAR interface

Within this **G0–G2 guarded original-source fragment**, map a concrete accepted packet `P` together with independent `F,G,chi` to the source-authenticated canonical typed proof `Canon(F,G,chi)`. On accepted original cubic fixtures, both charged histories have W=4V-1, so this is cost-equal for logical paid-node count. The map is proof-independent and erases original paid identifiers and unrelated byte lexemes. The corresponding semantic state includes the independently authenticated original clauses, graph, strict charge vector, topological factor/affine DAG, fixed paid identities, source ancestry, terminal equation, and witness ledger. Its soundness is a **whole-proof retraction**, not yet a step-by-step simulation preserving original intermediate states. No cost-sound transformer is claimed for historical RES, LOCAL-CONVERT, paid DEF, branching or assumption discharge.

A CEGAR path that reaches terminal `0=1` only by accepted but untrusted raw bytes is **not** semantically authenticated. The accepted SAT-source LSPV-3/557 packet fails the independent numeric-charge/source guards; under G0–G2 the canonical source-based proof does represent a real contradiction. Do not confuse this source-dependent recovery with a general derived-proof correctness checker.

## Chain, publication and next target

[P2-D1] OPEN: no authoritative accepted-byte full R_mix341 grammar. [P2-C3] OPEN: no whole-calculus transition-complete cost-sound abstraction. [P2-B1] OPEN: no superpolynomial unrestricted mixed-proof minimum. [P2-B2]/B3 OPEN: no noncircular same-calculus SAT-decider-to-proof transfer. [P1-01], [P1-03], [P1-04] OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE:** this refines the already known /560 restricted reconstruction by adding a bounded regenerated-evidence packet and an independently persisted external source. It does not discharge a new dependency or alter a global status. Source-specific model size and original checker operational acceptance remain qualified.

**Next decisive target:** locate original historical *paid DEF with all defining facets and a facet-to-RES transition* or authenticated RES/LOCAL-CONVERT/context bytes; only then try full native all-rule CEGAR. Without such artifacts, keep unknown rule transitions in a conservative MAY abstraction and do not assert B1 or B3. This run did not modify automations, schedules, historical tariffs, or the two Route A / three Route B allocation. P versus NP OPEN.

## Numbered references

[1] Cook, S. A., and Reckhow, R. A. (1979). The Relative Efficiency of Propositional Proof Systems. *Journal of Symbolic Logic* 44(1), 36–50. https://doi.org/10.2307/2273702.

[2] Cousot, P., and Cousot, R. (1977). Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints. *POPL*, 238–252. https://doi.org/10.1145/512950.512973.

[3] D'Silva, V., Haller, L., and Kroening, D. (2014). Abstract Satisfaction. *POPL*. https://doi.org/10.1145/2535838.2535868.

[4] LSPV-2/341, `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`.

[5] LSPV-1/560, `research/agents/lspv-1/2026-11-10_1755_LSPV1_SOURCE_DRIVEN_RETRACTION560.md`.
