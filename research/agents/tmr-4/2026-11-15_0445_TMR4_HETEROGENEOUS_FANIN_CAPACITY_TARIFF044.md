# TMR-4/044: Exact integer-capacity fusion tariff for heterogeneous shared-gate DAGs

**2026-11-15 04:45 PST (America/Los_Angeles).** Governing directive: `research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md` SHA `54c9177fc211dfca6c94d89d6ebbf3f3908809d6`.

**Scientific classification:** PROVED/RESTRICTED as a symbolic theorem in the precisely qualified preauthenticated gate-builder system below; independent mathematical peer review OPEN. Finite executed V8 evidence COMPUTATIONAL. Superpolynomial initial SAT potential and arbitrary-machine same-system transfer OPEN. P versus NP OPEN.

## 1. Candidate and falsifiers fixed before source/literature retrieval

**Candidate:** A nonlinear integer capacity-cover component repairs TMR-1/043's raw connected-component tariff when the authentic shared gate language contains multiple priced fan-ins, preserving DAG reuse and obtaining the *exact minimum whole-DAG paid cost* rather than a rounded-down fractional lower bound.

1. **F1:** A legal free operation merges input-connected components. Then the component drops at cost zero.
2. **F2:** A genuine paid gate has more inputs or less cost than the declared catalog. The tariff may overdischarge.
3. **F3:** Sharing, NOT, free SELECT, constants, alternative output gates or unrecognized Boolean equivalence completes AND_n with fewer paid gates than capacity-cover predicts.
4. **F4:** Source authentication, SAT decision, parsing, Gaussian elimination, learning or a physical finite-tape program is silently identified with this preauthenticated gate-building calculus.

F1 and F2 are authentic falsifiers in **enlarged** systems, not transitions of the qualified system. F3 is ruled out within the stated complete gate grammar by the connectivity theorem. F4 remains OPEN for transfer and is not CEGAR-refined away.

## 2. Source, state, complete legal operations and zero closure

Reuse TMR-1/043's explicitly authenticated proper-3CNF Craig source pair $A_n,B_n$, $n\ge2$, with $4n$ clauses on side A, $5n-1$ on side B, $9n-1$ total, $6n-1$ source variables, and binary encoded length $N_n=\Theta(n\log(n+2))$. Their disjoint shared-variable projections are $U=\{1^n\}$ and $V=\{0,1\}^n\setminus\{1^n\}$; therefore their unique extensional separator is $\mathrm{AND}_n$. This source is kept *unchanged*: a different machine model is not claimed.

Qualify the explicitly distinct circuit-builder $R_{\mathrm{CAP}}(\mathcal K)$. State $C=(A_n,B_n,G,P,q,v,h)$ stores the entire append-only shared Boolean gate DAG $G$, the paid gate-identity ledger $P$, selected output $q$, reversible metadata view $v$, and completed-goal flag $h$. Input wires $x_i$, constant wires 0/1 and unlimited fanout/reconvergence are available. A finite positive-price catalog $\mathcal K=\{(a,w_a)\}$ lists **native** $a$-input AND gate instructions with $a\ge2$, exact rational prices $w_a>0$. Gate arguments may repeat or be constant 1, so an $a$-gate can join any $d+1\le a$ existing distinct components. APPEND_AND_a is charged $w_a$ once on a new, unique gate identity. APPEND_NOT has fixed price 1. Reusing, reading, sharing, branching/reconverging, and selecting any already built wire cost no extra *gate-construction* events. SELECT, NOP and reversible metadata VIEW have price 0 and create no gates or wires. Actual GOAL holds only if the selected output computes $\mathrm{AND}_n$ for all common inputs; it is a predicate, never a free SAT oracle operation. Completed states are absorbing. **No** other wire-creating, inference, bulk-merge, source-read or physical-machine action is legal in this qualified laboratory. Those operations are MAY, not excluded, in a broader proposed SAT-machine simulation.

The true zero-cost SCCs consist of alternative selections/views of one fixed paid DAG, and all zero-reachable states have the **same** gate dependency graph. A directed authentic zero step never changes an input connectivity component. For an actual machine, zero-cost closure is entirely different and must be proved separately.

## 3. The explicit integer capacity-cover obstruction

Ignore gate-edge orientation solely to define connectivity among the $n$ original input vertices. Let $c(G)$ be their number of connected components. Define the exact finite, nonnegative rational capacity-cover function

$$
H_{\mathcal K}(1)=0,\qquad
H_{\mathcal K}(c)=\min_{(a,w_a)\in\mathcal K}
\left\{w_a+H_{\mathcal K}(\max\{1,c-a+1\})\right\}\quad(c\ge2).
$$

Equivalently,

$$
H_{\mathcal K}(c)=
\min\left\{\sum_a w_a z_a:
\sum_a(a-1)z_a\ge c-1,\ z_a\in\mathbb Z_{\ge0}\right\}.
$$

This is an **explicit small unbounded integer capacity-cover recursion**, not the unknown optimal complexity of an arbitrary Boolean function. Define the canonical seven-vector in order CNF, XOR, SEP, FUS, GAMMA, INTERFACE, MACHINE by

$$
\mathbf p(C)=(0,0,0,H_{\mathcal K}(c(G)),0,0,0).
$$

For a unit-price catalog containing every arity $2,\ldots,f$,

$$
\boxed{H_f(c)=\left\lceil\frac{c-1}{f-1}\right\rceil.}
$$

This integer rounding is needed: a raw linear weight on $c-1$ obtains only $(n-1)/(f-1)$, while the rounded dynamic component proves the attainable integer bound.

## 4. All-step theorem, simulation relation and tariff matrix

**Theorem (PROVED/RESTRICTED).** For every fixed finite positive-rational catalog and every legal transition of $R_{\mathrm{CAP}}$, the seven-coordinate potential with $\lambda=(0,0,0,1,0,0,0)$ satisfies $\lambda^\top\Delta_r\le w(r)$. All completed goals have potential zero, and

$$
\boxed{\min_{\text{completed shared DAG }G} W_{R_{\mathrm{CAP}}}(A_n,B_n)
=H_{\mathcal K}(n).}
$$

**Proof of local inequality.** An appended $a$-input gate may merge at most $a$ existing input-connected components, and thus $c'\ge\max(1,c-a+1)$. The capacity-cover recursion is nondecreasing in $c$. Prepend that same gate to an optimal capacity cover for $c'$; hence $H(c)\le w_a+H(c')$. NOT and authentic zero-cost operations preserve $c$, so their discharge is zero. Every goal computing AND_n depends essentially on all $n$ input bits, making them all connected to the selected output within the undirected DAG; $c=1$ and $H(c)=0$. Telescoping proves the lower bound. For the matching upper bound, start with $n$ singleton components, and follow an optimal capacity-cover sequence, each time AND-combining $\min(a,c)$ current component conjunctions and filling unused native inputs with constant 1. This reduces the component count by $\min(a-1,c-1)$, preserves every input variable, and attains $H(n)$ at exact gate price. Every paid identity occurs once, with arbitrary sharing permitted. Thus the minimum is exact.

**Conservative abstraction:** Map full concrete $G$ to the partition $\Pi_G$ of the original inputs induced by undirected gate connectivity, retaining the current metadata view; retain the authenticated input and paid ledger in the related concrete state rather than claiming the partition recovers them. APPEND_AND_a maps to the abstract union of the at-most-$a$ predecessor-component blocks at cost $w_a$; APPEND_NOT maps to an unchanged partition at price 1; SELECT/VIEW maps to an unchanged partition at zero. Every concrete step therefore has an abstract one-step successor of identical or lower cost. An abstract $c=1$ MAY-goal can be an overapproximation (not every connected DAG computes AND_n); every genuine completed goal nonetheless maps to one, preserving all real cheap paths and never deleting genuine paths through CEGAR. Literal SAT correctness, parsing, and machine control are not abstractions justified by this simulation.

**Exact rule-by-component matrix:** all coordinates but FUS have zero discharge. APPEND_AND_a has $\Delta_{\rm FUS}=H(c)-H(c')$, $0\le c-c'\le a-1$, and cost $w_a$. NOT has $\Delta=0$, cost 1. SELECT, VIEW, NOP have $\Delta=0$, cost 0. This schema is complete for **all** legal transitions and all $n$, not merely sampled rows. The attached JSON enumerates individual partition/view rows for $n\le5$ plus the symbolic general rule schema.

**Exact rational LP and dual:** At any fixed $n\ge2$, maximize $H(n)\lambda_{\rm FUS}$ with $\lambda\ge0$ and one tariff inequality per legal row. $\lambda=1$ satisfies every inequality. A matching upper dual places unit mass on every transition of an explicit optimal AND-construction path; the weighted sum of those row constraints is $H(n)\lambda\le H(n)$, since its discharges telescope to $H(n)$ and its costs sum to $H(n)$. Hence the LP and dual both have exact optimum $H(n)$. All arithmetic can be normalized to integer half-units for the four published catalogs; the symbolic proof holds for arbitrary positive rational prices.

## 5. Authenticated hostile traces and model boundary

- **Raw component FAIL in the richer real ternary system:** with three isolated inputs, one authentic price-one AND3 merges all three and changes $c-1$ by 2. The old $\lambda_{\rm FUS}=1$ for raw $c-1$ overcharges 2 for a step costing 1. The repaired $H_3$ changes by only 1.
- **One-price AND4 FAIL if imported into a fan-in-three model:** at four isolated inputs, $H_3(4)=2$ and a one-price AND4 would take it directly to zero. That added operation is genuine only in the enlarged catalog and must not be CEGAR-deleted there. Recomputing $H_4$ repairs the tariff.
- **Free MERGE FAIL if imported:** even one directed zero-cost connection from separated inputs to connected inputs decreases $H_3$ without charge; its reverse need not exist. SCC contraction alone cannot repair a directed free edge. Directed zero-reachability saturation collapses the scalar potential accordingly.
- **Sharing/compact circuit control:** reusable outputs, repeated wires, constants, NOT, output changes, and branch reconvergence cannot join more than the paid gate's fan-in, so none invalidates the model-specific proof. They remain legitimate features rather than free-work assumptions.
- **Affine, Horn, 2-SAT, separator-DP, autarky, definition, learned-clause, equality and SAT-specific algorithm controls:** these are not primitives of the *preauthenticated circuit construction service*. Their inclusion in a real SAT machine may produce a cheaper decision without constructing this separator, so transfer is OPEN, not established by this report. In fact the published $A_n,B_n$ source pattern is compact and structurally recognizable and must not be treated as a hard SAT family.

## 6. Reproducibility and dependence ledger

**Native executed evidence:** exactly serialized `audit()` in `experiments/tmr/tmr4_capacity_fusion094.js`; `results/raw/tmr/2026-11-15_0445_TMR4_CAPFUS094_NATIVE_V8_RAW.json` and `results/raw/tmr/2026-11-15_0445_TMR4_CAPFUS094_MATRIX.json` contain raw counters and exact-rational finite rows. V8 checked 303,760 assertions, including 133,276 paid partition rows, 4,616 two-view zero SCCs, 75 independent tight primal/dual checks and 51 explicit AND-source construction steps, with zero failures. Partitions for $n=2,\dots,7$ were enumerated exhaustively for four priced catalogs; $n\le5$ full rows are published. Finite tests are **COMPUTATIONAL**. The general theorem is symbolic and independently reviewable.

**Corpus:** first governing directive, replacement directive, proof1 full current blob SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`, proof2 authentic full Git blob SHA `930c5eeddafce656717f28055a7a9a755f44737c` (1,051,196 characters), root main.tex authentic Git blob SHA `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34` (2,545,859 characters); current issue #3; AGENTS.md, CODEX.md, skill, five handoffs; original TMR-1/043 report, JS and matrix; TMR-2/043 nonlinear rank report and exact CHECK matrix; TMR-5/039 BATCH-EQ rank matrix; original TMR-4/043 physical multip
ort I/O code and result; LEAD-0029 October squeeze audit. All root files were recovered and left unchanged.

**Primary methodological literature inspected:** P. and R. Cousot, "Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints," POPL 1977, DOI https://doi.org/10.1145/512950.512973; J. Krajíček, "Interpolation theorems, lower bounds for proof systems, and independence results for bounded arithmetic," J. Symbolic Logic 62 (1997), DOI https://doi.org/10.2307/2275578. These are background methods, not a source for the newly proved capacity-cover theorem.

**Dependency/qualification:** R_CAP authenticated shared circuit-building transitions, zero SCC, tariff and exact LP PASS/PROVED RESTRICTED. False raw connectivity tariff in widened fanin FAIL. Free merge/cheap wide-fanin controls FAIL only upon explicitly expanding the model. Finite tests COMPUTATIONAL. No genuine physical SAT algorithm-to-circuit-builder simulation. Source-authentication and gate-construction costs not forced on arbitrary correct deciders. Initial $H(n)=O(n)$, thus strictly below the superpolynomial target. Same-system SAT transfer, superpolynomial initial gap and P versus NP OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt, proof2.txt and main.tex unchanged. Historical `/341` FAIL on full accepted language; `/386` RESTRICTED to guarded fragment. Existing five schedules and ownership untouched.

**Next TMR-4 target:** charge the *actual physical finite-tape program* that recognizes and solves TMR-2/043's nonlinear signed-NAE family, carrying its complete source parser, dynamic state, witness construction and final decision through an all-step cost-underestimating abstraction, then explicitly test whether any nontrivial SAT-specific component survives that genuine polynomial path.
