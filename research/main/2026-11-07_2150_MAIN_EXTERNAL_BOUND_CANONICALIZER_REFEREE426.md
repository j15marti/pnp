# LSPV-5/426 independent referee: external-source binding survives recovered-packet canonicalization

**Pacific timestamp:** 2026-11-07 21:50 PST  
**Role:** LSPV-5 independent red team, Route B primary  
**Tracker nodes:** `[P2-D1]`, `[P2-B2]`, `[P2-L3-490]`, `[P2-L5-411]`, `[P2-L5-413]`, `[P2-L5-419]`, `[P2-L5-425]`, new `[P2-L5-426]`  
**Status:** **PROVED-RESTRICTED** two-input source-binding/canonicalization composition theorem; **COMPUTATIONAL** exact recovered-checker replay in two independently implemented languages; full historical $R_{\mathrm{mix341}}$, B1, B2, B3 and P versus NP remain **OPEN**.

## IDEA: preregistered hypothesis and falsifiers

Initial hypothesis: `[P2-L5-425]`'s compact canonicalizer could be extended to a precisely authenticated SOURCE/RES packet fragment if native Resolution acceptance depended only on normalized clauses, an oriented pivot and canonical parent references.

Falsifiers stated before search:

1. Resolution acceptance depends on raw ID spellings, unchecked provenance or unbounded ignored payloads;
2. repeated literals, tautologies, pivot orientation or duplicate clauses make canonicalization change acceptance;
3. the recovered historical grammar does not specify a native RES byte rule at this scope; or
4. a current tracker/report already proves the exact SOURCE/RES canonicalization theorem.

Search triggered falsifier 3. `[P2-L5-413]` proves by exact recovered-code replay that its complete inference dispatch accepts only AND3 and XOR and rejects RES, LOCAL-CONVERT and DEF as unknown. `[P2-L5-411]` proves a no-weakening ordinary-Resolution literal-substitution compiler, but that is a theorem in a distinct ordinary-Resolution calculus, not an accepted mixed packet grammar. I therefore did not invent a RES record or choose an unauthorized TAGGED/EXTENSIONAL completion.

The revised target was the immediately actionable gap in `[P2-L3-490]`: prove and replay that exact external-source multiset binding is invariant under `[P2-L5-425]`'s canonicalization, including alias/metadata packets and same-length satisfiable source substitutions.

## Claim card

**Claim ID:** LSPV-5/426.  
**Quantifiers:** for every parsed packet $P$ accepted by the fixed recovered SOURCE/AND3/XOR checker and every external CNF $F$ accepted by the exact LSPV-3/490-style multiset/variable-bound binder, the canonical packet $C(P)$ is checker-accepted and the binder accepts $(F,C(P))$.  
**Model:** post-`JSON.parse` packet objects; separately parsed textual DIMACS external source; exact clause multisets with duplicate multiplicity; deterministic host implementations.  
**Resource:** explicit pair length, checker/binder work and source reads; no machine-runtime lower bound.  
**SAME_REALIZATION:** the same external source $F$, the same parsed packet semantics, and the exact canonicalizer $C$; no source replacement or equisatisfiable reduction.  
**Weakest material conclusion:** source binding adds $|F|$ bits to the recovered compact witness rather than invalidating the canonical representative.  
**Easy/hostile controls:** source permutation, literal permutation, duplicate-clause multiplicity, malformed header/count/termination, all 324 indispensable-clause equal-length SAT replacements, affine ghost bits, ignored metadata and ID aliases.

## SEARCH: current state, primary literature and repositories

### Project continuity

Both complete trackers were read before work. Search-time `proof1.txt` was blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 bytes), unchanged; `proof2.txt` was blob `b5408617bea82f550ab2a0ab09b0f78f14ba8366` (327,050 bytes). Search-time `main` was `3614fb7c6b1d4b103eca4f19717db810e727b99c`. Exact final prewrite/postwrite blobs are recorded in the publication receipt.

Read the governing handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`; `AGENTS.md`; `CODEX.md`; `.codex/skills/pnp-research/SKILL.md`; its complete `references/modes.md` and `references/research-protocol.md`; current Grok `GROKPROOF/2026-11-08_0320_PROGRESS.md`; Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`; LSPV-1/495; LSPV-3/490; LSPV-4/486; and LSPV-5/411,/412,/413,/425 with cited code/data.

The current issue #3 body was read and reports 1,288 comments. Two direct full-comment retrieval attempts failed with `Transport closed`; current affected peer nodes were instead read from the complete tracker and exact role reports. This access limitation is recorded rather than disguised as comment review.

Root `main.tex` again returned an empty content field while identifying nonempty blob `68188a24badda635a5983fda1c381cdb694fd497`. The local partial workspace lacked the repository skill script and root manuscript, so the mandatory preflight could not execute locally. The script itself, blob `81da28522b2cc5cd0738a94a2c0966b76c761a04`, was read. No partial `main.tex` rewrite was attempted.

### Exact artifacts under test

- Recovered checker: local preserved `replay/413/lspv2_341_independent_verify.js`, SHA-256 `0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae`; historical repository blob is `[P2-L5-413]`'s `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`.
- Packet: `replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json`, SHA-256 `12d723c92c683ec1a59e17d95d0d47156babe7febe27b7432dc01279abcb8d95`; historical repository blob `fe27fe1011d0021e721ccaeb747ed58da65d7464`.
- LSPV-3/490 report blob `bf93862e04cffb379e6411bf0ca511a098511da7`, exact adapter blob `b113119b7b87dac7510603804d91918e80f301b0`, raw blob `72da0d58124e0ece67448d854756160721eaa5fb`.
- LSPV-5/425 canonicalizer blob `cbb330c40e927c2b516866d39baa77c700db14d5` and canonical SHA-256 `1637821fc706fd80abcaf70cbd458d1ad648bcf1576e1eed564b519bb62aba25`.

### Primary literature

Targeted searches were `Cook Reckhow 1979 relative efficiency propositional proof systems PDF`, `Urquhart 1987 hard examples resolution Tseitin expander`, `Pang degree-size Res(PC) 2610.00837`, and `FRAT original formula source authentication certificate checker`. Primary/authoritative results inspected:

- Cook--Reckhow (1979) defines polynomially checkable propositional proof systems and relates existence of **some** polynomially bounded system to NP=coNP. It does not prove that this fixed recovered or historical calculus has polynomial witnesses.
- Urquhart (1987) gives exponential ordinary-Resolution lower bounds for suitable expander/Tseitin contradictions. This is a restricted proof-system theorem.
- Pang, arXiv:2610.00837, gives a degree--size relation and exponential results in fixed $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_p)$ settings. It does not cover every historical mixed rule.
- FRAT and verified DRAT/LPR work use an explicitly supplied original formula plus a proof/checker interface. That architecture motivates a separate two-input binder but does not authenticate this project's historical grammar.

A separate Google-branded interface was unavailable; indexed research search and direct primary/repository files were used.

### Required repository deltas

- `konard/p-vs-np` unchanged at `ecedd2b45f1c524d85c00b2da27a9c140025550c`; `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2` enumerates allowed axioms and scoped formal results, not an $R_{\mathrm{mix341}}$ source binder.
- `blkph0x/p-vs-np-proof-research` unchanged at `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` explicitly scopes its implemented directions and supplies no same-$R$ compiler.
- `meelgroup/frat-xor` at `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` specifies explicit CNF/XOR input and proof syntax.
- `tanyongkiam/cake_lpr` uses branch `master`, head `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`; `README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c` documents the final release and checker trust boundary. A first `main`-branch fetch returned 404 and was corrected, not counted as review.
- `marijnheule/drat-trim` at `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; `README.md` blob `eb6ffcc4a85ff1c74a5995b6caae4372381dcd47` explicitly treats DIMACS formulas as clause multisets and DRAT proofs as ordered steps.
- `openai/math` at `4eaee87548250b2682affda7d05d947c05554bae`; its README warns that not all results are formalized and supplies no relevant same-system theorem.
- `anthropics/formal-math` at `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`; `eth/Challenge.lean` blob `6297ab1398884550253bdd1475704729d02ce89b` contains explicit `sorry` placeholders and cannot be used as an ETH refutation or B3 bridge.

Repository text and badges were treated as evidence, never authority for P versus NP.

## Established-family ledger

| Field | Exact record |
|---|---|
| Family | Connected simple bridgeless cubic odd-charge Tseitin; suitable expander subsequence for the published Resolution lower bound. Pang $F(n,3,8n)$ remains a separate strict-random-3-CNF restricted-system control. |
| Exact 3-CNF | One edge variable per graph edge. At each cubic vertex, include the four signed proper width-three clauses excluding the four local assignments of parity opposite to its charge. Thus $3h/2$ variables and $4h$ clauses. |
| Size parameter | $h$ vertices; indexed encoding $N=\Theta(h\log h)$. Recovered fixtures use $V=h$, $E=3h/2$ (except the bridge control), $4h$ clauses and $W=4h-1$ proof records. |
| Theorem/source | Urquhart: exponential ordinary shared-DAG Resolution lower bounds for suitable expander Tseitin formulas. Pang: exponential size in the stated fixed $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_p)$ model under its hypotheses. |
| Proof model | Model-specific syntactic proof DAGs, not arbitrary algorithms. The recovered packet is a distinct SOURCE/AND3/XOR certificate sublanguage. |
| Known methods | The recovered declared semantics uses three AND3 nodes per vertex and $h-1$ GF(2) XOR nodes. Gaussian elimination, branching, learned clauses, extensions and shared DAGs remain legal controls wherever native or simulated. |
| Remaining transfer | Authenticate the exact full historical byte grammar and prove an all-native-rule lower bound or polynomial retraction. External source binding and compactness in this strict sublanguage do not accomplish that transfer. |

The finite packet certifies its own specialized UNSAT sources under the recovered checker. Urquhart/Pang certify proof-size hardness only in their stated systems. No empirical solver-difficulty claim is made.

## ITERATE: exact composition theorem

Let $V(P)$ mean acceptance by the recovered SOURCE/AND3/XOR checker. Let $M(F)$ be the multiset of signed literal lists in independently parsed external CNF $F$, preserving duplicate clause multiplicity. Let $C_P$ be the packet's internal source-clause multiset and $n_P$ its declared external variable bound. Define the distinct adapter

$$
B(F,P)=V(P)\land[M(F)=M(C_P)]\land[n(F)=n_P].
$$

Let $C$ be the canonicalizer of `[P2-L5-425]`.

### Theorem 426.1 (binding-invariant canonicalization)

For every parsed packet $P$ and external source $F$ in this recovered schema,

$$
B(F,P)\Longrightarrow B(F,C(P)).
$$

Moreover, the pair $(F,C(P))$ has explicit length

$$
|F|+O\!\left(\sum_i V_i(E_i+W_i+1)\right).
$$

For the accepted recovered cubic fixtures $E=O(V)$ and $W=4V-1$, this is $|F|+O(\sum_i V_i^2)$.

**Proof.** Theorem 425.1 already proves $V(P)\Rightarrow V(C(P))$. Inspection of the construction shows that $C$ preserves, entry by entry, each packet fixture's graph edge list and every source clause's vertex and signed literal list. It changes only record IDs/references, projects checker-unobserved affine bits, removes ignored fields and normalizes the graph display name. Hence $M(C_P)=M(C_{C(P)})$ and $n_P=n_{C(P)}$. The two exact binding predicates are therefore unchanged. The size bound is Theorem 425.1 plus the separately supplied source bits $|F|$. No hash collision, semantic oracle, equisatisfiable replacement or new inference rule occurs. ∎

### Corollary 426.2 (hostile external sources remain rejected)

If $F'$ has the same byte length and header as $F$ but changes an indispensable clause to a valid tautological clause, and the resulting source is SAT under its deletion witness, then $M(F')\ne M(C_P)$ and $B(F',C(P))$ rejects. This is a binding statement, not a proof that arbitrary source mutations are easy to classify.

### Branching/shared-DAG semantics

Canonicalization preserves the exact existing parent-reference DAG and does not duplicate shared nodes. This schema has no branch contexts or native split/discharge rule, so the theorem neither adds such a rule nor licenses branch-local reuse. If a future full grammar includes contexts $\Gamma\vdash C$, their assumptions must be included in the canonical identity; the present proof cannot be silently extrapolated.

## Executed verification and hostile controls

The new Node implementation independently reconstructed both the canonicalizer and the LSPV-3/490-style binder, then executed the exact preserved checker:

- 1,408 checks and 352 expected rejections;
- seven fixtures and 63 accepted external bindings;
- all 324 independently witnessed, equal-length satisfiable one-clause substitutions rejected after canonicalization;
- duplicate-clause multiplicity substitutions rejected;
- clause-order and literal-order permutations accepted because binding is semantic multiset equality;
- bad variable bounds, headers and terminations rejected;
- baseline, ignored metadata, paired affine ghost bits, numeric ID alias, lexical ID alias and duplicate-member last-wins packets all collapsed to the exact 71,853-byte canonical SHA and remained externally bound.

The independent Python implementation used separate parsing, canonicalization and multiset code:

- 1,335 checks and 345 expected rejections;
- 14 accepted original/permuted-source bindings;
- the same 324 equal-length SAT mutants rejected;
- exact agreement on 71,853 bytes and SHA-256 `1637821fc706fd80abcaf70cbd458d1ad648bcf1576e1eed564b519bb62aba25`.

The 324 mutants are finite **COMPUTATIONAL** controls. The universal implication is the symbolic preservation proof above.

## Independent challenge and barriers

This composition repairs one precise objection to `[P2-L5-425]`: the compact representative can remain bound to a separately supplied original CNF without trusting a digest. It does **not** make the recovered checker a full Cook--Reckhow system for arbitrary CNFs, because it remains specialized and incomplete. It also does not authenticate raw JSON spellings: duplicate members still acquire last-wins semantics before canonicalization.

Relativization or an algebraic oracle cannot manufacture the missing historical RES/LOCAL-CONVERT/DEF byte productions. Conversely, this source-binding theorem imposes no lower bound on arbitrary SAT algorithms. Cook ER and GF(2) shortcuts remain explicit upper-bound controls. Compactness of an existing witness does not construct that witness and does not establish B3.

Cross-domain classification: verified-certificate pipelines with separately parsed original formulas are a **THEOREM-ARCHITECTURE ANALOGY** only. The exact project theorem comes from the explicitly defined $B$ and $C$, not from importing DRAT/FRAT correctness.

## Resource ledger

- **Logical nodes/weights:** unchanged; canonicalization preserves the recovered DAG and binder adds no inference node. Historical rule weights are untouched.
- **Evidence bits:** published packet 197,514 bytes; canonical packet 71,853 bytes; seven serialized external sources total 10,907 bytes; new programs/raw output are separately charged artifacts.
- **Parsing/source reads:** each composite check parses the external source, reads its clause tokens, constructs exact signed-literal multiset keys, parses/canonicalizes the packet and invokes the recovered checker. The `[P2-L3-490]` region-probe lower bound remains a source-binding task bound, not ideal $W_R$ or SAT-decision work.
- **Construction/search:** repository reads, literature search, failed RES target, alias generation, 324 mutations, hashing, serialization, checker invocations and output are charged host work. Discovery remains intentionally outside the ideal proof minimum.
- **Work/span/space:** no weighted critical-path, parallel schedule or retention/recomputation optimum is inferred. Implementations use ordinary host memory and are not the FLMV machine; no $s'$, native-time exponent or peak-space theorem is claimed.

## Tracker decision and precise remaining gap

Material evidence refines `[P2-L3-490]` and `[P2-L5-425]` and narrows `[P2-D1]`'s recovered-sublanguage interface; add `[P2-L5-426]`. It does not change `[P2-B1]`, `[P2-B2]`, `[P2-C3]` or proof1. Full historical grammar, completeness for arbitrary CNFs and noncircular same-calculus B3 remain **OPEN**.

**Actual advance:** exact external source identity and polynomial canonical packet size now coexist for the recovered SOURCE/AND3/XOR sublanguage.  
**Verification:** 1,408 Node plus 1,335 independent Python checks; 697 expected rejections; 324 equal-length SAT substitutions independently rejected in both implementations.  
**Publication status:** report, two programs, raw result and handoff prepared for a conflict-safe current-head commit and complete readback.  
**Precise remaining gap:** obtain an authoritative full historical parser/format for RES, LOCAL-CONVERT, DEF and branching/context rules; then prove source-bound canonicalization and compactness for every legal proof of every CNF, followed separately by an all-rule lower bound and noncircular B3.  
**P versus NP remains OPEN.**
