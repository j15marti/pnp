# LSPV-3 HEAVY-FIRST CERT PEBBLING169 | 29 October 2026 16:24 PDT

**Status:** RESTRICTED PROVED/EXACT modulo independent referee, COMPUTATIONAL controls, P vs NP OPEN.

The full 6-page mathematical proof, Python 192+40-source reproducibility suite, independent checker, raw JSON, and plot exist as an archived local ZIP. This GitHub PUBLIC proof and compact public code are smaller standalone counterparts; **do not claim the complete local script or PDF is synchronized**. All code and data status is explicit.

## Exact role-to-role theorem

For a fully explicitly encoded, source-authenticated, verified binary tree of CNF module bags with running intersection, maximum bag size w and m polynomially bounded nodes, heavy-subtree-first evaluation and **on-demand** subtree-size recomputation retain at most 1+floor(log2 m) complete result tables of <=2^w bits each, with O(1) transient tables. Conservative indexed-RAM decision T <= D(N)+O(m^3+m2^w poly(N)); work bits O(2^w log(m+1)+(w+log m)log N+log^2 m). For w=O(log N), polynomial same-run T and S. One controller handles SAT and UNSAT, no answer bit: SAT uses recomputation plus original-clause witness verification; UNSAT uses source-authenticated exact-table transcript with independent recomputation. No claim of universal ordinary Resolution proofs. Integer polynomial-VALUE rank Phi=u(C+1)+r applies only after verified polynomial-chunk bounds.

Comb first strict token crossing at m=5: left-first 3 registers, heavy-first 2. For right-heavy comb m=2h+1: R_left=h+1, R_heavy=2; slopes 1/2 and 0 as m tends to infinity. Balanced tree m=2^(h+1)-1 yields R=h+1. These are scheduling controls, not all-algorithm lower bounds. Existing Sethi-Ullman/pebbling methods are the mathematical antecedent, and Elberfeld et al. FOCS 2010 gives stronger known fixed-width logspace methods.

## Evidence and precise limitations

Complete dependency-free Python seed 1691029: 192 small truth-table and memo comparisons (96 SAT, 96 UNSAT; 96 witnesses), 40 larger memo comparisons, 15-node UNSAT table transcript replay and four corrupted-certificate rejections. Full raw SHA256 859ea81655c5d165645beed3e23470155a6d0ba44e5f302cc890869a45394c12. **These tested formulas are ordinary CNF, not strict signed exact22**. All input discovery, candidate failures, local joins, source bits, physical head transport and output are accounted separately.

Root main.tex currently blob f34568e380028a26eb309d269c40d37dc460b8db, 15,543 characters, containing ONE BEGIN LSPV-1 OWNED and NO balanced END/BEGIN markers for other roles. **LSPV-3 did not edit it. LSPV-5 must recover root from verified snapshots**. GitHub code paths, reference SHA and citations are in the theorem file.

Next LSPV-3 lemma: polynomial recognition and certified total live information for an **unbounded-treewidth connected strict exact(2,2)-3CNF** subclass with sound answer-preserving compact moving summaries, or a connected hostile source falsifying one precise compiler. No universal SAT contraction / P=NP / P!=NP proof.

No schedule/task/role changes.
