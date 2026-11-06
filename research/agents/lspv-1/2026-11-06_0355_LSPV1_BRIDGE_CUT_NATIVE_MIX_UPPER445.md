# LSPV-1/445: bridge-cut original-coordinate proof reduces mixed logical work by two nodes

**2026-11-06 03:55 PST | Route B | PROVED/RESTRICTED mathematical theorem; COMPUTATIONAL original-source trace.** R_mix341 grammar and weights unchanged. B1/B2/B3, all-rule superpolynomial lower bounds, and P versus NP remain OPEN.

## IDEA -> SEARCH -> ITERATE and falsifiers

**Hypothesis:** A bridge in a connected simple cubic odd-charge Tseitin instance permits a shorter historical mixed refutation than the known 4h-1-node whole-source AND3/GF(2) proof, by using the two connected bridge sides to force opposite values of the bridge edge. Falsifiers: (1) GF(2) cancellation on one side leaves >2 original coordinates; (2) two endpoint original clauses together with the row fail to force the bridge bit; (3) AND3/LOCAL uses a fresh coordinate or support >3; (4) a valid full proof needs more than 4h-3 paid distinct nodes or leaks an assumption. The construction and independent finite replay refute these falsifiers within the historical /341 rule text. No completeness or all-machine conclusion is asserted.

**Prior work not claimed new:** LSPV-3/125,/134 proved exact individual clause criticality; LSPV-3/429 proved the unique essential UNSAT core; LSPV-2/341 proved the bridgeless 4h-1 optimum and all-source 4h-1 upper proof. LSPV-1/444 and LSPV-5/REFEREE383 provide strong additional transformation/shortcut controls.

## Exact 3-CNF, source and system

Let G=(V,E) be a finite connected simple cubic graph, h=|V|, n=3h/2, with at least one bridge. Let χ:V→F_2 have odd sum. Each edge e gives an original variable x_e. At each vertex v place the four **proper signed width-three** clauses falsified precisely by the four incident-edge assignments whose XOR differs from χ_v. Thus the source has exactly 4h clauses, 3h/2 variables and Θ(h log(h+2)) indexed bits. Summing vertex equations shows UNSAT. On suitable cubic expander sequences the Urquhart (1987) and Ben-Sasson/Wigderson (2001) lower bounds yield 2^{Ω(h)} **ordinary unrestricted shared-DAG Resolution** size, but do not carry over to the larger mixed calculus. Bridges are a focused easy/shortcut control, not a proposed hard family.

Historical R_mix341 from `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb, has free original source axioms, unit-paid binary RES, AND3 binary conjunction on at most three **original-variable** coordinates with truth-table verified affine annotation, unit-paid typed GF(2) row XOR, paid LOCAL-CONVERT from already derived local factor under exact constant-support implication, and paid conservative DEF. All paid nodes have at most two parents. The construction below uses no DEF, no weakening and no split/discharge.

## Theorem: explicit bridge upper bound

For every such graph and odd charge vector,

$$
W_{R_{\mathrm{mix341}}}(F_{G,\chi})\le 4h-3.
$$

If deleting bridge e=uv produces sides A and B of sizes k_A and k_B, a balanced certificate has unbounded-parallel unit-weight span at most 5+ceil(log2(max(k_A,k_B)-1)).

**Proof.** On side A with endpoint u and other incident original edges a,b, take all four original clauses at each vertex w∈A\{u}. Conjoin each vertex quartet into its exact local parity row with 3 paid AND3 inferences, 3(k_A-1) total. Sum the k_A-1 rows in k_A-2 paid XOR nodes. All internal edge coordinates cancel, leaving

$$
x_a\oplus x_b=\chi(A)\oplus\chi_u=:t_A.
$$

Of the four **original** signed clauses at u choose the two forbidding patterns with x_e=1⊕χ(A) and x_a⊕x_b=t_A. Conjoin the two clauses (one AND3), then conjoin the resulting three-original-coordinate factor with the derived affine row (one AND3). The resulting local 8-row factor entails x_e=χ(A), as verified by a paid LOCAL-CONVERT, not by a free oracle. All factors involve only the original coordinates (e,a,b). The side costs 3(k_A-1)+(k_A-2)+3=4k_A-2. The other side derives x_e=χ(B) at cost 4k_B-2. Odd total charge makes the two units complementary; one oriented RES yields false. Summing costs gives 4h-3. The root's dependency graph is acyclic, contains genuine signed source clause IDs, counts each shared node once, and does not use branch assumptions. A balanced local AND3 quartet tree has depth 2, XOR aggregate depth ceil(log2(k-1)), and final AND3/LOCAL/RES adds three levels. QED.

This is a **legal rule-level exhibited upper proof**, not a global optimum, nor a byte-level execution of an authoritative historical proof checker.

## Explicit control and work/span

Take two K4 copies, subdivide one original edge of each, and join the subdivision vertices with one bridge. Then h=10, n=15, m=40; source χ_0=1 and all other charges zero. Canonical 440-byte DIMACS SHA-256: `4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18`. Previously proved criticality and unique-core lemmas give 36 essential source clauses, a 35-node lower floor by binary-premise ancestry. The displayed new proof uses **only those 36 source clauses** and has 28 AND3, 6 XOR, 2 LOCAL, 1 RES, **37 distinct paid nodes**, ideal span 7. Hence **35 ≤ W_R(F) ≤ 37**; exact optimum remains OPEN. The known all-source upper is 39. Neither 35 nor 37 is a lower bound on unrestricted SAT algorithms.

Python produced the complete 37-node typed original-source trace and checked 2^15=32,768 assignments plus 36 separate deletion SAT controls. An independently written Node verifier regenerated signed source clauses and SHA, checked DAG ordering, AND3 full truth tables and original-coordinate scope, XOR rows, LOCAL implication, correctly oriented RES and source ancestry; **1,163 assertions including five rejected forged certificates**. Executed host producer 1.72 s / 96,656 KiB max RSS; independent verifier 0.06 s / 32,628 KiB max RSS. A complete ZIP provided to the user contains `bridge37.py`, `verify.js`, full `trace.json`, `input.cnf`, logs, raw summary, hash manifest, and this report. The GitHub compact script covers a subset of checks; it is NOT the full independent typed replay.

**Resource distinction:** Ideal W minimizes after free optimal selection. Actual construction and verification charge original source/index reads, parse/hash, graph traversal, selection, all intermediate row bit masks, node IDs and references, storage/retrieval, output bytes, failed controls, recomputation and simultaneous peak working space. A materialized polynomial graph-to-proof producer fits polynomial bit bounds; the intentionally exhaustive finite test harness is not part of proof-search upper bounds. No same-machine FLMV contraction follows; its all-phase condition s'≤max(ρ,η,λ,λs) remains unchanged.

## Evidence and reconciliation

Read historical five-role handoff pinned 4e29ed7, current issue #3, /341, LSPV-1/442,/444, LSPV-3/429,/445, LSPV-5/REFEREE383, actual Grok `GROKPROOF/2026-11-06_0920_PROGRESS.md` (SHA 6b32bc30…), Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (SHA 9a5b05d6…), and AGENTS/CODEX/project research skill. Required external check: `konard/p-vs-np/scripts/proof_status.json` SHA 93b77ed3 and `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` SHA 18d693ea, plus `meelgroup/frat-xor/format.md`, `tanyongkiam/cake_lpr/README.md` and `peitl/short-proof/README.md`. Other proof formats do not establish accepted historical R_mix341 byte grammar. Indexed literature web search covered Urquhart 1987, Ben-Sasson/Wigderson 2001, Haken 1985, Cook 1976, Cook–Reckhow 1979 and graph minimality; Google-branded search was not independently available. Similar clause criticality and unique core had **already** been proved in the project and were reused, not rediscovered. Root main.tex returned a current blob SHA but zero readable bytes and is not safe to edit.

**Remaining OPEN:** determine exact 35–37 minimum if valuable; obtain an authenticated historical /341 certificate byte grammar for LOCAL/DEF, show genuinely superpolynomial full mixed Wbar across **all** legal rules on a certified hard family and prove the noncircular same-calculus B3 `SAT in P => Wbar_R polynomial`. B1, B2, B3, and **P versus NP remain OPEN**.

### Primary sources

1. Urquhart, A., *Hard examples for resolution*, JACM 34 (1987), 209–219, DOI 10.1145/7531.8928.
2. Ben-Sasson, E., Wigderson, A., *Short proofs are narrow: Resolution made simple*, JACM 48 (2001), 149–169, DOI 10.1145/375827.375835.
3. Haken, A., *The intractability of resolution*, Theoretical Computer Science 39 (1985), 297–308.
4. Cook, S. A., *A short proof of the pigeon hole principle using extended resolution*, SIGACT News 8(4) (1976).
5. Cook, S. A., Reckhow, R. A., *The relative efficiency of propositional proof systems*, JSL 44 (1979), 36–50.
