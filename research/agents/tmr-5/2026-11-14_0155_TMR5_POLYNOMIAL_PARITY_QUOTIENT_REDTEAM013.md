# TMR-5/013: polynomially amplified parity-quotient undercharging and one-cell off-head audit

**Date:** 2026-11-14 01:55 PST (America/Los_Angeles). **Role:** new TMR-5 Machine Bottleneck Redteam and canonical synthesis owner. **New amplified example:** CANDIDATE/RESTRICTED pending TMR-1/TMR-3/TMR-4 independent review. **Peer verdict:** TMR-4/016 inert-erasure exactness and the single optional-roundtrip gate obstruction survive mathematical review after a concrete one-cell input-read correction, at PROVED/RESTRICTED model scope. **Finite tests:** COMPUTATIONAL. **Unrestricted 3-SAT separation and P versus NP:** OPEN.

## 1. Independently checked peer claim and smallest implementation defect

I read the ORIGINAL TMR-4/016 report, source and raw result, as well as TMR-3/014 original source/report/raw and TMR-2/015. The TMR-4/016 executable (blob `6a4300b02c7c0598bd04bd42d8374c7002975673`) takes its initial source-head position to be 0 (left endmarker), but its outward step reads `x.charCodeAt(s.p)` whenever `s.p<L`. Therefore for every nonempty source it reads the first data bit on the **left-endmarker** transition, before physically visiting data cell 1. At position L it does not read the last data cell. This is a genuine one-cell lookahead in that particular *finite simulator*, rather than a legal transition of a standard source-reading locally moving TM.

This does **not** falsify TMR-4/016's symbolic two-sweep theorem. Exact repair: update parity, last-bit and clause-mask registers only when the current physical position satisfies `1 <= p <= L`, reading `x[p-1]` on the transition from cell p to p+1. Position 0 reads the left marker, position L reads the last data bit before moving onto the right marker. It still takes exactly L+1 right moves and L+1 return moves. TMR-3/014's separate native physical trace already uses this correct current-cell rule, `bits[head-1]` with `1 <= head <= n`.

Under this repair, TMR-4/016's claims follow directly. Erasing a parity register that never controls any transition yields a strong cost-exact quotient: all other fields, next-state control, actual work, source, both terminal labels and each transition remain the same. When parity controls an extra scan, erasure leaves a sound existential MAY simulation but introduces a cheap abstract gate edge that cannot be replayed from an odd source's reached gate state. Refinement must retain the parity bit or establish a genuine source-conditioned reachability invariant. The real extra scan is not spurious.

**Replay distinction:** this audit statically examined TMR-4's exact published JavaScript but did not natively execute that original source. The separate executable below is independently authored and was directly executed in hosted V8. An independently written Python enumerator was executed natively in the local container, and is **LOCAL-ONLY**, not a published GitHub verifier.

## 2. NEW TMR5-PQ13: an arbitrarily high polynomial gap caused by erasing one bit

Fix an integer d >= 0, chosen once when the program is compiled. Use a deterministic locally moving **multihead read-only source model** with d+1 auxiliary input heads, plus any original heads/work tapes of a fixed total correct 3-SAT decider A. All heads initially sit at the left endmarker, every head moves at most one cell per transition, and every movement/finite-control gate is charged one transition. The number of heads is fixed for each d, independent of input length. The auxiliary heads read only the same immutable input; no source symbol is supplied by an oracle. On input x, set L=|x| and q=L+1.

A uniform wrapper B_(A,d) first runs a q-step outward parity scan on one dedicated head and a q-step return, leaving all original A heads and writable work untouched. At its gate, parity 0 starts A; parity 1 executes a dummy detour consisting of q^d complete outward-and-return journeys of the scanning head, controlled by d further source-head **positions** as q-state odometer digits, then starts A. Each counter-head increment costs one rightward movement; each reset traverses all q positions leftward and is fully charged. A executes unchanged on the original input, so SAT, UNSAT, malformed behavior, totality and all-length uniformity are preserved. This theorem concerns timing under a declared multihead model, not a new SAT algorithm.

The exact detour cost in the stated one-head-move-per-transition phase protocol is

$$
D_d(q)=2q^{d+1}+2\sum_{j=1}^{d}q^j.
$$

Proof: q^d leaves each require 2q physical scanning-head moves. Odometer digit j, counting from the outermost, incurs q^j rightward increments and q^j leftward reset moves across all nested iterations. Every head returns to position zero. No counter update, reuse, terminal output or input reread is uncharged. The d=0 convention has one roundtrip and an empty counter sum.

Therefore, with the same A and same source x,

$$
T_{B_{A,d}}(x)=T_A(x)+2q+1+
\mathbf{1}[P(x)=1]\left(2q^{d+1}+2\sum_{j=1}^{d}q^j\right).
$$

All auxiliary head positions are physical state; they are not counted as writable *work-tape cells*. In the finite-control restricted instantiation below, visited writable work cells are zero, but the d+1 head positions provide O(d log q) bits of positional state. **This is not a claim of zero total configuration information.** With one original read-only input head only, a charged head-position compiler or writable counters are needed; exact runtime/space costs of that different model are NOT inherited for free.

### One-bit MAY quotient and Bellman check

Take the physical configurations of this **fixed program and fixed source** and erase only the parity/last-read control register, retaining phase, all source-head positions, any A work tapes and work heads, clause-mask state, source binding and output label. At the return gate the resulting MAY graph contains both a parity-zero skip and a parity-one detour transition, even though only one is actually reachable from the fixed input. Both have nonnegative unit cost. Every concrete transition still has its projected abstract edge at exactly cost one, and both terminal labels are preserved. This is a cost-sound forward simulation, not a cost-exact bisimulation.

For the finite sign-stream controller, define the abstract potential

$$
\Phi(F,p)=2q-p+1,\quad\Phi(R,p)=p+1,\quad
\Phi(G)=1,\quad\Phi(D)=\Phi(H)=0.
$$

Here D includes every detour and odometer phase. These functions obey `Phi(u) <= 1+Phi(v)` on **every** abstract edge, including both gate branches, every counter movement/reset and the final halt, with `Phi(H)=0`. The shortest abstract terminal cost is exactly 2q+1: prepass and return cannot be bypassed, while the false parity-zero gate branch can skip the detour and still preserve the correct SAT/UNSAT label. On every true odd-parity source the actual runtime is larger by exactly D_d(q), hence

$$
\frac{T_{\mathrm{actual}}(x)}{d_{\mathrm{MAY}}(x)}
=1+\frac{D_d(q)}{2q+1}=\Omega(q^d).
$$

For any prescribed constant polynomial degree d this is one **fixed** uniform source program over arbitrarily long inputs, using d fixed additional source heads; no per-length advice, unbounded word arithmetic, oracle, SAT-solver template or free lookup construction occurs. This shows that even losing **one finite-control bit** can destroy *any program-independent constant-factor or fixed-degree approximation guarantee* for the minimum cost of a permissive MAY quotient in this multihead class. It is an obstruction to a proposed abstraction, **not** a SAT decision lower bound. For arbitrary A, the quotient's total cost also includes its true T_A(x), so only the additive D_d(q) gap is guaranteed without an upper bound on A.

Exact repair: retain the physically computed parity through the gate. A quotient restricted to truly source-reachable states could also be exact, but its correctness is a separate reachability proof and is not a free SAT oracle or an operational runtime bound.

## 3. Actual executed tests and hostile controls

New **independently authored** standalone program `experiments/tmr/tmr5_parity_amplifier013.cjs` was directly executed as functions in hosted V8, then its exact functions were serialized with `Function.prototype.toString` and published as a Node-compatible standalone file. It uses no peer imports or wrapper. It checks the legal read location on the first left-marker move, every physical one-head move (including all odometer resets), every actual Bellman inequality, flipping erased parity on every reached state, terminal parser labels with an independent set-based evaluator, the parity-spurious gate, and the **exact** cost D_d(q).

| Parameter | Executions (inert + gated) | Charged steps | True odd-source spurious paths |
|---|---:|---:|---:|
| d=0 | 516 | 9,898 | 129 |
| d=1 | 516 | 25,768 | 129 |
| d=2 | 516 | 197,958 | 129 |
| d=3 | 126 | 66,878 | 31 |
| **Total** | **1,674** | **300,502** | **418** |

The tested restricted input grammar is the authentic three-variable proper three-literal sign-stream 3-CNF language: every three bits encode one of eight forbidden assignments, SAT iff fewer than eight assignments are forbidden, UNSAT iff all eight occur, and malformed for incomplete triples. It is **not** general NP-complete 3-SAT. The fixtures include all binary strings through length seven for d<=2, through length five for d=3, and genuine 24/27-bit SAT and UNSAT controls for d<=2. Full totals: 468 SAT, 6 UNSAT and 1,200 malformed executions, zero assertion failures. The 418 true odd-source paths incur 275,092 additional physically charged transitions; the proved primary-scan lower portion is 243,834 transitions.

A separate **native CPython** implementation independently evaluated all one-head moves and positional-counter updates over 450 additional runs, totaling 196,124 charged moves (231 SAT, three UNSAT, 216 malformed), 226 odd detours and zero assertions. Its exact file `/mnt/data/tmr5_independent_parity013.py` is LOCAL-ONLY and must not be described as a repository publication. No native OS Node replay of the newly published JS, arbitrary-general-SAT TM compiler, full `preflight.py` or LaTeX compilation was executed.

## 4. Dependency synthesis and scientific firewall

1. **PROVED/RESTRICTED after independent symbolic review:** TMR-3/014's genuine two-crossing global-suffix dependence can occur even in linear time; TMR-4/016's inert parity is safely erased after the current-cell correction, while its gated parity cannot be erased without a replay-spurious abstract path. Neither observation gives processing hardness.
2. **NEW CANDIDATE/RESTRICTED, pending peer review:** the exact multihead odometer amplification and one-bit Bellman underestimation above. Finite executions remain COMPUTATIONAL.
3. **CONDITIONAL:** the all-transition cost-sound simulation/potential lemma gives only `Phi(initial) <= T_A(x)`; a superpolynomial initial potential requires a separate noncircular proof and cannot be obtained by deleting real cheap paths.
4. **OPEN unrestricted transfer:** every correct fixed total uniform ordinary deterministic 3-SAT machine, all integer time exponents k, all polynomial workspace regimes, same-machine charges, both SAT and UNSAT labels, arbitrary compact encodings and source rereads. Head positions, cache/recompute, Horn, 2-SAT, Gaussian XOR/Tseitin, bounded treewidth, products, padding and sharing remain allowed. No target arrow is closed by this report. A correct polynomial 3-SAT algorithm is a legitimate alternative endpoint.

**Next precise target:** TMR-1 or TMR-4 should independently review the present same-source all-edge multihead theorem, especially the read-location repair and the odometer cost formula. Then seek a *computably justified*, program- and source-sensitive abstract quotient that is strong enough to retain every cost-relevant gate without simply replaying the entire unknown execution. TMR-5 should challenge that quotient on freely reencoded, cached, algebraic and recomputing machines.

## 5. Sources and publication inventory

Primary sources checked for their actual scope:
1. P. Cousot and R. Cousot, *Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints*, POPL 1977, pp. 238-252, https://doi.org/10.1145/512950.512973 . Conservative abstract execution is background, not a time lower bound.
2. E. Clarke, O. Grumberg, S. Jha, Y. Lu, H. Veith, *Counterexample-Guided Abstraction Refinement*, CAV 2000, pp. 154-169, https://doi.org/10.1007/10722167_15 . Source-path feasibility must be established before a MAY path is discarded.
3. L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6) (2005), pp. 835-865, https://doi.org/10.1145/1101821.1101822 . This is a restricted simultaneous low-space result, not an unrestricted all-polynomial-time lower bound.

Original peer reports/code/raw: TMR-3/014, TMR-4/016, TMR-2/015, TMR-1/015 and TMR-5/012; original literature sources verified, no historical legacy checker reclassification. Controlling 12:49 PST replacement directive read FIRST (SHA `47459817e66dccf1f3079e6c724c0fd2643e7bc4`). Both entire trackers recovered (proof1 28,714 chars SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`, proof2 1,051,196 chars via authenticated blob SHA `930c5eeddafce656717f28055a7a9a755f44737c`), main.tex complete 2,522,180 chars (SHA `903092cd483c0b17694c9f500fa03b5a703508cc` at preflight), latest issue #3, AGENTS.md, CODEX.md, pnp-research skill and five current handoffs. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No task or schedule mutation.

**Shared GitHub artifacts:** this report, `experiments/tmr/tmr5_parity_amplifier013.cjs` (blob `04a314930338e7374a0f9f568bf5baa7a5081d3c`), `results/raw/tmr/2026-11-14_0155_TMR5_PARITY_AMPLIFIER013_RAW.json`, and the updated TMR-5 handoff. Verify all files by readback before claiming publication. Root main.tex is TMR-5 synthesis-owned; its update and readback are recorded separately in issue #3. **P versus NP remains OPEN.**
