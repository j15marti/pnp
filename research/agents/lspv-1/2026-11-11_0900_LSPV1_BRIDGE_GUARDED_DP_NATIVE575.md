# LSPV-1/575: Native checker-accepted 63-paid guarded bridge refutation improves the 103-paid witness

**2026-11-11 09:00 PST | LSPV-1 General SAT Lower-Bound Lead | Historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## IDEA, exact claim and four predeclared falsifiers

**Theorem 575.1 (source-fixed archived /386 upper bound).** For the exact signed 10-vertex, 15-original-edge, odd-charge, guarded cubic-bridge Tseitin formula used by LSPV-1/574, there exists a complete byte-exact certificate accepted by the unchanged archived /386 full CLI with all 41 mandatory signed SOURCE clauses, 62 distinct paid strict-Resolution inference nodes, one globally once-paid fresh conservative AND2 owner, no defining facets and an empty terminal clause. Consequently, for this **archived sibling calculus only**,

$$
\overline W_{386,\mathrm{CLI}}(F_{\mathrm{bridge}})\le 62+1=63<103.
$$

The new upper bound improves the earlier /574 legal witness by **40 paid logical nodes**, or **38.8%**. Neither 63 nor 103 is proved optimal. This does not authenticate a full original historical `R_mix341` dispatcher and provides no all-rule superpolynomial lower bound.

Before searching/constructing, the precise falsifiers were: (F1) this supposed original guarded SOURCE fails source-grounding, odd-charge cubic structure or completeness; (F2) any generated RES step has an illegal signed pivot, wrong oriented parents, forward reference, tautological/inexact resolvent or duplicate paid-charge omission; (F3) the original complete CLI rejects the packet or accepts a built-in hostile mutation; (F4) the asserted UNSAT input or the reported paid-work/terminal-ancestry ledger is false. The independently executed Node and exhaustive controls below defeat these falsifiers within the declared scope. Independent LSPV-5 review is pending.

## Exact original input and deterministic derivation

Use vertices 0 through 9, original edges indexed 1 through 15 in this order:

```json
[[0,3],[0,4],[1,2],[1,3],[1,4],[2,3],[2,4],
 [5,8],[5,9],[6,7],[6,8],[6,9],[7,8],[7,9],[0,5]]
```

The odd charge vector is `[1,0,0,0,0,0,0,0,0,0]`; guard variable is `x16`. The original in-band source is exactly 40 signed guarded wrong-parity clauses (four per vertex), followed by the unit `[16]`. It is the same graph, charge and guard as /574, not an altered formula or outside-source substitution. One separately paid owner `[0,17,1,2]` declares fresh `x17=x1 AND x2`. The owner is terminal-dead but legitimately paid once and activates the archived CLI's built-in gate-mutation control. No owner facet is inserted for free.

Run deterministic Davis-Putnam Resolution elimination with fixed pivot order

```
7, 5, 3, 6, 4, 1, 2, 8, 11, 10, 13, 9, 14, 12, 15
```

over the original signed guarded clauses. For each pivot, take all exact oriented pairs `(A contains +p, B contains -p)`, generate their exact clean non-tautological resolvent, memoize every identical clause globally as the first-created DAG node, and reuse it on later encounters. The retained terminal cone derives the negative guard unit `[-16]`. Resolve this against mandatory SOURCE unit `[16]` to obtain the empty clause. Retain **all** mandatory original SOURCE records, including terminal-dead ones, and topologically reindex all parent references. This constructs one legal whole shared proof DAG and charges every distinct paid RES record once, irrespective of the number of uses.

The accepted packet contains 41 SOURCE, 62 RES, 0 DEF facets, one gate owner declaration and **103 proof records**. Terminal-ancestor set size is 99; exactly 37 original SOURCE records are terminal ancestors; original SOURCE record indices **2, 3, 20, 21** are terminal-unreachable. This preserves the /574 distinction that mandatory SOURCE presence does not imply mandatory terminal ancestry; a different proof can leave a different set of source clauses unused.

The graph has one bridge; the four-terminal-dead-source phenomenon and finite success are not lower bounds for bridgeless expander families. The 62 RES record count was obtained by a deterministic generator replay of the published fixed order; exploratory variable-order search involved separately paid discovery work, which is not silently included in or equated to `W`.

## ITERATE: authentic original operating-system Node checker

Unlike the preceding hosted-V8-only /574 evidence, this run copied the **verbatim 6,345-byte original archived /386 checker** from `experiments/arc/lspv2_386_independent_verify.js`, checked its exact Git blob **338305c0ce101704205e57543756b8127074a986**, and executed that unchanged file as a real **Node.js v22.16.0 OS subprocess**. The deterministic standalone reproducer was itself executed in a source-path-matching local checkout, and it invokes the unchanged original checker as an OS subprocess. No original checker inference rule or corruption-test logic was patched.

**Original complete CLI returned ACCEPT** with 8,194 assertion groups and **11/11 bundled malformed-certificate tests rejected**, and reported `paid=63, res=62, def=1, records=103, sources=41`.

A separate exact RES audit independently recomputed all 62 signed parent/pivot/resolvent triples, parent-before-child indices and the final contradiction. Exhaustive enumeration of all **32,768** assignments to 15 original edge variables found **zero** satisfying the original 40 unguarded vertex parity clauses. All 41 mandatory signed SOURCE records occur in the accepted packet. This is finite executable evidence plus a constructive legal derivation; no optimum has been established.

**Exact accepted bytes:** `results/raw/arc/2026-11-11_0900_LSPV1_575_BRIDGE_GUARDED_DP_NATIVE_ACCEPTED.json`, Git blob `d5de0f477cd736ec5fd7b01be18350f9cb594fd2`, length **6,764 bytes**, SHA-256 `8442f01d5fc66e5b063c52b88cc80b30d7480ce05e2d9cc5f4abdec1e714981c`.

**Reproducer:** `experiments/arc/lspv1_575_bridge_guard_dp.cjs`, Git blob `46899797a015b87102441fef61c8ba583917b4e1`.

**Machine-readable OS and independent ledger:** `results/raw/arc/2026-11-11_0900_LSPV1_575_BRIDGE_NATIVE_OS_RAW.json`, Git blob `aefd192fb112bd7a7d88ba599ded03ff4727c0a9`.

Reproduce from the repository root:

```bash
node experiments/arc/lspv1_575_bridge_guard_dp.cjs
```

The historical checker, independent derivation audit and full assignment enumeration complete in one short OS process. The construction used two prior bounded random-order exploration chunks, 800 and 7,000 orders, followed by the pinned deterministic final-order replay; the published certificate and reproducible program depend only on the fixed final order, not a random oracle.

## Search and corpus reconciliation

Read full current root `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, full `proof2.txt` blob `7db80e8b55a7f5c348fbb2ed8decd3ceaa2657f3`, issue #3 and current peer comments, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, archived /341 and /386 checker bodies and original semantic /341 declaration, latest all-five handoffs and actual LSPV-1/574, LSPV-2/559, LSPV-3/572, LSPV-4/545, LSPV-5/489 reports, relevant 539–549 work and the /568 and /569 DP/normalization results. The prior /574 accepted a 103-paid source-identical proof, so this is not a rediscovery of the source-ancestry caveat; the measured increment is a cheaper accepted native whole-DAG certificate with genuine OS replay.

Primary theoretical checks: Cook and Reckhow, *Journal of Symbolic Logic* 44 (1979), DOI [10.2307/2273702](https://doi.org/10.2307/2273702), distinguishes proof system and decision problem; Cousot and Cousot, POPL 1977, DOI [10.1145/512950.512973](https://doi.org/10.1145/512950.512973), requires conservative concrete/abstract transfer; Clarke et al., CAV 2000, DOI [10.1007/10722167_15](https://doi.org/10.1007/10722167_15), CEGAR refinement must replay concrete counterexamples; Ben-Sasson and Wigderson, JACM 48 (2001), DOI [10.1145/375827.375835](https://doi.org/10.1145/375827.375835), Resolution-specific width/length phenomena. The external FRAT-XOR format is **not** an original mixed-rule grammar. None of these works closes the absent historical dispatcher.

## Resource ledger, abstraction and exact dependencies

The minimum-work objective remains over **free optimal completed whole shared proof DAGs**, not this one policy. For a fixed authenticated source F,

$$
\overline W_R(F)=\min_{P:\,\operatorname{NativeAccept}_R(F,P)}\;
\sum_{u\in\operatorname{PaidNodeIDs}(P)}w_R(u),
$$

where each paid node is charged once, including globally paid owners, and legal AND obligations, original SOURCE binding, branch contexts and assumption discharge cannot be ignored. The complete historical relation must additionally allow all genuine GF(2), AND3, LOCAL-CONVERT, fresh/exported/private wires, branch sharing, weakening, reconvergence, deletions and verified charges. An archived /386 witness can upper-bound **only its fixed sibling model**, not the unknown full historical R.

For P2-C3, any source-exact cost-sound may abstraction with concrete-to-abstract simulation and completed-refutation preservation cannot assign a certified *lower bound* above 63 for this particular archived /386 source. This accepted concrete cheap path is not CEGAR-spurious. Unknown historical rules must be overapproximated, not excluded by lack of examples. Original SOURCE completeness, terminal ancestry, context and paid-owner identity remain separate.

Logical work W=63 is distinct from the 6,764 input bytes, code and source retrieval, discovery over 7,800 candidate orders, truth-table enumeration, native checker replay and 11 negative tests, actual machine time, dependency span and all-phase peak space; no time/space complexity inference is made from W. No uncharged oracle or nonuniform answer table is used in the accepted proof.

- **P2-D1: OPEN.** Only original /386 SOURCE/DEF/RES authenticated; complete original `R_mix341` parser and real cross-rule transition remain missing.
- **P2-C3: OPEN.** No all-native-rule sound alpha/gamma/transformer proof.
- **P2-B1: OPEN.** No superpolynomial all-rule `Wbar` lower bound; this is a restricted finite upper bound.
- **P2-B2 and P2-B3: separately OPEN.** No polynomial SAT-algorithm-to-same-calculus proof-length transfer.

**Role handoff:** LSPV-2 Route A to continue original mixed-dispatcher search and check source binding; LSPV-3 Route B independently replay all RES/source/freshness identities; LSPV-4 Route A charge discovery, proof bytes, span and memory separately; LSPV-5 Route B independently rerun the exact OS executable and challenge source/parent/cost invariants, including alternate lower-cost certificates; LSPV-1 Route B maintains quantifiers and dependency ledger.

The five existing roles, titles, identities, Pacific schedules, historical rule/weight values, ownership boundaries and TWO Route A / THREE Route B labels remain unchanged. **P versus NP remains OPEN.**
