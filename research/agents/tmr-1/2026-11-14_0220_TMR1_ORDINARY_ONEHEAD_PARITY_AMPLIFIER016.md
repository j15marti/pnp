# TMR-1/016: ordinary single-input-head parity amplifier with charged binary work counters

**Date:** 2026-11-14 02:20 PST (America/Los_Angeles). **Role:** NEW TMR-1 Machine Model Lead. **Claim:** TMR1-OH16, **CANDIDATE/RESTRICTED**, pending independent TMR-5/TMR-4 review. **Finite evidence:** COMPUTATIONAL. **P versus NP:** OPEN.

## 1. New result and prior-art distinction

TMR-5/013 produced polynomially amplified cost underestimation for a permissive one-bit parity-erasing MAY abstraction, using one extra read-only input head as scanning head and $d$ more read-only input heads as positional odometer digits. It explicitly did **not** transfer its exact timing to the standard **one-original-input-head** machine. The present result supplies that missing model transfer by a different, paid, binary-work-tape implementation. It does not claim the exact TMR-5/013 multihead formula survives. That formula survives only in its declared multihead model.

### Theorem candidate TMR1-OH16

Let $A$ be any **one fixed** total correct uniform deterministic 3-SAT decider on all encoded binary input lengths, on a standard finite-alphabet multitape machine with one locally moving read-only original input head, left/right endmarkers and finite control. There is, for every fixed integer $d\ge0$, **one fixed** equally ordinary single-input-head wrapper $B_{A,d}$ using $d+1$ additional locally moving *writable* binary work tapes. On input $x$ of encoded length $L$, put $q=L+1$, and let $P(x)$ be XOR parity of the actual $L$ source bits.

The wrapper makes an outward physical scan and return, simultaneously building a little-endian binary $q$ register and computing $P(x)$ in finite control. It uses ordinary local read/write/increment transitions for the register. If $P(x)=1$, it executes $q^d$ additional full outward-and-return input-head sweeps, controlled by $d$ nested binary work-tape counters, all updates, comparisons, carry propagation and reset movements charged. It restores the original input head to the left marker and then starts $A$ with all original work tapes untouched.

Write $H_{A,d}(x)$ for the full charged wrapper prepass, including the parity gate, and $D_d^{\rm loc}(q)$ for its extra odd-parity delay. One can implement it so that

$$
2q+1\le H_{A,d}(x)\le6q+1,
\qquad
2q^{d+1}\le D_d^{\rm loc}(q)=O_d(q^{d+1}),
$$

and

$$
T_{B_{A,d}}(x)
=T_A(x)+H_{A,d}(x)
 +\mathbf 1[P(x)=1]D_d^{\rm loc}(q),
$$

up to a fixed number of initial/final control transitions, which can be absorbed consistently into $H$. The wrapper uses at most $(d+1)(\lceil\log_2(q+2)\rceil+3)$ extra **visited writable cells**. Its fixed source and work alphabets, tape count and program do not depend on $L$. Head positions encode no free oracle information. This is a **candidate exact construction** in a fully specified model, not a time lower bound on $A$.

The bound $H\le6q+1$ is obtained without an unbounded-word operation. Over $q$ binary increments starting at zero, bit $j$ toggles $\lfloor q/2^j\rfloor$ times; total bit-write transitions are less than $2q$. Each increment traverses its carry cells rightward and returns the work head leftward, contributing $2(\text{bit flips}-1)$ head movements. Thus the total counter work is less than $4q$ transitions. The original input head takes exactly $2q$ moves. The gate takes one transition. Each of $q^d$ later scans requires exactly $2q$ physical input-head movements. With $d$ fixed, all nested counter maintenance totals $O_d(q^d\log(q+2))$, absorbed in $O_d(q^{d+1})$. Every stored counter is bounded by $q$, so each additional work tape visits $O(\log q)$ cells.

### Unbounded polynomial distortion in the ordinary single-head model

Use the genuine, unbounded but **regular restricted** language $G$ whose original proper-3CNF clauses are sign triples on the three fixed variables. Each triple forbids one of eight assignments. A finite-control machine tracks the three-bit word position and an eight-bit forbidden-mask, and correctly labels SAT if some mask is absent, UNSAT if all eight occur, and MALFORMED if the binary length is not divisible by three. It needs **no writable cells** for classification, even for arbitrarily many clauses.

Combine this finite-control classifier with the preceding paid parity scan and delay. Define a source-bound MAY abstraction by forgetting **only** the finite-control parity bit, retaining the source, input and work-head positions, counters, mask, parser state, program and both terminal labels. Its gate includes the parity-zero skip branch, even when that branch is not reachable against the actual odd-parity source. Every actual primitive step maps to a cost-one abstract step; the quotient is forward cost-sound. The cheaper gate edge fails exact replay from a reached odd-parity gate state.

For every odd-parity valid $x$ of this restricted language, let $C(x)$ be the actual total physical transition cost and $M(x)$ the minimum abstract terminal path cost. The entire even-gate physical prefix is a valid MAY path, so $M(x)\le H(x)\le6q+1$, while the actual odd execution incurs $2q^{d+1}$ further real head moves. Therefore

$$
\frac{C(x)}{M(x)}
\ \ge\
1+\frac{2q^{d+1}}{6q+1}
\ =\ \Omega(q^d).
$$

For every fixed polynomial exponent $r$, choosing a fixed $d>r$ gives one fixed standard single-input-head machine and cofinally many valid lengths where the ratio eventually exceeds $q^r$. This is **not** per-length nonuniform minimization, because $d$ and the program are fixed before the input length varies. It also does **not** assert that every cost-sound abstraction loses parity; retaining that one gate-relevant bit repairs this example.

There are both SAT and UNSAT odd-parity length-unbounded controls: the SAT stream is 001 followed by any number of 000 triples. The UNSAT stream contains all eight triples 000 through 111, then 001, then any number of 000 triples. All-eight basic triples have even parity; the additional 001 makes it odd. Correctness and the gap hold on both labels, not just malformed inputs.

For the explicitly given potential, set $\Phi(F,p)=2q-p+1$, $\Phi(R,p)=p+1$, $\Phi(G)=1$, $\Phi(D)=\Phi(H)=0$ for the outward, return, gate, delay and terminal abstract phases. Paid work-tape microsteps in the outward phase leave $p$ unchanged and satisfy $\Phi(u)\le1+\Phi(v)$; all source moves lower the potential by at most one; both abstract gate branches obey the same inequality. All terminal potentials are zero. Thus $\Phi(\mathrm{initial})=2q+1$ is a **valid but merely linear** lower bound, consistent with arbitrarily large odd-source underestimation. No unknown runtime is defined as the potential.

## 2. Independent audit of TMR-5/013

The original TMR-5/013 report, exact JavaScript and raw counter ledger were directly read. Its multihead odometer claim is consistent: for $q^d$ leaf sweeps the dedicated scan head pays $2q^{d+1}$; a positional digit at level $j$ increments a total $q^j$ head cells and physically returns the same $q^j$ cells across carries, yielding precisely

$$
D_d^{\rm multihead}(q)
 =2q^{d+1}+2\sum_{j=1}^d q^j.
$$

The original model has $d+1$ extra read-only heads; their positions encode $O(d\log q)$ bits not counted as writable work cells. The current one-head construction **uses paid writable binary counters instead**, so its delay is a different function, bounded above/below as proved above. The earlier independent discovery that TMR-4/016's simulator read a bit while on the left marker is also confirmed from the source analysis. The present implementation reads data only from current physical positions $1,\dots,L$ and reads no adjacent cell.

**Peer verdict:** TMR-5/013's exact formula is valid in its *declared multihead model*, subject to its exact phase protocol. It cannot be substituted as an exact cost in the present ordinary single-head model. All general-SAT lower-bound implications remain OPEN.

## 3. Actual executable evidence and controls

The source file is experiments/tmr/tmr1_onehead_parity_counters016.cjs; its immutable raw evidence is results/raw/tmr/2026-11-14_0220_TMR1_ONEHEAD_PARITY016_RAW.json. The **exact source** was directly executed as a standalone function in hosted V8, then written verbatim as Node-compatible JavaScript and read back. The code has independent current-cell input-head movements, local binary work-tape heads, separate charged read/write/head-motion steps, explicit binary counter equality/reset, full original source readback and a source-independent set-based classifier for correctness controls. Program-level recursive nesting is fixed by $d$ and can be unrolled into finite control; no dynamic stack or growing-word arithmetic is needed in the specified machine. Numeric host values are used **only** to audit bounds and count tests, not as a decision oracle.

| $d$ | Sources | Charged transitions | Peak visited extra work cells | Largest measured odd/cheap ratio |
|---:|---:|---:|---:|---:|
| 0 | 515 | 27,098 | 5 | 1.462 |
| 1 | 259 | 51,155 | 12 | 16.094 |
| 2 | 67 | 208,674 | 18 | 428.919 |
| 3 | 35 | 4,707,375 | 24 | 11,988.019 |
| **Total** | **876** | **4,994,302** | | |

Every fixture verifies the actual SAT/UNSAT/MALFORMED label, source parity, all input-head restoration, actual $q^d$ sweeps, complete transition partition, visited-cell logarithmic cap and minimum physical swept-work lower bound. The fixtures exhaust binary strings through length 8, 7, 5, 4 respectively, plus four 24/27/25-bit adversarial SAT, UNSAT and malformed controls per $d$. No randomness. Errors: zero. An actual odd 27-bit UNSAT control had physical/cheap ratios 16.094, 428.919 and 11,988.019 for $d=1,2,3$.

**Limitations:** The executing program is a microinstruction-ledger simulation, not a mechanically generated finite transition table or native OS-TM emulator. The asymptotic construction is argued mathematically; finite tests are only COMPUTATIONAL. Neither a native Node replay nor an independent native Python implementation was performed this run. Full repository preflight.py and LaTeX compilation were not run because the connector has no locally checked-out repository. There is no unrestricted SAT solver time bound and no claim of an upper bound on the unknown $T_A$ for arbitrary $A$.

## 4. Dependencies, falsifiers, literature and next arrow

The model transfer improves the scope of TMR-5/013's **abstraction-counterexample** from a declared multihead source interface to an ordinary local-input-head machine with fully charged $O(\log L)$ writable storage. It **does not** improve any lower bound on correct general 3-SAT deciders. Inert parity can be safely erased, as TMR-4/016 explains; cost-relevant parity cannot be erased by the same source-oblivious MAY rule. The construction treats compact GF(2), Horn, 2-SAT, bounded-treewidth solvers, products, sharing, renaming, padding, auxiliary variables and recomputation as permitted arbitrary behavior inside the untouched $A$. No result assumes any of those representations must be expanded.

Primary sources checked at declared scope:

1. P. Cousot and R. Cousot, *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints*, POPL 1977, pp. 238-252, https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml . Sound MAY abstraction is not guaranteed to preserve exact minimum cost.
2. E. Clarke, O. Grumberg, S. Jha, Y. Lu and H. Veith, *Counterexample-Guided Abstraction Refinement*, CAV 2000, pp. 154-169, https://doi.org/10.1007/10722167_15 . Spurious counterexample paths require a feasibility test; this does not create an unrestricted cost lower bound.
3. F. C. Hennie and R. E. Stearns, *Two-Tape Simulation of Multitape Turing Machines*, JACM 13(4), 1966, pp. 533-546, https://doi.org/10.1145/321356.321362 . Classical fixed-tape simulations are different from assuming arbitrary extra read-only heads are free. No Hennie-Stearns theorem is used to derive the stated exact costs.

**Corpus read:** superseding directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; full proof1.txt 28,714 bytes SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; full proof2.txt 1,051,196 bytes recovered from authenticated Git blob 930c5eeddafce656717f28055a7a9a755f44737c; full main.tex 2,525,134 bytes recovered from Git blob d3db01d221df39f096f31237643268132edfcd87; AGENTS.md, CODEX.md, skill, issue #3 through TMR-5/013, all five latest handoffs, original TMR-1/015, TMR-3/014, TMR-4/016, TMR-5/013 reports/source/raw, and relevant historical resource-governance notes. Older role identities were not reactivated. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical root main.tex stays unchanged, owned by TMR-5. No tasks or schedules were touched.

**One next target:** TMR-5 should independently replay the exact one-head code and inspect the binary counter head-local realization, especially the $6q+1$ first-sweep bound and the all-source forward cost simulation. TMR-2/TMR-3 should test whether any source- and program-sensitive quotient can remove *provably inert* dependencies without permitting cost-relevant gates; TMR-4 should prove a noncircular all-transition abstraction schema. Until an all-machine, all-polynomial-exponent necessity and its unrestricted transfer are proved, P1-01/P1-03/P1-04 and P2-00 remain OPEN.

END_OF_VERIFIED_REPORT::TMR1::2026-11-14_0220_PST
