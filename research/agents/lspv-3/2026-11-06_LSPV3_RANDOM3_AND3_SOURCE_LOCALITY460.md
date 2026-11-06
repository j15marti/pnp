# LSPV-3/460 | Native AND3 initial-source scarcity on a published hard random 3-CNF family

**2026-11-06 PST | Route B | PROVED/RESTRICTED analytic theorem; COMPUTATIONAL finite controls | P versus NP OPEN.** The current result is *not* a full R_mix341 lower bound.

## Hypothesis and four falsifiers

Hypothesis: The published random 8n proper signed 3-CNF family almost surely has no two original clauses on the same three **original variables**, so historical source-support-three AND3 cannot directly merge two distinct source clauses. Falsifiers: (F1) such collisions have nonvanishing probability (refuted symbolically); (F2) one proper 3-clause can yield a nontrivial condition on fewer original variables by LOCAL-CONVERT (refuted); (F3) wide RES, paid DEF, later derived local factors and shared proofs can bypass this local restriction (**yes**, so no unrestricted claim); (F4) a PRNG makes collisions spuriously frequent (**yes** initially: a xorshift32 low-bit generator was rejected and replaced by SHA256-counter; both raw results are preserved).

## Published-family ledger and formal model

For n variables sample 8n source clauses independently with replacement. Each selects an unordered three-element set T uniformly from [n], and independent fair literal signs. All clauses are strict proper signed 3-CNF; standard indexed bit length N=Theta(n log n). Chvatal and Szemeredi, *Many hard examples for resolution*, JACM 35(4) (1988), DOI 10.1145/48014.48016, establish high-probability UNSAT and exponential **ordinary shared-DAG Resolution** size for their random k-CNF with c*2^(-k)>=0.7 (including c=8,k=3). Pang, arXiv:2610.00837v2 (2026), reports further fixed-degree Res(PC_r/F_p) lower bounds, but no general extension predicate rules. These do NOT establish full mixed R_mix341 hardness; sampled deterministic test sources are not separately UNSAT-certified.

Mandatory known-method controls: Urquhart 1987 and Ben-Sasson--Wigderson 2001 cubic-expander odd Tseitin strict 3-CNFs have exponential **ordinary Resolution** size, but each of the h vertices has FOUR clauses on one original triple and the existing LSPV-2/341 historical semantic AND3/GF(2) construction attains an exactly 4h-1-node mixed refutation. Haken unary PHP is Resolution-hard, Cook extended Resolution gives polynomial PHP proofs, and 3-CNF lower-bound preservation needs actual reverse simulation. Braun, arXiv:2609.23015v2, proves a DAG Res(XOR) lower bound for wide bit-PHP, not for arbitrary conservative paid DEF; LSPV-1/457 only supplies bidirectional ER splitter transport in a *separate* grammar.

## Theorem 460.1 (exact source-triple collision count)

Let Z_n count indexed unordered pairs of original clauses with identical three-variable supports. Each of the M=binom(n,3) triples is uniform and independent, giving

$$
\mathbb E Z_n=\frac{\binom{8n}{2}}{\binom n3}
=\frac{24(8n-1)}{(n-1)(n-2)}
=\frac{192}{n}+O(n^{-2}).
$$

By Markov,

$$
\Pr(Z_n>0)\le\mathbb E Z_n=O(1/n).
$$

For 8n<=M the exact no-collision probability is the product over j=0,...,8n-1 of (1-j/M). Thus with probability 1-O(1/n), each original proper ternary clause has a distinct original-variable triple.

## Theorem 460.2 (local-only closure)

Restrict the *unaltered* historical semantic grammar to original-source clauses, native AND3 combining two conditions on a union of at most three **original** variables, and source-implied LOCAL-CONVERT outputs on at most three original coordinates; forbid RES, DEF, assumed SPLIT/DISCHARGE, unlicensed affine axioms and semantic oracles in THIS restricted analysis.

A proper signed 3-clause C holds at exactly seven of its eight local assignments. Any non-tautological Boolean consequence D of C depending on at most three original variables can be false only on the unique local assignment falsifying C. If D omitted even one of C's three coordinates, flipping that missing coordinate would produce a C-satisfying assignment still falsifying D. Hence D necessarily depends on all three C coordinates, and with at most three support positions D is exactly equivalent to C. Every other implication is tautological.

When no two original source variable triples coincide, nontrivial factors derived separately from two original clauses have combined original-variable support at least four. AND3 cannot join them; tautological outputs add no semantic strength. Induction over arbitrary acyclic shared local-only proof DAGs shows every nontrivial conclusion is semantically equivalent to one original clause. Thus this fragment cannot produce a nontrivial affine equation or contradiction. Source sharing, reconvergence and free after-the-fact proof choice do not change this restricted conclusion. HOWEVER native unrestricted RES readily creates width-four first-generation clauses (prior LSPV-3/459 proves ~144n expected source pairs), while paid DEF and later derived local factors are further escapes; no all-rule Wbar_R or B3 follows.

## Computational execution and adversarial controls

Python generator and independent Node verifier were run on 16 deterministic SHA256-counter seeded sources: n=256,512,2048,8192 with seeds 11,23,47,89. Original signed DIMACS SHA256 hashes and all candidate-pair counts were independently reconstructed. IID theory expectations for one sample are respectively 0.75850, 0.37712, 0.09388, 0.02345. Observed counts: (0,0,2,1); (0,0,0,1); (0,0,0,0); (0,0,0,0).

Initial xorshift32 modulo-power-of-two tests produced n=8192 counts (0,2,2,2), inconsistent with the IID prediction. This failed generator was rejected, its raw results retained; SHA256-counter pseudorandomness is STILL not an iid proof. Four-facet source-parity control checked all eight truth rows and three native AND3 conjunctions yielding x1 XOR x2 XOR x3 = 1; a source-duplication mutation changed pair count by exactly original triple multiplicity. Independent Node replay: **1,421,493 assertion groups PASS** and four intentional corruptions rejected (SHA, pair count, parity facet, missing fixture). The checker is NOT the authoritative historical R_mix341 accepted-byte checker. Sampled formulas were not individually UNSAT certified.

Measured host producer: 2.76 sec / 122,996 KiB peak RSS; Node verifier: 6.65 sec / 159,680 KiB peak RSS. Generation, indexing, source hashes, reads, failed RNG, construction, verification, serialization, caches, retrieval and peak simultaneously live memory all cost actual machine resources; these measurements are not same-machine FLMV exponents or a lower bound on full proof work.

## Source and duplication audit

Reviewed original LSPV-2/341 blob c87acd11, governing November 2 handoff blob c3889a3e, LSPV-3/438 (already proves high-width parity cut projection and exponential flat-clausal encoding, so it is NOT claimed here), /448-/449 and /458-/459, peer LSPV-1/423,/457 and LSPV-2/422, AGENTS.md, CODEX.md and repo research skill, current issue #3, actual Grok GROKPROOF/2026-11-06_1617_PROGRESS.md blob b931933c and Claude ONETAPE-0001 blob 9a5b05d6. Actual outside file reads: konard/p-vs-np scripts/proof_status.json blob 93b77ed3; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea and resolution_width_lab/THEOREM.md blob b9030425; meelgroup/frat-xor format.md blob 986a21aa; tanyongkiam/cake_lpr README.md blob e94f45e9; peitl/short-proof README.md blob 93d2090d; openai/math README.md blob cc5b0a03. Primary literature searched using indexed web; no direct Google-branded search or third-party formal proof replay claimed.

**OPEN:** historical authoritative accepted-byte LOCAL-CONVERT/DEF/private-exported-port contract, polynomial source-preserving normalization of ALL mixed proofs or legal counterexample, full mixed superpolynomial Wbar_R lower bound, and separate noncircular same-R B3. Root main.tex returned a current SHA but zero readable bytes; unchanged to preserve ownership. All five roles, two Route A/three Route B, fixed historical weights, schedules and identities unchanged. P versus NP OPEN.

Full runnable producer, independent verifier, complete corrected and rejected raw JSON, measured host logs and SHA256 manifest are in the user-facing reproducibility archive.