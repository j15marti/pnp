# TMR-2/050: Exact proper-3CNF dynamic prefix-rank order firewall

**2026-11-15 11:19 PST (America/Los_Angeles) | TMR-2 / PNP Information Necessity | Track A**

**Scientific status:** **PROVED/RESTRICTED** for the explicitly defined CNF and matrices, independent mathematical peer review OPEN. Finite exact Q and GF(2) checks are **COMPUTATIONAL**. No general SAT circuit or machine lower bound. **P versus NP remains OPEN.**

## 1. Precise target and precommitted falsifiers

**Candidate C050:** For a fixed strict proper-3CNF F with a declared x:y cut, the peak rank of *prefix products of actual clause-indicator functions*, minimized over legal clause-factor multiplication orders, might be a more meaningful dynamic obstruction than one static matrix rank. Specifically define

\[
\rho_{\mathrm{prefix}}(F;X:Y)=\min_{\pi}\max_{0\le t\le |F|}
\operatorname{rank}_{\mathbb Q}M_{\bigwedge_{j\le t} C_{\pi(j)}}(X,Y),
\]

after certified constant-size existential pin elimination as explicitly qualified below. This is a property of a **fixed formula's partial assignment evaluation relation**, not SAT on encodings, not an arbitrary adaptive contraction machine, and not a lower-bound theorem.

Four falsifiers specified before the source/corpus review:

1. A cheap, admissible clause order collapses an exponentially large intermediate rank on the very same source.
2. DISJ retains exponential rank *for all orders at completion* but its decision/evaluation circuit is linear size.
3. An invertible basis-change argument silently crosses from Q to GF(2); integer Walsh-Hadamard is singular in characteristic two.
4. A correct total solver first checks a constructive all-zero witness and accepts in linear source time, despite large displayed ranks.

**Outcome:** all four controls identify genuine limits. We give an explicit, *unique-satisfying*, strictly ternary family for falsifier 1 and direct calculations for the others. The repaired useful candidate is only a **model-scoped, charged Boolean-semiring contraction cost** with preprocessing/order discovery included; no universal implication is asserted.

## 2. Exact strict-3CNF construction and theorem

For each integer k>=1 use variables x_1,...,x_k, y_1,...,y_k, and fresh global z,a,b. Let P(z,a,b) be the conjunction of the **seven** distinct width-three clauses forbidding each assignment to (z,a,b) other than (0,0,0). Every clause has three distinct variables and contains no literal-complement pair. Thus P has exactly one satisfying triple, (0,0,0).

Define the **EQPIN** formula

\[
E_k=P(z,a,b)\land
\bigwedge_{i=1}^k
\left[(\neg x_i\lor y_i\lor z)\land
(x_i\lor\neg y_i\lor z)\land
(\neg x_i\lor a\lor b)\right].
\]

It has precisely 2k+3 variables and 7+3k proper ternary clauses, 21+9k literal occurrences and encoded length \(\Theta(k\log k)\) with binary variable identifiers. It has the **unique full satisfying assignment** 0^(2k+3). Indeed, P forces z=a=b=0, the first two clauses then enforce x_i=y_i, and the last enforces x_i=0, hence y_i=0.

With P already certified, compare two prefix multiplication orders on the x:y evaluation matrix:

- **Bad:** Multiply both equality clauses for every i *before* the x_i pin clauses. At that intermediate prefix, the matrix is exactly I_2^{\otimes k}, with rank **2^k over every field**. The final matrix is the rank-one projector onto x=y=0.
- **Good:** Multiply all k x_i-pin clauses *before* any equality clause. Every prefix matrix has precisely one potentially nonzero row (x=0), so rank is **exactly one at every prefix**. The clauses then force y=0 without increasing rank.

This proves the exact, unbounded-order gap

\[
\boxed{\max_t\operatorname{rank}M_{\mathrm{bad},t}=2^k,\qquad
\max_t\operatorname{rank}M_{\mathrm{good},t}=1.}
\]

No projection or forbidden algebraic oracle is needed: P is a fixed seven-clause pin gadget and all factors occur in the original strict 3CNF. Clause multiplication order is a legal algebraic computation choice. It follows that **the exponentially large intermediate rank of a prescribed order is not an intrinsic necessity for the same formula**. More generally the complete satisfying-assignment indicator of any unique-solution formula is a product of coordinate delta functions, so *every* full-assignment cut has rank one (zero for UNSAT). This observation does not make randomized Valiant-Vazirani isolation a free deterministic reduction.

## 3. DISJ, expander and basis hostile controls

**Strict 3CNF DISJ:** Set

\[
D_k=P(z,a,b)\land\bigwedge_{i=1}^k
(\neg x_i\lor\neg y_i\lor z).
\]

Its x:y evaluation matrix after pin certification is \(D^{\otimes k}\), where \(D=\left(\begin{smallmatrix}1&1\\1&0\end{smallmatrix}\right)\), so its Q and GF(2) ranks are 2^k and it has exactly 3^k full satisfying assignments. Nevertheless 0^(2k+3) satisfies it, and a linear-size depth-two AND-of-clauses circuit evaluates it. Thus **even the min-order peak must be >=2^k**, since the completed matrix itself has that rank, yet ordinary SAT decision remains cheap. DISJ is an irrevocable false positive for any static/dynamic rank-to-general-SAT-time inference.

**Strict 3CNF expander-graph controls:** For graph G=(V,E) append the same P gadget and ternary clauses \((\neg x_u\lor\neg x_v\lor z)\) for all edges. P forces z=0, recovering the all-negative Horn graph relation exactly while retaining strict clause width three. The cube Q3 has 8 graph vertices and 12 edges; the Petersen graph has 10 vertices and 15 edges. Both accept the all-zero witness; finite cuts below reproduce exact Q=GF(2) ranks. TMR-5/046 already proved exponentially large *all-balanced-cut* rank on bounded-degree expanders with Horn controls, which this report adopts rather than reclaims. No inference from graph-expansion rank to decision hardness survives.

**Walsh-Hadamard field guard:** \(H=\left(\begin{smallmatrix}1&1\\1&-1\end{smallmatrix}\right)\) is invertible over Q, and

\[
HDH^\top=\begin{pmatrix}3&1\\1&-1\end{pmatrix}.
\]

Both D and HDH^T have rank two over Q. But det H=-2, so H is singular modulo two. Over GF(2), D has rank two whereas HDH^T has rank **one**. Never advertise this as a rank-preserving GF(2) local basis change.

## 4. Reproducible independent exact finite audit

Published standalone Node-compatible JavaScript (also executed in hosted V8) uses **BigInt rational fractions with gcd reduction** for Q Gaussian elimination and a separately implemented BigInt bit-row GF(2) eliminator. It builds the *actual strict 3CNF source clauses* and matrix entries, not a rank formula substituted for computation. There are no random seeds: the listed cut partitions are fixed.

| Family | Parameters | Exact Q rank / GF(2) rank | Other exact check |
| --- | --- | --- | --- |
| EQPIN E_k, bad and good | k=1..5 | bad 2,4,8,16,32; good 1 each | 1 full assignment; final rank 1 |
| DISJ D_k | k=1..5 | 2,4,8,16,32 | 3,9,27,81,243 solutions |
| Strict-ternary cube Q3 Horn control | 3 balanced cuts | 7,7,6 in both fields | all-zero witness |
| Strict-ternary Petersen Horn control | 3 balanced cuts | 6,12,11 in both fields | all-zero witness |
| Integer Walsh test | 2x2 | Q 2 to 2; GF(2) 2 to 1 | invalid change of characteristic rejected |

All EQPIN source encodings were exhaustively checked for unique full satisfiability through k=5. The executable verifies each ternary clause has three distinct variable IDs, rejects duplicate source clauses, and verifies the all-zero witness. Every matrix pivot is exact. The finite arithmetic operation counters and intermediate rational numerator/denominator bit lengths are in raw JSON. **All checks passed; zero failures.** These are finite checks, not time measurements or asymptotic rank proofs; the symbolic construction establishes the latter.

Reproduction: run the standalone source using \`node experiments/tmr/tmr2_dynamic_prefix_rank050.js > /tmp/tmr2_050.json\`. The JSON object should match the immutable raw result after whitespace-insensitive parsing:

- Executed source: \`experiments/tmr/tmr2_dynamic_prefix_rank050.js\`, Git blob **9a527541ee4d0432cc949ae43730a6d42bc4fcac**
- Exact raw results: \`results/raw/tmr/2026-11-15_1119_TMR2_DYNAMIC_PREFIX_RANK050_V8_RAW.json\`, Git blob **7e7dd0913f1b49f97808c5bac3332855fa87124b**
- Version v1.0.0, no randomness, CPython cross-check performed locally on representative ranks but not a published independent reimplementation.

## 5. Same-realization and representation resource ledger

| Resource | EQPIN E_k | DISJ D_k | Explicit charge/limit |
| --- | --- | --- | --- |
| Encoded source variables | 2k+3 | 2k+3 | global 3-variable pin counted |
| Strict ternary clauses | 7+3k | 7+k | no hidden auxiliary extension |
| Literal occurrences | 21+9k | 21+3k | distinct clauses; length \(\Theta(k\log k)\) |
| Clauses to parse / witness-check | O(k) | O(k) | **one fixed all-input correct decider** can parse, test allzero, and otherwise invoke exact exponential fallback |
| SAT time on these particular families | O(N) | O(N) | witness checked during streaming; every source symbol charged, output YES |
| Retained workspace on these paths | O(log N) | O(log N) | for parser/index/active-clause counters; output is a decision bit |
| Exact-rank benchmark memory | >=2^(2k) matrix entries | >=2^(2k) entries | deliberately exponential test apparatus, NOT a SAT decision cost |
| Benchmark Q arithmetic | BigInt exact fractions | BigInt exact fractions | pivot counts, numerator/denominator bit lengths persisted |
| Discovery, caching, rereading, switching | may be paid | may be paid | no free general optimal-order search; **the exhibited order itself is explicit** |

The same fixed fallback decider is total and correct on all encoded CNFs: validate the source, evaluate allzero, return YES if true, and otherwise use exhaustive assignments with verification. Its **all-input worst case is exponential**, so this is NOT a P=NP algorithm. The O(N) times are for these *explicit families only*. A local basis change does not remove enumeration costs in general. The good order is explicit here; we do not claim all CNFs admit polynomially discoverable low-peak orders, and sharing/rewiring remains legal.

## 6. Mandatory four-gate decision table

| Gate | Verdict | Exact reason |
| --- | --- | --- |
| **1. DISJ sanity** | **PASS as falsification** | Strict ternary D_k preserves full 2^k rank but has O(k) evaluation circuit and easy witness; rank-to-general-circuit lower-bound implication **FAILS**. |
| **2. Relativization** | **NOT APPLICABLE WITH REASON** for the exact finite/symbolic rank lemma | No separation attempted. Any eventual all-machine proof needs an identified nonrelativizing step; Baker–Gill–Solovay, algebrization and Natural Proofs audits remain **OPEN** for such a transfer. |
| **3. Simultaneous DTISP** | **NOT APPLICABLE WITH REASON** to algebraic prefix-rank identities; **OPEN** for unrestricted transfer | No FLMV forbidden-pair claim. The one explicitly exhibited all-input correct fallback solver has jointly accounted O(N) time and O(log N) workspace **on this easy family**, not on all inputs. |
| **4. Configuration counting** | **PASS as upper-bound guard** | For fixed deterministic total read-only-input machine, T<=2^O(s+log N), or 2^O(s) if s>=log N. This is only a runtime upper bound given space; no mandatory work lower bound inferred. |

Controls and scope: Horn, 2-SAT, equality/union-find, affine/Gaussian, bounded-treewidth, simple autarky/forced literals, product decomposition, compact CNF/circuits, and padding all remain legal. Our EQPIN exhibits equality plus forced-zero shortcut; DISJ is product/Horn/2-SAT; graph controls are Horn. Extension variables are fully counted; nonunique new variables can change solution counts. XOR isolation remains randomized and promise-sensitive. The tensor here is **not** the SAT decision function on formula encodings. Underlying arithmetic Q vs characteristic-two must not be conflated.

## 7. Literature and corpus reconciliation; next lemma

Primary literature: Valiant and Vazirani, *NP Is as Easy as Detecting Unique Solutions* (TCS 1986), https://doi.org/10.1016/0304-3975(86)90135-0 ; Baker, Gill and Solovay, *Relativizations of the P=?NP Question* (SIAM J Comput 1975), https://doi.org/10.1137/0204037 ; Reingold, Vadhan, Wigderson, *Entropy Waves, the Zig-Zag Graph Product, and New Constant-Degree Expanders* (Annals 2002), https://annals.math.princeton.edu/2002/155-1/p04 . Exact published expander rank proof and 452-cut finite control were recovered from **TMR-5/046**; no new priority is claimed for that theorem. Historical TMR-2/043-046 already falsified separator-rank and nonlinear multiscale static tariffs via cheap SAT source families; /047-048 established scoped physical read information tariffs only O(N). /049's counted majority CNF guard remains separate. These controls are retained, not retitled as hardness.

Governing directive: \`research/coordination/2026-11-15_SAT_COMPRESSION_CIRCUITS_FIVE_AGENT_REFOCUS.md\` on main SHA **7b8804dc7587abc5134055b5b0d16a143055ca5a**. Read AGENTS.md, CODEX.md, repository skill, current five TMR handoffs and issue #3. Root proof1.txt visible SHA **06f7ebc8c2283304a0f5200b518c6e48fa41e343**. Large proof2.txt SHA **930c5eeddafce656717f28055a7a9a755f44737c** and main.tex SHA **6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34** were present, but their content was returned empty by the connector; this run does **not** claim independently recovered their full bodies. Repository-local \`preflight.py\`, full suites and LaTeX were not executable without a checked-out repo. No shared root edits were attempted.

**TRACKERS REVIEWED AT AVAILABLE CURRENT CONTENT/METADATA; NO MATERIAL CHANGE.** /341 remains **FAIL** as a full logical UNSAT authority and /386 **RESTRICTED**. No identity, title, schedule, ownership or enabled state changes.

**Next sharply defined lemma:** For a declared **read-once OBDD order**, prove a width/rank transfer with exact per-edge branching-program cost, then test whether reordering/sharing or Horn/Q3 preprocessing makes the lower bound vanish. TMR-4 should independently audit the circuit-to-cut direction: is the proposed transfer limited to OBDDs or does cheap fan-out invalidate it? TMR-3 should retain same-execution time/space. An unrestricted SAT solver/circuit lower bound remains **OPEN**.

**P versus NP remains OPEN.**
