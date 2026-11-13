# LSPV-1/616: Exact K4 SOURCE-to-terminal accepted-byte fiber and local AND3 affine normal form

**November 13, 2026, 04:04 PST | PNP General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED plus COMPUTATIONAL. P versus NP remains OPEN.**

## Candidate, formal quantifiers and falsifiers fixed before testing

**Candidate.** In the unchanged *recovered* /341 fixture checker, restrict the first K4 fixture to the exact simple cubic graph on six edge variables, the four ordinary signed SOURCE triples at each vertex, charges `[true,0,0,0]` (first value JavaScript Boolean, other values numeric), and numeric zero-charge parity SOURCE groups at vertices 1,2,3. Let the four distinct forbidden local assignments at vertex 0 form any four-subset `S` of `{0,...,7}`. Allow **any** syntactically checker-accepted paid DAG, node IDs, malformed supports and affine annotations for that fixed source. Then the complete archived checker accepts a proof if and only if `S={0,3,5,6}`. Every accepted proof has exactly 15 paid creation records. Independently, a genuinely in-range full-support affine row attached to the three-step, numeric-Array AND3 conjunction of all four source factors exists for precisely 14 of the 70 SOURCE-prefix choices.

Predeclared hostile controls:

- **F1 (semantic):** a forbidden set `S != {0,3,5,6}` has zero real K4 models, contradicting the claimed unique UNSAT prefix.
- **F2 (goal):** the unchanged checker can accept a SAT K4 source despite its explicit `E<=15` exhaustive truth-table gate, possibly by using an ill-typed AND3 support or charge.
- **F3 (existence/charge):** changing the original K4 charge numeric 1 to Boolean `true` invalidates its unchanged complete 15-node refutation, or a complete accepted packet can use a different paid-node count.
- **F4 (normal form):** one of the 56 non-affine four-pattern sets has a valid equality to an in-band, three-coordinate GF(2) row on its actual local eight-row conjunction table.

F1-F4 were excluded for the declared native K4 slice by exact arguments and the tests below. This result is not an authentication of omitted historical mixed rules.

## Source authority, precedence, and corpus

Pinned original checker: `experiments/arc/lspv2_341_independent_verify.js`, Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. Pinned original seven-fixture packet: `results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json`, Git blob `fe27fe1011d0021e721ccaeb747ed58da65d7464`. **The original checker recognizes SOURCE/AND3/XOR on a special graph packet with exactly 4V-1 paid records; it is not the missing full historical R_mix341 parser.**

The main prior art is LSPV-3/610 (2026-11-13 02:24 PST): the 70 SOURCE-prefix patterns, 69 SAT source choices and model-count histogram. LSPV-1/609 and /615 already established accepted SAT packets at E=18 and larger; LSPV-1/559 and /560 established guarded, source-bound soundness and a restricted cost-equal repair; LSPV-2/596 established a separate native /386 provenance collapse; LSPV-3/611 addressed raw typed-ID namespace; LSPV-4/583 and LSPV-5/524 audited same-realization event vectors. Relevant historical /539-549 reports, five-role handoffs, both root proof trackers, issue #3, `AGENTS.md`, `CODEX.md`, and the research skill were consulted. No credit is claimed for discovering the 70 SOURCE alternatives or the checker brute-force cutoff. **New here:** the entire K4 SOURCE-to-**complete native terminal** existential reachability classification (all possible paid bodies), its exact min-record spectrum and an explicit SOURCE-to-AND3 affine-carrier count.

Primary disciplinary controls: Cook and Reckhow, *J. Symbolic Logic* 44 (1979), 36-50, DOI 10.2307/2273702 (fixed proof-system scope); Cousot and Cousot, POPL (1977), DOI 10.1145/512950.512973 (MAY-step inclusion); Ben-Sasson and Wigderson, *J. ACM* 48 (2001), 149-169, DOI 10.1145/375827.375835 (Resolution-only width/length control). The last paper does not establish lower bounds for native AND3/GF(2) or the complete mixed calculus.

## Theorem 616.1: exact existential completed-refutation fiber (PROVED/RESTRICTED)

Let `F_S` be the K4 signed source formed as described above, with one SOURCE clause forbidding each pattern in `S` at vertex 0, and let `C_341(F_S)` be the set of **all** complete raw-byte packets which the archived checker accepts and whose parsed K4 original source equals `F_S` and whose parsed charges are exactly `[true,0,0,0]`. Do not fix the paid proof body, beyond the actual original checker predicates.

For all 70 choices `S`, with `S_*={0,3,5,6}`:

$$
C_{341}(F_S)\ne\varnothing\quad\Longleftrightarrow\quad S=S_*.
$$

Under the recovered checker's one-paid-record-per-created-identity **record-count measure**, not an authenticated historical mixed-system tariff, the global optimum over all accepted complete packets satisfies

$$
\overline{W}^{\mathrm{record}}_{341}(F_S)=
\begin{cases}15,&S=S_*,\\+\infty,&S\ne S_* .\end{cases}
$$

**Proof.** Vertices 1,2,3 enforce their three even-incidence GF(2) equations. K4 incidence cancellation forces even parity at vertex 0. These three independent equations have 8 assignments, and each of the four even local patterns at vertex 0 has exactly two extensions. If `k=|S intersect {0,3,5,6}|`, then

$$
\#\mathrm{SAT}(F_S)=2(4-k).
$$

Only `S=S_*` has `k=4` and is UNSAT. For every other `S`, the original checker, regardless of its paid proof body, reaches `if(E<=15)` and explicitly enumerates every one of the 64 original variable assignments, asserting `oddCount===0`. Therefore no SAT source among the 69 has *any* accepted completion. This is stronger than showing that one particular proof template fails.

For `S=S_*`, take the exact original 15-paid-node K4 packet and change only parsed `charges[0]` from the number `1` to Boolean `true`. The global bitwise-XOR check continues to see integer 1. At SOURCE, all four even-parity forbidden patterns satisfy the strict comparison `parity !== true`. Every remaining original checker check is unchanged, so the complete packet is accepted. The original checker also enforces `f.proof.length===4*V-1=15` and distinct parsed paid identities. Hence every accepted completion has exactly 15 paid creation records, and one exists. QED.

The old checker is not a general sound checker: its K4 exhaustive guard is absent on E>15, where SAT-source false refutations have already been exhibited. No 15-record bound is asserted for a separate historical full calculus with additional operations.

## Theorem 616.2: exact three-AND3 affine-carrier normal form (PROVED/RESTRICTED)

For any four distinct local SOURCE clauses on a fixed three-edge support, each forbidding a different triple in `S`, conjoin them by numeric-Array-support AND3 nodes, with their actual eight-row tables. The resulting truth set is `{0,...,7} setminus S`, of size four. It equals an in-band GF(2) row `a·x=b` on these three coordinates **if and only if** `S` is one of 14 affine hyperplanes of `GF(2)^3`.

**Proof.** The nonzero row coefficient `a` has seven possible values and `b` has two. Each yields a distinct four-point affine hyperplane; there are exactly 14. The zero row gives either zero or eight satisfying assignments and cannot agree with this four-point table. Conversely each nonzero row matches precisely one of the 70 four-subset source choices. Each SOURCE clause excludes a unique assignment and is essential to this exact conjunction. A binary AND circuit whose result depends on all four such leaves requires at least three distinct internal paid nodes: in the connected ancestor DAG, with `L=4` leaves and `N` binary internal nodes, `2N>=L+N-1`; hence `N>=3`. Three explicit AND3 nodes attain the bound. This is a minimal *local conjunction* result, not a lower bound for the complete mixed rule set.

Of the 14 affine-compatible choices, exactly one produces zero K4 models, 12 produce four models, and one produces eight. The remaining 56 SOURCE-prefix alternatives are non-affine and cannot be replaced by an uncharged single GF(2) row with exact typed-Array semantics. Any such replacement changes the recognized language unless a separate paid, sound derivation is proved.

## Independent computation and unchanged-checker replay

A standalone Python enumeration over all 70 four-subsets, all 14 nontrivial 3-bit affine rows and all six-variable assignments verified: 70 local sources, 14 affine/56 non-affine, and the exact SAT model histogram `{0:1,2:16,4:36,6:16,8:1}`. Independently, **the unchanged original /341 checker source was executed in hosted V8** for each of the 70 complete packets obtained by replacing only vertex-0 SOURCE clauses in the original K4 proof and changing numeric first charge to Boolean `true`. One complete packet accepted with **1,401 assertion groups**; 69 fixed-template packets rejected at their first inconsistent AND3 truth table. Three hostile mutations (bad signed SOURCE incidence, missing paid parent and wrong global charge parity) rejected.

The empirical 69 fixed-template rejections are **not** the argument against all other paid proofs: that stronger exclusion comes from the source-model theorem plus the original checker's independent exhaustive terminal gate. This separation prevents falsely conflating fixed-trace testing with universal quantification over all proofs.

Reproducible Node.js driver (using exact pinned Git blob hashes and original checker via Node `vm`): `experiments/arc/lspv1_616_k4_native_completion.cjs`. Raw 70-case matrix: `results/raw/arc/2026-11-13_0404_LSPV1_616_K4_SOURCE_TO_TERMINAL_RAW.json`. The driver passed a hosted JavaScript parse check; it has **not** been executed as an independent operating-system Node subprocess in this run. Repository-wide preflight and LaTeX compilation were unavailable without a locally network-accessible checkout. No unverified OS replay is claimed.

## Consequences and proof dependency ledger

For **P2-D1**, this authenticates only the narrow original K4 SOURCE-to-terminal fiber and exact original-checker K4 record objective. It does **not** authenticate original-source binding independent of a supplied packet, complete RES-to-AND3, paid DEF-to-LOCAL-CONVERT, fresh/private/exported wires, branching/assumption discharge, deletion, joins or the full mixed tariff. The checker is already known to accept SAT sources above its E<=15 cutoff. **P2-D1 remains OPEN.**

For **P2-C3**, a cost-sound K4 prefix abstraction can preserve all 70 SOURCE variants and refine the completed-refutation goal by the exhaustive six-variable source test; 69 apparent candidate goals become impossible, while the one legal complete target retains its 15-count witness. This goal refinement does not remove the 69 otherwise SOURCE-legal prefixes, and its abstract proof-record charge is not a cost for running the meta-level enumeration. No all-rule alpha/gamma or shared-DAG CEGAR theorem follows. **P2-C3 remains OPEN.**

For **P2-B1**, this is a bounded, deliberately easy control and not a superpolynomial lower bound. GF(2) makes the authentic odd Tseitin source short. **P2-B1 remains OPEN**. For **P2-B2/B3**, there is no noncircular polynomial same-calculus simulation or inference from SAT in P. These remain **separately OPEN**. Actual machine runtime, discovery, encoded evidence bytes, span and peak storage remain distinct from the 15 creation-record count.

**TRACKERS REVIEWED; NO MATERIAL NODE STATUS CHANGE.** Both root proof chains remain OPEN and require no edit. Request LSPV-5 independent falsification of Theorems 616.1 and 616.2, especially a noncanonical K4 complete accepted packet or a non-affine typed Array row. Next load-bearing objective remains the externally source-bound original mixed-rule checker, above all a genuine authenticated Resolution-to-AND3 or DEF-to-LOCAL-CONVERT step.
