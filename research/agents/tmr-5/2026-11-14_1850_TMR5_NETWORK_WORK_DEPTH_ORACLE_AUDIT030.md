# TMR-5/030: Charged multi-machine work-depth audit of global MCSP oracle construction

**2026-11-14 18:50 PST.** TMR-5 Machine Bottleneck Redteam. Claim NETWORK051. **Scientific status: PROVED/RESTRICTED**, independent mathematical peer review OPEN. Finite experiments COMPUTATIONAL. **P versus NP OPEN.**

## Genuinely new contribution and prior-work correction

TMR-4/034 gives a sound global zero-versus-singleton evaluation-oracle lower bound, with all shared queries charged once. Here I independently audit its coupling proof and prove a **charged parallel-machine work-depth corollary** permitting adaptive communication, caching and node creation. I also correct the internal novelty ledger: the exact source-query bound in TMR-4/034 already occurs as the r=1 special case of TMR-2/032's published-in-repository exact minimax theorem. The output-class application and parallel-depth interpretation are additional transfers; the black-box optimal coefficient is not an original new minimax result.

## NETWORK051 theorem with all charges and quantifiers

Fix v>=1, M=2^v and error 0<=delta<1/2. The oracle b_0 returns zero at all M assignment positions, while b_j returns one exactly at j. One controller may create any finite network of finite-alphabet processors, each adaptive, with caching, recomputation, reads, communication and output writes. All such transitions and node creation are charged. Source queries expose one bit per request, never formula syntax or nonuniform advice. In each synchronized elapsed time step, every active processor can make **at most one** source query. Source index lookup may be granted free except for the charged query event; that only strengthens a lower bound.

Suppose on b_0 the network emits an output in class Y_0 and on each b_j an output in disjoint class Y_1, each with probability >=1-delta. These may be ordinary exact MCSP YES and NO classes for fixed target truth-table length N=2^n and gate threshold s=floor(N^mu), but **only conditional on a constructor satisfying these output promises**. No such SAT-to-MCSP constructor is assumed to exist.

On the zero oracle with fixed shared randomness rho, let Q_rho be the set of distinct source addresses accessed by *any* node, W_rho the sum of all processor transition/event charges, T_rho the synchronized elapsed time, k_rho(t) the number of source-capable active processors during tick t, and K_rho=max_t k_rho(t). Then

$$
\Pr_\rho[j\in Q_\rho]\ge 1-2\delta\quad(\text{each }j);
\qquad
\mathbb E W_\rho\ge\mathbb E|Q_\rho|\ge(1-2\delta)M.
$$

Moreover, pathwise,

$$
|Q_\rho|\le\sum_{t<T_\rho}k_\rho(t)\le K_\rho T_\rho,
\qquad
\boxed{\mathbb E[K_\rho T_\rho]\ge(1-2\delta)2^v.}
$$

If a deterministic cap K_rho<=K(v) holds on *every* run, then

$$
\boxed{\mathbb E T_\rho\ge(1-2\delta)2^v/K(v).}
$$

Consequently polynomially many such evaluation-only machines cannot have polynomial expected elapsed time when v grows, even with arbitrary shared intermediate computation and arbitrary work space. With dynamically varying K, one may NOT replace E[KT] by E[K]E[T]; correlations can defeat that inference.

**Proof.** Couple the zero-oracle and single-positive-j runs using exactly the same random tape. All local transitions, source answers, messages, output writes and switches remain identical up to the first query at j. If the zero run never queries j, the complete final outputs coincide and cannot both belong to disjoint output classes. Thus Pr(j unqueried) is at most the sum of the two error probabilities, <=2delta. Sum indicators over all M addresses for E|Q|; every distinct probe contributes at least one charged work event. At most k(t) distinct source queries may occur during tick t, which gives the pathwise work-depth bound, and a deterministic K cap yields the expected elapsed-time bound. QED.

**Sharpness and attribution:** An abstract OR/needle decision algorithm chooses with probabilities delta, delta and 1-2delta to output ONE without queries, output ZERO without queries, or query all M coordinates and decide exactly. It incurs error delta and E|Q|=(1-2delta)M on zero. The bound is **not** a construction of a high-complexity MCSP-NO output. TMR-2/032 gives, for zero vs exactly r ones, exact expected-query minimax Q*=(1-delta)h_{M,r}(delta/(1-delta)). For r=1, H(q)=(M-q)/M, h(z)=M(1-z), whence Q*=(1-2delta)M. Thus the source-query optimum is a corollary of TMR-2/032; TMR-4/034 correctly adds disjoint-output coupling but must not claim a novel optimal query coefficient.

## Unrestricted-machine falsifier and input accounting

Here v is the number of formula variables, M=2^v is the number of evaluation points, n is target function arity, N=2^n its full explicit truth-table length, and L is the source CNF encoded **bit length**. They are separate quantities. For each v>=3, four proper three-distinct-variable clauses using both polarities of two helpers jointly enforce any chosen literal. One block per variable enforces one witness a. An extra repeated forcing block yields unique SAT; an opposite forcing block yields UNSAT at the **same L=Theta(v log v)**. A syntax-aware machine distinguishes the cases in O(L) time by inspecting that block, without testing 2^v assignments. Therefore the implication from evaluation-only source queries to **every** deterministic 3-SAT decider is **FALSIFIED/RETIRED**. The oracle-network work-depth theorem survives unchanged as PROVED/RESTRICTED.

Under a polynomial cap K(L), evaluation-only expected time is >=2^{Omega(L/log L)}/K(L), but **this is not a SAT time lower bound**. Input delivery, source preprocessing, messages and tape movement need charging when translating to the user's physical single-tape-network model. No such unrestricted simulation exists here. One-tape total, one-way input plus one work tape, and free indexed-source queries are distinct models.

## Primary-source theorem matrix

| Original source and exact location | Input, thresholds, model, hypotheses, conclusions | Audit |
| --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021 **Theorem 1, printed p.23:3** | Ordinary exact MCSP decision, full N=2^n truth-table input, threshold 2^{mu_1 n} for a particular sufficiently **small** existential mu_1>0; uniform deterministic one-way read-only input plus one two-way work tape. **CONDITIONAL**: exclusion from DTIME_1[N^{1.01}] implies P!=NP. | Antecedent remains OPEN. Network oracle work is a different computational task. |
| Same STACS paper **Theorem 2, p.23:3** | Exact MCSP, same physical tape model with two-sided randomized error, **different larger mu_2** near 1; proved nonmembership BPTIME_1[N^{1.99}]. | Do not substitute larger threshold into Theorem 1. |
| Same, **Theorem 3, p.23:4** | Exact MCSP threshold 2^{mu n}, any 1/2<mu<1; randomized one-way-input one-work-tape oracle algorithms restricted to oracle-query lengths N^{o(1)}; some mu'>0 yields an N^{1+mu'}-time exclusion. | High-threshold short-query barrier, not low-mu magnification. |
| McKay, Murray, Williams, STOC 2019 accepted version **Theorems 1.2-1.3, printed pp.2-3** | Search-MCSP with A-oracle gates, explicit N=2^n table, time-constructible s(n)>=n; one-pass streaming with poly(s) space/update using short Sigma_3SAT^A oracle queries; nonexistence for certain PH-oracle problems implies P!=NP. | Search with oracle gates is not ordinary exact decision MCSP and not source-evaluation SAT. |
| TMR-2/032 exact sparse-oracle minimax and TMR-4/034 global coupling | Oracle-only zero-vs-r-support source; all source bit reads charged, no syntax. | r=1 recovers the coefficient; NETWORK051 adds synchronous charged work-depth, still restricted. |

Primary originals inspected with page screenshots: [STACS 2021](https://drops.dagstuhl.de/storage/00lipics/lipics-vol187-stacs2021/LIPIcs.STACS.2021.23/LIPIcs.STACS.2021.23.pdf), [STOC 2019](https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf). Related primary literature inspected for background but **no theorem imported**: [Chen et al., ITCS 2020 locality](https://doi.org/10.4230/LIPIcs.ITCS.2020.70), [Oliveira-Santhanam ECCC 2018](https://eccc.weizmann.ac.il/report/2018/139/). Natural-proof or locality barriers do not prove separation impossible.

## Integrated peer audit and ranked dependency map

| Original work and exact path | Status and missing transfer |
| --- | --- |
| TMR-1/031 and /033, research/agents/tmr-1/2026-11-14_1810_TMR1_LINEAR_SPARSE_STREAM_DECODER033.md | Indexed circuit O(t log t) and linear shared sparse-output generation are CANDIDATE/RESTRICTED, peer review OPEN. No multiply-indexed-cost-to-total rule; no ordinary MCSP decision lower bound. |
| TMR-2/032 research/agents/tmr-2/2026-11-14_1720_TMR2_EXPECTED_QUERY_MINIMAX032.md; /033 one-sided acceptance fiber | Exact oracle mean-query minimax subsumes r=1 global decision; one-sided MCSP input-bit read bound remains restricted and at most linear, not N^{1.01}. |
| TMR-3/033 research/agents/tmr-3/2026-11-14_1820_TMR3_MULTIHEAD_SUFFIX_FRONTIER033.md | Near-N ingress under physical common-left-origin heads is PROVED/RESTRICTED pending review; does not cover freely distributed source inputs or superlinear post-ingress work. |
| TMR-4/034 research/agents/tmr-4/2026-11-14_1838_TMR4_GLOBAL_ORACLE_SHARED_TRACE_BARRIER034.md | Source coupling independently mathematically verified for oracle-only access. New work-depth corollary does not cross the formula-syntax interface. |
| TMR-5/029 research/agents/tmr-5/2026-11-14_1750_TMR5_POLYREPEAT_STREAMING_AMORTIZATION_AUDIT029.md | Fixed program with L=o(N), polynomial output, MCSP-NO target and shared O(N) output (CANDIDATE/RESTRICTED). Falsifies automatic summation of indexed costs even for short sources. |
| Claude ONETAPE/DIRECTPRODUCT originals, TMR-2 Walsh/moment original, LSPV-3/615 original checker falsifier and GROKPROOF original progress | Retain restricted/failed status. None proves arbitrary multitape 3-SAT lower bounds. |

**Surviving routes ranked:** (1) CHMY exact small-mu ordinary MCSP decision N^{1.01} lower-bound premise, OPEN but strongest known conditional implication to P!=NP. (2) Syntax-aware polynomial-explicit-output SAT-to-MCSP with exact threshold, both labels and charged construction, OPEN; reverse label orientation UNSAT-to-YES would conditionally imply NP=coNP. (3) Physical one-tape ingress and randomized input queries, PROVED/RESTRICTED but insufficient exponent. (4) Evaluation-only parallel network product, PROVED/RESTRICTED but cannot be generalized to all syntax-aware SAT algorithms, as the forcing-block family explicitly demonstrates.

**Retired implications:** a global assignment-evaluation query lower bound is an unrestricted SAT-machine lower bound; indexed-output lower bounds add across outputs despite sharing; high-mu CHMY Theorem 2 automatically satisfies low-mu Theorem 1; E[K]E[T] may replace E[KT] without a deterministic machine cap. None of these retire valid underlying restricted results.

## Verification, provenance and next step

Independent **native CPython** executed experiments/tmr/tmr5_network_workdepth051.py, producing results/raw/tmr/2026-11-14_1850_TMR5_NETWORK051_RAW.json. It completed **32,410 assertions, zero failures**, M=1..44, K=1..8, all singleton positions, four sharpness branches, and 15,234 coupled adaptive network source traces. This is a semantic event-proxy execution, **not** native replay of TMR-4/034's original peer script and not a compiled finite-state TM. Asymptotic status rests on the elementary proof above, not finite tests. TMR-4's original source experiments/tmr/tmr4_global_oracle_audit050.py and exact raw results were inspected. Historical controls inspected: research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex, .../2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex, research/agents/tmr-2/2026-11-14_0823_TMR2_MAXSAT_WALSH_SIGN_ROBUSTNESS022.md, research/agents/lspv-3/2026-11-13_0727_LSPV3_615_HASH_BINDING_SOUNDNESS_COUNTEREXAMPLE.md and GROKPROOF/2026-10-31_0522_GROK_PROGRESS.md.

Preflight: controlling Nov14 directive read FIRST and rechecked unchanged blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a; Nov13 replacement, both trackers, canonical main.tex, AGENTS/CODEX/skill, all TMR handoffs, issue #3 through TMR-4/034 and original evidence read. proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; authentic proof2 Git blob 930c5eeddafce656717f28055a7a9a755f44737c (1,051,196 characters); authentic main.tex Git blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 (2,545,859 characters), recovered after empty Contents API bodies. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex left unchanged pending independent review, all five existing schedules untouched.

**Peer request:** TMR-2 independently verify the r=1 attribution and disjoint-class postprocessing; TMR-3 audit the parallel k(t) work ledger, source initialization and E[KT] versus E[K]E[T]; TMR-4 seek a truly syntax-aware, polynomial full-table, both-label MCSP reduction; TMR-1 audit exact low-mu and uniformity of the magnification premise. **Next TMR-5 target:** find or falsify inevitable superlinear *ordinary MCSP decision work after source input acquisition* at the precise low-mu threshold, without imposing an evaluation oracle or a chosen representation.

END_OF_REPORT::TMR5::030::2026-11-14_1850_PST
