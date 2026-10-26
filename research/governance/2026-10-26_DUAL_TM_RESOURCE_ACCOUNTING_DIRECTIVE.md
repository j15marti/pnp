# DUAL-TM RESOURCE ACCOUNTING DIRECTIVE
Date: 2026-10-26
Audience: existing P vs NP LSPV-1 through LSPV-5 agents
Status: Research directive; P versus NP OPEN. Preserve historical evidence, roles, prior task instructions, schedules, and disabled states.

## New user direction
Track all candidate unrestricted SAT solvers and proposed time-space contradictions in TWO DISTINCT ordinary deterministic machine models. Do not silently transfer numerical lower bounds, costs, or space conventions across models.

**Model M1: standard deterministic single-tape TM.** One read/write head and one tape initially holding the N-bit input. Count T1 actual finite-alphabet transitions, P1 total tape footprint including the initial input, H1 head moves, C1 crossings by explicitly identified tape boundaries, I1 distinct input positions inspected, and emitted output length L1. Immediate accounting: N <= P1 <= N+O(T1), H1 <= T1, C1 <= T1. A one-tape crossing-sequence lower bound is NOT automatically a multitape lower bound.

**Model Mk: deterministic fixed-k multitape TM.** Separate read-only input tape and fixed finite k work tapes, one head each, finite tape alphabets. Count Tk transitions, Sk distinct visited work cells (input excluded), Qk physical cell probes, Ck crossing events, Bk actual boundary-crossing bits where meaningful, and output Lk. Immediate accounting: Sk <= k Tk+O(1), Qk,Ck = O(k Tk). Constants may depend on fixed k; k must not grow with N. Work space must be simultaneous, not a sum of historical allocations.

**Same-machine ledger for any adaptive solver A.** Charge all parsing, discovery, failed probes, rule switching, Gaussian elimination, 2-SAT processing, attention implementations, child construction, input access, memory movement, caching, replay, joins, and retained ancestor states. Subcounters like probes and crossing events are already part of time; avoid double-counting. Generated strings use work space unless they are explicitly output-only and not reread. A supposed free primitive belongs to a different strengthened model until compiled with a justified bit-time and memory bound.

## Explicit simulation arrows
For fixed k, a conservative one-tape simulation can encode the k tapes and read-only input on a shared tape and rescan the active representation:
  T1 <= O(Tk (N+Sk+log(Tk+2))), P1 <= O(N+Sk+log(Tk+2)).
Consequently the certified polynomial ceilings transform as t1 <= tk + max(1,sk), p1 <= max(1,sk), with usual fixed constants/polylogs. Also retain the generic O(Tk^2) one-tape bound when Tk >= N and Sk=O(Tk). Distinguish the fast TWO-tape Hennie-Stearns O(Tk log Tk) simulation from the ONE-tape simulation. These are construction upper bounds, not necessary lower bounds.

A one-tape SAT lower bound T1 >= N^(ell-o(1)), if actually established for the same language/encoding, would imply the necessary diagonal inequality tk+max(1,sk)>=ell for the simulated Mk solver. Do not claim ell=3 or any other currently unproved SAT exponent. Conversely FLMV/Williams/Buss-Williams boundaries must be checked in their NATIVE computational model, deterministic versus nondeterministic polarity, read-only input and workspace conventions, and with strict margins. Do NOT transfer an exponent pair by taking the time of one realization and the space of another.

Williams square-root-space simulation for multitape computations is a SPACE-only conclusion: it does not preserve the source time exponent. Any later one-tape two-fifths-power simulation also needs independently checked exact hypotheses, peer-review status, and time cost.

## Specific role assignments, complementary rather than duplicate
- LSPV-1 Formal Proof Lead: maintain two-ledger master theorem graph and identify precise model-native contradiction targets; demand ONE resulting machine satisfying all joint bounds and both SAT/UNSAT cases.
- LSPV-2 Circuit & Reduction Builder: translate source parsing, virtual-child access, ordinary gate simulation, input/head motion, and wire counts into both TM models; attempt an explicit single-tape and fixed-k simulator on identical SAT instances.
- LSPV-3 Adaptive Certificate Theorems: use model-specific counters for certificate guessing versus deterministic acquisition; track crossing sequences, probe volume, reusable memory and source-authenticated child calls without assuming an arbitrary solver emits any restricted proof.
- LSPV-4 Circuit Resource Auditor: independently validate exponent transfers, tape-footprint versus work-space definitions, upper/lower direction of inequalities, and FLMV/native-model applicability. Search for diagonal forbidden regions after REAL simulation overhead.
- LSPV-5 Red Team: falsify model mixing, double-counted communication, one-tape-to-multitape lower-bound jumps, uncharged free primitives, RAM-style random access on TMs, and hidden space under virtual input construction. Provide small hostile controls.

## Research execution
At each existing agent's next permitted run: PROPOSE 2-4 falsifiable candidate constraints first; SEARCH primary literature/project records second; BUILD formal proof/counterexample and reproducible checks third. Add an exact row for source model, target model, direction of implication, T/S/work/probes/crossings/output, parsing and simulation overhead, quantified inputs, and status PROVED/CONDITIONAL/FALSIFIED/OPEN. Share additive handoffs and verified GitHub readback; never overwrite peer research. All previous agents remain disabled unless the user separately requests reactivation. No agent should infer P != NP from any restricted theorem without the unrestricted transfer.
