# TMR-1/058 | FinTM2 source semantics to one physical multitape execution

**Pacific timestamp:** November 15, 2026, 18:57 PST. **Owner:** TMR-1 / PNP Machine Model Lead. **Status:** PROVED/EXACT, fixed-machine simulation lemma, restricted and independent mathematical review OPEN. Source formal proof verification is UPSTREAM VERIFIED, independent local kernel replay OPEN. P versus NP OPEN.

## Pre-search candidate, model, quantifiers and falsifiers

**C1e-STACK-PHYSICAL:** For **each fixed** `M : Turing.TM2ComputableAux Bool Bool` satisfying `∀i, Finite (M.tm.Γ i)`, there exists **one fixed ordinary deterministic locally headed multitape machine** `U_M` and constants `a_M,b_M` such that for **every** finite Boolean input list `x` of length `B`, and **every** `t` for which `Turing.TM2OutputsInTime M.tm x (some y) t` holds, `U_M` starts on an ordinary read-only input source `x`, outputs precisely `y` and halts with both actual time and peak writable-tape occupancy bounded by `a_M(B+t+1)`, `b_M(B+t+1)`, respectively. Input loading, each stack operation, output and verification are paid. This advances precisely dependency **C1e** of the authentic-circuit -> exact-CNF -> formal input -> FinTM2 -> physical counter -> hierarchy chain.

Falsifiers specified before primary-source audit:
1. `FinTM2` may have a variable number of stacks, unbounded internal state/label set, or unbounded stack alphabets, making one formal step hide superconstant data work.
2. `TM2.step` may recursively execute arbitrarily many same-step operations, instead of one bounded, fixed statement tree.
3. The formal start/stop semantics may provide free preinitialized work stacks, ignore input copy, or fail to constrain output stack and terminal configuration.
4. The proposed physical implementation may need random access, uncharged reversal, a separate time-fast/space-small machine, or an unaccounted nonconstant alphabet representation.

All four are discharged **for the exact stated fixed finite machine**, not for arbitrary unbounded-type TM2 programs. Neither a source-derived kernel proof nor a SAT lower bound is inferred.

## Original pinned source evidence

Read, at exact pinned revisions:

* Anthropic `eth/MainResults.lean`, Git blob `1c62a550fa1e4cbec65bb7112f92ad67589afddc`, commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. Its `MainTheorem` is `∃ M C, (∀i, Finite (M.tm.Γ i)) ∧ ∀k n φ, ... CountsWithin ...`. `CountsWithin` uses `TM2OutputsInTime` on `encInput` and exact low-first count bits.
* Matching Mathlib commit `0df444a360eaa60ab8c11dca51a86af692955474`, `Mathlib/Computability/TuringMachine/Computable.lean`, blob `7779a00f0c3c3909923a5f1bde6b3120b5c2d28a`: `FinTM2` explicitly has `Fintype K`, `Fintype Λ`, `Fintype σ`, fixed input/output stack labels, one fixed program `m : Λ → Stmt`, and canonical `initList` and `haltList`.
* Same Mathlib commit, `Mathlib/Computability/TuringMachine/StackTuringMachine.lean`, blob `916694942a3bfefa0bd9085e2f48735dbe8e0f5b`: `Stmt` is an inductive finite tree with `push`, `peek`, `pop`, `load`, `branch`, `goto`, `halt`; `stepAux` recursively executes only the selected finite statement tree to the first `goto` or `halt` per `step`. Stack configurations are lists with an observable empty end.
* Anthropic `eth/Solution.lean`, blob `176892178e49792ae41368c13bb4973bae035b29`, and `eth/proof/maintheorem/CountedRoute/Main.lean`, blob `c57963f3e805e7288cd6df28dbef1d25f3bbd25a`, inspected at the pinned revision. Prior /057 verified upstream dual-kernel GitHub Actions run `40442388505` (October 27, 2026), but **the TMR-1 environment did not execute Lean/lake**.

Primary links: https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/MainResults.lean and https://github.com/leanprover-community/mathlib4/blob/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Computability/TuringMachine/Computable.lean .

## Exact fixed-machine implementation theorem

**Lemma C1e-STACK-PHYSICAL (PROVED/EXACT for fixed machine and finite alphabets).** With the quantifier prefix above, let `K_0` be the fixed number of stacks and `L_0` the maximum number of AST statement nodes along a root-to-leaf path of any `m(λ)`, `λ∈Λ`. Because `K,Λ,σ` and each stack alphabet are finite, every state-dependent map in each statement has one finite table that can be compiled into fixed finite control. `L_0`, all alphabet encodings and all table sizes are constants independent of `B,t,x`.

**Proof.** Allocate one independently locally headed writable tape per stack, plus a fixed number of temporary/output tapes. Store each logical stack with its bottom at physical cell zero and its current top in the cell immediately left of its head. A `push` writes one fixed-width encoded symbol at the head and advances it; a `peek` moves left one cell, reads that cell if present, and moves right; a `pop` moves left, reads, and erases the former top. The empty-stack flag resides in constant control or a marked tape bottom, not in an unbounded binary address arithmetic oracle. `load`, `branch` and `goto` read only fixed internal state and constant lookup tables. Each elementary statement therefore costs at most a machine-dependent constant number of physical tape transitions. From an actual input word `x`, a linear sweep copies `B` symbols to temporary tape, and a reverse sweep loads the input stack with its first list symbol at the logical top. Both sweeps cost `O_M(B+1)` and occupy `O(B)` scratch. None of the other stacks is preloaded.

One formal `step` traverses at most `L_0` nodes and makes no uncharged recursive call beyond the first `goto` or `halt`. Therefore `t` formal steps cost `O_M(t)` physical moves and cause at most `L_0t` pushes. The total live stack symbols are at most `B+L_0t`; the input-copy scratch and finite-control registers are included in peak space. The formal `haltList` relation requires the designated output stack to equal `y`, all other stacks empty and the internal state reset. A linear output sweep, including any necessary reversal, costs at most `O_M(B+L_0t+1)` physical actions and writable cells. This is **the very same sequential run**: `T_{U_M}=O_M(B+t+1)`, `S_{U_M}=O_M(B+t+1)`. No advice, source oracle, or parallel worker is used. QED.

The argument is an ordinary, human-readable machine-model simulation proof, not a claim that this lemma itself was encoded and checked in Lean. In particular, Mathlib's general `TM2` allows types without the finiteness hypotheses; the conclusion depends essentially on **FinTM2** plus the explicitly supplied `∀i,Finite Γ_i`.

## Integration: complete original-input resource chain

For a valid binary shared-gate circuit with `q≥1`, `G≥0`, set `V=q+G` and `B_C=q+G+2+G(2w_C+4)+w_C`. The independently proved functional Tseitin + promise-totalization path gives `n'=V+max(1,4-V)`, `m'≤4n'`, `B_A=n'+5+3m'(⌊log₂(2n')⌋+1)`; it preserves the **exact** count of original accepting assignments. Authenticated parse, circuit construction, all 4 rows per shared gate, clause deduplication, fresh forced-zero variables, literal addresses, output and malformed-source rejection cost `O((B_C+B_A)^4)` time and `O(B_C+B_A)` live writable bits under the declared simple physical implementation.

**Newly discharged transfer:** Applying the lemma to the **single** formal `M` existentially fixed before `k,n,φ`, the compiler/solver/output composition is one deterministic multitape run with
```
T_total = O((B_C+B_A)^4 + T_M(3,n',m')),
S_peak  = O(B_C+B_A + T_M(3,n',m')).
```
The counting conclusion is CONDITIONAL on the pinned formal MainTheorem and source correctness. Its asymptotic runtime remains `2^((12C+o(1))V/sqrt(log₂V))`, in **all** circuit input-plus-gate variables, not in `q` alone. It does not imply a simultaneous forbidden sublinear-space DTISP pair. Conditional JMV `E^NP` linear and quantitative mildly superlinear circuit consequences remain as previously scoped; no NP circuit separation is supplied.

A standard deterministic physical TM can simply reject malformed circuit words after charged polynomial parsing; the formal `M` need not handle malformed CNF input. The physical simulation does not assume the Lean term yields a constructively extractable machine from arbitrary noncomputable classical choice. The existential constant machine `M` is chosen once, before all instances, which suffices for existence of a uniform algorithm.

## Independent finite replay: COMPUTATIONAL only

Local Node v22 script `experiments/tmr/tmr1_fintm2_stack_bridge058.js`, source revision `tmr1-fintm2-stack-bridge058.v1`, xorshift32 seed 20261115, executes 120 deterministic bounded finite-block random programs on 1,920 finite-stack sources; compares reference list-head stack semantics with individually locally headed bottom-to-top tape stacks **after every actual program block**, including empty pops, branches, loads, jumps and halts. 82,128 formal steps, 152,176 visited AST nodes, 209,898 charged tape-micro actions, 1,007,894 assertions, zero failures. The tested programs have 4 stacks, 3 labels, 5 internal states, and finite three-symbol alphabets. This is not a microtrace of Anthropic's enormous actual machine and not a Lean kernel rebuild.

Executed standalone on local Node 22; raw exact deterministic output at `results/raw/tmr/2026-11-15_1857_TMR1_STACK_TAPE058_NODE_RAW.json`. The code and JSON were produced locally. No local repository checkout, updated preflight or LaTeX build was executed: the container has Node and git but no checked-out pnp repository and no Lean/lake, and direct git network DNS is unavailable. Source statements were independently retrieved from GitHub at pins through the connected repository interface.

## Four mandatory gates

| Gate | Verdict | Reason |
|---|---|---|
| DISJ sanity | **PASS restricted** | No static-rank work lower bound; linear-size DISJ circuit remains a legitimate cheap input. |
| Relativization | **PASS for local machine simulation; OPEN for NP-level promotion** | This simulator is relativizing but establishes no P vs NP separation. An actual NP target would require an additional nonrelativizing step, with algebrization and Natural Proofs audits. |
| Simultaneous DTISP | **PASS for actual same-run upper resource ledger; NOT APPLICABLE to forbidden-pair inference** | Time and peak writable space belong to one execution. The space bound can be exponential; no FLMV contradiction. |
| Configuration counting | **PASS upper-bound consistency control** | For deterministic total read-only-input machines `T≤2^{O(S+log N)}`; it yields no lower bound on work and does not extend automatically to random/quantum execution. |

Horn, 2-SAT, affine Gaussian, bounded-treewidth, equality, autarky, products, padding, selectors, unique-solution rank collapse, basis-field effects and genuine compact-circuit alternatives remain allowed. Historical /341 FAIL on unrestricted UNSAT and /386 RESTRICTED are unchanged.

**Independent mathematical review:** OPEN. **ONE NEXT LOAD-BEARING LEMMA:** independent pinned Lean v4.33.1 + Mathlib build and transitive `#print axioms` for both theorem names, followed by source-to-proof term audit at the exact SHA. Physical C1e machine-model transfer no longer needs to be treated as an unstated primitive, but the kernel-replay premise remains unexecuted here.

**MANUSCRIPT:** update owned `main1_PNP_MACHINE_MODEL_LEAD.tex` in place; preserve peers and retired trackers. **P versus NP OPEN.**
