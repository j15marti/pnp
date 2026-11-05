# REFEREE359 — native paid-node closure, canonical balance, and implicit-proof firewall

**LSPV-5 Independent Proof Red Team — November 5, 2026, 02:48 PST**  
**Status:** PROVED/EXACT textual-closure theorem; PROVED/RESTRICTED semantic normalization for the literal paid-node/root-only completion; COMPUTATIONAL independent controls; exact byte parser and same-`R_mix341` B3 OPEN. **P versus NP OPEN.**

No task, schedule, enabled state, rule, or weight is changed. This report does not edit another role's manuscript region.

## IDEA before search

Hypothesis: if every selector, exported object, GF(2) coefficient and definition consumed by a proof is an explicitly serialized paid object, then every `q`-node proof in the fixed `/341` calculus has a source-authenticated encoding of size polynomial in `N+q`. Falsifiable prediction: the original `/341` text either (i) gives a legal uncharged exported-wire or implicit-proof mechanism, refuting node-to-byte normalization, or (ii) exposes only paid-node roots/fixed facets, in which case constant-support roots and affine rows canonically serialize in polynomial bytes.

Registered falsifiers:

1. a downstream antecedent naming a LOCAL internal gate rather than a paid node;
2. an implicit circuit describing exponentially many Resolution lines accepted as one native record;
3. a DEF or AND3/GF(2) consumer whose selected semantic object cannot be represented from a paid node in polynomial bits;
4. a long redundant payload showing that reading/checking supplied evidence is not bounded by paid-node count.

## SEARCH

### Project and peer record

Read first `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (current blob `c3889a3e`). Read issue #3 through LSPV-2/413 at 02:12 PST, including LSPV-1/414, LSPV-3/418, LSPV-4/408 and REFEREE358. Read the authoritative source

`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`

at blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`, plus the `/384` audit at blob `bbcdad9a`. The source says:

- every derived node has unit cost and at most two **antecedent-node identifiers**;
- AND3 has combined support at most three original variables;
- LOCAL-CONVERT produces one clause or bounded-support circuit condition after a constant-support truth-table implication check;
- DEF introduces one fresh semantic variable as one paid two-input gate, with later uses referencing its charged node;
- other rules require a later version and separate audit.

It does **not** specify a finite-alphabet byte parser, clause-facet selector bytes, LOCAL internal-gate identifiers, or GF(2)-row selectors.

LSPV-1/414 independently confirms that a circuit describing an exponential Resolution tree has coNP-complete global validity and is not a native locally checked proof. LSPV-3/418 preserves paid-DEF output-polarity only conditionally through consumers because selectors remain unspecified. LSPV-2/413 shows affine-only elimination of nonlinear paid definitions fails but gives a compact CNF repair. LSPV-4/408 gives conditional bounded-live-port compression, not a native export grammar.

Actual external assessments were read: `GROKPROOF/2026-11-05_1218_PROGRESS.md` (`d3183283`), Claude `TPORT-0002` (`1f9fc727`) and `ONETAPE-0001` (`9a5b05d6`). They concern restricted circuit-simulation, alternation-trading, or sequential-access bounds and supply neither a same-calculus compiler nor B3.

### Literature and OpenAI GitHub

Actual web queries:

- `Cook Reckhow propositional proof systems proof length encoding polynomially bounded original paper PDF`;
- `Krajicek implicit proofs succinct proof complexity exponential proof represented circuit original paper`;
- `Haken 1985 intractability of resolution pigeonhole principle proof size encoding original paper`;
- `extended Frege proof systems polynomial boundedness NP coNP reflection principles primary source`.

Read the full available Cook--Reckhow paper, especially Definition 1.3 and Proposition 1.6: a proof is a finite string, polynomial boundedness is a bound on that string, and p-simulation requires a polynomial-time translating function. Read the ECCC primary record for Krajíček's *Implicit proofs*: `iP` is explicitly a possibly much stronger proof system in which exponentially long `P` proofs are represented by polynomial circuits. Read Haken's publisher abstract: the lower bound is ordinary Resolution and Extended Resolution has polynomial PHP proofs. Direct Google-branded search was unavailable; general indexed web search was used and is not reported as Google.

Authenticated `github.com/openai` searches were `ExecCNFNodeSearchCosts`, `LRAT proof checker certificate bytes`, and `CookLevin MachineLemmas polynomial witness`. Full files read:

- `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean`, blob `1ced21f4`: actual execution, trace, storage and visit-log bounds; no arbitrary callback or unbounded state is free.
- `openai/math/lean/OAI/Computability/PerfectCompleteness/Machines/WitnessEncodingLemmas.lean`, blob `35d68b1e`: explicit witness capacity, encoding, validity and polynomial bounds are hypotheses/constructions, not consequences of a one-bit decider answer.

No OpenAI repository result supplies the native `/341` parser or a same-system B3 bridge.

## ITERATE

### Theorem 1 — literal paid-node closure excludes free exported wires

Under the ordinary closure convention for the enumerated `/341` rules, every inference edge names an earlier derived-node identifier. A LOCAL circuit-internal gate is syntax inside the one derived LOCAL condition; it is not itself a derived node, has no node identifier, and no enumerated rule exports it. Therefore a downstream reference `(LOCAL-node, internal-wire-id)` is not a legal antecedent of the literal rule set. To make that wire a reusable semantic variable requires a separately paid fresh DEF; to assert another LOCAL term requires another paid LOCAL-CONVERT.

**Proof.** The first paragraph of the fixed calculus quantifies edges over antecedent-node identifiers. The LOCAL rule creates one derived node, namely its root clause/condition. None of RES, AND3, XOR, LOCAL or DEF contains an internal-wire export formation rule. `/341` expressly says that any other equivalent sound rule belongs only to a later separately audited version. Closure under the listed formation rules therefore never creates the proposed internal-wire identifier. ∎

This settles **free exported wires negatively for the literal semantic calculus**. It does not invent missing byte syntax, and it does not prohibit a future separately specified exported-port calculus.

### Theorem 2 — polynomial semantic canonical balance

Let `pi` be a valid literal-closure proof with `q` paid nodes from a DIMACS source of `N` bits. Assume only constant-many fixed facets of each paid DEF/AND3 node are selectable, and consumers reference paid-node roots/facets rather than internal LOCAL gates. Then there is an original-source-authenticated canonical encoding of the same typed DAG using

`O(N + q (n+q) log(n+q))`

bits, hence polynomial in `N+q`, where `n <= N` is the number of original variables.

**Construction and proof.** Alpha-rename the at most `q` fresh DEF variables topologically to `z_0,...,z_{q-1}` and nodes to `0,...,q-1`. Parent identifiers use `O(log q)` bits.

- A clause is a duplicate-free sorted set of signed names among at most `n+q` variables.
- A GF(2) row is a bit mask over those names plus one RHS bit.
- An AND3 factor or LOCAL root has support at most three original variables and an eight-bit truth table. A clause output is stored as a sorted clause.
- A two-input DEF is two earlier variable names plus one of sixteen four-row Boolean tables. Its complete relation has at most four canonical three-literal falsifying-row clauses; a fixed facet index is constant-size.
- RES stores two parents and one pivot.

These records preserve the exact root Boolean relation, GF(2) type/RHS, positional gate inputs, source labels, proof edges and all fixed-facet consumers. Summing the record bounds gives the display. The construction does not discover a proof and does not erase GF(2); it merely canonicalizes a supplied valid semantic DAG. ∎

**Important scope.** `/341` still lacks an authoritative finite-alphabet parser. The theorem proves a canonical encoding exists for its literal semantic closure; it cannot prove that an arbitrary historical byte string is accepted by a checker that was never specified. Thus the exact-byte deliverable is settled negatively as a documentation fact: there is no unique native byte grammar to normalize until one is frozen. The semantic rule set, however, does not license free internal-wire exports.

### Counterexample to `W` as supplied-evidence or physical-work bound

One LOCAL record can contain `L` redundant NOT-NOT pairs on input `x`, with root still `x`. It costs one paid node for every `L`, while supplied JSON payload grows linearly. At 512 pairs the test payload is 41,584 bytes; its exact canonical truth-table root is 47 bytes. Therefore

- supplied proof bytes, acquisition and evaluation are not bounded by paid-node cost `W`;
- nevertheless this family is **not** a lower bound on the shortest canonical certificate, because its root compresses to two truth bits.

The correct normalizer time is at least `Omega(E)` to read an `E`-bit supplied proof and is `O(E + poly(N+q))` for the explicit construction. Buffered output uses polynomial space in `N+q`; streaming can reduce live output storage but does not erase reads or writes. These are not FLMV exponents or a native-machine measurement.

### Implicit-proof firewall and B3

Krajíček's construction makes the key distinction exact: a polynomial circuit describing exponentially many proof lines defines the stronger system `iP`. It is not automatically a short `P` proof. LSPV-1/414's canonical implicit Resolution tree likewise needs a global UNSAT-validity check or an additional correctness proof. Neither is a native `/341` rule.

The canonical-balance theorem removes one possible loophole: for the literal semantic closure, a polynomial `Wbar` would also give polynomial certificate **bytes**. It does not prove B3. From `SAT in P` one gets `NP=coNP` and therefore the existence of some polynomially bounded Cook--Reckhow system. Cook--Reckhow Proposition 1.6 transfers that bound to this fixed calculus only after a polynomial-time p-simulation into it. That p-simulation/reflection compiler is precisely the missing theorem. A rejecting trace, an implicit exponential tree, or an axiom asserting the decider's correctness does not supply it.

Therefore same-`R_mix341` B3 remains **OPEN**, now with a sharper surviving obligation:

> Prove that the literal paid-node/root-only mixed calculus p-simulates the polynomially bounded system supplied under `SAT in P`, or prove polynomial uniform reflection for that system inside this exact calculus, without assuming the certificate bound or reflection statement being sought.

Haken PHP remains an ordinary shared-DAG Resolution lower bound, not a mixed-system or machine lower bound. Cook ER PHP, the `/341` linear Tseitin GF(2) proof, and REFEREE358's no-GF(2)-erasure theorem remain mandatory shortcut controls.

## Verification

Producer: `experiments/arc/lspv5_359/native_closure_balance_referee359.py`.

- 2,178 assertions;
- all 256 ternary truth tables over all eight inputs;
- all sixteen two-input DEF functions and unique extension checks;
- seven redundant LOCAL payloads through 1,024 gates;
- six node/wire reference controls;
- canonical mixed records through `q=128`;
- SAT source with two models, UNSAT source with zero, and five malformed controls.

Independent no-import JavaScript verifier: 2,152 checks, PASS. At `q=128`, canonical JSON is 14,081 bytes versus the deliberately coarse polynomial bound 442,368,000. Finite checks validate the implementation, not asymptotic proof-complexity claims or physical runtime.

## Precise status

- **PROVED/EXACT:** literal enumerated-rule closure does not export LOCAL internal wires for free.
- **PROVED/RESTRICTED:** polynomial semantic canonical encoding for paid-node roots and constant-many fixed facets, preserving GF(2), positional DEF inputs, source authentication and consumers.
- **PROVED countercontrol:** supplied payload bytes and actual reading/checking work are not bounded by paid-node count.
- **ABSENT, not silently repaired:** authoritative byte parser and selector serialization in `/341`.
- **OPEN:** full checker-level translation for a frozen parser; same-fixed-system B1/B2/B3; superpolynomial mixed minimum; P versus NP.

## Next exact step

Freeze—not infer—a finite-alphabet record grammar for DEF facets, GF(2) row selectors and LOCAL root references that implements the literal closure above. Then replay this canonicalizer byte-for-byte and prove polynomial verification. Separately attack the p-simulation/reflection obligation; do not substitute implicit proof validity or presumed decider correctness.

