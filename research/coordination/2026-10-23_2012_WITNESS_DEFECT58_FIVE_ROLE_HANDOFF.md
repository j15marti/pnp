# WITNESS-DEFECT58 five-role source-coherent algorithm handoff
Date: 2026-10-23 20:12 Asia/Seoul. P versus NP OPEN.

Role 2's exact restricted result: canonically match positive and negative proper ternary clauses with identical source triples. Suppose each original variable participates in at most two paired supports and t signed ternary clauses remain unmatched. Select ONE true literal per unmatched clause (3^t possibilities); reject contradictory source requirements; handle remaining matched supports by graph-factor degree intervals [1,2] (after forced-edge adjustments). Interval (g,f)-factor on general multigraphs is polynomial by KNOWN matching theory. This gives a uniform deterministic exact source-assignment algorithm in 3^t poly(N). It supersedes the earlier project-specific 2^(3t) bit-boundary algorithm. Bipartite continuation was independently implemented via lower-bound circulation; nonbipartite implementation remains untested, not falsely claimed.

Family: q even >=4, connected cubic prism with 2q paired triple supports and 3q original source edges. The 4q-clause paired core is monotone signed exact-(2+,2-). Six additional mixed-sign 3-clauses cover all six nonconstant assignments to the same support triple, making UNSAT. Replace just one of these with a distinct 3-clause satisfied by the all-rungs-TRUE witness to obtain SAT at the same n, m=4q+6 and encoded N. Full augmented instances are NOT monotone exact-(2,2). Exhaustive q4/q6 model counts 75/0 and 1571/0. Tested q=4,6,8,12,20,40,80 plus 5 nonlocal bipartite three-matching graphs with both labels. Program reports nonbipartite K4 unsupported rather than promising an unimplemented blossom algorithm.

Exact compatibility control: on prism q4, forcing source edges x1=x2=0 and x5=x6=1 leaves every paired support locally completable but forces a shared rung both TRUE and FALSE. The flow program found and checked a global infeasibility mincut; flipping x6 to FALSE restores SAT. Original signed clauses are reread on each reconstructed SAT witness.

Current Role4 SHARED-SWITCH-MINIMAL-UNSAT57 was independently regenerated at q=3,5,16,64: all proper ternary, orientation parity recovered by a paid source scan, with 16 vs 0 models at small q. It is a hostile control: clause criticality and ternary count do not imply expensive decision.

A proper reverse 3-CNF AND-of-OR evaluation circuit uses 3m-1 gates, 6m-2 gate input wires and 9m-2 functional Tseitin clauses including output TRUE. Exactly one witness occurrence is selected per clause; this is NOT an exactly-one restriction on original literal values. Occurrence graph for signed exact-(2,2): 4n vertices, 4n complementary conflict edges (disjoint K2,2), +4n clause-triangle edges, total 8n.

Full reproducible stdlib audit: 162 checks, zero failures. Report path:
research/agents/lspv-2/2026-10-23_2012_LSPV-2_WITNESS_DEFECT58.tex
Minimal code:
research/agents/lspv-2/2026-10-23_2012_WITNESS_DEFECT58_minirepro.py
Finite summary:
research/agents/lspv-2/2026-10-23_2012_WITNESS_DEFECT58_raw_summary.json
Extended LaTeX/PDF, full flow code, source results and bibliography accompany the scheduled response.

Role 1: No mandatory enumeration, static representation, or all-decider lower bound from graph factors or 3^t.
Role 3: Compare t against compiler source identities; import the published 198-variable exact signed-(2,2) UNSAT source.
Role 4: Falsify the three-literal-witness completeness proof and nonbipartite limitations; challenge source cut certificate.
Role 5: Integrate exact theorem, KNOWN factor algorithm, and missing general-factor implementation separately. MAIN64 exact source join and MAIN85 SAT root quotient are unchanged.

Next missing step: implement deterministic nonbipartite interval graph factor; test the independently recovered 198-variable exact-(2,2) UNSAT original. Neither P=NP nor P!=NP follows.