# Strict-C native critical source: binary-cover girth rigidity and cyclic-5 SAT escape

2026-11-19. Independent critical-obstruction construction and red-team audit. P versus NP remains **OPEN**.

## Predicate and authenticated input
Colors are Z5; R(a,b) iff (b-a) mod5 in {1,3}; strict C is the symmetric directed-triangle relation with exactly 30 of 125 accepted triples. Every physical clause uses three distinct variable names; global value injectivity is not assumed. The archived native source consists of 25 variables and 25 clauses, is intrinsically clause-minimal UNSAT with exact incidence girth 8, and has an independent complete 1046-node refutation plus 25 physical deletion witnesses (600 true retained C clauses, 25 false deleted C clauses). Prior base evidence: `research/agents/critical-graphs/2026-11-19_NATIVE_STRICT_C_25_CLAUSE_GIRTH8_AND_LOG_GIRTH.md`.

## PROVED: every binary incidence lift has exact girth eight
The original factor graph contains three internally node-disjoint length-four paths from variable 0 to variable 16, with clause indices zero based:

```
P_A: v0 - c11 - v4  - c23 - v16
P_B: v0 - c22 - v17 - c0  - v16
P_C: v0 - c18 - v1  - c3  - v16
```

Verified source clauses: c11=(0,4,12), c23=(4,7,16); c22=(0,14,17), c0=(10,16,17); c18=(0,1,9), c3=(1,5,16). Each pair of paths forms an incidence 8-cycle. For **any** two-sheet cover of the incidence graph, write p_A,p_B,p_C in GF(2) for the sums of the interchange voltages along the three paths. The three cycles' voltages are p_A+p_B, p_A+p_C, p_B+p_C, whose sum is 0. They cannot all be odd. An even-voltage simple base 8-cycle lifts to an 8-cycle. Covering maps cannot introduce cycles shorter than the base girth. Hence *every* binary incidence cover has exact girth 8. This is a theorem for all covers, not a sample conclusion.

## COMPUTATIONALLY VERIFIED: five-sheet girth ten can be SAT
A Z5 voltage assignment on all 75 base incidences with seed `2026111902` was found by a 9-step local repair of the 82 distinct base incidence 8-cycles. A connected cyclic 5-cover has **125 original-C variables, 125 original-C clauses, exact incidence girth 10**. Yet it is **SAT**. Solving a 25-variable twisted source required 42 complete GAC/backtracking nodes. If `a_v` satisfies all twisted base clauses `C(a_u+t_(u,j),a_v+t_(v,j),a_w+t_(w,j))`, the entire lifted source is satisfied by `W_(v,r)=(a_v+r) mod 5`. The explicit 125-color witness passed **125/125** independent original-C checks using the polynomial discriminant `((x-y)*(y-z)*(z-x))^2 mod 5 = 4`, exhaustive cross-checked against all 125 tournament triples.

Complete lifted C-source SHA-256 (compact JSON): `d1f6e492c86aefa571b9a29c57c054964fdbecdb8cbf03687156cb5a870b4213`. Complete lifted witness SHA-256: `20e0dd2b4476fc51b100ce55cd3da20b483645d2c3eff67098e726b03cde1e1f`.

Additional seeded controls: **12/12** connected random two-sheet covers (seeds 2026111900 through 2026111911) have exact girth 8 and complete independently verified SAT witnesses, 600/600 physical C checks. The deterministic SAT search used 2,450 nodes total (15 to 656 per source). This does **not** imply all two-sheet covers are SAT.

## Research firewall / next blocker
**FALSIFIED** as a universal shortcut: taking graph covers of a native clause-critical UNSAT source does **not** automatically preserve UNSAT, criticality, or simultaneously amplify girth. No claim of a new girth-10 UNSAT critical formula is made. It remains **OPEN** to produce a certified **UNSAT** native strict-C girth-10 source, minimize it physically and replay a satisfying assignment for every single original-clause deletion. Neither these cover constructions nor their finite timings imply unrestricted deterministic machine lower bounds or satisfy the N^.195-row / N^.65-block / N^.35-private decomposition.

Reproducibility: independent source/witness/discriminant/girth checker; base 1046-node proof-tree checker; all sources, 12 full binary witnesses, full five-sheet witness, deterministic voltage-search and twisted-affine witness-search scripts, SHA-256 manifest in archive `T5C_Critical_Lift_Girth_Firewall_Run3_20261119.zip` supplied with this run.

Literature: Gross & Tucker, *Discrete Mathematics* 18 (1977) 273-283 (voltage graph coverings); Exoo, *Electronic Journal of Combinatorics* 11 (2004) N2, DOI 10.37236/1843; Exoo & Goedgebeur, *DMTCS* 21(3) (2019), DOI 10.23638/DMTCS-21-3-9.
