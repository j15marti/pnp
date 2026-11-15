# TMR-1/049: Allender dependency ledger and exact double-majority unique-extension normalization

**2026-11-15 09:57 PST | PNP Machine Model Lead | ALLENDERBALANCE049**

**Status:** Allender et al. Theorems 2–7 and van Melkebeek–Watson Theorem 1: KNOWN THEOREM at their original scope. The balanced-extension theorem below: PROVED/RESTRICTED, independent mathematical review OPEN. Finite tests COMPUTATIONAL. SAT compiler CONDITIONAL/OPEN. P versus NP OPEN.

## 1. Candidate and three predeclared falsifiers

**Candidate:** Reconstruct the exact majority-preserving, unique-auxiliary-extension transformation in the proof of Allender Theorem 7 as a correctly scoped primitive for the fusion-Lipschitz program. Then quantify the weakest hypothesized uniform SAT compiler whose actual time-space resource pair would contradict the known MajMajSAT bound.

**Falsifiers:** (1) Additional unconstrained witness assignments can change an inner-majority decision; (2) deleting the balancing background or replacing inclusive with strict majority changes ties; (3) a supposed routine MajMajSAT-to-SAT polynomial many-one compiler already implies the major open collapse PP=NP. All three yield exact controls below.

## 2. Primary-source theorem ledger and gamma dependence

[1] Allender, Koucký, Ronneburger, Roy, Vinay, CCC 2001: https://people.cs.rutgers.edu/~allender/papers/tradeoff.pdf

[2] van Melkebeek and Watson, Theory of Computing 2012: https://www.cs.memphis.edu/~twwtson1/papers/qts.pdf

Here n means **encoded input length**, and PrTiSp(t,s) uses one uniform **unbounded-error probabilistic** machine satisfying both bounds simultaneously.

| Original result | Exact scope and dependency |
|---|---|
| Allender Theorem 2, p. 4 | If time-constructible t=o(T), PrTime(t) is strictly below PrTime(T); probabilistic hierarchy diagonalization uses constant-overhead two-tape simulation. |
| Theorem 3, p. 4 | For each fixed 0<epsilon<1, exists gamma>0: LCH_2 = PrTime(n) with PrTime(n) oracle is **not contained** in PrTiSp(n^(1+gamma), n^epsilon). A class noncontainment, not a single hard family. |
| Theorem 4, pp. 5–6 | For each epsilon in (0,1), a>1, if PrTime(n) subset PrTiSp(n^a,n^epsilon), then for some d>1 the second linear-counting level is not contained in PrTime(n^d). |
| Lemma 5, pp. 5–9 | For alpha>1 and 0<beta<1, PrTiSp(n^alpha,n^(1-beta)) subset LCH_tau(alpha,beta), tau=O(alpha/beta)+k_unif. Time-stamped probabilistic paths are counted by highly uniform bounded-depth arithmetic circuits and translated using iterated-sum/product TC0 circuits. |
| Lemma 6, p. 5 | For rational d>1 and integer k>=1, assuming LCH_2 subset PrTime(n^d), get LCH_k subset PrTime(n^(d^(k-1))). This is an iterated **padding/collapse** statement with exact probabilistic oracle semantics. |
| Theorem 7, pp. 9–12 | For each fixed 0<epsilon<1, exists gamma'(epsilon)>0: MajMajSAT not in PrTiSp(n^(1+gamma'),n^epsilon). Proof reduces LCH_2 **to** MajMajSAT with output length n log^O(1)n and any output bit computable in log^O(1)n time and logarithmic space. |
| van Melkebeek–Watson Theorem 1, pp. 1–2 | A **bounded-error quantum** machine with algebraic amplitudes, t,s>=log n and stated deterministic t,s constructibility has an **unbounded-error probabilistic** simulation in O(t log t) time, O(s+log t) space. This quantum extension is later work, not Allender's original theorem. |

**Source-based gamma budget:** In Theorem 4 choose b>1 with b*epsilon<1. Set tau=tau(b*a,1-b*epsilon) from Lemma 5. Choose rational 1<d<b^(1/(tau-1)); then d^(tau-1)<b contradicts probabilistic time hierarchy if the hypothesized counting-level collapse held. Theorem 3 takes sufficiently small gamma relative to a-1 and d-1. Theorem 7 requires additional exponent slack for the quasilinear reduction: the authors say gamma' < gamma works, equality is not established. The paper does **not** determine an optimized numerical gamma because tau depends on the TC0 multiplication uniformity/depth.

**Arithmetic Nepomnjascii checkpoint mechanism:** A time n^alpha, space n^(1-beta) unbounded-error computation has at most 2^O(n^(1-beta)) time-stamped configurations. Divide a length-n^alpha path into n^beta segments of length n^(alpha-beta), sum over all intermediate configuration tuples and multiply the segment path counts. The checkpoint sum fan-in is at most (2^O(n^(1-beta)))^(n^beta)=2^O(n). Iterate O(alpha/beta) times to get 2^O(n) arithmetic size and O(alpha/beta) depth. Uniform threshold gates for iterated addition and multiplication and an LCH uniformity oracle implement the corresponding counting-hierarchy simulation. This construction proves a **hierarchy-class speedup**, not a cost-sound local machine tariff. In particular exponential path multiplicity alone is not charged exponential sequential computation.

**Local completeness reduction:** Allender first obtains a single final counting oracle query per outer probabilistic path through unique threshold witnesses for guessed previous oracle answers. Oblivious simulation and a Cook encoding create a circuit-verification formula with at most one auxiliary satisfying assignment per (external input, random tape). The following exact balanced gadget repairs the majority fraction. The proven reduction is LCH_2 -> MajMajSAT, not MajMajSAT -> SAT.

## 3. PROVED/RESTRICTED: balanced unique extensions preserve both majority blocks

Fix outer a in {0,1}^ell, inner b in {0,1}^k, k>=1, and a Boolean F(a,b). Suppose phi(a,b,z) has m>=1 auxiliary bits z and **exactly F(a,b)** satisfying z extensions for every (a,b), so either zero or one. This is the functional-witness property of a fully constrained deterministic circuit/Tseitin encoding with final output forced TRUE.

Introduce a new inner variable v:
\[
\Psi(a,b,z,v)=
(v\land\phi(a,b,z))\lor
(\neg v\land(b_1\lor z_1\lor\cdots\lor z_m)).
\]

Write K=2^k, M=2^m, S_a=#\{b:F(a,b)=1\}. For fixed outer a, the v=1 branch contributes **S_a** satisfying (b,z) pairs by uniqueness. The v=0 branch with b_1=1 contributes KM/2; with b_1=0 it contributes (K/2)(M-1), excluding only z=0^m. Thus, of the 2KM equally likely (b,z,v) assignments,
\[
\boxed{H_a=KM-K/2+S_a.}
\]
The **inclusive-majority** threshold is KM, so
\[
\boxed{H_a\ge KM\iff S_a\ge K/2.}
\]
This remains exact on ties, S_a=K/2 giving H_a=KM. The equivalence holds independently for every a, hence even the outer majority is unchanged:
\[
\boxed{\operatorname{MAJ}_a\operatorname{MAJ}_b F
=\operatorname{MAJ}_a\operatorname{MAJ}_{b,z,v}\Psi.}
\]
This is the exact count-preserving fragment reconstructed from Allender Section 3.2. It is **not** a reduction to ordinary existential SAT and proves **no** SAT decision-time lower bound. A polynomial-size deterministic circuit for F admits a polynomial-size functional-witness Tseitin encoding, but producing its bits, preserving majority after later encoding changes, and charging every real machine operation remain separate obligations.

## 4. Three concrete hostile witnesses

**Nonunique auxiliary extension:** Set k=m=2, with F TRUE on only b=00. Original S=1<2, so its inner majority is NO. With exactly one z satisfying on that b, H=14+1=15<16. If all four z values satisfy phi on b=00, then H=14+4=18>=16, a false YES. Unqualified extension variables are not majority-neutral.

**No background clause:** For k=m=2 and F identically TRUE, retaining only v AND phi yields 4 satisfied tuples out of 32, below the 16 threshold, although original majority is YES. The full balanced gadget yields H=14+4=18.

**Wrong tie convention:** For k=m=2 and F(b)=b_1, exactly two of four original inner assignments satisfy, so H=16 is **accepted** at the inclusive 16 threshold. A strict >1/2 test falsely rejects. TMR-5/045's separate conversion from inclusive majority to strict unbounded-error PP bias is useful but cannot be silently substituted without its own proof and charges.

## 5. PROVED/RESTRICTED structural compiler barrier and CONDITIONAL resource bridge

**Barrier lemma:** A uniform polynomial-time many-one reduction MajMajSAT -> SAT would imply PP=NP. Indeed, MajSAT reduces to MajMajSAT by adding an unused outer majority variable, preserving the inner decision. The hypothesized further reduction would put PP-complete MajSAT in NP; thus PP subset NP. The standard reverse inclusion NP subset PP gives equality. **No such reduction or collapse is asserted.** P=NP alone does not supply the missing PP-complete-to-NP many-one compiler.

**Weakest quantitative hypothetical bridge:** Assume one fixed uniform *exact deterministic* SAT-oracle procedure R correctly decides **all** MajMajSAT inputs of bit length N, uses at most N^b SAT queries of length at most N^a, nonoracle time N^r and retained writable space N^u. Assume one fixed uniform exact deterministic SAT subroutine uses time m^t, space m^s for each query length m, with a fully charged matching input interface and actual whole-run memory accounting. Then for *materialized* queries, with polylogarithms omitted:
\[
\theta_{\rm mat}=\max(r,b+at),\qquad
\eta_{\rm mat}=\max(u,a,as).
\]
For *virtual read-only* queries whose bits cost at most N^h per subroutine input access, with all generator/index/state storage already included in u and a separately proved physical machine simulation:
\[
\theta_{\rm virt}=\max(r,b+at+h),\qquad
\eta_{\rm virt}=\max(u,as).
\]
These are **conditional bookkeeping equations**, not a compiler construction. For any fixed 0<sigma<1, if a genuinely correct compiled uniform MajMajSAT algorithm meets theta<1+gamma(sigma) and eta<sigma **simultaneously**, with strict slack for model/logarithmic overheads, Allender Theorem 7 forbids it. If R writes Omega(N) query bits on writable tape, eta>=1 and the sublinear-space condition fails. The reverse reduction SAT -> MajMajSAT cannot transfer the lower bound to SAT.

For **bounded-error quantum** SAT subroutines, one must separately prove an adaptive error-reduced measured interface, then invoke van Melkebeek–Watson under the amplitude/constructibility assumptions; TMR-5/045 presents an O(log N) repetition and union-bound conditional template. **Unbounded-error** small-bias PP subroutines cannot be treated as reliable adaptive oracle bits.

## 6. Native exhaustive verification

Published separate source: experiments/tmr/tmr1_allender_balance049.py. Separate raw JSON: results/raw/tmr/2026-11-15_0957_TMR1_ALLENDER_BALANCE049_PY_RAW.json.

Actually executed CPython on a deterministic full truth-table grid with ell=1,2 outer bits, k=1..3 inner bits, m=1..3 auxiliary bits, ell+k<=4, all tables F. The executable directly enumerates (b,z,v), not only algebraically evaluates the formula. It checked **394,800 nested truth tables**, **1,184,352 fixed-a count/threshold equalities**, **404,592 exact inner ties**, **394,800 outer-majority decisions**, and all three negative controls. **Zero failures.** No random seed; finite evidence COMPUTATIONAL. The symbolic proof in Section 3 is all-size, pending independent peer review.

## 7. Fusion qualification, dependency statuses, peer instructions

The exact count gadget is a **Boolean relation transformation**, not a physical SAT transition system. It supplies a correct algebraic interface for majority-preserving circuit encodings, **not** an exponential-size initial fusion potential. One compact circuit edit may alter exponentially many semantic assignments. All sender/receiver semantics, AND branches, sharing, storage, input access, source authentication, zero-cost behavior, signed tariff rows and real machine work still require independent proof.

| Dependency | Status | Narrowest next task |
|---|---|---|
| Arithmetic checkpoint to LCH_tau; hierarchy collapse to Thms 3/7 | KNOWN THEOREM [1] | TMR-3 recheck exact uniformity/time-space bound and gamma slack |
| Balanced unique extension with both majority blocks | PROVED/RESTRICTED here, peer review OPEN | TMR-2 check all future 3-CNF encodings satisfy functional uniqueness and inclusive ties |
| MajMajSAT -> uniform exact SAT oracle compiler | OPEN | Construct sound compiler or identify inherent PP-vs-NP barrier |
| Compiler aggregate time/space and quantum error semantics | CONDITIONAL/OPEN | TMR-3 audit virtual input, query read costs and whole-network space |
| Cost-sound zero-cost/tariff abstraction for actual MajMajSAT machines | OPEN | TMR-4 forbid free semantic answer edges, keep all true MAY paths |
| Same-system superpolynomial SAT machine lower bound | OPEN | TMR-5 redteam all restricted model transfers |
| P != NP | OPEN | No promotion |

**Corpus audit and unchanged authority:** First read the 2026-11-15 Allender coordination directive (blob 1760aefab5944a063f64b62142e358fbd2b94235), then the fusion directive (54c9177fc211dfca6c94d89d6ebbf3f3908809d6), TMR replacement (47459817e66dccf1f3079e6c724c0fd2643e7bc4), both complete root proof trackers, full root main.tex, issue #3, AGENTS.md, CODEX.md, research skill, all five current TMR handoffs, prior TMR-1/048 record system and TMR-5/045 Allender experiment. This new exact *inner inclusive-majority* formula differs from TMR-5/045's *strict-PP bias* normalizer and does not re-claim prior work. No canonical proof-spine arrow has changed status. Historical /341 remains **FAIL** as full logical UNSAT authority and /386 remains **RESTRICTED** to its tested guarded odd-charge fragment.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 SHA 930c5eeddafce656717f28055a7a9a755f44737c, main.tex SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. No schedule or agent changes. P versus NP OPEN.

## References

[1] E. Allender, M. Koucký, D. Ronneburger, S. Roy, V. Vinay. *Time-Space Tradeoffs in the Counting Hierarchy*. CCC 2001. https://people.cs.rutgers.edu/~allender/papers/tradeoff.pdf

[2] D. van Melkebeek, T. Watson. *Time-Space Efficient Simulations of Quantum Computations*. *Theory of Computing* 8, 2012. https://theoryofcomputing.org/articles/v008a001/
