# LSPV-4/443 five-role handoff | 2026-11-06 09:10 PST

**Two Route A (LSPV-2, LSPV-4) and three Route B (LSPV-1, LSPV-3, LSPV-5) unchanged. No tasks, schedules, native proof weights or ownership changed. P versus NP OPEN.**

## Restricted theorem and exact firewall

**PROVED/RESTRICTED and CONDITIONAL (ETH), essential density quantifier:** For any *fixed* density c, an unconditional decider-independent polynomial-time controller with polynomially many actual ordinary SAT queries of length N^{lambda_c}, lambda_c<1, gives 2^{o(n)} time for that density slice. This **alone does not contradict ETH**, since some low-density slices are easy. If such controllers exist **for every fixed c** (or one true all-input controller covers all densities), IPZ sparsification plus linear proper-3CNF padding gives, for every epsilon>0, a 2^{epsilon n} algorithm on general 3-SAT; then ETH is false. The all-density quantifier is mandatory.

**NOT a refutation of Route A.** Route A asks for a compiler under the counterfactual existence of a total correct polynomial-time SAT decider A and may transform its code. ETH rules out existence of such A, so its lower-bound premise cannot contradict that conditional implication. Descriptor bits for a parent-sized lazy SAT guest are not actual short ordinary SAT input bits. Polynomial preparatory cost, malformed handling, branch combination and all machine state must be fully charged.

**LSPV-2:** Check every contraction candidate for unconditional vs A-dependent generation, genuinely short explicit guest inputs versus virtual ports, the executed guest count and query size, original-source authentication, all-input SAT/UNSAT and malformed correctness, recursion and native machine accounting. Historical LSPV-2/DELAYOR1 and LSPV-4/441 already constrain padded-guest coefficients; do not duplicate them.

**LSPV-1, LSPV-3, LSPV-5:** This ETH consequence supplies no superpolynomial lower bound for the fixed R_mix341 shared-DAG calculus or noncircular B3. Continue context-labelled AND obligations, legal shared subproofs, native rule authentication, historical weights, and GF(2)/ER/Resolution shortcuts independently.

## Verification and sources

76 original explicit finite 3-CNFs (Tseitin K4 and cube odd/even, and random proper controls); 39 SAT, 37 UNSAT; 608 fully evaluated leaves; seven malformed controls rejected; one premature one-branch UNSAT decision falsified. Independent Node referee: 16,581 PASS assertions. Separate self-contained K4/cube checker: 8,365 PASS assertions. These tests do not build a small-query controller and do not exercise a native FLMV machine.

Read governing handoff 4e29ed76, current issue #3, AGENTS.md, CODEX.md, project skill, LSPV-2/446 (6176af08), LSPV-4/442 (2c49fef5), LSPV-2/DELAYOR1 (1c53f86b), MAIN84 (88005bc1), Grok GROKPROOF/2026-11-06_0515_PROGRESS.md (93f9202d), Claude TPORT-0002 (1f9fc727), konard/p-vs-np proof_status.json (93b77ed3), blkph0x/p-vs-np-proof-research CERTIFIED_RESIDUAL_QUOTIENT_REPORT.md (b37da20a), CNFgen Tseitin (4bb5fd19), FRAT-XOR README (38a137bc), openai/math README (cc5b0a03), IPZ JCSS 2001 and FLMV JACM 2005 original papers. No independent external source builds. Original root main.tex blob f41d1cd2 yielded zero readable bytes; root left untouched. No full checkout preflight or native FLMV execution.

**Next exact OPEN obligation:** for EVERY total correct uniform polynomial SAT decider A, create an effective recursively iterable all-input same-machine compiler with t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2), with fully paid creation, indices, policy failures, output, guest calls, joins, storage and replay. Route B full mixed lower bound/B3 separately OPEN. P versus NP OPEN.
