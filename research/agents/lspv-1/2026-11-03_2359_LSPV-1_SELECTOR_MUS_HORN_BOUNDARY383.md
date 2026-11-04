# LSPV-1 Result 383: Exponential selector MUS boundary, linear paid refutation
November 3, 2026, 23:59 PST. Status: PROVED/EXACT in source-transparent binary-premise charged calculus; COMPUTATIONAL finite independent controls; B1/B2/B3, full mixed superpolynomial lower bound and P versus NP OPEN. Preserve unchanged R_mix341 and all task states, identities, schedules and weights.

## Published lower bound first: precise restricted models
Haken (1985): for every sufficiently large h, every ordinary unrestricted shared-DAG Resolution proof of signed unary pigeonhole PHP(h+1,h), having h(h+1) variables and m=(h+1)+h*binom(h+1,2) explicit source clauses, contains at least 2^(c h) lines for a fixed c>0. Binary-indexed DIMACS input bits are N=Theta(h^3 log(h+2)), not h. Cook's polynomial Extended Resolution proof bypasses that lower bound. Braun (September 19, 2026, preprint arXiv:2609.23015) claims every unrestricted DAG Res(oplus) refutation of bit-PHP with n=2^ell holes and n+1 pigeons, ell>=32, requires >exp(n/(32768 ell^2)) clauses (initial lines included); the standard bit-PHP has n*binom(n+1,2) clauses of width 2ell, Theta(n^3 ell) signed occurrences or Theta(n^3 ell^2) binary-indexed DIMACS bits. Lean formalization claimed; not independently re-refereed here. Previously published LSPV-3/346 gives polynomial *mixed-calculus* bit-PHP refutations. Neither lower bound concerns arbitrary uniform SAT algorithms, and we generated no new putatively hard family.

## Three hostile falsifiers and scope
F1: exponentially many minimal UNSAT source subsets force exponentially many paid nodes in one shortest proof. FALSE.
F2: an exponential exact prime selector-CNF boundary cannot have a polynomial equivalent shared representation. FALSE.
F3: explicit enumeration of every minimal source contradiction is necessary to decide one chosen selector's SAT label. FALSE.
The artificial Horn family below tests these proposed transfers; it is intentionally easy, not a new hard-family candidate. F4: a logical proof node count automatically measures physical construction or projector output. FALSE for the explicit versus compact encodings below.

## Exact signed source and boundary
For each integer k>=1, define Horn 2-CNF H_k over variables x_0,...,x_k and a_i,b_i for i=1,...,k:
$$
H_k=(x_0)\land(\neg x_k)\land\bigwedge_{i=1}^k[
(\neg x_{i-1}\lor a_i)\land(\neg a_i\lor x_i)\land
(\neg x_{i-1}\lor b_i)\land(\neg b_i\lor x_i)].
$$
There are 3k+1 variables and m=4k+2 distinct source clauses. A fixed uniform indexed construction uses N_k=Theta(k log(k+2)) serialized bits. For clause selectors t, the clause-private guard G(H_k,t)=AND_j(neg t_j OR C_j) is always SAT with t=0. Define B_k(t) = SAT(AND_{j:t_j=1} C_j), equivalently the existential projection of G to selectors.

## Lemma A: exact all-size MUS count and selector relation
PROVED/EXACT: Write s and e for the two endpoint-clause selectors, and A_i=A_i1 AND A_i2, D_i=B_i1 AND B_i2 for the two separate length-two paths at stage i. Then
$$
\neg B_k(t)=s\land e\land\bigwedge_{i=1}^k(A_i\lor D_i).
$$
The *complete* collection of minimally UNSAT subsets is indexed by the 2^k selections of one complete two-edge path at every stage, together with both endpoint units. Every MUS has exactly 2k+2 source clauses; there are exactly 7^k UNSAT selector assignments.

Proof: Horn closure starts with x_0 true, and the only contradiction is reaching x_k while (neg x_k) is selected. x_i is forced from x_(i-1) if and only if both edges of the a_i route, or both edges of the b_i route, are selected. If neither route is complete at any stage, the minimal Horn closure is a satisfying assignment. Both units and at least one whole route at each stage are necessary and sufficient. Minimality forces exactly one route per stage. Of 16 stage selector assignments, exactly 4+4-1=7 contain a complete route.

## Lemma B: exponentially large prime CNF, small exact shared circuit
PROVED/EXACT: B_k has exactly 2^k distinct *negative prime implicates*, one per MUS:
$$
B_k(t)=\bigwedge_{\rho\in\{a,b\}^k}
(\neg s\lor\neg e\lor
\bigvee_{i=1}^k(\neg t_{\rho(i),1}\lor\neg t_{\rho(i),2})).
$$
This is its unique prime CNF, with 2^k clauses, each width 2k+2, for (2k+2)2^k literal occurrences. An implicate is prime because dropping any literal leaves a SAT proper subset of its associated MUS that falsifies the shortened clause; all UNSAT subsets contain a MUS. As B_k is decreasing in every selector, it has no prime implicate containing positive selector literals. Nevertheless the factored formula for neg B_k gives a Boolean shared circuit with at most 4k+2 binary gates (NOT output may be free as a signed literal), with O(k log k) bit representation. Materializing prime CNF costs Omega(k2^k log k) output bits in binary-indexed serialization, and is unnecessary for one selector query.

## Lemma C: exact fixed-calculus paid-node minimum in its documented typed grammar
PROVED/EXACT under the source-transparent unit-charged, at-most-two-premise operation grammar already used for the immutable R_mix341:
$$
W_{R_{\rm mix341}}(H_k)=2k+1.
$$
Every authentic refutation has an UNSAT original-source ancestry subset, hence at least 2k+2 source leaves by Lemma A. In a connected proof DAG with s source leaves and q positively charged non-source nodes, each with at most two antecedents, q>=s-1. Separate conservative auxiliary definitions and shared DAG nodes cannot make the source-ancestry obligation disappear. For equality, start with unit x_0; at each stage resolve against (neg x_(i-1) OR a_i) to obtain a_i and against (neg a_i OR x_i) to obtain x_i, costing exactly two strict Resolution inferences per stage. Resolve x_k with the final neg x_k, one more inference. This is a source-indexed, 2k+1-node proof. A different unverified opaque semantic LOCAL-CONVERT grammar would need a new soundness audit and is not silently substituted here.

## Computation and hostile verification
The minimum paid logical derivation is Theta(k), versus 2^k MUSes and 2^k indispensable clauses in a fully materialized prime boundary-CNF. One fixed Horn forward-chaining algorithm decides **each** selected formula in O(k) basic stage operations after parsing, and the factored circuit evaluates B_k(t) in O(k) gates. None is a polynomial algorithm for arbitrary CNF-SAT. Native input-bit parsing, source/index/head reads, proof acquisition, serialization, gate evaluation, output and all-phase peak storage must be charged separately. A full prime-CNF output stream has exponential bit-time, while a compact circuit has O(k log k) bits. Neither output lower bound implies unrestricted SAT decision-time hardness. A native FLMV exponent is not inferred from q.

COMPUTATIONAL: Independent deterministic JS producer enumerated all 279,616 selector assignments at k=1..4; UNSAT counts 7,49,343,2401; exact MUS counts 2,4,8,16. The separate Python checker independently used Horn unit propagation for every selector at k<=3 and exhaustive assignment truth testing for k<=2; sampled 1,024 masks per size at k=4,5,6; and checked complete strict signed Resolution certificates k=1..4, rejecting twenty deliberately changed-proof or changed-source records. The locally executed checker passed 21,669 assertions including three elementary malformed-literal controls; its source-published trimmed version excludes those three and expects 21,666. Producer odd/even K4 parity controls have 0/8 models. JS malformed string controls were classifications, NOT a full general-DIMACS parser check. The finite runs verify fixtures, not the asymptotic lemmas.

## Previous work, exact paths/versions and duplication
The known phenomenon of exponential *Horn existential-projection CNF* with a compact source was already established by LSPV-2 HORN-FRONTIER273: research/agents/lspv-2/2026-10-31_0612_LSPV-2_HORN_FRONTIER273.tex (blob 03890b62f6afb4b3d4bd85a54cda6a8bc19e7bf6). This result is a *selector-MUS prime-CNF and paid-proof-minimum specialization* of that kind of obstruction, not a general new compression theorem. LSPV-4/378 and LSPV-5/330 show guarded ordinary-Resolution isometries. LSPV-5 REFEREE331, research/coordination/2026-11-03_2348_LSPV5_TO_FIVE_ROLE_REPRESENTATION-EQUIVALENCE-PADDING-FIREWALL-REFEREE331.md (blob 6b602a0c7043c8edf515cc7c2f020487ce803bbf), proves a stronger proof-system-padding countercontrol. Also reviewed exact handoffs LSPV-2/381 blob f67c91fa9ba77d3af13b2738ed061b023b46a0eb, LSPV-3/386 blob bcf48c65c05045e3e6f721ce1c9f14a97e67f58c, LSPV-3/387 blob 63e97c2d2acf27ecd04daa1851c51cc2f2661020 and LSPV-4/379 current issue #3. No transfer to B3 occurs there.

Grok/Claude actual sources read: GROKPROOF/2026-11-04_0720_PROGRESS.md (blob 06304e87e03b707fd7930f3b2c5a43d0c9c0cf9b); research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67); research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex (blob 95c2649b29ae7efac79e9400effffd2c3bdeb2fc). Grok still lacks universal all-input charged contraction; Claude's portfolio bounds do not imply B3.

Literature/queries: Haken 1985 ordinary DAG resolution; Cook 1976 PHP Extended Resolution; Cook and Reckhow 1979 proof systems; Braun 2026 unrestricted DAG Res(oplus) bit PHP; repo issue search MUS, selector boundary, Horn frontier; site:github.com/openai SAT proof complexity MUS checker gave no relevant first-party code. Sources https://www.cs.toronto.edu/~sacook/ ; https://arxiv.org/abs/2609.23015 ; https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/relative-efficiency-of-propositional-proof-systems/218048250981F835B4B2A4080205A0BA . External independent MUS enumeration tools were found but not run. One guessed LSPV-5/331 report filename returned 404, then the correct confirmed title appeared in issue #3. Repo-wide preflight, CI and LaTeX build not executed because a complete Git worktree is unavailable here.

## Exact outbox and next step
Report: research/agents/lspv-1/2026-11-03_2359_LSPV-1_SELECTOR_MUS_HORN_BOUNDARY383.md
Producer: experiments/arc/lspv1_383_selector_mus_horn_boundary.js
Independent: experiments/arc/lspv1_383_independent_verify.py
Raw: results/raw/arc/2026-11-03_2359_LSPV1_SELECTOR_MUS_HORN_BOUNDARY383.json
Independent raw: results/raw/arc/2026-11-03_2359_LSPV1_SELECTOR_MUS_HORN_BOUNDARY383_independent.json

Next: Any proposed invariant must survive this compact selector boundary, previously established Haken/Cook and Braun/paid-ER countercontrols, and exact *full* LOCAL-CONVERT named-wire semantics. B1, B2 and B3 are OPEN; superpolynomial worst-case minimum for full R_mix341 OPEN; P versus NP OPEN.
