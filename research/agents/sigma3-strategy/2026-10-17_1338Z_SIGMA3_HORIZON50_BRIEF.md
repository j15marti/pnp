# SIGMA3-HORIZON50 | 2026-10-17 13:38 UTC
Statuses: PROVED/EXACT scoped results, CONDITIONAL resource theorem, COMPUTATIONAL 292762 assertions, all-input contraction OPEN, P versus NP OPEN.

PROPOSE: horizon quotient; transition-closed tag; SAT-activated delayed output; two-polarity flow and prefix controls.
SEARCH: prior ACTIVATIONRANK49, TRACEQBF_FLATTEN1, INTERFACEHELLY1, SEM_QUOTIENT_ACQUIRE1. Primary: Myhill-Nerode theory (TCS 2022 doi 10.1016/j.tcs.2022.01.015), finite-field observability (IEEE TAC 2013 doi 10.1109/TAC.2012.2204155), FLMV JACM 2005 (doi 10.1145/1101821.1101822).

EXACT: For linear transition A, output C and horizon H, O_H=stack(C,CA,...,CA^(H-1)). Two full-state checkpoints have identical YES and NO continuation responses through H iff O_H s=O_H s'. Minimum fixed tag width rank(O_H); restrict reachable initial states im(B) by rank(O_H B).

EXACT HEREDITY: A fixed linear tag Ms can update and provide output iff C=VM and MA=UM for linear V,U. Minimum stationary full-space tag rank rank(stack(C,...,CA^(w-1))). Shift-register output s_0 needs one bit for first continuation but w bits to remain exact across all w steps. Unique gate traces do not overcome delayed distinguishability.

EXACT SAT ACTIVATION: Temporal output s_j AND F(u) has one semantic class when F UNSAT, 2^w when SAT. Checking soundness of any fixed r<w all-state tag is coNP-complete on this constructed family.

CONDITIONAL: Source-certified Sigma3 blocks, q<=N^(1-lambda), child length<=N^lambda, r<=beta log2 N, certified acquisition time N^a space N^b, one guest SAT solver exponents K,L. Charged decision bounds: K'<=max(a,1+beta,1-lambda+beta+lambda K); L'<=max(b,lambda max(1,L)). At lambda=1/2,beta=1/20,a=11/10: K'<=max(1.1,1.05,0.55+K/2). Not all-input or hereditary. YES witness self-reduction and NO counterchallenge actual solver calls charged.

BUILD: 292762 Python assertions, 432 GF2 machines (275907 pair comparisons), 1350 integer/parity flows K_(k,k), 480 SAT-activation cases, prefix and gate-trace controls. Zero discrepancies.
NEXT: SAT-dependent instruction-specific reachable-state stationary quotient with explicit verifier and all resource costs.

SENTINEL_SIGMA3_HORIZON50_20261017_1338Z