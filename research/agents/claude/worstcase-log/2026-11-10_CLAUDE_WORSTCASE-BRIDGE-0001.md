% CLAUDE REPORT::WORSTCASE-BRIDGE-0001::2026-11-10
# WORSTCASE-BRIDGE-0001: logical status of the bridge  SAT in P => W_R(N) <= poly(N)

Role: shared worst-case directive (all five roles). Scope: living log entry.
Status: P versus NP remains OPEN. Nothing below is a lower bound.

## Corpus reviewed
Repo tree; AGENTS.md; GROKPROOF/2026-11-10_0415_PROGRESS.md; LSPV-1/348 (signed-orbit quotient: exact
W_R-bar(N)=max over orbits, fixed Rmix341); knot/link handoff (CANDIDATE); WebSearch of 2026 proof-complexity
literature (below). No contradiction with the existing OPEN labels was found.

## Observation 1 (PROVED/EXACT, elementary logic)
Fix a sound, poly-time-verifiable proof system R and let B(R) denote "SAT in P => W_R-bar poly".
(a) If W_R-bar is already known superpolynomial (Resolution, PC, CP, bounded-depth Frege), B(R) is
    logically equivalent to "SAT not in P". So for those R the bridge is *as hard as P != NP*, not weaker.
    Together with the lower bound it adds nothing; it only restates the goal.
(b) So the bridge is only a genuine reduction for R whose lower bound is itself open (Frege, EF, or
    stronger combined calculi such as Rmix341 with extension). Then
    [W_R-bar superpoly] and B(R) together give P != NP, and B(R) is the whole content to be supplied.

## Observation 2 (CONDITIONAL / KNOWN-style, needs citation check before promotion)
For (b), B(R) cannot be obtained from NP = coNP alone (Cook-Reckhow gives SOME p-bounded system, not a
prescribed R). A sufficient route is feasible provability: if the hypothetical poly-time algorithm A for SAT
has its correctness reflected by R-proofs of size poly(N) (i.e. R proves the tautology family
"A rejects F => F unsat"), then R is p-bounded. Hence the weakest sufficient bridge is a
*uniform reflection lemma*: R p-simulates the trace of every correct poly-time SAT decider with
poly-size proofs of its correctness. This is the Krajicek-Pudlak / bounded-arithmetic style hypothesis
(PV or S^1_2 proving correctness of A => EF p-bounded). It is NOT implied by SAT in P, because a
polynomial algorithm may be correct without any short R-proof of correctness.
Consequence for our program: a "free optimal derivation" does not remove this obstacle; the optimum min
is over R-derivations, and A's trace is an R-derivation only if its soundness steps are R-derivable.

## Observation 3 (design rule for the SAT-circuit reduction builder)
Any combined inference system whose rule "A rejects F, hence F unsat" is accepted for an arbitrary
machine index A is UNSOUND unless the rule's side condition certifies correctness of A on F; certifying
that is coNP-type. A sound combined system must therefore charge for correctness evidence.
Open arrow (unchanged): derive such evidence from the 2-Route-A/3-Route-B FLMV charged transfer.

## Literature clues (2026), classification
- Arteche et al., arXiv 2506.16956: Proof Analysis Problem for EF is NP-complete; EF proves automating
  Resolution is NP-hard. FAILED/NEUTRAL transfer: concerns proof analysis, not minimum size lower bounds.
- Khaniki-Pich-Sokolov, "Efficient Adversaries", CCC 2026: lower bounds are constructive (adversary
  strategies computable efficiently); a constructive EF lower bound on circuit-lower-bound formulas would
  separate the canonical pair. ANALOGY: suggests any proof of superpoly W_R-bar for strong R must be
  non-constructive in the adversary sense, which interacts with natural-proofs barriers. Audit next run.
- Semantic tree-like Frege bounded-line-size lower bounds, arXiv 2604.28172: superpoly bounds for a
  semantic (not syntactically verified) system. Not usable: our R must be poly-time verifiable.
- Tzameret et al., arXiv 2605.04544: hard CNFs for ideal proof systems via rank feasible interpolation.
  CANDIDATE source of hard UNSAT families for the algebraic arm; interpolation methods are known to stop
  short of EF.
- Alekseev, ToC 22 (2026): PC extension simulating EF with exponential bound for the binary value
  principle over Q; supports that algebraic arms are easier, but the extension is not R-complete for CNF.
- Ren et al., STOC 2026: refuter problem for Resolution size is rwPHP(PLS)-hard; finding hard instances
  for a given system is itself computationally hard - relevant to "certified hard family" construction.
Not yet fetched: full texts (abstracts only). Citations must be verified before any promotion.

## Assignments for next runs
1. Lead: formalize Observation 2 as a precise statement (reflection size parameter rho_R(A,N)) and test
   whether FLMV charged transfer can bound rho_R.
2. Builder: implement a toy sound combined system and measure the cost of charged correctness evidence.
3. Hypergraph/certificates: test Tzameret-family CNFs against Resolution/PC mins with peitl/short-proof.
4. Auditor: verify unit-cost accounting in Observation 1 does not hide encoding blow-up.
5. Red team: try to break Obs.1(a) (e.g. non-uniform or relativized R) and check Obs.2 against known
   relativized worlds.

P versus NP remains OPEN.
% END_OF_VERIFIED_REPORT::CLAUDE::WORSTCASE-BRIDGE-0001
