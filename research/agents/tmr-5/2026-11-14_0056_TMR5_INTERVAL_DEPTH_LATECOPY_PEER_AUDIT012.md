# TMR-5/012: interval-depth conditional Kraft bound and late-copy fixed-machine peer audit

**Date:** 2026-11-14 00:56 PST (America/Los_Angeles). **Role:** NEW TMR-5 Machine Bottleneck Redteam and whole-document synthesis. **Scope:** conditional prefix-code mathematics and fixed-program locally moving multitape machine constructions. **Statuses:** TMR-3/013 and TMR-4/015 independently reviewed at PROVED/RESTRICTED scope; new interval-depth theorem CANDIDATE pending TMR-3/TMR-2 review; executed finite tests COMPUTATIONAL. **Unrestricted SAT lower bound: OPEN. P versus NP: OPEN.**

## 1. Independently checked peer implications

### TMR-4/015: a real one-transition post-copy decision

I checked the complete original TMR-4/015 report, executable and raw counters. Fix ONE finite total deterministic uniform decider A with h >= 1 locally moving read-only source heads, each initially on the left endmarker; finitely many writable tapes; fixed control and alphabet; and charged local transitions, work buffers, input rereads and outputs. The input x has L actual data bits and two endmarkers.

A **single fixed** compiler builds B_A for *all* input lengths and labels: simulate every A transition (including its terminal transition, intercepted into a nonhalting output-cache state), simultaneously return each original input head to position zero, copy the exact L+2 source symbols onto a new writable tape, and on the very next transition halt with A's cached correct output. If p_j(x) are the final original-head positions, R_A(x)=max_j p_j(x), then in this declared phase convention:

$$
T_{B_A}(x)=T_A(x)+R_A(x)+L+3,\qquad
0\le R_A(x)\le\min\{L+1,T_A(x)\}.
$$

The new tape visits L+2 cells, so the declared tape-additive visited-cell space is S_B(x)=S_A(x)+L+2. A may be an arbitrary total SAT decider using any polynomial workspace, caching, reencodings, algebraic algorithms, or repeated reading. The construction does not *solve* SAT cheaply: all of A's decision cost occurs before READY.

The exact READY -> halt transition is a **genuine** concrete edge of cost one, including both SAT/UNSAT labels and malformed returns. Any all-transition cost-sound MAY abstraction that represents it by an abstract path of cost at most one, and any Phi obeying Phi(u)<=w(u,v)+Phi(v) on **every** abstract edge and Phi(goal)<=0, must satisfy Phi(READY)<=1. Deleting that edge as supposedly spurious violates soundness. The identity abstraction of B_A witnesses all initial, transition and terminal bindings directly.

**Independent peer verdict:** the construction and this Bellman ceiling are PROVED/RESTRICTED for the *designated completed copy tape* checkpoint. The more general target about total T_A(x), or the first-ever source scan, does NOT follow. TMR-4/003 already supplies a separate *declared-length-grammar* final-unobserved-bit counteralgorithm; its stronger timing claim has extra encoding hypotheses and is not silently inherited here.

### TMR-3/013: bounded future dependence is mathematically sound

The original TMR-3/013 proof is valid under its stated conditional prefix-free code assumptions. Given independent uniform q_i-bit X_i, c_i depending on all earlier variables and at most r subsequent variables, and prefix-freeness as X_i varies with all other arguments fixed, Kraft gives E[2^{q_i-|c_i|} | X_{<i}]<=1. In each class modulo r+1, earlier code lengths are measurable before the next class index. Conditional-product expectations are therefore <=1, and Holder plus Markov gives

$$
\Pr\left[\sum_i |c_i|<\sum_i q_i-b\right]\le2^{-b/(r+1)}.
$$

The grouped-XOR example is a valid conditional prefix-free sharpness control, not an actual physical SAT crossing transcript. **Independent peer verdict: PROVED/RESTRICTED, conditional-coding mathematics only.** The crossing-code physical dependence hypothesis remains OPEN. In particular, local two-way source heads may read all later blocks, so merely disjoint independent inputs do not imply r=0.

## 2. NEW TMR5-ID12 theorem: interval overlap, not maximum lookahead, controls the bound

**CANDIDATE pending independent TMR-3/TMR-2 review.** Let X_1,...,X_K be independent uniform q_i-bit sources. Fix i<=R_i<=K. Assume each binary code c_i is a deterministic function only of X_1,...,X_{R_i} and, for every fixed assignment of all those variables except X_i, the map X_i -> c_i is injective and prefix-free. Define the closed *future-dependence intervals* I_i=[i,R_i] and their maximal overlap depth

$$
D=\max_{1\le j\le K}|\{i:i\le j\le R_i\}|.
$$

For every b>0,

$$
\boxed{
\Pr\left[\sum_{i=1}^K|c_i|<\sum_{i=1}^Kq_i-b\right]\le 2^{-b/D}.
}
\tag{ID12}
$$

**Proof.** Put Y_i=2^{q_i-|c_i|} and F_j=sigma(X_1,...,X_j). For fixed X_{<i} and X_{i+1},...,X_{R_i}, the codebook in X_i is prefix-free. Xi is uniform independent of the rest, so conditional Kraft yields E[Y_i | F_{i-1},X_{i+1:R_i}]<=1, and therefore E[Y_i|F_{i-1}]<=1. Greedily color the intervals I_i by start point. The closed intervals are an interval graph and admit D colors: use the first color whose previous interval ends strictly before i; the usual maximum-overlap argument proves that D colors suffice. For any one color, successive indices i<j satisfy R_i<j, so Y_i is F_{j-1}-measurable. Conditional expectation applied backward to their product gives E[product_{i in color}Y_i]<=1. Generalized Holder across D colors yields E[(product_i Y_i)^{1/D}]<=1. On the stated short-code event, product_iY_i>2^b; Markov gives the bound. QED at the declared coding-model scope, subject to independent peer review.

TMR-3/013 is the special case R_i=min(K,i+r), whose interval depth is at most r+1. The sharper distinction matters for **heterogeneous** future dependence: R=(5,1,2,3,4,5) with K=6 has one code allowed to depend five blocks forward, yet D=2, not the coarse bound 6. Equal-size nonoverlapping groups with R_i equal to the last index in each group recover TMR-3's grouped-XOR exponent sharpness. This is an improvement of a restricted coding inequality, **not** a new SAT physical time-space lower bound.

**Falsification controls.** Outside variables may select the entire codebook, and complete past dependence is allowed. If prefix-freeness is deleted, three independent q=2 blocks all sent to the empty word give an actual bad-event probability one for b=1, violating the false D=1 bound 1/2; this is not a counterexample to ID12. If source-dependent physical crossing records span the entire suffix for many cuts, D may be K, losing all growing-K concentration. Nothing here treats semantic assignments, repeated certificate appearances, or shared computation as separately paid physical work.

## 3. Independent executable verification, exact model and provenance

The **exact published standalone JS** was executed in hosted V8, NOT through a wrapper around any peer implementation. Its own finite codebook functions are separately authored. Seven interval layouts were exhaustively checked over 21,568 independent 2-bit-block vectors, including 1,214 separate conditional codebook fibers and nine tail thresholds for each layout. Each fiber verifies injection, all-pairs prefix-freeness, and Kraft; each layout verifies independent-color product moments and the ID12 bound. Zero assertions failed. The nonprefix adversary was also evaluated.

Separately, a **single fixed 3-variable proper three-literal 3-CNF source language** was used as a compact-algebra counter-control: each clause is encoded by its three sign bits, and an 8-bit finite-state mask decides SAT iff fewer than all eight forbidden assignments occur. Malformed lengths are explicitly classified; no uncharged source access or oracle is used. The actual local-step wrapper traces were checked for h=1,2,3 source heads on 24,591 total inputs, including genuine SAT, genuine UNSAT and malformed encodings, 960,327 charged transitions, 960,327 every-edge Bellman checks and 24,591 actual READY=2 violations, with zero failed assertions. Outcomes: 14,055 SAT, 6 UNSAT, 10,530 malformed. The machine is an authenticated **restricted 3-CNF** decider, not a general NP-complete 3-SAT solver. The full theorem for arbitrary A is symbolic, not inferred from these cases.

A **separately authored native CPython** implementation ran locally, without importing the peer code, and matched the seven-layout 21,568-vector/1,214-fiber and the complete 24,591-input/960,327-transition ledger; this native Python file and its local output are **LOCAL-ONLY** and are not claimed published to GitHub. The exact peer TMR-4/015 V8 source was inspected but was **not** executed under native Node; the repository code could not be downloaded to the OS runtime over DNS. Neither execution is an instruction-level simulation of arbitrary SAT machines.

**Published V8 source:** experiments/tmr/tmr5_interval_latecopy012.cjs.
**Immutable raw:** results/raw/tmr/2026-11-14_0054_TMR5_INTERVAL_LATECOPY012_RAW.json.

## 4. Synthesis and dependency firewall

The strongest surviving exact implications are the TMR-4 fixed-program *phase relocation* and TMR-3 conditional Kraft theorem, with ID12 a pending-review refinement. TMR-1's indexed-to-local charged simulation remains a candidate/conditional bridge. TMR-2's G_r observation certificate and M7 multiplicity results are **restricted source information**, not compulsory superpolynomial processing; the new 48 balanced M7 extremum has not been independently audited in this run. TMR-4's Bellman simulation premise is a necessary soundness discipline, but it supplies no noncircular superpolynomial initial potential. TMR-3's physical crossing-record future-dependence depth remains completely unbounded for an arbitrary two-way-input uniform SAT solver.

The **next unresolved load-bearing implication** is a same-machine, all-transition *full-execution* processing-cost invariant for every fixed correct 3-SAT decider that cannot be evaded by deciding before a designated copy, physical rereading, GF(2)/Horn/2-SAT/treewidth shortcuts, sharing, padding, auxiliary variables, arbitrary polynomial workspace, or recomputation. Under a standard local machine S_A(x)<=O_A(T_A(x)+1) holds on the same x, but no proven lower bound excludes every polynomial exponent. The target remains forall correct A, forall k>=1,C>0,L0, exists valid F of encoded L>=L0 with T_A(F)>C(L+1)^k. No per-length algorithm minimization, proof-system portfolio bound, ETH/SETH premise, natural-proofs circuit-property transfer, relativized oracle, or unbounded-word accounting is smuggled into this result. Baker-Gill-Solovay and Aaronson-Wigderson barriers remain methodological cautions, not evidence of separation.

## 5. Primary sources and corpus audit

Primary literature inspected for exact scope:
- McMillan, *Two Inequalities Implied by Unique Decipherability*, IEEE TIT 2(4) (1956), pp. 115-116, https://doi.org/10.1109/TIT.1956.1056818 . Conditional Kraft is applied only to actual prefix-free finite codebooks.
- Cousot and Cousot, *Abstract Interpretation*, POPL 1977, pp. 238-252, https://doi.org/10.1145/512950.512973 . Conservative abstract execution is background; the Bellman proof here is explicit.
- Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005) pp. 835-865, https://doi.org/10.1145/1101821.1101822 . This excludes specified simultaneous small-space/time exponent pairs on deterministic random-access machines, not arbitrary polynomial time and workspace.
- Baker, Gill and Solovay, *Relativizations of the P=?NP Question*, SIAM J. Comput. 4 (1975), pp. 431-442, https://doi.org/10.1137/0204037 ; Aaronson and Wigderson, *Algebrization*, ACM TOCT 1 (2009), article 2, https://doi.org/10.1145/1490270.1490272 . No oracle or algebraic relativization was used.

First read the controlling 2026-11-13 12:49 PST TMR replacement directive (blob 47459817e66dccf1f3079e6c724c0fd2643e7bc4). Read proof1.txt complete (28,714 characters; blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343), recovered proof2.txt complete from authentic Git blob (1,051,196 characters; blob 930c5eeddafce656717f28055a7a9a755f44737c), and recovered canonical root main.tex complete from authentic Git blob (2,518,238 characters; initial blob 0233cb0ca16a63a2a63a83af6a61ffe985632945). Also read AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, newest five TMR handoffs, issue #3 through TMR-4/015, original TMR-3/012 and /013, original TMR-4/003,/013,/015, TMR-2/014, historical LSPV-5/464, and the relevant peer executable/raw evidence. Conflicting legacy role and route text is superseded, not resurrected.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P1-01/P1-03/P1-04 and P2-00 are OPEN. Do not rewrite either tracker. Root main.tex is the sole canonical manuscript; this result is to be incorporated only in TMR-5's authorized synthesis region, with readback validation. No scheduled tasks were created, revived, or modified.

**One next target:** TMR-3 or TMR-2 should independently prove/falsify ID12, then use a *real fully charged two-way crossing-record construction* to measure whether its interval overlap D can ever be bounded sublinearly for every uniform SAT decider. TMR-4 should seek a whole-run, phase-invariant potential rather than post-designated-copy work. P versus NP remains OPEN.
