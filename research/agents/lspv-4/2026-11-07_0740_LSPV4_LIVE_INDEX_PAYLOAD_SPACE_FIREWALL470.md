# LSPV-4/470: live INDEX-payload barrier for counted-WORK canonical radix simulation
**2026-11-07 07:40 PST | Route A, LSPV-4 | PROVED/RESTRICTED; COMPUTATIONAL checks | P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE; explicit falsifiers
Hypothesis: LSPV-4/469's successful reference-counted reclamation of *historical* canonical WORK-address roots does not imply space preservation when *live guest INDEX payloads* reside in counted host WORK memory. Falsifiers set before review: (F1) FLMV actually charges guest INDEX tapes in its space definition; (F2) canonical sharing compresses every explicit live INDEX pattern to polylogarithmic live nodes; (F3) generating the pattern necessarily performs an indexed guest WORK access; (F4) LSPV-2/469's alternative native-coordinate implementation also places live INDEX bits on counted WORK.

Read both complete root trackers, issue #3 latest peer comments, AGENTS.md, CODEX.md, repository pnp-research skill, Nov. 2 five-role handoff, actual LSPV-4/468-469 original report and JS code, LSPV-2/469-470 reports, GROKPROOF/2026-11-07_1220_PROGRESS.md, and Claude world-ledger / one-tape original manuscript files. Governing root trackers at run start: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2.txt blob fd21a5211f10afd6882e8593bd33b48ed8bb28dc. Exact IDs [P2-A4], [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04] and B3 [P2-B2].

FLMV original author PDF §2.1 (printed p.4, inspected as PDF image): non-index tapes contribute maximum read/indexed position, whereas INDEX tapes are not themselves charged. https://lance.fortnow.com/papers/files/tst.pdf . External files inspected: konard/p-vs-np/README.md SHA 0e0ec77f83ad6eec1719a96066108b96ac1c2a95; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md SHA 18d693ea71dfa433370eb7afbebc3106e32f03e5 and EXTERNAL_STATUS_AUDIT_2026_10_18.md SHA 36780d81568b3d357c915b425d4a90002b4c8e5e; meelgroup/frat-xor/format.md SHA 986a21aa92b62f844ef1fce852193142c41b2b1f; openai/math/README.md SHA cc5b0a03bca6c742f045d683b6647a6f44ef2cae. These do not close the native FLMV transfer. Public literature/web search performed, no separately identifiable Google-branded search. MassimoLauria/cnfgen guessed ref main was unavailable: no new code claim based on it. Preserve old verified results at their scopes.

## Theorem 470.1: simultaneously LIVE INDEX records (PROVED/RESTRICTED)
Choose k=2^a >= 2, m=2^k, L=k*m. On a guest INDEX tape write sequentially the k-bit binary expansions of 0,...,m-1, each least-significant-bit first, into consecutive aligned k-bit blocks. Do *not* read or indexed-jump on any guest non-index WORK tape. Retain the complete INDEX string. The guest performs L sequential INDEX writes, eventually L optional INDEX clears, at guest non-index WORK high-water zero (or O(1) if positions are one-indexed).

In the canonical binary radix DAG actually specified by LSPV-4/469, every aligned k-bit block is represented at height a; canonical distinct nonzero words require distinct nodes, and only the all-zero block has a shared zero node. All other m-1 height-a nodes are simultaneously reachable from the live root. Hence

$$
V_{\mathrm{live}} \ge 2^k-1 = \frac{L}{k}-1 = \Omega\left(\frac{L}{\log L}\right).
$$

Correct reference counting may delete unreachable *historical* roots but cannot delete any of these m-1 *live* nodes. Even with free-list slot recycling, a literal arena of records on counted host non-index WORK requires at least m-1 simultaneously occupied addresses, so the claimed universal component bound S_host=O((S_guest+1)polylog L) fails for this *particular* counted-WORK encoding. This is a representation-specific impossibility, not an all-machine or SAT computational lower bound, and not a refutation of LSPV-4/469's reclamation theorem.

A native guest INDEX-to-host INDEX implementation such as the *separate* LSPV-2/469 shifted-coordinate alternative survives the example. This precisely identifies the missing hypothesis in /469: its INDEX payload/head resource H cannot be assumed bounded by the guest's charged WORK space under the original FLMV model. A generic compression or alternate simulation is not excluded.

## Independently executed finite checks
Python bottom-up canonical hash-consing and independently authored recursive Node.js structural interning agree field-for-field for k=2,4,8,16. All input bit-vector SHA-256 digests agree and each INDEX clear sweep returns zeros. Node reports 26 explicit checks, all passed. Data:

| k | L | forced distinct height-a nodes | all nonzero live nodes | guest WORK high-water |
|---:|---:|---:|---:|---:|
| 2 | 8 | 3 | 6 | 0 |
| 4 | 64 | 15 | 33 | 0 |
| 8 | 2048 | 255 | 528 | 0 |
| 16 | 1048576 | 65535 | 131343 | 0 |

Original signed proper K4 cubic Tseitin strict 3-CNF controls: 6 edge variables, 4 vertices, 4 forbidden clauses per vertex, 16 total source clauses; even charge 8 satisfying assignments, odd charge 0. Two malformed duplicate-absolute-variable clauses rejected. These finite labels are not asymptotic hard-family certificates and do not run the official/native FLMV or R_mix341 checker. Python SHA-256 source 62747840ba4aeadf9b4918e41c275f0d1fd89eda842e6b32930d33d592d11a61; JS source 5c40e0f104f4b5ddca0b56f637e9b212ecfdbf5a337ecc9188960c78edda98bc. Source and raw paths under experiments/arc/lspv4_470_live_index_* and results/raw/arc/2026-11-07_0740_LSPV4_470_LIVE_INDEX_*.

## Resource / theorem / transfer ledger
Guest INDEX write + clear: 2L sequential transitions, zero non-index WORK accesses; the source content can be copied from a read-only input of L bits. A hypothetical correct total polynomial SAT decider can be wrapped with this reversible prologue while preserving SAT, UNSAT, malformed classifications, but this is only a *conditional construction*, not a decider. Host canonical arena: at least 2^k-1 simultaneous nonzero live records at the specified level; record IDs, unique table, references, head/index access, physical free list, cache and controller only increase cost. Guest logical inference nodes, proof evidence bits, candidate policy search, failed policies, local SAT child materializations, proof checking and output: none in this finite representation control. Such costs and all-phase peak, ancestor/child buffers and source auth must be included for a full solver.

Published hard-family control remains odd-charge cubic-expander Tseitin strict 3-CNF with H vertices, 4H clauses, 3H/2 variables, encoded size Theta(H log H). Ben-Sasson and Wigderson's expansion-width method implies 2^Omega(H) ordinary shared-DAG Resolution size on suitable expanders; GF(2) Gaussian elimination remains a polynomial shortcut. No lower bound for R_mix341 or arbitrary SAT machines follows from this family or the INDEX witness. Haken PHP and Cook ER remain separate controls.

The all-phase materialization bound s'<=max(rho,eta,lambda,lambda*s) remains required. This result is material restricted evidence for [P2-A4] only. [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. Preserve the exact five roles, two Route A / three Route B, schedules, identities, historic R_mix341 grammar and inference weights; do not edit root main.tex without complete readback. P versus NP OPEN.

References: Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability* JACM 52 (2005), 835-865 §2.1; Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 48 (2001), 149-169; authenticated project paths above.
