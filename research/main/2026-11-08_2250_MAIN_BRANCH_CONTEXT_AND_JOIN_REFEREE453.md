# LSPV-5 independent red-team report: explicit branch contexts, AND discharge, and source-cover preservation

**Run:** 453  
**Role:** LSPV-5, Route B independent red team  
**Time:** 2026-11-08 22:50 PST (America/Los_Angeles)  
**Tracker node:** `[P2-L5-453]`  
**Status:** **PROVED/RESTRICTED** meta-lemma; **COMPUTATIONAL** exact control packet. Historical accepted-byte `R_mix341`, the full-family mixed-rule transfer, superpolynomial $\overline W_R$, and noncircular B3 remain **OPEN**.  
**P versus NP:** **OPEN**.

## Claim card before search

**Initial hypothesis.** The graph-sensitive source-cover lower bound `[P2-L5-452]` extends unchanged to explicit branching proof DAGs only when every split branch has an authenticated context and discharge is a genuine AND hyperedge requiring both complementary cases. Implicit ambient-formula access or erased contexts are hidden oracles, not harmless syntax.

Assumptions fixed before search: a sound source-explicit proof calculus; a finite acyclic dependency DAG; one empty-context false root; contexts $\Gamma$ made from assumption literals; premise reuse from $\Gamma_0$ into $\Gamma$ only when $\Gamma_0\subseteq\Gamma$; split on $x$ discharges both $\Gamma,x\vdash\bot$ and $\Gamma,\neg x\vdash\bot$; distinct nodes charged once; and maximum inference indegree $a>1$. `BRANCH_CTX` below is a new control calculus, not an amendment to historical `R_mix341`.

**Precise falsifiers.**

1. The authenticated historical grammar supplies a native split/discharge rule that bypasses original-source ancestry.
2. A branch-local lemma can be soundly reused under an incompatible sibling context without a separate legal discharge.
3. A valid reconvergent DAG discharging every AND case can refute while its root ancestry contains fewer original sources than a semantic source cover.
4. The current LSPV-1/526 or LSPV-3/526 accepted-byte evidence authenticates such a historical branch rule or erases the context obligation.

## IDEA -> SEARCH -> ITERATE result

None of falsifiers 1--4 fired at the claimed scope. The governing `/341` report declares only binary Resolution, binary-premise AND3 and XOR, unary LOCAL-CONVERT, and fresh two-input DEF, with original sources free and each derived line unit cost. It does not declare a native case split, assumption discharge, or weakening rule, and no authoritative byte checker was found. Thus this run proves a theorem for an explicitly labelled control calculus and does **not** silently add a rule to `R_mix341`.

The initial claim was sharpened in two directions.

* The source-cover theorem needs no special ban on branching. For any selected legal proof DAG, the false root's original-source ancestors must be an unsatisfiable subset. Hence every semantic source cover remains compulsory. Assumption and join nodes cannot remove ancestors and may only increase charged work.
* Context intersection controls sharing. A node reusable in both complementary branches must be valid under a context contained in the intersection of those branch contexts. In particular, a conclusion depending on $x$ cannot leak into the $\neg x$ branch. Unconditional lemmas and sources may be shared and are charged once.

## Restricted theorem

Write nodes as $\Gamma\vdash C$. A source has context $\varnothing$. A sound inference may use a premise proved in $\Gamma_0$ under target context $\Gamma$ only when its assumptions are justified; the exact verifier below uses the stronger equality condition that the conclusion context is the union of its premise contexts. A split node is the directed AND hyperedge

$$
\frac{\Gamma\cup\{x\}\vdash\bot\qquad \Gamma\cup\{\neg x\}\vdash\bot}{\Gamma\vdash\bot}.
$$

The two premises are obligations, not OR alternatives. An alternative complete derivation can avoid this split, but once the split is selected both antecedents are present.

**Source-cover preservation.** Let $S$ be the distinct original-source nodes in the ancestry of an empty-context false root. If $S$ were satisfiable, soundness of every context-labelled inference and complete discharge of every assumption would make the root true under some extension of that satisfying assignment, contradiction. Thus $S$ is unsatisfiable. Consequently any semantic argument that every unsatisfiable subset contains at least $r$ sources, including `[P2-L5-452]`, applies unchanged to branching DAGs.

**Work bound.** Retain only root ancestors. With $r$ original-source leaves and $q$ paid nodes, including any assumption/discharge nodes, the underlying dependency graph is connected and has at least $r+q-1$ edges. At most $aq$ edges enter paid nodes, so

$$
q\ge\left\lceil\frac{r-1}{a-1}\right\rceil.
$$

Zero-antecedent paid assumption nodes only strengthen the inequality. Reconvergence does not duplicate nodes: the count uses the union of distinct nodes and edges. For the historical prose bound $a=2$, `[P2-L5-452]` therefore remains $q\ge r-1$ **if** a faithful historical implementation is source-explicit and sound. This conditional does not authenticate one.

**Context-intersection lemma.** If the same stored node is referenced in branches $\Gamma\cup\{x\}$ and $\Gamma\cup\{\neg x\}$, its proved context $\Delta$ must satisfy

$$
\Delta\subseteq(\Gamma\cup\{x\})\cap(\Gamma\cup\{\neg x\})=\Gamma.
$$

Therefore a branch-local conclusion cannot be shared across complementary branches. An unconditional lemma may be shared. The result distinguishes logical distinct-node work from weighted span and from any realizable retention/recomputation schedule.

## Exact finite control and hostile mutations

The valid packet uses the satisfiable-looking local notation $a=1,b=2$ and the UNSAT source

$$
F=\{(a),(\neg a\lor b),(\neg a\lor\neg b)\}.
$$

It splits on $b$. The source $(a)$ is referenced by both branches but stored and charged once. The $b$ branch derives $\neg b$ unconditionally and resolves it with assumption $b$; the $\neg b$ branch derives $b$ unconditionally and resolves it with assumption $\neg b$; an explicit AND node discharges both. Exact results: three authenticated source nodes, two paid assumption nodes, four paid Resolution nodes, one paid split/join node, seven paid distinct nodes, weighted critical-path span three, and all three sources in root ancestry.

An independently authored Node verifier reconstructed clauses, oriented pivots, premise references, contexts, split polarity, acyclicity, source ancestry, distinct-node work, span, and the sharing ledger. Result: **PASS**, 65 checks. It rejected all seven mutations with exact codes:

| Mutation | Required result |
|---|---|
| omitted sibling case | `SPLIT_ARITY` |
| reuse the $b$-branch contradiction as the $\neg b$ branch | `SPLIT_CONTEXT` |
| expose a branch-local false node as root | `ROOT_CONTEXT` |
| forward/cyclic dependency | `FORWARD_REFERENCE` |
| double-count the shared node | `LEDGER` |
| remove an original source but keep its references | `MISSING_REFERENCE` |
| claim $\{a\}$ refuted from the single inconsistent assumption $\neg a$ | `SPLIT_ARITY` |

The last control is a minimal soundness counterexample to one-branch discharge: $\{a\}$ is satisfiable although $\{a,\neg a\}$ is not.

SHA-256: producer `c292f8e17b7f4bec06e3380eeed7eca571cdef21d8d1d0bb8cb009be93cfc267`; independent verifier `6c6cdd076eb801b33a6057212c8bc908305562625898470c91ee509d34df7f14`; raw JSON `1a4034e2ac8aa16efdb7fcaec67add9002cd7c4b15657446297c506b02369943`. The raw artifact is 22,463 bytes. This is not an execution of a historical checker.

## Established-family and known-method ledger

| Item | Exact scope and remaining transfer |
|---|---|
| Haken PHP | Ordinary shared-DAG Resolution lower bound for pigeonhole formulas: A. Haken, *The intractability of resolution*, TCS 39 (1985), DOI `10.1016/0304-3975(85)90144-6`. This is restricted-system proof-size hardness, not all algorithms. Cook-style extension variables remain a mandatory shortcut control. |
| Published strict-3 Tseitin test family | `[P2-L5-452]`: connected cubic $G$, variables $x_{e,t}$ for $t\in\mathbb F_3$; one width-3 ALO per edge and one width-3 negative forbidden-tuple clause per locally invalid incident triple. Size: $3|E|$ Boolean variables and $|E|+18|V|$ clauses. Nonzero total charge certifies UNSAT. Pang arXiv:2610.00837v2, Thm. 7.2(b), gives exponential size only for fixed-degree opposite-characteristic $\operatorname{Res}(\mathrm{PC}_r/\mathbb F_p)$ on its stated expander encoding. Exact lower-bound-preserving transfer to this strict3 source and all `R_mix341` rules remains **OPEN**. |
| Branching and learned lemmas | Buss--Hoffmann--Johannsen, LMCS 4(4:13), 2008, DOI `10.2168/LMCS-4(4:13)2008`: unrestricted WRTL/WRTI without regularity is equivalent to DAG Resolution; clause learning and variable extensions can provide short legal routes. These are upper-bound controls, not exclusions. |
| Incremental assumptions/proof state | Fazekas--Pollitt--Fleury--Biere, *Certifying Incremental SAT Solving*, LPAR 2024, introduces a separate proof format/checker for incremental contexts. It supports the need to authenticate assumptions and evolving clause databases; it does not authenticate `R_mix341`. |
| Remaining Route B gap | Authenticate `[P2-D1]`; prove all-rule normalization/source retraction `[P2-C3]`; carry an established superpolynomial lower bound through every legal shortcut to `[P2-B1]`; independently prove noncircular same-calculus B3 `[P2-B2]`. |

Certified UNSAT, certified proof-size hardness, and empirical solver difficulty are kept separate. No empirical runtime is used as a lower bound.

## Current peer evidence replay

The exact LSPV-1/526 and LSPV-3/526 artifacts were read and rerun. The first direct attempt failed before scientific execution because a locally reconstructed upstream `/523` file had one extra final newline, violating the packet's pinned Git-blob SHA. An ephemeral copy removed exactly that reconstruction byte; all three upstream hashes then matched their published pins (`/523` `c8c62a5...`, `/524` `3fa42e25...`, `/525` `1d6334fa...`). No published file or theorem was changed.

LSPV-1/526 then passed: 21 original sources, 34 DEF plus 114 RES = 148 paid nodes, critical path 18, 52,645 checks, 512 assignments with nine source models; historical checker flag false. LSPV-3/526 passed: 21 SOURCE, 102 FACET, 114 RES, 237 records and 148 paid inferences. Both are proposed ER2-OWNER local identity packets with no branch assumptions or case splits. They neither falsify this context theorem nor authenticate historical bytes.

## Search and repository audit log

Indexed web search was available; no separate Google-branded portal was available, so no Google-specific use is claimed. Primary statements inspected included Haken 1985; Buss--Hoffmann--Johannsen 2008 (full PDF definitions of resolution DAGs, postorder lemma reuse, clause learning and variable extension); and Fazekas et al. 2024 on certified incremental SAT.

Required change-aware repositories were checked at their pinned heads. `konard/p-vs-np` remained `ecedd2b45f1c524d85c00b2da27a9c140025550c`; `blkph0x/p-vs-np-proof-research` remained `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`. Targeted searches for branch assumptions, contexts and clause learning returned no new relevant file. Neither repository authenticates `R_mix341` or proves B3. Rotating proof-format heads checked: `meelgroup/frat-xor` `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `tanyongkiam/cake_lpr` `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`, `marijnheule/drat-trim` `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, `digama0/frat` `aa18581497830b49a6ab6cbc9e0dc778c14885b5`, and `peitl/short-proof` `2c524cfceecf68b56f51d23f6b63255b502856d3`. These are distinct formats or restricted optimizers, not historical authentication.

Continuity reads included the governing historical handoff at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, issue #3, `AGENTS.md` blob `19656...`, `CODEX.md` blob `754999...`, the complete research skill and mode/protocol references, the actual current Grok and Claude directories, `/341`, `/452`, and current LSPV-1/526 and LSPV-3/526 reports/code/raw/handoffs. Both trackers were read completely. Prewrite tracker blobs: `proof1.txt` `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; `proof2.txt` `5119cddf3844775795297a817bdb12e582a44ddd`.

## Resource ledger

Logical work is seven paid distinct nodes and weighted span three in the finite control. The restricted lower bound intentionally excludes discovery cost. Actual work charged separately: tracker/handoff/issue/peer/Grok/Claude reads; repository-head and primary-literature searches; packet construction; 22,463 output bytes; independent parse/reconstruction; exact peer replay; report/handoff/tracker/outbox preparation; Git publication and readback. The producer's reported peak RSS is stored in raw JSON. Retention and recomputation are distinct: the packet retains the shared source once and references it twice; recomputing a duplicate would be a different realizable schedule, not a lower minimum. The initial pinned-SHA newline failure is explicitly recorded above.

The current root `main.tex` blob `fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba` again returned zero readable bytes. It was not edited. A durable role-owned fallback insertion is supplied. No task, role, identity, title, schedule, timezone, enabled state, allocation, historical grammar, or historical weight was changed.

## Tracker determination and remaining gap

`proof1.txt`: no material status, dependency, evidence, or gap change.  
`proof2.txt`: material restricted evidence at `[P2-L5-453]`, depending on/refining `[P2-L5-452]`, `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, and `[P2-B2]`.

**Actual advance:** explicit branch-context/source-cover preservation and a context-intersection condition for legal shared lemmas, with exact AND-discharge and adversarial controls.  
**Verification:** the new independent verifier passed all valid checks and rejected seven hostile packets; current peer packets replayed at their stated proposed scope.  
**Precise remaining gap:** authenticate the historical byte grammar and native rule set, then prove a lower-bound-preserving transfer from an established hard 3-CNF family across every mixed shortcut to superpolynomial $\overline W_R$; separately prove noncircular B3 for that same fixed calculus. None is supplied here. P versus NP remains **OPEN**.
