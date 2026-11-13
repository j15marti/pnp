% LSPV-1 REPORT::613::2026-11-13T01:02:00-08:00
# LSPV-1/613: Exact charge-value observational congruence and an all-Boolean accepted SAT-source packet

**13 November 2026, 01:02 PST | General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED source-level local grammar theorem + COMPUTATIONAL original-checker replay. P versus NP OPEN.**

## Candidate before search and four falsifiers

**Candidate 613.1.** In the **unchanged archived /341 fixture verifier only**, every use of the JSON `charges` array factors through (i) the JavaScript bitwise XOR of its elements and (ii) strict comparisons of each local integer forbidden-pattern parity against the corresponding charge. Consequently, replacing a charge by any other JSON value with the same two observations leaves the checker verdict unchanged, provided all other packet fields are held fixed. In particular, with exclusively Boolean charges, the local parity comparisons become vacuous, while the total XOR requires an odd number of `true` entries.

Predeclared falsifiers: F1, a third executable charge-dependent condition invalidates the congruence. F2, changing the known accepted vertex-5 charge `"0"` to `false`, `null`, `[]`, `[0]`, or `{}` changes acceptance. F3, making *all* 12 charges Boolean with one `true` rejects despite the unchanged signed SOURCE/proof. F4, a same-bitwise-value **numeric** 0 incorrectly passes the source parity check, or an all-false vector incorrectly passes the total parity gate. Additional controls corrupt an AND3 table and a terminal GF(2) row.

## Original executable and exact lemma

Immutable original checker `experiments/arc/lspv2_341_independent_verify.js` has Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. It is a restricted standalone SOURCE/AND3/XOR cubic-fixture verifier, **not** a source-authenticated checker for full historical `R_mix341`.

The only two syntactic sites reading `f.charges` in the original mathematical verifier are:

```js
assert(f.charges.length===V,"charges size");
assert(f.charges.reduce((x,y)=>x^y,0)===1,"odd parity charge");
// For each original clause c at vertex v:
let parity=loc.reduce((x,y)=>x^y,0);
assert(parity!==f.charges[v],"source forbidden pattern parity");
```

The length check is separately fixed by the theorem. Let `Q` be the set of JSON-parsed arrays of the same length. For charge vector `q` define the observed global parity
$$
X(q)=q_0\mathbin{\hat\ }q_1\mathbin{\hat\ }\cdots\mathbin{\hat\ }q_{V-1}
$$
where each operation has exact ECMAScript 32-bit numeric XOR semantics; and define for each original clause occurrence `c` the Boolean `B_c(q)=[p_c !== q_{v(c)}]`, with integer `p_c\in\{0,1\}`.

**Theorem 613.1 (exact fixed-packet charge congruence, PROVED/RESTRICTED).** For any two JSON-parsed charge arrays `q,q'` of length `V`, fixing the graph, signed source clauses, witnesses, entire paid proof DAG, source IDs, contexts (none in this fragment), final row and all other fields, if
$$
X(q)=X(q'),\qquad B_c(q)=B_c(q')\quad\text{for every SOURCE occurrence }c,
$$
then the unchanged checker accepts `(F,q)` if and only if it accepts `(F,q')`, and traverses the same assertion count and identical native proof records.

**Proof.** The two displayed computations are the complete charge-dependent reads in the pinned original source. Replacing `q` by `q'` with the same observations preserves each conditional assertion and therefore the entire subsequent execution, including factor tables, XOR rows, source ancestry and terminal checking. For JSON Boolean charges, `p_c` is a Number and `q_v` is a Boolean, hence `p_c !== q_v` is always true, independent of the signed pattern. Bitwise XOR maps Boolean `true` to 1 and `false` to 0, so `X(q)=1` exactly when the number of true values is odd. The theorem concerns accepted JS byte-object semantics, **not** sound Boolean inference. QED.

**Consequence for P2-D1:** A schema declaring `charge: 0 | 1`, `charge: string`, or even `charge: number` would omit genuinely accepted packets. Semantic source pinning cannot be inferred from either a successful original-checker run or the global odd-XOR field. Unknown historical full-rule behavior remains MAY.

## Original checker packet and falsification

Reused the **already published** independently generated LSPV-1/609 fixture, original accepted Git blob `8d6d9bc7f2940a77edf2a07fcb72af111ba5b928}`, with 12 graph vertices, 18 original edge bits, 48 original signed width-three clauses and 47 distinct paid AND3/XOR nodes. The source itself is **SAT**, with exactly 64 independently enumerated models and first satisfying assignment `000000010010000001`. The present experiment keeps every SOURCE occurrence, deletion witness, signed clause, entire proof DAG and String-supported final AND3 step unchanged, modifying only `charges`. This is therefore an intentionally **false refutation accepted by a defective verifier**, not a proof of UNSAT.

The following original-code hosted V8 executions passed:

| Charge field mutation | Native verdict | Native assertions |
|---|---|---:|
| Previously accepted mixed numeric / `"0"` baseline | ACCEPT | 5,155 |
| All Boolean: `[true,false,...,false]` | ACCEPT | 5,155 |
| All Arrays: `[[1],[0],...,[0]]` | ACCEPT | 5,155 |
| One `true`, remainder `null` | ACCEPT | 5,155 |
| One `true`, remainder JSON `{}` | ACCEPT | 5,155 |
| Only vertex-5 `"0"` changed to `false` | ACCEPT | 5,155 |
| Only vertex-5 changed to numeric `0` | REJECT | source parity |
| All `false` | REJECT | odd XOR |
| One `true`, remaining numeric zero | REJECT | source parity |
| All Boolean, corrupt AND3 table | REJECT | conjunction |
| All Boolean, corrupt terminal RHS | REJECT | GF(2) |

A second targeted set replacing only the vertex-5 charge accepted twelve different nonnumeric JSON forms (including `null`, `[]`, `[0]`, `{}`, `""`, and `"0x0"`) while the numeric zero and XOR-changing values rejected. These are **fully executed unchanged-original-body tests in hosted V8**, using only mocked `fs.readFileSync`, process arguments and console output. They are not independent OS Node execution.

This run publishes an actual all-Boolean fully formed packet, not only a table of expected local values. It is serialized as 28,165 UTF-8 bytes of formatted JSON; compact content serialization has 10,735 characters. Native logical record count remains 47; the unchanged checker reports 5,155 assertion groups. These are not fixed historical `R_mix341` weighted charges, proof-construction time, span, or measured peak memory.

## Reproducibility and evidence

- Unchanged source checker: `experiments/arc/lspv2_341_independent_verify.js`, Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`.
- Immutable source baseline: `results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_SAT_ACCEPTED.json`, Git blob `8d6d9bc7f2940a77edf2a07fcb72af111ba5b928`.
- Reproducer: `experiments/arc/lspv1_613_native341_charge_congruence.cjs`; pins original Git blobs and runs the **unmodified checker as a separate Node OS process** when executed in a full checkout.
- New complete all-Boolean packet: `results/raw/arc/2026-11-13_0102_LSPV1_613_ALL_BOOLEAN_SAT_ACCEPTED.json`.
- Raw hosted execution ledger: `results/raw/arc/2026-11-13_0102_LSPV1_613_CHARGE_CONGRUENCE_HOSTED_RAW.json`.
- The OS reproducer has **not** been executed in this hosted run. Its OS replay remains for independent LSPV-5 falsification. Full repository preflight and LaTeX compilation are also not claimed.

## Corpus, preceding results and literature

Read both root trackers (proof1.txt Git blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`; full proof2.txt immutable blob `f678f707880da4dfc97dabf778430c6dc816cb1f`), issue #3 and recent comments, `AGENTS.md`, `CODEX.md`, research skill, latest five-role handoff, original checker /341, separate /386 dispatch evidence, actual LSPV-1/539, /609-/612, LSPV-2/539,/593, LSPV-3/549,/608, LSPV-4/549,/557,/579, and LSPV-5/520. Relevant 539-549 results remain separately scoped. Also reviewed contemporaneous PROVED/RESTRICTED charge-coercion, shared-DAG and CEGAR evidence.

**Prior-art honesty:** LSPV-3/582 and LSPV-1/609 had already demonstrated checker-accepted SAT sources through charge coercion; LSPV-4/557 had tested a Boolean positive and even numeric fractional padded charges on a *different* SAT fixture. The old verifier's unsoundness and Boolean coercion are **not** discoveries of 613. The increment is a complete fixed-packet observational-congruence theorem, the all-Boolean/all-Array/all-null equivalence classes on the independently generated /609 fixture, hostile controls, and a separately published native accepted all-Boolean certificate. This remains a restricted parser-characterization lemma, not closure of any main proof obligation.

Primary sources: ECMAScript 2026, [strict equality / IsStrictlyEqual](https://tc39.es/ecma262/2026/#sec-isstrictlyequal) and [bitwise XOR](https://tc39.es/ecma262/2026/#sec-binary-bitwise-operators-runtime-semantics-evaluation); Cook and Reckhow, JSL 44(1), 1979, [doi:10.2307/2273702](https://doi.org/10.2307/2273702); Cousot and Cousot, POPL 1977, [doi:10.1145/512950.512973](https://doi.org/10.1145/512950.512973); Clarke et al., CAV 2000, [doi:10.1007/10722167_15](https://doi.org/10.1007/10722167_15). ECMAScript semantics transfer directly to this JavaScript checker. Proof-complexity and CEGAR results supply methodological obligations, not unverified mixed-rule transfer theorems.

## Main dependency and interface ledger

**[P2-D1] OPEN.** This characterizes a previously underdocumented accepted-byte property of /341. Complete historical `R_mix341` including SOURCE, RES, AND3, GF(2), LOCAL-CONVERT, paid DEF/defining facets, wire freshness/export/private boundaries, branches, weakening, contexts, discharge, joins, deletions and all tariff values remains unauthenticated as **one** checker. The /386 checker is not composable by assumption, and CANON1/2/2R cannot substitute.

**[P2-C3] OPEN.** Any cost-sound abstraction must include real accepted malformed charge values if it models /341, even if a *separate* sound typed reference checker rejects them. Concrete states must still carry exact original-source bytes, entire shared DAG, first-use paid owners, contexts/discharge, definitions, provenance and all legal rule transitions. No `alpha/gamma`, goal-preserving all-rule simulation or non-overcharging proof exists.

**[P2-B1] OPEN.** No superpolynomial all-rule minimal shared-DAG work bound is established. All GF(2), extension, preprocessing, branch, reconvergence, semantic and algebraic shortcuts remain eligible.

**[P2-B2/B3] OPEN separately.** A short unrelated proof, existence of a polynomial SAT algorithm, or this checker behavior gives no polynomial optimal work in the historical same fixed calculus without an explicit transfer theorem. **[P1-01/03/04] OPEN. P versus NP remains OPEN.**

**DUPLICATION / CONTRADICTION:** /613 is consistent with /609 and /557; it broadens the **observed admitted JSON charge types** on a second published satisfiable-source packet and provides the exact congruence criterion. Any claim that only String-valued charges cause the defect is refuted; the defect stems from the mixed use of strict comparison and coercive XOR. It does not contradict /610's separate sufficient Array-support soundness condition, since the accepted /613 packet still has an actual String-valued AND3 support.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The root proof files retain their OPEN labels and SHA values. No role/automation identity, schedule, Pacific timezone, route allocation, ownership boundary, tariff or historical research weight was changed. Two Route A and three Route B labels remain in force.

**Handoff:** LSPV-2 (Route A), seek the missing single authoritative externally source-bound original mixed-rule dispatch. LSPV-3 (Route B), incorporate the charge observational signature into the exact recovered byte grammar; do not confuse it with semantic parity. LSPV-4 (Route A), keep UTF-8 evidence bytes and physical verifier costs separate from distinct paid owner work. LSPV-5 (Route B), run the new OS reproducer, independently test Boolean/Array coercion and try a no-String-support terminal counterexample. LSPV-1 retains P2-D1→P2-C3→P2-B1 quantifiers and B2/B3 firewall. Next load-bearing target: authentic historical RES→AND3 or paid DEF→LOCAL-CONVERT acceptance with external signed-source binding.

% END_OF_VERIFIED_REPORT::LSPV-1::613
