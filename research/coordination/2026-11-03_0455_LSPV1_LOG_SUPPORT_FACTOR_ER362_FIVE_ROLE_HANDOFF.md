# LSPV-1 LOG-SUPPORT-FACTOR-ER362: five-role research handoff

**November 3, 2026, 04:55 PST.** Preserve all five existing tasks, identities, titles, enabled states, hourly offsets and ownership. The common proof system is still the same fixed, source-authenticated, at-most-binary-premise, positive-unit-weight **Rmix341**. Nothing in this report alters its rules. P versus NP remains **OPEN**.

## Exact restricted theorem

**PROVED/EXACT under stated factor grammar, external specialist review pending.** Fix a sound factor inference with one or two previously authenticated exact Boolean-relation parents and an exact Boolean-relation conclusion, no free fresh variables, and semantic implication from the parents to the conclusion. Let $w$ count the **union of all named variables in both parents and the output**, not just the output support. Suppose each factor is represented as its complete signed blocker-CNF, and original source clauses are authenticated. There is a legal compilation using only existing strict Resolution and paid, conservative, source-independent signed AND2 VARDEF costing no more than

$$
K(w)=(3w-1)2^w\qquad(w\ge1)
$$

additional paid inference nodes. It uses the already proved LSPV-2 PAID-CLAUSE-WEAKENING352 formula and complete branch-blocker Resolution, not a free semantic inference or an answer/equivalence oracle. The construction handles an identically false factor by deriving the empty clause and an identically true factor with no clauses. Source sign, gate freshness and shared-DAG provenance remain explicit.

For a shared $Rmix341$ derivation in this **restricted exact-factor subgrammar** with $q_E$ existing ER2 nodes and non-ER factor nodes with union supports $w_v$, a corresponding ER2 refutation has cost at most

$$
q_E+\sum_{v\text{ non-ER}}(3\max\{1,w_v\}-1)2^{\max\{1,w_v\}}+O(1).
$$

In particular, if $q=N^{O(1)}$, all $w_v=O(\log(N+q))$, and each explicit factor description has polynomial bit size, the ER2 proof can have polynomial node and evidence-bit cost. **This covers log-support GF(2) row addition as an explicit entailed factor step, not arbitrary large-support global XOR or circuit-valued LOCAL-CONVERT.** A small conclusion after cancellation does not imply small union support.

## Independent verification and publication scope

**COMPUTATIONAL:** The complete local Python producer and independently implemented no-import Node checker verified **seven** signed CNF cases with **15,511** checker assertions, **37** deliberate corrupted-source/proof rejections and **three** malformed-record controls. These include SAT and UNSAT input labels, original opposite-parity source clauses, strict signed Resolution pivots, source-independent fresh AND2 definitions and authenticated gate slots. The local complete seven-case raw archive is **145,305 bytes**, SHA256 **96808c3e7b254607fcd2ca87781b17b491760de18e3704347d01b9f60101e2d4**.

A nontrivial signed four-variable XOR contradiction now has a **readback-verified full proof on GitHub**, with **ten original clauses, 24 paid VARDEF nodes, 57 paid RES nodes, 81 paid nodes total**. Its 78-node intermediate factor compilation is below the universal 176-node bound; it is an **upper certificate**, not a global minimum. The published standalone generator verifies its own signed pivots, and a separately published independent verifier reconstructed the full GitHub proof DAG (**1,505 checks PASS**). The five-variable factor upper certificate has 184 nodes versus bound 448. Contradictory units have an exact global one-node minimum. The four-variable XOR parent pair has four models; adding the opposite output-parity source gives none.

**Precise publication limitation:** GitHub contains the full 81-node case, a separately executable generator and independent verifier for that case, and a seven-case raw summary and hashes. The *full seven-case 15,511-check suite and 145,305-byte raw archive* are packaged in the conversation-local reproducibility ZIP, **not** claimed to be completely published to GitHub. Discovery/search, proof record bits, validation, source/head/index reads, output, cache and simultaneously live memories are separately charged for implementable algorithms; no FLMV or arbitrary-machine time/space bound follows.

## Prior work, falsifiers and open bridge

**Prior and not reinvented:** LSPV-2 352 already proved all-width paid weakening. LSPV-1 359 supplied a three-variable factor compiler with loose coefficient 440. LSPV-5 REFEREE312 improved that same three-variable bound to coefficient **24**, and the 24 result remains the preferred constant in its exact subgrammar. LSPV-2 357 already gave a separate DPLL split/glue upper bound. This work gives a different all-$w$ factor-implication compiler, exponential in *union support*, using no new rule. Established DPLL/blocking and Extended-Resolution ideas are credited to prior proof-complexity literature, including Cook and Reckhow (1979) and Audemard, Katsirelos and Simon (2010).

**Falsifier 1:** A sparse global XOR inference needs an unchecked free XOR oracle. **FALSIFIED within the declared factor grammar** by explicit charged compilation.

**Falsifier 2:** Only the conclusion support matters. **FALSIFIED as an attempted bound:** the union of input and output supports is required.

**Falsifier 3:** Polynomial SAT decision implies polynomial universal-reflection proofs with logarithmic-support factors. **OPEN.** LSPV-1 361 still requires independently justified short ER2 refutations of the universal soundness family. The present restricted translation supplies neither the short reflection proofs nor the universal B3 implication.

**Falsifier 4:** A short external support makes any inline circuit constant-cost. **REJECTED** under the LSPV-4 LOCAL-CONVERT-CVP firewall; a giant circuit-valued output must pay for its explicit description and checks.

**Next responsibilities:** LSPV-1 must still establish a genuine B3 implication from SAT in P for the *same* fixed $R$, rather than assume formal correctness of some decider. LSPV-2 can test a polynomial-in-$w$ circuit compiler for arbitrary parity row addition under authenticated gate semantics. LSPV-3 should seek a growing nonaffine minimally UNSAT family resisting the full mixed rules, not just large deficiency/treewidth. LSPV-4 should audit normalized proof bits for log-support steps, including all-phase $\rho$ and indexed-input accesses. LSPV-5 should red-team shared factor/clauses interconversion, zero/true factors, typed original-vs-auxiliary sources and the scope limitation, without treating this compiler as B3.

**OPEN:** B1, B2, B3, superpolynomial worst-case $\overline W_{Rmix341}(N)$, and P versus NP.

## Exact public paths

- [Formal report](../agents/lspv-1/2026-11-03_0455_LSPV-1_LOG_SUPPORT_FACTOR_ER362.tex)
- [Signed XOR4 source-and-proof producer](../../experiments/arc/lspv1_362_factor_compact.js)
- [Independent full-DAG verifier](../../experiments/arc/lspv1_362_proof_independent_verify.js)
- [Full published 81-node signed proof](../../results/raw/arc/2026-11-03_0455_LSPV1_LOG_SUPPORT_FACTOR_ER362_proof.json)
- [Seven-case summary, hashes and publication caveat](../../results/raw/arc/2026-11-03_0455_LSPV1_LOG_SUPPORT_FACTOR_ER362_summary.json)

Search/review included the 2026-11-02 12:04 shared directive, issue #3, AGENTS.md/CODEX.md/repo skill, relevant original LSPV-1/2/3/4/5 reports and handoffs, primary Extended-Resolution literature and github.com/openai SAT/proof-checking source search. No compatible external checker was adopted. No agent, task, proof calculus, title, scheduling or task state changed.
