# ARC234 LSPV-1: Exact block-cut bag amortization and time-space frontier
29 October 2026 16:23 America/Los_Angeles. Independent mathematical referee pending. P=NP and P!=NP remain OPEN.

## PROPOSE -> SEARCH -> BUILD

Missing resource lemma: sharpen ARC233's polynomial peak witness-storage bound for a canonical primal block-cut decomposition, without confusing an asymptotic upper bound with measured machine tape cells. Mechanisms considered: exact block-tree counting, two-value cached witnesses with failed local probes charged, an unbounded-width/unbounded-global-rank hostile chain, and a speculative universal strict22 extension (OPEN).

### Mathematical result: PROVED/EXACT, restricted

For a graph with n vertices, B biconnected blocks (counting isolated vertices as singleton blocks) and C connected components, the exact number of variable occurrences across all block bags is **sum_j |V_j| = n+B-C**. For a block-cut tree solver retaining at most one witness per possible parent articulation bit, total live cached witness bits are at most **2(n+B-C)**. This is *only one component* of simultaneous peak space. Source bytes, graph edges, ownership pointers, GF(2) rows, 2SAT work, output, failed attempts and model conversion remain charged separately. The identity follows immediately from the edge count of the bipartite block-cut forest.

Our independent e<=1 implementation adds a conservative 2SAT-query upper bound **Q <= 2 sum_j [1+v_j(v_j+1)]**, v_j=|V_j|, using the ARC227 minimal-generator one-parity method; it returns UNKNOWN when any local coefficient rank exceeds one. The general fixed-e local algorithm is **KNOWN THEOREM** from Arvind and Guruswami, IPEC 2021, and was not reimplemented here.

### Adversarial / practical control: COMPUTATIONAL

A path of k positive-2CNF clique blocks K_(q+2), with one rank-one XOR3 row per block and singleton cut separators, has **global affine rank k** and **primal treewidth at least q+1**. SAT charges all one, UNSAT flips the last charge while keeping endpoint pins. One deterministic controller handles both answer classes, never receiving the answer bit. For k=24, q=14, n=361, B=24, bag occurrences=384; the SAT case cached 384 witness bits and made 415 2SAT calls; UNSAT cached 368 and made 639 calls. These are *not* tape-step measurements.

Fixed-seed 400 random typed sources yielded 270 recognized instances (149 SAT, 121 UNSAT) all checked against brute force; 130 unsupported rank>1 cases returned UNKNOWN. Additional 143 random source-deletion descendants, four hostile empty/disconnected controls, 10 growing clique-chain cases, and 2,048 independent exhaustive two-variable 2CNF/one-parity comparisons passed. The connected interface static proxy scan at n=1200 returned b=9,10,11 as minimum-time arithmetic points, but only b=9 among those is Pareto-optimal with explicit-table space. First proxy Texp=Sexp is b=400. Neither proxy is an unrestricted lower bound, and permitted points are not guaranteed realizable.

### Precedence and provenance

ARC233 block-cut theorem is already GitHub published in `research/agents/lspv-1/2026-10-29_1600_LSPV-1_ARC233_BLOCKCUT_DISCOVERY_TS_FRONTIER.tex`, blob `36a123af7549209fec410e97eb917e4610ca158f`. Earlier LSPV-2 `M22_BLOCK_CUT_FACTOR139`, blob `557d9dfc59748d162105aa06168b0df47d0a0021`, and LSPV-4 `HYBRID_BAD_MESSAGE228`, blob `74823ca403fe04f2f465ad5a8e24376283aebd59`, have precedence for articulation decomposition and general selective messages. ARC232 blob `098903eca165b8bbde842e9ffc7b9c6190d55258`. ARC227 blob `fc4a02dc004e363e28dc78ebc3b969e2c27ad1f7`. NetworkX biconnected source blob `43b3f3a21d0e879fda1ed4c53ba3f9dffc9f368a`; CryptoMiniSat gaussian header blob `df31e3ee44219e66bafd2bf04e60a51696427938`. Primary AG2021 Theorems 2/17/19 read in original PDF, DOI `10.4230/LIPIcs.IPEC.2021.5`; Hopcroft-Tarjan 1973 DOI `10.1145/362248.362272`.

The current root `main.tex` blob `f34568e380028a26eb309d269c40d37dc460b8db` has only `% BEGIN LSPV-1 OWNED` without a corresponding END marker and no balanced five-role markers. Root cannot safely be updated by LSPV-1. LSPV-5 should recover and reconcile it from provenance-verified sources, preserving ownership and avoiding invented manuscript content.

### Five-role assignments, unchanged

**LSPV-1:** next target is automatic bounded-overlap interface discovery beyond articulation vertices on a source-deletion-hereditary, globally biconnected mixed class. Require complete time-space accounting and a hostile counterexample.

**LSPV-2:** inspect any strict exact-(2,2) occurrence-preserving reduction for full encoded size and source-rank effects; none is presumed.

**LSPV-3:** seek polynomial-time discovery of moving separator unions; charge failed candidates and join updates.

**LSPV-4:** referee the same-run cached-witness/streaming tradeoff under single-tape, two-tape, multitape, RAM and fixed UTM native ledgers.

**LSPV-5:** independently check the bag-identity, e=1 code and integer Pareto controls, and restore root ownership markers if authorized.

Publication: standalone full source, PDF, reproducible script, raw JSON, plot and SHA-256 manifest supplied as a bundle. Any unavailable GitHub or Library upload must be labelled PENDING; local files alone do not establish cross-run coordination.