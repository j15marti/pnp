# REFEREE447: Independent source-set and PC-padding audit of the published opposite-characteristic strict-3CNF transfer

**2026-11-08 16:54 PST | LSPV-5 independent red team | Route B | exact node [P2-L5-447]**

**Verdict.** The elementary padding theorem in **[P2-L1-518]** survives an independent formal-polynomial audit. For each former binary clause $B$, the two strict clauses have falsity polynomials $Q_B(1-z)$ and $Q_Bz$, whose sum is $Q_B$; substitution $z=0$ commutes with both PC inference rules and maps the complementary padded axiom pair to $Q_B,0$. Pang's primary TeX also supports the fixed-$r$, opposite-characteristic model qualification used in /518. One source-authentication refinement is required: the paper writes uniqueness clauses for $a\ne b$, which is an ordered-index notation if expanded literally, but the two orders are identical clauses and Pang's polynomial system is a set. Thus the exact counts $24h$ and $57h/2$ are canonical **clause-set** counts. A byte-level or multiset encoder must explicitly choose $a<b$ or deduplicate. This does not change the PC degree or fixed-$r$ proof-size conclusion.

This is material evidence and scope refinement for **[P2-L1-518]**, **[P2-F6]**, and the missing-transfer node **[P2-C3]**. It does **not** authenticate the historical mixed grammar **[P2-D1]**, prove the full mixed lower bound **[P2-B1]**, or prove noncircular same-calculus B3 **[P2-B2]**. P versus NP remains OPEN.

## IDEA registered before search

**Initial repair hypothesis.** The external XLRUP provenance/status boundary found in **[P2-L5-446]** can be repaired by a uniform exact-byte manifest wrapper with polynomial charged overhead, while the historical four-hint-to-binary-rule gap stays open.

**Falsifiable prediction.** Hashing the complete source/proof bytes, checking the pinned executable identity, and requiring an exact success marker would separate verified, rejected, malformed, and source-rebound inputs without a semantic oracle.

**Registered falsifiers:**

1. the official checker API already binds exact source bytes and returns distinct failure status;
2. no syntactic wrapper can distinguish the cases without deciding SAT/equivalence;
3. hashing, parsing, or verification is nonuniform or superpolynomial;
4. the frozen historical /341 calculus already authenticates an equivalent four-premise rule.

## SEARCH changed the target

Before implementing that secondary wrapper, the fresh tracker and coordination read exposed the newer peer node **[P2-L1-518]**, which claims a published established-family transfer directly relevant to the user-prioritized Route B gap. The run therefore pivoted to the higher-value exact falsifier: independently test its source convention, polynomial identities, and theorem quantifiers. The wrapper repair remains a separate engineering target; no credit for it is claimed here.

### Governing project state read

- Full trackers: `proof1.txt` initial blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; `proof2.txt` changed concurrently during the run and was refetched before publication. Exact current SHA is recorded in the publication receipt/readback rather than treating the initial value as current forever.
- Five-role refocus at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, file blob `033b54...`; current issue #3 through the latest visible comment page.
- `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`; `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`; full research instructions and modes.
- Historical declaration `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`; recovered exhibited checker `experiments/arc/lspv2_341_independent_verify.js`, blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. Fresh inspection again found the checker covers the exhibited AND3/XOR subset, not a full Resolution/LOCAL/DEF/branching implementation.
- Peer /518 report blob `407ca3822d21387a4710d8ec41aebc831cda7856`; published JS blob `08a6718b663e0144d830490e0d428b06432ec2b3`; raw blob `10e428ec4e944cf9c29c28ff8daf9b1324b880c6`; handoff blob `382432e13b8f3c99622fa569456d7e527f5b923a`.
- Current Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md`, blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`; current Claude world-ledger artifact `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`, blob `79e4d4e...`. Neither supplies the present PC simulation or historical transfer.

The scratch environment contained no repository checkout, root `main.tex`, `AGENTS.md`, or local project skill. That is an environment-layout limitation. Authoritative project files were read through GitHub, and the local script is an independent reproducer, not an execution of the historical checker.

### Primary source and literature checks

The actual arXiv source archive for Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, was downloaded and inspected, not inferred from search snippets:

- archive SHA-256 `bdfec0ad02594c0e847c4849f492fc038aa18b2cb40a83933efc0e9a1d631bec`;
- `deg--size.tex` SHA-256 `5865b5044471163104d58bdef55e4460bbb0107b852ec02e2be7bde2b09e49d8`;
- Section 1 defines clause falsity polynomials, PC linear-combination and variable-multiplication rules, syntactic $\operatorname{Res}(\mathrm{PC}_r/\mathbb F_p)$, finite DAG refutations, and node-count size;
- the quantitative theorem says that, for fixed $p,r$ and constant width, linear PC degree implies exponential DAG size;
- Section 7 defines one-hot $\mathrm{Tseitin}_q(G,b)$ and states the fixed-prime $q\ne p$, fixed-degree regular edge-expander lower bound;
- the source explicitly says that the cited encodings differ and asserts a constant-degree substitution/consequence simulation. This remains an external 2026 preprint claim grounded in cited earlier PC-degree work, not a theorem newly proved by this project.

The indexed search also checked the earlier Alekhnovich--Razborov opposite-characteristic PC lower-bound citation and mandatory Cook ER/Tseitin controls. A Google-branded interface was unavailable; no claim of Google use is made.

### Required repository change review

Pinned change-aware checks found no relevant delta that defines historical `R_mix341` or proves B3:

- `konard/p-vs-np` head `ecedd2b45...`, `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`;
- `blkph0x/p-vs-np-proof-research` head `7dedc73...`, `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`, `REVIEW_ADDENDUM.md` blob `6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70`;
- `meelgroup/frat-xor` head `18cd6bc...`, external XLRUP only;
- `tanyongkiam/cake_lpr` head `033aad...`; `CakeML/cakeml` head `b3e6ea...`; `peitl/short-proof` head `2c524c...`; `openai/math` head `4eaee8...`; `anthropics/formal-math` head `16a5ce...`.

Repository names, CI badges, and formalization labels were not treated as proof of the target theorem.

## ITERATE: independent theorem audit

### 1. Exact family/encoding ledger

| Field | Audited statement |
|---|---|
| Family | One-hot mod-3 Tseitin on an oriented connected 3-regular edge-expander $G$ with $h$ vertices and nonzero total charge |
| Original variables | $3|E|=9h/2$ Boolean indicators $x_{e,a}$ |
| Canonical original clauses | $3h/2$ existence + $9h/2$ distinct uniqueness + $18h$ forbidden-flow = $24h$ |
| Strict encoding | Replace each binary $B$ by $(B\vee z)\land(B\vee\neg z)$ for one globally fresh $z$ |
| Strict size | $9h/2+1$ variables, $57h/2$ proper signed three-literal clauses, $\Theta(h\log h)$ explicit bits |
| Published model | Fixed-$r$ syntactic $\operatorname{Res}(\mathrm{PC}_r/\mathbb F_2)$, DAG size = number of nodes |
| Lower bound | Conditional on Pang v2 and cited degree theorem: $\exp(\Omega_r(h))$ for every fixed $r$ |
| Known shortcut | Linear-size $\operatorname{Res}(\mathrm{lin}_{\mathbb F_3})$ proof in the matching characteristic; paid historical Boolean-gate/algebraic shortcuts remain to be tested |
| Remaining transfer | Every legal historical mixed shared-DAG proof must be simulated at fixed $r$, or a legal shortcut must falsify that transfer |

Certified UNSAT, certified proof-size hardness, and empirical solver difficulty are distinct here. Nonzero total charge proves UNSAT. The exponential statement is restricted-system proof-size hardness conditional on the named theorem. No empirical solver-runtime hardness is claimed.

### 2. Source-set convention

Pang writes the edge uniqueness clauses as $\neg x_{e,a}\vee\neg x_{e,b}$ for $a\ne b$. Literal ordered expansion gives six records per edge, but $(a,b)$ and $(b,a)$ are the same clause. In the paper's set-valued $\mathcal Q(F)$ semantics, they collapse to the three unordered clauses.

The independent generator checked $h=4,6,8,10$:

| $h$ | ordered records | distinct uniqueness clauses | canonical original clauses | strict clauses |
|---:|---:|---:|---:|---:|
| 4 | 36 | 18 | 96 | 114 |
| 6 | 54 | 27 | 144 | 171 |
| 8 | 72 | 36 | 192 | 228 |
| 10 | 90 | 45 | 240 | 285 |

Therefore /518's count and polynomial argument are correct for a canonical clause set. The phrase “exact source clause multiset” needs the extra convention $a<b$ or canonical deduplication. If an external format intentionally preserves duplicate records, the record count changes by $9h/2$, but duplicate identical axioms do not change minimum PC degree or the existence of a proof DAG; exact source-byte hashes do change.

### 3. Formal-polynomial simulation

The independent checker represents a polynomial over $\mathbb F_2$ as a set of formal monomials and uses symmetric difference for addition, without silently multilinearizing. It exhausts all four signed binary clauses on two different old variables.

For $B=(\ell_1\vee\ell_2)$,

$$
Q_{B\vee z}=Q_B(1-z),\qquad Q_{B\vee\neg z}=Q_Bz,
$$

so over $\mathbb F_2$ (indeed over any field),

$$
Q_{B\vee z}+Q_{B\vee\neg z}=Q_B.
$$

This costs degree at most three and establishes the old-to-strict PC simulation. For the strict-to-old direction, evaluation at $z=0$ maps the two new axioms to $Q_B$ and $0$. The script separately checks the two PC inference forms on a finite basis of formal lines:

$$
\sigma(f+g)=\sigma(f)+\sigma(g),\qquad
\sigma(x_if)=x_i\sigma(f),\qquad
\sigma(zf)=0.
$$

All **214** assertion-accounted symbolic/source checks passed. A same-polarity corruption is rejected because $Q_{B\vee z}+Q_{B\vee z}=0\ne Q_B$. Reusing an old variable in place of fresh $z$ and repeated-variable clauses are rejected as violations of proper strict-3CNF syntax.

This independently supports

$$
D_{\rm PC}(F_{\rm old};\mathbb F_2)
\le D_{\rm PC}(F_{\rm strict};\mathbb F_2)
\le \max\{3,D_{\rm PC}(F_{\rm old};\mathbb F_2)\}.
$$

No equisatisfiability-only step is used.

### 4. Independent challenge and shortcut control

- **Global $z$ branching:** setting either $z$ value returns the same original hard formula. This is an upper-control branching strategy, but a valid split must discharge both cases and does not itself falsify the fixed-$r$ lower bound.
- **Characteristic-3 algebra:** Pang's corollary gives a linear-size proof in the matching field. This is decisive evidence that algebraic shortcuts must not be excluded. It is not a native `R_mix341` proof until the exact historical GF(2)/gate/LOCAL interfaces and costs are authenticated.
- **Extension variables:** Cook ER demonstrates why an ordinary or fixed-$r$ lower bound does not automatically survive a stronger system. The missing all-rule simulation remains the actual Route B bottleneck.
- **Branch sharing:** the ideal minimum may share nodes and choose its proof after the fact. The Pang theorem already counts DAG nodes, but its rules are not the historical mixed rules.

## Resource ledger

| Phase | Observed/bounded cost |
|---|---|
| Primary source download/read | 31,255-byte archive; 80,057-byte TeX |
| Local checker | 7,380-byte Python source; formal polynomial/source-set enumeration only |
| Raw evidence | 3,100-byte JSON |
| Replay observation | 1,295,253 ns and 11,648 KiB platform-reported maximum RSS in one CPython run |
| Logical proof nodes | Not measured by the checker; external theorem counts Res(PC) DAG nodes |
| Explicit evidence bits | Source/script/raw sizes above; Git blobs and SHA-256 recorded separately |
| Search/construction | Charged as actual project/source reads and local execution; no discovery-free algorithm inferred |
| Parsing/index/head reads | Project trackers, issue, governance, peer reports, primary TeX, and repository pins were explicitly read |
| Verification | 214 finite formal/source assertions; no historical native checker run |
| Output/update | Report, code, raw, handoff, tracker replacement, root owner-region reconciliation, and issue readback are separate publication phases |
| Cache/retrieval/recomputation | Local extracted source and generated JSON retained for this run; not counted as proof-node work |

The observed replay is a finite validation cost, not an asymptotic proof-search bound. Minimum logical work, weighted span, and a realizable time/space schedule remain separate quantities.

## Status and next exact gap

**Actual advance:** /518's non-equisatisfiability PC padding transfer is independently validated at the formal-polynomial level, and its source-count claim is narrowed from an implicit multiset reading to an explicit canonical clause-set convention. This strengthens the established-family ledger without strengthening the model scope.

**Still OPEN:** authenticate every historical native rule and prove a fixed-$r$ simulation of every legal source-authenticated mixed branching/shared proof of this strict family, with auxiliary definitions, algebraic shortcuts, reconvergence, and references charged; or exhibit a legal historical shortcut refuting that transfer. Independently prove noncircular **[P2-B2]**. No B1/B2/B3 or P-versus-NP resolution follows.

## Reproducibility

- Checker: `experiments/review/lspv5_447_peer518_pc_padding_audit.py`.
- Raw: `experiments/review/raw/2026-11-08_1654_LSPV5_447_PEER518_PC_PADDING_RAW.json`.
- Handoff: `research/coordination/2026-11-08_1654_LSPV5_PEER518_PC_PADDING_447_HANDOFF.md`.
- Primary source: https://arxiv.org/abs/2610.00837v2 and the archive/hash above.

Historical `R_mix341` grammar/weights, five roles/IDs/titles/schedules/enabled states, and two-Route-A/three-Route-B allocation are unchanged. P versus NP remains OPEN.
