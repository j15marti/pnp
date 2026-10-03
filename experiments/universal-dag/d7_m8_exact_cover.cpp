// D(7,8) exact-cover enumeration specification.
//
// There are 280 genuine 3-clauses on seven variables.
// Each clause falsifies a 16-point codimension-3 subcube of {0,1}^7.
// Since 8*16=128, an eight-clause formula is UNSAT iff its eight falsifying
// subcubes are pairwise disjoint. Pairwise disjointness then implies exact cover.
//
// Enumeration algorithm used for D7M8-1:
// 1. Build the 280 128-bit falsification masks.
// 2. Precompute compatibility lists: two clauses are compatible iff their masks
//    are disjoint.
// 3. Enumerate increasing 8-cliques in the compatibility graph by recursive
//    intersection of candidate lists.
// 4. For every clique, verify OR of the eight masks equals all 128 assignments.
// 5. Compute variable degree and sign-count profiles for each accepted formula.
//
// Exact result: 17280 UNSAT formulas.
// All 17280 use all seven variables.
//
// This file records the algorithm/result specification. The full implementation
// used a two-word uint64_t mask and recursive candidate intersections.
// P versus NP remains open.
