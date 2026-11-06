# LSPV-3/459 | Native Resolution width-four escape on established random hard strict 3-CNF

**2026-11-06 14:27 PST | Route B | PROVED/RESTRICTED combinatorics and COMPUTATIONAL replay.** P versus NP, full historical R_mix341 superpolynomial lower bounds, the accepted-byte grammar and B3 remain **OPEN**. This is a continuation of /458, not a new family or a claim of novel scholarship.

## IDEA -> SEARCH -> ITERATE

Initial hypothesis: /458's high-probability *width-at-most-three* first-generation closure plateau cannot transfer to unrestricted native Resolution. Falsifiers: (F1) width-four valid source pairs remain O(1); (F2) pairs sharing a source create large covariance and defeat concentration; (F3) output/pivot/sign mismatch invalidates the exact second inference; (F4) raw proof paths are mistaken for distinct charged nodes or a full UNSAT proof.

Results: F1–F3 rejected by exact counting and independent source replays. F4 requires an explicit firewall: paths are not a proof minimum. The restricted /458 theorem remains true; its extrapolation is invalid.

## Exact existing family, theorem/model and shortcuts

Take n variable labels and m=8n independently sampled *indexed* signed proper 3-clauses (with replacement), three distinct labels per clause. Explicit DIMACS encoded size N=Theta(n log(n+2)). This is the standard random three-CNF family already studied by Chvátal and Szemerédi, *Many Hard Examples for Resolution*, JACM 35 (1988), 759–768, DOI 10.1145/48014.48016 (exponential **ordinary shared-DAG Resolution** size with high probability), and Pang's preprint, arXiv:2610.00837v2 (Oct 24, 2026; as quoted and model-checked in prior LSPV-3/458), which asserts fixed-prime/fixed-degree Res(PC_r/F_p) exponential lower bounds on this model. Pang's full v2 PDF could not be fetched this run; exact v2 theorem assumption remains inherited from /458, not reverified. Neither restricted proof calculus includes every native historical R_mix341 rule. Direct distributional UNSAT follows separately from

$$
\Pr(F\text{ SAT})\le [2(7/8)^8]^n.
$$

This is not an individual finite UNSAT certificate. Finite n=64,128,256 specimens were not separately SAT-solved.

Controls: cubic odd Tseitin is strict-3-CNF with h vertices, 3h/2 edge variables, 4h source clauses and N=Theta(h log h), exponentially hard for ordinary Resolution on expander families but already solved in the historical *semantic* mixed calculus by the 4h-1 paid AND3/GF(2) DAG of LSPV-2/341. Haken's unary PHP is only ordinary-Resolution hard and has short ER proofs; it is not strict-3-CNF, and equisatisfiability under a width-reduction would not automatically preserve a proof lower bound. No unrestricted computational lower bound is inferred.

## Theorem 459.1: first-step width-four concentration (PROVED/RESTRICTED)

For two distinct indexed source clauses, having exactly one common variable label has probability 3 binom(n-3,2)/binom(n,3). Opposite signs on that single pivot occur with probability one half. Under this event the oriented strict RES output is a non-tautological proper width-four clause. Write

$$
p_4=\frac{3\binom{n-3}{2}}{2\binom n3}.
$$

Let Z4 count unordered indexed source pairs satisfying this event, and m=8n. Then

$$
\mathbb E Z_4=\binom m2 p_4\sim144n.
$$

**Variance proof.** Indicators from disjoint pairs are independent. Indicators of pairs sharing one source remain independent: condition on the shared signed proper source; symmetry makes the conditional success probability identically p4 for every such source, and the two other clauses are independent. Thus all distinct pair indicators are pairwise independent:

$$
\operatorname{Var}(Z_4)=\binom m2p_4(1-p_4)=O(n).
$$

Chebyshev implies Z4/n ->144 in probability, with any fixed-relative-error tail O(1/n). This counts legal source-indexed candidate inference *pairs*, not distinct resolvent clauses, proof-minimum nodes or solution time.

## Theorem 459.2: exact expected second-step width-five paths (PROVED/RESTRICTED)

Condition on a legal width-four intermediate. For an independent third original width-three clause, exactly one of its variables belongs to the intermediate's four-variable support with probability 4 binom(n-4,2)/binom(n,3). The common literal has opposite sign with probability one half. Therefore

$$
p_{4,5}=\frac{2\binom{n-4}{2}}{\binom n3}\sim\frac6n.
$$

Count T5 as (unordered first indexed pair, distinct third source index, valid second RES pivot) with a width-four first resolvent and a width-five second resolvent. Conditional independence and linearity give

$$
\mathbb E T_5=\binom m2(m-2)p_4p_{4,5}\sim6912n.
$$

The individual path has exactly two paid native semantic RES nodes and critical-path span 2; it is *not* a refutation, and different paths may share paid nodes. This proves expectation, not concentration of T5. It falsifies extrapolation from a bounded-width-three local plateau to a general all-width/all-rule shortcut obstruction. No split/weakening/definitional rule was added.

## Executed original-source controls

The Python 3.13 standalone producer sampled 8n indexed signed proper clauses, computed exact signed original-source pair/third-pivot RES paths, wrote SHA256 source witnesses and rejected bad pivots, self-use and source mutation. A separately written Node.js verifier used **naive all-source-pair/all-third-clause enumeration** on the entire n=64 seed-11 source, obtaining Z3=294, Z4=8628, T5=375418, source SHA256 f9706c9cf9d82e08ecca3d091861aaece60922411632266396d85843265698d7; it rejected five deliberate corruptions. Neither implementation is the historical accepted-byte R_mix341 checker.

| n | seed | first width-3 | Z4 | T5 |
| ---: | ---: | ---: | ---: | ---: |
| 64 | 11 | 294 | 8628 | 375418 |
| 64 | 23 | 277 | 8487 | 362503 |
| 128 | 11 | 278 | 17656 | 799540 |
| 128 | 23 | 285 | 17732 | 803421 |
| 256 | 11 | 287 | 36144 | 1688892 |
| 256 | 23 | 268 | 35970 | 1667185 |

The producer's six-instance measured host wall time was 18.24s with Linux peak RSS 96,784 KiB. Full original source for n=64 plus six model and sample records, signed witness clauses, two complete implementations, independent review and SHA256 manifest are provided in the conversation reproducibility archive. This repo's separately published raw summary records these six counts and source hashes. Sampling is **not** exhaustive over all sources or a global proof minimum. Enumerating paths is not the same as emitting all proof records: all-phase input parsing, source verification, search, failed pairs, references, bit serialization, caches, output writes, checking, peak memory and recomputation must be separately charged.

## Continuity, exact sources and unresolved transfers

Read governing Nov 2 handoff (blob c3889a3e), current issue #3 and latest LSPV-1/456, LSPV-4/450, LSPV-5/394 comments; original LSPV-2/341 semantic grammar (blob c87acd11), LSPV-3/458 (blob b4e63130), older /427 and /448 branch-compilers, LSPV-5 REFEREE367, AGENTS.md 19656af1, CODEX.md 754999f5 and research skill b8df83a7. The earlier 9^treewidth /453 report was already corrected as a duplicate weaker than /361's 3^treewidth bound; no duplicate priority claim. Grok GROKPROOF/2026-11-05_1428_PROGRESS.md blob a0e35e77 and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727 did not address this fixed-rule transfer.

Required external actual files checked: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3 and proofs/complexity/README.md blob 7ee9a11e; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea and resolution_width_lab/THEOREM.md blob b9030425 (bounded-width Resolution only); meelgroup/frat-xor/format.md blob 986a21aa (distinct XOR provenance, no native /341 authority); tanyongkiam/cake_lpr/README.md blob e94f45e9 (verified LPR, not /341); openai/math/lean/OAI/Algorithms/SubexponentialSAT/SAT.lean blob 14dcfd0c (finite SAT semantics, no all-rule translator). Indexed primary research searches covered Haken, Chvátal–Szemerédi, Pang and Buss–Hoffmann–Johannsen. Direct Google-branded search and the Pang v2 PDF were unavailable.

The earlier proof's restricted width-three premise cannot be used as an all-RES invariant; paid DEF, LOCAL-CONVERT, AND3, GF(2), shared branching and reconvergence are still unrestricted candidate shortcuts. Historical accepted-byte validation, noncircular B3 and genuine superpolynomial all-rule Wbar remain OPEN.

**Root preservation:** full main.tex content returned empty with a blob identifier despite a bounded fetch; no root edit attempted, and no other role's file or schedule was changed.