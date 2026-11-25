# CC01 target, 2026-11-24 18:21 PST

Input: an explicit simple cubic graph, two edge-membership bits per edge, exactly one selected incident edge per vertex per copy, and explicit edge-local four-state masks/nonnegative integer costs. Optional reference pair defines movement costs and a no-new-overlap guard. No arbitrary hidden consumers of private vertices.

Pipeline: source parse and certified unit/binary forced closure -> prove/refute alternative-neighborhood dominance -> discover private two-port diamonds without a supplied manifest -> exact four-state cost/count/lift projection -> certified kernel closure -> a declared bounded-kernel or unpinned bipartite terminal -> original-source reconstruction/verification.

Candidate A: every nonempty two-matching ternary core permits neighborhood-dominance contraction or the disjoint-resource-clique terminal. Falsifier: an actual source graph whose alternatives all have incomparable external neighborhoods and whose conflict graph has an induced three-vertex path.

Candidate B: maximal disjoint diamond strings can be discovered and projected exactly in polynomial time, preserving every edge-local guard, total cost, count and original matching lift. Falsifiers: unequal boundary bits extend through a diamond; discovered diamonds overlap; arbitrary edge masks break the four-state gluing; parallel edges, loops or closed necklaces lose a legal source configuration.

Candidate C: repeated diamond inflation is universally progress toward a trivial kernel. Falsifier: contraction recovers an arbitrary original cubic graph, including Petersen. This candidate is expected to fail; a correct compiler still provides a constructive infinite-family terminal.

No universal P=NP or P!=NP conclusion is licensed. Reference enumeration is restricted to small graphs/kernels and is charged explicitly. Local closure is a specified polynomial repertoire, never complete semantic closure for free.
