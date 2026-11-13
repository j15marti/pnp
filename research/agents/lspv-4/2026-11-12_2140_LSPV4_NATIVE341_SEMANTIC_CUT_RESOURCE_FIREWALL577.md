% LSPV-4 REPORT::577::2026-11-12T21:40:00-08:00
# LSPV-4/577: Exact 64-model semantic cut and byte-resource firewall in the recovered /341 checker

**2026-11-12 21:40 PST | PNP Time-Space Resource Auditor | historical Route A | PROVED/RESTRICTED mathematical semantic-cut theorem; COMPUTATIONAL independent full-domain and original-code tests. P versus NP remains OPEN.**

## Candidate theorem and four falsifiers

Candidate: for a recovered checker that accepts a satisfiable-source empty-sink trace, no abstract system can simultaneously simulate *all* accepted checker paths, preserve the actual signed SOURCE model set through sound transitions, and interpret every accepted sink as an UNSAT proof. For the original LSPV-1/609 SAT-source packet, a single false affine-row alias discards **all 64** real source models.

F1: actual SOURCE UNSAT. Excluded by 2^18 exhaustive assignments, with exactly 64 models. F2: multiple independently false vertex rows. Excluded: eleven true rows preserve all 64, while v5/d17 eliminates all 64. F3: incorrect Boolean AND3 conjunction is the first error. Excluded: all twelve independent vertex conjunction tables match the recorded factor tables; the d17 table equals 153. F4: the unchanged original checker rejects the packet or accepts type-repaired variants. Excluded in hosted V8: positive accepted with 5,155 assertion groups, four negative controls rejected.

## Source authority, corpus and precedence

Authoritative **only for the recovered /341 SOURCE/AND3/XOR fixture sublanguage**: exact checker at experiments/arc/lspv2_341_independent_verify.js, Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0; exact packet at results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_SAT_ACCEPTED.json, Git blob 8d6d9bc7f2940a77edf2a07fcb72af111ba5b928; producer at experiments/arc/lspv1_609_bridge_slice_forge.cjs, blob 001fc1934e22adb9d26a917ca044b3beaff41664.

**CORPUS REVIEWED.** Both root proof trackers including full 1,049,641-character proof2 Git blob f678f707880da4dfc97dabf778430c6dc816cb1f (contents API showed empty), issue #3 and current comments, AGENTS.md, CODEX.md, repository skill, full tree survey, original checkers, current handoffs and materially relevant original LSPV reports including /539-549 and /571-576; peer LSPV-1/609, LSPV-3/551, LSPV-5/516, and LSPV-2/589-590.

**DUPLICATION / CONTRADICTION AUDIT.** LSPV-3/551 first established an *accepted satisfiable original source* for an earlier different packet. LSPV-5/516 independently replayed that packet on OS Node and proved two-sided membership failure of the /341 executable versus the separately published five-rule declaration. LSPV-1/609 proved the smallest V=12 threshold and independently constructed the present second witness. None of those findings is new here. The incremental finding is the exact **unique 64-model semantic-loss location for the /609 packet**, with same-packet accepted work, reference and serialization evidence, plus a new portable original-checker OS runner. It is NOT a valid historical R_mix341 counterexample.

## Theorem 577.1: unique all-model loss and sound-simulation incompatibility

Let F be the 48 actual signed original three-clauses of /609, on a 12-vertex, 18-edge connected cubic graph. The eleven vertex clauses other than v5 genuinely encode their incidence GF(2) equations with charges whose XOR is 1. Vertex v5's four actual clauses instead impose

$$
x_0\oplus x_1=0,
$$

independent of x_10. But node d17 asserts the false row

$$
x_0\oplus x_1\oplus x_{10}=0.
$$

Every edge outside v5 is incident to exactly two other vertices. Summing the **eleven true rows** cancels those edges and gives

$$
x_0\oplus x_1\oplus x_{10}=1.
$$

Thus in every model of F, x_10=1 and the d17 row is false. An independent exhaustive 262,144-assignment evaluation finds exactly 64 models of F. Every other claimed vertex row holds on all 64 models, so the **unique false local affine row** is d17 and the elimination is **64/64**. Independent local truth-table evaluation still gives the correct d17 conjunction table 153, proving that the error is the **factor-to-affine-row alias**, not its Boolean conjunction.

The checker accepts the packet and derives the syntactic sink 0=1. If a semantic may-abstraction includes the entire accepted checker path, never removes any actual source model at a sound step, and interprets the sink as genuine UNSAT, it both preserves a 64-element model set and requires it to be empty, a contradiction. This formal incompatibility is scoped **to the recovered unsound checker with these three simultaneous obligations**. One may abstract the buggy checker faithfully by marking the step invalid. Neither the historical unified dispatcher nor its accepted language is known, so the malformed packet cannot be used as a legal short R_mix341 proof.

The exact source of the defect is JavaScript type coercion: charge at vertex 5 is the string "0", bypassing strict numeric source pattern parity comparison; global bitwise parity coerces that string to zero. Support at d17 is string "102"; substring includes(10) passes, but truth-table iteration visits character indices 1, 0, 2 instead of integer edge identifiers 0, 1, 10, making the false affine alias appear valid. Replacing that support by the numeric array [0,1,10] causes the original checker to reject with invalid affine alias; replacing charge by integer 0 rejects at source parity.

## Same-packet resource ledger

| Distinct resource coordinate | Recovered /341 packet |
|:--|--:|
| Original signed SOURCE records | 48 |
| Once-paid AND3 records | 36 |
| Once-paid GF(2)/XOR records | 11 |
| **Stipulated logical paid work** | **47** |
| SOURCE-parent applications | 48 |
| Derived-parent applications | 46 |
| **All reference applications** | **94** |
| SOURCE / derived ASCII reference-ID bytes | 134 / 128 |
| **All reference-ID bytes** | **262** |
| Shared antecedent records with fanout greater than one | **0** |
| Compact JSON.stringify evidence | 10,690 bytes |
| Actual published pretty JSON input | 28,120 bytes |
| Original full checker assertion groups | **5,155** |
| Dependency span in paid deduction levels | **14** |

The paid-work identity 36+11=47 is exact for these fixed accepted packet records only. It is **not** the minimum cost of a sound native refutation of F, which cannot exist in a sound refutation system because F is SAT. The 94 parent occurrences are separately charged per use, and 262 bytes measure the literal recorded reference IDs, not decoded source clauses or physical memory. The 28,120-byte original input file and its 10,690-byte compact serialization are different byte presentations. The 5,155 assertion groups include original bundled negative checks and are not a machine-step or time lower bound. No physical peak RAM, reference-decoding cycles, recomputation schedule, full context cost or proof-discovery runtime has been measured.

Authenticated recovered-fragment rule ledger: SOURCE has no extra unit paid inference charge but has parsing and provenance costs; AND3 and XOR each have one stipulated unit charge and two parent applications. Exact time, scratch and writable peak are *unmeasured*. Missing historical Resolution, LOCAL-CONVERT, paid DEF/facets, exported/private wires, weakening, branching, context/discharge, joins and deletion have **no invented tariffs**. An illegitimate affine shortcut is excluded from any sound historical rule system but remains an actual execution for the recovered checker, so it cannot be silently CEGAR-pruned from that different system.

## Execution, falsification, primary literature and research status

Independent hosted V8 execution of the **unchanged source checker body** with only filesystem/argument/console adapters accepted the exact pinned packet with 5,155 assertions. Controls rejected: typed array support (invalid affine alias), numeric charge (source forbidden pattern parity), nonexisting antecedent (missing antecedent), and altered terminal RHS (bad GF2 elimination). Independently enumerated every possible signed-source assignment and reconstructed all twelve local truth tables. New standalone experiments/arc/lspv4_577_native341_semantic_resource_firewall.cjs pins both Git blobs, implements these tests, and invokes the actual OS Node checker, but **a separate OS execution of this new program remains outstanding**. Raw data: results/raw/arc/2026-11-12_2140_LSPV4_577_NATIVE341_SEMANTIC_CUT_RESOURCE_RAW.json.

Mandatory general-candidate falsifiers still open include cheap legitimate GF(2), extension-variable proofs, learned shared lemmas across compatible branches, retention/recomputation, large identifiers, compact affine rows and abstractions overcharging legal concrete paths. None is excluded by this finite SAT-source falsifier. Cook and Reckhow, J. Symbolic Logic 44 (1979), 36-50, DOI 10.2307/2273702, require a sound proof system. Cousot and Cousot, POPL 1977, DOI 10.1145/512950.512973, prescribe model-matched abstraction. Clarke et al., CAV 2000, DOI 10.1007/10722167_15, motivates genuine replay in the *same* concrete system. Hong and Kung, STOC 1981, DOI 10.1145/800076.802486, uses a different I/O pebble machine, so its charges cannot be added without a transfer theorem.

**WHAT CHANGED RELATIVE TO ROOT MAIN:** an exact second-packet 64-model loss certificate and distinct byte/application ledger are added to the existing source-authentication caveat. **ADOPTED**: peer /551, /609, /516 and /576 at original scope. **REJECTED**: recovered-checker acceptance as a valid UNSAT proof, combining sibling /341 and /386 fragments, or equating proof work, serial evidence, verifier time and physical RAM. **RETIRED**: none.

**[P2-D1] OPEN -> [P2-C3] OPEN -> [P2-B1] OPEN. [P2-B2] and [P2-B3] separately OPEN. [P1-01/03/04] unchanged OPEN. TRACKERS REVIEWED; NO MATERIAL CHANGE. P versus NP remains OPEN.** Exactly the existing five identities, Pacific schedules, historical 2 Route A/3 Route B labels, weights and manuscript ownership boundaries are untouched; no automations changed.

Next: authenticate the actual historical full mixed-rule dispatcher, then use a strictly typed original-source RES-to-AND3 or DEF-to-LOCAL-CONVERT edge to establish true goal preservation and cost-sound transition inclusion. A source SAT test is a disqualifier for a refutation proof, not a shortcut to a lower bound.

% END_OF_VERIFIED_REPORT::LSPV-4::577
