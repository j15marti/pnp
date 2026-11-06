# LSPV-1/439 | Paid edge-gate clausal port for published odd-Tseitin 3-CNF

**November 6, 2026, 00:44 PST | Route B lead.** **PROVED/RESTRICTED** strict Resolution with explicitly owned conservative gate facets; **COMPUTATIONAL** source and adversarial replay; **CONDITIONAL** historical mixed-gate acceptance; full mixed lower bound, B1/B2/B3 and P versus NP **OPEN**.

## IDEA → SEARCH → ITERATE and falsifiers

Starting from LSPV-1/438's edge-shared semantic identity, test whether *real original source clauses* plus paid conservative DEF owners admit short correctly oriented binary Resolution derivations of the entire proposed guarded GF(2) row's clausal cover. Falsifiers: (F1) missing canonical blockers; (F2) uncovered violating charge-one assignment at g=1; (F3) invalid pivot, unowned facet, duplicated shared proof, or assumption leakage; (F4) no historically native facet/row-export grammar. F1–F3 are discharged only in the **declared source-plus-facet system**. **F4 remains OPEN.** A first attempt eliminating x but not guard g did *not* yield the unguarded charge-zero blockers; the repaired construction pays one more Resolution pivot on g.

## Exact established-family ledger

Let G_h be a connected simple bridgeless cubic graph with h even vertices and |E|=3h/2 edges, and odd total vertex charges χ_v. One Boolean x_e per edge. For each cubic vertex of charge χ_v, add exactly the four signed proper-width-three clauses falsified by the four local bit triples b with b_1⊕b_2⊕b_3≠χ_v. Thus F_h has 4h exact 3-clauses, 3h/2 variables and Θ(h log(h+2)) binary-indexed source bits. XORing vertex equations proves UNSAT. For suitable expanding cubic sequences, the published Urquhart (1987) and Ben-Sasson–Wigderson (2001) theorems yield 2^{Ω(h)} **ordinary unrestricted shared-DAG Resolution** size; they do not imply full-mixed or unrestricted algorithmic hardness. The previously proved LSPV-1/435–/436 signed substitution and Boolean restriction *preserve that lower bound* under the following original-source proper-three guard/split construction, rather than relying on equisatisfiability.

For every C_i=(a_i∨b_i∨c_i) use (g∨a_i∨y_i) and (¬y_i∨b_i∨c_i). Add four proper-three clauses (¬g∨p^s∨q^t), s,t∈{0,1}. The result K(F_h) has 8h+4 source clauses and 11h/2+3 variables. Earlier /436 proved clause indispensability and a linear source-arity work floor 8h+3 for binary-premise unit-paid sound systems. Its conditional mixed upper control 12h+2, and /341's 4h-1 unguarded semantic mixed proof, remain **legal shortcuts**. Cook ER, Haken Resolution PHP, and Braun Res(⊕) bit-PHP are independent controls with different systems and encodings.

## Theorem 439.1: Explicit source-authenticated local port

Fix a cubic vertex of charge c∈{0,1} and an ordering x_1,x_2,x_3. For every wrong triple b let a_{b,j}=x_j if b_j=0, otherwise ¬x_j. The **eight actual original** clauses at this vertex are

$$
(g\vee a_{b,1}\vee y_b),\qquad(\neg y_b\vee a_{b,2}\vee a_{b,3}).
$$

Use one paid **globally edge-shared** conservative owner w_j=(¬g)∧x_j for each of the three incident edges. The exact owner facets are

$$
(\neg w_j\vee\neg g),\quad(\neg w_j\vee x_j),\quad(w_j\vee g\vee\neg x_j).
$$

These nine facets **are not free original-source axioms**. Referencing them is legal only in an explicitly specified, paid, owner-qualified facet completion of the calculus. Historical R_mix341 has not yet been shown to permit this syntax.

For each forbidden b, resolve its two original clauses on y_b, then eliminate the three signed x_j literals by three correctly oriented binary RES steps. For a positive x_j use (w_j∨g∨¬x_j); for negative ¬x_j use (¬w_j∨x_j) with the owner facet as positive premise. Exactly four paid nodes yield

$$
B_b=g\vee\bigvee_{j=1}^3w_j^{1-b_j}.
$$

**Charge zero:** all four wrong triples have odd weight, hence some b_j=1 and ¬w_j already occurs in B_b. Resolve on g with the facet (¬g∨¬w_j), obtaining the exact canonical width-three blocker C_b(w). Four additional steps yield all canonical clauses of w_1⊕w_2⊕w_3=0. **Twenty distinct paid RES nodes** suffice; the dependency span is at most five RES layers after source/facet availability.

**Charge one:** all four wrong triples have even weight. The four B_b are the exact blockers of w_1⊕w_2⊕w_3⊕g=1 on g=0, costing **sixteen distinct paid RES nodes**. On g=1 all four violating assignments have odd w parity, so at least one w_j=1; the existing owner facet ¬g∨¬w_j is a *subsuming clause* that blocks that assignment. Thus the sixteen nodes plus owned facets cover every falsifying assignment of the four-variable affine row. We **do not claim** derivation of the four missing canonical g=1 clauses without weakening; the subsuming cover is sufficient for semantic row entailment but is **not** automatically an accepted historical LOCAL→GF(2) rule.

Every inference is oriented, has two antecedents, preserves indexed source and owner ancestry and shares all nodes/edge definitions globally. No branch hypothesis is discharged, no source lemma leaks across branches and no paid node is counted twice. These are **witnessed upper bounds**, not exact minima.

For an odd-charge source chosen with one exceptional charge-one vertex, the exhibited local clausal RES work is 20(h−1)+16=20h−4, with 3h/2 globally shared paid DEF owners. If historical owner-qualified facets and a *paid* row exporter of cost ≤c_0 per vertex were authenticated, plus a paid row-to-unit port, standard GF(2) joins, and the guarded pad contradiction, the **conditional** full mixed work would be ≤(22.5+c_0)h at unit weights. This is larger than /436's previous conditional 12h+2 shortcut and does not improve the best upper bound. No native mixed certificate has been accepted.

## Independent verification, raw evidence and machine resource firewall

Python producer: complete explicit 17-source/facet-leaf proof DAG per charge, 20 or 16 paid RES nodes, every oriented pivot and parent ID checked, all 2^11=2048 valuations checked per charge. Independent Node verifier regenerated each original source clause and facet without importing the Python constructor; replayed each topological step, checked all eight violating assignments, and rejected six mutations (pivot, parent, acyclic order, source corruption, missing blocker, wrong cover). **6,565 independent assertions passed**. Each charge has 72 satisfying local assignments to the extended clauses; this count does not imply satisfiability of globally odd-Tseitin. Local host runs observed Python wall 1.44 seconds, 96,144 KiB max RSS, and Node wall 0.26 seconds, 33,264 KiB max RSS. Scripts and full evidence are in the companion reproducibility archive. These implementations are not the authoritative historical checker or an actual same-machine FLMV experiment.

Each local recorded inference has ≤4 literals, signed IDs, two references and a pivot, so explicit dense-index evidence is O(h log(h+2)) bits overall for h vertices and bounded local work, apart from separately charged gate owner references, caches, source provenance and exporter evidence. Actual algorithms charge input reading/indexing/head read, all gate setup, failed discovery, parsing, serialization, verification, output, retained/recomputed DAG material, peak concurrent space and machine conversions. The ideal proof minimum charges shared nodes once and intentionally omits discovery cost.

## Source and research provenance

Governing five-role handoff historical commit 4e29ed7646f484707767acb6e63ec5f38afd98a8; issue #3 current body/comments; reports /435 ffbb0928, /436 2c72bdf3, /438 b77f7f04; LSPV-3/436 4d3cfc17 (two proposed, different facet-access grammars); LSPV-3/438 63e4318d; LSPV-3/441 437bf093 (typed proposed GATE-LOCAL Cook shortcut); AGENTS.md 19656af1, CODEX.md 754999f5, research skill b8df83a7; actual GROKPROOF/2026-11-06_0515_PROGRESS.md 93f9202 and Claude ONETAPE 9a5b05d6 were examined.

Required pinned external repositories: konard/p-vs-np @ ecedd2b45f1c524d85c00b2da27a9c140025550c (README 0e0ec77f, complexity README 7ee9a11e, proof status 93b77ed3); blkph0x/p-vs-np-proof-research @ 7dedc73f758dfbdc072e7aa29dfc08505761ebd5 (METHOD_INDEX 18d693ea, proof-portfolio bridge 22215cec, REVIEW_ADDENDUM 6a7cc2f). FRAT-XOR format 986a21aa and cake_lpr README e94f45e9 are distinct checker languages, not substitutes for native Rmix acceptance. Read relevant indexed primary research including Pich/Santhanam on Extended Frege self-provability and Cook/Reckhow proof systems. Direct Google-branded search and container GitHub DNS were unavailable; connected GitHub source reads and indexed web literature search were used. No Lean or CakeML replay claimed.

**Next missing exact implication:** legally export the actual 16/20-step local clausal consequences through historical paid owner/facet/LOCAL rules into a certified GF(2) row, or produce a precise incompatibility witness under a genuinely fixed grammar. Separately establish superpolynomial Wbar_R over *all* mixed legal proofs and noncircular B3: SAT∈P ⇒ Wbar_R polynomial for the *same* fixed R. **B1/B2/B3 and P versus NP OPEN.**

### Primary references
[1] A. Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), 209–219.
[2] E. Ben-Sasson and A. Wigderson, *Short Proofs Are Narrow*, JACM 48 (2001), 149–169.
[3] S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50.
[4] J. Pich and R. Santhanam, *Towards P ≠ NP from Extended Frege Lower Bounds*, JACM 73 (2026), DOI 10.1145/3801091.