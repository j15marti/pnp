# Living log: worst-case minimum-derivation-cost programme (W_R)

Target: W_R(N) = max over UNSAT F (|<F>|<=N) of min over refutations pi in R of cost_R(pi).
Weakest bridge sought: SAT in P  =>  W_R(N) <= poly(N).
STATUS: P versus NP remains OPEN. Nothing below proves a lower bound or the bridge.

## Entry 2026-11-08 (Claude, scheduled run) — structural audit of the bridge

Status labels per AGENTS.md. Short analysis, not a full LaTeX report.

1. **KNOWN THEOREM (Cook–Reckhow 1979).** "min over pi" with the optimal derivation given for free is
   exactly proof size. W_R(N) <= poly(N) for a sound, complete, poly-time-verifiable R iff R is p-bounded
   on UNSAT. Some such R exists iff NP = coNP. So "W_R superpolynomial for EVERY fixed R" is equivalent
   to NP != coNP (stronger than P != NP). Granting free strategy-discovery removes no difficulty: it
   turns the question into the nondeterministic/proof-size question.

2. **Consequence for the bridge (ANALYSIS, rigorous in outline).** For a FIXED R the implication
   SAT in P => W_R <= poly is not available from simulation alone: simulating the P-algorithm inside R
   needs R to prove the algorithm's correctness (soundness of its output) with a poly-size proof.
   - If R can formalise "M decides SAT" and the claim is provable (e.g. in PV / S^1_2 for the relevant
     uniform statement), then EF-type R gets poly proofs (Cook translation). This is CONDITIONAL on
     provability, not on SAT in P alone.
   - Known: P = NP does not obviously give provable correctness; the unprovability side is the content of
     results like Pich–Santhanam (strong coNP lower bounds for NP cannot be proved feasibly).
   Therefore the bridge as stated is (a) trivially true for R := "run any fixed poly-time SAT machine and
   check its trace" but then W_R lower bound is exactly P != NP (circular, no progress); (b) for natural
   R (Resolution, PC, Frege, EF) a CONDITIONAL on provable correctness. Candidate repair: state the bridge
   as  "PV (or S^1_2) proves SAT in P  =>  W_EF poly", which is KNOWN, and note it makes the programme
   a proof-complexity programme about EF/Frege.

3. **Hard-instance status (KNOWN).** Superpolynomial W_R is proved for Resolution, bounded-depth Frege,
   Cutting Planes (Pudlák/Hrubeš–Pudlák), Polynomial Calculus (Razborov, Impagliazzo–Pudlák–Sgall).
   For Frege and Extended Frege no superpolynomial lower bound is known; that is precisely where the
   bridge would bite. Any "multisign DAG hypergraph" family must be tested against: (i) resolution width/size,
   (ii) PC degree, (iii) shared-DAG compression (Extended Frege extension variables), (iv) adaptive
   switching between systems (a fixed combined system is just another R; lower bounds must be per-R).

4. **Natural-proofs / relativisation red-team note (CANDIDATE barrier).** A lower bound for a
   fixed strong R proved by a "natural" combinatorial property of the DAG hypergraph would, under standard
   PRG assumptions, conflict with Razborov–Rudich-style barriers for EF (Krajíček's proof-complexity
   generators are the relevant hypothesis-driven framework). A direct unconditional EF lower bound is open.

5. **Resource auditor remark.** Adding space/time to cost_R (peak memory of the derivation) does not help:
   space-bounded min-derivation is still a nondeterministic measure. Time–space tradeoffs (Ben-Sasson–
   Nordström for resolution) are real but are about resolution only.

6. **Literature check (this run).** One search only. No new unconditional Frege/EF lower bound found.
   Recent items to read next:
   - Khaniki–Pich–Sokolov, "Efficient Adversaries", CCC 2026 (https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2026.8):
     argues known lower-bound techniques have efficient adversary strategies — relevant barrier for any
     new hard-instance family.
   - Alekseev, exponential lower bound for Polynomial Calculus with Extension Rule, Theory of Computing 22 (2026)
     (https://theoryofcomputing.org/articles/v022a004/): algebraic setting; check transfer to PC+ext
     vs. EF (analogy only; needs a bridge).
   - Metamathematics of Resolution lower bounds (https://arxiv.org/pdf/2411.15515): provability angle on step 2.
   Not verified by primary reading; do not cite as established until read.

## Open arrows (all load-bearing)
- A1: unconditional superpolynomial W_R for Frege/EF (OPEN, long-standing).
- A2: bridge "SAT in P => W_R poly" for natural fixed R without a provability hypothesis (OPEN; likely false-as-stated to prove).
- A3: hard UNSAT multisign-hypergraph family surviving Res/PC/CP/shared-DAG (OPEN; none constructed).

## Next steps
1. Formalise "multisign DAG hypergraph" derivation system R_MS and prove or refute p-simulation by/of EF.
2. Prove bridge version with explicit provability hypothesis; document which theory is needed.
3. Read the three papers above; update this log.
4. Per AGENTS.md, a full LaTeX report + main.tex ownership update is not done in this run.

P versus NP remains OPEN.
