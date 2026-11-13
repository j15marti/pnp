# LSPV-4/592: Exact Davis-Putnam guard-erasure DAG projection and same-calculus firewall

**2026-11-13 12:36 PST | PNP Time-Space Resource Auditor | historical Route A.** Classification: **PROVED/RESTRICTED** mathematical DP DAG projection, **COMPUTATIONAL** independent exhaustive controls; full historical R_mix341 and P versus NP **OPEN**.

## Candidate and precommitted falsifiers

**Candidate.** For every finite original signed CNF F with fresh guard g and any complete variable-elimination order ending in g, a canonical strict Davis-Putnam (DP) Resolution DAG on F is identical, including its chronological shared parent identities, to the pre-g portion of the corresponding DP DAG on G=(g) AND ∧_{C∈F}(¬g OR C), after deleting ¬g from every nonunit clause. On UNSAT F the guarded proof has exactly ONE additional final guard-pivot Resolution inference. This gives a narrow, explicit cost-underestimating transition projection but NOT the same-source all-transition P2-C3 theorem.

F1: A genuine x-pivot uses guard SOURCE as a parent, violates chronological signed pivots, or loses a shared reference under index rebasing. F2: tautological resolvents or repeated clauses invalidate the proposed one-to-one canonical DP record map. F3: a satisfiable even-charge input incorrectly produces a final paid g-resolution or an empty strict clause. F4: the /386 odd-Tseitin-only parser is silently treated as accepting arbitrary strict 3-CNF or the mixed R_mix341 checker is claimed recovered.

## Theorem 592.1: signed shared-DAG guard projection

Let F be a finite CNF on variables X, represented by canonical non-tautological signed clauses. Let g∉X be fresh. Fix a permutation x_1,...,x_n of X. DP_X means eliminate variables in that order: for each x replace all active x-positive/x-negative clauses by all **distinct, nontautological** complementary-pivot resolvents, retain all x-free clauses, and preserve chronological SOURCE/RES indices for proof ancestry. A derived identical active clause is reused rather than paid again in the chosen DP implementation; paid Resolution record *occurrences* remain distinct when actually emitted.

Define G_g(F)={(g)}∪{(¬g∨C):C∈F} and execute DP_{X,g} on G_g(F), with g eliminated last. Let L_g(C)=C∪{¬g} and P_g(L_g(C))=C.

**Exact statement.** After every original-variable elimination prefix, the guarded active database is exactly { (g) }∪L_g(active unguarded database), and every pre-g paid RES record has a corresponding strict RES record, with identical pivot, signed parent clauses and shared DAG ancestry, under the chronological index rebasing which removes the single unit SOURCE (g). Consequently

```
R_guarded_before_g(F) = R_strict(F)
R_guarded(F) = R_strict(F) + 1_{F UNSAT}.
```

If F is UNSAT, the unguarded variable-free database contains the empty clause. The guarded database contains (¬g) and (g); one actual strict g-resolution yields the empty clause. If F is SAT, no (¬g) appears, and no final g-resolution exists.

**Proof.** Initially L_g is injective on signed clause sets and gives a one-to-one mapping of every F SOURCE occurrence to its guarded SOURCE occurrence; the added (g) is tracked separately. For x≠g, (g) is x-free. L_g preserves both polarities of x. A pair of lifted parents has a non-tautological x-resolvent iff the corresponding F parents have a non-tautological x-resolvent, and their results satisfy Res_x(L_g(A),L_g(B))=L_g(Res_x(A,B)). No positive g can occur in these results, so no new g-tautology arises. Injection preserves duplicate filtering. By induction, the exact active clause sets, emitted RES chronology and both signed parent pointers correspond at each x step. Each guarded paid pre-g RES identity maps to one strict paid RES identity once; all shared references rebase consistently. After eliminating X, the variable-free F database is either empty (SAT) or contains the empty clause (UNSAT), by the exact existential DP satisfiability identity. In the latter case L_g(∅)=(¬g), and exactly one RES between (g) and (¬g) yields ∅. No other new RES exists at the final step. QED. This is a mathematical theorem for the specified canonical DP compiler, not a claim about every legal native proof.

## Corollary 592.2: whole-DAG resource simulation on the selected path

Under the synthetic **strict Resolution** one-unit-per-new-inference tariff, each pre-g paid edge maps to exactly one strict paid edge, cost 1≤1; the final guarded g-pivot maps to the already reached strict empty goal with cost 0≤1. The source and guard unit map without paid work. If a separate unused paid /386 CLI gate owner is present, it has no strict analogue and maps at cost 0≤1. Hence **along this particular DP construction** R_strict = W_guarded−2 when the /386 packet contains one dead paid owner (as LSPV-2/605 explicitly does). Every paid strict identity is charged once; shared SOURCE parents are reused without additional inference charges.

This map **changes the source** from G_g(F) to F and is therefore not the required same-source P2-C3 simulation. It cannot be inserted into a lower-bound proof without separately authenticating the source translation in the fixed target calculus. It does not simulate arbitrary /386 DEF, paid definitions, branch/join, XOR, AND3, LOCAL-CONVERT, deletion or an unknown mixed operation. Unknown transitions remain conservative MAY. A candidate potential must still obey Phi(a)≤c(a,b)+Phi(b) on **every** actual abstract edge and Phi(goal)≤0. Telescoping cannot be inferred from this restricted projection.

## Independent finite execution

The newly published Python program constructs both signed CNFs independently, runs canonical DP from original signed clauses, checks every actual resolvent and chronological parent reference, then compares each paired clause and parent index under guard erasure. In 16 odd-charge prism cases m=3,...,15,20,30,40 (2m cubic vertices, 3m edges, 8m proper signed three-clauses) all paired DAGs agree. The charged /386-style one-owner accounting agrees exactly with LSPV-2/605's original-checker samples for m=3,...,12. Examples:

| Prism m | Strict proper-3CNF RES | Guarded RES | Guarded W including one genuine paid CLI sentinel |
|---:|---:|---:|---:|
| 3 | 79 | 80 | 81 |
| 4 | 159 | 160 | 161 |
| 5 | 239 | 240 | 241 |
| 10 | 639 | 640 | 641 |
| 40 | 3039 | 3040 | 3041 |

The empirical identity R_strict=80m−161 held at each of the 16 m values. **This numerical linear formula was not independently proved for all m.** The generic guard-erasure theorem above is proved for all finite F and all elimination orders.

The auditor also exhausts 256 subsets of the eight proper 3-clauses on variables 1,2,3 and all six variable orders (1,536 cases), plus 18 explicit unit, empty and mixed-width cases: **1,554 exact checks, 1,536 SAT and 18 UNSAT**. It separately tests even-charge satisfiable prism sources at m=3,4,5: each gives identical strict/guarded RES counts and no terminal guard resolution. These are finite, locally executed standard-library Python checks, not original-checker executions.

Published executable: `experiments/arc/lspv4_592_guard_projection.py`, Git blob `894998fb8c684654919c7904cf4a0b4810c8228e`, SHA256 `b839f55e314534803716af843f51a603773ce1851bc4f420b3dd99db5663792f`. Published raw: `results/raw/arc/2026-11-13_1236_LSPV4_592_GUARD_PROJECTION_RAW.json`, Git blob `10dc8f99c7a40af6be8007a55502240895a6053e`, SHA256 `adb1532175a6a266b12d7bb15ef7614aaa6262a033061689d4c3696448acfbd3`. These published blobs exactly match the locally executed files.

## P2-B2/B3 quantitative bridge and P2-D1 firewall

The family-specific source relation is explicit: F_m has 8m strict three-clauses, whereas G_m has 8m clauses of width four plus a guard unit. Their SAT labels coincide under g=1, but their literal source bytes and rule languages do not. On odd-charge prism, F_m is UNSAT by parity of edge incidence. LSPV-2/605 proved a conservative O(m) native guarded /386 DP proof in the unbounded-index mathematical grammar and executed twelve OS Node packets; the new exact projection gives a short **ordinary strict Resolution** proof of F_m, not an original-/386-accepted proof of F_m.

Thus the weak family-restricted bridge holds trivially for this easy prism class in strict Resolution, independently of the existence of any hypothetical general SAT decider: W_RES(F_m)≤(3m+1)3^9, with N_m=Theta(m log m), and so for every correct deterministic decider A this restricted family has W_RES(F_m)≤C(N_m+T_A(N_m)) with universal C, provided the stated mathematical Resolution convention. This is **NOT** an R_mix341 B2/B3 result, does not quantify over arbitrary UNSAT F, and supplies no hard-family lower bound. It underscores why inexpensive algebraic or Resolution shortcuts must remain legal in any B1 minimization.

A verifier accepting G_m is not thereby a sound source-bound verifier for F_m. LSPV-3/620 and /621 independently establish the recovered /341 SAT-source false acceptance and /386 restricted odd-charge source; the complete historical R_mix341 dispatcher and exact mixed tariffs are still unauthenticated. Never substitute this projection or an invented new grammar as an authentic native transition. The /341 64-model counterexample remains a genuine failure for that sibling, not a spurious CEGAR path.

## Resource axes and transfer audit

* **Logical inference work:** exact DP counts above. SOURCE and the g-unit are zero tariff; the optional /386 CLI owner is genuinely once-paid and unused, not a free extension.
* **Evidence and indices:** the guard adds a signed literal to each original clause; removing it changes clause bytes, IDs, and parser domain. No equality of evidence lengths is claimed. Bit length N_m=Theta(m log m) for canonical indexed strict sources.
* **References and verification:** the ordered shared parent DAG is explicitly rebased and independently replayed. The original /386 checker was **not executed in this run**; /605 reports separate original OS replays. We do not assign its assertion counters to our program.
* **Time, span and memory:** logical RES count is not DP discovery time, original-checker sequential bit time, proof parallel span or physical peak RAM. The program stores all records and active clauses and is not an optimal-space machine realization.
* **Zero-cost rules, deletion and reuse:** no native deletion, recomputation, contexts or mixed rules are in the DP construction. Do not erase paid histories or extrapolate no-recomputation cost to arbitrary proof DAGs.
* **Cost partition:** all pre-g RES identities have a one-to-one image; the guard-pivot and one unused paid owner are separately isolated. No sum of overlapping local lower bounds is taken.

## Corpus reconciliation, literature and status

Read both root trackers: `proof1.txt` blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`; full `proof2.txt` via Git blob `930c5eeddafce656717f28055a7a9a755f44737c` (file endpoint returned empty); issue #3 and current comments; `AGENTS.md`, `CODEX.md`, project skill, user two-gate handoff, LSPV-1 full-chain review, root `main.tex`; LSPV-2/539, /547, /549, /604, /605, LSPV-3/620, LSPV-4/539 and /549, /591, LSPV-5/523, LSPV-1/443, Grok 2026-11-13. Claude-specific project reports under `research/agents/claude` were not directly loaded; no corresponding full mixed authority was found.

Distinct from LSPV-2/605: /605 proves DP native acceptance on a restricted guarded source and bounded-prism asymptotic upper bound. **New here** is the all-CNF exact pre-g shared-parent-DAG projection, its one-final-inference delta and independent strict-3CNF construction with exhaustive same-DAG controls. This does not supersede /605 or claim priority over general DP substitution folklore.

Primary references: [1] Davis & Putnam, JACM 7(3), 1960, DOI 10.1145/321033.321034 (Resolution elimination); [2] Cook & Reckhow, JSL 44, 1979, DOI 10.2307/2273702 (fixed proof systems versus complexity); [3] Cousot & Cousot, POPL 1977, DOI 10.1145/512950.512973 (simulation/abstraction); [4] Ben-Sasson & Wigderson, JACM 48, 2001, DOI 10.1145/375827.375835 (Resolution size/width, not arbitrary mixed-calculus bounds). These provide no R_mix341 grammar or arbitrary-algorithm compiler.

**Affected IDs:** restricted diagnostic for P2-C3 and P2-B2/B3; source firewall P2-D1; prism is unsuitable as P2-B1 hard candidate. All remain **OPEN**. P2-B2/B3 are separately OPEN. No physical machine lower bound, generalized proof-system lower bound, or P versus NP separation follows.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither tracker contains a newly closed load-bearing node. No agent, schedule, identity, historical weight, route allocation or main.tex ownership was changed. The next useful falsifier is one authenticated *same-original-source* R_mix341 mixed-rule cross-transition and its exact count-once abstract successor, or a genuine same-calculus arbitrary-decider reflection compiler. P versus NP remains OPEN.

END_OF_VERIFIED_REPORT::LSPV-4::592
