# REFEREE349 — native root normalization and trace-only B3 firewall

**PNP Independent Proof Red Team | November 4, 2026, 17:48 PST**  
**Status:** PROVED/EXACT for the strict root-only typed serialization of the already fixed `R_mix341` rules; PROVED minimal counterexample to uncharged internal-wire assertion export; PROVED general trace-only barrier for sound refutation systems; COMPUTATIONAL finite controls. B1/B2/B3, superpolynomial `Wbar_Rmix341`, unrestricted SAT hardness, and P versus NP remain OPEN.

## IDEA before search

The initial hypothesis joined the two immediate deliverables:

> A full native normalization is sound only if every reusable wire has source-rooted typed ancestry, while a rejecting machine trace yields an `R_mix341` refutation only after a separate same-system reflection proof of the decider's correctness.

The falsifiable prediction was a dichotomy. Either the authoritative `LOCAL-CONVERT` grammar licenses independently consumable internal wires, in which case a smallest SAT counterexample should exist, or it derives only the circuit's root condition, in which case the circuit can be replaced by its constant-support truth table and all reusable wires must be separately paid fresh DEFs. In both cases, a locally valid reject trace alone should fail on a reject-all machine.

Registered falsifiers:

1. a root-only record may still require superpolynomial encoded evidence relative to `N+q`;
2. an internal circuit wire may be safely consumed as a true assertion merely because the circuit root is implied;
3. a fresh exact DEF relation may accidentally assert that its output is true;
4. local validation of a total polynomial rejecting trace may suffice without a correctness/reflection premise.

## SEARCH

### Governing project and exact native text

Read first the governing five-role handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, then issue #3 through LSPV-3/406 and the latest peer reports. The authoritative rule source is:

- `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`.

It declares free exact-source clause leaves, unit-weight derived records with at most two parents, RES, original-support-at-most-three AND3 truth tables, GF(2) XOR, unary constant-support truth-table-checked `LOCAL-CONVERT`, and fresh conservative two-input paid DEF. It says a `LOCAL-CONVERT` node derives **a clause or bounded-support Boolean circuit condition**. It gives no operation for naming or consuming an internal circuit gate. By contrast, it explicitly says later uses of a DEF reference its charged node. Therefore the strict native reading has one exported result per `LOCAL-CONVERT` record: its root condition. An internal reusable wire is not a native conclusion and must be introduced by paid fresh DEF.

Also read:

- `research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md`, blob `bbcdad9a...`;
- `research/agents/lspv-4/2026-11-03_0736_LSPV-4_LOCAL_CONVERT_CVP_GATE_TRACE363.md`, blob `7192adc3...`;
- `research/agents/lspv-3/2026-11-04_1724_LSPV-3_PORT_COHERENCE_GRAMMAR406.md`, blob `4d2abf92...`;
- REFEREE341–348 and current LSPV-1/403–404, LSPV-2/403–404, LSPV-3/404–406, LSPV-4/398.

LSPV-3/406 proved freshness/model coherence but left the circuit-port grammar unresolved. This run resolves the semantic question without changing the rule set: internal gates are private representation syntax because the fixed rule never exports them; public reusable values are exactly the separately paid DEF conclusions. The separate circuit-valued interpretation U from LSPV-4/363 remains useful for raw verification-cost controls, but U's internal gates are not public native proof conclusions.

### Grok and Claude

Actually read:

- `GROKPROOF/2026-11-04_2315_PROGRESS.md`, blob `f5b8ef62d441e5ea6cf5d28ed1df74cfd0474884`;
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`;
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

Grok's white-box residual extraction and implementation certificates remain open. Claude's portfolio and one-tape results are restricted machine theorems. None supplies native `R_mix341` reflection or B3.

### Primary literature and actual queries

Actual general-web queries:

- `site:cs.toronto.edu Cook Reckhow propositional proof systems p simulation PDF`;
- `feasible reflection principles proof complexity p-optimal proof systems primary paper PDF`;
- `Extended Frege reflection principle machine computation trace correctness proof complexity primary`;
- `Res XOR Tseitin formulas polynomial refutation Gaussian elimination proof complexity primary paper`.

Sources read:

- Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems* (JSL 1979), author PDF: a proof system requires a fixed effective verifier/map; p-simulation is a uniform proof translator preserving the proved formula.
- Cook and Nguyen, *Logical Foundations of Proof Complexity*, reflection-principle chapter: soundness/reflection of a proof system is a separate formal principle.
- Soltys, *Extended Frege and Gaussian Elimination* (2002): even a polynomial algorithm such as Gaussian elimination receives an explicit feasible correctness proof; polynomial runtime alone is not substituted for reflection.
- Khaniki, ECCC TR20-034: Res(PC)/Res(XOR)-type lower bounds are stated for exact algebraic proof models and characteristics, not arbitrary SAT machines.

Haken's established anchor remains exact and restricted: there exist `c>0,h0` such that for every `h>=h0` and every ordinary shared-DAG Resolution refutation of the explicit unary `PHP_(h+1)^h` CNF, the proof has at least `2^(ch)` lines. Source axioms plus binary resolvents are allowed; extension definitions, GF(2), AND3, `LOCAL-CONVERT`, and arbitrary machine steps are not. Cook's Extended Resolution PHP proofs and the native XOR shortcut on odd Tseitin are mandatory countercontrols.

Direct Google-branded search was unavailable. General web search was used; no Google-specific search is claimed.

### OpenAI GitHub

Actual `github.com/openai` queries:

- `reflection proof verifier machine trace correctness`;
- `LOCAL CONVERT exported wire circuit verifier`;
- `SAT implementation certificates runtime assembly`;
- `GF2 Gaussian elimination proof certificate Lean`.

The first, second and fourth returned no applicable result. The third found `openai/math/lean/OAI/Algorithms/SubexponentialSAT/RuntimeAssembly.lean`, which explicitly calls `ImplementationCertificates` open obligations. This is an implementation safeguard, not a theorem that traces imply `R_mix341` refutations.

## ITERATE I: exact strict-native normalization

### Typed serialization forced by the fixed rules

Use the following serialization of the already declared semantics; it adds no rule and changes no weight.

1. A source leaf contains an exact source-clause index.
2. Every paid record contains its rule tag and at most two earlier record/source identifiers.
3. RES contains the normalized parent clauses, named pivot and normalized resolvent.
4. AND3 contains an explicit declared list of at most three original variables and its at-most-eight-bit truth table. All referenced conditions are checked to use only that declared syntactic support.
5. XOR contains an explicit affine variable mask and RHS.
6. `LOCAL-CONVERT` contains a declared support list of size at most the fixed calculus constant `c_R` and the root truth table. A supplied circuit payload may be checked, then discarded; its internal gates are not identifiers visible to later nodes.
7. DEF contains one globally fresh output identifier, two earlier signed inputs and one of the finitely many two-input Boolean gate tables. Its exact conservative relation is attributed to that paid node. A later use references the DEF record.

The declared support is syntactic/authenticated, not an unproved semantic-essentiality oracle. Hidden references outside the list, duplicate fresh IDs, forward references, cycles, malformed masks and malformed source strings are rejected.

### Theorem 349A — polynomial original-source typed normalization

Let `pi` be any legal `q`-node `R_mix341` refutation of an explicit CNF source `F` of bit length `N`, under the strict native reading above. There is a uniform original-source-preserving typed encoding `Norm(F,pi)` of length polynomial in `N+q`, constructible and checkable in polynomial bit time. It changes neither the proof DAG nor its paid-node cost.

#### Proof

Let `n0<=N` be the original variable count. Every DEF introduces one fresh variable, so at every point there are at most

`V = n0+q <= N+q`

available variables. Normalize every clause as a sorted non-tautological literal set; it has at most `2V` literals and polynomial encoded length. An affine row is a `V`-bit mask plus one RHS bit. AND3 has at most eight semantic bits. A `LOCAL-CONVERT` root has at most `2^c_R` semantic bits, a constant because `c_R` is fixed independently of the source and proof. A DEF has constant gate code plus `O(log V)` identifiers. Parent and source references use `O(log(N+q))` bits.

Consequently a deliberately loose total bound is

`N + q*O(V log(V+2) + 2^c_R + log(q+2)) = (N+q)^{O(1)}`.

RES is checked by literal-set scans, AND3 and `LOCAL-CONVERT` by exhaustive fixed truth tables, XOR by mask addition, and DEF by freshness, topological order and its constant gate relation. The root ancestry authenticates exact source indices; unused records may be discarded. A materialized compiler/checker uses polynomial time and polynomial peak space. A read-only repeated-rescan checker can instead use logarithmic indices plus current literal/mask bits and polynomial time; every source/proof read and head/index update remains charged. Construction, serialization and output are not free. QED.

This is a node-to-bit normalization theorem for proofs already rooted in the original source, not a proof-search theorem and not an evaluator-to-original source-retraction theorem. It says a polynomial `W_R` bound would correspond to polynomial evidence; it neither establishes that bound nor translates a proof whose axioms are a transformed evaluator CNF back to `F`.

### Theorem 349B — minimal uncharged internal-wire counterexample

Take the satisfiable source `(x)`. Let a one-input circuit have gates

`g0=x, g1=NOT g0, g2=NOT g1`,

with root `g2=x`. The parent condition `x` implies the root, so the root-only `LOCAL-CONVERT` is legal. But the internal wire `g1=NOT x` is not implied by `x`; treating `g1` as an asserted true condition yields `(x) AND (NOT x)` and a false refutation of a SAT source.

Therefore no sound completion can make arbitrary internal gates free asserted exports. There are exactly two sound choices compatible with the fixed system:

- keep internal gates private and export only the root; or
- expose a reusable wire as a separately paid, globally fresh exact DEF relation, which does not assert that the wire is true.

The first is the strict native `LOCAL-CONVERT` reading; the second is already the native DEF rule. An uncharged third category is illegal.

## ITERATE II: noncircular B3 audit

### Theorem 349C — rejecting traces alone cannot yield sound refutations

Let `R` be any sound CNF refutation system, including `R_mix341`. There is no compiler `C` with the following trace-only specification:

> for every total polynomial-time machine `M`, CNF `F`, and locally valid computation trace in which `M(F)` outputs UNSAT, `C(M,F,trace)` is an `R` refutation of `F`.

#### Proof

Choose the total constant-time machine `M_reject` that outputs UNSAT on every syntactically valid input. On the satisfiable source `(x)`, its start-to-reject trace is locally valid. The promised compiler would output an `R` refutation of `(x)`, contradicting soundness. Malformed rejection does not help because `(x)` is valid. QED.

The theorem still holds when trace construction, code acquisition, every transition, output and verification are fully charged. It refutes a trace-only B3 proof, not B3 itself.

Under the assumption `SAT in P`, one may choose a fixed correct polynomial decider `A`. Its correctness is a true external mathematical fact, but local trace checking proves only that `A(F)` rejected. To turn that rejection into a derivation in the same fixed calculus, a proposed route must additionally prove one of:

1. polynomial `R_mix341` reflection/correctness proofs for `A` plus a polynomial source-retraction compiler; or
2. a different direct family-wide construction of polynomial `R_mix341` refutations for all UNSAT sources.

Assuming item 1 is not a noncircular proof of B3: it is precisely the missing polynomial-certificate/reflection obligation. Cook–Reckhow gives some polynomially bounded proof system under NP=coNP, not polynomial boundedness of this preselected `R_mix341`. No project, Grok, Claude, literature or OpenAI-GitHub source read here supplies the missing same-system reflection theorem.

## Verification and iteration failures

Producer:

`experiments/arc/lspv5_349/native_root_normalization_b3_referee349.py`

Independent JavaScript checker:

`experiments/arc/lspv5_349/verify_native_root_normalization_b3_referee349.js`

Raw ledger:

`results/raw/arc/2026-11-04_1748_LSPV5_349_NATIVE_ROOT_NORMALIZATION_B3.json`

The initial plan attempted to normalize public internal ports. Search falsified that premise: no such native export rule exists, and LSPV-3/406 independently identified the gap. The iteration therefore split ports into private root syntax versus paid exact DEFs. The finite audit then tested the separating one-variable circuit directly.

Python producer: **1,807 checks**. Independent JavaScript: **1,200 checks**. Controls include 375 deterministic random circuits over one to three inputs, all truth-table rows, five native record shapes, six malformed native records, fresh exact-definition semantics, SAT/UNSAT unit sources, five malformed sources, and correct versus reject-all traces. Raw SHA-256:

`cd9758f2a3507975e13ba81afaad51f0209446830d3d66a2142e88c2611f8a2d`.

Finite execution corroborates the explicit constructions; it does not prove B3 or an asymptotic lower bound.

## Exact classification

- **PROVED/EXACT:** polynomial node-to-bit typed normalization for proofs already authenticated to the original source, under the strict root-only serialization of every native rule already named in `R_mix341`.
- **PROVED/EXACT:** arbitrary internal circuit wires cannot be consumed as free true assertions; reusable wires require paid fresh exact DEF.
- **PROVED/EXACT:** local rejecting traces of arbitrary total polynomial machines do not soundly compile to refutations.
- **COMPUTATIONAL:** finite circuit, native-record, malformed, SAT/UNSAT and trace controls.
- **NOT PROVED:** retraction from an arbitrary transformed/evaluator source to the original CNF; a compiler from a hypothetical correct SAT decider to `R_mix341` proofs; polynomial same-system reflection; B1, B2 or B3; a superpolynomial `Wbar_Rmix341`; unrestricted SAT hardness; P versus NP.

## Exact next step

The grammar-side ambiguity is removed by the strict rule closure: `LOCAL-CONVERT` exports one root condition; public values are paid DEFs. The remaining decisive obligation is no longer raw serialization. It is semantic reflection:

> prove, from `SAT in P` without presupposing polynomial certificates, that every UNSAT source has a polynomial `R_mix341` proof; or exhibit a logically independent reason this fixed calculus p-simulates an appropriate polynomially bounded proof system.

Reject traces, recognizers, Haken Resolution hardness, Cook ER shortcuts and Tseitin XOR shortcuts do not supply that arrow. No task, schedule, enabled state, role, rule or weight was changed.
