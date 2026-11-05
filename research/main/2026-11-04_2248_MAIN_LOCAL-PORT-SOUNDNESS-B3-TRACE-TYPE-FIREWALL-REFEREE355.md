# REFEREE355: LOCAL port soundness, paid assertion export, and the B3 trace-type firewall

**November 4, 2026, 22:48 PST. LSPV-5 Independent Proof Red Team. IDEA -> SEARCH -> ITERATE.**

**Overall status.** **PROVED/EXACT:** a sound native `R_mix341` completion cannot automatically export a LOCAL circuit's internal gates as asserted proof conditions. The single checked LOCAL root is the automatic assertion; an internal gate is only a term unless it receives its own paid implication inference, and a fresh public semantic variable still requires paid DEF. A three-derived-node satisfiable-source discriminator makes the unsoundness explicit. **PROVED/RESTRICTED:** explicit constant-support internal term ports can be normalized polynomially in their encoded evidence count, but not necessarily in paid-node count. **COMPUTATIONAL:** 1,351 checks across independent Python and JavaScript implementations. **OPEN:** exact private-term/path bytes, DEF facet and GF(2)-row selectors, a full all-consumer polynomial node/bit compiler, actual noncircular same-fixed-`R_mix341` B3, a superpolynomial full-mixed minimum and P versus NP. Fixed rules, weights, roles, schedules and enabled states are unchanged. No other role's manuscript region was edited.

## IDEA before SEARCH

**Initial falsifiable hypothesis.** The strongest permissive exported-wire reading should fail soundness before cost becomes relevant. A LOCAL record may validly assert its checked root, but an internal gate need not be entailed by the parent. Prediction: a satisfiable two-variable source has a three-node AND3--LOCAL--RES trace deriving the empty clause if an internal `NOT x` gate inside an entailed tautological root is automatically exposed as an asserted condition.

Four falsifiers were registered:

1. the source, AND3 factor or LOCAL root is not legal under the literal `/341` rules;
2. the parent factor actually entails the internal `NOT x` gate;
3. treating every internal gate as an asserted proof fact remains sound on all two-variable factors;
4. a polynomial SAT decider can use its internal configuration bits as `R_mix341` assertions without separately deriving their logical content from the source.

## SEARCH: governing source, issue/peers, Grok/Claude, primary literature and OpenAI GitHub

Read the 118,528-character governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (blob `c3889a3e...`) and the authoritative original calculus `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`). The relevant original statements are:

- every rule preserves logical consequence, with DEF interpreted conservatively;
- AND3 produces an exact truth-table factor on support of at most three original variables;
- LOCAL-CONVERT derives **a clause or bounded-support Boolean circuit condition** from one factor/equation after a constant-support implication check;
- DEF alone introduces one fresh variable, with all defining relations attributed to that paid node and later uses referencing it.

Current issue #3 was read through LSPV-4/404. The closest peer results were assessed rather than merged by authority:

- LSPV-1/410 gives a linear mixed lower/upper sandwich for an odd-wheel family, so that family is not a superpolynomial B3 witness.
- LSPV-2/409 and LSPV-3/412 improve paid-DEF/facet replay under an extra individually addressable DEF-facet selector assumption; neither authorizes native LOCAL internal assertions.
- LSPV-4/404 proves a public paid-DEF-to-LOCAL projection lemma under an explicit typed selector assumption. Its failed outside-support test reinforces that typing/support cannot be omitted.
- REFEREE349 argued for a strict root-only reading; REFEREE350 retained a grammar caveat because the bytes do not specify private/public internal IDs. REFEREE353 proved that every fresh public semantic variable has one paid DEF owner. REFEREE354 proved that an AND3 GF(2) annotation consumed by XOR is proof type, not disposable semantic metadata.

Actual independent assessments were located and read. `GROKPROOF/2026-11-05_0515_PROGRESS.md` (blob `f348f7bb...`) keeps the universal all-input fully charged transformation open; it has no native LOCAL/B3 theorem. Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob `1f9fc727...`) and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (blob `9a5b05d6...`) concern restricted alternation/sequential-access results, not this grammar or bridge.

Recorded general-web queries included:

- `extended resolution extension variable circuit gate definition fresh variable proof system primary paper PDF`;
- `proof logging circuit internal wires definitions asserted conditions soundness DRAT LRAT primary`;
- `P equals NP extended Frege polynomially bounded reflection principle propositional proof systems primary paper`;
- `Haken pigeonhole resolution Cook extended resolution PHP primary exact model`;
- `Braun 2026 Res(oplus) bit pigeonhole principle DAG lower bound arxiv`;
- `Resolution over linear equations modulo 2 lower bounds Tseitin Res XOR primary paper`.

Useful primary evidence:

- Beckmann--Buss's author-hosted paper states the Extended-Frege extension rule as `x <-> phi` with `x` new and absent earlier. Bryant--Heule's 2023 ER proof-generation paper likewise requires a new extension variable plus defining clauses checked by the proof checker. Internal circuit structure is not silently asserted true; a named semantic abbreviation is tied to its definition.
- Modern LRAT descriptions distinguish an added clause from the dependency IDs justifying it. A referenced object is not automatically a new asserted clause.
- Fleming et al. and the bounded-arithmetic literature treat reflection as an explicit proof object/theorem. Pich--Santhanam's ECCC TR23-199 makes self-provability an additional condition in transfers involving EF and SAT upper bounds. This supports the firewall; it does not prove or refute actual B3.
- Haken's 1985 result is ordinary Resolution hardness for pigeonhole tautologies, while its own abstract notes polynomial Extended-Resolution proofs. Braun's 2026 theorem is an unrestricted-DAG `Res(oplus)` lower bound for bit-PHP, still an exact proof-system result.

Accessible sources included <https://mathweb.ucsd.edu/~sbuss/ResearchWeb/NPsearchFrege/paper.pdf>, <https://www.cs.cmu.edu/~bryant/pubdir/tocl23.pdf>, <https://www.cs.mun.ca/~nfleming/papers/TFNP.pdf>, <https://eccc.weizmann.ac.il/report/2023/199/>, and <https://arxiv.org/abs/2609.23015>. Some publisher full texts were unavailable, so author/ECCC/arXiv versions were used. **Direct Google-branded search was unavailable**; no Google result is claimed.

Authenticated `github.com/openai` searches were `extended resolution proof checker`, `LRAT clause dependencies`, `circuit internal wire proof`, and `ExecCNFNodeSearchCosts`. No relevant proof checker/compiler was found. The complete OpenAI Math execution-cost file remains useful accounting infrastructure, not a same-`R_mix341` proof translation. Unrelated code matches were not treated as mathematical evidence.

## ITERATE I: the exact satisfiable-source discriminator

Use the strict DIMACS source

```text
p cnf 2 2
1 0
1 2 0
```

Thus `F=(x) AND (x OR y)`, with the two models `(x,y)=(1,0),(1,1)`. In valuation order `00,01,10,11`:

1. **AND3** of the two source clauses derives their exact conjunction, factor `x`, table `[0,0,1,1]`.
2. **LOCAL-CONVERT** derives the circuit root `x OR (NOT x)`, table `[1,1,1,1]`. The implication `x => (x OR NOT x)` passes the exact local check. Inside this circuit, gate `g=NOT x` has table `[1,1,0,0]`.
3. Under the proposed **automatic asserted-export** interpretation, use internal `g` as clause `(NOT x)` and resolve it with source clause `(x)`, deriving the empty clause.

The parent factor does **not** entail `NOT x`; both source models falsify it. Hence the permissive interpretation refutes a satisfiable authenticated source and violates `/341`'s declared soundness.

### Theorem (LOCAL assertion-port soundness)

In any sound completion of the original `R_mix341` rules, a LOCAL record automatically asserts only the root condition whose implication was checked. An internal circuit gate cannot automatically be exported as an asserted proof condition. It may instead be:

1. private syntax local to the root record;
2. an expression/term port, carrying a Boolean function but no claim that the function evaluates to true; or
3. the subject of a separate paid inference/definition.

If an internal expression over existing variables is to become an asserted proof condition, that implication requires its own paid LOCAL-CONVERT record and check. If it is to become a fresh reusable semantic variable, it requires a paid conservative DEF owner.

**Proof.** The displayed legal AND3 and legal LOCAL root have a satisfiable source. The internal gate `NOT x` is not a logical consequence of the parent. Any generic rule automatically asserting every internal gate therefore derives a false condition, and RES makes the soundness failure explicit. Since the original rule promises consequence preservation, that generic assertion export is not a legal completion. A separately checked internal condition is simply another paid LOCAL inference; a new assignment coordinate is covered by the original fresh DEF rule and REFEREE353's provenance induction. QED.

Two derived nodes already witness the nonconsequence: AND3 followed by LOCAL containing the bad internal term. Three are minimal for the parent--LOCAL--downstream-consumer pattern ending in an explicit contradiction.

### What this settles and what it does not

This resolves the most dangerous ambiguity: **exported wire does not mean free asserted fact**. The semantic assertion interface is root-only. It does not forbid serialization of private subexpressions or selection of an internal term as syntax inside a later expression. Such a term port must retain its non-assertive type, and any binding to a fresh public variable is paid.

The remaining byte-level question is whether a later record may address a private term by a path/ID and, if so, how sharing, scope and source/support authentication are encoded. That affects normalization cost even though it no longer affects soundness.

## ITERATE II: restricted normalization consequence

Suppose a completion explicitly serializes `p` distinct referenced internal term ports, each a Boolean function of at most three named original inputs, in a supplied `E`-bit proof. None is an asserted fact. By the exact three-input circuit catalogue used in LSPV-3/411, each term can be rebound by at most four paid arbitrary two-input DEF gates, after which all consumers can reference the paid output. Therefore this exported-**term** fragment has a source-preserving normalization using at most `4p` new DEF nodes plus consumer replay.

This is polynomial in explicit evidence because `p<=E` under any nonempty port encoding. It is **not** necessarily polynomial in source length plus old paid-node count `N+q`: one uncharged LOCAL payload could contain arbitrarily many encoded ports. Thus:

- polynomial-in-`E` normalization survives explicit term exports;
- node-only polynomial balance requires a paid-port bound or a proof that `p<=poly(N+q)`;
- automatic asserted exports are excluded outright by soundness, not merely charged later.

Full normalization still needs the exact DEF defining-facet selector, DEF-to-GF(2) row typing, AND3 annotation preservation and all consumer rewrites. The current theorem removes one illegal consumer class rather than declaring the whole compiler finished.

## ITERATE III: exhaustive and independent verification

`experiments/arc/lspv5_355_local_port_soundness.py` parses both-label strict DIMACS controls, reconstructs the exact AND3 factor, checks the LOCAL root implication, distinguishes port kinds and exhibits the false permissive refutation. It then exhausts all 15 nonempty Boolean factors over two variables against all 16 internal functions. For every pair, the circuit root `g OR NOT g` is entailed; automatic assertion of `g` is unsound exactly when the factor does not entail it.

Exact catalog:

- 15 nonempty factors;
- 16 internal functions;
- 240 factor/function pairs;
- **175 unsound automatic asserted exports**;
- 65 pairs where the particular internal function happens to be entailed.

The Python audit passed **687 checks**, including two-model SAT, zero-model UNSAT, four port modes, five malformed encodings and Resolution mutations. `experiments/arc/lspv5_355_local_port_soundness_independent.mjs` independently reproduced the complete catalog and witness in **664 checks**. Combined: **1,351 checks**.

Finite enumeration is confirmation of the elementary general soundness proof, not the source of that proof.

## ITERATE IV: B3 trace-type firewall

The target remains

`SAT in P  =>  exists C,k forall N: Wbar_Rmix341(N) <= C(N+1)^k`.

No proof or refutation of this actual same-fixed-system implication was obtained. The LOCAL result does refute one concrete noncircular-looking shortcut:

> “Serialize the polynomial decider's internal configuration circuit and expose selected internal state bits as proof facts.”

A machine state bit has a value in one syntactic execution. That does not make the corresponding Boolean condition a logical consequence of every assignment satisfying the source CNF. The LOCAL discriminator has exactly this shape: the full circuit root is justified, while an internal bit is not. Turning trace/configuration terms into assertions for free is an unsound semantic oracle.

A valid trace bridge must instead do all of the following:

1. define every fresh logical wire conservatively using paid DEF or inline it as a term;
2. derive each asserted clause/equation/condition from authenticated source premises using native rules;
3. prove that the final rejection state entails contradiction for every source valuation, not merely record that one program execution rejected the source string;
4. bound the resulting paid nodes, encoded bytes, construction/checking work and peak space polynomially.

Item 3 is the missing correctness/reflection step. EF's short self-reflection results do not automatically formalize an arbitrary externally chosen SAT decider's global correctness or provide a translation into this exact calculus. Pich--Santhanam's self-provability conditions underscore that this is extra structure. Cook--Reckhow still yields some polynomially bounded system under `NP=coNP`, not a polynomial simulation into preselected `R_mix341`.

Therefore actual B3 remains **OPEN**. The result is a precise type/soundness barrier, not an oracle separation or a lower bound for all possible bridges.

## Established-hard-family controls with exact boundaries

- **Haken PHP:** standard unary pigeonhole CNFs; quantification over every ordinary Resolution refutation; exponential length for infinitely many sizes. No extension variables, GF(2), LOCAL circuits or arbitrary machines. Haken's abstract itself contrasts polynomial Extended-Resolution proofs.
- **Cook ER:** polynomial PHP refutations introduce explicitly defined new variables. This defeats any attempt to transfer the Resolution lower bound through paid DEF without a polynomial backtranslation in the correct direction.
- **Odd Tseitin:** `/341` has linear mixed refutations by local parity extraction and XOR summation. Resolution hardness is therefore a mandatory negative control, not mixed-system hardness.
- **Braun bit-PHP:** for `n=2^ell`, `ell>=32`, every DAG-like `Res(oplus)` refutation has more than `exp(n/(32768 ell^2))` clauses. Its lines are disjunctions of affine equations for a specific bit-PHP encoding. It is not an ER, `R_mix341` or SAT-machine lower bound.

No restricted proof-system result is promoted to unrestricted computational hardness.

## Fully charged physical-cost and XOR-state ledger

The concrete discriminator has three paid logical nodes. Its physical checker must still parse source bytes, truth-table entries, gate opcodes, port-kind tags, parent IDs and the RES pivot; evaluate the circuit; validate implication; and store or recompute tables.

For a supplied proof of `E` bits with `p` explicit term ports, an exact checker must read the port definitions and type tags. A buffered indexed implementation uses `O(E)`-scale host storage and polynomial time; a repeated-scan read-only implementation can reduce writable scratch at the cost of more head movement and rescanning. A normalized output binding every referenced port requires `Omega(p)` output records/bits and up to `4p` paid DEF nodes in the stated three-original-input fragment. Discovery, template lookup, rewriting references, serialization and independent checking remain separately charged. No host RSS or native FLMV exponent was measured.

Offline state-XOR control: the native root-only and permissive asserted-port views have the identical LOCAL root truth table, so `d_logic(root)=0`. A declared one-bit port-kind tag changes from term to assertion, so a fixed materialized encoding has `d_phys>=1`. Proof validity changes even though the logical root delta is zero. This is an offline diagnostic, not a universal runtime lower bound: reads, head moves, unchanged writes and recomputation can cost work without changing any recorded data bit.

## Precise outcome and next unresolved step

**Settled:** free asserted export of LOCAL internal gates is incompatible with native soundness. The exact semantic typing repair is:

`checked root -> asserted condition; internal gate -> term; separately asserted term -> paid LOCAL; fresh semantic name -> paid DEF`.

This strengthens the root-only semantic reading while allowing typed private-term serialization.

**Not settled:** the machine-readable term-path syntax and scope; whether paid DEF nodes expose addressable clause/GF(2) facets; the exact bit/node balance for term payloads; and a whole-DAG compiler covering RES, AND3 annotations, GF(2), DEF and every legal LOCAL consumer.

**B3:** actual noncircular same-fixed-`R_mix341` B3 remains OPEN. A successful proof must construct typed native evidence for decider correctness rather than assert trace bits. P versus NP remains OPEN.

## Artifacts

- Python checker: `experiments/arc/lspv5_355_local_port_soundness.py`
- Independent JavaScript checker: `experiments/arc/lspv5_355_local_port_soundness_independent.mjs`
- Raw record: `results/raw/arc/2026-11-04_2248_LSPV5_355_LOCAL_PORT_SOUNDNESS.json`
- Five-role handoff: `research/coordination/2026-11-04_2248_LSPV5_LOCAL_PORT_SOUNDNESS_REFEREE355_HANDOFF.md`
