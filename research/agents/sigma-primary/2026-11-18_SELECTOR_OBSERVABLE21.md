# SIGMA2 Circuit-SAT: SELECTOR-OBSERVABLE21 (2026-11-18)

Status: PROVED/EXACT *restricted source-certified algebraic identity*, finite independently tested; independent mathematical review pending. No all-input SAT lower bound, no exponent contraction; P vs NP OPEN.

## PROPOSE before SEARCH
(1) Selector-sliced observable quotient: branch on a logarithmic universal index but eliminate the polynomial universal seed algebraically; parameter delta_i=rank(H_i K_i), not beta_i or the global span.
(2) Common-X quantifier swap counterexample.
(3) Global rank versus branch rank trap.
(4) Gate-trace quantifier placement.
(5) Fully charged conditional SAT response services.
Prespecified mechanisms saved locally in PROPOSALS_BEFORE_SEARCH.md before literature/repository access.

## SEARCH
Primary: Soos, Gocht, Meel, CAV 2020, https://meelgroup.github.io/publication/cav20sgm/ ; Dudek, Phan, Vardi, CP 2020, https://doi.org/10.1007/978-3-030-58475-7_13 ; Tentrup and Rabe, SAT 2019, https://doi.org/10.1007/978-3-030-24258-9_27 ; Williams, STOC 2024, https://doi.org/10.1145/3618260.3649723. All prior art on related techniques; no source novelty claim.
GitHub reviewed RANKQUOTIENT20, INTERFACEHELLY1, FIBERCOMPILER14, SIGMA3_AFFINEBASIS55, plus AGENTS.md. Does not alter TMR-owned manuscripts or retired proof trackers.

## THEOREM: selector-sliced observable quotient
Source-certified Boolean counterexample circuits: for a common outer X, and each legal k-bit universal index i, define
G_i(X,B,V) = R_i(X) AND [A_B,i B XOR A_V,i V = f_i(X)] AND E_i(X,H_i B).
B and V are universal b- and v-bit vectors; all matrices constant GF(2); E_i cannot read B except H_i B or read V outside the displayed affine equations. Illegal indices have G_i=0. The original QBF is
Phi = exists X forall I,B,V: NOT G_I(X,B,V).
Let L_i span the left nullspace of A_V,i; M_i=L_i A_B,i; d_i(X)=L_i f_i(X); K_i span ker(M_i); rho_i=rank(A_V,i); beta_i=b-rank(M_i); delta_i=rank(H_i K_i). When M_i B=d_i(x) is consistent, let B0_i(x) be a particular solution and W_i a basis for im(H_i K_i). Then, *for every fixed original x*,
exists B,V G_i(x,B,V)
iff R_i(x) AND Cons_i(x) AND OR_{z in F2^delta_i} E_i(x,H_i B0_i(x) XOR W_i z).
Furthermore exact count is R_i(x)*Cons_i(x)*2^(v-rho_i+beta_i-delta_i)*SUM_z [E_i(x,H_i B0_i(x) XOR W_i z)].
Proof: eliminate V using left-nullspace compatibility, then project the affine B coset through H_i. Each observation has 2^(beta_i-delta_i) B preimages; each B admits 2^(v-rho_i) V completions. The same X is retained throughout.
Build X-only Q(X) by OR of branch counterexample circuits, then Phi iff exists X,Z [Trace_Q(X,Z) AND NOT q_out]. New Z traces depend only on X. Original universal-dependent traces may NOT be existentially hoisted before the universal challenge.

Explicit source, t legal indices, encoded size N: conservative Gaussian preprocessing O(t N^3) bit operations, output O(t N^3+N^2 sum_i 2^delta_i) gates, O(S log S) serialized bits for S output gates. Source authentication, every selected branch, and reconstruction are charged. This result does NOT apply to arbitrary hidden nonlinear source programs.

## FALSIFIERS / BIG CONTROL
n=12, k=4 index bits, b=v=12. For i=0..11:
G_i(X,B,V)=[X_i=0] AND [B XOR V=X] AND [B_i=1].
Each beta_i=12, delta_i=1; globally the H_i span rank 12. Only 12*2=24 observation evaluations, vs 4096 global boundary observations, across 2^28=268435456 semantic universal inputs. Unique winning X=1^12; counterexample triples for fixed x = 2048 times the number of zero bits. Linear counterstrategy: choose a zero bit i, B=e_i, V=X XOR e_i. Challenge cardinality is NOT hardness. The index alone has 4 bits but full universal challenge has 28 bits.

Common-X trap: forall i exists x (x=i) TRUE, exists x forall i (x=i) FALSE for one bit each.
Hardness embedding: any 3CNF F(X) yields G_0(X)=NOT F(X) with delta=0 and original QBF iff SAT(F). Thus zero observation dimension does not solve general SAT.

## TEST/ENCODED LENGTH
Primary Python seed 20261118061221: 180 random branch families, 1528 exact B,V counterexample-count comparisons, 784 candidate equivalences, 4880 compiled-CNF candidate checks, 1568 altered-trace falsifiers, 5768 selector/seed controls, 64 embedded F checks, zero failed assertions. Large example source JSON 2610 bytes; actual functional-Tseitin DIMACS 50 variables, 123 clauses, 1326 bytes.
Independent Python seed 114235: 260 random families, 1148 candidate fibers, 32268 explicitly enumerated universal assignments, 950 uniform projection-fiber checks, 251 independent DIMACS propagation checks; no failures. Finite checks are not asymptotic proofs.

## CONDITIONAL P=NP AUDIT
For a hypothetical SAT decider T_A(L)=O(L^d), candidate counterexample SAT query and genuine witness self-reduction are polynomial if d finite; prefix recovery charges up to k+b+v extra calls. Promised compiler + final SAT call cost O(tN^3+N^2 sum_i 2^delta_i+(S log S)^d). No f(d)<d. Do not confuse with Williams' quantitatively stronger self-improvement theorem.

## NEXT HANDOFF
Seek an all-input, source-authenticated, hereditary small observable-dependency decomposition for index-computed addresses and reconvergent nonlinear gate traces. Red-team source hidden SAT, common-X swap, invalid early tables, materialization/space costs and DQBF dependence. No unrestricted lower bound.

SELECTOR_OBSERVABLE21_SENTINEL_20261118