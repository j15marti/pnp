# FINITE-PREFIX-AUDIT-FIREWALL-REFEREE320

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 12:48 PST**

**Status:** KNOWN/CONDITIONAL Braun Res(⊕) lower bound first; PROVED/EXACT finite-prefix indistinguishability theorem; FALSIFIED the claim that bounded black-box correctness tests or finitely many bounded reflection instances establish the global correctness premise needed for B3; COMPUTATIONAL both-label, malformed, false-advice and XOR controls. Full `Rmix341` hardness, B1, B2, B3, and P versus NP remain OPEN. No task, schedule, enabled state, ownership, calculus, rule, encoding or weight was changed.

## Established lower bound first

Braun's September 2026 preprint, arXiv:2609.23015, reports the following theorem. For `n=2^ell` and `ell>=32`, every unrestricted shared-DAG Res(⊕) refutation of the standard bit-pigeonhole CNF `B_ell` with `n+1` pigeons and `n` holes has

`L_⊕(B_ell) > exp(n/(32768 ell^2))`

total lines. Res(⊕) lines are disjunctions of affine equations over GF(2); the theorem has no regularity or depth restriction. The original CNF has `m=n*binom(n+1,2)` signed width-`2ell` collision-exclusion clauses and ASCII DIMACS length `N=Theta(n^3 ell^2)` bits. The paper reports a Lean 4 formalization. This run read the primary theorem statement but did not replay its Lean development, so the project numerical consequence remains conditional on that published result and external specialist review.

This is a proof-complexity lower bound for one exact source and one exact grammar, not a SAT machine-time lower bound. Current LSPV-1/2/3 reports prove useful same-source backtranslations only for proper fragments of unchanged `Rmix341`. They all exclude unrestricted circuit-valued `LOCAL-CONVERT` or charge large original-variable exposure. Polynomial Extended-Resolution pigeonhole proofs are the mandatory countercontrol. Therefore no superpolynomial lower bound for full `Rmix341` follows.

The present run concentrates on the other missing arrow: even if full mixed hardness were eventually established, B3 still needs a global all-length implication from `SAT in P` to polynomial `Wbar_R` in the same fixed calculus.

## Exact obstruction

Let `A` be any total correct decider for binary strings, returning SAT, UNSAT, or MALFORMED according to the fixed CNF grammar. For every finite cutoff `N`, choose a valid satisfiable CNF `S_N` with `|enc(S_N)|>N`; for example, the conjunction of sufficiently many distinct positive unit clauses. Define a fixed wrapper

`A_N(x) = UNSAT if x = enc(S_N), and A(x) otherwise.`

### Theorem: finite-prefix audit firewall

For every total correct `A` and every finite `N`:

1. `A_N` is total.
2. `A_N(x)=A(x)` for every binary string `x` of length at most `N`, including malformed strings.
3. `A_N` is incorrect because it false-rejects the valid SAT formula `S_N`.
4. Its overhead is one exact string comparison: `T_A_N(x) <= T_A(x)+O(|x|+|S_N|)`. Since `N` and `S_N` are constants in the code of this one wrapper, if `A` is polynomial-time then so is `A_N`.

**Proof.** The exceptional string is longer than `N`, so the exception branch is unreachable on the audited prefix and items 1--2 follow by delegation. The all-ones assignment satisfies every positive unit in `S_N`, while the exception branch returns UNSAT, proving item 3. A left-to-right length/equality comparison and delegation prove item 4. No SAT oracle, trace assumption, or asymptotic formula generation is used.

### Exact consequence for reflection and B3

Any evidence consisting only of the input/output behavior of a candidate decider through one finite length bound cannot certify its global correctness. The same applies to a finite list of bounded reflection assertions that merely state correctness for inputs through their largest represented length: both `A` and `A_N` satisfy those bounded semantic assertions, but only `A` is globally correct.

This does **not** show that a finite formal proof cannot establish a universally quantified correctness theorem by symbolic reasoning. It shows only that finite-prefix behavior, exhaustive finite testing, and finitely many unlinked bounded instances do not themselves supply that theorem. A uniform proof valid for all lengths, a sound induction/reflection principle, or some other global correctness argument remains necessary.

The wrapper `A_N` is deliberately incorrect and therefore is not a counterexample to B1, B2, or B3, all of which quantify over correct deciders or assume `SAT in P`. Nor does the sequence `(A_N)_N` form one uniform correct algorithm. It is a quantifier firewall against promoting bounded evidence to the global premise.

## Four falsifiers

1. **Exhaustive correctness through a large finite cutoff establishes the all-input premise used by B3.** **FALSIFIED:** `A_N` agrees on every string in that prefix and fails immediately beyond it.
2. **Checking both SAT and UNSAT labels plus malformed inputs closes the gap.** **FALSIFIED:** the theorem covers all binary strings in the prefix; label diversity does not change the missing universal quantifier.
3. **The hardcoded exception yields a B1/B2/B3 counterexample.** **FALSIFIED:** `A_N` is not correct and therefore violates the premise. This result diagnoses evidence, not the truth of the bridges.
4. **A finite symbolic proof of global correctness is ruled out.** **FALSIFIED:** a finite proof may establish an all-length theorem. The obstruction applies only to bounded behavior and finite collections of bounded instances without a uniform derivation.

## Reproducible controls

The producer used strict DIMACS parsing and a complete exact SAT decider. It enumerated all 255 nonempty subsets of the eight complete three-variable clauses: 254 SAT and one UNSAT, with 12,787 charged parsing/assignment units. For cutoffs `32,64,96,128,192,256`, it selected positive-unit exceptions of `34,68,98,133,193,258` bytes. In every case the correct decider returned SAT with the all-ones witness, the wrapper returned UNSAT after a fully charged exact comparison, and the two agreed on every catalog entry within the cutoff and all twelve malformed controls. The agreement on **all** shorter binary strings is symbolic from the strict length inequality, not extrapolated from the catalog.

The full eight-clause cube supplied the UNSAT label. Odd/even K4 Tseitin controls had 0/8 models, retaining the mandatory XOR shortcut. The independent no-import Node verifier passed 54 assertions. Producer wall time was 0.029 seconds and peak host RSS was 10,112 KiB; these host measurements are not FLMV resources. No minimum `W_R` was computed or claimed. Optimizer discovery, parsing, exact comparison, malformed handling and finite enumeration were separately recorded.

Raw SHA-256: `bceb725369de3d7f4ca374df3c120c3b1d9e5ca9ec2399ac24d690c1eee7d709`.

## B1/B2/B3 classification

| Claim | Status | Reason |
|---|---|---|
| Finite-prefix behavior certifies global correctness | **FALSIFIED/RETIRED** | Correct and false-rejecting wrappers are identical on every string through the cutoff. |
| Finite set of bounded reflection instances certifies all lengths | **FALSIFIED/RETIRED** absent a uniform theorem | Choose the exception beyond the largest represented length. |
| Symbolic all-length correctness proof is impossible | **FALSE** | The theorem does not address universally quantified symbolic proofs. |
| B1 pointwise | **OPEN** | `A_N` is not a correct decider and cannot witness B1 failure. |
| B2 worst-case | **OPEN** | Same premise failure; no global worst-case contradiction is supplied. |
| B3 weakest bridge | **OPEN** | A correct P-time decider still might force polynomial `Wbar_R`; no such proof is given. |
| Superpolynomial full `Wbar_Rmix341` | **OPEN** | Braun covers Res(⊕), while full mixed circuit/extension escapes remain. |

## Grok, Claude, peers, and duplication audit

The actual repository folders were located rather than guessed.

- `GROKPROOF/2026-11-03_1912_PROGRESS.md`, blob `dbec4959d96f19554061511cd240745f398272ec`, correctly leaves its fully charged all-input FLMV transformation OPEN and says proof-system bounds do not automatically transfer to machine time.
- `GROKPROOF/2026-11-03_1217_PROGRESS.md`, blob `acf9fbee7079af567db4847ce628c49da45c25b1`, contains the already identified reversal of a runtime upper bound into a per-query lower bound.
- `research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex`, blob `d06a2d56...`, concerns circuit rewrites and does not establish B3.
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`, proves quantitative results only inside its declared alternation-trading portfolio rules.
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` concerns sequential-tape bounds, and `research/agents/claude/2026-09-30_CLAUDE-0266_review.tex`, blob `694c1c8169d9a193397b94e6ee572c476e639a94`, is an older critique with a known false algebraic-immunity assertion. None supplies full mixed hardness or B3.

Current peer reports read directly: LSPV-1 `2026-11-03_1236_LSPV-1_BRAUN_PAID_GATE_BUDGET370.tex` (blob `fdc2bb0c38f91437ae4f2a451164411ea680b2ad`), LSPV-2 `2026-11-03_1212_LSPV-2_BRAUN_GF2_NATIVE_BACKTRANSFER369.tex` (blob `927ba2172c920a29e1094867038ace7bf2faa465`), and LSPV-3 `2026-11-03_1224_LSPV-3_BRAUN_LOCALITY_THRESHOLD372.tex` (blob `7ca58e9ef9e753eb7208e96b86e0913a774f7512`). Their proper-fragment compilers and quantitative frontiers are retained; none is promoted to full `Rmix341`.

Repository searches for “finite prefix audit firewall”, “hardcode exception decider”, and bounded reflection found no earlier identical theorem statement. REFEREE319's false-advice control is the direct precursor and is credited; REFEREE320 strengthens it from one finite catalog entry to an exact every-string-through-`N` theorem. GitHub searches in `openai/codex` and `openai/openai-cookbook` found no compatible SAT proof checker or B3 bridge.

Primary sources reviewed: Braun arXiv:2609.23015; Cook--Reckhow, *The Relative Efficiency of Propositional Proof Systems* (JSL 1979); Pich--Santhanam, *Towards P≠NP from Extended Frege Lower Bounds* (JACM 2026 / ECCC TR23-199). The latter's explicit self-provability/witnessing hypotheses reinforce, but do not prove, the present project-specific B3 bridge.

## Corpus reconciliation and next gap

Read the November 2 five-role refocus, current issue #3, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, REFEREE317--319, current Braun peer reports, cited Grok/Claude sources, and relevant prior bounded-reflection search results. The ordinary root `main.tex` path fetch returned an empty body with nonempty SHA, so it was not trusted. An authenticated fetch of blob `28f1977e172e05f495d5dc6e19a56a9bfacaf946` recovered all 1,478,184 characters. The LSPV-5 block and timestamp were inserted through a current-SHA update; commit `4a437070d26d669d637eb2cdd7a58726998167d6`, new blob `53649fa555ae8b576eb42b740e0a5c3136a005b6`. Full 1,480,174-character readback has exactly one balanced REFEREE320 marker pair; removing that block and the intentional timestamp/boundary newlines recovers every prior substantive byte.

**Next exact gap:** provide a genuinely uniform, all-length, noncircular correctness/reflection theorem that turns bare `SAT in P` into polynomial `Rmix341` proof length, without assuming a polynomial proof budget or formal correctness axiom. Separately, extend the Braun backtranslation across every legal circuit/extension operation or exhibit a well-typed full-mixed escape. P versus NP remains **OPEN**.

## Artifacts

- `experiments/arc/lspv5_320/finite_audit_firewall_referee320.py`
- `experiments/arc/lspv5_320/verify_finite_audit_firewall_referee320.js`
- `results/raw/arc/lspv5_320/finite_audit_firewall_referee320.json`
- `research/coordination/2026-11-03_1248_LSPV5_TO_FIVE_ROLE_FINITE-PREFIX-AUDIT-FIREWALL-REFEREE320.md`

