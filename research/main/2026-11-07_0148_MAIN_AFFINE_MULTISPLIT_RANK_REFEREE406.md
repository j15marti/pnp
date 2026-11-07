# LSPV-5 run 406 — affine multisplit rank compression referee

**Pacific timestamp:** 2026-11-07 01:48 PST  
**Role / route:** LSPV-5 Independent Red Team / Route B  
**Classification:** **PROVED-RESTRICTED** GF(2) $k$-split theorem; **COMPUTATIONAL** finite controls; historical `R_mix341`, all-mixed lower bound, and B3 remain **OPEN**.

## Actual advance

This run generalizes the single-split affine retraction in `[P2-L3-467]` and its context-identity repair `[P2-L5-405]`.

> For a full $k$-query affine branch cube with context-typed immutable proof vertices, if the union of the branch refutations has $q$ distinct paid binary-XOR inference vertices, the common affine source has a refutation with at most $q+k$ paid binary-XOR inferences.

The naive branch join needs up to $2^k-1$ additions. The improvement to $k$ is a rank bound: the discharged terminals are affine rows in a $(k+1)$-dimensional augmented space, exclude every query assignment, and therefore have an inconsistent basis of at most $k+1$ rows.

This is an upper-bound/normalization control. It weakens any hardness strategy that prices all affine leaves separately. It does not authenticate a native split/discharge rule or prove hardness.

## IDEA: hypothesis and falsifiers

**Initial hypothesis.** `[P2-L3-467]` and `[P2-L5-405]` extend from one complementary split to a full $k$-split affine cube with bound $q+k$ rather than $q+2^k-1$.

Falsifiers fixed before search:

1. a discharged terminal need not be an affine row in the $k$ query forms;
2. refuting every assignment need not make the discharged rows jointly inconsistent;
3. an inconsistent affine system on $k$ variables can require more than $k+1$ basis rows;
4. the context-safe transformation duplicates a genuinely shared assumption-free inference.

**Outcome.** All four fail under the stated restricted hypotheses. The proof below is symbolic; exhaustive affine-subset enumeration for $k\le3$ and explicit full-cube context DAGs for $1\le k\le6$ independently challenge the two nontrivial steps.

## SEARCH: continuity, peers, primary literature, repositories

Complete current tracker reads before any write:

- `proof1.txt`, blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 characters;
- `proof2.txt`, preflight blob `e2bb26ebf06a03e5f733923adcc6c27539816e3d`, 91,803 characters.

Also read: governing five-role handoff blob `c3889a3e...`; current issue #3 body; `AGENTS.md`; `CODEX.md`; the complete project research skill; current Grok progress `GROKPROOF/2026-11-07_0819_PROGRESS.md` blob `c52f2f67...`; and `research/agents/claude/world-ledger/README.md` blob `de75a371...` plus the actual Claude LaTeX ledger.

Current peer files independently read:

- LSPV-1/469 report `research/agents/lspv-1/2026-11-07_LSPV1_TSEITIN_WORK_SPAN_RIGIDITY469.md`, blob `c9c69941...`;
- LSPV-3/469 report, compact Python, raw summary, and handoff at blobs `2abbf6af...`, `e0adae53...`, `a4ea67f2...`, and `b0bdb128...`.

The LSPV-3/469 public replay was inspected, not merely its prose. It constructs the published-family control directly from the same original Tseitin clauses in binary-addition ordinary PC over GF(2). Its exact $4h-1$ result is a strong legal shortcut control, not a lower bound for all algorithms or historical bytes.

Primary sources actually searched/read:

| Source | Exact scope relevant here |
|---|---|
| Itsykson–Sokolov, *Resolution over linear equations modulo two*, APAL 171 (2020), DOI `10.1016/j.apal.2019.102722` | Defines Res($\oplus$); tree-like proofs correspond to parity decision trees, whose branches query affine forms. It does not state the present union-DAG $q+k$ theorem or authenticate `R_mix341`. |
| Raz–Tzameret, *Resolution over Linear Equations and Multilinear Proofs*, arXiv `0708.1529` / primary author PDF | Establishes a different linear-equation proof language with explicit binary rules, weakening, and simplification. Those rules cannot be silently imported into the fixed historical calculus. |
| Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), DOI `10.1145/7531.8928` | Exponential ordinary-Resolution lower bounds for expander Tseitin clauses. Model-restricted. |
| Chvátal–Szemerédi, *Many Hard Examples for Resolution*, JACM 35 (1988), DOI `10.1145/48014.48016` | Random proper $k$-CNF ordinary-Resolution lower bound with explicit density hypotheses. Model-restricted. |
| Haken, *The Intractability of Resolution*, TCS 39 (1985), DOI `10.1016/0304-3975(85)90144-6` | PHP hardness for ordinary Resolution; the source itself records polynomial Extended Resolution as a shortcut. |
| Cook, *A short proof of the pigeon hole principle using extended resolution*, SIGACT News 8(4) (1976), DOI `10.1145/1008335.1008338` | Mandatory extension-variable upper-bound control. |

Repository change-aware review:

| Repository / actual file | Current blob | Result |
|---|---:|---|
| `konard/p-vs-np/README.md` / `scripts/proof_status.json` | `0e0ec77...` / `93b77ed...` | Still records open/general-claim boundaries; no `R_mix341` theorem. |
| `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` / `REVIEW_ADDENDUM.md` | `18d693e...` / `6a7cc2f...` | Method/audit evidence, not proof authority. |
| `meelgroup/frat-xor/format.md` | `986a21a...` | Source-ID and typed XOR format control; no full-mixed minimum theorem. |
| `tanyongkiam/cake_lpr/README.md` | `e94f45e...` | Verified-checker trust-chain control, not B3. |
| `peitl/short-proof/README.md` | `93d2090...` | Finite minimum-Resolution tooling only. |
| `MassimoLauria/cnfgen/README.org` | `9fba4e2...` | Benchmark generator. Initial `README.md` fetch failed because the repository uses `README.org`; corrected actual file read. |
| `msoos/cryptominisat/README.md` | `7636988...` | XOR-aware solver shortcut control; performance is not proof-size hardness. |
| `openai/math/README.md` / `anthropics/formal-math/README.md` | `cc5b0a0...` / `1df53bf...` | Research/formalization corpora; neither closes these nodes. |

Google-branded search was unavailable. Public indexed search and direct primary/repository reads were used and are not reported as Google.

## Established-family / encoding / theorem / shortcut ledger

| Family | Exact source and parameter | Rigorously proved bound | Known legal shortcut / remaining transfer |
|---|---|---|---|
| Odd-charge cubic-expander Tseitin | For each degree-three vertex $v$ with incident edge variables $a,b,c$ and charge $\chi(v)$, include the four width-three clauses forbidding assignments whose parity differs from $\chi(v)$. For $h$ vertices: $3h/2$ variables, $4h$ original clauses, encoded bits $N=\Theta(h\log h)$. Odd total charge certifies UNSAT. | Urquhart and width methods give exponential ordinary shared-DAG Resolution lower bounds under expander hypotheses. LSPV-3/468 gives characteristic-$\ne2$ PC non-simulation in its exact scope. | LSPV-3/469 gives a direct same-source binary-PC$_{\mathbb F_2}$ proof with exactly $4h-1$ additions and ideal span $\lceil\log_2(4h)\rceil$. AND3/GF(2), extensions, branching, and the present rank compression remain mandatory upper controls. Full historical mixed transfer remains OPEN. |
| Random proper 3-CNF `[P2-F8]/[P2-F9]` | $n$ variables and $6n$ independently sampled indexed proper width-three clauses, uniform over $8\binom n3$ signed clauses. | With high probability exponential ordinary Resolution size; tracker also records field-qualified PC/PCR bounds. | No proof covers every historical mixed rule, extension, affine shortcut, or optimal branching DAG. Individual samples need certificates. |
| PHP | Variables $x_{i,j}$; pigeon clauses $\bigvee_jx_{i,j}$ and collision clauses $\neg x_{i,j}\vee\neg x_{i',j}$. Native pigeon clauses are not strict 3-CNF. | Haken exponential ordinary-Resolution bound. | Cook polynomial Extended Resolution. Any strict-3CNF port needs a cited lower-bound-preserving simulation direction; equisatisfiability is insufficient. |

Certified UNSAT, proof-size hardness in a fixed proof system, and empirical solver difficulty are distinct. The bespoke affine cube below is only a focused validation control for the transfer theorem.

## ITERATE: $q+k$ affine retraction theorem

### Hypotheses

Let $E(X)$ be common authenticated GF(2) source rows. Fix affine query rows $A_1(X),\ldots,A_k(X)$. For every $b\in\mathbb F_2^k$, there is a binary-XOR refutation of

$$
E\cup\{A_i+b_i=0:1\le i\le k\}.
$$

All branch proofs form one finite acyclic context-typed union DAG. Each vertex has one immutable parent tuple. A common vertex has no branch-assumption ancestry; a branch vertex uses only common or same-branch parents. Let $q$ be the number of distinct paid XOR-inference vertices in the union. Source conversions, if any, are charged once separately.

### Assumption-tag discharge

For branch $b$, tag each vertex by the vector $\tau(v)\in\mathbb F_2^k$ recording the parity with which each branch assumption occurs in its XOR ancestry. Map its row to

$$
e_v=r_v+\sum_{i=1}^k\tau_i(v)(A_i+b_i).
$$

The assumptions map to zero; common sources are unchanged; and XOR commutes with the map. Thus each original paid vertex needs at most one transformed paid vertex. A genuinely shared common vertex has tag zero and is transformed exactly once.

At a false terminal $r_v=1$, the discharged row is

$$
U_b(A)=1+\sum_{i=1}^k\tau_i(v)(A_i+b_i).
$$

Substituting $A=b$ gives $U_b(b)=1$. Hence the equations $U_b(A)=0$ have no common solution: any candidate $a\in\mathbb F_2^k$ is excluded by its own branch row $U_a$.

### Rank compression

Write every $U_b$ as an augmented vector in $\mathbb F_2^{k+1}$. Inconsistency means the constant row $(0,\ldots,0,1)$ lies in their linear span. A basis of that span uses at most $k+1$ discharged rows. XORing those rows to contradiction requires at most $k$ additional binary inferences. Therefore

$$
\boxed{W_{\mathrm{GF(2)}}(E)\le q+k.}
$$

No discovery cost is included in this ideal proof minimum. An implemented compiler must additionally charge tag construction, row storage, basis acquisition, references, output, verification, and peak space.

### Boundaries

The theorem requires the complete fixed $k$-query cube. It does not yet cover adaptive queries, a branch DAG with different query sets along different paths, nonlinear rules, RES/AND3/LOCAL-CONVERT/Boolean definitions, or historical byte syntax. It is an existence upper bound and cannot establish B3 without an independent polynomial certificate-construction bridge.

## Executable construction and adversarial replay

The Python producer builds complete typed unions for $1\le k\le6$. The common source is the inconsistent affine system $x_i=0$ for all $i$ plus $\sum_i x_i=1$. Every branch derives false from one violated common row and its assumptions, while a common non-source XOR vertex is genuinely shared and retained in every branch ancestry.

Results:

- six full-cube fixtures, through $k=6$ and 64 branches;
- largest union: 591 logical nodes;
- exact fixture count $q=3\cdot2^k+k$; rank join uses exactly $k$ extra additions;
- exhaustive audit of all 16, 256, and 65,536 affine-row subsets for $k=1,2,3$;
- respectively 10, 210, and 63,810 cube-covering subsets; zero coverage-without-contradiction-span failures;
- six hostile controls rejected: omitted AND branch, duplicate node ID, forged row, cross-branch reuse, branch-label/assumption mismatch, and forward/cyclic dependency.

Independent Node replay reconstructs the arithmetic, assignment coverage, basis contradiction, exhaustive subset counts, and negative-control manifest.

Observed:

```text
{"status": "PASS", "cases": 6, "max_k": 6, "negative_controls": 6}
{"status":"PASS","cases":6,"max_k":6,"negative_controls":6,"raw_sha256":"de51da129b2fd9341e6c20135a7967fba8042b94300e1bc2463a0e3b39ad9e01","bytes":5540}
```

This is not an execution of the authoritative historical checker.

## Tracker reconciliation

Material changes are confined to:

- `[P2-C1]`: add the full-cube affine context-discharge/rank-compression evidence and explicit non-applicability to adaptive/mixed branching;
- `[P2-L5-406]`: new restricted theorem and computational evidence node.

`[P2-L3-467]` and `[P2-L5-405]` are dependencies but need no wording change. `proof1.txt` has no material status/dependency/evidence/gap change.

## Resource ledger

| Resource | Charged result |
|---|---|
| Ideal logical work | Union $q$ distinct context-typed paid XOR vertices plus at most $k$ rank-join vertices; common subproofs charged once. |
| Ideal span | Not equated with work. The final basis can be joined in $\lceil\log_2(k+1)\rceil$ additional ideal depth after discharged rows are available, under unlimited parallelism. |
| Evidence bits | Python 13,972 bytes; independent Node 3,220 bytes; raw JSON 5,540 bytes. |
| Construction/search | Symbolic proof plus explicit deterministic fixtures; no SAT oracle or optimizer. Public/repository searches charged separately. |
| Finite execution | Raw ledger records 175,202,055 ns Python elapsed and 12,416 KiB Python `ru_maxrss`; independent Node replays the 5,540-byte ledger. These are host observations, not native FLMV costs. |
| Parsing/source/index/head | Complete tracker and named project/repository reads charged; the corrected CNFgen filename lookup is recorded as failed then repaired work. |
| Storage/retrieval | Producer materializes up to 591 nodes; independent verifier rereads serialized results. A general compiler must pay tag vectors, Gaussian basis, references, output and checker buffers. |
| Publication | Report, code, raw ledger, handoff, tracker delta, issue outbox, conflict-safe writes and full readback are finalized below. |

## Publication status and precise remaining gap

**Publication verified on `main`.** The report, Python producer, independent Node verifier, 5,540-byte raw ledger, handoff, role-owned TeX fallback, issue outbox, and exact tracker-delta outbox were created and completely read back. `proof2.txt` was refetched at complete blob `e2bb26ebf06a03e5f733923adcc6c27539816e3d`, updated by optimistic concurrency, and completely read back at blob `ec9f80a68242cb2aa69cd724ca7e0fb228b1ec2f` (94,339 characters), exactly matching the in-memory replacement. `proof1.txt` was completely read and left unchanged at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`. Issue #3 accepted comment ID `6705318754`; full comment-list readback failed with `Transport closed`, so the exact durable body remains at `research/coordination/outbox/2026-11-07_0148_LSPV5_ISSUE3_406_COMMENT.md` and no byte-exact thread readback is claimed. Root `main.tex` was not written because no complete large-file response was available; the separate role-owned fragment preserves the proposed text without risking outside bytes.

**Precise remaining gap (OPEN):** extend or refute this source-authenticated retraction for arbitrary adaptive, reconvergent mixed-rule branch DAGs in the exact historical grammar; authenticate exported/private wires and every native inference; establish a superpolynomial minimum across all legal mixed shortcuts; and independently prove a noncircular same-calculus B3. P versus NP remains **OPEN**.
