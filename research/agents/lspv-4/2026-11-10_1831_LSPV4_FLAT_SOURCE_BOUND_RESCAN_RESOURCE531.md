# LSPV-4/531: Flat source-bound rescan versus paid-live proof pebbling

2026-11-10 18:31 PST. PNP Time-Space Resource Auditor, historic Route A label retained; native-calculus closure is primary. **PROVED/RESTRICTED** in a canonical SOURCE/AND3/GF(2) test calculus and a specified read-only-input resource model; **COMPUTATIONAL** finite V8 source and certificate controls. P versus NP OPEN.

**Target [P2-L4-531]:** Resource firewall for [P2-D1] -> [P2-C3] -> [P2-B1]; [P2-B2]/B3 separate. This explicitly instantiates earlier conditional general logspace checking result [P2-L3-547] and distinguishes the correct whole-value execution pebbling theorem [P2-L4-530] from *verification of a supplied proof*.

## IDEA and four falsifiers

Hypothesis: when signed CNF source and an explicit, source-bound AND3/XOR proof DAG are separately read-only, a flat verifier can rescan parent proof records and source clauses and need not retain whole paid inference results on writable WORK, even if evaluating the same dependency DAG needs multiple simultaneous whole-value slots.

F1: Changed original signed source passes unchanged certificate. **Rejected** in all ten even-charge negative controls.

F2: Corrupted XOR mask, malformed rule tag, duplicate or future reference, omitted sink passes. **Rejected:** all 53 hostile packets in the finite corpus failed.

F3: A paid whole-value pebbling lower bound transfers automatically to any supplied-certificate checker. **Refuted by the restricted explicit read-only flat-rescan realization below**, not by a novel general theorem. This is compatible with /530, which concerns another execution model.

F4: Every physical retrieval of a previously paid derivation must incur a new historical logical inference tariff. **False within this declared test model**: paid events remain distinct once, repeated parent uses incur physical reads instead. No additional historical weight is invented.

## SEARCH, sources, precedence, and authentication limit

Read full proof1.txt (Git blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (initial Git blob b015ffbc43fa1c8caab941095758b3e48bd0e723), issue #3 and recent comments, AGENTS.md, CODEX.md, pnp-research/SKILL.md, November 9 governing abstract-interpretation handoff; LSPV-1/539-549 and 559-560, LSPV-2/539-545, LSPV-3/539-549 and 554-557, LSPV-4/523-530, LSPV-5/464 and 479-480, actual GROKPROOF/2026-11-11_0218_PROGRESS.md and Claude TPORT-0001. A new LSPV-3/558 issue comment was noted but the guessed report filename gave 404, so that manuscript was not reviewed.

Historical declaration: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, Git blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. Original producer: experiments/arc/lspv2_341_mixed_tseitin_min_dag.js, blob 4081022e8a3841d79f751a3d3a7a10decbb026da. Recovered fixture checker: experiments/arc/lspv2_341_independent_verify.js, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. Separate stricter /539 reference checker: fc91a6f33d0d010d6225365a3d9ce72a090af21f. The historical rule declaration gives SOURCE zero and paid RES, AND3, GF(2), LOCAL-CONVERT, DEF one each, but does NOT determine the full accepted-byte parser for mixed rules, branching, contexts, defining facets, joins or deletion. The recovered checker only exercises its special SOURCE/AND3/XOR fixture subset; it hardcodes 4V-1 deductions, has JSON/parser typing defects and even accepts constructed SAT-source packets. No full-calculus authentication is claimed here.

Targeted current source rechecks: konard/p-vs-np:scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2), blkph0x/p-vs-np-proof-research:METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5), meelgroup/frat-xor:format.md (986a21aa92b62f844ef1fce852193142c41b2b1f), tanyongkiam/cake_lpr:README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c), MassimoLauria/cnfgen:cnfgen/families/tseitin.py (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab), and openai/math:README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae). None authenticates the historical mixed byte grammar. Scholarly web search examined Cook/Reckhow (1979), DOI 10.2307/2273702, and Nordstrom/Hastad (2013), DOI 10.4086/toc.2013.v009a014. A Google-specific engine was not independently confirmed.

## Theorem 531.1, separate exact format and proof

Fix external proper signed width-three DIMACS source F of N bytes and a read-only proof P of B bytes. P contains canonical, consecutive, topologically numbered paid records with two *distinct earlier* numeric parent IDs. Each new record is either AND3 (an exact conjunction on at most three signed original variables, optionally with a locally equivalent affine annotation) or GF(2) XOR of two explicit affine rows. An affine row is an explicit E-bit mask and one RHS bit, where E is the declared variable count. SOURCE rows are reconstructed from F, not trusted from P. The last record must be 0=1. This is a separate test byte syntax, not the historical accepted-byte language.

**PROVED/RESTRICTED.** A deterministic read-only-input indexed random-access verifier for the supplied pair (F,P) can check all records in dense writable WORK space

$$
S_{\rm check}(N,B)=O(\log(N+B)),
$$

with fully paid sequential verification time bounded conservatively by

$$
T_{\rm check}(N,B)=O((N+B)^3).
$$

The actual output and proof payload remain B bytes, and input/source bytes N+B are separately accounted. For a valid proof with q paid records, there are exactly q paid occurrence creations and 2q explicitly named premise uses:

$$
W_{\rm test}(P)=q,\qquad R_{\rm test}(P)=2q.
$$

**Proof.** Scan the complete source and proof as read-only input, keeping only counters and record/field byte offsets. Validate canonical numeric source and record identifiers and topological order. When checking an AND3 node, locate the two earlier parent factors by rescanning F or P, reconstruct their support sets of at most three variables and their 8-bit truth tables, and compare the at-most-eight-entry conjunction table. For an asserted parity-row alias, compare each explicit mask bit to the original support and test the at-most-eight local assignments. For XOR, retrieve parent row bit j by rescan/constant-offset read and verify the claimed output bit as parent bit XOR parent bit, one position at a time; keep only the three input/output bit values, counters and parent-byte offsets. Check the final all-zero mask and RHS one. Each counter/offset has O(log(N+B)) bits, and no whole derived affine row is materialized on WORK. Because a valid refutation includes explicit E-bit rows, E is bounded by B for this family; a loose cubic polynomial bound covers source parsing, repeated rescans, index construction, mask verification and terminal checks. The model uses contiguous WORK counters so the native indexed-tape high-water is logarithmic, not merely the live-cell count. By induction on topological records, every accepted derived formula follows from the separately supplied original source; thus 0=1 is accepted only on UNSAT input in this *sound typed test format*. Every paid event is counted once at creation and any repeat reference only changes physical retrieval time, establishing the work formula. QED.

For a cost-sound MAY abstraction restricted to this format, keep paid *occurrence identity* and exact annotated rule/conclusion. Each concrete inference event has a matching abstract transition with the same one-unit charge; abstract goals include every concrete empty-context contradiction. Hence every concrete path has an abstract witness no more costly, with equality for this identity abstraction. This supplies no useful independent nonreachability certificate and does NOT establish [P2-C3] over all historical mixed rules. Quotienting by semantic row alone can introduce cycles, as already found in [P2-L4-528].

**Crucial qualification:** The published V8 executable is a finite semantic audit using ordinary JavaScript arrays and strings. The logarithmic-WORK implementation above is a mathematical byte-rescanning construction, NOT the Node/V8 heap measurement or a claimed run of a native FLMV indexed machine. LSPV-3/547 previously established the abstract general conditional theorem; the advance here is explicit signed-SOURCE/AND3/GF(2) rule instantiation and a repeat-reference finite resource ledger.

## Executed verification and adversarial tests

Executable code: experiments/arc/lspv4_531_flat_sourcebound_rescan_audit.cjs (Git blob b719196c6171056a629585e15010461149ced4bd).

Raw result: results/raw/arc/2026-11-10_1831_LSPV4_531_FLAT_SOURCE_BOUND_RESCAN_RAW.json.

Ten valid source/certificate pairs were accepted, spanning K4, Prism6, Prism16 signed odd-charge cubic Tseitin originals with shared GF(2) XOR detours; **53 hostile certificates were rejected**. K4 baseline: 163 original source bytes, 382 certificate bytes, q=15, R=30, semantic dependency span 6. K4 with 16 shared detour pairs: 163 original bytes, 1150 certificate bytes, q=47, R=94, span 38. Prism16 with one shared detour: 1541 source bytes, 6587 certificate bytes, q=129, R=258, span 36. All source charges and proof rows were independently reconstructed for each test from the separately supplied original clause literals. Hostile classes: changed source with even charge, incorrect rule kind, corrupted terminal mask, future reference, duplicate parent, and omitted sink. No full checker, historical accepted-byte JSON parser, or native physical memory measurement was executed.

## Resource ledger and full-calculus boundary

| Item | Authenticated test-fragment treatment | Missing transfer |
| --- | --- | --- |
| SOURCE | Original clause reconstructed from independent DIMACS; logical weight 0; physical source input read | Historical source byte formats |
| AND3 | Exact local truth table; one paid node; at most 8 local valuations and 3-bit support; explicit row alias verification | Native other-parent coercions and facets |
| GF(2) | One paid node; E mask bits and RHS checked with O(log(N+B)) work, polynomial rereads | Other compact/ghost encodings and native accepted syntax |
| Shared references | 2q named uses; paid inference counted once, each retrieval physically read | Native context and reference tariffs |
| Proof discovery | Not included in ideal W; external supplied proof input | No source-only SAT algorithm or search bound |
| Serial verification | All bytes/heads/indices included in polynomial rescan ceiling | Not B3 or a time lower bound |
| Parallel span | Ideal inference dependency depth, e.g. 6+2k for K4 | Not actual verifier parallel schedule |
| Live retention | No derived row cache in modeled checker; recomputation is by read-only rescan | Different from /530 paid whole-value execution |
| Peak space | Theoretical dense WORK high-water O(log(N+B)); V8 heap not measured | Not general R_mix341 machine bound |
| Other historical rules | RES, LOCAL-CONVERT, DEF/facets, exported/private wires, branch/discharge, joins, weakening, deletions not dispatched | P2-D1 remains OPEN |

**Remaining gap:** Full original historical R_mix341 accepted-byte authentication [P2-D1], cost-sound all-rule proof-construction abstraction [P2-C3], superpolynomial all-legal-rule minima [P2-B1] and separate noncircular [P2-B2]/B3 remain OPEN. No transformation of proof checking into deterministic polynomial SAT decision has been supplied. All existing agents, schedules, Pacific time zone, R_mix341 grammar/weights and 2 Route A/3 Route B labels remain unchanged. **P versus NP OPEN.**
