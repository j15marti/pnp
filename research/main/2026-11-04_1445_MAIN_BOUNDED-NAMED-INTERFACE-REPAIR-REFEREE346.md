# REFEREE346 — bounded named-interface repair for shared proof DAGs

**PNP Independent Proof Red Team | November 4, 2026, 14:45 PST**  
**Status:** PROVED/EXACT tiny-output-support counterexample; PROVED/RESTRICTED compiler synthesis already subsumed by project LSPV-1/362, LSPV-3/386, and LSPV-4/396; COMPUTATIONAL finite controls; full `R_mix341`, B1, B2, B3, unrestricted SAT hardness, and P versus NP OPEN.

## IDEA before search

The missing obligation is a typed, polynomial-overhead backtranslation after authenticated evaluator source retraction. The initial proposal was:

> If every copied node that becomes type-illegal depends on at most `b` original variables, replace it by complete Resolution closure, paying at most `3^b` once per shared DAG node. For `b = O(log(N+r))`, the translation is polynomial.

Assumptions: one fixed explicit source formula, an already proved source-retraction prefix, source-authenticated acyclic proof DAGs, genuine strict Resolution, and no semantic SAT oracle. Falsifiable prediction: high fan-out does not multiply logical repair nodes, but parity, exact definitions, nonclausal factors, or unbounded interfaces defeat the claim.

Four registered falsifiers were:

1. the LSPV-3/402 AND3 step grows from one evaluator input to four original inputs;
2. a shared repaired node has many consumers and might require tree unfolding;
3. a repaired assertion is later consumed as an exact definition or GF(2) row;
4. an affine relation has exponentially many CNF blockers but one compact XOR row.

## Exact established lower-bound anchor

For the standard explicit unary pigeonhole CNF `PHP_{h+1}^h`, with `h(h+1)` Boolean variables, `h+1 + h*binom(h+1,2)` source clauses, and ordinary signed DIMACS length `N_h = Theta(h^3 log(h+2))`, Haken (1985) proves

`exists c>0 exists h0 forall h>=h0 forall ordinary shared-DAG Resolution refutations pi: |pi| >= 2^(c h)`.

The proof system has only authentic source clauses and binary Resolution; it has no extension variables, GF(2), AND3, `LOCAL-CONVERT`, circuit axioms, semantic oracle, or arbitrary machine step. Cook (1976) gives polynomial Extended Resolution proofs of the same pigeonhole family. Hence Haken's theorem is not a lower bound for ER, `R_mix341`, or arbitrary uniform SAT algorithms. This run does not regenerate a hard family or reconfirm the published proof.

Under the declared signed-DIMACS encoding, the Resolution lower bound can be restated only as `2^(Omega((N_h/log N_h)^(1/3)))`. This is still a proof-system-specific statement; changing the encoding does not promote it to machine hardness.

## SEARCH

### Project, Grok, and Claude

The governing handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` and issue #3 were read first. Material project results actually read were:

- `research/agents/lspv-3/2026-11-03_2324_LSPV-3_LOCAL_IMPLICATE_GUARD386.tex`, blob `6cfe61a3d3f3fe11a52b3edbe986de861d08c1e9`: already proves the general `3^k` bounded-interface Resolution saturation lemma and a 27-node compiler for three named wires. The saturation lemma is not new here.
- `research/agents/lspv-3/2026-11-04_1327_LSPV-3_ORIGINAL_SUPPORT_TRANSPORT_FIREWALL402.tex`, blob `4b301395cd6860b55a6fc879f4e38a1b29e8b182`: literal downstream AND3 replay can become type-illegal after source retraction; its displayed last step is nevertheless repaired by strict RES on `(p),(not p)`.
- `research/agents/lspv-1/2026-11-04_1400_LSPV-1_UNBOUNDED_ORIGINAL_SUPPORT_RETRACTION400.md`, blob `40ccc26eb671cb81eca4b89b1a4a12b074eff8ad`: transitive original support can grow to arbitrary `k`; this falsified the initial original-support formulation.
- `research/agents/lspv-2/2026-11-04_1424_LSPV-2_ADAPTIVE_GATE_COLLAPSE_TREE400.tex`, blob `188aa3bd5ae19ecd5afa58cf666e28bf59ebe09a`: adaptive gate collapse gives a separate polynomial translation for strict Resolution plus conservative AND2 when the collapse tree has few leaves; it excludes AND3, GF(2), and `LOCAL-CONVERT`.
- `research/agents/lspv-1/2026-11-03_0455_LSPV-1_LOG_SUPPORT_FACTOR_ER362.tex`, blob `e0e793fcdd43d828a5f956d2f62a09b0d587f6c4`: already proves an exact-factor shared-DAG compiler of cost `(3w-1)2^w` under bounded union named support and explicit records. The present logarithmic-interface sufficiency is therefore a duplicate at stronger exact semantics.
- `research/agents/lspv-4/2026-11-04_1436_LSPV-4_ASSERTION_RETYPE_REPAIR396.tex`, blob `890819f7c4de2e1d25594f7c08c465d8db5cf87b`: already composes LSPV-3/386 with REFEREE341 to obtain `3(L-1)+27q` for the three-wire assertion-only evaluator grammar. This current report does not reclaim that compiler.
- `research/agents/lspv-3/2026-11-04_1424_LSPV-3_SEMANTIC_PORT_VALIDATION_FIREWALL403.tex`, blob `6aa1602164372928b66a77d90fd6c4cd661a8ce7`: exact essential-support testing for arbitrary compact circuits is coNP-complete for each fixed threshold. A free semantic-support oracle cannot be assumed.
- `research/main/2026-11-04_1352_MAIN_CERTIFICATE-WORK-PEQUIVALENCE-FIREWALL-REFEREE345.md`: encoded certificate work is polynomially invariant under mutual exact-source p-simulation, unlike raw node count.

Current Grok was located from the repository rather than guessed: `GROKPROOF/2026-11-04_2215_PROGRESS.md`, blob `3521be6e0a50f47a2228e08d785af65916968543`. It proposes memoized shared subcomputations but proves no all-input compiler. Its strict claim that `Omega(N^1.1)` exceeds an `N^(1.1+o(1))` budget repeats the equality-boundary overstatement already corrected by LSPV-1/399.

The current applicable Claude folder contains no report later than October 28. The exact files read were `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`, and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`. They concern restricted alternation-trading portfolios and sequential-access crossing sequences, not source-rooted mixed-proof translation.

### Primary literature and web

Actual queries included:

- `Davis Putnam resolution closure existential projection at most 3^k clauses primary paper`
- `extended resolution bounded number extension variables simulation resolution 2^k primary source`
- `bounded treewidth CNF resolution proof polynomial size primary paper Atserias Dalmau`
- `Tseitin circuit encoding shared DAG extended resolution proof polynomial simulation primary source`
- `Martin Furer Efficient Arbitrary Resolution Proofs Unsatisfiability Restricted Tree Width PDF 2012`

Relevant sources were opened and read beyond result snippets where available:

- Davis and Putnam, *A Computing Procedure for Quantification Theory*, JACM 7 (1960), DOI `10.1145/321033.321034`: variable elimination by Resolution supplies the projection argument underlying the `3^b` closure lemma.
- Atserias and Dalmau, *A Combinatorial Characterization of Resolution Width*, full author PDF: width and space are proof-system-specific; the paper does not supply an ER-to-Resolution or arbitrary-algorithm compiler.
- Bryant and Heule, *Generating Extended Resolution Proofs with a BDD-Based SAT Solver*, TACAS 2021, full paper: BDD conjunction and existential quantification can generate checkable ER proofs, including polynomial proofs on pigeonhole benchmarks. This is positive evidence that shared circuit structure helps inside a declared proof system, and negative evidence for transferring ordinary Resolution hardness.
- Kiesl, Rebola-Pardo, Heule, and Biere, *Simulating Strong Practical Proof Systems with Extended Resolution*, JAR 2020, open article: ER polynomially simulates DRAT and DRAT polynomially simulates DPR. This is a system-specific p-simulation theorem, not a machine-to-`R_mix341` bridge.
- Fuerer, *Efficient Arbitrary and Resolution Proofs of Unsatisfiability for Restricted Tree-Width*, LATIN 2012, DOI `10.1007/978-3-642-29344-3_33`: the accessible full abstract states `poly(n) * exp(w)` Resolution bounds and that abbreviations for repeated subclauses can reduce proof length/running time from quadratic to linear in `n`. The closed proceedings text was not available through the search interface, so no stronger claim is attributed to it.

Direct Google-branded search was unavailable. General web search was used; this report does not claim that the Google UI was searched.

### OpenAI GitHub

Queries `resolution proof certificate DAG verifier` and `Tseitin encoding circuit gate SAT` in `github.com/openai` returned no applicable compiler. The files actually read were:

- `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean`, blob `1ced21f44ad49370d1b812e862c03c3a91d7f836`: proves instruction/visit/stack bounds for one concrete execution, not proof backtranslation.
- `openai/math/lean/OAI/Algorithms/SubexponentialSAT/RuntimeAssembly.lean`, blob `41df76f44884b50cca30460fa2d23bc3bf0848a0`: explicitly labels its `ImplementationCertificates` as open implementation obligations. It reinforces, but does not prove, the needed charged bridge.

## ITERATE: proved tiny-output-support firewall

### Theorem 346 (a unit output can retain Haken-hard premise complexity)

Let `P_h=PHP_{h+1}^h` be Haken's explicit unary pigeonhole CNF and let `z` be fresh. Define

`Gamma_h = { (z or D) : D in P_h }`.

Then `Gamma_h` is satisfiable and entails the one-variable unit `(z)`. Nevertheless every ordinary shared-DAG Resolution derivation of `(z)` from `Gamma_h` has `2^(Omega(h))` inferred lines.

#### Proof

Setting `z=1` satisfies every clause, so `Gamma_h` is SAT. Setting `z=0` leaves exactly `P_h`, which is UNSAT, hence `Gamma_h |= z`.

Every source clause contains positive `z`. Resolution never introduces a new literal, and no clause contains `not z`; therefore every clause in a derivation of `(z)` still contains `z`, and no inference pivots on `z`. Delete `z` from every source and derived clause. Each source becomes its corresponding pigeonhole clause `D`; each inference remains the same ordinary Resolution pivot; the final `(z)` becomes the empty clause. Thus a length-`s` derivation of `(z)` would give a length-at-most-`s` refutation of `P_h`. Haken's theorem forces `s>=2^(c h)` for all sufficiently large `h`. QED.

This counterexample has conclusion support one, allows arbitrary shared-DAG reuse, and uses no generated hard family. It proves that small **output** support, small output circuit, or a shared final node does not imply a polynomial translation. The complete authenticated parent interface is the necessary parameter. It remains an ordinary-Resolution statement and supplies no mixed-system or machine lower bound.

## Restricted repair synthesis (already present in project form)

Search falsified **transitive original support** as the right parameter. In the LSPV-1/400 family, the paid gate `p` depends essentially on all `k` original inputs, yet the bad endpoint has the one-wire atomic interface `(p),(not p)` and closes in one strict Resolution inference. The revised parameter is the number of **named atomic wires in a clause interface**, not the number of original inputs hidden behind their definitions.

### Shared bounded named-interface repair

Fix an authenticated source-retraction prefix of cost `q` from evaluator sources to the original CNF `F`. Let `pi` be a source-rooted acyclic downstream proof DAG with `r` paid nodes. Suppose a topological translator maintains, for every assertion node, a conjunction of already derived clauses that implies that assertion. Every downstream node is one of:

1. a rule whose exact retyped instance remains legal and can be copied once;
2. strict RES, translated by resolving strengthened parents when the pivot survives, or by inheriting a parent subclause when it does not; or
3. an assertion-consequence node `v` whose translated parent clauses all use a declared common set `U_v` of at most `b_v` named atomic wires, whose conclusion is semantically implied by those parent clauses, and whose consumers require implication only—not exact equality, a GF(2) row, or a conservative definition.

Then there is a source-rooted shared Resolution/mixed DAG with

`cost <= q + r_copy + sum_{v bad} 3^(b_v) <= q + r * 3^b`,

where `b=max_v b_v`. Each translated node representation is constructed once and reused by all consumers. In particular, if `q` is polynomial and `b <= c log_3(N+r+q+2)` for a fixed constant `c`, the node overhead is polynomial. This is a restricted synthesis of LSPV-3/386 with source retraction; LSPV-4/396 already proves the three-wire evaluator instance, while LSPV-1/362 proves a stronger exact-factor variant with paid weakening. No academic or project novelty is claimed for this compiler.

#### Proof

Traverse `pi` topologically. Preserve the authenticated source-retraction prefix and copy exact legal nodes. For a bad assertion node `v`, let `Delta_v` be the conjunction of its already derived parent-clause representations over `U_v`. Saturate `Delta_v` under genuine nontautological binary Resolution. There are exactly `3^(b_v)` proper clauses over `U_v` including the empty clause, so at most that many distinct charged clauses are added.

For each complete assignment to `U_v` that falsifies the output assertion, form its blocking clause `B`. Soundness gives `Delta_v |= B`. Davis-Putnam elimination, equivalently the complete saturation lemma already proved in LSPV-3/386, yields a derived clause `D subseteq B`. The conjunction of all such `D` is source-derived and implies the output assertion. Cache this conjunction as `v`'s translated representation. It may be stronger than the output, which is safe only because all declared consumers use assertion consequence rather than exact identity. At a false root, the representation contains the empty clause.

The cached representation is referenced by every outgoing edge; fan-out does not reproduce its inference nodes. This proves the logical-DAG bound. It does not prove a corresponding runtime bound without a schedule. QED.

### Immediate repair of the current counterexample

LSPV-3/402 and the all-`k` LSPV-1/400 family have retyped original support `k` but a one-name atomic endpoint. The theorem's local repair has `b_v=1` and one RES node. Thus those families falsify literal AND3 copying but do **not** falsify bounded named-interface repair.

### Where the theorem fails

- **Exact identity:** if a consumer needs a wire definition rather than an assertion, a stronger consequence is insufficient. For example, `x` implies `x or y` but is not equal to it.
- **GF(2) or nonclausal factors:** a clause representation cannot silently replace an affine row or exact factor. A separately proved coercion is required.
- **Unbounded named interface:** `3^b` is exponential. There is no polynomial theorem when `b` grows linearly.
- **Compact parity:** an even/odd parity relation on `b` bits has `2^(b-1)` dense CNF blockers but one `O(b)`-bit XOR row. The closure compiler is not representation-independent.
- **Source authentication:** a short auxiliary contradiction not derived from `F` remains invalid.

Hence shared subcomputations are helpful but not sufficient. Polynomial overhead needs a structural restriction such as logarithmic named interface, a small adaptive collapse tree, bounded treewidth with an explicit decomposition, or a declared p-simulation such as BDD-to-ER. None is known to cover every `R_mix341` proof or every uniform SAT decider.

## Fully charged resource ledger

Let `V` be the number of named wires. A direct materialized compiler can enumerate a closure using a naive all-pairs fixed point in

`O(r * 9^b * b * log V + input/source parsing)` bit-level comparison work,

and writes at most `O((q+r*3^b) * b * (log V + log(q+r*3^b)))` proof bits, aside from already supplied payloads. These deliberately loose bounds are polynomial for logarithmic `b`. Whole-certificate verification, parent-ID access, pivot checks, source provenance, output, and malformed rejection are charged.

Materializing the whole translated DAG uses space bounded by its output size. A streaming schedule can keep one local closure in `O(3^b b log V)` bits plus live cached representations, but the latter depends on the proof DAG's frontier. High fan-out does not multiply logical nodes, yet long-lived shared nodes require storage, retrieval, recomputation, or repeated source reads. No sublinear-space exponent is claimed. The corrected all-phase envelope `s' <= max{rho,eta,lambda,lambda*s}` remains binding.

## Verification

`experiments/arc/lspv5_346/bounded_interface_repair_referee346.py` and the independent no-import JavaScript checker cover:

- 560 deterministic SAT/UNSAT CNF interfaces for `b=1..6`;
- 19,434 exactly checked entailed clauses;
- 20,275 producer assertions;
- 127 independent verifier checks;
- guarded pigeonhole controls for `h=1,2,3`: `Gamma_h` SAT, zero models with `z=0`, and a `z=0` witness after every single guarded source deletion;
- transitive original support `k=4..128` with one atomic interface and one repair node;
- shared fan-out through 1,024 consumers, comparing one DAG repair with tree duplication;
- compact parity through `b=16`;
- seven malformed interfaces, all rejected.

Raw SHA-256: `dca75afe155e31f8316d45e33390b74ff263b8b39bd89e2b666e172b2e6d30eb`.

Finite tests validate the implementation and hostile controls, not the asymptotic theorem or a global minimum.

## Exact proof status and bridges

- **PROVED/EXACT:** the guarded-PHP tiny-output-support firewall above, as a direct corollary of Haken's theorem.
- **PROVED/RESTRICTED BUT DUPLICATE/SYNTHESIS:** the shared bounded named-interface assertion compiler above; LSPV-1/362, LSPV-3/386, and LSPV-4/396 have the substantive positive components.
- **ALREADY KNOWN IN PROJECT:** the local `3^b` saturation lemma (LSPV-3/386).
- **COMPUTATIONAL:** finite SAT/UNSAT, malformed, fan-out, and parity controls.
- **FALSIFIED:** transitive original support as the necessary repair parameter; sharing alone as a sufficient representation-independent condition.
- **OPEN:** an authoritative `LOCAL-CONVERT`/factor grammar showing that every retracted node fits the theorem or another polynomial compiler.
- **OPEN:** B1, B2, B3, a superpolynomial `Wbar_Rmix341`, unrestricted SAT hardness, and P versus NP.

The theorem addresses a restricted proof-to-proof transfer only. It does not turn Haken's ordinary-Resolution lower bound into mixed-system hardness. BDD/ER and GF(2) shortcuts remain mandatory countercontrols.

## Next unresolved step

Freeze the exact exported-wire semantics of every native `AND3` and `LOCAL-CONVERT` output. Then classify each consumer edge as assertion-only or exact. Either:

1. prove a polynomial bound on the maximum named interface or an adaptive decomposition for every node produced by the transparent evaluator compiler; or
2. exhibit one authenticated proof family in which a bad node has superlogarithmic named interface and feeds an exact/GF(2) consumer, defeating this repair.

That is the first remaining rule-level obstacle. It is still far short of B3.

No root `main.tex` integration was attempted: this run publishes through the role-owned dated report, five-role handoff, raw data, verifier, and issue #3, avoiding an unsynchronized edit to the shared root.
