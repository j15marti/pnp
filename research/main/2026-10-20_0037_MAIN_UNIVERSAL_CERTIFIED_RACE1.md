# UNIVERSAL-CERTIFIED-RACE1 | Fastest-correct SAT solver and proof-path allocation

Date: 2026-10-20 Asia/Seoul. **P versus NP: OPEN.**

## New user allocation

Five existing hourly roles remain at :00 MCSP hardness magnification, :12 certified universal fastest-correct algorithm, :24 ARC/FLMV charged contraction, :36 adversarial red team, :48 synthesis. Only two proof paths remain active: (1) MCSP magnification and (2) ARC/FLMV. The temporarily disabled :24 role was re-enabled, no new tasks created, unrelated work remains paused. GitHub failure never pauses research: shared Google Docs fallback applies.

## IDEAS BEFORE PRIMARY LITERATURE

(1) Choose fastest correct solver separately for each instance; (2) enumerate provably-correct algorithms and time-share by description length; (3) preserve same one-way-input/one-work-tape or random-access machine resource bound for the portfolio; (4) convert portfolio speed to valid MCSP threshold descent or an ARC hereditary contraction. Attack hidden hardcoded answers, proof-unprovability, delayed/padded deciders, tape replay, peak memory, and impossible promises.

## Theorem A: INSTANCEWISE-FASTEST-CIRCULARITY1 (exact)

For *every* decidable Boolean language L and *every* input x of encoded length N, there is a globally correct total program p_x of size O(N) running in O(N) steps ON x: hardcode x and the bit L(x); compare a supplied input with x, return the hardcoded bit on equality, and otherwise run a fixed correct brute-force decider. Hence min over all total globally correct algorithms p of T_p(x) is O(N), regardless of whether L is in P. This is **not** a uniform efficient solver: p_x depends on x and already contains L(x). A computable uniform SAT algorithm with polynomial overhead versus this unrestricted per-input optimum would itself put SAT in P. The desired fastest-instance oracle cannot be assumed free.

## Theorem B: CERTIFIED-UNIVERSAL-DOVETAIL1 (exact in defined guest-step accounting)

Fix a recursively axiomatized arithmetic theory T sound about program termination and SAT correctness. A self-delimiting q encodes a program p and a formal T-proof that p is total and decides SAT correctly on EVERY input. Include a fixed certified exhaustive solver q0.

Algorithm U_T(x), stage j=1,2,...: enumerate codes q of length b<=j; restart proof verification; if verified, simulate p(x); give q exactly 2^(j-b) *total simulated guest steps*, including proof check. Return the first output of any verified program. T-soundness makes YES and NO both correct; q0 ensures termination.

For fixed certified q length b, proof-check work v_q and candidate runtime t_p(x), choose stage j=b+ceil(log2(v_q+t_p(x))). It returns by then. Total guest work through stage j is at most
  sum_{k<=j} sum_{ell<=k} 2^ell 2^(k-ell)
 =sum_{k<=j} (k+1)2^k = O((j+1)2^j).
Therefore
  T_U^guest(x) = O(2^b(v_q+t_p(x)) (b+log2(v_q+t_p(x))+1)).
This is an **abstract simulated-work** result. Full code enumeration, interpreter simulation, one-way input replay, proof checking and peak simultaneous/work tape must be charged to obtain CHMY/FLMV time-space bounds.

Hutter (2002) already gives a stronger near-fastest construction within the **provably-correct and provably time-bounded** algorithm class (factor five plus program-specific additive overhead). Blum (1967) gives recursively computable functions with arbitrarily improvable program runtimes, but not a SAT-specific lower bound.

A fixed T-provably-correct polynomial SAT algorithm yields polynomial abstract work for U_T. Crucially, P=NP alone does **not** supply such a fixed-T formal proof, and even when it does the winner's unknown exponent K is not thereby reduced.

## Exact model and implication guards

* CHMY: randomized two-sided error one-way read-only input and one-work-tape MCSP at a larger specific threshold; no new both-promise high-to-low-beta compiler or same-machine universal portfolio.
* OPS: Gap-MCSP lower-bound premise must hold for every sufficiently small beta in the prescribed nonuniform circuit model, not an abstract universal interpreter.
* FLMV/ARC: the conditional time-space recurrence still lacks the arbitrary-decider all-input hereditary stage in one deterministic random-access realization. Racing can increase peak writable state and replay costs; K is not absorbed just by taking the fastest correct member.
* An unverified candidate that says UNSAT cannot be trusted. Generic witness checking confirms SAT-YES but not arbitrary UNSAT-NO without further certificates.
* Individual hardcoded p_x programs have code length O(N), so the factor 2^b may be exponential; their 'fast' execution does not make U_T fast.

## Executable bounded control

Complete standard-library reproducible code and machine-readable results are in the downloadable research package. Exhausted 256 three-variable proper-width-three clause-subsets. Four bounded-universe correct programs were accepted, two incorrect always-YES/NO programs rejected. Certified race produced 256/256 correct decisions, 1,024 per-candidate controls, no discrepancies. Winners: brute 255 inputs, special guarded program 1 input. Maximum *abstract guest steps* 17. Exhaustive finite certification is a toy surrogate, not a proof of correctness for unbounded SAT.

## DAG / priority

ESTABLISHED: unrestricted per-instance best can be O(N) via hardcoding; exact scoped proof-certified dovetail and abstract-work bound; prior Hutter result.
COMPUTATIONAL: bounded 256-instance finite audit, zero failure.
CONDITIONAL: if fixed T proves a polynomial SAT decider, then U_T uses polynomial abstract guest work.
OPEN: any useful MCSP same-one-tape threshold descent rho>lambda; fixed-T provability under P=NP; jointly bounded certified universal race; all-input ARC contractor.
RETIRED: free omniscient fastest-instance choice, unverified first NO answer, generic race eliminates unknown exponent K, direct MCSP/FLMV model transfer.
P versus NP OPEN.

NEXT LEMMA: CERTIFIED-PORTFOLIO-SAME-REALIZATION2. Explicitly charge every proof/candidate discovery, stream read, replay, interpreter step and peak writable bit in a compatible machine, then prove a genuine source-promise reduction or all-input resource contractor rather than merely optimal algorithm selection.

## Primary papers

Hutter, The Fastest and Shortest Algorithm for All Well-Defined Problems, IJFCS 2002, DOI 10.1142/S0129054102001199.
Blum, A Machine-Independent Theory of the Complexity of Recursive Functions, JACM 1967, DOI 10.1145/321386.321395.
Cheraghchi et al., One-Tape Turing Machine and Branching Program Lower Bounds for MCSP, STACS 2021, DOI 10.4230/LIPIcs.STACS.2021.23.
Oliveira, Pich, Santhanam, Hardness Magnification Near State-of-the-Art Lower Bounds, Theory of Computing 2021, DOI 10.4086/toc.2021.v017a011.
Fortnow et al., Time-Space Lower Bounds for Satisfiability, JACM 2005, DOI 10.1145/1101821.1101822.
Prior project ARC-0005-ORBIT and LSPV-4-MOVINGCOVER1 independently mention portfolio and Hutter limitations.

P versus NP remains OPEN.
