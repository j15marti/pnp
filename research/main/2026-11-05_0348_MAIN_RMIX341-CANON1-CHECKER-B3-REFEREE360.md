# REFEREE360 — `Rmix341-CANON1` exact checker, normalization, and B3 firewall

**LSPV-5 Independent Proof Red Team — November 5, 2026, 03:48 PST**  
**Status:** PROVED/EXACT for the proposed finite-alphabet root-only/fixed-facet completion; PROVED polynomial normalization from the literal semantic closure into that completion; the historical `/341` byte language remains underdetermined; same-fixed-calculus B3 remains OPEN. **P versus NP OPEN.**

No task, schedule, enabled state, semantic inference rule, or paid-node weight is changed. No other role's manuscript region is edited.

## IDEA before search

Hypothesis: the last grammar gap can be removed without strengthening the calculus by freezing one finite-alphabet serialization in which every reusable object is either a paid node root or one of four fixed facets of a paid DEF. Prediction: a polynomial checker will accept the native odd-Tseitin `4h-1` proof and a one-step Resolution proof, while rejecting an internal-wire selector, false affine annotation, wrong GF(2) sum, bad DEF facet, forward reference, wrong source hash, malformed JSON and SAT/even-parity controls. If an unbounded selector or semantic-validity oracle is needed, the hypothesis is false.

Registered B3 falsifiers were: (i) a transition trace whose final reject bit is treated as a proof; (ii) an axiom asserting correctness/reflection for the assumed decider; (iii) a per-instance or per-length nonuniform minimum-proof selector; and (iv) an implicit exponentially long proof accepted without a native proof of its global validity.

## SEARCH

### Project, issue #3, Grok and Claude

Read first `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (blob `c3889a3e`), the original fixed calculus `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11`), REFEREE359, and issue #3 through LSPV-4/411. Material peer findings:

- LSPV-3/420 proves typed gauge covariance for the five semantic rules but still reports the byte parser absent; it also gives the exact ordinary-Resolution B3 meta-barrier.
- LSPV-3/419 proves sparse affine lineage for the unambiguous AND3/GF(2) sub-DAG.
- LSPV-2/414 proves semantic support recognition coNP-complete even for paid DEF networks; under `SAT in P`, SAT-miter queries can find support, but do not emit a native mixed refutation.
- LSPV-4/409 and /411 distinguish compact logical DAGs and SAT-miter acquisition from actual evidence scheduling and native proof production.
- LSPV-1/415 shows recognition of sound clocked SAT programs is arithmetically hard; this defeats a blanket program-correctness oracle, but does not itself refute B3 for one specially structured assumed decider.

Read actual `GROKPROOF/2026-11-05_1218_PROGRESS.md` (blob `d3183283`) and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (`1f9fc727`) and `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (`9a5b05d6`). They give restricted circuit/time-space arguments, not an exact `/341` checker or a same-system B3 compiler.

### Primary literature and repositories

Actual indexed-web queries:

1. `Haken 1985 intractability of resolution pigeonhole principle exponential lower bound primary paper PDF`;
2. `Gocht Nordstrom Certifying parity reasoning efficiently using pseudo-Boolean proofs primary paper PDF`;
3. `Krajicek implicit proofs exponential proof circuit represented primary paper`;
4. `Cook Reckhow relative efficiency propositional proof systems p simulation polynomial bounded primary`;
5. `LRAT exact syntax clause IDs hints verified checker`;
6. `extended resolution proof format extension instruction syntax`.

Sources actually read:

- Haken, *The Intractability of Resolution*, TCS 39 (1985), DOI `10.1016/0304-3975(85)90144-6`: the lower bound is for ordinary Resolution on PHP encodings; the abstract explicitly contrasts polynomial Extended Resolution PHP proofs.
- Cook--Reckhow, *The Relative Efficiency of Propositional Proof Systems*, Definition 1.5 and Proposition 1.6: polynomial boundedness transfers to a fixed target only through a polynomial proof translation/p-simulation.
- Reckhow, *On the Lengths of Proofs*, chapters 3--4: a verification system has a finite encoding and polynomial verification; `NP=coNP` yields some polynomially bounded system, not every named calculus.
- Krajíček, *Implicit Proofs*, ECCC TR03-055: circuit descriptions of exponentially long proofs define a possibly stronger system `iP`.
- Gocht--Nordström, *Certifying Parity Reasoning Efficiently Using Pseudo-Boolean Proofs* (AAAI 2021): concise XOR logging is obtained in a PB system with extension variables; this is a control, not a translation into arbitrary Resolution or into an unspecified `/341` parser.
- Cruz-Filipe et al., *Efficient Certified RAT Verification*, and Tan--Heule--Myreen, *Verified LRAT and LPR Proof Checking*: exact IDs, sorted clauses, hints and parser restrictions are part of a checkable proof format; they are not cosmetic.

Direct Google-branded search was unavailable. General indexed web search was used and is not represented as a Google search. The Gocht--Nordström journal page returned an access-denied page; the author-hosted paper and indexed publication record were read instead.

Authenticated `github.com/openai` queries were `LRAT proof checker certificate bytes`, `ExecCNFNodeSearchCosts`, and `parity XOR proof checker`. The first returned no result. The second found and the full prior audit read `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` (current search commit `4eaee875...`; prior content blob `1ced21f4`), which charges actual traces, visitation and storage. The parity query found no applicable proof checker. Code search is implementation evidence, not a mathematical theorem.

## ITERATE

### 1. Exact proposed grammar

`Rmix341-CANON1` is ASCII JSON with duplicate keys rejected. The document has exactly five fields: format tag, canonical source CNF, SHA-256 of the canonical source object, a topologically ordered paid-node list, and a final typed reference. Original variables are integers `1..n`; fresh DEF variables are assigned consecutively. Clauses and GF(2) masks are sorted and duplicate-free.

References are only:

- `{"src":i,"view":"clause"}`; or
- `{"node":i,"view":kind}`; or
- `{"node":i,"view":"clause","facet":j}` for a DEF facet `j in {0,1,2,3}`.

The keys `wire` and `selector` are illegal. Thus no LOCAL internal gate is exported.

Each record is exactly one paid node:

| Rule | Exact record semantics |
|---|---|
| RES | two earlier clause views, explicit pivot and the exact non-tautological resolvent |
| AND3 | two clause/factor views whose union has at most three original variables; exact conjunction truth table; optional affine view accepted only after equality on all at most eight rows |
| GF2 | two earlier affine views and their exact symmetric-difference mask/XOR RHS |
| LOCAL | one earlier relation and one clause or factor implied on every valuation of at most three original variables |
| DEF | next fresh variable, two earlier variables and one four-bit binary truth table; four fixed clauses exclude the unique wrong output for each input row |

Contradiction is exactly an empty clause, `0=1`, or an all-zero factor. Source clauses are free; every listed record has the unchanged unit paid weight.

This is a **proposed exact completion** of the literal `/341` semantics. It is not historically authoritative: `/341` never chose JSON, duplicate-key behavior, a DEF facet byte, or a final-reference syntax. Hence the requested pre-existing “exact native byte grammar” has no unique answer. The counterexample to uniqueness is minimal: `/341` does not decide whether the legal semantic facet of a paid DEF is named by `(node,facet)`, expanded as a clause root, or unavailable. These completions have different accepted strings while implementing the same prose rules. `CANON1` chooses the first and explicitly freezes it.

### 2. Checker soundness

**Theorem.** If the `CANON1` checker accepts `(F,pi)`, then `F` is UNSAT.

**Proof.** Induct over paid nodes. Source views are clauses of the authenticated source. RES emits the exact resolvent. AND3 emits the exact conjunction of its parents, and an affine view only after extensional equality. GF2 adds two valid equations over GF(2). LOCAL emits only a relation implied by its parent on the complete constant support. A DEF adds the graph of a Boolean function; its four facets are exactly the clauses excluding `(a,b,z != f(a,b))`. Every assignment to the previous variables has a unique extension to the fresh variable, so the topologically ordered DEF bank is conservative. Therefore every exposed view is entailed by the source plus conservative definitions. An accepted final contradiction has no satisfying extension, and conservativity implies that the original source has no model. ∎

**Verification time.** For an `E`-byte canonical certificate, parsing/hashing and source authentication cost `O(E)` byte access. Sortedness checks, clause Resolution, mask addition and dictionary lookup are polynomial; AND3/LOCAL enumerate at most eight rows. The implementation has a coarse deterministic `O(E^2)` bit-time upper bound and `O(E)` resident representation bound; ordinary RAM hashing/sorting is faster but is not promoted to a fixed-tape theorem. Certificate construction, reads, writes, allocation, output, and peak storage remain physical costs separate from `W`.

### 3. Full semantic-to-exact normalization for the frozen completion

**Theorem.** Let `pi` be a valid `q`-node proof in the literal paid-node/root-only semantic closure audited in REFEREE359, from an `N`-bit source with `n` original variables. If DEF consumers use one of the four fixed relation facets, then `pi` translates rule-for-rule into `CANON1`, preserving the source, DAG, rule types and paid cost, with

`|CANON1(F,pi)| = O(N + q(n+q) log(n+q))`.

**Proof.** Hash the canonical original source; topologically alpha-rename paid nodes and at most `q` fresh DEF variables. A clause or affine row names at most `n+q` variables; an AND3/LOCAL relation has at most eight truth bits; a DEF has two earlier names, four truth bits, and a constant facet index. Serialize each original semantic root exactly and retain each parent edge. The checker conditions are precisely the rule side conditions, so induction gives acceptance. Summing the records gives the bound. The transformation is polynomial in the supplied semantic proof plus its output; an arbitrarily bloated supplied LOCAL payload still costs `Omega(E)` to read but normalizes to its constant truth table. ∎

This closes the polynomial **normalization/translation** theorem for the frozen root-only/fixed-facet completion. It does not retroactively make `CANON1` the unique historical parser, nor does it cover an unlisted free exported-wire rule.

### 4. Executable hostile controls

The producer generated the K4 odd Tseitin CNF with four degree-three equations and odd total charge. Each vertex uses three AND3 nodes to conjoin its four CNF clauses and authenticate the affine row; three GF2 nodes add the four rows. The accepted proof therefore has exactly `12+3=15=4h-1` paid nodes, 2,614 canonical bytes, 31 typed references and 128 enumerated truth assignments. An independent JavaScript implementation replayed 309 conditions and obtained the same final `0=1` and source hash.

Accepted controls: odd K4 Tseitin, one-step `(x),(not x)` Resolution, and one-step LOCAL conversion from an original empty clause to a false factor. A three-node legal DEF-facet/Resolution prefix is checked and then rejected only because it is not a refutation.

Rejected controls:

- even-charge K4 trace ending in `0=0`;
- a SAT source with no contradiction;
- wrong source hash, forward reference and duplicate JSON key;
- private `wire` selector and facet 4;
- nonfresh DEF, false LOCAL implication, corrupt AND3 table, false affine annotation, wrong GF2 sum and noncanonical source clause.

These finite controls validate the checker implementation, not asymptotic proof hardness or machine runtime.

### 5. B3 attack: exact obstruction remains p-simulation/reflection

`CANON1` removes the payload/byte-balance escape. It does not turn a polynomial SAT decider into a native refutation producer.

Assume `SAT in P` via a fixed uniform correct decider `A`. Then `NP=coNP`, so Cook--Reckhow gives **some** polynomially bounded proof system `P_A`. To conclude `Wbar_Rmix341` polynomial one must still prove one of:

1. a polynomial-size simulation of every `P_A` proof by the same fixed `R_mix341`; or
2. a native polynomial proof of the relevant bounded reflection/correctness statements plus a polynomial compilation of rejecting computations.

Neither follows from the one-bit answer or transition legality. The minimal trace-only countercontrol is a machine that immediately prints UNSAT: its one-step transition trace is locally valid on both the UNSAT source `(x)&(not x)` and the SAT source `(x)`. Any rule mapping the first trace to contradiction from transition legality alone also maps the SAT trace and is unsound. Adding “`A` is correct” as an axiom is circular and not one of the five native rules. Selecting a minimum proof after seeing each input establishes existence only if a polynomial bound is already known; it is a nonuniform optimizer, not a B3 derivation.

Haken's theorem starts from a certified hard family but only proves superpolynomial ordinary-Resolution length. Indeed, because ordinary Resolution is unconditionally not polynomially bounded, its own statement `SAT in P => Wbar_Res polynomial` is equivalent to `P != NP`; it cannot serve as an easier black-box bridge. Cook's Extended Resolution PHP proofs and the native K4/Tseitin GF(2) proof show why restricted lower bounds do not transfer to this mixed system. Gocht--Nordström shows another concise parity certificate in a different stronger format. None supplies the missing arbitrary-decider compiler.

Therefore:

- **FALSIFIED:** trace-only, correctness-axiom, hidden semantic-oracle, nonuniform-minimizer, and implicit-proof-without-validity candidate bridges.
- **OPEN:** existence of a noncircular same-`R_mix341` B3 theorem. This run neither proves nor refutes B3 itself.

## Exact status and next obligation

- **PROVED/EXACT:** sound polynomial checker for `Rmix341-CANON1`.
- **PROVED/EXACT:** rule-for-rule, source-authenticated, cost-preserving polynomial normalization from the literal root-only/fixed-facet semantic closure into `CANON1`.
- **PROVED documentation fact:** historical `/341` does not determine a unique byte language; `CANON1` is a conservative proposed freeze, not a discovered pre-existing parser.
- **PROVED hostile controls:** 15-node odd Tseitin proof; even/SAT/malformed/wire/facet/LOCAL/AND3/GF2 rejections; independent 309-check replay.
- **OPEN:** p-simulation/reflection into the same fixed calculus; B1, B2, B3; superpolynomial `Wbar_Rmix341`; P versus NP.

Next: either adopt a normative serialization such as `CANON1` (after peer audit of the DEF-facet convention), or give a different exact parser and polynomial mutual translation. Independently, attack a specifically stated `P_A -> R_mix341` compiler; further balance proofs cannot fill the B3 gap.

## Artifacts

- `experiments/arc/lspv5_360/rmix341_canon1_referee360.py`
- `experiments/arc/lspv5_360/verify_rmix341_canon1_referee360.mjs`
- `results/raw/arc/2026-11-05_0348_LSPV5_REFEREE360_raw.json`
- `research/coordination/2026-11-05_0348_LSPV5_RMIX341_CANON1_REFEREE360_HANDOFF.md`
