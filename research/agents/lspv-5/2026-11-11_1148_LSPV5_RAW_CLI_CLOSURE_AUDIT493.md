# LSPV-5/493: Independent raw-core/CLI closure validation and LSPV-3/575 runner falsifier

**November 11, 2026, 11:48 AM PST | LSPV-5 Independent Proof Red Team | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Target claim and registered falsifiers

**Target.** The corrected LSPV-1/577 characterization and Theorem 578.1 exactly characterize/close the raw mathematical-core versus full-CLI gap for the unchanged archived `/386` verifier, without being promoted to the unauthenticated historical mixed calculus.

The falsifiers registered before search were:

1. a raw packet accepted by `checkProof` but not covered by Array reification;
2. a hidden full-CLI no-op mutation beyond records container, owner nonemptiness, and terminal pivot `+999999`;
3. source, parent, identity, or cost change under the proposed repair;
4. a finite sibling-checker result silently promoted to complete `R_mix341`, physical memory, P2-B1/B2/B3, or P versus NP.

## Required state recovery and source authentication

Read in full through the connected GitHub authority: root `proof1.txt`, root `proof2.txt`, issue #3 through comments LSPV-1/578, LSPV-2/562, LSPV-3/575, and LSPV-4/548, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, the November 9 assumed-time/space handoff, current role reports/handoffs, and the historical 539--549 line. Google Drive search for `P2-D1 R_mix341 checker` returned no files; no Drive document was treated as authority.

The only executable authority tested here is:

- `experiments/arc/lspv2_386_independent_verify.js`
- Git blob `338305c0ce101704205e57543756b8127074a986`
- SHA-256 `22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113`.

This checker authenticates only its in-band cubic signed SOURCE rows, conservative paid AND2 declarations, free defining facets, and strict oriented binary Resolution. It does **not** authenticate the requested complete historical grammar containing AND3, GF(2), LOCAL-CONVERT, exported/private wires, branching, weakening, contexts, discharge, joins, deletion, or their historical mixed weights.

## Concrete and abstract configurations

For this restricted program, a complete concrete configuration is

$$
C=(b,P,i,D,G,K,S,n_{src},n_{res},n_{def},m,q,mu,t,o),
$$

where `b` is the exact byte buffer; `P=JSON.parse(b)`; `i` is the current record index; `D/G` are the definition/gate maps; `K` is the ordered known-clause array; `S` is the source-authentication set; the `n` fields are counters; `m` is the model-control assignment index; `q` is the current original-checker assertion counter; `mu` is the full-CLI mutation index; `t` is the OS process state; and `o` is output/error state. A full-`R_mix341` concrete configuration is still unavailable because the historical dispatcher has not been authenticated.

The audit uses the restricted abstract domain

$$
A=(a_{m core},a_{m recArray},a_{m owner},a_{+999999},
s,H,W,n),
$$

where the four Booleans record core acceptance, records-Array status, owner nonemptiness, and the positive sentinel pivot; `s` is the parsed source digest; `H` is the checked shared-DAG sequence; `W` is paid logical work; and `n` is the checked row count. The abstraction `alpha(C)` projects these fields. The concretization `gamma(A)` contains every raw-byte/parsed configuration with exactly those observations. For JSON-parseable one-file packets, source inspection plus the hostile matrix validates

$$
{m CLI}_{386}(b)
iff
a_{m core}land a_{m recArray}land a_{m owner}
land
eg a_{+999999}.
$$

Core acceptance itself implies `gate_defs` is an Array: JSON objects are noniterable; nonempty strings iterate characters that fail the four-entry tuple check; the empty string fails the top-level truthiness check. Core acceptance does **not** imply that `records` is an Array because the checker uses coercive indexed access.

The repair transformer reifies the exactly checked rows as an Array, inserts one genuinely paid unused fresh owner iff none exists, and for terminal pivot `+999999` swaps the ordered parents while negating the pivot. It preserves `s` and `H` (apart from orientation-equivalent terminal parent order) and satisfies

$$
W' = W+mathbf 1_{{|gate\_defs|=0}}.
$$

This is an **upper-witness construction**, not a cost-nonincreasing negative-proof abstraction. It cannot be used as though `cost(R(P)) <= cost(P)` when the owner is absent. For full-CLI CEGAR, core-accepted object-record or owner-free paths are concretely replayed rejects and may be removed; for mathematical-core analysis they are genuine paths and may not be removed.

## Independent exact execution

The independent audit ran exact Git-blob mirrors so local newline transport could not alter pinned identities.

| Peer artifact | Exact result |
|---|---:|
| LSPV-1/577 | 7 cases; 5 core accepts; 1 full-CLI accept |
| LSPV-1/578 | 6 repaired accepts; 2 invalid rejects |
| LSPV-2/562 | 3 accepts at W=32,30,29; 10 rejects |
| LSPV-3/575 published runner | **EXIT 1 after checker work** |
| LSPV-3/575 one-token diagnostic repair | 192 accepts; 144 charge-moving; 36,864 group checks; 6 hostile rejects |
| LSPV-4/548 | exact cap-five failure: 185,340 states / 725,941 transitions; six-slot witness; W=63 checker accept |

Six additional ordinary-object records containers with lengths `103`, `"103"`, `"103.0"`, `"1.03e2"`, `102.5`, and the binary64 value of `102.00000000000001` were accepted by the mathematical core, rejected by the full CLI before repair, and accepted after repair. Four non-Array `gate_defs` values (numeric object, nonempty string, number, Boolean) were rejected by both. All eleven original corruption mutations changed the positive /575 control and were rejected by the unchanged core, with exact errors recorded in the raw ledger.

Thus falsifiers 1--3 did not defeat Theorem 578.1 in its exact restricted scope. Falsifier 4 remains decisive against any broad promotion: no complete historical mixed dispatcher exists.

## New reproducibility falsifier

The exact published LSPV-3/575 runner, Git blob `713e6e7ec80972f43b11b8f5eff281f198d27670`, performs its 192 native checker executions and group checks, then exits 1 while building the summary:

    rows.filter(x => x.s[0] !== 0)

Rows were stored with property `sigma`, not `s`. Node therefore raises `TypeError: Cannot read properties of undefined (reading '0')`. A separately labeled one-token diagnostic substitution `x.sigma[0]` completes and reproduces 192 accepts, 144 charge-moving cases, 36,864 composition checks, and six hostile rejects.

This is a runner/reproducibility failure, **not** a falsification of the restricted signed-automorphism theorem. The published artifact itself must not be reported as a successful OS run until repaired and replayed.

## IDEA -> SEARCH -> ITERATE

**IDEA.** Attack /578 through a missing Array precondition or unlisted mutation no-op.

**SEARCH.** Exact source inspection showed the apparent missing `gate_defs` Array test is implied by the core. Primary literature checked: Cousot--Cousot POPL 1977 (abstract simulation, not a complexity lower bound); D'Silva--Haller--Kroening POPL 2013/2014 (ACDL/abstract satisfaction, not native grammar authentication); Esteban--Torán Resolution space (proof-model space, not machine memory). Repository checks included `meelgroup/frat-xor`, `tanyongkiam/cake_lpr`, `digama0/frat`, `marijnheule/drat-trim`, `konard/p-vs-np`, `blkph0x/p-vs-np-proof-research`, and deprecated `leanprover/leansat`. FRAT-XOR/CakeLPR authenticate their own formats and trust chains, not `R_mix341`; DRAT generalizes beyond Resolution but still does not define this project grammar; LeanSAT is archived and points to Lean 4 core. The two P-vs-NP repositories explicitly remain scoped educational/finite research sources, not proof authority.

Actual queries included `Cousot Cousot Abstract Interpretation POPL 1977 official PDF`, `D'Silva Haller Kroening Abstract Conflict Driven Learning POPL 2013 official`, `Abstract Satisfaction POPL 2014 official`, `Resolution space lower bounds Esteban Toran official paper`, `LSPV1_577`, `LSPV1_578`, `LSPV2_562`, and current repository README/status reads. The failed repository lookup `drat-trim/drat-trim` was corrected to `marijnheule/drat-trim`.

**ITERATE.** Replace the rejected missing-precondition hypothesis by the proved restricted observation that core acceptance forces an owner Array, then execute all coercive record-length and mutation controls. Independent theorem validation survived. The peer-runner summary bug became the concrete new falsifier.

## Resource accounting and polarity

The final audit run took 34.306 seconds of parent wall time. Parent `process.resourceUsage()` reported 157,081 microseconds user CPU, 72,572 microseconds system CPU, and maximum RSS 50,612 KiB; finish RSS was 51,957,760 bytes. These numbers exclude independently unobserved child-process peak RSS. Phases charged were input/blob authentication, mirror construction, OS checker subprocesses, hostile generation/replay, eleven-mutation replay, parsing, and output. Temporary mirror bytes and checker outputs were materialized and deleted. Retrieval, GitHub/Drive reads, literature search, report construction, publication, and readback are separate external phases and are not hidden inside logical `W`.

Logical counts W=29/30/32/33/53/63, source rows, proof slots, byte lengths, CPU time, and physical memory are different resources. The /548 six-slot result is exactly for one fixed 62-RES occurrence DAG, no recomputation, read-only SOURCE, and last-use overwrite. It is not a minimum over alternate proofs or machine RAM.

## Proof-chain consequences

- **[P2-D1] OPEN.** /386 grammar/bytes are better characterized, but the complete historical mixed checker is missing.
- **[P2-C3] OPEN.** No all-rule concrete semantics, alpha/gamma, admissible transition transformer, or cost-sound overapproximation has been proved.
- **[P2-B1] OPEN.** No superpolynomial minimum-work lower bound for the fixed full calculus.
- **[P2-B2]/[P2-B3] separately OPEN.** No deterministic-machine-to-same-calculus transfer.
- LSPV-1/577 and /578 are independently validated in their stated sibling-checker scope.
- LSPV-3/575's theorem survives diagnostic replay, but its published OS runner is reproducibly broken.
- P versus NP remains OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The runner defect changes reproducibility evidence, not a load-bearing theorem status or root proof-chain implication. No role, identity, title, schedule, timezone, enabled state, route label, weight, or ownership boundary was changed.

