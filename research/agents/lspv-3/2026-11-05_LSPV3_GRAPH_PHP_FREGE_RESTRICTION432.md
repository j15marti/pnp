# LSPV-3/432: graph-PHP Frege restriction upper bound and exact Resolution transport

**2026-11-05, America/Los_Angeles. Route B.** **PROVED/RESTRICTED:** substitution theorem for Frege and strict-resolution restriction transport, both standard proof-theory principles, applied to existing graph PHP. **KNOWN:** Buss polynomial Frege/Cook polynomial ER pigeonhole proofs and published exponential Resolution hard sparse expander graph-PHP. **COMPUTATIONAL:** 2,401 independent finite proof replays. **OPEN:** native R_mix341 complete paid-DEF/facet export semantics, same-fixed-calculus p-simulation and B3, full-mixed worst-case superpolynomial bound, P versus NP.

## IDEA, SEARCH, ITERATE

Hypothesis: every graph-PHP source, including graphs hard for ordinary Resolution, admits a polynomial Frege/ER refutation because a standard complete-PHP proof can be specialized by setting missing edges false. A *native* R_mix341 consequence requires a separate exact source-authenticated ER-to-Rmix341 compiler. Falsifiers: (1) restricted complete axioms do not exactly equal graph-PHP source clauses, (2) a strict-RES restriction proof needs an unlicensed weakening step, (3) a satisfiable restricted source is incorrectly accepted, (4) paid-DEF facets are assumed public without native authorization, (5) a published expander theorem is incorrectly stated for directly width-three graphs.

Recovered original LSPV-2/341 and LSPV-3/384 Hall-to-PHP upper, /426 alias counterexample, /427 branch lift, /430 essential-source theorem, /431 path restriction, the governing five-role handoff, issue #3, AGENTS.md, CODEX.md and research skill. Read Grok 2026-11-05 12:18 progress, Claude TPORT-0002, primary Buss (1987), Cook (1976), Haken (1985), de Rezende et al. (CCC 2020), Mikša/Nordström (JACM 2024) and Kiesl et al. (JAR 2020). Reviewed konard/p-vs-np README blob 0e0ec77f, blkph0x/p-vs-np-proof-research README blob f397a774, and FRAT-XOR format.md blob 986a21aa; no external native Rmix341 compiler emerged. Indexed web was used; no Google-branded session or third-party solver execution is claimed. Duplication audit: the Hall-ER case and path direction firewall were already in /384 and /431. The contribution of this note is the uniform Frege-substitution scope and independent full finite restriction replay; no mathematical novelty is asserted.

## Exact source family and proved model

Let G=(P,H,E) be bipartite, with P={0,...,h} and H={0,...,h-1}; source variable x_{p,j} exists precisely for an edge. The basic graph-PHP formula is

$$
F_G=\bigwedge_{p\in P}\left(\bigvee_{j\in N(p)} x_{p,j}\right)\wedge\bigwedge_{j\in H}\bigwedge_{p<q:\,j\in N(p)\cap N(q)}(\neg x_{p,j}\vee\neg x_{q,j}).
$$

It is UNSAT by h+1>h. Left degree at most 3 gives directly a CNF with width at most 3, |E|<=3(h+1), m=(h+1)+sum_j binom(deg_H(j),2)=O(h^2) original clauses and O(h^2 log(h+2)) signed-index bits. The cited sparse-expander lower bounds concern exact specified graph models and proof systems; this report does NOT claim its arbitrary finite degree-three graphs are expander-hard or that the published constructions all have left degree three.

**Theorem 432.1 (known Frege substitution closure; all sizes).** Let CompletePHP_h be the basic complete bipartite PHP with h+1 pigeons and h holes. Uniformly substitute false for every missing-edge variable and retain all present-edge variables. Each complete positive pigeon source restricts to the *exact* sparse pigeon source. Each complete negative collision involving a missing edge becomes true; every other collision is exactly a sparse source. Therefore

$$
\mathrm{CompletePHP}_h\big|_{\rho_G}=F_G.
$$

By Buss's polynomial Frege proof of negated CompletePHP_h and substitution closure of every fixed Frege system, apply rho_G to each proof line and simplify constants. This yields a Frege proof of NOT F_G with polynomial length and polynomial construction work. Standard ER p-simulation of Frege yields polynomial ER refutations, all in polynomial h and hence polynomial binary source length. This is an upper-proof theorem, not an unrestricted SAT time lower bound and NOT an authenticated Rmix341 certificate.

**Conditional same-R implication.** If the original, unchanged R_mix341 has a *uniform polynomial, source-authenticated* p-simulation of the required ER proofs, including individually selectable conservative paid-definition facets and legally reusable RES premises, then W_Rmix341(F_G)<=poly(|encode(F_G)|) for *every* graph-PHP. Prior /384 invoked this facet assumption; later peer reviews continue to find the historical DEF/LOCAL export contract underdetermined. Do not assume the compiler. A global polynomial upper would eliminate this family as a superpolynomial mixed minimum-hard target, not establish B3.

**Theorem 432.2 (classical strict-Resolution restriction; checked).** Every q-inference exact binary-RES refutation pi of F and partial Boolean assignment rho yields an original-source-identified binary-RES refutation of F|rho with at most q inferences, without weakening. Inductively carry a *subclause* of each restricted unsatisfied proof line. If both current parents still have complementary pivot, resolve. If fixing the pivot or previous strengthening removes a pivot, reuse a suitably stronger parent. If a parent becomes satisfied by a non-pivot literal, the original resolvent also becomes satisfied. The empty target remains empty. Shared DAG nodes count once and redundant nodes may be pruned. Thus L_RES(F|rho)<=L_RES(F). This is an UPPER-bound direction, never a way to transport a lower bound from complete PHP to its sparse restriction. Project /431 provides the sharp opposite-direction falsifier: the full PHP is exponentially RES-hard yet a degree-two path restriction has exact 2h paid mixed/RES nodes.

## Independent finite experiment, model and cost limits

A no-import Python producer generated a 43-paid binary-RES refutation of complete PHP(4,3), starting from 22 exact signed source clauses on 12 variables. It then restricted the *same* proof to ALL 7^4=2,401 four-pigeon/three-hole graphs with nonempty pigeon neighborhoods. Every reconstructed sparse original was UNSAT, every transported proof used only correctly oriented native RES, and costs after DAG pruning were 2..43 paid nodes. An independent no-producer-import JavaScript checker rebuilt each source and proof from scratch and reproduced the entire 31-bin paid-node histogram. **307,807 independently evaluated assertions passed; three deliberate bad-source, bad-pivot and missing-goal mutations were rejected.** A compact self-contained independent reproducer was also run with **217,891 checks passed**. Detailed seven-case source/graph certificates and full histogram are in the local reproducibility bundle; the committed raw summary reports exact aggregates. Finite proof sizes are upper bounds from one choice of original proof, NOT exact global minima.

Machine resource firewall: logical unique-node count, weighted critical-path depth, explicit bitstring lengths, construction/search, parsing, source/index/head reads, proof checking, output, failed policy attempts, retention, recomputation and all-phase peak writable space are separate. No claim of native random-access FLMV time-space savings is inferred. The ideal W_R allows free choice of optimal legal DAG, which can only lower its value. New extension gates or case-split rules are not silently added. Shared lemmas require discharged or justified contexts.

## Next obligation

Authenticate and replay a genuine historical R_mix341 paid-DEF/facet-to-RES interface on a specialized published PHP certificate, including degenerate gates after substitutions and exact source-identity reference. If a proposed checker completion differs from the original grammar, mark it a different calculus. Independently ask whether any published 3-CNF family resists *all* already legal mixed shortcuts. Route A remains a distinct all-input solver-transform question. Full native normalization, superpolynomial mixed Wbar, noncircular same-R B3 and P versus NP OPEN.

### Primary references

1. Buss SR. Polynomial size proofs of the propositional pigeonhole principle. J Symbolic Logic. 1987;52:916-927. DOI 10.2307/2273826.
2. Cook SA. A short proof of the pigeon hole principle using extended resolution. SIGACT News. 1976;8(4):28-32. DOI 10.1145/1008335.1008338.
3. Haken A. The intractability of resolution. Theor Comput Sci. 1985;39:297-308.
4. de Rezende SF, Nordström J, Risse K, Sokolov D. Exponential Resolution Lower Bounds for Weak Pigeonhole Principle and Perfect Matching Formulas over Sparse Graphs. CCC 2020, article 28. DOI 10.4230/LIPIcs.CCC.2020.28.
5. Mikša M, Nordström J. A Generalized Method for Proving Polynomial Calculus Degree Lower Bounds. J ACM. 2024;71(6):37. DOI 10.1145/3675668.
6. Kiesl B et al. Simulating Strong Practical Proof Systems with Extended Resolution. J Autom Reason. 2020;64:1247-1267.
