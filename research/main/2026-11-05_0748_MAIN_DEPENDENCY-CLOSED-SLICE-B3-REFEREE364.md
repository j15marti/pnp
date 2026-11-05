# REFEREE364 — dependency-closed mixed-proof slicing and the residual B3 gap

**LSPV-5 Independent Proof Red Team — November 5, 2026, 07:48 PST**  
**Status:** reference-only proof slicing **FALSIFIED** by a legal seven-node CANON2 proof; dependency-plus-owner closure with order-preserving alpha-renaming **PROVED/RESTRICTED** for frozen source-authenticated CANON2R; same-\(R_{\mathrm{mix341}}\) B3 **OPEN**. P versus NP **OPEN**.

## IDEA

Before searching, I proposed:

> Delete every node outside the ordinary backward reference ancestry of the final contradiction, compact node identifiers, alpha-rename the surviving paid definitions, and replay the result.

Assumptions: REFEREE361's sound CANON2 rules, REFEREE362's exact raw-source wrapper, REFEREE363's arbitrary-precision integer semantics and node-to-bit bound. Falsifiable prediction: this naïve normalizer fails when a later DEF consumes an earlier auxiliary only through its numeric input field rather than an explicit proof reference. The proposed repair was to close the slice under both:

1. explicit proof-parent edges; and
2. auxiliary-owner edges from every mentioned fresh identifier to its unique paid DEF node.

For B3, the falsifiable prediction was that even the repaired normalizer is only proof-to-proof postprocessing: it cannot construct the first short native proof from a decider's reject bit or trace.

## SEARCH

### Governing, issue, peer, Grok and Claude material

Read first:

- research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, blob c3889a3e514ddbd747150dcb68607013a3b2d154;
- issue #3 through LSPV-1/419, LSPV-2/418, LSPV-3/424, LSPV-4/414 and REFEREE363;
- original /341, CANON2/361, CANON2R/362, and REFEREE363;
- the full LSPV-1/419 report on branch research/lspv1-419-one-sided-reflection, blob 3d231e11;
- LSPV-2/418 clause-to-LOCAL adapter, blob 47a9b20;
- LSPV-3/424 high-width GF(2) factor obstruction, blob 8aa955a3.

Independent assessment:

- LSPV-1/419 gives a valid-looking **conditional** route if one fixed P-time decider has one-sided rejection soundness formally proved in a suitable feasible theory and the native ER facets exist. Bare SAT in P does not provide that reflection proof. The condition therefore does not meet the requested B3 without formalized decider correctness.
- LSPV-2/418 repairs a conditional clause-parent LOCAL typing mismatch with a paid AND3 adapter. It does not adjudicate the historical grammar.
- LSPV-3/424 correctly blocks high-width affine erasure into only bounded original-variable factors. A general normalizer must retain sparse GF(2) types or use paid auxiliaries; the present theorem retains them.
- LSPV-4/414's exact raw-acquisition lower bound remains authentication cost only.

Actual external assessments read:

- GROKPROOF/2026-11-05_1218_PROGRESS.md, blob d3183283d6869f92617c0c758c9d31d1a201c32f: universal fully charged transformation open.
- research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67: restricted portfolio/alternation theorem, not B3.
- research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex, blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a: sequential-access result, not the random-access mixed-proof bridge.

### Literature and GitHub searches

Actual indexed-web queries:

- extended resolution proof unused extension variables renaming proof trimming dependency graph primary paper
- DRAT proof trimming backward core dependencies proof checker paper
- Cook Reckhow reflection principle proof systems p simulation extended Frege primary literature
- extended Frege extended resolution polynomial equivalence proof systems

Actual GitHub queries:

- github.com/openai: proof dependency graph trim unused nodes certificate SAT resolution — no result;
- j15marti/pnp: dependency closed slicing alpha renaming DEF auxiliary proof — no result;
- j15marti/pnp: formal reflection B3 PV1 decider soundness — found earlier LSPV-1 reflection work and the precise remaining implication.

Useful sources:

- Wetzler--Heule--Hunt, DRAT-trim (SAT 2014), uses backward checking to mark necessary clause dependencies and can emit optimized proof subsets. This motivates slicing but does not cover hidden extension-variable ownership in this grammar.
- Cook--Reckhow (JSL 1979) treats proof length, p-simulation and extension abbreviations; extension variables must remain correctly defined.
- Standard proof-complexity surveys state Extended Resolution and Extended Frege p-simulate one another. This strengthens the need to preserve definitions rather than erase them.
- DRAT supports extended-resolution-like variable additions; practical trimming tracks stronger dependencies than a bare Resolution edge graph.

Direct Google-branded search was unavailable. Indexed web and authenticated GitHub search were used; no direct-Google claim is made.

## ITERATE

### 1. Seven-node legal counterexample to reference-only slicing

Take authenticated source

\[
F=(x)\wedge(\neg x).
\]

This source is deliberately easy; the example tests certificate normalization, not hardness or minimum cost.

Use two paid definitions:

\[
z:=0,\qquad w:=f(z,x)=x,
\]

where the second gate's four-row truth table is \([0,0,1,1]\): it ignores its first positional input but still names \(z\). From the four exported facets of \(w\):

1. resolve facets 1 and 3 on \(z\) to obtain \(\neg x\lor w\);
2. resolve with source \(x\) to obtain \(w\);
3. resolve facets 0 and 2 on \(z\) to obtain \(x\lor\neg w\);
4. resolve with source \(\neg x\) to obtain \(\neg w\);
5. resolve \(w,\neg w\) to contradiction.

The actual CANON2 checker accepts all seven paid nodes.

Ordinary proof-reference ancestry contains the second DEF and five RES nodes, but not the first DEF: the edge \(w\to z\) occurs only in the numeric DEF input field. Deleting the first DEF and compacting the remaining fresh output maps \(w\) to identifier 2 while its unmapped input \(z\) is also 2. The result attempts to define a variable from itself; the actual checker rejects it as a bad DEF input.

Therefore:

**Theorem 364A.** Backward reachability using only explicit inference references is not a sound normalizer for CANON2/CANON2R.

This is an original-rule legal proof counterexample. It does not exploit malformed input, a semantic oracle, a free exported wire or a false inference.

### 2. Dependency-closed slicing and alpha-renaming theorem

For an accepted proof \(\pi\), define \(S\) as the least set of nodes satisfying:

1. the final node is in \(S\);
2. every explicitly referenced node of a node in \(S\) is in \(S\);
3. if a semantic field of a node in \(S\) mentions auxiliary identifier \(v>n\), the unique paid DEF owner of \(v\) is in \(S\).

The semantic fields include DEF outputs and ordered inputs; RES pivots and output literals; AND3 factor supports and optional affine masks; GF(2) masks; and LOCAL output supports. Source identifiers are fixed and need no owner.

**Theorem 364B (source-authenticated dependency slice).** Delete all nodes outside \(S\), preserve the remaining order, compact node IDs, and map the \(k\)-th surviving DEF output to \(n+k\). Apply that same injective order-preserving map to every auxiliary occurrence. Then:

- every retained rule remains legal and semantically identical up to alpha-renaming;
- the exact source object, source clause indices, raw source bytes and raw/source hashes are unchanged;
- the final result is still contradiction;
- paid nodes do not increase: \(q'\le q\);
- combined with Theorem 363A, canonical output length remains polynomial in source length and \(q\).

**Proof, rule by rule.**

- DEF freshness: closure retains the owner of every auxiliary input. Because owners precede consumers, order-preserving renaming maps every input below the fresh output. Ordered input positions, aliases and truth rows are unchanged.
- RES: an injective sign-preserving variable rename commutes with each oriented resolvent. Pivots and complementary nonpivot literals are preserved.
- AND3 and LOCAL: relation evaluation is invariant under an injective coordinate rename. In frozen CANON2 these supports are original-only, so the map is actually the identity there.
- GF(2): symmetric difference and RHS addition commute with a coordinate bijection. Frozen CANON2's affine firewall again makes the coordinate map identity.
- DEF facet selectors: facet number is indexed by the two ordered input bits, not the numeric variable names; it remains unchanged.
- DAG/source authentication: node references are reindexed, source references are untouched, and the final contradiction predicate is invariant under alpha-renaming.

This is a complete pruning/renaming theorem for already accepted CANON2R proofs. It does not translate disputed historical rule variants into CANON2R; the paid adapters from LSPV-2/417--418 and LSPV-3/423 address only stated interface cases.

### 3. Verification and independent challenge

The Python producer used the actual REFEREE361 CANON2 checker:

- hidden-owner chains of lengths \(2,3,10,50\);
- \(0,1,7\) genuinely dead trailing definitions in each case;
- 12 original certificates accepted;
- all 12 reference-only slices rejected as bad DEF inputs;
- all 12 dependency-closed/renamed certificates accepted;
- owner closure sizes exactly \(k+5\), while explicit ancestry stayed at 6;
- exact source object and source hash preserved;
- SAT same-sign control and three malformed controls rejected;
- 105 counted assertions after adding the full mixed fixture.

The full LSPV-2/416 certificate exercises DEF, RES, AND3, LOCAL and GF(2). After appending two dead definitions it had 19 nodes; dependency slicing returned the exact live 17-node mixed proof, preserved source authentication and passed the actual checker.

An independently written JavaScript DEF/RES checker repeated 38 checks across the chain family and rejected the SAT and malformed controls.

The family also refutes a proposed size invariant: constant explicit-reference ancestry does not bound dependency-closed proof size. With a chain of \(k\) owner definitions, explicit ancestry remains 6 but every valid ownership-closed slice has \(k+5\) nodes.

### 4. B3 iteration

Theorem 364B cannot close B3:

- its input is an already accepted \(R_{\mathrm{mix341}}\) proof;
- completeness supplies some proof for every UNSAT source but no polynomial size bound;
- owner closure can retain all \(q\) nodes, as the chain family demonstrates;
- a decider reject bit or locally valid computation trace supplies neither a native proof nor the missing semantic edge from rejection to UNSAT.

LSPV-1/419's one-sided feasible-reflection condition is a genuine **additional sufficient hypothesis**: a fixed formal proof of no false UNSAT rejection can translate to EF/ER and then to the native DEF/RES fragment if its facet grammar is available. It is not bare B3 because the requested implication

\[
\mathrm{SAT}\in P
\Longrightarrow
\text{one suitable P-time decider has feasible one-sided reflection}
\]

remains unproved. Treating that reflection theorem as an axiom would import precisely the formalized decider correctness excluded by the present user direction. The Gödel countercontrol blocks every-decider reflection in a fixed feasible theory, although B3 needs only one suitable decider and therefore is not refuted.

Thus the weakest noncircular same-system B3 transfer remains open.

## Exact status

| obligation | status |
|---|---|
| reference-only backward slice | **FALSIFIED** |
| owner-closed pruning and alpha-renaming | **PROVED/RESTRICTED for CANON2R** |
| source/raw authentication during slicing | **PRESERVED exactly** |
| high-width GF(2) erasure | **not attempted; prohibited by LSPV-3/424 control** |
| disputed historical LOCAL/AND3 ports | **OPEN outside stated adapters** |
| historical native /341 byte grammar | **OPEN** |
| same-\(R_{\mathrm{mix341}}\) B3 from bare SAT in P | **OPEN** |
| full-mixed superpolynomial \(\overline W_R\) | **OPEN** |
| P versus NP | **OPEN** |

Haken remains ordinary-Resolution PHP hardness only. Cook ER and Tseitin/GF(2) remain shortcut controls. No restricted proof lower bound is transferred to arbitrary SAT machines.

## Physical costs

For explicit evidence length \(E\):

- parsing and acquiring the supplied proof costs \(\Omega(E)\) bit access;
- a materialized owner/reference graph, closure set, maps and output use \(O(E)\) peak space;
- balanced-map construction, closure and rewriting take \(O(E\log(E+2))\) deterministic RAM work; hash maps give expected linear work;
- a rescan implementation can reduce writable space at polynomial time, as in the LSPV-4 verifier methodology;
- writing a materialized normalized proof costs \(\Omega(E')\), even though \(q'\le q\);
- proof discovery and choice of a minimum remain outside \(W_R\), while all actual construction/access/output costs remain separate.

No machine-runtime lower bound follows from owner-chain length or logical node count.

## Reproduction

- experiments/arc/lspv5_364/dependency_slice_referee364.py
- experiments/arc/lspv5_364/verify_dependency_slice_referee364.mjs
- results/raw/arc/2026-11-05_0748_LSPV5_REFEREE364_raw.json
- results/raw/arc/2026-11-05_0748_LSPV5_REFEREE364_independent.json

No task, schedule, role, enabled state, inference rule, logical weight or other role's manuscript region was changed.
