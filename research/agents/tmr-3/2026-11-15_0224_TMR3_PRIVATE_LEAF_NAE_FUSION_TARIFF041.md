# TMR-3/041: signed private-leaf NAE elimination, same-machine physical cost and explicit-output tariff

**2026-11-15 02:24 PST | LEAFNAE080 | PNP Time-Space Tradeoffs.** Governing directive: `research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md`, Git blob `54c9177fc211dfca6c94d89d6ebbf3f3908809d6`. **Status: PROVED/RESTRICTED for the exact mathematical class and physical output-tape tariff, pending independent peer review; finite V8 tests COMPUTATIONAL. P versus NP OPEN.**

## 1. Candidate and four falsifiers fixed before the literature/corpus audit

**Candidate:** TMR-2/040's exponential rational-rank and fooling-cover proper-3CNF `Q_k` remains uniformly polynomial-time satisfiable even after *arbitrary individual variable sign complements*, arbitrary bijective relabeling, arbitrary clause/literal order, and exact duplicate clauses. A **private-leaf NAE** source recognizer and witness constructor, with paid full parsing and checking, should repair the prior *degree-only* witness shortcut. The genuine one-output-tape witness emission phase should have an exact seven-column physical tariff, with fused WRITE+HALT, independently of the prior input-endmarker tariffs.

**Falsifiers:** (1) a sign complement makes the recognizer's extension unsatisfying; (2) grouping duplicate/unmatched signed clauses falsely authenticates an NAE block; (3) a shared variable is reused as two nominal "private" variables; (4) a physical step writes an output bit and halts at unit cost, falsifying an independently additive interface+terminal price. The fourth is a real cost counterexample to the invalid `(1,1)` tariff. A fifth transfer guard is that a SAT **decision** machine need not print a witness.

## 2. Exact source class and elimination theorem

Let `F` be a properly parsed finite 3-CNF, with three distinct variable identifiers in each clause. Deduplicate exact clauses, sorting within each clause by *actual variable identifier* and sign (never indexing memory by the numerical value of an identifier). Call the resulting clause set `U`. The class `PL-NAE` is defined by all three conditions:

1. Every clause `C` in `U` has its *literalwise complementary clause* `bar C` in `U`, and the paired `{C,bar C}` form one NAE constraint. Two different polarity-pairs on the same variable triple count as **two groups**, not one.
2. Every distinct clause belongs to exactly one complementary pair; there are no unmatched source clauses. Duplicate original copies are retained for source provenance, but have no extra logical force.
3. For each pair/group `e`, at least one of its three variables occurs in **no other distinct group**. Choose one such `v_e` by the smallest signed-ID-independent absolute identifier. Such selected variables are pairwise distinct.

Write `S` for the variables appearing in two or more groups, `L` for one selected private variable per group, and `R` for all other unselected variables. The defining relation of a pair is

$$
\operatorname{NAE}(\ell_1,\ell_2,\ell_3)
=(\ell_1\vee\ell_2\vee\ell_3)
\wedge(\neg\ell_1\vee\neg\ell_2\vee\neg\ell_3).
$$

**LEAFNAE080-A, exact source elimination theorem (PROVED/RESTRICTED, peer review OPEN):** For **every** assignment `s` to the shared variables `S`, there is an extension `a` to all source variables satisfying `F`. Therefore

$$
\boxed{\exists_{V(F)\setminus S}\,F\ \equiv\ \top.}
$$

**Proof:** Set the unselected private variables `R` to zero, preserving the arbitrarily fixed values of `S`. Process groups in any order. For a group, evaluate its two literals not using the chosen private variable `v_e`. If their values differ, either setting of `v_e` satisfies NAE; select zero. If both values are `b`, choose `v_e` so its *literal value* is `1-b`. Each `v_e` occurs nowhere else, so its assignment cannot invalidate a prior or later group. Each NAE group now contains a true and false literal and satisfies both original complementary clauses. All source clauses belong to groups, so `F` is satisfied. This is constructive and handles arbitrary signed literal gauges, not just positive NAE triples. QED.

This is an *existential cheap quotient*, not a zero-cost physical TM operation: discovering the pairing/private leaves and producing a witness still incurs charged transitions.

**Application to TMR-2/040:** `Q_k=AND_i NAE(X_i,Y_i,W_i) AND_(i<j) NAE(X_i,X_j,Z_ij)` belongs to PL-NAE, since every group has a private `Y_i`, `W_i`, or `Z_ij`. Its primal graph contains `K_k` and its original `X`-by-rest evaluation matrix has exact rank `2^k` and 1-rectangle cover `2^k`, *as already proved by TMR-2/040 and independently checked in TMR-5/037*. Under signed gauge changes, those numerical measures remain equal for the **tracked corresponding partition**, because row and column assignments are permuted. Yet `exists_(Y,W,Z) Q_k` is the constant TRUE relation for **all** X assignments. This is why the 2^k evaluation rows do not represent 2^k compulsory SAT-decision actions.

## 3. Concrete uniform decider and physical time-space ledger

Fix one deterministic finite-alphabet multitape machine `D_PL`, with one left-initialized locally moving read-only input head and a fixed number (at most six) of writable tapes. Source input is a standard self-delimiting signed proper-3CNF encoding, for example the same unary-width/unary-clause-count strict-termination grammar qualified in TMR-3/039-040; `L` is its **actual bit length**, not the largest numeric identifier. Every head move, ID comparison, counter update, input reread, sorting/deduplication, cached record, branch, output, and fallback operation is paid at one physical transition per primitive TM step. Neither the JavaScript audit nor this report claims that a compiled finite-state transition table was executed.

`D_PL` first parses the complete source and EOF, rejecting malformed inputs. It copies canonical signed clauses into work tapes, compares and removes exact duplicates, pairs clauses with their exact literal complements, checks that no clause is unmatched, then compares variable identifiers across all groups to find a genuine private leaf for each. It produces the constructive assignment from section 2 and *independently verifies every original clause*. It accepts only when the independent verification succeeds. If the source is well-formed but the PL-NAE detector fails, it runs a fixed exhaustive complete SAT search and returns the correct label. The fallback is deliberately not polynomially bounded.

**LEAFNAE080-B, conservative physical upper bound:** On every valid PL-NAE source, the exact abstract algorithm above has a fixed finite-alphabet locally moving multitape implementation satisfying

$$
T_{D_{\rm PL}}(F)=O((L+1)^6),\qquad
S_{D_{\rm PL}}(F)=O((L+1)^2).
$$

No RAM hash, unbounded-word constant-time arithmetic, or numerical-ID-sized array is needed. One implementation uses serialized records of at most `O(L)` bits each, at most `O(L)` original clauses/groups/variables, and `O(L^2)` total visited writable record cells. A full repositioning/copy/compare pass over the fixed record tapes takes at most `O(L^2)` local moves. The source parser uses polynomial sweeps and bitwise counter updates. Clause pairing and deduplication need at most `O(L^2)` record comparisons; private-leaf detection at most `O(L^2)` identifier comparisons; witness construction and original-clause replay at most `O(L^2)` further comparisons. Binary counters and record sweeps can be implemented with finite-state fixed-tape routines, each comparison costing at most `O(L^2)`; the loose `O(L^6)` budget also absorbs repositioning, parsing and bookkeeping. An explicit sparse variable/value witness record has at most `O(L)` used identifiers each `O(L)` bits and therefore at most `O(L^2)` output bits. This is an existential compilation upper bound, not a clocked native-machine benchmark or a full transition-list proof.

The same **one fixed `D_PL`** accepts every source obtained from `Q_k` by independent variable complementation, bijective relabeling, clause/literal permutation or duplicate-clause insertion, in polynomial paid time measured in the **new encoded length**, and correctly decides all other well-formed formulas by exhaustive fallback. In contrast, TMR-2/040's particular degree-only assignment fails on `Q_2` after complementing `X_1`: the degree assignment makes `NAE(neg X_1,Y_1,W_1)=NAE(1,1,1)`, whereas the private-leaf method sets a leaf to restore NAE.

**Resource segregation:** abstract logical group work is not physical time; elapsed sequential machine steps are the charged total; parallel span does not follow from a sequential bound; evidence length means actually emitted witness bits, not 2^k semantic rows; messages are absent; peak writable cells include *simultaneously* live tables, counters, scratch and outputs; rerereads, retention, retrieval and recomputation remain paid. No mandatory proof DAG is assumed.

## 4. One exact genuine physical transition-class tariff

Qualify a **separate post-discovery explicit-witness output subprotocol** in which a single designated output tape has `B>=1` prescribed consecutive cells, initially blank, and a successful terminal goal requires all `B` cells contain the *correct complete explicit sparse variable/value certificate* and the emitter has halted. The source, program, control, input/work/output tape/head positions, paid history, full source provenance and pending output contract remain concrete. The other tapes can perform arbitrary cached/recomputed work. A single physical step writes at most one cell on that **one** output tape. This is an authentic local physical class; the higher-level SAT witness search is not declared free.

All physical steps cost one and no zero-cost primitive steps exist: `cl0` and zero-cost SCCs are the identity. In canonical seven-column order define

$$
p(C)=(0,0,0,0,0,\ B-\#\{\text{nonblank required output cells}\},\
{\bf 1}[\text{unfinished and nonhalted}]).
$$

The signed one-step discharge of the interface component lies in `{-1,0,1}`: writing a blank removes one, overwriting a nonblank leaves it unchanged, erasing a nonblank reinstates one. The machine flag can drop by one only on HALT. Every actual physical step, including input reread, shared computation, extra definitions, storage, head moves, final write and halt, is covered by these signatures. No hypothetical zero-cost step is invented.

| Authentic rule class | `w` | `Delta_int` | `Delta_machine` |
|:--|--:|--:|--:|
| Move, recompute, cache, or overwrite nonblank | 1 | 0 | 0 |
| Write one blank output cell | 1 | 1 | 0 |
| Halt without new write | 1 | 0 | 1 |
| Write the final blank output cell and halt in the same step | 1 | 1 | 1 |
| Erase one filled output cell | 1 | -1 | 0 |
| Erase one filled output cell and halt | 1 | -1 | 1 |

A real final WRITE+HALT transition has discharge `(1,1)` for cost one. This **falsifies** charging one independently to the interface and one to HALT. The full nonnegative cone for these two participating components is exactly

$$
\boxed{\lambda_{\rm int}\ge0,\quad\lambda_{\rm machine}\ge0,\quad
\lambda_{\rm int}+\lambda_{\rm machine}\le1.}
$$

With the other five components defined identically zero, the exact rational certificate is `lambda=(0,0,0,0,0,1,0)`. Every certified completed goal has zero potential; one-step undercharging and telescoping establish the genuinely model-matched **restricted output cost** `W_emit>=B`. For initial vector `(B,1)`, the linear primal is `max B*lambda_int+lambda_machine=B`, and the exact dual one-row multiplier `y=B` is feasible and attains the same value. This is a one-output-tape sequential bit-emission lower bound, **NOT** a lower bound of `B` for an ordinary SAT decider that returns only a one-bit YES/NO label, not a lower bound on constructing the witness, and not a claim about multi-output-head parallel work.

The independent six-row JSON tariff and signed enumeration appear in `results/raw/tmr/2026-11-15_0224_TMR3_LEAFNAE080_TARIFF_MATRIX.json`.

## 5. Exact execution, hostile controls, provenance

The single exactly executed ES2020 function was serialized by `Function.toString()` into `experiments/tmr/tmr3_private_leaf_nae080.js`. Standalone Node wrapper was not separately executed. The raw JSON from this execution is immutable in `results/raw/tmr/2026-11-15_0224_TMR3_LEAFNAE080_V8_RAW.json`.

**39,457 exact assertions, zero failures** in the primary witness/tariff audit. A SECOND, independently coded ES2020 verifier, `experiments/tmr/tmr3_leafnae_projection081.js`, executed **6,150 assertions, zero failures**, including **2,976 signed private-leaf extensions across every core assignment** in its seeded bounded finite hypergraphs and eight rejected full-eight-clause UNSAT assignments. Raw second result: `results/raw/tmr/2026-11-15_0224_TMR3_LEAFNAE081_PROJECTION_RAW.json`. This independently tests the universal existential-projection quantifier, not just the canonical allzero core. : `Q_k` for k=2..7; 288 seeded arbitrary-gauge/renaming/literal/clause permutation/duplicate tests; 1,000 seeded random valid proper-3CNFs through six variables (witness checked against brute-force SAT for false-positive prevention); 6 malformed/unmatched controls; the explicit flipped-X1 failure of the old degree witness; the full eight-clause UNSAT core and proper affine four-clause partial group controls; 36,090 exhaustive signed single-output-cell overwrite/erase and optional-HALT rows for output regions B=1..6; 91 exact rational grid points with denominator 12 satisfying the joint tariff cone. These are finite **COMPUTATIONAL** controls, not a compiled physical TM or an asymptotic proof.

| Hostile control | Result or boundary |
|:--|:--|
| Horn, dual-Horn, 2-SAT/Krom | Not needed for accepted class; unmatched/width-two source does not permit false positive. Fallback remains exact |
| XOR/complete Tseitin 3-CNF | Four unsigned parity clauses lack the required one-pair-per-group private leaf; no false declaration |
| High treewidth, non-Schaefer, exponential rank and 1-rectangle cover | Prior Q_k properties coexist with a full cheap source witness and tautological existential shared-core projection |
| Autarky, private leaves, equality | Constructive private-leaf assignment is a total satisfying autarky; equality and mixed constraints outside the class use fallback |
| Arbitrary signed gauge, rename, shuffled records, duplicate copies | Correctly authenticated after comparisons; existing degree-only witness genuinely fails a sign-gauge test |
| Compact circuit, extension, learning, Gaussian reasoning | All legal alternatives stay allowed by the total decider; this is a *positive* cheap route, not an alleged universal necessity |
| Caching, rereading, recomputation, sharing | Every physical operation has a charged step in the upper-bound program and only one designated output cell can change per transition |
| Padding and large identifier magnitudes | Charges actual `L`-bit records and dense used-variable entries; no array sized by the numeric identifier |
| Zero-cost shortcut | No zero-price native TM transitions; logical existential projection is not a physical zero-cost computation |
| /341 and /386 | Historical /341 **FAIL** on full accepted UNSAT authority; /386 **RESTRICTED** to guarded odd-charge fragment, neither modified |

This extends TMR-2/040's original *positive-polarity* degree witness and the TMR-5/037 rank/circuit guard control by preserving polynomial satisfiability under arbitrary source-variable complementation. The one-tape output tariff is structurally analogous to earlier TMR-3/037, but now states a complete **signed** physical row inventory with negative discharge and the strict witness-vs-decision goal separation. It does not claim novel NAE-SAT complexity classification.

**Corpus read:** Governing 2026-11-14 directive, November 13 TMR replacement, root proof1 full SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`; proof2 complete Git blob `930c5eeddafce656717f28055a7a9a755f44737c` (1,051,196 chars); main.tex complete Git blob `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34` (2,545,859 chars); current issue #3, AGENTS.md, CODEX.md, pnp-research skill, five current TMR handoff heads, original TMR-2/040 and TMR-5/037 proof/code/raw, TMR-3/040 and TMR-4/041 tariff/code/data, and original LEAD/0029 Lipschitz audit. Exact related prior work and overlaps are acknowledged above.

**Primary literature cross-check:** [1] Schaefer, *The Complexity of Satisfiability Problems*, STOC 1978, DOI https://doi.org/10.1145/800133.804350, establishes the general tractable-versus-NP-complete relational classification, not this program's physical bound. [2] Darmann and Döcker, *On simplified NP-complete variants of Not-All-Equal 3-Sat and 3-Sat*, 2019, https://arxiv.org/abs/1908.04198, shows NAE hardness survives some bounded-degree restrictions, without contradicting this *private-leaf* subclass. [3] TMR-2/040 and TMR-5/037 provide the exact Q_k rank/circuit-evaluation results that this run accepts at their original restricted scope.

**Barrier/transfer status:** The source quotient is paid to acquire, and this emitter cost is for an explicit-certificate goal. The same-system transfer from unrestricted fixed total deterministic SAT deciders to any *superpolynomial* dynamic fusion potential remains **OPEN**. No result here changes [P1-01], [P1-03], [P1-04], [P2-B1/B2/B3], or [P2-C3]. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root `main.tex` and all five scheduled agents unchanged. P versus NP remains OPEN.

**Next peer request:** TMR-2 independently verify the for-all-shared-assignment existential projection; TMR-4 embed the actual paid private-leaf routine as a MAY execution path and check the output tariff under arbitrary tape writes; TMR-5 attack the finite-alphabet O(L^6) compilation with a malicious variable-ID/duplicate/interleaving source; TMR-1 audit the distinction between Q_k's exponential evaluation rank and the constant existential projection.

END_OF_VERIFIED_REPORT::TMR3::041::2026-11-15_0224_PST
