# P3PS03 addendum: scalable connected source checks

After the main audit, reran only structural checks (not the timed-out large Pfaffian computation). Start b disjoint octahedron incidence blocks, each with six triples on two elements per color: all binary words except 000 and 111. For each adjacent block i,i+1 exchange X coordinates of local triples 001 in i and 010 in i+1. Both swapped incidence edges can be placed on the exterior face of their respective components before a two-edge splice, which preserves planarity; sequentially attach a new block. The two chosen edges are distinct in every interior block. Each element still has degree three. The unchanged complementary pairs 011,100 give an explicit source solution per block. Every source tested is connected and planar. All three pair matching support tests retained every triple in each tested size.

Observed for the deterministic acquired NetworkX embedding of the direct conflict graph (same underlying graph as uncontracted field graph, since all coefficients positive):
blocks, triples, maximum face length, greedy face count, unsupported triples
1,6,3,2,0
2,12,5,4,0
4,24,7,8,0
8,48,7,14,0
16,96,7,28,0
32,192,7,54,0
64,384,7,108,0

For each recorded embedding all vertices carry nonzero field, so at least ceil(triples/maxFaceLength) faces are necessary. This is a finite structural audit, not proof of a uniform lower bound for every embedding or all stronger closures. It suggests face coverage alone will not be exhaustive.

Constructive complementary closure for the entire chain family: partition incidence vertices by their original block (triple ownership determined by Y,Z indices, not modified X index). Each seam has two crossing X edges; a block has at most four boundary wires and exactly six triple vertices. Enumerate its 64 internal selections and boundary words, keep actual witnesses satisfying each local equation. Join consecutive block tables by exact two-bit boundary equality using ordinary path DP, O(b) constant-sized local operations; retain predecessor and lift. In fact each prefix has equal numbers of all element colors and no Y/Z crossings, so its two oppositely directed X crossing bits must agree by P3AGE03 conservation; the separator state can be one bit. No global anchor enumeration necessary. This proves tractability for the displayed infinite family, not all P3DM. Both the phase-field terminal and local-color interfaces should remain portfolio lanes. Separate structural test code provided; it uses the same loops as the two executed structural checks (combined output). No large Pfaffian timing or universal obstruction claimed.
