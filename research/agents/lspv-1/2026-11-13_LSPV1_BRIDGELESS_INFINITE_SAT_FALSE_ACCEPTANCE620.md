# LSPV-1/620: Infinite bridgeless, all-source-essential SAT family falsely refuted by the archived /341 checker

**13 November 2026 PST | LSPV-1 General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED mathematical family + original-checker source-code acceptance argument, COMPUTATIONAL five-size hosted original-body replay. P versus NP OPEN.**

## One candidate and four falsifiers, fixed before the experiment

**Candidate 620.1.** For every integer k >= 6, a signed proper 3-CNF on the simple cubic, bridgeless, vertex-biconnected prism graph C_k x K_2 can have 2^k genuine satisfying assignments and nevertheless have every one of its 8k original source clauses individually essential. The same *in-band* source can be packaged as a complete 8k-1-paid-record purported contradiction accepted by the unchanged recovered /341 checker, subject to finite JavaScript runtime representation and resource capacity. The resulting certificate is NOT a mathematical UNSAT proof.

F1. The prism is not cubic/bridgeless/biconnected, or deleting one original clause destroys the claimed independent witness.

F2. The modified source constraint matrix is not full row rank, or the row matrix after pinning three incident edges fails the V+2 rank/consistency condition.

F3. The unmodified recovered checker rejects a complete packet at one of the tested sizes, or a source/AND3/XOR/deletion obligation is silently omitted.

F4. Replacing either malformed charge by numeric zero, replacing a String terminal support with its numeric edge array, or corrupting a premise/terminal is still accepted.

F1/F2 are excluded by the all-k graph/rank proof below and finite exact Gaussian verification. Five positive original-body checker runs exclude F3 for k=6,7,8,9,10; eight precise negative controls exclude F4 in the tested k=6 packet.

## Corpus and provenance

Read current root proof1.txt (blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343), proof2.txt (blob 930c5eeddafce656717f28055a7a9a755f44737c through immutable blob), issue #3, AGENTS.md, CODEX.md, the pnp-research skill, current LSPV-1/619, LSPV-2/599, LSPV-3/609 and /614, LSPV-4/586 and LSPV-5/524. Historical LSPV-1/539-549, LSPV-2/539 and /549, LSPV-3/539 and /549, and LSPV-4/539 and /549 were cross-checked for distinct models, cost and old controls. Source authority: experiments/arc/lspv2_341_independent_verify.js, Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0; this is NOT the full historical R_mix341 checker. The distinct archived /386 checker handles signed SOURCE, paid DEF ownership/facets and RES, without authenticating mixed transitions.

**Prior art:** LSPV-1/615 gives a scalable checker-accepted SAT family using bridged graphs; LSPV-1/618 proves a bridgeless soundness condition with at most one exceptional charge; LSPV-1/619 supplies one 12-vertex bridgeless, all-source-essential counterexample with two exceptional charges. LSPV-3/609 already proves the operational-goal versus semantic-UNSAT impossibility; this report does not reclaim it. **The increment in /620 is the all-k bridgeless/all-essential exact model-count theorem plus a uniform original-checker false-certificate compiler and five-size replay.** The k=6 base reproduces /619's 64 SAT models, 16 deletion witnesses per clause and 5,583 native assertions. It is not a new distinct k=6 fixture.

## Theorem 620.1: exact infinite mathematical source family

For integer k >= 6, let G_k=C_k x K_2 have top vertices T_i, bottom vertices B_i (0 <= i < k), top and bottom ring edges and vertical spokes T_i B_i. Put r=floor(k/2). Designate exceptional vertices t=T_0 and s=B_r. Define V=2k and E=3k.

For every ordinary vertex v impose its three-edge parity equation with prescribed RHS q_v, where q_{T_1}=1 and every other q_v=0. At t and s, impose **only the parity of their two horizontal ring edges**, omitting their vertical spoke. Encode each local equation by four original signed width-three clauses, one forbidding each of the four incompatible assignments of its **three incident Boolean edges**. Thus the exceptional two-edge equations are each still represented by four proper, distinct three-literal clauses, and F_k has precisely 4V=8k clauses.

Let B'_k be the V x E binary matrix of these equations. Then

$$
\operatorname{rank}_{\mathbb F_2}B'_k=V=2k,\qquad
\#\operatorname{SAT}(F_k)=2^{E-V}=2^k.
$$

For EVERY original clause C in F_k, the formula F_k\setminus\{C\} has exactly

$$
2^{E-V-2}=2^{k-2}
$$

assignments falsifying C and satisfying every other original clause. Thus **all 8k source clauses are individually essential** despite the original formula being SAT. The prism graph is cubic, bridgeless and vertex-biconnected for all k >= 6.

**Proof.** Introduce a formal ground vertex *, and replace the *removed incidence* at t on spoke T_0 B_0 by an edge *B_0, and the removed incidence at s on spoke T_r B_r by an edge *T_r. Keep every other original edge. The reduced incidence matrix of this augmented graph H_k, deleting the ground row, is exactly B'_k. The two complete horizontal rings, together with k-2 remaining normal spokes, are connected, and the two ground edges attach * to the rings. Therefore H_k is connected. The reduced binary incidence of a connected graph has rank V, proving the first formula and consistency of every RHS q. Since E-V=k, there are exactly 2^k solutions.

Fix any vertex v and one of its four incompatible local three-bit assignments a. Pin all three *original* incident edge bits to a and remove the row for v, which is automatically satisfied after toggling q_v because a violates exactly that local parity equation. The residual incidence graph has all vertices except v and the ground *. Each horizontal ring remains a cycle or a connected path after deleting at most one vertex. Of the k-2 normal vertical spokes, at least k-3 >=3 remain unpinned, so the two remaining rings are connected. The two exceptional original spokes are disjoint; pinning all three original edges incident to v removes at most one of the two ground edges, so * remains connected to a ring. Thus the residual reduced incidence matrix has rank V-1. Its E-3 unpinned columns give exactly 2^{(E-3)-(V-1)}=2^{k-2} solutions for EVERY RHS. Each such solution falsifies the selected clause and, because it gives a distinct three-bit local assignment, satisfies the other three clauses at v and every clause at every other vertex. Finally, the prism has connected rings and at least k-1 surviving spokes after any one vertex deletion and remains connected after any edge deletion. QED.

The rank argument is a symbolic proof for all k >= 6; finite computation is a regression test rather than the logical basis.

## Theorem 620.2: accepted operational false-proof family (restricted to archived /341)

Number the edges so that the incident supports of t and s are [0,1,10] and [2,3,12], respectively. The explicit compiler fixes these names and chooses the remaining names bijectively. Supply the actual signed F_k clauses as the in-band SOURCE fields, with checker charges at t and s **String "0"** and all other charges the intended numeric q_v.

For each vertex, three paid binary AND3 records conjoin its four original signed clause factors. At t, set the final AND3 support to String "102"; at s, set it to String "123". At every other vertex, keep the genuine numeric support Array. Associate to each vertex a row claiming full three-edge parity with RHS q_v. XOR these V claimed rows with V-1 paid XOR records, yielding a zero-mask RHS-one terminal row. Every original SOURCE node is an ancestor. Include a valid per-clause deletion witness from Theorem 620.1 and the zero all-even witness.

The unchanged checker source verifies that (a) its charge XOR bitwise-coerces both malformed String zeros to 0, while its local numeric-parity versus charge strict inequality accepts all exceptional forbidden patterns; (b) its String.support membership checks recognize 0,1,10 inside "102" and 2,3,12 inside "123"; (c) its local truth-table evaluator writes only single-character indices 0,1,2 or 1,2,3, never actual edges 10 or 12, leaving the omitted spoke bit fixed to zero during row testing; (d) the resulting two-edge source truth tables appear identical to the checker to full three-edge parity rows with the omitted spoke fixed to zero; and (e) all claimed full three-edge row masks XOR to zero while the RHS XOR equals one. The original checker independently brute-forces source SAT **only when E<=15**, whereas this family begins at E=18.

Thus, for every constructible k>=6 within the concrete JavaScript representation/resource bounds, the source-code checks admit a complete 4V-1=8k-1-paid-record false refutation. There are no branching, DEF, LOCAL-CONVERT, Resolution or paid sharing cross-rule claims. The compact packet has polynomial, O(k^2 + k log k), evidence length because the 8k deletion witnesses each contain 3k bits. Logical paid work, source/certificate bits, actual time, checker assertions, span and peak space remain distinct.

**Crucial:** the checker returns its field certifiedMinimum=8k-1 for bridgeless instances, but this is merely its fixed-record count and claimed minimum; F_k is SAT and has no sound UNSAT refutation. This does not establish any lower bound on the authentic full mixed calculus.

## Computational original-body evidence and falsifiers

The committed generator and complete Node OS replayer are:

- experiments/arc/lspv1_620_bridgeless_infinite_false_acceptance.cjs (Git blob bc5ec658631d3bee32963009c2578fc79a3cc0d8)
- results/raw/arc/2026-11-13_LSPV1_620_BRIDGELESS_SCALABLE_HOSTED_RAW.json (Git blob 2b23196072b87f2acb04fbe9b4c1acceb903b8e2)
- results/raw/arc/2026-11-13_LSPV1_620_K6_SAT_ACCEPTED.json (Git blob 711ae18dc62f4eebaf355cb94fc9c595702e8571)

The exact, unchanged original checker body was executed in hosted V8, with only its filesystem input and output adapters replaced:

| k | V | E | Actual SAT models | Deletion models per clause | Paid records | Original assertions | Result |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 6 | 12 | 18 | 64 | 16 | 47 | 5,583 | ACCEPT |
| 7 | 14 | 21 | 128 | 32 | 55 | 6,949 | ACCEPT |
| 8 | 16 | 24 | 256 | 64 | 63 | 8,443 | ACCEPT |
| 9 | 18 | 27 | 512 | 128 | 71 | 10,065 | ACCEPT |
| 10 | 20 | 30 | 1,024 | 256 | 79 | 11,815 | ACCEPT |

Eight k=6 hostile mutations were rejected: either exceptional charge to numeric 0, either terminal String.support to its numeric edge Array, incorrect AND3 truth table, flipped terminal GF(2) RHS, invalid signed SOURCE variable, and corrupted deletion witness. Source rank, E, V, and all clause-deletion model counts were tested exactly by the compiler's GF(2) elimination. All five positive packets preserve the full provenance/shared source ancestry and mandatory AND3 obligations.

**Verification limits:** The exact committed OS-Node reproducer was created, parsed as JavaScript and verified by GitHub content readback, but it has not been run as an independent Node operating-system subprocess in this run. No complete historical R_mix341 checker, external source commitment or cross-rule transition was authenticated. The hosted checker is the genuine archived /341 body, not a mathematical soundness oracle.

## Dependencies and research consequence

[P2-D1] OPEN. This is substantive evidence about the recovered accepted-byte language and the failure of source-soundness in a scalable biconnected family. The missing full historical accepted-byte calculus is still not authenticated. Unknown rules must be included as MAY transitions, not dropped.

[P2-C3] OPEN. If abstracting original checker acceptance, all these false refutations are genuine operational paths and cannot be refined away as spurious; mathematical UNSAT must be a separate, source-bound goal (prior LSPV-3/609). Charge every distinct shared paid owner once, retain typed charge/support semantics and original signed provenance. No cost-sound all-rule historical abstraction is established.

[P2-B1] OPEN. The source is a rich SAT control with an O(k) *false* checker refutation. It defeats proposed source-sound acceptance inference, not all-rule UNSAT lower bounds. Maintain all legal GF(2), extension, branching, reuse and reconvergence shortcuts. No all-input superpolynomial lower bound.

[P2-B2/B3] OPEN separately. Neither any checker, abstract solver, nor SAT in P transfers polynomial minimal native work without an explicit same-calculus theorem. P1-01/03/04 remain OPEN.

## Prior primary literature (model boundaries)

1. Cook and Reckhow (1979), The Relative Efficiency of Propositional Proof Systems, *J. Symbolic Logic* 44:36-50. https://doi.org/10.2307/2273702 . A legitimate propositional proof system must be sound; this recovered verifier is not a sound source-bound refutation system.
2. Cousot and Cousot (1977), Abstract Interpretation: A Unified Lattice Model for Static Analysis, POPL, pp.238-252. https://doi.org/10.1145/512950.512973 . MAY abstraction can cover operational checker paths without validating their mathematical interpretation.
3. Clarke et al. (2000), Counterexample-Guided Abstraction Refinement, CAV. https://doi.org/10.1007/10722167_15 . Concretely accepted paths are not spurious relative to operational acceptance.
4. Urquhart (1987), Hard Examples for Resolution, JACM 34:209-219. https://doi.org/10.1145/7531.8928 . Resolution-only lower bounds do not transfer to this mixed Boolean/GF(2) path.

**TRACKERS REVIEWED; NO MATERIAL PROOF-NODE STATUS CHANGE.** Neither root tracker is strengthened by an original checker accepting SAT. Do not create or reschedule roles. LSPV-5 independent falsification remains required.
