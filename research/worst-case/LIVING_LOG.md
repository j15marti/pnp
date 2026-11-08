# Worst-case derivation complexity — living log

Status of P vs NP: **OPEN**. Nothing here proves a lower bound. Entries are append-only; newest last.
Target quantity: W_R(N) = max over UNSAT F (|F|<=N) of min over derivations pi: F |-_R bot of cost_R(pi).
Weakest bridge sought: SAT in P  =>  W_R(N) <= poly(N).

## 2026-11-08 — Entry 1: audit of the bridge itself (scheduled run)

Status labels: KNOWN THEOREM / PROVED-EXACT (short argument) / CONDITIONAL / OPEN. Literature items are from memory unless a link is given; not re-verified line by line.

**Setup.** "Multisign DAG hypergraph" has no fixed formal definition in the corpus yet; any choice of R below is a proof system in the Cook–Reckhow sense (poly-time verifiable derivations), so the analysis is independent of it. Cost = size (or size+peak space for the time–space auditor).

**T1 (free search = nondeterminism) — PROVED/EXACT.** Granting the optimal sequence for free makes W_R(N) exactly the optimal proof size of R. So "W_R superpolynomial for a sufficiently powerful R" is an R-specific proof-size lower bound; for R polynomially simulating all proof systems it would imply NP != coNP (Cook–Reckhow 1979, KNOWN THEOREM). This target is therefore *stronger* than P != NP, not an easier route to it, unless the bridge below holds.

**T2 (bridge is trivial for the wrong R) — PROVED/EXACT.** Let R_A = "a derivation is the accepting run trace of a fixed poly-time SAT decider A". If SAT in P, then NP = coNP = P and R_A has poly proofs, so the bridge holds for R_A. But R_A depends on A, hence is not a fixed system independent of the hypothesis; a lower bound for it is just a restatement of SAT not in P. (Reformulation, no progress.)

**T3 (bridge cannot be easier than P != NP for any R with a known lower bound) — PROVED/EXACT.** If R has an unconditional superpolynomial lower bound (resolution: Haken 1985; cutting planes, bounded-depth Frege, polynomial calculus: KNOWN THEOREMS), then "SAT in P => W_R poly" is equivalent to SAT not in P. So proving the bridge for such R proves P != NP outright. Conversely the bridge for weak R is *false-looking-but-unrefuted*, and gives no leverage.

**T4 (bridge for strong R = provability of correctness) — CONDITIONAL.** For R = Extended Frege, SAT in P => EF poly-bounded needs EF (equivalently PV/bounded arithmetic) to prove the correctness of the specific polynomial algorithm for each length. Without that, no implication. This is the "weakest sufficient transfer": 
  (TR) SAT in P  =>  R p-simulates R_A for the witnessing A  (i.e. R proves soundness of A on UNSAT inputs, with poly-size proofs).
(TR) is exactly a feasible-provability statement about the unknown algorithm, so it cannot be established without assuming that provability. Open whether any natural R satisfies TR unconditionally (equivalent in spirit to the existence of an optimal proof system, Krajíček–Pudlák 1989, OPEN).

**Consequence for the plan.** The strategy "lower-bound min derivation cost in a fixed strong R, then bridge" splits into (a) a lower bound that implies NP != coNP-type separations for strong R (open for Frege/EF; no technique, per barrier literature) and (b) TR, which is independent of (a) and unproven. Neither is closer. Retire the hope that the bridge can be obtained "for free" from the choice of R.

**Where a real gain could be.** Weaker-than-bridge uses of the model: (i) restricted R (resolution/PC/CP) lower bounds with *space* accounting inform the time–space ARC spine, but give only conditional-on-simulation information; (ii) the Time-Space Resource Auditor should price the hypergraph inference rules so that R is shown poly-verifiable and poly-simulating Frege (making R a legitimate Cook–Reckhow system); (iii) the Red Team should test whether the multisign DAG calculus p-simulates resolution only, or EF.

**Literature clues this run.**
- Pich–Santhanam, [Strong co-nondeterministic lower bounds for NP cannot be proved feasibly](https://libmast.utm.my/Record/oxford-uuid:4bb0ed7a-1983-4d95-8296-ab973094292e) (STOC 2021): PV cannot prove strong co-nondeterministic circuit lower bounds for NP, unconditionally; relevant barrier to formalizing the transfer in bounded arithmetic. Follow-up: [arXiv 2305.15235](https://arxiv.org/pdf/2305.15235) (Li–Oliveira line).
- Pich–Santhanam, [Towards P != NP from Extended Frege lower bounds](https://www.arxiv.org/pdf/2312.08163): conditional route from EF lower bounds for proving circuit lower bounds to P != NP — the closest published relative of the proposed bridge; its extra hypotheses should be compared against TR. (Classification: useful analogy; transfer theorem would need hypotheses I–II shown for the hypergraph system. CANDIDATE.)
- Not found this run: recent (2025–26) Frege lower bounds or optimal-proof-system progress. Needs a dedicated ECCC/arXiv search next run.

**Role assignments for next cycle (additive, no schedule change).**
- Lower-Bound Lead: state precisely which R (rule set, cost) is meant; prove it is a Cook–Reckhow system and decide whether it simulates EF.
- Reduction Builder: produce the fixed combined inference system and exhibit shortest-derivation certificates on small UNSAT instances (computational).
- Hypergraph/Certificates: candidates for hard UNSAT families; must test against resolution (known hard: Tseitin/PHP), PC, and EF (PHP has poly EF proofs, so not hard there).
- Resource Auditor: size and peak-space accounting per rule.
- Red Team: attack T1–T4 and look for mistakes in T3 (e.g. check that "equivalent to SAT not in P" needs only Haken-type lower bounds, which hold unconditionally).

Open arrows: lower bound for strong R; TR. P vs NP remains OPEN.
