# LSPV-1/510: exact multi-root cycle-excess accounting for shared proof DAGs
**2026-11-08 10:00 PST | Route B | PROVED/RESTRICTED combinatorial theorem + COMPUTATIONAL certificates | P versus NP OPEN**

**Affected nodes:** new [P2-L1-510], refining [P2-L1-509], [P2-F13], and earlier single-root work/span result [P2-B12]. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. [P1-01], [P1-03], [P1-04] remain OPEN.

## IDEA and four pre-search falsifiers
Hypothesis: [P2-L1-509]'s connected terminal-overlap lower bound can be sharpened into an **exact topological budget** over entire multi-root shared derivations, including reconvergence and any deficient-arity steps. This may create a structural pruning test for the existing 15..19 finite Resolution optimization, but must not be mistaken for superpolynomial hardness.
F1. A full 19-inference source-indexed Resolution proof fails the proposed accounting equality.
F2. The published 15-merge abstract provenance control violates the equality, or is erroneously treated as legal Resolution.
F3. Multiple goals, shared source leaves, or a goal used by another goal invalidate the component/cycle count.
F4. A proposed improvement to 15..19 inadvertently assumes that all legal Resolution DAGs contain the four cycles of the *known* 19-node proof.

## SEARCH: continuity and exact evidence
Read both live complete trackers: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, 18,553 characters; proof2.txt blob 371ba561c782179b82260f58711bbdd0844156bc, 465,781 characters (prepublication). Reviewed coordination issue #3 and recent LSPV-3/506, LSPV-5/438, LSPV-2/497, LSPV-4/498, LSPV-1/509 reports, governing 2026-11-02 five-role handoff, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. Inspected actual Grok GROKPROOF/2026-11-08_0930_PROGRESS.md and Claude research/agents/claude/world-ledger/README.md. These assessments do not authenticate full historical R_mix341.
Verified that [P2-B12] /469 already contained the single-root identity q-(m-1)=mu+arity_defect, so the present work does **not** claim discovery of that older result or of Euler's graph identity. This run explicitly generalizes and applies that accounting to the *multi-goal* c-component construction of /509. Also located [P2-B6] LSPV-1/462, which had already proved an artificial clocked-system B3 countermodel; an independent clock selfcheck was explored locally but NOT promoted or republished as novel evidence.

External change-aware reads: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; peitl/short-proof/short.py blob 6508dae79e341d7015949d5919de29a132fbf267; meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f; openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. The first two repositories remain scoped research inventories, not P-vs-NP solutions. Peitl's exact Resolution minimization implementation is relevant to finite proof search, but no exact optimization result is borrowed without execution. OpenAI/math is research data, not authority. Separate Google-branded search was unavailable; public web searches covered Pang's 2026 Res(PC) preprint, resolution proof minimization and Cook–Reckhow.
Primary literature: Cook and Reckhow (1979, JSL 44:36–50), Ben-Sasson and Wigderson (2001, JACM 48:149–169, DOI 10.1145/375827.375835), and Pang (arXiv:2610.00837v2, dated 2026-10-24, preprint). None proves this project-specific historical transfer.

## ITERATE: exact theorem and mathematical proof
Let a finite **acyclic, original-source-explicit, context-free** inference DAG be pruned to the union of the ancestors of all requested terminal conclusions. Let m be the number of **distinct original source vertices in this pruned union**, q the number of **distinct paid inference vertices**, e the number of directed premise-reference incidences (count repeated premise slots if admitted), and c the number of weakly connected components of the **underlying undirected multigraph**. Every paid inference v has premise arity d(v) in {0,1,2}; original sources have no incoming proof edges.

Define undirected cyclomatic excess and arity deficit
$$
\mu=e-(m+q)+c,\qquad
\delta=\sum_{v\text{ inference}}(2-d(v))=2q-e.
$$
**Theorem 510.1 (PROVED/RESTRICTED, exact multi-root budget).** With the precise assumptions above,
$$
\boxed{q=m-c+\mu+\delta.}
$$
Both mu and delta are nonnegative. This is an *identity*, not a new nontrivial asymptotic proof lower bound.

**Proof.** For an undirected graph with m+q vertices, e edge incidences and c components, its cycle-space dimension is e-(m+q)+c (also valid for a multigraph with parallel reference edges), hence mu>=0. Since every inference has at most two premise slots, delta=2q-e>=0. Adding definitions gives mu+delta=q-m+c, proving the identity. Distinct proof nodes are counted once; any sharing, multi-root dependencies, reconvergence and source fan-out is included. No discovery work or native calculus rules are added. QED.

If the essential-source overlap graph on r conclusions is connected, then all essential original sources and their corresponding goal ancestries must occupy a common weak component. In the existing /509 gadget every one of the 16 sources is indispensable for at least one requested facet; the overlap edges 0–2 and 1–2 ensure the complete pruned union is connected, c=1. For genuine binary Resolution, all paid steps have arity two, delta=0. Thus
$$
\boxed{q=15+\mu.}
$$
Any as-yet-unfound **legal** joint Resolution proof with q<=18 must consequently have cyclomatic rank mu<=3. A proof with q=15 would necessarily have mu=0. This is a necessary structural search filter, NOT proof such alternatives do not exist.

## Exact original-source checks and the competing controls
Use the same 16 proper signed 3-CNF clauses on seven variables from /507 and /509 and the three required consequences of h=x AND t:
$$
Q_0=(\neg x\lor\neg t\lor h),\quad
Q_1=(x\lor\neg h),\quad
Q_2=(t\lor\neg h).
$$
The independently replayed **legal** /507 Resolution proof has m=16, q=19, e=38, c=1, mu=4, delta=0, and critical-path depth 4. The /509 abstract 15-merge provenance DAG has m=16, q=15, e=30, c=1, mu=0, delta=0, and depth 8. That latter DAG does NOT implement Resolution, so it is not an alternative legal proof or an upper bound. Both precisely satisfy the identity.

Two separately written implementations checked the directed topological dependencies, connected components, exact signed pivots and output clauses of the /507 proof, as well as the /509 abstract control. The independent Python run also checks the /509 exact essential-source sets. Python: 13 grouped assertions; JavaScript: legal19 and abstract15 identities plus three rejected malformed proof controls. Python test data: results/raw/arc/2026-11-08_1000_LSPV1_510_MULTIGOAL_CYCLE_RAW.json. These are finite checks, NOT an execution of historical R_mix341. The exact minimum of the joint Resolution problem remains OPEN in 15..19.

## Resource ledger and applicability
Ideal distinct-node work for the known legal proof is 19, source clause vertices 16, parent references 38 and weighted critical-path depth 4 under unit-weight/unlimited parallelism. The abstract structural competitor has 15 merges/30 references/depth 8 but is **not a legal cost control**. Literal bytes, proof IDs, acquisition, source-index reads, serialization, verification, storage/retrieval and failed exact search are additional physical phases, not charged to ideal W_R. The finite Python and JavaScript sources are separate artifacts; local execution has no same-machine FLMV interpretation. The cycle count is computable with O(m+q+e) graph operations *after* the proof graph is given, not a polynomial-time method to find the optimal proof.

For an unrestricted mixed calculus with multi-premise nodes, free definitions, typed rules, branch assumptions or unknown historical weights, the exact binary-premise identity cannot be used without first authenticating the rules and adapting the incidence accounting. The proof remains a graph-theoretic control, not a superpolynomial worst-case mixed lower bound or an arbitrary-machine hardness theorem.

## Hard-family / known-shortcut / missing-transfer ledger
| Established control | Size/encoding and certified scope | Known applicable shortcut | Missing transfer |
| --- | --- | --- | --- |
| Odd-charge cubic expander Tseitin | h vertices, 3h/2 variables, 4h exact signed 3-CNF clauses, O(h log h) bits; exponential ordinary shared-DAG Resolution size for suitable expanders | Historical *declared* local AND3/GF(2) construction has 4h-1 nodes | Full accepted-byte native R_mix341 grammar and all-rule lower bound OPEN |
| Pang random proper 3-CNF | n variables, 8n sampled proper signed clauses; O(n log n) bits; exponential Res(PC1/F2) lower bound with high probability per 2026 preprint | /498–/502 support-limited mixed simulations; unrestricted extensions and algebra must be admitted as controls | Full historical native reduction/translation OPEN |
| Existing satisfiable 16-clause output gadget | 7 variables, 16 original signed 3-CNF clauses; independent per-goal source deletion witnesses | Legal 19-node shared Resolution output proof, abstract nonlegal 15-merge topology | Exact q in 15..19 and historical mixed-native replay OPEN |

## Publication / proof-chain status
Proposed new [P2-L1-510] is only a **multi-root exact graph-excess refinement** of /509 and /469; it neither closes nor changes the epistemic status of [P2-D1], [P2-C3], [P2-B1], [P2-B2]. Historical grammar, native weights, five identities, two Route A/three Route B allocation, schedules and enabled states remain unchanged. Root main.tex not edited. P versus NP OPEN.
