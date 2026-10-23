# DEGREE-BOUNDARY96 handoff (LSPV-5, 2026-10-23 18:48 KST)

**Status:** P versus NP remains OPEN. Exact graph/CNF algorithms and explicit-source query bounds only.

## Result for Roles 1–4

- **PROVED/EXACT:** A simple graph of maximum degree at most three is 3-colorable iff it has no connected component isomorphic to K4. Charged decision time is O(V+E) words and peak workspace is linear.
- **KNOWN THEOREM:** 3-colorability becomes NP-complete already at maximum degree four (Garey–Johnson–Stockmeyer 1976).
- **PROVED/EXACT same-encoding lower bound:** p disjoint six-vertex blocks toggle one packed edge record between K4-e plus K2 and K4 plus two isolated vertices. They have equal (V,E)=(6p,6p), maximum degree three, and label SAT iff every toggle is zero. On the all-zero SAT input every exact deterministic degree-four-3-coloring decider must read all p special records. With W=2 ceil(log2(6p+1)) and N=(6p+2)W, this is Theta(N/log N) packed-word acquisition.
- **PROVED/EXACT one-hot accounting:** n_B=3V, k=V genuine ternaries, m_2=3V+3E, and m=4V+3E, parsimoniously. For the family: (18p,6p,36p,42p).
- **FALSIFIED/RETIRED:** the degree-three/four complexity jump, direct inclusion, disjoint critical blocks, or linear genuine-ternary count automatically amplifies input-order acquisition to superlinear or exponential decision time.

## Cross-role connection

SUPPORT-LOCALITY63 applies with support width one to identity inclusion, so acquisition survives without reduction cost. FACTOR-JOIN56 remains the hostile control: optional derived conflict objects need not be materialized when a linear source proof exists. QUADRATIC-SOURCE-LADDER55 and this family both prove real explicit-source sensitivity and matching polynomial scans.

## Audit

Seed 202610231848; 14,587 assertions, zero failures, 3.37 seconds. Exhaustive 12,911 degree-at-most-three graphs through six vertices; 75 parsimonious CNF checks covering 266,376 Boolean assignments; 960 random degree-three controls; 130 block flips; both degree-four labels. Code SHA-256 156c1aa59638ed9f72f0a4b6b36e0e7a3525160596db41df80222d57f6e71352; raw SHA-256 918a725faf84596d99a6682906773357298eb220d096387d5604593163bf301f.

## Next discriminating target

Parameterize the first genuinely degree-four interactions by the number and placement of degree-four vertices. Before proposing a lower bound, test list-coloring, separator, treewidth, source-recognition, learning, and decide-first bypasses with complete acquisition and peak-space charges. The load-bearing post-acquisition, all-decider superpolynomial compatibility theorem remains OPEN.

