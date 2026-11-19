# SELECTOR-ADVERSARY2: large-backdoor refuting covers that remain source-easy

19 November 2026, Asia/Seoul. Specific assignment: construct adversarial explicit inputs against proposed selectors. P versus NP remains **OPEN**. Independent mathematical review is pending.

## Result card

**PROVED/EXACT, restricted explicit family.** The supplied row/block layout contains connected ordinary-CNF families with all of the following properties at once:

1. every shared row has exactly one refutable block;
2. the selected block changes at every step of a Gray traversal and the selector's range has size equal to the number of rows;
3. every selected residual has syntactic strong-Horn backdoor number `q`, where `q=N^{.35-o(1)}` is available under the layout bounds;
4. every selected residual nevertheless has a two-unit Resolution refutation, and a source-aware deterministic algorithm authenticates the grammar and emits the complete selector in `O(N polylog N)` time and `N^{.35+o(1)}` peak writable space;
5. deleting one target block gives a unique, equally easy SAT row with a streamed full witness.

This falsifies the inference that the small-Horn-backdoor cover used by POSITIVE-SELECTOR-HORN2 is close to necessary, or that backdoor enumeration measures mandatory witness cost. It does **not** falsify that report's sufficient theorem. It also supplies no lower bound: the adversarial family is deliberately easy.

The selected pipeline is encoded source -> grammar authentication -> row-specific block -> local refutation/witness -> full output. The attacked claims were: a row-independent small candidate set suffices; nearby rows reuse a selected index; large strong backdoors force large work; and short per-row correct paths automatically form a short whole strategy.

## Explicit connected local core

For `q>=1`, use private variables

    p, x_1,y_1,...,x_q,y_q.

Define `C_q` by the unit clauses `(p)` and `(not p)`, the disjoint positive clauses

    (x_j or y_j),  1<=j<=q,

and negative connectors

    (not p or not x_1),
    (not y_j or not x_{j+1}) for 1<=j<q,
    (not y_q or not p).

The incidence graph is connected. The first two clauses refute `C_q` immediately. Its syntactic strong-Horn backdoor number is exactly `q`: each pair `(x_j or y_j)` requires at least one selected variable, and the pairs are disjoint; selecting every `x_j` attains the bound. Negative connectors and unit clauses are already Horn.

This is a selector-specific integration of a known project firewall, not a novelty claim for “large static backdoor, easy formula.” Earlier project reports STRICT22-BACKDOOR-SELECTOR-GATE271, GLOBAL-BACKDOOR-PRODUCT162, and ADAPTIVE-BACKDOOR-TREE-EXACT355 already reject static-backdoor hardness in other families. The 2024 backdoor-depth literature likewise proves that backdoor size is strictly dominated by component backdoor depth and that bounded depth gives linear-time SAT for fixed depth. [1] The connected core here prevents the simplest initial component split, while its explicit unit conflict remains decisive.

## Guarded selector family

Let `z` have `h` shared bits and `R=2^h`. For row `a`, define its mismatch clause

    g_a(z) = OR_{j:a_j=0} z_j  OR  OR_{j:a_j=1} not z_j.

It is false exactly at `z=a`. Choose any injection `f:{0,1}^h->[B]`. In block `f(a)`, prefix every clause of a fresh `C_q` by `g_a`. All other blocks contain only authenticated satisfiable padding.

At row `a`, the guard disappears and block `f(a)` becomes `C_q`; every other guarded core is deleted as satisfied. Thus exactly block `f(a)` is UNSAT. Private variables are disjoint by construction. Every local refutation consists of the two guarded unit clauses after checking that their guards are false under `a`.

For the canonical explicit family use `B>=R` and

    f(a) = 3a+1 mod R,

on the integer represented by the shared bits. Since `R` is a power of two, this is a permutation. It is computed and inverted in logarithmic workspace. Every two distinct rows have distinct selected blocks, so a Gray traversal makes `R-1` selector changes. Any row-independent candidate set covering every row must contain all `R` active blocks. These properties defeat reuse heuristics, yet `f` is algebraically trivial.

For asymptotic layout compliance, take

    R <= N^.195, B <= N^.65,
    q = floor(N^.35 / polylog N).

Each guarded literal carries an `O(log N)` identifier and each guard has `O(log N)` literals, so an active block uses `N^{.35+o(1)}` encoded bits. The `R` active blocks use `N^{.545+o(1)}` bits. Fill the remaining blocks with source-declared satisfiable private padding so total encoded length is `Theta(N)` while no block exceeds `N^{.35+o(1)}`. Parsing, checking owner-tagged private identifiers, validating the canonical cores, and reading all padding costs `N^{1+o(1)}` time. The selector array uses `R log B=N^{.195+o(1)}` bits; one current block uses `N^{.35+o(1)}` bits.

Hence `q` greatly exceeds the POSITIVE-SELECTOR-HORN2 budget `.135 log_2 N`, so its NO-COVER promise fails on every row. Nonetheless the direct specialist runs within the target resources. This establishes only that the promise is sufficient and non-necessary.

## Matched one-hole SAT family

Delete active block `t*`. The unique row `a*=f^{-1}(t*)` now satisfies every surviving block through its guard. Every other row retains its selected `C_q`. A deterministic source-aware algorithm reads the missing target, computes `a*`, verifies every clause, and streams arbitrary private values plus all padding-variable values. Output time is `Theta(N)` when the encoding declares `Theta(N/log N)` variables; only the current block's values need be live.

Thus the same large-backdoor distractors are easy on both polarities. A wrong SAT row encounters the surviving complementary units in its selected block and is rejected.

## Restricted selector-interface lower bounds and their firewall

The same family can realize an arbitrary selector table, as proved in SELECTOR-ADVERSARY1. That yields two exact but interface-restricted statements.

**Equality-query theorem.** Suppose an algorithm sees only queries `Bad(z,i)` and is promised exactly one bad block for every row. For every deterministic algorithm, there is a table `f_A` forcing at least `R(B-1)` queries before all indices can be output: independently for each row, answer NO until only one candidate remains. After simulating the algorithm, `f_A` is an explicit table and the guarded construction materializes it as an ordinary CNF.

The quantifiers are

    for every deterministic equality-query algorithm A,
    there exists a table f_A causing R(B-1) queries.

There is no single fixed table asserted hard for all algorithms. More importantly, an unrestricted source-aware algorithm reads the encoded table or recognizes the canonical affine selector and bypasses the oracle game. Therefore this is **PROVED/EXACT only for the declared restricted interface** and is not an execution lower bound.

**Advice/query counting theorem.** A verifier/decoder that must handle all `B^R` selector tables, has a `k`-bit instance-dependent advice string, and makes at most `Q` binary oracle queries can distinguish at most `2^{k+Q}` cases. Therefore

    k + Q >= R log_2 B.

This bounds the combined information entering that interface. The original CNF itself already contains enough source bits, so the inequality does not apply to unrestricted computation without separately proving that source access reduces to this channel.

## Correct paths, polarity, and outputs

The required outputs and wrong-path checks are:

| Mode | Successful output | Wrong-path soundness | Fully charged work |
|---|---|---|---|
| Deterministic NO specialist | selector `A[z]` for all rows and source-backed local refutations, or UNKNOWN | each index must name a source block; both guarded units must reduce to complementary units | parse/authenticate all `N` bits; evaluate all `R` rows; emit `R log B` bits; verify/replay every selected row |
| Supplied NO path for one row | block index plus two clause references | reject a wrong block, noncomplementary units, or a guard not falsified by that row | source lookup and `O(h)` guard checking remain; one row path proves only one row |
| Supplied NO whole strategy | a table/program mapping every row to a block, plus a verifier route | reject any missing row or invalid local proof | charge the whole table/program and every universal row; a compact affine program is allowed |
| Supplied SAT path | the one-hole row and a streamed full private assignment | reject if any original clause fails | source access, all clause checks and full output remain |
| Free polarity route | correct SAT/UNSAT label only | no witness/refutation supplied | construction and verification still required; as a decision interface this is answer advice |

For the canonical family, the NO strategy is the `O(log N)`-space program `f`; the local proof is one reusable schema whose actual source clause references are checked per row. This explicitly falsifies “many selector changes imply a large strategy.” For arbitrary table families the complete table has `R log B=N^{.195+o(1)}` bits, still below square-root workspace.

A general universally sound `k`-bit verifier of fully charged replay cost `(V,S)` can be enumerated deterministically in

    O(2^k (V+k+1)) time,
    O(S+k+log V) writable space.

This is an upper bound, not a claim that enumeration is necessary. When row predicates are independent, enumerate candidate row proofs separately at additive cost rather than enumerating their Cartesian product. When existential choices depend on universal history, either bound and check the entire strategy or charge all universal histories. A single favored root-to-leaf trace is insufficient.

Read-only random-access certificates are additional inputs: certificate length, addresses, accesses and production remain charged. Ordinary space-bounded nondeterminism does not give free two-way access to old guesses; store them or use a proved paid consistency method. [2] This family's streaming verifier avoids rereads by holding only the current row index and clause references. An accepting nondeterministic transducer's output becomes valid only after final acceptance; otherwise output must be buffered or reproduced consistently.

## Exact time-space exclusion ledger

The machine convention is a uniform random-access Turing machine/RAM with bounded words, read-only indexed source, write-only output, and charged work/index tapes. Polylogarithmic simulations are absorbed only where the cited theorem permits them.

| Polarity/model | Sourced simultaneous exclusion | Application here |
|---|---|---|
| Deterministic SAT/UNSAT decision | Buss--Williams certify SAT outside `DTISP(N^{1.34070},N^{.5})`, with `o(1)` terms in both exponents; subpolynomial-space benchmark `c<2cos(pi/7)=1.801937...`. [3] | Excludes an all-CNF deterministic `(1.33,.5)` decider. It does not exclude this promised easy family or a specialist lacking an arbitrary-CNF reduction. Deterministic complementation preserves resources. |
| Nondeterministic UNSAT / conondeterministic SAT | Diehl--van Melkebeek--Williams: for `c^2 d<4`, some `e>0` rules out simultaneous nondeterministic tautology algorithms with the stated time bounds; setting `c=d` gives `d<cuberoot(4)=1.587401...`. [2] | The positive `e` is not specified as `.5`; no `(1.33,.5)` conclusion follows from that theorem alone. |
| Explicit NO-side point | FLMV Corollary 6.5 gives space exponent `(1+c)/c^2-c`; at `c=1.10` it is `.635537...`, while it is negative at `c=1.33`. [4] | Supports a NO-side `(1.10,.5)` calibration with slack, not `(1.33,.5)`. |
| Nondeterministic SAT | None of the reviewed NO-side statements supplies a nondeterministic-SAT `(1.33,.5)` exclusion. | A satisfying assignment can be guessed and checked; retaining it uses linear workspace, while a rereadable external assignment is a different model. No opposite-polarity transfer is made. |
| Fixed proof system | Resolution or another proof language can have strong certificate lower bounds. | The present complementary-unit Resolution proof is constant size. Proof-system lower bounds never transfer to unrestricted execution without a costed bridge. |

**Correction retained.** The SELECTOR-ADVERSARY1 row attributing Fortnow's result to nondeterministic SAT is withdrawn. The cited argument is on the UNSAT/conondeterministic side; LOCAL4 and POSITIVE-SELECTOR-HORN2 already recorded this correction. The finite constructions in SELECTOR-ADVERSARY1 remain unaffected.

For an all-CNF, both-polarity sound verifier with `V=N^{1.33+o(1)}`, `S=N^{.5+o(1)}`, and whole advice length `k<=alpha log_2 N`, deterministic enumeration would contradict the Buss--Williams point when `alpha<.01070`. This corollary needs all-CNF completeness, a known clock and the same standard-machine simulation. It does not apply to the present promise family.

## Arbitrary CNFs and the polynomial-seed proposal

The new adversary strengthens the negative conclusion: even a polynomially large strong backdoor can be irrelevant because a cheaper proof is visible before branching. Consequently a successful extension beyond POSITIVE-SELECTOR-HORN2 must combine multiple authenticated terminal routes and allow early refutation, component/depth methods, unit propagation, affine methods, source grammar recognition and exact proof reuse. It cannot insist that one static parameter explain every easy residual.

The generic seed arithmetic remains unchanged. A full-support scanner with a local exact seed using time `m^c` and space `m^s` has displayed bounds

    time exponent max(1.195, .845+.35c),
    space exponent max(.35, .35s).

The target requires `c<=97/70` and `s<=10/7`, plus all preprocessing and compiler costs. “Polynomial” alone gives no such exponents. Iterating a formal recurrence requires a uniform hereditary compiler for every child; this family supplies no arbitrary-CNF compiler, and its cheap unit route merely shows why a controller must preserve shortcuts.

## Executed evidence and T5 control

`selector_adversary2_audit.py` exhaustively checked eight finite layouts (`h=2,3`, `q=1,2,3,4`): 320 residual SAT checks, 48 exact minimum-backdoor computations, 48 connected-core checks, and 48 direct complementary-unit refutations. Every row had exactly the affine-predicted bad block. Every Gray step changed the selected block. Each one-hole instance had exactly the predicted SAT row. The restricted 8-row/16-block cyclic query control forced 120 negative equality queries before inference, matching `R(B-1)`.

The T5 H9 control (threads `BBB/FBB/FFF/BB`) was rebuilt independently. The full graph is UNSAT with one color fixed; all 11 edge deletions have complete witnesses; five rotations passed 550 original-arc checks. Its standard one-hot encoding has exact strong-Horn backdoor number 36 from nine disjoint positive five-clauses, yet fixed deletion witnesses are cheap. T5 therefore reinforces the same firewall: representation-specific backdoor size is not witness-acquisition hardness, and a fixed control gives no growing-girth lower bound.

The code is a functional standard-library checker. Its brute-force routines are independent finite oracles, not proposed asymptotic algorithms or measured native RAM implementations.

## Prior work, status, and gates

Fresh project searches recovered the static-backdoor criteria and easy-family firewalls in STRICT22-BACKDOOR-SELECTOR-GATE271, ADAPTIVE-BACKDOOR-TREE-EXACT355, GLOBAL-BACKDOOR-PRODUCT162, the exact selector realization in SELECTOR-ADVERSARY1, and POSITIVE-SELECTOR-HORN2. The new contribution is the connected row/block integration that violates the latter's small-backdoor promise on every selected residual while preserving an explicit refutable cover and matched one-hole SAT family. It is not a general large-backdoor discovery.

No local repository checkout is available, so project preflight and LaTeX compilation were not run. This role has no assigned TMR root manuscript; publication is additive and changes no owner, title, schedule, or enabled/paused state. Corpus review is targeted, not exhaustive.

**PROVED/EXACT:** connected core beta_H=`q`; guarded unique selector; canonical full-range/Gray-changing selector; one-hole SAT theorem; source-aware upper bound; restricted equality-query and advice/query theorems; correct-path soundness accounting.

**COMPUTATIONAL:** eight finite layouts, restricted query control, and H9 witness checks.

**FALSIFIED INFERENCE:** small static backdoor is necessary for target-cost selection; many selector changes imply a large strategy; one fixed/global small candidate set covers all rows; a per-row path is a whole strategy; generic polynomial seed gives exponent `1.33`.

**CONDITIONAL:** costs for noncanonical encodings and any transfer through a new arbitrary-CNF compiler.

**OPEN:** a uniformly discoverable multi-terminal refuting cover for arbitrary residuals; hereditary source-to-layout reduction; independent audit; P versus NP.

Gates: DISJ PASS; relativization PASS for the elementary construction with no separation bridge; simultaneous DTISP PASS for the displayed same-execution upper bounds and OPEN for arbitrary-CNF transfer; deterministic configuration counting PASS as an upper-bound consistency check only; Natural Proofs/algebrization NOT APPLICABLE because no circuit separation is claimed.

**Next blocker:** define and cost a source-aware portfolio whose success certificate is a disjunction of independently sound terminals (unit/UP, Horn/Krom depth, affine, bounded treewidth, and an exact fallback), then prove a cover theorem for every UNSAT row. The portfolio must charge failed recognizers and cannot infer SAT from all of them returning UNKNOWN.

## Primary sources

[1] J. Dreier, S. Ordyniak, S. Szeider, *SAT Backdoors: Depth Beats Size*, JCSS 142 (2024), 103520, especially Theorem 19 and Corollary 20. https://repositum.tuwien.at/bitstream/20.500.12708/208047/1/Dreier-2024-Journal%20of%20Computer%20and%20System%20Sciences-am.pdf

[2] S. Diehl, D. van Melkebeek, R. Williams, *A New Time-Space Lower Bound for Nondeterministic Algorithms Solving Tautologies*, Wisconsin TR1601 (2007), Theorems 1-2 and Section 2.1. https://research.cs.wisc.edu/techreports/2007/TR1601.pdf

[3] S. Buss, R. Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds*, CCC 2012, Theorem 2/table. https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/samCCC-cr.pdf

[4] L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), machine model and Corollary 6.5. https://lance.fortnow.com/papers/files/tst.pdf
