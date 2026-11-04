# Worst-case derivation-cost programme: living log

Target quantity: W_R(N) = max over UNSAT F, |F|<=N, of min over derivations pi of F in R, cost_R(pi).
Strategy search is not charged. Bridge target: SAT in P  =>  W_R(N) <= poly(N).
P versus NP remains OPEN. Nothing here proves a lower bound. Statuses follow AGENTS.md.

## Entry 2026-11-04 (scheduled run, single agent; the five-role split was not instantiated)

### Result 1 (PROVED/EXACT, elementary): the bridge is vacuous for any R with a known superpolynomial W_R
Let R have a proved bound W_R(N) >= N^{omega(1)}. Then "SAT in P => W_R poly" is logically
equivalent to "SAT not in P". Proof: the consequent is false, so the implication is equivalent to
the negation of its antecedent. So for such R (resolution, cutting planes in the monotone-interpolation
range, bounded-depth Frege, etc.) a proof of the bridge IS a proof of P != NP. It cannot be a weaker step.
For R with W_R unknown (Frege, Extended Frege) the bridge is a non-vacuous conditional, and is the
Cook-Reckhow / Krajicek-Pudlak question below.

### Result 2 (PROVED/EXACT, elementary): a "computational" R makes the bridge trivial and the lower bound equivalent to P != NP
Take R_comp whose derivation of F is an accepting run of a fixed universal machine U on (e, F), with
cost = |e| + steps, where the rule is "e halts on F with output UNSAT". Then
SAT in P => W_{R_comp}(N) <= c + poly(N) (hardwire the poly-time decider e*). Conversely
W_{R_comp}(N) poly => SAT in P on UNSAT instances only, which is coNP-side: the UNSAT-side decider is
poly-time when the minimising e is fixed per length; with non-uniform e it gives SAT in P/poly.
Subtlety to record: min over e of |e| + steps allows a different e for each F, which is a
non-uniform advice. So W_{R_comp} poly <=> coNP-membership of UNSAT in P/poly (the free-strategy
minimisation buys advice). Hence "free knowledge of the best sequence" in a computational R yields only
SAT in P/poly-type statements, and P/poly lower bounds for SAT are themselves open (Karp-Lipton: NP in P/poly
collapses PH to Sigma_2). STATUS: PROVED/EXACT for the equivalence W_{R_comp} poly <=> UNSAT in P/poly
(with |e| charged). This is a barrier-style observation, not progress.

### Dichotomy (summary)
- R syntactic with proved lower bound: bridge == P != NP (Result 1).
- R computational / free strategy: lower bound == non-uniform circuit lower bound for SAT/UNSAT (Result 2); no easier.
- R in between (Frege, EF): bridge needs a simulation of the P-algorithm inside R.
  KNOWN THEOREM (Cook 1975/PV; Krajicek-Pudlak 1990): if a poly-time SAT algorithm's correctness is provable in
  PV/S^1_2, then EF is polynomially bounded. Without provability the implication SAT in P => EF p-bounded is OPEN.
  So the weakest sufficient bridge for R=EF reduces to: "every poly-time SAT decider has feasibly provable correctness",
  which is a reflection-style statement and is not known; it is also not implied by anything cheap.

### Consequence for the plan
1. Drop "bridge for syntactic R" as a route: it is P != NP in disguise.
2. Lower bounds for W_EF would imply no new information on SAT in P, but they would refute provable-correctness
   of any poly-time SAT algorithm (contrapositive). That is a genuine, weaker conditional target: 
   "EF superpoly  =>  no PV-verifiable poly-time SAT algorithm" (KNOWN THEOREM direction). Does not give P != NP.
3. Open arrows kept: (a) superpoly W_EF (OPEN, famous); (b) bridge from SAT in P to a fixed R without
   provability hypothesis (OPEN); (c) free-strategy minimisation = advice, so non-uniform lower bound needed.

### Literature check (from memory; no live search was run this session, so treat citations as unverified)
Cook-Reckhow 1979 (proof systems; NP=coNP iff a p-bounded system); Haken 1985 (resolution, PHP); Krajicek-Pudlak 1989
(optimal proof systems, EF); Ben-Sasson-Wigderson 2001 (width-size); Razborov 2015 (proof complexity survey);
Pitassi-Santhanam 2010; Beame-Pitassi surveys. Action for next run: live-search for recent "optimal proof system" and
"feasible reflection / provable correctness of SAT algorithms" results and confirm.

### Next targets
- T1: Formalise "free strategy = advice" precisely with the Karp-Lipton consequence (short note, check it).
- T2: Test whether any natural R between resolution and EF has a provable simulation of a restricted poly-time SAT class (e.g. 2-SAT, Horn): the bridge restricted to a promise subclass, as a sanity check.
- T3: Red-team Result 2's nonuniformity accounting.
