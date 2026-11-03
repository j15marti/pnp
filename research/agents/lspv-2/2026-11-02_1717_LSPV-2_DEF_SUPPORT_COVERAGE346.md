# LSPV-2 DEF-SUPPORT-COVERAGE346: source-independent DEF and output-support audit

**November 2, 2026, 5:17 p.m. PST.** **PROVED/EXACT** within the explicitly specified source-independent-variable-DEF reading of the pre-existing Rmix341; **COMPUTATIONAL** for the independently checked finite source-partition enumeration; **OPEN** for any more powerful source-bearing-factor DEF interpretation, the worst-case superpolynomial mixed proof minimum, B3, and P versus NP.

## Fixed calculus and caveat

Inputs are general encoded CNF formulas, with SAT, UNSAT, and malformed strings handled separately. Original labelled clauses are free premises. Each derived proof-DAG node has at most two explicit proof-premise dependencies and unit cost, allowing shared intermediate proofs, temporary growth, exact resolution (RES), binary AND3 and affine GF(2) XOR, and separately charged local conversion/weakening. For the **VARDEF** interpretation, one charged conservative fresh-variable instruction y <-> g(a,b) introduces three locally authenticated clause slots for a named two-input Boolean gate on **variable/literal names**. It has no original-clause proof premises and any slot use must cite that paid DEF node.

A different operation, "in one inference define an auxiliary variable as a gate of two **source-bearing formula factors**," is NOT the same rule. If that broader rule was intended by a peer, the minimum below is not certified for the union until its precise inference semantics and checker are fixed. This is the discrepancy identified by LSPV-3 SPLIT-HARDNESS-TRANSPORT344; it is not permission to change the common calculus silently.

## General rigidity lemma: saturation of the source lower bound

**Theorem (PROVED/EXACT).** For any clause-minimally UNSAT formula with m indispensable sources in a conservative proof calculus with at most two explicit proof premises per positive-unit-cost derived node, q >= m-1. If q=m-1, every used inference has exactly two named premises; its entire contradiction ancestry, considered as an undirected graph, is a tree. All m original clauses occur once; a paid zero-premise VARDEF, unary conversion, or sharing that reconverges is impossible.

**Proof.** The connected ancestry graph on m original sources and q derived nodes has at least m+q-1 edges. At most two proof-premise edges enter each derived node, giving at most 2q edges. Thus q>=m-1. Equality forces indegree two at every derived node and exactly m+q-1 undirected edges, hence a tree. A zero-premise paid DEF reduces the indegree sum and makes equality impossible. The claim does **not** eliminate a hypothetical source-bearing binary DEF, which would have different semantics.

## Independently checked finite optimum

Use the original six clauses of G342:

    C0 = (-3  1  4)
    C1 = (-1  2)
    C2 = ( 1  3)
    C3 = (-4 -3)
    C4 = (-2 -1  3)
    C5 = (-2  4)

Every one of the 16 full assignments violates at least one clause. The six source-deletion model counts are **(1,3,3,3,1,1)**. All **14 single signed-occurrence inversions** yield SAT controls.

The earlier G342 exact-5-inference exclusion searched disjoint-source binary trees using exact clause resolution, exact affine XOR, and AND3 when the **union of the premise supports** had at most three variables. This audit strengthens the last operation: it allows a conjunction whenever the **output Boolean truth function** has essential support at most three, even if the premises jointly mention four variables.

The stronger rule adds **four** candidate AND operations in the full dynamic program. With exact equivalent clause and affine aliases supplied as a free lower-bound relaxation, every disjoint-source binary inference tree is exhaustively enumerated through **63 nonempty source subsets**. For subset sizes one through six, the independently checked numbers of resulting Boolean functions are

    6, 18, 46, 84, 112, 54.

The full set has **54** terminal truth functions, **none identically false**. The Node producer examines **844** possible operand pairs and records **566** generated outputs under the strengthened relaxation. The separate Python implementation reproduces the subset counts, 844 pairs, zero contradiction, and all source SAT/deletion/flip controls.

By the rigidity lemma, any five-node refutation in the declared VARDEF calculus must be one of these binary source-once trees: there is no room for a charged independent DEF or unary conversion. A separately verified six-node resolution DAG reaches the empty clause using pivots **(4,3,4,3,2,1)**, reusing source C3. Consequently

    W_Rmix341^VARDEF(G342) = 6 > 5 = mu(G342)-1.

This is a fully bounded finite optimum with a mathematical coverage argument over the **specified** rule syntax. It is **not** a claim for any unformalized two-source-factor DEF. If such a rule is added, the safe current statement for that larger system is **5 <= W(G342) <= 6**.

As a positive control, H342's six-clause minimally UNSAT source reaches contradiction with **five** mixed AND3/RES steps in the same strengthened search. The K4 even/odd parity controls have 8/0 satisfying models. The Node program rejects eight malformed structures and one corrupted resolution trace. The independent no-import Python checker records **45 assertion groups** and independently verifies all six resolution pivots.

## Three falsifiers and current dispositions

1. **A four-variable-premise / three-variable-output exact AND3 shortcut defeats G342.** FALSIFIED in complete finite enumeration: four newly admitted operations, no contradictory terminal.
2. **A paid conservative variable-gate DEF appears in a minimum m-1 inference proof.** FALSIFIED by the general source-capacity lemma; a different source-bearing-factor DEF is **OPEN** pending a fixed rule/checker.
3. **Mixed-system bit-pigeonhole formulas retain the large Res(XOR) minimum.** FAMILY FAILURE: the LSPV-3 BPHP-FULL-COOK-CERTIFICATE346 gives an explicit polynomial RES+DEF proof compiler for these sources; LSPV-5 REFEREE299 independently audits the syntactic ER simulation. Do not infer mixed hardness from Braun's September 2026 restricted Res(XOR) result.

## Logical versus machine resource ledger

For G342, the logical minimum is **six distinct paid nodes**. The exact optimizer's 844 operand tests, 63 subset accesses, generated states, grammar acquisition, proof checking, failed candidates, source/index reads, and host execution are **outside** that minimum and must be paid in an implemented solver upper bound. In the local reproducibility archive, Node producer host execution was 0.04 seconds with 32,368 KiB peak RSS, and the separate Python verifier was 0.78 seconds with 96,012 KiB peak RSS. These are host-level controls, not matched-machine FLMV bounds. Source proof encoding length and scheduled storage/retrieval are separate from six logical nodes. For any claimed recursive space contraction, retain s' <= max{rho,eta,lambda,lambda*s} with rho covering all phases, including allocate-then-free preprocessing.

The fixed universal target remains Wbar_R(N) for **encoded bit length N**; no superpolynomial mixed-system lower bound was established. B1, B2, and the weakest sufficient B3 remain **OPEN**. P=NP and P!=NP remain **OPEN**.

## Corpus and literature audit

Read the verified 12:04 PST worst-case minimum five-role handoff, issue #3, AGENTS.md, CODEX.md, the pnp-research skill, original LSPV-2 G342/MACRO345, LSPV-3 SPLIT-HARDNESS-TRANSPORT344 and BPHP-FULL-COOK-CERTIFICATE346, and LSPV-5 EXTENSION-SIMULATION-BARRIER-REFEREE299. Checked public research on Resolution automatization (Atserias & Müller, arXiv:1904.02991), Cook--Reckhow proof systems (1979), and Braun's 2026 bit-PHP Res(XOR) preprint (arXiv:2609.23015). Queried github.com/openai for SAT/Resolution implementation matches and j15marti/pnp for G342, Rmix341 and guard/substitution work. OpenAI code results were unrelated to the specific mixed proof rule. Direct unauthenticated web access to the private project issue/handoff returned 404; authenticated GitHub connector reads succeeded. No novelty is asserted from negative search.

**Next exact step:** have all roles jointly sign an unambiguous DEF syntax, including whether source-bearing formula-factor inputs are legal, and add an independent finite checker covering every such operation. Only then promote or retire the G342 mixed exact-six minimum. Separately seek a growing nonaffine hard family for the **entire** fixed combined calculus and a genuinely proved B3 bridge.

**Artifacts:** role-owned local full LaTeX report and Python/Node independent outbox in the companion reproducibility archive. GitHub compact rerunner: experiments/arc/lspv2_346_def_support_coverage_compact.js. GitHub machine-readable summary in results/raw/arc/2026-11-02_1717_LSPV2_DEF_SUPPORT_COVERAGE346_public.json.

**Sources:** Cook & Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 1979; Atserias & Müller, *Automating Resolution is NP-Hard*, arXiv:1904.02991; Braun, *An Exponential Lower Bound for the Bit Pigeonhole Principle in Resolution over Parities*, arXiv:2609.23015 (restricted preprint claim).