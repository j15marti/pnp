<!-- CLAUDE REPORT::BRIDGE-WINDOW-0001::2026-11-02 -->
# CLAUDE BRIDGE-WINDOW-0001: where the weakest bridge B3 can live

Role: General SAT Lower-Bound Lead (B1/B2/B3). Directive: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`.
Status: elementary PROVED/EXACT lemmas + KNOWN-technique transfer, stated in the directive's cost model. **P versus NP remains OPEN.** No lower bound on Wbar_R is claimed.

## Fixed objects
R sound, complete, effectively specified, nonnegative weights; W_R(F) = min DAG cost; Wbar_R(N) = max over UNSAT, |enc F|<=N.
LB(R): Wbar_R is superpolynomial. B3(R): SAT in P => Wbar_R <= C(N+1)^k. R <=_p R' means W_R(F) <= poly(W_R'(F)+|F|) for all F (R' p-simulates... i.e. R' at least as strong: write R' >= R when W_R'(F) <= poly(W_R(F)+|F|)).

## Lemma 1 (bridge window) — PROVED/EXACT
(a) If LB(R) is already a theorem, then B3(R) <=> SAT not in P. (Conclusion of B3 is false, so B3 is the contrapositive of "SAT not in P".) Hence for Resolution, cutting planes, bounded-depth Frege, etc., where LB is unconditional, B3 is not a bridge: it is P != NP itself.
(b) If R' >= R then B3(R) => B3(R') and LB(R') => LB(R).
So a useful bridge needs R with LB(R) unproved yet B3(R) provable; stronger R makes B3 easier and LB harder, weaker R the reverse. The directive's "preselected R" must therefore be at least as strong as every system with a known lower bound; Extended Frege (EF) is the natural minimal candidate, with the Pich–Santhanam EF+witnessing-axiom variant as a second.

## Lemma 2 (reflection sufficiency for B1, per decider) — KNOWN technique (Cook 1975 translation), restated with explicit costs
Fix a deterministic decider A. For lengths n and time bound t let x be n formula-bit variables, u the O(t)-size computation-trace variables (EF extension variables, one per gate/cell of the t-step run), y an assignment. Define the tautology
 Ref_A^{n,t}(x,u,y) = NOT[ Trace_A(x,u) accepts-UNSAT AND Eval(x,y)=1 ]  (sound iff A is correct on length-n inputs finishing in <= t steps).
Claim: if R is EF-like (closed under substitution of constants, modus ponens) and Ref_A^{n,t} has an R-proof of cost s(n,t), then every UNSAT F with |enc F|=n, A(F)=reject, T_A(F)<=t has W_R(F) <= s(n,t) + O((n+t)^2).
Proof: substitute x:=F, u:=actual trace (cost-free substitution of constants). The antecedent gate constraints for the concrete trace are derived by unit-propagating the t gate definitions (O(t) lines, each over a bounded-width formula). Eval(x=F,y)=1 follows from the clauses of F by deriving each clause-OR and the conjunction (O(n) lines). Modus ponens yields a contradiction. QED.
Consequence: B1(A) for EF holds whenever EF poly-proves Ref_A; in particular when PV proves the soundness of A (Cook; Cook–Krajíček 2007 show PV |- P=NP iff PV defines an algorithm returning a model or an EF refutation). B2 and B3 follow for that A.

## Lemma 3 (tension) — PROVED/EXACT given Lemma 2
Suppose SAT in P via correct A with running time t(n)=poly(n) and R >= EF. If LB(R), then Ref_A^{n,t(n)} has no polynomial-size R-proofs. Proof: otherwise Lemma 2 gives W_R(F) <= poly(n) for every UNSAT F (A is correct on all inputs), contradicting LB(R). So any proof of B3(EF) that goes through reflection must establish short proofs of Ref_A for an A whose existence is the hypothesis; "P=NP => EF poly-bounded" is the open statement that "polynomial algorithm exists => its soundness is EF-provable", and it is **exactly where the circularity lives**: the UNSAT answer of a machine is verified by no independent witness, unlike the SAT side (Levin search outputs checkable witnesses, so completeness is free; soundness of reject IS the content of P=NP).

## Directive-quantifier bookkeeping
Lemma 2 gives a per-decider B1 for those A with short reflection proofs; the arbitrary-A statement B1 for all correct A is stronger than B3 and is not needed. The parity-recognizer + exhaustive-fallback control still refutes B1 for Resolution only because Res lacks short Ref_A for that A; it does not touch B3(EF) (global runtime exponential).

## Literature check (this run)
- Cook–Krajíček, *Consequences of the provability of NP ⊆ P/poly*, JSL 2007: provability of P=NP in PV <=> PV-computable model-or-EF-refutation. Source via search results above; consistent with Lemma 2/3. Duplicate of known theory; no novelty claimed.
- Pich–Santhanam, ECCC TR23-199: SAT needs superpolynomial circuits if the witnessing formulas w_n^k(f) are tautologies AND EF + w_n^k(f) has a superpolynomial lower bound. Clue: the "reflection" hypothesis can be added as axioms; this suggests defining R* = EF + w-axioms as the fixed R and asking whether B3(R*) is provable (the w axioms are exactly "f verifiably refutes the circuit"), shifting the gap to LB(R*).
- Reflection principles, propositional proof systems and theories (arXiv 2007.14835) and Krajíček BSL 2023 survey: standard framework (theory T corresponds to system P iff short proofs of translations and T proves soundness of P). Access: abstracts via search only; not read in full.
Searches: "P = NP implies Extended Frege polynomially bounded", Pich–Santhanam abstract. No source states B3(EF) as a theorem; it is open.

## Falsifiers proposed
1. Exhibit a correct poly-time A (assuming SAT in P) with provably no short EF proof of Ref_A — would refute the reflection route (not B3 itself).
2. A fixed R with unconditional LB where B3(R) is claimed informative — contradicts Lemma 1(a).
3. Weight convention where trace gate definitions are not O(1) per line: re-check Lemma 2's O((n+t)^2) under bit-weighted costs.
4. A system R in which substitution of constants costs more than 0 (e.g., resolution-with-sources-only): Lemma 2 does not apply.

## Controls
Both-label: reject-only reflection is used; SAT-side answers carry witnesses and are not reflected. Malformed inputs: A's rejection of malformed strings is outside Ref (Eval fixed to well-formed encodings). Free best-derivation selection: only in W_R; Ref proof cost s(n,t) is a derivation cost, no search cost charged. No machine time/space claims.

## Next missing implication
Prove or refute: for fixed R* = EF (+ w axioms), SAT in P => exists poly-time correct A with poly-size R*-proofs of Ref_A (then B3(R*) holds). Pair with a lower bound LB(R*) only if one is proved — none is.
<!-- END_OF_VERIFIED_REPORT::CLAUDE::BRIDGE-WINDOW-0001 -->
