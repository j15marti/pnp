# TMR-3/056: A fully charged succinct Tree Evaluation interface, and a compact QBF family defeating generic query-volume claims

**2026-11-15 16:41 PST | TMR-3 / PNP Time-Space Tradeoffs | Track B | SUCCINCT-QTREE056**

**Status.** PROVED/EXACT in the precisely stated uniform succinct Boolean-tree source/access model, subject to independent mathematical review. The classical TQBF PSPACE-completeness theorem is KNOWN. The explicit canonical family and charged representation/short-circuit counterexample are project-specific restricted results, with no claimed literature priority. Finite hosted-V8 checks are COMPUTATIONAL. No new arbitrary nonassociative Tree Evaluation evaluator, generic space simulation improvement, SAT lower bound, or P-versus-NP separation is asserted. **P versus NP remains OPEN.**

## 1. Exact candidate and precommitted falsifiers

**Named dependency C3-QUERY-VOLUME and C3-GENERIC-TREE-INTERFACE** in the selected pipeline: authenticated finite input -> exactly generated virtual node/leaf descriptors -> genuine adaptive evaluator calls -> correct root bit -> charged sequential time and simultaneous writable workspace. TMR-3/054 proves this chain for an associative finite-state comb with Q=B; TMR-3/055 shows that a public head schedule does not provide canonical P-complete work values. This run asks whether an analogous *generic* promise of polynomial query count follows from compact authenticated node generation. The answer is NO for the explicit left-first evaluator: even a source that can be recognized and solved in logarithmic workspace can force its query volume to be exponential. It additionally calibrates the general succinct-tree evaluator against TQBF.

F1 (source/representation): a compressed tree descriptor must not be treated as a materialized input with an exponential-size leaf table, and a read-only node-path port must not be counted as a free writable address buffer.

F2 (query semantics): a lower bound against left-first recursive short circuit, or against a black-box leaf oracle, may be evaded by a source-aware solver and cannot be promoted to arbitrary correct algorithms.

F3 (quantifiers): the 3CNF auxiliary variables must be existentially quantified *after* all original alternating variables, with functional unique extensions; otherwise the claimed root bit may change.

F4 (complexity target): polynomial-time evaluation of every authenticated succinct alternating AND/OR tree would imply P=PSPACE; the existing space-only Williams/Cook--Mertz simulation makes no such polynomial-time promise. A conditional class collapse cannot be used as an unconditional runtime/space lower bound.

## 2. Concrete source grammar, uniform parser, and charged node access

For integers k,m >=1 set w=ceil(log2(k+1)). An encoded word consists of unary 1^k 0, unary 1^m 0, k quantifier bits q_1...q_k (1 is existential OR, 0 is universal AND), and m clauses of three signed literal records, each one sign bit followed by exactly w index bits representing an integer in [1,k]. The sign bit 1 means negation. Repeated indices, opposing literals and unit clauses written as repeated triples are legal. The exact length is

    N=2k+m+2+3m(w+1).

A fixed total parser rejects invalid delimiters, zero counts, nonbinary symbols, out-of-range/zero indices, truncated records and trailing data. Counters and repeated read-only source sweeps authenticate the source in O(N^2) bit operations and O(log N) writable space in a conventional constant-tape model. No gate table is preloaded.

The source represents QBF(q,F) where F is the conjunction of the authenticated clauses. Consider the COMPLETE full binary tree of height k. At a node with depth d<k and binary root-to-node assignment path p of length d, the gate is OR if q_{d+1}=1 and AND otherwise. Its two children have descriptors p0 and p1. At depth k, the leaf is F(p). All descriptors are uniform and their exact lengths are at most k+O(log k).

With the **descriptor already on a separate read-only port**, a fixed transducer returns any gate, child descriptor bit, or leaf bit in O(N^2) sequential steps and O(log N) *additional* writable space: for each literal it rescans the read-only path to obtain the selected assignment bit. Outputting an entire child descriptor costs O(k) real output transitions. The original source length and all source/path head movements are included. If the caller needs a persistent or rereadable node path, the caller must store and pay for up to k path bits. The logarithmic bound is a per-query auxiliary bound, not a complete-tree evaluator's space bound.

A fixed blank-work-tape, left-first depth-first short-circuit evaluator stores one mutable k-bit assignment/path and O(k) branch/return information. It makes at most

    Q <= 2^(k+1)-1

node requests, including at most 2^k leaf requests. Parsing and all actual repeated node generation give the *same-run upper budget*

    T_all = O(2^k N^2),    S_peak = O(k+log(N+2)).

The output is exactly one QBF truth bit; malformed inputs are rejected. This is exponential-time, polynomial-space evaluation, not a new sublinear-height evaluator. A local input-head implementation may rescan the node path instead of receiving it as free random-access memory; the O(N^2) per-request budget is conservative enough to pay these moves.

**Correctness.** A depth-k leaf is F(a) by literal evaluation. Induct on remaining depth: existential quantifiers take the disjunction of the two descendant truth bits and universal quantifiers take the conjunction. Therefore the root is QBF(q,F), on every authenticated source. Malformed source rejection is disjoint from valid-source evaluation. The same fixed machine stores its own recursive path and outputs its own result, so T and S belong to one execution.

## 3. Class calibration: the authenticated succinct-tree language is PSPACE-complete

Membership in PSPACE follows from the preceding depth-first algorithm since k<=N. For hardness, start with prenex TQBF, the classical PSPACE-complete problem. Represent its quantifier-free matrix by a polynomial-size binary Boolean circuit. Introduce one new existential gate variable per circuit gate, append all these existentials *after* the original quantifier prefix, and impose the standard functional width-three Tseitin clauses and an asserted output gate. For each original assignment there is exactly one gate extension satisfying all gate equations, and the asserted output is satisfied iff the original matrix evaluates to true. Therefore

    Q_1 x_1 ... Q_n x_n phi(x)
      iff
    Q_1 x_1 ... Q_n x_n exists z_1 ... exists z_g H_phi(x,z).

The transformation produces the authenticated fixed-three-literal-record grammar above in polynomial bit time, padding short clauses by repeated literals, without changing the quantifier order. This is a conventional reduction and does not represent an innovation in PSPACE completeness.

**Exact consequence.** An *all-valid-source*, deterministic polynomial-in-N-time algorithm evaluating this succinct tree model, including every local node access and construction expense, would put PSPACE in P. Hence it would imply P=PSPACE and in particular P=NP. This is **CONDITIONAL**, not an impossibility proof. It says nothing against a space-saving but exponential-time evaluator, and is not a hardness transfer to the more restricted Williams block-respecting image without an independently proved representation/compiler.

## 4. A small authentic Q3CNF family with exponential queries for a specified evaluator but an easy direct decider

Fix n>=1, any original quantifier word q in {OR,AND}^n, and a desired root bit g in {0,1}. Put e_i=0 for OR and e_i=1 for AND. Introduce original variables a_1,...,a_n and auxiliary variables z_0,...,z_n, with prefix

    Q_1 a_1 ... Q_n a_n  exists z_0 ... exists z_n.

Impose z_0=g; for i=1,...,n impose the functional gate equation

    z_i = (a_i ? z_(i-1) : e_i);

and impose z_n=1. Each gate equation is encoded by the FOUR genuine three-literal truth-table clauses

    (a_i != u) OR (z_(i-1) != v) OR (z_i = (u ? v : e_i))

for u,v in {0,1}, with literal equalities translated into signed ordinary clauses. The two unit requirements use repeated ternary literals. Thus there are exactly k=2n+1 declared variables, m=4n+2 three-literal clauses, and total encoded length N=Theta(n log n). Every original a has exactly one extension satisfying the functional gates and z_0 condition; with the terminal pin z_n=1 this extension is satisfying iff f_q,g(a)=1.

Define f_q,g(a) by starting at y=g and scanning i=1,...,n, resetting y to e_i whenever a_i=0 and leaving y unchanged whenever a_i=1. In particular f is determined by the **last zero coordinate**, if one exists, otherwise g. Its value is computable in O(n) bit operations and O(log n) auxiliary writable space from the original assignment and q.

**Lemma 056-A (root bit and full original-prefix visitation).** For every n,q,g the complete quantified 3CNF above has truth value g. Moreover, an ordinary recursive evaluator which visits branch a_i=0 before a_i=1 and short-circuits on Boolean OR/AND must reach *every one* of the 2^n original-assignment prefixes (depth n), no matter how it evaluates each existential auxiliary suffix, provided it correctly returns the suffix result.

**Proof.** At a node whose target output is y, induction on the remaining original variables shows that setting the next original bit to zero yields the neutral child value e_i, while setting it to one yields y. Consequently OR(0,y)=y and AND(1,y)=y, so the parent output is y. The left child is neutral and can never short-circuit its parent; both child subtrees must be entered. Induction from the root gives exactly 2^n visits to depth n and root value g. The functional Tseitin clauses make each depth-n suffix return f_q,g(a), proving the source-level statement. QED.

This gives at least 2^(n+1)-1 real node-entry queries for **that particular evaluator**, including all its original-variable internal nodes, although the authenticated source is only Theta(n log n) bits long. However, one fixed alternative recognizer can verify the entire special-family grammar, regenerate and compare the source's clauses from its quantifier prefix and candidate g, and then return g. Using repeated source scans and O(log N) counters this takes polynomial(N) time and O(log N) workspace. A source-aware algorithm therefore *legally bypasses* the enormous query volume. Nothing here lower-bounds arbitrary correct QBF or SAT algorithms. The family is a hostile control for an attempted "query complexity of one evaluator implies unavoidable computation" transfer.

## 5. Separate genuine black-box leaf-query theorem

For an arbitrary, independent black-box Boolean leaf table on a complete all-existential binary tree of height k, its root is the OR of 2^k leaf bits. Any deterministic leaf-query algorithm must query all 2^k leaves on the all-zero oracle: if some leaf remains unread, changing that one unseen bit to one leaves the transcript unchanged but flips the correct root answer. This is an exact all-oracle query lower bound. It is **NOT** a lower bound in the encoded-Q3CNF source model: different leaf tables may have small, recognizable descriptions, and reading the source can reveal the answer without visiting leaves. No oracle result is transferred to native SAT computation without an exact source-to-oracle simulation that charges access and preserves the quantifiers.

## 6. Same-realization resource and model budget

| Stage/interface | Total bit-time upper charge | Peak writable bits/cells (same machine) |
|---|---|---|
| Source parse and complete validation | O(N^2) including head resweeps | O(log(N+2)) |
| Virtual node-gate/child-bit service, readonly descriptor supplied | O(N^2) per request (usually less) | O(log(N+2)) **additional**; path descriptor not silently free |
| Virtual CNF leaf evaluation | O(N^2) per request including literal-index/path searches | O(log(N+2)) additional |
| Explicit left-first DFS evaluator | Q<=2^(k+1)-1 calls, O(2^k N^2) total time | O(k+log(N+2)), including mutable path, branch/return data and provider scratch |
| Compact hard-query family source-aware recognizer | O(N^3) conservative verified-regeneration budget | O(log(N+2)) counters; no full source copy |
| Output and malformed case handling | One terminal bit, validation included | included above |

Read-only source and query ports are explicitly declared; obtaining or retaining a query descriptor is charged to the caller. The node generator's logarithmic *auxiliary* workspace cannot be substituted for the whole DFS machine's O(k) workspace. The code checks logical node calls and source syntax; it is NOT a native step-by-step locally headed Turing-machine compilation or timing measurement. No cost is borrowed from another machine or simultaneous network. No polynomial-time generic simulation is claimed.

## 7. Four mandatory gates, legal controls, barriers

| Gate | Status and justification |
|---|---|
| DISJ sanity | **PASS restricted.** No static rank-to-work inference. Horn, 2-SAT, affine, independent-product, bounded-treewidth, unique-solution and trivial recognizable-source shortcuts remain legal. |
| Relativization | **NOT APPLICABLE WITH REASON** to an unrestricted separation, none claimed. The black-box lower bound is explicitly oracle-scoped. Nonrelativizing P-vs-NP, algebrization and Natural Proofs bridges remain OPEN. |
| Simultaneous DTISP | **PASS in declared end-to-end QBF evaluator; OPEN for Williams/FLMV/SAT transfer.** One algorithm has T=O(2^k N^2) and S=O(k+log N). No strict small-space forbidden-box pair follows. |
| Configuration counting | **PASS as deterministic upper-bound consistency only.** A complete deterministic halting run obeys T<=2^{O(S+log N)}, with physical input heads included. The class collapse is conditional, not an unconditional work/space lower bound. |

The compact hard-query input is precisely a legal cheap-path control. Query volume for a fixed evaluator, an enormous implicit tree, and the all-oracle information lower bound cannot be combined to exclude adaptive source-aware algorithms. The special nonassociative general Tree Evaluation, the Williams image-specific node compiler and any improved height-exponent theorem remain OPEN. Historical /341 is FAIL as a full source-bound UNSAT authority; /386 is RESTRICTED. No new quantum claim, majority-threshold transfer or numerical Allender exponent is made.

## 8. Executed finite audit, corpus reconciliation, publication status

Hosted V8 executed **11,541 exact assertions, zero failures**, and a second deterministic execution produced byte-identical result objects. The executable checked 896 independent authenticated generic Q3CNF instances against both a truth-table bottom-up quantifier elimination and left-first short-circuit traversal; 98 generated compact Q3CNF instances including 16-prefix and 64-prefix controls; 168 exhaustive unique-extension examples; 510 single-flip black-box OR adversaries; and five malformed-source rejections. Seed 20261115, executable revision tmr3-succinct-qtree056-v1. All generated source words obey the exact N ledger and are parsed afresh. The test evaluates node queries as logical oracle calls; no native tape runtime or Lean/kernel verification is claimed. Finite tests are COMPUTATIONAL.

New files: research/agents/tmr-3/2026-11-15_1641_TMR3_SUCCINCT_QTREE_QUERY_FIREWALL056.md (this report), experiments/tmr/tmr3_succinct_qtree056.js, results/raw/tmr/2026-11-15_1641_TMR3_SUCCINCT_QTREE056_V8_RAW.json, updated root main3_PNP_TIME_SPACE_TRADEOFFS.tex (on a stacked branch based on PR #169), and compact preserved-history handoff. Review/merge/readback must not be confused with one another.

**Corpus reviewed.** New end-to-end directive first, compatible SAT-compression directive, current AGENTS/CODEX/skill, full main3 on the unmerged TMR-3/055 branch, peer main1/main2/main4/main5 current sections, all five peer handoffs, TMR-3/054 and /055 original reports and PR metadata, TMR-5 independent full-head CVP audit, targeted repository search on succinct tree/QBF and earlier implicit-source firewalls, and original Williams 2025 presentation of block-respecting implicit Tree Evaluation. No retired proof trackers were read. Earlier TMR-3/055 already exhibits P-complete work-bit access; this run is a *different* PSPACE-complete succinct-tree evaluator and an explicit compact, easy, exponential-query source family. Neither result overturns Williams's established space-only simulator.

**Unavailable/unexecuted:** no local repository checkout or updated preflight was run; no native tape microcode test, full LaTeX build, model-independent mathematical review, or general Tree Evaluation evaluator was executed. The existing historical root main.tex is not a required active tracker. Claim status and actual publication remain distinct.

**ONE NEXT LOAD-BEARING LEMMA:** characterize the **block-respecting Williams image** of authentic canonical computations well enough to prove or falsify a bound on both the query count Q and the cost of each virtual work-value access for a specified nonassociative evaluator. The PSPACE-complete generic succinct tree is a sound cautionary superfamily, not a proof that the Williams-special image is PSPACE-hard under a low-cost transfer.

### Sources

[1] R. R. Williams, *Simulating Time With Square-Root Space*, STOC 2025, Section 3.2 and Theorem 1.1. https://doi.org/10.1145/3717823.3718225 ; https://arxiv.org/html/2502.17779

[2] Classical TQBF PSPACE-completeness, e.g. University of Washington CSE531 Lecture 6, Anup Rao, 2012, https://homes.cs.washington.edu/~anuprao/pubs/CSE531Winter12/lecture6.pdf ; University of Illinois Chicago CS505 Lecture 9, https://www.cs.uic.edu/~block/courses/cs505-spring2025/lecture-09.html

[3] R. E. Ladner, *The Circuit Value Problem Is Log Space Complete for P*, SIGACT News 7(1), 1975, https://doi.org/10.1145/990518.990519 ; referenced as the TMR-3/055 prior scope, not a replacement for the QBF argument.

[4] TMR-3/054, *End-to-end canonical streaming-graph reconstruction with charged virtual access*, original report on stacked PR #164.

[5] TMR-3/055, *P-complete canonical work values with public work-head movements*, original report on stacked PR #169.
