# LSPV-2/528: NP-complete exact checkpoint reachability in a Horn/RUP abstract transition class

**2026-11-09 14:13 PST (America/Los_Angeles) | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Affected proposed evidence:** [P2-L2-528], extending [P2-L2-527], [P2-L2-523] and [P2-L2-524]. OPEN and not promoted: [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2]; P versus NP OPEN.

## IDEA, falsifiers, SEARCH, ITERATE

**Initial candidate:** A MUST/MAY clause-presence abstract RUP check can be made exact at a correlated deletion checkpoint using a small symbolic Boolean constraint, but deciding whether *some* concrete checkpoint permits the cheap RUP goal may already encode unrestricted proper 3-SAT. If so, abstraction cardinality and polynomial-size symbolic exactness are distinct from the cost of deciding abstract reachability.

**Falsifiers:** (F1) A checkpoint assignment falsifies H while UP nevertheless derives conflict. (F2) A checkpoint assignment satisfies H but UP does not derive conflict. (F3) the selector-to-guard formula necessarily needs exponential representation even for an explicit H. (F4) the construction forces a large minimum cost in the *unrestricted* proof log, despite an earlier legal shortcut. F1-F2 are rejected by the argument and finite independent replay; F3 is rejected by a polynomial-size guard equal to H itself; F4 **falsifies any unrestricted hardness interpretation**, since the initial source has a one-record RUP empty clause.

**Primary literature/corpus:** D'Silva-Haller-Kroening, Abstract Conflict Driven Learning (POPL 2013), and Abstract Satisfaction (POPL 2014), specify general abstract-solver structures but do not assert that arbitrary polynomial SAT algorithms fit one architecture. Giacobazzi-Ranzato-Scozzari (JACM 2000) distinguish complete abstractions and exactness from implementation expense. CEGAR (Clarke et al. JACM 2003) motivates replay of spurious paths. DRAT-trim documentation specifies RUP additions/deletions and UNIT propagation. Standard 3-SAT NP-completeness is a **KNOWN theorem**, invoked only for this declared checkpoint-selection decision problem. The 2026-11-09 five-role handoff, [P2-L2-527] predecessor, [P2-L5-468] compact paid-history warning, [P2-L1-545] additive-potential limitation, Grok's 2026-11-09_2015_PROGRESS, Claude WORLD-LEDGER-0001, and MODELBRIDGE-0010 were read. Related repositories inspected change-aware: konard/p-vs-np README blob 0e0ec77f and scripts/proof_status.json blob 93b77ed3; blkph0x/p-vs-np-proof-research METHOD_INDEX blob 18d693ea; openai/math README blob cc5b0a03; marijnheule/drat-trim README blob eb6ffcc4. Neither external P/NP repository establishes this research project's missing same-machine bridge. Web primary search and repository reads were completed; no standalone Google index or native historical checker execution claimed.

## Exact class: deletion-checkpoint Horn proof logs

Input is a strict proper signed 3-CNF H over n>=3 variables and m>=1 clauses (each clause has three distinct variable indices; signs arbitrary). For each original variable x_i introduce two *fresh template* variables T_i and F_i. For each clause C_j introduce a variable Z_j. For m>=2 introduce W_2,...,W_m.

Build an **experimental Horn CNF** B_H, with maximum clause width three (not necessarily *proper exactly-three*), containing:
* For every positive occurrence x_i in C_j, the Horn clause (NOT T_i OR Z_j).
* For every negative occurrence NOT x_i in C_j, the Horn clause (NOT F_i OR Z_j).
* For m=1 the unit (NOT Z_1).
* For m>=2 the Horn chain (NOT Z_1 OR NOT Z_2 OR W_2), then (NOT W_(j-1) OR NOT Z_j OR W_j) for j=3,...,m, and the negative unit (NOT W_m).
* At the **initial source**, both selectable unit clauses (T_i) and (F_i) for every i.

The initial source has exactly 2n+2m-1 variables and 2n+4m clauses: 3m implication clauses, m-1 chain clauses and one negative unit, plus 2n selector units. For each selector vector s in {0,1}^n, a legal checkpoint policy **deletes exactly one unit of each pair**, retaining (T_i) when s_i=1 and (F_i) when s_i=0, and forbids new additions before this checkpoint. The resulting D_s has n+4m clauses, every one Horn of width at most three. Its construction and encoding length are O((n+m)log(n+m)) for ordinary binary-indexed DIMACS. Each deletion is an explicit paid record in the policy, followed by one proposed RUP addition of the empty clause, with logical record vector (#deletions,#additions)=(n,1). This is not a native R_mix341 calculus or a model of all CDCL.

**Question CHECKPOINT-RUP-EXISTS:** given H, does there exist a legal choice of n deletions (one from each pair) after which empty clause is RUP under D_s? Original-source authenticity is preserved by storing the initial DIMACS bytes and the exact clause identities.

## Theorem 528.1 (PROVED/RESTRICTED): exact correspondence

For every original strict proper signed 3-CNF H and every Boolean assignment s,

$$
\operatorname{UPconflict}(D_s)=1
\quad\Longleftrightarrow\quad
s\models H.
$$

**Proof.** The only positive way to derive Z_j under the selected units is by a retained trigger for a literal satisfied by s. Hence standard Horn forward chaining derives Z_j exactly when clause C_j is satisfied. The chain derives W_m exactly when all Z_1,...,Z_m are derived. The negative unit NOT W_m then yields a unit-propagation conflict precisely if every C_j is satisfied. If some C_j is false, assign the selected T/F triggers true, all nonselected triggers false, each Z_j true iff C_j is satisfied, and W_j true iff the first j Z flags are true. This is a satisfying extension of D_s, so sound UP cannot derive contradiction. This also covers m=1 by the direct negative unit. No semantic SAT or equivalence oracle enters the concrete UP implementation.

**Corollary 528.2 (KNOWN-COMPLEXITY, derived reduction):** CHECKPOINT-RUP-EXISTS is NP-complete under polynomial many-one reductions. Membership follows by guessing n selector bits and replaying Horn UP in polynomial time. Hardness follows from the polynomial construction H -> B_H and Theorem 528.1, since proper 3-SAT is NP-complete. This is not an unconditional superpolynomial runtime lower bound; NP-completeness does not establish P!=NP.

## Theorem 528.3 (PROVED/RESTRICTED): exact small symbolic guard and spurious MAY join

The post-deletion database set has 2^n members but is represented by n independent pair-choice bits and a fixed clause database. The exact symbolic legality guard for a one-record terminal empty RUP addition is simply

$$
g_H(s) = \bigwedge_{j=1}^{m}\bigvee_{\ell\in C_j}\operatorname{value}_s(\ell).
$$

This has O(m) logical gates for proper 3-CNF (plus indices). A complete symbolic abstraction can therefore encode *all* endpoint eligibility without explicitly enumerating 2^n databases. Deciding whether the guard is satisfiable remains NP-complete.

For the coarse MUST/MAY interval, all fixed Horn clauses are mandatory and each pair of units is possible. The MAY database U contains both units of every pair and has an immediate UP contradiction, so mayRUP(empty) is true even when H is UNSAT and no actual checkpoint D_s permits that step. A concrete replay rejects the abstract path. Refinement by the exact selector guard removes every such spurious path while retaining all real paths. Each concrete n-deletion, one-RUP sequence maps to an abstract sequence costing at most n+1, so the sound MAY direction is preserved at that declared logical-record level.

**Critical early shortcut:** The *initial* database with all 2n selector units already makes every Z_j true, hence RUP(empty) immediately, regardless of H. Therefore the unrestricted DRAT-minus proof-log minimum of this UNSAT source is at most ONE addition record, before any deletions. The parameterized theorem is about an explicitly **policy-restricted checkpoint**, not the unrestricted full-log refutation optimum. The source is always UNSAT; its post-deletion databases may become SAT. Excluding the early shortcut from an all-path lower-bound abstraction would be unsound. This control is essential.

## Independent finite replay and scope

Two independently implemented, standard-library source-authenticated verifiers ran on original DIMACS bytes with explicit malformed controls and scalar UP loops:

| Measured property | Python | Independent Node.js |
| --- | ---: | ---: |
| Distinct original 3-CNF cases | 28 | 29 |
| Exhaustive post-deletion Horn databases | 920 | 1,440 |
| Original satisfiable cases | 26 | 27 |
| Original unsatisfiable cases | 2 | 2 |
| Spurious coarse MAY-join cases | 2 | 2 |
| Assertion groups | 1,991 | 1,595 |
| Instrumented UP clause scans | 149,684 | 203,708 |
| Instrumented UP propagated units | 15,996 | 25,583 |
| Rejected malformed source/parameter cases | 11 | 10 |

Sources include the canonical eight signed proper three-variable clauses (UNSAT) and even/odd K4 signed proper 3-CNF Tseitin controls (16 clauses, 6 variables, 8 or 0 satisfying edge assignments), plus separately seeded proper-3CNF samples. The first four common original DIMACS SHA256 fingerprints agreed across the two locally executed programs; SHA values appear in the raw ledger. The *published* independent JS was fetched at Git blob SHA 1456696bbe27e529ae750a3d11a71481d0a0ba0b and independently replayed in a V8 harness with crypto hash calls substituted; its **1,566 semantic assertions, 1,440 selector databases and 203,708 UP scans** passed. Real Node crypto SHA matching is supported by the separately executed local JavaScript, not the substituted replay.

Finite K4 is not an expander-size hardness certificate. Established expander-Tseitin ordinary Resolution lower bounds remain only **restricted-model control evidence**; native GF(2) elimination is a legal computational shortcut. The original rPar hardness/DRAT-minus separation of [P2-L2-526] also remains a control rather than a new algorithmic lower bound.

## Resource accounting and Route A transfer firewall

The original-to-Horn template uses O(n+m) clauses, source parse O((n+m)log(n+m)) bit data and at most 2n+2m-1 variables. For each fixed selector s, the concrete Horn-UP check is polynomial, using O(n+m) explicit clause and assignment workspace (times index bit widths). The exhaustive *test runner* checks 2^n checkpoint databases and pays its actual clause scans above. The exact symbolic guard is small, but finding a satisfying selector is exactly the original SAT task: an algorithmic cost bound for it is **not** supplied. Output bytes, parsing, source authentication, learned clause generation, indices, caches and all simultaneous state would need physical charging in any claimed SAT decider or FLMV transformation.

Unlike a sound negative proof for a full calculus, this construction identifies an NP-complete abstract-path feasibility subproblem and an immediate unrestricted shortcut. It proves no budgeted nonreachability for native R_mix341 or unrestricted DRAT, and no time-space contraction on the matched FLMV machine. The universal solver-dependent transformation for every total correct polynomial SAT decider, unknown time/space exponents, malformed/SAT/UNSAT all-input behavior, recursive iteration, and

$$
t'\leq\max(11/10,3/5+t/2),\qquad
s'\leq\max(1/2,s/2)
$$

remain **OPEN**. In particular s'<=max(rho,eta,lambda,lambda*s) is not established by guest time alone, and no model conversion is assumed. Historical grammar, weights, five task identities, enabled states, schedules and 2 Route A / 3 Route B allocation are unchanged.

## Artifacts, citations, remaining action

**Code:** experiments/arc/lspv2_528_horn_selector_independent.mjs. **Raw summary:** results/raw/arc/2026-11-09_1413_LSPV2_528_HORN_SELECTOR_RAW.json. **Handoff:** research/coordination/2026-11-09_1413_LSPV2_HORN_SELECTOR_FIVE_ROLE_HANDOFF528.md. Complete local independent Python/Node scripts and full raw case tables are bundled in the accompanying reproducibility ZIP.

[1] D'Silva V, Haller L, Kroening D. Abstract Conflict Driven Learning. POPL 2013. https://www.kroening.com/papers/popl2013.pdf

[2] D'Silva V, Haller L, Kroening D. Abstract Satisfaction. POPL 2014. https://www.kroening.com/papers/popl2014.pdf

[3] Giacobazzi R, Ranzato F, Scozzari F. Making Abstract Interpretations Complete. JACM 2000. https://www.math.unipd.it/~ranzato/papers/jacm00.pdf

[4] Clarke E et al. Counterexample-Guided Abstraction Refinement. JACM 2003. https://www.cs.cmu.edu/~emc/papers/Papers%20In%20Refereed%20Journals/Counterexample-guided%20abstraction%20refinement.pdf

[5] marijnheule/drat-trim. README.md, blob eb6ffcc4. https://github.com/marijnheule/drat-trim

[6] Chew L et al. Hardness of Random Reordered Encodings of Parity for Resolution and CDCL. AAAI 2024. https://arxiv.org/abs/2402.00542

**Actual advance:** Exact reduction theorem and NP-complete reachability classification for an inexpensive per-state Horn/RUP transition, plus compact exact-guard and early-shortcut controls. **Remaining implication:** To use abstract interpretation for universal Route A, prove source-authenticated overapproximation and fully charged same-machine transfer for *every* total SAT decider; no such transfer follows here. **P versus NP OPEN.**
