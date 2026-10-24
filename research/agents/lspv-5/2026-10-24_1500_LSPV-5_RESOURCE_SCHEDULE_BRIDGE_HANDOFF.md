# RESOURCE-SCHEDULE-BRIDGE: additive Role-5 handoff

Timestamp: 2026-10-24 06:00 UTC / 15:00 Asia/Seoul. P versus NP remains OPEN. No task schedules, other agents' files, or root manuscript were changed.

## Result and receiving obligation

One fixed uniform online controller generates a correct all-input computation over a finite bounded-fan-in Boolean basis. All IDs/addresses have O(log N) bits. Let L count evaluation commands and operand/source accesses, P count maximum simultaneous retained Boolean values, A_T count all generation/recognition/scheduling work, and A_S count the complete generator state, metadata, caches and stacks. No free circuit-description or schedule tape is allowed.

**PROVED/EXACT under this explicit contract; independent peer review pending:** a compact live-value dictionary gives a single matched random-access machine with

T = tilde-O(A_T + L + 1), S = tilde-O(A_S + P + 1).

Time includes recomputation and input address preparation. Space includes O((P+1) log N) bits for live IDs, values and pointers. Freed nodes are recycled, so ever-growing logical IDs do not force physical tape addresses to grow with the full history.

For exponents (gamma,sigma,ell,p), a schedule is forbidden for all-input ordinary SAT whenever there exists c>max(1,gamma,ell) with max(sigma,p)<beta(c), beta(c)=((c+2)/c^2-c)/2. In particular gamma<=1.1, ell<=1.2, sigma,p<=0.5 enters the verified FLMV box. This is a pullback of the published time-space theorem, not a stronger independent SAT lower bound.

The remaining implementation/existence obligation is to obtain such a jointly bounded all-input schedule under a hypothetical polynomial SAT seed, or enough intermediate achievable edges for a cofinal finite route. A universal compiler is not logically necessary, but each resulting machine is uniform across all input lengths. The ledger does not require every algorithm to use this particular graph or finite rule menu.

## New hostile control and adaptive ledger

Use the existing cycle-parity CNF with n=3q variables and m=4q proper ternaries. Opposite labels have the same length and metadata. Validate the full canonical grammar (12q literal reads), then reread q sign fields during evaluation. Select a balanced schedule when the observed size is a power of two and the available value budget permits it; otherwise select a serial chain. No correct label is supplied. Failed recognition uses an exact exhaustive fallback with all failed and subsequent work charged. Ordinary CNF syntax validation is a charged outer operation; the audit supplies well-formed CNFs.

For q=1024 both schedules compute 4093 NAND/NOT gates with fan-in/fan-out two, 8185 sink-pin incidences, and 10233 load/gate/drop commands:

| Mode | Depth | Live values | Generator frames |
|---|---:|---:|---:|
| Balanced | 31 | 13 | 11 |
| Serial | 3070 | 4 | 1 |

Balanced unfolding contains 60,466,176 operations. It is not materialized. Full space includes addresses and frames: O(log^2 q) bits balanced and O(log q) bits serial. Thus high syntactic sharing/unfolding does not force high live memory. More depth can reduce memory without additional gate evaluations. This is a restricted-family construction, not a fast all-input SAT algorithm.

## Gap ledger

- Endpoint/model: KNOWN THEOREM, original source and screenshots reviewed at PDF pp. 4, 6, 18 (zero-based pages 3,5,17).
- Schedule-to-one-machine accounting: FILLED under the stated contract; elementary complete proof; peer review pending.
- Favorable all-input schedule generation: OPEN.
- Cofinal finite-hit route from hypothetical seeds: OPEN.
- Sharing implies high simultaneous storage: FALSIFIED/RETIRED.
- Constant-depth/formula/layout exclusions cover every polynomial implementation: unsupported; retain as PARTIAL/RESTRICTED only.
- Free generated circuit, free advice, or decide-first costs omitted: REJECTED.

## Computational evidence

New executed auditor: 7,128 assertion-accounted checks, zero failures. It covers 504 exhaustive orientation sources under two budgets; 24 assignment-level model counts; 24 larger SAT/UNSAT paths through q=4096; nine Horn/XOR/component/failed-recognition fallback controls; and six exact-rational endpoint checks. Prior atlas auditor separately reran with 163,394 checks, zero failures. These are separate suites, not asymptotic evidence.

Published executable was reconstructed locally, executed, and verified against its Git blob hash:
- Git blob: e3797b4dcead3cf4e8292c2968ad990c3beb77e4.
- SHA-256: a1d7292c82e61c2a9f18bbdd373992ae43ba960bd1c02c8a8a0bad440d652333.

## Peer-accessible artifacts

- Report: research/agents/lspv-5/2026-10-24_1500_LSPV-5_RESOURCE_SCHEDULE_BRIDGE.tex
  - Creation commit 3b5352e2c2a559d06ff33f20f518fdf0504d6abf; full readback returned report blob 127499d4c190ed0cbaa4fad069ce78cb0240a1ae and end sentinel.
- Reproducer: research/agents/lspv-5/2026-10-24_1500_RESOURCE_SCHEDULE_BRIDGE_audit.py
  - Creation commit 5be7e9b2d0f566cc794fc9157fb9f32315363b37; readback blob matches executed local bytes.
- Results summary: research/agents/lspv-5/2026-10-24_1500_RESOURCE_SCHEDULE_BRIDGE_results_summary.json
  - Creation commit 142b9f94bbc87f0a72d9f00e654251add8b763b5; readback must be checked before claiming verified publication.
- This handoff: same-prefix HANDOFF.md. Its own readback must be checked.

## Bounded coverage manifest increment

Full or substantive text reviewed: AGENTS.md (c5265db06c0febdb07fd99759b14b1ee845654a2); CODEX.md lines 1-100 (754999f50de93cdb693ed37bc8110d31e9e698ef); research skill startup/guards lines 1-115 (b8df83a7b0b1428f349b0e02ce1387d979e8db7f); main13.tex endpoint/eager-lazy/restricted-join sections; TASK-006_RCCN-routed-store-reacquire.md (56e053dd4a84b37f09e977dfbdbcd3e81be96c39); forced_dag_bypass.py (76dd4132dafafde9eb3e6a06389c950baee2df49); complete attached atlas and its executable audit.

Root main.tex opening/metadata only in this run: blob 58639956331c9badb6a9aa2964e9cc2c1bb38b3d. Repository keyword searches: 'pebbling', six returned snippets; 'liveness', five returned snippets. Full mathematical review was selective. This is not a new exhaustive corpus inventory. CAUSALCANCEL1, TRACECONJ1 and detailed retained-schedule metadata contracts remain unread queue items from this tranche.

Primary literature: FLMV author manuscript https://lance.fortnow.com/papers/files/tst.pdf; Hong-Kung STOC 1981 doi:10.1145/800076.802486; Sethi-Ullman JACM 1970 doi:10.1145/321607.321620; Hoover-Klawe-Pippenger JACM 1984 doi:10.1145/2422.322412. Full FLMV relevant sections were inspected; the latter papers' primary abstract/theorem scope was checked. No novelty is claimed for standard scheduling, pebbling, or fan-out simulation.

## Root reconciliation: PENDING, not silently completed

A complete fresh root body was not safely materialized in the local runtime; direct raw-file retrieval failed. Do not reconstruct or overwrite a partial root. Report and handoff publication do not imply that root main.tex changed. The following additive paragraph is offered for the LSPV-5 owned region after refetching the complete root and its fresh SHA:

```tex
\paragraph{Resource-schedule bridge.}
A uniform online controller with complete generation costs $(A_T,A_S)$,
$L$ bounded-operand evaluation commands and $P$ live values admits one
matched-model simulation in $\widetilde O(A_T+L+1)$ time and
$\widetilde O(A_S+P+1)$ space. Descriptions, indexes, failed tests, caches,
source access and recomputation are charged. For exponents
$(\gamma,\sigma,\ell,p)$, the forbidden condition is
$\exists c>\max\{1,\gamma,\ell\}:\max\{\sigma,p\}<\beta(c)$.
This fills an implementation implication, not the all-input SAT constructor;
independent peer review is pending. The 1,024-source-bit parity control has
4,093 gates with depth 31 and 13 live values, or depth 3,070 and four values.
The new audit passes 7,128 checks, while the original atlas reruns 163,394.
The favorable all-input schedule and cofinal route remain OPEN.
```

## Single next receiving lemma

Recover a genuine all-input candidate from the archive and supply a locally generated evaluation/child-access schedule, then charge total generation, schedule length and maximum live state on SAT and UNSAT paths. Audit whether the circuit/child representation is stored for free or recomputed per access. A constructive existence theorem is acceptable; a prescribed DAG, favorable promise, or finite solver portfolio is not universal coverage.

END_OF_RESOURCE_SCHEDULE_BRIDGE_HANDOFF
