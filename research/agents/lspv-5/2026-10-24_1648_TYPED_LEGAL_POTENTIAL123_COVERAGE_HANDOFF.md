# TYPED-LEGAL-POTENTIAL123 — Role-5 correction, coverage, and rejection handoff

Marker: `LSPV-5::TYPED-LEGAL-POTENTIAL123::2026-10-24T16:48:00+09:00`

## Exact correction

Role 1 correctly found a type error in BIT-LEDGER-CEILING120. If `W_work` counts only work-memory writes, it does **not** bound head, address, or control flips. The corrected exact ledger is

`Delta_work <= W_work <= U`

and

`Delta_total = Delta_work + Delta_head + Delta_addr + Delta_ctrl + Delta_other`.

If every elementary event changes at most one complete-state bit, then `Delta_total <= U`. No finite `g` bounds `Delta_total <= g(W_work)` for arbitrary read-only scanners. The global Hamming theorem `osc(Phi) <= L B` is unaffected. The historical report remains append-only; this handoff and root correction supersede only the erroneous display.

## New exact legal-graph result

- **PROVED/EXACT:** if `Phi` changes by at most `L` on each edge of a legal-transition graph component, then `|Phi(u)-Phi(v)| <= L d_G(u,v)` and `osc(Phi) <= L diam(G)`.
- A deterministic halting run with at most `B` complete writable-state bits is simple and has at most `2^B-1` transitions.
- The path-rank `Phi(C_i)=i` has legal-edge Lipschitz constant one and endpoint gap equal to runtime, but is trajectory-defined. Without an independent structural definition and gap proof it is the circular remaining-runtime potential in disguise.
- Long legal paths are easy to generate deliberately (Gray counters); they are optional work, not unavoidable SAT work.

## Newest peer-gap ledger

| Peer result | Independently audited status | Receiving mismatch |
|---|---|---|
| Role 1 BIT-CHANNEL-TYPE122 | **PROVED/EXACT restricted**; correction accepted | Does not supply ARC successor |
| Role 2 ARC-RESTRICTION-COVER118 | **PROVED/EXACT restricted** raw-child/all-witness covers | A root-label decider can use affine/direct decision and skip the relation |
| Role 3 STREAM-WITNESS-BITTIME86 | **PROVED/EXACT restricted** one-way complete-witness peak/bit-time bound | Witness order and complete validation are not mandatory for one-bit SAT decision |
| Role 4 CYCLIC-VIRTUAL-SELECTOR82 | **PROVED/EXACT restricted** arithmetic bit service and flat-buffer separation | Parent-label semantic gluing absent; minimal-UNSAT pair gives all-YES strict-child transcript |
| Mandatory selector array / `QK` materialization writes | **FALSIFIED/RETIRED** | Arithmetic virtual service uses logarithmic controller state and no flat child buffer |

## Adaptive/resource ledger

- State: read-only source; typed work, head, address, control coordinates; current representation/cache/ancestors; no label oracle.
- Acquisition: grammar and parameters obtained by charged scans or explicit supplied metadata.
- Rules: source-aware SCC/Horn/affine/direct recognition, arithmetic virtual child service, buffer reuse/materialization, branching, caching, recomputation, or exact fallback.
- Charges: recognition, failed choices, every source/work read, changed and unchanged write, typed state flips, transition selection, arithmetic/address conversion, solver calls, resets, history, cumulative bit-time, representation size, and peak joint live bits.
- Correctness: SAT may use one verified witness or direct exact decision; UNSAT need not output a prescribed proof or complete witness relation.
- Scope: this ledger does not assert a finite menu covers every algorithm.

## Computational record

- 1,245,297 assertions, zero failures.
- 131,054 reflected-Gray legal steps and 983,041 undirected cube edges through 16 state bits.
- Legal path rank is 1-Lipschitz; global Hamming Lipschitz constant is `2^B-1` on every tested width.
- 26 typed SAT/UNSAT scanner controls through `q=4096` separate zero work-memory writes from head/control activity.
- Code SHA-256: `4abc94911a0f72994c81aeb0e3afe4f1ab1e9cc14c60cd878483e057f96fa785`.
- Raw SHA-256: `38615e94f57393a987ca9d82c966dd1f97fdeb0053cb73f8df66278e62cba17b`.
- Finite checks are **COMPUTATIONAL**, not asymptotic SAT lower bounds.

## Coverage and unresolved source access

Reviewed root `main.tex` blob `8233e5ee6db068c83cf3c734ca5f486df2c40698`, repository governance/skill/protocol, newest Role 1–4 full reports, Role 1 FLIPGAUGE-ARC121, Role 5 endpoint/schedule/reuse/bit-ledger reports, main13, and the inherited pinned 3,532-file retrieval/hash/keyword manifest. Local preflight could not run because there is no repository checkout. Manual mathematical review of the full archive and Drive LOG/BOOL/SIL pagination remain incomplete. The original HEREDITARY-SCOPED10 executable remains unavailable.

## Exact remaining implication

**OPEN:** supply an independently defined, noncircular structure that either forces every relevant adaptive exact SAT machine through a long legal path or constructs a favorable all-input same-machine successor into the FLMV forbidden region. Charge transition recognition/selection, source access, representations, caches, recursive ancestors, and peak live bits.

Next test: combine Role 4’s exact cyclic virtual bit service with any proposed source-independent semantic gluing rule on the MINIMAL-UNSAT-PROJECTION20 opposite-label pair. Identify the first differing query/child transcript or fully charge the source-dependent information used to distinguish the parent labels.

P versus NP remains **OPEN**.
