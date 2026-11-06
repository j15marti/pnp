# LSPV-4/444: Unordered original-source authentication, read-once space floor, and charged bucket repair
**2026-11-06 09:36 PST; Route A primary. PROVED/RESTRICTED and COMPUTATIONAL. P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE
Hypothesis: exact authentication of every clause permutation of the known strict cubic Tseitin 3-CNF needs linear retained state in a read-once pass, but admits a charged multipass repair.
Falsifiers: (F1) injectively represent all first-half subsets in sublinear states; (F2) reread/index source while calling it read-once; (F3) ambiguous mapping of signed clause to original facet; (F4) duplicate/missing corruption accepted by the two-bit buckets. F1 impossible by counting, F2 expressly excluded, F3/F4 attacked by independent finite controls. This does **not** rule out faster random-access normalization.

## Established source, theorem and shortcut ledger
A fixed authenticated simple cubic graph G has H vertices, M=3H/2 edges, Boolean variables x_e and charges chi_v. Each v has increasing incident edges a<b<c and four **original proper 3-CNF** clauses
$$
C_{v,p,q}=\ell_p(x_a)\lor\ell_q(x_b)\lor\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),\qquad\ell_0(x)=x,\quad\ell_1(x)=\neg x.
$$
There are m=4H distinct clauses. Signed literal records use 12H(w+1) bits with w=ceil(log2(M+1)); with a graph/charge header, N=Theta(H log H). For suitable *growing odd-charge cubic expander* families, ordinary **shared-DAG Resolution** size is 2^{Omega(H)} (Urquhart 1987; Ben-Sasson/Wigderson 2001). This is NOT mixed R_mix341, ER, or all-algorithm hardness. Connected Tseitin SAT is exactly total charge parity zero; GF(2) is the mandatory fast shortcut, and finite K4/cube/Petersen samples are not asymptotic-hard certificates.

## Theorem 444.1 (PROVED/RESTRICTED)
A deterministic one-pass, read-once recognizer receives m fixed-width clause records. It must accept every permutation of the exact original clauses and reject a one-missing/one-duplicated expected clause. After its first m/2 records, it cannot reread the input; all persistent state, even head positions and caches, is charged.

For every subset S of [m] of size m/2, present an ordered prefix containing precisely S. If two distinct S,T ended in the same state, append the complement of S. Prefix S yields a valid permutation; prefix T yields a duplicate and a missing clause, yet the common state and suffix would force the same answer. Contradiction. Therefore at least binomial(m,m/2) post-prefix states exist and
$$
S_{bits}\ge\lceil\log_2 {m\choose m/2}\rceil\ge m-\log_2(m+1)=\Omega(H)=\Omega(N/\log N).
$$
The lemma does NOT apply to random-access machines allowed to reread, to arbitrary SAT algorithms, or to any claimed generalized computation lower bound.

## Theorem 444.2 (PROVED/RESTRICTED)
Given an authenticated graph/charge reference with indexed endpoint and vertex incidence tables, decode each signed clause to its unique facet ID j=4v+2p+q, rejecting foreign/incorrect facets. Divide m possible IDs into buckets of b; in each bucket maintain b **two-bit saturated counters**, scan all original clauses, increment the appropriate counter, reject every 0 or 2, clear and reuse the bank.
$$
T_{bucket}(N,b)=O(\lceil m/b\rceil N\,polylog N),\qquad S_{bucket}(N,b)\le 2b+O(\log N).
$$
On a valid source the specified algorithm performs exactly m ceil(m/b) clause visits. b=Theta(N^{1/2}) fits memory but incurs N^{3/2-o(1)} source-work; the N^{11/10+o(1)} local-work target in *this design* demands b>=N^{9/10-o(1)}, missing space. A different verifier could improve this tradeoff. An untrusted graph header would require a separately charged authentication stage; this theorem assumes an authenticated direct-access header and is not an all-input compiler.

## Reproducibility and physical resource ledger
Python archival producer built original signed clauses for K4, cube and Petersen, both even and odd charges, with permutation, reordered-literal, duplicate/missing, wrong sign, foreign ID, missing and extra clause controls: **672 instances, 192 accept, 480 reject, 4,637 assertions**. Independent Node reconstructed the clauses and source hashes without importing producer: **17,702 PASS assertions**, **431,888 clause visits**, with brute-force small SAT parity controls. K4 has binomial(16,8)=12,870 distinct first-half sets and 300 explicit contrasting suffix tests. Seed 202611060936.

The indexed read-only input, source lookup/head reads, bucket clearing, scan repeats, reference retrieval, counters, output and highest simultaneous workspace are charged. No child was generated, no guest SAT solver executed, no proof inference or branch-join performed, and no general failed-policy discovery search was invoked. Host Python/Node measurements are not native random-access TM measurements. For a full compiler, all-phase peak still obeys the required analysis s'<=max(rho,eta,lambda,lambda*s), with rho including every local phase even if later freed.

## Continuity, literature and status
Read current issue #3, the Nov-2 governing five-role handoff, AGENTS/CODEX/skill, LSPV-2/446 and /447, LSPV-4/442 and /443, Grok 2026-11-06_1617 and Claude TPORT-0002 actual files. Inspected **both** required external repos: konard/p-vs-np README and scripts/proof_status.json (model-limited formalization); blkph0x/p-vs-np-proof-research METHOD_INDEX, INDEPENDENT_AUDIT and CERTIFIED_RESIDUAL_QUOTIENT_REPORT (proof-producing, assumption-limited methods). CNFgen tseitin.py, FRAT-XOR format.md and openai/math README inspected; search covered FLMV 2005, Reingold 2008, Urquhart 1987 and Ben-Sasson/Wigderson 2001. No independent external checkout/build; no separate Google-branded search.

Root main.tex returned blob f41d1cd2 but zero readable bytes, so no unsafe update was made. Exactly five roles, 2 Route A / 3 Route B, schedules and native proof weights remain unchanged. **Actual advance:** restricted authentication state floor plus exact, charged, finite-tested multipass repair. **OPEN:** any universal recursively iterable all-input SAT contraction satisfying t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2); full mixed-calculus lower bound; noncircular B3. **P versus NP OPEN.**
