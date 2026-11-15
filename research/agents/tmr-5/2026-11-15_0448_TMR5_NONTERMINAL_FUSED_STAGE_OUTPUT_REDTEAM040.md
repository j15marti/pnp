# TMR-5/040: Independent M_STAGE replay and a genuine combined nonterminal gate/output fusion tariff

**November 15, 2026, 04:48 PST (America/Los_Angeles).** TMR-5 / PNP Machine Bottleneck Redteam. Governing directive: `research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md`, blob `54c9177fc211dfca6c94d89d6ebbf3f3908809d6`.

**Result:** **PROVED/RESTRICTED**, mathematical peer review **OPEN**, for one newly qualified fixed-port physical multitape *record-and-marker* machine; independent symbolic and finite peer check of TMR-3/043 **PASS/RESTRICTED**. Tests **COMPUTATIONAL**. This is a genuine one-microstep joint discharge, not a SAT computation or proof-system-to-machine transfer. P versus NP remains **OPEN**.

## 1. Candidate and four falsifiers declared before source review

**Candidate:** The independently correct restricted TMR-3/043 activation tariff and TMR-4/043 physical simultaneous-output accounting cannot be assigned their separately maximal prices and then added in a larger physical machine. One authentic *nonterminal* transition can both activate an arbitrarily large staged graph and mark one cell on each of a fixed number of distinct output tapes. The exact joint rule forces a coupled rational tariff. Retain all earlier paid staging and sharing identities.

Predeclared falsifiers: (F1) the joint step writes two cells on one tape, jumps a head, or uses length-dependent control; (F2) the gate records or marker cells were already implicitly charged as if they were written in the joint step, or one is duplicated; (F3) the activation is actually HALT rather than a genuine nonterminal rewrite; (F4) a cross-system calibration is falsely called a contradiction to the original `R_CONN`, `M_STAGE`, or physical literal-copy theorem. The concrete rules below exclude F1-F3; F4 is an explicit **FAILED TRANSFER** only, with the original peer theorems retained.

## 2. Source audit and exact novelty boundary

Read first the fusion directive, then the November 13 TMR replacement directive, `proof1.txt` (28,714 chars; SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`), the **full authentic Git blob** of `proof2.txt` (1,051,196 chars; SHA `930c5eeddafce656717f28055a7a9a755f44737c`), and the **full authentic Git blob** of `main.tex` (2,545,859 chars; SHA `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`). Ordinary GitHub contents reads returned empty bodies for the latter two and were not interpreted as empty files. Reviewed issue #3 and recent comments through TMR-3/043, `AGENTS.md`, `CODEX.md`, the repository pnp-research skill, all five latest handoffs, TMR-1/043 source/matrix, TMR-2/043 nonlinear rank/control and matrix, TMR-3/043 original physical source/code/matrix, TMR-4/043 physical m-port source/matrix, and historical `LEAD-0029` Lipschitz audit.

Relevant primary context: Aho and Ullman, *Optimization of Straight Line Programs*, SIAM Journal on Computing 1(1), 1972, DOI [10.1137/0201002](https://doi.org/10.1137/0201002), emphasizes that the representation and permitted program transformations matter for charged straight-line evaluation. This paper is not asserted to prove the present elementary staging construction. We use the standard fixed-number-of-tapes transition convention: a single machine step can write **at most one cell per tape**, but may simultaneously write on several distinct tapes. No word-RAM unit-cost bulk write or oracle is assumed.

**Prior results preserved, not rediscovered:** TMR-1/043 establishes the unit coefficient for an actual paid fan-in-two APPEND gate in its preauthenticated `R_CONN` calculus. TMR-3/043 gives a real physical nonterminal one-header ACTIVATE discharge of `n-1` in a different staging representation. TMR-4/043 proves simultaneous physical m-port copy tariffs in its different full literal-copy service. **New in /040:** independent physical replay of TMR-3 plus a separately qualified *same-microstep, same-state* AND activation/output collision with a complete exact rational seven-column cone and primal/dual.

## 3. Precise qualified physical machine `M_STAGE_OUTPUT_m`

Fix an integer **m>=1 once for the program**, so the number of tapes and the transition table are finite and independent of input length. For every **n>=2**, give the machine a read-only input tape `1^n#`, one initially blank writable staging tape `W`, and m distinct, initially blank, designated output tapes `O_1,...,O_m`. The input and W heads begin at cell zero; the m output heads remain at their own cell zero. Alphabet on W is `{blank,0,1,g}`, and on each output is `{blank,@}`. The same fixed finite control handles every n. One genuine transition reads its scanned finite tuple, writes at most one symbol on each separate tape, moves each head by at most one cell, and costs **exactly one**, regardless of the number of different tape heads acted on.

The complete authentic successful-source program is:

| Control/rule | Physically genuine work | Next state | Cost |
|---|---|---|---:|
| INIT | Write W[0]=0, advance input and W heads | SECOND | 1 |
| WRITE_GATE | For every subsequent input 1, write one `g` on one W cell and advance both heads | EMIT | 1 each |
| EOF_BACK | Read input `#`, move W head left one cell | BACK | 1 |
| BACK_G | While W scans `g`, move W head left one cell | BACK | 1 each |
| ACTIVATE_AND_MARK | At W[0]=0, write **W[0]=1 AND O_i[0]=@ for every i** in this **one** physical transition; all heads stay | **READY (not HALT)** | 1 |
| HALT | From READY with W[0]=1 and outputs marked, enter HALT, with no writes | HALT | 1 |

The flag is *not* a paid new AND gate; it changes the public interpretation of existing gate records. The `n-1` distinct `g` symbols, paid once each by WRITE_GATE, stand for the implicit position-indexed chain of AND gates `y_2=x_1 AND x_2`, `y_i=y_(i-1) AND x_i`. The qualified record-building **goal** requires the true source `#` to have been inspected, every `g` at W[1]..W[n-1], W[0]=1, the m output markers `@`, and a subsequent true HALT. This is *not* a general circuit-evaluation contract, a 3-CNF decision, or a native Resolution proof. Malformed source behavior is outside this restricted successful-source theorem; a fixed rejecting-sink extension cannot be used to infer SAT complexity.

The complete state retains exact input, fixed program, all control/head/tape contents, paid event and gate identities, and goal status. No authentic physical transition has zero price. Physical `cl_0` is identity and every zero SCC singleton. A separately permitted reversible VIEW alias, if included, may change **only** metadata and preserves every component; no free read, gate write, or output marker is introduced. All AND-like staged records and mandatory output obligations are explicitly retained, and the `m` output markers are on genuinely distinct tapes. Unknown richer machine operations remain conservative MAY and are **not** excluded by this restricted model.

## 4. Exact reduced-product seven-vector and ALL paid transition rows

Define `f(C)=n-1` until header W[0] becomes 1, then zero (the number of disconnected original input vertices in the **activated**, not latent, implicit gate graph minus one). Define `q(C)` as the number of required W[1]..W[n-1] cells that are not the paid `g` symbol, `o(C)` the count of the m output cells not equal to `@`, and `h(C)=1` until true HALT, zero afterward. All four coordinates are nonnegative on every reachable state; every completed goal makes all zero.

$$
\mathbf p(C)=(0,0,0,f(C),q(C),o(C),h(C)).
$$

Exact signed rule-by-component discharge, with canonical columns (CNF, affine, separator, fusion, Gamma, interface, machine):

| Genuine rule | Delta FUS | Delta Gamma | Delta interface | Delta machine | Price |
|---|---:|---:|---:|---:|---:|
| INIT | 0 | 0 | 0 | 0 | 1 |
| WRITE_GATE | 0 | 1 | 0 | 0 | 1 |
| EOF_BACK | 0 | 0 | 0 | 0 | 1 |
| BACK_G | 0 | 0 | 0 | 0 | 1 |
| ACTIVATE_AND_MARK | n-1 | 0 | m | 0 | **1** |
| HALT | 0 | 0 | 0 | 1 | 1 |
| Optional free VIEW/NOP metadata (separate fixture) | 0 | 0 | 0 | 0 | 0 |

The three other columns are identically zero. Note that `q` counts **historically minted physical records**, not an independently necessary abstract tree unfolding. One cost-one ACTIVATE_AND_MARK can discharge `n-1` activated connections **and** m physical outputs while the machine remains nonterminal.

## 5. New exact nonnegative tariff cone and rational primal/dual

Write nonnegative `c=lambda_FUS`, `g=lambda_Gamma`, `a=lambda_interface` and `b=lambda_machine`. Every authentic transition meets the scalar Lipschitz inequality **if and only if**

$$
\boxed{g\le1,\qquad (n-1)c+ma\le1,\qquad b\le1.}
$$

Necessity is witnessed by actual WRITE_GATE, ACTIVATE_AND_MARK and HALT steps, respectively. Sufficiency follows by the COMPLETE six-row inventory, including the genuine positive/zero transition classes. This does not claim feasibility for any other machine's MAY operations. Initial vector

$$
\mathbf p(C_0)=(0,0,0,n-1,n-1,m,1).
$$

The exact rational LP and its matching finite dual are

$$
\max \Phi(C_0)
=\max\{(n-1)c+(n-1)g+ma+b:\ g\le1,\ (n-1)c+ma\le1,\ b\le1\}
=\boxed{n+1}.
$$

A valid rational **primal certificate** is `(c,g,a,b)=(0,1,1/m,1)`; a matching **dual certificate** assigns paid rule multiplicities `y_WRITE=n-1, y_ACTIVATE=1, y_HALT=1`, with total price `n+1`. These numbers cover the initial obstruction vector componentwise, so weak duality is exact. The genuine fixed-machine trace has `1+(n-1)+1+(n-1)+1+1=2n+2` physical steps; the potential gives a valid but nonsharp, linear lower bound. The actual shared records are charged once, and the return-to-flag transitions are not falsely declared free.

**Uniform all-n coefficient firewall:** for one fixed m, requiring the same nonnegative coefficient vector for ALL n>=2 forces `c=0`, since `(n-1)c+ma<=1` for unbounded n. Positive fixed fusion weight is impossible in this qualified physical representation. `g=1,a=1/m,b=1,c=0` remains a uniform certificate with initial `n+1`. Letting m itself grow with n changes the fixed-tape machine model and is forbidden without compilation.

**Smallest genuine joint-row falsifier:** n=2, m=1. Independently admissible single-coordinate calibrations `c=1/(n-1)=1` and `a=1/m=1` would assign the **single genuine nonterminal** ACTIVATE_AND_MARK operation weight `(n-1)c+ma=2>1`. For n=3,m=2 the same overcharge is 2. They cannot be added in this *new* system. This does **not** refute R_CONN, original M_STAGE or literal-copy service, none of which includes this exact joint rule with both obligations.

## 6. Independent TMR-3/043 replay, finite evidence and hostile controls

The independently authored executable reconstructs M_STAGE directly when m=0, without importing the TMR-3 program. It replays the six physical rules and the **original** vector `(f,q,n-r+1[not halted])` for historical rightmost input position r, confirming exact rows: INIT (0,0,1), WRITE_GATE (0,1,1), EOF_BACK (0,0,1), BACK_G (0,0,0), ACTIVATE (n-1,0,0), HALT (0,0,1). Thus TMR-3/043's restricted cone `(n-1)c<=1, a+b<=1` and `2n+2` trace accounting receive **PASS/RESTRICTED independent peer verification**, not a claim of verifying every external simulator or native binary.

**Exactly executed native V8 audit() serialized unchanged** as `experiments/tmr/tmr5_fused_stage_output094.js`. Its immutable direct output is `results/raw/tmr/2026-11-15_0448_TMR5_FUSEDSTAGE094_V8_RAW.json`. Results: **315 complete traces**, **21,420 genuine unit-cost microsteps**, including **63 original M_STAGE replay traces**, **4,284 original typed rows**, **252 joint-shortcut physical traces**, **144,060 exact integer-scaled rational tariff-grid checks**, and **298,603 assertions with zero failures**. All n=2..64, m=0..4 were exhaustively parameter-swept, with exact finite-state deterministic state replay, explicit head and per-tape write-cap assertions. Four separate strict coupled-row negative controls and every postcondition passed. No source randomness; all samples reproducible. These are **COMPUTATIONAL**, not an all-machine proof. Native OS Node, finite-tape compiler binary, full preflight.py/check_research_reports.py and LaTeX were not executed; the symbolic proof above supplies all-n and fixed-m claims.

Controls: a physical multi-output cost-one transition does not imply a free arbitrary circuit macro; the graph can have large semantic support yet only one activated header. A constant-sized header does not make the prior n-1 gate writes unpaid. Horn, Krom, Gaussian/Tseitin, treewidth, autarky, equality, extensions, learning, alternate input representations, rereading, caching and recomputation are **not** declared illegal in unrestricted SAT machines; rather, this unary record-output task makes none of them an obligatory SAT burden. Any future SAT or proof abstraction must preserve genuine simultaneous writes and compact activation as MAY. CEGAR may not delete the authentic joint row. Historical `/341` remains **FAIL** as a full logical UNSAT authority, and `/386` remains **RESTRICTED** to its guarded odd-charge fragment.

## 7. Ranked dependency map and weakest next peer repair

| Dependency | Verdict | Exact scope |
|---|---|---|
| TMR-3/043 actual M_STAGE six-step-row taxonomy and nonterminal activation | **PASS/RESTRICTED** | Independent reconstruction, finite V8 replay plus symbolic row proof |
| TMR-1/043 R_CONN APPEND connectivity theorem | **PASS/RESTRICTED, unmodified** | Only its preauthenticated shared fan-in-two circuit calculus |
| TMR-4/043 fixed-m simultaneous physical outputs | **PASS/RESTRICTED, unmodified** | Only its specified literal-copy service |
| M_STAGE_OUTPUT_m joint authentic nonterminal fusion row | **PROVED/RESTRICTED**, peer review OPEN | One fixed m physical multitape machine, each tape writes at most one cell |
| Exact joint tariff cone / primal-dual `n+1` | **PROVED/RESTRICTED**, peer review OPEN | Qualified record-and-marker goal only |
| Additive independently maximized FUS and output tariffs | **FAIL** | Only when transferred into the newly enriched physical joint system |
| Superpolynomial fusion-safe initial potential on explicit SAT family | **OPEN** | Neither this linear record obligation nor nonlinear matrix rank suffices |
| Same-system transfer covering all correct uniform SAT deciders | **OPEN** | No bridge from record-output task or selected proof grammar |
| Historical checker `/341` and `/386` | **FAIL**, **RESTRICTED** respectively | Prior accepted-language audit scopes maintained |

**Weakest surviving lemma for peers:** Given a proposed dynamic SAT-machine obstruction that charges latent circuit fusions and physical input/output obligations, produce a single uniform (program-sensitive) potential whose exact seven-column tariff remains valid when an arbitrary genuine fixed multitape transition combines several logically distinct discharges. TMR-2 should attempt a nonfactorizing, shortcut-closed SAT component; TMR-3 should provide an actual physical fused operation inventory; TMR-4 should independently replay this joint LP and preserve all MAY paths; TMR-1 must keep same-system SAT transfer independent. A representation-dependent large activated graph does not substitute for a superpolynomial forced processing obligation.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No edits to `proof1.txt`, `proof2.txt`, `main.tex`, legacy historical evidence, user automations, or other agents' ownership regions. P versus NP **OPEN**.
