# LSPV-3/393 | Source-block duplication firewall
**November 4, 2026, 05:24 PST. PROVED/EXACT in the unchanged fixed R_mix341 calculus, independently audited finite evidence; external mathematical referee pending. P versus NP OPEN.**

## Precise new result
For a connected simple bridgeless cubic graph G with h vertices, any odd Tseitin vertex charge b, and every integer r >= 1, let T^[r](G,b) be the explicit signed CNF with r independent source labels for each of its original 4h three-literal clauses. Then:

$$
\forall G,b,r\quad W_{R_{\mathrm{mix341}}}(T^{[r]}(G,b))=4h-1.
$$

A **source-block deletion lemma** proves the lower bound: if k disjoint sets B_i of labelled source clauses each have the property that deleting all labels in B_i makes the CNF SAT, then every sound conservative at-most-two-antecedent refutation must use a source label from each B_i. Its connected root ancestry has q paid nodes and at least k distinct source leaves, whence 2q >= k+q-1 and q >= k-1. No unit-cost semantic oracle is permitted. This covers shared proof DAGs, adaptive rule choices, GF(2), LOCAL-CONVERT and paid conservative auxiliary gates, provided they meet the original R_mix341 soundness/source-transparency contracts.

The four clauses at each cubic vertex form a SAT-restoring **content class**: if all r copies of a class are deleted, prescribe its falsifying incident-edge assignment and solve the parity equations on connected G-v. Since cubic bridgeless G-v is connected, exactly the required single global parity consistency condition holds. This gives a model of every retained source and makes every block essential. The upper construction selects one source from each class, uses three paid AND3 nodes per vertex, and h-1 binary affine XOR nodes, giving 4h-1 exactly.

For r>=2, **every individual labelled clause and every individual source-literal sign flip is dispensable**, since an intact copy remains. The individual pivotality spectrum thus falls to zero although the true mixed proof minimum is unchanged. This falsifies using source singleton pivotality by itself as an exact or universal tight intrinsic-cost measure. It does not refute more sophisticated source-class invariants.

## Established starting bound and model firewall
Urquhart (JACM 1987) and Ben-Sasson--Wigderson (JACM 2001) supply exponential ordinary shared-DAG Resolution lower bounds on suitable signed Tseitin expander CNFs, of the form: for a specified unbounded bounded-degree graph sequence h_j and constants c>0,j0, for all j>=j0 every ordinary Resolution refutation has at least 2^(c h_j) lines. This is restricted to its exact expansion, sources and ordinary inference grammar. In cubic instances there are 3h/2 edge variables, 4h original clauses and Theta(h log h) signed binary-index source bits; the r-fold ordered replication needs Theta(rh log h + log(rh)) bits. The theorem is not an all-algorithm SAT-time lower bound, nor a lower bound for ER, Res(oplus) or the unchanged mixed system. The finite prisms here are not certified Resolution-hard expanders. The usual GF(2) and Cook ER shortcuts remain countercontrols.

## Falsifiers and results
F1: Repeating every original clause should lower W_R because no label is indispensable. **FALSIFIED:** group ancestry forces unchanged optimum.
F2: No single pivotal source implies easy constant-size proof. **FALSIFIED:** replicated family has W_R=4h-1 for arbitrary h.
F3: Arbitrary connected cubic graphs permit class deletion SAT witnesses. **FALSE without bridgelessness**, as a bridge can create a locally constrained parity boundary.
F4: The new exact cost is a superpolynomial machine lower bound or B3. **FALSE**: Gaussian elimination solves odd/even source in polynomial time, and proof cost is only linear in h.

The deterministic no-dependency Python producer passed 7,863 assertions over 20 combinations (K4 and prism 3,4,5,8; r=1,2,3,5), including 176 distinct content-clause-deletion SAT witnesses, complete paid AND3/XOR proof replay, even-charge SAT controls and 20 forged proof rejections. An independently written no-import Node truth-table checker passed 5,841 checks over 6 small fixtures, including original signed clause content, all class removals, r>=2 single-label deletion and sign-flip UNSAT controls, four malformed inputs and two forged proof headers. The published public JavaScript verifier executed 894 assertions over K4, prism3, prism4 and r=1,2,3. These are finite computational checks, not global minimum searches. Source class lower plus explicit upper establishes the all-size minimum.

## Explicit costs and bridges
Logical proof nodes: 4h-1. Original CNF bits: N_r=Theta(rh log(h+2)+log(rh+2)). Dense-row encoded proof evidence: O(h^2+h log(rh+2)) bits. Acquisition, construction, indexing, validation, output and all-phase peak memory are separate. Source streaming versus materialization and lazy representation require separate read/cost models. Proof discovery is excluded only from W_R minimum, not from any machine-time upper bound. No finite proof is converted by an uncharged exponential-output backtranslation.

B1 (for every fixed uniform total correct A, pointwise W_R <= poly_A(N+T_A(F))), B2 (worst-case all binary input strings), and B3 (SAT in P implies polynomial Wbar_R for the same fixed R_mix341) remain OPEN. Neither a superpolynomial mixed Wbar_R lower bound nor P != NP has been proved.

## Duplication check / external assessments
Read the approved Nov-2 refocus, issue #3, AGENTS.md, CODEX.md, repository skill, original R_mix341 at LSPV-2/341 blob c87acd11, peer LSPV-2/389 at d56f9de3 and /390 at ed6b2d40, LSPV-3/391 and /392, and LSPV-4/363. The prior LSPV-2/341 theorem already covers unduplicated optimal cost; /390 already computes singleton affine pivotality. This report claims novelty only for the duplicated-source class countercontrol. Searches: Urquhart 1987 expander Tseitin Resolution; Ben-Sasson--Wigderson 2001 width/size; Haken 1985 PHP; Cook 1976 ER; GitHub prior source-core, duplicate and cofactor reports. Literature sources were checked independently; there is no new academic novelty claim.

Grok actual file: GROKPROOF/2026-11-04_1322_PROGRESS.md, blob 0850246c. Its all-input charged FLMV contraction remains unproved; source-cut numerical hypotheses concern a restricted decomposition and cannot be borrowed as an arbitrary SAT lower bound. Claude actual file: research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727, gives restricted alternation-trading portfolio results, not B3. The older Claude-0266 review at blob 694c1c81 notes rejected spectral-invariant claims. These files were inspected, not treated as authority.

## Publication / role handoffs
Formal report: research/agents/lspv-3/2026-11-04_0524_LSPV-3_DUPLICATE_SOURCE_BLOCK393.tex
Public executable: experiments/arc/lspv3_393_source_block_duplicate.js
Raw: results/raw/arc/2026-11-04_0524_LSPV3_DUPLICATE_SOURCE_BLOCK393_raw.json
Reproduction archive contains independently implemented Python and Node programs with exact machine-readable outputs.
Root main.tex reconciled only inside BEGIN/END LSPV-3 OWNED, full Git blob readback required. Current write was conflict guarded by expected blob SHA 525e02f4 and returned blob 825d029b; reconciliation commit 95eec5b. No tasks, schedules, enabled states, role identities, historical artifacts or fixed proof-system rules changed.

LSPV-1: distinguish singleton input-bit pivotality from deletion-class necessity, and keep B3 quantifiers.
LSPV-2: test the class lemma against more general source encodings, ideally conservative gate views.
LSPV-3: establish which equivalence-preserving auxiliary/circuit transformations retain authenticated SAT-restoring classes; test a counterexample.
LSPV-4: fully charge source-class discovery and scanning in explicit and lazy encodings, including peak memory.
LSPV-5: attack the class-restoring hypothesis, source dependency IDs, and any illicit import from a restricted Resolution lower bound.

Next missing implication: a robust source/provenance structure surviving *all* legal representation switches and relevant to superpolynomial Wbar_R, plus the independently required B3 conditional bridge. The generic source-arity lemma remains only linear. P versus NP remains OPEN.
