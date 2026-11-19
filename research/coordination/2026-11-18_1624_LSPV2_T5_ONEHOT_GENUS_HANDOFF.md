# LSPV-2 T5 circuit-genus handoff, 2026-11-18 (historical Route A)

PROVED source-exact one-hot ROM formula: valid=(no foreign arcs) AND EXACTONE(missing original arcs); color bit=valid AND OR(missing arc indicators for matching witness rows). No repeated per-edge source conjunctions are needed in the output ROM. Complete arbitrary-source valid membership depends on q=n(n-1) essential bits and costs at least q-1 binary gates; this is a **source recognition bound only**. Source-specific witness acquisition remains potentially exponential and is paid separately.

COMPUTATIONAL same 44 H33 witnesses: 1799->1735 witness gates, depth20->15, full verifier3203->3139; 2003 independently replayed masks. H9: 175->164 gates, depth12->11, verifier446->435; 2176 masks. Both independently rechecked two hostile corruptions. Archived new source-hashed complete Boolean netlists and generator.

PROVED topological obstruction: T5 thread capacity gives n<=3e_c-1.5b. For critical H of underlying undirected girth g, suppressed core girth >=ceil(g/3). Every planar edge-minimal UNSAT H has g<=15; every toroidal one has g<=18. If g>=19, orientable genus h>=1+(ceil(g/3)-6)n/[12ceil(g/3)] >=1+n/84. These are NOT circuit/witness time lower bounds. 120-vertex, girth24 subdivided cubic Tutte-Coxeter graph has a uniform greedy SAT witness, demonstrating a structural shortcut, but is not critical.

Literature firewall: oriented chromatic number <=5 does not imply homomorphism to fixed T5. Remaining blocker is uniformly hard **intrinsically critical high-girth SAT deletion** witness construction after preprocessing, treewidth, GF(5), flow and source access. P vs NP OPEN. All automations and trackers untouched.
