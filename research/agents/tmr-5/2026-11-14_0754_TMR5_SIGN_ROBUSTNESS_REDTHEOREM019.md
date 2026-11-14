# TMR-5/019: independent polarity-sensitivity audit, exact Hamming robustness, and block-sensitivity falsifier

**Pacific timestamp:** November 14, 2026, 07:54 PST (America/Los_Angeles). **Role:** TMR-5, NEW machine bottleneck redteam / canonical synthesis. **Repository:** j15marti/pnp, main.

**Peer result:** TMR-2/021 SCB21 receives favorable INDEPENDENT SYMBOLIC REVIEW at PROVED/RESTRICTED scope, with a separately implemented truth-table audit. **New TMR5-RSB19:** CANDIDATE/RESTRICTED, pending TMR-2 or TMR-1 independent mathematical review. **Finite experiments:** COMPUTATIONAL. **Unrestricted all-machine superpolynomial 3-SAT bound and P versus NP:** OPEN.

## 1. Exact source model and independent peer audit

Fix proper three-distinct-variable clauses with an explicit sign bit for every literal occurrence. Legal single-bit mutations invert one sign without changing clause identity, variable IDs, clause count, or encoded length. The full legal length L includes all headers and IDs; for the deliberately fixed-variable E3 sign stream, L=3m. One fixed finite total deterministic multitape decider applies across all L, with every source scan, work cell, reread and output transition charged.

For a clause occurrence C_i in F, write H_i=F with that one occurrence deleted and C_i^(j) for negation of its jth literal. I independently checked the two directions of TMR-2/021's proof:

* If F is UNSAT, H_i UNSAT implies no single sign mutation can help, whereas H_i SAT implies **all three** mutations make F SAT. Any H_i-model falsifies C_i, hence each negated literal in turn becomes true. Thus s(F)=3e(F), where e counts deletion-essential *occurrences*.
* If F is SAT, H_i is SAT and the jth mutation makes F UNSAT exactly when **every H_i-model** has original literal j true and the other two original literals false. Therefore at most one literal sign per SAT clause is pivotal, s(F)<=m, and such a clause is logically entailed by H_i. These are **complete-source valid edits**, not online-continuation premises.

Distinct essential UNSAT occurrences have distinct satisfying H_i witnesses. Therefore e(F)<=min(m,2^n,8 binom(n,3)); these are structural counts, not compulsory runtime. The peer's stated theorem survives this independent proof check. Its original published report, source and raw evidence were inspected; the new audit below uses an independently written evaluator, not the peer's masks implementation.

## 2. New exact all-r counterexample: isolated UNSAT input with zero single-bit sensitivity

Use the fixed-variable three-bit-per-clause E3 language. There are exactly eight clause signatures sigma in {0,1}^3. Clause C_sigma excludes **only** assignment sigma. For any integer r>=1 let

$$
U_r=\bigwedge_{\sigma\in\{0,1\}^3}\bigwedge_{j=1}^{r} C_{\sigma}, \qquad L=24r.
$$

All eight forbidden assignments occur, so U_r is UNSAT. Define the legal polarity Hamming distance d(U_r,SAT) as the smallest number of original sign positions that must be inverted to obtain a SAT formula of **the same m occurrences and fixed variable IDs**.

**TMR5-RSB19, exact candidate theorem, with complete elementary proof:**

$$
\boxed{d(U_r,\mathrm{SAT})=r,\quad
\#\{\text{SAT formulas at exactly distance }r\}=8\cdot3^r.}
$$

To make U_r SAT, at least one forbidden signature must disappear entirely. Each of the r original occurrences of that signature must have a sign bit changed, giving distance >=r. Conversely, choose one of eight signatures and invert exactly one of the three bits in **each** of its r occurrences, preserving all other occurrences; the chosen signature disappears, giving SAT at exactly r edits. At distance r, no edits can be spent elsewhere or twice on one occurrence. Thus there are precisely 8*3^r nearest SAT sign strings.

In particular, for r>=2 every single-bit neighbor remains UNSAT:

$$
\boxed{s(U_r)=0\quad(r\ge2),\qquad d(U_r,\mathrm{SAT})=L/24.}
$$

**Exact block sensitivity:** A sensitive block is a set of sign coordinates whose simultaneous flipping changes the decision, and distinct blocks must be disjoint. For each of eight signatures, choose the r coordinates corresponding to one fixed literal in all r of its occurrences. Flipping that block deletes the signature and yields SAT, producing eight pairwise disjoint sensitive blocks. Conversely, any label-changing block must modify at least r positions, and there are 24r total positions, so there are at most floor(24r/r)=24 blocks by this crude count. A **sharper** bound is eight: any SAT-producing block must touch every one of the r occurrences of at least one of eight original signatures. Charge a distinct complete signature group to each disjoint sensitive block; two disjoint blocks cannot both delete the same group's all-r occurrences. Hence bs(U_r)=8 for all r>=1.

Here the single-bit sensitivity is zero for r>=2, yet eight disjoint simultaneous-edit blocks remain decisive. This falsifies any claim that a complete valid-label adversary can be characterized by the pivotal **individual** bits alone. It does **not** refute TMR-2/021, whose claim is explicitly about individual polarity bits.

**A 24-bit negative certificate:** Reading the three signs of one recorded occurrence of each of the eight signatures suffices to verify UNSAT for this particular U_r, in an unrestricted addressable bit-query model. This certificate is constant-size as r grows even though d(U_r,SAT)=Theta(L). On a physically sequential source tape, moving to the far-away occurrence still costs transitions. Certificate size is not an unrestricted machine-time lower bound.

## 3. Independent experiment and honest correction trail

An **independently written** pure JavaScript truth-table evaluator was executed directly under hosted V8, NOT native Node, on 2,232 generated proper-3CNF formulas with 3..6 variables and 1..18 clauses, spanning both labels. Each individual sign mutation was checked against complete assignment enumeration and independently evaluated H_i-model entailment. The run checked **63,612** valid sign mutations: 237 UNSAT and 1,995 SAT base formulas, 2,400 pivotal UNSAT flips, 1,576 pivotal SAT flips, and 87,198 assertions with zero failures. Tests included Horn patterns, shared duplicated clauses, disjoint products on six variables, variable renaming, XOR-style clause patterns, explicit even-parity XOR3 full assignment checks, proper-3CNF lifting of a two-literal clause with an auxiliary variable, and repeated-clause padding.

Separate exhaustive all-sign-bit Hamming layers for U_1, U_2, U_3 evaluated 63,471 mutated formulas; SAT counts were respectively 24 at distance 1, 72 at distance 2 and 216 at distance 3, with zero SAT configurations at smaller distances. Eight disjoint blocks for each r and the zero individual sensitivity for r>=2 were checked.

**Failed test control preserved:** The first published draft used low LCG bits for polarity choices. It accidentally generated zero UNSAT random fixtures and zero pivotal random mutations, despite passing its local assertions. It is NOT adequate both-label evidence. That original source/raw pair and an intermediate correction remain published unchanged as an audit trail. The **FINAL** executed source switches to higher PRNG bits, supplies explicit SAT/UNSAT families and exact algebraic controls, and fixes the raw metadata. Cite ONLY this final pair for the 2,232/63,612/87,198 counts.

* FINAL executed source: `experiments/tmr/tmr5_sign_robustness019_final.cjs`, Git blob `597752e5f35a5162ffea1fad1f760471398f3a16`.
* FINAL immutable raw: `results/raw/tmr/2026-11-14_0755_TMR5_SIGN_ROBUSTNESS019_FINAL_RAW.json`, Git blob `fd2e6f9474b3d054fc6a071d4398d7b95dd1745b`.
* Historical undercovered first source/raw: `experiments/tmr/tmr5_sign_robustness019.cjs`; `results/raw/tmr/2026-11-14_0750_TMR5_SIGN_ROBUSTNESS019_RAW.json`.
* Historical intermediate correction: `experiments/tmr/tmr5_sign_robustness019_corrected.cjs`; `results/raw/tmr/2026-11-14_0752_TMR5_SIGN_ROBUSTNESS019_CORRECTED_RAW.json`.

The exact FINAL code was executed via V8 Function on the unchanged code body with its stdout expression replaced solely by `return audit()`; the identical program and raw data were published and read back. No OS-native execution, general-TM compiler, LaTeX compile, or asymptotic brute-force claim is made. The symbolic theorem, not finite testing, establishes the stated all-r result.

## 4. Uniform-machine counteralgorithm and transfer audit

One fixed finite-state E3 classifier reads each three-bit signature in one locally moving input scan, ORs its corresponding bit into an eight-bit finite-control mask, then outputs UNSAT iff the mask equals 255. For proper three-variable sign streams this costs O(L) transitions and O(1) writable cells. It decides U_r and all its legal polarity neighbors, for every r, without computing Hamming distance, block sensitivity, deletion-essential clauses or assignment histories. On the unrestricted 3-SAT encoding, one **fixed** total correct general decider can branch on the recognized E3 sublanguage and otherwise use charged exhaustive search. Its cost on E3 is polynomial while the general worst case is not thereby polynomial.

Thus large legal distance from SAT, a highly redundant UNSAT representation, block sensitivity, and every fixed-size sensitivity measure fail to force superlinear semantic cost on this family. Arbitrary input rereading, sharing and compact finite-control masks are legal. No oracle, nonuniform per-length program or memory-for-time substitution was used.

TMR-3/020's **hybrid INDEX** lemma is a separate correct-looking restricted all-query statement; this report does NOT claim independent full proof of its physical model. Even a future verified delayed-INDEX locality lower bound only imposes linear retrieval cost on a distinct two-phase service, not the all-exponent cost of deciding arbitrary SAT. TMR-4/021's cached/head factor results are certified optional exact abstractions, not coverage of every deterministic decider. TMR-1/021 correctly distinguishes sensing from nonsensing heads.

## 5. Integrated dependency and epistemic status

The strongest surviving mathematical implications are (a) complete-source valid polarity edits force scans of individually pivotal bits for any correct source-local deterministic decider; (b) scoped delayed INDEX services have substantial physical local-access costs; (c) certified whole-tape factor quotients can exactly preserve physical machine cost. None yields the missing **every-correct-A** superpolynomial post-acquisition SAT computation burden.

The exact target remains

$$
\forall A\,\forall k\ge1\,\forall C>0\,\forall L_0\,
\exists F:\quad |F|\ge L_0\ \land\ T_A(F)>C(|F|+1)^k,
$$

where A is one fixed finite total correct uniform general 3-SAT decider on all lengths, and every writable cell and actual source movement is charged. This implication is **OPEN**. Even when S_A(F)<=O(T_A(F)) on the same execution, neither SCB21 nor RSB19 excludes unrestricted polynomial space/time. No P=NP algorithm was produced. Root proof1/proof2 remain **OPEN**.

**Primary references checked:** [1] Nisan, *CREW PRAMs and Decision Trees*, SIAM J. Comput. 20(6):999-1007 (1991), https://doi.org/10.1137/0220062 (block sensitivity defined in an explicitly different computational model); [2] Huang, *Induced subgraphs of hypercubes and a proof of the Sensitivity Conjecture*, Annals of Mathematics 190:949-955 (2019), https://doi.org/10.4007/annals.2019.190.3.6 (global sensitivity-vs-degree result, not a pointwise SAT lower bound); [3] Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6):835-865 (2005), https://doi.org/10.1145/1101821.1101822 (restricted simultaneous random-access time/space regimes; no all-polynomial-space exclusion). No theorem from these papers is imported beyond its verified scope.

**Repository records independently inspected:** current TMR replacement directive, both complete root proof trackers, complete root main.tex via authentic Git blob, issue #3 and latest comments, AGENTS.md, CODEX.md, repo pnp-research skill, five TMR handoffs; original TMR-2/020 and /021 reports, TMR-2/021 exact code and raw; TMR-3/020 report/code/raw; TMR-1/021, TMR-4/021 and TMR-5/018 reports. Historical checker failures were preserved without reopening their superseded work allocation.

**One next target:** Have TMR-2/TMR-1 independently audit the all-r radius, nearest-neighbor count and exact eight-block bound. Then test whether a proposed *global* compulsory SAT processing invariant survives U_r's small negative certificate, XOR Gaussian elimination, bounded-width dynamic programming and an all-input general machine that recognizes these cheap structures. OPEN until an all-machine charged transfer is demonstrated.

END_OF_REPORT::TMR-5::019::2026-11-14_0754_PST
