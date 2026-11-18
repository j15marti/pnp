# SIGMA2 / T5 STATICSELECTOR34: quantified universal-selector firewall

Date: 2026-11-18, America/Los_Angeles.
Owner: PNP Sigma2 Circuit Agent.
Classification: PROVED (elementary general theorems), COMPUTATION VERIFIED (one source), CONDITIONAL (hypothetical SAT self-reduction), OPEN (unrestricted witness time lower bound; P vs NP).

## PROPOSE, SEARCH, BUILD
Before literature review, propose and attempt to falsify: on intrinsically edge-minimal UNSAT T5 graphs, every fixed collection of bad-edge universal challenges must contain every edge, although a candidate-dependent selector can be computed cheaply. Require exact source-preserving witness and quantified CNF audits.

Prior repository files directly fetched: research/agents/tmr-2/2026-11-18_1212_TMR2_T5_BICYCLIC_TRANSFER091.md; research/agents/cross-track/2026-11-18_0024_T5_PC_CRITICAL56_STATUS.md; research/agents/cross-track/2026-11-18_1028_T5_BIPARTITE_GIRTH8_WITNESS67_STATUS.md; research/agents/sigma-primary/2026-11-18_GATEFIBER33.md. Primary literature: Bang-Jensen/Hell/MacGillivray 1988, DOI 10.1137/0401029; Kayll/Morris 2023, DOI 10.55016/ojs/cdm.v18i2.73457; Williams 2024, DOI 10.1145/3618260.3649723.

## THEOREM 34A (static bad-edge hitting number)
Fix T5 on Z5, R(a,b) iff (b-a) modulo 5 is 1 or 3. Let H=(V,E), n vertices, m>=2 original arcs, be intrinsically edge-minimal UNSAT, meaning H is UNSAT and every H-e is SAT. For a coloring c, write Bad_H(c) for its set of violated arcs.

For every e, choose c_e satisfying H-e. It must violate e or it would color H, hence Bad_H(c_e)={e}. Consequently the only fixed, candidate-independent subset S of E that intersects Bad_H(c) for every c is S=E: omitting e lets c_e evade S. The minimum fixed universal edge-challenge menu has exactly m entries. Rotations c_e+t modulo 5 give five distinct singleton-violation assignments per edge, totaling at least 5m distinct assignments. All statements are proved for arbitrary edge-critical T5 H. They do NOT give an unrestricted time, witness-search, circuit, information, or communication lower bound.

## THEOREM 34B (cheap adaptive universal response)
For arbitrary H and any candidate coloring B, a deterministic source scan finds the first violated original arc index or returns NONE if B is satisfying. On an UNSAT H it returns a valid arc for all B. Its output uses ceil(log2 m) bits. A fixed-H priority-encoder circuit is O(m log m) gates; a word-RAM scan after charged source/color loading uses O(N+m) operations, and naive sequential-tape indexing is polynomial (e.g. O(m(n+N)) bit operations). An adaptive edge-selector therefore defeats the inference from m necessary static selectors to expensive adaptive challenge selection. Computing the selector on any input does not prove it always returns an edge; the latter universal claim is exactly UNSAT(H).

## Exact criticality formula and quantifier swaps
Let W contain one legal original 5-color assignment W_e per deletion H-e. CheckDel(W) verifies all original constraints outside e, for every e. Then:

Critical(H) iff EXISTS W FORALL B [
   CheckDel(W) AND
   (NOT ValidColor(B) OR OR_(e in E) NOT R(B[u_e],B[v_e]))
].

This is semantically a Sigma2 Boolean circuit QBF. The criticality language is in DP (all deletions SAT is NP with a polynomial witness table, H UNSAT is coNP); no DP-hardness or Sigma2-hardness is claimed.

With a selected failed-edge index I, the equivalent indexed formula has prefix EXISTS W FORALL B EXISTS I and matrix CheckDel(W) AND (NOT ValidColor(B) OR (I<m AND BadEdge(B,I))). Syntactically E-A-E, it projects to the Sigma2 predicate because I implements a disjunction. A faithful gate-level Tseitin CNF has prefix EXISTS W FORALL B EXISTS I,T with functional trace T after B; hoisting T before B is invalid.

The quantified swaps are refuted on any edge-critical H: FORALL e EXISTS c_e Sat(H-e) is true but EXISTS c FORALL e Sat(H-e,c) is false, since for m>=2 every edge survives another deletion. FORALL B EXISTS I BadEdge(B,I) is true but EXISTS I FORALL B BadEdge(B,I) is false, because each individual T5 arc can be satisfied. Every challenge B refers to a single shared original H, not a newly generated source.

## Finite experiment, reconstructed from original TMR-2/091 paths
Four internally disjoint u=0 to v=1 paths have traversal orientation words ++, +++, ++-, ---. This yields a genuine connected 9-vertex 11-arc oriented graph, undirected girth 5 and cycle rank 3. Its endpoint-difference T5 path-cofactor rows are
 ++   (0,1,1,0,2)
 +++  (3,0,3,1,1)
 ++-  (1,3,0,3,1)
 ---  (3,1,1,3,0).
The four-way product is zero at every difference d in Z5, an explicit UNSAT certificate. Root-gauge DFS found a legal coloring of H-e for every one of the 11 edges, with exact original-label counts in sorted arc order (180,60,60,60,40,180,60,60,60,40,40). Every such coloring violates precisely its designated missing edge in H.

The exhaustive independent coloring loop covered all 5^9=1,953,125 original-label assignments via 390,625 normalized root-zero representatives and fivefold rotation; no coloring satisfies H. Exactly 840 colorings violate one and only one arc, with the same per-edge counts, and the first-violation scan classifies every coloring. There are at least 55 explicit distinct rotated edge-deletion witnesses. Our different 76-byte ASCII source serialization of this graph, with sorted records, has SHA-256 d00bdd387422a708c592ba17b6a2bab5a53c96d26804502994e32e34f209f5e4; TMR-2/091 reported a different 112-byte serialization of the same four-path graph.

## Exact QDIMACS and independent verifier
Generated an actual functional 3-CNF with prefix EXISTS W (297 bits, including 33 pinned root bits), FORALL B (27 bits), EXISTS I (4 bits), EXISTS T (3744 gate bits). Totals: 4072 variables, 11266 clauses of length at most three, exactly 176127 ASCII bytes. Invalid 3-bit color codes 5,6,7 are explicitly guarded. Each gate is fully biconditional Tseitin, so T is uniquely determined by W,B,I and cannot generally be moved before B.

A separate QDIMACS parser and functional CNF checker completed 1157 pinned checks, including all 16 indices for all 11 singleton-bad-edge witness assignments, 800 random valid B, 120 invalid B, 50 corrupted witness tables and 11 designated-deletion comparisons. Zero mismatches. Trace values change with the universal B. The universal space of 2^27 raw bit strings was not exhaustively enumerated, but all 5^9 legal original colorings were covered by the independently implemented finite loop and the invalid-code implication was separately checked.

The designated YES input G=H-e has its coloring c_e satisfying every surviving edge; it defeats all legal bad-edge selectors for G. For NO H, every valid B has a bad edge. This is a source-faithful distinction, not an arbitrary-machine hardness result.

## Charged cost and handoff
On explicitly charged vertex/edge records, table length 3nm bits, or 3m(n-1) with a connected-source root gauge; B is 3n bits and I is ceil(log2 m). All source scans, validity checks, gate compilation, certificate size, SAT access and memory are charged. Conditional on a deterministic SAT solver running O(L^d), standard T5-to-CNF partial-assignment checks extract a T5 witness with at most 1+5n actual SAT queries of L=O(N log N) bits and crude total cost O(n(N log N)^d+poly(N,n)). This is not an iterable exponent contraction f(d)<d.

NEXT: test the 33-vertex/44-arc girth-eight critical source from TMR-2/079; investigate an all-input, source-preserving many-one reduction to intrinsically critical designated deletions, charging the original source, criticalization, and witness extraction. Falsify with Z5 transfer/flow, path cofactors, separator DP, graph syntax recognition, short certificates, source-aware algorithms and padding. Do not attach a fixed hard gadget to unrelated NP-hard material or transfer a static-selector bound to unrestricted uniform machine time.

P versus NP OPEN.

References:
[1] Bang-Jensen, Hell, MacGillivray (1988), The Complexity of Colouring by Semicomplete Digraphs, https://doi.org/10.1137/0401029
[2] Kayll, Morris (2023), On Colouring Oriented Graphs of Large Girth, https://doi.org/10.55016/ojs/cdm.v18i2.73457
[3] Williams (2024), Self-Improvement for Circuit-Analysis Problems, https://doi.org/10.1145/3618260.3649723
