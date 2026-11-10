# LSPV-1/556: High-bit ghost-mask closure of the recovered /341 accepted-byte verifier

**2026-11-10 PST | PNP General SAT Lower-Bound Lead, Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## IDEA and four falsifiers, registered before evidence search

**Candidate NATIVE-556:** The unchanged original /341 SOURCE/AND3/XOR *fixture* verifier fails to range-check affine mask bits beyond the original edge-variable count E. For every real odd-Tseitin proof fixture with V vertex parity rows, k added high-coordinate mask bits produce exactly 2^(k(V-1)) distinct checker-accepted proof packets when vertex high masks have zero total XOR and all downstream XOR outputs are recomputed. Each remains the same 4V-1 paid-node DAG and original source. This is accepted-byte grammar analysis, NOT a historical full R_mix341 rule authentication, SAT lower bound, or genuinely legal auxiliary definition.

F1: the native parser rejects an out-of-range leaf mask. F2: an even-parity collection of high masks breaks a later XOR or the terminal 0=1. F3: the separate strict reference accepts an out-of-range mask as a legal source-variable row. F4: an odd total ghost mask also passes the sink, or a corrupted in-range leaf bit passes the local affine check. All four falsifiers were directly tested: F1/F2 did not occur; F3 was rejected in the typed reference; F4's two corruptions were rejected by the original fixture checker.

## Required audit and primary search

Read BOTH complete current root trackers, [proof1.txt](../../proof1.txt) and [proof2.txt](../../proof2.txt), current [issue #3](https://github.com/j15marti/pnp/issues/3) and recent specialist comments, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, the 2026-11-09 abstract-negative handoff, the 16:24 FLMV handoff, latest native five-role handoffs and relevant actual LSPV-1/548, 553-555, LSPV-2/341 and /539-540, LSPV-3/552-553 and LSPV-4/525 reports. Read the original pinned /341 producer/checker, and independent typed /539 executable, not only summaries. Targeted original Grok material: GROKPROOF/2026-11-10_1435_PROGRESS.md. Targeted external repositories: konard/p-vs-np/scripts/proof_status.json (its individual theorem scopes), blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (its explicitly bounded results), meelgroup/frat-xor/format.md (a DIFFERENT mixed proof grammar), and tanyongkiam/cake_lpr/README.md (verified checker interface; different grammar). Neither external repository supplies the missing historical R_mix341 byte parser.

Relevant primary literature: Cook and Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1):36-50, DOI 10.2307/2273702; Cousot and Cousot (1977), *Abstract Interpretation: A Unified Lattice Model*, POPL, DOI 10.1145/512950.512973; Urquhart (1987), *Hard Examples for Resolution*, JACM 34(1):209-219, DOI 10.1145/7531.8928. These papers establish proof-checking, abstraction and Resolution-hardness contexts, not the ghost-mask observation or full historical checker.

**Pinned original files, validated by GitHub blob read:** producer experiments/arc/lspv2_341_mixed_tseitin_min_dag.js SHA 4081022e8a3841d79f751a3d3a7a10decbb026da; checker experiments/arc/lspv2_341_independent_verify.js SHA fcb7d4ced8f922de14c0bda16263a8cc7853e8e0; typed LSPV-2/539 source-bound reference experiments/arc/lspv2_539_strict_fragment_reference.cjs SHA fc91a6f33d0d010d6225365a3d9ce72a090af21f. The two latter grammars must not be conflated.

## Theorem 556.1: exact high-mask acceptance fiber (recovered checker only)

Fix any one of the seven original /341 odd-charge cubic-Tseitin fixtures with V vertices, E edges, m=4V genuine source clauses and q=4V-1 paid AND3/XOR records. The original verifier executes, for each AND3 factor's asserted affine row of mask M, exactly these *finite* checks: (a) every set bit among indices e=0,...,E-1 belongs to the asserted factor support; (b) the equality with its factor truth table holds on the support's at-most-eight assignments, evaluating parity only for indices e<E. It does NOT check that (M >> E)=0. For XOR nodes, the checker requires exact arbitrary-precision BigInt XOR of parent masks, and for the sink it requires M=0 and rhs=1.

Let M_v be the original row mask of the final AND3 factor at vertex v, and let k>=1 and h_v in GF(2)^k. Define a new leaf mask by

$$
M'_v=M_v\oplus (h_v 2^E).
$$

Keep every source clause, graph, source ID, paid ID, parent, support, truth table, RHS, deletion witness and charge *identical*. Recompute the mask of every subsequent XOR node from its updated parents in the original topological order, without changing RHS or paid nodes.

The verifier accepts this modified packet **if and only if**

$$
\bigoplus_{v=0}^{V-1}h_v=0.
$$

Proof: The AND3 checks query only e<E, where new and old masks agree, so every local check and the actual source factors remain unchanged. Each XOR step holds by construction with the recomputed mask. The final mask is the old zero mask XOR (2^E times the sum of all h_v). Since the terminal check tests the *entire* BigInt for exactly zero, the terminal passes precisely for zero total ghost parity; all other unchanged checks still pass. The map from the V high-bit vectors to changed leaf masks is injective, and one linear vector equation of rank k has k(V-1) degrees of freedom. Hence for fixed k, **exactly**

$$
\boxed{2^{k(V-1)}}
$$

distinct such accepted packets exist. For each: q=4V-1, the same whole paid DAG, no new source, no new paid definition, and the same actual UNSAT formula. This is a statement about the specified finite packets interpreted by the recovered JavaScript checker; arbitrary finite k is understood within the memory capacity and BigInt semantics of an executing host.

## Theorem 556.2: local semantic misannotation, but cost-preserving low-bit projection

Take the original K4 row for vertex zero: low mask 0x7, rhs 1. Its four genuine source clauses are satisfied by the six-original-variable assignment with x_0=1 and all other x_e=0. Under the intended semantics of every high bit as an additional Boolean variable y, setting y=1 changes the claimed row's parity from 1 to 0, falsifying it while preserving all four antecedent source clauses. Thus an out-of-range ghost row is **not** an exact GF(2) consequence on an extended universe of variables. It is an accepted malformed annotation under that interpretation.

Conversely, the projection

$$
\pi_E(M)=M\bmod 2^E
$$

commutes with XOR and maps every mask in the constructed ghost lift back to the unchanged original proof. Consequently **these variants do not yield a cheaper proof**, and by themselves do not falsify a putative full-calculus lower bound. For this explicitly characterized fiber, the low-bit quotient is a sound cost-preserving *normalization* of the accepted packet to the existing valid proof, provided one uses the actual source-bound original-variable semantics. A general normalization theorem for ALL native accepted packets, auxiliaries, DEF owner facets, contexts, branches and other opcodes is NOT established.

A parser that rejects all high masks may be a well-designed separate reference checker, but its accepted language is strictly smaller than the original recovered fixture verifier's accepted-byte language. It cannot be substituted as the sole overapproximating native relation in a lower-bound proof without an independently proved, cost-preserving normalization covering the omitted bytes.

## ITERATE: original-code replay and independent strict reference differential

Directly executed the pinned original producer and checker function bodies in V8, with the file-input/output shell adapted and the mathematical verification body unchanged. Exhausted the 2^(2*(4-1))=64 K4 two-high-bit vectors with zero total XOR. **All 64 were accepted by the original checker**; only the all-zero vector was accepted by the separate source-bound typed /539 reference, and all 63 nonzero vectors were rejected. Both references accept the unmutilated baseline.

All seven recovered historical fixtures independently accepted baseline, a two-row high bit at index E and a three-bit high pattern at index E+256, with identical native checker assertion counts in each variant:

| Fixture | V | E | Original clauses | Paid nodes | Checker checks per variant |
| --- | ---: | ---: | ---: | ---: | ---: |
| K4 | 4 | 6 | 16 | 15 | 1401 |
| K33 | 6 | 9 | 24 | 23 | 2255 |
| CUBE | 8 | 12 | 32 | 31 | 3237 |
| PETERSEN | 10 | 15 | 40 | 39 | 4347 |
| PRISM6 | 12 | 18 | 48 | 47 | 5583 |
| PRISM16 | 32 | 48 | 128 | 127 | 25003 |
| BRIDGE_K4x2 | 10 | 15 | 40 | 39 | 4177 |

The sum is 46,003 native assertions per seven-fixture sweep, with 21 accepted fixture runs. The high bit at E+256 on K4 was accepted by the recovered checker and rejected by the separate typed reference as "mask references outside source." A single unpaired high bit was rejected by original native terminal as "invalid sink." An unpaired in-range bit mutation was rejected as "invalid affine alias." The exact source-local counterassignment above was checked.

**Execution limitation:** These are actual original JavaScript mathematical verifier bodies replayed in Code Mode V8. The separately published Node.js CLI reproducer was syntactically compiled and its source was read back, but was not executed as a standalone OS Node process. No noncryptographic V8 adapter was counted as a real SHA256; original GitHub blob SHAs were independently fetched. Neither the complete historical rule checker nor the repository-wide preflight was executed.

Reproducer: [experiments/arc/lspv1_556_native_ghost_masks.cjs](../../experiments/arc/lspv1_556_native_ghost_masks.cjs). Raw ledger: [results/raw/arc/2026-11-10_LSPV1_556_NATIVE_GHOST_MASK_RAW.json](../../results/raw/arc/2026-11-10_LSPV1_556_NATIVE_GHOST_MASK_RAW.json). Independent specialist review remains pending.

## Dependency and all-resource ledger

- **[P2-D1] OPEN:** A new exact characterization of the *incomplete fixture checker's* high-coordinate accepted bytes, not the historical all-rule grammar. The checker ignores high bits locally, retains them globally in XOR/sink. A fixed source-bound accepted-byte semantics and policy for auxiliary variables remain missing.
- **[P2-C3] OPEN:** Abstract configurations must distinguish original source variable scope, raw mask words and any authenticated definition-owned auxiliary mask extension; source semantics and exact paid IDs cannot be inferred from JSON shape alone. An abstract may-edge must not discard the accepted high-bit family solely by imposing the new typed /539 reference grammar. For this family, a cost-preserving low-bit projection is proved, not for every possible native operation.
- **[P2-B1] OPEN:** An entire fixed native calculus and a superpolynomial all-input proof minimum remain unproved. These seven parity-hard-for-Resolution controls already have 4V-1 paid proofs in the declared mixed semantic calculus. Ghost aliases do not lower that work.
- **[P2-B2]/B3 OPEN:** No all-machine same-R upper-bound transfer. No SAT-in-P or FLMV implication follows.
- **[P1-01], [P1-03], [P1-04] OPEN:** No uniform all-input deterministic SAT solver.
- Logical work q stays 4V-1; raw JSON bytes grow with high mask length, parsing/traversal/BigInt computation incur real time and memory, unchanged DAG span is not input-runtime, source acquisition/verification and proof discovery are distinct. No oracle, answer table or uncharged GF(2) definition is introduced.

**Shared interfaces:** LSPV-3 should independently authenticate the intended mask-width/fresh-wire/DEF ownership conventions and determine whether /341's raw high bits are normalized, rejected or interpreted as fresh equations by any *true* historical native checker. LSPV-5 should falsify the parameterized fiber and the projection lemma against original source and terminal checks. LSPV-2/4 retain Route A. All five identities, schedules, enabled states, titles, ownership boundaries, weights and existing two-Route-A/three-Route-B split remain untouched.

**Actual advance:** A new exact, parameterized family of accepted-but-out-of-range affine mask packets, independently differential-tested in the original recovered checker, with a precise cost-preserving projection that isolates what can and cannot be normalized. **Remaining blocker:** full authoritative R_mix341 accepted-byte semantics [P2-D1] and full-rule cost-sound abstraction [P2-C3]. **P versus NP OPEN.**
