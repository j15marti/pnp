# LSPV-1/485: Syntactic two-way nonlinear-gate transfer (reconciliation of LSPV-4/370 and LSPV-1/484)
**2026-11-07 11:58 PST | Route B | PROVED/RESTRICTED composition; COMPUTATIONAL finite controls. P versus NP OPEN.**

**Exact nodes:** materially sharpens [P2-F13] using [P2-L2-371] and [P2-F9]. The historical [P2-D1], [P2-C3], [P2-B1] and [P2-B2] remain OPEN. No modification to roles, weights, grammar, schedules or agent allocation.

## IDEA -> SEARCH -> ITERATE
**Hypothesis:** LSPV-1/484 provided explicitly SYNTACTIC Res(XOR) affine Booleanity and assumption discharge, but used a $4^g$ gate partition. The PRIOR LSPV-4/370 had already proved $2^g$ affine specialization while relying on an earlier conditional source-guard account. Combining the prior gate lemma with the /484 syntactic guard repair yields the stronger $2^g$ syntactic translation for their common, explicitly restricted typed grammar.

**Four falsifiers:** F1 some two-input Boolean truth table cannot become affine after fixing only one input; F2 reconvergent/shared gates require fixing both affine inputs; F3 complementary one-input affine guards cannot be discharged using the target's NATIVE syntactic rules; F4 an authentic historical uncharged private/exported LOCAL port bypasses the three-exposed-wire restriction. F1 is excluded by the ANF identity below, F2 by the original topological LSPV-4/370 proof, F3 by /484 and the new finite source-authenticated certificate, while F4 is OPEN.

**Repository/literature search actually performed:** Both root trackers read in full; current coordination issue #3 and peer comments; governing Nov 2 five-role handoff; AGENTS.md, CODEX.md, repository skill; actual original LSPV-2/341 grammar at blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb; LSPV-2/371 blob 92fc7f8e88a0beec38d0c2e6a6fe5ce2d3de6585; LSPV-4/370 blob b9a18082c1c58d1b0c360042e9ef2482a44b11ce; LSPV-1/484 blob 64962f90c6093aaea5917659aed1c38e12489373; LSPV-3/480 blob 2ca529700c03fc0a0baed8219db7ec428fc660d9. Actual Grok file GROKPROOF/2026-11-07_1815_PROGRESS.md blob 0532370c9bf99b1204be4e0efd9ef96290454ec7; actual Claude file research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67.

Required repository change-aware rechecks: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f; tanyongkiam/cake_lpr/README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c; openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. External method indexes, checker formats and repo labels are not proof of a native historical R_mix341 rule. A distinct Google-branded search front end was unavailable; ordinary indexed web search and the primary HTML paper were used. No PDF was analyzed.

**Important duplication finding:** LSPV-4/370 (November 3, 2026) ALREADY proves the $2^g$ two-input affine-partition theorem. The advance here is its integration with the more recent charged syntactic assumption-guard derivation, not rediscovery of the partition.

## Scoped transfer theorem
Use precisely the DISTINCT typed source-authenticated R_loc3,DEF2 model in LSPV-1/484: original signed strict 3-CNF clauses, paid RES and GF(2), globally fresh conservative acyclic paid binary DEF gates, and paid AND3/LOCAL steps exposing only up to three affine forms without hidden or free ports. No new rule is introduced into historical R_mix341. Assume /484's stated per-primitive syntactic bounded-interface replay lemma, which has not been implemented for ALL native historical rules.

For any original UNSAT F with n original variables, m source clauses, and a legally authenticated q-distinct-paid-node proof in this typed fragment containing g genuinely NONAFFINE binary DEF gates, there is a syntactic shared-DAG Res(XOR) refutation of the SAME original source of size

$$
\boxed{S_{\mathrm{syn\,Res}(\oplus_2)}(F)\le C(n+1)2^g(m+q+1),}
$$

with fixed C determined by the grammar. This is a PROOF-OUTPUT-EXISTENCE bound, not actual SAT search runtime or whole-R_mix341 cost.

**Proof:** Every binary Boolean truth function has unique form
$$
f(u,v)=c\oplus\alpha u\oplus\beta v\oplus\gamma uv,\quad
c,\alpha,\beta,\gamma\in\{0,1\}.
$$
When $\gamma=0$, no gate split is needed. Otherwise, given current affine inputs A(X), B(X), split ONLY on A=0 and A=1. In a child A=a, the gate output is the affine expression
$$
f(a,B)=c\oplus\alpha a\oplus(\beta\oplus a)B.
$$
Topological substitution, including shared and reconvergent named wires, keeps every gate output affine on each consistent cell. There are at most $2^g$ cells. Replay the original proof with these annotations using the SAME /484 charged syntactic local-rank-3 compiler. Its derivation of affine Booleanity $B(A)=(A=0)\lor(A=1)$ uses $O(n)$ native Res(XOR) proof lines, not a free semantic assumption. Context guards are explicit disjunctions of OPPOSITE affine branch assignments; both complementary children are mandatory and are joined using paid linear-combination and false-constant deletion steps. Sharing is charged once within each leaf proof, and a total of at most $2^g-1$ joins is needed. Combining with /484's per-cell node bound gives the claim. Note that the untested full historical grammar may have legal operations violating the bounded-interface premise. QED conditional on that already stated typed-local replay lemma.

## Established published 3-SAT family and quantitative consequence
Pang, A Degree–Size Relation for Resolution over Polynomials, arXiv:2610.00837v2 (24 October 2026), §1 and Theorem 7.2(a), https://arxiv.org/html/2610.00837v2, proves in the cited preprint that random proper signed 3-CNF $\mathcal F(n,3,8n)$ with n variables and m=8n clauses sampled independently with replacement from $8\binom n3$ possible signed clauses requires, with probability $1-o(1)$, $\exp(\kappa n)$ nodes in EVERY shared-DAG syntactic Res(XOR) refutation for some $\kappa>0$. The binary source length is $N=\Theta(n\log n)$. The original source is already strict 3-CNF; no lower-bound-preserving 3-CNF reduction is assumed. The result concerns proof-system size, not certified named finite instances or all-machine SAT hardness. The present run does not independently replay Pang's asymptotic proof.

For these sources, any q-node proof in the stated typed mixed grammar satisfies
$$
\boxed{g\ln2+\ln\big(C(n+1)(8n+q+1)\big)\ge\kappa n.}
$$
If q is polynomial, $g\ge(\kappa/\ln2)n-O(\ln n)$. This sharpens /484's $\ln4$ coefficient by factor two but still gives ONLY an $\Omega(n)$ required nonlinear-gate count, compatible with polynomial q. If $g=o(n)$ then q must be exponential in this restricted typed model. Native odd-Tseitin GF(2), Haken Resolution and Cook Extended Resolution remain obligatory shortcut controls. No universal mixed lower bound is inferred.

## Executed certificate, adversarial controls, resources
The published executable experiments/arc/lspv1_485_twobranch_syntactic.cjs (blob 9067b858c43f58d537ec5855cf72b8512e3c44db) was fetched back from GitHub and independently replayed in V8, producing 470 syntactic records with 5,649 total assertions, all 16 binary truth tables, an explicit Booleanity derivation for affine mask 43, TWO complete branch guards, one paid complementary join, and six deliberately corrupted certificate rejections. Its original source is the 16-clause odd-K4 proper signed 3-CNF, not an auxiliary unsound axiom. Exhaustive even-charge control has 8 models, odd has 0. Nodes use SOURCE, BOOL, WEAK, LIN and DROP native syntactic Res(XOR) steps. This is NOT an execution of the historical /341 checker, and it does NOT implement the full symbolic mixed-proof compiler.

A distinct extended local Node v22.16.0 verifier produced 21,648 checks on 45 seeded shared-gate DAGs, independent AND gate leaf counts 2/4/8/16 for g=1/2/3/4, and the same source-authenticated 470-node two-branch DAG with six rejected corruptions. This local code is NOT claimed byte-identical to the shorter published V8 artifact. Raw data records that distinction.

Charge q once per source-calculus distinct paid node. The syntactic target certificate charges every branch-local application, reference, Booleanity, weakening, guard, source clause and join; shared proof nodes are not duplicated WITHIN each leaf. The ideal weighted critical path, proof-size total, serialized evidence bits and an implementable schedule are different objectives. Actual algorithm runtime includes original-source/index/head reads, preprocessing including any allocate-then-free memory, proof discovery/failures, mask computation, Gaussian elimination, branch construction, retrieval/recomputation, serialization/output and verification. Streamed output time is at least output bits, and peak simultaneous machine space requires a separate measurement. In Route A notation $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$; no bound here proves same-machine FLMV recursion or a SAT algorithm.

## Remaining barriers and scientific status
[P2-D1] authenticated complete historical grammar including RES/LOCAL/private/exported wires; [P2-C3] all-legal-rule original-source normalization or legal counterexample; [P2-B1] superpolynomial worst-case minimum over ALL historic mixed rules; [P2-B2] noncircular SAT-in-P to polynomial same-R refutation bound. ALL OPEN. Main.tex was not modified because a complete owner-safe reconciliation was not established; no unauthorized manuscript changes. P versus NP OPEN.

## References
[1] Shuo Pang (2026), A Degree–Size Relation for Resolution over Polynomials, arXiv:2610.00837v2, Theorem 7.2(a).
[2] LSPV-4/370, research/agents/lspv-4/2026-11-03_1436_LSPV-4_AFFINE_BINARY_FACTOR370.tex.
[3] LSPV-1/484, research/agents/lspv-1/2026-11-07_1141_LSPV1_SYNTACTIC_AFFINE_GUARD484.md.
[4] LSPV-3/480, research/agents/lspv-3/2026-11-07_1134_LSPV3_OR_PORT_PROJECTION_FIREWALL480.md.
