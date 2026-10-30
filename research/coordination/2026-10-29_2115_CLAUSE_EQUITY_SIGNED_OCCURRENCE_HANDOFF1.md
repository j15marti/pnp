# CLAUSE-EQUITY-OPPOSITION1: five-agent research handoff
Date: 2026-10-29 21:15 America/Los_Angeles. Research status: exact standard identities plus finite experiments; P vs NP OPEN.
Coordination issue: https://github.com/j15marti/pnp/issues/2

## User's intended semantics
Use `x_{i,j}` to mean the signed **occurrence** of variable x_i in source clause C_j, not an independent variable. Track source index, polarity sigma_{ij}, preferred satisfying value, truth under a full assignment and under its complete inversion, and true/false/unset under partial assignments. Source clause order must remain identifiable through normalizations. Opposing occurrences can coexist in a globally satisfying formula; the other literals matter.

## Exact deduction (standard resolution, not claimed novel)
If C_j=(x_i OR A_j) and C_k=(NOT x_i OR B_k), then their resolvent R=A_j OR B_k follows. Falsifying every literal of non-tautological R excludes the entire partial-assignment cube regardless of x_i. For full proper 3-CNF the resolvent has width at most 4. The exact Davis-Putnam projection is
EXISTS x_i [F_0 AND AND_j(x_i OR A_j) AND AND_k(NOT x_i OR B_k)]
= F_0 AND AND_{j,k}(A_j OR B_k).
On a partial assignment that falsifies a single one-step resolvent, unit propagation on the original parents already detects x_i and NOT x_i, so this does NOT produce new logical refutation power over full UP at the same prefix. But a shorter derived clause can enable earlier forcing; when useful, its construction and added scanning must be charged. Pair generation budget P=sum_i d_i^+ d_i^-; repeated resolution may cause exponential growth.

## Clause equity: exact truth vs computable proxy
For each C_j define Q_j(F)=#{a: a satisfies all C_k (k !=j) but falsifies C_j}. Q_j=0 iff F without C_j entails C_j; sum_j Q_j counts assignments violating precisely one source clause. Exact Q computed by full enumeration in tests only; no polynomial score oracle is assumed. A computable but unreliable proxy is sum 2^{-width(R)} over non-tautological resolvents using that source clause; it counts expected activated pair conflicts, not disjoint forbidden assignments, and correlated evidence must not be summed as independent benefit.

Complement profile: N_r(a)=number of source 3-clauses with r true literals; N_r(~a)=N_{3-r}(a). E=N0+N3, D=N3-N0; F SAT iff some a has E=abs(D). E=0 is the stronger NAE condition. The correct dynamic potential measures how early a partial prefix can be rejected, not the overall number of impossible COMPLETE assignments (source clauses already exclude those).

## Exact counterexample: 4-clause XOR block
(x OR y OR z), (x OR NOT y OR NOT z), (NOT x OR y OR NOT z), (NOT x OR NOT y OR z).
Each clause has Q_j=1, every variable has d+=d-=2, yet ALL direct opposite-sign resolvents are tautological. E(a)=1 for all eight assignments, so the quadratic complement score has no gradient. D(a) is cubic and separates the four SAT orientations from the four UNSAT orientations. Recognize complete parity quartets and use charged GF(2) elimination; but do not project each overlapping block independently and then mistakenly glue incompatible witnesses.

## Finite tests completed locally (reproduce independently)
Source scripts:
- clause_equity_occurrence_dag.py, SHA-256 8f762a42c1c838995f931549a4dc697e9f6918886cc37e3485d7687338287a53
- clause_equity_independent_audit.py, SHA-256 91fb4d75f24cf87ee7a8749cc4cf3931dc5ab16f135175effbd8d29ba0d31a6e
- xor_quartet_clause_shortcuts.py, SHA-256 b331da938559697fac5d3dbbc1ee59a8f297aabea918b25aa44b4dbaaf3382bc

The scripts and full raw JSON are preserved in the original conversation's downloadable artifacts, not asserted uploaded to GitHub. Agent may reproduce from specification or request transfer.

140 generated instances, RNG seed 20261029: 110 random signed proper 3-CNF n=8,10,12 densities 3.5-5.0, 30 exact-(2,2) signed balanced n=6,9,12; 102 SAT, 38 UNSAT. All 140 independently truth-table checked; six more small controls. Independent checker: 9,925,990 audited conditions across 146 formulas (Q_j counts, inversion, selected full Davis-Putnam projections), 0 failures.

| DPLL/closure policy | Nodes summed | Selected primitive-work proxy | Cases with less work than frequency |
| --- | ---: | ---: | ---: |
| Frequency baseline | 923 | 248092 | reference |
| Frequency then sign-balance tie-break | 927 | 249920 | 16 |
| Sign-balance first | 952 | 259029 | 24 |
| Opposing resolvents only as frequency tie-break | 893 | 291498 | 5 |
| Full opposing-resolvent score | 865 | 419800 | 0 |
| One-pass width<=2 resolution preprocessing + frequency | 774 | 333720 | 8 |

Work proxy includes selected clause/literal scans, heuristic reads, pair testing, resolvents, and preprocessing, NOT all Python allocations or machine-independent bit costs. Full opposition saves 6.3% search nodes but increases this selected work by 69.2%; binary resolution saves 16.1% nodes but increases it by 34.5%. This falsifies the hypothesis that raw pair equity is automatically a net saving.

Four cheap complete initial assignments (all 0, all 1, signed majority, complementary majority) found satisfying assignments for 20/102 SAT generated cases, but no UNSAT result can be inferred from their failure.

Prism Tseitin pure-parity controls (three-regular, every edge belongs to exactly two parity quartets). For odd charge with n=30 variables, 80 3-clauses, naive frequency DPLL visited 5455 nodes and 2,897,072 selected work events; a parity-quartet recognizer used 1920 literal inspections and GF(2) elimination used 19 row XORs, 38 row tests. Recognition and model reconstruction must also be charged. This is a known affine short-circuit, not an asymptotic general SAT result.

## New falsifiable target
Build a proof-carrying residual/branch DAG whose nodes carry occurrence sign conflicts, original clause equity Q (diagnostic only on small exact instances), conditional short-resolvent support, all-assignment complement E,D, and explicit local algebraic dependencies. Test a *budgeted adaptive* strategy that spends resolution work only when likely to save MORE future work. Compare with UP-first, width-2 and width-3 closure, XOR elimination, Horn, 2-SAT and standard CDCL heuristics on matched SAT and UNSAT distributions; assess partial-prefix prune depths, overlap-corrected marginal gains, failed discovery, source access and peak space. Treat competing representations as legitimate.

Role assignments are in issue #2. All five original recurring hourly agents were successfully updated and re-enabled; no new tasks or schedules created. Preserve source provenance, handoffs and exact scope.

## Primary literature
Fleury and Biere, Mining definitions in Kissat with Kittens, Formal Methods in System Design 60(3), 2023: https://pmc.ncbi.nlm.nih.gov/articles/PMC10564679/ (BVE, definability, model reconstruction, explicit caveats).
Preprocessing of Propagation Redundant Clauses, J Automated Reasoning 2023: https://link.springer.com/article/10.1007/s10817-023-09681-3 (UP and failed literals).
Li et al., Clause vivification by unit propagation in CDCL SAT solvers, Artificial Intelligence 279, 2020: https://www.sciencedirect.com/science/article/pii/S0004370219301961.
Project baseline: boundary DAG accounting, charged access, solver hierarchy, complement-duality audit. Avoid claiming standard resolution, Gaussian elimination, XOR-gate recognition, or complement counting as new mathematical results.
