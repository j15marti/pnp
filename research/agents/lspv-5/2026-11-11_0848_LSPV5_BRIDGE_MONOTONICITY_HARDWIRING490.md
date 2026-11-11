<!-- LSPV-5 REPORT::BRIDGE-MONOTONICITY-HARDWIRING490::2026-11-11T08:48:00-08:00 -->
# LSPV-5/490: the pointwise bridge B1 fails by hardwiring, and B3 is P ≠ NP itself for every already-lower-bounded system

**Role:** LSPV-5, Independent Proof Red Team (:48, historical Route B)
**Timestamp:** 2026-11-11 08:48 PST (America/Los_Angeles)
**Shared objective:** the worst-case minimum derivation cost
$\overline W_R(N)=\max_{F\in\mathrm{UNSAT},|\langle F\rangle|\le N}\min_{\pi:F\vdash_R\bot}\mathrm{cost}_R(\pi)$
and the primary bridge B3: $\mathrm{SAT}\in\mathrm P\Rightarrow\overline W_R(N)\le\mathrm{poly}(N)$ ([P2-B2]).

**Status summary:**
- Theorems 1–3 are **PROVED/EXACT**. They are short logic and diagonal-style arguments.
- Corollary 4 is **KNOWN THEOREM plus PROVED/EXACT**: B1 is **FALSIFIED/RETIRED** for Resolution, Cutting Planes and bounded-depth Frege.
- Corollary 5 is **CONDITIONAL** on the exact form of Krajíček–Pudlák.
- The finite PHP control is **COMPUTATIONAL**.
- [P2-D1], [P2-C3], [P2-B1], [P2-B2]/B3 and P versus NP remain **OPEN**.

## 1. Target and falsifiers

The red-team task is to look for failures of the proposed transfer theorems. I set two falsifiers before starting:

- **(F1)** A legal, total, correct SAT decider $A$ whose runtime on some UNSAT family is polynomial while $W_R$ on that family is superpolynomial. This would refute the pointwise bridge B1 for $R$.
- **(F2)** A demonstration that, for a fixed $R$, proving B3 is no easier than proving P ≠ NP. This would refute the framing of B3 as the "weak" arrow.

The user's methodological point stands and is not attacked. Taking the minimum over all valid derivation sequences, with free knowledge of the best one, is a legitimate lower-bound measure. Search cost is correctly left uncharged. What is attacked below is only the *transfer* from $\overline W_R$ to arbitrary algorithms.

## 2. Results

Throughout, $R$ is a fixed sound and complete refutation system with an instance-independent cost.
- $\mathrm{LB}(R)$ means "$\overline W_R$ is superpolynomial".
- $\mathrm{B3}(R)$ means "$\mathrm{SAT}\in\mathrm P\Rightarrow\overline W_R\le\mathrm{poly}$".
- $\mathrm{B1}(R)$ means: for every total correct $A$ there is a polynomial $p_A$ such that $W_R(F)\le p_A(|F|+T_A(F))$ for all UNSAT $F$.

### Theorem 1 (logical form of B3) — PROVED/EXACT

$\mathrm{B3}(R)\iff(\mathrm{SAT}\notin\mathrm P)\vee\neg\mathrm{LB}(R)$.

So whenever $\mathrm{LB}(R)$ is a known theorem, $\mathrm{B3}(R)\iff\mathrm{SAT}\notin\mathrm P\iff\mathrm P\ne\mathrm{NP}$.

*Proof.* This is material implication. When $\neg\mathrm{LB}(R)$ is false, the right-hand side reduces to $\mathrm{SAT}\notin\mathrm P$. ∎

**Consequence.** Take any $R$ with a published superpolynomial lower bound: Resolution, Cutting Planes, bounded-depth Frege, or Polynomial Calculus in its scoped models. For such $R$, a proof of B3 *is* a proof of P ≠ NP. It is not a weaker intermediate step.

So the "weakest sufficient bridge" is weaker than P ≠ NP only for systems whose lower bound is itself open. This red-teams the allocation; it is not a reason to abandon the route.

### Theorem 2 (monotonicity under simulation) — PROVED/EXACT

Suppose $R'$ cost-simulates $R$: there is a polynomial $q$ with $W_{R'}(F)\le q(|F|+W_R(F))$ for every UNSAT $F$. Then:
- $\mathrm{B3}(R)\Rightarrow\mathrm{B3}(R')$, and
- $\mathrm{LB}(R')\Rightarrow\mathrm{LB}(R)$.

*Proof.* Under SAT ∈ P, $\overline W_R\le$ poly, so $\overline W_{R'}(N)\le q(N+\mathrm{poly}(N))$. The second implication is the contrapositive of the same inequality. ∎

**Consequence.** Choosing the system is a strict trade-off. Strengthening $R$ (adding paid definitions, GF(2), AND3, LOCAL-CONVERT) makes B3 easier and $\mathrm{LB}(R)$ harder. Weakening $R$ does the opposite.

If historical $R_{\mathrm{mix341}}$ cost-simulates Extended Resolution, which is plausible given its paid auxiliary definitions, then $\mathrm{LB}(R_{\mathrm{mix341}})$ implies a superpolynomial ER/EF lower bound. That has been open since Cook–Reckhow (1979). This premise is **CANDIDATE**: it depends on [P2-D1] grammar authentication.

### Theorem 3 (uniform hardwiring) — PROVED/EXACT

Suppose cost is at least 1 per inference node, and $\mathrm{B1}(R)$ holds. Let $n\mapsto F_n$ be any polynomial-time computable sequence of UNSAT CNFs with $|F_n|\ge n$. Then $W_R(F_n)\le\mathrm{poly}(|F_n|)$.

*Proof.* Define the decider $A_{\mathrm{hw}}$ on input $x$:
1. For $n=1,2,\dots$, generate $F_n$ while $|F_n|\le|x|$, and output UNSAT if $x=F_n$.
2. Otherwise decide $x$ by brute force (handling malformed input as well).

$A_{\mathrm{hw}}$ is one fixed program, total and correct on all inputs. Step 1 costs $\sum_{n\le|x|}\mathrm{poly}(n)=\mathrm{poly}(|x|)$, so $T_{A_{\mathrm{hw}}}(F_n)\le\mathrm{poly}(|F_n|)$. Applying B1 with $A=A_{\mathrm{hw}}$ gives the claim. ∎

$A_{\mathrm{hw}}$ uses no oracle, no nonuniform advice and no promise. Its worst-case runtime $T^{wc}$ is exponential, which is why the argument says nothing about B2 or B3.

### Corollary 4 (B1 falsified for weak systems) — KNOWN THEOREM + PROVED/EXACT; B1 FALSIFIED/RETIRED

Each of the following has an explicit, polynomial-time constructible UNSAT family with superpolynomial minimum proof size:

| System | Hard family | Source |
|---|---|---|
| DAG Resolution | $\mathrm{PHP}^{n+1}_n$ | Haken 1985 |
| DAG Resolution | expander Tseitin | Urquhart 1987 |
| Cutting Planes | clique–colouring | Pudlák 1997 |
| bounded-depth Frege | PHP | Ajtai 1988; Krajíček–Pudlák–Woods 1995; Pitassi–Beame–Impagliazzo 1993 |

Each proof line has polynomially many symbols, so the node count is polynomially related to proof size. By Theorem 3, **B1 is false for each of these systems**.

The same holds for any fragment of $R_{\mathrm{mix341}}$ that is cost-equivalent to one of them, such as a RES-only normal form. That fragment claim is **CONDITIONAL** on the fragment equivalence.

B1 survives only for systems strong enough to have short proofs of every polynomial-time constructible UNSAT sequence.

### Corollary 5 (B1 forces an optimal proof system) — CONDITIONAL

The cited source attributes the following result to Krajíček–Pudlák: a system $Q$ is non-optimal iff some polynomial-time algorithm outputs tautologies hard for $Q$ (Monroe, arXiv:1212.1789; Beyersdorff–Köbler–Messner, TCS 2009). Assume that statement in its exact length-based form. Also assume $R$-proofs have length polynomial in $W_R$; that link is open per [P2-D3] for $R_{\mathrm{mix341}}$.

Then $\mathrm{B1}(R)$ for any $R$ implies that $R$ is an optimal proof system.

Optimal proof systems are not known to exist; non-existence would give NE ≠ coNE. So B1 for *any* fixed system is at least as strong as an unresolved structural conjecture. This status is **CONDITIONAL**: the literature statement must be checked against its exact quantifiers ("hard" meaning infinitely often superpolynomial) before promotion.

### What survives

- **B2** ($\forall A$: $\overline W_R\le\mathrm{poly}(N+T_A^{wc}(N))$) is untouched by hardwiring, because hardwired deciders have exponential $T^{wc}$.
- **B3** is untouched in truth value. Its difficulty is pinned by Theorem 1.

The only known non-vacuous bridge-type theorem remains Cook (1975): if a SAT algorithm's correctness is PV-provable, then EF has polynomial-size refutations. This is already recorded as LSPV-1/357. It concerns EF, not $R_{\mathrm{mix341}}$, and provability is an extra hypothesis.

Pipatsrisawat–Darwiche (2011) and Beame–Kautz–Sabharwal (2004) give the correct positive scope of the user's strategy. A $\overline W_{\mathrm{Res}}$ lower bound is an unconditional lower bound for CDCL-type algorithms, whose runs are Resolution derivations. It is not a lower bound for arbitrary algorithms.

## 3. COMPUTATIONAL control

`experiments/review/lspv5_490_uniform_hardwiring_b1_audit.py` ran in 2.4 s, with 3,007 assertions passing.

- $A_{\mathrm{hw}}$ (hardwired $\mathrm{PHP}^{n+1}_n$ recognition, brute-force fallback) agreed with brute force on 3,000 random CNFs and on one hostile near-miss: PHP$_2$ with its last clause removed.
- Exact minimum tree-like Resolution size, via a falsified-clause decision-tree DP, was compared with $A_{\mathrm{hw}}$'s charged step count:

| $n$ | variables | clauses | chars | $A_{\mathrm{hw}}$ steps | minimum tree-Res nodes |
|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 3 | 9 | 18 | 5 |
| 2 | 6 | 9 | 47 | 103 | 21 |
| 3 | 12 | 22 | 143 | 342 | 85 |

At these sizes $A_{\mathrm{hw}}$ is *slower* than the minimum proof. Finite data shows nothing asymptotic: the separation in Corollary 4 rests entirely on the cited known theorems. The control only checks the totality and correctness of the hardwired decider.

Raw output: `results/raw/review/2026-11-11_0848_LSPV5_490_UNIFORM_HARDWIRING_RAW.json`.

## 4. Literature preflight and barrier transfer

**Obstacles addressed:**
1. The non-circular same-$R$ bridge B3.
2. The strength trade-off in choosing $R$.

**Sources checked this run:**
- Krajíček–Pudlák hard-sequence and optimality characterisation, as stated in Monroe, arXiv:1212.1789.
- Beyersdorff–Köbler–Messner, TCS 2009.
- Köbler–Messner–Torán, ECCC 2009.
- Alekseev, Theory of Computing 22 (2026): a lower bound for Polynomial Calculus with extension. That system simulates EF only in a restricted algebraic setting. This is **not** an EF lower bound and does not transfer to $R_{\mathrm{mix341}}$ without an exact simulation.
- ECCC 2026/109 (provable TFNP reductions over EF): EF-provable membership in FP yields systems polynomially equivalent to EF. This is an ANALOGY to the Cook-1975 bridge, needing a SAT-specific instance.
- Arteche–Khaniki–de Rezende, arXiv:2506.16956: EF proves that automating Resolution is NP-hard. This is consistent with the user's point that search cost must not be charged to the minimum.

**Transfer classification:**
- Cook-1975 / ECCC-2026-109: EXACT THEOREM TRANSFER *for EF only*, under a provability hypothesis.
- K–P optimality: EXACT TRANSFER to B1 (Corollary 5, conditional on exact form).
- Topology / knot–link handoff (2026-11-09): FAILED TRANSFER as a bridge, because NP-hardness of a link problem is not a machine lower bound. Consistent with that handoff.
- Post-quantum ledger items 1–7: not relevant this run. Hardwiring is a uniformity argument, not an algebraic invariant.

## CORPUS REVIEWED

- AGENTS.md (including the 2026-11-09 knot/link and world-ledger notes) and `proof1.txt` in full.
- `proof2.txt`: header, D1–D3, Route A, B1–B9, and the newest L1/L5 entries.
- The 2026-11-02 worst-case refocus directive.
- LSPV-1/357 (Gödel/PV reflection), LSPV-1/462 (R_clock), LSPV-1/466 (compact-witness B3).
- LSPV-5/489 and this cycle's commits from LSPV-1/574, LSPV-2/559, LSPV-3/572 and LSPV-4/545.
- The `main.tex` executive header and ownership markers.

## DUPLICATION / CONTRADICTION AUDIT

These are already in the corpus and are only reused here:
- B4 (B1 ∧ B2 ⇒ P ≠ NP).
- R_clock ([P2-B6]): B3 fails for an artificial system.
- PV reflection (357).

New in this report:
- the explicit Theorem 1 equivalence for known-lower-bound systems;
- the monotonicity trade-off (Theorem 2);
- the hardwiring falsification of **pointwise B1** (Theorem 3 and Corollary 4);
- the B1 ⇒ optimality link (Corollary 5).

Repository search found "p-optimality would also suffice" for B3 at proof2.txt:266. That is the converse direction and does not overlap. No contradictions found.

## WHAT CHANGED RELATIVE TO ROOT MAIN

- B1, the "stronger optional pointwise simulation" in the 11-02 directive, is downgraded from OPEN to **FALSIFIED/RETIRED** for Resolution, Cutting Planes and bounded-depth Frege.
- B1 for $R_{\mathrm{mix341}}$ is reclassified: it implies R is p-bounded on every polynomial-time constructible sequence. For a RES-equivalent fragment it is FALSIFIED.
- B3 for already-lower-bounded systems is identified with P ≠ NP.

## ADOPTED / REJECTED / RETIRED PRIOR COMPONENTS

- **Adopted:** the uncharged-search inner minimum (the user's clarification) and the PV bridge (LSPV-1/357) as the only known positive bridge.
- **Retired:** pointwise B1 for any system with an explicit polynomial-time constructible hard family.
- **Rejected:** describing B3 as "weaker than P ≠ NP" without naming $R$'s lower-bound status.

## STALE OR OVERSTATED CLAIMS FOUND

- The 11-02 directive's phrasing "B1 … stronger optional" omits that B1 is already false for the systems where lower bounds are known. Recommended wording: "B1 is false for every R lacking short proofs of all P-constructible UNSAT sequences."
- **Predecessor check:** LSPV-4/545 has verified pushed code and raw data (commits `1e6b51d7`–`baf307df`, 08:43–08:45 PST). Its report was not yet present at 08:49, and its run window was still open, so no retry was issued. The next agent should re-check.

**Trackers:** proof2.txt updated with [P2-L5-490]. proof1.txt reviewed with no material change.

**Next exact target:** settle the exact quantifier form of Krajíček–Pudlák for Corollary 5. Then decide via [P2-D1] whether $R_{\mathrm{mix341}}$ cost-simulates ER. If it does, B1(R_mix341) is equivalent to an open optimal-proof-system question, and LB(R_mix341) is equivalent in difficulty to an EF lower bound.

P versus NP remains **OPEN**.

<!-- END_OF_VERIFIED_REPORT::LSPV-5::BRIDGE-MONOTONICITY-HARDWIRING490 -->
