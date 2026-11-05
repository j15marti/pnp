# LSPV-2/420: Exact essential-support verification parameterized by paid nonlinear gates

**November 5, 2026, 08:12 PST.** Research role: PNP SAT-Circuit Reduction Builder (LSPV-2).
**Status:** PROVED/RESTRICTED all-size theorem for the conservative, separately paid, two-input native DEF-prefix syntax; COMPUTATIONAL independent finite checks; full historical native grammar, consumer-preserving normalization, B1/B2/B3, mixed worst-case superpolynomial hardness, and P versus NP OPEN. Independent academic red-team review remains pending. No task identity, enabled state, schedule, proof rule, node weight, or another specialist's manuscript region changed.

## IDEA, stated before SEARCH

Prior work LSPV-2/406, /414, /419 and LSPV-3/382 already established that deciding whether an arbitrary explicit Boolean circuit has at most three essential original-variable inputs is coNP-complete, even when its network consists of separately paid legal conservative two-input DEF gates. This is not a new complexity-hardness discovery.

**Falsifiable repair hypothesis.** Let E be the total explicitly encoded size of a paid acyclic two-input DEF network, k the number of **nonaffine** gates in the designated output's transitive dependency cone, and a the number of distinct syntactically active original coordinates. The exact essential-support set can be found in O(a*16^k*poly(E+1)) bit time and polynomial peak working memory, by reducing each candidate input's two-run inequivalence to finitely many GF(2) linear systems. This is a *parameterized semantic-support checker*, not a new inference rule.

Precommitted falsifiers: (F1) XOR cancellation makes the procedure report spurious support; (F2) unrelated dead nonlinear gates change the result; (F3) nonlinear gates with repeated inputs invalidate the guessed-input equations; (F4) giant sparse original-variable headers force an impossible dense memory allocation; (F5) gate definitions are silently treated as source-entailed asserted Boolean facts.

## SEARCH: authenticated source and novelty audit

Read first the governing November 2 five-role research handoff at research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, current issue #3 through LSPV-5 REFEREE364 (07:48 PST), original R_mix341 specification research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb), root AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. Reviewed LSPV-2/389, /406, /414, /417 and /419; LSPV-1/419, LSPV-3/424, LSPV-4/415, REFEREE363 and REFEREE364. The latter proves dependency-plus-DEF-owner closure is needed even in the frozen CANON2R proof serializer; merely following explicit reference pointers is insufficient.

Actual external assessments: GROKPROOF/2026-11-05_1428_PROGRESS.md (blob a0e35e77f5d35edb41cef00daf72e36d1536ae44) and research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67), plus CLAUDE_ONETAPE-0001 (blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a). Their small-space/portfolio discussions do not close the mixed-proof grammar or B3.

General web literature queries included Haken 1985 pigeonhole Resolution lower bound, Cook 1976 Extended Resolution PHP, Raz and Tzameret 2008 Resolution over linear equations, multiplicative complexity of XOR-AND circuits, Soeken SAT multiplicative complexity, and Gwynne and Kullmann XOR CNF fixed-parameter translations. Sources included Haken TCS (1985), DOI 10.1016/0304-3975(85)90144-6; Raz–Tzameret APAL (2008), DOI 10.1016/j.apal.2008.04.001; NIST work on multiplicative complexity of six-variable Boolean functions; Soeken (2020) arXiv:2005.01778; Gwynne–Kullmann (2014), arXiv:1406.7398. These works concern related systems and do not directly prove this exact source-authenticated gate-prefix statement, nor B3. There is no claim of academic originality for generic FPT circuit reasoning.

Authenticated OpenAI GitHub queries included ExecCNFNodeSearchCosts in openai/math; read the complete lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (blob 1ced21f44ad49370d1b812e862c03c3a91d7f836). It proves resource bounds for a different explicitly defined executable SAT subroutine, not a native proof compiler. Direct Google-branded search was not accessible; indexed general web search was used, without representing that as Google-branded browsing.

The established published hardness anchor remains Haken's exponential lower bound for *ordinary binary DAG Resolution* of standard explicitly encoded unary PHP formulas. With h+1 pigeons, h holes, input bit length Theta(h^3 log(h+2)), every Resolution proof has 2^Omega(h) lines. Cook's polynomial Extended Resolution PHP proofs are the mandatory countercontrol. Likewise affine GF(2) shortcuts invalidate transferring ordinary Resolution bounds on odd Tseitin to R_mix341. None supplies an unrestricted SAT-machine lower bound.

## ITERATE: theorem and all-size proof

**Theorem 420.1 (PROVED/RESTRICTED, with specialist review pending).** For every explicit acyclic, separately paid conservative two-input Boolean DEF network whose designated output has k nonaffine paid ancestors and a distinct original-coordinate ancestors, the set Ess(C) of original input positions on which the output depends essentially is deterministically computable in O(a*16^k*poly(E+1)) bit time and poly(E+1) peak working space, for explicit encoded evidence length E. Consequently, for k=O(log E) the exact semantic-support predicate is polynomial-time decidable, regardless of how many original coordinates cancel through GF(2) algebra. The bound counts complete parsing, reading, matrix construction and elimination, checks, and output and does not include finding the input circuit or a proof.

**Proof.** Every two-input Boolean function with truth table f(0,0),f(1,0),f(0,1),f(1,1) has the unique algebraic normal form over GF(2)

$$
f(u,v)=c\oplus \alpha u\oplus\beta v\oplus\gamma uv,
\qquad
\gamma=f(0,0)\oplus f(1,0)\oplus f(0,1)\oplus f(1,1).
$$

A gate is nonaffine precisely when gamma=1. First obtain the exact syntactic backward cone of the target gate, discarding all irrelevant dead gates, and densely index its a original coordinates (while retaining original identifier strings for exact output). For each candidate original position j, consider two linked executions C(x) and C(x xor e_j). Their original-variable values differ only at j.

At every one of the k nonaffine gates guess its two input bit values separately for both copies, four guessed bits in total per gate. This gives 16^k assignments of guessed local gate-input values. For any fixed assignment of guesses, every nonaffine gate output becomes a known constant in each copy by its exact four-entry truth table, while every affine gate output becomes an explicitly maintained affine form in the a original input bits. For each guessed nonaffine gate input, impose an affine equality between the computed predecessor expression and the guessed bit, four equalities per nonlinear gate. Add one affine equality saying the two final output bits differ. The resulting at most 4k+1 affine equations in a original inputs can be checked by Gaussian elimination.

If any system is consistent, its satisfying assignment supplies a real, definition-consistent witness C(x)!=C(x xor e_j): all guessed gate inputs are enforced and all gate outputs follow the actual paid truth tables. Conversely, any genuine witness determines one of the 16^k guessed patterns, and its assignment satisfies all corresponding equalities, so that branch is consistent. Thus j is essential iff at least one branch is consistent. Repeating over a positions and explicitly charging each polynomial-size linear system proves the claimed total time and polynomial *peak* memory. If the output has no original-coordinate ancestor, Ess(C) is empty immediately. No correctness oracle, uncharged proof edge, or P-time SAT decider is assumed. QED.

**Support and export distinction.** This theorem computes semantics of a designated **paid DEF output**. It does not establish a legal source-entailed Boolean *assertion* about that output, nor authorize it as a GF(2) row, a public LOCAL-CONVERT wire, or an AND3 antecedent. Those remain disputed aspects of original /341 grammar. It therefore cannot yet be inserted as a fully legal refutation-translation step. It is also not a superpolynomial minimum refutation lower bound. For sparse original identifiers, the theorem uses exact lexicographic integer comparisons and dense *active* reindexing; arbitrary precision is needed in a production parser.

## Computational producer, independent challenge, and repairs

Published deterministic no-dependency JavaScript producer: experiments/arc/lspv2_420_fpt_semantic_support.js, source blob 1cd475d4fe4f741f5d05dcf6511b75ac20ea6de9. Published separately implemented truth-table oracle: experiments/arc/lspv2_420_fpt_semantic_support_independent.js, source blob 9aa69d8ff1916f827e1214a77b545247d45530e6.

Both were retrieved from authenticated GitHub readback and evaluated in the JavaScript V8 research tool, not merely inspected. The producer passed 1,287 assertions over 1,282 circuits: all 880 distinct single-gate input/table cases for 1..5 originals, 400 seeded nested circuits, and two guard controls. The nonlinear-cone-gate histogram was k=0:571, k=1:625, k=2:70, k=3:14, k=5:2. The largest enumerated guess count was 6,291,456. SAT-enabled guard had six essential original coordinates; cancelled/UNSAT guard had none.

The separate checker passed 2,291 checks, including its own 1,402 nested/cancellation cases, 880 single-gate cases, five sparse-ID controls with nvars=10^9, and three malformed-gate rejections. It computes *full evaluations for all assignments in the small dependency cone*, independently of the producer's affine linear solver.

Two implementation defects were found and corrected during this run. The initial FPT implementation skipped nonlinear gates outside the output cone but evaluated all dead gates, leading to a false negative; it was repaired to compute only live cone gates. An initial independent truth-table oracle incorrectly demanded explicit assignments to originals appearing only in dead gates; it now assigns them an arbitrary constant. Both published final versions passed authenticated readback execution. Finite checks support, but do not replace, the all-size algebraic theorem.

Raw data (including blobs, parameters and constraints): results/raw/arc/2026-11-05_0812_LSPV2_FPT_NONLINEAR_SUPPORT420_raw.json. Deterministic seeds: 4201337 and 2026420. Native CANON2/CANON2R was inspected but no complete nested-DEF LOCAL/GF(2) translation was claimed executed. The JS parser currently accepts safe-integer variable identifiers, not arbitrary-width decimal identifiers beyond 2^53. The symbolic theorem is not subject to that JS limitation when implemented with arbitrary precision.

## Full physical-cost accounting and transfer status

The logical weight of t legal DEF gates is t, regardless of the 16^k semantic-checker time. The actual checker must acquire and parse every supplied record, identify and map active names, traverse the ancestor cone, enumerate guessed gate-input configurations, rebuild affine expressions, solve matrices, verify the output and serialize support results. Its materialized peak working memory remains polynomial in explicit E; the exponential number of guesses is processed sequentially and does not imply exponential simultaneous storage. The cost bound is in **input circuit evidence E**, not automatically in original CNF source length N plus paid-node count q if circuits or LOCAL payloads were unbounded and uncharged. Proof acquisition, proof validation, computation runtime and minimum logical-node count must remain separate. FLMV all-phase memory retains s'<=max{rho,eta,lambda,lambda*s}, with rho>=1 whenever a full input copy is materialized, even if freed before child calls.

The weakest sufficient conditional B3 remains

$$
\mathrm{SAT}\in\mathrm{P}\quad\Longrightarrow\quad
\exists C,d>0\ \forall N:\ 
\overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^d.
$$

This theorem does not imply B3: it verifies one semantic property of a *supplied* paid gate DAG and constructs no native refutation from an arbitrary uniform polynomial-time SAT decider. Neither polynomial formalized correctness nor polynomial native proof existence is assumed. **B1, B2, B3, full mixed normalization, worst-case superpolynomial Wbar, and P versus NP remain OPEN.**

## Publication and next falsifier

Code, independent verifier, full deterministic results, this report and five-role handoff were published to role-owned paths with authenticated readbacks. Root main.tex could only be retrieved as empty content despite GitHub reporting nonempty blob 1b8a7d9a1514b06c96501849a7902b7aa3dae2a1, so it was *not overwritten*: no unsafe other-role modification or silent loss of existing text was attempted. Current issue #3 was informed.

**Next precise test:** For k=O(log E), feed the semantic-support checker into a *separately declared candidate* LOCAL-CONVERT wire interface. Build a nested conservative paid-DEF + GF(2) + AND3 mixed proof with true original-byte source authentication; check that each consumed output is an actually authorized and paid typed view, not merely a semantic circuit value. Either derive a full source-authenticated polynomial compiler *for the unchanged historical rules* or demonstrate a **legal**, rather than merely candidate-grammar, counterexample. Keep one fixed R and B3 as an independent remaining theorem.
