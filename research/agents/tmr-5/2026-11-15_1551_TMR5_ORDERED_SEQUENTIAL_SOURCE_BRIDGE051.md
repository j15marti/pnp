# TMR-5/051: An actual sequential-input-head bridge for TMR-3/054's complete streaming-graph chain

**November 15, 2026, 15:51 PST | PNP Machine Bottleneck Redteam | Track B, cross-track synthesis**

**Independent verdict:** PROVED/EXACT in the restricted ordered-query streaming model; external mathematical peer review OPEN. COMPUTATIONAL for executed finite tests. No generic Tree Evaluation improvement, SAT lower bound, or P-versus-NP separation.

## Candidate, quantifiers, integration point, falsifiers

Candidate: **for every fixed constant-state transducer** delta:[C] x {0,1} -> [C] x {0,1}, every B>=1, every gamma-encoded source x of length B, and every 1<=L<=B, TMR-3/054's complete blank-start graph-provider-plus-comb-evaluator chain can be executed with an ordinary **locally moving read-only input head**, rather than its declared indexed-source primitive, with the same asymptotic query-time and space bounds. The *fixed* leaf query order j=1,...,B is indispensable. The source is gamma(B), a zero delimiter, then B payload bits; malformed encodings must reject.

Precommitted falsifiers: (F1) recovering the previous-anchor source address physically requires Theta(B) movements per **ordered** query; (F2) the output depends on unprovided checkpoint work-cell contents or the symbol at the previous STATE cell is ignored; (F3) anchor lookup or arithmetic exceeds the simultaneous space budget; (F4) a claim silently extends this special comb schedule to arbitrary adaptive oracle queries, arbitrary work-tape revisits, or the original Williams TreeEval.

Named dependency closed: **TMR-3/054 indexed-source-to-locally-headed-input interface for its exact Q=B monotone comb schedule.** This strengthens rather than replaces that draft's model. The unsupported all-checkpoint and arbitrary TreeEval interfaces remain OPEN.

## Independently proved source-head movement identity

Let R=ceil(B/L), let block lengths d_1,...,d_R be L except the last truncated block, and let a_j=L floor((j-1)/L). The original source is authenticated during one forward scan of N=B+2 floor(log2 B)+2 cells, while constructing R genuine (state, MOVE-position) anchor records of w=ceil(log2 C)+ceil(log2(B+1)) bits each. Physically rewind the input head B positions from the endmarker to the first payload cell. For each j=1,...,B, move the head back from j-1 to a_j, replay the source bits a_j+1,...,j using the stored anchor and the **previously written** state transition, and leave the source head at j.

At the t-th query within a block, the backward move is precisely t-1 and the forward replay is precisely t. Consequently, the true head-movement total for all Q=B requests is

    H_queries = sum_{blocks i} sum_{t=1}^{d_i} (2t-1)
              = sum_i d_i^2 <= B L.

Including the genuine initial full input scan and reset gives the **exact** authenticated-input movement count for this implementation

    H_total = N + B + sum_i d_i^2.

The full original source-symbol read count is

    N + sum_i d_i(d_i+1)/2.

This is a symbolic all-B proof, independent of sampled inputs. The proof works because j is increasing; for arbitrary source-jump requests the equality is false, and TMR-3/054's adverse alternating-source control remains genuine.

## Whole-chain correctness and same-realization ledger

For a fixed delta, q_0=0 and p_0=0; each original paid source step computes (q_i,m_i)=delta(q_{i-1},x_i) from the real previously written STATE value, and p_i=p_{i-1}+m_i, moving the physical MOVE head when m_i=1. A separately charged LENGTH-head comparator for 2p_B>=B gives the output. The independent provider does one authenticated source scan, saves anchors at 0,L,...<B on a **sequential** writable tape, answers Q=B graph requests by seeking the original input head as above, and uses the leaf results in a height-B left-comb accumulator. Each anchor has the genuine state/position by induction, each replay reconstructs (q_j,p_j,m_j) by determinism, and the comb accumulator equals p_j after leaf j. Therefore the returned YES/NO matches the authentic original source computation on every well-formed word. Invalid gamma delimiters/lengths/letters are rejected after paid grammar parsing.

The disjoint time components are: N header/authentication source scans; B source reset moves; sum_i d_i^2 paid query input-head movements; Rw bit-cell anchor writes; O(BRw) physical anchor-tape seeks/copies; Q=B updates of O(log B)-bit state/position/count/address registers; one final threshold comparison and label. Exact finite-alphabet bit arithmetic, control switching and indexing add only polylog(B+2) overhead. No source read, cache, shared anchor or query is free. The **one matched machine** has

    T = O((N + B L + B R w) polylog(B+2)),
    S = O(R w + log B).

With L=ceil(sqrt B), the promised restricted bounds become T=O(B^(3/2) polylog B), S=O(sqrt B log B), now in the standard sequential read-only-input model. A direct legal streaming counter computes this same transducer output in O(B polylog B) time and O(log B) space. Accordingly this is **not** a lower bound, not a generic improvement over Williams/Cook-Mertz, and not a SAT transfer. No promised randomized or quantum result follows.

## Independent executable evidence

Actual local Node v22 execution on deterministic revision **tmr5-seqsource051.v1**, seed 20261115, exhaustive all 256 two-state delta tables and all payload strings B=1,...,5 for every L=1,...,B, plus 12 seeded three-state tables with all payload strings to B=7. It checks gamma encoding/decoding, authentic previous-work-symbol transitions, all graph state/position/movement responses, each move/read count, sequential checkpoint-head movement, all comb decisions, malformed sources, and the exact squared-block identity.

**Results:** 69,099 complete source-to-output cases; 312,936 virtual graph queries; 2,359,567 assertions; 11 malformed source controls rejected; zero failures. For B=64,L=8 the exact source-head movement total is 78+64+512=**654** and peak anchor storage is 64 bits. For B=1024,L=32 it is 1046+1024+32768=**34,838** and anchor storage is 384 bits. Seeded data are finite COMPUTATIONAL evidence; the general formula above has a separate symbolic proof. The interpreter counts actual source and anchor **head movements**, not a fully compiled finite-control TM transition table or Lean kernel.

Files:
- research/agents/tmr-5/2026-11-15_1551_TMR5_ORDERED_SEQUENTIAL_SOURCE_BRIDGE051.md (this report)
- experiments/tmr/tmr5_seq_source_bridge051.js
- results/raw/tmr/2026-11-15_1551_TMR5_SEQHEAD051_NODE_RAW.json
- main5_PNP_MACHINE_BOTTLENECK_REDTEAM.tex (owner living synthesis)
- research/agents/tmr-5/handoff.md (compact current entry prepended, historical body preserved)

Local exact SHA-256: executable 8085c33fce1d93e6c2f7880997a4286aff52710f4759a15360cf98271896f005; raw 9209202dd49ad354d84366171554b5f2b73bf8b3f0c9855c2fe1445ae8d3b96e.

The TMR-3/054 **unmerged** original report, executable and raw evidence were read on draft PR #164, branch research/tmr3-endtoend-streaming-graph054-20261115, including original file blobs 1935ce6a6ea0a5534e0ce80cac6e26e02e3594c2, 3429f96b84d3d9df8ce75d93f04575eb9bc8f103 and 1dc05109f2f9b89dfdaa8db75e5316eddf3c22c9. The new theorem is a precise **interface transfer**, not an attack on the original indexed model. Work-dependent preloaded states in TMR-3/053 still resist source-only selection; no spurious graph paths were removed.

## Four mandatory gates

| Gate | Verdict | Reason |
| --- | --- | --- |
| DISJ sanity | PASS restricted | No inference from assignment cut rank to SAT/circuit hardness; interleaved DISJ and compact algebra remain legal |
| Relativization | NOT APPLICABLE WITH REASON | No P-versus-NP separation or nonrelativizing claim; generic oracle and algebrization/Natural Proofs barriers remain for future unrestricted steps |
| Simultaneous DTISP | PASS restricted, OPEN unrestricted | Identical standard sequential-input realization has stated T and S. No general SAT machine or FLMV forbidden-region pair |
| Configuration counting | PASS as upper-bound guard | Deterministic total read-only-input machine obeys T<=2^{O(S+log N)}; never inverted to a runtime lower bound; not applied to quantum/probabilistic machines |

DISJ, Horn/2SAT, affine Gaussian, bounded treewidth, equality, autarkies, padding, auxiliary selector/count-normalizer, XOR isolation, unique-solution rank one, alternate local bases and adaptive compact/cached algorithms are not excluded. /341 remains FAIL as full UNSAT authority; /386 RESTRICTED.

## Ranked pipeline dependencies and highest-value next lemma

1. **TMR-3 /054** restricted canonical provider+evaluator PASS with the new sequential-head conversion. Generic checkpoint work-cell provider, actual arbitrary replay query budget, general evaluator and a strict matched DTISP transfer remain OPEN.
2. **TMR-1 /054** parsimonious density-four CNF source compiler PASS as restricted symbolic mathematics; the exact Anthropic pinned formal statement (eth/MainResults.lean SHA 1c62a550fa1e4cbec65bb7112f92ad67589afddc) and proof entry (eth/Solution.lean SHA 176892178e49792ae41368c13bb4973bae035b29) were independently fetched and inspected. No kernel build or transitive proof review was executed. The inherited E^NP hierarchy transfer is CONDITIONAL; NP-level inference OPEN.
3. **TMR-2 /054** DISJ frontier/multicut exact combinatorics PASS restricted, adaptive physical SAT-machine transfer OPEN.
4. **TMR-4 /054** fault-observable all-live shared wrapper is a valid scoped falsifier of raw gate-work tariffs; general circuit-to-adaptive-BP costed compiler OPEN.

**One next lemma:** an authentic blank-start arbitrary-work-tape virtual checkpoint-bit provider handling repeated work-head visits, charged adaptive Q node requests and locally headed source input, composed with a genuinely height-sensitive evaluator on the **same** simulation. Exact static/streaming protocols do not supply it.

Sources: TMR-3/054 draft PR #164; Williams, *Simulating Time With Square-Root Space*, arXiv:2502.17779v1 (2025), https://arxiv.org/html/2502.17779; Cook and Mertz, *Tree Evaluation is in Space O(log n log log n)*, SIAM Journal on Computing (2025), DOI 10.1137/24M1690126; pinned Anthropic October 2026 formal-math eth/MainResults.lean and Solution.lean; original TMR-1/054 report/code/raw; TMR-2/054 and TMR-4/054 reports; user governing directive SHA 8451d955f6cd5397de0895f8ebb46e30818842c3. Preflight/LaTeX/Lean builds NOT run: no local repository checkout. Existing five schedules and ownership untouched. **P versus NP remains OPEN.**
