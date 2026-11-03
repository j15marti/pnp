# LSPV-3 ADAPTIVE-RESIDUAL-WIDTH364: fixed-mixed proof-cost envelope

**November 3, 2026, 06:24 PST | PNP Hypergraph & Proof Certificates | P versus NP OPEN.**

## Substantive theorem and exact quantifiers

Keep the **unchanged** sound, complete, effective, charged at-most-binary-premise `Rmix341` including RES, AND3, GF(2), LOCAL-CONVERT, and paid conservative source-independent two-input VARDEF. Each distinct derived node has unit logical cost; authenticated source clauses are free. For **every** UNSAT CNF F and **every** complete adaptive variable decision tree T having UNSAT leaf residuals with Resolution refutations of q_alpha nodes, the fixed combined system satisfies

$$
W_R(F) \le |I(T)|+\sum_{\alpha\in L(T)}q_\alpha.
$$

Original-source *strict signed Resolution* lifts a leaf derivation of contradiction to a clause contained in its branch-blocker without weakening or new gate definitions. Branches combine using at most one ordinary signed pivot each. Choosing independent Davis–Putnam elimination orders at the leaves gives

$$
W_R(F) \le |I(T)|+\sum_{\alpha\in L(T)}\sum_i3^{w_i(\alpha)}.
$$

Therefore any size-N UNSAT CNF having b selector variables such that **all** 2^b residuals have primal treewidth at most w obeys

$$
W_R(F) \le 2^b N3^w+2^b-1.
$$

An UNSAT candidate with b+w=O(log N) cannot give superpolynomial minimum derivation cost, even with high original treewidth. This is an upper-bound condition, not a characterization of hardness. Selectors and elimination orders may be chosen after the fact for free in proof minimization; acquiring them is not a free SAT algorithm.

## Growing exact family

For all n>=2,b>=0, independently choose a Hamiltonian variable path P_alpha for each alpha in {0,1}^b; form guarded contradictory Horn paths H_{n,b}. Every one of m=2^b(n+1) source clauses is indispensable and occurrence-sign-sensitive. A true source-by-source isolated-violation witness gives the global **full mixed** lower bound m-1 for all legal shared DAGs. Exact signed RES certificates with n steps per leaf and 2^b-1 branch merges match it:

$$
W_{Rmix341}(H_{n,b})=2^b(n+1)-1.
$$

Thus heterogeneity among guarded leaves does not inherently amplify minimum proof-cost excess beyond the source-count floor. Explicit source encoding has at least m clauses, so this is not superpolynomial in input bits.

## Controls and independent verification

Python producer seed **202611030624**, finite pairs (n,b)=(3,0),(4,1),(5,2),(6,3),(8,2),(8,3). Independent local Node verifier: **2,361 checks** PASS, 196 strict RES pivots, 202 clause-deletion SAT witnesses, 864 single-occurrence sign repairs, 3,752 exhaustively enumerated assignments (zero original SAT models), 30 malformed-DIMACS and 12 corrupted-certificate rejections, and even/odd K4 parity controls (8/0 models). Original input bits: 264,768,2232,6264,3680,9280; exact logical optima: 3,9,23,55,35,71. Full proof DAG JSON SHA-256: `e71f48f4e5a96a6e5a249725cb454976ee5689eb6c389cac6a8d58536973e93d`. Published independent Node checker is a separate compact implementation and its assertion count can differ from the local full replay.

## Falsifiers

F1 (free weakening needed for branch lift) FALSIFIED. F2 (small residual treewidth plus small selector set can be superpolynomially proof-hard) FALSIFIED in this model. F3 (heterogeneous Horn leaves have necessary superlinear minimum excess) FALSIFIED. F4 (source-arity proof survives adding a **free** high-fan-in semantic macro) FALSE; that would alter R.

## Corpus, literature, duplication and limitations

Read user-approved 2026-11-02 12:04 refocus, issue #3, AGENTS.md, CODEX.md, repo pnp-research skill, original LSPV-2 MIXED341, LSPV-3 STRICT3-UP-BACKDOOR354, DP-WIDTH-UPPER361, ORTHOGONAL-SNAKE362, LINEAR-TREEWIDTH363, peer LSPV-4 AFFINE-COORDINATE-REPLAY360 and LSPV-5 same-support compiler handoff. Web primary research queries: `DPLL resolution lifting`, `SAT backdoors depth beats size`, `Davis Putnam induced width`, `strong backdoors bounded treewidth`, `extended resolution 2026`, and `github.com/openai theorem proving`. Relevant prior literature: Beame/Kautz/Sabharwal (IJCAI 2003); Fomin et al. (SODA 2015); Dreier/Ordyniak/Szeider (JCSS 2024). Prior project 354 and 361 contain constituent bounds; the precise zero-weakening adaptive synthesis and heterogeneous mixed exact calibration are the **narrow project contribution**. No novelty is claimed for classical DPLL or backdoor theory. A 2026 lower bound for algebraic polynomial calculus with extension measures bit size in a different calculus, and is not transferred.

Logical node minima are distinct from proof discovery, proof bits, checking, parsing, source/index/head reads, memory and same-machine runtime. No numerical FLMV claim is made; retain all-phase peak bound s'<=max{rho,eta,lambda,lambda*s}. B1, B2, B3 and the superpolynomial full-mixed Wbar bound remain OPEN. This is a family/structural-hardness-indicator failure, **not** a worst-case transfer counterexample.

## Exact outbox and next gap

- Formal role report: `research/agents/lspv-3/2026-11-03_0624_LSPV-3_ADAPTIVE_RESIDUAL_WIDTH364.tex`
- Authenticated certificate producer: `experiments/arc/lspv3_364_adaptive_backdoor.py`
- Independent Node verifier: `experiments/arc/lspv3_364_independent_verify.js`
- Raw verified results: `results/raw/arc/2026-11-03_0624_LSPV3_ADAPTIVE_RESIDUAL_WIDTH364_summary.json`

The full local archive includes both executable implementations, every signed proof DAG and raw controls. **Next:** exhibit a growing nonaffine UNSAT family whose optimal mixed proof cost remains high even though every adaptive branch decomposition and local/residual algebraic shortcut has been considered, and separately prove B3 for exactly the same preselected R. No task IDs, titles, schedules, enabled states or ownership change. P versus NP remains OPEN.
