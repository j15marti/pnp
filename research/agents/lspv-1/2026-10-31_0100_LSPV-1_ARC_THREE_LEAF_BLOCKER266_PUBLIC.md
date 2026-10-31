# LSPV-1: ARC-THREE-LEAF-BLOCKER266 (2026-10-31 01:00 PDT)

**Status:** KNOWN THEOREM (resolution and subsumption), PROVED/EXACT restricted source-indexed classification, pending independent mathematical referee; COMPUTATIONAL both-label controls. **Universal arbitrary-A -> Phi(A), P=NP and P!=NP all OPEN.**

## Single exact sublemma

Let F be a source CNF with original clauses of width at most 3, and let R_2(F) consist of non-tautological resolvents derived either by one step between two distinct ORIGINAL clauses or by one more step with a THIRD distinct ORIGINAL clause. Every record retains all original clause IDs, pivots and both resolution steps. For R in R_2(F), let rho_R be the coherent source cube assigning all literals of R FALSE.

**Restricted theorem.** A coherent source cube rho is rejected by this specific two-step certificate rule iff there is R in R_2(F) with rho_R contained in rho. The inclusion-minimal rejected cubes correspond exactly to literal-inclusion-minimal R, duplicates removed. Every such rejected cube is UNSAT under F; every R has width <=5. This does NOT characterize all UNSAT source cubes.

**Proof.** Binary resolution soundness gives F entails every indexed R, so rho_R and every extension contradict F. The only accepted certificate is such a recorded derivation falsified by rho, which proves the converse *for this rule*. Falsification-cube inclusion is equivalent to derived-clause literal-set inclusion. Two width-3 clauses resolve to width <=4; the third width-3 clause resolves to width <=5. This is familiar bounded resolution, not a new general SAT theorem.

**Strict advantage over direct source-pair blockers (one finite family):** With original C0=(x OR a OR b), C1=(NOT x OR c OR d), C2=(NOT a OR e OR f), resolution on x then a yields R=(b OR c OR d OR e OR f). Under rho=(b=c=d=e=f=0), source clauses reduce to (x OR a), NOT x, NOT a and are UNSAT. No original-source one-pivot resolvent has its entire falsification cube in rho. Yet F is SAT, for example all variables TRUE.

**Incompleteness:** H8, consisting of all eight proper signed clauses on one triple, is globally UNSAT but has no empty clause among these three-original-leaf conclusions. Neither two failing global endpoints nor a fully incompatible SS/SU/US/UU clause-pair extreme matrix proves UNSAT; an explicit SAT source passes the latter control.

## Four falsifiers

F1, depth-two blockers add nothing to one-step source-pair blockers: FALSIFIED by the SAT chain above. F2, depth-two closure decides every UNSAT source: FALSIFIED by H8. F3, adding this policy necessarily reduces total work: FALSIFIED by selected work counts. F4, endpoint failure or pair-extreme incompatibility alone determines UNSAT: FALSIFIED by independently checked SAT sources.

## Native-model and policy accounting

With fixed-width directly indexed ORIGINAL clause records, a supplied three-leaf resolution proof can be authenticated and checked in polylog(N) time and O(log N) temporary writable bits, including source indices and index-tape operations. Exhaustive discovery has O(m^3) candidates and O(m^3 polylog N) time with such addressing; streaming uses O(log N) scratch, but retention of all clauses may require O(m^3 log N) bits. Variable-width unindexed sources require additional offset scanning or an explicitly charged directory. This cubic policy therefore does not fit the intended N^(11/10) ARC stage. The local module makes zero ordinary SAT child/guest-A calls; unresolved cases must use an exact, separately charged fallback. Neither SAT witness checking nor UNSAT proof verification may be skipped.

The ACTUAL FLMV random-access model (Section 2.1) indexes writable work tapes as well as input; the largest accessed work-tape position counts toward space. Guest DELAY/replay, source reads, child access, tape reset, representation conversion, policy search, child-bit queries and simultaneously retained ancestor state are NOT free.

## Reproducible controls

Local producer and separately coded Python verifier examined 15 ORIGINAL source formulas (10 SAT and 5 UNSAT) with H7/H8, XOR, Horn, Krom, signed renaming, two dense seeded proper-3CNFs, an original-source chain, and the SAT extreme-incompatibility pair. All original signed occurrences retain S and U local targets, each inversion, every SS/SU/US/UU source-pair mode, coherent 0^n/1^n assignments, full clause truth counts, complement checks, intermediate flips and source proof IDs.

Producer checks: 4,227. Independent verifier checks: 123,637. Baseline UP-DPLL explored 711 nodes; depth-two augmented UP-DPLL explored 362, but selected baseline work was 22,154 versus **45,398** including partial source-enumerator/output charges. There were 5,390 source resolution candidate checks, 4,028 failed candidates, at least 6,295 source clause-query proxies, and 948 emitted learned-clause literal occurrences. Maximum traced CPython allocation was 209,790 bytes. These figures are host-level partial-event proxies, NOT a complete FLMV step or space accounting. The full 331KB raw dataset and expanded producer/checker are in the local reproducibility bundle; remote raw upload pending due container-session bridge failure.

## Corpus reconciliation and next barrier

Read REDIRECT1, CONTRACT1, AFFINE-SMALLBIAS-DESCENT-GATE2, CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1, AGENTS/CODEX/pnp-research, root main.tex, issue #3, preceding ARC-PIVOT-ANTICHAIN265, recent LSPV-2/3/4/5 peer handoffs, and DP-QUADRATIC-OUTPUT-FIREWALL234. Bounded resolution and Kullmann-style signed-clause conflict research overlap the logical rule; no novelty claimed. LSPV-2 affine projection and LSPV-4 quiescent guest processing remain restricted positive primitives; LSPV-3 Horn minimum-support optimization is not a mandatory SAT cost; LSPV-5 DELAY/semantic selector escape closes no all-input theorem. Affine small-bias descent remains ONLY a restricted MCSP semantic no-go.

**Single remaining OPEN arrow:** Construct one uniform hereditary source-authenticated compiler Phi(A), for an arbitrary correct polynomial-time SAT decider A with unknown K,L, with real short ordinary SAT children or certified terminals on every residual, SAT+UNSAT correctness, and complete simultaneous resource bounds K'<=max(11/10,3/5+K/2), L'<=max(1/2,L/2) on FLMV's actual machine. The formal fixed point (6/5,1/2) lies inside the actual FLMV (241/200,11642479/23232400) forbidden boundary, but no such compiler exists in the verified project.

## Primary sources

[1] Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), DOI 10.1145/1101821.1101822, especially Section 2.1 and Theorem 5.7.

[2] Beame, Karp, Pitassi, Saks, *The Efficiency of Resolution and Davis-Putnam Procedures*, SIAM J Comput 31 (2002), DOI 10.1137/S0097539700369156.

[3] Oliver Kullmann, *Constraint Satisfaction Problems in Clausal Form II: Minimal Unsatisfiability and Conflict Structure*, Fundamenta Informaticae 109 (2011), DOI 10.3233/FI-2011-429.

END_OF_VERIFIED_REPORT::ARC-THREE-LEAF-BLOCKER266::P_VS_NP_OPEN
