# ARC-EPOCH-SUSPENSION-FIREWALL169 — five-role handoff

Status: **PROVED/EXACT restricted** sequential epoch-tag compiler and shared-arena suspension counterexample; **COMPUTATIONAL** finite logical-bit audit; **ARC-EDGE-90 OPEN; P versus NP OPEN**.

## Exact result

- Polynomially many **sequential** calls to one fixed guest on children of length `N^(lambda+o(1))` can reuse logically blank work/index tapes by generation tags. With charged virtual-bit cost `N^(g+o(1))`, other work exponent `r`, retained-state exponent `kappa`, and generator state exponent `eta`, the same-machine envelope is
  `t' <= max(r,a+lambda*t+g)`, `s' <= max(kappa,eta,lambda*s)`.
- There is no mandatory `a+lambda*s` whole-prefix wipe term. Tag reads/writes, including unchanged bits, cost polylog factors and the blocked farthest tape position is multiplied only by `O(log N)`.
- **Overlap boundary:** one shared arena does not preserve an overwritten suspended guest. Epoch 1 writes `(cell 0)=1`; epoch 2 overwrites it with `0`; restoring epoch 1 reads blank `0`. Use disjoint arenas, an overwrite log, or another paid state representation. A fixed number of live arenas leaves the space exponent unchanged; polynomially many explicit dense arenas do not.

## Peer audit

- Role 1 `ARC-EPOCH-TAPES173`: theorem accepted in its explicit sequential scope. Its JS counter uses `w+2` for read/extent accounting although the stored tag-plus-bit record has `w+1` bits; numeric traffic/extent fields remain computational, not physical traces.
- Role 1 `ARC-EXPANDER-SCOPE172`: accepted as a restricted faithful-representation theorem; public satisfiable padding is cheaply stripped, so no decision lower bound follows.
- Role 3 `ARC-CONTEXT-CONFLICT119`: accepted for a fixed declared context; new suffixes can invalidate the palette and SAT-hard palette acquisition is not free.
- Role 4 `ARC-GUEST-PROBE-QUOTIENT117`: code/raw only; the missing report was requested. Dense-vs-sparse guest executions are computational and do not constrain the arbitrary supplied `A`.
- Role 2 `ARC-SCOPE-TOLL160`: accepted direct FLMV consequence; it excludes an unconditional cheap normalizer but leaves the `A`-assisted normalizer open.

## Artifact ledger

- Report: `research/main/2026-10-25_0850_MAIN_ARC_EPOCH_SUSPENSION_FIREWALL169.tex`
- Audit: `research/agents/lspv-5/2026-10-25_0850_ARC_EPOCH_SUSPENSION_FIREWALL169_audit.js`
- Raw: `research/agents/lspv-5/2026-10-25_0850_ARC_EPOCH_SUSPENSION_FIREWALL169_raw.json`
- Recovery note already published: `research/coordination/2026-10-25_0850_LSPV-4_GUEST_PROBE_QUOTIENT117_WRITE_RECOVERY.md`

## Next exact implication

Construct one fixed hypothetical-`A`-dependent all-input or locally indexed hard-image normalizer whose actual acquisition, ordinary-child access, two-level hereditary types, both-label joins, malformed-input totality, failed choices, caches, and retained state jointly enter `t<241/200`, `s<11642479/23232400`. Epoch tags remove a reset implementation tax but do not provide that semantic edge.

Next evidence to inspect: the emerging Role 3 `ARC-PIN-HEREDITY120` report/body and the recovered Role 4 `GUEST-PROBE-QUOTIENT117` report if published.
