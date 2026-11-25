# Hybrid DP: affine absorption and effective compatibility rank
2026-11-24 21:56 PT. Analytical iteration. P vs NP remains open.

## Exact transition
Let A have arbitrary feasible boundary set S, and B have affine feasible set b0+im H. Join by Pa+Qb=t over GF(2). Set C=QH and choose D with ker D=im C. The join is feasible at a iff DPa=D(t+Qb0). Normalize this affine filter, detecting inconsistency. Its effective rank rho=rank(DP) is the number of independent constraints imposed on A, not the raw interface rank.

Choose a linear right inverse of C on im C (extend arbitrarily to the ambient space). For compatible a, all solutions b are b0+H[R(t+Pa+Qb0)+Kq], where K spans ker C and q is unrestricted. Thus any affine output projection of the join is an affine image of the filtered nonlinear child times a free affine fiber. This proves exact reconstruction and polynomial transition cost for the affine component.

## Representative composition
For degree k, retain actual feasible witnesses whose square-free monomial feature vectors span the degree <=k evaluation space. Filtering by rho independent affine equations multiplies a degree-k test by their degree-rho indicator, so degree k+rho child representatives suffice. For a free s-bit fiber, assignments of Hamming weight <=k span degree-k features: the evaluation matrix indexed by subsets of size <=k is the subset-incidence triangular matrix with diagonal 1. Cartesian products followed by affine output mapping and Gaussian basis compression preserve degree-k features. Charge all candidate pairs, witness storage and reconstruction. For fixed k+rho, this is polynomial.

## Conditional global bound
For a supplied polynomial-size hybrid decomposition, use effective rank rho at affine/nonlinear joins, raw independent filter rank at general nonlinear joins, and zero at independent affine-image products. If the maximum sum of charged ranks along any root-to-leaf path is a fixed constant K, leaf acquisition is polynomial, and all other symbolic transitions are certified polynomial, root nonemptiness is decidable in N^{O(K+1)} time. This is a sufficient condition, not universal closure. Protected deficiency-core contraction may remove additional constraints while preserving external projections.

## Infinite-family separation
Take arbitrary nonlinear S on a in GF(2)^n and a free affine partner b in GF(2)^n, join a=b. Raw interface rank n, effective rank zero. More generally constrain b to an affine subspace of codimension c; effective rank <=c. A sequence of such free-copy joins can have arbitrarily large raw cumulative rank but zero effective rank. This illustrates why synchronized replica copies should not be charged as nonlinear filters when their free affine fibers can be eliminated. Actual nonlinear copies of S are not free affine partners.

## Barrier
A nonlinear partner can have full affine hull yet exclude a single required boundary state. Replacing it by its affine hull is unsound. In particular the always-SAT guarded construction G=AND_i(not a OR not b OR C_i) has boundary support either all four states or all except 11 depending on SAT(F). Exact acquisition remains NP-hard. Also a sequence of genuine nonlinear joins can accumulate unbounded effective rank; no universal constant bound established.

## Next target
Discover polynomially a hybrid decomposition with bounded effective compatibility budget, or a different exact matching/consensus terminal or charged contraction when that budget grows. Preserve source semantics and guard provenance. Do not claim P=NP from compact states, fixed-degree feedback, or restricted-family theorems. No new computational benchmark executed in this iteration.
