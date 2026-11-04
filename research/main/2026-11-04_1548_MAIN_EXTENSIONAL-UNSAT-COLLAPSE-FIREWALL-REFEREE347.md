# REFEREE347 — extensional UNSAT collapse and authenticated-cut dichotomy

**PNP Independent Proof Red Team | November 4, 2026, 15:48 PST**  
**Status:** PROVED/EXACT elementary extensional-collapse theorem; PROVED/EXACT authenticated-cut dichotomy under stated translators; COMPUTATIONAL finite controls; fixed full `R_mix341`, B1, B2, B3, unrestricted SAT hardness, and P versus NP OPEN.

## IDEA before search

The missing obligation is a signed-hypergraph/DAG invariant that remains meaningful under shared circuits, GF(2), auxiliary definitions, lazy representations, and arbitrary uniform algorithms. The initial candidate was the **minimum fully encoded authenticated separator work** across all source-rooted derivations and all exact representations.

Assumptions: one fixed `R_mix341`; exact source bytes; no semantic oracle; uniform polynomial-time verification; source parsing, proof/cut payload, construction, access, checking, output and peak space all charged. Falsifiable prediction: if the separator measure depends only on the represented Boolean relation, compact or constant representations collapse it; if it authenticates the full source ancestry, it becomes polynomially equivalent to ordinary encoded certificate work and is system-relative rather than absolute.

Registered falsifiers:

1. all UNSAT CNFs denote the same constant-false Boolean function;
2. a local cut can contain only the root's at-most-two predecessors while hiding all ancestry;
3. equality/parity boundary matrices can be exponentially large while definitional circuits and GF(2) certificates remain linear;
4. a large live frontier can be defeated by rereading or recomputation, so no schedule-free space bound follows.

## Established certified anchors, exact scope

For the standard explicit unary `PHP_{h+1}^h`, with `h(h+1)` variables and `(h+1)+h*binom(h+1,2)` source clauses, Haken proves

`exists c>0 exists h0 forall h>=h0 forall ordinary authentic shared-DAG Resolution refutations pi: |pi| >= 2^(c h)`.

The declared signed binary-index CNF encoding has `N_h=Theta(h^3 log(h+2))` bits. The proof system has authentic source clauses and ordinary Resolution only: no DEF, ER, GF(2), AND3, LOCAL-CONVERT, implicit circuit, or arbitrary machine transition. Cook's Extended Resolution proof of the same pigeonhole family is polynomial. Therefore Haken does not lower-bound `R_mix341` or unrestricted SAT computation.

Urquhart's expander Tseitin lower bounds are likewise ordinary-Resolution results. Project LSPV-2/341 gives exact linear `4h-1` paid-node mixed proofs for bridgeless cubic odd Tseitin by compact GF(2) reasoning. These are mandatory countercontrols, not transfers.

## SEARCH

### Project, issue, Grok and Claude

Read first the controlling `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` and current issue #3. Material current paths read were:

- `research/main/2026-11-04_1352_MAIN_CERTIFICATE-WORK-PEQUIVALENCE-FIREWALL-REFEREE345.md`;
- `research/main/2026-11-04_1445_MAIN_BOUNDED-NAMED-INTERFACE-REPAIR-REFEREE346.md`;
- `research/agents/lspv-1/2026-11-04_1500_LSPV-1_PHP_COFAC_MITER_HARDNESS_FIREWALL401.md`;
- `research/agents/lspv-2/2026-11-04_1513_LSPV-2_ADAPTIVE_SEMANTIC_LOCALITY402.tex`;
- `research/agents/lspv-3/2026-11-04_1524_LSPV-3_DECOMPOSABLE_PORT_SUPPORT404.tex`;
- `research/agents/lspv-4/2026-11-04_1536_LSPV-4_GUARDED_HORN_PROJECTION_FIREWALL397.md`;
- `research/agents/lspv-3/2026-11-02_1651_LSPV-3_SIGNED_EXPANDER_CAMOUFLAGE347.tex`;
- `research/agents/lspv-4/2026-11-04_0236_LSPV-4_CUT_INTERFACE_TWO_WAY_FIREWALL382.tex`;
- `research/agents/lspv-4/2026-11-04_0340_LSPV-4_EXACT_OR_CUT_ACQUISITION383.tex`.

LSPV-1/401 already proves that an identically-zero circuit can have Haken-hard ordinary-Resolution cofactor miters, while ER escapes. LSPV-2/402 proves only an extensional-port width-or-leaves compiler. LSPV-3/404 gives a polynomial support checker only for decomposable nondegenerate gates and explicitly fails under reconvergence. LSPV-4/397 rejects unproved Horn-consequence validation from an arbitrary 3-CNF. None supplies B3.

Current Grok `GROKPROOF/2026-11-04_2315_PROGRESS.md` was located from the repository. It proves only a restricted black-box writing bound and leaves white-box residual extraction open; its equality-boundary exponent comparison is not a strict asymptotic separation. Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, `..._1521_CLAUDE_ONETAPE-0001.tex`, and `..._0939_CLAUDE_DIRECTPRODUCT-0001.tex` concern restricted alternation/sequential-access or conditional portfolio models. They provide no exact-source mixed proof compiler or B3.

### Primary literature and actual queries

Actual web queries included:

- `Cook Reckhow propositional proof systems syntactic formulas semantic equivalence proof complexity primary paper PDF`;
- `proof complexity semantically equivalent formulas different proof lengths extended resolution primary paper`;
- `Haken pigeonhole principle resolution exponential Cook extended resolution polynomial primary sources`;
- `p-simulation proof systems source formula preserving translations Cook Reckhow primary`;
- `Resolution remains hard under equivalence PDF`.

Sources read beyond snippets where available:

- Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, full author PDF, especially Definitions 1.3 and 1.5: proofs are encoded strings for the **same output formula**, and p-simulation is a uniform polynomial-time proof translator.
- Haken, *The Intractability of Resolution*, publisher theorem/abstract metadata; direct full text was blocked by the publisher.
- Kleine Büning and Lettmann, *Resolution Remains Hard Under Equivalence*, DOI `10.1016/S0166-218X(99)00055-4`: its conditional theorem concerns deriving some consequence from polynomial-size equivalent CNFs, not refuting an already contradictory constant representation. This distinction is consistent with Theorem 347 below.
- Bryant/Heule and ER literature already reviewed in REFEREE346: compact extensions can shorten pigeonhole proofs.
- The 2026 open article *The Relative Strength of #SAT Proof Systems*: p-simulation preserves the same source formula, and arbitrary circuit equivalence needs source certificates; compact representations do not authenticate themselves.

Direct Google-branded UI was unavailable. General web search was used, and no claim of a Google-specific search is made.

### OpenAI GitHub

Actual scoped queries were `proof certificate source formula equivalence`, `Cook Reckhow proof system p simulation`, `Resolution refutation CNF`, and `Decision DNNF certificate SAT`. No applicable separator or B3 compiler was found. The files actually read were:

- `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean`: concrete execution/setup/visit cost bounds, explicitly not an arbitrary callback theorem;
- `openai/math/lean/OAI/Algorithms/SubexponentialSAT/RuntimeAssembly.lean`: `ImplementationCertificates` are explicitly open obligations and no satisfying primitive machine is constructed.

Code is implementation evidence only, not a mathematical transfer theorem.

## ITERATE I: extensional UNSAT collapse

### Theorem 347A (no nontrivial purely extensional refutation lower bound)

Fix any refutation system `R` containing genuine ordinary Resolution, with free authentic source clauses and nonnegative paid-node weights. For every `n>=1`, let `C_n` be a class of proper `n`-variable CNFs containing

`U_n = {(x1),(not x1)} union {(x1 or xi),(x1 or not xi): 2<=i<=n}`.

Every variable occurs, every source clause is nonempty and nontautological, `U_n` denotes constant false, and it has a one-paid-node Resolution refutation.

Let `I_n(F)` be nonnegative and **extensional**: if `F` and `G` have the same truth table on the aligned named variables, then `I_n(F)=I_n(G)`. If `I_n(F)<=W_R(F)` for every UNSAT `F in C_n`, then for every UNSAT `F in C_n`,

`I_n(F)=I_n(U_n)<=W_R(U_n)<=1`.

If the input grammar permits the empty clause as a free source, the upper bound strengthens to zero.

#### Proof

Every UNSAT `n`-variable CNF has the all-zero truth table, hence is semantically equivalent to `U_n`. Resolve `(x1)` with `(not x1)` to obtain the empty clause in one paid inference. Apply extensionality and the assumed lower-bound inequality. QED.

### Consequence for signed hypergraphs and separators

Any signed-hypergraph/DAG measure minimized over **all** exact representations of the Boolean relation may select `U_n`; it is therefore at most one on every closed UNSAT relation. Truth-table rank, model set, ideal logical state, minimum relation circuit, or an unrooted separator cannot prove a growing refutation lower bound.

The result does not say source structure is irrelevant. It proves the opposite: every nontrivial candidate must retain authenticated source identity or restrict permissible transformations. Once that source is retained, the invariant is intensional and its robustness must be proved by uniform source-preserving translations.

This is an elementary firewall, not a P-versus-NP theorem and not a novelty claim about general proof complexity.

## ITERATE II: authenticated-cut dichotomy

Define a **strong cut certificate** `(pi,K,sigma)` for exact source `F` to include a complete valid source-rooted `R` refutation `pi`, a cut `K` intersecting every source-to-root path, and semantic/authentication data `sigma`. Charge `|F|`, all proof/cut/payload bits, verifier work and verifier peak space. Let `SC_R(F)` be the minimum charged work and let `CE_R(F)` be REFEREE345's minimum fully encoded proof/checking envelope.

### Theorem 347B (strong cuts are certificate-work equivalent)

If one fixed polynomial-time translator adds a canonical valid cut annotation to every `R` proof and one fixed polynomial-time translator erases/checks that annotation while preserving the exact source and proof, then

`CE_R(F) <= poly(SC_R(F))` and `SC_R(F) <= poly(CE_R(F))`.

The first direction discards the annotation and retains the full authenticated proof. The second chooses a canonical cut, for example the root or all proof nodes, and writes its checked annotation. Thus strong separator work is another p-equivalent certificate encoding, not a new absolute invariant.

If ancestry is not recursively authenticated, the root's at-most-two predecessors form a cut of size at most two in binary-premise `R_mix341`. This local record hides the entire cost of proving its parents. Hashes or pointers repair nothing unless their ancestry is checked, returning to the strong case.

Therefore the candidate has an exact dichotomy:

1. **purely semantic or locally authenticated:** trivial/unsound as a growing refutation lower bound;
2. **fully exact-source authenticated:** polynomially equivalent to encoded certificate work within a declared p-equivalence class, hence representation-relative.

### Theorem 347C (raw-node p-equivalence collapse)

If a class of exact-source proof representations is closed under `Pack`, where one paid `PACK` node contains and replays a complete serialized proof, then no measure can both polynomially lower-bound raw paid-node cost in every representation and yield a superpolynomial representation-invariant lower bound. `Pack(P)` is exact-source p-equivalent to `P` on fully encoded proof strings but has one outer paid node. The packed evidence and replay may remain exponential; only raw node count collapses. Counting those bits restores REFEREE345 certificate work, not representation-independent node cost.

### Theorem 347D (uniform recognizable-family terminal)

For every polynomial-time recognizable UNSAT CNF family `H`, one fixed uniform sound complete exact-source certificate system can give every `F in H` a constant certificate beyond the source. Its verifier first parses the exact source, accepts a special empty certificate only when recognition proves `F in H`, and otherwise uses a complete assignment-table certificate listing, for every assignment, an authentic source-clause index falsified by that assignment. The fallback is polynomial-time in source-plus-certificate length and cannot accept a SAT formula because a satisfying assignment has no falsified clause.

Taking `H` to be canonical unary PHP gives linear parsing/recognition work and constant extra certificate bits on a family that is exponentially hard for ordinary Resolution. This is one uniform verifier, not per-input hardcoding. Therefore exact source-byte authentication alone cannot make a measure invariant across all sound complete proof systems; one must fix a grammar or require a uniform exact-source p-simulation into it.

## Specialist falsifiers and fully charged corrections

- **Compact equality:** the audited `EQ-MISMATCH_n` boundary equality matrix is `I_(2^n)`, but local XOR definitions plus a balanced mismatch OR tree have a source-authenticated strict-Resolution refutation in `5n-1` inferences and `O(n log n)` encoded bits. Matrix size/rank is not an absolute proof-work lower bound. Log-rank and deterministic communication remain linear and are not refuted.
- **Compact parity:** direct parity CNF needs `2^(n-1)` blockers, but GF(2) or a prefix-XOR circuit uses linear structure. Any table lower bound is representation-restricted.
- **One-shot frontier:** a parity root followed by outputs `y_i=x_i XOR r` has linear live frontier if rereads are forbidden, but a two-pass random-access schedule uses `O(m)` time and `O(log m)` workspace. Frontier is exact only for the declared no-reread schedule.
- **Lazy residuals:** with `A=2^k` assignments and total explicit residual volume `B`, eager emission costs `Omega(B)`. A lazy generator costs according to actual probes `P*g`; there is no `Omega(B)` lower bound unless all bits are queried. Source indices, canonicalization, cache, recomputation and output remain charged.
- **Recognizable-family terminal:** one fixed sound complete proof system can give constant certificates to canonical PHP by exact source recognition and use a full assignment-table fallback elsewhere. This defeats invariance across arbitrary sound systems without per-input nonuniformity; recognition still costs `O(|F|)`.
- **Nonuniform representation choice:** choosing a different hardcoded proof representation per input or per length violates the fixed-uniform quantifiers. A valid comparison fixes the systems and translators first.

## Verification

Producer `experiments/arc/lspv5_347/extensional_unsat_collapse_referee347.py` and an independently written no-import JavaScript checker cover:

- proper constant-false unit-core representations for `n=1..12`, each with an independently replayed one-node Resolution refutation;
- all 256 CNFs over two named variables: 95 SAT and 161 UNSAT, with all 161 UNSAT formulas sharing exactly the zero truth table;
- explicit unary PHP for `h=1,2,3`, plus one-collision-deletion SAT siblings;
- odd/even K4 Tseitin controls with 0/8 models;
- seven malformed encodings and five corrupted proof records, all rejected.

Producer: 497 checks. Independent JavaScript: 48 checks. Raw SHA-256: `05824aef0beb912e99333e6d124b8e1d2952c63d44a93f7c539651237c180b98`.

Truth-table enumeration is an offline finite diagnostic and is not claimed as a SAT algorithm. Constructing `U_n` takes `O(n)` clauses and `O(n log n)` signed-ID bits. Its proof checks with two source reads, one pivot check, and explicit empty output. All materialized bytes and checking work are charged.

## Exact status and B bridges

- **PROVED/EXACT:** Theorem 347A, purely extensional UNSAT collapse.
- **PROVED/EXACT under explicit translators:** Theorem 347B, strong-cut/certificate-work polynomial equivalence.
- **PROVED/EXACT:** Theorem 347C, raw-node collapse under exact-source p-equivalent packing.
- **PROVED/EXACT:** Theorem 347D, one fixed recognizable-family terminal plus complete table fallback.
- **PROVED/RESTRICTED:** no-reread live-frontier lower bound and its two-pass counterexample; extensional-port and decomposable-gate project lemmas.
- **COMPUTATIONAL:** finite SAT/UNSAT, PHP, Tseitin, malformed and corrupted-proof controls.
- **FALSIFIED:** truth-function-only, full boundary-matrix size/rank, uncharged table materialization, raw cut width, or schedule-free frontier as representation/algorithm-independent refutation lower bounds.
- **OPEN:** exact full `LOCAL-CONVERT` grammar and node-to-bit polynomial balance for fixed `R_mix341`.
- **OPEN:** B1, B2, B3, a superpolynomial `Wbar_Rmix341`, unrestricted SAT hardness, and P versus NP.

The order remains `max_F min_pi`, with one fixed system before inputs. No per-input representation selector is substituted for a uniform decider. Fully encoded strong-cut B1/B2/B3 would imply the raw-node versions, but the converse needs the still-open node-to-bit normal form.

## Next unresolved step

Stop seeking a truth-function-only intrinsic lower bound for closed UNSAT formulas. Freeze the exact source-authenticated representation class and `LOCAL-CONVERT` payload semantics, then ask the narrower, mathematically coherent question:

> Are all legal `R_mix341` source representations mutually exact-source p-simulable with a uniform polynomial envelope, and does every polynomial SAT decider's rejection computation translate into one member of that fixed class?

The first clause is a representation-equivalence theorem; the second is B3/reflection. Neither is proved. A successful invariant can be robust only inside the first declared equivalence class, not across arbitrary semantically equivalent representations.

No root `main.tex` edit was attempted; publication is through the dated role-owned report, reproducibility artifacts, five-role handoff and issue #3.
