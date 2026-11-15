# TMR-3/034: Count-once fusion tariff and a genuine multitape one-step counterexample

**2026-11-14 19:28 PST (America/Los_Angeles).** Claim **FUSTAR052**. Role: TMR-3 PNP Time-Space Tradeoffs. Status: **PROVED/RESTRICTED** for the explicitly specified source-bit fanout transition system, independent TMR-4/TMR-5 machine-level review **OPEN**. Finite evidence **COMPUTATIONAL**. **P versus NP OPEN.**

## Governing assignment and exact new contribution

The newer user-approved handoff research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md, verified on main and announced in issue #3 comment 6888581733, supersedes MCSP-first scientific routing while retaining all five existing TMR identities and schedules. MCSP, MKTP and FLMV remain supporting branches. This run supplies the TMR-3 first target: a machine-readable rule tariff slice, exact paid costs, sharing-safe component restrictions, one genuine paid simultaneous-step counterexample, and a closed-form rational dual cone.

Prior LEAD-0029 already showed that raw semantic mass fails under cheap compact operations. TMR-5/030 already charged source queries once across processors, and TMR-3/033 already proved a restricted physical MCSP input-ingress bound. **New here:** a completely explicit local finite-alphabet multi-work-tape trace in which ONE honest TM transition reduces an arbitrary number of unresolved *views*, one distinct cached key, and one real queued message simultaneously. This falsifies independent tariff summation without claiming that any SAT algorithm performs that trace.

## Qualified concrete laboratory

Fix an authenticated one-bit read-only input x in {0,1} with source head parked at cell zero. A finite deterministic controller has three writable tapes:
1. Unary subscriber tape A, with m marked token cells and its head at the append frontier.
2. One-cell cache tape B with alphabet {unready, ready0, ready1}, its head parked at that cell.
3. Message tape C, each occupied cell marked 1 (pending) or 0 (consumed), with its own two-way head h.

The program has finitely many states implementing the following exact transition types; operations requiring their guard can be selected by finite control and each counts **one complete TM transition**. A single multitape step can read the parked source bit, write cache B, erase the current message symbol on C, and advance C's head. This is one transition, NOT three independent charged operations. The abstract runner stores tape A as its unary length m and stores C explicitly as a tuple; these are exact sufficient encodings for this restricted laboratory, not a universal SAT-machine abstraction. Source bit x is immutable and the cache value is set to exactly x.

Physical transition classes: SUBSCRIBE writes a new unary token and advances A; PUSH writes a pending symbol at the unused C frontier and advances C; REWIND moves the C head left; ADVANCE moves C right over an already consumed cell; FILL changes cache B from unready to ready-x while reading x; POP erases the currently marked message cell and advances C; FILL_POP performs FILL and POP in **the same physical multitape transition**. All physical transitions have exact cost 1. There are no real zero-cost edges; identity/stuttering is a mathematical equivalence, not an elapsed transition. Therefore authentic zero-cost SCC closure is trivial on this concrete model. A gratuitous zero-price alias rewrite must not be inserted as a concrete machine operation.

For any m>=1 and q>=1 the state with m tokens, q queued messages, unready B and C positioned at the first message is **reachable** by m SUBSCRIBE steps, q PUSH steps, and q REWIND steps. In particular an arbitrarily large m does not require nonuniform advice, a free giant initial tape, or an uncharged queue. All its setup work is charged. The counterexample concerns the *last edge*, where a previously constructed many-view obligation is resolved via one shared source cache.

## Exact reduced-product obstruction components

Define for a complete state C:

p_occ(C) = m if B is unready, otherwise 0. This counts unresolved subscriber *views*, not compulsory independent computation.

p_key(C) = 1 if B is unready and m>0, otherwise 0. This counts the distinct unresolved canonical source-cache key after sharing.

p_msg(C) = the number of pending 1 cells on physical message tape C. This counts actual unconsumed message tokens, NOT just an equivalence class of copied values.

Set p(C)=(p_occ,p_key,p_msg). Every completed laboratory goal has B ready (if a subscription was requested) and zero pending message cells; all such goals have p=0. When m=0 and no message exists, the empty request is already completed without reading x. A SAT decision goal is **not** modeled here.

For each physical edge r:C->C', w(r)=1 and Delta_r=p(C)-p(C'). The full symbolic matrix, including m=0 and post-cache-ready cases, is at results/raw/tmr/2026-11-14_1928_TMR3_FUSTAR052_MATRIX.json.

| Legal operation and guard | Delta_occ | Delta_key | Delta_msg | Exact w |
| --- | ---: | ---: | ---: | ---: |
| SUBSCRIBE, first unready key | -1 | -1 | 0 | 1 |
| SUBSCRIBE, further unready view | -1 | 0 | 0 | 1 |
| SUBSCRIBE after cache ready | 0 | 0 | 0 | 1 |
| PUSH pending message | 0 | 0 | -1 | 1 |
| REWIND / ADVANCE head | 0 | 0 | 0 | 1 |
| FILL with m>=1 | m | 1 | 0 | 1 |
| FILL with m=0 | 0 | 0 | 0 | 1 |
| POP pending message | 0 | 0 | 1 | 1 |
| FILL_POP with m>=1 | m | 1 | 1 | 1 |
| FILL_POP with m=0 | 0 | 0 | 1 | 1 |

These are simultaneous Delta values. Counting a bit as a cache acquisition, a logical subscriber discharge, and a physical message removal does not license charging three steps.

## Theorem FUSTAR052 (exact restricted dual feasible cone)

**Statement.** For the above fixed finite-alphabet source-fanout machine family, a length-independent vector lambda=(lambda_occ,lambda_key,lambda_msg) with nonnegative rational or real coordinates satisfies

lambda dot Delta_r(C) <= w(r)

for **every** legal physical transition and every reachable subscriber count m>=0 **if and only if**

lambda_occ=0, lambda_key>=0, lambda_msg>=0,
lambda_key+lambda_msg<=1.

**Proof, necessity.** For every integer m>=1, create m subscribers, one pending message, leave B unready, and rewind C to that message. The fully legal FILL_POP step costs exactly one transition and has Delta=(m,1,1). Thus for all m,

m lambda_occ+lambda_key+lambda_msg<=1.

Any fixed positive lambda_occ fails by taking m arbitrarily large. With lambda_occ=0, m=1 gives lambda_key+lambda_msg<=1. Nonnegativity is a hypothesis.

**Proof, sufficiency.** SUBSCRIBE and PUSH only increase components, so have nonpositive weighted discharge. REWIND and ADVANCE leave all components unchanged. A FILL edge discharges at most lambda_key; POP discharges at most lambda_msg; their combined FILL_POP edge discharges at most lambda_key+lambda_msg<=1. The m=0 and ready-cache variants discharge no more. These exhaust the concrete transition inventory above. Every edge has w=1. Therefore the stated cone is sufficient. QED, **restricted to this exact laboratory**.

The choice lambda=(0,3/5,2/5) is an exact feasible certificate. With a finite externally enforced subscriber cap M, the FILL_POP row instead permits M*lambda_occ+lambda_key+lambda_msg<=1. The M-dependent positive view coefficient tends to zero as M grows. It cannot be treated as a fixed uniform all-length lower-bound weight.

**Smallest displayed counterexample:** x=1, m=2 subscriber tokens, one pending message, cache unready, C at that pending cell. FILL_POP costs 1 and has Delta=(2,1,1). Candidate lambda=(1/2,1/2,0) charges 3/2>1; independent component weights (0,1,1) charge 2>1. The final state is real and can also be obtained by two separate transitions FILL then POP, but the cheaper single-step route is legal and cannot be erased or priced as two. It is a genuine shared-operation falsifier, not a spurious abstraction trace.

## Replay and hostile controls

Exact native CPython executed experiments/tmr/tmr3_fusion_tariff052.py and emitted immutable stdout results/raw/tmr/2026-11-14_1928_TMR3_FUSTAR052_RAW.json. It completed **133,770 assertion checks, zero failures**, covering 612 reachable seed/random-walk states, 44,336 enumerated legal event edges, both source bits, subscriber counts 0..17 and messages 0..11, plus 180 deterministic random traces of 90 steps each. All checks use fractions.Fraction for dual weights. The explicitly illegal additive weights failed as expected and the legal weights passed. Dynamic controls included post-POP states, READY cache states, consumed-message head ADVANCE, empty requests, arbitrary repeated subscribers to the same key, a prior message backlog, and distinct orderings of FILL and POP. Eight increasing subscriber witnesses certify finite violations of positive view weights; the universal all-m statement is proved symbolically, not inferred from tests.

The runner is an exact *event-semantics* interpreter for this chosen model. It is **not** native finite-state multitape code or a full SAT decision machine. Constructibility of the one-step FILL_POP is justified by the conventional simultaneous multihead/multitape transition definition; a concrete compiler and independent tape-level replay remain a peer-review obligation. This model grants no circuit-minimization oracle, source-dependent advice, or uncharged subscription creation.

Hostile interpretation controls: (i) subscriber occurrences are not independent delivered messages; (ii) actual message cells remain separately charged; (iii) no raw number of views yields a superpolynomial lower bound; (iv) the cached input key has just two possible source values and is deliberately cheap; (v) Horn, 2-SAT, XOR/Gaussian elimination and bounded-treewidth families can introduce still more fusion mechanisms, so lambda_key=1 here cannot be imported as a universal SAT obstruction; (vi) a true physical zero-work shortcut cannot be relabeled as a paid proof-calculus rule.

## Primary-source theorem and model matrix (background, NOT imported as a SAT bound)

| Original theorem and location | Exact model/input/resource claim | Scope in this run |
| --- | --- | --- |
| Fortnow, Lipton, van Melkebeek, Viglas (JACM 2005), Section 2.1, printed p.4 | Uniform random-access multitape TMs with simultaneous indexed input/work operations; writable work/index tapes count as space, read-only input and one-directional output excluded. | Confirms physical simultaneous multitape events cannot be double-charged as separately timed reads/writes. Does not say our source-fanout task is SAT. |
| Same, Theorem 3.1 and Corollary 3.2, printed pp.6-7 | SAT to nondeterministic-linear-time model transfer using locally computable quasi-linear reductions, polylog overhead; one deterministic machine and simultaneous time/space. | Requires genuine SAT algorithm with same-resource pair. Not supplied by this laboratory. |
| Same, Corollary 5.8, printed p.18 | NTIME[n] not contained in DTISP[n^c,o(n^d)] for d=((c+2)/c^2-c)/2; for c=241/200, d=11642479/23232400>1/2. Deterministic indexed random-access and uniform. | Numeric reference only; no reduction of our goal to SAT or contradiction. |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida (STACS 2021), Theorems 1-2, printed p.23:3 | Ordinary explicit MCSP[s] on N=2^n truth tables. Small existential mu_1 and one-way-input/one-work-tape N^1.01 **conditional P!=NP** premise differ from larger mu_2 randomized N^1.99 **proved** lower bound. | Neither theorem is a tariff lower bound for source subscriptions. Threshold, model and input-length transfer remain OPEN. |

Primary originals: https://lance.fortnow.com/papers/files/tst.pdf (sections 2.1, 3.1, 5.4); https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23 (STACS 2021). Source PDFs reviewed with page screenshots. No unverified MCSP/MKTP reduction or ETH/cryptographic assumption imported.

## Prior-work ledger and exact unrestricted gap

- research/agents/lead/2026-10-07_0855_LEAD-0029_LIPSCHITZ_SQUEEZE_AUDIT.md: source of the earlier semantic-mass and one-step Lipschitz guard. **ESTABLISHED negative-control history**, not repeated as a new lower bound.
- research/agents/tmr-3/2026-11-14_1820_TMR3_MULTIHEAD_SUFFIX_FRONTIER033.md and original experiments/tmr/tmr3_multihead_suffix_audit047.py with raw results: **PROVED/RESTRICTED** physical-input ingress, review OPEN; only linear in MCSP truth-table N.
- research/agents/tmr-5/2026-11-14_1850_TMR5_NETWORK_WORK_DEPTH_ORACLE_AUDIT030.md with original experiments/tmr/tmr5_network_workdepth051.py: **PROVED/RESTRICTED** evaluation-only oracle work-depth; no syntax-aware SAT bridge.
- research/agents/tmr-2/2026-11-14_1920_TMR2_MCSP_EDGE_QUANTILE_COUNTERCONTROL034.md: **PROVED/RESTRICTED** typical-YES input-probe quantile; one input-read exponent, not MCSP small-mu N^1.01 decision cost.
- research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex and .../2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex: historical restricted crossing/portfolio findings; no arbitrary-machine lower-bound transfer.
- research/agents/lspv-3/2026-11-13_0727_LSPV3_615_HASH_BINDING_SOUNDNESS_COUNTEREXAMPLE.md: original logical authority failure remains retained. No checker soundness is inferred.

**OPEN load-bearing arrows:** (1) lift this local vector to a complete SAT machine configuration space with every transition, including affine/circuit shortcuts and arbitrary workspace; (2) demonstrate a noncircular, fusion-safe superpolynomial initial Phi on explicit growing valid SAT inputs; (3) prove every completed SAT/UNSAT goal has nonpositive Phi; (4) bind the same machine and resource accounting; (5) for any qualified proof-calculus route, separately prove SAT-in-P implies a polynomial native derivation on the same family. Neither the optimal restricted cone nor finite tests discharge any of these.

## Peer request and one next target

TMR-4: independently compile the three-tape FILL_POP step in an actual finite-alphabet TM and feed the exact matrix to an exact-rational LP with zero-cost identity closure. TMR-5: replay m=2,q=1 and check that no unpaid pointer, head motion, read or queue creation is hidden. TMR-2: test whether distinct affine and separator obstruction keys admit an analogous one-step shared discharge even after canonicalization. TMR-1: retain correct fixed-machine/all-polynomial separation quantifiers and both-label terminal guard.

Next TMR-3 target: expand the complete tariff matrix by one *actual* affine/XOR cache update, look for a single paid transition that discharges two distinct canonical keys, and either refine the reduced-product components or publish the legal violation. This would test whether p_key survives beyond source-copy fusion.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both root proof trackers recovered (proof2 original Git blob 930c5eeddafce656717f28055a7a9a755f44737c) and canonical main.tex recovered (original Git blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34). No root document promotion or task change. **P versus NP remains OPEN.**

END_OF_REPORT::TMR3::034::2026-11-14_1928_PST
