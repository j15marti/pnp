# LSPV-3/552: Parametric SAT-source acceptance in the recovered /341 fixture checker

**2026-11-10 13:27 PST | Hypergraph & Proof Certificates, Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Affected nodes:** P2-D1, P2-C3; new material evidence P2-L3-552. P2-B1, P2-B2/B3, P1-01/03/04 OPEN. This finding concerns the pinned recovered SOURCE/AND3/XOR *fixture checker*, NOT the intended full historical R_mix341 calculus.

## IDEA -> SEARCH -> ITERATE and falsifiers

Candidate: Extend the previous LSPV-3/551 accepted satisfiable original CNF into a parameterized checker-accepted family, and prove the sharp minimum cubic size for any genuine numeric signed SAT source that can evade the recovered checker's small-source exhaustive test. Four falsifiers: F1 triangle expansion breaks cubicity, connectedness, the bridge or stable source edge indices; F2 its explicit assignment ceases to satisfy all clauses; F3 original checker rejects enlarged packets or repairs a malformed charge/support alias; F4 a smaller cubic graph escapes exhaustive source SAT verification. F1-F3 were contradicted by six original-code V8 positive controls and independent Python structural/SAT tests; F4 was excluded by inspecting and proving the exhaustive-branch condition of the pinned original code.

Pinned producer: experiments/arc/lspv2_341_mixed_tseitin_min_dag.js, Git blob 4081022e8a3841d79f751a3d3a7a10decbb026da. Pinned checker: experiments/arc/lspv2_341_independent_verify.js, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. Original SAT packet: LSPV-3/551, blob 706947c767361e7c979b8208677eb983d33838f4. Original checker logic is unmodified, with only CLI I/O adapted for V8 testing.

## Theorem 552.1: parameterized SAT-source acceptance

For each t>=0 for which its finite JavaScript arrays and numeric indices are representable, there is an explicit connected simple cubic graph with

$$
V_t=12+2t,\qquad E_t=18+3t
$$

and an original proper signed strict-three CNF F_t with

$$
m_t=4V_t=48+8t
$$

numeric signed clauses. It is SAT, yet the original recovered checker accepts a fake terminal 0=1 with exactly

$$
q_t=4V_t-1=47+8t
$$

distinct paid AND3/XOR records. This is a uniform combinatorial scheme. Literal unbounded t is not executable on a fixed finite-capacity JS runtime.

**Proof.** Begin with the bridged 12-vertex graph in /551. Vertex 0 has original incident edge IDs [0,1,12]. The four edges [0,2,5,12] form a cycle disjoint from vertex 8 and bridge edge 17. Expand vertex 8 into a triangle: retain one of its incident original edges, move the endpoints of the other two to new vertices a,b, and add edges (8,a),(a,b),(b,8). This preserves old edge identifiers, old cycle, bridge and simplicity, connectivity and all cubic degrees; it adds two vertices and three edges. Repetition proves the V_t and E_t formulas.

At vertex 0 use four signed 3-clauses forbidding local patterns 000,001,110,111 on the [0,1,12] support. They impose x_0 XOR x_1=1, independently of x_12. Every other vertex retains the four even-parity Tseitin clauses. Assign exactly cycle edges [0,2,5,12] the value 1 and all others 0. Every vertex except 0 sees even parity; vertex 0 has (x_0,x_1,x_12)=(1,0,1), satisfying x_0 XOR x_1=1. Hence every clause is satisfied.

Generate the original odd-charge proof skeleton using the pinned producer. Set charge[0] to string "1", not numeric 1; set AND3 node d0.table=238, d1.table=230, and d2.table=102, d2.support="012" (string, not [0,1,12]). Set deletion assignments null and the essential count to zero; the graph retains a bridge so the checker does not require every clause essential. The original checker bitwise charge XOR coerces string "1" to one, but its strict local source comparison with that string fails to authenticate the four vertex-0 parity clauses. Its string support check accepts substring 12 in "012", while iteration over the support uses character indices 0,1,2 instead of original indices 0,1,12. It therefore accepts the false affine alias x_0 XOR x_1 XOR x_12=1. On the exhibited SAT assignment that alias is false. The remaining generated vertex rows XOR to 0=1 and the checker accepts. The proof is about original JS execution semantics, not the intended sound proof rules.

**Theorem 552.2: sharp minimal cubic threshold.** In the original checker's accepted fixture language, restrict original clauses to genuine numeric signed literals, with true CNF SAT interpreted by its clauseSat predicate. If E<=15 the unchanged verifier enumerates all 2^E assignments and asserts that the number of satisfying assignments is zero, so it rejects every genuinely SAT source. In a cubic graph, 2E=3V, V is even, and E is divisible by three. The first possible edge count above 15 is E=18, V=12. The checker additionally demands 4V clauses and 4V-1 proof records. Therefore every accepted SAT source in this explicitly restricted numeric-cubic class satisfies

$$
\boxed{V\ge12,\quad E\ge18,\quad m\ge48,\quad q\ge47.}
$$

The /551 t=0 example attains all four minima. This is NOT a lower bound on legitimate native proofs, a claim of minimum byte encoding or an arbitrary checker theorem.

## Original-code and independent controls

| t | V | E | SAT clauses | paid records | original checker assertions | five hostile mutations |
|---:|---:|---:|---:|---:|---:|---|
| 0 | 12 | 18 | 48/48 | 47 | 2272 | REJECT |
| 1 | 14 | 21 | 56/56 | 55 | 2416 | REJECT |
| 2 | 16 | 24 | 64/64 | 63 | 2560 | REJECT |
| 3 | 18 | 27 | 72/72 | 71 | 2704 | REJECT |
| 4 | 20 | 30 | 80/80 | 79 | 2848 | REJECT |
| 5 | 22 | 33 | 88/88 | 87 | 2992 | REJECT |

Each mutation was tried at each size: change only charge to numeric 1; change only support to exact integer array; corrupt AND3 table; corrupt terminal XOR; corrupt signed source incidence. All 30 were rejected by the original checker. A separate independent Python graph/source constructor verified all six SAT witnesses, graph properties and the bridge. The new exact V=14 packet (41,582 UTF-8 characters) was committed, refetched and independently replayed with the original unchanged checker: ACCEPT with 2,416 assertions, despite a 21-bit witness satisfying all 56 source clauses. The standalone Node script was syntax compiled but not run as a native OS subprocess. No actual FLMV machine or historical full mixed checker was run.

## Abstract-interpretation and lower-bound implications

A proof-state abstraction must preserve original source identity, paid global node identities, shared-DAG dependencies, contexts, freshness and all actual legal rules. The recovered checker's bare ACCEPT cannot be taken as an entailment certificate: this parameterized family supplies concrete accepted configurations with SAT original sources. A sound mathematical abstraction must reject these malformed accepted packets through an independently proved type/source/factor boundary. It must NOT delete legitimate Resolution, DEF/facet, LOCAL-CONVERT, export/private, branch/discharge, reconvergence or compact algebraic transitions. The separate LSPV-2/539 strict SOURCE/AND3/XOR reference checker is a useful sound restricted semantic system but is not the historical full byte grammar.

Logical paid work q_t, source and evidence bits, proof discovery, sequential execution, parallel span and actual simultaneous peak space remain distinct. Replaying original V8 code materialized JS host objects, with no FLMV memory bound. The construction does not establish a full-calculus P2-C3 invariant, P2-B1 superpolynomial W_R lower bound or P2-B2/B3 transfer.

## Search, duplication and provenance

Original issue #3, AGENTS.md, CODEX.md, repo research skill, both complete root proof trackers, older/new native-focus handoffs, current LSPV-2/537-539, LSPV-3/550-551, LSPV-1/553-554, LSPV-4/522-523, the original /341 source and checker, latest Grok progress and Claude world ledger were reviewed. The previously published /551 one-size accepted SAT certificate is credited. The new result proves an iterative source-preserving family, supplies a new exact 14-vertex accepted packet and establishes the sharp native-fixture E threshold.

Change-aware actual reads: konard/p-vs-np README (blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95) and scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5); meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f); tanyongkiam/cake_lpr README (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c). None specifies the historical full R_mix341 accepted-byte language. Primary literature: Cook and Reckhow, Journal of Symbolic Logic 44 (1979), DOI 10.2307/2273702; Cousot and Cousot, POPL 1977, DOI 10.1145/512950.512973; Ben-Sasson and Wigderson, JACM 48 (2001), DOI 10.1145/375827.375835 (Resolution-only scope).

## Reproducibility and publication

Producer/checker replay: experiments/arc/lspv3_552_parametric_native_sat_forgery.cjs. Independent graph/source script: experiments/arc/lspv3_552_independent_source_witness.py. Original-V8 raw ledger: results/raw/arc/2026-11-10_1327_LSPV3_552_PARAMETRIC_NATIVE_RAW.json. Exact larger accepted-byte packet: results/raw/arc/2026-11-10_1327_LSPV3_552_ACCEPTED_SAT_V14_PACKET.json. Published files were SHA/readback verified. The full native grammar, its true sound checker and all unrestricted proof obligations remain OPEN.

**Actual advance:** parameterized source-soundness failure of the recovered checker, sharp minimum source size, and a new accepted larger SAT packet. **Precise gap:** authenticate the actual complete R_mix341 grammar, then prove cost-sound whole-DAG transformers and an all-rule lower bound. P versus NP OPEN.
