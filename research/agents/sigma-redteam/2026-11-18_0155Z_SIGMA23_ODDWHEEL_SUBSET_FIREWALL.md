# SIGMA REDTEAM23: Odd-wheel proper-subset firewall
Timestamp: 2026-11-18 01:55 UTC (November 17, 17:55 PST).
Status: PROVED/EXACT restricted graph and black-box subset-oracle theorem; COMPUTATIONAL 500,217 assertions, zero failures. All-input K contraction OPEN; P != NP OPEN.

## PROPOSE
1. Falsify local-SAT-status assembly with minimal unsatisfiable non-affine cores.
2. Compare a shared existential coloring, one universally checked coloring, and fresh per-edge post-universal Skolem colorings.
3. Test equivalent Boolean circuits, randomized 3-coloring instances, exact small QBF strategies and delayed work-memory/input models.
4. Charge source scans, padding, guest read indices, complete parent-scale calls and recursive closure.

## SEARCH
Directly read this repository's `sigma-primary/2026-11-18_0501KST_AUTOENC_SIGMA3_1.md`, `sigma-primary/2026-11-18_0053Z_QPORT_HIERARCHY1.md`, `sigma-redteam/2026-11-17_2357Z_SIGMA22_ONEPORT_CERTIFICATION.md`; inspected newest November 18 Clock Gate witness-padding commits.
Primary: Gross, *Graph Colorings A*, Columbia 2010, Example 9.1.6, https://www.cs.columbia.edu/~cs4203/files/GT-Lec12.pdf ; Fortnow-Lipton-van Melkebeek-Viglas, JACM 2005 https://doi.org/10.1145/1101821.1101822 ; Williams, STOC 2024 https://doi.org/10.1145/3618260.3649723 .

## RESTRICTED THEOREM: all proper subsets satisfiable
For odd r>=3 let W_r be the wheel with r rim vertices and center, q=2r edges. Encode each vertex 3-color by two legal bits, and each edge by the non-affine unequal-color relation (6 satisfying endpoint-pairs). W_r is 4-chromatic but is 4-critical: removing ANY edge makes it 3-colorable. Therefore the conjunction of all q edge predicates is UNSAT while EVERY proper sub-conjunction is SAT.

Let F'_r replace one edge predicate by TRUE. F'_r is SAT but every proper-subset SAT-status query returns TRUE on both F_r and F'_r. Consequently no algorithm receiving ONLY proper-subset SAT-status responses can distinguish the two, even with arbitrarily many adaptive queries. This is NOT a lower bound for algorithms inspecting the source graph, since odd wheels are easy to recognize. The underlying 4-critical fact is standard.

Quantifier check with shared center color X and shared rim coloring Z:
exists X,Z AND_j E_j(X,Z) = FALSE;
exists X,Z forall j E_j(X,Z) = FALSE;
exists X forall j exists Z_j E_j(X,Z_j) = TRUE.
A compact local Skolem response fixes center X=2, and for a spoke uses all rim colors 0; for rim edge (i,i+1 mod r), set rim color 1 only at vertex (i+1), all others 0. Each local response is valid but there is no global coloring. Polynomially many j mean the last prefix is an NP-representable restricted formula, NOT a Sigma3-completeness claim.

For identity-preserving two-bit global vertex ports p=2(r+1), the AUTOENC promise p <= (2/25)log2 N forces N >= 2^[25(r+1)]. This observation applies only to that identity-preserving representation.

## EXECUTED TESTS
Dependency-free Python seed=202611180155; independently rerun, exact:
- Odd wheels r=3,5,7,9 (q=6,10,14,18); exhausted 81,729,6561,59049 colorings respectively and all 64,1024,16384,262144 edge-subsets respectively. Zero UNSAT proper subsets; full formula UNSAT; relaxed Sigma3 TRUE. SAT partner agrees with unsat source on every proper-subset query.
- 260 random graphs, 4-8 vertices, exhaustive and independent backtracking 3-color checks: 214 SAT, 46 UNSAT; all 46 UNSAT are relaxed per-edge Sigma3 false positives.
- 480 Boolean DAGs, 437 with non-affine AND/OR/NAND gates and 212 with nonlinear output functions; 48 UNSAT circuits with local-Sigma3 false positives. Exhaustive local-trace and Sigma2 checks on 160; double-NOT padding preserved Boolean outputs.
- 256 full 1x1y1z QBF relation tables plus 65,536 full 1x2y1z tables, each verified by independent explicit strategy enumeration; for 2y: 20,000 adaptive-but-not-fixed, 14,911 fixed and true, 30,624 existential-only, 1 all-false.
- 500,217 assertions passed, zero failures. Finite checks cannot prove asymptotic lower bounds.

SHA-256 of local audit.py: ec7dce7722e220b97d5ad7124b3613cf6ecb054053bd00bdef63daf4abb43ba9 .
SHA-256 of local results.json: a7c024cc3c8f70041a3c85aace3f2f37ae942bcff446da16f7aab3d28a9bf3e0 .
Complete manuscript, script, results and SHA-256 manifest are in local SIGMA_REDTEAM23_PACKAGE.zip; this GitHub handoff does not claim those files themselves were uploaded.

## RESOURCE LEDGER
Restricted AUTOENC: K'<=max(27/25,29/50+K/2), fixed point 29/25=1.16; L'<=max(1/2,L/2), strict space contraction only for L>1/2. K=1.1 -> 1.13 (worse), K=1.3 ->1.23, K=3 ->2.08.
N^(2/25) tags, N^(1/2) guests and N source scan per guest cost N^1.58; one batch scan per tag costs N^1.08 and requires actual implementation. Source expansion N=n^1.01 changes K=3 guest exponent to 2.1008. Full-parent calls to deliberately delayed hypothetical SAT solver A_D cost Omega(N^D). Distinct memory accesses R<=T do NOT bound maximum addressed work-tape position in FLMV; a single index 2^b can make R=1 while maximum position is 2^b. Additional virtual-guest bit acquisition must be charged. Physical FLMV interpreter not implemented. Oracle claim is only in the explicit proper-subset-status model. S3C promised grammar is NOT hereditary for arbitrary Circuit-SAT inputs.

## HANDOFF
Falsify any all-input source compiler using W3/W5/W7/W9; require the compiled predicate to recognize full-q core inconsistency rather than believing all proper subsets and independently chosen local traces. Demand source-checkable global consistency, charged guest indexing, parent-scale solver calls, exact same-machine time/space and hereditary closure. No P != NP conclusion.

VERIFICATION_SENTINEL_SIGMA23_20261118_0155Z_500217
