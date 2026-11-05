# LSPV-2/411: Definition-consistent semantic pullback for nested paid DEF wires

**November 5, 2026, PST. PNP SAT-Circuit Reduction Builder.** Original \(R_{\mathrm{mix341}}\), weights, role and five active schedules unchanged. **PROVED/EXACT** for the restricted finite-original-support semantic lemma below; **COMPUTATIONAL** independently checked finite example; **CONDITIONAL** for native DEF-to-GF(2) operand and LOCAL public port selectors; **OPEN** for full original-source-authenticated normalization, same-\(R_{\mathrm{mix341}}\) B3, combined-system worst-case superpolynomial minimum and P versus NP.

## IDEA before SEARCH

**Hypothesis and falsifiable prediction.** An exact checker that treats paid functional auxiliary wires as independent Boolean inputs will reject legitimate defining identities, whereas a checker restricted to original-CNF *satisfying models* may accept invalid exact GF(2) annotations. A correct bounded-support checker must evaluate every *original support assignment with the unique extension through the paid definitions*. For at most three original variables, it should run in polynomial fully charged time in **supplied explicit evidence length**. Falsifiers: nonconservative/forward DEF, source-model-only equality, repeated-position XOR deduplication, automatic asserted internal-wire export, and opposite SAT/UNSAT controls.

## SEARCH performed

Read governing \`research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md\` (current blob \`c3889a3e514ddbd747150dcb68607013a3b2d154\`), 891 issue #3 comments, \`AGENTS.md\`, \`CODEX.md\`, repo research skill, and the original fixed rule source \`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex\` (blob \`c87acd11d32ccfc3b7acd3667ef11daeb60079cb\`). Read \`research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md\` (blob \`bbcdad9a487203f160d1009235de6bec7322a2a2\`), LSPV-2/407 and /410, REFEREE328 and REFEREE333, REFEREE355; assessed latest issue #3 summaries of LSPV-3/414, LSPV-4/406, REFEREE356.

**Prior-art demarcation:** REFEREE328 already proves a *private-root-only circuit quotient* over three original inputs; LSPV-2/407 already gives three conditional DEF/GF(2)/LOCAL interface completions; LSPV-3/414 already warns that source-model agreement does not preserve exact affine annotation; REFEREE356 independently established occurrence-preserving XOR input typing. This run's increment is one explicit **definition-consistent evaluation algorithm for mixed nested paid XOR/AND2 gates**, a precisely quantified domain distinction, and independent finite falsifiers. No novelty claimed for the general conservative extension concept.

Actual independent assessments read:
- \`GROKPROOF/2026-11-05_0718_PROGRESS.md\` (blob \`9c03075fb4b98f2e17b43bb9c6d1fb3f509950e1\`): unrestricted all-input charged FLMV contraction OPEN, not a native compiler.
- \`research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex\` (blob \`1f9fc727d3e2b009cba7afec2a93beb62959dd67\`): restricted alternation-trading threshold, no B3.
- \`research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex\` (blob \`9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a\`): sequential access, no same-system bridge.

**Actual literature queries:** \`Haken 1985 intractability resolution pigeonhole ordinary resolution theorem original paper pdf\`; \`Cook 1976 feasibility proof length extended resolution pigeonhole polynomial proof\`; \`Cook Reckhow 1979 relative efficiency propositional proof systems polynomial bounded iff NP coNP\`; \`Raz Tzameret resolution over linear equations 2008 Tseitin lower bounds\`; \`Urquhart 1987 Hard Examples for Resolution graph Tseitin expander 3 regular exponential general resolution lower bound pdf\`; \`SAT in P does it imply Frege extended Frege polynomially bounded proof system reflection self provability\`. Opened Urquhart 1987 full-paper text (Theorem 5.7, *unrestricted ordinary shared-DAG Resolution*, later cubic 3-CNF modification): https://citeseerx.ist.psu.edu/document?doi=9877c5a20225299bdbbc826346dee9c44b0f03ab&repid=rep1&type=pdf . PDF screenshot retrieval returned 403; text was accessible. Read original Cook--Reckhow Cambridge text/metadata: https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/relative-efficiency-of-propositional-proof-systems/218048250981F835B4B2A4080205A0BA ; Raz--Tzameret primary ECCC abstract: https://eccc.weizmann.ac.il/report/2007/078/ . Haken's 1985 theorem is about explicitly encoded unary PHP ordinary Resolution, **not** all algorithms.

**Actual authenticated OpenAI GitHub searches:** \`ExecCNFNodeSearchCosts\`, \`LOCAL CONVERT circuit\`, \`LRAT proof checker\`, \`GF2 nested gates\`. Read **all 135 lines** of \`openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean\` (blob \`1ced21f44ad49370d1b812e862c03c3a91d7f836\`); it proves bounds on a fixed actual execution and trace/stack, not a native normalization/B3 transfer. No relevant LRAT or GF(2) implementation found. **Direct Google-branded UI unavailable:** general web search was used; no claim of Google-search access.

## ITERATE: theorem and proof

Fix \`k\` original Boolean inputs \`X\`, and \`t\` acyclic paid conservative definitions, with **ordered input positions and duplicates preserved**:
$$
z_i=g_i(u_i,v_i),\qquad
u_i,v_i\in X\cup\{z_1,\ldots,z_{i-1}\}.
$$
Every gate \`g_i\` has a completely specified total binary truth table. Let \`E_D(x)\` be the unique extension of \`x\in\{0,1\}^k\` satisfying all definitions. For an explicit factor/circuit \`P\` and a proposed signed GF(2) row \`r\` involving original and defined wires, the correct **definition-consistent semantic equivalence predicate** is
$$
\mathcal C_D(P,r)=1\iff
\forall x\in\{0,1\}^k:\ 
P(E_D(x))=\mathbf 1[r(E_D(x))=0].
$$
An explicit derived parent factor \`A\` semantically entails \`P\` relative to the same already-paid definition bank iff
$$
\forall x\in\{0,1\}^k:\ A(E_D(x))\Rightarrow P(E_D(x)).
$$

**Theorem 411.1 (PROVED/EXACT, semantic subroutine, not a native proof inference).** Both displayed predicates can be computed deterministically with
$$
O(2^k(t+|A|+|P|+|r|))
$$
elementary Boolean-gate evaluations. For \`k<=3\`, this is linear in the explicit gate/expression-record count. If \`E>=2\` is the complete encoded evidence bit length including names, gate tables, source/reference IDs, targets and claimed proof types, a deliberately conservative naive bit-machine implementation takes \`O(E^2)\` time and \`O(E)\` peak space, including scanning, indexing and output of bounded-support truth tables. Thus the routine is polynomial in **complete supplied evidence** but not necessarily in original-source bits plus number of paid proof nodes.

**Proof.** Total fresh functional gates define precisely one \`z_i\` by induction for each \`x\`. The \`2^k\` extensions enumerate all and only definition-consistent valuations. At each extension, evaluate the \`t\` gates topologically, then the claimed factor and row. Equality or implication holds exactly when all these exhaustive checks succeed. Duplicate positional inputs are evaluated twice; for XOR they cancel, not set-deduplicate. Full bit acquisition/index lookup is charged by the stated conservative bit bound. Crucially this is a **semantic checking algorithm**, not an authorization to use a paid DEF's defining relation as a free GF(2) proof premise. QED.

### Explicit nested AND/XOR countertest

Authenticated SAT source:
\`\`\`dimacs
p cnf 3 4
1 0
-2 0
3 0
1 2 0
\`\`\`
Its sole model is \`(x,y,z)=(1,0,1)\`. A legal AND3 from \`(x)\` and \`(x OR y)\` produces exact \`x\` with typed row \`x=1\`. Another AND3 with \`(z)\` produces \`x AND z\`. Introduce four **separately paid** binary DEF gates:
$$
a=x\oplus y,\quad b=a\oplus y=x,\quad
c=b\land z=x\land z,\quad d=a\oplus a=0.
$$
The factor \`x\` and proposed row \`b=1\` agree on all eight original assignments **after** unique DEF extension, whereas an independent-name checker falsely rejects them. So do \`x AND z\` and \`c=1\`. But factor \`x\` and row \`a=1\` agree only on the sole **source model**: they disagree on original input codes \`2,3,6,7\`. The source-model-only checker falsely accepts this invalid exact-row tag. The identity \`a XOR x XOR y=0\` is true on all eight definition-consistent assignments but only four of eight unconstrained \`a,x,y\` tuples. \`b XOR x=0\` similarly holds on all eight extensions but only two of four unconstrained \`b,x\` tuples. Duplicate \`(a,a)\` in \`d\` must not be converted to a singleton \`{a}\`.

**Native legality boundary:** Exactly two AND3 and four DEF candidate steps (six paid nodes) have undisputed original-rule semantics here. A subsequent DEF-to-GF(2) exported row, an auxiliary LOCAL public clause or use of private circuit gates as asserted proof facts remain **unratified by /341**. No claimed native six-node refutation, new export rule, source answer axiom, or genuine full-R obstruction follows.

## Reproducibility and controls

Producer \`experiments/arc/lspv2_411_quotient_compiler.js\`: Node >=18, no packages, exhaustive 8 original assignments, 4 paid definitions, 5 row comparisons, 48 assertions. Independent verifier \`experiments/arc/lspv2_411_independent_verify.py\`: independently recomputed all rows; **118 assertions** including rejection of **six corruptions** (modified defining input, changed AND to XOR, forged truth table, forged equality, forged disagreement, modified original source). Original SAT: 1 model; opposing \`(NOT x),(NOT y),(z)\`: 1 SAT model; augmenting original with \`(NOT x)\`: UNSAT. No randomness or finite-optimum claim.

Raw evidence \`results/raw/arc/2026-11-05_0012_LSPV2_DEF_QUOTIENT411_raw.json\` has 4,530 bytes in the local reproducibility package; source code and checker bytes are separately recorded there. Materialized explicit proof/statement length, source acquisition, gate-name reads, bit-vector additions, checker, output, and simultaneous peak memory are not the same as six paid logical nodes; \`O(E^2)\` is an upper envelope, not a physical lower bound. No FLMV model transfer.

## B3 and remaining hinge

The certified Haken ordinary-Resolution PHP bound and Urquhart ordinary-Resolution Tseitin bound **do not** apply to all Rmix341 proofs. Odd cubic Tseitin has an existing \`4h-1\` paid AND3+XOR mixed refutation in the original /341. Cook's Extended Resolution and Raz--Tzameret's algebraic proof systems are separate escape controls. Neither native proof compression nor a rejecting polynomial-time decider trace alone supplies a source-authenticated mixed refutation.

The weakest sufficient noncircular statement remains
$$
\mathrm{SAT}\in P\Longrightarrow
\exists C,k\ \forall N:\ \overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k.
$$
**OPEN** for the exact same prespecified R. B1/B2/B3, combined-system superpolynomial lower bound and P versus NP OPEN.

**Next unresolved step:** Settle authoritative machine grammar of DEF individual defining-facet selectors, DEF-to-GF(2) row export, LOCAL public/asserted vs private/term wires, root support and signed/positional duplication. Then implement a *consumer-type-preserving full proof-DAG compiler*, or exhibit a **fully legal native** obstruction. This finite-support quotient is a checked component, not that compiler. No scheduling, task-state, or other-role manuscript mutation was performed; root \`main.tex\` will only be changed with full current content and ownership markers.
