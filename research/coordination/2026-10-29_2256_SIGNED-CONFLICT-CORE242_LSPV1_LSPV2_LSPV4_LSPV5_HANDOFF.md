# SIGNED-CONFLICT-CORE242, LSPV-3, 2026-10-29 22:56 PDT

## Exact research status
PROVED/EXACT restricted statements, pending independent referee. COMPUTATIONAL finite hostile controls. P=NP and P!=NP OPEN. Issue #3 is active; issue #2 equity scoring remains paused. No tasks, schedules, enabled states or repository ownership changed.

The user requires each **original source clause** and signed source occurrence x_{i,j} to carry local S_j (every literal TRUE) and U_j (every literal FALSE), both inverted targets, and then comparison against **globally coherent** 0^n, 1^n, single and multi-flip/complement trajectories. Neither local occurrence signs nor incompatible S/U labels are separately assignable variables. Ordinary SAT of a source clause needs only one true literal.

## Proved scope
For any proper fixed-width r-CNF, construct the clause sign-conflict graph H whose edges connect source clauses sharing a variable with opposite signs. If deleting a vertex cover M of k clauses leaves a unate core, all original variables outside T=union supports of M can be fixed to their preferred sign values without affecting satisfiability. The surviving clauses have support in T, |T|<=rk. Enumerating T gives an exact source-authenticated SAT/UNSAT algorithm; every rejected T-assignment has a source-clause falsifier certifying the whole T-subcube. Find M by charged two-way graph vertex cover search in O(N + sum_i d_i^+ d_i^- + 2^k|E|+2^(rk)N) abstract indexed-RAM work. At k=O(log N), fixed r, it is polynomial. An unbounded k or failed cover attempt conveys no decision.

**Constructive SAT:** if k<r, begin with all source literals TRUE in each retained core clause, process each exceptional clause and protect one true occurrence; flip an unprotected variable if necessary. At most k flips preserve all protected exceptions and cannot falsify any initially r-TRUE core clause. Thus proper 3CNF with k<=2 is automatically SAT.

**Sharp falsification k=r:** on n=r^2 variables, take all positive r-subsets plus r negative disjoint r-subsets. Every full assignment must falsify something, and graph matching plus deletion prove minimum cover exactly r. For r=3, source is UNSAT with n=9, m=87, cover 3. Deleting one negative clause gives SAT with cover 2.

**Strict22 firewall:** in proper signed exact-(2+,2-) 3CNF, a unate core requires deleting >=2 occurrences per variable. Thus every such clause conflict cover has k>=2n/3=m/2. This approach does not solve general strict22 in polynomial time.

## Finite tests and adverse resource result
Seed 202610292256. 34,128 independent source pair SS/SU/US/UU comparisons, 2,800 three-clause joint extreme-mode checks and 60,780 complement-clause checks passed. Exhaustive 255 nonempty 3-variable signed-clause subset formulas included 92 with k<=2, all SAT. Additional 400 constructed small unate-core width3/4 cases compared against 145,408 complete assignments; no failures.

On r=3 UNSAT sharp case, controller certified 512 failed T cubes, while its **selected-work proxy** was 94,851 versus competent UP-first DPLL's 7,927 and 23 recursion nodes; traced simultaneous controller peak 2,141,379 versus baseline 5,712 Python bytes. On r=3 SAT two-exception case, constructive repair made 2 flips; controller cost 50,610 versus DPLL 2,767. On strict22 W1 UNSAT15, budget4 failed, controller 21,052 versus 13,777. Strict22 S SAT15 similarly 7,975 versus 1,046. The discovery/diagnostic overhead is genuine; no claim of overall solver speedup. Native single-tape head crossings, communication and physical memory-bit changes are *not measured* by these Python proxies.

## Readback and provenance
The GitHub public self-contained proof, supplementary checker and finite summary were uploaded and read back with exact content equality:
- [LaTex report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-10-29_2256_LSPV-3_SIGNED-CONFLICT-CORE242_PUBLIC.tex), blob 4295da705dcb01434f93bbe9cf772e2a9e896b15.
- [Compact checker](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-10-29_2256_LSPV-3_SIGNED-CONFLICT-CORE242_spotcheck.py), blob 388d2ca8509f3d6e0882e44e5ee46b9155798e1a.
- [Raw summary](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-10-29_2256_LSPV-3_SIGNED-CONFLICT-CORE242_summary.json), blob e532883b3637d7eebf7000039871885a787ab6bd.
The full PDF, full TeX, 28KB Python source, 3MB raw JSON and BibTeX are local downloadable artifacts in the originating run. SHA256 code 4f43d8a67a83a1f2d2dc08a912b62dfb636e48cd029842275e6de9cf509f19ac; raw 878dd4a18c60d4d07066d1d72ed6a0d34dfdf54b800475ab5e1c318dfe038ae5. A persistent Library upload was attempted but failed with container_session_unavailable. Do **not** claim the full raw artifact is in GitHub or Library.

## Role-specific assignments and next missing lemma
LSPV-1: independently referee the protected flip theorem and the sharp UNSAT family, especially source distinctness and k=r matching lower bound.
LSPV-2: derive genuinely new non-tautological consequences in **connected strict22**, after saturated UP, that are not explained by unate backdoors.
LSPV-4: audit the full discovery, failed budget branching, 512 source-cube checks, original source reads, simultaneously measured peak and physical machine-model limits.
LSPV-5: reconcile status only if source evidence is checked; preserve clause S/U representation firewall and P vs NP OPEN.

**Next OPEN lemma:** polynomial-time recognize a different bounded-interface/structural class in connected strict22 with authenticated SAT and UNSAT decisions, post-UP cube pruning, and fully charged total-work superiority on adversarial SAT/UNSAT controls over competent DPLL/CDCL. This is not implied by a small conflict cover, which is prohibited in strict22.
