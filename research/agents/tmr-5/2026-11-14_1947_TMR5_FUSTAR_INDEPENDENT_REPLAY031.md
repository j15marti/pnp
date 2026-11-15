# TMR-5/031: Independent FUSTAR052 replay, exact completion cost, and deterministic-command qualification

**2026-11-14 19:47 PST (America/Los_Angeles).** TMR-5 PNP Machine Bottleneck Redteam. Claim **FUSTAR053**. Scientific status: **PROVED/RESTRICTED** for the explicitly qualified physical source-bit cache laboratory, with independent native CPython finite evidence **COMPUTATIONAL**. The unrestricted SAT-machine transfer, fusion lower bound, and P versus NP remain **OPEN**.

## 1. Claim and precommitted falsifiers

**Claim audited:** TMR-3/034's authentic one-step FILL_POP changes one cache bit and one message cell in a single fixed-tape multitape transition while making arbitrarily many *logical subscriber views* ready. Thus independent addition of component tariffs is unsound. Independently test the complete restricted dual region, rather than inheriting the peer's Python runner.

Before searching the corpus and primary models, the following falsifiers were fixed:

1. FILL_POP secretly requires an additional cache fill, message-head move, source lookup, or uncharged initial subscriber/message construction.
2. An actual permitted opcode has weighted discharge greater than one for the proposed nonnegative rational weights, or a zero-cost operation changes the vector.
3. An explicit physical execution reaches the terminal goal more cheaply than the purported tariff/necessity bound, especially by reusing cached information and shared subscriber identities.
4. Selecting among the event labels quietly assumes a nondeterministic or externally advised controller, invalidating any claim about one fixed source-only deterministic SAT machine.

All four were tested where applicable. Falsifier 4 is a **real qualification gap** for the original event-menu language: a deterministic controller cannot expose seven unrelated transitions from the same fully specified state unless it includes selector state or explicit control input. A separately qualified **fixed finite command-interpreter** provides the missing selection input, charging each read and leaving this result RESTRICTED, not an unrestricted-machine bridge.

## 2. Primary and original evidence inspected

Controlling current directive: research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md, main blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6. Then the TMR replacement, both proof trackers, authentic main.tex Git blob, AGENTS.md, CODEX.md, pnp-research skill, all five latest handoffs, and issue #3 through TMR-3/034.

**Peer originals:** TMR-3/034 report research/agents/tmr-3/2026-11-14_1928_TMR3_FUSION_TARIFF_FANOUT034.md (blob 2b8a8dd7333d5b3b8cde2bdc1cca9dc792b05593), exact peer source experiments/tmr/tmr3_fusion_tariff052.py (blob b17b071eaa592220d87182942abc238edf42935f), matrix results/raw/tmr/2026-11-14_1928_TMR3_FUSTAR052_MATRIX.json (blob 347e84a001d3977071da8e41c333873a9fa6e298), and raw run results (blob 815742d43934595a86c002b2b84e57a932e5b9a8). Prior semantic shortcut: research/agents/lead/2026-10-07_0855_LEAD-0029_LIPSCHITZ_SQUEEZE_AUDIT.md, especially raw mass, minimum remaining gate cost and prescribed-DAG guard. The /341 legacy checker remains FAIL for full logical authority and /386 remains RESTRICTED. Neither is used here.

**Primary model reference, no SAT theorem imported:** Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, DOI https://doi.org/10.1145/1101821.1101822, Section 2.1 distinguishes machine resource accounting. A standard fixed-tape multitape transition reads one symbol per tape, writes one per tape and independently changes each head in one step. This local machine definition is stipulated explicitly below; FLMV's SAT lower bound is **not** transferred to this cache laboratory.

## 3. Independently specified physical command model

One fixed finite deterministic interpreter has authenticated read-only source symbol $x\in\{0,1\}$ with stationary source head; a separate read-only command stream with alphabet $\{S,P,R,A,F,O,Z\}$ and a command head advancing one cell per charged transition; unary subscriber tape with an append-frontier head; stationary one-cell cache tape $U/0/1$; and message tape with alphabet blank, pending 1, consumed 0 and independently moving head. The command stream is explicit **input**, not advice. This is a different, more fully specified interface than the peer's free event menu, and still is **not** a SAT machine.

Each opcode is one genuine transition when its symbol/head guard is met. $S$ appends one physical subscriber token; $P$ writes one pending message at the message-tape frontier; $R$ moves the message head left; $A$ moves it right across a consumed cell; $F$ caches $x$ if unready; $O$ changes one pending message from 1 to 0 and moves right; $Z$ performs the $F$ and $O$ writes and moves **simultaneously**. Source bit read, command read/advance, cache write, message write and message-head move are part of the same $Z$ transition. There is no authentic zero-cost transition.

The decisive row of the finite transition function is, with subscriber append head at blank, source head on $x$, cache symbol $U$, command symbol $Z$, and message head on 1:

$$
\delta(q;x,Z,\square,U,1)
=(q;x,Z,\square,x,0;\,S,R,S,S,R).
$$

The movement tuple here refers to source, command, subscriber, cache and message heads respectively; source stays, command goes right, subscriber stays, cache stays, message goes right. There is **one** transition, not independent read, cache and message charges. A finite state can reject malformed commands. The Python program interprets this specified event semantics and is **not** a compiled finite-state TM execution or a standalone proof of the full transition table.

The source-access model and command input differ from arbitrary uniform 3-SAT deciders. This is a restricted counterexample to double-counting, not a model-independent SAT lower bound.

## 4. Independently proved exact completion-cost theorem

Let $C_{m,q,x}$ be the reachable state after exactly $m$ SUBSCRIBE operations, $q$ PUSH operations, and $q$ REWIND operations, with the cache initially unready. These are $m+2q$ explicitly paid setup steps; $m,q\ge0$. The message head is at the first pending cell. The abstract vector matches the authentic physical tapes:

$$
\mathbf p(C)=
\bigl(m\,1_{\{\mathrm{cache}=U\}},
1_{\{m>0,\mathrm{cache}=U\}},
\#\{\mathrm{pending\ message\ cells}\}\bigr).
$$

The laboratory terminal goal is: if $m>0$, cache equals authenticated source bit, and all pending messages have been physically erased; with $m=0$, a ready cache is unnecessary. **It is not a SAT/UNSAT terminal predicate.**

**Theorem FUSTAR053 (new relative to TMR-3/034):** In the exact authentic opcode inventory, the minimum number of additional paid transitions from $C_{m,q,x}$ to that laboratory goal is

$$
\boxed{W_{\min}(C_{m,q,x})=\max(q,\,1_{\{m>0\}}).}
$$

**Lower bound.** Exactly $q$ distinct cells initially contain a pending 1. Only $O$ and $Z$ can erase a pending cell, and either erases at most one per step. Thus every successful execution has at least $q$ transitions. If $m>0$, cache $U$ must change to ready, which requires at least one $F$ or $Z$ transition. Hence at least $\max(q,1_{\{m>0\}})$ steps, regardless of scheduling, repeated reads, cache hits, or new subscriber creation.

**Matching upper bound.** For $q>0,m>0$, apply one $Z$ (simultaneous FILL_POP) and then $q-1$ successive $O$ steps; the head advances into the next pending cell each time. For $q>0,m=0$, use $q$ successive $O$ steps. For $q=0,m>0$, one $F$ suffices. For $q=m=0$ the goal is already completed. These legal commands meet the lower bound exactly, proving the theorem.

Consequences: at $q=1$, the exact remaining cost is one **for every $m$**, not $m$ or $m+1$. The subscriber tokens are still physically present; their *logical views* merely share the one cached source bit. No independent subscriber delivery or deletion is asserted.

## 5. Independent tariff cone and counterexample

The real $Z$ row at any $m\ge1,q\ge1$ gives

$$
\Delta_Z=(m,1,1),\quad w(Z)=1.
$$

For $\lambda\ge0$ independent of $m$, the condition $m\lambda_{\rm occ}+\lambda_{\rm key}+\lambda_{\rm msg}\le1$ at all $m$ forces

$$
\boxed{\lambda_{\rm occ}=0,\qquad
\lambda_{\rm key}+\lambda_{\rm msg}\le1.}
$$

Conversely $S,P$ only *increase* the pending vector, $R,A$ leave it unchanged, $F$ lowers the key by at most one, $O$ lowers one pending message, and $Z$ lowers both. Thus, together with coordinate nonnegativity, this region is the **complete restricted nonnegative dual cone**. No LP approximation or finite upper bound on $m$ is required for the symbolic necessity/sufficiency proof.

A specific reachable example has $x=1,m=2,q=1$, a ready-at-frontier subscriber tape with two marked cells, cache $U$, and one pending message 1. Its single legal $Z$ transition changes the vector $(2,1,1)$ to $(0,0,0)$ at cost 1. Weights $(1/2,1/2,0)$ assign discharge $3/2>1$, and $(0,1,1)$ assign discharge 2. Both are **FAIL** and must not be repaired by deleting $Z$. The nonnegative exact certificate $(0,3/5,2/5)$ satisfies every enumerated row and the symbolic all-$m$ inequalities.

**Further blocker:** any size-uniform tariff initially assigning a positive price to *subscriber occurrences* is defeated by this real shared-source step. If the initial state contains no pending messages and one unresolved key, feasible initial potential is at most one, regardless of how many token aliases are already present. With $q$ pending messages, its growth reflects physical queue-erasure work that was also paid to create those messages, not an unproved SAT obstruction. Therefore this laboratory cannot deliver a superpolynomial initial potential for input length $L$ merely by large $m$ or alias mass.

## 6. Native independent replay and exact provenance

This role wrote and **natively executed CPython**, separately from the peer code:

- Source: experiments/tmr/tmr5_fustar_independent053.py. Local Git blob 45b85245360fbe743c7940b0a0a1afb0344f8a0b. Local SHA256 be38de5bd0be1afef72c12a66a765b09ffcb304317cd1023541352f64bd6b8bc.
- Immutable stdout: results/raw/tmr/2026-11-14_1947_TMR5_FUSTAR053_RAW.json. Local Git blob 6c9b2864f929b9d037189e4d1b8b6fa4cdc3b072. SHA256 c1e86663ab32c2dea6aeb537d19c0252293b2ddb5a7d685c1fe9972837c188e7.

**602 assertions, zero failures**; 486 independently enumerated legal paid rows across 126 physically built profiles, $x=0,1$, $m=0,\ldots,8$, $q=0,\ldots,6$; ready-cache/post-POP controls; two bad dual certificates; and positive-occurrence-weight witnesses with denominators through 1009. The exact completion-cost formula was checked on each profile. The full-all-$m$ statement is symbolic mathematics; the finite tests are **COMPUTATIONAL**. Source and raw published Git blobs must match these locally executed hashes before any claim of shared execution identity.

## 7. Ranked integrated dependency map

| Rank / claim | Verdict | Exact reason / next repair |
| --- | --- | --- |
| A. Real simultaneous source fill plus one queued-message pop | **PASS/RESTRICTED** | One fixed finite-alphabet transition exists; explicit command-head scheduling is required to qualify deterministic selection |
| B. Uniform nonnegative dual cone for the source fanout laboratory | **PASS/RESTRICTED** | Exact symbolic cone as above, with independent physical-tape event replay |
| C. Positive uniform price for each unresolved subscriber view | **FAIL** | Any $m$ views disappear after one cached-key fill; $Z$ has $\Delta=(m,1,1)$ at cost 1 |
| D. Independent sum of cache and message charges | **FAIL** | $Z$ jointly discharges both for the price of one operation |
| E. Exact remaining lab work | **PASS/RESTRICTED** | $W_{\min}=\max(q,1_{\{m>0\}})$; actual cheap shared path retained |
| F. Source-only deterministic execution represented by free event menu | **RESTRICTED** | Event choice must be encoded in finite control or charged command input; our command-tape refinement is explicit but changes input signature |
| G. Authentic zero-cost SCC closure for every SAT/proof transition | **OPEN** | Only this model's identity closure is established; unknown transitions are MAY |
| H. Affine/Horn/Krom/separator/fusion quotient invariants on real SAT machine | **OPEN** | Gaussian elimination, definitions, learning, autarkies, DP, caching and reconvergence can discharge multiple candidate components |
| I. Superpolynomial initial fusion-safe potential on explicit family | **OPEN** | No candidate family and all-step tariff/terminal certificate supplied; count-once aliases cannot give it |
| J. Same-system polynomial native derivation or arbitrary correct machine transfer | **OPEN** | The command-driven cache task has no SAT/UNSAT goal or verified reduction; historical /341 FAIL and /386 RESTRICTED |
| K. FLMV/MCSP magnification or sparse-NP bridge | **OPEN/SECONDARY** | Input measure, physical model, promises and circuit thresholds not transferred; no such theorem used here |

**Weakest surviving scientific step:** qualify a *SAT-relevant*, syntax-aware concrete system and exhibit a fusion/affine/separator obstruction that remains invariant under every legal compact shared operation. The present uniform dual certificate prices at most one unresolved cache key plus physical message-erasure work, which is not a candidate superpolynomial lower bound. Then independently test an exact rule-by-component tariff and both-label goal preservation; only afterward attempt a multiscale family and same-system transfer.

**Peer request:** TMR-3 check the charged command-tape refinement and the exact optimal-completion lemma; TMR-4 compile the finite transition table and test zero-cost SCC/LP treatment under real zero-cost alias operations; TMR-2 introduce an affine-canonical-key or separator component and supply the first authentic counterexample/control; TMR-1 decide whether any fixed SAT-related machine or sound source-bound calculus can genuinely implement the required state/goal structure. TMR-5 will independently replay the next such tariff row.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1.txt full, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt full Git blob 930c5eeddafce656717f28055a7a9a755f44737c (1,051,196 chars); canonical main.tex full Git blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 (2,545,859 chars). No tracker or root manuscript claim was promoted. No scheduled task changed. **P versus NP OPEN.**

END_OF_REPORT::TMR5::031::2026-11-14_1947_PST
