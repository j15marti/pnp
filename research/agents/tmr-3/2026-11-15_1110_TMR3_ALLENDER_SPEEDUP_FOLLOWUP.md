# Allender speedup follow-up: sharper rational slack and linear-leaf checkpointing

2026-11-15 11:10 PST. TMR-3 follow-up to the user's direct request to simplify the speedup and examine its implications.

## Status

**PROVED/EXACT:** the rational parameter improvement and its explicit slack; the finite path-count identities; the algebraic implication of the precisely stated fixed-depth hypothesis below.

**CANDIDATE:** the complete fixed-depth checkpoint simulation FK, pending independent verification of machine-model interfaces and uniform circuit wiring. No numerical hierarchy depth K has been established here. The proposed linear-in-space-deficit lower-bound corollary is **CONDITIONAL on FK**, not a promoted strengthening of the literature.

**COMPUTATIONAL:** 71,288 assertions, zero failures. These tests do not establish asymptotic class containments.

No SAT algorithm, MajMajSAT-to-SAT compiler, superpolynomial lower bound, or P-versus-NP separation is claimed. This is a proof-analysis follow-up, not a runtime improvement for an implemented SAT solver.

## Candidate and falsifiers

Candidate: stop the arithmetic checkpoint construction at linear-time counting leaves, rather than single transitions, to reduce the hierarchy-level cost while preserving exact path multiplicities and inclusive majority.

F1: the leaf is not genuinely in a fixed linear-time counting-hierarchy level after configuration loading, source access, endpoint comparison and threshold encoding.

F2: the arithmetic replacement/wiring computation has hidden depth depending on the space deficit, or exceeds the charged linear-time hierarchy interface.

F3: checkpoint labels exceed O(n), or an exponentially large circuit is treated as a cheap physical machine.

F4: exact hierarchy-oracle answers are replaced by independently sampled weak-majority answers, changing the acceptance sign.

## 1. Source dependencies

Allender et al. [1], Theorem 2 and Lemmas 5-6, supply the unbounded-error time hierarchy, a small-space-to-LCH simulation, and the conditional collapse LCH_k subset PrTime(n^(d^(k-1))) if LCH_2 subset PrTime(n^d). Their Theorem 4 uses padding b with b*sigma<1 and d^(k-1)<b. Section 3.2 gives quasilinear, locally generated reductions to MajMajSAT, requiring exponent slack.

Hesse, Allender and Barrington [2] supply fully uniform constant-depth threshold arithmetic. Their 2014 corrigendum [3] retracts part of Corollary 6.6; the present candidate uses the arithmetic circuit result, not that corollary.

Van Melkebeek and Watson [4], Theorem 1, supplies bounded-error quantum to unbounded-error classical simulation with O(t log t) time and O(s+log t) space under its algebraic-amplitude and constructibility assumptions.

These are dependencies, not claims that the papers prove FK or the conditional corollary below.

## 2. Exact simplification of the existing parameter choice

Put m=k-1, k>=2. The preceding report used b=3/2 and d_old=1+1/(4m). The actual hierarchy contradiction requires only

    d^m < b.

For this fixed k and b, the endpoint is d_*=b^(1/m), not an admissible equality. A sharper rational choice is

    d_new = 1 + 2/(5m).

For c=2/5, the binomial coefficients satisfy binom(m,j)/m^j <= 1/j!. For j>=2, j! >= 2*3^(j-2). Therefore

    (1+c/m)^m < exp(c)
                 <= 1+c+c^2/[2(1-c/3)]
                 = 97/65
                 < 3/2.

In particular,

    3/2 - d_new^m > 1/130.

The improvement in d-1 is exactly (2/5)/(1/4)=8/5, or 60 percent, for the SAME k. This does not mean a 60 percent improvement in runtime, nor necessarily a 60 percent improvement in the final lower-bound exponent if another hypothesis limits it. No numerical k, tau, or gamma is invented.

A general rational safe rule for rational b>1 is

    d = 1 + (b-1)/(2*b*m).

Writing q=(b-1)/(2b), the binomial/geometric estimate gives

    d^m < 1/(1-q) = 2b/(b+1) < b.

This avoids root computation and leaves explicit slack b(b-1)/(b+1).

## 3. Linear-time counting leaves

Fix a finite fair-coin machine M and a compatible configuration encoding. A leaf contains the original n-bit input, two complete configurations, a segment length at most O(n), and a count threshold or bit position. Its full input length is O(n). Assume the fixed machine can be initialized, simulated for that segment, and checked against the destination in O(n) time in the chosen source model. This includes input/head initialization, work-tape contents, clock, endpoint comparison and index parsing.

Let f be the number of q-bit coin strings that carry the source to the destination, with q=O(n). Duplicate transitions count separately, since they correspond to different coin strings. This is a numerator count, not reachability.

The threshold language f>=y is in PrTime(n). For 0<=y<=2^q, a fair initial selector can choose between (i) simulating the q-bit path and (ii) accepting on exactly 2^q-y of q-bit strings. The total accepting count is

    A = f + 2^q-y

out of 2^(q+1), so inclusive majority is equivalent to f>=y. Values outside the range are handled deterministically. Strict-sign normalization, when needed, uses a further O(q)-coin balancing construction and does not change the hierarchy level.

For a desired bit j, nondeterministically guess z in [0,2^q], check bit_j(z)=1, and ask two EXACT threshold-oracle questions:

    f>=z, and NOT(f>=z+1).

Exactly one candidate z satisfies the two threshold conditions, namely z=f. The outer machine takes O(n) time including query writing; converting existential acceptance to unbounded-error majority adds only linear overhead. Hence the count-bit predicate belongs to LCH_2 in this compatible model.

This is a hierarchy containment, NOT a procedure that outputs f in O(n) ordinary time. No sampled PP calls are substituted for exact oracle answers. The full machine-interface verification remains part of FK's review gate.

## 4. One-level checkpoint budget and candidate FK

Suppose a fixed machine has time T=O(n^alpha), workspace S=O(n^sigma), with 1<alpha, 0<sigma<1. Complete configurations use O(S+log T+log n) bits, including control, all heads and clock.

Divide its time interval into segments of length at most n. There are O(T/n) segments. The descriptor of a full checkpoint tuple has length

    O((T/n)*(S+log T+log n)).

For fixed powers with alpha+sigma<=2 this is O(n). To retain slack for all interface bookkeeping, FK below uses the STRICT interior alpha+sigma<2.

For endpoints c_0 and c_r, exact counting gives

    paths(c_0,c_r,T)
      = sum over c_1,...,c_(r-1)
          product over i=0,...,r-1 paths(c_i,c_(i+1),segment_i).

This is one sum-product layer over linear-time counting leaves. Checkpoint choices have O(n)-bit labels. The expression may have 2^O(n) size, and the total count has O(T) bits. Products contain only polynomially many factors. Fully uniform threshold arithmetic is the relevant tool for converting the sum and product to constant threshold depth. Leaf bits are accessed through the preceding LCH_2 predicate.

**Candidate FK:** There is a fixed integer K>=2, independent of the fixed rational exponents alpha and sigma, such that

    alpha>1, 0<sigma<1, alpha+sigma<2
       => PrTiSp(n^alpha,n^sigma) subset LCH_K,

in a precisely matched source model.

The candidate is supported by the construction above, but NOT marked as a verified theorem. Its remaining promotion obligations are a complete source-model initialization/access simulation, exact uniformly generated arithmetic wiring and its hierarchy level, and an independent proof that K can be chosen uniformly in the exponents. The original Allender theorem alone gives a finite level for each exponent pair; it does not by itself supply the uniform K required here.

A count-bit oracle is not an SAT oracle. Treating the leaves as free, or materializing the exponential circuit at unit cost, would falsify the intended transfer.

A robust variant can stop at n^q with q<1 chosen strictly above alpha+sigma-1. Then checkpoint descriptors have length n^(alpha+sigma-q)=o(n), and segment simulation admits polylogarithmic overhead while remaining below linear time. This does not remove the need to verify the complete hierarchy interface.

## 5. Exact consequence if FK is verified

Let delta=1-sigma be rational in (0,1), K satisfy FK, and m=K-1. Define

    d = 1 + delta/(8m),       b = 1 + delta/4.

Suppose, for contradiction,

    LCH_2 subset PrTiSp(n^d,n^(1-delta)).

Since PrTime(n) subset LCH_2, padding by b gives

    PrTime(n^b) subset PrTiSp(n^(bd),n^(b(1-delta))).

The padded pair satisfies b(1-delta)<1 and

    bd + b(1-delta) < 2.

For example, using m>=1, its sum is at most

    2 - 3delta/8 - 7delta^2/32 < 2.

FK would put this class in LCH_K. The initial assumed inclusion also yields LCH_2 subset PrTime(n^d), so Allender's Lemma 6 yields

    PrTime(n^b) subset LCH_K subset PrTime(n^(d^m)).

But

    d^m < 1/(1-delta/8) < 1+delta/4 = b,

and the exact gap between the latter two bounds is

    delta*(4-delta)/(4*(8-delta)) > 0.

This contradicts the time hierarchy. Thus FK implies a lower-bound region with LCH_2 time excess proportional to the space deficit, with coefficient 1/[8(K-1)].

For the MajMajSAT completeness reduction, use internal deficit delta/2 and reserve additional time slack. The conditional resulting exclusion is

    MajMajSAT notin PrTiSp(n^(1+c*delta),n^(1-delta)),
    c = 1/[32(K-1)],

for fixed rational delta in (0,1). Extension to arbitrary real exponents must be made through slightly weaker rational exponents with appropriate additional slack. This manuscript does not fix a numerical c or promote the statement without FK.

Bounded-error quantum consequences would use [4] only AFTER the classical statement is justified, and with a strictly smaller time exponent to absorb the logarithm. No arbitrary unbounded-error quantum conclusion follows.

## 6. Implications for the existing virtual SAT compiler

The previous ONE-query compiler ledger remains

    theta=max(r,a*t+h),     eta=max(u,a*s),

with all source generation, retained state, input addresses and access costs charged. Those formulas describe a hypothetical compiler and a target SAT solver, not a construction.

If FK and its corollary were established, the existence of a strict forbidden-region choice of sigma would simplify, for eta<1, to

    theta + c*eta < 1+c.

Equivalently, when theta>=1,

    (theta-1)/(1-eta) < c.

This is an exact algebraic simplification of the conditional region: choose eta<sigma<1-(theta-1)/c. It is not an unconditional SAT lower bound. The required exact MajMajSAT-to-SAT compiler is still missing, and no inference from P=NP supplies it. Multi-query weak-majority composition also remains invalid without a separate theorem.

## 7. What cannot be inferred

The construction replaces time by stronger counting-hierarchy operations. It does not give the original ordinary algorithm a faster runtime, and its output is not another small-space ordinary machine to which the same speedup can automatically be reapplied.

Within the original single-chain argument, b*sigma<1 and d^(k-1)<b imply d<sigma^(-1/(k-1)). At fixed positive sigma this is a finite ceiling for that chain, not a general lower-bound barrier. Taking sigma to 1 closes the available interval for b.

No repeated padding step alone turns a fixed superlinear lower bound into a superpolynomial one. No result here removes the sublinear-space restriction. The exponential arithmetic circuit is not a small Tree Evaluation instance with free leaves or a cheap evaluator. Its node generation, integer bits, leaf predicates and evaluation work must remain visible in any attempted compression transfer.

## 8. Required verification gates

| Gate | Status and reason |
|---|---|
| DISJ sanity | PASS as scope control: no rank-to-runtime assertion; easy Horn/2-CNF formulas are not declared hard. |
| Relativization | OPEN for an arbitrary-oracle version of FK. This note uses ordinary machines and makes no P-versus-NP separation. Oracle access and query storage would need a new audit. |
| Simultaneous resources | PASS for algebraic accounting; OPEN for any SAT transfer. Both T and S refer to one source machine, and the output is a hierarchy simulation, not a claimed same-space fast algorithm. |
| Configuration counting | PASS as an upper bound for configuration labels only. It supplies no lower bound on work. Branch multiplicities are preserved. |

Natural-proofs/circuit-hardness transfer is not invoked. Compact algebra, caching and sharing remain legal. Historical /341 remains FAIL as a full UNSAT authority and /386 remains RESTRICTED.

## 9. Evidence and corpus review

Executed source: audit_speedup.py. Raw output: results.json. Standard-library CPython; seed 20261115 applies only to small layered graphs. Exact fractions are used for all exponent checks. The single invocation completed within the configured 30-second limit.

Results: 71,288 assertions; zero failures; 3,969 synthetic (K,delta) pairs; 22,363 threshold-count pairs; 120 small fair-branch layered graphs. Tests include independent coin-string enumeration, matrix products, checkpoint sum-products, inclusive ties, exact count-bit candidates, duplicate coin edges, an out-of-budget exponent pair, and the weak-PP AND counterexample. Synthetic K values are NOT measured circuit depths. Finite tests do not establish FK.

Reviewed: Allender directive; current SAT-compression directive; TMR-3/049 original report; current portions of all five TMR handoffs; AGENTS.md, CODEX.md and the repository research skill; available proof1 content; main.tex/proof2 SHA metadata; issue #3 body; targeted repository checkpoint search; primary papers [1], [2], [4] with PDF screenshot inspection, and corrigendum abstract [3]. TMR-4/050 already supplies the multiplicity-preserving checkpoint identity; it is reused, not claimed new. The new proposed ingredient is stopping at counting leaves and seeking a UNIFORM hierarchy-level bound.

Limitations: the connector returned empty bodies for oversized main.tex and proof2.txt. A full checkout/preflight and repository-wide tests were not executed. Their complete current contents were not recovered, so no existing tracker, manuscript or canonical handoff is rewritten. This is an additive draft research publication with peer review requested, not a completed full-preflight scheduled run. All schedules and identities are unchanged.

**TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.**

Next proof obligation: independently establish or falsify FK, especially the fixed hierarchy level for exact count-bit leaves and the charged uniform circuit-wiring interface. No further coefficient tuning should be mistaken for closing that obligation.

## References

[1] Allender, Koucky, Ronneburger, Roy and Vinay. Time-Space Tradeoffs in the Counting Hierarchy. CCC 2001. https://people.cs.rutgers.edu/~allender/papers/tradeoff.pdf

[2] Hesse, Allender and Barrington. Uniform Constant-Depth Threshold Circuits for Division and Iterated Multiplication. Journal of Computer and System Sciences 65 (2002), 695-716. https://people.cs.rutgers.edu/~allender/papers/division.pdf

[3] Hesse, Allender and Barrington. Corrigendum. Journal of Computer and System Sciences 80 (2014), 496-497. DOI:10.1016/j.jcss.2013.09.002. Publisher and Rutgers abstracts checked; full correction not downloaded. No use of Corollary 6.6.

[4] van Melkebeek and Watson. Time-Space Efficient Simulations of Quantum Computations. Theory of Computing 8 (2012), 1-46. https://www.cs.memphis.edu/~twwtson1/papers/qts.pdf
