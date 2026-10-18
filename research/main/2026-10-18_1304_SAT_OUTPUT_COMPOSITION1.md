# SAT-OUTPUT-COMPOSITION1 — Two-tier 3-SAT result bits -> hard Circuit-SAT

**Date:** 2026-10-18, 13:04 Asia/Seoul. **Proof status:** P versus NP OPEN.

## Proposal and formal construction

For independent input 3-CNFs (F_1,ldots,F_m), set (b_i={\rm SAT}(F_i)\in\{0,1\}). Feed these fixed decision bits into a separately chosen Circuit-SAT family (C_{m}(b,z)). Study (H(F_1,ldots,F_m)=\exists z\, C_m(b,z)).

This is a *nonadaptive SAT-output composition*, not a single ordinary Circuit-SAT reduction unless the SAT bits can be represented without computing them. The resulting predicate is in (P_{\parallel}^{NP}). A uniform, existential exact two-sided SAT-answer gate (G(F,b,w)) with (\exists wG\iff b={\rm SAT}(F)) would put UNSAT in NP and imply NP=coNP. Positive witness gates can be exact for monotone outer predicates.

## Concrete worked family and lower-bound caveat

Choose a connected degree-3 graph (G_m=(V,E)); let (b_i) be vertex parity charges. Its outer Circuit-SAT constraints are
[
C_G(b,x)=\bigwedge_{v\in V}\left(\bigoplus_{e\ni v}x_e=b_v\right).
]
The direct 3-CNF contains 4m clauses. Because a connected incidence matrix has rank (m-1),
[
\exists x C_G(b,x)\quad\Longleftrightarrow\quad\bigoplus_i b_i=0.
]
Every even charge has (2^{|E|-m+1}) witnesses; odd charge has none. For constant-degree expander graphs, the odd-charge *direct 3-CNF* has known exponential resolution lower bounds (Urquhart 1987). Inner odd-charge Tseitin 3-CNFs on expanders are also exponentially hard for resolution. THESE ARE PROOF-SYSTEM LOWER BOUNDS, NOT UNRESTRICTED SAT RUNTIME LOWER BOUNDS; Gaussian elimination decides Tseitin satisfiability in polynomial time.

Thus (H(F_1,...,F_m)=1\iff\bigoplus_i\mathrm{SAT}(F_i)=0). Its outcome depends on each oracle answer, but neither lower bound proves a hierarchy separation.

## Exact exhaustive computation

A dependency-free Python experiment used six inner (K_4) Tseitin 3-CNFs (each 6 edge vars, 16 3-clauses) and an outer (K_{3,3}) Tseitin Circuit-SAT instance (9 edge vars, 24 direct 3-clauses). It realized and checked all 64 Boolean SAT-result vectors, obtaining 32 outer SAT and 32 outer UNSAT instances. Every SAT instance had exactly 16 witnesses. With all six inner problems UNSAT the outer is SAT. Six cases with exactly one inner SAT all made the outer UNSAT. These are finite correctness tests, not asymptotic lower bounds.

## Proof DAG

- **ESTABLISHED:** odd-charge expander Tseitin resolution lower bound (Urquhart 1987); connected-graph incidence rank; exact 64-vector exhaustive test; monotone one-sided SAT-answer witness gating.
- **CONDITIONAL:** resource-preserving, uniform restricted-model solver simulation may transport an established source bound.
- **OPEN:** robust lower-bound-preserving outer restrictions that genuinely depend on inner SAT bits; matched-model lower-bound composition; MCSP magnification/promise-preserving transport; P vs NP.
- **RETIRED:** unconditional two-sided existential SAT-answer gate (would imply NP=coNP); general unrestricted time lower bound inferred from separate resolution lower bounds.

## Project reconciliation and decision

Reviewed K-ELIMINATION-TRANSFER4, PCP-GATE1, and MAGRED-PROMISESLOPE1. The recovered cofinal clock can absorb an unknown exponent for a **fixed clock-independent semantic bit map**, but cannot by itself transfer resolution lower bounds to arbitrary algorithms. The PCP-GATE1 gating triangle (uniform deterministic gating, low succinct complexity, unconditional hard side) remains open. MAGRED-PROMISESLOPE1 rules out getting exponent-slope amplification from polynomial output inflation without additional structure.

**Allocation:** Develop SAT-OUTPUT-COMPOSITION1 as an experimental restricted-model transport track, subordinate to the current primary META-LIFT/MCSP target. Focus on **ROBUST-OUTER-RESTRICTION1**: construct a parameterized outer Circuit-SAT family whose relevant hard side survives substitution by inner SAT-output gadgets, for a *single explicitly matched proof/solver model*, and prove a polynomial-cost reverse simulation. Any MCSP bridge must account for all threshold/gap, size, clock, and uniformity parameters. Falsify designs where parity/Gaussian elimination makes the whole family easy.

## Primary papers

1. A. Urquhart, *Hard examples for resolution*, JACM 34 (1987), 209–219. https://doi.org/10.1145/7531.8928
2. S. R. Buss and L. Hay, *On truth-table reducibility to SAT*, Information and Computation 91 (1991), 86–102. https://doi.org/10.1016/0890-5401(91)90075-D
3. M. Alekhnovich, E. Hirsch, D. Itsykson, *Exponential lower bounds for the running time of DPLL algorithms on satisfiable formulas*, JAR 35 (2005), 51–72. https://doi.org/10.1007/s10817-005-9006-x
4. A. Garg, M. Göös, P. Kamath, D. Sokolov, *Monotone Circuit Lower Bounds from Resolution*, ToC 16(13) (2020). https://doi.org/10.4086/toc.2020.v016a013
5. I. C. Oliveira, J. Pich, R. Santhanam, *Hardness Magnification Near State-of-the-Art Lower Bounds*, ToC 17(11) (2021). https://www.theoryofcomputing.org/articles/v017a011/


## Follow-up: monotone CLIQUE outer and one-sided witness gate

Replace the parity/Tseitin outer with the CLIQUE decision function. Let (m=\binom v2), choose one independently supplied 3-CNF (F_e) for each possible graph edge, and put (b_e=\mathrm{SAT}(F_e)). The outer Circuit-SAT has existential vertices (z) describing a size-(k) subset (S) and accepts iff every edge inside (S) has (b_e=1):
[
H_{v,k}((F_e))=1
\iff
\exists S\subseteq[v],\ |S|=k:\forall e\in\binom S2,\ \mathrm{SAT}(F_e)=1.
]

**Exact positive-only compilation (ESTABLISHED):** This entire language is in NP. One polynomial-size certificate consists of the chosen (S), plus a separate satisfying assignment for each (F_e) with (e\subseteq S). Verification is polynomial in total input size. It needs no UNSAT certificates for unused edges and therefore avoids the two-sided SAT-output gate obstruction. The witness verifier converts to an ordinary Circuit-SAT instance via standard gate encoding.

The full Boolean CLIQUE function on the supplied (b_e) has known superpolynomial (and in specified ranges exponential) **monotone circuit** lower bounds (Razborov 1985; Alon-Boppana 1987). These bounds are NOT unrestricted Circuit-SAT runtime lower bounds. The existence of a polynomial-size witness verifier is consistent with their monotone circuit lower bounds.

**Finite test (ESTABLISHED):** For all (2^6=64) possible SAT output vectors of six inner (K_4) Tseitin 3-CNF instances, the positive-only witness gate agreed with direct 3-CLIQUE checking on a 4-vertex graph: 23 SAT and 41 UNSAT. The dependency-free project experiment prints this result.

**Highest-value target:** CLIQUE-OUTPUT-TRANSPORT1 / ROBUST-OUTER-RESTRICTION1. Develop a model-matched lifting theorem in which the outer monotone circuit lower-bound invariant survives substituting inner SAT-result gadgets through polynomial-size positive witness gates. Precisely state what restricted model survives; do not infer general SAT time hardness or MCSP magnification without a separate machine/threshold/gap preserving bridge.

Primary sources: https://www.people.cs.uchicago.edu/~razborov/research.html and https://doi.org/10.1007/BF02579196 .
