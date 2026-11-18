# SIGMA REDTEAM33: Iterated input-expansion phase transition and exact QBF witness firewall

**UTC:** 2026-11-18 20:12. **Status:** Conditional resource-ledger theorem proved algebraically; two independent finite auditors total **544,452 checks, zero failures**. Unrestricted hereditary Circuit-SAT resource contraction OPEN. P versus NP OPEN.

## PROPOSE and SEARCH
Before the literature search, chose: (1) audit original-input expansion on every recursive reduction; (2) separate the one-step K=3 comparison from the published SAT time-space certificate after iteration; (3) physically embed an arbitrary Circuit-SAT child under syntactically positive one-bit cutset; (4) exhaust QBF quantifier placement, compact Skolem strategies, non-affine gate circuits, unique traces and equivalent rewrites; (5) challenge padded hypothetical solvers, oracle interpolation and sparse-address RAM accounting.

Inspected current j15marti/pnp reports REDTEAM28, REDTEAM31 and REDTEAM32, including the minority-polarity claimed tagged-source recurrence and the arbitrary-F guest trap. Primary sources: Fortnow and van Melkebeek, DIMACS TR 2000-06, https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2000/2000-06.html ; Fortnow et al., JACM 2005, https://doi.org/10.1145/1101821.1101822 ; Williams, STOC 2024, https://doi.org/10.1145/3618260.3649723 .

## A. Conditional recursive expansion theorem
Suppose, contrary to the current missing closure proof, that an *unrestricted hereditary* source compiler is available and every ordinary n-bit problem is re-encoded to tagged length N=n^(alpha+o(1)) at every invocation. Suppose the fully charged physical compiler obeys, in tagged-source units,

    K'_N <= 0.59 + K/2 + o(1)
    L'_N <= max(0.5,L/2) + o(1).

Original-input exponents then obey the **upper-bound recurrences**

    K_{j+1} <= alpha*(0.59 + K_j/2) + o(1)
    L_{j+1} <= alpha*max(0.5,L_j/2) + o(1).

For alpha<2, the bounding recurrences have fixed points

    K_* = 0.59*alpha/(1-alpha/2)
    L_* = alpha/2.

At alpha>=2, a nominal N^(1/2) guest can have at least n bits, so this encoding does not certify any shrink in original-input size. These statements concern the *algebra of claimed upper bounds*, not measured optimal SAT complexity. They require every input decoder, no-answer SAT call, parent-sized call, repeated source read, and work-address charge. Moreover actual generated guests need not remain in the tagged grammar, so the hypotheses are not presently established.

## B. Exact published-curve margin
Fortnow and van Melkebeek's **2000 explicit sufficient forbidden region** for the deterministic SAT time-space tradeoff is c<golden ratio with space exponent

    d < d_old(c) = ((c+2)/c^2-c)/2.

If the hypothetical recursively closed construction also produced a uniform SAT decider in the matching random-access Turing-machine model, the *specific older certificate* would contradict the fixed-point exponents when

    alpha/2 < d_old(0.59*alpha/(1-alpha/2)).

The unique root in [1,1.03] solves

    174050 alpha^4 - 655979 alpha^3 + 910000 alpha^2
    - 2410000 alpha + 2000000 = 0

and is **alpha_crit = 1.00970585730656...**.

| alpha | K_* | L_* | d_old(K_*) | margin? |
| --- | ---: | ---: | ---: | --- |
| 1.000 | 1.180000 | .500000 | .551913 | positive |
| 1.005 | 1.191859 | .502500 | .527546 | positive |
| 1.009 | 1.201433 | .504500 | .508242 | positive |
| 1.010 | 1.203838 | .505000 | .503442 | absent |
| 1.020 | 1.228163 | .510000 | .455991 | absent |

This is an **input-length exponent** threshold (N=n^alpha), not a fixed 0.97% increase in bytes, and is **not a proven barrier to stronger later published SAT tradeoffs**. Absence of this certificate does not establish a correct fast algorithm.

The independent one-step benchmark is K=3, target 2.10: alpha*2.09 < 2.10 iff **alpha < 210/209 = 1.004784688995...**. For alpha=1.005 the one-step target fails (2.10045) while the older asymptotic fixed-point certificate still has positive margin. These are distinct questions.

## C. Literal child identity, padded guest and closure
For arbitrary ordinary Circuit-SAT F(y), define the tagged monotone factor

    C_F(c,y) = c AND NOT F(y).

For each y, NOT EXISTS c C_F(c,y) = **F(y) exactly**, and FORALL y EXISTS c C_F(c,y) is true iff F is UNSAT. Thus a single tagged parent can emit an *arbitrary ordinary SAT guest*. That guest is not automatically eligible for the parent's syntactic minority-polarity compiler. Re-applying the claimed recurrence without proving a new tagged-source representation and charging its length is unsound.

In a deliberately padded source N=n^2, an n-bit guest formally fits N^(.5) but does not shrink from the original n bits. A **reached** call to an artificially delayed yet correct A_D on that guest costs n^D, not n^(D/2). For alpha=2 the advertised recurrent time expression becomes K'<=1.18+K and cannot establish self-contraction. The REDTEAM31 actual raw-factor cap N^(.45) would force alpha >=20/9 for the particular direct embedding of a raw n-bit F factor, an even worse guest-length budget. These are implementation/encoding counterexamples, not arbitrary-SAT time lower bounds.

Five independently serialized *toy* factor sources had physical lengths 740, 1128, 1711, 1596 and 1596, with a positive tagged factor and TRUE fillers; every original guest fit the source-relative square-root cap. They verify physical length arithmetic only, **not** full admission to the actual compiler's source grammar.

## D. Exact shared-c Sigma1/2/3 and trace-prefix audit
For any G(x,u), set

    H_G(c,t,b,u)=(NOT t AND c) OR (t AND NOT b)
                 OR (t AND b AND NOT c AND G(x,u)).

With globally fixed x, universal y=(t,b,u), and post-universal c,

    EXISTS x,y,c H_G = TRUE
    EXISTS x,c FORALL y H_G = FALSE
    EXISTS x FORALL y EXISTS c H_G iff EXISTS x FORALL u G(x,u).

For a winning x, c=NOT t is a compact legal Skolem response. Moving global x after y creates false positives. Moving uniquely determined *internal gate traces* before y can create false negatives, e.g. F(y)=y AND NOT y is constantly false but its NOT-gate trace changes with y.

**Primary finite auditor** (standard-library Python, seed 202611182007): **20,115 assertions**, zero failures. Exhausted 256 H_G truth tables (31 Sigma3-true, 32 winning x strategies), evaluated 700 random small DAGs (302 non-affine, 74 zero-output circuits with variable internal traces), 700 equivalent double-NOT rewrites, 950 randomized CNFs (14,132 identity checks), 508 one-spike oracle controls, exact-rational curve checks and memory/solver ledger controls.

**Independent auditor** (separate implementation): **524,337 assertions**, zero failures. Exhausted all 65,536 ordered relation pairs on one shared c and two universal y bits: 4,160 false positives from separate factor-local c guesses, 1,890 cases of Sigma3 true but Sigma2 false. Exhausted 65,536 G truth tables with two global x bits and two universal u bits: 14,911 Sigma3-true, and 35,714 false positives when x is placed illegally after y. Numerical root by independently iterating the recurrence and bisection = 1.0097058573065598.

The finite checks do not imply asymptotic complexity bounds.

## E. Triple-ledger, oracle, and machine firewall
- **Time:** source creation, input expansion, guest serialization/decoding, any parent-sized SAT calls, negative SAT answers and recursively emitted children must be charged. A deliberately delayed correct solver tests whether the literal child invocation actually preserves the purported exponent improvement.
- **Space:** alpha/2 is conditional on the entire live-workspace ledger (decoder, offsets, trace and strategy advice); there is no independently established model-preserving conversion to FLMV random-access Turing-machine space.
- **R:** the count of distinct RAM locations is at most the number of accesses and thus R<=T is tautological. Touching address 2^100 in a short computation does not limit the largest work-tape position to a small value. Account for address representation and the exact target machine model.
- **Quantifiers:** x remains globally committed; c and functional gate traces respond after y; shared y pins remain identical across all factor guests. No free global strategy table or re-guessed shared c.
- **Oracle:** C_O(c,y)=c AND NOT O(y) has guest O(y). All-zero and one-spike black-box oracle inputs differ only at one query. A black-box lower bound here is not a white-box SAT complexity lower bound, and none of the reported identities supplies a nonrelativizing lower bound.

## HANDOFF
1. Prove genuine all-input hereditary closure and charge **alpha on every level**, not just initial source construction.
2. Track both independent thresholds: one-step alpha<210/209 at K=3, and the older FvM curve's conditional fixed-point threshold alpha<1.00970585730656.
3. Exercise the direct arbitrary-child C_F factor, genuine serialization, padding and delayed A_D; disallow source-relative guest shrink as a stand-in for original-input shrink.
4. Continue exhaustive Sigma1/Sigma2/Sigma3, compact Skolem, equivalent circuit, non-affine guard, gate-trace, oracle and adversarial high-address tests.
5. Do not transfer FLMV lower bounds until the all-input compiler, uniformity, machine model and full time/space ledger are actually established.

**Proof status:** restricted conditional resource accounting and finite tests passed; general Circuit-SAT contraction remains unproved; no P != NP proof claimed.

VERIFICATION_SENTINEL_SIGMA33_PADDING_RECURSION_20261118_2012Z
