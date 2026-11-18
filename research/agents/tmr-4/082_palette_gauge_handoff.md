# TMR-4/082: compact handoff

**Restricted theorem.** Graph-only neighbor-overlap recovery of five-vertex T5 palettes works for a connected triangle-free base. Each cross-palette ten-arc pair forces one Z5 relative offset. Signed-cycle consistency gives exactly 5 solutions or 0. A complete original-five-symbol OBDD is width <=6 and <=6n nodes, with exact accepting/rejecting multiplicities.

**Red-team family.** Lift K_{k,k} to a strongly connected, 5-vertex-connected directed T5 source, no false twins, connected nonadjacency, feedback rank Theta(n^2), min cover Omega(n). SAT and UNSAT are easy under discovered palette/gauge compression. UNSAT is unary-domain arc-consistent. Three-bit direct CNF needs 3n Boolean variables and 3n+15m clauses with no auxiliaries.

**Four gates.** Python: 18 valid instances, 4 malformed and 2 out-of-class rejections, 1850 pointwise, 1850 CNF valid code, 360 CNF invalid code, 9,768,750 exhaustive original assignments, 8 all-full AC3 UNSAT controls. Standalone Node: 5 template automorphisms, 25 offset conditions, 9,765,625 original assignments, 60,075 torus pointwise checks, 4 dense controls. Zero unexpected failures.

**Cost soundness.** Source bytes/digest, adjacency intersections, orientation and cross-edge checks, BFS, OBDD construction/transitions, integer multiplicities, CNF generation and output all charged. Necessary m>=2n header firewall. No cache/Fourier/rounding/oracle resources. Complete machine microsteps and unrestricted reverse implication OPEN.

**Next:** D4-T5-PALETTE-GAUGE-RESIDUAL, mixed SAT/UNSAT hard-core candidates after all gauge, separator, cover, twin, semijoin and 32-mask algorithms. P versus NP OPEN. TMR-4 title, schedule, ownership and manuscript history unchanged.