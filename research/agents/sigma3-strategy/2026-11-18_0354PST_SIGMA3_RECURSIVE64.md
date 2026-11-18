# SIGMA3-RECURSIVE64: Recursive certified separators eliminate the SAT-guest exponent on a restricted promise

**Timestamp:** 2026-11-18 03:54 America/Los_Angeles. **Status:** PROVED/EXACT scoped theorem, COMPUTATIONAL finite auditors, CONDITIONAL K/L bounds; P versus NP OPEN. Independent mathematical review pending.

## PROPOSE before SEARCH
Recorded four proposals in the reproducibility bundle before literature search: (1) verified hierarchical separator recursion; (2) SAT-dependent nonlinear guards and tiny Horn/XOR local traces; (3) YES/NO negative-witness certificate firewall; (4) source replay and z=y, parity/integral-flow and quantified-prefix adversarial controls.

## SEARCH and prior art
Reviewed repo SEP63, PHLEDGER62 and proof1.txt. One-level tagged block compression, clause-index QBF encoding, and K/L conditional guest estimates are PRIOR PROJECT WORK. Literature: Mählmann-Siebertz-Vigny, *Recursive Backdoors for SAT* (arXiv:2102.04707); Dreier-Ordyniak-Szeider, *SAT Backdoors: Depth Beats Size* (JCSS 142, 2024, DOI 10.1016/j.jcss.2024.103520); Samer-Szeider, incidence-treewidth #SAT (arXiv:cs/0610174); Cook-Reckhow, *Relative Efficiency of Propositional Proof Systems* (JSL 1979, DOI 10.2307/2273702); Fortnow-Lipton-van Melkebeek-Viglas, SAT time-space lower bounds (JACM 2005, DOI 10.1145/1101821.1101822). This is a scoped project synthesis, not a new general theorem about backdoors.

## Theorem A: Exact hereditary recursion under a *verified source grammar*
Suppose a CNF carries a mechanically verified rooted separator hierarchy. At every node of original/padded encoded size n, separator S has |S| <= beta log2(n); after assigning S, clauses separate into disjoint private children of total sizes <=n and each size <=C n^lambda, for fixed 0<lambda<1; all leaves have constant-size complete source. Every clause has a unique persistent owner. The source-level certificate is verified, not trusted; restrictions retain original owner IDs and padded node measures.

For each boundary assignment a, test local clauses and all independent children; accept if at least one a makes all children SAT. TRUE gives a common boundary commitment and merged private witnesses. FALSE gives, for **each** a, either a falsified local clause or a specific failing child with a recursively checkable NO proof. NO is never assumed free. This is an exact induction, and NO proof trees are polynomial-sized under the structural promise.

For node-local access,
  T(n) <= n^beta [O(n)+sum_i T(n_i)].
Since sum_i n_i^p <= (max_i n_i)^{p-1} sum_i n_i <= C^{p-1} n^{1+lambda(p-1)}, every p>1+beta/(1-lambda) gives
  **T(N) <= N^{1+beta/(1-lambda)+o(1)}**.
Naive full-root source replay per visited node costs at most an additional factor N, so N^{2+beta/(1-lambda)+o(1)} is a conservative sequential-replay upper. The simpler physical indexed-source implementation charges O(N) simultaneous writable memory. Other smaller-space access models require explicit layout verification.

**Key new insight:** If the strict sublinear separator grammar truly holds *recursively down to constant leaves*, there is NO remaining SAT oracle call. The one-level lambda*K coefficient disappears entirely. With beta=.1,lambda=.5 this restricted algorithm has an ideal node-local exponent 1.2, not 0.6+0.5K. Efficient all-CNF acquisition of such a tree would instead yield P=NP; it does not prove P!=NP. Certification feasibility for arbitrary CNF remains OPEN.

## Theorem B: One-level conditional K/L exact ledger
For a *top-level only* verified separator, children remain arbitrary Circuit-SAT. Let one uniform correct SAT machine A use m^{K+o(1)} time and m^{L+o(1)} writable space, K>=1. With all child sizes summing to O(N), maximum child N^{lambda+o(1)}, and verification cost N^{a+o(1)},
  T_dec <= N^{max(a,beta+1-lambda+lambda*K)+o(1)}.
All actual YES/NO child calls and O(N^{beta+1}) source serialization scans are charged. Complete witness extraction by SAT self-reduction has
  T_wit <= N^{max(a,beta+1-lambda+lambda*K,1+lambda*K)+o(1)}.
Single-machine peak writable space is conservatively N^{max(1,lambda*L)+o(1)} when a full source/index is materialized. Under a physically justified read-only indexed source it could be N^{lambda*max(1,L)+o(1)} plus traversal state. No forbidden DTISP region follows.

## Exact firewalls
(1) Externally checkable polynomial NO certificates for **all** unrestricted Circuit-SAT instances imply UNSAT in NP and hence NP=coNP, not automatically P=NP. Restricted separator NO trees carry no general result.
(2) For Phi=exists x forall y exists z C, x must be committed once globally; independently choosing x for each y solves a different prefix. exists x forall y[x=y] is FALSE, while forall y exists x[x=y] is TRUE.
(3) In the previous clause-index encoding, Phi_F=exists x forall j exists z [z=g_F(x,j) AND z=0], where g_F is the clause-falsification bit, is TRUE iff SAT(F). Even though the local trace z is unique and tiny, finding global x is SAT-hard and a losing j can depend on x.
(4) z=y, GF(2) K_{r,r} parity systems, and signed integral-flow conservation are explicit easy-strategy controls regardless of graph width. AND is non-affine and blocks unrestricted Gaussian elimination.
(5) Recompacting an already restricted parent may invalidate the strict **relative** child-size exponent; original-source padding and ownership remain essential.

## Finite adversarial audit
Primary Python (fixed seed 20261118035464): **25,420 assertions, zero discrepancies**. 232 structured cases (224 tiny exhaustively checked and 8 larger planted), 144 tiny SAT and 80 tiny UNSAT, 144 independently verified YES assignments, 80 independently checked recursive NO proof trees, five two-round source restrictions, 420 random GF(2) matrices with primal/dual certificates, four K_{r,r} parity+signed integral-flow controls through r=13, 350 nonlinear quantified clause-index cases (294 TRUE/56 FALSE), 300 arbitrary source candidates rejected by the tested fixed certificate, and three dense positive pairwise-CNF separator failures.
Independent JavaScript: **64,066 assertions, zero discrepancies**, including 280 structured exhaustive comparisons, 280 actual two-round restrictions, 240 random unstructured source-rejection controls, 350 nonlinear quantified cases, z=y and prefix falsifiers.
Total 89,486 assertions, zero discrepancies. Largest planted source had 1,036 clauses; largest observed child/parent ratio 0.7023809524 (finite observed ratio, NOT an asymptotic exponent). All counts are implementation checks, not lower bounds.

## NEXT
Stress **certificate acquisition**, not just verification: SAT-dependent nonlinear selection of mixed Horn and XOR residuals; build two-stage sources whose original padded size inherits the verified grammar while active-byte reserialization breaks it. Find whether a cheap source-only acquisition algorithm succeeds on every CNF; record failing source family, recursive tree proof size, exact both-polarity strategies, source scans, and SAME-MACHINE peak writable space. An all-input claim requires a genuine acquisition/closure theorem and must address the consequence P=NP.

**OPEN:** all-CNF efficient acquisition; all-input hereditary lambda<1; forbidden simultaneous DTISP region; P versus NP.

SIGMA3_RECURSIVE64_20261118_0354PST_READBACK_SENTINEL
