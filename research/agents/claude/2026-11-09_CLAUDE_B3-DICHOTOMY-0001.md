# CLAUDE B3-DICHOTOMY-0001: what the bridge B3 can and cannot do (2026-11-09)

Status: PROVED/EXACT (elementary logic) + KNOWN THEOREM citations. P vs NP remains OPEN. No lower bound on Wbar_R is claimed.

## Setting
Fixed sound, complete, effectively specified R; Wbar_R(N) as in `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`.
B3(R): SAT in P  =>  Wbar_R(N) <= C(N+1)^k for some C,k.
LB(R): Wbar_R is superpolynomial.

## Proposition 1 (B3 + LB => P != NP). PROVED/EXACT
Contrapositive of B3 applied to LB(R). Trivial; this is the intended use.

## Proposition 2 (B3 is vacuous-or-circular when LB(R) is already known). PROVED/EXACT
If LB(R) is an unconditional theorem (R = Resolution [Haken 1985], tree-like, bounded-depth Frege [Ajtai; Pitassi-Beame-Impagliazzo; Krajicek-Pudlak-Woods], polynomial calculus, cutting planes [Pudlak]), then B3(R) is equivalent to "SAT not in P".
Proof: LB(R) makes the consequent of B3 false, so B3(R) holds iff the antecedent fails. QED.
Consequence: proving B3 for such R is exactly proving P != NP. So the bridge is only informative for R whose lower bound is OPEN (Frege, Extended Frege, strong mixed calculi like the ER2/OWNER system of the /5xx reports). Evidence about weak subsystems of R (e.g. the 148-node CORE splice, LSPV-1/526) says nothing about B3 for R.

## Proposition 3 (B3 for strong R is a feasible-reflection statement). KNOWN-THEOREM-based, CONDITIONAL
- NP = coNP iff some proof system is polynomially bounded (Cook-Reckhow 1979). P = NP gives NP = coNP, hence SOME poly-bounded system, but it does not identify a PRESELECTED R (the web-search summary retrieved this run wrongly implied EF is the witness; it is not known to be).
- P = NP gives the trivial system "x is a proof of F if x = empty and the poly-time decider A rejects F". It is p-bounded but its soundness for A is not an R-derivation: it fails the "no hidden validity oracle / uncertified machine correctness" rule of the directive, correctly.
- For R = EF the missing step is: EF proves (propositionally, with poly-size proofs) the correctness of the SAT algorithm A. By Cook / Krajicek-Pudlak translation this is equivalent to PV (equivalently the theory behind EF) proving "A is a correct SAT solver". Whether P = NP implies such provability is a known open problem; Krajicek's book (Proof Complexity, 2019, ch. on EF/PV) states it as the question whether EF is optimal / whether feasible reflection holds. So B3(EF) is not known, and a proof of it would be a new theorem about P = NP => PV-provability of correctness for some algorithm, not a bookkeeping exercise.
- Relativization: B3 is a statement about a specific R; any proof must use the structure of R (it cannot be a black-box Cook-Reckhow argument), since for R = Resolution B3 is equivalent to P != NP (Prop. 2) and so cannot be provable by methods that do not already separate.

## Proposition 4 (conditional weakening that is actually provable). PROVED/EXACT
Define R+A: R plus axioms Corr(A) = "A's poly-time computation trace on F rejecting implies F unsat" as a REFLECTION RULE charged one node. Then trivially Wbar_{R+A}(N) <= poly if SAT in P via A. But R+A is chosen after A, violating "fix R independently of instances and sizes" - it is a family of systems indexed by algorithms, i.e. a uniform alternation of quantifiers (exists A) before R. B3 requires R before A. This is the exact quantifier failure to flag whenever a "wrapper" is proposed: hardness against R+A for every A is B1/B2 for a universal R-hat = union over A, which is not effectively a single sound system unless soundness of each A is provable in it. Soundness of the union is the Levin-search issue: it is sound only if every added Corr(A) is true, which is undecidable to enforce.

## Where this leaves the research program (concrete recommendation)
1. Retire any plan that treats B3 as a lemma to be proved after LB(R); Prop. 2 shows it is either vacuous or P != NP itself for weak R, and Prop. 3 shows it is an open feasible-reflection problem for strong R.
2. The only route where B3 may be a genuinely different, checkable statement is to choose R as a *theory-based* system (EF / PV-translation) and prove LB(R) via a route whose hypothesis includes "R proves correctness of A" - i.e. make B3 an explicit conditional assumption (CONDITIONAL status), not a derived arrow. Then the theorem produced is: LB(R) + Reflection(R) => SAT not in P; and Reflection(R) false would mean P=NP world where EF cannot verify its own solver, itself a notable separation of bounded arithmetic. Label accordingly; never as unconditional.
3. Pich-Santhanam (STOC 2021) is the relevant barrier: lower bounds for strong systems that are feasibly provable would yield strong circuit lower bounds, so any feasible-looking LB(R) argument for EF should be audited against it. Related: arXiv 2405.02232 (iEF, proof complexity to circuit complexity).

## Corpus reviewed / audit
Read: AGENTS.md, five-role refocus directive, LSPV-1/526 report head, claude world-ledger README pointers. No duplicate of Props. 2-4 found by file-name search under research/ (not exhaustive byte-reading). Nothing in the corpus claims B3 is proved; this note agrees with that status.
Stale/overstated claims found: none new. Caution retained: web-search summary above is unreliable on EF; only the Cook-Reckhow equivalence was used.

OPEN: LB(R) for any strong R; B3 for any strong R; P vs NP.
END_OF_VERIFIED_REPORT::CLAUDE::B3-DICHOTOMY-0001
