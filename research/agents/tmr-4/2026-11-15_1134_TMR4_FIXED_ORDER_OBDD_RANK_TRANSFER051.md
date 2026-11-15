# TMR-4/051: Exact prefix-rank transfer to fixed-order read-once BDDs, and the all-order Horn firewall

**2026-11-15 11:34 PST | PNP Cost-Sound Abstraction | Tracks A/C.** Status: **PROVED/EXACT (restricted, elementary theorem, independent mathematical review OPEN)** for the OBDD transfer and explicit DISJ constructions; **COMPUTATIONAL** for the finite exhaustive checks; **OPEN** for unrestricted circuits, SAT-machine time, and P versus NP.

## 1. Precommitted candidate, model and falsifiers

**Candidate OBDD051.** Fix a Boolean function f on n Boolean inputs, one common variable permutation pi, and any deterministic read-once ordered binary decision diagram B (arbitrary fanout/sharing, tests may be skipped and terminals reached early). An internal node tests a variable; along each path test indices strictly increase in pi-order. Count distinct internal graph nodes **once**, not expanded decision-tree leaves. For p=0,...,n, M_p(f,pi) is the 2^p by 2^(n-p) 0/1 matrix with rows indexed by assignments to the first p variables in pi and columns by the rest.

**Falsifiers**, fixed before literature/current-corpus inspection: (i) DISJ_k has high rank at the grouped x:y cut but a short interleaved OBDD and a linear-depth-two unbounded-fan-in circuit; (ii) even all-balanced-cut high rank on bounded-degree Horn expanders may coexist with cheap general circuits and trivial SAT witnesses; (iii) a unique-solution full assignment indicator has rank one; (iv) skipped tests, early constant terminals, shared DAGs, and an adaptively changed input order must not be charged as a fully unfolded, frozen-order tree. All four are retained as real controls, not CEGAR-spurious paths.

**Representation distinction.** Here f is the Boolean assignment-evaluation function of a fixed formula, not the language SAT on variable-length formula encodings. A lower bound on BDD **representation size** is not automatically a lower bound on the time required to decide SAT for the encoded source.

## 2. Scoped rank-to-width and size theorem

**Theorem OBDD051-A (PROVED/EXACT, restricted).** Write V(B) for the total number of distinct internal nodes in B, and F_p for the set of states at the first node whose next test lies strictly after prefix p (including terminals) reached by evaluating some prefix assignment. For every field K and every p,

```
rank_K(M_p(f,pi)) <= |F_p| <= V(B)+2.
```

Hence for every legal pi and B,

```
V(B) >= max_p rank_K(M_p(f,pi)) - 2.
```

For **complete leveled** oblivious read-once branching programs, where every path reads all n bits in the same order and early terminals are represented by explicit continuing states, the sharper per-layer statement is `width_p >= rank_K(M_p)`. The separate conversion from reduced/skipping BDDs to complete layered programs can create extra nodes and is **not free**. The V+2 inequality is the model-safe claim for reduced DAGs.

**Proof.** Evaluate the first p bits of each row assignment, following only tests within the prefix, and stop at the first test after p or a terminal. Determinism and fixed ordering give exactly one frontier state q for each prefix assignment, even when some variables were skipped. All suffix assignments then cause exactly the same suffix Boolean function g_q for all prefixes reaching q. Thus M_p factors as R_p G_p over K: R_p is a 0/1 one-hot row-to-frontier incidence matrix and G_p lists the residual suffix functions of reached frontier states. Consequently rank(M_p) <= |F_p|, independent of sharing and field. There are at most V(B) distinct internal nodes and two constant terminals; hence the second inequality. For complete leveled branching programs all frontier states lie at layer p, giving width_p. This proof does not assume a prescribed tree, unique path per leaf, or separate payment for a shared node.

**Cost-underestimation boundary.** This is a *structural* transfer, not a priced simulation of arbitrary physical machine transitions. If one pays one unit per actually allocated distinct BDD internal node, the derived lower bound concerns the size of the final allocated representation; it does **not** charge an arbitrary solver with producing that representation. A free arithmetic shortcut, a shared circuit computation, or a different variable order is outside this obligation. No zero-cost SCC quotient is used to exclude such paths, and no SAT decision time tariff is asserted.

## 3. DISJ is both a valid scoped bound and a fatal unrestricted transfer

Let `DISJ_k(x,y) = AND_{i=1}^k (NOT x_i OR NOT y_i)`, with x_i and y_i Boolean. For the grouped order `pi_bad=(x_1,...,x_k,y_1,...,y_k)`, the middle matrix is `D^(tensor k)`, `D=[[1,1],[1,0]]`. Its determinant is plus/minus one; its rank is `2^k` over **every field**, including GF(2). The theorem proves grouped-order BDD internal size at least `2^k-2`, and a direct reduced BDD construction has exactly `2^(k+1)-2` internal nodes.

The genuine legal shorter order `pi_good=(x_1,y_1,...,x_k,y_k)` has exactly **2k** internal reduced-BDD nodes: one x_i tester per pair, a y_i tester only after x_i=1, with a shared failure terminal. Every input variable is essential, so 2k is minimum node size for this function over all orders. An explicit depth-two unbounded-fan-in AND-of-ORs circuit has O(k) gates and O(k) wires; the formula is Horn/2-CNF and is SAT via `0^(2k)`. An unrestricted circuit or SAT runtime lower bound inferred from the grouped rank is FALSE, while the fixed-order OBDD statement remains valid.

**Exact enumeration** in the published executable: for k=3 all 6!=720 orders have minimum six internal nodes, maximum 14, minimum peak prefix rank over GF(2) two, maximum eight, with 48 node-optimal orders. Grouped x:y ranks by prefix are `[1,2,4,8,4,2,1]`; interleaved `[1,2,1,2,1,2,1]`. For k=4, the grouped order has 30 nodes, peak GF(2) rank 16; interleaved has eight nodes and peak rank two. These are finite **COMPUTATIONAL** checks alongside the elementary exact symbolic formulas above.

## 4. Stronger all-variable-order firewall from TMR-5/046

For simple graphs G of maximum degree d>=1 and edge-expansion h>0, let `F_G = AND_{uv in E(G)}(NOT x_u OR NOT x_v)`. TMR-5/046's existing induced-matching proof gives, for each partition with both sides >=n/3,

```
rank_K(M_{A,B}) >= 2^(h*n/(6*d*(d+1)))
```

over every field K. At the p=floor(n/2) cut of **every** variable order pi (for n>=3), Theorem OBDD051-A immediately yields

```
V(OBDD_pi(F_G)) >= 2^(h*n/(6*d*(d+1))) - 2.
```

For any explicit constant-degree, constant-expansion graph family this is an exponential lower bound on every fixed-order reduced OBDD, even when an optimal order may be selected. This is a **new scoped consequence of an earlier project lemma plus the standard frontier factorization**, not a novel general circuit lower bound or a claim of priority over published expander/OBDD results. The *same functions* have linear-size AND/OR/NOT circuits, linear numbers of 2CNF clauses and obvious all-zero satisfying witnesses, so even a min-over-all-orders exponential OBDD bound cannot be promoted to arbitrary circuits or SAT-machine hardness.

Finite additional exact control: for C6, all 6!=720 orders have reduced OBDD sizes between 12 and 14 internal nodes, and peak GF(2) ranks between four and five. The canonical cyclic order gives prefix ranks `[1,2,3,4,3,2,1]`. C6 is a finite illustration, not a constant-expansion asymptotic family.

**Unique solution control.** `f(x)=1` exactly when `x=0^8` has rank **one** at every prefix and a reduced OBDD with eight nodes; this also calibrates TMR-2/050's unique-solution, bad-intermediate-rank example. Rank of a particular intermediate product is not an unavoidable terminal rank or solver work charge.

## 5. Same-realization ledger and exact Track-C wire tax

| Resource | Exact scope/charge | What does NOT follow |
| --- | --- | --- |
| BDD nonterminal graph nodes | V, each shared DAG node counted once, two terminals uncharged in V but present in V+2 | No automatic TM transition lower bound |
| Fixed-order BDD evaluation | At most n variable decisions; input reads/head seeks/address arithmetic and BDD storage access must be charged in a physical machine implementation | No unit-cost indexed access on an ordinary tape |
| Ordering/discovery | Given pi for this theorem; if searched, every trial, failed order and decomposition discovery is paid by that algorithm | Existence of good pi does not supply free uniform discovery |
| Rank enumeration | Experimental full truth-table matrices can require 2^n bits and GF(2) elimination, not a source-local polynomial-time certificate | Rank proof does not imply fast rank computation |
| General circuit | Reused gates counted once; DISJ and Horn expanders have O(n) nodes/wires despite large cut rank | No polynomial circuit-to-OBDD converter is shown |
| Circuit-to-CNF | TMR-1/050 standard functional Tseitin: n inputs, g gate identities -> V_CNF=n+g counted variables, at most 3g+n+1 distinct clauses, O((n+g)log(n+g)) encoded bits | Never replace the original input n by CNF V without charging the expansion; no Williams all-polynomial-size premise established |
| SAT / UNSAT | Fixed Horn/DISJ sources accept 0^n; unrestricted input decider may cheaply recognize such structures and use a correct fallback | No restricted representation lower bound forces an unrestricted SAT decider to construct a BDD |
| Model realization | Finite experiment constructs 0/1 truth tables in V8, GF(2) bit-row Gaussian elimination via BigInt XOR, and hash-conses reduced DAG nodes | No one-machine simultaneous DTISP lower bound is derived |

Circuit sharing and auxiliary variables are not silently unfolded. Invertible separate-cut bases preserve rank; integer Walsh-Hadamard is not invertible modulo 2. All accounting uses fixed formula assignment-evaluation matrices, not the SAT language's encoded-input function. No Valiant-Vazirani randomized isolation is treated as a deterministic reduction.

## 6. Four mandatory gates

| Gate | Status and reason |
| --- | --- |
| 1. DISJ sanity | **PASS** for fixed-order OBDD transfer; **FAIL** for any attempted unrestricted circuit/SAT transfer. The 2^k grouped rank coexists with the explicit 2k-node reordered BDD and linear circuit. |
| 2. Relativization | **PASS/RESTRICTED** as a purely finite algebraic BDD lemma, which may relativize. **OPEN** for unrestricted P-vs-NP promotion: a nonrelativizing step has not been supplied; Baker-Gill-Solovay blocks a fully relativizing separation. Algebrization/Natural Proofs audit remains OPEN for any future unrestricted constructive rank property. |
| 3. Simultaneous DTISP | **NOT APPLICABLE WITH REASON** to final graph-size lower bounds. **OPEN** for any proposed FLMV or SAT machine implication: no single total deterministic decider with strict time AND space bounds and all costs is constructed. Total sequential work and aggregate space are required for networks. |
| 4. Configuration counting | **PASS** as a direction/scope guard: a total deterministic read-only-input machine with workspace s and input length N has at most `2^O(s+log N)` configurations, hence a halting run at most that many steps, or `2^O(s)` if s>=log N. This is a runtime upper bound, never an OBDD/work lower bound; randomized and quantum machines require different accounting. |

## 7. Corpus reconciliation, prior art and next lemma

Read FIRST the SAT compression/circuit directive blob `7b8804dc7587abc5134055b5b0d16a143055ca5a`, then current proof1 (SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`), proof2 (SHA `930c5eeddafce656717f28055a7a9a755f44737c`), main.tex (SHA `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`), AGENTS, CODEX, repo skill, five current handoffs, issue #3 (2174 comments at read), and directly relevant TMR-1/050, TMR-2/050, TMR-5/046 reports/code. The connector returned **empty contents** for oversized proof2/main.tex despite their valid SHAs; full current bodies were **not independently recovered in this run**. Local git clone/preflight was unavailable due network resolution. No root edit was attempted. Historical `/341` FAIL as full logical UNSAT authority and `/386` RESTRICTED remain unchanged.

Already known: Bryant (1986) defined reduced OBDDs and variable-order sensitivity. TMR-2/050 established unique-solution, clause-order rank traps and requested precisely this fixed-order transfer. TMR-5/046 proved the all-balanced-cut Horn-expander rank firewall. TMR-1/050 established explicit functional Tseitin cost. **New in this run** is the precise frontier factorization transfer with early-terminal/skipping-safe V+2, its all-order Horn corollary, and independent complete small-order verification. This does not alter root proof chains. **TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.**

Primary literature: R. E. Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE Transactions on Computers 35(8), 1986, pp. 677-691, https://doi.org/10.1109/TC.1986.1676819 ; https://people.eecs.berkeley.edu/~russell/classes/cs289/f04/readings/Bryant:1986.pdf . TMR-5/046 cites Bova and Slivovsky, *On Compiling Structured CNFs to OBDDs*, SAT 2016, https://pubmed.ncbi.nlm.nih.gov/32025195/ . Baker, Gill, Solovay (1975), https://doi.org/10.1137/0204037 . Repo sources: TMR-1/050, TMR-2/050, TMR-5/046, named above. No novelty claim over classical OBDD communication arguments.

**One next lemma:** seek a *fully specified, adaptive, sharing-safe circuit-to-dynamic-cut interface* with operation-by-operation undercharging that remains small on every Horn expander, DISJ, affine and unique-solution control. Prove or falsify it against a compact shared circuit and a physical solver. An OPEN load-bearing transfer cannot be promoted. P versus NP remains OPEN.

**Evidence:** `experiments/tmr/tmr4_obdd_rank_transfer051.js` revision `tmr4_fixed_order_obdd_rank051.v1` and `results/raw/tmr/2026-11-15_1134_TMR4_FIXED_ORDER_OBDD_RANK_TRANSFER051_V8_RAW.json`; deterministic exhaustive, seed NONE, machine V8, errors ZERO. No Python stages. Standalone Node/CI and physical TM implementation not run.

END_OF_VERIFIED_REPORT::TMR-4::051
