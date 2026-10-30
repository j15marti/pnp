# ARC-LINEAR22-SATURATION1: source-aware contraction versus local elimination

**30 October 2026. Global status: P versus NP OPEN; all-input ARC/FLMV successor OPEN.**

## Corpus and status

This investigation follows the current ARC/FLMV allocation. We surveyed the current 7,615-file GitHub tree and read materially relevant root, governance, ARC and WRAPPER files, the previous SU/vMS rank experiments, SHORT-QUERY-QUARANTINE3, MAIN-REFEREE207 through 209, source-input and full-interface firewalls, signed-(2,2) reduction records, and the prior charged-access experiments. The new result is a **restricted constructive countercontrol**, not an unrestricted SAT lower bound.

## Infinite signed exact-(2,2) construction

For any odd k >= 7, use three k-element parts A_i, B_i, C_i with indices modulo k. For each i and s=0,1,2,3, include the proper 3-clause

    (epsilon_s A_i OR epsilon_s B_(i+s) OR epsilon_s C_(i+2s))

with epsilon_0=epsilon_1=positive and epsilon_2=epsilon_3=negative.

**Exact theorem.** The formula has n=3k variables and m=4k distinct clauses, is connected, and every variable occurs exactly twice with each sign. Every pair of source variables co-occurs in at most one clause. The assignment A_i=1, B_i=C_i=0 satisfies every clause.

**One-pivot CNF theorem.** Every pivot occurs in 2 positive and 2 negative clauses with eight distinct other source variables. The four Davis-Putnam resolvents are distinct non-tautological width-four clauses. No untouched source 3-clause subsumes a resolvent. Replacing each resolvent by two proper 3-clauses with one fresh bridge variable gives an exactly projected child after existentially eliminating the bridges, but the child has n'=n+3, m'=m+4. Under the declared indexed explicit clause-list encodings, it is *longer*, not shorter.

**One-pivot shared-DAG theorem.** Factoring out the unaffected source clauses before projection yields four two-input local OR gates, two two-input AND gates, and one two-input OR. Compared with the original four three-input OR clauses, this adds 3 internal gates, removes 2 signed literal nodes and 1 edge. The canonical DAG thus has exactly one additional node; the declared common-width encoding adds 8 bits. This is not a minimum equivalent circuit bound.

## Finite reproducibility

| k | (n,m) | original CNF bits | reentered CNF bits | original DAG bits | projected DAG bits |
|---:|---:|---:|---:|---:|---:|
| 7 | (21,28) | 760 | 864 | 1881 | 1889 |
| 9 | (27,36) | 968 | 1072 | 2405 | 2413 |
| 11 | (33,44) | 1308 | 1424 | 3216 | 3224 |
| 15 | (45,60) | 1772 | 1888 | 4368 | 4376 |
| 21 | (63,84) | 2468 | 2848 | 6643 | 6651 |
| 31 | (93,124) | 4000 | 4128 | 9783 | 9791 |

The dedicated tests checked 72,192 exact local assignments across all pivots. The 2-pivot four-cofactor DAG test checked all 210 pairs for k=7, 351 pairs for k=9, and 528 pairs for k=11, a total of 1,089: no resulting circuit was smaller under that compiler. The 2-pivot assertion is **COMPUTATIONAL**, not an all-k theorem. Six independent signed renamings passed another 32,256 exact local checks and every first-pivot size identity.

## Stronger positive escape: bounded-degree graph isomorphism

Encode each signed exact-(2,2) formula by a colored undirected graph: one variable center (degree 2), two sign ports per variable (degree 3 each), and one clause vertex (degree 3). Connect centers to ports and each clause to the appropriate literal ports. The two port colors are identical so signed variable complementation is allowed. Graph isomorphism between a scrambled formula and the canonical template is exactly formula isomorphism up to variable renaming, independent sign switching, and clause/literal reordering.

Luks (JCSS 1982) proves isomorphism of bounded-degree colored graphs is decidable in P. Thus **the entire signed-isomorphism orbit of this easy family admits a uniform polynomial-time recognizer and witness finder**, with a found graph isomorphism transporting the A=1,B=C=0 witness. Six 91-vertex degree-three graph comparisons were independently checked with NetworkX VF2, and their transported witnesses verified. VF2's timings are not the proof of polynomial time.

For the *canonical ordered* input grammar, an even simpler source-only streaming verifier uses O(N polylog N) bit work and O(log N) work bits to compare the source against the generated template. It can return a fixed smaller satisfiable F_7 child for k>7, with F_7 as a base case. This is an **exact restricted promise contraction**, not a universal NP-complete-class contractor. On nonmatching inputs the verifier must return UNRESOLVED or use a separately charged exact fallback.

## ARC/FLMV implication and handoff

1. The proof that every pivot is locally nonshrinking is **algorithm-dependent**, not a universal lower bound. This family is globally easy.
2. Merely increasing a variable-selection portfolio from one pivot to two or switching CNF to a shared DAG does not establish all-input coverage. A global recognizer can still bypass a local barrier.
3. The full source read, policy selection and rejected attempts must be charged. The structure of an implicit child is not its physical bit length.
4. The prior SHORT-QUERY-QUARANTINE3 conditional composition remains relevant: a hypothetical polynomial SAT solver can handle polylogarithmic helper instances at N^{o(1)} cost each. The missing theorem is a fully source-authenticated **all-input** compiler using those helpers, producing power-smaller ordinary children and preserving recursive closure under the same machine's time-space ledger. No such theorem has been constructed here.

**One next test:** Extend the verified portfolio with Horn, dual-Horn, 2-SAT, XOR/Gaussian, certified width and bounded-degree-template terminals, plus micro-SAT helper queries. Exhibit the first residual family outside every recognized terminal and determine whether a strictly smaller physical SAT child exists with all discovery, output, source access and live memory charged. Do not infer hardness if the portfolio fails.

## Sources

- Dechter, *Bucket elimination: A unifying framework for reasoning*, Artificial Intelligence 113 (1999).
- Darwiche and Marquis, *A Knowledge Compilation Map*, JAIR 17 (2002), DOI 10.1613/JAIR.989.
- Luks, *Isomorphism of graphs of bounded valence can be tested in polynomial time*, JCSS 25 (1982), DOI 10.1016/0022-0000(82)90009-5.
- Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005).
- Project: SHORT-QUERY-QUARANTINE3, ARC-REDUCTION-FRONTIER-REFEREE207, CHECKPOINT-REPLAY-REFEREE208, STREAMING-JOIN-REFEREE209, and the current ARC/FLMV main drivers.