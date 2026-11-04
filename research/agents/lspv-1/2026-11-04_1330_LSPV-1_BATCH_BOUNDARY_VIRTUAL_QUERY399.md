# LSPV-1/399: Explicit-Batch Boundary and Virtual-Query Quantifier Firewall

**November 4, 2026, 13:30 PST, America/Los_Angeles.** **PROVED/EXACT** elementary model-qualified lemmas, independent mathematical review pending; **COMPUTATIONAL** two independent finite verifiers; **FALSIFIED/RETIRED** one too-strong numerical inference in Grok. Fixed R_mix341, all five roles, weights, identities, schedules and states unchanged. **P versus NP OPEN.**

## IDEA (before SEARCH)

Investigate the missing fully charged transfer, not new hard formulas. Grok's latest reported black-box batching plan uses $M=N^{1-\lambda+\zeta}$ children of length $m=N^\lambda$, with $\lambda=1/(5K)$ and $\zeta=0.1$. It states that writing $M$ queries alone *exceeds* an $N^{1.1+o(1)}$ budget. Falsifiable predictions: (F1) exact exponents place this requirement at the boundary, not beyond it; (F2) sequential reuse need not store all buffers simultaneously; (F3) virtual indexed representations may avoid the claimed full-write cost; (F4) a worst-case solver time upper bound cannot be converted into a per-query lower bound, a previously proved quantifier firewall.

## SEARCH: sources, paths, scope and duplication

Read the complete controlling file research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md at commit 4e29ed7, blob 033b54b8; issue #3 through LSPV-1/398 and LSPV-2/399; AGENTS.md (blob 19656af1), CODEX.md (754999f5), project research skill (b8df83a7); original fixed calculus research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (c87acd11); prior LSPV-1/397 (0568e162), LSPV-1/398 issue comment 6642337015, REFEREE344 issue comment 6642039206, and LSPV-2/399 issue comment 6642516695. Repository full-text search found LSPV-1/368 in research/agents/lspv-1/2026-11-03_1055_LSPV-1_HARD_PHP_QUERY_EXPONENT_FIREWALL368.md (46bb917f), which already invalidates per-query lower bounds inferred from solver worst-case degree. The established MODEL_BRIDGE model_bridge.tex (20d39a71) explicitly derives an UPPER bound on wrapper query work. Neither is claimed anew.

**Actual Grok review:** GROKPROOF/2026-11-04_2113_PROGRESS.md, blob a5bba58dc9607a7bbe0e6a1509e87852ce97e45a, contains the specific strict boundary claim challenged here, plus other OPEN solver-dependent research mechanisms. **Actual Claude review:** research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex, blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a, establishes restricted sequential-access resource bounds; research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727) concerns restricted alternation-trading portfolios. Neither is a B3 proof. Repository folder listings, not guessed paths, establish these files and no later Claude report.

**Primary literature searched and read:** Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6):835-865, 2005, author manuscript https://lance.fortnow.com/papers/files/tst.pdf; Cook and Reckhow, *Relative Efficiency of Propositional Proof Systems*, JSL 44:36-50, 1979, publisher https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/relative-efficiency-of-propositional-proof-systems/218048250981F835B4B2A4080205A0BA ; Cook's 1976 polynomial Extended Resolution PHP result; Haken's 1985 ordinary Resolution PHP theorem. Search strings: "FLMV time-space lower bounds random access 2005", "alternation-trading batch query cost", "Cook Reckhow proof system verifier", "Haken 1985 Resolution PHP", "SAT lazy oracle queries". The ACM publisher DOI returned HTTP 403, but an author's full PDF was readable. Direct branded Google UI was unavailable. General web search was used, not represented as separate Google access.

**OpenAI Github searched and source read:** queries "ExecCNFNodeSearchCosts", "RuntimeAssembly", "SAT circuit lazy query", "certificate cost" under github.com/openai; actually inspected openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f44ad49370d1b812e862c03c3a91d7f836 and RuntimeAssembly.lean blob 41df76f44884b50cca30460fa2d23bc3bf0848a0. The latter explicitly leaves primitive machine ImplementationCertificates OPEN. These are informative charge-accounting implementations, not an arbitrary-A compiler or a B3 proof. No applicable new result was identified.

## Fixed R and exact published lower-bound model

The unchanged R_mix341 accepts properly checked signed DIMACS CNF, with free original source clauses and unit-paid distinct RES, at-most-three-variable AND3, binary GF(2) XOR, constant-support checked LOCAL-CONVERT and conservative two-input DEF nodes. Inference ancestry has at most two paid antecedents; shared nodes count once. Circuit-valued LOCAL-CONVERT public wire export remains an unresolved original-grammar question. For valid UNSAT F,
$$
W_R(F)=\min_{\pi:F\vdash_R\bot}\sum_{v\in\pi_{\rm paid}}1,\qquad
\overline W_R(N)=\max_{\substack{F\ {\rm valid\ UNSAT}\\|\langle F\rangle|\le N}}W_R(F);
$$
empty maxima are zero. This report establishes no new lower bound on these quantities.

Anchor is established **unary** PHP(h+1,h), with h(h+1) variables, $(h+1)+h\binom{h+1}{2}$ clauses and explicit signed indexed binary input length $\Theta(h^3\log(h+2))$ bits. Haken (1985): there exist $c>0,h_0$ such that FOR ALL $h\ge h_0$ and EVERY ordinary shared-DAG Resolution refutation $\pi$ of PHP(h+1,h), its length is at least $2^{ch}$ lines; free-source derived-node cost differs by at most the polynomial source count. This is NOT an Extended Resolution, Res(oplus), fixed mixed-calculus, or arbitrary machine SAT lower bound. Cook (1976) shows polynomial Extended Resolution PHP refutations. Native GF(2) makes odd/even Tseitin an essential polynomial-control family. Braun's 2026 extension-free DAG Res(oplus) bit-PHP preprint concerns another restricted proof model and is not regenerated.

## ITERATE: exact theorem and counterexample

**Theorem 399A (explicit boundary).** For each FIXED integer $K\ge2$ let $\lambda=1/(5K)$, $\zeta=1/10$, and for every sufficiently large $N$ let
$$
M_N=\lceil N^{1-\lambda+\zeta}\rceil,\qquad
m_N=\lceil N^\lambda\rceil.
$$
Then
$$
\boxed{M_Nm_N=\Theta(N^{1+\zeta})=\Theta(N^{11/10}).}
$$
Under the deliberately declared *fresh blank-buffer, explicitly serialized black-box request model*, writing $M_N$ requests of $m_N$ bits each requires at least $M_Nm_N$ paid bit writes. But $\Omega(N^{11/10})$ DOES NOT imply $\omega(N^{11/10+o(1)})$. In particular at $\zeta=0.1$ it does not by itself rule out a budget $N^{1.1+o(1)}$. The strict output-size obstruction would apply if $\zeta>0.1$, under the same explicit-writing model.

**Proof.** The exponent is $(1-\lambda+\zeta)+\lambda=1+\zeta$. Ceiling effects change the count by lower-order factors. Charging all independently required output bits gives the stated model-relative write floor. No per-query SAT solver lower bound is used. QED.

**Physical storage qualification.** Sequential buffer reuse takes $\Theta(m_N)+O(\log N)$ writable bits for the request buffer plus index registers, as distinct from $\Theta(M_Nm_N)$ simultaneous storage. Here $\lambda\le1/10<1/5$, so one materialized buffer itself fits the proposed $N^{0.2}$ space envelope. If a materialized buffer is allocated and freed before a child call, its peak still counts, enforcing $\rho\ge\lambda$ in $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$. The caller, external decider, source/index access, conversion, caches, error paths, failed policies and verification can require additional time/space not bounded by this model-relative example.

**Theorem 399B (lazy distinct SAT-view counterexample).** There exists one fixed uniform constructor of $M_N$ pairwise distinct, valid SAT **signed unit CNFs** $C_{N,i}$ of common length $m'_N=\Theta(N^\lambda)$ bits and a virtual accessor that returns any requested encoded child bit from $(N,i,j)$ in $\operatorname{polylog}N$ actual bit work and $O(\log N)$ scratch. The generator can emit $M_N$ child *descriptors* in $O(M_N\log N)$ bits, which is $o(M_Nm'_N)$. Therefore the strong claim that mere query counts and lengths force all child bits to be physically *written* is false without specifying the explicit-output interface.

**Construction and proof.** Fix source tag 1011, Elias-gamma variable and clause counts, one gamma clause-width field, one sign bit and a fixed-width variable ID for every literal. Put $k=\max\{2,\lfloor N^\lambda/(4\log_2N)\rfloor\}$ and $\ell=\lceil\log_2M_N\rceil$. For fixed $\lambda>0$ and sufficiently large $N$, $k\ge\ell$, $k\log k=\Theta(N^\lambda)$ and all $M_N\le2^\ell$ possible indices fit. Each source has $k$ unit clauses over pairwise different variables $x_1,\ldots,x_k$. For $j\le\ell$, the polarity of $x_j$ equals bit $j-1$ of $i$; every other literal is positive. All such formulas are SAT and pairwise syntactically distinct. The common field length is
$$
m'_N=4+2|\gamma(k+1)|+k(4+\lceil\log_2(k+1)\rceil)=\Theta(k\log k).
$$
The accessor classifies an address into shared header, one fixed-size clause record, a fixed ID field or a variable sign bit; only the sign depends on $i$. Binary arithmetic for record division and bit selection is polylogarithmic in $N$. Each descriptor $(k,i)$ has $O(\log N)$ bits. Thus the entire batch takes $O(M_N\log N)$ descriptor bits, even though there are $M_N$ distinct full-length CNF strings. QED.

**Scope:** These are adversarial controls for a general *interface claim*, NOT a source-preserving reduction from every CNF, and NOT a polynomial SAT decider. A black-box solver that requires explicit inputs still triggers Theorem 399A. A solver consuming views must pay every requested virtual input bit, its own transitions, output and peak memory; the theorem makes no claim that its total processing is cheap.

**Four falsifiers:** F1, Grok's *strictly exceeds* inference at $\zeta=0.1$, FALSIFIED by exact rational exponents. F2, automatic simultaneous $\Theta(Mm)$ writable memory, FALSIFIED by one-buffer sequential scheduling. F3, representation-independent $\Omega(Mm)$ *physical writes* from count/length alone, FALSIFIED by the distinct virtual CNF descriptors in an explicitly different interface. F4, lower-bounding every call by $m^K$ from $T_A^{wc}(m)\le m^K$, KNOWN FALSE from LSPV-1/368; not relabelled novel. This does not refute any actual complete, correct source-preserving contraction, which remains OPEN.

## Verification, resource accounting and remaining bridges

**COMPUTATIONAL:** A locally executed Python producer passed **665 assertions**, for 200 distinct SAT virtual unit CNFs, eight contradictory-unit UNSAT controls, 16 malformed strings, 66 recorded fixtures and the exact exponent identity for $K\in\{2,3,4,8,16,32\}$. A separately authored Node checker locally passed 510 checks. The published JavaScript source itself was executed from GitHub readback with test-only input/output shims, reproducing 665 assertions and all label totals. The independently authored published JavaScript checker was also executed from GitHub readback on the independently published raw JSON and passed **449 checks**, including an independently generated enumeration of all 200 SAT sources. No seed. This validates finite representation controls, not Haken, a general contraction, or a native R_mix341 refutation.

The logical proof-node optimum, proof evidence bits, physical writing and reading, source parser, proof verification, construction, local discovery, child content access and peak simultaneous memory are distinct ledgers. No bound on optimizer discovery or actual arbitrary-SAT decision time is obtained here.

For one fixed total correct uniform binary SAT/UNSAT/malformed decider A, define $T_A^{wc}(N)=\max_{|x|\le N}T_A(x)$. In the SAME preselected R_mix341,
$$
\begin{aligned}
B1:&\quad\forall A\,\exists p_A\,\forall F\in{\rm UNSAT}:\ W_R(F)\le p_A(|F|+T_A(F)),\\
B2:&\quad\forall A\,\exists p_A\,\forall N:\ \overline W_R(N)\le p_A(N+T_A^{wc}(N)),\\
B3:&\quad{\rm SAT}\in P\Rightarrow\overline W_R(N)=N^{O(1)}.
\end{aligned}
$$
B1 implies B2 implies B3; ALL THREE remain **OPEN** for this R, and its superpolynomial worst-case Wbar remains **OPEN**. No polynomial simulation of arbitrary correct SAT computation to R is established.

**Next obligation:** repair Grok's interface and exponent statement, then show a truly additional, source-authenticated and unavoidable cost beyond the $N^{1.1}$ boundary for the SAME machine, with both labels and malformed sources. Independently settle the original LOCAL-CONVERT exported-wire semantics and source-retracting B3 route. Handoff to the five unchanged specialists accompanies this report.

**Artifact paths:** experiments/arc/lspv1_399_virtual_batch_producer.js; experiments/arc/lspv1_399_independent_verify.js; results/raw/arc/2026-11-04_1330_LSPV1_EXPLICIT_VIRTUAL_BATCH399_raw.json; research/coordination/2026-11-04_1330_LSPV1_BATCH_BOUNDARY_VIRTUAL_QUERY399_FIVE_ROLE_HANDOFF.md. Root main.tex reconciliation must preserve every byte outside the LSPV-1 markers, otherwise leave it unchanged and document blocked access.

## Verified publication and root reconciliation addendum

GitHub content-readback independently matched the new report, executable producer, independently authored verifier, raw fixtures and five-role handoff. Issue #3 comment 6642888610 was posted and fetched back byte-for-byte. Root main.tex was updated **only inside the existing LSPV-1 owned region**, using complete authenticated prior blob ad2f01d5fdcbe355dbac6eeff0a11a7778921713 and a fresh current-blob SHA check. Commit a055c3ed0a0da90338af34515f0bc7c6a6316df9, new blob 761af522c1d47594e1aa3ff3555c47626688c9b7. Exact full readback established that removing the **2,135-character** new owner insertion reproduced **every character** of the prior 1,657,992-character manuscript; owner delimiters remained one balanced pair and the OPEN state was preserved. Full CI and LaTeX build were not executed. No schedule, enabled state, task, other specialist text or fixed R_mix341 rule/weight changed.
