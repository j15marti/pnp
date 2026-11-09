# LSPV-3/532: linear refutation of a pinned ternary-path strict 3-CNF

**2026-11-09 04:30 PST | Route B | PROVED/RESTRICTED symbolic + COMPUTATIONAL finite controls. P versus NP OPEN.**

**New node [P2-L3-532].** Refines [P2-L3-529], [P2-L3-530], [P2-D3], and the upper-control requirement of [P2-C3]. Load-bearing historical grammar [P2-D1], full normalization [P2-C3], all-rule superpolynomial minimum [P2-B1], noncircular same-R B3 [P2-B2] OPEN. Companion [P1-01], [P1-03], [P1-04] OPEN.

## IDEA -> SEARCH -> ITERATE

**IDEA.** The previous no-auxiliary exact boundary CNF lower bound of $3^{k+1}$ [P2-L3-530] does not impose exponential logical refutation work when the very same signed modular path is constrained by actual original strict-3CNF boundary pins. Predict a linear-size, entirely source-authenticated ordinary Resolution certificate, with no free unit axioms, extension definitions, oracle calls or branch discharge.

**Predeclared falsifiers:** (F1) pins cannot be derived from original proper three-literal sources; (F2) an incorrect pivot, parent direction, tautology, omission or illegal source breaks the refutation; (F3) the source is SAT or the final forbidden tuple is not original; (F4) the exact source-checked linear certificate was already published here, requiring a narrowed claim. F1-F3 are rejected by proof and two independent checkers; F4 narrows the result to an **explicit charged pinned strict-3CNF upper control**, not novelty of bounded-treewidth tractability. A preliminary generator mistakenly rejected duplicated common literals in valid resolvents; it was corrected to set-union with tautology rejection and retested.

**SEARCH and authenticated continuity.** Read both full trackers and current issue #3, the Nov. 2 governing handoff, repository AGENTS.md/CODEX.md/skill, LSPV-3/529 and /530, peer LSPV-1/533 and LSPV-5/458, older native accepted-subgrammar LSPV-3/491; actual Grok file GROKPROOF/2026-11-08_1130_PROGRESS.md (blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70) and Claude file research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex (blob 79e4d4e7e0e3edff3aba8610852c45534bdde128). External required sources: konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and RESOLUTION_STANDARD.md blob 729a9164d6aad2dc7ae49fb24127759859a60f11. FRAT-XOR format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f; cake_lpr README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c; short-proof README.md blob 93d2090dba9739bc4983c65ea639a24e1f5e0fab; openai/math README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. No new universal theorem asserted. General web search, not a separate Google-branded search, accessed primary Urquhart (1987), de Colnet-Mengel (2021/2022) and the Cai-Li arXiv:2610.02047 (Oct. 2026) bounded-weighted-incidence-treewidth preprint.

## Theorem 532.1 (PROVED/RESTRICTED)

For every integer $k\ge1$, use the existing [P2-L3-529] signed cubic modular-three **path** with $k$ vertices, $k-1$ internal groups $I_0,\ldots,I_{k-2}$, and $k+2$ boundary groups $B_0,\ldots,B_{k+1}$. Each group $e$ consists of three original Boolean indicators $x_{e,0},x_{e,1},x_{e,2}$ with an original positive ALO clause.

Each internal group has incidence sign +1 at its left vertex and -1 at its right; boundary signs are +1. Every vertex has charge zero and all **18** original wrong-charge signed triples:
$$
\neg x_{e_1,a}\lor\neg x_{e_2,b}\lor\neg x_{e_3,c},
\qquad
\epsilon_1 a+\epsilon_2 b+\epsilon_3 c\not\equiv0\pmod3.
$$
There are exactly $20k+1$ original proper strict-3CNF clauses before pins. The unpinned path is SAT, and its full boundary relation has an exponential no-auxiliary flat-CNF representation minimum [P2-L3-530].

Pin every $B_j$ to value zero except $B_{k+1}$ to value one. To derive each required positive indicator $p_j=x_{B_j,a_j}$, introduce two globally fresh **original source** variables $u_j,v_j$ and four signed original proper width-three clauses:
$$
(p_j\lor u_j\lor v_j),\quad (p_j\lor u_j\lor\neg v_j),\quad
(p_j\lor\neg u_j\lor v_j),\quad (p_j\lor\neg u_j\lor\neg v_j).
$$
These are neither unit assumptions nor uncharged DEF facets. Resolving on $v_j$ twice and then $u_j$ once derives $p_j$ with three paid RES steps.

The total signed **original strict 3-CNF source** has
$$
\boxed{m=24k+9\text{ clauses},\qquad n=8k+7\text{ variables}.}
$$

At each of the first $k-1$ vertices two positive input indicators are already available (the left boundary pair initially, then the previous internal unit and the next boundary unit). Exactly two of three outgoing edge candidates have wrong local charge. Each is forbidden by an **original** ternary clause. Resolve each such original clause against the two positive input indicators (2 RES steps per wrong candidate), obtaining two negative candidate units. Resolve both negatives against the original outgoing ALO clause (2 more RES steps), obtaining the correct positive internal state. Six steps per nonterminal vertex.

The final vertex has three positive pinned or propagated indicators whose signed charge is one, so its original forbidden triple exists. Three Resolution inferences derive the empty clause. All intermediate units are globally unconditional original-source consequences, so the DAG needs no new case-split rule, no hidden AND obligation and no branch-local assumption leakage.

Consequently the *exhibited* certificate has exactly
$$
\boxed{W_{\mathrm{exhibited}}(k)=3(k+2)+6(k-1)+3=9k+3}
$$
distinct unit-paid RES inferences, $18k+6$ explicit premise references, and ideal unit-weight unlimited-parallel dependency depth $4k+1$. It is a constructive **upper bound, not a minimum**. Signed IDs and all literal occurrences use $O(\log k)$ bits, yielding source plus proof evidence $O(k\log k)$ bits. An implemented materialized generator, verifier and source ledger have polynomial bit-complexity, store $O(k\log k)$ bits and charge input parsing, output, graph construction, references and verification. They do not claim FLMV same-machine contraction.

## COMPUTATIONAL checks and resource ledger

A standalone original-source JS generator was run for $k=1,2,3,4,5,8,12$. A separately authored Python verifier reconstructed the entire exact signed original source independently, checked every signed RES pivot and clause, source ancestor, monotone DAG ID, terminal empty clause and malformed/corrupt reference control. A second compact JS generator was executed separately in V8 and independently replayed every refutation. All seven controls passed.

| k | source clauses | paid RES | premise refs | span | source ancestors |
|---:|---:|---:|---:|---:|---:|
| 1 | 33 | 12 | 24 | 5 | 13 |
| 2 | 57 | 21 | 42 | 9 | 20 |
| 3 | 81 | 30 | 60 | 13 | 27 |
| 4 | 105 | 39 | 78 | 17 | 34 |
| 5 | 129 | 48 | 96 | 21 | 41 |
| 8 | 201 | 75 | 150 | 33 | 62 |
| 12 | 297 | 111 | 222 | 49 | 90 |

**42** deliberately malformed or corrupted certificates rejected. **Seven explicit SAT source-deletion witnesses** independently checked: remove only the first ternary facet of the final pin, set all edge groups one-hot at zero, and final-pin gadget $u=v=0$. Every remaining original clause is satisfied. This shows a genuine source-critical facet, not a bogus proof of contradiction from already-unsound premises.

Host measured Node $k=12$: 0.02 s elapsed, 24,052 KiB peak RSS; Python seven-case verifier: 0.65 s elapsed, 96,800 KiB peak RSS. Both measurements include host/runtime overhead and are not Turing-machine lower bounds. Independently serialized full certificate at $k=12$ is 23,413 JSON bytes. Source+certificate size bound $O(k\log k)$ is asymptotic; explicit node work, evidence bits, depth, materialized storage and actual construction time remain distinct.

## Established-family ledger and transfer

**Urquhart (1987), JACM 34:209-219, DOI 10.1145/7531.8928:** exponential ordinary-DAG-Resolution lower bounds for expander Tseitin, not for every mixed or arbitrary algorithm. **de Colnet and Mengel (2021/2022):** regular-resolution bounded-degree Tseitin length characterized by treewidth (up to stated factors), a model-specific known upper control. **Cai-Li (2026), arXiv:2610.02047:** bounded weighted incidence treewidth positive Resolution upper bounds (preprint, assumptions retained). **Pang (2026), arXiv:2610.00837v2:** opposite-characteristic fixed-degree polynomial-resolution hard modulo-three expander families under its hypotheses; no transfer to full historical mixed R. This run's bounded-path family is **not** such an expander-hard family. The change from full unpinned boundary relation to source-pinned contradiction is explicit.

**Remaining transfer**: [P2-D1] accepted-byte native LOCAL-CONVERT / DEF facets / Resolution / GF(2) grammar; [P2-C3] simulation for *all* legal proof DAGs; [P2-B1] superpolynomial optimum over all legal rules; [P2-B2] noncircular same-calculus SAT-in-P bridge. No superpolynomial work or P-vs-NP result follows.

**Publication artifacts:** code experiments/arc/lspv3_532_pinned_ternary_path_linear.cjs; raw results results/raw/arc/2026-11-09_0430_LSPV3_PINNED_TERNARY_PATH532_RAW.json; five-role handoff research/coordination/2026-11-09_0430_LSPV3_PINNED_PATH532_FIVE_ROLE_HANDOFF.md. This run read both trackers in full; proof1 initial blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; proof2 initial blob d07c7427eb8035b4bf968aa6cea29320bd30a214. Update [P2-L3-532] only with current complete blob and SHA and verify readback. Do not alter main.tex without complete ownership-safe bytes. Historical rules, weights, agents, two Route A/three Route B allocation, titles, schedules and enabled states unchanged. P versus NP OPEN.

