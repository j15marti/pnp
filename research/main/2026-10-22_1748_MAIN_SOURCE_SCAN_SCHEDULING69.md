# SOURCE-SCAN-SCHEDULING69

Timestamp: 2026-10-22 17:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

This bounded synthesis asks whether the complete-source requirement from SOURCE-CHANNEL-COMPLETENESS57 necessarily destroys the conditional ARC exponents from SHRUNK-QUERY-ENVELOPE67 and DEPTH-FIRST-VIRTUAL-COMPOSITION68. The answer is schedule-sensitive: a complete source scan is affordable once per parent, but not once per child; retaining every child descriptor is also outside the space target.

## Repairs proposed before source review

1. **Lazy depth-first descriptor generation:** retain one child descriptor and one iterator per ancestor, never a sibling list.
2. **Verify-once transcript:** charge a complete parent scan once and amortize it across the child stream instead of replaying it for every child.
3. **Source-complete recursive descriptor:** expose every source/timer/solver/trace/history influence used by the virtual evaluator and charge the ancestor stack explicitly.

The second mechanism is the substantive test below. It works arithmetically only under a strong streamability premise that remains OPEN.

## Repository sources reviewed after fixing the repairs

1. `research/main/2026-10-22_1648_MAIN_DEPTH_FIRST_VIRTUAL_COMPOSITION68.md`: fixed-depth descriptor stacks and local virtual reads add no hidden polynomial exponent.
2. `research/main/2026-10-22_0548_MAIN_SOURCE_CHANNEL_COMPLETENESS57.md`: source access is a distinct charged channel; digest-only bounds and easy source families cannot be promoted to language lower bounds.
3. `research/agents/rp-derandomization/2026-10-22_0636_RP_COMPONENT_BIAS23_HANDOFF.md`: source-disjoint hitting is restricted, and the actual WRAPPER still lacks a complete original-source dependency certificate.

The independent 17:11 KST review keeps all load-bearing implications OPEN.

## Model

At one node of ordinary encoded length `n`, let a candidate transformer produce

- `Q = n^(alpha+o(1))` children;
- one descriptor of length `D = n^(delta+o(1))` for each child;
- virtual child length `n^(beta+o(1))`;
- a polylogarithmic-time local bit evaluator once the current descriptor is available.

The target values are

`(alpha,beta,delta)=(0.6,0.5,0.5)`.

Three concrete source-complete schedules have different resource ledgers.

## Lemma 69A — exact one-level scheduling ledger

### A. Child-local parent replay

If validating or generating each descriptor independently scans the `n`-bit parent, source work is

`Q*n = n^(alpha+1+o(1))`.

The one-step time map is at least

`c' = max(alpha+1, alpha+beta*c)+o(1)`.

At the target parameters the base exponent is `1.6`, so this schedule cannot reach `1.2`.

### B. Retain every descriptor

If one parent pass constructs all descriptors but they are retained simultaneously, descriptor storage is

`Q*D = n^(alpha+delta+o(1))`.

At the target parameters this is `n^(1.1+o(1))` space, not `n^(0.5+o(1))`.

### C. Shared streamable compiler

Suppose instead that one complete parent scan constructs a child stream in an order permitting each descriptor to be emitted, processed and discarded before the next descriptor, with no retained `Q`-sized state. The exact charged work is

`n + Q*D = n^(max(1,alpha+delta)+o(1))`,

and peak descriptor storage is `D=n^(delta+o(1))`.

The one-step time map becomes

`c' = max(1,alpha+delta,alpha+beta*c)+o(1)`.

For the target parameters this is exactly

`c' = max(1.1,0.6+c/2)+o(1)`,

with non-decider peak space `n^(0.5+o(1))`.

**Status: ESTABLISHED scheduling identities.** They do not prove that schedule C can implement exact SAT semantics on arbitrary inputs.

## Lemma 69B — recursive source scans remain inside the envelope

Let

`lambda=max(1,alpha+delta)`.

Under schedule C, depth-first composition has time map

`f(c)=max(lambda,alpha+beta*c)`.

Its fixed point is

`c_* = max(lambda, alpha/(1-beta))`.

For `(alpha,beta,delta)=(0.6,0.5,0.5)`,

`lambda=1.1` and `c_*=1.2`.

Equivalently, at recursion level `i`, once-per-node source/descriptor work has exponent

`alpha*(1-beta^i)/(1-beta) + lambda*beta^i`,

which is already one of the terms in the composed recurrence. Thus complete linear source acquisition once per active parent is not by itself fatal.

By contrast, schedule A replaces `lambda` by `alpha+1=1.6`, giving fixed point `1.6`.

**Status: ESTABLISHED accounting identity; CONDITIONAL application.**

## Lemma 69C — canonical scheduling trilemma

Within the three explicit schedules above, an ARC implementation must choose among:

1. per-child replay, which violates target time;
2. retaining all descriptors, which violates target space;
3. a shared streamable compiler, which meets the arithmetic target but requires a new semantic construction.

This is not an unrestricted time-space lower bound: a fourth representation or algebraic reuse mechanism is not excluded. It is a mandatory audit for current descriptor proposals.

The streamability premise fails whenever a complete scan leaves `Q` unfinished child states or descriptors in memory, when descriptors must be revisited after later source records arrive, or when exactness requires a separate full parent replay for each child.

## Relation to the two P-vs-NP routes

### ARC/FLMV

The source-channel firewall is refined rather than removed. Source acquisition may be charged without losing the desired recurrence, but only if a single scan yields the exact child stream with one live descriptor and no parent-label call. The missing arrow is now:

> construct an all-input, hereditary, source-complete, streamable compiler producing exact jointly reconstructive children within the target ledger.

**Status: OPEN.** Exact FLMV model transfer also remains OPEN.

### SAT to ordinary MKTP

A streamable compiler plus local virtual evaluator normally supplies a short procedure for target bits. All descriptors, the original source, scan program, access time and output length must enter ordinary KT. Nothing here produces the missing label-sensitive HIGH side or deterministic total both-label generator.

**Status: OPEN.**

## Circuit-SAT and WRAPPER controls

Functional Tseitin traces permit deterministic forward evaluation only when primary-source identities and shared predecessor gates are retained. They do not imply streamability of an exact child family. DIGEST-LUMP19 and CLAUSE-COHERENCE20 still reject hidden state and independently sampled occurrences.

For the existing WRAPPER source, a one-time complete dependency scan is a legitimate polynomial preprocessing step. That can expose an easy direct decider or a non-disjoint coin dependency, but it gives neither a universal RP hitting set nor a language outside P.

COMPONENT-BIAS23 remains **ESTABLISHED restricted** only for certified source-disjoint original-tape factors. Both `P=RP` and `P!=RP` remain **OPEN**.

## Finite audit

The stdlib-only audit checked:

- seven explicit source scales through `N=4096`;
- exact source-read, descriptor-work and peak-storage counts for all three schedules;
- 5,000 random parameter/depth recurrence identities for both the shared-stream and per-child-replay modes;
- 991 starting exponents across 30 depths at the target parameters.

Result: **69,515 checks, zero failures.**

This validates the arithmetic and scheduling implementation only. It does not construct the streamable semantic compiler or prove a class result.

## Five-role ledger

| Role | Status | Single next discriminating test |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | Compute ordinary KT for a schedule-C target, including parent source, descriptor generator, recursive reads and full output. |
| :12 P!=RP | **OPEN** | Run a complete source scan on one generalized WRAPPER and apply the direct-decider plus SAT-NO controls before any interface lower-bound claim. |
| :24 ARC/FLMV | Lemmas 69A-B **ESTABLISHED accounting**; compiler **OPEN** | Implement one exact two-label child stream using one parent scan and at most one live `N^0.5` descriptor; report any unfinished-state memory. |
| :36 P=RP | COMPONENT-BIAS23 **ESTABLISHED restricted** | Use the complete scan to certify source-disjoint original-coin factors or output the first overlap. |
| :48 synthesis | Schedule-C target **CONDITIONAL** | Reject any constructor that rescans per child or retains `Q` child states; seek a genuine source-ordered exact compiler. |

## Conclusion

Complete source access is not automatically incompatible with the ARC endpoint. The distinction is whether the scan is amortized once per parent or replayed once per child. Among the canonical schedules, only a shared streamable compiler meets both target exponents. Building that compiler with exact all-input hereditary semantics is the remaining constructive task.

No root manuscript, automation or role assignment was modified.
