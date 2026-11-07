# LSPV-1/464 | Literal-alias conservative padding is inert for ordinary shared-DAG Resolution

**2026-11-06 America/Los_Angeles (PST) | Route B lead | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

Affected shared proof-chain node: **[P2-B8] (new restricted evidence)**. Read full current proof1.txt (blob 27e11e225417ec3d0a2adad510ffec35406845c1) and proof2.txt (blob 8cb09888b7537d127a371f4c1381211c12dd79bb) before this iteration. Reviewed [P1-01], [P1-03], [P1-X3], [P2-D1], [P2-D2], [P2-B1], [P2-B2], [P2-B7], [P2-C1], [P2-C3], [P2-F2], [P2-F8]. All load-bearing nodes remain OPEN.

## IDEA -> falsifiers -> SEARCH -> ITERATE

**Hypothesis (before searching):** LSPV-1/463's disjoint satisfiable padding theorem extends to a _shared-original-variable_ conservative gadget when its auxiliary variables admit a globally consistent section assigning each auxiliary a signed original literal or a constant. Prediction: every source-authenticated ordinary Resolution proof DAG of F AND G projects to an F-only DAG using no more paid inference nodes. This is a theorem about source projection, NOT a purported full mixed-calculus normalization.

Four falsifiers: (1) after aliasing two variables, a Resolution inference on an aliased pivot becomes illegal; (2) a tautological substituted premise yields an essential non-tautological conclusion with no legal smaller surviving parent; (3) reconvergence forces a paid shared ancestor to be duplicated; (4) a G source clause survives after the alleged total section or a SAT source changes truth value. All four were checked in the symbolic proof and local finite controls.

**SEARCH:** Project duplicate review found LSPV-1/463 (disjoint SAT padding), LSPV-3/409 (conditional bit-normalization/B3), LSPV-5/317 (D_A proof-system simulation), LSPV-5/340, /343 (reflection and source-retraction firewalls), LSPV-5/367 (context-typed shared RES equivalence), LSPV-3/463 (one split source-only native RES discharge), and LSPV-3/457 (source-ancestry bound). These do NOT establish the specific shared-original-variable literal-section equality below. The new result is a natural extension of the standard Resolution restriction/subsumption argument, NOT a claim of mathematical novelty beyond the project.

Read governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, issue #3 including current peer updates, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md; actual GROKPROOF/2026-11-06_2316_PROGRESS.md and research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex. The GitHub-owned root main.tex was NOT edited because a complete safe owned-region readback and current ownership marker were not established.

External actual files read: konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (checked finite-machine scope only); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and README.md blob f397a7747eaca82df3d754d0a4b4bab1fe10f814 (bounded/promise claims, not general P/NP); meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (explicit XOR authentication); tanyongkiam/cake_lpr/README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c (certified LPR checker with exact format); openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae and lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f44ad49370d1b812e862c03c3a91d7f836 (machine work and memory are explicit, not a native proof compiler). General indexed web queries: Cook-Reckhow proof-system boundedness, Atserias-Müller Resolution automatization, proof restriction under literal substitutions, and Raz-Tzameret linear-equation Resolution. Google-specific access was not used. No repository is treated as a P-versus-NP solution.

## Theorem 464.1: shared-input literal-section padding

Let F be any UNSAT CNF over original variables X. Let G be a CNF over X union Y, Y disjoint from X. Assume there exists one globally consistent substitution sigma with sigma(x)=x for x in X and, for every y in Y, sigma(y) belongs to {0,1,x_i,NOT x_i : x_i in X}, such that **every clause** of sigma(G) is a Boolean tautology. Equivalently G(x,sigma(x)) is true for **every** original assignment x, including ones falsifying F. No per-instance oracle or assignment-dependent choice is allowed.

Let S_RES(H) denote the minimum number of distinct paid binary Resolution inference nodes in any source-authenticated unrestricted shared refutation DAG of H, with free authentic source clauses and no weakening/definition/GF(2)/oracle rules. Then

$$
\boxed{S_{\mathrm{RES}}(F\land G)=S_{\mathrm{RES}}(F).}
$$

**Proof.** Ignoring G gives the <= direction. For the reverse, take an arbitrary Resolution DAG pi refuting F AND G, including all sharing and arbitrary pivots. Process it topologically **once**. Each clause C has its Boolean literal substitution sigma(C), simplified by deleting false constants, deduplicating literals, and marking the result TOP when true constant or opposite literals occur. Maintain either TOP or an already derived non-tautological clause D contained in sigma(C). Every F source remains itself; every G source becomes TOP.

For an inference C=Res_p(A,B), where A has p and B has NOT p, consider sigma(C).
* If sigma(C)=TOP, output TOP and pay no new node.
* If sigma(C) is not TOP and one parent image is TOP, its complementary pair can only use the substituted pivot, since any complementary pair not involving that pivot would remain in sigma(C). The OTHER parent image is a subclause of sigma(C), so keep its derived subclause without paying.
* If both parent images are non-TOP, their maintained derived subclauses either omit one required complementary pivot (then keep that parent, which is already a subclause of sigma(C)), or retain both pivot signs. In the latter case resolve the two maintained clauses on the substituted pivot. The resolvent is non-tautological and contained in sigma(C). If sigma(p) is a constant, one of the first cases applies.

This is the standard subclause-preserving restriction/substitution repair. One output is associated with each OLD DAG node, so identical ancestors and joins remain shared. Each old paid inference produces **at most one** new paid binary Resolution inference. The final empty clause maps to empty, which cannot be TOP, and is derived from F sources only. Thus S_RES(F) <= S_RES(F AND G); equality follows. QED.

The claim applies to signed aliases and shared original variables, not only disjoint satisfiable padding. It does **not** extend by this proof to a general nonlinear Skolem section y=f(X): inlining arbitrary circuits is a separate rule-specific proof simulation with real size and bit costs. Nor is it a proof that the fixed historical R_mix341, Extended Resolution, GF(2), LOCAL-CONVERT, or mixed assumption discharge is substitution-stable.

## Published-family control and exact finite certificate

Use odd-charge cubic Tseitin. For connected cubic graph on h vertices, one edge bit per edge (3h/2 original variables) and four signed proper 3-clauses forbidding the incorrect parity at each vertex gives 4h original 3-clauses and Theta(h log h) explicit binary-indexed source bits. When vertex charges sum to one mod 2 the conjunction is UNSAT. Urquhart (1987) and Ben-Sasson-Wigderson (2001) establish exponential ordinary shared-DAG Resolution lower bounds on **suitable expanding** cubic graph sequences. The four-vertex K4 test below is only a finite UNSAT control; it has no individually certified asymptotic hardness.

For K4 with six edge variables and charges (1,0,0,0), construct the exact 16 original signed 3-clauses. Enumerating all 64 assignments verifies UNSAT. A source-indexed Davis-Putnam Resolution DAG has 31 paid nodes. Choose a source clause C containing signed literal l, introduce a fresh y and the two conservative alias source clauses (NOT y OR l) and (y OR NOT l). Derive C'=(C minus l) OR y, then rederive C from C' by two correctly oriented paid Resolution steps. Route one used original source leaf through the two paid steps. The resulting refutation has 33 paid nodes and genuinely cites the shared-variable G source; literal substitution y=l erases these two detour nodes and reconstructs the original 31-node F-only DAG with source indices and signed pivots intact.

An independent Python generator exhaustively checked 5,292 source-compatible non-tautological local Resolution substitutions over three variables, including both signed literal aliases and constant sections: 1,302 parent-1 repairs, 1,302 parent-2 repairs, 1,752 one-resolution repairs and 936 tautological targets. Source SHA-256 in the generator's declared signed line serialization is 34ab5803fdd2e53200195c719932845ba626351cea7118ad241a5cfa8f967189.

A second, independently implemented Node.js checker rebuilt the K4 and both DAGs and ran the same 5,292 local tests. It passed 12,941 assertions and rejected 2 deliberate invalid-reference controls. **Finite results are COMPUTATIONAL**, not a certificate accepted by the historical mixed checker.

Measured execution: Python 0.021 s, peak 96,524 KiB RSS; Node 0.07 s, 34,160 KiB maximum RSS. These are actual host measurements, not machine-independent SAT lower bounds. The ideal logical minimum excludes search deliberately. The constructed 33-node upper bound charges proof construction, parser, sources, references, transformations, output and verification when used as an actual algorithm. The raw work count and explicit certificate bits are different quantities.

## Proof-chain implications and open arrows

[P2-B8] records this stronger **ordinary-Resolution-only** padding firewall. It strengthens the previous [P2-B7] disjoint padding result but does not establish historical rule closure or any full-mixed lower bound. It warns that a fixed-input rejecting trace or literal-alias circuit does not by itself furnish an original-source contradiction in Resolution. The full Rmix341 historical byte grammar [P2-D1], all-mixed superpolynomial [P2-B1], and weakest noncircular B3 [P2-B2] remain OPEN. Neither a polynomial-time SAT decision algorithm nor its formal correctness has been constructed.

Next falsifier: exhibit a legal historical R_mix341 GF(2), AND3, LOCAL-CONVERT or paid DEF inference that invalidates literal-section non-expansive projection; alternatively prove a native rule-by-rule simulation with complete original-source provenance and exact serialization. This work does not edit the historical calculus, weights, any agent identity, task or schedule. P versus NP OPEN.

## Primary sources

1. A. Urquhart. Hard Examples for Resolution. *JACM* 34(1):209–219, 1987. DOI 10.1145/7531.8928.
2. E. Ben-Sasson and A. Wigderson. Short Proofs are Narrow: Resolution Made Simple. *JACM* 48(2):149–169, 2001. DOI 10.1145/375827.375835.
3. S. Cook and R. Reckhow. The Relative Efficiency of Propositional Proof Systems. *JSL* 44(1):36–50, 1979. DOI 10.2307/2273702.
4. A. Atserias and M. Müller. Automating Resolution is NP-Hard. arXiv:1904.02991, 2019.
5. R. Raz and I. Tzameret. Resolution over Linear Equations and Multilinear Proofs. *Annals of Pure and Applied Logic*, 2008.

END_OF_VERIFIED_REPORT
