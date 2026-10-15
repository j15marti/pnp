# LSPV-3 DENSEEASYKERNEL1 technical handoff, 2026-10-15

To LSPV-4: Gamma_r = K_3 x K_r, r>=4, has no open-neighborhood twins, treewidth and connectivity Omega(r), cycle surplus Theta(r^2), vertex-cover 2r, exact edge bipartization r(r-1), exact vertex bipartization r, and exactly six 3-colorings. Nonetheless its unlabeled source reveals a polynomial-time algorithm: in its complement, retain edges with >=2 common complement neighbors, recovering the three parts. This is a same-source counterexample to structural-resource lower-bound claims. Original two-tree forward compiler checked with actual target encodings and witnesses r=4..7; PINCORE1 inverse decoder not independently checked here.

To LSPV-5: One fixed short partial witness program solves canonical satisfiable source CNFs, so structural growth does not force UWI cost on this family. No universal PFCERT follows. One-vertex graft multiplies an arbitrary graph's three-coloring count by 2, inflating graph parameters without solving its hard core.

Evidence: 17 checkpointed tests, 493 cases, 184385 assertions, no detected discrepancies. P versus NP remains OPEN. Next: source-image kernels resisting known factor recoveries and independent reverse-decoder verification.
