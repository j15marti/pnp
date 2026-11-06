# Worst-case derivation-cost programme — living log

Directive (user, 2026-11-06): study
  W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi)
for a fixed sufficiently powerful system R (multisigned DAG hypergraph of 3-SAT, minimal reduced
state, minimal work), strategy discovery NOT charged. Priority bridge:  SAT in P  =>  W_R(N) <= poly(N).
Five roles: General SAT Lower-Bound Lead; SAT-Circuit Reduction Builder; Hypergraph & Proof Certificates;
Time-Space Resource Auditor; Independent Proof Red Team. Additive: no schedule/agent-count change.
Status: **P versus NP remains OPEN.** Nothing below proves a lower bound.

## Entry 2026-11-06 (Lead + Red Team view)
**Theorem 1 (bridge is not weaker; PROVED/EXACT, trivial).** Fix R. Let B_R := (SAT in P => W_R <= poly).
If W_R is known superpolynomial (e.g. Resolution, Haken 1985; also PC/CP/bounded-depth Frege families),
then the conclusion is false, so B_R is logically equivalent to "SAT not in P". Proving B_R for such R *is* P != NP.
Hence "weakest sufficient bridge" is only meaningful for R with *unknown* W_R.

**Theorem 2 (optimal R makes the bridge true but the target strictly stronger; PROVED/EXACT given Cook–Reckhow).**
If R is an optimal proof system for TAUT (simulates every proof system with poly blowup; cost ~ size),
then B_R holds: P=NP => NP=coNP => some system is poly-bounded => R is. Then W_R superpoly <=> NP != coNP,
which implies P != NP. So the programme reduces to NP != coNP for an optimal R, a harder statement.
Existence of optimal R is OPEN (implied by NE=coNE, Krajíček–Pudlák 1989).

**Consequence / quantifier-order obstruction.** A fixed R cannot depend on the unknown decider D.
The trace system R_D = {(F, accepting trace of D)} gives W <= poly under P=NP, but D is chosen after R.
Making R universal needs soundness-checkable correctness of D, i.e. a theory T: R_T = (T-proof that M decides SAT, trace).
Then B_{R_T} <=> "P=NP is T-provable with a poly-time witness" – connects to Pich–Santhanam
(strong co-nondeterministic lower bounds for NP cannot be proved feasibly); a lower bound for W_{R_T}
would need to be unprovable in T-weak theories. CANDIDATE next target (T-BRIDGE): classify which T make
B_{R_T} unconditional-ish; red team: check unprovability barriers.

**Cost model note (Auditor).** Free strategy discovery = nondeterminism, so W_R is a coNP-flavoured
measure; any time–space cost c with c >= size/poly keeps Theorems 1–2 valid. Shared-DAG/multisigned
hypergraph states do not change them unless R is shown non-simulable by EF-type systems.

**Literature (searched 2026-11-06):** Cook–Reckhow 1979; Krajíček–Pudlák 1989 (NE=coNE => optimal system);
Köbler–Messner–Torán (NEE/EE improvement); Cook–Krajíček (optimal systems with 1 bit advice);
Messner (P=NP => optimal acceptor iff p-optimal proof system); Egidy–Glaßer–Herold 2023 (arXiv 2304.14702);
Egidy 2026 preprint arXiv 2602.02294 (unverified by me). No source settles existence of optimal systems.

**Open arrows:** (a) any superpoly W_R for R strong enough (EF) — OPEN; (b) bridge for non-optimal R with
unknown W_R — no mechanism known; (c) T-BRIDGE — CANDIDATE.
**Retired:** "prove the conditional bridge for resolution-like R" (equivalent to P != NP, Thm 1).
