# LSPV-4 LOCAL-CONVERT CVP / gate-annotation resource audit 363

**PNP Time-Space Resource Auditor**, task \`6ad42a1f03448191b8ded0c1f2dfa791\`. November 3, 2026, 07:36 PST (America/Los_Angeles). **P versus NP OPEN.** No task, title, enabled state, schedule, ownership, or preselected calculus changed.

## Scope and obstruction

Follow the verified November 2 12:04 five-role handoff, coordination issue #3, \`AGENTS.md\`, \`CODEX.md\`, project \`pnp-research\` skill, LSPV-2 Rmix341 definition, and LSPV-4 354/361/362 evidence-cost work. General encoded CNF-SAT is the target. Exact source and certificate syntax, rather than just the number of named original Boolean variables in an output factor, determine verifier resources.

The fixed **Rmix341** grammar includes unit-weight, source-labelled binary RES; binary AND3 on conditions of at most three original variables; binary XOR; unary LOCAL-CONVERT, which permits a clause or a *bounded-support Boolean circuit condition* on implication-checked local semantics; and charged conservative two-input DEF. Original clauses are free axioms. There is **no** new rule, free oracle, or exemption from charging DEF. We analyze the consequential syntax choice explicitly:

> **Circuit-valued-output interpretation U:** A LOCAL-CONVERT record may contain an explicitly serialized, arbitrary-length, acyclic fan-in-two Boolean gate DAG but only at most three original-variable inputs. Such *internal representation gates* occur in the output syntax; whether they must instead count as separate charged DEF nodes has not been completely resolved in the unchanged Rmix341 specification. Results mentioning a **unit-cost single node** below are conditional on U, not a silent extension of R.

If the intended grammar instead bounds the gate DAG to O(1) or charges every internal gate as a separate DEF node, the specific node-cost gap changes. A shorter normalized presentation with the same downstream functionality may also exist. **This audit makes no claim that every optimal R proof contains a long gate DAG.**

## Result A. LOCAL-CONVERT checking is P-complete under U (KNOWN THEOREM + exact reduction)

Fix the *satisfiable* source

$$
F_+=(x)\wedge(x\vee y).
$$

Use one legitimate paid AND3 node on the two original clauses. The resulting local factor is

$$
S(x,y)=x\wedge(x\vee y)=x.
$$

Let \`G\` be any topologically ordered Boolean circuit with its input bits fixed as constants, and let \`t_G\` be its designated output. As the candidate output of one LOCAL-CONVERT record, provide a serialized circuit

$$
C_G(x,y)=x\wedge t_G.
$$

It has original-variable support contained in \`{x}\`, regardless of how many internal circuit gates compute \`t_G\`. The exact rule legality condition is

$$
S\models C_G\quad\Longleftrightarrow\quad t_G=1.
$$

The forward direction uses assignment x=1; the reverse direction is immediate. A logspace transducer embeds the original CVP circuit with fixed inputs into the output gate-DAG and appends two gates. Membership in P follows from forward gate evaluation on at most eight input rows. Hence the unannotated LOCAL-CONVERT legality problem **under U is P-complete under logspace reductions** by Ladner's CVP theorem. This is not a proof that the problem is outside L; \`L=P\` remains open. It is also not a lower bound for SAT decision, refutation discovery, or \`W_R\`.

For a *UNSAT* source control, add \`(\neg x)\` to \`F_+\`; the original two source references and AND3 factor remain unchanged. The local output legality still depends on \`t_G\`, even though this larger CNF is contradictory. A different, independently checked RES node between \`(x)\` and \`(\neg x)\` certifies UNSAT in one derived node. **Do not** conjoin the contradictory source before testing local implication, because a false antecedent entails every target and would invalidate the reduction.

### Explicit all-ones query lower bound

Take \`G_b\` computing \`t_G=\bigwedge_{i=1}^k b_i\` using k separately encoded Boolean constants and k-1 AND gates. On b=1^k the local conversion is legal, but flipping any one independent constant bit makes it illegal. Therefore any deterministic exact checker using the ordinary single-bit read-only input-probe model must read all k constants on that valid certificate. This yields **Omega(k) source/certificate access**, despite only two charged proof nodes in the displayed derivation *under U*. It is a representation/verification lower bound, **not** an arbitrary-SAT-decider time lower bound. Input length includes all k explicitly represented gates.

## Result B. Truth-table gate annotations give deterministic logspace checking (PROVED/EXACT, same U subclass)

For each serialized gate g of a LOCAL-CONVERT circuit over original support size s <= 3, append an authenticated s-variable truth vector v_g in {0,1}^{2^s}, at most eight bits. The read-only verifier checks:

1. Grammar, source labels and all earlier gate references; reject malformed, out-of-support inputs and cycles.
2. Every gate's eight (or fewer) entries by a constant-time Boolean operation on its *referenced annotated parent entries*; obtain parent entries via **paid** indexed read-only rescans.
3. The already authenticated parent local factor P and the output annotation satisfy P(a) => C(a) for all at most eight assignments a.
4. All indices, input-head movements, proof-source queries and certificate framing are counted. Any source preprocessing and construction also contributes to full peak space.

For full annotated evidence size M, counters for gate index, input-row index, parent record offset, source record offset, and finite-control state require **O(log(M+2)) writable bits**. A straightforward repeated-rescan implementation uses at most **O((M+2)^3) bit steps** (a deliberately loose bound). The added annotation is at most 8g bits for g gates, plus conventional record framing, and can be generated in O(g) gate-evaluation work for this fixed support when all gate truth vectors are retained (O(g) working bytes); annotation discovery/generation is not free.

This proves a **supplied-certificate** logspace verifier for this typed local subrule with additional evidence, not a logspace verifier of the unannotated CVP-hard subrule or the whole mixed calculus. An arbitrary SAT decider's reject trace is not thereby a proof. In the ALL-PHASE inequality \`s'<=max{rho,eta,lambda,lambda*s}\`, a host producer materializing all g vectors has local-phase rho as high as one in a suitable g-scaled input measure. The proof checker in the *annotated read-only* model instead retains logarithmic writable space and uses rescans.

## Four falsifiers

**F1 (FALSIFIED under U):** "Three original variables guarantee constant LOCAL-CONVERT checking work." The k-constant AND chain requires k authenticated constant-bit reads.

**F2 (CONDITIONAL BARRIER):** "A deterministic O(log M)-space, polynomial-time verifier for arbitrary *unannotated* circuit-valued LOCAL-CONVERT is immediate from an eight-row truth table." It would imply L=P, since the rule-checking language is P-complete. This is a conditional implication, not an unconditional space lower bound.

**F3 (FALSIFIED):** "Supplied gate coefficient/truth annotations can be accepted without verifying their internal gate transitions." Corrupting even one annotation could authenticate a false target. A sound checker rejects every forged intermediate/output vector in the tested grammar.

**F4 (FALSIFIED as an unnormalized proof-presentation claim):** "Inference-node count q alone polynomially bounds the raw bytes of every legal certificate." Under U the candidate may contain g gates within one LOCAL-CONVERT output for arbitrary g while q=2. This does **not** rule out the existence of a shorter equivalent proof or a canonical bounded-output syntax; the previous LSPV-4 evidence normalization remains conditional precisely at such circuit-valued exits.

## Falsification experiment

A Python producer (\`202611030736\`, deterministic) and independent no-producer-import Node.js referee check the fixed signed CNF source, two clause parents, factor mask, topologically ordered gates, eight-bit gate vectors, and exact implication. Python tested **792** distinct SAT/UNSAT-labelled local-conversion records (396 each), with **396 original SAT witnesses** and **396 exhaustive UNSAT controls**; additionally 201 forged final annotation and 201 forward-reference controls rejected. Chain lengths 1,2,3,5,8,16,32,64,128: all legal all-one chains and **259** individually flipped illegal neighbors checked. Python accepted 2 valid raw DIMACS strings and rejected 10 malformed DIMACS encodings and 11 malformed proof records; three explicit opposite-label controls passed.

The independently written JavaScript referee also generated its own circuits, checked source labels and gate transitions, and passed **5,858** assertions, including 1,100 separate opposite-source-label circuit cases, corruptions and chain sign flips. The Python process took about **0.13 seconds**, with host peak RSS **96,520 KiB**; Node host RSS was approximately **33,252 KiB**. Host measurements are neither indexed-TM step counts nor FLMV peak writable-space bounds. The full raw JSON and both programs are supplied in the reproducibility package. The public compact reproducer tests the same core claim.

The k=128 all-one chain uses 255 original constant/AND gates plus two embedding gates. The LOCAL-CONVERT record has only **one charged node under U**, yet contains 257 gate records and 2,056 explicit annotation bits. Its 128 independent sign/constant flips change the legal certificate into an illegal one.

## Corpus and literature reconciliation

Prior project: LSPV-2 \`2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex\` fixes Rmix341's five rules; LSPV-4 \`2026-11-02_2340_LSPV-4_CANONICAL_EVIDENCE_REPLAY354.md\` explicitly leaves LOCAL-CONVERT circuit normalization open; LSPV-4 \`2026-11-03_0603_LSPV-4_GF2_MATRIX_POWER_REPLAY361.tex\` and \`2026-11-03_0640_LSPV-4_AUGMENTED_AFFINE_LOGSPACE362.tex\` establish only supplied ROW/XOR verification; LSPV-5 REFEREE314 source-aware compiler and LSPV-1 BUDGETED-PROOF-SEARCH364 leave B3 open. The recent peer reports' local exits do not establish a universal raw-circuit syntax normalization.

Literature searches: \`Ladner 1975 circuit value problem logspace complete P\`, \`bounded support Boolean circuit value P-complete\`, \`DRAT LRAT certified verification\`; project GitHub queries \`reflection proof 2026-11-03\` and \`LOCAL-CONVERT Rmix341\`; github.com/openai search via GitHub connector for \`SAT verification\` in \`openai/tiktoken\` returned no relevant result (an uninformative narrow scope, **not** a novelty claim). Original sources: Richard E. Ladner, *The Circuit Value Problem Is Log Space Complete for P*, SIGACT News 7(1):18–20 (1975), DOI:10.1145/990518.990519; Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1):36–50 (1979), DOI:10.2307/2273702. Existing production SAT proof tools such as \`marijnheule/drat-trim\` and \`leanprover/leansat\` treat supplied proof evidence separately from deciding SAT.

## Bridge status and next exact obligation

**PROVED/EXACT:** Reduction and gate-annotation verifier under U and its fixed local source; k-bit sensitivity. **KNOWN THEOREM:** CVP is P-complete under logspace reductions. **COMPUTATIONAL:** Finite control counts. **CONDITIONAL:** The applicability of U to all intended circuit-valued Rmix341 presentations; normalization without losing permissible downstream uses. **OPEN:** B1, B2, B3; a superpolynomial \`Wbar_Rmix341(N)\`; a same-machine FLMV contraction; P versus NP.

The next smallest useful target is to settle **the exact intended LOCAL-CONVERT output grammar and downstream DEF/source-dependency semantics**, then either formally enforce gate-by-gate charged definitions or supply polynomially bounded, downstream-preserving canonical output normalization and a full mixed-rule logspace verifier with paid indexed input queries. The proof cost definition continues to grant the optimal derivation freely without charging optimizer discovery. No result here changes the \`Rmix341\` system or proves the weakest sufficient B3 bridge.
