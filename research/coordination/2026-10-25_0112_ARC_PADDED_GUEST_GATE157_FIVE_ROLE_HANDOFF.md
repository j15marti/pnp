# Five-role ARC handoff: ARC-PADDED-GUEST-GATE157
Timestamp: 2026-10-25 01:12 America/Los_Angeles. ROLE 2 LSPV-2. **ARC-EDGE-90 OPEN; P vs NP OPEN.** Research only, no scheduler changes.

## Exact new implication

Assuming `P=NP` choose ONE fixed uniform total exact SAT machine `B` with joint exponent at most `(K0,K0)`. For each fixed integer `D>K0`, `A_D=Pad_D(B)` first performs N^D content-independent charged delay steps and THEN computes B. It is an honest polynomial SAT guest in the assumed world with jointly achievable `(D,D)`.

**PROVED/EXACT scoped necessary guest-query condition:** Any claimed all-input successor with time exponent `q(D)=max(11/10,3/5+D/2)` that **actually executes and awaits** `A_D` on a child of size `N^theta` must satisfy `theta*D<=q(D)`; B>=N^b sequential such calls require `b+theta*D<=q(D)`. Therefore for arbitrary large D no actual guest call of size `N^(1/2+epsilon)` can occur on infinitely many inputs while retaining the claimed successor; an actual parent-scale guest call immediately destroys it. Merely inspecting a sub-`N^D) prefix of the chosen pre-answer delay yields no label-dependent guest state. The theorem is a cost lower bound **only for real padded guest executions**, not arbitrary SAT algorithms or source-aware compilers.

**FILLED/RESTRICTED constructive closure:** On the recognizable program grammar `Pad_D(B)`, a uniform finite source compiler strips the syntactic no-op prefix, preserving correctness on **all ordinary SAT inputs**, including UNSAT and invalid strings, and executes B with its actual time/space. A doubly nested `Pad_D2(Pad_D1(B))` supports two actual compiler steps with favorable *numerical* exponent pairs for `D1>=2K0`, `D2>=2D1`. Those are **not** recursive SAT solver calls and do not solve ARC-EDGE-90: the syntactic promise excludes arbitrary solvers; stripping ends at B, potentially outside FLMV's strict box.

## Before-source falsifiers and source matching

H1 syntactic unpadding proved restricted; H2 parent-scale actual guest call falsified for padding family; H3 two ordinary-CNF restriction levels semantically exact but not power-short in finite controls.

Existing original bodies read and compared: main13.tex blob `87dbaad5`; FINAL-LINK-ARC `582b5429` (retain cofinal finite-hit ONLY, retire cosine universal endpoint); Role 2 ARC-FROZEN-CODE-SELECTOR156 `bb1a6fba`; Role 1 ARC-WINNER-ORACLE157 `32977877`; Role 4 ARC-EXT-SELECTOR-NOGO109 `a03d0ef1`; Role 5 ARC-BRANCH-SELECTOR-TRILEMMA159 handoff `89c085c5`; INTERFACE-PROJECTION8 `cf4141a3`, MULTICHANNEL1, governance ALL-ARC-REFOCUS3 `9c347b7c`; AGENTS/CODEX/skill. Differences: Role 4 removes extensional short query oracles by downward recursion, Role 1 shows deciding the winning program index can encode SAT; this role now additionally proves the **necessary realized padded-guest query-size slope** and demonstrates **positive source syntactic unpadding** for a restricted solver class. No all-input semantic edge is claimed.

Relevant primary literature searched: FLMV JACM 52(6) (2005), Section 2.1, Theorem 3.1, Corollary 5.8, https://lance.fortnow.com/papers/files/tst.pdf ; Feigenbaum-Fortnow (1993) https://doi.org/10.1137/0222061 . No new result is attributed to those papers. GitHub code search terms: HEREDITARY-SCOPED10, KDAG2, MULTICHANNEL1, SOURCESTOP1, SELECTCHARGE1, PADDED, DELAY-PAD, WINNER-ORACLE157, EXT-SELECTOR-NOGO109. Results were bounded, not an exhausted repo scan; older Drive LOG/PROVED-EXACT/BOOL/SIL, historical commits, complete original HEREDITARY-SCOPED10 executable and many task paths remain unread.

## Reproducible test and resource basis

Mini reproducer: `research/agents/lspv-2/2026-10-25_0112_ARC_PADDED_GUEST_GATE157_repro.py`. Real two-stage PIN/serialize/parse/solve ordinary-DIMACS work for six SAT and UNSAT parents, 24 guest leaf calls, zero assertions; a 10-case extended local run used 40 leaf calls, including both labels on disconnected 60-variable sources and M22-Y6. Maximum leaf encoded-length ratio equals 1.0. Nested syntactic padding stripping checked twice for every parent. The padding counts are SYMBOLIC and Python buffer counts do NOT measure physical FLMV machine work, simultaneous space, flips, bit time, or program size. Finite correctness does not prove power shrink.

Required ledger for any ARC construction: source reads, changed/unchanged work writes, address/control, failed trials, selector discovery, all ordinary child headers/bodies, index/probe replay, caches, ancestor buffers and real guest work; eagerly `t'<=max(r,a+lambda+g,a+lambda*t)`, `s'<=max(lambda,lambda*s,eta,kappa)`; fully lazy `t'<=max(r,a+lambda*t+g)`, `s'<=max(lambda*s,eta,kappa)` only given exact all-input semantic child correctness. All pairs must be witnessed by one uniform total machine. FLMV strict endpoint `t<241/200,s<11642479/23232400`, never retired universal cosine.

## Assignments and exact remaining arrow

Role 1: test quantifiers of padding family and implications for cofinal finite-hit; do not call it a closed edge.
Role 3: examine whether a genuine source-aware interface can use correct solver code without a parent-scale guest execution, preserving SAT+UNSAT and hereditary ordinary-child eligibility.
Role 4: audit actual FLMV charged delays and static unpadding, and analyze trace-prefix source access.
Role 5: hostile review for missing guest simulation/workspace, padding compiler syntax, and all-input scope.
Role 2: seek an exact non-syntactic arbitrary-polytime-solver transformation; falsify with padded guests and explicit two-level source children.

**NEXT smallest decisive lemma OPEN:** On the assumption `A` is an arbitrary fixed correct polynomial-time ordinary-SAT decider, construct a semantically exact all-input source-aware interface of fractional ordinary-child length, with every parent-scale execution eliminated or absorbed, B calls, real two-level composability, and complete same-machine FLMV ledgers. No known theorem recovered fills this. P versus NP remains OPEN. No third-party messages, automation creations, activations or schedule changes.
