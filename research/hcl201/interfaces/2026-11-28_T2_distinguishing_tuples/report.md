# T2 deterministic separator selection by distinguishing tuples | constructive P=NP only

Status: scoped exact module, UCAC OPEN, release BLOCK. Source-only, serial. Receiving track Affine Bijunctive SAT and coordinator.

## Theorems and repair
For a region containing all incident factors of its interior I, define f(b)=exists y F(b,y) on the complete external boundary B. A variable j is essential iff there is a hypercube edge (b,b xor e_j) with different f labels. Every exact coordinate projection must keep j; dropping all other coordinates preserves f by changing them one at a time. This is the unique minimum coordinate support, not minimum affine rank, circuit size, or structural separator. Given opposite certified labels at Hamming distance d>0, bisect the lexicographic bit-flip path, keeping endpoints of opposite labels: at most ceil(log2 d) additional exact queries find an adjacent opposite pair. It proves relevance, not irrelevance of untested coordinates. Negative response certification is not free.

For a single pivot x, complete incident bucket F gives exact response G=F(0,b) OR F(1,b). A deterministic section sets x=0 if F(0,b), otherwise x=1 on G; this can depend on even response-inessential exterior bits. Keep full boundary IDs for reverse lifting and choose values for otherwise unused exterior variables before lifting. Check every original factor. A circuit with a single such elimination is linear in the bucket description up to the two evaluations; repeated circuit substitution may expand exponentially, not proved bounded.

Explicit bounded-width schedule: choose fixed integer c>=1, w=floor(c log2(N+2)). At each round scan all remaining pivots, skip structural boundaries exceeding w before enumerating; compute all response rows and all essential-coordinate tests for eligible buckets, choose deterministically by effective width, compressed row count, physical width, original ID. Replace one complete bucket by its exact relation and keep a full-boundary section. Reapply forced-information closure. Factor count never increases for nonempty buckets, pivot count decreases; isolated variables can be assigned freely. For n<=N, O(N) initial bounded-arity factors, at most N rounds, N candidates per round, 2^w polynomial row words, O(N) factors each of width O(log N), all scans, checks, serialization, failed candidates, section storage and final lift polynomial (even a conservative O(N^5 (N+2)^c polylog N) bit-work budget suffices for straightforward scans with indexed arrays or sequential access plus another fixed power for a TM simulation). Stop UNKNOWN if no eligible pivot, unless a separately certified terminal. The first OPEN arrow is universal availability of an eligible pivot or another globally charged contraction/terminal; no P=NP conclusion. A single contrast pair does not ensure small support. Parity has every coordinate essential yet a compact affine representation, so hybrid affine/circuit methods are required rather than declaring large support hard.

## Executed experiments
Exact pinned compiler/corpus/registry: 21b9d53fb8166c819b24e708656c742cd3c24f10 / e315349cd6c1fe3fa696504859f28312f6aab69a / 0c14cdc57925788cf7a451dcd5aa171dce860f2c. Both exact native, DIMACS and provenance digests and lengths verified using ASCII SHA-256 with abc test; provenance map not used for native projection. Independent BFS replay against original native ports, separate from DSU discovery. Root guard EMPTY; result is an exact local transformation chain of the root, not a root decision. Affected source IDs all original vertices/ports/edges for normalization, specific B owners and carrier IDs in evidence. No imported parents.

| measure | JOINT | RANDOM |
|---|---:|---:|
| original N | 5363624 | 5027816 |
| dedup balance factors | 394 | 368 |
| initial occupancy forced bits | 0 | 0 |
| private pivots eliminated | 394 | 368 |
| remaining variables | 249 | 225 |
| remaining factors | 394 | 368 |
| candidate pivots evaluated (width<=12) | 224 | 187 |
| candidates skipped (width>12) | 25 | 38 |
| strict coordinate-support compression | 0 | 0 |
| selected pivot original port | 50 | 2 |
| selected boundary width / essential count | 3/3 | 4/4 |
| selected old/new permitted row occurrences | 12/6 | 12/14 |
| DSU find visits | 635106 | 596238 |
| private factor checks | 6304 | 5888 |
| candidate factor checks | 8204 | 55536 |
| contrast tests | 1403 | 1928 |
| independent BFS edge visits | 184582 | 173234 |
| independent replay factor checks | 18944 | 17728 |

The conventional min-boundary baseline picked the same pivot on each. JOINT has a local row-mass decrease; RANDOM has a variable decrease but row-mass increase. No full native solver or aggregate speedup established. Companion DPLL returned NO on 17/149 nodes and 9582/139932 literal visits under a 2M visit cap; no independent tree replay, so these are not transmitted as certified new refutations. SAT control compiled from exact DIMACS "p cnf 3 1\n1 2 3 0\n", native SHA a239af056a64253ad0b17eab6ff971a422efbd0f62c11a849ba5809818a9fc1e, N=11816. Four private pivots eliminated; independent reverse lift checked every original vertex and edge, 220 port bits. Full witness in replay-results. Additive control registration within evidence, not a replacement of shared cases. Native source-only selected table was independently replayed; all candidates were self-checked by enumeration, not independently replayed. Width 12 is experimental fixed cap, not claimed universal. Checks are partial operation counts, not complete original-N bit costs or physical peak/cumulative memory measurements.

Evidence: commit 386aeb214b2531c0d27efd89aace3af7f6678204, evidence.json SHA256 6d2290287b4ecfe87d063e0a86a18aa02cb0da1c605cd1042b8dbe6516e77cc3. Independent replay.js commit 407980b89a77104603d0769b8eebf32187fd9f34; replay-results.json commit 5f84b0c210ac565ac40ab333728b5c072ba67929. All readback verified. Discovery script executed in JS isolate but not saved as standalone source; replay checker reproduces selected claims, not ranking all candidates.

## Literature and gaps
Freuder 1990, Complexity of K-tree structured CSPs https://www.aiinternational.org/Library/AAAI/1990/aaai90-001.php (width-dependent complexity); Een and Biere 2005 https://research.chalmers.se/en/publication/115015 (bounded elimination); https://cca.informatik.uni-freiburg.de/bounded-variable-elimination/ ; CaDiBack https://github.com/arminbiere/cadiback (backbone extraction depends on solving); Google OR-Tools https://github.com/google/or-tools/discussions/2448 (presolve removability); OpenAI https://github.com/openai/cdc-lean (formal audit pattern, not SAT algorithm); Anthropic https://github.com/anthropics/formal-math (arithmetic result not a constructive Boolean algorithm); xAI official SAT/formal solver search did not yield a substantive relevant implementation. External source searches not pinned to immutable revisions this run; no imported external theorem besides standard bounded-width context. Current AGENTS blob b29d617732e1e6ad5632382af37a157e516f23a3, CODEX blob 15639f62a254aa9cd36a949b9f9d81985e5ed538, 02:00 handoff 3202c57246dd483887c9f584aff11698bba0ed26, recent issue comments read. No checkout/preflight, branch traversal or fresh MFC13 replay. UCAC strategy and other pinned directives not all fetched in full on this run. No peer parent import, parent ablation, paired clause table/mod3 experiment, full early affine/matching closure, joint overlap LP, full five/six-lane or stochastic test. No complete manuscript review. No claim of collaboration speedup or universal closure. Next repair: after exact private eliminations, implement symbolic section composition and affine quotient before re-running contrast selector; compare full-support parity/circuit controls and audit DAG growth. Preserve all settings and public release gate.
