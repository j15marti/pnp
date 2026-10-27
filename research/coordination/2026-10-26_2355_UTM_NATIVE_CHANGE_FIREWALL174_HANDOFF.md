# LSPV-5 additive handoff: UTM-NATIVE-CHANGE-FIREWALL174

Date: 2026-10-26 23:55 America/Los_Angeles. Additive handoff to the five active LSPV tasks only. P versus NP and ARC-EDGE-90 remain OPEN.

## Exact result

UTM-CROSS-WRITE1 is independently upheld in its declared scope: one fixed universal one-tape machine for the common-input portfolio theorem, and one fixed-`k`, fixed-state/alphabet, blank-work, one-sequential-input-head machine for the `D`-sensitive configuration theorem.

The new proved firewall is that actual symbol-change complexity is not simulation-invariant. A native parity machine keeps parity in finite control and has `D=0`. A valid fixed interpreter for that same fixed program materializes the simulated state in a work cell and has `D=#1(x)` while preserving linear time and the output. Therefore a fixed-universal `D_U` lower bound does not lower-bound every native implementation's `D_M`; an explicit metric-preserving simulation theorem is required.

Formal writes and changes also differ: self-writing each step has `W=T,D=0`, while toggling each step has `W=D=T`. Only `D<=W<=kT` is unconditional under the usual transition convention.

With `I0` initially nonblank work cells, the safe configuration count is

`A_I0(S,D) <= 2 q h^k sum_{j<=min(D+I0,kh)} binom(kh,j)(g-1)^j`, `h=2S+3`.

The simplified exponent faces require fixed `q,g,k,I0` and one input head. Explicit outside-model countercontrols use `q_N=2^m`, a packed alphabet `g_N=2^m`, or two independently moving input heads; the last decides separated DISJ with `S=D=0` after positioning the heads.

## Role-addressed consequences

- **LSPV-1:** splice only within one fixed program and complete machine model. Keep every portfolio member globally sound. Separate fixed-universal from native metrics. A full-parent guest validation is not contraction.
- **LSPV-3:** add initial nonblank advice and every input/work head to the streamed configuration. Malformed/time-out coNTIME branches accept. Separate formal writes from actual changes and local UNSAT-component certificates from worst-case all-UNSAT coverage.
- **LSPV-4:** preserve checkpoint-relative residual entropy. A pinned output floor or fixed-`U` change bound does not constrain a cheaper native representation without an explicit transfer theorem.

## Reproducer

`2026-10-26_2355_UTM_NATIVE_CHANGE_FIREWALL174_repro.py` executes 1,388,120 exact assertions with no failures. Canonical raw-payload SHA-256: `70a220fa11c656936467b589e47fc3438be989e36e07787bc6c8d4fe27b72f88`.

## Status

- Fixed-`U` common-input count: **PROVED/EXACT restricted**.
- Fixed-parameter `A(S,D)` count: **PROVED/EXACT restricted**.
- Fixed-`U` `D` lower bound transferring to native `D`: **FALSIFIED/RETIRED**.
- Omitting initial markers or allowing silent state/alphabet/head growth: **FALSIFIED/REPAIRED**.
- Exact22 promise to full ordinary SAT, all-UNSAT affordable coverage, same-machine ARC successor: **OPEN**.

