# LSPV-5 manual research audit: random-access FLMV-compatible theorems and the adaptive-address barrier

**November 9, 2026 (PST) | Direct user-requested interactive research | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Research question.** Can Williams's 2025 space-efficient time simulation, or another known theorem on random-access machines, be combined with the Fortnow–Lipton–van Melkebeek–Viglas (FLMV) SAT time-space bounds, **without** the postulated universal iterative contraction [P2-A2]?

This is a separate interactive study; it does not claim to be a scheduled LSPV-5 research run or to modify any tasks. Current project obligations [P1-01], [P1-03], [P1-04], [P2-A1], [P2-A2], [P2-A3], [P2-A5], [P2-C3] remain as previously marked. Both complete root trackers were read. No material node status was changed: **TRACKERS REVIEWED; NO MATERIAL CHANGE**.

## IDEA: Attempt a same-machine time-to-space bridge

Fix a uniform total deterministic SAT decider $A_P$ that is correct on every binary source, including malformed encodings, with runtime $T_A(N)=N^{c+o(1)}$ on the exact FLMV indexed random-access machine. Assume only SAT in P, so $c$ is an unknown *fixed finite* exponent, potentially arbitrarily large. Attempt to convert $A_P$ to a correct, **simultaneously fast and small-space** deterministic decider $B$ satisfying a known SAT time-space forbidden inequality. A more limited candidate is to make memory access oblivious and invoke Ryan Williams's 2025 square-root-space theorem.

Falsifiers fixed before reviewing and testing:
1. A computation's next read/write address can depend on its input or a prior read and cannot be computed from the time index alone.
2. A time-to-space simulator fails to preserve a sufficiently small time exponent, or incurs nontrivial machine-conversion overhead.
3. A collecting abstraction of addresses loses correlation and invents impossible data, while an exact relational abstraction remains cheaply representable.
4. The optimized deterministic SAT space lower bound and the postulated simulator's space upper bound do not cross for all possible finite $c$.

## SEARCH: original theorem statements and precise model matching

### The exact model

FLMV, *Time-Space Lower Bounds for Satisfiability*, JACM 2005, section 2.1: a uniform deterministic random-access Turing machine can have multiple index/non-index tapes; index-tape addressing moves a non-index head in one step and erases the index; source input is read-only; non-index space is measured by the largest accessed/indexed position, and can exceed time on the original machine. The same section permits an **equivalent sparse representative** storing only accessed cells, with space at most time and *polylogarithmic time overhead*. This is an equivalent-machine bound, not a measurement of the original native machine. [1]

### Model-and-proof ledger

| Result | Exact applicable scope | What is proved | Where the bridge fails |
|---|---|---|---|
| Fortnow, *Time-Space Tradeoffs for Satisfiability*, JCSS 2000 | General random-access (includes nondeterministic lower-bound statements) | Essentially linear-time SAT is incompatible with sufficiently sublinear workspace | Does not constrain unknown large polynomial $c$ |
| Fortnow–Lipton–van Melkebeek–Viglas, JACM 2005, Thm 1.1; Cor. 5.8 | General **deterministic random-access TM** | For all $c<\varphi$ some positive space exponent excluded; displayed branch $\beta(c)=((c+2)/c^2-c)/2$ when positive | Requires an **independent simultaneous space upper bound** |
| FLMV, Sec 2.1 sparse representation | Same RAM/TM computational power after equivalent-machine sparse normalization | Time $T$ gives a normalized representative with $S\le T$ at polylogarithmic time overhead | Space exponent essentially $c$; noncontradictory |
| Williams, *Inductive Time-Space Lower Bounds for SAT*, Computational Complexity 2006/2007 | Random-access machines; **subpolynomial space** | Excludes SAT at $N^{\sqrt3}$ time with $N^{o(1)}$ space | Does not imply every SAT-in-P machine uses subpolynomial space |
| Buss–Williams, CCC 2012 | Random-access SAT $DTISP(N^{c+o(1)},N^{s+o(1)})$, specified alternation-trading | Necessary $c+s\ge 2\cos(\pi/7)\approx1.801937736$; stronger parameter tradeoffs also studied | With $s\le c$ it remains compatible for arbitrary large $c$ |
| Ryan Williams, STOC 2025, Thm 1.1 and Remark 1.6 | Multi-tape TMs; extension to random-access only with suitably *oblivious*, efficiently accessible register schedules | $\mathrm{TIME}[T]\subseteq\mathrm{SPACE}[O(\sqrt{T\log T})]$ for multitape; $O(\sqrt T\operatorname{polylog}T)$ for the qualified oblivious model | **Does not preserve a time-$T$ bound**; arbitrary *adaptive* random-access extension explicitly open |
| van Melkebeek–Raz, TCS 2005 | One $d$-dimensional work tape, random access to **input only** | SAT pure-time lower bound $N^{a}$ for $a<\sqrt{(d+2)/(d+1)}$ | Not FLMV's unrestricted arbitrary work-tape random-access model |
| Savitch, 1970 | General nondeterministic-space to deterministic-space simulation, with model representation qualifications | $\mathrm{NSPACE}(s)\subseteq\mathrm{DSPACE}(s^2)$ for suitable $s$ | No preservation of small deterministic running time; NP verifier != deterministic UNSAT decider |

Sources read: FLMV full original PDF (especially section 2.1, Theorems 1.1/5.7 and Cor. 5.8); Williams's original 2025 paper (Theorem 1.1, Remark 1.6, Sec 4.1 and Discussion); Buss–Williams 2012 original paper; Williams 2006/07 original abstract; van Melkebeek–Raz original article; Fortnow JCSS 2000.

**Model caveat.** Williams's 2025 paper explicitly presents arbitrary random-access $T\mapsto T^{1-\epsilon}$ space simulation as an *open question*. It notes that arbitrary data-dependent accesses create computation-graph indegrees too high for the direct bounded-fan-in block-tree method. Do not silently turn its oblivious special case into a generic FLMV machine theorem.

### A useful direct inequality, but no contradiction for arbitrary polynomial $c$

For simultaneous deterministic SAT time/space exponents, Buss–Williams's necessary product inequality gives

$$
c+s\ge 2\cos(\pi/7)\approx1.801937736.
$$

The 2005 displayed FLMV branch additionally gives $s\ge\beta(c)$ where positive. If **one additionally assumed, without proof**, a time-preserving RAM simulator $s\le c/2$, then:

$$
c/2<\beta(c)\quad\Longleftrightarrow\quad 2c^3-c-2<0,
$$

which holds for $1\le c<c_*=1.1653730430624147\ldots$ (positive root of $2c^3-c-2=0$). The stronger Buss–Williams product condition would be violated when

$$
3c/2<2\cos(\pi/7)
\quad\Longleftrightarrow\quad
c<\tfrac43\cos(\pi/7)\approx1.20129182387.
$$

For $c=6/5$, $\beta=23/45\approx0.51111$ and $s=c/2=0.6$ **do not** violate the displayed 2005 branch; however $c+s=1.8<1.801937736$ **would** violate the later product constraint **if** the time-preserving RAM simulator actually existed. This is a conditional numerical calculation, not proof of that simulator. For $c=2$, $s=c/2=1$ is not excluded by either. An arbitrary P exponent $c$ cannot be assumed to lie in either forbidden interval.

## ITERATE: a restricted adaptive-address counterexample

### Theorem RAM-OBLIVIOUS-1 (PROVED/RESTRICTED)

Fix $d\ge1$, $M=2^d$, and independent Boolean cells $y_0,\ldots,y_{M-1}$ in a read-only addressable table. An input includes a $d$-bit address $a$, and the desired answer is $\operatorname{INDEX}_M(a,y)=y_a$.

A native random-access algorithm reads the address $a$ and makes **one data-table probe** at address $a$. Consider instead a simulator constrained to a fixed sequence of data-table reads, where that sequence is independent of both $a$ and the table contents; it may perform arbitrary computations on the values observed but has **no other access to table bits**.

**Then every correct deterministic simulator of this restricted kind must query all $M$ distinct table cells**, so it needs at least $M$ table probes.

*Proof.* If it omits a cell $j$, take input address $a=j$ and two tables $y,y'$ that agree on every queried cell and differ only at $j$. All data probes return identical observations; the simulator therefore returns the same bit on both inputs, whereas the correct results $y_j$ and $y'_j$ differ. Contradiction. The full-scan schedule attains the bound. QED.

**Limits:** Here the source already has $N=M+d$ bits; a bound $M=\Theta(N)$ is **not** exponential in input size and proves nothing about SAT. The lower bound only applies to an input-independent, fixed-schedule, bit-probe access model; preprocessed index structures, structured or correlated data, circuits, multiple-pass encoding and different machine policies are outside the stated proof.

### Theorem RAM-ABSTRACT-2 (PROVED/RESTRICTED)

Consider the program: initialize an $M$-cell table to zero; write $1$ at address $a$; read at address $a$; output. Every concrete execution returns $1$. The domain

$$
A^\#=\mathcal P(\text{write addresses})\times\mathcal P(\text{read addresses})
$$

with each projection independently abstracted to all addresses forgets the cross-time relation. Its Cartesian concretization admits a write at $u$ followed by a read at $v\ne u$, spuriously returning $0$. A relational domain retaining the invariant $\texttt{writeAddress}=\texttt{readAddress}$ restores exactness with a compact $O(\log M)$-bit symbolic constraint.

This is a demonstrable precision failure in naive Abstract Interpretation, not a lower bound on symbolic representation size, SAT time or machine space.

### Adaptive memory dependency frontier

For read $r_i$ at address $a_i$, the relevant prior write is the **most recent** $j<i$ such that $w_j=a_i$, if any. In an arbitrary adaptive RAM computation each $w_j$, $a_i$ and the stored values can depend on earlier data. A naive static all-possibilities dependency graph potentially links a read to every preceding write, giving $\Theta(T^2)$ candidate pairs over a $T$-operation transcript. This is a worst-case size for the *particular all-pairs construction*, not a lower bound for all circuit representations or for actual memory. Because the access schedule itself is computation-dependent, it cannot be supplied as Williams's input-independent oracle without an additional proof.

**Candidate CEGAR repair, still OPEN:** maintain a relational abstract state with (source identity, symbolic address equations, last-write provenance, equality/alias classes, cross-branch history). Given a requested read, attempt to prove a bounded-size set of possible last writes; if the set is too large, refine based on a concrete input/trace. Show for **every** possible polynomial-time SAT solver that this process is uniform, total, source-correct, uses charged memory and has a sufficiently small simultaneous time exponent. None of those unrestricted bounds is established. A fixed-source feasible test is not enough.

## COMPUTATIONAL validation and raw materials

- Python: $703{,}136$ assertion checks for $d=1,\ldots,9$, **zero failures**.
- Independent JavaScript/V8: $1{,}051{,}638$ checks for the same range, **zero failures**.
- $1{,}022$ omitted-cell two-table adversarial pairs validated.
- $348{,}502$ off-diagonal cross-address pairs showing spurious results after marginalization.
- Bad-address controls read the other cell and correctly return zero.
- Executable files: 
  - \`experiments/review/lspv5_manual_adaptive_random_access_probe.py\`
  - \`experiments/review/verify_lspv5_manual_adaptive_random_access_probe.mjs\`
  - \`results/raw/arc/2026-11-09_1914_LSPV5_MANUAL_ADAPTIVE_RANDOM_ACCESS_RAW.json\`
- These are independent finite controls in simplified abstract machine semantics, not an implementation of a historical FLMV checker.

## Repo continuity and scientific boundary

Read full \`proof1.txt\` (blob \`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b\`) and \`proof2.txt\` (prepublication blob \`a73beac1143490e4f18ae498a1f65b63ef5b4ac3\`), current \`research/coordination/2026-11-09_1624_ASSUMED_TIME_DERIVE_SPACE_FLVM_FIVE_ROLE_HANDOFF.md\` (blob \`644b0d4745f2edeb8718c7e536a7da995b36b36f\`), LSPV-5/473, and relevant Grok REWIRE and Claude ONETAPE reports. Change-aware reviews of \`konard/p-vs-np/scripts/proof_status.json\` (blob \`93b77ed3d8fe456f81c690035f45f07910a247f2\`) and \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` (blob \`18d693ea71dfa433370eb7afbebc3106e32f03e5\`) found no generic random-access SAT time-to-space theorem. Primary literature was located via internet searches and original published PDFs. This interactive task did **not** run repository-wide preflight or authoritative historical R_mix341 certificate checking, did **not** change \`main.tex\`, and did **not** modify any task or other agent-owned files.

## References

[1] Fortnow L, Lipton R, van Melkebeek D, Viglas A. *Time-Space Lower Bounds for Satisfiability.* JACM 52(6), 2005. https://lance.fortnow.com/papers/files/tst.pdf

[2] Fortnow L. *Time-Space Tradeoffs for Satisfiability.* JCSS 60(2), 2000. https://www.sciencedirect.com/science/article/pii/S0022000099916719

[3] Williams RR. *Inductive Time-Space Lower Bounds for SAT and Related Problems.* Computational Complexity 15, 2006. https://link.springer.com/article/10.1007/s00037-007-0221-1

[4] Buss SR, Williams RR. *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds.* CCC 2012. https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/samCCC-cr.pdf

[5] Williams RR. *Simulating Time with Square-Root Space.* STOC 2025, Thm 1.1 and Remark 1.6. https://people.csail.mit.edu/rrw/time-vs-space.pdf

[6] van Melkebeek D, Raz R. *A Time Lower Bound for Satisfiability.* TCS 348 (2005): 311–320. https://www.sciencedirect.com/science/article/pii/S0304397505005402

[7] Savitch WJ. *Relationships Between Nondeterministic and Deterministic Tape Complexities.* JCSS 4 (1970): 177–192.

## End-of-study status

**Actual advance:** a rigorously scoped input-adaptive lookup obstruction and an explicit abstract-domain correlation failure, together with a machine-model ledger of applicable SAT time-space bounds. **Verification:** two independent finite checks, no failures, raw files saved. **Remaining gap:** a true, arbitrary-adaptive-random-access, uniform and both-label time-to-space simulation with a *simultaneous* runtime exponent capable of violating FLMV/Buss-Williams for **every** fixed polynomial-time SAT exponent. That implication is OPEN. **P versus NP remains OPEN.**
