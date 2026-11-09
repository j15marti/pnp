# LSPV-5/464: history-separated DAG abstraction and the cyclic-quotient firewall

**2026-11-09 09:44 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Exact proof-chain status.** This run proposes [P2-L5-464], refining still-open [P2-D1], [P2-C3], and [P2-B1]. It is distinct from [P2-L5-462], which merges a state before first payment with the state after caching; /464 proves that quotienting the nodes of an acyclic proof DAG by abstract label can create a cyclic dependency graph, and that tree-unfolding the quotient can overcharge sharing. [P2-B2] remains a separate noncircular B3 problem. No proof1.txt status changes.

## IDEA: precommitted hypothesis and falsifiers

**Hypothesis.** A cost-sound abstraction of complete shared proof DAGs cannot use one dependency vertex per abstract conclusion label. Such a label quotient can be cyclic even when every concrete dependency graph is acyclic. Restoring acyclicity by duplicating abstract labels along paths can then charge the same shared concrete subproof more than once. A safe structural repair retains a distinct abstract occurrence vertex for each concrete paid node and every dependency hyperedge, retains a global abstract paid-label history, and charges an abstract label only on its first occurrence at no more than the infimum concrete fresh-node charge in that label's fiber.

Falsifiers fixed before search:

1. the live proof trackers already contain this exact quotient-cycle plus fiber-infimum theorem;
2. every label quotient of a finite acyclic proof dependency graph is acyclic;
3. duplicating abstract occurrences and charging each occurrence can never exceed count-once concrete work;
4. some authenticated historical native transition cannot be simulated by the proposed occurrence/history transformer at no greater cost.

F1 was rejected after complete tracker and peer review; related /462, /536 and the resource-auditor theorem do not contain the graph-quotient result. F2 is false by the three-node witness below. F3 is false by the shared-diamond witness. F4 remains unresolved for the complete historical calculus because LOCAL-CONVERT, DEF/facet, side-read and branch interfaces are not fully authenticated; the generic transformer theorem is therefore restricted rather than presented as full [P2-D1].

## SEARCH: continuity and exact sources

Read both complete live trackers before research: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b (18,553 characters) and proof2.txt blob 0664f18f1d87c1ea484f0ef35331611cfe1dc3ac (773,939 characters). Read current issue #3 through the 09:34 PST [P2-L3-537] comment, governing 2026-11-09_ABSTRACT_INTERPRETATION_NEGATIVE_FIVE_ROLE_REFOCUS.md blob 8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b, the historical November 2 refocus, AGENTS.md, CODEX.md, and .codex/skills/pnp-research/SKILL.md. The requested knot/link handoff filename was searched rather than assumed; it is not present at current main, so that access limitation is explicit.

Actual current peer reports:

- LSPV-1/538, blob 274616eac4632909c19ef9540ca8b87ac2ddd30e, proves that side evidence can carry all-source dependency even with few named parents;
- LSPV-2/522, blob 34cc4d39b02f86d20f686495a4837470700eae6a, gives a separate affine may-CEGAR solver and an exponential restricted guest-search control;
- LSPV-3/537, blob a551a988ee704b0abda9dba1f1f0a6625e2daf30, gives the all-facet affine threshold and a local AND3 factor/provenance transformer;
- LSPV-4/522, blob bfc4a48f25be4961f5ec9b423f27430c971e4b00, gives the canonical cubic-pool deduplication repair;
- LSPV-5/462 and /463 give paid-history and branch-join polarity controls.

Also read GROKPROOF/2026-11-09_1230_PROGRESS.md, blob 0ee19c6b2fdf92b64427ab737fe563346779c828, and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67. Neither authenticates all historical mixed rules or supplies same-calculus B3.

### Primary abstract-interpretation hypotheses

- Cousot and Cousot, *Abstract Interpretation* (POPL 1977), <https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml>, supplies sound fixed-point approximation through ordered concrete/abstract domains and transformers; it is not a proof-cost lower-bound theorem.
- Cousot and Cousot, *Refining Model Checking by Abstract Interpretation* (ASE 1999), <https://cs.nyu.edu/~pcousot/COUSOTpapers/ASE-99.shtml>, explicitly warns that abstraction can be unsound for minimum/maximum path-length questions. Weighted proof distance is therefore an additional obligation beyond semantic reachability.
- D'Silva, Haller, and Kroening, *Abstract Conflict Driven Learning* (POPL 2013), <https://www.kroening.com/publications/view-publications-dhk2013-popl.html>, proves correctness under completely additive/reductive powerset-transformer hypotheses. Those hypotheses do not by themselves establish count-once proof-DAG cost soundness.
- D'Silva, Haller, and Kroening, *Abstract Satisfaction* (POPL 2014), <https://www.kroening.com/publications/view-publications-dhk2014-popl.html>, defines proof rules as abstract transformers and requires sound transformer approximation. It does not provide the missing historical grammar or a superpolynomial minimum.

### Required repository review

- konard/p-vs-np remained at head ecedd2b45f1c524d85c00b2da27a9c140025550c; README blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 remains finite-machine scoped.
- blkph0x/p-vs-np-proof-research remained at head 7dedc73f758dfbdc072e7aa29dfc08505761ebd5; METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 remains a conditional/bounded method catalogue.
- meelgroup/frat-xor remained at 18cd6bc17af10a9891c10a846ce966166f9fe0dc; format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f is a different typed XOR grammar.
- peitl/short-proof master README blob 93d2090a documents shortest ordinary Resolution only.
- MassimoLauria/cnfgen remained at 24e633bdbed0d0998493bee99c42faf480c7dc96; Tseitin generator blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab supplies family instances, not mixed hardness.
- openai/math remained at 4eaee87548250b2682affda7d05d947c05554bae; README cc5b0a03bca6c742f045d683b6647a6f44ef2cae warns of heterogeneous verification.
- anthropics/formal-math remained at 16a5ce41304fcdaea4e0be7c132e1c361dc26da5; README blob 1df53bfc14a022088d1b5757698f692bf79390b4 supplies no present transfer.

General indexed web research was available; no separately authenticated Google-branded interface was available.

## ITERATE: concrete and abstract domains

Fix source $F$ and a fully specified weighted calculus $R$. A concrete proof-construction state is

$$
c=(F,G,\iota,\mathcal H,\Gamma,\Pi,\Delta,P,b).
$$

$G=(V,E)$ is the complete finite acyclic directed hypergraph of constructed occurrences; $\iota$ gives globally unique identities; every hyperedge in $\mathcal H$ records all mandatory premises and authenticated side reads; $\Gamma$ records assumption contexts; $\Pi$ records exact original-source/facet provenance; $\Delta$ records fresh definitions and owners; $P\subseteq V$ is the distinct paid-node set; and $b$ is cumulative native work. Terminal refutations require an empty conclusion in a discharged context and every AND premise.

Let $q$ map concrete node/rule records to labels in $L$. The repaired abstract domain contains

$$
a=(O^\#,\lambda^\#,\mathcal H^\#,\Gamma^\#,\Pi^\#,\Delta^\#,H^\#,b^\#).
$$

$O^\#$ retains a distinct occurrence vertex $o_v$ for each represented concrete node and retains its directed hyperedges; $\lambda^\#(o_v)=q(v)$ is the coarser label; contexts, provenance, definitions and side dependencies overapproximate their concrete counterparts; and $H^\#\subseteq L$ is global paid-label history, separate from topology.

The abstraction $\alpha$ maps every concrete occurrence injectively to $o_v$, maps exact labels through $q$, maps paid nodes to $q(P)$, and overapproximates contexts/provenance. $\gamma(a)$ is the set of concrete states admitting such a topology-preserving occurrence map and satisfying every retained exact field. The abstract order is inclusion of concretizations, so this is a may overapproximation.

### Theorem 464.1: label quotient can destroy acyclicity

The concrete chain

$$
v_0(A)\longrightarrow v_1(B)\longrightarrow v_2(A)
$$

is acyclic. Identifying vertices solely by label produces $A\to B$ and $B\to A$, a directed cycle. Therefore one dependency vertex per abstract label cannot generally represent a valid proof DAG. Search-state revisitation does not repair a cyclic proof dependency graph.

### Theorem 464.2: history-separated occurrence simulation

Let legal concrete fresh-node insertion $v$ have native charge $w(v)\ge0$. Give abstract label $\ell$ first-payment charge

$$
\widehat w(\ell)
\le
\inf\{w(v):v\text{ is a legal fresh insertion and }q(v)=\ell\}.
$$

The abstract transformer adds a fresh occurrence $o_v$ and every abstracted premise hyperedge, overapproximates context/provenance/definition fields, charges $\widehat w(q(v))$ only if $q(v)\notin H^\#$, and then inserts $q(v)$ into $H^\#$. References point to an existing occurrence and cost zero.

Every concrete shared proof DAG $P$ has an admissible abstract image $P^\#$ with

$$
\operatorname{cost}(P^\#)
=
\sum_{\ell\in q(V(P))}\widehat w(\ell)
\le
\sum_{v\in V(P)}w(v)
=
\operatorname{cost}_R(P).
$$

**Proof.** Occurrence vertices preserve acyclicity, hyperedges, AND obligations and reconvergence. Choose one occurrence $v_\ell$ for every label used by $P$. The fiber condition gives $\widehat w(\ell)\le w(v_\ell)$. Sum over labels, then add the remaining nonnegative concrete weights. QED.

If every concrete terminal refutation maps to an abstract terminal refutation, then $W^\#(F)\le W_R(F)$. Hence a genuine proof that $W^\#(F)>B$ implies $W_R(F)>B$. Spurious abstract paths only reduce $W^\#$ and weaken the method.

For any reachable one-step insertion of weight $w$, an abstract first charge greater than $w$ violates the path inequality. The fiber infimum is therefore the greatest state-independent universally safe charge. If one label merges zero-cost reuse with fresh insertion, the safe charge becomes zero unless paid/fresh status is separated, recovering [P2-L5-462] as a special precision warning.

### Counterexample 464.3: unfolding double-counts sharing

A weight-one lemma $L$ is referenced by two branches that reconverge. Concrete distinct-node work charges $L$ once. Tree-unfolding duplicates the lemma occurrence and charges two. Keeping occurrence identity for actual sharing and a global paid history restores charge one.

## Named native-rule transformers and authentication boundary

- **SOURCE:** add a free occurrence with exact source identity; source erasure must overapproximate all matching sources.
- **Resolution:** preserve both parent occurrences, oriented pivot/conclusion alternatives, union of source/side-read provenance and compatible contexts; charge first label at the fiber bound.
- **AND3:** preserve both parents; use exact local truth-table intersection only where /537's bounded fragment applies, otherwise top; provenance is exhaustive union.
- **GF(2):** preserve both bona-fide row parents and overapproximate their legal row combination; semantic parity without row provenance is insufficient.
- **LOCAL-CONVERT:** preserve its actual input, exported/private-wire interface and side reads. Because complete historical port semantics are unknown, the current safe transformer admits top interface/source footprint.
- **DEF/facets:** preserve declared inputs, global freshness and paid owner occurrence; every facet references that owner. Repeated-input and tautological facets remain controls.
- **Reuse/reference:** point to the existing occurrence, charge zero and leave paid history unchanged.
- **Split/discharge/reconvergence:** no historical authority is assumed. Any authenticated rule must preserve every AND branch, context discharge and reconvergence; OR alternatives remain choices. Until authenticated, a may abstraction must conservatively admit unknown effects rather than silently add or omit a rule.

LSPV-1/538 shows that named parents do not exhaust source dependencies: side evidence may authenticate all sources. Missing any legal rule or side dependency breaks coverage; inflating a charge breaks the cost direction.

## Independent verification

- experiments/review/lspv5_464_history_separated_dag_abstraction.py, SHA-256 b028fd6ea5afe9a3ac6e3e1544562c0374a3ddeb59d11eb4669894b9a8a811a1
- experiments/review/verify_lspv5_464_history_separated_dag.mjs, SHA-256 1e2a08c5307c4542a2fdebd2746efbfe5c509db7044d76c0ec6383a7cbdac134
- results/raw/arc/2026-11-09_0944_LSPV5_464_HISTORY_SEPARATED_DAG_RAW.json, SHA-256 48e0afbfb22a2f9722febc5eed089e472db7daf517be350c84652e313f37710f

Python enumerated all forward-edge DAGs on one through four ordered vertices and every binary labeling: 1,098 DAG/label cases. Naive label quotienting was cyclic in 948 cases, including 726 with non-self-loop cycles. Across 84,750 positive-weight cases, repaired occurrence/history cost exceeded concrete work zero times. It also checked the $A\to B\to A$ witness, shared-diamond overcharge and unsafe maximum-fiber charge. Independently authored JavaScript reproduced every count with 85,852 checks. Directed edges are a special case of hyperedges. These are semantic/cost reconstructions, not an authoritative historical checker or finite proof-minimum optimizer.

## Established-family and shortcut ledger

| Family | Exact source encoding and size | Published restricted theorem | Mandatory controls and missing transfer |
|---|---|---|---|
| Odd-charge cubic Tseitin on suitable connected expander $G$ | One Boolean variable per edge; at each of $h$ degree-three vertices, the four signed proper 3-clauses falsified exactly by wrong local parity tuples. Thus $n=3h/2$, $m=4h$, binary-indexed source length $N=\Theta(h\log h)$. | Urquhart 1987 gives exponential ordinary shared-DAG Resolution length for qualifying expanders. | GF(2) Gaussian elimination, the declared $3h+(h-1)$ mixed shortcut, ER, sharing and preprocessing remain legal. No all-rule historical lower bound. |
| Unary $PHP^{n+1}_n$ | Pigeon at-least-one clauses and pairwise hole-collision clauses; starts outside strict 3-CNF. | Haken 1985 gives exponential ordinary Resolution size. | Cook's polynomial Extended Resolution proof is mandatory. Any 3-CNF conversion needs a precise lower-bound-preservation direction, not equisatisfiability alone. |

Compact mod-3 one-hot adders, opposite-characteristic algebra, extension variables and shared-DAG preprocessing remain mandatory controls. Shortcuts are evidence about the true minimum, never exclusions.

## Semantic, cost and resource separation

- Semantic bottom in a sound model overapproximation may certify no model; it does not state a proof minimum.
- Absence of a cost-bounded proof requires complete rule/goal coverage and the cost inequality above.
- Failure to derive bottom, rejection of a cyclic abstract quotient, widening loss or bounded-search exhaustion proves neither SAT nor a lower bound.
- Abstract correctness or a polynomial abstract certificate does not establish same-calculus B3.

Logical work counts distinct nodes. Evidence includes occurrence/label IDs, dependencies, references, contexts, source provenance and paid history. Construction, parsing, graph enumeration, serialization and output were executed but are not native asymptotic bounds. A real implementation must also charge source/index/head reads, refinement, caches, failed policies, retrieval/recomputation, verification and simultaneous peak storage. Ideal $W_R$ still excludes discovery.

## Actual advance and precise gap

**Actual advance.** [P2-L5-464] proves that label quotienting can destroy proof-DAG acyclicity while occurrence duplication can double-count sharing. Occurrence topology plus global paid history and fiber-infimum first-label costs gives a cost-nonincreasing simulation theorem.

**Precise remaining gap.** Exact LOCAL-CONVERT ports, DEF/facet ownership, all side reads and any native split/discharge remain [P2-D1] OPEN. A whole-system transformer and a superpolynomial lower bound on its abstract minimum remain [P2-C3] and [P2-B1] OPEN. Noncircular same-calculus B3 remains [P2-B2] OPEN. P versus NP remains OPEN.
