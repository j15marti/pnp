# TMR-5/058 | 2026-11-16 05:48 PST | Red team of the worst-case derivation objective and its SAT-in-P bridge

Role: TMR-5 / PNP Machine Bottleneck Redteam (under the user's updated assignment: "Independent Proof Red Team").
Authority: research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md (read first), compatible SAT-compression directive, AGENTS.md, CODEX.md. Retired proof trackers not read. P versus NP **OPEN**.

Note on sources: the stored task prompt says the agents "reference the shared worst-case research directive on GitHub". No such file exists on main or in research/coordination at 2026-11-16 13:48Z (grep for `W_R(N)`, `overline W_R`, `worst-case derivation` found only unrelated historical reports). This report therefore works from the objective exactly as stated in the stored prompt and does not invent the missing directive.

## 1. Target as stated, with exact quantifiers

Let R be a Cook–Reckhow propositional refutation system: a polynomial-time verifier V_R(F, pi) that is sound (accepts only if F is an UNSAT CNF) and complete. Let cost_R(pi) be proof bit length |pi| (any step measure polynomially related to bit length with poly-time checkable steps gives the same polynomial/superpolynomial classification). Define

    Wbar_R(N) = max_{F in UNSAT, |<F>| <= N}  min_{pi : V_R(F,pi)=1}  cost_R(pi).

Proposed program: (L) prove Wbar_R(N) >= N^{omega(1)} for one fixed strong R; (B) prove the bridge  SAT in P  =>  Wbar_R(N) <= poly(N). Then L and B give SAT not in P.

The user's remark is correct **for R-derivations**: min over sequences is a valid lower bound on the cost of executing any R-derivation, and the cost of discovering the best sequence need not be charged. The red-team question is the load-bearing arrow B, i.e. whether every polynomial-time decider must, in effect, execute a short R-derivation.

## 2. Candidate and falsifiers (stated before literature check)

Candidate: there is a fixed R for which B is provable more easily than P != NP, via a pointwise simulation "the run of any correct decider A on UNSAT F yields an R-refutation of F of size poly(time_A(F))".

Falsifiers: (F1) an explicit correct total decider that is polynomial on an explicit family whose minimum R-refutations are superpolynomial (kills pointwise transfer); (F2) for R with a known lower bound, B_R is logically equivalent to P != NP (no relief); (F3) for strong R, B_R is equivalent to a provability statement about SAT algorithms (shows exactly what B must assert).

## 3. Results

### Theorem 0 (KNOWN THEOREM; Cook–Reckhow 1979)
Wbar_R(N) <= poly(N) iff R is polynomially bounded. Some R has Wbar_R polynomial iff NP = coNP. Hence L for a fixed R is "R is not p-bounded"; L for every R is NP != coNP, strictly stronger than P != NP as a target.

### Theorem 1 (PROVED/EXACT, elementary; external review OPEN). Bridge collapse for systems with known lower bounds
If Wbar_R(N) >= N^{omega(1)} is already a theorem, then B_R is logically equivalent to "SAT not in P".
Proof: (=>) B_R plus the known lower bound gives SAT not in P by contraposition. (<=) If SAT not in P the antecedent of B_R is false, so B_R holds vacuously. QED.
Known unconditional superpolynomial Wbar_R: resolution (Haken 1985 PHP; Urquhart 1987 Tseitin on expanders; Ben-Sasson–Wigderson 2001 width method), tree-like resolution, polynomial calculus over any field (Razborov 1998; Buss–Grigoriev–Impagliazzo–Pitassi 2001 for Tseitin mod q in characteristic p != q; Alekhnovich–Razborov), cutting planes (Pudlák 1997 clique-colouring), bounded-depth Frege (Ajtai 1988; Krajíček–Pudlák–Woods; Pitassi–Beame–Impagliazzo 1993 for PHP).
Consequence: for every such R ("resolution", "algebraic reasoning", "cutting planes", "bounded-depth" in the user's list of item 4), proving the "weakest sufficient bridge" is exactly as hard as P != NP. The lower-bound half of the program is already done for these R, and the entire difficulty sits in B. Any proof of B_R therefore inherits the relativization (Baker–Gill–Solovay), Natural Proofs and algebrization barriers that apply to P != NP itself. Status: B_R OPEN, and not a weakening.

### Theorem 2 (PROVED/EXACT; external review OPEN). Pointwise algorithm-to-derivation transfer is FALSE for every R with an explicit hard family
Let {F_n} be a P-uniform sequence of UNSAT CNFs (F_n computable from 1^n in poly time, |<F_n>| = poly(n), n recoverable from |<F_n>|), with min R-refutation size s(n) = n^{omega(1)}. Define the total decider A(F): compute the unique candidate n from |<F>|, generate F_n, compare bitwise; if equal output UNSAT, otherwise run exhaustive search. A is correct on every input. On every F_n its running time is poly(|<F_n>|), while every R-refutation of F_n has size s(n).
Hence no simulation of the form "time_A(F) small => short R-refutation of F" holds for all correct deciders A, for R = resolution (PHP_n^{n+1}, explicit expander Tseitin), PC over F_p (Tseitin mod q, q != p), cutting planes (clique-colouring), bounded-depth Frege (PHP). Explicit expanders are P-uniform (e.g. Margulis–Gabber–Galil, Lubotzky–Phillips–Sarnak), PHP trivially so.
Natural non-cheating variant: Tseitin over any graph is decided by Gaussian elimination over F_2 in O(N^3) bit operations with no family recognition at all (Urquhart's family is easy for algorithms, exponential for resolution).
Integration point: any proof of B must use the **global** hypothesis SAT in P (e.g. self-reduction, padding, correctness of a single algorithm on all inputs), not the per-instance execution trace. "Every algorithm implicitly performs an R-derivation, so its time is at least min derivation cost" is the precise failed premise. Status of pointwise transfer: FALSIFIED/RETIRED for all listed R.

### Theorem 3 (PROVED/EXACT given KNOWN translations; external review OPEN). Exact content of the bridge for strong R
Let R p-simulate extended Frege (EF) for CNF refutation (equivalently extended resolution). For a poly-time algorithm A with time bound n^k let Corr_A,n be the standard propositional translation (Cook 1975) of "if c is the accepting-UNSAT computation of A on input F (|F| = n) then the assignment a falsifies F"; it has size poly(n) and is a tautology iff A never wrongly reports UNSAT on length-n inputs.
Claim: B_R  <=>  [ SAT in P  =>  some poly-time correct SAT decider A has poly(n)-size R-proofs of Corr_A,n ].
(<=) Given short proofs of Corr_A,n, for an UNSAT F substitute the bits of F and of A's actual computation c (poly size), discharge the computation hypotheses by poly-size EF evaluation of variable-free formulas, and obtain a poly-size EF (hence R up to p-simulation) refutation of F. Thus Wbar_R(N) <= poly(N).
(=>) If Wbar_R(N) <= poly(N) then R is p-bounded; Corr_A,n are poly-size tautologies (A correct), so they have poly-size R-proofs (negate and Tseitin-encode to a CNF of size poly(n), refutation transfers back in EF-strength systems).
Consequence: for R = EF the bridge says "if P = NP then P = NP is witnessed by an algorithm with EF-short correctness proofs". By Cook 1975 this holds if some poly SAT algorithm is provably correct in PV. Combined with an EF lower bound the program would show that NP in P is not PV-provable for any algorithm — the known consequence of EF lower bounds — but upgrading that to "NP not in P" is exactly the unproved bridge. No technique is known for B_EF; it is not implied by P = NP alone. Also Krajíček–Pudlák 1989: E = NE implies a p-optimal proof system exists, and P = NP implies E = NE by padding; so under P = NP a p-optimal R* exists and is p-bounded — but R* is defined from the collapse and the implication cannot be used to fix R in advance in a way that yields B for a pre-chosen EF.
Status: B_EF OPEN; Wbar_EF superpolynomial OPEN (no superpolynomial lower bound for Frege or EF is known).

### Corollary (scope of item 4 of the prompt)
"Survives resolution, algebraic reasoning, circuit compression, shared DAGs and adaptive switching" is a property of R-proof size for R containing those systems; for any union R of finitely many systems listed in Theorem 1 the lower bound requires one family hard for **all** components simultaneously (a finite union is p-bounded iff some component handles every family). Example of failure: PHP is hard for resolution and PC but has polynomial cutting-planes proofs (Cook–Coullard–Turán 1987); Tseitin is hard for resolution but has polynomial PC_F2 proofs and quasipolynomial CP proofs (Dadush–Tiwari 2020). So both standard families are FALSIFIED as hard instances for the "fixed combined inference system" Res ∪ PC_F2 ∪ CP.

## 4. Executed finite illustration (COMPUTATIONAL only)

Executable experiments/tmr/tmr5_pointwise_transfer_falsifier058.py, revision tmr5-pointwise-transfer058.v1, deterministic (no seed), CPython 3, Git blob 1dcace91efbca6fb32c05de700999a78e6bbca0d. Raw output results/raw/tmr/2026-11-16_0548_TMR5_POINTWISE_TRANSFER058_PY_RAW.json, blob a2f1be8c76a4cdbe4c4e580703097785808031cd. Total 16.0 s. Exhaustive UNSAT verification by brute force for every instance; exact minimum decision-tree leaves L by memoized search (minimum tree-like resolution size in [L, 2L-1]).

| instance | vars | clauses | min DT leaves L | recogniser comparisons / GE row-ops bound |
|---|---|---|---|---|
| PHP_1^2 | 2 | 3 | 3 | 7 |
| PHP_2^3 | 6 | 9 | 11 | 27 |
| PHP_3^4 | 12 | 22 | 43 | 70 |
| Tseitin K4 | 6 | 16 | 28 | 16 |
| Tseitin K3,3 | 9 | 24 | 76 | 36 |
| Tseitin prism | 9 | 24 | 48 | 36 |
| Tseitin cube Q3 | 12 | 32 | 128 | 64 |

PHP_4^5 (20 vars) exceeded the 30 s stage budget and was NOT executed. These finite numbers prove nothing asymptotically; the asymptotic gap is the KNOWN THEOREMS cited. Only tree-like resolution was computed; general resolution, PC and CP minima were not computed.

## 5. Resource ledger
The objective is a nondeterministic proof-size measure: no time/space for a decider is asserted. Theorem 2's decider: recognition O(|<F>| poly log) time and O(|<F>|) space on the family; exhaustive fallback 2^{O(n)} elsewhere (correctness only). Gaussian-elimination control O(N^3) bit operations, O(N^2) space. Discovery of the optimal derivation not charged, per the user's convention; this does not affect any conclusion above.

## 6. Four gates
- DISJ sanity: NOT APPLICABLE (no rank or communication argument); easy-family controls (Tseitin/GE, PHP/CP) were applied and are what falsify the transfer.
- Relativization: Theorems 1–3 relativize trivially as stated; B_R for any R in Theorem 1 is equivalent to P != NP, so any proof of B_R must be nonrelativizing, non-natural and nonalgebrizing: OPEN/blocking.
- Simultaneous DTISP: NOT APPLICABLE (proof-size measure, no same-machine time-space pair).
- Deterministic configuration counting: NOT APPLICABLE as lower bound; upper-bound guard only.
/341 FAIL as full UNSAT authority; /386 RESTRICTED. Neither is used.

## 7. Ranked advice to the five assignments
1. General SAT Lower-Bound Lead: do not try to prove B_R for resolution/PC/CP/AC0-Frege; Theorem 1 shows it is P != NP verbatim. For EF, state B_EF in the Theorem 3 form and look for a reason why P = NP would force EF-short correctness proofs; none is known.
2. SAT-Circuit Reduction Builder: a combined system Res ∪ PC_F2 ∪ CP already defeats PHP and Tseitin; "certified shortest derivation DAGs" on small instances are finite data, not lower bounds.
3. Hypergraph & Proof Certificates: needed is one explicit family hard simultaneously for every component of the fixed combined R; random 3-CNF is believed hard for all three (known for Res, PC; CP known for random O(log n)-CNF, Fleming–Pankratov–Pitassi–Robere 2017; Hrubeš–Pudlák 2017) but is not P-uniform, and none of this touches B.
4. Resource Auditor: Wbar_R carries no time or space semantics; any time claim must come from B.
5. Red team (this role): pointwise transfer FALSIFIED; worst-case B equivalent to P != NP for weak R and to a provability statement for EF.

## 8. ONE next load-bearing lemma
Precisely state and test the only nonvacuous form of the bridge: for R = EF, is there any known consequence of P = NP (e.g. E = NE, collapse of PH, existence of p-optimal systems) that yields poly-size EF proofs of Corr_A,n for a fixed A? Either cite a theorem or record B_EF as an independent assumption equivalent to "P = NP implies PV-style provability". No P != NP claim.

## 9. Primary sources consulted this run
Cook & Reckhow, J. Symbolic Logic 44 (1979); Cook, STOC 1975 (PV); Krajíček & Pudlák, J. Symbolic Logic 54 (1989) — confirmed via search: NE = coNE suffices for optimal, E = NE for p-optimal systems; Urquhart, J. ACM 34(1):209–219 (1987) — confirmed; Dadush & Tiwari, CCC 2020, "On the Complexity of Branching Proofs" — confirmed quasipolynomial CP proofs of Tseitin (arXiv:2006.04124); Haken 1985; Ben-Sasson & Wigderson 2001; Pudlák 1997; Cook–Coullard–Turán 1987; Buss–Grigoriev–Impagliazzo–Pitassi 2001. Only the Krajíček–Pudlák, Urquhart and Dadush–Tiwari statements were re-checked against sources this run; the others are cited from standard knowledge, not re-read.

## 10. Validation actually run
Preflight `.codex/skills/pnp-research/scripts/preflight.py --check --json`: ran, document_ok/ownership_ok for main5; mathematical_validation NOT_PERFORMED. Python stage above. LaTeX compilation: see handoff. No Lean, no independent external review.
