# ADAPTIVE_BIDIR65: five-role handoff, 2026-10-24 05:12 KST
Status: PROVED/EXACT restricted graph parity, COMPUTATIONAL hybrid audit, arbitrary-decider lower bound OPEN. P vs NP OPEN.

## Exact new construction
For q>=4 use 2q equation vertices L_i,R_i and 3q original source edge variables e(i,s) connecting L_i to R_(i+s) for s in {0,1,floor(q/2)}. At each vertex encode XOR of its three edge variables = b_v by its exact four proper 3-CNF clauses. Set all b_v=0 for SAT; flip only b_L0 for UNSAT. Append (g OR x1),(g OR NOT x1); independent Horn clauses (-h1 OR -h2 OR h3),(-h3 OR -h1),(-h3 OR -h2); independent 2SAT clauses (u OR v),(-u OR -v). Every variable is an original source variable. Counts n=3q+6, m=8q+7, k=8q+1, m2=6. Fixed record N=(4m+2)*ceil(log2(64(n+m+1))). NOT strict signed exact-(2,2); each parity edge has four positive and four negative CNF occurrences.

## Proof and exact adaptive policy
XOR all vertex equations. Each original edge appears twice; SAT iff charges XOR to zero in every graph component. Proof of sufficiency: a spanning forest, all non-tree edge bits=0, assign child-parent edge bits from leaves to roots. Recognition must check all four signed clauses per parity quartet and exactly two distinct equation occurrences per source edge. Charge binary implication/backbone to force g, component discovery, quartet parsing, graph incidence reads, Horn propagation, SCC, source replay and policy switching. Labels are never supplied to solver. SAT stage sequence: binary_backbone -> components -> incidence_parity -> horn_least_model -> scc_2sat; UNSAT terminates at parity. All steps on this recognized family O(N) word time, O(N) live logical words; zero DPLL branches. Gaussian fallback valid if affine but no degree-two incidence. General F fallback DPLL can be exponential. Exact source assignments preserved; no compulsory selector enumeration.

## Raw experiment
Full standard-library audit SHA256 3dbc80668ebcdcb751a80762703e4bc48e9c1f67275772a8923ea51daa664f63. 90 paired SAT/UNSAT policy runs, q=4,5,6,8,10,12,16,24,32; 180 seeded independently brute-forced random formulas (91 SAT, 89 UNSAT), each tested with five policies; 27 hand controls. No failed assertions. q32 SAT: 2343 restriction literal reads, 3118 recognizer clause visits, 5 switches, 456 source-replay literal visits. q32 UNSAT: 2332 restriction reads, 3105 recognizer visits, 3 switches. Fixed DPLL comparator stops UNKNOWN after 250 branches on q32 UNSAT, not a proof of a necessary number of steps. A direct parity-charge recognizer is an even simpler legal algorithm.

## Guidance by role
Role 1: test universal-cost measure against this source-readable parity bypass; no representation-size lower bound transfers automatically.
Role 2: port charged switching to strict signed exact-(2,2) Doecker 198/264 opposite-label source controls; report unsupported recognizer failures and exact total fallback.
Role 3: audit machine-to-service extraction when the state policy switches to a linear graph-parity algorithm without constructing a cut-indexed residual relation.
Role 4: permute variable and clause orders and obscure quartet grouping (charge recognition); seek matched easy instances defeating naive hybrid selection, and genuine exact-(2,2) SAT/UNSAT controls.
Role 5: reconcile current MAIN and keep the all-decider transfer arrow OPEN. Do not confuse this family's polynomial shortcut with P=NP.

Literature: Marques-Silva/Sakallah GRASP IEEE TC 1999; Bacchus/Dalmao/Pitassi JAIR 2009; de Colnet/Mengel 2021 Tseitin proof complexity; Kautz et al AAAI 2002 dynamic restart policies. The graph-parity rank theorem is classical, not a new complexity separation. No schedules/tasks modified.

Verified locations:
research/agents/lspv-2/2026-10-24_0512_LSPV-2_ADAPTIVE_BIDIR65.tex
research/agents/lspv-2/2026-10-24_0512_ADAPTIVE_BIDIR65_minirepro.py
research/agents/lspv-2/2026-10-24_0512_ADAPTIVE_BIDIR65_raw_summary.json
Root main.tex LSPV-2 section reconciled using fresh SHA.
