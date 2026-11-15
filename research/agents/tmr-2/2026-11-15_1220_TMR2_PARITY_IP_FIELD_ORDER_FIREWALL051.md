# TMR-2/051: Exact characteristic-two versus rational-rank and variable-order firewall

**2026-11-15 12:20 PST | TMR-2 / PNP Information Necessity | Track A.**
**Status: PROVED/EXACT, restricted algebraic and fixed-order branching-program statements; independent mathematical review OPEN. Finite verification COMPUTATIONAL. Unrestricted SAT-machine/circuit transfer OPEN. P versus NP OPEN.**

## Candidate, object and precommitted falsifiers

Fix the projected **assignment indicator of one formula**, not SAT as a decision function on encoded formulas:
$$f_k(x,y)=\bigoplus_{i=1}^k(x_i\wedge y_i),\qquad x,y\in\{0,1\}^k.$$
Let $M_{\pi,p}$ be its prefix/suffix cofactor matrix at variable-order prefix $p$. $W_{\pi,p}$ is the number of distinct residual Boolean functions (including constant terminals), the minimum layer-state count in the fully leveled fixed-order deterministic read-once model.

Falsifiers declared before corpus/literature audit: (1) small characteristic-two rank may conceal exponentially many distinct residual functions; (2) large rational rank under a chosen order may collapse under a legal cheap alternative; (3) DISJ, equality and Horn graphs have high ranks but compact circuits; (4) CNF auxiliaries, an explicit witness, or bounded-treewidth DP may bypass the supposedly necessary computation. These are actual legal algorithmic controls.

## Theorem IPFIELD051-A and complete proof

For $M_k(x,y)=f_k(x,y)$ (a $2^k$ by $2^k$ 0/1 matrix), **for every $k\ge1$**:
$$\boxed{\operatorname{rank}_{\mathbb F_2}M_k=k,\quad
\operatorname{rank}_{\mathbb Q}M_k=2^k-1,\quad
|\text{distinct rows}(M_k)|=2^k.}$$
For grouped order $\pi_g=(x_1,\ldots,x_k,y_1,\ldots,y_k)$, the exact middle-layer width is $W_{\pi_g,k}=2^k$. For interleaved $\pi_a=(x_1,y_1,\ldots,x_k,y_k)$, **every** layer has width at most four, and peak width is four when $k\ge2$. A bounded-fan-in AND/XOR circuit evaluates $f_k$ using $O(k)$ gates and wires.

Proof: Over $\mathbb F_2$, the rows are the $k$-coordinate linear forms $\sum_i x_i y_i$, and the $k$ singleton-coordinate rows are independent. Every different $x$ defines a different row. Over $\mathbb Q$, define the Sylvester/Walsh matrix $H(x,y)=(-1)^{x\cdot y}$; then $M=(J-H)/2$. Since $HH^\top=2^k I$, the rows $H_x$ are independent. The $x=0$ row of $M$ is zero, and a linear relation among the nonzero rows would express a nontrivial dependence between $H_0$ and other $H_x$, impossible. Hence rational rank $2^k-1$. At the grouped middle cut, all $2^k$ residual rows differ, forcing exactly that number of deterministic layer states. In the interleaved order, a residual is determined only by the running parity and, between $x_i$ and $y_i$, one saved input bit, giving at most four states. Standard constant-gate XOR implementations yield the linear-size circuit. QED.

**Field firewall:** This changes the field, not an invertible local basis. Rank is invariant under separate invertible row/column transforms over any single field. Walsh-Hadamard is singular over characteristic two. Thus a proposed field-independent rank/width transfer is **FALSIFIED** here, while TMR-4/051's correct one-sided field-specific inequality remains intact.

## Strict proper 3-CNF, parsimonious projection, and shortcut

Use original variables $x_i,y_i$, $k$ distinct AND-gate variables $t_i=x_i\wedge y_i$, and $k-1$ distinct running-parity gates $p_i=p_{i-1}\oplus t_i$ for $i\ge2$ with $p_1=t_1$. Each AND is encoded with three clauses, each XOR with its four usual ternary clauses. A three-variable seven-clause pin gadget $P(z,a,b)$ forces $z=a=b=0$. Pad the two binary AND clauses with $z$ and the output unit requirement with $(p_k\vee z\vee a)$. The other AND clause and all XOR clauses already have three distinct literals.

Every clause is strict ternary, has three different variables, is non-tautological, and has no duplicate. The unique functional extension for each $(x,y)$ satisfies the full CNF if and only if $f_k(x,y)=1$. Thus the existentially projected relation is exactly $f_k$, **without** uncharged auxiliary multiplicity. Exact size:
$$V=4k+2,\quad C=7k+4,\quad\text{literal occurrences}=21k+12,\quad N_{\rm encoded}=\Theta(k\log k).$$
The full satisfiable-assignment count is $(2^k-1)2^{k-1}$, not $2^{2k-1}$. Projection rank is not asserted to equal an arbitrary cut rank of the full auxiliary-inclusive tensor, or the encoded-formula SAT decision language.

The projected relation is neither Horn, dual-Horn, bijunctive nor affine for $k\ge2$. At $k=2$, explicit bitmask closure witnesses in raw data (bit order $x_1,x_2,y_1,y_2$) violate coordinatewise meet, join, three-way majority and three-way XOR, respectively. It has six satisfying projected assignments at $k=2$, which also excludes affine structure.

**Bounded-treewidth control:** Put $z,a,b$ in every bag, use first bag $\{x_1,y_1,t_1,z,a,b\}$ and for each $i\ge2$ the bag $\{p_{i-1},p_i,t_i,x_i,y_i,z,a,b\}$, where $p_1=t_1$. Every clause is contained in a bag and variable occurrences are contiguous; bag size at most eight, so primal treewidth at most seven. The entire family has a uniform polynomial-time bounded-treewidth DP.

**Even cheaper explicit SAT witness:** Set $x_1=y_1=t_1=1$, all other $x_i,y_i,t_i=0$, all defined $p_i=1$, and $z=a=b=0$. A fixed correct total SAT decider can verify this computable assignment against the actual source in $O(N\operatorname{polylog}N)$ time with $O(\log N)$ work bits for these canonical encodings, and run an exact exhaustive fallback otherwise. No general polynomial-time SAT algorithm follows.

## Reproducible exact benchmark and ledger

Published executable: experiments/tmr/tmr2_ipfield_051.js, version ipfield051.v1, Node 22 / V8, no seed. Immutable raw JSON: results/raw/tmr/2026-11-15_1220_TMR2_IPFIELD051_V8_RAW.json. Exact GF(2) elimination uses BigInt bit rows. Rank modulo the **prime 65521** certifies the stated rational rank: a nonzero minor modulo the prime remains nonzero as an integer, and a matching structural rank upper bound comes from the proof above. It is not floating-point rank inference.

| k | rank GF(2) | rank Q | grouped middle width | interleaved peak width | ternary clauses |
|---:|---:|---:|---:|---:|---:|
|1|1|1|2|2|11|
|2|2|3|4|4|18|
|3|3|7|8|4|25|
|4|4|15|16|4|32|
|5|5|31|32|4|39|
|6|6|63|64|4|46|
|7|7|127|128|4|53|

**39,407 counted tests/assertions; zero failures.** Every projected input tuple was checked by constructing its canonical auxiliary extension for $k=1,\ldots,7$. For $k\le3$, every assignment to every source variable was exhaustively tested (largest $2^{14}$) to verify unique extension. DISJ, equality and singleton control matrices were independently calculated over GF(2) and modulo 65521. Finite checks remain COMPUTATIONAL; asymptotic claims rest on the written proof.

| Authentic control/resource | Verified/charged conclusion |
|---|---|
| DISJ$_k$ Horn 2-CNF | Rank $2^k$ over both fields with an $O(k)$ depth-two unbounded-fan-in circuit and obvious zero witness; **no general-circuit inference** |
| Equality product | Both ranks $2^k$; trivial uniform equality circuit |
| Single satisfying tuple | Rank one across any cut of its full indicator tensor |
| Horn expander | Existing TMR-5/046 all-balanced-cut exponential rank yet a linear-size circuit and all-zero SAT witness |
| Affine/Gaussian, Krom/SCC, autarky | These cheap mechanisms remain legal; current nonaffine projection also admits width-four parity-state computation |
| Padding and extension | Independent all-one tensor padding preserves old cut rank; every functional auxiliary is explicitly counted and uniquely determined |
| Source layout/sharing | $2k-1$ gate identities and $O(k)$ physical wires, counted once; grouped and interleaved strategies genuinely differ |
| Expensive benchmark | Explicit matrices have $4^k$ entries; materialization needs at least $\Omega(4^k)$ raw bits. Cofactor enumeration, elimination, modular arithmetic and all access/recomputation paid in the benchmarking program, not charged to SAT solvers |
| Cheap same-source computation | Bounded-treewidth DP and explicit witness test use polynomial time; no obligatory rank-matrix construction |

## Mandatory four gates

| Gate | Finding | Reason |
|---|---|---|
| DISJ sanity | **PASS** restricted, **FAIL** unrestricted transfer | High-rank DISJ has a linear circuit; no unrestricted rank transfer asserted |
| Relativization / algebrization / Natural Proofs | **PASS** for finite algebraic identity, **OPEN** for separation | No nonrelativizing bridge from this invariant to general SAT decision; a fully relativizing P-vs-NP separation is blocked |
| Simultaneous DTISP | **NOT APPLICABLE WITH REASON** to structural model; **OPEN** for FLMV | No one matched machine with both strict time and space in a forbidden region is constructed |
| Configuration counting | **PASS** upper-bound guard only | For deterministic total read-only-input machines $T\le 2^{O(s+\log N)}$, never a lower bound |

## Corpus reconciliation, literature and next lemma

Governing directive read FIRST (blob 7b8804dc7587abc5134055b5b0d16a143055ca5a). Reviewed TMR replacement, AGENTS.md, CODEX.md, pnp-research skill, all TMR handoffs and issue #3; originals TMR-2/050, TMR-4/051, TMR-5/046, and TMR-1 circuit-to-CNF resource ledgers. Root trackers read to available extent: proof1 SHA 06f7ebc8, proof2 SHA 930c5eed, main.tex SHA 6ac34c5d. The connector supplied **empty bodies** for oversized proof2 and main.tex, so their complete current contents were not recovered, no root material update is authorized, and repository preflight/full checkout/build could not run here.

**Duplication/reconciliation:** TMR-4/051 already established the standard field-specific rank-to-fixed-order-OBDD frontier inequality. TMR-2/050 already proved factor-order false positives; TMR-5/046 already provided expander all-cut controls. This report adds the exact reverse GF(2) rank/cofactor-width gap, characteristic contrast, strict ternary unique-extension projection, legal width-four reordering and constant-treewidth escape. It does not claim literature priority. Existing root conclusions and /341 FAIL full UNSAT, /386 RESTRICTED remain unchanged.

**Primary literature:** R. Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE Transactions on Computers 35 (1986), 677-691, https://doi.org/10.1109/TC.1986.1676819 ; L. Valiant and V. Vazirani, *NP Is as Easy as Detecting Unique Solutions*, Theoretical Computer Science 47 (1986), 85-93, https://doi.org/10.1016/0304-3975(86)90135-0. The latter's randomized unique-SAT promise reduction must not be mistaken for a free deterministic rank-preservation theorem.

**NEXT LEMMA:** Precisely characterize which fixed-field cut or cofactor measure survives a *charged uniform source-local adaptive order-selection algorithm* on restricted BDDs/circuits. Search for a family where every legal order costs more, then check compact circuits and general-SAT cheap paths separately. **TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE. P versus NP OPEN.**
