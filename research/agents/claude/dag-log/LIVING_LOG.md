# Living log: worst-case minimum-derivation program (W_R(N)), "DAG proof" routine

Target: W_R(N) = max over UNSAT F, |F|<=N, of min over refutations pi of cost_R(pi); weakest bridge SAT in P => W_R(N) <= poly(N).
Status of P vs NP: OPEN. Nothing below is a proof of a lower bound or of the bridge.

## 2026-11-07 17:50 UTC  (run Claude/DAG-LOG-0001)

**Corpus reviewed (survey):** AGENTS.md; research/agents/lspv-1..4 reports of 2026-11-07 (esp. LSPV-3/476 shared Resolution-DAG cube retraction, LSPV-3/477 first-inference firewall, LSPV-1/480 bit-PHP backtranslation, LSPV-1/336 clocked optimality reflection, LSPV-1/353 universal reflection); Claude world-ledger and TPORT reports. No prior file named as this routine's living log existed; this file starts it.

**Bridge dichotomy (KNOWN, folklore; restated, not new):**
1. Weak fixed R (Resolution, bounded-depth Frege, PC/Nullstellensatz, cutting planes): unconditional superpolynomial W_R exists (Haken 1985; Ben-Sasson-Wigderson; Pang bit-PHP, cf. LSPV-1/480). But then "SAT in P => W_R <= poly" is *equivalent* to P != NP (its premise would be refuted by a known-true conclusion's negation), so it cannot be proved by simulation. It is false-as-a-simulation: a P algorithm for SAT does not yield short R-proofs unless R can prove the algorithm's correctness.
2. Strong fixed R (one that p-simulates every proof system, i.e. an optimal system): bridge holds trivially, but a superpoly W_R then implies NP != coNP-type separation; the lower bound is as hard as the target. Existence of an optimal/p-optimal system is itself open (Krajicek-Pudlak 1989; Messner), and no superlinear Extended Frege size bound is known.
3. Middle route: R = charged-cost system with derivation steps priced in time/space (the Time-Space Auditor's model). Bridge then needs cost_R(pi) <= poly from a P algorithm: only if "run machine M for t steps" is a unit rule with cost t, in which case W_R <= poly(N) iff SAT in P, circular again.
4. Free choice of the optimal sequence (user's clarification) is sound for lower bounds but does not escape 1-3: it only helps if the system is weak enough that minimum cost is bounded below, which is case 1.

**Consequence / priority:** the weakest sufficient bridge must be a *reflection* statement: R proves (with poly-size proofs) the soundness of the specific P algorithm for SAT. That is exactly the open "optimality/reflection" arrow already tracked by LSPV-1/336, /353, /405. Status: CANDIDATE bridge; OPEN.

**Literature check this run:** web search for 2025-26 news on optimal proof systems / Extended Frege bounds found nothing new; a CCC 2026 paper (LIPIcs vol 383, art. 8) on hardness for EF tautologies encoding circuit lower bounds is flagged for a read next run (not yet read; no claim drawn from it).

**Next run:** (a) read CCC 2026 art. 8; (b) tie the dichotomy to tracker nodes [P2-D1],[P2-D2] by LSPV-5; (c) test whether the hard-instance families of LSPV-3/476-477 survive in a mid-strength system (Res(XOR)/PC over GF(2)), per agent 3.

END_OF_LOG_ENTRY::DAG-LOG-0001
