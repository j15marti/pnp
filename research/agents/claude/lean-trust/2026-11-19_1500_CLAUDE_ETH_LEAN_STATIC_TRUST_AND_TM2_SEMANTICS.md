# CLAUDE routine | 2026-11-19 ~15:00 PST | Static trust surface of pinned Anthropic ETH Lean tree + Mathlib TM2 semantics

Status: P versus NP remains OPEN. This is an additive role-owned report by the hourly Claude routine (`research/agents/claude/`). It edits no TMR manuscript; corrections/evidence for TMR-1 and TMR-5 go through issue #3.

## Named dependency advanced

TMR-1 (main1, "ONE next load-bearing lemma") and TMR-5 (main5, "One highest-value next lemma") both name the same open arrow in the Track C chain:

> independent pinned Lean v4.33.1 + Mathlib rebuild of `MainResults.mainTheorem` / `MainResults.ethIsFalse`, transitive `#print axioms` audit, and physical FinTM2 semantics.

This run splits that arrow into (a) kernel replay, (b) transitive source trust surface, (c) Mathlib TM2 semantics used by the statement. It closes (b) at the STATIC level and (c) at the source-reading level, and reports (a) as BLOCKED in this environment.

## Candidate and falsifiers (stated before searching)

Candidate: the 1,052-file pinned `eth/` tree introduces no trust beyond Mathlib + Lean's three standard axioms at the source level, and the Mathlib TM2 notions in `MainResults.lean` denote a finite-control, finite-alphabet multi-stack machine with step = one bounded block, matching TMR-1's C1e physical simulation.

Falsifiers: (F1) any `axiom`/`sorry`/`admit` outside `Challenge.lean`; (F2) any kernel-bypassing or native-evaluation construct (`native_decide`, `Lean.ofReduceBool`, `implemented_by`, `extern`, `debug.skipKernelTC`, custom `elab`/`macro`/`addDecl` meta code, `unsafe`, `opaque`); (F3) an import outside Mathlib/Batteries/in-tree; (F4) a TM2 semantic gap: steps not bounded per block, halting not forced by the target configuration, or an infinite work alphabet giving free unbounded registers.

## (a) Kernel replay: BLOCKED (not executed)

`git clone` of `anthropics/formal-math` succeeded and `git checkout 16a5ce41304fcdaea4e0be7c132e1c361dc26da5` was confirmed. Installing the Lean toolchain (elan installer; then, separately, the official v4.33.1 release tarball) was refused by this session's permission policy. No retry/workaround was attempted. Therefore: no `lake build`, no `#print axioms`, no Comparator, no nanoda was run here. The upstream-CI evidence recorded by TMR-1 (run 40442388505, job 121985557508) remains the only kernel evidence; this report does not upgrade it.

Unblock (for the user/owner): allow the Lean toolchain install in the routine environment, then in `eth/`: `lake exe cache get && lake build && lake env lean scripts/PrintAxioms.lean`, optionally `bash ../.github/scripts/comparator-check.sh` (needs go, cargo, jq; builds comparator 5756749, nanoda 68d5ca9, landrun 811cfff). Upstream README reports ~8 min on 24 vCPUs, ~7 GB peak; this container has 4 CPUs / 15 GB, so expect roughly 30-60 min.

## (b) Static transitive trust scan: PASS (static only)

Executable: `experiments/claude/lean_trust_scan.py` (blob `1cdd046f656adaa498a3df4cfb090650e94c3b16`), run with `python3 -I`, 2.6 s. It strips nested `/- -/` block comments, `--` line comments and string literals, then regex-matches 19 trust-relevant constructs.

Raw: `results/raw/claude/2026-11-19_anthropic_eth_lean_trust_scan.json`. Tree: 1,052 `.lean` files, 152,420 lines, content digest sha256 `c06409176b299ba6e2b2bd1154b6dbe7ed3fe6626f0ca85e21094911f6e4dc4d` (sorted relative path + bytes).

Result: `sorry` 2 hits, both `Challenge.lean` lines 13 and 17 (the intended Comparator placeholders; `Challenge` is imported by nothing). Every other count is 0: `admit`, `axiom` declarations, `opaque`, `unsafe`, `partial def`, `implemented_by`, `extern`, `native_decide`, `ofReduceBool`/`reduceBool`, `skipKernelTC`, `set_option debug.*`, `elab`/`macro`/`syntax`/`macro_rules`, `run_cmd`/`#eval`, `addDecl`/`mkAxiom`, `@[csimp]`, `maxHeartbeats 0`, `import Lean`. There is no `set_option` of any kind in the tree. 1,046 files use the Lean module system (`module`, `import all`), which only affects visibility.

Import closure (F3): 99 distinct import roots; all resolve to in-tree modules except `Mathlib` and `Batteries` (a Mathlib dependency pinned by `lake-manifest.json`). PASS.

Control (scanner sanity): `results/raw/claude/2026-11-19_lean_trust_scan_planted_control.json`. A planted file with 5 live constructs (2 axioms incl. `private axiom`, `native_decide`, `implemented_by`, `set_option debug.skipKernelTC`) and 3 decoys (nested block comment, line comment, string literal) yields exactly the 5 live hits and 0 decoy hits.

Scope limits: static regex matching is not a proof-term audit. It does not scan Mathlib/Batteries themselves (a `native_decide` there would show up as `Lean.ofReduceBool` in `#print axioms`, which was NOT run). It cannot detect statement mismatch; that is Comparator's job and the TMR-1/TMR-5 manual reading. It complements, not replaces, (a).

## (c) Mathlib TM2 semantics at Mathlib 0df444a: PASS (source reading)

Fetched raw at the pinned revision: `TuringMachine/Computable.lean` blob `7779a00f0c3c3909923a5f1bde6b3120b5c2d28a` and `TuringMachine/StackTuringMachine.lean` blob `916694942a3bfefa0bd9085e2f48735dbe8e0f5b` (both equal TMR-1's cited blobs: independent confirmation), `StateTransition.lean` blob `e5493de7dbd43075678491ebd35aad2de59f8edc` (new pin).

Facts read off the source:

1. `FinTM2`: `Fintype K` (stacks), `Fintype Λ` (labels), `Fintype σ` (states), `Fintype (Γ k₀)`; program `m : Λ → TM2.Stmt`. `Stmt` is an inductive tree (`push/peek/pop/load/branch` with a continuation, leaves `goto`/`halt`), so each block is a finite loop-free tree.
2. `TM2.step` on `⟨some l, v, S⟩` runs `stepAux (m l)` to the first `goto`/`halt`; on `⟨none,_,_⟩` it returns `none`. One step therefore costs at most `D = max_l depth(m l)` stack operations, a machine constant.
3. `TM2OutputsInTime tm l (some y) t := EvalsToInTime tm.step (initList tm l) (some (haltList tm y)) t`, and `EvalsToInTime` is `∃ steps ≤ t, (flip bind step)^[steps] init = some halt`. Since `haltList` has label `none`, reaching it means halting; determinism makes `steps` the actual halting time. `haltList` also forces all non-output stacks empty and `var = initialState`. `initList` places the input list on `k₀` with the list head on top, so `encInput` is read first-bit-first.
4. (F4, infinite alphabet) Lemma, PROVED/EXACT here (informal, independent review OPEN): for any `FinTM2` and any input, every symbol ever on a stack `k ≠ k₀` lies in the finite set `{f v : push k f _ occurs in some m l, v ∈ σ}`, and on `k₀` in that set plus the finitely many input-alphabet values. Proof: `pop`/`peek` never create symbols; the only creation is `push k f`, whose value is `f v` with `v ∈ σ` finite, and there are finitely many push nodes in finitely many finite trees. Consequently the extra hypothesis `∀ i, Finite (M.tm.Γ i)` in `MainResults.InTime`/`MainTheorem` is semantically redundant, and an infinite declared work alphabet cannot supply free unbounded counters. A physical multitape simulation encodes only the reachable symbols with O(1) bits each.

Consequence for the chain: (c) supports TMR-1 C1e as written (finite control, bounded ops per step, exact halting semantics). One caveat to record: `MainTheorem` is a classical `∃ M`; the proof may be nonconstructive (`Classical.choice` is permitted), so it guarantees existence of ONE fixed finite machine but not an explicitly extractable one. Existence suffices for TMR-1's diagonal/hierarchy use (the language is defined against all machines); it does not suffice for any claim that requires running the machine.

## Primary-corpus search (Google DeepMind / OpenAI repositories)

`google-deepmind/formal-conjectures`, `FormalConjecturesForMathlib/Computability/Complexity.lean` (main, blob `9371e7702155d651bbd32ccff3e3bddf4146dcc6`): defines `ComplexityTheory.P`/`NP`/`coNP`/`BPP` over `List Bool → Bool` via Mathlib `TM2ComputableInPolyTime`, i.e. the same `FinTM2` + `TM2OutputsInTime` model, with NO work-alphabet finiteness hypothesis. By lemma (c4) this is still the textbook class P. So the Anthropic statement and a community formal P/NP statement live in one machine model; a future NP-level step of the Track C chain could be stated against `ComplexityTheory.NP` without a model change. No ETH or SAT-lower-bound statement was found there by code search. `openai/ten-proofs` (Lean certificates for ten proofs) matched only a Ramsey file for "SAT"; nothing applicable. The Google Doc "P vs. NP Proof Attempts" was reread (survey of holographic, tensor-network, IPS, GCT, functional-IPS and hardness-magnification attempts and their barriers); it contains no new statement bearing on this dependency.

## Four gates

DISJ sanity: NOT APPLICABLE (audit of a formal upper-bound source; no rank/communication lower bound used). Relativization: NOT APPLICABLE (no separation inferred; the Track C conclusion remains a conditional E^NP mildly superlinear i.o. circuit bound, which relativization does not block per TMR-1's scoping). Simultaneous DTISP: NOT APPLICABLE (no time-space claim; TMR-1 C1e unchanged). Deterministic configuration counting: PASS as consistency check (finite control + finite reachable alphabet, lemma c4, gives the standard 2^{O(S+log N)} configuration bound for the TM2 machine). /341 FAIL and /386 RESTRICTED unchanged; algebrization/Natural Proofs not engaged.

## Status table

| Item | Status | Review |
|---|---|---|
| Static trust surface of pinned eth tree | COMPUTATIONAL PASS (static) | independent of TMR-1 CI evidence; no kernel |
| Import closure Mathlib/Batteries/in-tree | COMPUTATIONAL PASS | same |
| TM2 step/halt/IO semantics at 0df444a | PASS (source reading) | blobs match TMR-1 |
| Reachable-alphabet finiteness lemma | PROVED/EXACT (informal) | independent review OPEN |
| Local kernel build, `#print axioms`, Comparator/nanoda | OPEN: BLOCKED by environment permission | not executed |
| Track C NP-level step | OPEN | unchanged |

## Next load-bearing lemma

Unchanged and now narrower: execute the local kernel replay (a) at commit 16a5ce4 and record the exact `#print axioms` output; with (b) and (c) done, that single execution is the remaining gap before the counting theorem can be cited as locally verified FORMAL rather than upstream-CI-only.

## Unexecuted checks disclosure

No Lean, lake, Comparator, nanoda, LaTeX or repository preflight was executed. Mathlib/Batteries sources were not scanned. The paper (`paper.pdf`) was not reread in this run.
