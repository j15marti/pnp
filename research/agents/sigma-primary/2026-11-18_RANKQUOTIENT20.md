# SIGMA2 CIRCUIT-SAT: RANKQUOTIENT20 (2026-11-18)

Status: PROVED/EXACT source-restricted projection, independently tested; no general SAT exponent contraction; P versus NP OPEN.

PROPOSE before SEARCH: affine-quotient boundary projection, rank-trap countermodel, witness reconstruction with common X, log-selector/long-seed distinction, fully charged SAT solver audit.

SEARCH primary: Soos-Gocht-Meel CAV 2020 (DOI 10.1007/978-3-030-53288-8_22); Dudek-Phan-Vardi CP 2020 (DOI 10.1007/978-3-030-58475-7_13); Eriksson et al. QBF Backdoors 2026 (arXiv:2604.15927); Williams STOC 2024 (DOI 10.1145/3618260.3649723); FLMV JACM 2005. SEARCH project: INTERFACEHELLY1, PHABSORB1, FIBERCOMPILER14 were fetched and reviewed. AFFINE_ANOMALY19 and SYMBOLIC_ELIM18 exact-name repo search had no hits; compared against thread handoffs.

THEOREM: For source-certified G(X,B,V)=R(X) AND [A_B B + A_V V=f(X)] AND E(X,B), with R,f dependent only on X and V absent from E, let L span ker(A_V^T), M=L A_B, beta=b-rank(M)=b-rank([A_B A_V])+rank(A_V). For each x, exists B,V G iff R(x) AND Cons(M B = L f(x)) AND OR_{z in F_2^beta} E(x,B0(L f(x))+Kz), K basis ker(M). This is an exact candidate-preserving identity. Gaussian elimination O(N^3) preprocessing, X-only circuit O(N^2+N*2^beta) gates, functional Tseitin 3-CNF. Original universal-dependent gate traces remain after universal Y; only new H(X) traces become existential.

LARGE CONTROL: b=8, v=16, eight equations B_i+parity(V)=X_i, E=(B0 OR B1 OR B2) AND (not B0 OR not B1 OR not B2). rank(A_V)=1, rank(M)=7, beta=1. 2^24 semantic challenges, exactly two compatible B for each x and 2^15 V extensions per B. The counterexample-fiber condition is NAE(X0,X1,X2); 192 losing X, 64 winning X. Actual generated winning 3-CNF: 60 variables, 163 clauses, 1,782 DIMACS bytes; 3-bit selector plus 21 other universal bits is not a 3-bit challenge.

RANK TRAP: A_B=A_V=I_8 has rank(A)=8, rank(A_V)=8, but beta=8, so total affine rank does not control the quotient. X-only arbitrary SAT can remain NP-complete even for beta=0.

EXACT COUNT: If rho=rank(A_V), each compatible boundary B has 2^(v-rho) reservoir completions, giving #G(x)=R(x)*2^(v-rho)*sum_{z in F_2^beta}[E(x,B0+Kz)] for consistent x, and zero otherwise. The extended local verifier checked 18,286 exact counterexample-fiber counts against brute force. The large NAE case has 65,536 counterexamples per losing candidate, precisely 1/256 of its 2^24 universal challenges.

TESTS: 2,016 exhaustive cores, 16,128 candidate/RHS fibers; 420 randomized cores, 1,902 candidate fibers, 225 reconstructed witnesses, 256 large-case fibers. Independent image-enumeration and pinned-X DPLL: 2,392 checks, zero failed. An initial witness-index bug detected in development was fixed and both scripts rerun.

P=NP charge: SAT solver O(L^d) yields O(N^3+S log S+(S log S)^d), S=N^2+N*2^beta; for beta<=alpha log_2 N the exponent is max(3,d*max(2,1+alpha)). No f(d)<d; no all-input or hereditary theorem.

HANDOFF: discover and certify source decomposition and hereditary beta bound without having first decided the instance; red-team dense A=[I|I], source-hidden 3-SAT, DQBF dependencies, common-input UWI, compact strategy and PHABSORB1. All-input P versus NP OPEN.

Verification source and full report produced as local run artifacts, not included in this abbreviated GitHub entry.

RANKQUOTIENT20_SENTINEL_20261118