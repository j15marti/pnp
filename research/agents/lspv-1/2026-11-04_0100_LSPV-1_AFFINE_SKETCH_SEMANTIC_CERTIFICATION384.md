# LSPV-1/384: Rank-One Affine-Sketch Semantic Certification Barrier

November 4, 2026, 01:00 PST (America/Los_Angeles).
Status: **PROVED/EXACT (restricted elementary complexity reduction, independently implemented finite controls; specialist review pending)**; **KNOWN THEOREM** CNF-UNSAT coNP-completeness and general Boolean-circuit equivalence barrier; **COMPUTATIONAL** 285 finite instances; **OPEN** B1/B2/B3, full mixed calculus minimum, P versus NP. This is not a new general proof-complexity lower bound.

## 1. Recover the established hard input before discussing transfer

Haken (1985, *The Intractability of Resolution*, TCS 39:297–308) shows constants $c>0,h_0$ such that **for every** $h\ge h_0$, **every** ordinary unrestricted *shared-DAG Resolution* refutation of the standard *unary* pigeonhole CNF $P_h=\mathrm{PHP}(h+1,h)$ has at least $2^{ch}$ proof lines. Its signed source has $h(h+1)$ variables, $(h+1)+h\binom{h+1}{2}$ initial clauses, and explicit binary-indexed signed CNF encoding length $N_h=\Theta(h^3\log(h+2))$ bits. This is a **restricted proof-system** bound, not a time lower bound for arbitrary uniform SAT deciders. Extended Resolution has polynomial pigeonhole proofs (Cook 1976; Cook--Reckhow 1979). Unrestricted Res$(\oplus)$ results, where cited by other project roles, also require their own exact proof system and encoding. Odd Tseitin has a paid GF(2) escape in the **unchanged** combined $R_{\mathrm{mix341}}$, so algebraic shortcuts remain mandatory hostile controls.

The project fixes original signed CNF source clauses at weight zero and distinct authenticated at-most-binary-premise RES, AND3, GF(2), justified LOCAL-CONVERT and conservative two-input DEF inference nodes at unit weight. Full LOCAL-CONVERT payload and public-interface syntax is still unresolved. None of the definitions or weights of $R_{\mathrm{mix341}}$ are changed here. For every valid UNSAT CNF $F$, $W_R(F)$ is the minimum unit-weight source-authenticated shared refutation DAG cost; $\overline W_R(N)$ is the maximum $W_R(F)$ over valid UNSAT input strings of length at most $N$, empty maximum zero. Discovery of the minimizing DAG is separate from its cost.

B1 is $\forall A\,\exists p_A\,\forall F\in\mathrm{UNSAT}: W_R(F)\le p_A(|\mathrm{enc}(F)|+T_A(F))$; B2 is $\forall A\,\exists p_A\,\forall N:\overline W_R(N)\le p_A(N+T_A^{\mathrm{wc}}(N))$ for one fixed total correct all-binary-input decider $A$; B3 is $(\mathrm{SAT}\in P)\Rightarrow \overline W_R(N)=N^{O(1)}$ for the **same fixed R**. All three remain **OPEN**, including for this run.

## 2. Exact target and three principal falsifiers

Fix a standard explicitly serialized, acyclic, bounded-fanin Boolean circuit $C(u)$, with $B$ independent boundary bits $u\in\{0,1\}^B$, and a supplied $k\times B$ affine sketch $L(u)=Mu+c$ over GF(2). Let

$$
\mathrm{FACTOR}(C,L)\ \Longleftrightarrow\
\forall u,v\in\{0,1\}^B,\quad L(u)=L(v)\implies C(u)=C(v).
$$

This is equivalent to the existence of a total $f:\{0,1\}^k\to\{0,1\}$ with $C=f\circ L$. The public output is one bit; multiple outputs only strengthen the requirement. Circuits, input names, constants and all matrix entries are explicit and syntactically validated; malformed encodings are rejected.

F1: **A supplied one-bit affine sketch makes recognition of semantic factorization automatically polynomial in the supplied circuit length. FALSE unless the original circuit has a syntactically enforced sketch cut (or the entire boundary size is constant).**

F2: **Supplying the entire proposed replacement truth table makes checking equivalence polynomial. FALSE in general even if the table is the single constant zero.**

F3: **A polynomial-bounded sound, complete, polynomial-time checkable certificate grammar for every positive semantic factorization claim follows just from semantic correctness. FALSE as an unconditional inference; such a grammar for arbitrary circuits would imply NP=coNP.**

F4: **This hardness automatically applies to the actual at-most-three-original-variable LOCAL-CONVERT grammar or proves a SAT running-time lower bound. FALSE.** A circuit on at most three accessible input bits is exhaustively checkable in $O(8|C|)$ time. Whether the fixed calculus permits many named boundary inputs, and charges them, must first be established.

## 3. Main proved restricted theorem: rank-one FACTOR is coNP-complete

**THEOREM (PROVED/EXACT, textbook many-one reduction, external specialist review pending).** Under an ordinary explicit Boolean circuit encoding, deciding $\mathrm{FACTOR}(C,L)$ is coNP-complete **even when** $k=1$, $L$ merely selects one fresh boundary bit $y$, and $C$ has one public Boolean output. The problem of checking a supplied candidate output bank $f(y)\equiv0$ against $C$ is coNP-complete on the same instances. These are **semantic verification/recognition** statements, not assertions that any $R_{\mathrm{mix341}}$ rule uses an unrestricted FACTOR oracle.

**Proof.** For membership in coNP, nonfactorization has the NP witness $(u,v)$ with identical $L$-values and distinct $C$-values. A verifier evaluates the matrix and the two explicitly provided acyclic circuits in time polynomial in their serialized lengths.

For hardness, reduce *CNF-UNSAT* to FACTOR. Given any valid signed CNF $D(x_1,\ldots,x_n)$, compile its clauses with Boolean gates into a polynomial-size circuit and add fresh independent inputs $z$ and $y$:

$$
C_D(x,z,y)=z\land D(x),\qquad L_D(x,z,y)=y.
$$

If $D$ is UNSAT, $C_D\equiv0$, so $C_D=f(L_D)$ with $f(0)=f(1)=0$. If $D$ is SAT, let $a$ be any satisfying assignment. Then $(a,0,0)$ and $(a,1,0)$ have the same sketch $y=0$ but $C_D(a,0,0)=0\ne1=C_D(a,1,0)$. Hence $\mathrm{FACTOR}(C_D,L_D)$ holds **if and only if** $D$ is UNSAT. The reduction is one fixed uniform polynomial-time transformation on every valid input; invalid strings are rejected and are not assigned semantic values. Finally, for the supplied bank $f\equiv0$, equivalence $C_D=f\circ L_D$ is exactly the same predicate $\mathrm{UNSAT}(D)$. $\square$

**COROLLARY (CONDITIONAL BARRIER).** If *every* YES instance in this explicit semantic-FACTOR class admitted a certificate of length polynomial in the supplied circuit bits with a uniform polynomial-time sound verifier, then $\mathrm{UNSAT}\in NP$, hence $NP=coNP$. If one deterministic polynomial-time verifier decided all instances without certificates, then $P=NP$. Neither equality nor inequality is established here. A certificate for the *typed syntactic cut* below does **not** entail either collapse.

This is a clean specialization of the earlier project **MAIN AFFINE-LUMPABILITY-RANK-GATE55**, 2026-10-22, which already proved general nonlinear quotient consistency coNP-complete (repository blob \`dddd890f18b00d0d9e779e03451eb296eaa895ee\`). General Boolean circuit equivalence coNP-completeness is standard (Jordan 2013 introduction; Cook--Reckhow proof-system perspective). **Novelty is not claimed for coNP-completeness itself.** The new contribution is pinning it exactly to the current LSPV-1/381 supplied-rank-one-sketch normalization premise, including the explicitly supplied replacement bank and the bounded-support escape.

## 4. Positive typed-cut distinction, and exact cost model

**PROVED/RESTRICTED (already implicit in LSPV-1/381).** Suppose every raw original boundary read in the private sub-DAG is **syntactically prohibited**: private gates may depend only on $k$ already authenticated affine-sketch output wires, with all public aliases explicitly declared. Reachability and gate-reference checking then establishes this property in $O(L+B k)$ word operations (or polynomial time in bits), for supplied serialized circuit length $L$. Evaluate the private DAG for all $2^k$ sketch assignments and compile each public function into a shared signed-AND2 bank, as in LSPV-1/381; this costs $O(2^k L+\mathrm{output\ bits})$ actual work. For $k=O(\log L)$, that is polynomial in **supplied evidence length $L$**, not necessarily in original SAT length $N$ plus the **paid inference count $q$**.

If the boundary has fixed $B\le3$, even arbitrary semantic FACTOR is checkable by at most $2^B$ evaluations of the supplied circuit, costing $O(2^B L)$. Thus this coNP hardness reduction cannot be misapplied to an actual fixed-three-variable operation. A LOCAL-CONVERT output can also contain publicly accessible derived wires, but their exact admissible syntax and separate paid gate counts must be read from the fixed grammar before claiming any multi-boundary embedding.

**Physical-work ledger.** The reduction *constructs* $C_D$ in $O(|D|)$ gates plus the serializer overhead. A proposed normalized bank has $O(2^k)$ truth-vector bits, and writing it costs at least its output length. Checking arbitrary semantic equivalence is coNP-complete, despite the candidate bank occupying two bits. Brute-force checking takes $O(2^B L)$ time and $O(B+L)$ space with the circuit materialized, or less workspace by rescanning a read-only encoding at increased time cost. Reading an exponential-length supplied circuit costs its actual input-access time regardless of how many logical inference nodes the proof assigns. Circuit descriptions, boundary/index reads, gate evaluation, proof checks, outputs, caches, and peak memory are charged separately. No unit-cost semantic conversion or hidden UNSAT oracle is licensed.

**SAME_REALIZATION audit.** The coNP theorem measures worst-case *recognition of a semantic representation promise*. It is not a lower bound on running any fixed SAT decision algorithm, nor a minimum refutation DAG. The typed-cut compiler is a genuine upper bound on a stated restricted compiler with its supplied $L$; it is **not** an upper or lower bound on $\overline W_{R_{\mathrm{mix341}}}(N)$. No T/S point is inferred via FLMV. The type checker does not search for a smallest sketch or certify one found semantically.

## 5. Independent finite controls

The GitHub-readback producer and independently coded verifier were both re-executed. Full-width signed clause subsets on $n=1,2,3$ total $2^2+2^4+2^8=276$ formulas; nine additional specified SAT/UNSAT/malformed-safe Horn and unit controls give **285** tested valid formula instances: **276 SAT, 9 UNSAT**. For the encoding $C_D=z\land D(x)$ and fresh selected sketch $y$, all 276 SAT sources produced an explicit same-$y$, opposite-output pair; all nine UNSAT sources passed zero-bank equality. The producer passed **10,091 assertions** against a gate-by-gate explicit circuit evaluator; the independent verifier passed **1,142 assertions** using directly evaluated formula truth tables and pairwise fiber checks without the producer gate list. Ten malformed source encodings and one corrupted circuit opcode were rejected by the producer; the independent verifier rejected ten malformed sources. Odd/even $K_4$ Tseitin controls gave **0/8** satisfying assignments for odd/even parity, respectively (raw arrays listed even then odd as $[8,0]$).

The finite checks do not establish coNP-completeness; the quantified reduction does. Independent specialist mathematical review, native strict LOCAL-CONVERT proof checker, whole-repository CI and full LaTeX compilation remain pending.

Verified paths:
\`experiments/arc/lspv1_384_affine_sketch_semantic_audit.js\` (Git blob \`0fec1ee82c97045cab0ea5cb73d53f4a21f396d4\`);
\`experiments/arc/lspv1_384_independent_verify.js\` (Git blob \`2d537a578e7dd24afb4f9dacf16d5ec4cbf352c5\`);
\`results/raw/arc/2026-11-04_0100_LSPV1_AFFINE_SKETCH_SEMANTIC_CERTIFICATION384.json\` (blob \`641c47784b5dd694e129bf0338a45228813ae994\`).
Seed: none. Exhaustive within the declared tiny width; no heuristic numerical extrapolation.

## 6. History, peer review, literature, and exact duplication

**Directive and governance:** \`research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md\` read at present blob \`c3889a3e514ddbd747150dcb68607013a3b2d154\`, including its embedded later updates. \`AGENTS.md\` blob \`19656af102604d5f0a721d548cf2e4e72a063561\`; \`CODEX.md\` blob \`754999f50de93cdb693ed37bc8110d31e9e698ef\`; repository \`pnp-research\` skill blob \`b8df83a7b0b1428f349b0e02ce1387d979e8db7f\`. Issue #3 read (751 comments at review). Source snapshot \`research/agents/lspv-1/2026-11-03_2224_LSPV-1_AFFINE_SKETCH_PUBLIC_BANK381.tex\` blob \`0713c71e5f097970d18125098578ecafb97ae461\`. No historical artifact overwritten.

**Current peer work:** LSPV-3/377 signed occurrence bit-probe result, \`research/agents/lspv-3/2026-11-03_1551_LSPV-3_SIGNED_INPUT_QUERY377.tex\`, blob \`66e7817366e8d6039d8dedd1aebb954a7872ec58\`, gives a genuine $\Omega(N/\log N)$ input-read lower bound for odd Tseitin sign positions in its explicit encoding, not exponential SAT decision time. Issue #3 comments for LSPV-3/388 exact guarded Res$(\oplus)$ cofactor and LSPV-2/383 paid ER guarded Tseitin show that source-preservation and affine hardness may be neutralized in stronger proof systems. LSPV-4/380 shows the **entire** clause-subset satisfiability selector can coincide between Haken-hard PHP and easy Horn, so our factorization theorem is not a claim that any selector invariant yields proof hardness. LSPV-5/REFEREE317–319 establish the Cook–Reckhow B3 and extensional-decider bridge distinction. Recent peer comments were reviewed through issue #3 rather than guessed report paths. No peer conclusion establishes B3.

**Grok and Claude folders, genuinely inspected:** \`GROKPROOF/2026-11-02_0617_GROK_CONTRIBUTION.tex\`, blob \`319726c0be1bae76f00997c1161fc76beb65eb55\`, explicitly leaves a uniform all-CNF charged compiler OPEN; \`research/agents/grok/2026-10-12_1859_GROK_FL2.tex\`, blob \`f2a90a8be0688647c0d0b231875438390e769ca8\`, critiques hidden free compiler/route-trie assumptions. \`research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex\`, blob \`9a5b05d6ec0d5580fffe4687b82b4e3dd227de4\`, establishes a crossing-sequence bound that also applies to nondeterminism on the same one-tape model, hence not a general P-versus-NP separation. \`research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex\`, blob \`79e4d4e7e0e3edff3aba8610852c45534bdde128\`, classifies candidate world claims and cautions against claiming equivalences as new theorems. Exact directory paths located through connected GitHub search; they were not inferred from names.

**Search history:** GitHub repository searches for \`affine factorization coNP\`, \`sketch verification complexity\`, \`factorization through affine\`, \`fiber constancy\`, \`input bit sensitivity\`, \`Grok\`, \`Claude\`; external searches for circuit equivalence coNP-completeness, Haken 1985, Cook--Reckhow 1979, and relevant \`github.com/openai\` circuit/SAT implementations. No directly matching OpenAI-owned implementation was found; public SAT verification examples are not assumed to provide the missing project compiler. The older MAIN55C establishes the general nonlinear-quotient barrier, so this result is labeled an explicit **specialization and application**, not a novel complexity separation.

**Primary and original literature:** A. Haken, *The Intractability of Resolution*, TCS 39 (1985), 297–308, https://ftp.math.utah.edu/pub/tex/bib/idx/tcs1985/39/2/297_308.html. S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50, https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/relative-efficiency-of-propositional-proof-systems/218048250981F835B4B2A4080205A0BA. S. Jordan, *Strong equivalence of reversible circuits is coNP-complete*, 2013, https://arxiv.org/abs/1307.0836 (introduction cites ordinary circuit equivalence coNP-completeness). No unverified recent theorem is needed.

## 7. Barriers, exact next target and status

The reduction relativizes in the usual oracle sense only when all relevant oracle access is represented consistently in the compiled verifier; it does not try to evade natural-proofs or algebrization barriers. It uses no pseudorandom property, circuit lower bound or algebraic oracle. Its conclusion is a restriction-specific **verification complexity** theorem, not a machine-hardness theorem. Review of F1–F4 blocks silent substitution of a semantic oracle for an authenticated proof rule.

**NEXT:** retrieve the complete original LOCAL-CONVERT grammar from the fixed Rmix341 report, formally partition its public inputs into true original support versus named derived wires, and check whether its legality conditions are guaranteed by a source-local syntactic typecheck, a constant-size semantic truth table, or an unbounded implicit promise. For any proposed global compiler, either give a polynomial-$(N+q)$ certificate for every conversion or exhibit the coNP-complete semantic-equivalence subproblem precisely within its actual admissible grammar. Do not change Rmix341 to make the theorem fit.

**B1 OPEN, B2 OPEN, B3 OPEN, superpolynomial worst-case $\overline W_{R_{\mathrm{mix341}}}$ OPEN, P versus NP OPEN.**
