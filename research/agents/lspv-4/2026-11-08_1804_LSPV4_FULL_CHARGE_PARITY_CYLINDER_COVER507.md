# LSPV-4/507 | Complete-charge Tseitin cylinder-cover firewall

**2026-11-08 18:04 PST | Route A | PROVED/RESTRICTED plus independent COMPUTATIONAL controls | P versus NP OPEN.**

Exact nodes: [P2-A4] new scoped resource-control evidence [P2-L4-507]. [P2-A2] universal contraction, [P2-A5] same-machine recursive applicability, [P1-01]/[P1-03]/[P1-04] all OPEN. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN.

## IDEA and predeclared falsifiers

Hypothesis: For a fixed connected cubic graph with H vertices, all 2^H charge assignments produce same-length original signed strict 3-CNF sources. Although SAT versus UNSAT is their easy total-charge parity, any deterministic correct decider's genuine completed INPUT-read trace cylinder intersects this 2^H-source set in precisely one source. Thus a cache that *only* reuses completed answers after matching exact trusted read cylinders cannot obtain cross-source hits. It needs 2^H terminal leaves for complete source-family coverage. This does not apply to code-aware algebra, legal incremental recomputation or shared internal computations.

Falsifiers: (F1) one vertex-charge flip does not invert the SAT label; (F2) the fixed-field 3-CNF source layout changes identifier positions or length instead of just a disjoint polarity quartet; (F3) a correct complete run can omit all four polarity positions of some vertex; (F4) two distinct charge patterns lie in one completed genuine cylinder. Independent finite tests and proof below test these precisely.

## SEARCH: actual research, primary sources and exact paths

Reviewed BOTH full root trackers (initial proof1 Git blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2 Git blob d40b17bd67d560eac034ef1dfe5a405368478f22), current coordination issue #3 and latest five-role comments, governing 2026-11-02_1204 five-role handoff (blob c3889a3e514ddbd747150dcb68607013a3b2d154), AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md. Peer LSPV-2/507 charged trace-trie report at research/agents/lspv-2/2026-11-08_1716_LSPV2_CHARGED_TRACE_TRIE507.md (blob c93fb2c603701fc84d28f359476f6e4ed402cc6e); LSPV-4/505 clipped monitor and LSPV-4/506 critical sign-bit star work. Actual GROKPROOF/2026-11-06_2316_PROGRESS.md (blob a20fb8b3640d7574faf238a4a83a021bb0984808) and Claude 2026-10-28_0924 world ledger (blob 79e4d4e7e0e3edff3aba8610852c45534bdde128) reviewed. Earlier parity-cache and trace-cylinder searches found related proposals, not a complete all-charge source proof; no novelty claim.

Required external change-aware files: konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and proofs/complexity/README.md blob 7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3 (its finite-machine formalization is not indexed FLMV); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and verify_residual_equivalence_barrier.py blob f204ac6009559c07602a43c400a0ee2ad47cb86d (different residual-obligation tests); MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (source generator); meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (external proof calculus); openai/math/CONTENTS.md blob 7e1ed90ac5a666f1bbecb22027387c4ad79e9d03 (not a same-machine simulation). Not an exhaustive audit of every repository. Google-branded search unavailable; public web search used.

Primary FLMV source: Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, https://lance.fortnow.com/papers/files/tst.pdf section 2.1 PDF page index 3 SCREENSHOT-INSPECTED. It charges WORK high-water and index erasings, and excludes indexed INPUT/OUTPUT from space. Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001) supply ordinary shared-DAG Resolution hardness on suitable cubic-expander Tseitin sources, **NOT** all-machine SAT hardness nor all R_mix341 rules. Acar/Blume/Donham, arXiv:1106.0478, separates memoization from PAID change propagation.

## Exact established family, grammar and theorem scope

Choose any connected simple cubic graph G=(V,E) with H vertices and m=3H/2 edge variables, numbered 1..m. For each vertex v with charge chi_v, impose the parity equation on its three incident edge variables, by exactly FOUR original signed proper three-literal clauses forbidding the four Boolean triples of parity different from chi_v. Order these four triples lexicographically and each triple's three literal identifiers increasingly. There are 4H original clauses, 12H signed literal records, no auxiliaries.

For the NEW independently specified fixed-field binary grammar, write an 8-bit marker A5, 12-bit H, 12-bit m and then 12H records containing w=ceil(log2(m+1)) bits of numeric variable ID plus one sign bit. The total is

$$
N=32+12H(w+1)=\Theta(H\log H).
$$

The header alone does NOT authenticate the graph: the complete fixed G clause/edge consistency is part of the source promise and independently checked in finite tests. This exact encoding is NOT byte-identical to LSPV-2/495; do not transfer prior source SHA-256 or assume the R_mix341 historical parser accepts it. The actual clauses are strict signed proper 3-CNF throughout.

For connected G, SAT(F_chi) iff the global XOR of vertex charges is zero, by incidence-matrix rank H-1 or a spanning-tree edge-flow witness. Suitable growing cubic expanders give exponentially hard **ordinary shared-DAG Resolution** odd-charge formulas; all odd charges on a fixed graph are isomorphic under variable complementation (differences have even parity and therefore are an edge boundary). The finite graphs K4/K3,3/Q3/Heawood are not an asymptotic hardness certificate. Gaussian elimination and code-aware source recognition are mandatory polynomial-time shortcut controls.

## ITERATE: singleton-cylinder theorem (PROVED/RESTRICTED)

For each v, the four lexicographically sorted forbidden triples for charge 0 and charge 1 are paired as 001/000, 010/011, 100/101, 111/110, respectively. In each pair the first two bits agree and the third bit flips. Therefore toggling chi_v flips **exactly the four third-literal polarity positions** Q_v in that vertex's source packet, with all identifiers, other sign bits, header bits and N unchanged. These disjoint quartets are indexed by v.

Let A be ANY deterministic total correct SAT/UNSAT/MALFORMED decider on the declared binary CNF encoding, with fixed fresh initial configuration and genuine completed INPUT-read trace on F_chi. For every v, the trace MUST observe at least one sign position in Q_v: if it did not, A's entire machine trajectory on F_chi XOR e_v would be identical, yet the SAT label must reverse. Now any other chi' differs from chi at some v. The trace already observed a Q_v position, and that bit differs on F_chi'; hence F_chi' does not lie in the genuine completed anchor cylinder. Therefore each completed read-trace answer cylinder intersects the complete charge family in exactly ONE source.

Consequences: a literal cache of complete trusted read traces and their answers cannot hit on any second DISTINCT charge source, regardless of optimal anchor ordering, indexing, trie compression or number of stored earlier anchors; all q distinct sources require q fresh guest executions unless an additional legal change-propagation/semantic process is performed. Complete cover requires at least 2^H distinct terminal leaves. The explicit parity-reading guest's full H-level binary trie has 2^(H+1)-1 nodes. This is 2^(Omega(N/log N)) growth as a **cache-leaf representation**, not computational hardness. On q separate fresh runs, at least qH source-bit observations are compulsory; this remains compatible with N^(11/10) local work when q=N^(3/5), H=Theta(N^(1/2)/log N). The theorem does not assert qH non-compressible persistent bits or hardness against all batching/computation strategies.

## Full resource ledger and shortcuts

For a literal completed-trace cache, all source reads, INDEX writes and erasures, WORK high-water, guest execution, source parsing, trace acquisition and authentication, failed misses, per-leaf trie/pointer construction, lookup, storage, references, retrieval, restarts, recomputation, output and simultaneous ancestor/child high-water must be charged separately. This workload supplies q misses and zero cross-charge hits; no free after-the-fact semantic oracle is allowed. A promised-family GF(2) recognizer needs only H sign observations, an XOR accumulator and O(log N) indexed-counter workspace if graph/record positions are uniformly recoverable. Authenticating independently supplied untrusted sources may cost O(N polylog N) time, and fallback to general SAT is NOT supplied. The direct easy algorithm disproves any interpretation of this cache cover as an all-algorithm exponential runtime/space lower bound.

No universal, both-label, malformed-aware, recursively iterable same-FLMV-machine solver-dependent contraction is established. In particular [P2-A2], full [P2-A4], [P2-A5] remain OPEN; the conditional targets t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2) do not follow from cache behavior. Cross-route [P2-D1]/[P2-C3]/[P2-B1]/[P2-B2] remain OPEN.

## Independent COMPUTATIONAL controls

Hosted Python and independently authored hosted Node.js scripts enumerate ALL 2^H source charge vectors; both explicitly build clauses and signed fixed-field bits. Tree-flow satisfiability witnesses for even charges, parity contradictions for odd charges, brute-force SAT for K4 and K3,3, quartet-bit differences for every K4/K3,3/Q3 mask and selected Heawood masks, and all charge-signature/trie cases pass. Exact independent raw cases agree, including SHA-256 for masks 0 and 1 of each graph:

| Graph | H | Source bits N | Sources | Full-trie nodes | Fresh probe floor |
|---|---:|---:|---:|---:|---:|
| K4 | 4 | 224 | 16 | 31 | 64 |
| K3,3 | 6 | 392 | 64 | 127 | 384 |
| Q3 | 8 | 512 | 256 | 511 | 2,048 |
| Heawood | 14 | 1040 | 16,384 | 32,767 | 229,376 |

The independent scripts and full raw JSONs are preserved in the run's reproducibility ZIP. Published standalone V8 verifier is a separate exact finite replay. No native FLMV instruction-level interpreter or historical R_mix341 parser was executed. There is no all-input proof or general computational lower bound.

**Publication safeguards:** Only the LSPV-4 owned report/code/raw/handoff and materially affected proof2.txt node [P2-L4-507] may be written on main with current full source and SHA readback. proof1.txt has no material change. Do not edit root main.tex without authenticating its full bytes/ownership markers; preserve all five agent identities, IDs, titles, schedules, enabled states, 2A/3B allocation, and original R_mix341 rules/weights. P versus NP OPEN.
