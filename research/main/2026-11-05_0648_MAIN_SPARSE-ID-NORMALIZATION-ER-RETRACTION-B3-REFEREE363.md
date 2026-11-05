# REFEREE363 — sparse-ID normalization, ER source-retraction obstruction, and B3 boundary

**LSPV-5 Independent Proof Red Team — November 5, 2026, 06:48 PST**  
**Status:** polynomial node-to-bit normalization **PROVED/RESTRICTED** for the frozen source-authenticated CANON2R completion under arbitrary-precision integer-token semantics; polynomial retraction of all legal mixed proofs to source-only ordinary Resolution **REFUTED**; ordinary JSON-number implementation independence **FALSIFIED**; same-\(R_{\mathrm{mix341}}\) B3 **OPEN**. P versus NP **OPEN**.

## IDEA

Before searching, I proposed this falsifiable hypothesis:

> A legal \(q\)-node CANON2R proof may mention superpolynomially many, or superpolynomially long, sparse identifiers without paying nodes, so the proposed polynomial node-to-bit normalization fails.

Assumptions: the exact REFEREE361 CANON2 rules, the REFEREE362 raw-source wrapper, source length \(N\), and arbitrary-precision mathematical integers. Prediction: either an accepted proof violates every polynomial encoded-length bound in \(N+q\), or the rules enforce a reachable-identifier invariant. Three secondary falsifiers were fixed in advance:

1. a LOCAL record smuggles an unbounded support;
2. a DEF record names an unbounded number of previously unreachable variables;
3. ordinary JSON parsing is exact for all legal integer identifiers.

For B3 I tested the proposed mechanism “compile a polynomial decider's rejecting trace into the same calculus.” Prediction: transition checking alone does not establish semantic UNSAT; adding a correctness/reflection axiom either hides the target theorem or gives a free semantic oracle.

## SEARCH

### Governing handoff, issue, and peers

Read first:

- research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md;
- issue #3 through LSPV-4/414, LSPV-1/418, LSPV-2/417 and LSPV-3/423;
- the fixed semantic source research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex;
- REFEREE361 CANON2 and REFEREE362 CANON2R;
- LSPV-4/413's polynomial-time/logspace explicit verifier;
- LSPV-1/418's source-clause-backed decision-DAG-to-Resolution audit;
- LSPV-2/417 and LSPV-3/423 typed-port adapter reports.

Peer findings used rather than assumed:

- CANON2 verification is polynomial in explicit evidence length \(E\), but this does not generate short evidence.
- LSPV-2/417 and LSPV-3/423 give constant-factor adapters for particular historical affine-parent semantics, not a full historical grammar theorem.
- LSPV-1/418 compiles a restricted source-clause-backed decision DAG to ordinary Resolution; Haken then constrains that restricted audit, not arbitrary SAT machines or the full mixed calculus.
- LSPV-4/414 proves exact raw acquisition costs; it does not change logical node cost.

Actual external project assessments read:

- GROKPROOF/2026-11-05_1218_PROGRESS.md, blob d3183283d6869f92617c0c758c9d31d1a201c32f: the universal fully charged all-input transformation remains open.
- research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67: restricted alternation-trading portfolio theorem, not B3.
- research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex, blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a: sequential-access crossing-sequence results, explicitly not the random-access mixed-proof bridge.

### Literature and repository queries

Actual web queries:

- Cook Reckhow relative efficiency proof systems polynomially bounded p simulation original paper PDF
- Haken pigeonhole principle resolution exponential lower bound exact model original paper
- Resolution over linear equations Res xor Tseitin lower bounds original paper
- SAT in P polynomially bounded propositional proof system Cook Reckhow equivalence NP coNP
- Cook polynomial size extended resolution proofs pigeonhole principle PHP extended resolution primary source
- Haken intractability resolution Cook extended resolution polynomial pigeonhole principle

Actual GitHub queries:

- OpenAI organization: propositional proof system resolution certificate verifier SAT — no results.
- j15marti/pnp: Rmix341 sparse identifier B3 CANON2 — found REFEREE361, LSPV-4/413, LSPV-3/422 and REFEREE362; no later sparse-ID theorem.

Useful primary findings:

- Cook--Reckhow (JSL 44, 1979) defines polynomial simulation/boundedness and proves that a polynomially bounded propositional proof system exists iff \(\mathrm{NP}=\mathrm{coNP}\). This is existence of some system, not domination by this preselected \(R_{\mathrm{mix341}}\).
- Cook (SIGACT News 8(4), 1976) gives polynomial Extended-Resolution proofs of PHP. A modern reconstruction records \(O(n^4)\) clauses.
- Haken (TCS 39, 1985) proves exponential ordinary-Resolution length for the standard PHP family while noting polynomial Extended-Resolution proofs. Exact model: the standard CNF encoding with variables \(p_{i,j}\), source clauses saying every pigeon occupies a hole and no two pigeons share a hole; arbitrary dag-like ordinary Resolution refutations; every refutation in the family is exponential in the parameter, hence superpolynomial in encoded CNF length.
- Published \(\operatorname{Res}(\oplus)\) results are system- and restriction-specific; they do not supply an unrestricted SAT-machine transfer.

Direct Google-branded search was unavailable. Indexed web search and authenticated GitHub search were used; no direct-Google claim is made.

## ITERATE

### 1. Sparse-ID attack fails: a reachable-identifier theorem

Let \(A_0\) be the number of distinct absolute variable identifiers appearing in the authenticated source, \(q\) the number of paid nodes, and \(R_i\) the set of variable/auxiliary identifiers reachable after the first \(i\) nodes.

**Theorem 363A (reachable IDs and polynomial encoding).** Every accepted CANON2 proof satisfies

\[
|R_q|\le A_0+3q.
\]

If the exact raw source has \(N\) bytes and identifiers use canonical arbitrary-precision decimal tokens, then the canonical CANON2R encoding length \(E\) obeys

\[
E=O\!\left(
N+q\,(N+q)\,(N+\log(q+2))
+q\log(q+2)
\right).
\]

Conversely \(q\le E\). Therefore polynomial paid-node size and polynomial canonical certificate-bit size are equivalent for this frozen completion.

**Rule-by-rule proof.**

- Source: \(|R_0|=A_0\le N\).
- RES: the pivot must occur with opposite signs in the two parents or the oriented-resolvent check fails. Its output is the parent union minus the pivot signs. It introduces no identifier.
- AND3: output factor support is exactly the parent-support union, of size at most three. Its optional affine mask is a subset of that support. No identifier is introduced.
- GF2: output mask is the symmetric difference of two parent masks. No identifier is introduced.
- LOCAL: parent/output combined support is exhaustively checked and has size at most three. It can introduce at most three previously unreachable original identifiers.
- DEF: it names two inputs and one mandatory sequential fresh output. Even if both inputs were previously unreachable original identifiers, it introduces at most three identifiers.

Induction gives \(A_0+3q\). Every original identifier has at most \(N\) decimal digits because it is bounded by the raw header value; every fresh DEF identifier has \(O(N+\log(q+2))\) digits. A canonical clause contains at most two signed literals for each reachable identifier, an affine mask at most one occurrence per identifier, a factor at most three support identifiers and eight truth bits, and every record has only constantly many remaining fields/references. Summing over \(q\) nodes proves the displayed bound. Strict canonical JSON admits no free whitespace blob. The reverse \(q\le E\) is immediate because every node occupies a nonempty record.

This is a bit/node normalization theorem. It is **not** a historical-/341 parser theorem and is **not** a retraction that eliminates mixed rules.

### 2. Finite adversarial controls

The actual REFEREE361 checker accepted five adversarial certificates, each with ten dead DEF nodes, ten dead LOCAL nodes and one final RES contradiction:

| header digits | paid nodes \(q\) | actual reachable IDs | \(A_0+3q\) | canonical bytes |
|---:|---:|---:|---:|---:|
| 16 | 21 | 51 | 64 | 2,197 |
| 17 | 21 | 51 | 64 | 2,208 |
| 18 | 21 | 51 | 64 | 2,219 |
| 80 | 21 | 51 | 64 | 2,901 |
| 200 | 21 | 51 | 64 | 4,221 |

The cases deliberately use DEF inputs absent from the source and LOCAL outputs containing new sparse original identifiers. They support the induction but do not replace it.

### 3. Numeric grammar counterexample and repair

The hypothesis that ordinary JSON parsing is automatically exact is false. These two legal JSON numeric fragments are distinct mathematical integer records:

~~~json
{"nvars":9007199254740992,"id":9007199254740992}
{"nvars":9007199254740993,"id":9007199254740993}
~~~

Python's arbitrary-precision JSON parser keeps them distinct. Ordinary JavaScript JSON.parse maps both identifiers to the same binary64 Number, and JSON.stringify then emits identical objects. The independent JavaScript control reproduced both collisions; lexical BigInt parsing distinguished them.

This does not falsify the frozen Python checker. It falsifies any claim that “JSON integer” alone specifies a language-independent exact grammar. Exact repair: either (a) require arbitrary-precision parsing of the original integer token before any conversion, or (b) encode every identifier/header as a canonical nonzero decimal string and parse to mathematical integers. Theorem 363A survives either repair without an inference node.

### 4. Full source-only Resolution retraction is impossible

**Theorem 363B (ER/PHP retraction obstruction).** There is no polynomial translation that takes every legal CANON2 mixed refutation and produces an ordinary Resolution refutation from only the original source clauses, with output size polynomial in source length plus mixed proof length.

**Proof.**

1. A binary Extended-Resolution definition \(z\leftrightarrow f(a,b)\) maps to one CANON2 DEF node with the four falsifying-assignment facets.
2. For the standard OR definition, the four exported facets are

\[
(a\lor b\lor\neg z),\quad
(a\lor\neg b\lor z),\quad
(\neg a\lor b\lor z),\quad
(\neg a\lor\neg b\lor z).
\]

Two ordinary RES nodes derive \((\neg b\lor z)\) and \((\neg a\lor z)\); the first facet is the remaining standard extension clause. Signed inputs and other two-input truth tables are handled by the same constant four-row construction. Thus binary ER embeds in CANON2 with constant-factor node overhead.
3. Cook gives polynomial-size ER refutations of standard PHP, so the corresponding CANON2 mixed refutations are polynomial.
4. Haken proves every ordinary source-only Resolution refutation of those same PHP formulas is exponential.
5. A polynomial source-only retraction would contradict Haken. \(\square\)

The checked four-node fixture contains one OR DEF, the two RES derivations above, and an independent final contradiction; the actual checker accepted it. The asymptotic PHP family, not the finite fixture, is the counterexample to polynomial retraction.

This theorem does **not** rule out provenance-preserving normalization that retains paid definitions, typed views and mixed rules. That stronger same-calculus normalization remains open beyond Theorem 363A and the existing local adapters.

### 5. B3 audit: the generic trace bridge is circular

Assume a fixed polynomial-time correct SAT decider \(A\). Define \(P_A\) on UNSAT inputs by taking \(F\) itself as the proof and rerunning \(A(F)\). Conditional on \(A\)'s correctness, \(P_A\) is a polynomially bounded Cook--Reckhow system.

By Theorem 363A, the statement

\[
\forall F\in\mathrm{UNSAT}\quad
\exists\pi\in R_{\mathrm{mix341}}(F):
|\pi|\le \operatorname{poly}(|F|)
\]

is equivalent whether \(|\pi|\) measures canonical bits or paid nodes. But a polynomial size-domination statement from \(P_A\) into this fixed \(R_{\mathrm{mix341}}\) is exactly the missing B3 consequent. Naming it “trace compilation” does not prove it.

The proposed trace routes fail as follows:

| proposed bridge | obstruction |
|---|---|
| check local machine transitions and final UNSAT state | proves only that the machine reached that label, not that \(F\) is UNSAT |
| add “\(A\) is correct” as a unit semantic rule | hidden reflection/SAT oracle; collapses every rejection to a free semantic jump |
| formalize correctness inside the proof | requires an independently bounded correctness/reflection proof, which is not supplied |
| choose the minimum mixed proof after \(A\) rejects | nonuniform optimizer selection is allowed for \(W_R\), but its polynomial size bound is precisely B3 |
| use Cook--Reckhow existence | gives some polynomially bounded system if \(\mathrm{NP}=\mathrm{coNP}\), not this fixed system |

Haken supplies a sharp control: soundness, completeness and polynomial verification alone cannot yield a generic fixed-system B3 bridge, because ordinary Resolution has all three properties yet remains exponentially hard on PHP even under the hypothetical assumption SAT is in P. The extra DEF/GF(2)/mixed rules might make CANON2R polynomially bounded; no proof or counterexample is known.

SAT inputs and malformed strings remain mandatory controls: neither has an \(R\)-refutation. A translator that consumes only the syntactic shape of a rejecting trace must explain how it excludes an incorrect reject on those inputs without importing global decider correctness.

## Controls and exact status

| obligation | status after REFEREE363 |
|---|---|
| CANON2R reachable-ID / node-to-bit normalization | **PROVED/RESTRICTED** |
| arbitrary-precision numeric-token semantics | **required** |
| ordinary JSON Number implementation independence | **FALSIFIED** |
| polynomial retraction to source-only Resolution | **REFUTED** by Cook/Haken PHP |
| provenance-preserving full mixed normalization | **OPEN** beyond local results |
| historical native /341 byte grammar | **OPEN** |
| same-\(R_{\mathrm{mix341}}\) B3 | **OPEN** |
| superpolynomial full-mixed \(\overline W_R\) | **OPEN** |
| P versus NP | **OPEN** |

Cook ER is a shortcut control, not a lower bound for the full mixed system. Haken is ordinary-Resolution hardness only. Tseitin/GF(2) remains a shortcut control; restricted \(\operatorname{Res}(\oplus)\) lower bounds do not transfer to arbitrary machines.

## Physical-cost distinctions

For a canonical proof of explicit length \(E\):

- acquisition and output require \(\Omega(N+E)\) bit access/writes in a materialized representation;
- canonical base64 decode/hash/strict source parsing is \(O(N)\);
- JSON/token parsing and arbitrary-precision identifier comparisons are polynomial in \(E\);
- local factor/affine checks enumerate at most eight rows, while wide Resolution/GF(2) work is charged by explicit list length;
- the current materialized checker uses \(O(N+E)\) peak storage; LSPV-4/413 separately supplies a rescan-based \(O(\log E)\)-writable-space verifier with a coarse polynomial-time bound;
- proof discovery and optimizer search remain outside \(W_R\) by definition.

These are verifier/construction costs, not lower bounds on arbitrary SAT machines. The ideal paid-node count is not physical time.

## Reproduction

- experiments/arc/lspv5_363/sparse_identifier_bound_referee363.py
- experiments/arc/lspv5_363/json_number_collision_referee363.mjs
- results/raw/arc/2026-11-05_0648_LSPV5_REFEREE363_raw.json
- results/raw/arc/lspv5_363/json_number_collision_referee363.json

No task, schedule, enabled state, role, rule, logical weight or other role's manuscript region was changed.
