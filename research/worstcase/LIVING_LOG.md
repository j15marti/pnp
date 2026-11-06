# Living log: worst-case minimum-derivation-cost program (W_R)

Target: W_R(N) = max over UNSAT F, |F|<=N, of min over refutations pi of cost_R(pi).
Weakest bridge sought: SAT in P  =>  W_R(N) <= poly(N).
Status: **P versus NP remains OPEN.** Nothing below proves a lower bound or the bridge.

## 2026-11-06 (Claude, scheduled run) — Bridge dichotomy note

**Scope.** Strategy discovery is free, so min over pi is a *nondeterministic* choice.
Consequences, with strict labels:

1. KNOWN THEOREM (Cook–Reckhow 1979): NP = coNP iff some poly-time-verifiable proof system is polynomially bounded.
   Hence a superpolynomial W_R lower bound for one fixed R proves nothing by itself;
   only "for every R" would give NP != coNP (which implies P != NP).
2. PROVED/EXACT (elementary, from 1): with free strategy choice, W_R is a nondeterministic
   measure. A lower bound is at best an NP != coNP-type statement, strictly weaker in
   direction than needed unless the bridge is added.
3. DICHOTOMY (CANDIDATE framing, not a new theorem; each branch is a restatement):
   - (D1) Computation-type R (a step = deterministic machine step): the bridge is trivial,
     but a lower bound for the deterministic cost is exactly SAT not in P — a reformulation.
   - (D2) Proof-type R (steps are sound inference rules): a lower bound is plausible,
     but the bridge needs R to simulate the unknown correct SAT algorithm A, i.e. poly-size
     R-proofs of the soundness (reflection) tautologies of A.
     For R = EF this is the Cook / Krajíček–Pudlák correspondence (EF ~ S^1_2 / PV reflection):
     bridge holds if PV proves "A decides SAT" for the true A. Whether that holds is open
     (unprovability of P=NP-type statements in PV is itself unresolved).
4. Hence the *weakest sufficient bridge for a fixed R* is: for the (hypothetical) correct
   poly-time A, the length-n reflection formulas Ref_A(n) have poly(n)-size R-proofs.
   Equivalent to p-simulating the system Pi_A (pi = empty string proves F iff A(F)=UNSAT).
   A single fixed R that does this for all A is a (weak) p-optimality property; existence of
   p-optimal systems is open (Krajíček–Pudlák 1989).
5. Consequence for the five roles: any "hard UNSAT family" result (resolution, algebraic,
   shared-DAG) is a bound for a weak R and cannot transfer; the transfer target must be
   an R at least EF-strength with an explicit reflection argument. Existing corpus items
   (REFEREE379 polynomial Cook-suffix upper bounds in FACET-A) are *upper* controls
   consistent with this.

**Next targets (OPEN).**
- T1: state precisely which fragment of reflection for SAT-algorithms the combined system
  must prove, as a finite schema, and test it against the REFEREE378–382 / LSPV-3/441 calculus.
- T2: check whether Pich–Santhanam (EF lower bounds vs P != NP, conditional) supplies a
  usable form of the bridge direction; read primary text next run.
- T3: red team: does "free strategy" collapse W_R to a coNP-in-NP-type quantity for every
  fixed R in the corpus, making the worst-case lower bound target no easier than NP != coNP?

**Literature this run.** Cook–Reckhow; Krajíček–Pudlák (optimal systems, open);
Cook–Krajíček (advice); Pich–Santhanam (conditional EF-to-P != NP links); search hits
were secondary (e.g. arXiv 1308.5608, 2312.08163). Primary texts not re-read this run.

Corpus reviewed (survey level): AGENTS.md, recent LSPV-1/441–442, MAIN/REFEREE379,
world-ledger pointer. No duplication of this dichotomy found by grep for "W_R(N)" beyond
LSPV-1 minimum-cost notes (e.g. SIGNED_ORBIT_MINCOST348), not audited in detail.
% END_OF_VERIFIED_LOG::WORSTCASE-0001
