# LSPV-2/549: Dual archived-checker accepted-byte polyglot and the noncomposition firewall

**November 10, 2026, 22:12 PST | SAT-Circuit Reduction Builder | historical Route A retained | PROVED/RESTRICTED code-property theorem + COMPUTATIONAL original-body controls | P versus NP OPEN.**

## One candidate, four falsifiers, and what is actually claimed

**Candidate:** The two genuinely archived and *different* original project checkers, the /341 SOURCE/AND3/XOR fixture checker and the /386 signed SOURCE/paid-DEF-facet/Resolution checker, accept a single byte-exact JSON certificate. This makes an actionable regression packet and exposes whether simultaneous operational acceptance is enough to authenticate a heterogeneous RES-to-AND3 inference.

**Precommitted falsifiers:** (F1) the /341 checker insists that `summary` be an actual JSON array, forbidding a shared object; (F2) the /386 checker rejects unknown `fixtures` or the extra `summary.length` property; (F3) a mutation of a RES or AND3 subproof changes *both* checker decisions, implying unrecognized cross-binding; (F4) identical JSON acceptance automatically establishes an authentic same-calculus RES/AND3/DEF transition. F1-F3 are contradicted by original-source execution. F4 is **not a permissible inference**: the two checkers verify different in-band source formulas and disjoint proof graphs, not a mixed proof.

**Authority:** /341 producer `experiments/arc/lspv2_341_mixed_tseitin_min_dag.js` Git blob `4081022e8a3841d79f751a3d3a7a10decbb026da`; /341 verifier `experiments/arc/lspv2_341_independent_verify.js` blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. Distinct /386 verifier `experiments/arc/lspv2_386_independent_verify.js` blob `338305c0ce101704205e57543756b8127074a986`. Its original checker-accepted 4,144-byte compact packet from LSPV-3/561 has Git blob `d0fa96a155672f8f6a6a3428eacafa15e79b9e88`, with source-grounded 17 signed guarded clauses, a paid gate owner and three zero-additional-charge DEF facets. These are *original archived implementations*, but **neither is the missing full five-rule R_mix341 parser**.

## Theorem 549.1: product join for two separately accepted JSON checker languages (PROVED/RESTRICTED)

Let `A` denote exactly the pinned /341 verifier and `B` the pinned /386 verifier. Define the following **top-level accessor projections** from the original checker source:

* `A` reads `fixtures` and the value `summary.length`. It never inspects `spec`, `gate_defs`, `records`, nor the other `summary` counters.
* `B` reads `spec`, `gate_defs`, `records`, and `summary.source`, `summary.def_views`, `summary.resolution`, `summary.paid_gates`, `summary.paid_total`, `summary.live_records`. It never inspects `fixtures` or `summary.length`.

For any separately accepted /341 packet `a` and /386 packet `b` with ordinary JSON objects as top-level encodings, construct `J(a,b)` by using `a.fixtures`, `b.spec`, `b.gate_defs`, `b.records`, and a *single* JSON object `summary` containing the six /386 counters and `length=a.fixtures.length`. Then, in these **two particular original checkers**,

```
Accept_A(J(a,b)) = Accept_A(a) = true
Accept_B(J(a,b)) = Accept_B(b) = true.
```

The proof is direct inspection of the two programs' exact read sets and checks. The /341 code tests `cases.length===data.summary.length` but does not require `Array.isArray(data.summary)`. The /386 code reads the six named summary counters without prohibiting `length` or unknown sibling fields. Hence `J` preserves every value tested by each program. This statement applies to the **specific original checker implementations**, not to hypothetical externally bound variants, to arbitrary JavaScript consumers, or to the full R_mix341 calculus.

There is a further **noncomposition control**: under fixed `J` one can corrupt an AND3 result and obtain (A REJECT, B ACCEPT), or corrupt an archived RES pivot and obtain (A ACCEPT, B REJECT). Thus no cross-grammar premise, source-identity mapping, fresh wire map, or count-once charging relation is validated by the two checkers. Double acceptance **does not authenticate any RES-to-AND3, DEF-to-AND3, LOCAL-CONVERT, branching, assumption-discharge or shared-cost transition**. This is a failure of the proposed *evidence inference*, not a theorem that interoperability is impossible under a properly specified new checker.

## Concrete byte-exact witness and executable controls

The witness is the JSON object

```json
{"fixtures":[<one original /341 K4 fixture>],
 "spec":<original /386 signed guarded K4 spec>,
 "gate_defs":<original /386 paid gate owners>,
 "records":<original /386 69 records>,
 "summary":{"length":1,"source":17,"def_views":3,
            "resolution":49,"paid_gates":1,
            "paid_total":50,"live_records":69}}
```

This is a structural display, **not** the complete byte payload. The complete 7,533-byte ASCII packet including its final LF is published verbatim at `results/raw/arc/2026-11-10_2212_LSPV2_549_DUAL_NATIVE_POLYGLOT_PACKET.json` (Git blob `b9c1d306c300a3f1917ee01ecab16358ac77d4de`). Do not reconstruct from the structural display when comparing bytes.

The genuine /341 leg is the original *unguarded* signed K4 odd Tseitin source: 16 original signed width-three clauses, 15 paid inference nodes, 12 AND3 plus 3 XOR, one empty affine contradiction and full ancestry. Its previously externally reconstructed signed DIMACS is 163 bytes, SHA256 `861b38239ec08050a7b38b3da04fd79c17d43624a8f755be5a1417d8f01745c8`. The distinct /386 leg is the 17-clause *guarded* signed K4 source, with 49 paid RES nodes, one paid two-input conservative gate owner, three free facet views, and an empty-clause sink. These are *not identical encoded CNFs*.

The unchanged checker bodies were executed in V8 using `Function` with only `fs` file reads, console logging, a clone helper and an output-only cryptographic digest adapter. They both ACCEPTED the same combined packet:

| Packet/control | Original /341 | Original /386 |
| --- | --- | --- |
| Combined 7,533-byte packet | ACCEPT, 1,401 checks | ACCEPT, 4,492 checks |
| Wrong /341 AND3 table | REJECT | ACCEPT |
| Wrong /386 RES pivot | ACCEPT | REJECT |
| Missing `fixtures` | REJECT | ACCEPT |
| Missing `records` | ACCEPT | REJECT |
| `summary` replaced with one-element array | ACCEPT | REJECT |
| Delete `summary.length` | REJECT | ACCEPT |
| Wrong /341 SOURCE literal | REJECT | ACCEPT |
| Wrong /386 SOURCE clause | ACCEPT | REJECT |

Thus **nine differential cases** passed: one both-accept and eight one-sided reject controls, with 4 /341-only accepts and 4 /386-only accepts. The results are in `results/raw/arc/2026-11-10_2212_LSPV2_549_DUAL_NATIVE_V8_RAW.json`, blob `f6b6322a9bd14a19522f545627271dd97668b01d`. This uses the original mathematical checker bodies, **not** separate hand-written emulators. The program's original file I/O was shimmed and the hash of the packet in the /386 output was stubbed; no inference check was edited. This run did **not** execute the standalone operating-system Node subprocesses.

The new, self-contained dependency-free Node runner is `experiments/arc/lspv2_549_two_native_checker_polyglot.cjs`, blob `bf2317e9200f6c092c6c65187e4b1ede71fa884c`. It pins every original Git blob, regenerates the packet using the original producer, invokes **both unchanged original checkers in separate native Node subprocesses**, replays all nine tests, checks source-byte length and native assertion counts, and writes its separate, explicitly labelled OS result to `results/raw/arc/2026-11-10_2212_LSPV2_549_DUAL_NATIVE_NODE_REPLAY_RAW.json`. The Node program passed JavaScript syntax compilation in V8; native OS execution remains an independent verification task and no resulting OS ledger is claimed to have been generated here.

## P2-C3 concrete state, abstract transition polarity and CEGAR

A concrete state must specify **which** authenticated proof language is being executed. A legitimate abstract configuration for a mixed calculus cannot identify the /341 truth-table `parents` with the /386 chronological numeric `parents` just because both occur in one JSON object. Track at least: (1) checker language version and pinned digest; (2) original formula bytes, SHA and signed clause-occurrence provenance; (3) source-parent identities and their type; (4) distinct first-paid identities and facet owner table; (5) authorized wire declarations and freshness/export scope; (6) active contexts and outstanding branch-AND/discharge obligations; (7) whether a cross-language conversion step has an **authenticated** checker rule; and (8) separate logical charges, certificate bits, construction time, critical span, and physical high-water state.

For a new abstract relation `Post#` to soundly overapproximate the true full calculus, every concrete legal step must have an abstract successor with **no higher logical cost**; both completed refutations and the original source commitment must remain represented. Since no source-authenticated cross-language transition is available, its effect remains `MAY` with charge floor zero, **not** the invented transition `RES -> AND3` at unit cost. In a CEGAR loop, a cheaply guessed stitched path is not confirmed by independent acceptance of both packet legs. It must replay on an authoritative *single* full mixed-rule checker; lacking that, it remains unverified rather than being promoted or permanently excluded. Genuine previously authenticated XOR, extension, learned clause, shared-node and reconvergent shortcuts remain allowed.

The resource ledgers cannot be merged into a single price for the combined artifact:

| Resource component | /341 component | /386 component | Combined artifact |
| --- | ---: | ---: | --- |
| Source clauses | 16 unguarded | 17 guarded | Two separate in-band sources |
| Paid logical inferences | 15 | 49 RES plus 1 gate owner = 50 | **No authenticated joint proof cost** |
| Zero-additional-charge facet records | not represented | 3 | not shared across verifiers |
| Topological records/nodes | 31 (16+15) | 69 records + gate sidecar | unlinked |
| Ideal proof depth | 6 for /341 K4 | 10 for the published /386 record DAG counting gate view depth 1 | **No joint span** |
| Certificate bytes | component-dependent | 4,144 original packet | 7,533 polyglot bytes |
| Physical construction time and memory peak | not measured here | not measured here | not measured here |

The 7,533 bytes are an encoding cost for **two independent certificates together**. Neither this byte count nor the sum 15+50 is a lower bound on SAT computation, on the cost of acquiring a shortest proof, or on the complete R_mix341 proof relation.

## Novelty, corpus reconciliation, external sources and next falsifier

LSPV-2/539 already proved soundness of a separately source-bound typed SOURCE/AND3/XOR reference fragment. /540-/546 documented JSON duplicate keys, nonfinite numeric identities, source permutations, byte-span rewriting, Unicode, invalid UTF-8 and BOM differences. /547 provided a *proposed* RES/AND3/XOR reference certificate, not a historical checker. /548 established the original /341 checker's integer and missing-terminal-ID behavior. LSPV-3/561 had just recovered and executed the **different** original /386 checker and published its compact authentic facet/RES packet. It explicitly warned that /386 is not /341. This investigation's **new contribution** is the *same raw JSON packet accepted by both original historical checkers*, a proved product-join lemma for their verified field projections, and a nine-case executable one-sided-mutation firewall. It is **not a full R_mix341 dispatcher discovery**.

Both root trackers were read: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, `proof2.txt` blob `3f32872d3fdddc96ecce6762dae45b2489a67d10` at preflight. Also surveyed issue #3 through LSPV-4/534, AGENTS.md, CODEX.md, project research skill, the /341 original declaration, LSPV-2/539-548, LSPV-3/561 and handoff, relevant LSPV-1 and LSPV-4 source/cost reports, and repositories `konard/p-vs-np`, `blkph0x/p-vs-np-proof-research`, `meelgroup/frat-xor`. None supplies the missing authoritative five-rule original dispatcher. Primary references: S. Cook and R. Reckhow, *Journal of Symbolic Logic* 44 (1979) 36-50, DOI 10.2307/2273702; P. Cousot and R. Cousot, POPL 1977, DOI 10.1145/512950.512973; FRAT-XOR, `meelgroup/frat-xor/format.md` and its formally checked XLRUP elaboration interface. These are proof-system and abstraction precedents, not historical /341 syntax.

**Proof consequence:** a material **P2-D1/P2-C3 evidence node** may record this independent-checker noncomposition firewall. It changes neither the complete historical calculus status nor any asymptotic theorem. P2-D1, P2-C3, P2-B1, and separately P2-B2/B3 remain **OPEN**; P1-01/03/04 and P versus NP remain OPEN. Fixed five research roles, existing two Route A / three Route B labels, titles, timezone, schedules, historical tariffs and manuscript ownership unchanged.

**Immediate next target:** Demonstrate one actual source-authenticated, original **single-dispatcher** accepted packet with RES feeding AND3 or paid DEF feeding LOCAL-CONVERT (the /341 and /386 checker outputs are independently insufficient), or prove an exact source-preserving, cost-sound interoperability compiler with a checker that verifies each cross-rule port.

**LSPV-2/549 VERIFIED STANDALONE REPORT; P versus NP OPEN.**
