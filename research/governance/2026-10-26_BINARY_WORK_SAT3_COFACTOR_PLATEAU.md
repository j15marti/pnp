# BINARY-WORK-SAT3: scope-complete ANF plateau and cofactor degrees
Date: 2026-10-26
Status: PROVED subject to independent peer audit for declared models; COMPUTATIONAL finite tests pass. P vs NP OPEN.
Additive to existing enabled agents. Do not change schedules or their research ownership.

## New theorem: ALL clause scopes
Let H be any nonempty family of nonempty supports e subset [n]. Give the clause selector a separate bit for each of the 2^{|e|} complete signed clauses on each e. Q=sum_e 2^{|e|}. Define U_H as UNSAT of the selected clauses. In the Boolean algebraic normal form over GF2, the full Q-variable monomial has coefficient one, hence deg(U_H)=Q and multiplicative AND-gate complexity >=Q-1, even with arbitrary XOR/NOT and sharing.

Proof: U_H(z)=prod_{a in {0,1}^n} [1+prod_{C falsified by a}(1+z_C)]. The top monomial coefficient equals the parity of assignment subsets S that cover every local pattern on every scope. Flipping a source variable acts as an involution on those S. Fixed S have both values at that variable and correspond to covering subsets on the remaining variables with all scopes restricted. Repeat until zero variables; because H is nonempty, there is one required empty scope and exactly one covering subset. Thus coefficient is odd. All nonempty mixed Boolean derivatives are nonzero.

## Decisive EASY comparison
For unary SAT with u=Q/2 independent variables, UNSAT=OR_{i<=u}(p_i AND q_i), has EXACT multiplicative complexity 2u-1=Q-1: u pairwise ANDs and u-1 ORs, each OR costs one AND if XOR is free. Choose u=4 binom(n,3) to equal the Q=8 binom(n,3) inputs of full 3SAT. Unary SAT and 3SAT then have IDENTICAL triplet (Q, full ANF degree Q, all 2^Q-1 nontrivial mixed derivatives), although unary SAT is easy. This falsifies any attempted superlinear SAT circuit lower bound depending only on that triplet.

For proper signed 2SAT clause selectors, a monotone circuit uses the implication graph on 2n literal vertices and Floyd-Warshall closure: at most 16n^3+2n-1 AND/OR gates and depth 4n+O(log n). Exhaustively checked all 4,096 selector combinations at n=3. At 3SAT, prior project monotone projection from missing-edge bipartite MATCHING into full selector UNSAT combined with Cavalar-Goos-Riazanov-Sofronova-Sokolov STOC26 gives a superpolynomial MONOTONE circuit lower bound; cannot transfer to general Boolean circuits because matching itself is in P.

## New cofactor rigidity theorem
For all n>=k>=1 with Q=2^k binom(n,k) and any clause C:
- coefficient of full monomial of U_{n,k}|z_C=0 on remaining Q-1 bits =0.
- deg(U|z_C=1)=Q-1.
- if n=k, U|z_C=0 is identically 0;
- if n>k, deg(U|z_C=0)=Q-2.
For n>k a second omitted clause D on the SAME scope, with falsifying patterns of C,D differing in exactly one coordinate, yields top (Q-2)-monomial coefficient 1.

Proof via coordinate-flip pairing on assignment covering sets, first eliminating variables outside their common support. The new lower-arity coverage requirements are redundant until n=k+1. At that base, 1 missing k-pattern gives 2 admissible covering subsets (even); two missing patterns differing on one coordinate require including at least one of them, giving 3 admissible subsets (odd). For n=k, any omitted signed full-width clause leaves one satisfying assignment. Verified 116 singleton and 142 same-scope distance-one pair coefficients for 1<=k<=n<=4.

Complete double-omission spectra at n=4: width1 Q8, 4/28 parity-one; width2 Q24, 216/276 parity-one; width3 Q32, 432/496 parity-one. These might suggest finer differentiating invariants, but counts alone DO NOT imply gate lower bounds with arbitrary sharing.

## Indexed-input post-read no-go
For any deterministic indexed-input SAT solver with T=N^{t+o(1)}, S=N^{s+o(1)}, t>=1, choose r=o(log N) physically unread input bits. Pre-read the other N-r source bits; simulate all 2^r completed virtual inputs sequentially while overriding deferred coordinates without physical reads; store 2^r answers. Then read deferred bits last and select answer. T'=N^{t+o(1)}, S'=N^{s+o(1)}, post-last-read work O(r+log N). This invalidates any UNIVERSAL post-acquisition-only superpolynomial work requirement without charging all speculative pre-read computation. It does not give a cheap SAT algorithm. The single-head sequential tape cannot inherit this indexed-input construction without simulation cost.

## Audit provenance
Complete local user research package BINARY_WORK_SAT3_complete_sources.zip contains 5-page LaTex PDF, all source code, JSON/raw stdout and hash manifest. Finite checks: 200 scope hypergraphs; 107 direct top-ANF coefficients; all 4,096 n=3 2SAT selectors plus 1,100 n=4 samples; 28,032 deferral table evaluations; 116+142 cofactor identities; unary truth tables n<=6. All passed. Do NOT claim this GitHub note includes uploaded script bytes.

## Next agent assignment / obligation
Test whether the cofactor spectrum across many omitted clauses admits an actual GATE-ELIMINATION lower bound beyond Q-1 on full 3SAT UNSAT while FAILING to give the same bound on unary and polynomial monotone 2SAT controls. Independently validate arbitrary sharing, negations, address costs and encoding. If the attempted invariant is still saturated by easy functions, mark FALSIFIED and move to general circuit or machine-native resource lower bounds. Do not confuse the current max-degree theorem with P != NP.

Sources: NIST multiplicative complexity https://pmc.ncbi.nlm.nih.gov/articles/PMC7047778/ ; Cavalar et al STOC26 https://eccc.weizmann.ac.il/report/2025/102/ ; Mishra-Santhanam ECCC TR26-260 https://eccc.weizmann.ac.il/report/2026/260/ ; preceding BINARY-WORK-SAT2 PDF in user's project context.
