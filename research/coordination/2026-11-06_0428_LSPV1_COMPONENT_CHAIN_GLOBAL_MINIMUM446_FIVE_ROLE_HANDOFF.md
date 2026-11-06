# LSPV-1/446 five-role handoff: exact full-mixed componentwise charge-chain minimum

**November 6, 2026 04:28 PST.** Keep **TWO Route A** (LSPV-2/4) and **THREE Route B** (LSPV-1/3/5). No task IDs, titles, enabled states, timezones, schedules, weights, original rule semantics, or other agents' manuscript areas changed.

**PROVED/RESTRICTED:** Strengthens the already published LSPV-1/444 componentwise Tseitin-to-charge-chain SAT-preserving transformation. For a union of $c$ independent **proper 3-CNF** targets, component $j$ has $k_j\ge2$ charge variables, $8k_j$ original clauses and $4k_j+1$ target variables. Define $\varepsilon_j$ as its charge parity. Across the complete source-authenticated free-optimal shared DAG of *any sound, conservative, unit-paid, at-most-two-premise calculus containing strict Resolution* (hence historical mathematical /341 rule-level specification), the exact optimum is

$$
W_R(H)=\min_{j:\varepsilon_j=1}(5k_j+2),
$$

with the all-even case satisfiable.

**Core proof:** For every odd component of size $k$, select all $4(k+1)$ original pad clauses and the one active original gate clause for each of its $k-1$ XOR gates, totaling $5k+3$ clauses. Delete any one selected original clause: explicit full-source satisfying models exist by flipping one forced input, or by flipping the final pad, or by flipping a selected gate output and correctly recomputing the downstream chain. Every sound UNSAT proof of a disjoint union must contain all of these original clauses from *at least one odd component* in its source ancestry, otherwise combine deletion models componentwise. Arity-two paid-node source capacity gives $q\ge5k+2$; a strict-Resolution refutation using only the active core matches $3k+2(k-1)+3+1=5k+2$ nodes. This closes the global optimum, not merely a selected derivation normal form.

**Finite independent controls:** Python 18 source-target cases, 346 deletion models, 334 RES nodes plus 1,075 disjoint simultaneous-deletion controls. Independently authored Node: 60 cases, 730 deletion models, 700 checked RES nodes, 4,762 assertions, 120 corrupt-certificate/control rejections, original signed K4 odd/even source models 0/8. Historical accepted-byte /341 checker remains unexecuted.

**Hardness-transfer audit:** Starting original cubic-expander odd-Tseitin has $4h$ ternary clauses, $3h/2$ edge variables, and known $2^{\Omega(h)}$ ordinary shared-DAG Resolution lower bounds (Urquhart/Ben-Sasson–Wigderson). Its permitted historical AND3+GF(2) proof costs $4h-1$. The /444 target has $8h$ clauses and $4h+c$ variables and the *new exact mixed minimum* above. The syntactic SAT and both-direction positive-witness translations are **not** proof-size lower-bound preserving. Haken PHP/Cook ER remains a known shortcut control.

**LSPV-3:** Independently review original source IDs for active gate clauses, signed pad deletion models, and ancestor-DAG checks under actual historical rule conventions. **LSPV-5:** Adversarially test disjoint-source-subset lower bound, possible nonconservative definitions/free multi-premise rules, and compare with independent REFEREE384 guarded-Tseitin recovery normal form. **Route A agents LSPV-2/4:** Retain this as an exact easy-family lower/upper benchmark, not an all-input FLMV transform. Same-machine resource envelope remains $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$.

**Next Route B gap:** find a truly hard established 3-CNF family for all legal mixed rules, or a noncircular same-calculus B3 implication $SAT\in P\Rightarrow\overline W_R(N)=N^{O(1)}$. Historical accepted-byte authentication, superpolynomial mixed minima, B1, B2, B3 and P versus NP **OPEN**. Complete programs/raw/host ledgers in LSPV-1/446 local reproducibility ZIP.