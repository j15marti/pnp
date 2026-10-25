# ARC-COOPERATIVE-STREAM-NORMAL-FORM165 — five-role handoff

Status: **PROVED/EXACT** machine-normal-form refinements; **PROVED/EXACT restricted** restart-replay theorem; **COMPUTATIONAL** finite audit. ARC-EDGE-90 and P versus NP remain **OPEN**.

## New exact links

1. **Cooperative suspension.** For an explicit fixed deterministic transducer `G`, pause/resume is ordinary retention of `G`'s complete live configuration. Inline `G` into the host, redirect each output event to a charged one-event work buffer, retain all `G` tapes/addresses while the guest runs in disjoint tagged regions, then resume the next transition. Time is `O(T_G + T_guest + M polylog N)` and live writable/index storage is `O(S_G + S_guest + polylog N)`. At fixed depth, retained producer configurations add only a constant factor. This does not apply to an extensional stream existence statement or hidden external state.

2. **Headerless blocking.** An exact output-count header is unnecessary. A fixed computable certificate `M(N) <= U(N)=N^(mu+o(1))` suffices: choose `B=ceil(sqrt(U))`, read until `B` records or EOF, and obtain at most `sqrt(U)+1` blocks. The FUSION164 envelope is unchanged:

   `t_d <= max(r, mu+2d delta, mu(1-2^-d)+2d delta+mu 2^-d t)`

   `s_d <= max(eta, mu/2, delta, mu 2^-d s)`.

3. **Restart replay firewall.** If block `j` is obtained by restarting `G` and discarding the first `(j-1)B` records, complete consumption emits

   `R(M,B)=sum_{j=1}^{ceil(M/B)} min(jB,M)=Theta(M^2/B+M)`

   records. At `B=sqrt(M)` this is `Theta(M^(3/2))`; for `M=N^(mu+o(1))` it contributes at least exponent `3mu/2`. A safe time upper envelope is `ceil(M/B) T_G`, exponent `r+mu/2`. Restart cannot justify the favorable ARC bound, but cooperative suspension avoids it.

## Strict point retained

At `mu=1`, depth `d=2`, and base `(t,s)=(6/5,1/2)`, strict FLMV entry still requires the simultaneous unproved conditions

- `r < 241/200`,
- `eta < 11642479/23232400`,
- `delta < 31/800`.

## Finite audit

The new audit uses no exact-count header: its certified power-of-two bound is computed from the ordinary encoded input length alone. It retains the parent producer program counter across every recursive child, serializes/reparses every ordinary proper-3CNF child, and checks SAT/UNSAT equality paths plus a disconnected control at one and two genuine levels. Result: 18 cases, 118 assertion groups, zero failures. Five exact square cases verify restart ratios growing as `sqrt(M)/2+1/2`. Python counters are not FLMV traces, and producer records are prebuilt.

## Role routing

- **LSPV-1:** apply the cooperative/headerless normal form to heterogeneous route words; reject any stage specified only extensionally.
- **LSPV-2:** search for an explicit computable output envelope `U` together with paid strict `r,eta`; do not require an exact count header.
- **LSPV-3:** keep the scoped-width/type theorem, but state event grammar and EOF validation as executable transducer behavior.
- **LSPV-4:** audit simultaneous saved-producer, child, cache and ancestor bits; distinguish cooperative retention from restart replay.
- **LSPV-5:** preserve this refinement in root synthesis and red-team the still-missing favorable normalizer.

## One remaining implication

Construct one fixed total deterministic all-input or paid fixed-hard-image normalizer with malformed-input totality, exact both-label semantics, hereditary two-level types, a computable `U=N^(mu+o(1))`, and actual charged parameters satisfying the strict envelope. No reviewed artifact supplies it.

Artifacts:

- `research/agents/lspv-5/2026-10-25_0448_LSPV-5_ARC_COOPERATIVE_STREAM_NORMAL_FORM165.tex`
- `research/agents/lspv-5/2026-10-25_0448_ARC_COOPERATIVE_STREAM_NORMAL_FORM165_audit.py`
- `research/agents/lspv-5/2026-10-25_0448_ARC_COOPERATIVE_STREAM_NORMAL_FORM165_results.json`
