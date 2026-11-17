# SIGMA3-AFFINEBASIS55: tight affine universal-challenge basis and two-sided strategies

**Timestamp:** 2026-11-18 05:31 Asia/Seoul. **Status:** PROVED/EXACT *restricted algebraic lemma* (independent mathematical review pending); COMPUTATIONAL finite audit; general P vs NP OPEN.

## PROPOSE
(1) Collapse an arbitrary-length universal affine challenge to a basis while maintaining the globally committed x. (2) Construct both YES Skolem strategies and NO Herbrand/linear-dual certificates. (3) Test unique nonlinear gate traces and deliberately nonlinear universal guards. (4) Audit K,L costs and whether this gives lambda<1 for any all-input recursive transformation.

## SEARCH
Project: SIGMA3-MIX54, SIGMA3-SWITCHGUARD52, proof1.txt, proof2.txt, AUTOENC-SIGMA3-1 handoff, RANKQUOTIENT20. Relevant prior art: Schaefer (STOC 1978) https://doi.org/10.1145/800133.804350; Balabanov et al. (AAAI 2015) https://doi.org/10.1609/aaai.v29i1.9750; Eriksson et al. (May 2026) https://arxiv.org/abs/2605.12073; Fortnow et al. (JACM 2005) https://doi.org/10.1145/1101821.1101822. **Affine QBF tractability is established prior art; no new general complexity classification is claimed.**

## THEOREM A: exact affine challenge basis
Given explicit matrices A(mxp), B(mxnx), C(mxny), vector d over GF(2), let
Phi = exists x forall y exists z: A z = B x + C y + d.
For fixed x, all challenges y are satisfiable **iff** y=0 and all unit-vector challenges y=e_j are satisfiable. Proof: solvability at zero means Bx+d in im(A); subtract the zero RHS from each unit RHS to obtain C_j in im(A), and use linearity.

Let L be a row basis for ker(A^T), D=LB, P=LC, e=Ld. Exact decision identity:
**Phi TRUE iff P=0 and linear equations Dx=e have a solution.**

## THEOREM B: complete strategies
TRUE: select x* solving Dx=e, solve A z0= Bx*+d and A zj=C_j for each j, then use Skolem z(y)=z0+SUM_j y_j zj. Appended functionally determined AND/XOR traces retain uniqueness, but constraints requiring a nonlinear gate to be 1 are NOT covered.

FALSE if P!=0: choose i,j with P[i,j]=1. For any x choose y(x)=0 if (Dx+e)_i=1, otherwise y(x)=e_j. The fixed dual vector u=L_i satisfies u^T A=0 and u^T(Bx+Cy(x)+d)=1, proving no z exists. FALSE if P=0 and Dx=e is inconsistent: choose y(x)=0, and for each x choose the first i with (Dx+e)_i=1 and dual u(x)=L_i. No negative certificate is free.

## THEOREM C: tightness in the BLACK-BOX affine oracle model
A deterministic tester receiving only evaluations of whether an **unknown** affine Boolean function g(y) is zero needs at least ny+1 queries to prove it is identically zero. With at most ny zero replies, a nonzero affine function can vanish at all queried points by linear algebra in ny+1 unknown coefficients. The zero vector and ny units attain the bound. **This is NOT a computational time/space lower bound when source matrices are readable.**

## Non-affine and prefix counterexamples
Replace the affine RHS by an arbitrary CNF gate F(y) in 0=F(y). Then Phi is TRUE iff F is UNSAT, despite locally trivial linear checks and unique gate traces. F(y)=AND_j y_j (ny>=2) passes every zero/unit basis test yet fails at y=all-ones. A mandatory F(x) guard over an otherwise trivial affine system gives SAT(F). Prefix swap trap: exists x forall y: x=y is FALSE, whereas forall y exists x: x=y is TRUE.

## Quantitative SAME-MACHINE ledger
Exact matrix-only decision by uniform Gaussian elimination: coarse upper bounds T<=N^(3+o(1)), writable S<=N^(2+o(1)); materializing full affine Skolem coefficient table by separate RHS solves: T<=N^(4+o(1)), S<=N^(2+o(1)). Zero SAT guest calls on the restricted entire-affine matrix language.

If P=NP and fixed A decides SAT in N^(K+o(1)) time, N^(L+o(1)) space, standard uniform circuitization gives coarse general Sigma3 bounds: decision N^(K^3+o(1)); extract global winning x N^(K^3+1+o(1)); extract local z(x,y) N^(K+1+o(1)); construct genuine counterchallenge y(x) N^(K^2+1+o(1)). Materialized children, failed calls, source rereads, and live buffers are charged. For q<=N^theta source-certified guests of length N^lambda with N^alpha tag values and N^delta universal tuples, K'<=max(a,rho,alpha+delta+theta+lambda K)+o(1), L'<=max(b,sigma,lambda max(1,L))+o(1) where a,b,rho,sigma explicitly charge acquisition, rereads and buffers. Prior restricted AUTOENC-SIGMA3-1 reaches lambda=1/2 but its child grammar is not hereditary; the new affine algorithm has zero SAT children ONLY under its strong syntax promise. No all-input reduction and no forbidden DTISP pair.

## BUILD/TEST
Seed 202611180525, Python 3 standard-library auditor. 1052 small Sigma3 affine instances independently exhaustively checked (386 TRUE; 540 universal-sensitive FALSE; 126 global-incompatible FALSE); 4060 fixed-x basis/all-challenge checks; 320 black-box affine adversaries; 2514 dual NO certificates; 1163 YES Skolem and unique nonlinear trace checks; 450 primal-dual GF(2) controls; K_(k,k) high-treewidth parity 24, signed integer flows 360 including 5400 vertex checks; 360 SAT-guard CNFs and 400 nonlinear-RHS CNFs; nine AND(y) basis failures; one prefix swap trap; **0 discrepancies**. Python checks are not native FLMV machine resource experiments or asymptotic lower bounds.

Local standalone auditor SHA256: 17a8167d10f99e4775f03d76c4b228e9954a8938b03d127256ff8e21393567dc
Raw-results SHA256: 2a4c18984eecbbaea395c3999deb12c62b41a9dece575dc6e3fe6c3df912e883
Local bundle SHA256: 0c6872281e03a7fdb4ff986c4da495f6a266ad0e239c70647c0258162109bcab

## Next experiment
Authenticate a mixed source with k nonlinear universal control bits; for each setting eliminate all remaining universal affine bits by the basis theorem, and charge 2^k branches, exact YES/NO dual certificates, source replay, and child encoding. Test against SAT-guarded indirect addressing, AND(y), MIX54 Horn/affine join and expander source nonclosure. Target hereditary children N^lambda with lambda<1 on **all input** SAT, not merely this affine promise. P versus NP OPEN.

END_SIGMA3_AFFINEBASIS55_20261118