# REFEREE352 — unlock-chain generic B3 firewall

**PNP Independent Proof Red Team | November 4, 2026, 19:54 PST**  
**Status:** PROVED/EXACT fixed-calculus counterexample to a generic decision-in-P-to-proof-bound principle, using ordinary 2-CNF; PROVED/EXACT same-source collapse in native `R_mix341` by unrestricted RES; COMPUTATIONAL independent finite replay. This does **not** refute B3 for the actual fixed `R_mix341`. Its full native LOCAL/export/DEF/GF(2) grammar, a polynomial certificate normalizer, B1/B2/B3, a superpolynomial mixed minimum, and P versus NP remain OPEN.

## IDEA before search

Test whether the weakest bridge could follow from only the abstract properties already demanded of `R_mix341`: one fixed uniform calculus, soundness, completeness, exact-source authentication, polynomial local checking, bounded premises, positive paid-node weights, and no semantic oracle.

**Assumption under attack.** For every decision problem `L in P`, every fixed proof calculus for nonmembership having those abstract properties has polynomial worst-case minimum paid cost.

**Falsifiable prediction.** A fixed exact-source calculus for 2-CNF can impose a locally checkable binary-premise administrative unlock chain of length `2^v` before enabling ordinary Resolution. Since 2-SAT is unconditionally in linear time, an exponential minimum would refute the generic principle without assuming `P=NP`. The same 2-CNF source should have a one-node refutation in actual `R_mix341`, proving that the result is a calculus-sensitivity control rather than a disguised B3 refutation.

Four falsifiers were fixed before search:

1. source authentication or soundness permits skipping the chain;
2. shared DAG reuse permits a counter jump;
3. a single activation or malformed empty source permits contradiction;
4. the same source is also hard for native `R_mix341`, which would misclassify the result.

## SEARCH

### Governing project and current peer state

Read first:

- `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`;
- current issue #3 through LSPV-1/407 and LSPV-4/401;
- the authoritative unchanged declaration `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`;
- REFEREE351 and current peer reports/handoffs LSPV-1/406-407, LSPV-2/406, LSPV-3/408, and LSPV-4/401.

The exact `/341` words still authorize unrestricted binary RES, support-at-most-three exact AND3 factors, binary GF(2) row addition, unary constant-support implication LOCAL-CONVERT, and one paid conservative two-input DEF. They do **not** serialize LOCAL circuit payloads or say whether internal gates are private, which wire IDs are public, whether a DEF gate relation is exposed as clauses/factor/affine row, or which exports require another paid definition.

Current findings used with attribution:

- LSPV-4/401 proves the flat explicit clause-output fragment: a factor on support `S`, `|S|<=3`, entails a supplied clause `C` iff `C` is tautological or it entails the restriction of `C` to `S`; the checker must output the original `C` to preserve consumer pivots. This does not specify circuit payloads or reusable exports.
- LSPV-3/408 conditionally eliminates a bounded number of paid DEF gates when defining clauses are selectable RES premises; its `3^(r+b)` bound is polynomial only for fixed `b`, and native selectors remain unspecified.
- LSPV-2/406 gives a conditional nested paid-XOR gate test and reports the unresolved question whether paid DEF relations export affine rows natively.
- LSPV-1/406-407 gives conditional feasible-reflection/antichecker routes, explicitly not a proof of B3.

Actual independent-assessment files read:

- `GROKPROOF/2026-11-05_0315_PROGRESS.md`, blob `2c21a1eb356b15a22f364d5d58a6b94360560943`: the all-input correctness-preserving resource contraction remains open; numerical FLMV membership does not construct it.
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`: exact results only inside its portfolio alternation-trading system.
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`: sequential-access crossing-sequence bounds, explicitly not the indexed random-access or proof-reflection bridge.

Neither independent assessment supplies the missing native grammar, normalization theorem, or B3.

### Primary literature and general web

Actual queries:

1. `Cook Reckhow 1979 relative efficiency propositional proof systems PDF p-bounded NP coNP`;
2. `Pudlak reflection principles propositional proof systems survey PDF 2020`;
3. `Aspvall Plass Tarjan 1979 linear time algorithm 2-SAT PDF`;
4. `artificial propositional proof system exponential proof length padding local verifier`;
5. `arXiv 2609.23015 Braun exponential lower bound bit pigeonhole principle resolution over parities Res XOR theorem`;
6. `Haken 1985 intractability of resolution pigeonhole principle exponential DAG resolution theorem`;
7. `Cook 1976 short proof pigeonhole principle extended resolution PDF`.

Read rather than relying on snippets:

- Cook–Reckhow, *The Relative Efficiency of Propositional Proof Systems* (JSL 1979), especially Definitions 1.3 and Proposition 1.4: `L in NP` iff `L` has **some** polynomially bounded proof system. This is an existential statement and does not p-bound every fixed verifier. <https://www.cs.utoronto.ca/~sacook/homepage/cook_reckhow.pdf>
- Pudlák, *Reflection principles, propositional proof systems, and theories* (2020), especially the introduction: reflection and efficient proof search/simulation are separate system-dependent properties; strong systems proving their reflection principles require additional structure. <https://iuuk.mff.cuni.cz/~koucky/EPAC/papers/TechRep-Pudlak-ArXiv-2007.14835.pdf>
- Aspvall–Plass–Tarjan, *A linear-time algorithm for testing the truth of certain quantified Boolean formulas* (IPL 1979): 2-CNF satisfiability is decided through SCCs in linear time on their RAM model. <https://mathweb.ucsd.edu/~sbuss/CourseWeb/Math268_2007WS/2SAT.pdf>
- Haken, *The intractability of resolution* (TCS 1985): the lower bound is for ordinary Resolution on pigeonhole tautologies; the paper itself contrasts polynomial Extended Resolution proofs. DOI `10.1016/0304-3975(85)90144-6`.
- Cook, *A short proof of the pigeon hole principle using extended resolution* (SIGACT News 1976): polynomial ER proofs are the mandatory PHP countercontrol. DOI `10.1145/1008335.1008338`.
- Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities* (arXiv:2609.23015): stated theorem is for unrestricted DAG-like `Res(oplus)` clauses on bit-PHP with `n=2^ell`, `ell>=32`, lower bound greater than `exp(n/(32768 ell^2))`. It does not cover ER or `R_mix341`; independent specialist review is still appropriate for this new work. <https://arxiv.org/abs/2609.23015>

The available browser exposed general web search, not a direct Google-branded search UI. No direct Google session is claimed. Search for a named prior “unlock-chain” theorem found no relevant primary result; absence is not a novelty claim.

### GitHub, including OpenAI

Authenticated project queries included:

- `R_mix341 LOCAL-CONVERT exported-wire AND3 GF(2) paid-definition grammar`;
- `unlock chain padded proof system B3`;
- `TPORT`, `ONETAPE`, and the exact Grok progress path.

Authenticated `github.com/openai` queries were:

- `propositional proof system reflection resolution verifier`;
- `DRAT resolution proof verifier CNF`;
- `ExecCNFNodeSearchCosts`.

The first two produced no relevant OpenAI implementation. The third located and this run read the complete `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean`, blob `1ced21f44ad49370d1b812e862c03c3a91d7f836`. It ties a concrete execution trace, visit log, instruction bound, and stack-bit bound to one program run. That is useful cost discipline but it is not a proof compiler, reflection theorem, or evidence that code is a mathematical proof.

## ITERATE I — the exact unlock calculus

### Definition of fixed `R_lock2`

Inputs are strict DIMACS CNFs with nonempty clauses of width at most two. Malformed headers, counts, terminators, widths, and variable IDs are rejected. Original source clauses are free, indexed, exact-source objects. Every derived record costs one, has at most two premises, and is checked in time polynomial in its explicit record and source:

1. `START(0)` creates an administrative token with counter zero.
2. `TICK(token i)` creates token `i+1`, only when `i+1<2^v`, where `v` is the authenticated header variable bound.
3. `ACTIVATE(source j, token 2^v-1)` copies exact source clause `j` into the active clause type. The checker retrieves the clause from the actual input by index; no digest or collision assumption is used.
4. `RES(active C∨x, active D∨¬x)` produces the exact non-tautological resolvent on the named pivot.

Only active clauses can be resolved. A refutation ends in the active empty clause. The grammar is fixed independently of `v` and the source.

### Theorem 352.1 — sound, complete, local, binary-premise

`R_lock2` is sound and complete for UNSAT 2-CNF, and its explicit proofs are polynomial-time checkable.

**Proof.** TICK records carry no logical clause. ACTIVATE copies one exact source clause, hence preserves consequence. RES is ordinary sound Resolution. Induction over the DAG proves that every active clause is entailed by the exact input, so no satisfiable source has a refutation. For completeness, construct the unique legal token chain to `2^v-1`, activate every source clause, and append any ordinary Resolution refutation; Resolution is refutationally complete for CNF. Every record has zero, one, or two explicit references and all arithmetic, source lookup, and clause checks are polynomial in the explicit source-plus-proof length. QED.

The exponential chain does not hide a semantic oracle. It is an intentionally perverse but legal administrative discipline, just as proof-system definitions permit syntactically redundant work.

### The hard/easy paired family

For `v>=1`, let

`U_v = (x1) AND (NOT x1) AND product_{i=2..v}(xi OR NOT xi)`

and

`S_v = (x1) AND product_{i=2..v}(xi OR NOT xi)`.

`U_v` is UNSAT by its two-unit core. `S_v` has exactly `2^(v-1)` models. Both use every declared variable syntactically, avoiding a free unused-header padding objection. Their signed decimal DIMACS lengths satisfy `N_v=Theta(v log v)`.

### Theorem 352.2 — exact exponential minimum

For every `v>=1`,

`W_Rlock2(U_v) = 2^v + 3`.

**Lower bound.** Every active clause has an ACTIVATE ancestor, and every ACTIVATE requires token `2^v-1`. Since START is the unique counter zero and each unary TICK increases by exactly one, any path to that token contains START plus all `2^v-1` ticks: at least `2^v` paid token nodes. No source is empty. The only clause-producing rules are ACTIVATE and RES, so an active empty clause needs at least two activated nonempty clauses and one RES inference. Thus at least `2^v+3` nodes are paid.

**Upper bound.** Build the full token chain, activate `(x1)` and `(NOT x1)`, and resolve once. The cost is exactly `2^v+3`. QED.

Because `N_v=Theta(v log v)`, the minimum is `2^{Omega(N_v/log N_v)}` and exceeds every polynomial in `N_v` along the family.

### Corollary 352.3 — generic bridge falsified, noncircularly

2-SAT is in linear time, yet the fixed, uniform, sound, complete, exact-source, positive-unit-weight, at-most-binary-premise, polynomially checkable calculus `R_lock2` has superpolynomial worst-case minimum refutation cost. Therefore **decision in P plus those generic proof-system properties does not imply polynomial minimum cost for an arbitrary preselected calculus**.

This is not a claim about all calculi. Cook–Reckhow's canonical decision verifier gives another polynomially bounded proof system for UNSAT 2-CNF. The example proves that choosing one fixed system matters and that local checkability is not p-simulation.

### Same-source native control

For every `U_v`, actual `R_mix341` resolves its two original unit clauses in one native RES node. Since source clauses are free and a contradiction is not itself a source, at least one paid node is necessary. Hence

`W_Rmix341(U_v)=1`.

This falsifies any attempted transfer of the unlock lower bound to the actual calculus. It also shows exactly what a valid B3 proof must exploit: particular unrestricted native rule structure or a proven p-simulation/reflection theorem, not merely generic soundness/completeness/local verification.

## ITERATE II — consequences for the two requested deliverables

### Native normalization grammar

This search did not uncover a new authoritative grammar beyond `/341`. The flat clause fragment is now exact by LSPV-4/401, and REFEREE351's typed-interface theorem gives a sufficient composition discipline after a serialization is fixed. But the following remain underdetermined by the native prose:

- whether a LOCAL circuit's internal gates are private checking payload or public reusable nodes;
- whether a public internal wire must be a separately paid DEF;
- the exact clauses/relations attributed to a DEF node and how consumers select them;
- whether a DEF XOR gate automatically has AFFINE type, or requires a paid LOCAL conversion;
- how exact public objects and all downstream named pivots/ports are serialized.

Consequently a full original-source-authenticated rule-by-rule native normalizer is still not a well-posed theorem from the current text alone. This is a specification limitation, not a legal counterexample to every possible completion. The already established minimal native counterexample remains the three-node AND3→LOCAL→RES pivot-loss fragment from REFEREE351/LSPV-4/400: implication-only in-place normalization is false.

### B3 for the same fixed calculus

The present result refutes a tempting **generic lemma**, not actual B3:

`SAT in P => Wbar_Rmix341 is polynomial`.

The actual implication remains OPEN. Under `SAT in P`, Cook–Reckhow supplies some polynomially bounded verifier, including the canonical decider verifier from REFEREE351. To reach the preselected `R_mix341`, one still needs a noncircular theorem that this calculus has polynomial proofs for all such rejected inputs—equivalently a p-simulation/feasible-reflection result or another system-specific structural argument. Assuming polynomial formalized decider correctness would simply reintroduce the missing certificate property unless independently derived.

The unlock example proves that no argument based only on “fixed + sound + complete + local + bounded-premise” can close that gap. The one-node native control proves that system-specific rules can close it on a sublanguage without any machine-trace reflection. For general CNF, no analogous all-input theorem is known.

## Established hard-family model audit

- **Haken PHP.** Standard unary `PHP_(h+1)^h` has `h(h+1)` variables, `h+1` pigeon clauses, and `h*binom(h+1,2)` binary collision clauses. Haken's result lower-bounds every ordinary shared-DAG Resolution refutation by `2^{Omega(h)}` lines for sufficiently large `h`. With explicit signed binary-index DIMACS its source length is `Theta(h^3 log h)`. It says nothing about DEF, AND3, LOCAL, GF(2), ER, or arbitrary SAT algorithms.
- **Cook ER.** Polynomial Extended Resolution PHP proofs are a direct representation/algorithm countercontrol. An exponential Resolution backtranslation would not establish mixed or machine hardness.
- **Braun Res(oplus).** The stated 2026 result is for unrestricted DAG-like `Res(oplus)` on bit-PHP under its exact clause language and quantifiers. It is not a lower bound for ER or `R_mix341`.
- **Tseitin.** Odd expander Tseitin CNFs may be Resolution-hard, while native `/341` AND3 extraction plus GF(2) addition yields linear mixed proofs. It is the mandatory affine-shortcut control.

None of these restricted theorems supplies B3 or an all-algorithm SAT lower bound.

## Computational verification

Artifacts:

- `experiments/arc/lspv5_352/unlock_chain_referee352.py`;
- `experiments/arc/lspv5_352/verify_unlock_chain_referee352.js`;
- `results/raw/arc/2026-11-04_1954_LSPV5_352_UNLOCK_CHAIN.json`.

The Python producer passed **41,595 assertions** on `v=1..12`: exact UNSAT/SAT model counts, every explicit token and logical node through the 4,099-node `v=12` proof, source authentication, named-pivot Resolution, six malformed DIMACS strings, premature unlocks, counter jumps, invalid source references, bad pivots, and attempted reuse of the UNSAT proof on the SAT partner. It also emitted symbolic cost rows through `v=64`.

The separately structured no-import Node verifier passed **16,707 checks**, independently reparsing every source, recomputing all model counts, reconstructing and digest-matching every proof, replaying every rule, checking the exact formula `2^v+3`, the one-node native-control field, and symbolic large-`v` growth. Finite replay supports the implementation; Theorems 352.1–352.2 are symbolic proofs for all `v`.

## Physical cost distinctions

For `U_v`, logical minimum paid nodes are exactly `2^v+3`. An explicit counter record needs `Theta(v)` bits, so the emitted proof has `Theta(v 2^v)` bits. Construction, serialization, source lookup, counter comparison/increment, clause checking, and full validation therefore require `Theta(v 2^v)` bit work in the straightforward explicit format. A sequential topological checker can keep the current `v`-bit counter and small clause records, using `O(v+log m)` writable bits, but this does not erase acquisition or output time. A random-reference verifier or retained DAG may use more space.

Optimizer discovery remains free in `W_R`; it does not help because every legal derivation contains the forced chain. Conversely, this ideal logical count is not asserted to lower-bound arbitrary machine runtime. The actual `R_mix341` proof on the same source has one logical node, while parsing and physical output still cost source-dependent work.

## Precise proof status and next unresolved step

- **PROVED/EXACT:** generic fixed/sound/complete/local/binary-premise properties do not imply polynomial proof minima even for a linear-time decision language.
- **PROVED/EXACT:** `W_Rlock2(U_v)=2^v+3` and `W_Rmix341(U_v)=1` on the identical sources.
- **PROVED/EXACT:** the generic B3 route is noncircularly falsified as a method.
- **NOT REFUTED / OPEN:** same-fixed-`R_mix341` B3.
- **OPEN:** full native LOCAL/export/DEF/AFFINE grammar and an unconditional global certificate normalization.
- **OPEN:** superpolynomial `Wbar_Rmix341`, B1/B2/B3, and P versus NP.

The next decisive B3 attempt must name a native rule-specific invariant or p-simulation that excludes `R_lock2`-style administrative slowdowns and derives short `R_mix341` proofs from `SAT in P` without assuming short reflection certificates. The next grammar step remains an authoritative serialization of LOCAL private/public ports and DEF-to-clause/factor/AFFINE exports, followed by exact-interface consumer recompilation.
