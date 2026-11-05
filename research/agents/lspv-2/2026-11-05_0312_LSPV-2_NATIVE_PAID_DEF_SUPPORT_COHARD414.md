# LSPV-2/414: Semantic support of a fully paid native DEF network is coNP-complete

**November 5, 2026, 03:12 PST (America/Los_Angeles).** **Role:** PNP SAT-Circuit Reduction Builder, LSPV-2. **Fixed original system:** \`R_mix341\` of \`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex\`, blob \`c87acd11d32ccfc3b7acd3667ef11daeb60079cb\`, unchanged. **Status:** PROVED/EXACT for the explicitly stated **legal paid two-input DEF prefix** semantic-support language and reduction; COMPUTATIONAL deterministic producer and independent checker; OPEN full native AND3/GF(2)/LOCAL consumer legality, original byte parser, complete normalization, B1/B2/B3, superpolynomial mixed minimum, and P versus NP. Academic novelty/independent specialist mathematical review pending. No tasks, weights, role ownership, schedule or enabled state changed.

## IDEA, stated before SEARCH, and falsifiers

**Hypothesis.** Even with every internal circuit gate implemented as a separately **paid, conservative, two-input native DEF** operation, deciding whether the globally exact function of a named paid output has **at most three essential original inputs** is coNP-complete. Prediction: the test stays hard on constructions with (i) a uniform satisfiable original CNF source, (ii) that original source entailing the output value, and (iii) no free LOCAL internal gates, uncharged circuits or hidden semantic oracles.

Four explicit falsifiers:
1. Paid binary DEF networks might admit a polytime semantic-support check because they have unique extensions. **FALSIFIED** by the CNF-UNSAT reduction below: uniqueness alone does not make dependence testing easy.
2. Promise \`F SAT\` and \`F entails h\` might force small global support. **FALSIFIED**: the same 50-byte satisfiable source entails both low- and high-support paid outputs.
3. A syntactic three-original-variable cone check might be complete for genuine semantic support. **FALSIFIED** by the UNSAT control, whose syntactic cone includes seven originals but whose function is exactly \`u\`.
4. Treating the output named by a paid DEF as an **asserted Boolean antecedent** might be native. **NOT ESTABLISHED**: /341 charges and authenticates its defining relation but does not specify DEF-to-AND3, DEF-to-GF(2), or LOCAL wire-export selector bytes. The present theorem does NOT license such a consumer.

## SEARCH: recovered primary sources, corpus, and duplicate audit

Read FIRST \`research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md\` (retrieved blob \`c3889a3e\`), current issue #3 through REFEREE359 and LSPV-4/409, AGENTS.md, CODEX.md, \`.codex/skills/pnp-research/SKILL.md\`. Read original /341 (\`c87acd11\`), \`research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md\` (\`bbcdad9a\`), own LSPV-2/413 (\`33ba2125\`), REFEREE359 (\`research/main/2026-11-05_0248_MAIN_NATIVE-CLOSURE-BALANCE-IMPLICIT-FIREWALL-REFEREE359.md\`, blob \`a0d80016\`), LSPV-3/418 and LSPV-4/409 issue handoffs. Actual Grok \`GROKPROOF/2026-11-05_0214_PROGRESS.md\` blob \`af7530c7\` and \`GROKPROOF/2026-11-05_1218_PROGRESS.md\` blob \`d3183283\` retrieved; actual Claude \`research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex\` blob \`1f9fc727\` and \`research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex\` blob \`9a5b05d6\` inspected. These explore different time/space/portfolio restrictions and do not provide a native B3 certificate compiler.

**Duplicate control:** LSPV-2/406 already proves coNP-complete semantic-support recognition for unrestricted source-entailed *circuit* payloads, and REFEREE359 already establishes paid-node/root-only semantic closure. THIS RESULT does not claim a novel coNP principle. Its narrower new mapping is to a network consisting **only of individually paid legal native two-input DEF gates**, even with one fixed satisfiable source. The gate output is evaluated as a function, **not** illicitly exported as an inference antecedent.

**Actual general-web queries:** \`Haken The Intractability of Resolution 1985 pigeonhole principle DOI\`; \`Cook Reckhow 1979 relative efficiency propositional proof systems polynomially bounded iff NP coNP\`; \`Gocht Nordstrom certifying parity reasoning pseudo boolean proofs 2021\`; \`Krajicek implicit proofs 2004 proof complexity implicit circuit\`; \`Pich Santhanam 2023 EF lower bounds conditional reflection\`. Read Cambridge Cook--Reckhow and Krajicek journal pages, original Haken publisher abstract indexed (direct DOI open returned 403), and original Gocht--Nordstrom publication abstract indexed (direct journal page blocked). Cook--Reckhow's author-hosted article states Proposition 1.6, conditional p-simulation, but does NOT give the target mixed-calculus compiler. Direct **Google-branded** search was not available; indexed general web is not represented as Google.

**Authenticated \`github.com/openai\` queries:** \`ExecCNFNodeSearchCosts\`, \`CookLevin\`, \`LRAT checker\`, \`definitional circuit check affine\`. Read complete \`openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean\` blob \`1ced21f4\`; it proves same-execution step/storage facts for a different formal machine, not the native R compiler. \`CookLevin\` search located formalization; \`LRAT checker\` produced no relevant implementation; no B3 compiler was found. The local container and Python execution service returned \`redis.exceptions.ResponseError\`, so no full checkout preflight or native Node process is claimed. GitHub connector exact-source V8 replay and separate semantic checking were used instead.

**Primary research exact model firewall:** Haken (1985) proves superpolynomial/exponential lower bounds on **ordinary DAG Resolution** refutations of explicitly encoded pigeonhole CNFs, for every Resolution refutation in the established family, not for mixed R or arbitrary uniform deciders. Haken's publisher abstract explicitly notes polynomial Extended Resolution proofs. Cook--Reckhow (1979) shows some polynomially bounded proof system exists iff NP=coNP; it cannot identify the same preselected /341 system. Krajicek's implicit proof systems use separate circuit-described exponential proofs with stronger semantics/checks. Gocht--Nordstrom (2021) gives efficiently certifiable XOR reasoning in a different pseudo-Boolean calculus. None authorizes /341 DEF row exports.

## ITERATE: exact restricted coNP-completeness theorem

Let \`SUPPORT3-PAIDDEF\` take an acyclic network of \`t\` freshly named, separately paid **two-input Boolean DEF gates** over original input variables \`z_1,...,z_n\`, with one designated output \`h\`, and ask whether the Boolean function computed by \`h\` has at most **three essential original inputs**. Every gate is a total Boolean function of its two inputs, so every original assignment has a unique conservative extension. Each paid DEF costs one original /341 logical node. No derived Boolean assertion is generated just by defining its output.

**Theorem 414.1 (PROVED/EXACT for this restricted native-legal DEF-prefix language).** \`SUPPORT3-PAIDDEF\` is coNP-complete even when each reduction instance additionally has a valid, satisfiable, original-source-authenticated CNF \`F\` in which every original variable occurs, and \`F\` entails that the designated paid output \`h\` equals one. These are promised properties of the constructed instances, not a claim that arbitrary promise verification is free.

**Proof, coNP membership.** To refute \`|ess(h)|<=3\`, nondeterministically provide four distinct original-variable indices and, for each index, a pair of \`n\`-bit assignments differing only in that input on which \`h\` differs. Evaluate each paid gate DAG on the eight assignments in polynomial time. This witnesses at least four essential variables.

**Proof, coNP hardness.** Reduce arbitrary explicit nonempty-clause CNF UNSAT, which is coNP-complete. Let its variables be \`X\`, add independent selector originals \`s_1,s_2,s_3,s_4\` and original \`u\`. Implement, using only legal paid two-input OR, AND, and NOT-as-\`NAND(v,v)\` gates, the output

$$
h_C(X,s_1,s_2,s_3,s_4,u)
= u\lor\left(C(X)\land s_1\land s_2\land s_3\land s_4\right).
$$

For all original variables \`v in X union {s_1,...,s_4}\`, define the uniform signed source

$$
F_n=(u)\ \land\ \bigwedge_v (u\lor v).
$$

It is satisfiable (all assignments with \`u=1\`), and every original variable occurs. By construction \`F_n\models h_C=1\` for every \`C\`, even without looking at its satisfiability label. All gate outputs are fresh conservative definitions; the paid prefix has \`t=O(|C|)\` nodes and fully explicit encoded length polynomial in the CNF length, with the same fixed source form at each \`n\`.

If \`C\` is UNSAT, \`h_C=u\` on **all** original assignments, so \`|ess(h_C)|=1\`. If \`C\` is SAT, fix any satisfying assignment to \`X\` and set \`u=0\`, all selectors one. Flipping **any one** \`s_i\` changes \`h_C:1->0\`. All four selectors are essential, so \`|ess(h_C)|>=4\`. Hence

$$
\boxed{C\in\mathrm{UNSAT}\quad\Longleftrightarrow\quad |\mathrm{ess}(h_C)|\le 3.}
$$

This is a polynomial many-one reduction from UNSAT, and membership gives coNP-completeness. The construction uses only the separately charged DEF-prefix part of the **unchanged** /341 semantic rules. It does NOT assume downstream native proof consumers can use \`h_C=1\` without additional rule authorization. \(\square\)

**Corollary 414.2 (PROVED/EXACT model limitation).** If an extension/completion of /341 permits an arbitrary paid-DEF output as a candidate AND3/LOCAL condition and requires the checker to recognize its *semantic* three-original-variable support merely from that gate DAG, then that support-recognition task is coNP-hard. Thus a blanket polynomial verification promise requires an extra **syntactic support restriction** or separately justified derivation certificate; paying each gate does not make arbitrary semantic support easy. This is a statement about the verification subproblem, **not** a legal counterexample to the native mixed proof system and **not** a proof that P differs from NP.

An inexpensive syntactic input-cone overapproximation is sound for accepting support<=3 when it finds at most 3 originals, but is incomplete: in the UNSAT case above the syntactic cone includes every \`s_i\`, yet the output is exactly \`u\`. Source-model-only evaluation is even worse: on satisfying assignments of \`F_n\`, every \`h_C\` equals 1 and loses all global support information.

## COMPUTATIONAL: fully charged gate-network controls

The verified **seven-original-variable** source has clauses \`(7), (7 OR 1),...,(7 OR 6)\`; its valid ASCII DIMACS is 50 bytes, seven clauses, 64 satisfying original assignments. Let \`X={1,2}\`, selectors \`{3,4,5,6}\` and \`u=7\`. Enumerate all \`2^8=256\` subsets of the eight proper nonempty clauses \`(1),(-1),(2),(-2),(1 OR 2),(1 OR -2),(-1 OR 2),(-1 OR -2)\`. For every CNF, build the fully explicit topologically named, fresh, separately paid gate DAG, compute its **global** output truth table across all 128 original assignments, independently test each of the seven essential coordinates and source entailment, and compare with an exact 4-assignment SAT test.

Results: **95 SAT and 161 UNSAT**, precisely **161 outputs with semantic support <=3**. Paid two-input gate counts range **7 to 25**, with no hidden/unpaid gates. UNSAT control \`C=(x_1) AND (-x_1)\` (mask 3) gives \`ess(h)={u}\`; SAT control \`C=(x_1)\` (mask 1) has essential support \`{x_1,s_1,s_2,s_3,s_4,u}\`. The producer executed **279,040 counted checks** in a V8 run using the complete builder, with 0 discrepancies. The **independently authored** direct-CNF verifier (no producer imports, no paid-gate evaluation code) was retrieved from GitHub and executed in a separate V8 invocation with read-only \`fs\` and \`assert\` shims: **35,607 checks PASS**, **four deliberately corrupted certification records rejected**. The authenticated producer was separately re-executed in V8 with restricted standard-module shims and reproduced the published JSON **byte-for-byte**. These are deterministic finite controls, not a mathematical coNP-hardness proof by experiment.

Published readback paths:
- \`experiments/arc/lspv2_414_paid_def_support.js\`, blob \`c89a1d0de001722e33db28e742272b96ccaf1dcb\`;
- \`experiments/arc/lspv2_414_independent_verify.js\`, blob \`b78ec81c64bf4cc4dd5c4c41a55b4e286879fd45\`;
- \`results/raw/arc/2026-11-05_0312_LSPV2_414_PAID_DEF_SUPPORT3_raw.json\`, blob \`d1311b98f1292fc0f769bba602e62a3c4fb598d9\`.

**Resource accounting.** \`t\` separately paid logical DEF nodes each cost 1. Output \`h\` alone is **not a native refutation** and does not define \`W_R(F)\`. The construction is produced in polynomial time and encoded polynomially in \`|C|\`, including source and paid gate evidence. Producing/reading \`E\` bits of the gate network costs at least linear read/write work; evaluating one assignment costs \`O(t)\` Boolean gate operations with \`O(n+t)\` bits of simple live state. The exhaustive support experiment costs \`O(n 2^n t)\` and is **NOT** a proved polynomial checker on general instances; the coNP-completeness result explains why a generic semantic support detector needs special care. Actual Python/Node RSS and native-TM peak space were not measured. No FLMV resource contraction is inferred.

**Both labels and malformed/corrupt control caveat:** the source \`F_n\` is SAT in all 256 experiments and every output is entailed; the varied CNF **predicate** \`C\` covers both SAT/UNSAT labels. Four corrupted raw certification records were rejected. There is no new 256-instance original-UNSAT native proof corpus. Earlier /341 and /413 still supply certified odd-UNSAT original proof controls and malformed-DIMACS rejection; those have not been silently reclassified as part of this run.

## First outstanding deliverable: exact native grammar

The literal original /341 rule says AND3 premises' combined support is at most three **original variables**, a LOCAL implication uses an explicitly constant-support truth-table test, paid DEF introduces one conservative two-input gate per node, and GF(2) addition consumes two **existing GF(2) rows**. REFEREE359 proved that a free LOCAL internal wire is not a native antecedent, and provided a polynomial *semantic canonical form* for paid roots/fixed facets. The historical proof specification still lacks exact selector/facet/row-export byte syntax. This run contributes a boundary condition: simply replacing syntactic support by semantic support of arbitrary paid DEF cones would introduce a coNP-complete checker subproblem. Our legal gate prefix alone cannot be called a legal **DEF→AND3→GF(2)→LOCAL** consumer DAG; no unauthorized port was silently inserted. An exact-byte source-authenticated full proof compiler, or an **explicit legal full mixed-DAG** obstruction, remains OPEN.

## Second outstanding deliverable: weakest-sufficient same-R B3

For the unchanged fixed calculus,

$$
\mathrm{SAT}\in\mathrm P\quad\Longrightarrow\quad
\exists C,k\;\forall N:\quad \overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k
$$

is **OPEN**. A semantic-support coNP-hardness subproblem does not prove that shortest native refutations are hard, nor does it disprove a hypothetical polynomial-time SAT decider: under P=NP that subproblem would also be in P. A decider's rejected output cannot be used as a native refutation without independently authenticated and efficiently represented machine-correctness/reflection. Cook--Reckhow's existence theorem identifies SOME proof system, not the preselected /341 calculus. No assertion about the implication itself is upgraded here.

**Next precise proof obligation:** freeze a **finite-alphabet native selector typing** for the fixed paid roots/facets without changing the semantic rules; make explicit whether any exported DEF value can feed AND3/LOCAL and, if so, require syntactic input-support at most 3 or a separately charged/sound certificate. Then attempt a consumer-preserving compiler with an exact checker for each GF(2), AND3 and LOCAL node; independently audit any rejection-trace-to-native-proof B3 route. ROOT \`main.tex\` fetch returned blob \`b2fbfd9f\` but **zero content bytes** even on disjoint line ranges, so it was **not overwritten**. Repository checkout preflight could not run due container infrastructure failure. No existing research files were erased.

## Primary references

1. A. Haken, *The Intractability of Resolution*. Theoretical Computer Science 39 (1985), 297–308. DOI [10.1016/0304-3975(85)90144-6](https://doi.org/10.1016/0304-3975(85)90144-6).
2. S. A. Cook and R. A. Reckhow, *The Relative Efficiency of Propositional Proof Systems*. Journal of Symbolic Logic 44 (1979), 36–50. [Original author-hosted paper](https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf).
3. J. Krajíček, *Implicit Proofs*. Journal of Symbolic Logic 69 (2004), 387–397. [Original publisher abstract](https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/implicit-proofs/B6E778CBA3308E4A172F66FFDEB07054).
4. S. Gocht and J. Nordström, *Certifying Parity Reasoning Efficiently Using Pseudo-Boolean Proofs*. AAAI 35 (2021), 3768–3777. DOI [10.1609/aaai.v35i5.16494](https://doi.org/10.1609/aaai.v35i5.16494).
