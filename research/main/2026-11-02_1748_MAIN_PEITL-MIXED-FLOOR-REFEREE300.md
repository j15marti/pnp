# PEITL-MIXED-FLOOR-REFEREE300

**PNP Independent Proof Red Team — November 2, 2026, 17:48 PST**

**Status.** **PROVED/EXACT** for the source-floor theorem in the fixed Rmix341 model; **COMPUTATIONAL/EXACT FINITE** for seven authentic Peitl–Szeider instances and all 19 corpus controls; **FAMILY FAILURE** for the five-clause Resolution-hard candidate; **RESTRICTED FINITE LOWER BOUNDS** for the six-, seven-, and eight-clause instances; **OPEN** for their exact mixed optima, any superpolynomial mixed lower bound, B1, B2, B3, and P versus NP.

## Claim card

- **Claim ID:** PEITL-MIXED-FLOOR-REFEREE300.
- **Obstruction attacked:** finite formulas maximizing shortest Resolution length might remain hard after the same preselected mixed calculus is allowed.
- **Fixed calculus:** Rmix341 with zero-cost authenticated source clauses; unit-cost binary RES, exact constant-three-variable truth-table conjunction/normalization (AND3), binary GF(2) row addition (XOR), charged conversions, and charged source-independent variable-gate DEF instructions. All rules are sound, effective, and fixed independently of the inputs.
- **Cost:** distinct paid inference nodes in a shared contradiction DAG. The best legal derivation is selected freely; optimizer discovery is not charged to the minimum.
- **Exact finite question:** for a clause-minimally UNSAT formula with (m) source clauses, can contradiction be reached at the universal binary source floor (m-1)?
- **Falsifiers:** (F1) an authentic Resolution maximizer has a shorter legal mixed DAG; (F2) every authentic small maximizer attains (m-1); (F3) a source-floor miss alone certifies the full mixed optimum; (F4) a finite gap supplies B3 or a superpolynomial (\overline W_R) bound.

## Exact source-floor theorem

Let (F=C_1\wedge\cdots\wedge C_m) be clause-minimally UNSAT. For a node (v), let \(\sigma(v)\) be the set of original clause indices in its ancestry. Soundness implies that the contradiction node has \(\sigma=\{1,\ldots,m\}\): omitting (C_i) would refute the satisfiable deletion (F\setminus\{C_i\}).

In Rmix341 every paid inference has at most two premises. Starting from (m) singleton source components, a binary node can reduce the number of ancestry components by at most one. Unary conversions and source-independent DEF nodes do not merge two indispensable source components. Therefore every refutation has at least

$$
m-1
$$

paid nodes. Equality forces all paid nodes to be binary source-merges, forces the two premise ancestries at every node to be disjoint, and forces the proof to be a full source-once binary tree. There is no cost left for a unary conversion, a source-free auxiliary definition, a repeated source, or a merge of overlapping ancestries.

Consequently, whether equality is reachable is decidable by a complete subset-partition dynamic program: for every nonempty source subset (S), retain every function obtainable by joining disjoint (A,B) with (A\dot\cup B=S). The implemented DP is deliberately a relaxation of Rmix341 at equality: exact clause and affine aliases are free, and AND3 is allowed whenever the output has essential support at most three. RES and XOR are exact. Charged conversions and source-independent DEF cannot occur in an (m-1)-node proof by the equality argument. Thus:

- if the relaxed DP reaches false, its recorded tree is a legal upper certificate when each tagged step is legal in Rmix341;
- if the relaxed DP does not reach false, no Rmix341 proof can have (m-1) nodes;
- the DP says nothing complete about (m,m+1,\ldots) nodes, where reuse, auxiliary definitions, conversions, and non-tree DAGs may occur.

This is an exact finite optimum certificate only when the lower floor and a legal upper witness coincide.

## Authentic corpus and result

The inputs are the 19 DIMACS files in `hardest.tar.xz` from Peitl and Szeider's `peitl/smu` repository. The upstream Git blob is `df4f0d28e5cf49f0d45bab7a89e630999b78f4b9`; the downloaded archive SHA-256 is `1fa6ca7c27763a5f49c3be631ce3c30369dde35da64fa2754014d0ae9197a59e`. The authors' `peitl/short-proof` v1.1.0 tool was downloaded with SHA-256 `3864dceb6df03b7d1be200893fdfc2f447766f3d3e1ddcbfb73f68090785d49a` and freshly reproduced the first seven displayed Resolution optima. Its reported length counts source clauses and derived lines, so the table subtracts (m) to match Rmix341's paid-node convention.

| authentic file | (n) | (m) | shortest Resolution lines | paid Resolution nodes | relaxed floor (m-1) reached? | certified Rmix341 result |
|---|---:|---:|---:|---:|---:|---:|
| `ssmu_1_2_1.cnf` | 1 | 2 | 3 | 1 | yes | (W=1) exact |
| `ssmu_2_3_1.cnf` | 2 | 3 | 5 | 2 | yes | (W=2) exact |
| `rsmu_2_4_1.cnf` | 2 | 4 | 7 | 3 | yes | (W=3) exact |
| `rsmu_3_5_1.cnf` | 3 | 5 | 10 | 5 | yes | (W=4) exact |
| `rsmu_4_6_1.cnf` | 4 | 6 | 13 | 7 | no | (6\le W\le7) |
| `rsmu_5_7_1.cnf` | 5 | 7 | 16 | 9 | no | (7\le W\le9) |
| `rsmu_6_8_1.cnf` | 6 | 8 | 19 | 11 | no | (8\le W\le11) |

The last three lower bounds are one above the universal floor because the complete relaxed tree DP excludes costs 5, 6, and 7 respectively; the Resolution optima supply the upper bounds. The DP performed 833, 2,231, and 6,615 pair tests and retained 82, 50, and 44 terminal full-source functions. These are restricted finite intervals, not global exact optima.

### Concrete mixed shortcut

The authentic five-clause formula is

$$
(\neg x_1\vee x_2)\wedge(\neg x_2\vee x_3)\wedge(x_1\vee\neg x_3)
\wedge(x_1\vee x_2\vee x_3)\wedge(\neg x_1\vee\neg x_2\vee\neg x_3).
$$

It has only three variables. Sequentially conjoin the five authenticated source truth tables using four binary AND3 nodes. Every intermediate and final function has essential support at most three; the final table is false. Clause minimality gives the matching four-node lower bound. Hence

$$
W_{Rmix341}(F)=4<5=W_{Resolution}(F)
$$

under the paid-derived-node convention. The raw artifact records the complete nested witness with exact source masks and truth tables; the independent verifier replays every operation. This is a genuine **FAMILY FAILURE** for treating this Resolution maximizer as mixed-hard. It does not show that all Peitl–Szeider maximizers are easy in Rmix341.

## Four falsifiers and dispositions

1. **F1: authentic finite Resolution maximizers retain their exact minimum in Rmix341. — FALSIFIED.** `rsmu_3_5_1.cnf` drops from five paid Resolution nodes to four legal AND3 nodes.
2. **F2: the source floor is always reachable once mixed rules are allowed. — FALSIFIED FINITELY.** Even the stronger relaxed equality DP excludes the floor for the authentic (m=6,7,8) instances.
3. **F3: exclusion of (m-1) determines the full mixed optimum. — FALSIFIED AS AN INFERENCE.** Above the floor, conversions, shared sub-DAGs, repeated sources, temporary growth, and DEF nodes re-enter. This run certifies only (6\le W\le7), (7\le W\le9), and (8\le W\le11).
4. **F4: the finite strict gaps establish a superpolynomial worst-case lower bound or B3. — FALSIFIED AS AN INFERENCE.** Seven fixed instances give neither asymptotics nor a conditional SAT-in-P bridge.

The optimizer's effort is irrelevant to these minimum statements by design. The producer enumerated all equality trees only to certify existence/nonexistence at the floor; this enumeration is not charged to (W_R).

## Controls and independent replay

All 19 authentic files were exhaustively checked UNSAT and clause-minimal. Every single occurrence-sign flip is SAT; this supplies same-source opposite-label controls and independently preserves the established sign-sensitivity lemma. Exact counts, signed clauses, deletion witnesses, sign-flip model counts, file bytes, and SHA-256 values are in the raw JSON.

Eight malformed DIMACS fixtures were rejected independently: missing header, bad keyword, count mismatch, out-of-range variable, missing terminator, duplicate literal, tautological clause, and negative dimensions. Odd-charge (K_4) Tseitin has zero models; the even-charge control has eight. The no-producer-import verifier independently reparsed all 19 files, enumerated labels/deletions/sign flips, reconstructed all seven floor DPs, replayed each positive witness, and repeated malformed and parity controls: **607 checks passed**.

Raw SHA-256: `2cd6e488eaf07930ed7eab3eed8b9d8433add3c2daaf543a005e7802c6c3dbd8`.

## B1/B2/B3 referee classification

This run proves none of B1, B2, or B3.

- **B1 remains OPEN.** No arbitrary total SAT decider is translated pointwise to Rmix341 proofs. A fast algorithm for this finite family would at most attack a pointwise claim and does not affect the finite mixed upper certificate.
- **B2 remains OPEN.** No relationship is proved between (\overline W_{Rmix341}(N)) and any decider's all-input worst-case runtime.
- **B3 remains OPEN.** Nothing here proves that SAT in P makes this same preselected Rmix341 polynomially bounded.

Correct classification: the five-clause result is a **candidate-family failure**. The three floor exclusions are **restricted finite lower bounds**. Neither is a transfer failure. A rejecting machine trace, nonuniform correctness axiom, instance-tailored rule, or free semantic jump is not used.

## Work and all-phase space ledger

The producer charges archive/file acquisition separately from logical cost. Its local phases include parsing, exhaustive model enumeration, every deletion and occurrence-sign neighbor, renamable-Horn detection, alias construction, subset-partition DP, witness extraction, parity and malformed controls, JSON serialization, and process overhead. The recorded producer run used 0.496 seconds and peak host RSS 10,880 KiB. It materializes truth tables, DP sets, source masks, and output; no sublinear-space or machine lower-bound claim is made. The verifier is a separately written executable and does not import the producer.

The logical certificates count shared inference nodes once. Encoding, validation, storage, retrieval, and recomputation are separate scheduled-machine costs. Any later machine transfer must retain

$$
s'\le\max\{\rho,\eta,\lambda,\lambda s\},
$$

where (\rho) covers every local phase. This run makes no FLMV exponent claim.

## Literature and project audit

Queries included “Peitl Szeider hardest formulas resolution shortest proof”, “saturated minimally unsatisfiable formulas hardest.tar.xz”, “minimum resolution proof length first ten”, “extended resolution lower bounds”, project searches for `Rmix341`, `VARDEF`, `AND3`, `SIGNED-EXPANDER-CAMOUFLAGE347`, `GRID-MINIMAL-HORN348`, `DEF-SUPPORT-COVERAGE346`, and `ARITY_WEIGHTED_HORN_MACRO346`, plus GitHub searches in `peitl`, `j15marti/pnp`, and `github.com/openai`.

- T. Peitl and S. Szeider, *Finding the Hardest Formulas for Resolution*, JAIR 72 (2021), 69–97, <https://doi.org/10.1613/JAIR.1.12589>. The paper's first shortest lengths are (1,3,5,7,10,13,16,19,22,26) when source axioms are counted. Its claims are Resolution-specific.
- Authentic corpus: <https://github.com/peitl/smu>. Shortest-proof implementation: <https://github.com/peitl/short-proof>.
- J. Krajíček, *The Case of ER*, in *Proof Complexity Generators* (2025), <https://doi.org/10.1017/9781009611664.009>. Strong lower bounds for extension-enabled systems remain a major barrier.

Current peer results were used adversarially: arbitrary signed incidence can still have an (m-1) mixed proof; high treewidth can coexist with a linear Resolution proof; source-independent VARDEF has an exact small finite calibration but source-bearing factor DEF remains undefined; and unit Horn macros can hide linear source evidence unless arity is charged. None supplies a representation-inclusive asymptotic invariant. No relevant OpenAI proof-complexity implementation was found. No novelty is claimed for the binary source-counting lemma or for the authors' finite Resolution optima.

The repository's prescribed pnp-research skill executable is absent from this partial local workspace, so that preflight could not be run locally; authenticated GitHub reads, ownership-safe paths, exact hashes, independent execution, and post-publication readback are used as the documented fallback.

## Exact next gap

Compute the **full** Rmix341 optima for `rsmu_4_6_1.cnf`, `rsmu_5_7_1.cnf`, and `rsmu_6_8_1.cnf`, allowing charged conversions, auxiliary definitions, repeated sources, and shared non-tree DAGs. An exact value above the source floor would be the first finite target for a rule-monotone invariant. Then extend or destroy that invariant on a growing nonaffine family. Independently, B3 still needs a theorem that SAT in P implies polynomial (\overline W_{Rmix341}) for this same fixed system. **P versus NP remains OPEN.**
