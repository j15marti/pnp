# COOK-RECKHOW-B3-TRANSFER-REFEREE317

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 09:48 PST**

**Status:** KNOWN Cook--Reckhow theorem; PROVED an exact conditional equivalence between B3 for the unchanged fixed calculus and length simulation of a decider-induced proof system; FALSIFIED the general lemma that soundness, completeness, and effective verification imply polynomial proof bounds; COMPUTATIONAL independent both-label and malformed controls. No length simulation into `Rmix341`, B1, B2, B3, superpolynomial `Wbar_Rmix341`, or P-versus-NP conclusion is proved. No task, schedule, state, ownership, calculus, rule, encoding, or weight was changed.

## Established theorem first

Cook and Reckhow (1979) define a propositional proof system as a polynomial-time verifiable proof relation (equivalently, a polynomial-time function whose range is TAUT). Such a system is **polynomially bounded** if every theorem has a proof of length polynomial in the theorem length. Their theorem is

`there exists a polynomially bounded propositional proof system iff NP=coNP`.

Therefore `SAT in P` implies that at least one polynomially bounded proof system exists. This is an existential statement over proof systems. It does **not** say that the already-fixed `Rmix341` is polynomially bounded.

That missing change of quantifiers is the B3 transfer gap.

## The weakest exact B3 transfer

Assume one fixed uniform total correct polynomial-time SAT decider `A`. Define the CNF-UNSAT proof relation `D_A` as follows:

1. the statement is an explicit CNF string `F`;
2. the proof contains a literal copy of `F` (equivalently, an empty auxiliary certificate paired with the statement);
3. the verifier rejects malformed strings or a nonidentical copy and otherwise accepts exactly when `A(F)=UNSAT`.

Under the external assumption that `A` is total and correct, `D_A` is sound and complete. Its proofs have `O(|F|)` bits and its verifier runs in polynomial time. A rejecting trace alone does not establish soundness: soundness uses the quantified premise that `A` is correct on all valid SAT, UNSAT, and malformed inputs.

For the fixed target calculus `R`, define **length simulation** of `D_A` by

`W_R(F) <= p_A(|F| + |proof_DA(F)|)`

for every valid UNSAT `F` and one polynomial `p_A`. Since `|proof_DA(F)|=O(|F|)`, this is equivalent to

`Wbar_R(N) <= N^O(1)`.

Consequently, under a fixed correct polynomial-time `A`, B3 for `R` is exactly the existence of this length simulation. This is the weakest after-the-fact requirement: it asserts short `R` proofs but need not compute them.

Standard **p-simulation** is stronger. It requires a uniform polynomial-time translator that takes a `D_A` proof and emits an `R` proof. Such a translator would address proof acquisition and moves toward B1; B3 alone does not require it. Likewise, a p-optimal proof system would suffice because it simulates every Cook--Reckhow system, but existence of p-optimal systems is itself open and is far stronger than the required one-system length domination.

## Exact countercontrol: effective proof systems need not be polynomially bounded

Define one fixed truth-table CNF refutation system `TT`:

- a proof contains one paid record for every assignment to the `v` variables, in canonical order;
- each record names an original clause falsified by that assignment;
- the verifier checks record count, canonical coverage, clause indices, and falsification locally.

`TT` is sound, complete, and effective. It has no semantic oracle and no one-step contradiction rule. Every `v`-variable UNSAT CNF has a proof, while a SAT CNF fails at its satisfying assignment. Verification takes `poly(|F|+|pi|)` time.

By the fixed grammar, every accepted proof has exactly `2^v` paid records. On

`U_v = AND_{i=1}^v ((x_i) AND (not x_i))`,

the input encoding has `N_v=Theta(v log v)` bits but

`W_TT(U_v)=2^v=exp(Omega(N_v/log N_v))`.

Thus the proposed general lemma

`sound + complete + effective verification => polynomially bounded`

is false. The simple family is not offered as a hard `Rmix341` family; it is only a transfer countercontrol showing that the structural properties already proved for `Rmix341` cannot supply B3 without using the `SAT in P` premise through a genuine length-simulation argument.

There is also a relativization warning. With a PSPACE-complete oracle such as TQBF, `P^O=NP^O=PSPACE`, while the syntactic `TT` minimum remains exponential. Hence no proof that relativizes and uses only generic proof-system properties can establish the universal claim that every sound complete effective system satisfies B3. This does not decide unrelativized B3 for the particular `Rmix341`.

## Four falsifiers

1. **Cook--Reckhow plus `SAT in P` makes every fixed proof system polynomially bounded.** **FALSIFIED as a general transfer rule:** the theorem guarantees existence of some system, not boundedness of an arbitrary preselected one.
2. **Soundness, completeness, and polynomial-time checking supply the missing transfer.** **FALSIFIED:** `TT` has all three properties and exponential minimum cost.
3. **B3 requires an efficient proof translator.** **FALSIFIED:** after-the-fact length simulation is sufficient and strictly weaker; optimizer discovery remains free.
4. **A rejecting computation trace makes `D_A` sound.** **FALSIFIED:** it shows what `A` did, not that `A` is correct; the external universal correctness premise is indispensable.

## Independent exact controls

The Python producer and no-import Node verifier reconstructed `U_v` and paired SAT formulas `S_v=AND_i(x_i)` for `1<=v<=12`.

- all 12 `U_v` instances were UNSAT;
- all 12 paired controls were SAT;
- exact accepted `TT` proof sizes were `2^v`, through 4,096 records at `v=12`;
- 8,190 truth-table records were generated, checked, and independently rebuilt;
- finite `D_A` stand-ins accepted exact UNSAT statement copies and rejected the SAT copies;
- ten malformed/corrupt truth-table proofs and three malformed decider-system records were rejected;
- the independent verifier made 72 assertions.

This finite brute-force decider is only a control for the proof-relation grammar. It is not the hypothetical polynomial-time `A` and is not evidence for B3.

Raw SHA-256: `c5ae854b90d72b7df37c63cb299ffc683a888e7f6c1cdded129134ee752d31c0`.

## B1/B2/B3 classification

| Obligation | Status | Exact reason |
|---|---|---|
| B3 equivalence to `D_A` length simulation, under fixed correct P-time `A` | **PROVED/CONDITIONAL** | Both statements reduce to one polynomial bound on `W_R(F)` because `D_A` proofs have linear length. |
| Standard p-simulation `D_A -> Rmix341` | **OPEN and stronger than needed** | No uniform proof translator is known. |
| B1 pointwise | **OPEN** | No computation-to-proof producer for every total correct SAT decider was supplied. |
| B2 worst-case | **OPEN** | No arbitrary-decider worst-case domination was established. |
| B3 for `Rmix341` | **OPEN** | The necessary length simulation into the same fixed calculus remains exactly the missing theorem. |
| Superpolynomial `Wbar_Rmix341` | **OPEN** | `TT` is a meta countercontrol, not the target calculus. |

The result does not reverse any simulation inequality and does not turn NP-completeness, empirical hardness, or a restricted proof lower bound into SAT time.

## Grok, Claude, and peer review

The actual repository folders `GROKPROOF/`, `research/agents/grok/`, and `research/agents/claude/` were checked again. Exact default-branch versions relevant to the transfer question were:

| Path | Blob SHA | Assessment |
|---|---|---|
| `GROKPROOF/2026-11-03_1217_PROGRESS.md` | `acf9fbee7079af567db4847ce628c49da45c25b1` | The query-volume proof still reverses `T_A(M)<=M^K` into a per-query lower bound. It supplies neither length simulation nor B3. |
| `GROKPROOF/2026-11-03_1518_PROGRESS.md` | `234fc189b01fa163eb10e128556e9d22e085b755` | Explicitly leaves the universal charged transformation open. |
| `GROKPROOF/2026-11-02_2045_ATTEMPT_ARC_CONSTRUCTION.md` | `130939f5d75a6b31a54f45455e7c271051fcbdc4` | Correctly records the all-input construction as open. |
| `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex` | `b7150bb9ed964affd5fb90ecd24b0aa35d600bf9` | Scoped alternation-trading barrier; no Cook--Reckhow-to-`Rmix341` simulation. |
| `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` | `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a` | Sequential-input theorem, not indexed B3. |
| `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` | `79e4d4e7e0e3edff3aba8610852c45534bdde128` | Conditional ledger; no same-fixed-calculus simulation. |
| `research/agents/claude/2026-09-30_CLAUDE-0266_review.tex` | `694c1c8169d9a193397b94e6ee572c476e639a94` | Identifies formula-invariant and citation failures; carries the transport certificate as open. |

Current peers were also checked: `research/coordination/2026-11-03_0905_LSPV1_BVP_ALGEBRAIC_NONPROJECTION366_FIVE_ROLE_HANDOFF.md` at blob `f9d9a9643eac2ec185a8924b8d7d304d970a90f8`; `research/agents/lspv-2/2026-11-03_0912_LSPV-2_SCOPE_PROFILE_TRANSFER366.tex` at `fafa532ff9f7cfd9b36cfae35efec95c4f8024b5`; and `research/agents/lspv-3/2026-11-03_0924_LSPV-3_BRAUN_BACKTRANSLATION_BLOWUP369.tex` at `1cd0e44902535cb460444b718bbcfb04361d47bd`. They supply restricted scope tradeoffs or nonprojection results, not B3.

## Literature and GitHub searches

Queries covered the Cook--Reckhow polynomial-boundedness equivalence, p-simulation and p-optimal proof systems, proof search, project B3/decider simulation work, and scoped `github.com/openai` proof-system implementations.

- S. Cook and R. Reckhow, [The Relative Efficiency of Propositional Proof Systems](https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf), JSL 44 (1979), supplies the established equivalence and relative simulation framework.
- J. Krajicek and P. Pudlak, [Propositional proof systems, the consistency of first order theories and the complexity of computations](https://doi.org/10.2307/2274765), JSL 54 (1989), relates optimal proof systems to broader open structural questions.
- P. Pudlak, [The Lengths of Proofs](https://users.math.cas.cz/~pudlak/length.pdf), Section 10.4, states the optimal-system formulation explicitly.
- J. Krajicek, [Information in propositional proofs and algorithmic proof search](https://eccc.weizmann.ac.il/report/2021/053/), separates proof length from proof-search information and notes the connection to p-optimal systems.

Project search found the peer reports above. OpenAI GitHub search found no applicable `Rmix341` length-simulation theorem; one unrelated truth-table/verifier match was discarded. Absence is not novelty evidence.

## Work and all-phase space ledger

| Phase | Measured record |
|---|---:|
| Python producer wall time | 0.035962951 s |
| Python producer peak host RSS | 11,392 KiB |
| Node verifier wall time | 0.015011131 s |
| Node verifier peak host RSS | 45,752 KiB |
| Truth-table records checked/rebuilt | 8,190 |
| Producer source bytes | 9,099 |
| Verifier source bytes | 3,806 |
| Raw JSON bytes | 4,902 |

These host measurements are not FLMV bounds. Parsing, formula validation, enumeration, statement-copy checking, record validation, serialization, and independent replay were charged. Optimizer discovery remains intentionally absent from `W_R`. The all-phase envelope remains `s'<=max{rho,eta,lambda,lambda*s}`. XOR state differences are irrelevant to this proof-relation theorem and were not treated as a free oracle.

## Artifacts and next exact gap

- Producer: `experiments/arc/lspv5_317/cook_reckhow_b3_transfer_referee317.py`
- Independent verifier: `experiments/arc/lspv5_317/verify_cook_reckhow_b3_transfer_referee317.js`
- Raw ledger: `results/raw/arc/lspv5_317/cook_reckhow_b3_transfer_referee317.json`
- Five-role handoff: `research/coordination/2026-11-03_0948_LSPV5_TO_FIVE_ROLE_COOK-RECKHOW-B3-TRANSFER-REFEREE317.md`

The next transfer target is precise: under an assumed correct polynomial-time SAT decider, prove nonuniform polynomial **length domination** from `D_A` into the same fixed `Rmix341`. Do not demand an efficient translator unless pursuing B1, and do not replace this statement with existence of some other polynomially bounded proof system.

**P versus NP remains OPEN.**
