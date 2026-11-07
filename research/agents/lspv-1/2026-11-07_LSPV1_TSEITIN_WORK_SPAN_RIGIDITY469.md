# LSPV-1/469 | Exact mixed Tseitin work-span rigidity and binary-ancestry excess identity

**Date:** 2026-11-07 PST. **Role:** LSPV-1, Route B. **Classification:** PROVED/RESTRICTED for the *declared semantic, source-explicit, unit-paid, at-most-two-antecedent* R_mix341 model of LSPV-2/341 (independent formal review pending); COMPUTATIONAL for five original-source signed strict-3CNF replays. The historical accepted-byte R_mix341 grammar has NOT been authenticated or executed. P versus NP OPEN.

## IDEA: hypothesis and falsifiers

Hypothesis: On the existing **published Resolution-hard cubic odd-Tseitin families**, the original LSPV-2/341 source-indispensability and binary-arity argument forces more than the scalar lower bound q >= 4h-1: every work-optimal legal proof is structurally a full binary tree, and a balanced AND3/GF(2) construction attains the absolute minimum logical critical-path span. This is an upper/lower control, not a strategy to artificially exclude mixing or sharing.

Precise falsifiers: (1) a legal m-1-node refutation with an active unary rule, zero-parent paid definition, or genuine reconvergent sharing; (2) a missing original source clause in the ancestry of a sound refutation despite the /341 deletion-satisfiability lemma; (3) an illegal AND3 three-variable annotation or a balanced XOR join needing more than two parents; (4) a shallower all-source proof despite the two-parent limit. Status after proof and finite controls: none survives under the **stated** model. These are not falsifiers of arbitrary proposed stronger rule systems.

## SEARCH: actual source and corpus audit

Governing local sources: root `proof1.txt` (preflight blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`), `proof2.txt` (preflight blob `7ca014e3d0d1ec04a7e6631cbd468b9861f3d76d`), issue #3 including its current thread, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, and governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (blob `c3889a3e`). **Fixed original declared rules** were read at `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`). Their 341 source-deletion proof and 4h-1 minimum are **existing prior results**, not rediscovered or claimed as novel. The present distinct result is the exact excess decomposition, optimality structure and independently attained span.

Relevant peer audit: `research/main/2026-11-05_0348_MAIN_RMIX341-CANON1-CHECKER-B3-REFEREE360.md` (blob `8719eba6`) explicitly warns CANON1 is not historical byte grammar; `research/agents/lspv-3/2026-11-04_1724_LSPV-3_PORT_COHERENCE_GRAMMAR406.md` (blob `4d2abf92`) audits freshness and provenance; `research/main/2026-11-07_0048_MAIN_CONTEXT_TYPED_AFFINE_UNION_REFEREE405.md` (blob `88bbe158`) warns against equal-row cross-context sharing; `research/agents/lspv-1/2026-11-07_0008_LSPV1_SHARED_DAG_NONADDITIVITY468.md` (blob `e5357688`) establishes separate abstract sharing benefits in another model. Actually located `GROKPROOF/2026-11-07_0819_PROGRESS.md` and `research/agents/claude/world-ledger/README.md`; neither closes P2-B1 or P2-B2. A guessed /341 peer Markdown path returned 404; authoritative .tex was subsequently retrieved, not silently substituted.

External source review and targeted search: Urquhart (1987), *Hard Examples for Resolution*, JACM 34:209-219, DOI 10.1145/7531.8928, provides exponential **ordinary Resolution** lower bounds on expander-derived Tseitin clauses, not on R_mix341. Braun, arXiv:2609.23015v2 (3 November 2026), provides a separate **Res(XOR)** bit-PHP bound with model-specific proof and encoding. Cook–Reckhow (1979) relates proof systems and efficiency, not B3 for the named mixed calculus. Direct public GitHub paths inspected: `konard/p-vs-np/README.md` blob `0e0ec77` (explicitly says NP subset P unknown); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea` and `REVIEW_ADDENDUM.md` blob `6a7cc2f8` (restricted exact LP/code results); `meelgroup/frat-xor/format.md` blob `986a21aa` (source-indexed XOR proof format); `tanyongkiam/cake_lpr/README.md` blob `e94f45e9` (certified checker scope); and `openai/math/README.md` blob `cc5b0a03` (mixed stages of validation). Direct `konard/p-vs-np/proof_status.md` returned 404; no result inferred from its absence. Google-branded search was unavailable; general indexed web search and direct GitHub reads were used. No paper, checker or repository provides an all-rule R_mix341 lower bound.

## ITERATE: exact theorem

**Theorem 469.1 (binary source-ancestry excess identity).** Fix a sound source-explicit refutation calculus where the only free assumptions are the authenticated original CNF clauses; every paid node has at most two explicitly cited parents, with nonnegative unit cost. Let F have m distinct individually indispensable source clauses. Take the entire acyclic **trimmed ancestor multigraph** of any legal refutation (retain one undirected edge for every parent occurrence), with m original source vertices and q paid vertices, and let d(v) be the number of parents of each paid vertex. Define

$$
E=\sum_{v\,\mathrm{paid}}d(v),\quad
\mu=E-(m+q-1),\quad
\delta=\sum_{v\,\mathrm{paid}}(2-d(v)).
$$

Then the undirected ancestor multigraph is connected, so \(\mu\ge0\); binary arity gives \(\delta\ge0\); and the **exact identity** is

$$
\boxed{q-(m-1)=\mu+\delta.}
$$

**Proof.** Soundness and clause indispensability force each of the m source clauses into the contradiction's ancestry: otherwise the used clauses would remain satisfiable after removing an absent indispensable clause, and conservative definitions cannot create a contradiction. Every ancestral node has a directed path to the unique final contradiction, so the underlying undirected multigraph is connected and has m+q vertices and E edges. Thus its cyclomatic rank is \(\mu=E-(m+q-1)\ge0\). Every original vertex has no cited parents, so \(E=\sum d(v)=2q-\delta\). Rearranging gives the boxed identity. This counts each distinct paid inference vertex once; parallel parent occurrences are kept as multiedges. QED.

**Rigidity corollary.** \(q=m-1\) iff \(\mu=\delta=0\). Consequently **every work-optimal refutation** for any source with an attained m-1 bound has exactly two parents per paid node and an undirected tree as its ancestry graph. Since every ancestral vertex reaches the unique sink, every other vertex has exactly one downstream consumer; neither paid shared-lemma reconvergence nor even repeated use of an original clause occurs in an optimum. Any genuine reconvergence or one-parent conversion in such a refutation increases q by at least one. This does **not** mean sharing never helps in other source families, as /468 demonstrates.

**Theorem 469.2 (simultaneous exact work and ideal span for odd cubic Tseitin).** Let G be finite connected simple bridgeless cubic with h vertices; F_(G,chi) has m=4h original signed strict-3CNF clauses forbidding wrong-parity triples and odd total charge, with 3h/2 original edge variables and N=Theta(h log h) indexed source bits. Use the declared original R_mix341 rules: unit-paid binary RES/AND3/GF(2)/LOCAL-CONVERT/fresh conservative DEF, and original sources free. Then

$$
\boxed{W_R(F_{G,\chi})=4h-1,\qquad
D_R^{\mathrm{ideal}}(F_{G,\chi})=\lceil\log_2(4h)\rceil
=2+\lceil\log_2 h\rceil.}
$$

The work equality is the **existing** LSPV-2/341 theorem; the exact minimum ideal span and all-optimum tree rigidity are the new consequences. **Lower bound on depth:** every rule has at most two antecedents, so a depth-d node depends on at most \(2^d\) distinct original source clauses. All 4h indispensable sources must contribute to the final false conclusion. Hence d >= ceil(log2(4h)). **Matching legal upper bound:** for every cubic vertex, conjoin its four signed original clauses as two parallel AND3 steps and one more AND3 step, all exact truth tables over the same three original edge variables. At depth 2 the output is exactly its parity equation, certified by eight-row exhaustive local equality. Binary GF(2) sum all h certified vertex rows through an ordinary balanced binary tree of h-1 paid XOR steps, of height ceil(log2 h). Every edge cancels twice and odd total charge yields 0=1. Total paid work 3h+(h-1)=4h-1 and depth 2+ceil(log2 h), simultaneously tight. Every paid node is a distinct inference and the derivation is a tree. No free split, weakening, semantic oracle, or new historical syntax is assumed. QED.

**IMPORTANT MODEL QUALIFICATION.** The theorem is about the historical **declared semantic** binary-parent logic, not an accepted-byte proof in a fully specified historical parser; actual proof bits, retrieval, construction and machine execution are additional. The graph family is hard for *ordinary Resolution* under the published expander hypotheses, yet easy in the stronger declared mixed calculus. No all-algorithm hardness is inferred.

## Computational and adversarial controls

Published exact script: `experiments/arc/lspv1_469_tseitin_work_span.js`, verified V8 execution of the **read-back published bytes**, blob `895c0bde77e848c7261985a23f0b980428cfe24a`. Raw output: `results/raw/arc/2026-11-07_LSPV1_469_WORK_SPAN_RIGIDITY.json`, blob `e73010c9d724722f092b10176b7bf4441d351286`, exactly reproduced in independent readback. Counts:
- K4: 16 original clauses, q=15, ideal depth 4; even-charge 8 models; 16 independent source-clause deletion witnesses.
- K3,3: 24 clauses, q=23, depth 5; even-charge 16 models; 24 deletion witnesses.
- Cube: 32 clauses, q=31, depth 5; even-charge 32 models; 32 deletion witnesses.
- Petersen: 40 clauses, q=39, depth 6.
- Prism6: 48 clauses, q=47, depth 6.
All five signed odd strict-3CNF proofs use balanced AND3/GF(2), every original source authenticated, and exactly 2q ancestry edges; all have mu=delta=0. Seven corrupted controls were rejected: altered original signed source, forged affine annotation, forged XOR mask, false final charge, cyclic parent, missing source dependency, and forged depth. Two separate abstract acyclic topology controls demonstrate one unary deficit (mu,delta)=(0,1) and two genuine reconvergent cycles (2,0); they are NOT falsely presented as native SAT derivations. Exhaustive SAT/UNSAT and clause-deletion evaluation was carried out only on cases with <=12 edge variables; no false claim of exhaustive check for the larger two graphs.

The script is a standalone Node-compatible pure-JS producer/checker, but the actual executed environment was a V8 isolate (`new Function`), **not** the historical checker and not a separately executed Node CLI. The published complete script was refetched and evaluated exactly against the published raw JSON: PASS.

## All-phase work / space / bit ledger

The **logical** minimum is 4h-1 unit paid nodes; the ideal parallel span is ceil(log2(4h)) with unlimited processors and zero-cost original source inputs. A dense, fully emitted row at each GF(2) node can use O(h) bits; naive full certificate statement/ID serialization is bounded by O(h^2 log h) bits, not 4h machine steps. Source creation/sign checks, source-byte authentication, per-vertex truth-table checks, GF(2) mask arithmetic, allocation, intermediate row storage, branch/strategy selection, hashing, proof output, parsing, verification, source/index/head access, readback and publication are separate paid phases. The demonstrated script keeps its full proof and model vectors in memory, with O(h^2) bit-scale representation excluding JavaScript runtime overhead. A sequential generator can run in polynomial bit time, for example O(h^2 log h) with dense elementary masks. No claim that an actual same-machine FLMV time/space schedule achieves the ideal parallel span or q logical work. No precise host RSS/timing was measured; no fabricated measurement. Search/discovery costs are intentionally omitted **only from ideal minimum W**, not algorithmic implementation. Source-reduction size N=Theta(h log h) assumes indexed variable names and no duplicative padding.

## Proof-chain decision and precise remaining gap

Material new node: **[P2-B12]** for the binary-ancestry excess identity and exact ideal span. Its dependencies are [P2-D1], [P2-D2], [P2-B1] and original /341. [P2-D1] is STILL OPEN because historical accepted-byte grammar is underdetermined. [P2-B1] and [P2-B2] remain OPEN. The simultaneous optimum is a **family upper-bound / source-structure control**, not a universal lower bound; B3 is untouched. The Route A FLMV same-machine all-input contraction remains [P2-A2] OPEN. No edits to other roles' manuscripts, `main.tex`, automation tasks, weights, titles, enabled states, time zones or five-role allocation.

**Actual advance:** exact excess decomposition for any sound binary source-explicit calculus with indispensable clauses; every optimal 4h-1-node Tseitin proof must be tree-shaped; a legal balanced derivation attains the provable minimum logical span in addition to minimum work.

**Verification:** five original strict-3CNF finite controls + seven hostile modifications, exact published script V8 readback replay PASS. **Publication:** report/code/raw/handoff and material tracker update are separately verified before final report. **Remaining gap:** source-authenticated historical accepted-byte R_mix341 rules, superpolynomial all-rule minimum, noncircular B3. **P versus NP OPEN.**
