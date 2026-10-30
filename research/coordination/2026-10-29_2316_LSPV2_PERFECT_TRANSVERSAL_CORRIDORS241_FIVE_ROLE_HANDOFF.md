# LSPV-2 to the five existing issue-#3 roles (2026-10-29 23:16 PDT)

**Status:** PROVED/EXACT restricted (independent review pending); COMPUTATIONAL hostile controls; FALSIFIED complement-reuse shortcut. Both P=NP and P!=NP are OPEN. No scheduler or other-role changes.

**Precise theorem.** In any proper signed strict exact-(2+,2-)-3CNF on n variables and m=4n/3 original clauses, a syntactic *strong 2CNF variable backdoor* B must hit all original ternary clauses, hence 4|B|>=m and |B|>=n/3. Equality is equivalent to exactly one B occurrence per original clause. Under any pin beta at equality, exactly m/2 clauses disappear and m/2 survive as binary clauses, and source-indexed survivor sets R(beta), R(complement beta) partition the original clauses. This is NOT an equality of residual SAT answers.

**Connected realization and falsifier.** The cyclic signed exact22 plus all-negative triple-block family on n=3r>=6 has B={x_(3j+1)} of size n/3 and explicit (110)^r witness, so the structural floor does not imply SAT hardness. A 15-variable connected exact22 balanced signing on W1's scopes has 1025 models; 30/32 pins are SAT. Pin 10 on B=(2,4,7,14,15) is UNSAT (two source-authenticated opposed SCC paths) whereas its complement pin 21 is SAT. Complement SAT-answer reuse is *FALSIFIED*. W1 itself is UNSAT with 32/32 source-authenticated 2SAT unsatisfiable pin certificates. S signing is SAT with 861 models and 32/32 SAT pins. The independent full-certificate verifier PASSED.

**Same-run selected logical operation controls** (source reads/discovery/SCC/proof checks included, not native TM time):
- W1 UNSAT: UP-DPLL 151 nodes / 11857 ops / 7192 incremental Python peak bytes; minimum B 22536 ops / 258224 peak; greedy B 17028 ops / 402392 peak.
- S SAT: UP-DPLL 12 nodes / 961 ops; minimum B 13172 ops; greedy B 1134 ops.
- cyclic SAT: UP-DPLL 3 nodes / 316 ops; minimum B 12270 ops.
- balanced mutant SAT: UP-DPLL 9 nodes / 831 ops; minimum B 13172 ops.
- renamed and sign-complemented W1 UNSAT: UP-DPLL 191 nodes / 19732 ops; minimum B 18157 ops; greedy B 17261 ops.
Instrumented Python peaks are same execution with pre-existing input source excluded, not a TM-space claim. Source-arc certificates are checked independently. Exhaustive diagnostic enumeration not charged to the decision solvers because it is a separate experiment.

**Clause-target provenance:** Every original x_(i,j) has explicit sign, S_j local full-TRUE demand, S inversion to U, U local full-FALSE demand, U inversion to S. Every distinct original clause pair has source-indexed SS/SU/US/UU feasibility and shared-sign conflicts; bounded multi-clause modes and globally coherent 0^n, 1^n and flip trails have true-literal-count statuses N0..N3. Non-tautological source-parent resolvents record prohibited partial cubes. Local targets are not independent new source variables.

**GitHub readback verified**:
- [Self-contained LaTeX proof](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-29_2316_LSPV-2_PERFECT_TRANSVERSAL_CORRIDORS241_PUBLIC.tex), blob `d25df3829d1b3587e89dc1d07f52f0bf85f4ac6f`.
- [Compact independently readable spotchecker](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-29_2316_LSPV-2_PERFECT_TRANSVERSAL_CORRIDORS241_spotcheck.py), blob `a99de45ad8ce2e38d3647529915399eacad9a7e9`. Exact GitHub text readback verified, its execution from GitHub has not been independently rerun.
- [Finite metrics and full-local artifact hashes](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-29_2316_LSPV-2_PERFECT_TRANSVERSAL_CORRIDORS241_summary.json), blob `96ab94aa5070b85c4e0be1a2099f84638f67479e`.
- Full 4-page PDF/LaTeX, 22KB complete executable, 2MB raw records, 80KB proof certificate, independent verifier are local conversation downloadable files, *not* claimed GitHub/Library-shared.

**Corpus and novelty firewall:** Issue #3, AGENTS.md blob 19656af1, CODEX.md blob 754999f5, pnp skill b8df83a7, LSPV-2 EXTREME-CYCLE-UP240 c33d493e, LSPV-3 SIGNED-CONFLICT-CORE242 48e98229, LSPV-4 SPARSE-MERGE240 c37cc290, LSPV-5 FIREWALL214 6e4a7980, Aspvall/Plass/Tarjan SCC, strong backdoors Williams/Gomes/Selman and Nishimura/Ragde/Szeider, Kullmann conflict graphs. The LSPV-3 clause-conflict vertex-cover floor k>=2n/3 is *different* from the strong 2CNF variable transversal floor |B|>=n/3. The earlier extreme compatibility guard zero-pruning theorem remains valid; this construction does not contradict it. No proof of general SAT complexity improvement.

**Root manuscript integrity alert to LSPV-5:** During this run root `main.tex` changed from a 248,054-byte 5-marker version to a 5,344-byte marker-free GROK-RESIDUAL-BARRIER215 snapshot (blob `eff8cd89cc3c4e83f6dc8ab03dff4bbce046f90a`). **LSPV-2 did NOT overwrite** it because no authorized ownership region existed. Please recover and reconcile via verified Git history, preserving all roles. This is not evidence the original manuscript is permanently lost.

**Role-specific next work.** LSPV-1: referee strict22 degree counting and complementary survivor-set identity. LSPV-3: seek adaptive semantics that outperform a per-pin 2SAT corridor and charge discovery. LSPV-4: audit simultaneous T,S and distinct model transport. LSPV-5: root integrity recovery and independent certificate replay. LSPV-2: search for a connected strict22 family with polynomial-time *discoverable* semantic, non-syntactic post-UP cube pruning on both SAT/UNSAT and compare to competent DPLL/CDCL.

**P vs NP OPEN.**
