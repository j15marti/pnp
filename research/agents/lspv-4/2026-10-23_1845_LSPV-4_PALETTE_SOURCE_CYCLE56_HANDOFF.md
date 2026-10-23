# LSPV-4 PALETTE-SOURCE-CYCLE56, 2026-10-23 18:45 KST

**Status: P versus NP OPEN.** Corrected verified LaTeX, two minimal reproducers and raw audit JSON are at this same `2026-10-23_1845_LSPV-4_PALETTE_SOURCE_CYCLE56` prefix in `research/agents/lspv-4/`. Root `main.tex` LSPV-4 ownership region is reconciled. The full supplementary three-Python-auditor package is also available in the originating conversation; it is not assumed shared as a local file across runtimes.

## Exact construction
Fix q>=3; graph vertices are a palette triangle B,T,F plus x_i,xbar_i for i mod q. Add the palette triangle and B-x_i, B-xbar_i, x_i-xbar_i for each i; add edge x_(i+1)-x_i when sigma_i=1, or x_(i+1)-xbar_i otherwise. The graph has V=2q+3 and E=4q+3. It is 3-colorable iff XOR_i sigma_i=0; 12 graph colorings on SAT and zero on UNSAT.

**Mixed-width 3-CNF** from one-hot graph colors has n=6q+9, k=2q+3 ternary clauses, m2=18q+18 binary clauses, total m=20q+21, and N=(80q+86)w encoded bits. It is not proper exactly-three-clause CNF.

**Proper exactly-three-clause CNF** uses one fresh free padding variable y_C per binary clause, replacing (a OR b) by (a OR b OR y_C) AND (a OR b OR NOT y_C). The padded source has n'=24q+27 original Boolean variables, k'=m'=38q+39 genuine ternaries, m2'=0, 114q+117 literal occurrences, N'=(152q+158)w' encoded bits. Each original graph-coloring witness extends to 2^(18q+18) proper formula witnesses. SAT count is 12*2^(18q+18), UNSAT count zero. All encoded metadata and positions are label independent. A source orientation flip changes three mixed-width literal words or six padded exactly-three literal words, each in disjoint addressed gadgets.

## Direct lower bound and matching upper bound
On **every SAT and UNSAT instance** of the correctly padded proper exactly-three-clause family, **every deterministic exact word-access decider for unrestricted proper exactly-three-clause SAT** must read at least one of the six orientation-dependent source cells per gadget. Otherwise one flipped orientation would produce the opposite answer with the same read transcript. This gives q=Omega(N'/log N') addressed-word input observations, even for a decider valid on all input formulas. The mixed-width version has the analogous three-word sensitivity.

A uniform checked template recognizer, padding-contracting parser and parity scan decides these formulas in O(q) word time, with O(q) charged reconstruction and replay. This is a tight input-order acquisition lower bound, not superlinear solving time or P!=NP.

## Controlled bridge
Every palette-pinned (B-adjacent) vertex has two colors, and arbitrary chords between these vertices are XOR inequality constraints; signed propagation solves in linear time. With t exceptional vertices not adjacent to B, enumerate all 3^t colors, solve the pinned remainder with parity propagation, yielding O(3^t(V+E)) time and O(V+E) peak words. At t=O(log N) still in P; unrestricted graph 3-coloring yields the NP-complete endpoint. This 3^t is an upper bound, not necessary enumeration.

## Transport audit
The original 2-SAT chain F_b is UNSAT iff AND_q(b)=1. The palette graph is UNSAT iff XOR_q(sigma)=1. A coordinatewise mapping sigma_i=g_i(b_i) would make the latter predicate affine and thus cannot reproduce AND_q for q>=2. A global reduction can compute AND_q but charges Omega(q) input acquisition and consumes the existing lower bound. The construction is an independent **direct inclusion** of a new sensitive family, not a free lower-bound amplification of F_b.

## Independent peer checks and next experiment
**Role 5:** independently check canonical exactly-three padding, the six changed literal cells, model-count factor 2^(18q+18) and the O(3^t) exception algorithm. **Roles 1-3:** consume q>=3 both-label proper formulas and the AND-to-XOR coordinatewise-transport impossibility in every charged lower-bound candidate. First possible amplification is t unpinned three-color vertices, with acquisition, exceptions, caching, failed paths, source-coherent reconstruction and peak space fully charged. A 3^t upper bound is not a lower bound.

**Audit:** 35,753 counted checks, zero failures, across three independently executed stdlib Python programs. 504 both-label mixed formulas (252 SAT/252 UNSAT), 504 both-label proper formulas, 3,576 three-word flips, 3,576 six-word flips, 504 proper padded YES witness replays, 744 chord trials and 5,456 excluded coordinatewise maps. Python scripts in the local complete package; the GitHub directory also contains separate mixed-width and properly padded minimal reproducers, plus the corrected raw JSON. No ETH/SETH/cryptographic assumptions. Root main.tex LSPV-4 ownership region reconciled.

Earlier QUADRATIC-SOURCE-LADDER55 and MAIN95, MAIN85, MAIN64, SOURCEPROBE19 were adopted, not re-claimed as new. P versus NP OPEN.

LSPV-4::PALETTE_SOURCE_CYCLE56::HANDOFF-VERIFIED-END
