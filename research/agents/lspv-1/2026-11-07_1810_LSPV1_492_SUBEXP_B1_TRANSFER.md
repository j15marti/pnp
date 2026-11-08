# LSPV-1/492 | Subexponential SAT versus pointwise B1 certificate-translation firewall

**2026-11-07 18:10 PST | Lead, Route B | CONDITIONAL THEOREM (external newly published subexponential SAT formalizations) + PROVED/RESTRICTED proof-system application + COMPUTATIONAL finite controls | P versus NP OPEN.**

**Exact trackers:** material new evidence [P2-B3], crosscheck [P2-F9], [P1-X1] and [P1-01]. Historical native requirements [P2-D1], [P2-C3], mixed worst-case lower bound [P2-B1], and weakest noncircular B3 [P2-B2] are all OPEN. Neither this report nor newly published ETH claims provide P=NP or P!=NP.

## IDEA and 4 predeclared falsifiers

**Hypothesis:** A newly published *uniform* subexponential algorithm for #3-SAT, if its formalized claim is correct, yields a stronger, non-tailored B1 counterexample in a **separate, fixed, sound, complete, effective** algebraic proof calculus, using existing *random proper 3-CNF* hardness rather than a bespoke family. We must not infer anything directly about historical R_mix341 or B2/B3.

**Falsifiers:** (F1) the cited subexponential result is only a promised SAT-instance algorithm or assumes an uncharged oracle; (F2) the machine's input representation and general binary-parser completion introduce exponential-in-n cost; (F3) the selected proof lower bound is tree-only, wrong characteristic, probabilistic solver performance or applies only to a different encoding; (F4) the alleged contradiction silently replaces the B1 per-input time by B2 worst-case time or the fixed R by historical R_mix341.

## SEARCH, dated sources and exact existing project work

Read **both complete** root proof trackers on GitHub main, current coordination issue #3 and newest comments, governing Nov 2 five-role handoff, AGENTS.md, CODEX.md and the pnp-research skill. Read the actual current Grok file \`GROKPROOF/2026-11-08_0118_PROGRESS.md\`, Claude's \`research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex\`, LSPV-1/482 and /491, LSPV-3/486, and red-team LSPV-5/422. These are scoped background, not proof authority. Grok's report did not note the new Oct 2026 formally presented ETH algorithms.

**New primary candidate algorithm sources, pinned:**
- OpenAI, *The Exponential Time Hypothesis is False*, dated October 25, 2026; repository \`openai/math\` commit \`4eaee87548250b2682affda7d05d947c05554bae\`, \`lean/docs/378.md\` and \`lean/ComparatorChallenges/SubexponentialSAT.lean\`. The stated Lean-covered claim is a deterministic counting/SAT machine for every fixed k-CNF with **polynomial tape space** and time \`(L+1)^{O_k(1)}2^{O_k(n (log log n)^2 / sqrt(log n))}\`. The paper claims a sharper rate; this report uses **only the weaker stated Lean rate**.
- Anthropic, *A 2^{o(n)} Time Algorithm for 3-SAT*, October 27, 2026; repository \`anthropics/formal-math\` commit \`16a5ce41304fcdaea4e0be7c132e1c361dc26da5\`, \`eth/README.md\`, \`eth/MainResults.lean\`, \`eth/Solution.lean\`, \`eth/Challenge.lean\`, \`eth/comparator.json\`. MainResults formally states one finite-alphabet \`Turing.FinTM2\` machine counting k-CNF on all-occurring variables and distinct clause lists, n>=4, m>=2, within \`2^{C min(km/sqrt(log m), k^2 n log log n /sqrt(log n))}\` steps. \`Solution.lean\` claims the actual proof of this precise statement and \`ETHIsFalse\`, with standard axioms only; \`Challenge.lean\` intentionally contains two \`sorry\` placeholders and is *not* the proof.
- Both papers are **claims with substantial formal evidence, not an independently replayed/peer-reviewed theorem in this run**. The Lean toolchain was absent; \`git\` outbound DNS failed. I examined the actual source statements and proof linkage but did NOT run \`lake\`, Comparator or nanoda. Their correctness and equivalence to the intended external cost model remain prerequisites.

**Established hard proof-family source:** Shuo Pang, arXiv:2610.00837v2, October 24, 2026, exact §7.1 family definition and Theorem 7.2(a): for fixed p prime, fixed r>=1, random \`F~F(n,w,Delta*n)\` (with-replacement independent uniform width-w signed clauses, Delta>=2^w) has \`exp(Omega(n))\` **all-DAG** proof-size lower bounds for \`Res(PC_r/F_p)\` with probability tending to 1. Underlying PC-degree work Alekhnovich--Razborov (2003). The preprint is cited at its exact scope, not independently replayed.

Required research repository checks: \`konard/p-vs-np/scripts/proof_status.json\` (no unrestricted P/NP proof); \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` (bounded/local algorithms and relaxations); \`meelgroup/frat-xor/format.md\` (distinct XLRUP certificate grammar); \`openai/math/README.md\` and \`anthropics/formal-math/README.md\` (proof-scoping); \`tanyongkiam/cake_lpr/main/README.md\` was **not accessible on main**, and no paper/code claims from that path are used. This is not a comprehensive audit of the full repository corpus. Public web research used an indexed search engine and primary arXiv HTML; no Google-branded search interface or PDF analysis.

## Family / theorem / encoding / known methods / transfer ledger

**Source family:** \`F_n~F(n,3,8n)\` consists of 8n independently drawn signed three-clauses. Each clause selects 3 distinct original variables from n and independently assigns signs, uniformly among \`8*binom(n,3)\` possibilities. Repetitions between clauses are allowed. The input has m=8n clauses and binary indexed length \`N_n=O(n log(n+1))\`; the original source is itself proper width-three CNF, so **no SAT-to-3SAT hardness-preservation reduction** is invoked. The theorem is high-probability, not a deterministic certified list of benchmark instances. Hardness means minimum proof size **in the named system**, not empirical solver difficulty.

**Fixed proof system:** \`R_3=Res(PC_1/F_3)\` with Pang's syntactic axioms, linear-equation resolution rules and unrestricted DAG sharing. Choose unit positive charge per paid proof line for this *distinct* system. Pang 7.2(a) supplies, for some \`kappa>0\`, asymptotically almost surely
$$
W_{R_3}(F_n)\ge \exp(\kappa n).
$$
The source may contain duplicate clauses, matching Pang's family, and its n-variable scope is literal. This does **not** extend to GF(2)-enabled historical R_mix341; its XOR/AND3, RES, LOCAL-CONVERT, DEF, branching and port semantics are not simulated.

**Known legal upper controls:** any algorithm can exploit arbitrary branching, Gaussian elimination, shared work, learned lemmas and extensions while deciding 3SAT. The stated subexponential algorithm itself is a *candidate uniform upper bound*, not a proof in R_3. Pang's bound already minimizes over legal shared-DAG algebraic lines inside R_3; it does not prohibit alternate machine computation. No shortcut is excluded from R_3 to protect its theorem.

## ITERATE: B1 non-tailored fast-algorithm incompatibility lemma

**Lemma 492.1 (elementary conditional consequence, PROVED under hypotheses).** Suppose there exists a uniform total correct CNF-SAT decider A and an infinite sequence of UNSAT proper 3-CNFs F_n with \`|encode(F_n)|=n^{O(1)}\`, \`T_A(F_n)=2^{o(n)}\`, while the fixed proof system R has \`W_R(F_n)>=exp(kappa*n)\` for some constant \`kappa>0\`. Then B1 is false for **this A and R**:
$$
\neg\left[\exists \text{ polynomial }p_A\ \forall F\in{\rm UNSAT}:
 W_R(F)\le p_A(|F|+T_A(F))\right].
$$

*Proof.* For every fixed polynomial p, \`n^{O(1)}+2^{o(n)}=2^{o(n)}\`, so \`p(n^{O(1)}+2^{o(n)})=2^{o(n)}\`. This is eventually strictly smaller than \`exp(kappa*n)\`. Contradiction. QED.

**Instantiation to existing work:** From the **Lean-scoped OpenAI machine claim**, \`T_A(F_n) <= poly(N_n) 2^{O(n (log log n)^2/sqrt(log n))}=2^{o(n)}\`. Canonical binary parsing, sorting/deduplicating repeated clauses, and renaming variables have polynomial overhead on these 8n-clause sources. For non-3-CNF and malformed encodings, choose a deterministic total parser plus exact brute-force fallback; this makes the same fixed A a total correct **general CNF-SAT** decider, though its worst-case runtime is not subexponential. Canonicalization preserves SAT/UNSAT; for counting it restores the factor \`2^(unused variables)\`, handled explicitly in the finite control. In particular, no special recognizer of expander structure or SAT answer is used.

Pang's hard family and this general-purpose subexponential solver therefore jointly **imply B1 fails for R_3 without the earlier /482 tailored polynomial-time Tseitin recognizer**. This is a strengthened, *conditional* B1 counterexample, **not** a contradiction between algorithms and restricted proof complexity. The implication is logically sound independently of whether the two external Oct 2026 computational claims withstand full independent review.

For comparison, choosing a brute-force fallback for arbitrary non-3CNF encodings can dominate \`T_A^{wc}(N)\`. Therefore no B2 counterexample, no noncircular B3 and no mixed-calculus result follows. The B1 lower bound concerns \`W_{R_3}(F)\`, **not** \`W_{R_{mix341}}(F)\`. A proof-translation from an A rejection computation to an original-source R_3 certificate must output \`exp(Omega(n))\` charged proof nodes on these sources despite the algorithm's \`2^{o(n)}\` runtime; native output-bit costs only increase this gap.

**Quantified scope:** The random source theorem guarantees existence of suitable F_n for all sufficiently large n with probability tending to one; we do not claim a named deterministic instance was found. The all-input SAT algorithm is external and currently unindependently-replayed in this run. R_3 proof size is a distinct syntactic metric, not a time lower bound. This report supplies no all-machine SAT lower bound and makes no hypothesis that ETH is true.

## Independent finite controls and cost accounting

Published JS program \`experiments/arc/lspv1_492_subexp_b1_firewall.js\` (the *exact* repo source executed via V8 connector) passed **297** assertions across 140 small random proper-width-three samples, 6 malformed strict-3CNF controls, original SAT/UNSAT full-assignment controls, source deduplication/unused-variable normalization, and illustrative rate computations. Because an initial low-bit LCG implementation made all 140 test sources SAT by parity correlation, that flawed preliminary generator was **corrected and replaced** (current code blob \`4b671264c333fc4abc74e1396602685fc173e34b\`), then exact source readback and fresh execution passed. This is a useful falsifier of poor randomized test methods, not a mathematical result.

A separately written local Python verifier passed **298** assertions across 140 independent finite sources, 7 malformed controls, and exhaustive SAT/UNSAT/normalization controls. These tests do **not** execute the external claimed subexponential solver, Lean kernel, or proof-size bound, and no finite instance is claimed to certify exp(n) proof size.

The symbolic rate \`(log log n)^2/sqrt(log n) -> 0\` follows from ordinary calculus, not from finite checks. For fixed k and any \`d>0\`, \`poly(N_n)*2^{O(n (log log n)^2/sqrt(log n))}=o(2^{d n})\`.

Logical minimum: proof-node count and output-bit lower bound are restricted to R_3. Algorithmic total time on 3CNF: polynomial parse/canonicalization plus external claimed runtime. General-CNF fallback: potentially exponential and charged; maximum over all binary inputs therefore not bounded here. Source/index/head reads and output are included only to the extent stated in the cited machine formalization, whose proof was not locally replayed. Space: OpenAI claims polynomial visited tape space for fixed k, but it is not independently audited. This report does not claim fully charged historical R_mix341 machine time, span, peak memory or same-machine FLMV suitability.

## Manuscript, tracker and publication safeguards

Root \`main.tex\` is intentionally untouched; its complete contents/ownership markers were not safely reconciled here. No historical R_mix341 grammar/weights, agent identity, time zone, task title/schedule/enabled status, route allocation, or other role manuscript was changed. See separate complete tracker readback and issue #3 comment for any exact [P2-B3] new evidence entry.

**Next decisive step:** independent Lean kernel/Comparator + nanoda replay of the published ETH source statement at pinned commits, then mathematical referee of the statement/input encoding; concurrently LSPV-3 must authenticate original-source native mixed rules and LSPV-5 must red-team whether any transfer argument implicitly treats fast decision computations as short historical proof certificates. B2/B3 remain OPEN; P versus NP OPEN.
