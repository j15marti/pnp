# LSPV-5/429 | Independent syntactic audit of the random-3CNF local-mixed transfer

**2026-11-08 01:05 PST | Route B independent red team | COMPUTATIONAL validation of [P2-L1-498]; no status promotion | P versus NP OPEN**

Exact nodes reviewed: **[P2-L1-498]**, **[P2-B1]**, **[P2-C3]**, **[P2-D1]**, **[P2-B2]**, **[P2-L5-409]**, **[P2-F9]**, peer control **[P2-L3-493]**, and the concurrently published proposed-calculus node **[P2-L3-494]**.

**TRACKERS REVIEWED; NO MATERIAL CHANGE BY LSPV-5/429.** Complete `proof1.txt` was read at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 characters). After a concurrent lease conflict, complete `proof2.txt` was refetched and read at blob `bc6ab7d62dfb2469403b693a616d5906843dbe8f` (358,800 characters), including [P2-L3-494]. LSPV-5/429 edited neither tracker. Historical `R_mix341` grammar/weights, all five role identities, task titles, schedules, enabled states, and the two-Route-A/three-Route-B allocation are unchanged.

## IDEA before search, assumptions, prediction, and falsifiers

Initial hypothesis: a noncircular proof of [P2-B2]/B3 for the same fixed historical calculus would need a rule-specific polynomial simulation from a decision-certificate proof system into `R_mix341`; soundness, completeness, effectiveness, and `SAT in P` alone do not provide it.

Assumptions: the historical system is fixed before inputs; $W_R$ counts distinct paid DAG nodes; a compiler must be uniform and polynomial; no semantic oracle or answer axiom is free.

Prediction: every valid bridge found in current work either supplies such a compiler or remains a conditional simulation hypothesis.

Precise falsifiers stated before search:

1. the historical grammar already contains a polynomial-cost computation-trace/reflection rule;
2. an accepted LSPV-1/3 trace supplies the bridge without assuming short `R_mix341` proofs;
3. Cook--Reckhow implies polynomial bounds for every fixed calculus under `P=NP`;
4. the tracker already records the exact simulation boundary.

Falsifier 4 fired: [P2-L5-409] already gives the identity-system boundary and states that assuming the required simulation is circular. I do not relabel that result. The revised question was therefore whether the newly published restricted transfer [P2-L1-498] actually uses legal syntactic target steps with constant overhead, or merely checks semantic implication.

## SEARCH: exact sources and change-aware repository review

Primary source read: Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, especially the native rules in Section 1, Fact 7.1, and Theorem 7.2(a):

- `Res(PC_r/F_p)` lines are disjunctions of degree-$r$ equations; the syntactic rules are weakening, contraction, false-constant deletion, linear combination, and multiplication, all within degree $r$.
- Fact 7.1 gives an $O(2^t t)$ syntactic derivation of a polynomial clause $C$ semantically implied by CNF premises when the premises and $C$ use at most $t$ variables.
- Theorem 7.2(a) states $\exp(\Omega(N))$ node lower bounds, asymptotically almost surely, for the original with-replacement family $\mathcal F(N,w,\Delta N)$ at fixed $w\ge 3$, $\Delta\ge2^w$, fixed prime $p$, and fixed $r\ge1$.

Actual web queries included `Pang 2610.00837 Res(PC_r/F_p) Definition Fact 7.1 resolution rule` and `arXiv 2610.00837v2 PDF Res polynomial calculus Fact 7.1`. A branded Google UI was not available and was not claimed; the accessible web research service and the arXiv primary text were used.

Project and peer reads:

- full live `proof1.txt` and `proof2.txt`, governing historical handoff at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, current issue #3 through comment `6719551217`, AGENTS/CODEX/research instructions;
- LSPV-1/498 report blob `c99ae09691941c5e2b5a5f2d1dee01da8065dfd8`, code blob `3f9ec32f5f122216ede8e85068bc7b7efb0b6772`, raw blob `e4240db04bd3c3c24d9c0b59e5a7ba66c4e5f0df`;
- LSPV-3/493 report/code/raw blobs `38a0b97484252096f4931770ba61cb9185a0fa04`, `09ca3e0aa1e9f3ba18ed84b5e586df789a6a3cd4`, `5a0d7dd9a9b426c949bb60ef8e82bbb702ed9eee`; both peer programs were executed, producing their reported PASS summaries;
- newest [P2-L3-494] tracker entry and handoff, tracker commit `2ca46e3559481862469265f73419b73f55f33557`: its unit-paid `CAST3` is explicitly a rule in a **proposed distinct calculus**, not historical accepted bytes. The attachment historical checker has no `LOCAL-CONVERT` or `CAST3` dispatch and rejects an unknown `LOCAL3` tag; this neither authenticates nor silently supplies a historical one-premise conversion rule. [P2-D1]/[P2-C3] remain open;
- latest actual Grok file `GROKPROOF/2026-11-08_0320_PROGRESS.md` (blob `72edb3140d8ed798d0905a827f85d3428728e396`) and Claude ledger/report blobs `de75a371ce3143a4495e6892df7fb04794a6b708`, `79e4d4e7e0e3edff3aba8610852c45534bdde128`.

Required repository deltas were checked at pinned heads: `konard/p-vs-np` `ecedd2b...` (`scripts/proof_status.json` blob `93b77e...`); `blkph0x/p-vs-np-proof-research` `7dedc...` (`METHOD_INDEX.md` `18d693...`, independent audit `b30515...`); `meelgroup/frat-xor` `18cd6b...`; `peitl/short-proof` `2c524...`; `tanyongkiam/cake_lpr` `033aad...`; `MassimoLauria/cnfgen` `24e633...` (`randomformulas.py` `b00a885...`); `openai/math` `4eaee8...`; `anthropics/formal-math` `16a5ce...`. None supplies the missing historical all-rule simulation or noncircular B3 bridge. Repository claims were treated as research evidence, not authority.

The attachments supplied in chat were also read. `REPORT(5).md` has SHA-256 `a4fbcf31f0d3a5a79cd7113dca56ece599713ec627d4deb9a8aa8e7f28027766`; `PNP_native_core_audit_2026-11-07.zip` has SHA-256 `30b8412b024e8618187a22eb7e75dcbb4e42b2d1db449340ad34e59befe49c83`. The executable verifier and baseline used below are additionally authenticated individually.

## ITERATE: independent syntactic construction and hostile native control

Published code: `experiments/review/lspv5_429_respc_local3_redteam.py`. Raw result: `results/raw/review/2026-11-08_0152_LSPV5_RESPC_LOCAL3_REDTEAM429.json`.

The Python program is independent of the peer JavaScript generator. It enumerates all $256$ subsets of the eight proper signed clauses on one fixed variable triple and all $14$ nonconstant affine equations on that triple. For every true implication, it constructs and rechecks a complete syntactic `Res(PC_1/F_2)` DAG using only source nodes, native Boolean disjunction axioms, weakening, linear combination, and false-constant deletion.

Results:

- 224 true implications;
- 8,224 checked target nodes; maximum 49 nodes per certificate;
- exact source-cardinality distribution $14,56,84,56,14$ for cardinalities 4 through 8;
- aggregate rule counts: 1,344 sources, 672 Boolean axioms, 2,432 weakenings, 2,208 linear combinations, 1,568 false-constant deletions;
- exact aggregate match to the LSPV-1/498 raw JSON;
- an ordinary Resolution inference compiled to one linear combination plus one false-constant deletion;
- an affine unit XOR inference compiled to one linear combination.

The historical attachment verifier `lspv2_341_independent_verify.js` was then run on its exact `baseline.json` and accepted it. An otherwise identical copy with the first proof rule tag changed from `AND3` to `LOCAL3` was rejected with `unknown rule`. This is an actual native-byte boundary test: it does **not** say Pang's syntactic target rejects LOCAL3; it says the historical 341 verifier does not recognize LOCAL3 as a native rule. Local input SHA-256 values are recorded in the raw output, including verifier `0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae` and baseline `12d723c92c683ec1a59e17d95d0d47156babe7febe27b7432dc01279abcb8d95`.

### Independent challenge

The most plausible falsifier was that ordinary Resolution was translated only semantically. Pang's actual rule list defeats that objection: view the complementary pivot literals as $x=0$ and $x-1=0$; one native linear combination derives a false constant equation, and native deletion yields the resolvent. The finite checker independently executes precisely those two steps. LOCAL3 uses Fact 7.1 at $t=3$, hence constant overhead. Unit affine XOR is one native linear combination. Thus the stated restricted simulation survived this audit.

The historical inclusion objection survives and is decisive for scope: `R_loc3` is a separately defined calculus, and the attached historical checker rejects the added rule tag. Therefore [P2-L1-498] cannot by itself update [P2-B1], [P2-C3], [P2-D1], or [P2-B2].

## Family / theorem / encoding / known-method / remaining-transfer ledger

| Item | Exact record |
|---|---|
| Family | $\mathcal F(n,3,8n)$: $8n$ iid clauses sampled with replacement from $8\binom n3$ proper signed width-3 clauses. |
| Encoding | Each clause is three distinct indexed original variables plus polarity bits; explicit binary length $N=\Theta(n\log n)$. No reduction to 3-CNF is needed. |
| Theorem/source | Pang arXiv:2610.00837v2, Theorem 7.2(a), using Alekhnovich--Razborov PC degree: $\exp(\Omega(n))$ shared-DAG syntactic `Res(PC_1/F_2)` size a.a.s.; preprint scope. |
| Certified property | Distributional a.a.s. UNSAT and proof-size hardness in that specified system. A finite sampled instance is not individually certified hard merely by the theorem; empirical solver difficulty is separate. |
| Restricted tested calculus | `R_loc3`: ordinary shared-DAG RES, same-support proper-3CNF LOCAL3 affine extraction, and unit-affine GF(2) XOR; unit paid inferences, free source leaves. |
| Known legal methods | Arbitrary Resolution sharing/reconvergence, local truth-table-derived affine lemmas, and global affine XOR are included. Cook ER, full extension variables, nonlocal AND3/factors, LOCAL-CONVERT feedback, and explicit branch discharge are controls outside this restricted theorem. |
| Remaining transfer | A polynomial backtranslation for **every** legal historical `R_mix341` rule and scoped branching/shared-DAG construction, with exact historical weights and source authentication; plus a noncircular same-calculus B3 compiler. |

## Work, span, evidence, and resource ledger

Logical validation counted distinct syntactic nodes once. Example DAG SHA-256 values in the raw file authenticate the two parity-orientation constructions. The measured run used 0.357305 seconds wall time, 0.115597 user seconds, 0.020565 system seconds, and 13,176 KiB maximum resident set, including two Node subprocesses for native baseline/hostile checks. Project/literature reads, GitHub publication, caches, and failed `/usr/bin/time` lookup are not folded into that measurement. The initial failed Python attempt exposed and repaired an inverted clause-falsity predicate before the recorded PASS run; it is not hidden as successful work.

Proof-node work, explicit serialized evidence bits, checking time, discovery/search, critical-path span, and realizable retention/recomputation schedules remain different quantities. No machine-time lower bound follows from the proof-size result.

## Status and precise gap

**Advance:** an independent, executable syntactic audit supports [P2-L1-498] and supplies an exact native historical rejection control. **No tracker status/dependency/evidence/gap changed materially**, because [P2-L1-498] already states both facts at the correct scope and [P2-L5-413] already records the historical checker boundary.

**TRACKERS REVIEWED; NO MATERIAL CHANGE BY LSPV-5/429.** [P2-L3-494] was read after the concurrent publication; [P2-B1], [P2-C3], [P2-D1], and [P2-B2] remain OPEN. The missing result is still a source-authenticated polynomial simulation/backtranslation covering every legal historical mixed rule and branching/shared DAG, or a legal counterexample to a precisely stated proposed transfer; separately, B3 still needs a noncircular compiler for this same fixed calculus. P versus NP remains OPEN.
