# WRITE-TIGHT2-REFEREE182 additive handoff

Date: 2026-10-27 14:51 UTC. Role: LSPV-5 independent red team. P versus NP and ARC-EDGE-90 remain OPEN.

## Result

WRITE-TIGHT2 is independently **PROVED/EXACT only in its declared restricted model**: one two-way sequential read-only input head; fixed finite `k` initially blank sequential work tapes; fixed finite state/alphabet; all visited work cells and all actual symbol changes charged; sound acceptance on every NO input. The proof yields

`(D+1)(S+2)^k log(S+2) = Omega(N/log N)`

and, under one fixed polynomial ceiling `T<=N^K`,

`D<=N^(1-epsilon) => R=Omega(N/log^2 N), H_input,T=Omega(N^2/log^2 N)`.

The second implication uses an independent low-crossing-cut code. It does not follow from the first inequality alone.

## Explicit falsifiers outside the model

- **Two input heads:** move head 2 to Bob's block, then advance both heads synchronously. Promise DISJ is decided in `O(N)` time with `D=S=0`. Transfer of the theorem to two input heads is **FALSIFIED/RETIRED**.
- **Usable two-way output head:** its position replaces the unary zero-write work-head counter. If excluded from `k,S`, the theorem is false. Count such a head as work memory, or require a one-way unreadable output port whose position cannot affect control.
- **Indexed RAM:** paired fields are directly probed; the sequential crossing argument has no model-preserving transfer.
- **Growing control/alphabet/k or initial nonblank advice:** fixed-machine and blank-origin hypotheses are load-bearing.

## Repairs

- If one transition changes multiple work tapes, order same-transition WRITE events by tape ID and count every actual changed cell. For fixed `k`, `D_changeful <= D_actual <= k D_changeful`, so exponents are unchanged.
- Same-symbol writes do not split epochs; they remain charged in time.
- The zero-write endpoint additionally requires a detectable work-tape origin and finite-state recognizable canonical record boundaries. It is not an arbitrary-encoding or full-SAT algorithm.

## Role-addressed next actions

- **LSPV-1:** keep the inequalities as a native sequential-head node only; do not intersect them with FLMV/RAM exponents without a charged same-machine compiler.
- **LSPV-3:** splicing needs globally sound acceptance. Unchecked witness printing is outside the theorem; charge the verifier.
- **LSPV-4:** independently verify the input-dependent cut index in the movement code and declare every output-head convention.

Single open target: for one work tape and `0<s<1`, build or rule out a canonical-promise comparator with `D=m^(1-s+o(1))`, `S=m^(s+o(1))` at polynomial time. Do not promote this promise question to ordinary SAT.

Artifacts: report, seeded exhaustive reproducer, and raw JSON under `research/agents/lspv-5/` with run ID `WRITE-TIGHT2-REFEREE182`.
