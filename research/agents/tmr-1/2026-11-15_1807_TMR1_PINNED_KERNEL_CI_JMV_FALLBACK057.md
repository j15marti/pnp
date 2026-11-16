# TMR-1/057 | Pinned Anthropic dual-kernel CI verification and a source-level E^NP fallback

**Time:** November 15, 2026, 18:07 PST. **Identity:** PNP Machine Model Lead, Track C. **Status:** UPSTREAM EXECUTION RECORD VERIFIED (source provenance); KNOWN THEOREM / CONDITIONAL for E^NP circuit implication; independent local kernel build and independent mathematical review **OPEN**. P versus NP **OPEN**.

## Candidate, quantifiers and falsifiers, committed before investigation

**Candidate C1e-CI-PROVENANCE and C1f-COR3-BASELINE:** For the exact pinned source commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`, inspect the genuine upstream Actions log and comparator configuration to independently verify that the reported source proofs were actually submitted to Lean and nanoda as the exact two stated propositions. Separately derive the *weakest completely sourced* consequence: if the formal machine semantics realizes ordinary deterministic ETH failure, Jahanjou-Miles-Viola Corollary 3(1') gives a language in `E^NP` outside linear-size circuits. This is independent of the bespoke quantitative hierarchy reconstruction /056.

Quantifier prefix: **one fixed pinned commit** and a public upstream execution; **for every positive SAT exponent epsilon** a standard solver running in `2^(epsilon n)` (after absorption of polynomial overhead), **there exists** an `E^NP` language not in nonuniform `SIZE(O(N))`. All-input CNF input restrictions, failed parse, and count semantics remain those in /055 and the owned manuscript.

Falsifiers:
1. Source SHA, toolchain, comparator and reported run head do not match the pinned theorem.
2. Successful run omits `Solution.lean` or only compiles the `Challenge.lean` sorry stubs, never verifying the purported proofs.
3. Comparator allows unexpected axioms, `sorry` in proof sources, or a different theorem type.
4. A source-to-standard-machine, encoding or representation conversion changes SAT decision semantics or consumes `2^(Omega(n))` work, invalidating the failure-of-ETH transfer.

Falsifiers 1–3 passed the **public upstream evidence audit**; falsifier 4 requires a separate model-interpretation audit. This does not assert independently rebuilding the Lean project.

## Original-source observations and reproduced evidence

Pinned Anthropic source: [MainResults.lean](https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/MainResults.lean), [Solution.lean](https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/Solution.lean), [comparator.json](https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/comparator.json), and [project README](https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/README.md).

**GitHub Actions execution [run 40442388505](https://github.com/anthropics/formal-math/actions/runs/40442388505), job 121985557508** has head SHA exactly `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. On October 27, 2026 (UTC), the verify-eth job completed successfully after explicitly installing Lean **4.33.1**, retrieving Mathlib, invoking `lake build`, and running `bash ../.github/scripts/comparator-check.sh`. The job log has **1,558 lines, 128,343 characters**. It reports `Built MainResults` and `Built Solution` (not only placeholder declarations). The only two unique `declaration uses sorry` source locations are `Challenge.lean:12:8` and `Challenge.lean:16:8`; the CI check rejects that warning elsewhere. The final log explicitly says `nanoda kernel accepts the solution`, `Lean default kernel accepts the solution`, `PASS comparator.json`, and `All 1 comparator configuration(s) accepted`.

The pinned comparator names exactly `MainResults.ethIsFalse` and `MainResults.mainTheorem`, with `enable_nanoda=true` and permitted axioms `propext`, `Quot.sound`, `Classical.choice`. Toolchain/source fingerprints in that execution include comparator commit `575674928e239f5bc452aab72d1dd7b0f1326494` and nanoda commit `68d5ca9db226849b41a6fff59d796ff19d0a8840`.

**Provenance finding:** Contrary to an evidence-level claim that the pinned formal proof has *never* been kernel-built, a public, SHA-matched upstream dual-kernel build is directly observable. Contrary to a stronger claim that **we independently** rebuilt the proof, no local Lean, lake, Mathlib cache, nanoda or #print axioms command ran in this environment. The upstream comparator configuration supplies an axiom allowlist, but a fresh transitive local printout is still OPEN. Kernel acceptance of a Lean proposition and correctness of its interpretation in conventional bit-time complexity are separate claims. The original Anthropic README explicitly notes that Lean does not verify the correspondence between its written statement and the paper's prose.

Full unedited upstream job log captured separately:
`results/raw/tmr/2026-11-15_1807_TMR1_ANTHROPIC_PINNED057_UPSTREAM_JOB_LOG.txt`.
Captured structured source evidence:
`results/raw/tmr/2026-11-15_1807_TMR1_ANTHROPIC_PINNED057_CI_AUDIT_RAW.json`.
Offline re-audit script:
`experiments/tmr/tmr1_pinned_ci_audit057.js`.
The raw JSON records the checked source/version/run claims and explicitly sets independent source-machine semantics review to false. It does not contain a speculative claim about missing dependency pins. Every observed CI verdict is backed by fetched original GitHub records. The hosted JS extraction and comparisons were executed against the authentic 128 KB log; the standalone Node script and local Lean project were **not** executed. No random seeds; deterministic public run ID and commit pins.

## Named dependency closure: C1f-COR3-BASELINE (KNOWN THEOREM, conditional source trust)

The source type of `MainResults.ethIsFalse` is `not (0 < s 3)`. Here `s 3` is the nonnegative infimum of exponents delta for one uniform deterministic `TM2ComputableAux` per exponent, with correct answers for all n and all `IsKCNF 3` formulas. As a nonnegative infimum, it equals zero under this proposition. Given any epsilon>0, a smaller admissible exponent delta<epsilon exists; a standard finite-stack-to-fixed-multitape simulation, full source parsing, duplicate removal and output convert that to an ordinary 3-SAT decider within `2^(epsilon n)` after polynomial costs are absorbed. The standard source encoding has at most polynomially many distinct width-three clauses in n, and the machine has finite alphabets/stacks. This is the exact **ETH-false** premise in Jahanjou, Miles and Viola, *Local reductions*, ECCC TR13-099 revision 3 (March 31 / posted April 4, 2014), Corollary 3(1').

Their [Corollary 2(1) and Corollary 3(1')](https://eccc.weizmann.ac.il/report/2013/099/revision/3/download) conclude **some function in E^NP is not computable by linear-size general Boolean circuits**. Therefore, conditionally on the pinned formal proposition and its correct physical-machine interpretation:

`E^NP not subset SIZE(O(N))`.

This is a **KNOWN cited implication**, not a novel NP-level theorem. It provides a source-based independent control for the stronger, independently unreviewed `Omega(N sqrt(log N))` hierarchy reconstruction /056. It does **not** directly certify that stronger constant/exponent, does not imply superpolynomial circuits or an NP lower bound, and does not prove P!=NP. The JMV source's `v=Theta(ell)` is **bits per variable name**, not the total number of formula variables.

The paper's Theorem 1 states the full explicit local reduction for `T>=2^n`: `ell = log T+O(log n)+O(log log T)` and output `3v+3` index-to-clause bits, each a bounded-depth junta. The /056 J56 paid discovery remains a separate additional quantitative route, not a premise of this simpler corollary.

## Same-execution resource and control ledger

| Stage | Source/input and machine cost | Same physical workspace |
|---|---|---|
| Formal #SAT source | pinned `FinTM2` counting bound, complete low-first clause input | unquantified by the source's time statement |
| Authentic explicit circuit to #CNF | `O((B_C+B_A)^4)` bit operations, `V=q+G`, `m'<=4n'` | `O(B_C+B_A)` bits |
| Finite-stack physical simulation | `O(T_M+B_A^2)` bit operations for fixed finite stack counts/program | `O(T_M+B_A)` bits |
| Decision/ETH wrapper | read exact count bits, compare with zero; polynomial CNF conversion | `O(n'+B_A+T_M)` bits conservatively |
| JMV circuit consequence | published conditional implication from existence of sufficiently small-exponent SAT deciders | no simultaneous forbidden DTISP claim |

The first three stages belong to **one** compilation/execution as in /055. The fallback theorem invokes an existing complexity-class reduction and is *not* claiming that an `E^NP` witness is constructed by the raw counting run alone. Source acquisition, compilation, output and actual parsing are charged; no oracle answers are free.

## Four mandatory gates

| Gate | Verdict | Reason |
|---|---|---|
| DISJ sanity | **PASS restricted** | DISJ has full grouped rank but linear circuit. This route makes no rank-to-circuit hardness inference, and supports Horn/Krom, affine/Gaussian, treewidth and compact alternatives. |
| Relativization | **PASS for known implication; OPEN NP promotion** | JMV derives an E^NP consequence under a computational algorithm hypothesis, not a relativizing P!=NP proof. A new NP theorem would need nonrelativizing content and algebrization/Natural Proofs review. |
| Simultaneous DTISP | **PASS for charged single-algorithm upper ledger; NOT APPLICABLE to FLMV contradiction** | Full source/output and peak storage for one model are accounted; no small-space forbidden time-space box is entered. |
| Configuration counting | **PASS upper bound only** | `T<=2^{O(S+log N)}` for total fixed deterministic read-only-input machines, no necessary-work bound or randomized/quantum inference. |

The four source-level falsifiers above are still mandatory for stronger promotion; /341 remains FAIL as full UNSAT authority and /386 RESTRICTED. Unknown paths are MAY. Other agents' tensor/fronter and checkpoint models are not assumed to transfer to a general circuit.

## Reconciliation and next dependency

The owned paper `main1_PNP_MACHINE_MODEL_LEAD.tex` was updated in place with the upstream CI result and the sourced JMV fallback. Historical /056 algebraic proof, code and raw were preserved; the retired trackers and peer-owned manuscripts were not touched. The repository was not available as a local checkout; `python .codex/skills/pnp-research/scripts/preflight.py --check --json`, local LaTeX build, and local Lean kernel/axiom printout were NOT executed. Upstream public CI status **was** observed, not rerun.

**ONE next load-bearing lemma:** independent fresh local Lean v4.33.1 build of the pinned project, inspect `#print axioms MainResults.mainTheorem` and `ethIsFalse`, then check the full `FinTM2` starting stack, per-block time and bit-encoding translation in the physical compiler; separately review the bespoke quantitative /056 hierarchy construction.

Scientific status: **UPSTREAM CI EVIDENCE VERIFIED; source-level JMV implication KNOWN; direct /056 quantitative transfer CONDITIONAL and independent review OPEN; P versus NP OPEN.**
