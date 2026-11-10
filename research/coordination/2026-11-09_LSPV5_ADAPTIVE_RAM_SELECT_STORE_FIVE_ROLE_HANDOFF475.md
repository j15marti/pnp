# Handoff: exact adaptive RAM select/store, circuit frontier, and FLMV

**November 9, 2026 PST | User-directed interactive research | No schedule/route changes | P versus NP OPEN**

## Verified new control

Original-source-aware symbolic execution of **arbitrary data-dependent addresses** can be represented exactly by the read-over-write recurrence:

$$
E_0(a)=M_0[a],\qquad
E_j(a)=\mathrm{ite}(g_j\land a=a_j,\ v_j,\ E_{j-1}(a)).
$$

For $R$ reads and $W$ prior possible writes, there are at most $RW\le(R+W)^2/4$ equality/select pairs in this **particular** shared symbolic compiler. This is a standard array-logic induction and a polynomial syntax upper bound, not a time/space lower bound or a fully charged bounded-fan-in circuit. Address-width costs, initial memory selection, actual physical simulator time and simultaneous peak space remain separate. On a quadratic-size bounded-fan-in circuit, Williams 2025 gives only $\widetilde O(T)$ space relative to $T$ original memory operations, without preserving time. The arbitrary adaptive-RAM sublinear-space and **simultaneously time-preserving** bridge remains OPEN.

Independent finite controls: Python **16,984** and V8 **33,920** assertion checks, zero violations. All initial bit-array sources of $M=2,4,8$ and all source addresses at program depths $1..8$ tested; read-after-write aliases, conditional writes and data-dependent future addresses covered. No native FLMV machine was executed.

Artifacts:
- [Full interactive LSPV-5 report](../agents/lspv-5/2026-11-09_LSPV5_INTERACTIVE_ADAPTIVE_RAM_READ_OVER_WRITE475.md)
- [Symbolic Python compiler](../../experiments/review/lspv5_475_adaptive_symbolic_ram.py)
- [Independent JS replay](../../experiments/review/verify_lspv5_475_adaptive_symbolic_ram.mjs)
- [Raw results](../../results/raw/arc/2026-11-09_LSPV5_475_ADAPTIVE_SYMBOLIC_RAM_RAW.json)

## Strongest falsifiers for future runs

1. **Alias collision:** a read after two writes at the same symbolic address must select the *latest enabled* write, with legality and source provenance correlated.
2. **Unpaid oracle:** array select/store nodes are not physically unit-cost RAM reads in a bounded-fan-in circuit; charge their input mux, address comparator, value width, assembly, and peak memory.
3. **Quadratic frontier:** a generic $O(T^2)$ unrolled circuit followed by square-root circuit evaluation yields no $T^{1-\epsilon}$ space reduction. A near-linear circuit would help only if both its construction and time-bounded evaluation were proved.
4. **Probabilistic ORAM ≠ input-independent deterministic schedule:** the Goldreich-Ostrovsky / later statistical ORAM guarantees depend on probabilistic access distributions; they do not freely transfer to FLMV deterministic all-input SAT.
5. **Unknown SAT exponent:** a hypothetical time-preserving $\widetilde O(\sqrt{T})$ RAM simulator still conflicts with current SAT bounds only in a restricted low-$c$ interval, not for all possible fixed finite $c$.

## Existing role-specific requests, preserving exact allocations

- **LSPV-1 (Route B):** check conditional machine-model theorems and all-exponent quantifiers; compare Pippenger-Fischer, Goldreich-Ostrovsky, Williams 2025 and FLMV primary statements without model conflation.
- **LSPV-2 (Route A):** design/test implicit bounded-block predecessor locality (or provide counterexamples), with charged memory access and actual evaluation time; no semantic oracle.
- **LSPV-3 (Route B):** source-authenticate relational address aliases, last-write guards and shared-DAG dependencies; test all-input/malformed branch contexts.
- **LSPV-4 (Route A):** audit physical address widths, full same-machine T/S, random-access input mux, sparse normalization and recomputation if enabled; DO NOT reactivate a disabled role.
- **LSPV-5 (Route B):** red-team every proposed near-linear circuit or obliviousization, including random-coin fixing, budget overcharging, nonlinear shortcuts and scope leakage.

Every scheduled run reads both root trackers, governing handoff, issue #3, relevant original papers/repositories, and follows IDEA -> SEARCH -> ITERATE with falsifiers. Only true material node changes merit conflict-safe tracker updates; this interactive report has **TRACKERS REVIEWED; NO MATERIAL CHANGE**. No tasks, schedules, titles, enabled states, $R_{\mathrm{mix341}}$ grammar/weights or manuscript ownership changed.

**Precisely remaining:** a correct and uniform arbitrary-adaptive RAM simulation with simultaneously small *time and space*, applicable at every finite polynomial time exponent or a separately proved all-exponent reduction. **P versus NP remains OPEN.**
