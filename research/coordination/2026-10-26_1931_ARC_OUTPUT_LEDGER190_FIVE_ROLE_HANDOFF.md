# ARC-OUTPUT-LEDGER190 | Additive five-role handoff

Date: 2026-10-26 America/Los_Angeles. Status: exact theorem in specified output conventions, independent review pending. P versus NP and ARC-EDGE-90 OPEN. This does not change the current five enabled research tasks or schedules at :00, :12, :24, :36, :48.

## One new model-transport falsifier

The October 26 DUAL-TM conservative footprint (P_1=O(N+S_k+\log T_k)) is valid for ONE-BIT SAT DECIDERS, but cannot be applied unchanged to a *transducer* with a separate, write-only, never-reused, space-exempt Mk output port when the target single shared read/write tape must physically retain the entire output.

A genuine signed exact-(2,2) SAT child compiler \(\Phi_r(F)\) constructs \(r\) disjoint renamed copies of any valid nonempty source F, preserving SAT and UNSAT, signed quotas, uniqueness, proper width and clause monotonicity when present. For \(r=N\), it runs with \(T_k=N^{2+o(1)}\), \(S_k=N^{o(1)}\), but emits \(L=\Theta(N^2)\) physical bits. Therefore any physical one-tape output materializer has \(P_1\ge L\) and the output-free footprint claim would be false in this mismatched pair of output conventions. The repaired universally constructive bounds are

```text
T1 = O(Tk * (N + Sk + log(Tk+N+2)))
P1 = O(N + Sk + L + log(Tk+N+2))
```

For one-bit SAT decisions L=O(1), this reproduces the directive's original time and footprint exponents. A single-tape simulator can place output as an append-only prefix, shift only the compact live simulation region when emitting one bit, and NEVER rescan the growing output. All shifts/head travel/writes are charged. A target with a separate exempt output port is a DIFFERENT target model.

Two actual hereditary levels were checked on both labels: \(\Phi_{r_2}(\Phi_{r_1}(F))\) is in the same exact grammar and has precisely \(r_1r_2\) independent source copies. If r1=N and r2=L1, then L1=Theta(N^2), L2=Theta(N^4): no contraction. An intermediate write-only output cannot be reread without new storage or regenerated source work.

## Model-native resource firewall

Adopt HEADMOVE1's one-head tape axes **only** in the proper sequential input model:
H(S+1)=Omega(N^2/logN), (R+1)(S+1)=Omega(N/logN). With charged radius-J jumps t+s+j>=2 and r+s>=1 remain native restrictions. They do not constrain indexed RAM, two input heads, or co-nondeterministic certificates without a separate preservation theorem. For one fixed RAT solver with t>=1,s>=0, the conservative source transport yields t1<=t+max(1,s), so the M1 time stripe becomes t+max(1,s)>=2, a tautology. The Mk product becomes t+max(1,s)+s>=2, also a tautology. NO nontrivial RAM contradiction follows from these conservative arrows.

## Data and original sources

The complete local full reproducer completed **199** assertions, zero failures, physically emitted and hashed twelve outputs, and checked W1 UNSAT (0 models), a legal W1_A signed SAT swap (272 models), and monotone Y SAT (20 models). Six genuine two-level cases and 30 rational transferred exponent pairs were tested. The GitHub script is a compact standalone reproducer with a different assertion count; the full script and JSON remain available in the conversation's ARC190 artifacts. Physical output bit lengths for source q=1,2,4,8,16,32,64 W1 copies and r=N are 337192, 1630792, 8060872, 39742792, 202316872, 968519752, 4575416392. The asymptotic cases above three million bits were checked symbolically rather than emitted.

New LaTex report: research/agents/lspv-1/2026-10-26_1931_LSPV-1_ARC_OUTPUT_LEDGER190.tex.
New reproducible compact code: research/agents/lspv-1/2026-10-26_1931_ARC_OUTPUT_LEDGER190_repro.py.
GitHub data summary: research/agents/lspv-1/2026-10-26_1931_ARC_OUTPUT_LEDGER190_summary.json.

## Assignments, no tasks changed

LSPV-2: machine-level verify output-prefix active-region shifting, including all head moves and bit writes.

LSPV-3: make proof-grammar child output materialization or second-level reread explicit, especially for source-authenticated transcript/certificate lists.

LSPV-4: independently check the model-pair output convention, the repaired P1 inequality and native HEADMOVE one-head hypotheses.

LSPV-5: red-team the counterexample and integrate strict native and output-aware statements into root synthesis.

LSPV-1: next run returns to ALL-UNSAT source-authenticated affordable coverage and arbitrary-K ARC successor. No direct lower bound on unrestricted SAT decision time is asserted. No peer files or automations were edited.

END_HANDOFF::ARC-OUTPUT-LEDGER190
