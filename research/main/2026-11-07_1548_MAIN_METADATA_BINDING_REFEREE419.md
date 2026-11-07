# LSPV-5/419: recovered checker binds the logical core but not declared metadata

**November 7, 2026, 15:48 PST | Route B independent red team | COMPUTATIONAL/PROVED-RESTRICTED | P versus NP OPEN.**

**Exact tracker IDs:** material evidence for `[P2-D1]` and `[P2-D3]`; new result `[P2-L5-419]`. Dependencies `[P2-C3]`, `[P2-B1]` and `[P2-B2]` remain OPEN. Historical $R_{\mathrm{mix341}}$ grammar, weights, roles, schedules and the two-Route-A/three-Route-B allocation are unchanged.

## IDEA: claim card and falsifiers fixed before search

**Target.** Determine whether the exact recovered `/341` SOURCE/AND3/XOR checker binds the packet's declared Tseitin source metadata---graph, charge vector, clause ownership/pattern, deletion witnesses, summary and stated rule definition---to the clauses and proof it accepts.

**Initial hypothesis.** The checker strongly recomputes graph, charges, clause literals, source incidence, proof parents/rules and deletion witnesses, but consumes several descriptive fields only partially or not at all. Mutating an ignored report/provenance field should preserve acceptance and the baseline output hash; mutating a checked semantic field should reject.

**Quantifiers/model.** This is a finite field-read and mutation audit of recovered checker SHA-256 `0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae` against exact packet SHA-256 `12d723c92c683ec1a59e17d95d0d47156babe7febe27b7432dc01279abcb8d95`. It does not authenticate absent RES, LOCAL-CONVERT, DEF, branching or discharge rules.

**Falsifiers stated before search.** (F1) every metadata mutation rejects; (F2) only nonsemantic report fields are ignored while graph/charge/ownership fields are bound; (F3) a checked clause-literal mutation also accepts; (F4) an independent field-consistency audit shows every accepted-mutated field is consumed. The experiment refuted F1 and the strongest reading of F2, supported F3's negation, and refuted F4.

## SEARCH: continuity, primary specifications and repositories

### Project state actually read

- Complete `proof1.txt`, blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, and complete initial `proof2.txt`, blob `ad317008264aa0f0c75cdd5fc6a059437f16a815`.
- Historical governing handoff at required commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, file blob `033b54b87b7cbe94912af5cf67daa52859143a07`, and current same-path handoff blob `c3889a3e514ddbd747150dcb68607013a3b2d154`; current issue #3 body and seven current comments through LSPV-4/480 comment `6714649012`.
- `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`, and its complete red-team mode and research-protocol references. Root `main.tex` returned blob `68188a24badda635a5983fda1c381cdb694fd497` with zero readable bytes, so no whole-document or ownership-region rewrite was attempted.
- Current peers actually read: LSPV-1/488 `research/agents/lspv-1/2026-11-07_LSPV1_PAID_GUARD_RESOLUTION488.md`, blob `4481c9a978ce907fac10c789f756c41d9b252426`; LSPV-2/478 `research/agents/lspv-2/2026-11-07_1518_LSPV2_ORACLE_EXTENSIONAL_BARRIER478.md`, blob `408893cbba6071250eda48943c45f86bddbfd817`; LSPV-3/484 `research/agents/lspv-3/2026-11-07_LSPV3_AFFINE_NONLINEAR_STRATA484.md`, blob `a5a1fd0cc2ce55baacadd3831cbdf5ee75404fbf`; LSPV-4/480 `research/agents/lspv-4/2026-11-07_1540_LSPV4_FLMV_EXPONENT_SLACK_BUDGET480.md`, blob `fda77cf7d35dbc6f392715a7c38604af1592252e`.
- Actual Grok file `GROKPROOF/2026-11-07_1330_PROGRESS.md`, blob `35ad4749b1d9779eadce95e46145b4eb103b8224`; relevant Claude assessment `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

The local workspace is an artifact subset and lacks `.codex/skills/pnp-research/scripts/preflight.py`; the required local command failed with file-not-found. This limitation is recorded, not converted into a successful preflight claim.

### Primary proof-system and proof-format controls

Queries targeted FRAT original-clause identity, LRAT verified checking and the Cook--Reckhow proof-system definition. The [FRAT paper](https://doi.org/10.1007/978-3-030-79876-5_31) gives explicit original steps and unique clause identifiers; the current FRAT-XOR specification concretely separates original clause/XOR introductions from derived records. [Efficient Certified RAT Verification](https://arxiv.org/abs/1612.02353) gives LRAT hints and certified checkers, with original CNF clauses assigned identifiers before derived steps. [Cook and Reckhow 1979](https://www.cs.utoronto.ca/~sacook/homepage/cook_reckhow.pdf) studies polynomially checkable proof systems and relative simulation; it does not make a free-form packet's unconsumed `definition` string authoritative.

These controls sharpened the repair: a checker may validly omit redundant display fields, but then those fields must be explicitly nonnormative and must not be used as proof of source identity, calculus grammar or theorem status. If they are normative, their consistency must be checked or cryptographically bound to a checked canonical object. Google-branded search was unavailable; indexed primary-source search was used and logged.

### Required change-aware repository review

Both newly required repositories were unchanged: `konard/p-vs-np` head `ecedd2b45f1c524d85c00b2da27a9c140025550c`, actual `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research` head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, actual `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`. Neither authenticates historical $R_{\mathrm{mix341}}$.

Rotating controls were read at pinned current heads: `meelgroup/frat-xor` `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `format.md` blob `986a...` and `cake_xlrup/BINARY_FORMAT.md` blob `97bd...`; `tanyongkiam/cake_lpr` `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`, README blob `e94f...`; `peitl/short-proof` `2c524cf...`, README blob `93d209...`; `openai/math` `4eaee87548250b2682affda7d05d947c05554bae`, README blob `cc5b...`; `anthropics/formal-math` `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`, `eth/Challenge.lean` blob `6297...`, containing explicit `sorry`. These are evidence about formats, shortest Resolution search and trust boundaries, not P-versus-NP proofs.

## Established-family/theorem/encoding/known-method ledger

| Family | Exact 3-CNF/source size | Established theorem/model | Known legal shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin | One edge variable per edge; each degree-three parity equation becomes its four proper signed 3-clauses excluding the wrong parity. For $H$ vertices: $3H/2$ variables, $4H$ clauses, $N=\Theta(H\log H)$ encoded bits | Ben-Sasson--Wigderson 2001 gives $2^{\Omega(H)}$ ordinary shared-DAG Resolution size on expanders | GF(2) summation, extension variables and shared derivations are mandatory upper controls | Authenticate and lower-bound every historical mixed shortcut, or prove a source-retracting simulation |
| Random proper strict 3-CNF $\mathcal F(n,3,8n)$ | $n$ variables, $8n$ width-three clauses, $N=\Theta(n\log n)$ | Pang 2026 Theorem 7.2(a), reported exponential minimum in its stated syntactic Res(XOR) model with high probability | Paid extensions, mixed rules and shared DAGs are mandatory controls | No full historical mixed-calculus transfer |
| Pigeonhole principles | Standard PHP source; no strict-3CNF encoding is assumed here | Haken exponential ordinary-Resolution lower bound | Extended Resolution is stronger; equisatisfiability alone preserves no lower bound | Need exact 3-CNF encoding and proof-to-proof preservation theorem |

The focused mutations below use the existing certified-UNSAT K4 Tseitin packet. They are provenance/checker controls, not a new candidate hard family.

## ITERATE: bound core, unbound declarations

### Exact accepted mutations

The Python producer regenerated twenty single-field variants. The recovered checker accepted all ten unbound-declaration variants with the baseline stdout SHA-256 `af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be`:

| Mutated path | Replacement | Meaning |
|---|---|---|
| root `version` | forged version | schema declaration ignored |
| root `definition` | says RES and DEF are free | grammar declaration ignored |
| `summary[0]` | `{}` | record contents ignored; only array length checked |
| `clauses[0].pattern` | `0` to `7` | source-pattern provenance ignored |
| `properties.variables` | `6` to `999` | reported count ignored |
| `properties.sourceClauses` | `16` to `0` | reported count ignored |
| `properties.inferences` | `15` to `0` | reported count ignored |
| `properties.oddUnsat` | `true` to `false` | reported status ignored |
| `properties.evenSat` | `true` to `false` | reported status ignored |
| `properties.predictedMinimum` | `15` to `0` | reported optimum ignored |

This includes more than cosmetic summary prose: `clauses[0].pattern` purports to identify the local parity pattern, and root `definition` purports to state the calculus. Their acceptance proves only that the checker derives or ignores these claims elsewhere; it does not make their forged contents true.

### Bound controls and independent challenge

Ten proof-semantic controls all rejected: graph self-loop, charge flip, clause-owner mutation, clause-literal mutation, duplicate source ID, wrong deletion source, wrong even witness, wrong proof parent, changed essential count and changed summary length. Thus the run did **not** find a false logical clause, invalid graph/charge pair or malformed proof accepted.

The separately authored Node verifier rebuilt all twenty mutations and made 52 assertions: ten checker accepts, ten checker rejects, exact output-hash equality for the accepts, and strict consistency rejection of all twenty. It independently requires the declared metadata to agree with the recomputed graph, clauses, witnesses and proof.

### Revised claim and weakest repair

**Revised claim.** The recovered checker authenticates a substantial logical core---graph topology, cubicity/connectivity, charges, clause vertex/literals/IDs, source incidence/parity, proof dependencies/rules/tables, deletion witnesses, even witness and essential count---but does not authenticate the ten listed declarations. In particular, packet `definition` is data, not authority for historical RES/DEF grammar, and `pattern` is not source provenance even though literal signs are checked directly.

Two repairs are sufficient, depending on intended language:

1. **Nonnormative-field repair:** specify the ignored fields as display-only, exclude them from certificate identity and theorem claims, and compute displayed values solely from the checked core.
2. **Normative-field repair:** check every field against a canonical recomputation, bind the canonical bytes, and fail on mismatch. Grammar authority still requires a historically authenticated external specification; self-description cannot bootstrap it.

Either repair defines or clarifies a checker language; neither silently changes historical $R_{\mathrm{mix341}}$. The previous parser repairs `[P2-L5-414/415/416/417/418]` remain separate prerequisites for raw-byte and ID identity.

## Work, evidence, span and machine-resource ledger

- **Logical work:** all ten accepted variants retain the same 15 checked inference nodes and baseline output hash. No $W_R(F)$ decrease was shown.
- **Explicit evidence:** compact baseline 77,713 bytes; twenty variants 77,522--77,717 bytes; preserved historical packet 197,514 bytes; checker 9,359 bytes.
- **Construction/search:** Python deep-copies the parsed packet, performs one mutation, writes a temporary packet and launches the exact checker per case. Discovery/search is excluded from ideal $W_R$ but charged here.
- **Verification and output:** Python producer: 20 cases, 2.7116 s wall, measured peak process-tree RSS 13,552 KiB. Independent Node replay: 52 assertions/20 cases, 2.5664 s wall, measured peak process-tree RSS 48,072 KiB. `/proc` sampling at 2 ms can undercount short-lived peaks; these are host measurements, not FLMV bounds.
- **Parsing/source/index/head reads:** each checker launch reads and parses the complete compact packet, reconstructs graph/source/proof maps, and captures output. The strict verifier recomputes all declared relations. Temporary packets are deleted after each case.
- **Storage/retrieval/recomputation:** producer 11,509 bytes, independent verifier 5,949 bytes, raw ledger 15,035 bytes, plus packet/checker copies and child-process state. Cases are sequentially recomputed; no cache-based asymptotic claim is made.
- **Work/span/schedule:** cases are independent and could run concurrently, but published scripts run sequentially. No weighted critical-path theorem, reference-cost theorem or same-machine FLMV schedule is claimed.

## Status, artifacts and remaining gap

**Actual advance:** an exact read/use matrix for twenty packet fields, including ten accepted forged declarations and ten rejected semantic controls, plus independent strict consistency verification. Status `COMPUTATIONAL/PROVED-RESTRICTED` for the recovered SOURCE/AND3/XOR checker only.

**Independent challenge:** some ignored fields may have been intended as redundant display metadata. That does not make the logical checker unsound, but it bars using those fields as evidence of source provenance, calculus grammar or minimum-proof status. No satisfiable source was accepted, no established-family lower bound transferred, and no proof was shortened.

Artifacts:

- `experiments/review/lspv5_419_metadata_binding_audit.py`, SHA-256 `09fea2d68404ed0bdd4d205d63292faa5332f2e51d2786ff7ee9e95288a4f0c0`.
- `experiments/review/verify_lspv5_419_metadata_binding.mjs`, SHA-256 `c18db18d8ee059ced1419215dd0409b0f2f422b62ed6b7a8f0213d762ce1e47c`.
- `results/raw/review/2026-11-07_1548_LSPV5_METADATA_BINDING419.json`, SHA-256 `3bb96cff5a62f799507448b682cc9e4a5ce90762e11c14d1f596d4011c9a0839`.

**Precise remaining gap:** recover historical authority for every native rule and classify every packet field as normative or display-only; then authenticate original source production and test RES, LOCAL-CONVERT, DEF, branching and assumption-discharge records before attempting `[P2-C3]`. Full mixed lower bound `[P2-B1]` and noncircular B3 `[P2-B2]` remain OPEN. **P versus NP remains OPEN.**
