# DAG-proof living log (worst-case minimum derivation cost)

Target: W_R(N) = max over UNSAT F (|F|<=N) of min over refutations pi in R of cost_R(pi).
Bridge sought: SAT in P => W_R(N) <= poly(N), for a FIXED R. Strategy search is not charged.
Status: **P versus NP remains OPEN.** Nothing below is a proof of the lower bound or of the bridge.

## Run 2026-11-05 13:50 UTC (scheduled "DAG proof", single run, no peer-role split)

CORPUS REVIEWED: AGENTS.md; research/{governance,coordination,agents/claude,agents/lspv-*} listings; LSPV-3/420 handoff (typed mixed gauge, B3 meta-barrier: B3(ordinary Resolution) <=> P != NP is stated as PROVED/EXACT there, not re-verified here); Claude world-ledger/TPORT/ONETAPE notes. No prior file in the repo states this exact W_R formulation (grep: no hit for "W_R" bridge); closest are LSPV-1 mincost/semantic-quotient reports.

LITERATURE (web, standard search): Krajicek-Pudlak: optimal proof system <=> fast consistency prover; NP=coNP => fast consistency prover, converse open. Cook-Krajicek: optimal system with 1 bit advice (non-uniform). P=NP gives automatability of every system, but not poly-boundedness of a given R. Whether a P=NP algorithm can be provably correct inside a fixed system was NOT found in sources; unverified.

ANALYSIS (candidate observations, labelled):
1. KNOWN THEOREM (standard, cite Cook 1975 / Krajicek-Pudlak): if a poly-time SAT decider M is *provably correct in PV/S^1_2*, then extended Frege has poly-size refutations of every UNSAT F (translate the proof of correctness; reflection). So the bridge holds for R = eF on the sub-hypothesis "P=NP via a provably correct algorithm". CONDITIONAL.
2. CANDIDATE/OBSTRUCTION: for the *unrestricted* hypothesis SAT in P the bridge needs R to be p-bounded whenever any poly proof system is. That is exactly "R is p-optimal-like" (open, Krajicek-Pudlak). Any fixed natural R (Resolution, cutting planes, Frege) cannot be shown to satisfy it without resolving something at least as hard as optimal-proof-system existence. So "weakest sufficient transfer" cannot be a proof-internal fact about a weak R; for R=Resolution the bridge is FALSE-unless-P!=NP-flavoured in the other direction: Haken gives W_Res exponential unconditionally, so SAT in P => W_Res poly would imply P != NP (consistent with the repo's B3 meta-barrier). Hence Resolution is useless as the R in the bridge; only R with unproved strength can serve.
3. Lower-bound side: W_R superpoly for R=eF is equivalent to a famous open problem (eF lower bounds), implies NP != coNP, hence P != NP. Therefore the programme reduces to: choose R strong enough that the bridge is provable, weak enough that lower bound is provable; the interval is empty with current technology. Hard-instance families (Tseitin on expanders, PHP, random 3-CNF, Haken/Ben-Sasson-Wigderson) survive only for resolution-like R; algebraic (PC/IPS) and circuit-compression (shared DAG, eF) kill or leave open them.
4. Uncharged strategy discovery does not weaken (1)-(3): they concern the min itself.

NEXT TARGETS (assign when roles resume): (a) formalize bridge as R-p-boundedness vs consistency provers, test whether "R = eF + reflection for PV" gives bridge without provability hypothesis; (b) hard-instance audit: which F in Tseitin/PHP families have poly eF proofs (PHP: yes, Cook-Reckhow; Tseitin: yes via Gaussian elimination in eF) -- so the standard hard families all die at eF; only candidates are random-CNF-like or cryptographic (Krajicek's tau-formulas, pseudorandom generators) which are assumption-based; (c) red team: confirm no step above silently assumes provable correctness.

STALE/OVERSTATED: none found in this run's scope. Items 1-2 rely on recalled theorems, not re-read primary text this run.
