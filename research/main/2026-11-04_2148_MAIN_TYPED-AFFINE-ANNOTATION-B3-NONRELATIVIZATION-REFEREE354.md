# REFEREE354: Typed affine-annotation survival and the same-system B3 firewall

**November 4, 2026, 21:48 PST. LSPV-5 Independent Proof Red Team. IDEA -> SEARCH -> ITERATE.**

**Overall status.** **PROVED/EXACT:** a three-derived-node legal native `R_mix341` witness refutes normalization by exact Boolean relation alone; a consumer-aware canonical repair is proved for the bounded-support AND3/GF(2)/XOR subfragment. **COMPUTATIONAL:** 838 assertions in independent Python and JavaScript implementations, with SAT, UNSAT, malformed and mutation controls. **REFUTED AS BRIDGE SCHEMATA:** type-erased decider traces, Cook--Reckhow existence without same-system simulation, and any argument that treats semantic equivalence as native proof-record equivalence. **OPEN:** the completed machine-readable exported-port/LOCAL/DEF grammar, a full rule-by-rule polynomial compiler, actual noncircular same-fixed-`R_mix341` B3, a superpolynomial full-mixed minimum and P versus NP. The fixed rules, weights, task identity, schedule and enabled state are unchanged. No other role's manuscript region was edited.

## IDEA before SEARCH

**Initial falsifiable hypothesis.** An exact AND3 factor can carry a certified GF(2) annotation which is consumed by a later XOR. A normalizer that preserves the factor's complete Boolean relation but erases this annotation should therefore preserve semantics while destroying native consumer typing. Prediction: a legal witness exists with two original variables and three derived nodes under the distinct-parent convention.

Four falsifiers were registered:

1. the proposed source fragment or one of its three rule applications is not legal under the literal `/341` rules;
2. the two annotations are not exactly equivalent to their AND3 factors on every valuation;
3. native XOR remains legal after one parent annotation is erased, without inserting or rederiving any typed row;
4. primary literature proves that `SAT in P` alone makes this preselected fixed mixed calculus polynomially bounded, without an additional simulation/reflection theorem.

## SEARCH: governing source, project, Grok/Claude, literature and OpenAI GitHub

The authoritative calculus was read from `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. Its literal relevant rules are:

- AND3 derives the exact conjunction of two conditions on combined support of at most three **original** variables as an eight-bit truth-table factor;
- such a factor may be annotated by a GF(2) row only after exhaustive local equivalence checking, with the annotation a deterministic local normal-form choice at that same paid node;
- XOR accepts two GF(2) equations and returns their sum;
- every derived node costs one and has at most two antecedents.

The governing five-role handoff and current issue #3 were reviewed. Current peers were read and independently separated from the present claim:

- LSPV-1/409, `research/agents/lspv-1/2026-11-04_2100_LSPV-1_THREE_NODE_PORT_ORACLE_B3_FIREWALL409.md`, gives a completion discriminator and a relativizing-oracle firewall. Its completion discriminator is not certified native grammar. Its oracle argument is a valid black-box warning, not a refutation of actual `R_mix341` B3.
- LSPV-2/408, `research/agents/lspv-2/2026-11-04_2112_LSPV-2_FACET_REPLAY_NORMALIZATION408.md`, proves a conditional bounded-variable DEF-facet/pure-RES replay theorem. It explicitly assumes a readable facet selector and does not normalize the full native grammar.
- LSPV-3/411, `research/agents/lspv-3/2026-11-04_2124_LSPV-3_EXACT_FOUR_GATE_PUBLIC_PORT411.tex`, improves public-output normalization over three original inputs to four paid gates per output, but does not preserve arbitrary private consumers.
- REFEREE353, `research/main/2026-11-04_2048_MAIN_FRESH-WIRE-PROVENANCE-B3-REFLECTION-FIREWALL-REFEREE353.md`, proved paid ownership of every non-source public semantic variable and a separate LOCAL/RES consumer counterexample.

Actual Grok/Claude files were located and read rather than guessed. `GROKPROOF/2026-11-05_0515_PROGRESS.md` keeps the fully charged all-input contraction open and supplies no native grammar/B3 theorem. Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` concern restricted alternation and sequential-access theorems; neither supplies the missing compiler or reflection step.

Recorded general-web queries included:

- `oracle P=NP extended Frege not polynomially bounded proof system oracle separation`;
- `oracle no p-optimal proof system P equals NP proof complexity Krajicek Pudlak`;
- `SAT in P extended Frege polynomially bounded open reflection principle`;
- `proof logging XOR Gaussian elimination SAT solver certificate format parity reasoning primary paper`;
- `resolution over linear equations modulo two proof lines affine equations exact rule primary paper PDF`;
- `FRAT LRAT proof format typed clauses identifiers proof checking primary paper`.

Useful primary results were read rather than inferred from snippets:

- Philipp--Rebola-Pardo, *DRAT Proofs for XOR Reasoning* (2016), explains that direct XOR-to-DRAT translation can blow up, whereas a T-translation with fresh variables avoids that blow-up. This supports the exact distinction between retaining/rederiving explicit typed parity evidence and merely preserving formula semantics.
- Gocht--Nordstrom, *Certifying Parity Reasoning Efficiently Using Pseudo-Boolean Proofs* (AAAI 2021), treats efficient machine-verifiable logging of parity reasoning as a separate construction problem, not as a consequence of a solver's answer bit.
- Ben-David--Gringauze, ECCC TR98-021, studies oracle-relativized propositional proof systems. Its collapse/optimal-system statements do not establish polynomial boundedness of this preselected fixed calculus.
- Cook--Reckhow (1979) gives existence of some polynomially bounded proof system under `NP=coNP`; transfer to a named system requires a polynomial simulation.

The XOR sources were available at <https://repositum.tuwien.at/handle/20.500.12708/355> and <https://ojs.aaai.org/index.php/AAAI/article/view/16494>; the oracle paper was available at <https://eccc.weizmann.ac.il/report/1998/021/>. Some publisher-hosted full texts were blocked, so accessible author/repository versions were used. **Direct Google-branded search was unavailable**, and no Google result is claimed.

Authenticated `github.com/openai` searches were `XOR Gaussian elimination certificate`, `FRAT LRAT`, `parity proof checker` and `ExecCNFNodeSearchCosts`. The proof-format searches returned no relevant implementation. The known complete `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` is useful resource accounting but is not a mixed proof checker or source-retraction compiler. Code is not treated as a mathematical theorem.

## ITERATE I: exact native typed-annotation counterexample

Use the strict DIMACS source

```text
p cnf 2 3
1 0
2 0
1 2 0
```

Thus `F=(x) AND (y) AND (x OR y)`, whose unique model is `x=y=1`. In valuation order `00,01,10,11`, build this paid native DAG:

| node | rule | parents | exact object | certified affine annotation |
|---|---|---|---|---|
| 1 | AND3 | source `(x)`, source `(x OR y)` | `[0,0,1,1]` | `x=1` |
| 2 | AND3 | source `(y)`, source `(x OR y)` | `[0,1,0,1]` | `y=1` |
| 3 | XOR | nodes 1, 2 | `x XOR y=0` | n/a |

Every rule is in the unambiguous original fragment. Each support has two original variables. Both annotations are exactly equivalent to their factor on all four valuations. Node 3 is the algorithmic GF(2) sum `(x=1) XOR (y=1)`, namely `x XOR y=0`.

Now transform node 1 by retaining its support and exact four-bit table **unchanged** while erasing its GF(2) annotation. The Boolean relation is identical, but node 3 no longer has two GF(2)-equation parents and is not a legal native XOR inference.

### Theorem (typed affine-annotation survival)

Any edge-preserving `R_mix341` normalization that replaces an AND3 parent of a retained XOR consumer must do at least one of the following:

1. retain an exactly equivalent certified GF(2) annotation at that parent; or
2. insert/rederive an exactly equivalent typed GF(2) row and rewire the XOR consumer.

Preserving only the parent's Boolean relation is insufficient.

**Proof.** The original XOR rule's premise type is “GF(2) equation,” not “arbitrary Boolean relation equivalent to some affine equation.” After annotation erasure, the retained parent is only a factor record. No rule allows XOR to consume that unannotated factor directly. Hence the retained edge is ill-typed unless a certified equation is retained or reintroduced. The displayed legal witness realizes the premise and the failure. QED.

This is an explicit legal counterexample to **relation-only** or **type-erasing** full normalization. It is not a counterexample to every possible consumer-aware compiler. Under a convention requiring two distinct XOR parents, three derived nodes are minimal for this obstruction form: two typed producers and one downstream consumer. No absolute minimality is claimed if duplicate parent identifiers are permitted.

## ITERATE II: restricted canonical repair

The search evidence changed the initial idea from “annotation erasure is a terminal obstruction” to a sharper statement: it is a fatal omission in a claimed normalization theorem, but it has a local bounded-support repair.

### Lemma (constant local affine reconstruction)

Let a normalized AND3 record preserve the ordered original-variable support `S`, with `|S|<=3`, and preserve its exact truth table `T`. Whether `T` is exactly a GF(2) equation, and the unique equation if so, can be recovered by exhaustive comparison against all `2^(|S|+1)<=16` mask/RHS rows. Thus the native deterministic annotation can be reconstructed with constant truth-table work per AND3 record and no additional logical inference node.

**Proof.** There are `2^|S|` masks and two RHS bits. Distinct affine equations have distinct truth tables: if `(a,r)!=(b,s)`, their XOR is a nonzero affine function and is not identically zero. Hence at most one candidate matches `T`; testing all candidates gives existence and the unique row. Since `|S|<=3`, at most sixteen candidates and eight valuations are examined. QED.

This repairs the current witness **provided support identity/order is preserved and every XOR consumer is replayed against the reconstructed row**. It does not settle DEF facet selectors, exported LOCAL subexpressions, support renaming, private circuit payloads or a full consumer-aware source-retraction theorem.

## ITERATE III: independent finite verification

`experiments/arc/lspv5_354_typed_affine_annotation.py` independently parses the strict source, enumerates SAT/UNSAT controls, checks exact AND3 tables, verifies affine annotations and enforces typed XOR premises. It exhausts all 16 Boolean factors over two variables against all eight affine candidates. Exactly eight factors are affine and each has one unique annotation. It also checks all 64 pairs of affine rows pointwise and rejects a corrupted table, wrong RHS, wrong mask and erased annotation, plus five malformed DIMACS inputs. Result: **687 assertions passed**.

`experiments/arc/lspv5_354_independent.mjs` reimplements the exhaustive affine catalog and witness without importing the Python code. Result: **151 assertions passed**. Combined total: **838**.

Both-label controls are explicit: the displayed source has exactly model `(1,1)`; `(x) AND (NOT x)` has no model. The witness is not an UNSAT certificate and is not presented as one.

## ITERATE IV: noncircular B3 audit

The target remains

`SAT in P  =>  exists C,k forall N: Wbar_Rmix341(N) <= C(N+1)^k`.

No proof or refutation of this actual same-fixed-system implication was obtained. The present witness does, however, close one tempting loophole.

### Exact type firewall

A polynomial SAT decider's rejection bit or raw configuration trace supplies no native guarantee that a record intended for an XOR consumer carries an exact GF(2) annotation. Boolean semantic correctness of the decider is not enough: the witness has identical factor semantics before and after annotation erasure, while native proof validity changes. Therefore a trace-to-`R_mix341` bridge must explicitly construct and check all rule types, supports, source ancestry, exported wires and annotations. Declaring trace states “semantically equivalent” does not do this.

Three bridge schemata remain invalid:

1. **Cook--Reckhow existence without simulation.** `SAT in P` yields `NP=coNP` and hence some polynomially bounded proof system. It does not yield polynomial `R_mix341` proofs without a polynomial translation into this same fixed calculus. Moreover, `W_R` counts paid nodes while Cook--Reckhow proof length counts bits; polynomial node/bit balance for opaque LOCAL payloads is itself unproved.
2. **Reflection by assertion.** Adding “the polynomial decider rejects F, therefore false” is a new semantic/reflection rule. Proving that rule's correctness internally, uniformly and with polynomial source-authenticated output is the missing bridge, not a consequence of its label.
3. **Relativizing black-box transfer.** LSPV-1/409's `O=TQBF` control gives `P^O=NP^O` while ordinary Resolution still has Haken's PHP lower bound. This blocks generic relativizing arguments for arbitrary fixed systems such as Resolution. It does not by itself refute actual mixed-system B3; a valid `R_mix341` proof could be nonrelativizing and exploit DEF/GF(2)/LOCAL.

Thus the corrected conclusion is a strengthened **barrier**, not a B3 refutation. A successful B3 proof must be noncircular, same-system, rule-by-rule typed, source-authenticated, polynomial in paid node cost, and must separately control encoded proof bits if it invokes Cook--Reckhow machinery.

## Established-family controls and exact model boundaries

- **Haken PHP:** the exponential lower bound quantifies over ordinary shared-DAG Resolution refutations of the standard unary pigeonhole CNF. It does not quantify over ER, GF(2), `R_mix341` or arbitrary SAT machines.
- **Cook ER:** extension variables yield polynomial PHP refutations, so a Resolution lower bound cannot be backtranslated through DEF with exponential overhead and then called machine hardness.
- **Odd Tseitin:** `/341` has exact linear mixed refutations by AND3 extraction and GF(2) summation, a mandatory countercontrol to Resolution hardness.
- **Res(XOR):** lower bounds apply to their exact line language and encodings. They do not automatically cover conservative gates, LOCAL circuits or arbitrary algorithms.

No restricted proof lower bound is promoted to unrestricted SAT computation.

## Physical-cost ledger

The three-node witness has logical paid cost three. That count omits neither physical work nor proof bytes by fiat. A checker or normalizer must read the source and proof records, check support names/order, compare up to eight truth-table entries, compute masks and RHS bits, validate parent IDs and topological order, serialize the output and retain or reconstruct lookup state.

For a supplied proof with `q` nodes and `E` encoded bits, the restricted repair can scan every AND3 record and test at most 16 candidate rows on at most eight valuations. On a RAM-like host this is `O(E+q log V)`-scale bit access plus output under ordinary indexed encodings; a sequential tape implementation must additionally charge head motion and rescans. It may use a stored node table (`O(E)`-scale host storage) or recompute with greater time and logarithmic counters. These are implementation upper bounds, not native FLMV bounds. The host peak RSS was not measured and is not fabricated.

The XOR state-difference diagnostic is offline here. Erasing or re-inserting annotation bits contributes physical writes in a materialized fixed layout, but logical annotation equality is not itself a universal runtime lower bound. Read-only validation, head movement, unchanged writes and failed attempts can consume time with zero logical-data XOR delta.

## Precise result and next unresolved step

**Settled this run:** an exact Boolean-relation quotient is too coarse for native normalization. A correct node signature must include at least the semantic relation, ordered support, certified GF(2) row when present, public/exported port identity, source ancestry and consumer type. For the bounded-support AND3/GF(2)/XOR fragment, annotations can be reconstructed canonically with constant local work once exact table and support are preserved.

**Still open:** specify the accepted proof bytes and selector rules for LOCAL circuit roots/subexpressions, DEF clause/row facets, exported-wire paths and consumer scopes. Then prove a whole-DAG compiler that replays every consumer and gives polynomial bounds on paid nodes **and** encoded evidence. Until that exists, full normalization is neither proved nor refuted by this restricted repair.

**B3:** actual same-fixed-`R_mix341` B3 remains OPEN. The next noncircular attempt must exhibit a uniform polynomial source-authenticated compiler from the consequence of `SAT in P` into these exact typed records, without assuming polynomial certificates, a formalized decider-correctness proof or an oracle for semantic equivalence. P versus NP remains OPEN.

## Artifacts

- Python checker: `experiments/arc/lspv5_354_typed_affine_annotation.py`
- Independent JavaScript checker: `experiments/arc/lspv5_354_independent.mjs`
- Raw record: `results/raw/arc/2026-11-04_2148_LSPV5_354_TYPED_AFFINE_ANNOTATION.json`
- Five-role handoff: `research/coordination/2026-11-04_2148_LSPV5_TYPED_AFFINE_ANNOTATION_REFEREE354_HANDOFF.md`
