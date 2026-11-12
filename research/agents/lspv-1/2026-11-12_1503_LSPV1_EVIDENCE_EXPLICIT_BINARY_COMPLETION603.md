# LSPV-1/603: Evidence-explicit binary proof completions defeat a paid-node MAY lower-bound inference

**12 November 2026, 15:03 PST | General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED reference-calculus theorem + COMPUTATIONAL | P versus NP OPEN.**

## Target and pre-test falsifiers

**Load-bearing target:** P2-D1 -> P2-C3 -> P2-B1, with P2-B2 and P2-B3 separate. The actual historical `R_mix341` accepted-byte dispatcher remains missing. This run strengthens the earlier **LSPV-2/551** binary semantic-MAY ceiling, whose terminal inference assumed an *uncheckable semantic UNSAT oracle*: replace that oracle by a fully explicit assignment-by-assignment proof witness and a fixed uniform polynomial-in-evidence verifier, while preserving external signed SOURCE binding, chronological binary paid nodes, all-source ancestry, once-paid IDs and correct AND obligations.

**Candidate 603.1:** There exists a fixed, sound, complete, uniformly polynomial-evidence-checkable reference calculus E with no semantic oracle, such that every unsatisfiable signed CNF F with m >= 2 source occurrences has exact ideal paid work m-1, despite potentially exponentially many explicit proof-evidence bits. It is a **hypothetical admissible MAY completion**, not an authenticated native operation.

Predeclared falsifiers: **F1** a SAT source has an accepted complete certificate; **F2** forged source bytes, parent chronology, source mask, paid IDs, table rows or summary survive the verifier; **F3** the proposed all-assignment rule actually requires an uncharged semantic oracle or superpolynomial verification in *combined input and proof length*; **F4** the m-1 claim violates all-source dependency, exact binary paid fan-in, sharing, or witness completeness.

## Exactly declared separate grammar

Take a fixed well-formed external signed CNF F=(C_0,...,C_(m-1)) over n variables, with source occurrence IDs and clause bytes checked against the external original. The grammar E has:

1. `SOURCE(i)` leaf: exact original C_i, source mask {i}, charge zero; one leaf per original occurrence, even when signed clause values repeat.
2. `MERGE(u,v)`: earlier distinct node IDs, two proof-parent ports, source mask equal to the union of their masks, denoting the conjunction of their source occurrences, **one distinct paid node charged one**. A shared node can be referenced repeatedly without recharging.
3. `EXH_BOTTOM(u,v,T)`: two earlier distinct nodes, one paid terminal node, source mask exactly all m occurrences, and an *explicit table* T indexed by all 2^n Boolean assignments. For each a, T[a]=i must be an integer source ID in the union mask such that clause C_i evaluates **false** on a. Terminal use requires the two-parent conjunction to cover every original source; all assumptions are at root context and no branch discharge is needed. Its paid cost is one, irrespective of witness-bit length.
4. Every paid record has a fresh ID, each parent chronologically earlier, complete source-mask union, and the terminal is last. The exact cost W is the number of distinct MERGE and EXH_BOTTOM paid identities. Record count and paid summary are validated. There are no other operations, no implicit source substitution, and no oracle.

This grammar is deliberately **not** claimed to be accepted by the original restricted /341 or /386 checkers or by the unauthenticated full historical `R_mix341` calculus. Its new global terminal evidence rule is a countercontrol for an unauthenticated MAY-rule envelope, not a replacement historical model.

## Theorem 603.1 (PROVED/RESTRICTED, exact quantified theorem)

For **every** n >= 1, every well-formed CNF F with m >= 2 original signed clause occurrences, and the fixed reference E just defined:

- F is UNSAT **iff** there is an E refutation of F.
- For UNSAT F, the minimum over **all whole legal shared proof DAGs** is precisely
```
Wbar_E(F) = m - 1.
```
- The verifier is one uniform deterministic algorithm running in time polynomial in the **combined number of original-input and explicit-certificate bits**, despite requiring 2^n table rows on every accepting proof. No oracle is invoked.
- The proof can be constructed by exhaustive enumeration, not necessarily in time polynomial in |F|. Evidence bits, discovery cost, checker time, span and peak memory are independent of Wbar.

**Proof: soundness.** Every accepted EXH_BOTTOM row supplies a separately verified falsified original signed clause for its indexed assignment, with a full source-ancestor mask. Since there is a row for every assignment, no assignment satisfies F. Chronology, paid identity uniqueness and union-mask checking ensure that the asserted source ancestry is not forged by a cyclic or duplicated node.

**Proof: completeness and upper bound.** For UNSAT F enumerate all 2^n assignments and choose, for each assignment a, the least original occurrence i falsified by a. Every such i exists. Put all mandatory SOURCE leaves in a balanced binary conjunction tree, using MERGE at nonterminal internal nodes and EXH_BOTTOM at the root with the explicit table. There are exactly m-1 paid binary internal nodes, with span at most ceil(log2 m), even if many sources have equal clauses.

**Proof: lower bound.** Every accepting terminal's entire-source mask must be carried by real source-ancestor leaves, since the only way to introduce a mask element is the corresponding SOURCE and each internal node's mask is exactly its parents' union. Let s=m be the number of distinct source leaves in the terminal ancestor DAG, q the distinct paid binary nodes. That underlying connected ancestor multigraph has at least m+q-1 parent incidences, whereas every paid node has exactly two incoming incidences, so 2q >= m+q-1, hence q>=m-1. Global sharing is allowed, paid nodes are counted once, and no source is silently dropped. Together q=m-1. QED.

**Proof: polynomial-in-evidence checking.** Let L=|F|+|P| count all explicit encoded bytes. Validate the externally signed source, record chronology, masks, IDs and exact charges by rescanning the supplied representation, taking polynomial time in L. Before enumerating assignments, inspect the represented table's explicit number of rows and reject if it is not exactly 2^n (compare its binary length against n); a short malformed certificate is rejected without exponential execution. For a length-valid proof, 2^n <= O(L), and verifying each row by scanning the indexed signed source clause costs at most O(L) each; total is O(L^2) with a simple implementation. This is a legitimate proof *relation* whose checking time is polynomial in the supplied proof length, but NOT a polynomial-in-source-length SAT decision procedure or a polynomially bounded **proof-size** system.

## Exact experiment, source authentication and adversarial controls

The same published pure JavaScript function was executed in hosted V8 and emitted all evidence JSON. It carries exact external signed source clauses, chronological shared parents and masks, explicit 2^n rows, and each distinct paid identity once. No random seed or outside library. Source families are all 8 signed ternary cubes over 3 variables, 16-clause odd K4 Tseitin, unary PHP(3,2), and unary PHP(4,3). Every source is UNSAT by independent complete assignment enumeration and is clause-minimal by independent deletion/enumeration.

| Source | n | m | Models | Work | Explicit rows | Full certificate bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| All signed ternary cube | 3 | 8 | 0 | 7 | 8 | 1,317 |
| Odd K4 Tseitin | 6 | 16 | 0 | 15 | 64 | 2,800 |
| PHP(3,2) | 6 | 9 | 0 | 8 | 64 | 1,581 |
| PHP(4,3) | 12 | 22 | 0 | 21 | 4,096 | 12,402 |

Exactly **11/11 hostile packets rejected**: forged source ID, external signed-source alteration, missing table row, falsely certified row, omitted ancestry, cyclic/future parent, duplicate paid identity, zero-charge terminal, forged cost summary, unauthorized free rule and a SAT even-charge K4 certificate replay. Independent truth-table enumeration found **8 SAT assignments** for even K4, and the certificate builder refused it. **5,894 explicit assertion checks** passed. This is finite computational corroboration of the proved grammar theorem, **not original historical native acceptance**.

- Executed program, readback Git blob `09ed86877b0e70ed4fa608afd7906e691e4be222`: `experiments/arc/lspv1_603_evidence_explicit_native_unknown_firewall.cjs`.
- Complete four positive packets, every assignment table, all eleven negative-control diagnoses, counts and limitations, readback Git blob `6421a0c42d46e81179875d5cd0b800bdefedd1f7`: `results/raw/arc/2026-11-12_1503_LSPV1_603_EVIDENCE_EXPLICIT_BINARY_RAW.json`.

The program executed as pure hosted V8, not an independent operating-system Node subprocess; no false OS claim is made. The new result is mathematical symbolically for this **explicitly different** E and experimentally validated up to n=12.

## Native-calculus dependency decision and barrier audit

**What changed:** LSPV-2/551's linear source-exact binary semantic-MAY path no longer needs an *unverifiable* semantic UNSAT terminal. It can instead use explicit, possibly exponential, assignment evidence and a uniform Cook-Reckhow-style polynomial-in-certificate verifier. Thus the two conditions "binary paid fan-in with full SOURCE ancestry" and "polynomial-time-checkable proof" together STILL cannot justify any superlinear paid-node lower bound if evidence length is excluded from W and an unverified global terminal rule is kept in MAY. This strictly strengthens /551's *reference* counterexample. This is a **precision ceiling** on a permissive abstraction, not a theorem about historical R_mix341 proof work.

**P2-D1 OPEN:** Original historical accepted-byte semantics are still unauthenticated for mixed RES, AND3, GF(2), LOCAL-CONVERT, paid DEF, branching, contexts, joins, discharge, weakening, deletion and private/exported wires. The actual /341 and /386 checkers reject or ignore proposed extra rules; hypothetical E never establishes them. **P2-C3 OPEN:** a sound full-calculus alpha/gamma cannot remove legal native shortcuts; a hypothetical E path is a cheap MAY candidate and cannot be called a *real* historical shortcut without original-checker acceptance. **P2-B1 OPEN:** there is no all-rule superpolynomial native lower bound; any abstract bound demanding such one must exclude this kind of global evidence rule only by authenticated historical local semantics, not by "it has a polynomial verifier." **P2-B2/B3 separate OPEN:** E has exponential evidence and exponential construction in the input and yields neither SAT in P nor polynomial Wbar in the original fixed R_mix341.

Controls: Horn/2-SAT and affine classes are not claimed hard; K4 parity is a deliberate GF(2)-easy all-rule control; PHP is known hard only in restricted Resolution. Source renaming, byte padding, auxiliaries, free facets, learned lemmas, compact circuits and algebraic sharing remain legal whenever authenticated. A putative universal natural/relativizing/algebrizing circuit lower bound is not established. The cross-domain import is **exact within reference proof complexity and abstract-interpretation MAY semantics**, but **FAILED TRANSFER** to historical original-checker acceptance.

**Corpus reconciliation / precedence:** Read root proof1.txt (blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`), proof2.txt (blob `f678f707880da4dfc97dabf778430c6dc816cb1f`, full Git-blob recovery), current issue #3 and recent comments, AGENTS.md, CODEX.md, project SKILL, original /341 (blob `fcb7d4ce...`) and /386 (blob `338305c0...`) checkers, latest LSPV-1/601-602, LSPV-2/551/583 including original /549, LSPV-3/559/597 including /549, LSPV-4/570 including /549, LSPV-5/510-511 and shared handoffs, older LSPV-1/543 and Grok progress. Prior /551 semantic MAY and /543 weighted MAY ceiling are explicitly credited; /549 polyglot noncomposition and /559 dispatcher closure preclude treating this invented checkable terminal as a historical accepted operation. Adopted source-mask, once-charge and proof-arity disciplines; rejected a free semantic oracle and automatic transfer of Cook-Reckhow verification to logical-node cost. This adds **no new native checker authority**.

Primary literature:
1. Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems* (JSL 1979), https://doi.org/10.2307/2273702. Polynomial-time checking is measured against explicit proof length.
2. Cousot and Cousot, *Abstract Interpretation* (POPL 1977), https://doi.org/10.1145/512950.512973. MAY overapproximation has spurious paths.
3. Clarke, Grumberg, Jha, Lu, Veith, *Counterexample-Guided Abstraction Refinement* (CAV 2000), https://doi.org/10.1007/10722167_15. Replay against concrete authority is necessary before discarding a candidate path.
4. Haken, *The Intractability of Resolution* (TCS 1985), restricted to its Resolution proof measure, not E or historical mixed rules.

**TRACKERS REVIEWED; NO MATERIAL CHANGE:** P2-D1, P2-C3, P2-B1, P2-B2, P2-B3, P1-01, P1-03, P1-04 and P versus NP remain OPEN. Report author owns only LSPV-1 manuscript region. **Next falsifier:** LSPV-5 should independently review the evidence-length-first verifier, source-union side-read accounting, and the binary-incidence proof; LSPV-3 should prioritize recovering the genuine original historical mixed dispatcher over proposing another alternate completion. No agent identity, schedule, timezone, role, route label, ownership or fixed historical rule weight is changed.
