# LSPV-3/470: A linear mixed cut proof with exponentially large exact flat-CNF intermediate rows

**November 7, 2026, 02:24 PST | Route B, LSPV-3 | PROVED/RESTRICTED representation obstruction; COMPUTATIONAL finite source-authenticated fixtures; P versus NP OPEN.**

## IDEA, falsifiers, SEARCH, revision

Initial hypothesis: the established odd-Tseitin strict-3CNF family admits an original-source AND3/GF(2) proof with two complementary high-width cut equations whose individual exact no-auxiliary CNF encodings are exponentially large. A proposed rule-by-rule mixed-to-flat-CNF translation that MUST materialize every intermediate affine row therefore has superpolynomial output cost even for a linear-node source proof. The actual historical byte grammar and a general proof-to-proof lower bound are separate open issues.

Predeclared falsifiers:
1. The row at a cut has a nonzero internal edge surviving cancellation, or complementary sides fail to have opposite RHS.
2. No efficiently constructible cut has linear boundary width on cubic graphs.
3. A smaller CNF using other ORIGINAL edge variables can represent the same cut parity predicate exactly.
4. Native semantic AND3/GF(2) requires unlicensed global entailment, free source normalization, or an implicit multi-premise inference.

The project source LSPV-2/341 establishes the *declared* local AND3 and binary XOR rule and the 4h-1 original-source upper proof. Emdin–Kulikov–Mihajlin–Slezkin (MFCS 2022, DOI 10.4230/LIPIcs.MFCS.2022.47) explicitly proves the standard 2^(b-1) no-auxiliary parity CNF bound, so that general bound is NOT new. This run's restricted increment is a constructive degree-three local-max-cut application and exact two-sided original-source certified rows in the established Tseitin family, with quantified converter overhead, independent replay and compact-resource upper controls. Replaced a tentative expander-only maximum-cut argument by the stronger degree-three local-optimal-cut lemma, which holds for ALL cubic graphs. Four falsifiers fail in the stated, restricted declared-semantic model. Falsifier 4 remains OPEN for historical accepted-byte syntax, which must not be conflated with /341's prose grammar.

## Literature and source search

- Urquhart, **Hard Examples for Resolution**, JACM 34(1):209–219 (1987), DOI 10.1145/7531.8928: exponential ordinary Resolution lower bounds for expander Tseitin instances. This is ordinary shared-DAG Resolution hardness, NOT all-system hardness.
- Emdin et al., **CNF Encodings of Parity**, MFCS 2022, DOI 10.4230/LIPIcs.MFCS.2022.47: exact 2^(b-1) bound without auxiliaries; compact clauses possible with many genuine auxiliaries.
- Ben-Sasson, **Hard examples for the bounded depth Frege proof system**, Computational Complexity 11:109–136 (2002), DOI 10.1007/s00037-002-0172-5: independent model-restricted expander-Tseitin proof-hardness reference, not a result for R_mix341.
- Existing j15marti/pnp material actually read: AGENTS.md blob 19656af1, CODEX.md, research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md blob c3889a3e, original research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex blob c87acd11, LSPV-3/437 blob 7cf00853, LSPV-3/469 blob 2abbf6af, LSPV-1/470 blob 6b762c70, LSPV-5/406 blob 60170059, current issue #3 and root proof1.txt/proof2.txt. Grok's actual GROKPROOF/2026-11-07_0819_PROGRESS.md blob c52f2f67 and Claude's actual research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex blob 79e4d4e7 were inspected.
- Required changed-source review: konard/p-vs-np/proofs/experiments/issue532/ideas/Idea28.md blob cfb3d707 gives Tseitin gate transformations and explicitly leaves ER lower bounds OPEN; konard/p-vs-np/scripts/proof_status.json blob 93b77ed3; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea reports bounded and family-specific findings. None authenticates R_mix341. Consulted meelgroup/frat-xor/format.md blob 986a21aa and tanyongkiam/cake_lpr/README.md blob e94f45e9 (the latter identifies a November 1, 2026 final planned release), useful as external checker/type controls, not interchangeable grammar. Searched github.com/openai/math and related formalization/solver corpora by existing project ledger; no new pertinent native grammar established. Public indexed web research and GitHub connector searches were used. Google-branded search was not independently accessed. Container git/curl DNS failed; direct GitHub connector successfully read and published public code.

## Exact family and published hardness scope

Let G=(V,E) be a finite connected simple bridgeless cubic graph with h even vertices and n=3h/2 edge variables. Choose odd vertex charges chi_v. For each v with incident e1,e2,e3, the four original proper width-three clauses forbid precisely the four local assignments of parity opposite chi_v. Thus F_(G,chi) has m=4h original strict-three clauses and ordinary indexed encoding length N=Theta(h log(h+2)) bits. Summing vertex equations yields 0=1, certifying UNSAT. Even-charge counterparts have exactly 2^(n-h+1) satisfying assignments. For the published expander subfamily, Urquhart's theorem gives 2^(Omega(h)) *ordinary Resolution* size lower bounds. Known controls that avoid Resolution reasoning include source-local AND3/GF(2), extended-resolution definitions, parity-native proof systems, and shared proof DAGs. None is silently removed from the inner W_R minimum.

## Theorem 470.1 (PROVED/RESTRICTED: constructive cubic cut and flat-CNF firewall)

Every such G admits a constructible nontrivial cut S, V\S with boundary B=delta(S) of cardinality b>=h. In the *declared-semantic* R_mix341 grammar of LSPV-2/341, source-labelled original clauses admit a refutation with two separately derived equations

$$
\bigoplus_{e\in B}x_e=\bigoplus_{v\in S}\chi_v,
\qquad
\bigoplus_{e\in B}x_e=\bigoplus_{v\notin S}\chi_v.
$$

Their RHS values differ, so their one binary XOR produces 0=1. The complete proof uses exactly 3h local AND3 inferences and h-1 binary XOR inferences, hence

$$
q=4h-1,\quad D\le 4+\lceil\log_2 h\rceil
$$

with source-independent, paid original-clause dependencies and balanced XOR subtrees. Each *individual equation*, considered as a Boolean predicate on the original edge variables with no additional auxiliary variables, requires at least 2^(b-1)>=2^(h-1) clauses in EVERY exactly equivalent flat CNF. In terms of indexed source bits, this is 2^(Omega(N/log N)). The bound concerns compulsory exact CNFization of an intermediate row, NOT an optimal translated refutation and NOT a lower bound for all mixed DAG proofs.

**Proof of the cut:** Start with any bipartition; if some degree-three vertex has <=1 crossing incident edges, flip its side. This strictly increases the number of crossing edges, so at most |E| improving flips occur. At termination every vertex has >=2 crossing edges. Counting incidences gives 2b>=2h, hence b>=h. A straightforward O(h^2) scanning implementation suffices.

**Proof of local derivations:** At each v, conjoin its four source clauses by THREE binary-antecedent AND3 steps on exactly its original three edge variables. Its eight-entry factor is exactly the affine parity equation. XOR sum the local rows in S and V\S, using balanced binary DAGs. Internal edges appear twice and cancel; crossing edges appear once. Charges on the complementary sides differ since the total charge is odd. Final binary XOR of the two boundary rows yields contradiction. No SPLIT, DISCHARGE, DEF, global entailment oracle, or LOCAL-CONVERT step is introduced.

**Proof of flat-CNF bound:** Fix every original variable outside B arbitrarily; an exactly equivalent CNF still computes the same parity predicate on b boundary bits. Any non-tautological clause implied by a parity predicate must contain all b variables, since otherwise two assignments differing only in a missing variable both falsify it, while exactly one satisfies parity. Consequently each clause can forbid at most one parity-invalid boundary assignment. There are precisely 2^(b-1) such assignments. This is the known parity-CNF lemma applied to a cut row. Extra ORIGINAL variables do not help: fixing them reduces any proposed representation to one of no greater clause count on B.

**Why the tempting transfer fails:** The quantified obstruction is to a translator requiring exact, *no-auxiliary, line-by-line flat-CNF materialization of the cut rows*. It does not rule out converters that eliminate rows before CNFization, retain a factored circuit, introduce legally paid definitions, use GF(2) natively, or rebuild a different proof. On published expander instances, an unrestricted polynomial-size mixed-to-ordinary-Resolution proof translator would contradict Urquhart once the mixed antecedent semantics were rigorously authenticated, but this argument is a proof-system separation, not all-algorithm hardness or B3. Accepted-byte historical authentication [P2-D1] remains OPEN.

## Independent computation and cost ledger

Python constructed exact original-source DIMACS strings, their SHA-256 digests, explicit paid AND3/XOR DAGs, balanced shared-parent references and complementary root rows. An independently written Node.js checker recomputed the original clause lists, all 8-entry factor masks, every GF(2) row, antecedent indices, source ancestry, the contradiction, odd/even model counts, and exhaustive ternary-clause implicates for b<=9. Sixteen mutated witnesses were rejected; 5,749 assertions passed. The two programs did NOT execute the historical native checker. Compact public JS replay independently reproduced all four width/count and both-label figures.

| Graph | h | Original clauses | Cut b | Paid q | Span | Min exact flat CNF clauses per row |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| K4 | 4 | 16 | 4 | 15 | 5 | 8 |
| K3,3 | 6 | 24 | 9 | 23 | 6 | 256 |
| Cube | 8 | 32 | 12 | 31 | 6 | 2,048 |
| Prism6 | 12 | 48 | 18 | 47 | 7 | 131,072 |

Source DIMACS sizes were 163,239,340,540 bytes. Full JSON proof fixtures were 5,975,9,116,12,260,18,743 bytes respectively. The producer's all-phase source enumeration, certificate construction and serialization used 0.45s wall clock and 96,140 KiB maximum resident memory; independent Node checker and corruption replay used 0.072s and 32,940 KiB RSS on the execution host. The ideal q excludes discovery cost deliberately. Balanced row DAGs have O(h log h) explicit sparse variable occurrences and O(h log^2 h) indexed evidence bits; construction, parsing, failed cut flips, all source/index reads, checking, output and live-memory overlap remain real machine work. The flat CNF expansion is NOT paid by the compact proof because it is not performed. These are host resource measurements, not FLMV exponents or same-machine transformation results.

Public compact code: experiments/arc/lspv3_470_cut_parity_compact.cjs. Raw summary: results/raw/arc/2026-11-07_0224_LSPV3_470_CUT_PARITY_SUMMARY.json. Full source-labelled proofs, Python producer, independent Node verifier and SHA manifest are included in the independently archived reproducibility bundle. The compact program reproduces theorem premises and finite controls, not an authoritative historical proof acceptance.

## Tracker effect, scientific status, and next target

Relevant nodes: [P2-D1] OPEN native accepted-byte grammar; [P2-C3] OPEN full-mixed proof translation; [P2-L3-465] earlier constant-section parity blowup; [P2-L3-468] prior characteristic-mismatch proof-system separation; [P2-L3-469] direct same-source GF(2) sparse-PC control; [P2-B1] OPEN all-mixed superpolynomial minimum; [P2-B2] OPEN noncircular B3. The restricted flat-CNF obstruction is evidence [P2-L3-470] attached to [P2-C3]; it does not close any OPEN load-bearing node. proof1.txt is read unchanged. Subsequent coordination issue #3 records the actual tracker write and readback.

Next decisive target: either authenticate one exact accepted-byte historic R_mix341 mixed source proof and extend source-retraction to AND3/LOCAL-CONVERT plus reconvergent paid DEF facets, or produce a genuinely LEGAL mixed proof that falsifies a precisely specified stronger normalization. Retain both shortcut controls and distinction between flat representation size, proof DAG work/span, and physical time/space. P versus NP remains OPEN.
