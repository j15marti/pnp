# LSPV-5/REFEREE386: bridge-cut near-floor topology and complete typed replay

**Role:** LSPV-5 independent red team (Route B)  
**Pacific timestamp:** 2026-11-06 05:48 PST  
**Status:** **PROVED-RESTRICTED** topology lemma and its application; **COMPUTATIONAL** exhaustive finite source/core and trace audit; global mixed minimum, B1/B2/B3, and P versus NP remain **OPEN**.

## 1. Idea -> search -> iterate

### Initial falsifiable idea

LSPV-1/445 gives a 36-source minimally UNSAT bridge-cut Tseitin core, the generic binary-ancestry floor $35$, and a 37-node native mixed derivation.  I attempted to close or sharply localize the two-node gap.  The prediction was that a pruned paid ancestry at the floor has no room for unary exports or reconvergence, and that every 36-node candidate has exactly one such unit of excess.

Precise falsifiers were:

1. the claimed 36-source core is not UNSAT or is not source-minimal;
2. a legal 35- or 36-node trace evades the topology accounting;
3. the 37-node trace uses unauthenticated sources, a false LOCAL implication, wrong affine rows, misoriented Resolution, or double-counted sharing;
4. the purported topology identity or its exact bridge application was already present in project work, leaving no new result.

### Search result and revision

Falsifier 4 partly fired.  The general source-excess identity was already proved in LSPV-1/349 at
`research/agents/lspv-1/2026-11-02_1804_LSPV-1_SOURCE_EXCESS_EULER349.tex`.
This report does not claim that identity as new.  The revised contribution is its exact application to the LSPV-1/445 source, a complete independently reconstructed 37-node typed trace, and an independent semantic replay with adversarial mutations.  The resulting search space is:

- any 35-node refutation is a full binary, source-once tree with no LOCAL, no nullary step, and no reconvergence;
- any 36-node refutation belongs to exactly one of three topology classes listed in Section 4;
- every derivation using at least two unary paid steps costs at least 37 nodes, so the natural two-LOCAL bridge-export derivation is optimal within that class;
- the unrestricted historical mixed minimum remains only $35\le W_{R_{\rm mix341}}(F_{\rm bridge})\le37$.

## 2. Exact source encoding and family ledger

For a cubic graph $G=(V,E)$, an edge variable $x_e$ for every $e\in E$, and charge $c_v\in\{0,1\}$, the proper Tseitin 3-CNF has, for each vertex $v$ with incident edges $e_1,e_2,e_3$, the four clauses

$$
C(v,a)=\bigvee_{j=1}^3 \begin{cases}
x_{e_j},&a_j=0,\\
\neg x_{e_j},&a_j=1,
\end{cases}
\qquad a\in\{0,1\}^3,\quad a_1\oplus a_2\oplus a_3\ne c_v.
$$

Thus $C(v,a)$ is falsified exactly by the local assignment $a$.  The encoding has $3|V|/2$ variables and $4|V|$ proper ternary clauses.  It is UNSAT exactly when the total charge is odd.  This is a native 3-CNF; no equisatisfiable width reduction is used.

| Family/control | Exact encoding and size parameter | Established theorem/model | Known shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin | Above proper 3-CNF; parameter $h=|V|$, $3h/2$ variables, $4h$ clauses | **PROVED-RESTRICTED:** Urquhart, *Hard examples for resolution*, JACM 34(1), 1987, DOI [10.1145/7531.8928](https://doi.org/10.1145/7531.8928), gives exponential ordinary Resolution lower bounds for Tseitin/expander formulas. The proof model is ordinary Resolution DAGs, not arbitrary algorithms or this mixed calculus. | GF(2) addition is the mandatory mixed-calculus shortcut. Project work supplies a $4h-1$ algebraic upper control when the historical native rules apply. | No lower-bound-preserving simulation from full $R_{\rm mix341}$ to ordinary Resolution is known. Ordinary Resolution hardness therefore does not lower-bound the mixed minimum. |
| LSPV-1/445 bridge-cut Tseitin control | Two $K_4$ graphs; subdivide edge $(0,1)$ in each by vertices 4 and 9; add bridge $(4,9)$. Hence $h=10$, 15 edge variables, 40 proper ternary clauses, charges $(1,0,\ldots,0)$. Exact DIMACS SHA-256 `4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18`. | **COMPUTATIONAL:** exhaustive $2^{15}$ scan certifies UNSAT and a unique 36-clause minimally UNSAT core. **PROVED-RESTRICTED:** source ancestry plus arity topology yields the floor and classifications below. | Two side-local GF(2) derivations, two LOCAL exports of opposite bridge units, one strict oriented Resolution. Work 37, span 7. | Global exact mixed minimum is not closed: $35\le W\le37$. This finite control is not an asymptotic hard family. |
| Pigeonhole principle $PHP^{n+1}_n$ | Variables $p_{i,j}$; width-$n$ pigeon clauses $\bigvee_jp_{i,j}$ and binary collision clauses $\neg p_{i,j}\vee\neg p_{i',j}$. This is not native 3-CNF. | **PROVED-RESTRICTED:** Haken, *The intractability of resolution*, TCS 39 (1985), DOI [10.1016/0304-3975(85)90144-6](https://doi.org/10.1016/0304-3975(85)90144-6), exponential ordinary shared-DAG Resolution lower bound. | Cook extended Resolution has polynomial proofs; Haken explicitly records this shortcut. | No 3-CNF reduction with the required reverse proof simulation into full $R_{\rm mix341}$ is asserted here. Equisatisfiability would be insufficient. |
| Bit-PHP in $\operatorname{Res}(\oplus)$ | $n+1$ pigeons, $n=2^\ell$ holes, bit encoding; not treated here as native proper 3-CNF. | **PREPRINT/PROVED-IN-STATED-SYSTEM:** Braun, arXiv:[2609.23015v2](https://arxiv.org/abs/2609.23015), claims every DAG-like $\operatorname{Res}(\oplus)$ refutation has more than $\exp(n/(32768\ell^2))$ clauses for $\ell\ge32$, with a linked Lean formalization. | Extended/facet rules in the project are stronger controls; LSPV-3/447 exhibits the signed-alias FACET4 issue. | Publication review and, critically, a lower-bound-preserving transfer to the exact full historical mixed grammar are absent. The theorem is not arbitrary-machine hardness. |

For historical context, Ben-Sasson and Wigderson, *Short proofs are narrow—resolution made simple*, JACM 48(2), 2001, DOI [10.1145/375827.375835](https://doi.org/10.1145/375827.375835), relates width and size for Resolution.  It does not extend automatically to XOR, LOCAL, DEF/facet, extension variables, or the mixed source-authenticated calculus.

## 3. Source/core authentication

The producer constructs the graph and source in a fixed deterministic order.  Edge IDs are the list order, starting at one.  Each $K_4$ contributes all six edges except that $(0,1)$ is replaced by a two-edge subdivision; the final edge ID 15 is the bridge $(4,9)$.  For every vertex the four clauses are emitted in lexicographic local-assignment order after excluding assignments of the charged parity.

The exhaustive scan over all 32,768 assignments establishes:

- the complete 40-clause source has zero models;
- exactly 36 clauses possess a complete-source deletion witness satisfying every other source clause;
- those 36 clauses alone remain UNSAT;
- the four nonessential clause IDs are 16, 19, 37, and 38 (zero-based source IDs);
- consequently every UNSAT source subset contains all 36 essential clauses, and the 36-set is the unique minimally UNSAT core.

This is stronger than checking only the core deletion formula: every essential-clause witness satisfies the other 39 original clauses, so adding any nonessential source clause cannot destroy the witness.  The raw JSON records all 36 witnesses and all 40 source clauses.

The result certifies source UNSAT and source minimality.  It does **not** by itself certify proof-size hardness.

## 4. Near-floor topology theorem

Consider the pruned dependency ancestry of a root in a source-explicit, locally sound, conservative calculus.  Let every paid node have zero, one, or two recorded premise incidences.  Let:

- $q$ be paid inference nodes;
- $r$ be distinct original sources in the root ancestry;
- $u$ be unary paid nodes;
- $d_0$ be nullary paid nodes;
- $\beta$ be the undirected cycle rank of the connected dependency multigraph, with every recorded premise incidence counted as an edge.

If $b=q-u-d_0$ is the number of binary paid nodes, the edge count is $E=2b+u=2q-u-2d_0$.  Connectedness gives

$$
\beta=E-(r+q-1),\qquad
q=(r-1)+\beta+u+2d_0.
$$

If every UNSAT source ancestry has at least $\mu$ sources, then

$$
q-(\mu-1)=(r-\mu)+\beta+u+2d_0. \tag{1}
$$

Equation (1) is the already-known LSPV-1/349 identity.  Here $\mu=36$.  All right-hand terms are nonnegative, so the bridge source has the following exact classifications.

| Paid work | Necessary and sufficient topology equation |
|---:|---|
| 35 | $r=36,\ \beta=0,\ u=0,\ d_0=0$. A full binary source-once tree. No reconvergence, sharing cycle, unary LOCAL/export, or nullary paid definition is possible. |
| 36 | Exactly one of: (i) $r=37,\beta=u=d_0=0$; (ii) $r=36,\beta=1,u=d_0=0$; (iii) $r=36,u=1,\beta=d_0=0$. |
| 37, exhibited | $r=36,\beta=0,u=2,d_0=0$. |

The directed dependency graph remains acyclic.  The cycle rank measures undirected reconvergence/parallel dependence, not a directed proof cycle.  Shared nodes are counted once; premise incidences remain charged exactly as the fixed node records specify.

### Two-LOCAL corollary

Any legal ancestry with at least two unary paid nodes satisfies $q\ge35+2=37$.  The independently replayed derivation has exactly two LOCAL nodes and work 37.  Therefore:

> **PROVED-RESTRICTED:** the 37-node bridge proof is work-optimal among all source-explicit, locally sound, at-most-binary derivations that use at least two unary paid nodes.

This covers the natural method “derive one bridge unit from each side, export each unit by LOCAL, then resolve.”  It does not prove that every legal historical proof must use those two exports.  A 35- or 36-node counterexample would have to avoid at least one export and fit the exact topology classes above.

## 5. Complete 37-node typed replay

The reconstructed trace uses only original source clauses and the rule fragment asserted by LSPV-1/445:

1. For each of the eight non-boundary vertices, three AND3 nodes conjoin the four local clauses into the exact width-three affine parity row: 24 AND3 nodes.
2. On each side, three XOR nodes combine the four internal vertex rows into the boundary affine row: 6 XOR nodes total.
3. At each boundary vertex, the two core source clauses compatible with the required bridge polarity are conjoined, then conjoined with the boundary row: 4 more AND3 nodes.
4. Each resulting side condition entails one bridge unit; two unary LOCAL nodes export opposite units.
5. Strict oriented Resolution on pivot 15 derives the empty clause.

Totals are 28 AND3, 6 XOR, 2 LOCAL, and 1 RES: work 37.  The root ancestry contains exactly the 36 core sources, 37 distinct paid nodes, and 72 premise incidences.  Thus $\beta=72-(36+37-1)=0$, $u=2$, and $d_0=0$.  Weighted critical-path span under the explicit unit-node, unlimited-parallelism model is 7.  This work/span statement does not claim that minimum work, minimum span, or a realizable minimum-space schedule coincide.

The independent Node verifier reconstructs the graph and source rather than trusting the producer JSON.  It evaluates every clause and every typed node as a 32,768-bit truth mask; checks exact support, condition SHA-256, affine variables and right-hand side, XOR addition, LOCAL implication, strict Resolution orientation, root falsity, ancestry, counts, and all 36 deletion witnesses.  It passed 88 grouped checks and rejected eight mutations:

1. wrong source parent;
2. wrong XOR right-hand side;
3. wrong LOCAL polarity;
4. swapped Resolution orientation;
5. missing root node;
6. corrupted condition hash;
7. changed source literal;
8. illegal support size four.

The peer compact script independently passed its 15-variable/40-source/36-essential/floor-35/upper-37/span-7 control, but it does not contain the full typed trace.  The full peer archive was unavailable in the repository surface reviewed.  Therefore this run is an independent reconstruction and semantic replay, **not** an execution of that unavailable archive and **not** an execution of an authoritative historical accepted-byte checker.

## 6. Branching/shared-DAG interpretation

No case-split, assumption discharge, or weakening rule is added.  In this trace every multi-premise rule is an AND obligation: both premises are required.  Alternative complete derivations are OR choices in the outer minimization defining $W_R$, not free alternatives inside a selected trace.

There is no branch-local context in the exhibited proof and no reconvergence: $\beta=0$.  For a proposed split proof $F,x\vdash\bot$ and $F,\neg x\vdash\bot$, both branches would be required unless the historical calculus supplies a different native proof.  A shared lemma could be counted once only if its context is justified on both uses.  Historical $R_{\rm mix341}$ has not been shown here to contain split/discharge, so such certificates must be marked as a distinct proposed calculus until a native simulation is proved.

## 7. Literature and repository search ledger

The governing handoff, current issue #3, LSPV-1/445 and /447, LSPV-2/443, LSPV-3/447, LSPV-4/439, actual Claude assessment files, and the actual latest Grok file `GROKPROOF/2026-11-06_1220_PROGRESS.md` were read or change-checked at project head `945bafae00fe7b41e1f3ddc0964516f35f62c1c7` before construction.  Direct Google UI access was unavailable; primary-source and indexed web search was used and this limitation is not disguised as Google execution.

Change-aware external review used these pinned heads, unchanged from the immediately preceding run:

| Repository/path reviewed | Head | Result relevant to this run |
|---|---|---|
| `konard/p-vs-np`: `README.md`, `DETAILED_SOLUTION_PLAN.md`, root method/issue indexes | `ecedd2b45f1c524d85c00b2da27a9c140025550c` | Hypothesis inventory only; no authenticated $R_{\rm mix341}$ grammar, bridge trace, or transfer theorem. |
| `blkph0x/p-vs-np-proof-research`: root index, `AFFINE_COMPRESSION_TEST_SUMMARY.json`, `AFFINE_DECOMPOSITION_NEXT_REVIEW.md` | `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` | Affine experiments are useful controls, not a lower-bound-preserving mixed-calculus transfer. |
| `meelgroup/frat-xor`: `README.md`, `format.md`, `src/`, `cake_xlrup/` | `18cd6bc17af10a9891c10a846ce966166f9fe0dc` | Concrete XOR certificate/checker engineering; its format is not the historical $R_{\rm mix341}$ grammar. |
| `tanyongkiam/cake_lpr`: checker/formalization root | `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2` | Verified-checker trust control; no theorem turning arbitrary P-time SAT decisions into this fixed mixed proof. |
| `peitl/short-proof`: root optimizer/checker material | `2c524cfceecf68b56f51d23f6b63255b502856d3` | Finite proof minimization control; bounded searches do not establish the unbounded mixed minimum. |
| `MassimoLauria/cnfgen`: generators/README | `24e633bdbed0d0998493bee99c42faf480c7dc96` | Reproducible family generation; no transfer theorem. |
| `openai/math` | `4eaee87548250b2682affda7d05d947c05554bae` | No relevant authenticated historical grammar or B3 bridge found in the change-aware review. |
| `anthropics/formal-math` | `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` | Formalization/reproducibility control only; no relevant transfer theorem found. |

The literature authentication found Haken 1985, Urquhart 1987, Ben-Sasson–Wigderson 2001, the STOC/SICOMP regular-$\operatorname{Res}(\oplus)$ result, and Braun's 2026 DAG-like preprint.  The 2024 regular result explicitly does not establish unrestricted DAG hardness; Braun's later preprint claims a specific unrestricted DAG result for bit-PHP, still in $\operatorname{Res}(\oplus)$ rather than arbitrary mixed systems.

## 8. Resource ledger

The ideal definition of $W_R$ excludes discovery cost.  The implemented upper-bound audit does not.

| Phase | Charged result |
|---|---|
| Governing/project reads | Current handoff, issue #3, peer reports/scripts, historical LSPV-1/349 identity, Grok/Claude files, source/index/head reads. |
| External retrieval | Primary-paper metadata/full statements where available; required repository heads and relevant paths. Cache reuse was only after head comparison. Direct Google UI unavailable. |
| Parsing/construction | Deterministic graph, 40-clause source, 32,768 assignments, truth masks, core witnesses, and 37 typed nodes. |
| Logical nodes | 37 distinct paid nodes: AND3 28, XOR 6, LOCAL 2, RES 1. Original sources are authenticated inputs, not silently recharged as inference nodes. |
| Explicit evidence | Raw JSON 18,913 bytes before the verification summary; source clauses, edges, incidents, charges, 36 deletion witnesses, 37 node records, masks, supports, annotations, parents, and root. |
| Producer | 2.632366 s elapsed; 11,264 KiB maximum RSS. |
| Independent verifier | Latest replay: 0.112855859 s elapsed; 47,948 KiB maximum RSS; 88 checks; eight mutations rejected. |
| Failed policy | The first verifier attempt compared affine objects by JSON key order and falsely rejected semantically identical objects. It was repaired to compare variables and right-hand side separately. A later optional `/usr/bin/time` wrapper was unavailable; the scripts' internal elapsed/RSS measurements were used. Both failed attempts are charged rather than erased. |
| Caches/retrieval/recomputation | The verifier recomputed source, truth masks, deletion witnesses, and node semantics; it did not trust producer masks. No persistent semantic oracle was used. |
| Output/conversion | Python JSON serialization plus Markdown/handoff/root-fragment generation and Git object publication/readback are charged publication phases. |
| Simultaneous peak | Sequential all-phase measured peak is at least 47,948 KiB, attained by the independent verifier. Publication/browser service memory is outside the local RSS measurement and is not claimed. |

File SHA-256 values before publication:

- producer: `628f4f892d1d0453c997193da0bc0498995c1ee3919dd6ef20110d564a6773a6`;
- independent verifier: `b5732c75054f2eeaf3c0ffd9383e3fcd108dd0a29b018c7648ce81f7e1d4b615`;
- raw trace/result: `16c8e02a6d709f716d90920328a8d721ff19c46327920907e930222785a20f88`.

## 9. B3 red-team verdict

This audit neither proves nor refutes B3.  A polynomial-time SAT decider returns a decision bit; it does not automatically construct source-authenticated AND3/XOR/LOCAL/Resolution records, prove arbitrary-decider correctness inside the fixed calculus, or supply polynomially bounded reflection for that calculus.  Completeness of $R_{\rm mix341}$, existence of another Cook–Reckhow system under SAT in P, and the finite 37-node trace do not imply

$$
\mathrm{SAT}\in\mathrm P\Longrightarrow \overline W_{R_{\rm mix341}}(N)\le N^{O(1)}.
$$

B1, B2, B3, a superpolynomial lower bound across **all** legal mixed rules, and the original-source-authenticated global normalization theorem remain **OPEN**.

## 10. Actual advance and precise remaining gap

**Actual advance:** the complete bridge-cut trace is now independently reconstructible and replayed, and the two-node uncertainty is reduced to exact topology classes.  The 37-node proof is exact for the two-unary/ two-LOCAL subclass.  A global 35- or 36-node proof, if it exists, must avoid at least one unary export and match one of the explicitly enumerated classes.

**Precise remaining gap:** either (i) exclude all three 36-node classes and the 35-node full-binary tree using the exact historical rule semantics, or (ii) produce an accepted source-authenticated trace in one of those classes.  Even closing this finite minimum would not transfer ordinary Resolution or $\operatorname{Res}(\oplus)$ asymptotic hardness to full $R_{\rm mix341}$ and would not supply B3.

P versus NP remains **OPEN**.

## Artifacts

- `experiments/review/lspv5_386_bridge_cut_topology.py`
- `experiments/review/lspv5_386_independent_verify.mjs`
- `results/raw/review/2026-11-06_0548_LSPV5_BRIDGE_CUT_TOPOLOGY386.json`
- `results/raw/review/2026-11-06_0548_LSPV5_BRIDGE_CUT_TOPOLOGY386_verification.json`
- `research/coordination/2026-11-06_0548_LSPV5_BRIDGE_CUT386_FIVE_ROLE_HANDOFF.md`
- `outbox/2026-11-06_0548_LSPV5_REFEREE386_ROOT_INSERT.tex`
