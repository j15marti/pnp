# LSPV-2/565: Source-bound per-transition value-novelty abstraction with native reification

**November 11, 2026 14:12 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate and falsifiers

**Candidate ALPHA565.** For the exact archived /386 SOURCE/paid conservative AND2 owner/free DEF facet/strict oriented Resolution checker, define an online abstract ledger retaining an independently authenticated signed-source SHA-256, a chronological set of available canonical signed-clause values, globally distinct paid owner IDs/wire dependencies, and each exact ordered signed RES port pair. Charge every new paid owner once; charge a RES transition 1 if its signed clause conclusion is a new value and 0 if an identical signed clause is already available. This is a sound **lower-cost** abstraction of every *legal concrete transition* in the /386 sibling, not an all-rule R_mix341 abstraction.

Four falsifiers: F1 paired parent/pivot transport changes legality or cost; F2 pivot-only or parent-swap-only mutation is incorrectly accepted; F3 an exact repeated, terminal-live RES value cannot be collapsed to a real original-checker-accepted proof; F4 binding the packet's internal signed source to a different independently supplied external DIMACS source is mistaken for a proof of that input. F1 through F4 passed the OS-run controls.

## Exact checked model, scope, and theorem

The original 6,345-byte archived checker is `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`. Pinned baseline is `results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json`, blob `318c52d99977ea4e91bc8554051138a700c1dc94`. Independently supplied source is `results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf`, blob `e8bc4300f1f4518cb447edaf3f699bcee4839803`, SHA-256 `3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c`. The 17 source occurrences include 16 guarded, signed cubic-Tseitin clauses and the mandatory positive guard unit. The source binder compares complete signed occurrence multisets, not just satisfiability class or variable support.

Let a legal prefix configuration `C` contain immutable external source bytes/hash, the complete original concrete chronological record list, source-occurrence provenance, already declared paid gate owners and fresh wires, legal signed parent ports, and cumulative concrete cost `W(C)`. Define `alpha(C)` as the same source hash, owner identity/definition ledger, known distinct clean clause values `V(C)`, source occurrence ledger, validity predicates for the original full CLI, and signed parent port predicates. Its abstract cumulative charge is

$$
\widehat W(C)=|G|+\#\{\text{RES transitions in the prefix whose signed result was not previously in }V\},
$$

where `G` is the **set of globally distinct paid gate owners** declared by the packet, charged exactly once. Free facets and SOURCE transitions cost zero. Unknown historical operations are not assigned fabricated native syntax or excluded: any future mixed-rule extension must provide separate MAY transitions and a separate coverage proof.

**Theorem 565.1, PROVED/RESTRICTED.** For each legal concrete SOURCE, DEF or RES step of the exact /386 checker on an independently bound source, the corresponding `alpha` step exists and has charge no larger than the concrete step; for RES it costs 0 or 1 versus exactly 1, and for SOURCE/DEF and paid owner declarations the respective charges are equal. A completed concrete empty-clause refutation remains represented by a completed abstract empty-clause state. Summation yields `W_hat(C) <= W(C)` on every accepted prefix/goal. This does not assert that arbitrary abstract traces are native-realizable.

**Proof.** SOURCE/DEF introduce their checked canonical signed clause into the value set at zero inference charge, retaining immutable source occurrence and paid owner identities. A legal RES consumes two already known signed clauses via an authenticated earlier ordered parent pair `(i,j)` and signed pivot `p`, verifying `p in K_i`, `-p in K_j`, and exact canonical clean resolvent. The abstract transition inserts that same verified signed result, charging either 1 if absent or 0 if already present. Therefore its charge never exceeds the native RES unit charge. It retains the same source, fresh wires, signed ports, and owner ledger. Induction on chronological prefixes proves inclusion and the terminal property. The proof applies to this code's checked semantics; the byte parser's noncanonical UTF-8/duplicate-key equivalence class remains the existing separate /557-/558 obligation and is not normalized away by this canonical-packet transformer. QED.

**Corollary 565.2, one genuine concretization.** Starting with the pinned original W29 signed K4 packet (17 SOURCE, 28 RES, one paid owner, 45 records), duplicate its next-to-terminal RES parent immediately before the terminal record and redirect that parent port to the duplicate. The original /386 checker accepts at W30, 46 records; the duplicate creates no new signed value, so `W_hat=29`. The reference coalescer maps the duplicate's dependent port to the earlier identical signed value, drops the nonterminal duplicate, and reproduces the **original W29 certificate byte for byte**. The complete original CLI accepts both certificates. This is a restricted reification of one abstract zero-charge reuse, NOT a theorem of arbitrary historical branch-context quotienting.

**CEGAR falsifier.** If an abstraction retains only the unordered pair of parent clause values and independently forgets pivot sign, it admits a pivot-only and a swap-only mutation that the original checker rejects. Refining the abstract state to carry paired oriented signed ports `[(parent_i,+p),(parent_j,-p)]` excludes those spurious transitions. A paired simultaneous swap and pivot negation is authentic and remains accepted. This inherits the orientation invariance of LSPV-2/564; the new contribution is an executable chronological step-cost ledger with a concrete coalesced witness and an independently SHA-bound external source.

## Original executable outcomes and distinct resources

The exact Git-blob-recreated original checker ran as a separate native Node.js v22.16.0 OS subprocess for each packet. Ten cases passed expected classifications: five original-checker ACCEPT and five REJECT, including one **native ACCEPT/reference external-source REJECT** (missing external clause) and one unknown-AND3-in-/386 negative. Accepted cases accumulated **17,878 original assertion groups**, including the original built-in corruption suite. No original mathematical code was modified. The independently developed reference replayer also checked the signed ports, source multiset, source SHA, gate owner freshness and exact native summary charges.

| Packet | Concrete paid W | Abstract W-hat | Native records | Native result |
|---|---:|---:|---:|---|
| Pinned baseline | 29 | 29 | 45 | ACCEPT |
| One extra terminal-live RES alias | 30 | 29 | 46 | ACCEPT |
| Exact coalesced reconstruction | 29 | 29 | 45 | ACCEPT |
| Paired parent and pivot orientation flip | 30 | 29 | 46 | ACCEPT |
| Pivot-only / swap-only / undercharge / forged SOURCE / added AND3 opcode | not valid | not valid | varies | REJECT |

The original native checker also accepts the unchanged duplicated packet when checked against the **different** 16-clause external file because it has no external source input; the independent binder rejects that attempted transfer. This is consistent with the earlier LSPV-2/559 counterexample, not a second checker soundness defect.

This witness measures: distinct paid logical owner and RES work; certificate UTF-8 bytes (2,867 baseline and 2,919 duplicate); actual Node subprocess assertions (not CPU time); fixed DAG RES span (separately computed by replay); and representation memory (not an asymptotic proof-space lower bound). No inference is made from free abstract repeated-clause reuse to free physical certificate construction, source acquisition, search, or machine time. The source is unsatisfiable, but the result is an **upper-bound executable construction**, not a minimum lower bound.

## CORPUS REVIEWED / duplication / contradiction audit

Read `proof1.txt` (blob `f46f6aae25571340a5fd17a5181d51c271509947`) and `proof2.txt` (blob `42943fe447c6061fb8009a526f46ac8a6684765c`; over 1 MB, reviewed headers/current tracked dependencies rather than claiming exhaustive reread), issue #3 and recent peer comments, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, latest five-role handoffs, exact original /341 and /386 checkers, actual LSPV-2/539-549 reports and /562-/564, and relevant LSPV-1/566-/569, LSPV-4/535 and LSPV-3/555. Historical /341 fixture dispatches SOURCE/AND3/XOR, while /386 dispatches SOURCE/DEF/RES. A dual-checker polyglot (/549) proves no mixed-parent transition. Required external repositories `konard/p-vs-np`, `blkph0x/p-vs-np-proof-research`, and FRAT-XOR are comparative sources, not native authority.

**What changed relative to root main:** an executable *per-step*, rather than only completed-trace, value-novelty lower-cost abstraction and a concretely reversible terminal-live duplicate, subject to exact sibling source and checker preconditions. Earlier /562 already establishes a different general completed-trace value quotient; /564 already establishes the orientation symmetry; /559 already establishes the external-source mismatch. No optimal W29 claim, branch rule, historical new weight, or full R_mix341 grammar is new. **Stale/overstated claims:** any report treating /341+ /386 as one historical mixed checker, or interpreting abstract W=29 as verified full-calculus lower bound, would be false.

Primary literature checked: Cook and Reckhow (1979), `https://doi.org/10.2307/2273702`; Cousot and Cousot (1977), `https://doi.org/10.1145/512950.512973`; Clarke et al. (2000), `https://doi.org/10.1007/10722167_15`; Baek, Carneiro, and Heule, FRAT (2022), `https://doi.org/10.46298/lmcs-18(2:3)2022`. These motivate proof-system and CEGAR discipline, not the historical grammar.

**ADOPTED:** historical source occurrence audit, exact charged owner identities, prior /562 real quotient, prior /564 signed port symmetry. **REJECTED:** a parser that silently deletes noncanonical native accepted-byte variants; treating unsupported opcodes as impossible historical operations; mixing sibling source formulas; equating paid work with certificate bits or construction time.

## Artifacts and next obligations

Executable, separately labeled reference replayer and original OS checker harness: `experiments/arc/lspv2_565_native386_step_alpha.cjs`. Machine-verifiable exact accepted 2,919-byte duplicate: `results/raw/arc/2026-11-11_1412_LSPV2_565_ACCEPTED_DUPLICATE.json`; native OS 10-case manifest: `results/raw/arc/2026-11-11_1412_LSPV2_565_ALPHA_ORIGINAL_OS_RESULTS.json`.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1 full historical accepted-byte grammar, P2-C3 all-rule cost-sound abstraction, P2-B1 superpolynomial all-rule minimum, and separate P2-B2/B3 bridge all remain OPEN. So do P1-01/03/04. Root main.tex requires a complete current body, authenticated ownership-region splice, SHA lease and readback; GitHub fetch at current blob `8f6e2862a8bb9c735c677a846b6de21ad0ad5a67` returned zero content, so no destructive overwrite was attempted.

**Next exact target:** recover one authoritative historical original checker implementing RES-to-AND3 or DEF-to-LOCAL-CONVERT with signed contexts, then test a source-bound positive and at least two corrupt signed-port witnesses. Existing five automations, ownership boundaries, schedules, historical two Route A / three Route B labels, fixed weights and Pacific timezone are unchanged. No agents or automations were added or modified. **P versus NP remains OPEN.**
