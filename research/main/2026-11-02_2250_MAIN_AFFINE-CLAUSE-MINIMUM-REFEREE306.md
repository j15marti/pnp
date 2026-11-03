# PNP Independent Proof Red Team — AFFINE-CLAUSE-MINIMUM-REFEREE306

**November 2, 2026, 22:50 PST, America/Los_Angeles.**  
**Task:** `6ad42a2a9a088191ab9042245f3b4393`, PNP Independent Proof Red Team.  
**Status:** **PROVED/EXACT** theorem in unchanged fixed `Rmix341`; **FALSIFIED** row-minimal shortcut; **COMPUTATIONAL** exhaustive finite audit. **OPEN:** superpolynomial worst-case minimum, B1, B2, B3, and P versus NP.

No task, title, enabled state, schedule, ownership, calculus, or weight was changed.

## Exact obstruction and four falsifiers

The obstruction is whether XOR/Tseitin families that are hard in Resolution remain candidates for the worst-case minimum in the already fixed mixed calculus, or whether local affine extraction collapses them to the binary source floor.

1. **F1 — FALSIFIED:** a row-minimal inconsistent width-at-most-three affine system has a clause-minimal canonical CNF and therefore exact cost `m-1`.
2. **F2 — PROVED/EXACT after repair:** if the *canonical CNF itself* is clause-minimally UNSAT, then its exact `Rmix341` minimum is `m-1`.
3. **F3 — PROVED/EXACT:** clause minimality has an exact affine projection test: every wrong local row pattern must extend to a solution of all other rows. Merely requiring one extendable wrong pattern per row is insufficient.
4. **F4 — FAMILY FAILURE, not a worst-case result:** every clause-minimal width-at-most-three affine family, including the verified odd cubic Tseitin cases, is source-floor easy in this calculus. This does not upper-bound the maximum over all UNSAT CNFs.

## Fixed calculus and cost

Use exactly the previously fixed, input-independent `Rmix341`: authentic source clauses are free; every distinct derived node costs one; every rule has at most two explicitly named proof parents; legal rules include binary Resolution, exact `AND3` truth-table conjunction/normalization on common original support of at most three variables, binary GF(2) row addition, paid local conversions, and paid conservative source-independent two-input `VARDEF`. Shared nodes count once. There is no SAT oracle, instance-tailored axiom, uncharged source-factor definition, or unrestricted semantic jump.

`W_R(F)` is the minimum sum of inference-node weights over all valid shared contradiction DAGs. The best proof is freely selected; discovery of it is not charged to this minimum. Parsing, source access, proof serialization, verification, and scheduled work/space are separately reported.

## The repaired exact theorem

Let `E` be affine equations over GF(2), each on one, two, or three distinct Boolean variables. Encode a row on `d` variables by all

$$
2^{d-1}
$$

clauses excluding the wrong-parity local assignments. Let `F(E)` be the conjunction of all these labelled source clauses and let `m` be their number.

### Projection criterion

For row `i` and a wrong local assignment `alpha` on its support, let `C(i,alpha)` be the unique canonical clause falsified by `alpha`. Then

$$
F(E)\setminus\{C(i,\alpha)\}\text{ is SAT}
\quad\Longleftrightarrow\quad
\exists x\;[E_j(x)=b_j\ (j\ne i)\ \land\ x|_{S_i}=\alpha].
$$

The reason is exact: the remaining clauses of row `i` allow its correct parity assignments plus only the deleted wrong pattern `alpha`. Therefore `F(E)` is clause-minimally UNSAT exactly when **every** wrong local pattern of **every** row extends through all other rows.

### Exact minimum

**Theorem.** If `F(E)` is clause-minimally UNSAT, then in the unchanged binary-premise unit-weight mixed calculus,

$$
W_{R_{\mathrm{mix341}}}(F(E))=m-1.
$$

**Lower bound.** Every one of the `m` labelled sources is indispensable. If a sound contradiction ancestry has `q` paid binary-premise nodes, its connected dependency graph has at least `m+q-1` edges and at most `2q`; hence `q>=m-1`. This covers sharing, reconvergence, paid conservative auxiliaries, representation switches, and temporary growth.

**Upper bound.** For row `i`, use exactly `2^{d_i-1}-1` legal `AND3` nodes to conjoin its canonical clauses. Every intermediate depends on at most the same three original variables, and the result is exactly the affine row. Clause minimality implies row minimality. An inconsistent row-minimal GF(2) system has an inconsistency dependency using all rows; over GF(2), every nonzero coefficient is one, so XORing every row yields `0=1`. Binary XOR uses `r-1` more nodes. Thus

$$
\sum_{i=1}^{r}\left(2^{d_i-1}-1\right)+(r-1)
=\sum_{i=1}^{r}2^{d_i-1}-1
=m-1.
$$

This is a global free-choice minimum in the fixed calculus, not an optimizer-depth observation.

## Exact counterexample to the discarded lemma

Take

$$
x=0,\qquad y=0,\qquad x\oplus y=1.
$$

Removing any one equation makes the affine system SAT, so it is row-minimal inconsistent. Its canonical CNF is

$$
(\neg x)\land(\neg y)\land(x\lor y)\land(\neg x\lor\neg y).
$$

The last clause is redundant under the two units. A two-node Resolution proof resolves `(x or y)` with `not x` to obtain `y`, then resolves with `not y` to obtain the empty clause. The three-source subformula is minimally UNSAT, so the binary source-arity lower bound is two. Consequently

$$
W_{R_{\mathrm{mix341}}}=2<3=m-1.
$$

This falsifies the row-minimal shortcut without changing the theorem's repaired clause-minimal hypothesis.

## Exhaustive and hostile controls

The Python producer enumerated every system on four variables with one through five distinct nonzero row supports of width at most three and every right-hand-side vector. A separately implemented no-import Node.js verifier repeated the enumeration and the projection tests without importing producer code.

| Quantity | Count |
|---|---:|
| Systems | 83,384 |
| SAT | 46,480 |
| UNSAT | 36,904 |
| Row-minimal inconsistent | 2,520 |
| Clause-minimal canonical CNF | 64 |
| Exact `m-1` constructions checked | 64 |
| Single-row RHS-flip SAT controls | 216 |
| Independent verifier assertions | 422 |

Named controls:

- unary contradiction: two clauses, exact cost one;
- odd 2-XOR triangle: six clauses, clause-minimal, exact cost five;
- the row-minimal counterexample above: four clauses, exact cost two;
- odd `K4` Tseitin: 16 clauses, zero models, clause-minimal, exact cost 15;
- even `K4` Tseitin: eight models;
- nine malformed DIMACS strings: all rejected.

The producer used 3.83 seconds and 9,856 KiB peak host RSS in this run. These are host-process measurements, not matched Turing-machine bounds. The logical `m-1` cost excludes enumeration, optimizer discovery, parsing, source/index reads, serialization, checking, and storage. The executable materializes the atlas, so its host space must not be confused with proof-DAG space or an FLMV all-phase bound.

## Literature and repository audit

Primary literature confirms the model separation. Urquhart's expander Tseitin formulas have exponential Resolution lower bounds, and Ben-Sasson--Wigderson explain the Resolution width/size mechanism. Itsykson--Riazanov--Smirnov give treewidth-tight results for regular Resolution and OBDD systems. Recent work still describes superpolynomial lower bounds for unrestricted DAG-like `Res(XOR)` as difficult/open, emphasizing that proof-system rules matter. None of these results is a lower bound for `Rmix341`, which directly extracts and XORs local affine rows.

Queries logged:

- Web: `Tseitin formulas resolution lower bounds expander primary paper`; `proof complexity XOR formulas resolution parity reasoning primary paper`; `extended resolution superpolynomial lower bounds open survey`; `GitHub Tseitin CNF generator resolution proof checker`.
- Project GitHub: `"width-3" affine`, `"row-minimal"`, `"3-XOR"`, `Tseitin`; the exact row-minimal/clause-minimal projection repair was not found. The result extends, rather than duplicates, LSPV-2 `MIXED-TSEITIN341`, which proved the bridgeless cubic graph case.
- `github.com/openai`: `Tseitin` returned two unrelated parity/PSD-rank preprint files; `"resolution proof"` returned one unrelated cohomology file. No reusable fixed-calculus verifier was found. Failed search is not a novelty claim.

Corpus reviewed: the 12:04 five-role refocus, current issue #3 through REFEREE305 and peer 351/352/354 updates, `AGENTS.md`, `CODEX.md`, the repository `pnp-research` protocol, LSPV-2 mixed Tseitin and restriction firewall, LSPV-3 BVP bit-blast collapse, LSPV-4 Peitl selector cap, and LSPV-1 strong-backdoor corridor. Relative to root synthesis, the new item is the exact clause-projection repair and its row-minimal counterexample; no previous theorem is weakened.

Primary sources:

- A. Urquhart, [Hard Examples for Resolution](https://doi.org/10.1145/7531.8928), JACM 34 (1987).
- E. Ben-Sasson and A. Wigderson, [Short Proofs Are Narrow—Resolution Made Simple](https://eccc.weizmann.ac.il/report/1999/022/), JACM 48 (2001).
- D. Itsykson, A. Riazanov, and P. Smirnov, [Tight Bounds for Tseitin Formulas](https://doi.org/10.4230/LIPIcs.SAT.2022.6), SAT 2022.
- K. Efremenko, M. Garlik, and D. Itsykson, [Lower Bounds for Regular Resolution over Parities](https://doi.org/10.1137/24M1696640), SICOMP 2025.

## B1/B2/B3 referee classification

- **B1:** not proved or falsified. The affine family has short mixed proofs, so no fast-family recognizer can witness a pointwise mismatch here.
- **B2:** untouched. No comparison with a total correct decider's worst-case runtime on every string of length at most `N` is made.
- **B3:** remains OPEN. Retiring an affine candidate family neither proves nor refutes `SAT in P => Wbar_Rmix341 polynomial` for the same fixed calculus.
- **Worst-case lower bound:** remains OPEN. The theorem is a family filter; it does not upper-bound the maximum over nonaffine UNSAT CNFs.

The next hard-family screen must exclude affine extraction and, per current peers, constant-size Horn/2CNF backdoors, isolated UNSAT subcores, selector-only amplification, and polynomial Extended-Resolution/definition shortcuts. It must then survive every mixed rule in the same preselected calculus. P versus NP remains OPEN.

