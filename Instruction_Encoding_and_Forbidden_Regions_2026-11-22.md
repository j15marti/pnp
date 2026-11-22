# Instruction count, program encoding, and forbidden regions

22 November 2026, America/Los_Angeles.

Status: definitions, elementary scoped bounds, and transfers of existing time-space exclusions. No unrestricted superpolynomial instruction lower bound for T5, compact T_q, or SAT is proved. This is an additive publication and technical answer, not a scheduled agent run or a claim of living-manuscript reconciliation.

## 1. Four different quantities

Fix one uniform deterministic program A, a finite instruction set, a precise encoding, and an N-bit input x.

| Quantity | Definition | Interpretation |
|---|---|---|
| L_A | Number of stored instruction records | Static program length in records |
| B_A | Encoded program length in bits | Static program description |
| I_A(x) | Number of executed instruction occurrences | Dynamic execution count, including repeated loop bodies |
| W_A(x) | Sum of the declared primitive bit costs of those occurrences | Charged computation rather than a unit-cost macro count |

A fifth quantity, an explicitly materialized execution trace, records instructions, operands or states over time. It is not automatically stored by a solver.

In a fixed bit-machine instruction model, I and elapsed primitive time T agree up to constants. In a bounded-word RAM model, each instruction may process O(log N) bits or incur a larger polylogarithmic bit cost. Transfer to a bit-machine theorem needs an actual simulation. An instruction that solves arbitrary SAT at unit cost is not permitted.

## 2. What minimal instruction encoding actually says

If K opcodes all use a fixed-length binary opcode field, its width is at least ceil(log_2 K). If a format must also distinguish every combination of d independent direct operands among M addresses, its fixed-length record needs at least

    ceil(log_2(K M^d))

bits. A separated-field implementation uses ceil(log_2 K) + d ceil(log_2 M) bits, plus any immediate values or flags.

These are counts of representable instruction records in that format, not a claim that every algorithm pays d log M bits afresh on every operation. Relative addressing, implicit destinations, pointer increments, register-indirect addressing, loops and shared code can avoid repeating those explicit fields. The bits manipulated in dynamic address registers still have their actual operation/storage costs.

With variable-length prefix-free instruction codes and opcode distribution P, the mean opcode length is at least H(P). This is an average source-coding bound, not a lower bound of log K on every individual instruction.

If an architecture literally refetches the full encoded record on every execution, total code-fetch bit traffic is

    F_fetch(x) = sum_{j=1}^{I_A(x)} length(instruction executed at j).

That is a valid architecture-specific ledger. A model permitting decoded instruction caches or fixed finite control need not pay the same repeated record-reading cost. Cache construction and retention should be charged when they actually occur.

## 3. Why growing static program-size lower bounds cannot hold here

There is one fixed finite brute-force program for each of T5, compact Q, and SAT. It parses the input, enumerates candidate assignments, evaluates constraints, and halts with the correct answer.

Therefore there is a constant B_0 such that a correct unrestricted-time solver has B_A <= B_0 for all N. The minimum static program length without a time restriction cannot grow as Omega(N), let alone superpolynomially in N.

The same loop may execute exponentially many times while occupying a constant number of stored instruction records. Large dynamic execution cost does not imply large static code.

If all B_A program bits are physically retained through T steps, that component contributes B_A*T to input-inclusive CM. For a fixed uniform program B_A is constant, so this does not create a new asymptotic hardness exponent.

An N-dependent program A_N, hardwired advice, or a separate circuit for every input length is a different model. Such descriptions must be counted, and construction/evaluation costs included when a uniform claim is intended.

## 4. Executed-instruction forbidden regions

For the compact regular-tournament decision language Q, use the established local SAT reduction and the compatible deterministic machine model.

If one counted instruction is a bounded bit-machine step, the known time-space exclusions are already instruction-count/workspace exclusions. If instructions operate on O(log N)-bit words, the following strict exponent examples transfer only when each instruction and the complete machine can be simulated with polylogarithmic time and workspace overhead.

Examples inherited from the additional forbidden-region note are:

| Simultaneous caps | Status |
|---|---|
| I <= N^{a+o(1)}, S_work = N^{o(1)}, fixed a < 2 cos(pi/7) | Forbidden |
| I <= N^{1.23+o(1)}, S_work <= N^{0.65+o(1)} | Forbidden, by the published (1.24, 0.666) time-space exclusion with strict slack |
| I <= N^{a+o(1)}, S_work <= N^{b+o(1)}, a+b < (1+sqrt(5))/2 | Forbidden for polynomial resource caps in the compatible model |

These are not unconditional lower bounds on dynamic instruction count when workspace is unrestricted. The nontrivial region comes from simultaneously limiting computation and storage, not from multiplying source-code length by the number of possibilities.

The dynamic instruction count includes all parsing, preprocessing, pointer/address operations, decoding when performed, circuit evaluation, failed work, loop tests, sharing, recomputation and final output in the chosen primitive machine.

## 5. A direct acquisition bound for actual instructions

Suppose a hard family encodes R independent input bits, and some correct deterministic execution must acquire all R. Suppose each primitive instruction can acquire at most b previously unobserved independent input-bit dependencies. Then

    b I >= R, hence I >= ceil(R/b).

The proof counts first acquisitions. Adaptively choosing an address does not reveal an unread input value unless the access itself returns it; an input-dependent precomputed index would have to be charged separately.

The explicit-tournament adversary family supplies such an R. A compact family computing OR of R independent constant-gate bits also does: on the all-zero input, skipping a bit permits a one-bit change that changes the answer. Copies of a bit do not add independent information.

Thus I=o(R) is forbidden for bounded-acquisition bit instructions, and I=o(R/log N) is forbidden when b=O(log N). These are polynomial input-access bounds, not exponential bounds from the number of assignments.

For a fixed straight-line circuit of maximum fan-in d>=2 whose single output depends on R independent input coordinates, at least (R-1)/(d-1) gates are necessary. In the output's ancestor graph, every source and non-output gate needs at least one outgoing edge toward the output, while the g gates have at most dg incoming edges. Thus R+g-1<=dg. This supports a genuine bounded-fan-in operation bound but is only linear, and it does not force an adaptive branching program to build one prescribed circuit.

## 6. The trace does not require fresh information at every instruction

For a deterministic computation, A, x and a step count I determine the first I steps by replay. With standard self-delimiting encodings,

    K(trace up to I) <= B_A + N + O(log(B_A+N+I+2)).

For the complete trace of a halting run, a replay program can stop when A halts, so even the explicit I parameter is unnecessary.

This does not provide fast decompression or a faster solver. It shows why the minimum description length of a trace cannot be identified with its expanded length. An exponentially long trace may have a short description.

A solver need not materialize the trace. One cannot charge storage for I instruction records merely because I instructions were executed. Conversely, actually executing a short loop still pays its repeated dynamic work even though the loop itself is compact.

## 7. The useful connection to circuit lower bounds

Let C_Q(N) be the minimum size of an unrestricted Boolean circuit deciding the encoded problem on every N-bit input, with a convention for malformed inputs. The circuit inputs are the instance-encoding bits, not a candidate assignment to one fixed instance.

For fixed machines with one-dimensional tapes, the standard time-to-circuit simulation gives

    C_Q(N) <= O_A((N+I) log(N+I+2)),

where I is the worst-case number of primitive steps and constants can depend on A. For I>=N this simplifies to O_A(I log(I+2)). The underlying simulation is due to Pippenger and Fischer [1]. Do not apply its tape-model bound directly to arbitrary unit-cost RAM instructions.

A sufficiently large unrestricted lower bound on C_Q(N) would therefore force many executed instructions. Proving a superpolynomial C_Q(N) would be sufficient for a P versus NP separation, but is stronger than necessary and remains open here.

In a simple bounded-fan-in straight-line program listing g gates, identifying opcodes and preceding inputs/gates gives an explicit encoding of size O(g log(N+g+2)). This is an available encoding, not a universal minimum: repetitive circuit families may have shorter generative descriptions.

Counting descriptions proves that most Boolean functions need very large programs or circuits in appropriate length-indexed models. It does not identify SAT or T5 as one of those functions, and it does not override the existence of their fixed looping brute-force programs.

## 8. Exact remaining proof target

The dynamic target is: for every fixed correct uniform solver A and every polynomial cap K N^c, there are arbitrarily large encoded inputs on which its charged instruction execution exceeds that cap.

The decisive missing step is an unavoidable computation bound surviving loops, sharing, indirect addressing, algebra, preprocessing and alternate representations. A lower bound on the length of an explicit trace, one chosen straight-line expansion, or one instruction format alone does not establish it.

Falsifiers/controls for proposed stronger claims:

1. A fixed enumeration loop has constant code and potentially exponential execution count.
2. A table-lookup opcode or unbounded-integer operation can hide work unless its semantics and bit costs are fixed.
3. Pointer-based loops do not repeat an explicit full input address in the stored instruction stream.
4. The deterministic trace is reconstructible from program, input and time, so fresh Shannon information per step is not automatic.

Model gates: DISJ/acquisition sanity is retained as a scoped query argument, not a SAT separation; no nonrelativizing advance is claimed; simultaneous DTISP transfers require the stated model/reduction; repeated complete deterministic configurations cannot occur in a halting self-contained run. No unrestricted circuit lower bound is claimed, so no Natural Proofs or algebrization barrier is asserted to have been overcome.

## 9. Search, validation, and publication scope

Primary literature search queried "Pippenger Fischer Relations Among Complexity Measures 1979 t log t combinational network" and computation-history/Kolmogorov descriptions. The authors' institutional abstract confirms the O(t log t) network simulation. Two PDF mirrors returned a rate limit and a timeout; no full-paper re-read is claimed in this run. The simulation is also the standard theorem already recorded in the project's unified circuit/CM note.

Bounded official-repository searches used the following queries on 2026-11-22:

- site:github.com/anthropics instruction counting formal verification SAT
- site:github.com/openai instruction counting circuit complexity SAT
- site:github.com/xai-org instruction counting verification
- site:github.com/google OR site:github.com/google-deepmind instruction count formal verification SAT

Repository metadata confirmed the actual owners anthropics/formal-math, openai/math, xai-org/grok-build, and google-deepmind/code-verification. Search results in the first two concerned SAT/formalization and were not adopted as new lower-bound theorems. The xAI results concerned software/session accounting and supplied no applicable mathematical bound. A partial read of google-deepmind/code-verification, Computational/docs/READING_THE_THEOREMS.md, blob 8ea014fe60bbb1a5118079255cecc0ee0de095d2, explicitly distinguishes an oracle-query budget from the adversary's internal running time; this is a relevant accounting caution, not a SAT theorem. No kernels or external repository tests were run.

The publication preserves the two previously completed reports and their executed-test records. No new computational experiments are required for the elementary encoding identities here. Repository preflight/compilation was not run because publication uses connected Git data operations without a checkout. Existing-file changes use the recovered full content and a current-head lease. Full published-content readback is the publication check. No agent schedules, identities, owned manuscripts or retired proof trackers are changed.

## References and related notes

1. Nicholas Pippenger and Michael J. Fischer. Relations Among Complexity Measures. JACM 26(2):361-381, 1979. DOI 10.1145/322123.322138. Author institutional record: https://scholarship.claremont.edu/hmc_fac_pub/597/
2. [Additional T5/T_q forbidden regions](Additional_T5_Tq_Forbidden_Regions_2026-11-22.md), including the Williams theorem/table citations, compact-language reduction assumptions, and corrected product-bound scope.
3. [Entropy lower bounds](T5_Tq_Entropy_Lower_Bounds_2026-11-22.md), including the complete executed semantic-check program.
4. [Local FLMV transfer](T_Odd_FLMV_Transfer_2026-11-22.md).
5. [T_q FLMV and CM model and regions](T_q_FLMV_and_CM_Forbidden_Regions_2026-11-22.md).
