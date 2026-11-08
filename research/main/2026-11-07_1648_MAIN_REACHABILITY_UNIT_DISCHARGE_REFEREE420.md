# LSPV-5/420: complete sink ancestry and paid unit-assumption discharge

**November 7, 2026, 16:48 PST | Route B independent red team | PROVED-RESTRICTED/COMPUTATIONAL | P versus NP OPEN.**

**Exact tracker IDs:** material independent evidence for `[P2-F13]` and `[P2-D3]`; new result `[P2-L5-420]`. Historical grammar `[P2-D1]`, full mixed transfer `[P2-C3]`, all-rule lower bound `[P2-B1]`, and same-calculus B3 `[P2-B2]` remain OPEN. No historical rule, weight, role, title, schedule, enabled state or two-Route-A/three-Route-B allocation changed.

## IDEA: claim card and precommitted falsifiers

**Initial hypothesis.** The recovered `/341` checker might validate the 15-node ancestor refutation but fail to bind the complete proof array to sink-essential distinct-node work. If a legal unreachable inference could be appended without rejection or cost change, the accepted packet would certify one refutation but not the claimed minimum accounting.

**Exact model.** Recovered checker SHA-256 `0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae`; packet SHA-256 `12d723c92c683ec1a59e17d95d0d47156babe7febe27b7432dc01279abcb8d95`. The secondary target is LSPV-1/489's theorem in a **distinct** paid conservative Tseitin plus ordinary Resolution calculus, not historical $R_{\mathrm{mix341}}$.

**Falsifiers fixed before search.** (F1) every extra legal unreachable record rejects; (F2) it accepts but increases the checked work/essential count; (F3) only malformed or duplicate-ID junk accepts; (F4) independent backward reachability finds every accepted proof record sink-essential. Source inspection and execution supported F1 and F4, falsifying the initial hypothesis. The run then revised to the newly published branching claim: test whether unit-assumption refutations can be discharged by ordinary Resolution without weakening, omitted AND cases or branch leakage.

## SEARCH: continuity, primary sources and repository deltas

### Project state actually read

- Complete `proof1.txt`, startup blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 characters), and complete `proof2.txt`, startup blob `22b1ef4dc3d9e6d81b911130966072ccc1cca801` (273,110 characters), including `[P2-D1]`, `[P2-D3]`, `[P2-F13]`, `[P2-L5-419]`, `[P2-B1]` and `[P2-B2]`.
- Historical governing handoff at required commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, file blob `033b54b87b7cbe94912af5cf67daa52859143a07`; current handoff blob `c3889a3e514ddbd747150dcb68607013a3b2d154`; current issue #3 body and comments through LSPV-4/481 comment `6715180375`.
- `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, skill blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`, red-team modes blob `c211e9f545f94b636b119f1e721b475a31e925f9`, and protocol blob `25b38dc02bc0b0331ed03b0a4c7ff1b1e2a4ed00`.
- Current peers actually read: LSPV-1/489 `research/agents/lspv-1/2026-11-07_LSPV1_RESOLUTION_UNIT_DISCHARGE489.md`, blob `fd7949f397563efd6816527874e096b0e3e9f1ea`; LSPV-2/479 `research/agents/lspv-2/2026-11-07_1618_LSPV2_EXPONENT_PROMISE_FIREWALL479.md`, blob `8b4c8b549ae7445aecb21f2afd7a21cbac4f799a`; LSPV-3/485 `research/agents/lspv-3/2026-11-07_1632_LSPV3_AFFINE_ANCHOR_RANK485.md`, blob `a0c7b79173cfaef74ddf22f632bf12d1ef19fea4`; LSPV-4/481 `research/agents/lspv-4/2026-11-07_1636_LSPV4_FINITE_ENTRY_WITHOUT_EXPONENT_EXTRACTOR481.md`, blob `7a5db210734e1b13b3f50df152f0921471fc5d06`.
- Actual current Grok directory was enumerated; relevant `GROKPROOF/2026-11-07_1920_PROGRESS.md`, blob `231561ce216699f286b705a0056584789ba9ee99`, was read. Relevant Claude assessment `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`, was read from the actual Claude directory.

The local artifact subset still lacks `.codex/skills/pnp-research/scripts/preflight.py`; the required local command failed with file-not-found. Root `main.tex` again returned blob `68188a24badda635a5983fda1c381cdb694fd497` and zero readable bytes, so no ownership-region edit was attempted.

### Primary literature and proof-format controls

The search targeted unit-assumption discharge, learned-lemma/shared-DAG semantics, and proof trimming. Buss, Hoffmann and Johannsen's [Resolution Trees with Lemmas](https://arxiv.org/abs/0811.1075) establishes the proof-system context relating dag Resolution and lemma-bearing trees; it does not authorize a historical mixed rule. The [FRAT paper](https://doi.org/10.1007/978-3-030-79876-5_31) distinguishes original records, derived records and final-use information. Cruz-Filipe et al.'s [LRAT work](https://arxiv.org/abs/1612.02353) makes dependencies explicit; current LRAT trimming performs backward reachability from the empty clause. These controls motivated an exact sink-ancestry audit instead of treating the array length or a report field as work evidence.

Google-branded search was unavailable. Indexed primary-source search was used; queries and returned papers are recorded above.

### Required change-aware repository review

- `konard/p-vs-np` unchanged head `ecedd2b45f1c524d85c00b2da27a9c140025550c`; `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2` lists scoped theorem/axiom manifests, not a full mixed-calculus lower bound.
- `blkph0x/p-vs-np-proof-research` unchanged head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` separates finite, conditional and open claims.
- Proof/checker controls: `meelgroup/frat-xor` head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; `tanyongkiam/cake_lpr` head `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`, README blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; `peitl/short-proof` head `2c524cfceecf68b56f51d23f6b63255b502856d3`, README blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`; `marijnheule/drat-trim` head `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, README blob `eb6ffcc4a85ff1c74a5995b6caae4372381dcd47`.
- Research/formalization controls: `openai/math` head `4eaee87548250b2682affda7d05d947c05554bae`, README blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`; `anthropics/formal-math` head `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`, `eth/Challenge.lean` blob `6297ab1398884550253bdd1475704729d02ce89b`, whose ETH claims still contain explicit `sorry`. No repository title, build or manifest supplies the missing $R_{\mathrm{mix341}}$ theorem.

## Established-family/theorem/encoding/known-method ledger

| Family | Exact encoding/size | Published lower bound and model | Known methods/shortcuts | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin | One variable per edge. Each degree-three parity equation is encoded by the four signed 3-clauses excluding wrong parity. For $H$ vertices: $3H/2$ variables, $4H$ clauses, $N=\Theta(H\log H)$ encoded bits | Ben-Sasson--Wigderson 2001: $2^{\Omega(H)}$ ordinary shared-DAG Resolution size on expanders | GF(2) addition is a short algebraic control; extension variables, branching and shared lemmas must be allowed when native | Authenticate every historical mixed rule or prove a polynomial source-retracting simulation |
| Random proper strict 3-CNF $\mathcal F(n,3,8n)$ | $n$ variables and $8n$ proper signed width-three clauses; $N=\Theta(n\log n)$ under binary identifiers | Pang 2026 Theorem 7.2(a): reported exponential lower bound with high probability in its stated syntactic Res(polynomial) model | Paid definitions, affine guards, learned lemmas and shared DAGs are mandatory upper controls | No theorem transfers this bound to the complete historical mixed calculus |
| Pigeonhole principles | Standard PHP clauses; no strict-3CNF conversion is silently assumed | Haken: exponential ordinary-Resolution lower bound | Extended Resolution can be much shorter | Need an exact 3-CNF encoding plus lower-bound-preserving proof simulation |

The finite K4 packets and the LSPV-1/489 guard gadget below are validation controls, not proposed hard families.

## ITERATE: initial hypothesis falsified, branching lemma independently sustained

### 1. Recovered-checker proof-array audit

The checker source contains four relevant constraints: proof length is exactly $4|V|-1$; every parent must already exist; the last record must be affine contradiction $0=1$; and every original source must be in the last sink's backward ancestry. Independent traversal found **all proof records and all source records reachable** in every one of the seven fixtures:

| Inference/source counts | Fixtures |
|---|---|
| 15/16, 23/24, 31/32, 39/40, 47/48, 127/128, 39/40 | all have complete sink ancestry |

The exact checker accepted a legal independent topological reorder with the baseline output SHA-256 `af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be`. It rejected: inserting a legal but unreachable AND3 record before the sink, appending one after the sink, inserting one while incrementing the ignored reported inference count, deleting the first proof record, replacing the contradiction sink by a legal nonsink, and duplicating an inference ID.

For each bridgeless fixture the separate deletion witnesses show every source clause is essential. Soundness relative to source subsets plus binary fan-in then gives the elementary lower bound: a one-sink acyclic derivation depending on $m$ distinct essential source leaves needs at least $m-1$ binary inference nodes. The packet exhibits exactly $m-1$. This certifies the restricted SOURCE/AND3/XOR node minimum; it says nothing about absent historical RES/DEF/branch rules.

### 2. Ordinary-Resolution unit-assumption theorem

Let $F$ be a CNF, $l$ a literal, and $\pi$ an acyclic ordinary-Resolution refutation of $F\cup\{(l)\}$ with $L$ Resolution inferences. Traverse $\pi$ topologically. Copy each $F$ source and mark the assumption source missing. At every original resolvent $C$ maintain a previously derived clause

$$
D\subseteq C\cup\{\neg l\}.
$$

If both transformed parents retain the oriented pivot, resolve them. If a parent has lost the pivot, reuse that stronger parent because it is already a subclause of the original child union $\{\neg l\}$. If the missing unit assumption is a parent, reuse the other parent, which contains $\neg l$. At the empty sink, the retained clause is either empty or $(\neg l)$. Every retained inference is ordinary oriented Resolution; bypasses add no rule and no inference. Hence at most $L$ paid inferences remain. Sharing and topological order are preserved.

This independently confirms LSPV-1/489 Theorem 489.1. It is a proof in ordinary Resolution, not an empirical inference from the finite tests.

### 3. Exhaustive and accepted-byte controls

The Python audit enumerated all 26 nonempty nontautological clauses over three variables, every CNF with one to three distinct clauses, and all six possible literal assumptions. Among these, 2,850 satisfiable CNFs became UNSAT under the assumption (475 per assumption). A complete Resolution closure produced one refutation for each. The independent subset/bypass transformation discharged all 2,850:

- original branch proofs contained 4,278 Resolution nodes in total;
- transformed proofs emitted 1,428 Resolution nodes;
- 2,850 Resolution nodes were legally bypassed;
- no weakening, branch-local source or new discharge rule appeared.

The exact published LSPV-1/489 Python source, blob `486bb82733155b84ffbc1b1a71ceeada43abf310`, was fetched and executed directly: 24 gate facets, six blocker facets, 17 cover Resolution steps, three globally derived negative guard units, three joins, 23 paid Resolution ancestors, 19 source ancestors, 42 total ancestors, cover span 6, global span 9. The independent Python reconstruction reproduced every count; the separately authored Node verifier made 72 assertions and reproduced the 23/19/42 ancestry and both spans.

### Revised claim and cross-branch scope

**PROVED-RESTRICTED:** unit assumptions can be eliminated from ordinary Resolution refutations with no weakening and no inference-count increase; a finite guard cover plus all discharged negative guards closes every AND obligation by paid joins. Globally valid derived clauses may be shared once; branch-local conclusions may not leak before discharge.

**Still OPEN:** the recovered historical checker rejects RES/DEF as unknown, so this theorem does not prove that historical $R_{\mathrm{mix341}}$ contains the required source facets, Resolution records, paid definitions, guard cover, or any branch syntax. It gives a legal candidate derivation only in the explicitly distinct ordinary-Resolution control calculus.

## Work, evidence, span and machine-resource ledger

- **Logical work:** recovered fixtures contain respectively 15, 23, 31, 39, 47, 127 and 39 sink-reachable inference nodes. The peer control has 23 paid RES ancestors, 19 source ancestors and 42 total ancestor nodes. Distinct nodes are charged once.
- **Evidence bits:** compact recovered packet 77,714 bytes in this serialization; checker mutations 77,620--77,813 bytes; Python audit 13,565 bytes; Node verifier 4,159 bytes; raw ledger 5,578 bytes. The preserved historical packet is 197,514 bytes.
- **Construction/search:** exhaustive finite generation considered all one-to-three-clause subsets of the 26-clause universe and six assumptions, used truth-table filtering, constructed Resolution closure proofs, then transformed them. This search cost is excluded from ideal $W_R$ but charged here.
- **Verification/output:** Python producer: 1.1889 s wall, measured peak process-tree RSS 13,472 KiB. Independent Node: 0.3868 s wall, 42,356 KiB peak process-tree RSS. Sampling used `/proc` every 2 ms and may undercount brief peaks; values are host measurements, not FLMV bounds.
- **Parsing/source/index/head work:** every exact-checker case reparses the packet and rebuilds maps. Peer-source replay fetches and executes the complete 3,264-character source. Temporary packets are created and deleted per case.
- **Storage/retrieval/recomputation:** cases run sequentially and recompute closures; no cache or parallel asymptotic claim is made. Actual solver search, failures, retained clauses, references, output and checking remain separately chargeable.
- **Work/span/schedule:** the 23-node peer proof has unit-weight critical path 9. This is neither its machine time nor a claim of optimal depth/space.

## Status, artifacts and precise remaining gap

**Actual advance:** the suspected unreachable-record accounting defect is absent in the recovered fixtures; complete sink ancestry and exact rejection controls were established. More importantly, the new peer unit-assumption discharge theorem and 23-RES joined certificate survived independent proof, exhaustive finite controls and separately authored replay.

Artifacts:

- `experiments/review/lspv5_420_reachability_and_discharge_audit.py`, SHA-256 `e55db50ff4a0ea070f4c9bd515776f2e11543a37e76f472bd7e3b9e1c2a54638`.
- `experiments/review/verify_lspv5_420_reachability_discharge.mjs`, SHA-256 `6e744e1b48768e8147af85ef4d20d9f00955667ed89e32bf11851fb29034ba65`.
- `results/raw/review/2026-11-07_1648_LSPV5_REACHABILITY_DISCHARGE420.json`, SHA-256 `18ee15d57fc7d56228b9dda6ba6da74d1bfbbf66054e0260e0be56b5a13036d8`.

**Precise remaining gap:** authenticate historical RES, DEF, original defining facets, RES-to-AND3 ports and any branching/discharge production, then prove the ordinary-Resolution construction simulates every relevant native mixed step with polynomial paid overhead. Only after that can `[P2-C3]` feed an all-rule `[P2-B1]`; the noncircular B3 `[P2-B2]` remains independent and OPEN. **P versus NP remains OPEN.**
