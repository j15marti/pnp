# Worst-case derivation-cost directive: living log

Status of P vs NP: **OPEN**. Nothing below proves a lower bound.

## Shared objective (from the 2026-11-04 scheduled directive)
W_R(N) = max over UNSAT F with |F| <= N of min over refutations pi of F in R of cost_R(pi).
Priority bridge: SAT in P  =>  W_R(N) <= poly(N).
The cost of finding the best derivation is not charged.

## Entry 2026-11-04 (CLAUDE, worst-case-0001)

### 1. What the free-search convention does (PROVED/EXACT, standard)
Not charging for strategy search makes min over pi the cost of a *nondeterministic* certificate.
If cost_R is proof size, or time to check a derivation that R's rules verify in poly time, then
W_R is the Cook-Reckhow proof-size function of R. Consequences:
- W_R(N) <= poly(N) implies NP = coNP (Cook-Reckhow 1979). So a superpolynomial lower bound on W_R, for a Cook-Reckhow R, would prove NP != coNP, hence P != NP. The strategy is the Cook-Reckhow programme and inherits its status.
- If cost counts only a poly-time-checkable certificate, nothing is gained over the proof-complexity formulation.

### 2. The bridge SAT in P => W_R <= poly (PROVED/EXACT trichotomy, by cases on R)
(a) R with an unconditional superpolynomial lower bound (resolution: Haken 1985; cutting planes: Pudlak 1997 / Hrubes-Pudlak; polynomial calculus, bounded-depth Frege): W_R is superpolynomial no matter what. The bridge is then equivalent to SAT not in P. It is not provable without proving P != NP, so it is useless as a *weakest* bridge.
(b) R = Extended Frege (or Frege): the bridge holds if the theory PV (or the relevant bounded-arithmetic theory) proves the correctness of some poly-time SAT algorithm, because then the correctness proof translates into poly-size EF proofs (Cook 1975; Krajicek-Pudlak). Without that provability the bridge is open. It is also a genuine simulation statement: it is equivalent to EF p-simulating the trivial system "pi = (algorithm M, claim M(F)=0)" on the relevant formulas.
(c) The trivial system (the proof is the run of a fixed poly-time decider) satisfies the bridge by definition, but it is not a "logical inference system" and fails the natural-system requirement (i.e. it hides the whole difficulty in M).
So the weakest sufficient bridge is not a pure counting statement. It is a *reflection / provable-correctness* statement for R. This is the missing transfer theorem and it is OPEN for Frege and EF (Krajicek's conjecture that EF is optimal is relevant; it is open).

### 3. Hard-instance survey (what is known, KNOWN THEOREM)
- Resolution: Tseitin on expanders, pigeonhole (Haken), random 3-CNF (Chvatal-Szemeredi, Ben-Sasson-Wigderson).
- Cutting planes: clique-coclique (Pudlak), Fleming et al. lifted instances.
- Polynomial calculus: degree lower bounds; Alekseev (Theory of Computing 22, 2026) gives an exponential bound for PC with square roots and extension variables, which simulates Res-Lin. This is the strongest recent algebraic system, still weaker than EF.
- Frege / EF: no superpolynomial bound known; Krajicek notes no combinatorial candidate tautology is known to be hard for EF. Filmus-Pitassi-Santhanam: depth-d Frege lower bounds on CNF tautologies would already give Frege lower bounds in a strong form.
- Hard-instance families surviving all of these simultaneously: none known.

### 4. Red-team notes
- Barrier: Razborov-Rudich natural proofs apply to lower-bound arguments for sufficiently strong systems when pseudorandom functions exist (Krajicek, "Feasible interpolation", Razborov 2015). A hard-instance argument for EF must be non-natural.
- Shared-DAG and circuit-compression variants of resolution (Res(k), regular vs general, Frege with extension) are all within EF, so the worst-case function for EF is a lower envelope of all of them. "Adaptive strategy switching" is already inside Frege: a Frege proof can mix methods line by line.
- A min over *all* sequences with free choice makes W_R the shortest proof. No model of derivation cost is stronger than this unless R itself changes. So the real choice is R, and the direct path is a lower bound for R in {Frege, EF}, which is open and which is equivalent to showing NP != coNP-type separations only when R is Cook-Reckhow-universal.

### 5. Literature check (this run)
Search found no 2025-26 superpolynomial Frege/EF bound. Newest relevant item: Alekseev, Theory of Computing 22 (2026), exponential lower bound for PC with square roots and extension variables.

### 6. Next targets
1. Decide whether any fixed R below EF but above the proved-lower-bound systems has both (i) a poly simulation from a nontrivial uniform SAT algorithm (bridge) and (ii) a candidate lower bound.
2. Formalise "provable correctness of M in R" as the minimal reflection hypothesis, and test whether it can be derived from SAT in P alone (expected answer: no, relativization/oracle models exist where P=NP yet no proof system provably captures M; to be verified).
3. Audit the corpus's ARC/FLMV spine for any link to W_R (none found).

All load-bearing arrows remain OPEN. P versus NP remains OPEN.
