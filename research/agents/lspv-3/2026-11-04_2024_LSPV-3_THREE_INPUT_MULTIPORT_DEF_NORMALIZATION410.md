# LSPV-3/410 | Three-original-input exported-port DEF normalization and its provenance firewall

**PNP Hypergraph & Proof Certificates | November 4, 2026, 20:24 PST | fixed original R_mix341 unchanged.**

**Epistemic status:** **PROVED/EXACT** for the stated *standalone conservative-DEF multiport normal form*, pending independent academic review; **COMPUTATIONAL** exhaustive/random finite verifications; **OPEN** native LOCAL-CONVERT public/private syntax, individual DEF-facet selectors, full original-source proof translation, B1/B2/B3, superpolynomial mixed lower bounds, and P versus NP. **Not an unconditional R_mix341 whole-proof compiler.**

## IDEA: explicit assumptions and 4 falsifiers, formulated before search

**Initial conjecture.** The potentially unbounded *internal* gate complexity of an already-paid, three-**original**-variable circuit is not intrinsic to the Boolean information on finitely many designated public ports. Given a paid acyclic binary-definition DAG on exactly original inputs x1,x2,x3 with b distinct exposed gate-output wires and no external use of private gate records, predict an exact conservative replacement using **at most 5b fresh paid binary gates**, with the SAME public output names and Boolean values on all eight source valuations, independent of reconvergence and the original internal gate count. This is a local interface theorem, NOT a claim that the native LOCAL-CONVERT rule exports arbitrary circuits or that all downstream inference steps remain legal.

**F1:** some one of the 256 Boolean functions on three inputs needs more than five arbitrary two-input Boolean gates under the explicit truth-table gate grammar. **F2:** reconvergence, cancellation or shared intermediate gates falsifies the public-output equivalence. **F3:** the replacement destroys a source SAT model, creates an UNSAT model, violates gate freshness, or changes high-support behavior when a public port is used as a named variable. **F4:** an inference later referring to a private definition/facet, rather than the designated public-output value, remains justified without reauthentication. The first three predictions passed rigorous tests; the fourth is a **valid boundary objection**, not assumed away.

## SEARCH: original research, corpus, exact paths and unavailable sources

The governing file was read FIRST: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, blob `033b54b8`. Current issue #3 and latest LSPV-1/408, LSPV-3/409, LSPV-4/401, REFEREE352 comments were reviewed. Governance: `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`. Original fixed calculus: `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11`). Original grammar clarification: `research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md` (blob `bbcdad9a`). Relevant originals read: LSPV-3/408 (blob `e73d2bfc`), /409 (blob `2b5a58bf`), LSPV-4/400 (blob `e01464b9`); newer peer findings checked in issue comments.

Actual independent-review files read: `GROKPROOF/2026-11-05_0315_PROGRESS.md` (blob `2c21a1eb`), `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`. None supplies native B3 or a complete compiler; Grok remains focused on a different charged FLMV transformation; Claude's sequential/random-access machine distinctions prevent resource-model transfer.

General web search queries run: `Shannon decomposition boolean function circuit cofactor if then else construct AND XOR 3 gates synthesis`; `Cook Reckhow relative efficiency propositional proof systems 1979 pdf polynomially bounded`; `Haken 1985 intractability of resolution pigeonhole principle exponential lower bound`; `Cook 1976 short proof pigeonhole extended resolution`; `proof system XOR clauses resolution XOR Tseitin polynomial size proof systems`. Primary Cook–Reckhow 1979 JSL paper read via author's full PDF (and page screenshot); the 2026 Braun Res(oplus) paper abstract was checked with exact theorem statement, full arXiv HTML was inaccessible (not misrepresented as fully read). Shannon/Boole expansion is a classical identity and is reproved below, not claimed as new mathematical literature. Direct Google-branded UI was unavailable; general web search was used, **not** misreported as direct Google access.

Authenticated github.com/openai repository queries run: `ExecCNF`, `Shannon`, `circuit equivalence`, `proof certificate resolution`. Full `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNF.lean` read at blob `e60f4d98`. Its explicit list/bit-cost discipline is relevant; it is not a native Rmix341 port compiler or B3 proof.

**Duplication/contradiction:** Standard Shannon cofactor synthesis is not novel. LSPV-3/406 already established unique extension for arbitrary fresh acyclic DEF DAGs; /407 established coNP-hard semantic equality with unbounded input support; /408 and /409 handled specific nonstructural aliases CONDITIONAL on addressable DEF clauses. LSPV-4/400 and REFEREE351 already falsified independent local conclusion rewrites with unchanged consumers. **New here** is a uniform, completely explicit **five-paid-gate per exposed public port** normal form for arbitrary reconvergent *three-original-variable* native DEF sub-DAGs, without equality oracle, plus evidence/consumer limits. No claimed novelty relative to classical Boolean synthesis.

## The original fixed R and exact quantified theorem

Original R_mix341 has zero-cost signed DIMACS source clause axioms, unit-cost distinct derived DAG nodes, at most two antecedents, RES on clauses, AND3 combining conditions with at most three **original** variables into an exact eight-bit factor, XOR sums of authenticated GF(2) rows, unary LOCAL-CONVERT implied bounded-original-support circuit conditions/clauses verified by eight-row checks, and one unit-cost globally fresh, two-input functional DEF gate with all defining relations attributed to its node. **The original rule does NOT fully serialize LOCAL internal/public exports, individual DEF defining-clause selectors or GF(2) row exposure.** All statements below keep the actual original DEF operation and avoid claiming anything about the unresolved exports.

**Theorem (standalone native DEF three-input public-vector replacement).** For every finite signed CNF F(x1,x2,x3) (SAT or UNSAT), every acyclic list D of t >=1 globally fresh paid arbitrary two-input Boolean-function gates with input wires among x1,x2,x3 and earlier gates, and every set P=(p1,...,pb) of b <=t distinct gate-output identifiers, there exists an acyclic list D' of at most **5b** native paid fresh binary gates such that for every valuation a of the ORIGINAL THREE inputs, the unique extensions satisfying D and D' agree on **all named public outputs P**. D' uses precisely the public names P as its final output names, introduces other globally fresh private intermediates, and introduces no new assertion of a public output's truth value. Thus the projections of model sets onto source variables and P are identical:

$$
\forall a\in\{0,1\}^3\quad
\bigl(p_1^D(a),\ldots,p_b^D(a)\bigr)
=
\bigl(p_1^{D'}(a),\ldots,p_b^{D'}(a)\bigr).
$$

For any original CNF F, including UNSAT, both extensions are conservative and have the same number of projected source solutions. This is a **semantic/model-preserving** equivalence and full DEF-node constructive certificate; it does **not** imply that derivations referencing old private wires, old defining clauses or their source DAGs can be copied without repair.

**Explicit construction.** For each exposed output function f=f(x1,x2,x3), enumerate its eight truth-table rows by evaluating D in topological order. Let f0(x2,x3)=f(0,x2,x3) and f1(x2,x3)=f(1,x2,x3). Both f0 and f1 are arbitrary binary truth tables and therefore one native two-input DEF gate each. Let

$$
a=f_0(x_2,x_3),\qquad b=f_1(x_2,x_3),\qquad d=a\oplus b,
\qquad t=x_1\wedge d,\qquad p=a\oplus t.
$$

These are **five** paid DEF gates. Over GF(2),

$$
p=f_0\oplus x_1(f_0\oplus f_1)
=\begin{cases}f_0,&x_1=0,\\f_1,&x_1=1,\end{cases}
=f(x_1,x_2,x_3).
$$

To avoid name conflicts, choose all four intermediates per port from a fresh private namespace outside all source, original, and public identifiers. Declare the **fifth** definition output with the designated original public name p_j, which is globally fresh within the reconstructed proof and is never defined a second time. The original private gates disappear. No public name is an input to a reconstructed output: each depends directly on the three original inputs, so any order of P is acyclic. This proves 5b paid nodes with shared DAGs allowed but not needed.

**Physical resource bound.** Let N denote the explicit signed DIMACS source bits and E the **explicit** input DEF DAG plus public-identifier list bits, including every wide wire identifier and gate mask; q=t input paid gates. Evaluation of all 8 input assignments costs 8t gate truth-table operations plus input parsing. Recording b output truth tables requires 8b bits; construction requires exactly 5b 4-bit gates and references. Canonical short private IDs give **O(E+b log(N+E+b+2))** explicit normal-form evidence bits if public IDs are preserved. A straightforward fully buffered implementation has polynomial bit time and O(poly(N+E+b)) all-phase peak bits; a deterministic deliberately conservative upper bound O((N+E+b+2)^3) bit-time and O((N+E+b+2)^2) space follows from elementary repeated scans and serialization, NOT an FLMV/small-space claim. Acquiring/verifying all source and gate records and writing/checking the 5b records are charged; the logical DEF count is separate from proof search and physical runtime. Nothing assumes that an E-bit arbitrary LOCAL payload is free.

**Scope fence.** If some public gate depends on more than three independent **original** variables, the five-gate bound has not been proved and is in general false for arbitrary functions. If a purported public port is a circuit condition **asserted** true by LOCAL-CONVERT, it is not made a proved consequence merely by introducing its DEF gate: assertion and functional definition are different rules. If a later inference references a private wire or a particular old defining-clause facet, the projection equality alone gives no legal replay. A proof compiler must either retain that wire/facet, or construct and charge an authentic replacement derivation. If a boundary uses three auxiliary ports with large original support, the 3-original-support AND3 test is NOT automatically preserved. These are the precise obstacles to extrapolating this theorem to the full mixed calculus.

## ITERATE: experimental challenge and revised claim

The first proposed claim, "normalize an arbitrary LOCAL circuit payload," was too broad because the original rule never specifies public/private export grammar and a LOCAL-derived **condition** is not a conservative gate. The revised theorem above is therefore restricted to **already-paid DEF networks with an explicit list of public gate outputs and three original inputs**. This is the strongest full-grammar-independent positive statement established here. It is not a new rule.

A standalone deterministic JavaScript producer independently verified every one of the **256** truth tables on all eight assignments (2,048 checks) and built a 1,280-paid-gate, 256-output shared certificate whose 2,048 public output evaluations matched. It also synthesized outputs of **500** pseudorandom reconvergent original DAGs, checking **27,544** output rows, and rejected five malformed gate records plus a corrupted output record. Source controls F_sat=(x1) and F_unsat=(x1) AND (NOT x1) have respectively four and zero models; unique extension preserves those counts, and x XOR x = 0 as well as XOR reconvergence are included among tested functions.

Independently authored Python executed the same **all-256, all-eight-row** truth-table check and 500 differently generated random DAGs, with **27,528** random output-row comparisons, 1,280-gate bundle controls, five malformed rejections, and a corrupted-output rejection. Distinct PRNGs explain the differing random-output test counts. Python results recorded locally as `/mnt/data/lspv3_410_independent.py`. All tests are finite checks; the all-size theorem rests on the five-gate algebraic identity and global fresh-name construction.

Published code: `experiments/arc/lspv3_410_three_input_multiport_normalizer.js`. Published raw: `results/raw/arc/2026-11-04_2024_LSPV3_THREE_INPUT_MULTIPORT410_raw.json`. The verifier is a **DEF-fragment witness checker**, not a native mixed proof checker.

## Certified hard families, bridge typing and exact next gap

**Haken 1985.** For h+1 pigeons, h holes, the standard ordinary unary PHP CNF has h(h+1) variables, Theta(h^3) clauses, and Theta(h^3 log(h+2)) signed literal index bits. Every **ordinary shared-DAG Resolution** refutation requires 2^{Omega(h)} clauses, for the published family. This quantification covers all Resolution derivations within that system, not ER/DEF/LOCAL/GF(2) or arbitrary algorithms. **Cook 1976** gives polynomial Extended Resolution PHP proofs; the established cubic odd-Tseitin source from /341 has exact **linear** W_Rmix341=4h-1 by XOR (the source has 4h clauses). The newer Braun (September 2026) theorem bounds **Res(oplus)** DAG refutations of the **bit** PHP with n=2^ell holes by more than exp(n/(32768 ell^2)) for ell>=32, but this is a different proof system and encoding, not Rmix341 or a machine lower bound.

The proof-system targets still have

$$
W_R(F)=\min_{\pi\text{ legal refutation DAG}}\sum_{v\in\pi\text{ paid distinct}}w(v),
\qquad
\overline W_R(N)=\max_{F\text{ valid UNSAT},\,|F|\le N}W_R(F),
$$

with N encoded bits. **B1** is pointwise A-to-R domination, **B2** is all-binary-input worst-case A-to-R domination, **B3** is SAT in P implies the same fixed R has polynomial worst-case Wbar_R. The implication **B1 => B2 => B3** is logical, but none is supplied by this interface theorem. Cook–Reckhow's 1979 characterization gives *some* p-bounded proof system under NP=coNP and their EF compression result concerns a stronger proof grammar; neither furnishes native B3. REFEREE352's generic locked-clock proof system defeats a generic-B3 shortcut without refuting native B3.

**Required next exact witness:** recover, or formally declare missing, the actual native **DEF-facet reference syntax** and **LOCAL-CIRCUIT public/private exports**. Build a case with one LOCAL-derived high-width port and authenticated downstream **RES, AND3, XOR, LOCAL** consumers; try a consumer-aware compiler that never changes source provenance or rule typing and has polynomial **encoded bits**, not just nodes. A genuine *legal* native counterexample to such a compiler would be decisive; an illegal identifier collision or an ambiguous export interpretation would not. Do not change native R to make this theorem pass.

**Root MAIN reconciliation:** root `main.tex` must only be edited after full byte retrieval and locating balanced LSPV-3 ownership markers at current SHA. If full content unavailable, leave it unchanged; do not overwrite content outside ownership.

## References

[1] Cook SA, Reckhow RA. The relative efficiency of propositional proof systems. *J Symbolic Logic*. 1979;44(1):36–50. Author PDF: https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf

[2] Haken A. The intractability of resolution. *Theor Comput Sci*. 1985;39:297–308. doi:10.1016/0304-3975(85)90144-6.

[3] Cook SA. A short proof of the pigeon hole principle using extended resolution. *SIGACT News*. 1976;8(4):28–32.

[4] Braun K. An exponential lower bound for the bit pigeonhole principle in resolution over parities. arXiv:2609.23015. September 19, 2026. https://arxiv.org/abs/2609.23015.
