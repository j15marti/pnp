# LSPV-4 PALETTE-SOURCE-CYCLE56, 2026-10-23 18:45 KST

**Status: P versus NP OPEN.** Standalone verified LaTeX, mini-reproducer and audit JSON are at this same `2026-10-23_1845_LSPV-4_PALETTE_SOURCE_CYCLE56` prefix in `research/agents/lspv-4/`. Root `main.tex` LSPV-4 ownership region is reconciled. The full supplementary two-Python-auditor package is also available in the originating conversation; it is not assumed shared as a local file across runtimes.

## Exact construction
Fix q>=3; graph vertices are a palette triangle B,T,F plus x_i,xbar_i for i mod q. Add palette triangle; B-x_i, B-xbar_i and x_i-xbar_i for every i; then add x_(i+1)-x_i if sigma_i=1 or x_(i+1)-xbar_i if sigma_i=0. V=2q+3, E=4q+3. The graph is three-colorable iff XOR_i sigma_i=0 and has exactly 12 colorings on SAT, zero on UNSAT.

One-hot source CNF has n=6q+9 Boolean variables, k=2q+3 ternary clauses, m2=18q+18 binary clauses, m=20q+21 total clauses, and 42q+45 literal occurrences. Canonical four-word clauses plus two header words, w=ceil(log2(64(n+m+1))) yields N=(80q+86)w bits. Flipping any single sigma_i changes precisely three literal words in that edge's negative binary clauses. These address groups are disjoint for different i, and all header/layout records are unchanged.

## Direct lower bound and matching upper bound
On **each both-label** member, **every deterministic exact decider of unrestricted proper-3CNF SAT** must read at least one literal field per edge orientation gadget, or it would have an identical transcript on the opposite-label one-bit-flipped input. Hence >=q=Omega(N/log N) addressed word reads under this explicit word-RAM input model. A uniform checked graph-template recognizer and parity scan runs in O(q) time, so this is input-order acquisition only, not superlinear time or P!=NP.

## Controlled bridge
Every palette-pinned (B-adjacent) vertex has two colors, and arbitrary chords between these vertices are XOR inequality constraints; signed propagation solves in linear time. With t exceptional vertices not adjacent to B, enumerate all 3^t colors, solve the pinned remainder with parity propagation, yielding O(3^t(V+E)) time and O(V+E) peak words. At t=O(log N) still in P; unrestricted graph 3-coloring yields the NP-complete endpoint. This 3^t is an upper bound, not necessary enumeration.

## Transport audit
The original 2-SAT chain F_b is UNSAT iff AND_q(b)=1. The palette graph is UNSAT iff XOR_q(sigma)=1. A coordinatewise mapping sigma_i=g_i(b_i) would make the latter predicate affine and thus cannot reproduce AND_q for q>=2. A global reduction can compute AND_q but charges Omega(q) input acquisition and consumes the existing lower bound. The construction is an independent **direct inclusion** of a new sensitive family, not a free lower-bound amplification of F_b.

## Independent peer checks and next experiment
**Role 5:** independently prove the three-changed-words claim after canonical CNF encoding, and check the exception-parameter algorithm with arbitrary pinned/unpinned boundary edges. **Roles 1-3:** use the q>=3 both-label formulas as source-coherent hostile controls for any acquisition/compression/continuation lemma, and test the fatal fieldwise AND-to-XOR transport obstacle. Build graph families with t genuinely unpinned vertices; charge discovery, source reads, selector representation, all failed color branches, DAG reuse, witness reconstruction and peak space. Falsify any proposed 3^t lower bound using a source-aware polynomial simplifier. The missing all-decider superpolynomial lower bound remains OPEN.

Audit: 31,169 counted checks, zero failures; 504 graph orientation vectors (252/252 SAT/UNSAT), 3,576 label-flipping field checks, 744 signed chord trials, and 5,456 fieldwise-transport maps excluded. No ETH/SETH/cryptography. Prior QUADRATIC-SOURCE-LADDER55, MAIN95, MAIN85, MAIN64, SOURCEPROBE19 were reviewed or adopted.

LSPV-4::PALETTE_SOURCE_CYCLE56::HANDOFF-VERIFIED-END
