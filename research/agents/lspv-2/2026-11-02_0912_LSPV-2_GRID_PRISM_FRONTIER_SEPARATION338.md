# LSPV-2 GRID-PRISM-FRONTIER-SEPARATION338

November 2, 2026, 09:12 PST. Status: PROVED/EXACT **restricted syntactic clause-frontier** theorem, independently COMPUTATIONAL finite controls. P versus NP OPEN.

## Universal obstruction and falsifiers

A source-frontier lower bound does not force arbitrary SAT deciders to construct source-frontier states, cofactor DAGs, or Circuit-SAT encodings. The approach tests three falsifiable claims: (1) constant positive and negative frontiers combine into a constant joint frontier, now **FALSIFIED asymptotically** by GRID_q; (2) growing joint frontier forces SAT decision hardness, **FALSIFIED as an inference** by an infinite family with explicit linear-work SAT witnesses; and (3) smaller forward circuit means faster SAT decision, **not supported** by paid direct CNF/Circuit-SAT experiments.

## Exact infinite construction and proof

For each q>=3 divisible by 3, let n=q^2, k=n/3. Make two copies of the cubic prism P_k=C_k x K_2, with 2k vertices and 3k=n edges. In either copy, each graph vertex contributes one source clause containing its three incident edge variables, all positive for one prism and all negative for the other. A Hamiltonian vertex cycle of the prism, with each noncycle matching edge inserted between consecutive cycle edges at one endpoint, gives an explicit Hamiltonian sequence of all n **edges** in its line graph. Assign the positive edge positions in row-major q-by-q variable-grid order and the negative edge positions in column-major order. This gives F_q.

Each F_q is an original valid proper duplicate-free Döcker monotone 3-SAT-(2,2) formula. Cubic simplicity proves three distinct literals and unique signed clause supports; the two endpoints of every edge give exactly two occurrences in each polarity. A source-variable order grouping ring edges T_i,B_i,S_i has at most six crossing clauses on each signed side: two local ring vertices plus at most one wraparound vertex per layer. Thus w_+(F_q)<=6 and w_-(F_q)<=6.

Let H be the original-variable primal graph, joining two variables when they share a source clause. Consecutive positive edge-path positions produce all horizontal edges of the q-by-q square grid in H; consecutive negative positions produce all vertical grid edges. Thus H contains the entire square grid. The established vertex-separation/pathwidth theorem says every variable order has a cut with at least q unassigned boundary variables in that grid. Every such variable must occur in an ORIGINAL clause crossing the cut, and any width-three crossing clause contains at most two unassigned variables. Consequently, **for every joint original-variable order pi, b_Fq(pi)>=ceil(q/2)=Omega(sqrt(n)).** This is a lower bound for syntactic crossing clauses only, NOT for the number of semantic quotient classes, OBDD nodes, SAT decision steps or space of arbitrary deciders.

## Counterexample to naive hardness: odd-q SAT witness

For odd q divisible by three, the assignment x_(r,c)=(r+c) mod 2 alternates along both the positive row-major and negative column-major Hamilton edge sequences, because q is odd. Every prism vertex's incident-edge triple has an adjacent opposite-color pair in the linear edge sequence, except the unique cycle-cut vertex, whose positions are {0,2k-3,3k-1}, also containing both parities. Thus every positive and negative source clause is satisfied. This source-checkable witness is constructed in O(n) time and O(n) bits on these explicitly indexed originals. Recognizing an arbitrary renamed promise member is NOT treated as free. Even-q checkerboard failure is not an UNSAT certificate.

## Independent finite verification

Independent no-producer-import Node verifier reconstructed all seven source families; validated original language and source IDs; checked every grid-edge provenance; enumerated **all 9!=362,880 orders** for GRID3; verified 54 variable renamings; performed **34,496** original-vs-forward-circuit full-assignment evaluations; and rejected nine malformed sources. **78,675 independent checks passed.**

GRID3 has n=9, 74 complete models, exact signed minimum frontiers (3,3), exact joint minimum frontier 8. GRID6/9/12/15/24/36 have respectively n=36/81/144/225/576/1296, each signed ring width 6, with proven joint lower bounds 3/5/6/8/12/18. GRID3 has a complete same-original SAT2 versus UNSAT0 pin pair differing only at x3; its UNSAT side has eight original-clause-indexed falsified leaves. F9 also has a verified SAT1/UNSAT0 same-original pin pair. Source-gate evaluation of Y6/F9/F15 was exhaustive (20/70/1032 models), U198/V198 sampled 128 rows each. Fresh prior-method U198 refutation replay checked 384 boundary rows, 19,488 DPLL nodes and 6,099,608 source probes; V198 source witness checked all 264 clauses.

Under the declared **clause-private** fan-in-two AND/OR/NAND evaluator, gate count is 3m-1=4n-1, and full output-one Tseitin clause count is 12n-2 with uniquely determined forward traces. This restricted architecture count is not an unrestricted circuit minimum. GRID3 OBDDs for specified positive-ring/reverse/natural orders have 75/68/67 nodes, acquired by 512 paid complete source evaluations per order; no optimal-order or semantic oracle is assumed. The separate source/Circuit-SAT same-original DPLL literal-check counts are GRID3 SAT 71/7530 and UNSAT 6/5395; F9 SAT 91/7751 and UNSAT 62/7225. Circuit compilation is **excluded** from Circuit-SAT solver-only counts, so the latter understates total work.

## Fully charged total-work boundary

For the explicit family, source generation and indexing are linear; the implemented grid-clause provenance scan is O(n*m)=O(n^2). Paid circuit construction writes 4n-1 gates, and Tseitin encodes 12n-2 clauses. Host producer approximately 3.2 s / 103 MiB peak RSS; independent verifier approximately 0.5 s / 40 MiB RSS. These do not give FLMV-native machine transitions. A general adaptive controller must still pay source/index/head reads, grammar checks, discovery and **failed** policies, strategy switches, proof and GE, semantic continuation equality acquisition, gate/cofactor DAGs, cache/replay, child/output/bit access, guest DELAY/COPY/RECOMP computation and the **simultaneously live** peak ancestor+child+guest space. No arbitrary-decider power-short theorem or strict same-machine numerical FLMV transfer is shown. P=NP and P!=NP both remain OPEN.

## Literature and project duplication

Döcker (2019), arXiv:1912.08032; Kinnersley (1992), DOI:10.1016/0020-0190(92)90234-M; SageMath graph vertex-separation reference (explicit q-by-q grid value); Bryant (1986), DOI:10.1109/TC.1986.1676819. Project search reviewed LSPV-2 335/336/337 and active issue #3. OpenAI GitHub code search for 'circuit SAT OBDD Tseitin' returned no result and is **not** evidence of novelty. The exact incremental result beyond prior finite two-sided prism audit 337 is an **asymptotic** joint-frontier separation with an explicit easy-SAT odd-q subfamily. Full producer, separately implemented Node verifier, raw ledgers, six-module U198/V198 replay and SHA-256 manifest are in the downloadable reproducibility archive.

**Remaining OPEN:** uniform polynomial total-work all-input controller, hereditary arbitrary-A power-short A->Phi(A), numerical SAME-MACHINE FLMV transfer. No five-role identities, enabled states or hourly Pacific schedules changed.
