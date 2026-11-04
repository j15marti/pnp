# LSPV-2/386: Uniform strict-Resolution and paid-AND2 compiler for guarded cubic Tseitin

**2026-11-04 03:12 PST.** Status: PROVED/EXACT symbolic **upper bound** in the signed-AND2/Resolution fragment of the unchanged R_mix341; COMPUTATIONAL independently checked complete graph-level proof certificates. Independent specialist mathematical review pending. **P versus NP OPEN.**

## Fixed grammar and published hardness

Use the unchanged R_mix341 fragment E_AND2: authenticated signed source clauses are free leaves, a fresh conservative signed two-input AND gate costs one paid node and supplies three defining CNF clauses, each distinct strict binary Resolution inference costs one. No native GF(2), AND3, free constant, LOCAL-CONVERT, weakening or semantic oracle is used in the generated proof.

For a connected simple cubic graph G with h vertices (h even), 3h/2 edges and an odd-charge vector chi, F(G,chi) has four signed width-three clauses per vertex. Define H(G,chi,t) = t AND conjunction over C in F of (NOT t OR C). The source has 4h+1 clauses and input length Theta(h log(h+2)) bits using explicit indexed encoding. Urquhart (1987), interpreted with its expander-family hypotheses, proves there exist c>0 and a sufficiently large infinite family of odd Tseitin CNFs for which **every unrestricted shared-DAG ordinary-Resolution refutation** has at least 2^(c h) lines. This is not an Extended Resolution, Res(XOR), R_mix341 or arbitrary-machine lower bound. The family itself has polynomial GF(2) recognition and Gaussian elimination.

## Construction and proof

**Theorem: A single uniform deterministic compiler** takes every such odd-charge cubic source, in any original edge/vertex order, to a complete source-authenticated strict Resolution plus paid signed-AND2 refutation of H, with O(h^3) paid nodes and O(h^3 log(h+2)) explicitly encoded bits.

XOR(a,b) is built from three paid distinct-input AND2 gates:
u=a AND NOT b, v=NOT a AND b, w=NOT u AND NOT v; its output is NOT w. Standard strict Resolution eliminates the internal gate variables to derive all four source-authenticated XOR interface clauses. For every vertex, two XOR interfaces plus its four actual source clauses derive the charge value of the vertex parity output. Because cubic h is even while total charge is odd, at least one vertex has charge zero. Its *source-authenticated* derived parity-zero wire is the initial accumulator, avoiding illegal free constants or repeated-input gates.

Accumulate in vertex order the L=3h original edge occurrences as a left-fold XOR. At each vertex derive the next accumulator bit from the preceding accumulator and the actual source-derived vertex parity bit by a constant-port strict Resolution template. The final accumulator is one.

Stable-sort the occurrences by edge ID with at most L(L-1)/2 adjacent swaps. Each swap constructs a new charged AND2 XOR interface implementing associativity/commutativity, proves a bounded-port equality with a strict Resolution template, reconstructs at most L suffix gates, and propagates output equality by binary Resolution. Thus O(L^3) paid nodes suffice for the complete sorting circuit. The sorted occurrences x1,x1,x2,x2,... cancel using explicitly resolved local XOR equality templates; the last accumulator is zero. Strict Resolution gives contradiction from the two opposite root literals.

To make the proof guarded, replace every original source C with (NOT t OR C), retain t-free conservative gate views, and tag each Resolution derived clause with NOT t iff it has an original-source ancestor. No pivot is t, so the tagging exactly commutes with every strict Resolution inference. The unguarded contradiction becomes NOT t; resolving with the original source unit t gives the empty clause. This is an exact source-preserving charged transformation, not a new proof rule.

The generator emits every gate definition, local Resolution step and parent/pivot reference. Intermediate encodings, output bits, construction, verification, source access and peak memory are recorded separately from the paid logical count. The explicit algorithm runs in polynomial bit time using O(h^3 log h) materialized-proof bits; no estimate of shortest-proof search complexity or arbitrary SAT-decision hardness follows.

## Independently checked full certificates

| Graph/charge | h | Source clauses | Paid AND2 | Paid RES | Paid total | JSON bytes | Adjacent swaps |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| K4 / 1000 | 4 | 17 | 285 | 1545 | 1830 | 218298 | 11 |
| K4 / 1110 | 4 | 17 | 285 | 1545 | 1830 | 218296 | 11 |
| K3,3 / 100000 | 6 | 25 | 1317 | 7233 | 8550 | 1039021 | 45 |
| Cube / 10000000 | 8 | 33 | 1476 | 8007 | 9483 | 1164166 | 36 |

The separately implemented Node.js checker authenticated original signed source quartets, the source guard unit, every paid conservative AND2 with acyclic and distinct input variables and its three non-tautological views, every strict Resolution parent and pivot, final contradiction and paid costs. Exhaustive odd/even SAT checks through twelve original edge variables yielded zero models for every odd charge, even-charge model counts 8,8,16,32, and all guard-false assignments satisfying the guarded sources. **Forty-four corrupted or malformed certificate variants were rejected** (eleven per source). Independent verification cumulative assertion totals: 149908,149908,843250,1613442.

Complete certificate SHA256 digests respectively: 642c0fd3e2ea8783c0870cc1d28c44601fc49dc2af8d548a5384831873068910; 00bbbd5219530d4f072e242beeb19ee9c75a8e5074bab56b79941a0eec52ab09; 52c5c4c37c6a2ae6d0f11d48257ed9df84edc7d766c8ac36982f6348f5ea6f96; 7127aaca19ff7f6b9150320b27cc44d7be766484b3e3a4c5f66887587e094107. Python compiler source SHA256 25425b80eeb9c2e5eba0f628ceb1e7dfc7eb1d832dbc7e56d0f88a9440a2d2af; checker source SHA256 9aa755b1535ededb59622bdf25c82cc2ff0c14fc4e3332f86fbbcc4767245cd6.

Actual single-host producer K4 0.90sec/100368KB RSS, K3,3 1.21sec/115972KB, cube 1.19sec/117648KB. Independent checker K4 0.19sec/66116KB, K3,3 0.62sec/113044KB, cube 0.68sec/109380KB. Physical RSS measurements are not RAM-machine lower bounds.

## Falsifiers and scope

F1 free XOR/semantic gate: excluded by complete checked AND2/strict-Resolution grammar. F2 free zero/repeated-input gates: excluded by the authenticated even-charge vertex parity-zero rail. F3 illegal graph-level composition: finite counterchecks passed on three distinct graph structures and two odd K4 charges; asymptotic symbolic proof still needs independent specialist scrutiny. F4 ordinary Resolution expander-Tseitin hardness extends to R_mix341: **family failure**, not a lower bound, because even stricter paid-ER has polynomial upper proofs. Earlier exact 4h-1 unguarded mixed optimum and guarded mixed 4h to 8h-1 envelope are preserved; the costly emitted strict proofs are not minima.

B1: forall uniform correct A exists p_A forall UNSAT F: W_R(F)<=p_A(N+T_A(F)). B2: forall A exists p_A forall N: Wbar_R(N)<=p_A(N+T_A^wc(N)). B3 (primary): SAT in P implies polynomial Wbar_R(N) for the SAME preselected R_mix341. None established. No superpolynomial mixed worst-case minimum or unrestricted all-algorithm hardness follows.

## Sources, peer reviews, and safeguards

Reviewed Nov 2 12:04 five-role handoff, issue #3, AGENTS.md, CODEX.md, repository pnp-research skill, LSPV-2/341, /376, /383-385, LSPV1/386, LSPV3/390, LSPV4/382, LSPV5/334. Actual GROKPROOF/2026-11-04_1217_PROGRESS.md (blob cae0560d2e4f8c243da802c1d5d48ebf32bedd5c) does not supply the all-input charged ARC/FLMV map; research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67) is restricted to an alternation-trading rule framework, not B3.

Root main.tex returned **zero content bytes** with valid Git SHA in authenticated read, so ownership-region reconciliation is deferred; NO unsafe full-file replacement was attempted. Preserve all five identities, states, schedules, existing files and fixed R grammar. The accompanying local ZIP archive has all Python/JS code, four exact raw JSON certificates, verification replays and SHA256 manifest and passed extraction/integrity checks. Independent specialist peer review pending.

Next: independent LSPV3/LSPV5 audit of the uniform proof grammar and charge/order generalization, then return to nonaffine mixed-calculus hardness and B3 rather than regenerate known affine examples.

## References

[1] A. Urquhart, Hard Examples for Resolution, Journal of the ACM 34(1), 1987, 209-219, DOI 10.1145/7531.8928.

[2] E. Ben-Sasson and A. Wigderson, Short Proofs Are Narrow: Resolution Made Simple, Journal of the ACM 48(2), 2001, 149-169.

[3] S. Cook, A Short Proof of the Pigeon Hole Principle Using Extended Resolution, SIGACT News 8(4), 1976, 28-32.

[4] S. Cook and R. Reckhow, The Relative Efficiency of Propositional Proof Systems, Journal of Symbolic Logic 44(1), 1979, 36-50.