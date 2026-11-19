# SELECTOR-ADVERSARY3: guarded K6 exact-one cores defeat local screens

18 November 2026, Pacific Time. Assignment: construct adversarial explicit inputs against proposed selectors, specialized to exact-one T5. P versus NP remains OPEN. Independent mathematical review is pending. This is an additive report; manuscript ownership, titles, schedules, and enabled/paused states are unchanged.

## Result card

**PROVED/EXACT for the declared family.** Replace the complementary-unit core of SELECTOR-ADVERSARY2 by the private-head Q encoding of K6. Guard one fresh copy for each shared row. The resulting ordinary-CNF layouts have, simultaneously:

1. exactly one refutable block per row and an affine full-range selector;
2. a selected residual that is a parity-feasible, semantically clause-critical Q-UNSAT instance;
3. no deletion under native generalized arc consistency from full domains;
4. a tail-coloring network that is strongly 5-consistent but globally UNSAT;
5. a unique matching SAT row after deleting one selected block;
6. a source-aware deterministic selector and SAT witness constructor that are near-linear in the actual padded input/output size.

This falsifies the sufficiency of per-head parity, generalized arc consistency, strong consistency below the alphabet-plus-one threshold, a row-independent bounded candidate set, and one supplied correct block index per row. It does not give an unrestricted lower bound: the canonical family is intentionally recognizable and easy. The exponent-compliant encoding uses authenticated satisfiable padding and is therefore not evidence of intrinsic hardness.

## Exact source and imported evidence

The exact-title archive `T5_Exact_One_Experiments_2026-11-18.zip`, Library ID `libfile_00b4599c2cfc8191a859b757dad101a0`, was retrieved. Its SHA256 is `d811f0ea0b00fc88ebecf2349585386a2f0079508139aa638a8635e765e8a30a`; all 23 manifest entries match. Its independent verifier again reports PASS for Q/P counts, the five-clause deletion counts, all 236 large-fixture deletion witnesses, and 55,696 clause checks. This run did not repeat the 2,320 main runs, 600 exploratory runs, or 4,096 four-variable systems. The retained exploratory outcome at n=40,m=60, seed 202611580003 remains UNKNOWN, not UNSAT.

The report recovers rather than duplicates:

- `SELECTOR-ADVERSARY2`, blob `21dbeeddcea57b6c00e45f21f6e38dde5f46ab2b`: guarded unique selectors, one-hole SAT instances, arbitrary-table/equality-query firewalls, and source-easy affine selectors, originally using complementary units.
- `QBOUNDARY2`, blob `b4b3c499004b8351a544a25f608c79deffd9d578`: exact Q boundary joins and the 100-versus-60 binary-projection collision.
- The exact-one package: private heads project to graph 5-coloring; the 283-variable/236-clause Mycielski fixture is fixed incidence-girth eight and has a recognizable certificate.

## The K6 Q core

Use tails v0,...,v5. For every edge e={u,v} of K6 introduce a fresh head h_e and constraint Q(h_e,u,v). There are 21 five-valued variables and 15 constraints. Each head occurs once, so every per-head parity graph is one edge and bipartite.

Because exists h Q(h,u,v) iff u!=v, a Q witness exists exactly when K6 has a proper 5-coloring. It does not. Deleting edge e allows its endpoints to share one color and the four other vertices to use the other four colors. Every remaining edge then has unequal endpoints and its head is obtained by choosing a winning endpoint's value. Hence the core is semantically Q-clause-minimal UNSAT, with an explicit witness after each of 15 deletions. The omitted head can receive any value and its deleted constraint would still fail because its tails are equal.

The old P relation behaves differently on the identical 15 scopes. Exact weighted enumeration of all 5^6 tail rows gives:

| Relation | Full witnesses on matched K6 scopes |
|---|---:|
| Q = exactly one win | 0 |
| P = two wins | 250,880 |

Both computations tested 1,171,875 head supports. The disjoint local accepted sets therefore do not induce an instancewise SAT ordering.

## Local-propagation counterexample

Native generalized arc consistency maintains a five-value domain for every head and tail and removes a value only when it has no support in one incident Q constraint. On the untouched K6 core, every value in every position of an isolated Q constraint has support. The executed fixed-point scan examines 585 support tuples, deletes zero values, and returns nonempty domains.

After fixing proper, pairwise-distinct tail colors, native GAC behaves as follows:

| Fixed tails | Proper partial cases | GAC wipeouts | Support-tuple tests |
|---:|---:|---:|---:|
| 0 | 1 | 0 | 585 |
| 1 | 30 | 0 | 34,985 |
| 2 | 300 | 0 | 391,974 |
| 3 | 1,200 | 0 | 1,381,796 |
| 4 | 1,800 | 1,800 | 1,015,848 |

These are exhaustive finite logical-operation counts, not native RAM timings. The script retains Python sets and raw records; process RAM is not measured.

Eliminating the private heads yields the standard binary disequality network for K6 with five colors. It is strongly 5-consistent: any proper assignment to at most four vertices uses at most four colors, so any designated next vertex has an available color. It is not 6-consistent: assigning all five colors to five vertices leaves none for the sixth. Exhaustive extension counts cover 6,150 successful cases for levels 1 through 5 and find the expected failure at level 6. This matches the established graph-coloring local-consistency phenomenon described by van Beek and Dechter: k-coloring networks are inherently strongly k-consistent but need not be strongly k+1-consistent.

Primary source: P. van Beek and R. Dechter, *Constraint Restrictiveness versus Local and Global Consistency*, Definitions and graph-coloring examples, https://ics.uci.edu/~dechter/publications/r36-constr-restr-vs-local-global-consist.pdf . The K6/T5 specialization and native-Q GAC counts here are new targeted integration, not a novelty claim for graph-coloring consistency.

This is a precise restricted falsifier. It does not rule out higher-order consistency, treewidth dynamic programming, graph recognition, inclusion of the six-tail pigeonhole core, algebraic encodings, compact circuits, or unrestricted source-aware algorithms.

## Guarded selector family

Let z have h Boolean shared variables and R=2^h. For row a, its mismatch clause g_a(z) is false exactly on a. Use B>=R blocks and the injection

    f(a)=3a+1 mod R.

Since R is a power of two, f is a permutation. In block f(a), prefix every clause in a fresh Boolean encoding of the K6 Q core by g_a. All private Boolean variables carry their block owner and are disjoint between blocks. At z=a, the guard disappears only from block f(a), leaving the Q-UNSAT core. Every other guarded block is satisfied by its mismatch guard. Thus each row has exactly one refutable block, all R blocks occur, and consecutive distinct rows—including a Gray traversal—always select different blocks.

A direct one-hot encoding uses five Boolean indicators for each of 21 Q variables. For each variable it has one positive at-least-one clause and ten negative at-most-one clauses. Each Q constraint contributes one ternary forbidding clause for every one of its 65 false value triples. Before guards, one block therefore has 105 Boolean variables and

    21(1+10)+15(125-60)=1206 clauses.

Every clause receives the h-literal mismatch prefix. The relation variables within each block remain private. For h=2 and h=3, the executed audit respectively constructs 4/8 rows and blocks, 420/840 private Boolean variables, and 4,824/9,648 guarded clauses. Every row selects the affine-predicted block.

Delete one complete target block t. The sole satisfying shared row is a=f^{-1}(t); every surviving block is disabled by its guard. Arbitrary declared private bits can then be streamed because every guarded source clause is already true. Other rows retain their unique selected K6 block. The audit checks every target in both finite layouts.

For the requested asymptotic layout, choose R<=N^.195, B between R and N^.65, and pad with authenticated satisfiable private blocks to actual encoded length Theta(N). Each active block has O(log N) guard-expanded bits and is below N^.35. This padding is explicit and charged. It shows the layout can host the adversary, but it is unrelated easy material and supplies no intrinsic-hardness claim.

## Sound specialist, outputs, and full costs on this family

The canonical deterministic NO specialist authenticates the entire source grammar, the private-owner declarations, the one-hot Q encodings, every guard, and the affine permutation. It then streams f(a) for every row. Each claimed block is checked to have guard false at a and to contain exactly the canonical K6 core. The K6 pigeonhole proof or a fixed graph-coloring certificate supplies sound local UNSAT; a wrong block has a true guard and is rejected. Parsing/padding costs N polylog N bit time under a simple encoding. Row traversal and streamed selector output cost O(R polylog N). Peak writable space is one current block plus O(R) bits only if a coverage bitmap is retained; canonical inversion eliminates the bitmap, giving O(N^.35 polylog N) under the block bound. Read-only input and write-only output are excluded only under that stated interface.

For the one-hole SAT family, compute a=f^{-1}(t), scan every original clause to verify its guard, and stream a complete assignment. Source checking and output are Theta(N) if the padding declares Theta(N/log N) variables. A guessed row alone does not remove this scan. A wrong row exposes a surviving active K6 block and is rejected.

This easy upper bound survives all free correct choices. It also shows why local-screen failure is not a lower bound: the source grammar gives a shortcut.

## Correct paths and advice

| Interface | Successful output | Wrong-path soundness and charged work |
|---|---|---|
| Uniform deterministic NO specialist | Complete selector/refuting cover, or UNKNOWN | Authenticate all source bytes, every guard/core, all rows or a proved compact strategy, and streamed output. Failure of a recognizer is UNKNOWN. |
| Uniform deterministic SAT specialist | Shared row plus complete private assignment | Verify every original source clause and output every declared value. |
| Free polarity routing | Correct SAT/UNSAT label | Label is answer advice for decision; it supplies no selector, refutation, or satisfying assignment. |
| One-row k-bit path | Block index and local proof | Reject an active-guard mismatch or malformed K6 proof. One row says nothing about other universal rows. Here k=ceil(log2 B)+O(1) references. |
| Whole NO strategy | Program/table mapping every row to evidence | Verify totality and every universal row. Canonical f is an O(log N)-description program; an arbitrary table takes R log B bits. |
| Adaptive/alternating route | Choices indexed by prior history | Bound and verify the whole strategy or charge every universal history; one favored trace is insufficient. |

A clocked universally sound k-bit verifier complete on all inputs of one polarity can be enumerated deterministically in O(2^k(V+k+1)) time and O(S+k+log V) writable space. Independent row certificates permit LOCAL4's sum over row searches rather than a Cartesian-product strategy search. Rereadable certificate access is an additional read-only input model: ordinary space-bounded nondeterministic guesses must be stored or given a proved paid consistency simulation. Replaying for output remains charged.

## Restricted interfaces and lower-bound firewall

The guarded family also inherits SELECTOR-ADVERSARY2's exact restricted statements. With only equality queries Bad(a,i) and exactly one bad block per row, an adversary can force R(B-1) negative queries, with the hard table chosen after the deterministic query strategy. A k-bit advice plus Q-query decoder handling all B^R tables obeys k+Q>=R log2 B. Neither applies to unrestricted execution reading the source: the canonical affine formula is visible and cheap.

Many selector changes likewise do not imply a long strategy. Here every distinct row changes the selected index, but f has a logarithmic description. Conversely, a supplied correct index for each row is a collection of local existential choices, not a proof that all rows are covered unless the universal traversal or strategy verifier is included.

## High-girth extension: exact existence, not an explicit hard generator

Erdos proved that for all g and k there are graphs with girth greater than g and chromatic number greater than k. Take k=5 and an edge-minimal non-5-colorable subgraph H. Then every H-e is 5-colorable, H is 6-chromatic, and its girth is still greater than g. Its private-head Q image is clause-minimal UNSAT with incidence girth greater than 2g. Every subformula using at most g constraints has a forest as its tail graph and is Q-SAT.

Primary source: P. Erdos, *Graph Theory and Probability*, Canadian Journal of Mathematics 11 (1959), 34-38, https://users.renyi.hu/~p_erdos/1959-06.pdf . The critical extraction and Q transfer are elementary consequences. This gives an existential family defeating every fixed bounded-clause UNSAT-core test. The proof is probabilistic/nonuniform at this point: it supplies neither the explicit input generator demanded for a uniform runtime claim nor a promise-preserving reduction from arbitrary CNFs. It establishes no superpolynomial witness cost.

The Nastase–Rodl–Siggers robust-critical theorem supplies large **odd** girth critical graphs, not full girth, and therefore does not replace the Erdos step for locally forest-like instances. Its exact abstract explicitly distinguishes odd girth. https://graph.knu.ac.kr/preprints/Note%20on%20Robust%20Critical%20Graphs%20with%20Large%20Odd%20Girth.pdf

## Simultaneous RAM exclusion ledger

Machine convention: uniform indexed/random-access Turing machines or bounded-word RAMs with a justified polylog-overhead simulation; read-only source, write-only output, and charged address/work storage. N is actual encoded length. The statements below do not apply automatically to the guarded promise or critical Q images.

| Polarity/model | Sourced statement | Application limit |
|---|---|---|
| Deterministic SAT/UNSAT | Buss–Williams Theorem 2/table gives SAT outside DTISP(N^(1.34070+o(1)),N^(.5+o(1))); subpolynomial-space benchmark c<2cos(pi/7). | Excludes an all-CNF deterministic (1.33,.5) decider, not this promised easy family. Deterministic complementation preserves resources. |
| Nondeterministic UNSAT / conondeterministic SAT | FLMV Corollary 6.5 gives space exponent (1+c)/c^2-c. At c=1.10 it is .635537..., while it is negative at 1.33. | Supports a NO-side (1.10,.5) calibration with reduction slack, not (1.33,.5). |
| Nondeterministic tautology/UNSAT | Diehl–van Melkebeek–Williams: c^2 d<4 implies some e>0 rules out both NTIME(N^c) and NTISP(N^d,N^e) tautology algorithms; c=d gives d<cuberoot(4). | The theorem does not state e=.5. Negation/reduction costs must be paid. |
| Nondeterministic SAT | No matching (1.33,.5) exclusion follows from the reviewed NO-side results. | The earlier opposite-polarity attribution remains withdrawn. |
| Fixed proof system | Resolution/circuit/interface lower bounds restrict that proof language or model. | No transfer to unrestricted algorithms without a proved compiler/simulation. |

Sources: S. Buss and R. Williams, https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/samCCC-cr.pdf ; L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, https://lance.fortnow.com/papers/files/tst.pdf ; S. Diehl, D. van Melkebeek, R. Williams, https://research.cs.wisc.edu/techreports/2007/TR1601.pdf .

For an all-CNF sound/complete verifier with replay V=N^(1.33+o(1)), workspace N^(.5+o(1)), advice k<=alpha log2 N, deterministic enumeration conflicts with the Buss–Williams point when alpha<.01070. This requires all-input completeness, a known clock, and the same machine simulation. It does not apply to a promise-only K6 recognizer or arbitrarily long free strategies.

The generic full-support scanner bound remains time exponent max(1.195,.845+.35c) and space max(.35,.35s) for a local seed ell^c,ell^s, with all omitted costs restored. Target (1.33,.5) requires c<=97/70 and s<=10/7. “Polynomial” alone supplies neither inequality. No arbitrary-CNF hereditary compiler is proved.

## Executed evidence

`q_selector_adversary3.py` is standard-library, deterministic, and has no random seed. It independently declares T5 and records exact scopes and full deletion witnesses. Raw JSON preserves:

- 15 K6 scopes; weighted Q/P results and 2,343,750 combined head-support tests;
- full-domain GAC and 3,510 proper pinned-domain GAC cases;
- all strong-consistency extension cases through level six;
- 15 full Q deletion witnesses and 210 surviving-clause checks;
- matched five-clause Q/P direct enumeration;
- every row and one-hole target for h=2,3 guarded layouts;
- exact output-size formulas and analytical peak-space conventions.

The script's logical counters omit interpreter instructions, allocator overhead and process memory. The native-GAC peak metric is 21 domain bitsets plus one constant-size Q support scan. The guarded specialist holds one current source block and counters; buffering its entire output would add R log B bits. These definitions are not measured RAM.

## Status, falsifiers, and next blocker

**PROVED/EXACT:** K6 Q criticality; GAC fixed point; strong-5/not-6 consistency; guarded unique selector and one-hole SAT theorem; ordinary-CNF one-hot size; source-aware specialist; high-girth existential critical transfer.

**COMPUTATIONAL:** all finite counters and witnesses listed above; imported package verifier PASS.

**FALSIFIED AS SUFFICIENT:** per-head parity; native GAC; strong consistency through alphabet size; all bounded local-core tests as a universal principle; many selector changes; one correct path per row without universal coverage; local-screen survival as execution hardness.

**CONDITIONAL:** actual costs under alternate encodings; RAM simulations/reduction slack; explicit high-girth construction and criticalization; arbitrary-CNF transfer.

**OPEN:** global five-letter compatibility after parity/capacity processing; a source-recognizable portfolio covering every UNSAT row; hereditary compiler meeting (1.33,.5); intrinsic critical growing-girth search hardness; independent peer audit; P versus NP.

DISJ/information gate PASS: no tuple-count or consistency-level lower bound. Relativization/algebrization/Natural Proofs: no separation asserted. Simultaneous DTISP: exact ledger above, promise transfer OPEN. Configuration counting: restricted interface only. Full project preflight and manuscript compilation were not run because no local checkout exists; corpus recovery was targeted.

**Next blocker:** test higher-order relational consistency and exact separator messages on the 283-variable critical fixture while charging table acquisition and witness traceback. The target is a sound three-valued portfolio (SAT/UNSAT/UNKNOWN), not an inference from surviving screens to hardness.
