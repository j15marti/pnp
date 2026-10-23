# SCC-ISOLATION68. Role 2 five-role handoff. 2026-10-24 07:12 KST

P versus NP remains OPEN. No arbitrary-algorithm representation-cost dichotomy was assumed.

**Restricted exact theorem.** For a strict proper signed exact-(2,2) three-CNF, perform only source-certified complementary-pivot contractions and write B for the resulting 2-CNF and T for unmatched ternaries. Occurrence conservation is
t_x + 2 b_x^+ + u_x^+ = 2, t_x + 2 b_x^- + u_x^- = 2.
Every source literal in a nontrivial implication SCC of B must appear in binary clauses of both signs. Therefore u_x^+ = u_x^- = 0. Consequently SCC equivalence on B cannot shorten T. Nonetheless B implies boundary binary relations and must not be thrown away.

**Existing exact projection (PAIRPATH73), operational corollary.** Components of B are paths/cycles; each internal degree-two source has one appearance of each sign. Eliminate internal sources with existential resolution, producing one binary clause per path over two distinct T endpoints, cycles project to TRUE. Boundary endpoints do not repeat among projected clauses, yielding a matching and no nontrivial SCC. This projection is imported, not newly invented. SCC prepass skipped only saves an extra O(p) edge scan, not asymptotic time.

**Additional elementary structural filter.** Initial untouched signed exact-(2,2) 3-CNF is never renamable Horn or dual-Horn: after any renaming 2n of each sign versus m=4n/3 clauses. After restrictions, Horn may emerge.

**Adaptive state and charged policy.** Source/sign census and component detection, certified pair discovery, then path projection or affine-quartet recognition; when one variable hits every residual ternary, branch over both values and call SCC on each exact restricted clause set, replay original witnesses; otherwise total DPLL fallback. Audit uses SciPy/HiGHS on 198-var hard component instead of waiting for an in-Python DPLL proof, and checks status computationally. The source does not disclose labels. Rule evaluation, failed tests, source reads, switches, reconstruction and peak memory are included in the bound ledger of the report.

**Computational evidence.** 265 assertion groups, zero failures. Strict q=4..128 paired-cycle SAT series, strict k=1..16 XOR quartet series, strict connected 6-var path core with 32 exhaustive boundary tests, and same-size strict 198-variable 264-clause D\"ocker UNSAT and documented 2-sign-swap SAT neighbor. Mixed labels each 240 vars, 320 three-literal clauses, 9 independent source components. Hybrid chooses paired-cycle, six quartets, path hit-variable branch/SCC, and large exact fallback. External HiGHS returned infeasible on U and feasible on V; U also relies on the previous independently recorded DOECKER-CORE-CERT61, no newly emitted formal UNSAT certificate. Full unabridged script/results/source in conversation research package; verified standalone TeX and compact executable in Role 2 GitHub directory.

**Role 1:** Reject any potential requiring source-T SCC contraction or rich representation on all algorithms; all-decider bridge remains OPEN.
**Role 3:** Red-team the SCC argument on multigraph two-cycles, clause-duplicate exclusions, input renamings, and bound after restriction.
**Role 4:** Construct connected same-support opposite labels with a genuine nonempty projected ternary boundary.
**Role 5:** Reconcile strict-source no-gain finding with valid mixed-CNF QUIET-EQUIV67 and root-label quotient barrier, preserving both.
**Role 2:** Build a source-compatible join solver on a matching of projected binary constraints plus overlapping ternaries. Search for polynomial continuations before any hardness claim.

The newest independently readback-verified Role 1 report available in this run was CUBICCOVER75 (2026-10-23 22:56 KST). If a newer predecessor report is expected but absent, request an original-body write retry; never invent a replacement. No automation created, reactivated or rescheduled.
