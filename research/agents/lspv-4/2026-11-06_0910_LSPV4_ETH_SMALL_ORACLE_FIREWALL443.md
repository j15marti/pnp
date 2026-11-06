# LSPV-4/443: ETH firewall for unconditional small-SAT-oracle contraction

**2026-11-06 09:10 PST, Route A primary. Status: PROVED/RESTRICTED elementary lemma, CONDITIONAL ETH corollary, COMPUTATIONAL checks, universal Route A OPEN. P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE: hypothesis and falsifiers

Hypothesis: An **unconditional decider-independent** polynomial-time algorithm that decides every sparse 3-CNF by making polynomially many SAT queries of sublinear actual binary length would yield a deterministic subexponential algorithm for sparse 3-SAT. Falsifiers: (F1) a child is only a compact descriptor of a *larger virtual query*; (F2) hidden superpolynomial preprocessing or query count; (F3) incorrect normalization of binary input size N versus variable count n; (F4) a construction that only exists *assuming* SAT in P or that nonblackbox transforms a particular polynomial-time solver. F4 prevents this ETH argument from refuting the current conditional Route A.

Search correction: project LSPV-2/DELAYOR1 (blob 1c53f86b) already proves the padded-blackbox exponent coefficient restriction and the subcube covering bound; LSPV-4/441 (blob 704db91d) proves guarded full-length fallback failure. LSPV-4/442 (2c49fef5) is a distinct branching/UP materialization falsifier. This note adds the precise adaptive small-oracle to subexponential consequence and **does not claim novelty** over standard ETH methodology.

## Theorem 443.1 (PROVED/RESTRICTED; ETH consequence CONDITIONAL)

Fix constants b, mu > 0 and 0 <= lambda < 1. Let C be a single uniform deterministic, **decider-independent** procedure which, for every proper sparse 3-CNF F with n occurring variables, at most c*n clauses, and ordinary dense-renumbered binary encoding N <= C0*n*log2(n+2), correctly decides the SAT/UNSAT label using:

1. At most N^b own steps, charging all source reads, parsing, preprocessing, policy and failed policy search, child construction, joins, caching and output.
2. At most N^mu **actually executed**, possibly adaptive, ordinary SAT queries, each of **explicit guest input bit length** <= N^lambda.
3. Correct answers for SAT, UNSAT, with a defined polynomial-time malformed-input path.

Then there is a total uniform deterministic sparse-3-SAT decider with

$$
T(n) \le N^b + N^{\mu+O(1)}2^{O(N^\lambda)}
=2^{O((n\log(n+2))^\lambda)+O(\log n)}
=2^{o(n)}.
$$

**Proof.** Simulate C, replacing each queried SAT oracle by exhaustive assignment search on the actual explicit queried formula. A formula encoded in ell bits contains at most ell distinct occurring variables, so exhaustive SAT takes 2^{O(ell)} poly(ell) time. Feeding the exact answer to the controller yields the exact same adaptive future transcript by induction. Thus even adaptive OR/AND branching, early termination, reconvergence and reuse of previously answered queries cannot defeat the upper bound. Because ell <= N^lambda and N=O(n log n), (n log n)^lambda=o(n) for lambda<1. ETH (in its equivalent sparse-3-SAT form by the sparsification lemma of Impagliazzo, Paturi and Zane) prohibits the derived 2^{o(n)} algorithm. QED.

**Corollary (CONDITIONAL on ETH).** A polynomial-time, unconditionally available, decider-independent all-input shrink-and-join controller with q=N^{3/5+o(1)} and genuinely short ordinary SAT children L=N^{1/2+o(1)} would refute ETH. This is **not an unrestricted time lower bound**, and the corresponding 2^{o(n)} upper bound is not an FLMV polynomial time-space contradiction.

**Nonapplicability to the actual Route A quantifiers.** Route A proposes: *if a uniform total correct polynomial SAT decider A exists*, construct a recursively iterable compiler possibly depending on A and satisfying t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2). ETH already rules out such an A. Therefore ETH is consistent with the **conditional implication**, and this theorem cannot refute it. Any proposed compiler must state whether it is unconditional and oracle-oblivious or code-dependent, and must distinguish explicit guest input length from a virtual input port.

## Existing published hard-family and method ledger

| Family | Exact original source | Theorem scope | Shortcuts and unresolved transport |
| --- | --- | --- | --- |
| Connected odd-charge cubic Tseitin on expanding graphs | H vertices; 3H/2 edge variables; 4H original signed 3-CNF clauses. For edge IDs a<b<c at vertex v, use (l_p(x_a) OR l_q(x_b) OR l_(p XOR q XOR 1 XOR chi_v)(x_c)) for p,q in {0,1}; l_0(x)=x, l_1(x)=NOT x. The established LSPV-2/446 binary packet has N=8+(H+1)+(M+1)+2Mw+12H(w+1)+2, w=floor(log2 M)+1, M=3H/2. | Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001): 2^{Omega(H)} **ordinary shared-DAG Resolution** refutation size on suitable odd-charge expanders. Mathematical odd-parity UNSAT certification is not a native R_mix341 certificate. | XOR of all vertex equations decides this authenticated family efficiently; never claim arbitrary SAT machine, ER, GF(2) or full fixed mixed-calculus hardness. LSPV-4/442 rules out only particular branch+UP+materialization architectures. |
| Sparse proper 3-CNF, m<=c*n | Dense-renumbered n variables and O(n) signed width-three clauses, N=O(n log n) bits. | IPZ 2001 sparsification connects general and sparse 3-SAT for subexponential algorithms. ETH is an **unproved hypothesis**, not an established lower-bound theorem against all algorithms. | Exhaustive search 2^n poly(N) is an upper bound. Our theorem is about unconditional oracle-size shrinkage for the entire input class, **not** a claim that individual Tseitin instances are worst-case for arbitrary SAT algorithms. |

No historical R_mix341 rule, grammar or weight was changed. Context-labelled AND/OR shared refutation DAGs, free hindsight choice of legal optimum, native GF(2)/ER upper controls and noncircular B3 remain Route B's separate OPEN work.

## Independent finite test and resource ledger

Executed Python producer oracle_replacement_control.py and independently authored JavaScript verifier: 76 exact source fixtures (K4 and cube original signed cubic Tseitin odd/even sources, and 72 seeded finite proper 3CNFs); 39 SAT, 37 UNSAT; 608 actually evaluated branch leaves; seven malformed source rejections; one explicit hostile control rejecting inference of UNSAT from a single UNSAT branch. Independent Node run: **16,581 assertions PASS**, checking SHA-256 source bindings, parsed clauses, residual syntax, compatible-assignment semantics, and all required AND/OR labels. The finite fixtures use strict DIMACS, **not** the LSPV-2/446 canonical packed binary interface. The tested branch children are not claimed to shrink to N^{1/2}.

The report is a **symbolic machine-time upper bound**, not host timings used as a lower bound. Controller cost N^b includes source/index/head operations, child formation, failed policies, output and join; each simulated guest question costs 2^{O(N^lambda)}. Explicit queries are charged at actual bit length. No $N^{1/2}$ peak-space claim is made for the controller, no native FLMV machine run was executed, and no paid R_mix341 inference certificate was generated.

## Sources actually inspected and continuity

Project governance at commit 4e29ed7646f484707767acb6e63ec5f38afd98a8; live issue #3; AGENTS.md (19656af1), CODEX.md (754999f5), repo skill (b8df83a7); LSPV-2/446 (6176af08), LSPV-4/442 (2c49fef5), LSPV-2/DELAYOR1 (1c53f86b), MAIN84 (88005bc1); Grok GROKPROOF/2026-11-06_0515_PROGRESS.md (93f9202d); Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727). Required new repositories: konard/p-vs-np/scripts/proof_status.json (93b77ed3) and blkph0x/p-vs-np-proof-research/CERTIFIED_RESIDUAL_QUOTIENT_REPORT.md (b37da20a), both inspected as unproved/incomplete-method sources. Also inspected MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd19), meelgroup/frat-xor/README.md (38a137bc), openai/math/README.md (cc5b0a03). No external repository executables were built.

Primary papers: Impagliazzo, Paturi, Zane, *Which Problems Have Strongly Exponential Complexity?*, JCSS 63 (2001), 512-530, DOI 10.1006/jcss.2001.1774; Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), 835-865, DOI 10.1145/1101821.1101822; Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), 209-219. Primary PDFs opened and visually checked. No Google-branded search was independently invoked. FLMV gives beta(6/5)=23/45, strict gap 1/90 over 1/2. The historical root main.tex could not be fetched in readable form despite a blob SHA, and was left unchanged. Full corpus preflight and native FLMV execution unavailable.

**Advance:** exact restricted theorem identifying what a truly unconditional general small-SAT-query compiler would imply. **Verification:** symbolic proof and 16,581 independent finite checks. **OPEN:** the desired uniform, decider-dependent, all-input, repeatedly iterable and fully charged FLMV contraction, and all fixed-mixed R_mix341/B3 obligations. **P versus NP OPEN.**
