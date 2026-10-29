# LSPV-4 handoff: TREE-AFFINE-COMPOSITION227
Date: 2026-10-29 12:32 America/Los_Angeles
Status: KNOWN THEOREM (2SUBSAT n^{O(e)}), PROVED/EXACT restricted composition, FALSIFIED/RETIRED invalid joins and branch potential, COMPUTATIONAL controls, unrestricted SAT OPEN.

## Adopted known theorem and primary correction
Arvind and Guruswami (IPEC 2021), Theorems 2/17: deterministic n^{O(e)} 2CNF-with-affine-codimension-e solver. Theorem 19: W[1]-hard by parameter e, NOT unconditional non-FPT. Brakensiek, Gopi and Guruswami (arXiv:1902.04740), Algorithm 5.2 pages 38-39, supplies exact GF(2)^e specialization. A direct implementation is in the accompanying reproducer. e=2 is ALREADY a known polynomial case; ARC227's stated e=2 next target should be treated as preexisting literature, not novel.

## Exact composition lemma
Every source clause/equation must be owned exactly once in a polynomially verifiable bag tree; all variable occurrences form connected subtrees; local clauses width <=2 and affine rank <=e_t. Enumerate all 2^{b_t} assignments to FULL shared interface B_t (every variable appearing elsewhere), and query all child subtree tables on intersections. Pinned local solver runs (L_t+1)^{O(e_t)} with row witnesses; gluing justified by running intersection. Charged T_k = D+poly(N)*sum_t 2^{b_t}(L_t+1)^{O(e_t)} and materialized witness table peak S_k=poly(N)+O(sum_t 2^{b_t}(b_t+N)). Polynomial when M,D,L_t poly(N), max b_t <= c log N, and max e_t <=e0 fixed. Arbitrary strict exact22 decomposition discovery not proved.

## Minimal falsifiers
Three-node path bags {x,u}, {u,v}, {x,v}, clauses (x) at first node and (not x) at third, no middle clause. Global UNSAT but unsafe parent-separator joins say SAT; correct running-intersection verifier rejects. Two nodes cannot witness nonconnected occurrences.
Six-variable strict22 cyclic-plus-block formula has 8 clauses, degree 2+2 and primal minimum degree four. A clause-per-bag tree decomposition forces one bag size at least five; in this exact architecture all variables shared so full interface >=5. Both root x0 children retain five distinct source variables, n^2 potential: two child cost 2*25=50>6^2=36. Not a lower bound for all SAT algorithms or all decompositions.

## Machine model
Single controller for both answer classes, with failed routes, child projections, proof acquisition and output materialization charged. Conservative 1-tape read/write simulation from fixed-k read-only-input multitape: T1=O(Tk(N+Sk+log(Tk+2))), P1=O(N+Sk+log(Tk+2)), upper bounds only; two fully writable tapes, RAM and fixed universal machine have independent ledgers. FOUR_PIN226 only source-free future-context model, cannot restrict decision-only compression.

## Finite controls and older ZIP replay
Seed 20261029. Independent local 2SUBSAT vs brute force 2560 (899 SAT,1661 UNSAT); independent tree vs brute force 300 (150 SAT,150 UNSAT); plus explicit two hostile controls. Source ZIPs Polynomial_Coverage_Proof_Study.zip, Adaptive_SAT_Restart_Extension.zip, Adaptive_SAT_Portfolio.zip materialized and replayed. Coverage/adversarial JSON identical. Restart timer/tracemalloc values changed; logical counts unchanged. Pinned control portfolio not all strict22 (only 44/312 strict22 root). User's 16-seed repair-only approach fails on disjoint-products 4/8/16/32, while authenticated component decomposition solves products.

## Repository repair notice
`j15marti/pnp/main.tex` fetched on 2026-10-29 at blob `311c8dd0658759f372c9be9a2065c327fdb1a203`, content exactly `PLACEHOLDER`. No root write made. LSPV-5 retains exclusive recovery ownership. Repo AGENTS.md blob 19656af102604d5f0a721d548cf2e4e72a063561, CODEX.md 754999f50de93cdb693ed37bc8110d31e9e698ef, repo skill b8df83a7b0b1428f349b0e02ce1387d979e8db7f read.

## Next LSPV-4 lemma
For arbitrary strict exact22 instances, construct and authenticate an all-input decomposition into bounded-e 2CNF-affine modules with full shared interface O(log N) in polynomial total time, or isolate a counterfamily FOR THAT EXACT GRAMMAR. P=NP and P!=NP OPEN.