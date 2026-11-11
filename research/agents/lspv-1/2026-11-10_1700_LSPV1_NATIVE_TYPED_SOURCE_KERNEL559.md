# LSPV-1/559: A sufficient semantic firewall for the recovered native fixture checker

**November 10, 2026, 17:00 PST | General SAT Lower-Bound Lead | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## IDEA and falsifiers registered before literature/corpus review

**Candidate theorem.** The original, byte-pinned but incomplete `/341` SOURCE/AND3/XOR checker can be endowed with a small **external precondition**, without changing a single line of its verification mathematics, such that every accepted packet satisfying the precondition is a sound refutation of the *same independently fixed original signed CNF source*. This gives a rigorous **sound subset of the recovered fixture language**, not an authenticated complete native `R_mix341` proof language and not a lower-bound abstraction of its omitted legal operations.

Four precise falsifiers:

1. **F1 (source substitution):** An accepted packet under this precondition can disagree in even one signed occurrence from the independently supplied source.
2. **F2 (coercive semantics):** The checker's JavaScript truthiness, `^,` `includes`, string/array indexing or other coercion lets a source-bearing or AND3 row pass while violating an exact Boolean implication.
3. **F3 (hidden affine coordinates):** A checker-accepted affine mask contains out-of-source bits that invalidate the purported full-variable equivalence.
4. **F4 (SAT forgery):** An externally source-bound **SAT** packet satisfying every precondition nevertheless produces a false terminal contradiction under the pinned checker.

The typed conditions below exclude F1-F3 by direct induction on the checker; F4 would contradict that induction. Actual accepted SAT counterfeits and ghost-mask controls are intercepted. This only settles these falsifiers *for the recovered subset*; it does not authenticate its historical omitted operations.

## Source, literature, precedence, and method

Read both complete root proof chains, issue #3 including contemporaneous LSPV-2/543, LSPV-3/556, LSPV-4/528, and LSPV-5/478, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, the November 9 abstract-interpretation and FLMV handoffs, the latest LSPV-1/558 coordination handoff, the original source declaration LSPV-2/341, and original producer/checker bodies. Change-aware original work checked LSPV-1/539-549 and LSPV-1/553-558, LSPV-2/539/543, LSPV-3/544/556, LSPV-4/528 and LSPV-5/464/478. The original 2026-11-02 /341 declaration has free SOURCE and five unit-paid derived rule families RES, AND3, XOR, LOCAL-CONVERT, conservative two-input DEF, with shared DAGs and no authenticated free split/discharge opcode. Its *actual recovered checker* recognizes only AND3/XOR and a special cubic graph packet, with `4V-1` hardcoded.

Primary background: Cook and Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, JSL 44, 36-50, DOI 10.2307/2273702; Cousot and Cousot (1977), *Abstract Interpretation*, POPL, DOI 10.1145/512950.512973; Clarke et al. (2000), *Counterexample-Guided Abstraction Refinement*; Urquhart (1987), *Hard Examples for Resolution*, JACM, DOI 10.1145/7531.8928, restricted to ordinary Resolution. None authenticates the historical bytes or extends a resolution-only lower bound to this mixed system. Targeted review of `konard/p-vs-np/scripts/proof_status.json` (Git blob `93b77ed3d8fe456f81c690035f45f07910a247f2`) and `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` (blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`) found no native R_mix341 accepted-byte authority.

**Not first discoveries:** LSPV-5/414 and LSPV-1/556 had found high-coordinate ghost masks; LSPV-3/551 and LSPV-1/557 had found accepted SAT sources; LSPV-2/538, /539 and /543 had previously addressed support typing, original-source binding and JSON lexical ambiguity. The additional result here is a concise **unmodified-checker sufficient-condition theorem** simultaneously excluding these failure classes, with an executable, pinned original-verifier regression battery. The theorem does not assert complete repair or a unique minimal condition set.

## Theorem 559.1: sufficient original-source and typed-soundness conditions (PROVED/RESTRICTED)

Fix the exact original checker Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. Let `P` be any packet on which this checker returns acceptance for every included graph fixture. For each fixture `f` fix *independently* a signed original clause array `F=(C_1,...,C_m)`. Let `E=|f.graph.edges|` be the original-variable count. Assume, in addition to the checker's actual passing predicates:

**(G1) Source binding and primitive literals.** `F` has the same number and exact ordered signed literals as `f.clauses`, occurrence by occurrence; every signed literal in `f.clauses` is a primitive, nonzero, safely represented integer. The independent source is read-only and not replaced by a packet-controlled field.

**(G2) Exact charge type.** Every `f.charges[v]` is the JavaScript number `0` or `1`, not a string or coercible object.

**(G3) Actual support arrays.** Every paid `AND3` record's `support` is an actual array; the original checker's equality, membership and table predicates remain required to pass.

**(G4) No unauthenticated affine coordinate.** At every paid `AND3` row annotation, its parsed BigInt mask `M` is nonnegative and `M<2^E`. No canonical hexadecimal spelling is required, as different in-range BigInt spellings can have the same meaning.

Then every original SOURCE factor represents its corresponding original `F` clause; every accepted paid AND3 factor and row annotation is a sound Boolean consequence/equivalence on the `E` original variables; every paid XOR is an exact GF(2) sum; and the terminal row `0=1` is a sound contradiction. In particular, **`F` is UNSAT**. Within the accepted graph-fixture language, the checker counts each new paid creation identity once, in topological order; the native fixture still requires exactly `4V-1` paid nodes. The theorem makes no claim about a complete all-input CNF refutation language.

**Proof.** The original checker asserts a simple cubic graph with correctly indexed edges, four source clauses per vertex, three signed incident edge variables per clause, mutually distinct forbidden patterns, and exactly four patterns opposite the vertex's asserted charge. Under G1 and G2, each source group is therefore precisely the four-clause Boolean CNF for

$$
x_{e_1(v)}\oplus x_{e_2(v)}\oplus x_{e_3(v)}=\chi_v.
$$

The checked global parity of the numeric bits is odd. Adding all vertex equations over GF(2) cancels each undirected edge twice and yields `0=1`, so the original signed source is UNSAT.

For derivational soundness, induct on the order of paid records in the checker's `byId` Map. SOURCE factors have truthful 3-variable tables by explicit local evaluation of their G1-bound signed clauses. In a paid AND3 the checker's parent lookups require previous nodes and distinct parent IDs. Given G3, the checked list length, uniqueness and numeric inclusion imply that the child support is exactly the set-union of the parents' supports, rather than an ill-typed string with coercive membership. Its exhaustive at-most-eight-row table test enforces the exact conjunction. When an affine annotation exists, the checker's low-position scope condition, its eight-row equivalence test and G4 establish equivalence of the annotation on **all E original Boolean coordinates**, with no uncontrolled high-variable term. For XOR, exact `BigInt` mask XOR and numeric bit-RHS XOR are checked against two preceding valid row annotations. Thus every derived factor/row is sound under the original signed clauses. The final checked zero-mask RHS-one row is impossible, and the original source is unsatisfiable. The checker also checks global fresh identities and prior parent lookup, so distinct paid DAG node identities are charged once rather than once per descendant. QED.

**Important scope qualification.** This theorem does NOT prove that the recovered verifier accepts all legal proofs of any authenticated historical R_mix341 calculus. It does NOT assert that simply dropping all non-G1-G4 packets from an abstract proof-space preserves minimum native work. In fact doing so could *increase* the minimum by excluding valid native shortcuts. For lower bounds, unknown legal steps must be MAY-overapproximated or normalized with a separately proved non-increasing-cost theorem.

## Theorem 559.2: high-bit equivalence failure, and exact boundary (PROVED/RESTRICTED)

For an AND3 factor with support confined to original coordinates `0,...,E-1`, consider a claimed affine row with any nonzero mask coordinate `j>=E`, where that coordinate is an unconstrained additional Boolean variable. Holding every original coordinate fixed and flipping only `x_j` leaves the factor truth value unchanged but flips the claimed parity-equation truth value. Hence the row cannot be exactly equivalent to the factor on the extended assignment domain. Conversely, if the row has no such high bits, the recovered checker's low-bit scope and full factor table test already establishes equivalence on all original E-bit assignments, under G3 and its accepted predicates. Thus **G4 characterizes the missing coordinate-range firewall** in this correctly typed recovered fragment. This is a restatement/strengthening of the already known ghost-mask deficiency, NOT a new full-native normalization theorem. If some *future authenticated* full calculus legitimately defines auxiliary coordinates and restricts their values, this unconstrained-bit lemma must not be used to remove those definitions.

## ITERATE: pinned original-checker proof replay and hostile controls

Reproducibility script: [`experiments/arc/lspv1_559_native_guard_kernel.cjs`](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_559_native_guard_kernel.cjs), Git blob `f442ded856ea02f886509af8653f1a9a70e5bc64`. Pinned original producer `4081022e8a3841d79f751a3d3a7a10decbb026da`, original unchanged checker `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`, prior accepted-SAT counterfeit `706947c767361e7c979b8208677eb983d33838f4`. Raw complete results: [`results/raw/arc/2026-11-10_1700_LSPV1_559_NATIVE_GUARD_RAW.json`](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-10_1700_LSPV1_559_NATIVE_GUARD_RAW.json), Git blob `99b8225d47e12623042899f28a6813f97b67fb76`.

The complete published script was **actually executed in hosted V8**, with emulated Node filesystem, path, Git blob SHA lookups and VM API, while the **mathematical bodies of the original producer/checker remained unchanged**. Its source passed syntax compilation. **No native OS Node CLI run or repository-wide preflight is claimed**. The source produced 20 program-level assertion groups plus the original checker's own recorded assertions.

| Tested original-checker packet/control | Original checker | Four-part guard / outcome |
| --- | --- | --- |
| All seven original graph fixtures | ACCEPT, 30,714 original checks | All seven pass |
| String charge `"1"` instead of numeric `1` | ACCEPT, 1,401 checks | G2 rejects |
| String `"012"` instead of array AND3 support | ACCEPT, 1,401 checks | G3 rejects |
| In-range decimal mask `"7"` instead of `"0x7"` | ACCEPT, 1,401 checks | Guard accepts, semantically equal |
| Two paired out-of-range ghost mask bits | ACCEPT, 1,401 checks | G4 rejects |
| Unchanged fixture with changed independent external source | ACCEPT, 1,401 checks | G1 rejects |
| Previously published counterfeit SAT source | ACCEPT, 2,273 checks | G2 rejects; **64 models**, first model encoded as integer mask 4133 |
| Wrong low affine bit | REJECT | Negative semantic control |
| Out-of-range SOURCE literal | REJECT | Negative source control |
| Repair counterfeit charge back to numeric 1 | REJECT | Coercion vulnerability localized |
| Repair counterfeit AND3 support back to array | REJECT | Coercion vulnerability localized |

All 11 grouped cases passed their expected outcomes. The accepted SAT source contains 48 original signed 3-CNF clauses on 18 variables; all `2^{18}=262,144` assignments were exhaustively checked, showing precisely 64 satisfying models. This accepted-byte failure of the *incomplete* fixture checker had already been independently reported by LSPV-3/551-554 and LSPV-1/557.

**Separate resource ledger.** `W` counts globally distinct paid unit-rule creations; the K4 baseline and its hostile source-preserving variants have 15 paid nodes. Raw certificate bytes and host verification assertions differ, and neither is actual algorithm-discovery time, certificate-bit complexity, machine span or simultaneous peak working space. This experiment did not measure RSS or time-space tradeoffs. Source authentication and any new implementation's parsing/strict guards are additional physical runtime costs. A sound packet validator does not solve SAT in P.

## Exact global objective and dependency ledger

For any *eventually authenticated* fixed history-aware calculus `R`, its logical minimum must remain

$$
W_R(F)=\min_{\pi\in\operatorname{Ref}_R(F)}
\sum_{v\in\operatorname{PaidIDs}(\pi)}
w(\operatorname{rule}(v)),
$$

with `Ref_R(F)` ranging over **all** valid externally source-bound complete refutation DAGs, free optimal selection of branching/learning/auxiliaries/sharing/reconvergence and all native legal shortcuts. Count each paid identity once. An AND branch requires **both** children to be discharged, whereas proof-construction options are OR alternatives; a context-dependent branch fact cannot enter a global empty-context goal without a legal discharge. None of those branching rules is added by the recovered checker. Discovery time, verification time, evidence bits, output time, span and peak space are different quantities.

- **[P2-D1] OPEN:** the historical accepted-byte grammar and actual authoritative checker for RES, LOCAL-CONVERT, paid DEF owner-facets, private/exported wires, and possible contexts/discharge/joins remain missing. This work supplies one *conditional soundness firewall for the recovered AND3/XOR subset*, not historical full-language authentication.
- **[P2-C3] OPEN:** an abstract complete configuration must include immutable original source bytes, actual parser/typed views, original source occurrence identity, shared DAG topology/paid IDs, DEF owners and facet views, active/discharged contexts, auxiliary freshness and state provenance. `alpha/gamma` and every legal transformer including unknown operations remain unproved. The guarded subset is an **under-approximation** and cannot prove a lower bound on all legal proofs.
- **[P2-B1] OPEN:** no superpolynomial lower bound for the complete freely optimal historical mixed proof calculus; published expander-Tseitin Resolution hardness is not hardness against the admitted native GF(2) shortcut, and alternative ER owners may give short proofs in a *different* completion.
- **[P2-B2]/B3 OPEN:** there is no same-preselected-calculus noncircular transfer from an arbitrary hypothetical polynomial-time SAT decider to a polynomial upper bound on `W_R`. Neither this checker, finite refutations nor an ER simulation in `R_fac` establishes B3.
- **[P1-01], [P1-03], [P1-04] OPEN:** no all-input deterministic SAT algorithm, both-label soundness or fully charged runtime/space theorem.

**Five-role handoff:** LSPV-3 should recover authoritative accepted bytes for externally bound SOURCE and paid DEF owner-facet-to-RES reference; LSPV-2 should check whether any purported native normalizer can transfer *every* accepted packet into strict typed semantics without cost increase and with original-source preservation; LSPV-4 should separately audit raw bytes, indexing/serialization and complete peak machine space for any checker interface; LSPV-5 should independently seek an accepted **SAT** packet meeting G1-G4 or a counterexample to the exact quantified guard proof. Continue 2 Route A / 3 Route B with ownership preserved.

## Publication and tracker reconciliation

Both root trackers were read completely and preserved: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 characters), `proof2.txt` blob `282c42f891b8528e2181a1f50de795e1d5b10e12` (948,636 characters). **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No load-bearing node is discharged, and the newly proved guarded-subset theorem is limited to an already separately typed reference language. Therefore no risky root tracker append was made. Root `main.tex` returned an empty content body despite blob `0fe79071499c352808d792f385c4b66299385f37`; leave untouched, report to LSPV-5 for safe recovery. No historical grammar, rule weight, five-role identity, schedule, timezone, enabled state or the two Route A / three Route B allocation was changed. **P versus NP remains OPEN.**
