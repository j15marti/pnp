# LSPV-3/496 | Exact ordinary-Resolution collapse of a typed mixed grammar with no RES-to-factor promotion

**November 8, 2026, 02:24 PST | LSPV-3, Route B | PROVED/RESTRICTED; COMPUTATIONAL original-source controls | P versus NP OPEN.**

**Tracked exact IDs:** [P2-D1], [P2-C3], [P2-B1], [P2-B2], [P2-D2], [P2-F13], [P2-L3-477], [P2-L5-412], [P2-L3-492], [P2-L3-495]; related Route A [P1-01], [P1-03], [P1-04] remain OPEN. This report does not change the historical R_mix341 rule set, weights, branch rules or allocations.

## IDEA (before searching): exact proposed typing and four falsifiers

Hypothesis: In a separately specified TAGGED grammar where ordinary RES outputs stay clauses and only original SOURCE factors or earlier AND3 factors may enter AND3, a proper signed strict-3CNF with pairwise distinct unsigned source supports forces every refutation to use RES alone. Therefore the system inherits ordinary Resolution lower bounds on the established Chvatal--Szemeredi random hard family. This is a theorem about a DISTINCT grammar, **not** historical R_mix341.

Falsifiers: **F1**, two different original three-variable supports have union size <=3; **F2**, some authenticated TAGGED rule promotes a derived RES clause into a factor; **F3**, a source or independent root carries an affine row that starts XOR without AND3; **F4**, the cited hard-family distribution has nonnegligible repeated-support probability or lacks the claimed Resolution bound. F1/F3 fail by the support/source-type definitions, F2 is excluded in TAGGED but is demonstrably permitted in a distinct EXTENSIONAL completion, and F4 is checked against the named theorem and elementary collision bound. Do not claim that F2 is excluded by the actual historical grammar, whose accepted bytes remain unresolved.

## SEARCH: verified continuity, hard family, evidence and shortcuts

Both current root trackers were completely fetched before research: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b (18,553 characters); proof2.txt blob d96f6d63680bdd37e619197ddd022f823fa0b4a5 (371,206 characters). Current coordination issue #3, the November 2 governing five-role handoff at commit 4e29ed7646f484707767acb6e63ec5f38afd98a8, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md were read. Root main.tex returned SHA 68188a24badda635a5983fda1c381cdb694fd497 with zero readable characters even for a requested range; no root mutation is safe. This is a retrieval limitation, not an assertion that main.tex is empty.

Relevant same-project work: LSPV-2/341 historical declared calculus (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb); LSPV-5/412 TAGGED/EXTENSIONAL underdetermination (blob b99084b9e1534654207042d00d6645361dfc5863); LSPV-3/477 first-inference obstruction and 54-source/24-live-RES fixture (report and code blob 270822c4365fa9f09ea2e31650fa8031fd5e4b10); LSPV-3/458 local-resolution scarcity (blob b4e63130743bd4b38152b7058e51676805f75201); LSPV-5/428 distinct-support RES-to-affine witness (blob 26322899acf45a3e733f22fdbd702f44ac419b7b); LSPV-3/495 paid CAST3 one-hot shortcut (blob 41176223e63396aade776171a848b127f3536187); LSPV-1/500 growing-local-support transfer (blob 2a53755f9f3843d87a2c593c659ec3d20b131e59); LSPV-5/430 sublinear locality audit (blob 047607272022516f3eec632830be2799d48b6b9f). Existing results /412 and /477 supplied the premise; the **new increment** is the all-derivation closure/equality despite unrestricted RES, plus one exact 2-paid-node typed fork on the same original fixture.

Actual independent critiques read: GROKPROOF/2026-11-08_0930_PROGRESS.md blob e3e8c9657e0f2b2e0751752135cf2558e28183cf; research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex blob 95c2649b29ae7efac79e9400effffd2c3bdeb2fc. External pinned sources checked: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f (finite/model-specific claims, not P-versus-NP proof); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (conditional/family claims); meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (explicit mixed proof interfaces, not historical authority); openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae (research artifacts with verification caveats). Earlier cake_lpr and short-proof paths are documented in /495; no change-aware evidence authenticates native mixed bytes. Indexed web search was used for Pang (arXiv:2610.00837v2), Haken ordinary DAG Resolution, Cook ER and FRAT-XOR; separate Google-branded UI was unavailable.

Primary published source: V. Chvatal and E. Szemeredi, *Many Hard Examples for Resolution*, JACM 35(4):759-768 (1988), DOI 10.1145/48014.48016, at k=3,c=6 and c*2^(-k)=0.75>=0.7. Control: Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (24 October 2026), Thm 7.2(a), a different and stronger specified syntactic system at random 8n signed proper clauses. Haken PHP ordinary Resolution and Cook Extended Resolution remain mandatory nontransfer controls. No theorem here concerns every SAT algorithm.

## ITERATE: precise grammar and theorem

Define one fixed sound, complete, effective, unit-paid system R_tag,0, **distinct from historical R_mix341**. Input is a valid original CNF with free source-labelled clauses. RES accepts any two already available clauses with correctly oriented complementary pivot and emits an ordinary clause of any width (tag RES). Every original SOURCE clause is separately viewable as a Boolean factor on its exact original support (tag SOURCE); a proper three-literal clause has no affine-row annotation. AND3 accepts exactly two **factor-tagged** parents whose combined ORIGINAL support contains at most three variables, emits their exact truth-table conjunction (tag AND3), and may annotate an exactly equivalent affine row only after local exhaustive checking. XOR accepts two already row-bearing parents and computes their GF(2) sum. No implicit promotion from RES clause to factor, no fresh DEF, no LOCAL-CONVERT, no case split/discharge, no other axioms. Proof DAGs may share every valid inference. This is a deliberately restricted, RES-complete typed calculus; no claim is made that its omissions are historical.

**Theorem 496.1 (PROVED/RESTRICTED, exact all-DAG collapse).** For every UNSAT proper strict-3CNF F whose source clauses have pairwise distinct unordered variable triples,

$$
W_{R_{\mathrm{tag},0}}(F)=W_{\mathrm{RES}}(F),
$$

where both minima count distinct unit-paid derived inference nodes in shared DAGs and source clauses are free.

**Proof.** Suppose a legal non-RES derived node exists; take the earliest one topologically. XOR would require an earlier row-bearing node, but no proper three-literal SOURCE is affine and RES emits only clauses. AND3 would require two earlier factor-tagged nodes. Since this is the earliest non-RES node, both must be distinct original SOURCE factors. Their three-element supports are different, hence their union has at least four variables, contradicting the AND3 support restriction. No other non-RES rule exists. Therefore every possible refutation uses RES alone, with no restriction on its width, branching choices, sharing, temporary enlargement or proof order. Conversely every ordinary shared-DAG RES proof is accepted. Both systems are RES-complete and unit-paid, so their attained minima agree. QED.

**Hard-family corollary 496.2 (PROVED/RESTRICTED with published hardness premise).** Sample n-variable, m=6n proper signed three-literal clauses independently with replacement, each unsigned triple uniformly among binom(n,3) and each sign uniformly among eight. The probability of a repeated unsigned triple is at most

$$
\frac{\binom{6n}{2}}{\binom{n}{3}}=O(1/n).
$$

Intersect this high-probability event with Chvatal--Szemeredi's high-probability UNSAT ordinary-Resolution exponential-size event. Then with probability 1-o(1) the stated formula has W_Rtag,0(F)=exp(Omega(n)) (accounting for free sources changes only O(n)). For explicit signed-index encoding N=Theta(n log n), this yields a restricted worst-case exp(Omega(N/log N)) lower bound along unbounded encoded lengths. This is **NOT** a bound on historical R_mix341 because its paid DEF and RES/AND3/LOCAL-CONVERT interfaces are not included, nor B3 or arbitrary-machine work.

**Exact typed counterwitness (EXTENSIONAL versus TAGGED).** Reuse the **original** independently verified 54-clause, 9-variable proper source from /477, which has 54 distinct supports and is UNSAT by all 512 assignments. Zero-based original source IDs:

$$
\begin{aligned}
C_0&=(\neg x_4\lor x_7\lor\neg x_9),\\
C_{10}&=(x_4\lor x_7\lor\neg x_8),\\
C_{44}&=(x_7\lor x_8\lor\neg x_9).
\end{aligned}
$$

One paid correctly oriented RES on x_4 yields R=(x_7 or not x_8 or not x_9). Then one paid AND3, **if and only if RES-produced clause views are admitted as factor inputs**, combines R and C_44 on support {7,8,9}, yielding the exact Boolean factor

$$
R\land C_{44}\equiv (x_7\lor\neg x_9).
$$

TAGGED rejects the second node, EXTENSIONAL accepts. Ordinary RES can derive the same final two-literal clause using a second resolution on x_8, so this witness demonstrates TYPE difference, **not a claimed proof-size separation or unavailable shortcut**. The finite example uses the project's established regression source, not a new allegedly hard problem; its 24-live-RES refutation is an upper bound, not an asymptotic hardness certificate.

## Independent verification and full-resource audit

The GitHub-published JS reuses the exact original /477 fixture and ordinary Resolution derivation, then checks the typed fork with full eight-row truth tables. **2,119 assertions** and six rejected negative controls passed in independent V8 replay of the published content; all 54 original clauses have distinct unsigned supports and all 512 original assignments violate the formula. The original-source ordinary proof has 24 live RES nodes (474 generated before pruning), with a separate two-node RES+AND3 typed witness not part of that refutation. Independent Python source-and-resolution reimplementation performed the same source enumeration, found a contradiction after 474 distinct RES outputs and rejected three orientation controls. This Python checker is independent, **not** the historical verifier. The historical recovered checker supports SOURCE/AND3/XOR only and does not accept this RES witness.

**Logical work:** 24 distinct RES nodes in exhibited live refutation; candidate typed fork has two separate paid inferences; mathematically quantified R_tag,0 minimum may be larger and is not computed for this fixture. **Parallel span:** the reproduced ordinary RES live DAG has sink depth six from original sources under unit-weight, unlimited-processor longest-path model; no span minimum is claimed. **Explicit bits:** new JS code 5,689 ASCII bytes, original /477 full source/proof JSON 11,361 bytes; output/raw JSON separately charged. **Actual executed work:** source parsing, 512 truth assignments, 1,431 unordered source-support pairs, ordinary DP derivation creating 474 nodes, 2,119 JS checks, six rejected hostile witnesses, independent Python replay. **Execution/memory:** full host process time and peak simultaneous memory for the GitHub connector and V8 replay are not separately instrumented; do not infer time/space exponents from logical costs. Any implementation also pays acquisition, full source-header validation, construction, proof indexing, reference reads, memory retention/recomputation, verification, output serialization, GitHub head and source reads, SHA conflict checking, failed attempts and publication. No FLMV inference follows.

The novel exact claim relative to /477 is the RES-closed TAGGED equality, not the already known SOURCE/AND3/XOR first-step barrier. Compared to /500's distinct richer LOCAL feedback calculus, TAGGED excludes the crucial RES->factor promotion and every paid definition: neither system simulates the other by a claimed cost-free identification.

## Publication, governance and remaining gap

Code: experiments/arc/lspv3_496_tagged_res_fork.cjs. Raw: results/raw/arc/2026-11-08_0224_LSPV3_TAGGED_RES_CLOSURE496.json. Handoff: research/coordination/2026-11-08_0224_LSPV3_TAGGED_RES_CLOSURE496_HANDOFF.md. Both root trackers reviewed; a material restricted evidence node belongs only in proof2.txt. No other historical file or role region should be modified.

**Advance:** exact complete-grammar collapse for a well-typed mixed subcalculus; concrete 2-node source-authenticated RES-to-AND3 ambiguity; rigorously scoped published random-family lower-bound corollary. **Still OPEN:** [P2-D1] full historical accepted-byte grammar, [P2-C3] proof-to-proof mixed normalization, [P2-B1] all-historical-rule superpolynomial minimum, [P2-B2] noncircular same-calculus B3. P versus NP OPEN.