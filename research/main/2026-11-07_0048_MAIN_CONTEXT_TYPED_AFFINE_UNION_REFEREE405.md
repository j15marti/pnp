# LSPV-5 run 405 — context-typed affine union referee

**Pacific timestamp:** 2026-11-07 00:48 PST  
**Role / route:** LSPV-5 Independent Red Team / Route B  
**Classification:** **PROVED-RESTRICTED** context-typed GF(2) retraction; **COMPUTATIONAL** finite controls; historical `R_mix341` transfer and B3 remain **OPEN**.

## Actual advance

`[P2-L3-467]`'s affine two-branch $q+1$ retraction is sound only with the following node accounting made explicit:

> $q$ is the number of distinct **context-typed inference vertices with fixed parent tuples** in one acyclic union proof graph. It is not the number of distinct affine row labels.

This run proves the restricted statement below and supplies an explicit legal-scope counterexample to row-label deduplication. The repair does not authenticate any new historical `R_mix341` rule, prove a lower bound for the full mixed calculus, or prove B3.

## IDEA: hypothesis and precise falsifiers

**Initial hypothesis.** The $q+1$ claim in `[P2-L3-467]` fails if its “shared nodes” are identified only by equal affine row or reused numeric ID rather than fixed derivation and assumption context.

Falsifiers fixed before search:

1. the peer checker keys every node by ancestry and branch context;
2. assumption-coefficient elimination maps a genuinely shared node identically without duplication;
3. $q$ already counts context-node incidences rather than rows;
4. the finite fixture validates a genuinely shared non-source inference that is assumption-free.

**Outcome.** Falsifier 2 holds mathematically after the repair. Falsifiers 1, 3, and 4 fail for the compact `[P2-L3-467]` executable: it evaluates fixed rows and branch formulas but has no proof-node IDs, fixed parent graph, context identity, or shared non-source vertex. The peer prose can be repaired without changing the numerical $q+1$ bound.

## SEARCH: authenticated continuity and literature

Complete current blobs read before write:

- `proof1.txt`, blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`;
- `proof2.txt`, preflight blob `d03cf5888745b70b8aa2a9b7b9ce4a429c6f0c7a`;
- governing five-role handoff, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, issue #3 body, current LSPV-3 run 467/468 report-code-raw-handoff artifacts, and actual Grok/Claude directories and assessments.

Issue-comment enumeration failed with `Transport closed`; the issue body and specifically named current artifacts were read, and the failure is not represented as review of all comments.

Primary and repository evidence actually inspected:

| Source | Exact item / pinned evidence | Result relevant here |
|---|---|---|
| Haken, *The Intractability of Resolution*, TCS 39 (1985), DOI `10.1016/0304-3975(85)90144-6` | published theorem/abstract | Exponential hardness is for ordinary Resolution on PHP; the paper explicitly notes polynomial Extended Resolution proofs. **PROVED-RESTRICTED**, not full-mixed hardness. |
| Razborov, *On the CDCL proof system* | `https://people.cs.uchicago.edu/~razborov/files/cdcl.pdf`, Definition 2.1 / Claim 3.2 context | Proof transformations preserve a vertex set while separately changing edges and the clause-labeling function. This authenticates the distinction between vertices and labels; it does not prove the present GF(2) lemma. |
| Itsykson–Riazanov–Smirnov, *Tight Bounds for Tseitin Formulas*, SAT 2022, DOI `10.4230/LIPIcs.SAT.2022.6` | theorem/abstract | Exponential-in-treewidth lower bounds are for regular Resolution and OBDD systems. **PROVED-RESTRICTED**. |
| Bhattacharya–Chattopadhyay, ECCC TR25-106 (2025) | `https://eccc.weizmann.ac.il/report/2025/106/` | Current Res($\oplus$) size bounds remain depth-restricted and use lifted Tseitin formulas. No unrestricted Res($\oplus$), `R_mix341`, or all-algorithm bound. |
| `konard/p-vs-np` | `proof_status.md`, repository commit `93b77ed...` | Claim-audit material only; no source-authenticated `R_mix341` transfer or noncircular B3. |
| `blkph0x/p-vs-np-proof-research` | `METHOD_INDEX.md`, repository commit `18d693...` | Method index/audit source; no theorem closing the present transfer. |
| `meelgroup/frat-xor` | format document, commit `986a21...` | Checker/format evidence, not a full-calculus proof-size lower bound. |
| `tanyongkiam/cake_lpr` | README, commit `e94f45...` | Verified-checker trust-chain evidence, not B3. |
| `peitl/short-proof` | README, commit `93d209...` | Finite minimum-proof tooling only; bounded computation is not asymptotic hardness. |
| `msoos/cryptominisat` | README, commit `763698...` | Algebra/XOR shortcut control; solver behavior is not proof-size hardness. |
| `openai/math` / `anthropics/formal-math` | READMEs, commits `cc5b0a...` / `1df53b...` | Formal-math research repositories; no authenticated theorem for these tracker nodes. |

Google-branded search was unavailable in this environment. Public primary-literature search was used and is not reported as Google. GitHub repository files were read directly rather than inferred from snippets.

## Established-family / encoding / shortcut ledger

| Family | Exact 3-CNF encoding and size parameter | Published lower bound and model | Strongest relevant shortcut / remaining transfer |
|---|---|---|---|
| PHP | Variables $x_{i,j}$. Pigeon clauses $\bigvee_{j=1}^{n}x_{i,j}$ plus collision clauses $\neg x_{i,j}\vee\neg x_{i',j}$. Long pigeon clauses require a cited lower-bound-preserving 3-CNF conversion before calling the result 3-CNF hardness. | Haken: exponential ordinary shared-DAG Resolution lower bound in the native PHP encoding. | Cook Extended Resolution has polynomial proofs. Therefore Haken alone cannot lower-bound the full mixed minimum. Exact preservation through any chosen 3-CNF conversion remains required. |
| Odd-charge cubic Tseitin | One variable $x_e$ per edge. For each degree-3 vertex with incident $a,b,c$ and charge $\chi(v)$, include the four width-3 clauses forbidding the parity-opposite assignments. For $h$ vertices: $3h/2$ variables and $4h$ clauses; bit length $N=\Theta(h\log h)$ under binary IDs. Odd total charge certifies UNSAT. | Exponential lower bounds are established for specified Resolution/regular/OBDD and restricted Res($\oplus$) models, with theorem-specific graph and depth assumptions. | Declared GF(2) addition gives a linear-size parity refutation when the exact rule is available. `[P2-L3-468]` adds a characteristic-sensitive non-simulation control, not an `R_mix341` lower bound. |
| Random proper 3-CNF controls `[P2-F8]` / `[P2-F9]` | Exactly three distinct noncomplementary literals per clause under the tracker's distribution and density parameters. | Existing tracker evidence is model-qualified and does not transfer to arbitrary mixed proofs or algorithms. | Preprocessing, learned clauses, algebra, extensions, branching DAG sharing, and source authentication all remain legal shortcuts to audit. |

Certified UNSAT, certified proof-size hardness in a fixed model, and empirical solver difficulty are separate claims throughout. This run's tiny affine graphs are validation controls, not proposed hard families.

## ITERATE: restricted theorem and adversarial challenge

### Context-typed affine split retraction

Let $E$ be common GF(2) source rows. Let branch $b\in\{0,1\}$ add one affine assumption $A_b$, with $A_0+A_1=1$. Each proof vertex has one immutable rule, fixed ordered parents, and scope `common`, `b0`, or `b1`. A `common` vertex may have only `common` ancestry. A branch vertex may use common vertices and vertices in its own branch only.

For a vertex $v$ in branch $b$, let $\tau(v)\in\mathbb F_2$ be the parity of occurrences of $A_b$ in its XOR ancestry and set

$$e_v=r_v+\tau(v)A_b.$$

- A common source has $\tau=0$ and is unchanged.
- The assumption source has $\tau=1$ and maps to zero, so it is omitted.
- At an XOR inference $v=u+w$, both $\tau$ and $e$ add, so at most one transformed inference is required for each original inference vertex.
- Any genuinely shared vertex has no assumption ancestry, hence $\tau=0$ in both branches and transforms identically; sharing is preserved.
- If a false terminal has $\tau=0$, its transformed branch already refutes $E$.
- If both terminals have $\tau=1$, the transformed terminals derive $1+A_0=A_1$ and $1+A_1=A_0$; one extra XOR derives $1$.

Thus an acyclic context-typed union with $q$ distinct paid XOR-inference vertices retracts to an $E$-refutation with at most $q+1$ paid XOR inferences. This is an elementary GF(2) statement; native simulation and exact historical weights remain separate obligations.

### Why equal labels are not shared nodes

Take common rows $a=0$ and $a=1$, and complementary branch assumptions $z=0$ and $z=1$. In branch 0 derive

$$U_0=(a=0)+(z=0),$$

and in branch 1 derive

$$U_1=(a=1)+(z=1).$$

Both vertices carry the same affine row $a+z=0$, but their parent tuples, assumption dependencies, and scopes differ. Merging them by row label would either give one vertex two definitions or leak a branch-local derivation across incompatible contexts. They must be paid as two distinct inference vertices. Reused large numeric IDs do not change this requirement.

### Executable replay

- `experiments/review/lspv5_405_context_typed_affine_union.py` builds and checks an explicit 13-node two-branch union with a genuinely shared non-source vertex. It obtains $q=7$, terminal tags one, and a one-inference common-source refutation, satisfying $1\le q+1=8$.
- It separately validates the equal-label/different-context witness and rejects six controls: omitted AND branch, cross-branch reuse, forged row, duplicate ID, forward/cyclic dependency, and illegal equal-row merge.
- `experiments/review/verify_lspv5_405_context_typed_affine_union.mjs` independently replays the raw-ledger invariants.

Observed outputs:

```text
{"status": "PASS", "q": 7, "negative_controls": 6}
{"status":"PASS","raw_sha256":"4f2e486717536d086cde4aacff42fdb2e9664c823f2c239d1664befd158434ab","bytes":3315,"q":7,"negative_controls":6}
```

The executable is an independent model, not execution of the authoritative historical checker.

## Tracker reconciliation

Material changes are limited to these affected IDs:

- `[P2-L3-467]`: repair $q$ to mean distinct context-typed inference vertices with fixed parents; record that its compact replay did not itself test DAG sharing.
- `[P2-C1]`: add the context-identity/source-scope obligation and the equal-row counterexample.
- `[P2-L5-405]`: new **PROVED-RESTRICTED / COMPUTATIONAL** node recording this theorem, replay, controls, and limitations.

`proof1.txt` has no material status/dependency/evidence/gap change. No restricted theorem is promoted to P-versus-NP resolution.

## Resource ledger

| Resource | Charged observation |
|---|---|
| Logical work | 13 union nodes; 7 paid XOR inference vertices; 1 actual common-source join; union sharing paid once. |
| Evidence bits | Python 10,652 bytes; independent verifier 1,818 bytes; raw JSON 3,315 bytes. |
| Construction/search | Manual theorem construction plus public/repository search; no semantic oracle and no finite optimizer. |
| Verification | Two independent-language executions; 6 rejecting controls; SHA-256 for all three artifacts. |
| Runtime/space | Exact Python elapsed nanoseconds and `ru_maxrss` are stored in the raw ledger; Node verified the 3,315-byte ledger. |
| Parsing/source/index/head | Complete tracker reads charged; named project and repository files read; issue-comment enumeration failure recorded. |
| Sharing/retention | One assumption-free non-source inference retained and referenced by both branches; counted once. Context-distinct equal-row vertices counted separately. |
| Work/span/schedule | Work is 7 paid union inferences. Span depends on the explicit topological schedule and is not equated with work. The finite replay is sequential; no parallel-time claim. |
| Publication/update | Report, code, raw ledger, handoff, tracker read/write/readback, issue post, and final readback are separately charged in publication status below. |

## Publication and precise remaining gap

Publication status is finalized after conflict-safe current-head writes and full readback. No `main.tex` write was attempted; the role-owned fallback fragment is separate.

**Precise remaining gap (OPEN):** authenticate the exact historical `R_mix341` rule grammar and weights, prove that every mixed legal branching/shared proof admits the required source-preserving context-typed normalization without exponential blow-up or exhibit a legal counterexample, and prove a noncircular same-calculus B3. No superpolynomial lower bound over all legal mixed rules is established. P versus NP remains **OPEN**.
