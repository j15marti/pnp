# LSPV-5/400 — corrected PC+Ext scope blocks an extension-variable transfer

**2026-11-06 19:48 PST, America/Los_Angeles**  
**Role:** Independent red team, Route B primary  
**Status:** KNOWN THEOREM with official author-corrected scope; PROVED/EXACT hypothesis-mismatch lemma; COMPUTATIONAL finite syntax controls; historical `R_mix341`, `[P2-B1]`, `[P2-B2]`, `[P2-D1]`, `[P2-B5]`, `[P2-C3]`, and P versus NP OPEN.

## IDEA → SEARCH → ITERATE

Initial hypothesis: the strongest published extension-variable lower bound might materially narrow the missing transfer from `[P2-F9]` to the full historical mixed calculus, provided it used the same strict 3-CNF source and covered the paid-definition rules in the correct direction.

Falsifiers stated before search:

1. the theorem concerns another source/system and lacks a lower-bound-preserving strict-3-CNF translation;
2. its extensions have locality, disjointness, field, or depth restrictions not guaranteed by historical `R_mix341`;
3. algebraic monomial size is not the fixed historical paid-node work;
4. native GF(2), LOCAL-CONVERT, AND3, branching, sharing, or reconvergence remain outside the simulation.

All four fired. The search also found a post-publication author correction that is material and therefore changed `[P2-B1]` and added `[P2-F10]`.

## Live-chain and peer reconciliation

Both required trackers were read completely before substantive work:

- `proof1.txt` blob `edf29de056457fa806e9d5ebc7548bf6f110505a`;
- starting `proof2.txt` blob `8440d4261a279fe59c96462679ef2d1f746026ae`.

A concurrent LSPV-4/456 update changed `proof2.txt` to blob `76baccfbe2a6308d0031dd4c3f41610b3d7c394c`. The complete replacement was re-merged against that blob, preserving the new `[P2-A4]` evidence. Final tracker blob is `8cb09888b7537d127a371f4c1381211c12dd79bb`; full readback was byte-for-byte equal, contained one `[P2-F10]` node, retained LSPV-4/456, and retained `OVERALL STATUS: OPEN`.

During publication, a peer also updated `proof1.txt` to blob `27e11e225417ec3d0a2adad510ffec35406845c1`, adding the same LSPV-4/456 restricted PATH3 result to `[P1-S3]`. That complete current node was re-read; it does not alter this Route-B result or close `[P1-01]`, `[P1-03]`, or `[P1-04]`. LSPV-5 made no `proof1.txt` write.

Relevant IDs: `[P1-01]`, `[P1-03]`, `[P1-X3]`, `[P2-D1]`, `[P2-D2]`, `[P2-B1]`, `[P2-B2]`, `[P2-B5]`, `[P2-C1]`, `[P2-C3]`, `[P2-F2]`, `[P2-F8]`, `[P2-F9]`, new `[P2-F10]`, and `[P2-L3-463]`.

Peer controls were independently scoped rather than promoted:

- LSPV-1/463 proves `S_RES(F ∧ G)=S_RES(F)` only for ordinary Resolution and a satisfiable disjoint-variable gadget; no all-rule restriction simulation.
- LSPV-3/463 proves a single split can be discharged with linear overhead only in the strict native Resolution fragment; no arbitrary shared/nested mixed-context normalization.
- LSPV-4/456 is a restricted aligned PATH3 Route-A result and does not close the all-input recurrence.

## Primary-source result and correction

Impagliazzo–Mouli–Pitassi, *Lower Bounds for Polynomial Calculus with Extension Variables over Finite Fields*, CCC 2023, DOI 10.4230/LIPIcs.CCC.2023.7:

- Definition 3: PC lines use field-linear combinations and multiplication by a variable; proof size is the total number of monomials in all lines.
- Definition 4: extension axioms are `z_j - Q_j(x_1,...,x_N)`; every `Q_j` depends only on original variables and is a `κ`-junta. Extensions cannot depend on earlier extensions.
- Definitions 6–7: the hard source `F^SEL` is built from a robust `k`-CSP and binary selector/pigeon variables. It has `O(n log n)` Boolean variables, polynomially many constraints, and width `O(log n)`.
- Theorem 1: for `M = n polylog(n)` and `κ = O(log log n)`, the claimed PC+Ext size is `2^{Ω(n/polylog n)}`; Theorem 2 gives a subexponential bound for larger `M,κ`.

The official ECCC entry TR22-038 now contains an author comment accepted 2026-02-25: the result currently works only when extension variables are over disjoint variable sets. The published LIPIcs PDF still states the broader claim, so this report uses the narrower author-corrected scope and records the publication/correction discrepancy explicitly.

Dahiya–Mahajan–Mouli, ECCC TR23-132, claims a stronger number/arity tradeoff for another XORified generalized-PHP source, but its author comment accepted 2026-02-22 likewise says the result currently only works for extensions over disjoint variables.

Primary sources:

- https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2023.7
- https://eccc.weizmann.ac.il/report/2022/038/
- https://eccc.weizmann.ac.il/report/2023/132/

## Exact mismatch lemma

Let the corrected theorem-compatible support family be a collection of sets `S_j` of original variables such that `|S_j|≤κ` and the `S_j` are pairwise disjoint.

For any `M≥2`, define arity-two supports

```
S_i = {x_0, x_i},  1≤i≤M.
```

Every support is a 2-junta, but every pair intersects in `x_0`. Hence the conflict graph is `K_M` and its maximum pairwise-disjoint subfamily has size one. Therefore:

> Bounded local arity alone does not imply that any nontrivial fraction of a legal overlapping definition family lies within the author-corrected PC+Ext theorem.

Dropping the other `M-1` extensions is not a lower-bound-preserving proof transformation: the optimal mixed proof is allowed to use them. Separately, a definition `z_3=Q(z_1,z_2)` is outside Definition 4 even when it has fan-in two, because the paper permits only original-variable dependencies. This is a theorem-hypothesis counterexample, not a claim that these definitions are authenticated historical `R_mix341` rules; `[P2-D1]` remains OPEN.

## Family / theorem / encoding / shortcut ledger

| Family | Exact encoding and size | Published lower bound and model | Known shortcuts / controls | Missing transfer |
| --- | --- | --- | --- | --- |
| `[P2-F8]` density-six random proper 3-CNF | `n` variables; `6n` independently sampled signed proper triples; `Θ(n log n)` encoded bits | with high probability exponential ordinary shared-DAG Resolution size | Cook-style extensions, PC/PCR, GF(2), branching and all native mixed rules remain legal candidates | all-rule `R_mix341` simulation/invariant |
| `[P2-F9]` same source | clause polynomial `∏_{x_i}(1-x_i)∏_{¬x_i}x_i=0` plus Boolean axioms | arbitrary-field PC degree `Ω(n)`; exponential monomial size; bounded-DNF PCR lower bound in its stated characteristic/q regime | extension variables and historical semantic/native rules still outside | polynomial backtranslation of every legal historical DAG |
| `[P2-F10]` selector `F^SEL` | robust `k`-CSP + selector/pigeon variables; `O(n log n)` variables; polynomially many width-`O(log n)` constraints | PC+Ext over `F_p`; nonrecursive original-variable `κ`-juntas; author-corrected to pairwise-disjoint supports | overlapping/nested definitions, Cook ER, native GF(2), branch/reconvergence are outside | not strict 3-CNF; no hardness-preserving width reduction or historical-rule translation |

None of these entries certifies a particular sampled instance as UNSAT and proof-size hard. `[P2-F8]` and `[P2-F9]` are high-probability asymptotic theorems; `[P2-F10]` is an existential family theorem with corrected subsystem scope. The finite checker below proves no UNSAT or proof-size hardness statement.

## Independent finite firewall

Published code: `experiments/review/lspv5_400_ext_support_firewall.py`.

Checks:

- eight pairwise-disjoint arity-two original-variable supports: accepted, maximum disjoint subset 8;
- eight arity-two star supports: all 28 pairs conflict, maximum disjoint subset 1;
- nested definition: rejected by the original-only condition;
- large numerical IDs: accepted;
- repeated input in one definition: normalized as one support variable and recorded;
- six corruptions rejected: duplicate output, nonpositive output, empty support, arity overflow, nonpositive input, negative `κ`.

Run result: 17 assertions, 6 corruptions rejected, 0.00021 seconds, 9,728 KiB measured peak RSS. This was an independent syntactic checker, not execution of an authoritative historical `R_mix341` checker.

## Search and repository audit

Public web search was used; a separate Google-branded engine was unavailable and is not claimed. Queries targeted the exact CCC title, its extension definition, ECCC revisions, and correction language.

Current repository/pinned review:

- governing five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`;
- issue #3 body and targeted comment searches for REFEREE399, LSPV-1/463, and LSPV-3/463;
- actual Grok `GROKPROOF/2026-11-06_2316_PROGRESS.md` blob `a20fb8b...`;
- actual Claude world-ledger assessment blob `79e4d4e...`;
- `konard/p-vs-np` head `ecedd2b45...`, proof-status manifest `93b77ed3...`: no delta since REFEREE399; formalized equivalences and restricted controls, not this transfer;
- `blkph0x/p-vs-np-proof-research` head `7dedc73f...`, method index `18d693ea...`: no delta; bounded-resolution/CDCL and Reed–Muller results remain restricted;
- `meelgroup/frat-xor` head `18cd6bc...`, format blob `986a21aa...`: exact source/XOR IDs and strict `i cx`/`i x` checking, but no historical `R_mix341` equivalence;
- `tanyongkiam/cake_lpr` head `033aad53...`, README `e94f45e...`: declared LPR checker only;
- `peitl/short-proof` head `2c524cfc...`;
- `MassimoLauria/cnfgen` head `24e633bd...`, random sampler blob `b00a885...`;
- `msoos/cryptominisat` head `ed61e217...`;
- `openai/math` head `4eaee875...`, README `cc5b0a03...`: manuscript/formalization scope warning retained.

The requested `konard/p-vs-np` path `research/Idea21.md` was unavailable; the current proof-status manifest was read instead. No unavailable path was treated as reviewed.

## Resource ledger

| Resource | Charged observation |
| --- | --- |
| logical proof nodes | none claimed for historical `R_mix341`; finite checker has 17 assertions |
| explicit evidence | 5,406-byte checker source; 3,449-byte raw JSON before repository framing |
| construction/search | exhaustive maximum disjoint-subset scan on four tiny controls; literature/repository discovery separately charged |
| parsing/source/index reads | complete tracker reads; governance/peer/source fetches; external repository files and commit heads |
| conversions | no CNF width conversion and no proof-system conversion claimed |
| verification/output | independent Python execution plus full GitHub readbacks |
| cache/retrieval/recomputation | connector responses retained during run; checker recomputed once for raw capture |
| failed policies | one stale proof2 outbox superseded after concurrent peer update; one unavailable konard path; no hidden retry counted as proof work |
| simultaneous peak | 9,728 KiB for the checker process; connector/service peak not observable and not converted to a complexity bound |

The repository preflight executable and authoritative historical checker were not run because this environment had connector access but no checked-out `j15marti/pnp` working tree. Root `main.tex` fetched as blob `68188a24badda635a5983fda1c381cdb694fd497` with zero content bytes, so it was not edited. A durable LSPV-5 LaTeX fallback fragment was published instead; no partial large-file overwrite occurred.

## Tracker effect and remaining gap

Material tracker changes:

- `[P2-F10]` added with the corrected theorem scope, exact source/model, finite firewall, and strict-3-CNF/full-mixed gaps.
- `[P2-B1]` narrowed: the strongest located PC+Ext control does not cover overlapping or nested definitions.

Unchanged OPEN obligations: authenticate historical paid-definition grammar and exact weights; prove a source-authenticated lower-bound-preserving translation covering every legal GF(2), LOCAL-CONVERT, AND3, definition, branching, scope, sharing, and reconvergence rule; or find another invariant/family that covers them. The correction supplies no noncircular `[P2-B2]` bridge.

**Actual advance:** a primary-source correction prevents an overbroad extension-variable hardness claim and gives an exact arity-two overlap firewall.  
**Verification:** symbolic conflict-graph proof, independent finite checker, complete conflict-safe tracker readback.  
**Publication status:** report, code, raw result, handoff, tracker outboxes, main.tex fallback, and issue-comment outbox published/read back; root main.tex blocked as above.  
**Precise remaining gap:** no theorem yet lower-bounds the minimum over all legal historical `R_mix341` branching/shared DAGs, and no noncircular same-calculus B3 transfer is known. P versus NP remains OPEN.
