# DECIDER-EXTENSIONAL-COLLAPSE-REFEREE319

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 11:48 PST**

**Status:** KNOWN Haken lower bound first; PROVED an exact extensional-collapse theorem for decider-induced statement-copy proof systems; FALSIFIED the claim that the code, delay, trace shape or verifier work of a correct decider changes the weakest B3 length target; PRESERVED the runtime distinction for B1/B2 and effective proof production; COMPUTATIONAL exhaustive both-label, malformed, false-advice and XOR controls. B1, B2, B3 for `Rmix341`, superpolynomial `Wbar_Rmix341`, and P versus NP remain OPEN. No task, schedule, enabled state, ownership, calculus, rule, encoding or weight was changed.

## Established lower bound first

Haken's 1985 theorem gives a constant `c>0` such that, for every sufficiently large number `h` of holes, every ordinary unrestricted shared-DAG Resolution refutation of the standard pigeonhole CNF `PHP_(h+1)^h` has at least `2^(c h)` derived clauses.

The standard encoding has `h(h+1)=Theta(h^2)` variables, `h+1` width-`h` pigeon clauses, and `h*binom(h+1,2)=Theta(h^3)` binary collision clauses. Under explicit ASCII DIMACS with binary-size variable names its input length is `N_h=Theta(h^3 log h)`. The theorem is therefore a superpolynomial lower bound for **ordinary Resolution line count on this source family**, not an unrestricted SAT-time lower bound.

It does not transfer to the fixed target calculus. `Rmix341` contains its paid ER2/extension fragment, and standard pigeonhole formulas have polynomial Extended-Resolution/Extended-Frege proofs. The current LSPV-2 source-exact reflection experiment strengthens the countercontrol: even a reflecting CNF that exactly specializes to an expander-Tseitin source retains a short authenticated mixed AND3/GF2 proof. Thus the project still needs either a lower bound already covering every mixed rule or a valid reverse domination theorem. This run addresses the latter at the weakest B3 level.

## Decider-induced proof systems

For a total SAT decider `A`, define the statement-copy verifier

`V_A(F,pi)=1`

iff all three conditions hold:

1. `F` is a valid CNF encoding;
2. `pi` is an exact literal copy of `F`;
3. `A(F)=UNSAT`.

If `A` is total and correct, this is sound and complete for CNF-UNSAT. If `A` runs in polynomial time, `V_A` is a Cook--Reckhow proof relation and every UNSAT `F` has a proof of exactly `Theta(|F|)` bits.

The external universal correctness premise remains essential. A rejecting trace records what `A` did; it does not prove that condition 3 is true exactly on UNSAT formulas.

## Exact extensional-collapse theorem

**Theorem.** Let `A` and `B` be any two total correct SAT deciders, with no runtime assumption. Then

`V_A = V_B = {(F,F) : F is a valid UNSAT CNF}`

as accepted proof relations. Consequently, for every UNSAT `F`, the minimum proof length in both systems is the same literal-copy length `Theta(|F|)`.

**Proof.** If `V_A(F,pi)=1`, validity and exact copying hold and correctness of `A` implies that `F` is UNSAT. Correctness of `B` therefore gives `B(F)=UNSAT`, so `V_B(F,pi)=1`. The reverse direction is symmetric. Invalid, SAT and nonidentical-copy pairs are rejected by both. No computation trace or simulation theorem is used.

This has a precise B3 consequence. Under the hypothesis `SAT in P`, choose any total correct polynomial-time decider `A`. The source proof relation is then the canonical linear-copy relation above. Length domination by the same fixed `R` is

`W_R(F) <= p(|F|+|pi|) = poly(|F|)`

for every valid UNSAT `F`, which is exactly polynomial `Wbar_R`. Choosing a different correct polynomial-time decider, padding its running time, changing its internal trace representation, or memoizing special cases cannot change this length target.

Hence the weakest B3 problem is **extensional**. Code-specific correctness proofs or traces can be a method for constructing target proofs, but they are not an additional part of the B3 statement and cannot make one correct decider's length target easier than another's.

This is an exact strengthening of REFEREE317's one-decider formulation, not a P-versus-NP result and not claimed as a novel Cook--Reckhow theorem.

## Boundary: B1 and B2 do not collapse

The extensional theorem concerns proof pairs and minimum proof length only.

- B1 retains `T_A(F)` and asks for a polynomial indexed by each algorithm. Delaying `A` changes the numerical right-hand side even though it leaves `V_A` unchanged.
- B2 retains `T_A^wc(N)` and therefore also depends on the implementation and its slow inputs.
- Effective p-simulation or computation-to-proof production may depend on how `A` is represented and how its correctness is justified.
- B3 discards those runtime terms and asks only whether `SAT in P` forces polynomial worst-case minimum in the fixed calculus.

Thus “runtime is irrelevant to B1/B2” is false, while “different correct decider code creates a different B3 length relation” is also false.

The latest LSPV-1 PHP firewall gives a complementary exact example: under `SAT in P`, one can pad a correct algorithm to have worst-case `Theta(N^K)` while recognizing the Haken family quickly. That refutes the attempted lower-bound inference from a worst-case runtime upper bound to the cost of each query. The present theorem explains why such padding is even less relevant to B3 length: it changes no accepted proof pair at all.

## Four falsifiers

1. **A specially chosen correct P-time decider can induce shorter statement-copy proofs than another correct P-time decider.** **FALSIFIED:** the accepted relations and minimum copy lengths are identical.
2. **Artificial delay or trace padding obstructs B3 length simulation.** **FALSIFIED:** delay changes verification work and B1/B2 runtime terms, not the source proof pairs or their lengths.
3. **A finite advice/table shortcut can safely add a rejected instance without a global correctness proof.** **FALSIFIED by exact control:** one wrong table entry false-rejects a SAT formula and makes the induced proof system unsound.
4. **The extensional collapse proves B3.** **FALSIFIED:** it identifies a unique canonical length target; the missing polynomial domination into the same fixed `Rmix341` remains entirely open.

## Independent exact controls

The finite catalog contains all 255 nonempty subsets of the eight complete clauses on three variables. Exactly one formula—the conjunction of all eight clauses—is UNSAT; the other 254 are SAT.

Three independently scheduled correct deciders were compared:

- direct exhaustive evaluation;
- a fixed finite lookup table with exhaustive fallback outside the catalog;
- an explicitly delayed exhaustive evaluator performing quadratic dummy work before deciding.

Across 765 valid formula/decider runs, all three accepted exactly the same single statement-copy pair. Their measured work differed sharply: 2,682 for brute force, 970,390 for the delayed wrapper, and 255 for the table lookup phase. The table's 2,682-work construction was also charged, giving 2,937 all-phase table work; the low lookup count is not treated as free preprocessing. The minimum accepted proof remained the same 98-byte statement copy.

A fourth decider contained one false advice entry for the satisfiable seven-clause neighbor `S0`. It accepted `S0` as an UNSAT proof, demonstrating loss of soundness. The verifier separately rejected three mismatched-copy records and twelve malformed statements. The independent no-import Node verifier rebuilt all 255 formulas and passed 783 assertions.

Mandatory parity countercontrols returned zero models for odd-charge K4 Tseitin and eight models for the even-charge control.

The finite table is a fixed control plus exhaustive fallback, not a nonuniform all-length SAT algorithm and not evidence for `SAT in P`.

Raw SHA-256: `1a105a3acbf39e5e63edda782c30477d2b34a2534a56cfa47194ac1673e0ad13`.

## B1/B2/B3 classification

| Obligation | Status | Exact reason |
|---|---|---|
| Equality of `D_A` accepted relations for total correct `A` | **PROVED** | All accept exactly valid UNSAT statement copies. |
| Equality of their minimum proof lengths | **PROVED** | Every accepted proof is the same literal copy. |
| Code-/delay-specific B3 length obstruction | **FALSIFIED** | Code and verifier work do not alter the accepted relation. |
| Effective translation from `D_A` into `Rmix341` | **OPEN and stronger than B3** | No proof producer is supplied. |
| B1 pointwise | **OPEN** | Runtime and computation-to-proof production remain algorithm-dependent. |
| B2 worst-case | **OPEN** | Worst-case runtime remains algorithm-dependent. |
| B3 weakest bridge | **OPEN** | Canonical linear-copy proofs are not known to have polynomial `Rmix341` simulations. |
| Superpolynomial `Wbar_Rmix341` | **OPEN** | Haken PHP has an ER escape; Tseitin has a GF2 escape. |

No simulation inequality is reversed, and no restricted proof lower bound is promoted to arbitrary SAT time.

## Grok, Claude and current peers

The actual repository directories `GROKPROOF/`, `research/agents/grok/`, and `research/agents/claude/` were located and read at explicit paths.

| Path | Blob SHA | Independent assessment |
|---|---|---|
| `GROKPROOF/2026-11-03_1912_PROGRESS.md` | `dbec4959d96f19554061511cd240745f398272ec` | Correctly leaves the universal all-input charged transformation OPEN and warns that proof-system lower bounds do not automatically transfer to unrestricted Turing-machine time. It supplies no B3 length domination. |
| `GROKPROOF/2026-11-03_1217_PROGRESS.md` | `acf9fbee7079af567db4847ce628c49da45c25b1` | Its query-volume proof uses an upper runtime bound as if it were a per-query lower bound; LSPV-1 368 gives a conditional uniform counterexample. |
| `research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex` | `d06a2d56befc775660c34a59067b61f0a8c142a8` | Finite circuit-rewriting improvements; explicitly no lower bound moved. |
| `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` | `1f9fc727d3e2b009cba7afec2a93beb62959dd67` | Restricted alternation-trading portfolio theorem, not a same-fixed-calculus B3 simulation. |
| `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` | `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a` | Sequential-access crossing-sequence result; explicitly not random-access B3. |
| `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` | `79e4d4e7e0e3edff3aba8610852c45534bdde128` | Correctly classifies the decisive general arrows as open or conditional. |
| `research/agents/claude/2026-09-30_CLAUDE-0266_review.tex` | `694c1c8169d9a193397b94e6ee572c476e639a94` | Useful arithmetic/citation audit, but its `AI=1` iff affine claim is false (`xy` has linear annihilator `1+x`); no B3 bridge. |

Current peer versions checked: LSPV-1 `HARD_PHP_QUERY_EXPONENT_FIREWALL368` at blob `46bb917f9db0831ed7d33ea4cd5a9736038b1c24`; LSPV-2 `SOURCE_EXACT_MIXED_ESCAPE368` at `a4f5298f6f762b3458094a8535c0981cec8c3f7b`; LSPV-3 `BVP_HORN_SOURCE_TRANSFER371` at `283c36490c1bee3fcb2d90abc4057504755e4345`; and LSPV-4 `SOURCE_EXACT_GENERAL_CNF_LIBRARY_BARRIER367` at `c3b681ee791ddf434e4a079d82e39d159bdb11f0`. They establish respectively a runtime-quantifier firewall, a same-reflection-source mixed escape, a cross-grammar output barrier, and a restricted explicit-library lower bound. None supplies B3.

## Literature and GitHub searches

Recorded web queries were: `Haken 1985 intractability of resolution DOI pigeonhole principle`; `Cook Reckhow 1979 relative efficiency propositional proof systems PDF`; `Krajicek 2021 information propositional proofs algorithmic proof search ECCC`; and `Krajicek Pudlak 1989 propositional proof systems consistency computations DOI`.

- A. Haken, [The Intractability of Resolution](https://doi.org/10.1016/0304-3975(85)90144-6), *Theoretical Computer Science* 39 (1985), supplies the established PHP Resolution lower bound.
- S. Cook and R. Reckhow, [The Relative Efficiency of Propositional Proof Systems](https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf), JSL 44 (1979), supplies the proof-system and simulation framework.
- J. Krajicek and P. Pudlak, [Propositional Proof Systems, the Consistency of First Order Theories and the Complexity of Computations](https://doi.org/10.2307/2274765), separates length simulation from effective p-simulation and connects reflection to optimal proof systems.
- J. Krajicek, [Information in Propositional Proofs and Algorithmic Proof Search](https://eccc.weizmann.ac.il/report/2021/053/), explicitly separates short proofs from the time needed to find them.

Recorded GitHub queries were project-scoped `decider-induced proof system extensional`, `statement-copy proof system`, and `D_A proof relation`, plus OpenAI-scoped `Cook Reckhow proof system SAT decider`. Project search recovered REFEREE317 and older transport work but no prior explicit extensional-collapse statement. The OpenAI-scoped search returned zero applicable results. Absence is not novelty evidence. All named Grok, Claude and peer files above were directly fetched successfully; no inaccessible file is represented as reviewed.

## Work and all-phase space ledger

| Phase | Measured record |
|---|---:|
| Python producer wall time | 0.078663292 s |
| Python producer peak host RSS | 10,368 KiB |
| Node verifier wall time | 0.005383721 s |
| Node verifier peak host RSS | 39,736 KiB |
| Valid formula/decider runs | 765 |
| Independent verifier assertions | 783 |
| Modeled decider work | 976,009 units |
| Malformed/mismatched controls rejected | 15 |
| Producer source bytes | 10,503 |
| Verifier source bytes | 3,590 |
| Raw JSON bytes | 3,051 |

These host measurements are not FLMV tape bounds. Parsing, canonical serialization, exact-copy comparison, three decider schedules, actual delay loops, false-advice checks, malformed rejection, model enumeration, XOR controls, serialization and independent replay were charged. The logical proof-length statement deliberately ignores proof discovery. The all-phase space envelope remains `s'<=max{rho,eta,lambda,lambda*s}`.

## Artifacts and next exact gap

- Producer: `experiments/arc/lspv5_319/decider_extensional_collapse_referee319.py`
- Independent verifier: `experiments/arc/lspv5_319/verify_decider_extensional_collapse_referee319.js`
- Raw ledger: `results/raw/arc/lspv5_319/decider_extensional_collapse_referee319.json`
- Five-role handoff: `research/coordination/2026-11-03_1148_LSPV5_TO_FIVE_ROLE_DECIDER-EXTENSIONAL-COLLAPSE-REFEREE319.md`

The next B3 target should no longer spend effort choosing among extensionally identical correct decider systems. It must prove a polynomial `Rmix341` length bound for the canonical UNSAT statement-copy relation—equivalently polynomial `Wbar_Rmix341` under `SAT in P`—or use a genuinely different noncircular transfer. Code-level correctness and trace theorems are useful only insofar as they actually construct those target proofs.

**P versus NP remains OPEN.**
