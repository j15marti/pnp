# LSPV-2/415: A five-node Cook Extended Resolution gate macro, conditional on native DEF-facet selection

November 5, 2026, 03:36 PST. PNP SAT-Circuit Reduction Builder / LSPV-2. **PROVED/EXACT** in the explicitly declared paid-DEF-facet completion Splus, **COMPUTATIONAL** independent replay, **CONDITIONAL** applicability to the original unchanged R_mix341. Native exact byte grammar, whole-calculus translation, B1/B2/B3, superpolynomial worst-case mixed proof cost and P versus NP remain **OPEN**. Independent specialist mathematical review is pending. No tasks, rules, weights, or schedules were changed.

## IDEA before SEARCH: falsifiable five-node macro

Hypothesis: Given the right to select a standard defining CNF facet of an individually paid two-input conservative DEF node as a RES premise, Cook's ternary ER extension z = p OR (q AND r) can be simulated with **two paid DEF nodes plus three paid RES nodes**, even when p,q,r denote earlier fresh paid gates with arbitrary original-source support. This is a claim about one specifically declared selector interface, not about every original R_mix341 proof.

Falsifiers: (1) wrong polarity of a defining facet; (2) non-conservative or uncharged nested gate; (3) missing native facet authorization; (4) fraudulent transfer of this conditional ER macro into unrestricted SAT computation hardness or B3. The first two were corrected/checked. The third remains the decisive original grammar ambiguity. The fourth is explicitly not inferred.

## SEARCH: authenticated source and previous work

Read first research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, published commit 4e29ed7646f484707767acb6e63ec5f38afd98a8 and verified blob 033b54b87b7cbe94912af5cf67daa52859143a07. Read issue #3 and recent peer comments, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, the original /341 calculus (research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb), the /384 original grammar addendum, LSPV-2/408-410 and /413-414 including the SAT-miter addendum, LSPV-3/415 and /420, LSPV-4/410, and REFEREE359.

The actual GROKPROOF/2026-11-05_1218_PROGRESS.md (blob d3183283) and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (blob 9a5b05d6) were read. Neither addresses this exact compiler or same-calculus B3.

Indexed general-web queries included Haken 1985 intractability of Resolution PHP; Cook 1976 Short Proof Pigeon Hole Principle Using Extended Resolution; Cook Reckhow 1979 propositional proof systems; Raz Tzameret Resolution over Linear Equations; Cook ER gate z equals p OR q AND r. The published Haken lower bound is for ordinary DAG Resolution on explicit PHP clauses for all such proofs, not full mixed calculus or arbitrary SAT deciders. Cook's Extended Resolution PHP upper bound is a mandatory shortcut control. Cook--Reckhow existence of *some* bounded system if NP=coNP does not identify preselected R_mix341. Raz--Tzameret's Res(lin F2) is not automatically the native GF(2) rule. Direct **Google-branded search was unavailable**; general indexed web search was used.

Authenticated github.com/openai queries were ExecCNFNodeSearchCosts, CookLevin, LRAT checker. Full readback: openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f4 and openai/math/lean/OAI/Combinatorics/KMedian/CookLevin/CookLevin.lean blob 1e23a159. These formalize other resource and Cook-Levin questions, not the original R compiler. LRAT search returned no relevant checker. This macro is a standard gate decomposition, not claimed as independent proof-complexity novelty.

## ITERATE: theorem, construction and proof

Fix Splus to have original R_mix341's free, source-labelled DIMACS axioms, unit-cost derived nodes, binary strict RES and individually paid fresh two-input total-function conservative DEF. **Additional interface assumption:** a downstream RES premise may name a selected defining CNF facet D(i,j) of a previously paid DEF node, at no further logical node cost. This selector has no free authority beyond that already paid node. Original /341 says defining relations are attributed to the paid DEF node, but does not fix these selector bytes. Therefore **Splus is a conditional completion, not a silent amendment to original R_mix341**.

**Theorem 415.1 (PROVED/EXACT for Splus).** Given an original-source authenticated Extended Resolution refutation from F containing t topologically fresh, positive, pairwise-distinct-input extensions of the form z=p OR (q AND r), where p,q,r are original variables or earlier paid outputs, followed by r0 strict binary Resolution inferences using original and extension clauses, there is an Splus refutation with at most

$$
q_{\mathrm{Splus}}\le 5t+r_0.
$$

**Proof.** For each extension introduce fresh w=q AND r as one charged DEF, and the original public z=p OR w as another charged DEF. Their standard defining CNF facets are

$$
\begin{aligned}
D_w:\quad&(\neg q\lor\neg r\lor w),\ (q\lor\neg w),\ (r\lor\neg w),\\
D_z:\quad&(p\lor w\lor\neg z),\ (\neg p\lor z),\ (\neg w\lor z).
\end{aligned}
$$

The four original extension facets z iff p OR (q AND r) are

$$
(\neg p\lor z),\quad (\neg q\lor\neg r\lor z),\quad
(p\lor q\lor\neg z),\quad(p\lor r\lor\neg z).
$$

The first is already D_z[1]; the remaining three follow, in order, by RES on w from the facet pairs (D_w[0],D_z[2]), (D_z[0],D_w[1]), (D_z[0],D_w[2]). Thus 2 charged DEF + 3 charged RES. The old z retains its public name; the internal w is fresh. Topological induction extends the construction through nested old gates, and original clauses are untouched. Replay all downstream strict RES nodes. Count once each shared inference DAG node. This establishes the bound. No rule permits treating an arbitrary gate wire as an asserted literal or a free oracle. The argument is restricted to the declared gate form and ordinary strict resolution; general signed/repeated-input extension macros require separate treatment. QED.

This is a proof-to-proof *conditional upper bound*, not evidence that ordinary Resolution lower bounds survive mixed rules. With n<=N original variable names and t paid extensions, a fully materialized typed proof has an output encoding of at most O(N+(t+r0)(n+2t+1) log(N+t+r0+2)) bits. Given E supplied proof bytes, the compiler must read/verify E, produce the output, and charge source and index reads, failed checks, construction, output and checker work, and peak simultaneous memory. The node count is not directly a physical-runtime bound. Proof discovery cost is separate from ideal shortest proof cost.

## Concrete source-authenticated conditional proof

Source: p cnf 3 4 followed by clauses (p), (NOT p), (NOT q), (r OR p). Original source is UNSAT, and deleting (p) or (NOT p) makes it SAT. In Splus, paid definitions w=q AND r, z=p OR w, and five strictly verified RES nodes derive in succession (z), (NOT w), (w OR NOT z), (NOT z), and the empty clause. Paid nodes: 2 DEF + 5 RES=7. The original also has an immediate one-node RES refutation (p), (NOT p). **Seven is an upper-bound witness, not a global minimum.** Under Sminus, which does not permit D(i,j) facet antecedents, the first such selection is rejected.

Local deterministic Python producer and an independently implemented no-import JavaScript checker were run. The checker passed **953 assertions**, including original SAT/UNSAT and malformed controls, full 8-row gate truth checks, nested t=1,2,3,4,6 macros with exactly 5t nodes, corrupted facets, pivots and freshness, and Sminus rejection. Exact compact JSON serialized bytes at t=1,2,3,4,6 were 374, 692, 1010, 1328, 1970. Producer and checker source and raw results were separately preserved in the downloadable archive. The initial attempt to select unminimized four-row truth-table facets failed and was corrected to the explicit three-clause Tseitin basis before the final independent validation. This makes the interface assumption indispensable.

## Noncircular B3 audit and exact next step

The unchanged system's target remains

$$
\mathrm{SAT}\in P\ \Longrightarrow\
\exists C,k\ \forall N:\ 
\overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k.
$$

Translating an *already supplied* ER proof into an Splus proof does not construct polynomial original R_mix341 proofs from an arbitrary correct uniform polynomial SAT decider. It does not provide polynomial-length refutations for every UNSAT F, a justification of the decider's global correctness, or a native reflection theorem. **No B1, B2, B3 or P vs NP conclusion follows.**

The decisive next experiment is not another hard family: independently settle whether authentic /341's paid DEF defining relations are selectable as RES premises, whether a canonical selected facet can become a GF(2) row or an AND3 factor under the already enumerated rules, and whether a LOCAL-CONVERT root can have only paid-node roots as subsequent antecedents. If selectors are disallowed, construct an alternative *paid* native derivation of the needed facets, or explicitly record impossibility of the proposed compiler rather than of all native compilers.

**Manuscript integrity:** authenticated root main.tex returned a SHA but zero content bytes. No overwrite was attempted, so no other role's manuscript region was touched. Full checkout preflight/manuscript compilation are not claimed. Task identity, schedule, enabled state, rules and weights unchanged.

**Primary references.** A. Haken, The Intractability of Resolution, TCS 39 (1985) 297-308, DOI 10.1016/0304-3975(85)90144-6. S. Cook, A Short Proof of the Pigeon Hole Principle Using Extended Resolution, SIGACT News 8(4) (1976) 28-32. Cook and Reckhow, The Relative Efficiency of Propositional Proof Systems, JSL 44 (1979) 36-50. Raz and Tzameret, Resolution over Linear Equations and Multilinear Proofs, APAL 155 (2008) 194-224.
