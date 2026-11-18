# SIGMA3-ORDERPAD67: Fixed-outer OBDD templates vs exponential global order, padding firewall

**Research date:** 2026-11-18 10:07 PST, America/Los_Angeles.
**Status:** PROVED/EXACT for scoped reductions and specified-order ROBDDs (independent review pending); COMPUTATIONAL finite tests; CONDITIONAL K/L resource bounds; **P versus NP OPEN**.

## PROPOSE BEFORE SEARCH
Four concrete alternatives recorded in local IDEAS_BEFORE_SEARCH.md before searching: (A) fixed-x two-variable guard OBDD versus full-source ROBDD order width; (B) nonlinear SAT-driven Horn/GF(2) guard selection; (C) high-treewidth parity/integer-flow tractability controls; (D) exact YES/NO continuation, trace uniqueness, prefix and witness-extraction audit. Selected A with added padding-normalization firewall.

## SEARCH / ORIGINAL PROJECT AND PRIMARY LITERATURE
Original source inspection: j15marti/pnp handoffs TEMPLATE66 (2026-11-18_0804PST), GUARD65 (0551PST), RECURSIVE64 (0354PST), and proof1.txt. Existing two-template SAT embedding, coNP-hard winning-strategy verification, and authenticated separator grammar are PRIOR PROJECT WORK. Literature search: Bryant 1986, Wegener 2000 OBDD order/cut methods, Schaefer STOC 1978, Fortnow-Lipton-van Melkebeek-Viglas JACM 2005. No claim of new general OBDD or SAT lower bound.

## THEOREM A: Exact two-challenge Sigma3 SAT encoding
For arbitrary explicit 3CNF F(u) (source length M), existential m-bit arrays a,b, universal bits s,t, and one existential continuation z, define
  E_m(a,b) := AND_i (a_i <-> b_i),
  g_F(u,a,b,s,t) := ((NOT F(u)) AND s) OR ((NOT E_m(a,b)) AND t),
  Phi_F := EXISTS u,a,b FORALL s,t EXISTS z: [z=g_F] AND [z=0].
Then **Phi_F TRUE iff F SAT**. Proof: challenges (s,t)=(1,0) and (0,1) separately force F(u)=1 and a=b. If F SAT, choose u satisfying F, a=b=0, z(s,t)=0. If F UNSAT, (s,t)=(1,0) defeats every outer x, with local inconsistent constraints z=1 and z=0.

For each fixed outer x=(u,a,b), the y=(s,t) guard is exactly one of 0, s, t, s OR t, hence a <=2-decision-node reduced OBDD. Each fixed x,y has a unique forced gate trace z=g, but winning existential commitments may be multiple. A wrong x has genuine counterchallenge (1,0) if F(u)=0 and (0,1) if F(u)=1 and a!=b. Validating the fixed universal strategy (1,0) wins for EVERY outer x is coNP-complete because it holds precisely when F UNSAT. Local counterchecks are NOT global UNSAT certificates without a charged SAT/UNSAT decision or separate proof.

## THEOREM B: Exponential **prescribed-order** global OBDD, hereditary for two restrictions
Take fixed variable order (u_1,...,u_p, a_1,...,a_m, b_1,...,b_m, s,t). Fix any u. Distinct a and a' induce distinct residual functions of (b,s,t): on b=a,s=0,t=1 the residual for a is 0 and the residual for a' is 1. Thus any ROBDD respecting the prescribed order needs >=2^m residual states across the a|b cut. Even with r a-bits fixed (and all b free), >=2^(m-r) distinct residuals remain; this holds irrespective of F satisfiability. This is the standard OBDD residual-function / one-way equality argument, not a Turing-machine or general circuit lower bound.

With interleaved order (u,a1,b1,...,am,bm,s,t), the equality portion is only O(m) ROBDD nodes, and when F is small/simple the entire guard is O(m). Thus the exponential bad-order property is readily evaded by reordering. Choosing a=b existentially makes equality trivial; it does not make the SAT residual smaller.

## THEOREM C: Padding normalization defeats a fake fractional lambda
Take m=M^2 independent equality pairs. The full source N is Theta(M^2 log M) in ordinary bit-encoded gates/variable IDs (Theta(M^2) in unit-cost gate count), while the *only hard SAT guest* remains F of size M = N^(1/2+o(1)). This apparently achieves lambda=1/2, but the reduction blows up the original size by delta=2+o(1); after expressing costs in M, guest exponent is delta*lambda*K=K+o(1), no speedup. Materializing the padded source already costs M^(2+o(1)) time. More generally one must normalize delta*lambda, account for acquisition/serialization, and prove a forbidden SAME-MACHINE time-space pair. This representation/padding example establishes no general lower bound.

## SAT A WITH K,L; EXACT CONTINUATIONS
For a single fixed uniform SAT decider A with time q^(K+o(1)) and writable space q^(L+o(1)), K>=1, L>=0, decide Phi from explicit source length N using ONE charged A(F) query of size M<=N:
  T_dec=O(N + M^(K+o(1))),
  S_dec=O(N + M^(L+o(1)))   (one reused full-source/query buffer).
Recover winning u with at most |u|+1 <= M+1 sequential actual YES/NO SAT calls on pinned F, charging all negative answers:
  T_wit=O(N + M^(K+1+o(1))),
  S_wit=O(N + M^(L+o(1))).
Then choose a=b=0 and z(s,t)=0. For false instances, an actual A(F)=NO decision (or valid UNSAT proof) is required to certify constant Herbrand (1,0). Source replay and materialization counted. If M=N^lambda, the visible N-time exponent max(1,lambda*K) is illusory from the original M perspective when delta*lambda=1. For ORIGINAL unpadded SAT self-reduction, lambda=1 and the usual K+1 exponent persists. P versus NP OPEN.

## FINITE ADVERSARIAL AUDIT
Python Python3 standard-library file audit67.py: 440 exhaustively checked small quantified formulas (184 true, 256 false); 236,558 genuine local Herbrand counterchallenges; 20 actual ordered/reordered ROBDDs for m=1..10 with two literal pins; 750 random GF(2) primal/dual (307/443), verified signed integer and GF(2) flow controls on K_(r,r) for r=3..14; z=y, nonlinear AND, unique trace, and prefix reversal. FINAL: **2,445,295 assertions, zero discrepancies**. An early integer-flow fixture had omitted the hub edge; repaired and fully rerun, final results only.

Independent Node JavaScript file independent67.js: 350 independently exhaustively evaluated quantified cases (162 true, 188 false); 348,500 distinguishability pairs and 21,590 after two a-bit restrictions; numerical padding normalization M=128..4096; prefix controls. FINAL: **2,583,971 assertions, zero discrepancies**. Combined **5,029,266 assertions, zero discrepancies**, finite implementation checks only.

Measured ROBDD m=10:
* F satisfiable: 6144 bad-order nodes, 66 interleaved nodes, 2048 prefix residuals (512 after two pins).
* F unsatisfiable: 3072 bad-order nodes, 33 interleaved nodes, 1024 prefix residuals (256 after two pins).
Source-physical sizes and effective exponent must be compared against M rather than padded N.

## STATUS / NEXT EXPERIMENT
PROVED/EXACT (scoped, review pending): Sigma3 equivalence; constant fixed-x y-guard templates; prescribed-order ROBDD 2^m residual distinction, hereditary with pins; padding exponent identity. COMPUTATIONAL: finite Python/JS audits. CONDITIONAL: K,L same-machine ledger. OPEN: uniform general Circuit-SAT solver-dependent hereditary query contraction with delta*lambda<1 and acquisition cost below target, full negative-answer and global strategy validation, forbidden SAT DTISP region, P != NP.

NEXT: Let quotient acquisition choose optimized variable order OR alternative source representations, and attach a SAT-dependent nonlinear Horn/GF(2) selector. Test two real recursive restrictions without padding. Measure effective query exponent on original M, YES and NO witnesses, certificate cost, rereads, and simultaneous space. The immediate falsifier for the current representational obstruction is the interleaved equality order.

## REPRODUCIBILITY
Detailed report, before-search proposals, Python auditor, independent JS auditor, JSON results, README, BibTeX in the conversation artifact SIGMA3_ORDERPAD67_20261118_bundle.zip (SHA256 94e0d463879e0a95ae421395e3eabf4ba7e9c9aaeaa3b480458cf093a03ec5fb).
Report SHA256 2ec7624015f1a9161c481b4cec77d3bbd31484ab9635d7b6ad955e44ca5da76f.

## PRIMARY REFERENCES
[1] Bryant, Graph-Based Algorithms for Boolean Function Manipulation, IEEE Transactions on Computers (1986), doi:10.1109/TC.1986.1676819.
[2] Wegener, Branching Programs and Binary Decision Diagrams (SIAM 2000), doi:10.1137/1.9780898719789.
[3] Schaefer, Complexity of Satisfiability Problems (STOC 1978), doi:10.1145/800133.804350.
[4] Fortnow et al., Time-Space Lower Bounds for Satisfiability (JACM 2005), doi:10.1145/1101821.1101822.

FINAL-SENTINEL-SIGMA3-ORDERPAD67-OPEN
