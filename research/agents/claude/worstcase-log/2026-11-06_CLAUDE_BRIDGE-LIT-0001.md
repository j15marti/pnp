# CLAUDE BRIDGE-LIT-0001 (2026-11-06): where the weakest bridge sits, plus literature clues

Role: Independent Proof Red Team (Claude). Status: no new unconditional result. **P versus NP remains OPEN.**
Target: wbar_R(N) = max over UNSAT F, |<F>|<=N, of min over refutations pi of cost_R(pi); bridge B_R: SAT in P => wbar_R <= poly.

## Corpus reviewed
LSPV-1/336 (clocked optimality: size-optimal R => bridge), LSPV-1/350 (minimally-UNSAT quotient, core sandwich), LSPV-3/437 handoff (latest), world-ledger rows (L13, L34-L40), AGENTS.md allocation notes. Nothing below duplicates 336/350; it re-derives the dichotomy independently and adds literature.

## 1. Dichotomy for the shared objective (PROVED/EXACT, elementary; consistent with 336)
Let R be a sound, complete system with poly-time verifiable proofs and cost(pi) >= |pi|^eps (Cook-Reckhow type).
(a) wbar_R poly => NP = coNP (KNOWN THEOREM, Cook-Reckhow 1979). Hence wbar_R superpoly alone shows only "R is not p-bounded".
(b) wbar_R superpoly AND bridge B_R => P != NP (since SAT in P => P=NP, so wbar_R poly, contradiction).
(c) B_R is exactly the statement "P=NP => R p-bounded". It is vacuous if P != NP, so it cannot be proved by assuming P != NP; it needs a P=NP-world argument.
So both load-bearing arrows are separate: LOWER (wbar_R superpoly, for a Cook-Reckhow R, is Frege-type hardness when R is strong) and BRIDGE (B_R).

## 2. Automatability is not the bridge (PROVED/EXACT, trivial; red-team point)
If P=NP, then for every Cook-Reckhow R, a shortest R-refutation of F is found in time poly(W_R(F)+|F|) (guess-and-verify is an NP search). So "SAT in P => R automatable" is free for every R.
It does NOT give boundedness: W_R itself may stay superpolynomial even when P=NP (no known obstruction). This matches the user's remark that strategy search need not be charged: charging it changes nothing in the needed direction. The missing step is size, not search. Failed-transfer label for any argument that derives B_R from automatability.

## 3. Literature clues (searched 2026-11-06; no 2026 result settles any arrow)
- Cook-Reckhow: p-bounded system exists iff NP=coNP. KNOWN.
- Krajicek-Pudlak: a p-optimal system exists iff TAUT has an almost-optimal algorithm. Optimal systems follow from NE=coNE; p-optimal from E=NE. Open unconditionally. For us: a size-optimal R gives B_R (LSPV-1/336), so existence of an optimal system is a sufficient route; it is not known.
- Egidy-Glasser (STOC 2025) and Egidy, arXiv:2602.02294 (Feb 2026, SPARSE-relativization): oracles blocking relativizable proofs of positive answers on optimal proof systems. Barrier: any proof that a concrete R is optimal (hence supplies B_R this way) must be non-relativizing. CANDIDATE barrier; exact oracle statements unverified here.
- Atserias-Muller: resolution is not automatable unless P=NP. Bounded-depth Frege not automatable unless P=NP (CCC 2024). arXiv:2506.16956 (v2 2026): non-automatability under P != NP is the best possible hypothesis, since P=NP gives automatability for all systems (agrees with section 2); also Proof Analysis for Extended Frege NP-complete. Not a lower bound on wbar_R.
- Frege superpolynomial lower bounds remain open; bounded-depth Frege lower bounds known. So LOWER arrow for strong R is a major open problem on its own.
- Learning link (arXiv:2111.10626): automatable optimal proof system => learning algorithms for circuits. Possible unexplored consistency test for any proposed optimal R.
Classification: Cook-Reckhow, KP, automatability facts = directly transferable theorems. Relativization oracles = barrier, not a tool. Learning link = analogy needing a bridge theorem.

## 4. Red-team conclusions and next targets
1. Any proposed hard family must be checked against a *bounded* R, not just resolution: Frege/EF-type compression kills all known hard families (odd Tseitin etc. already controls in 350).
2. Weakest viable bridge candidate: R that simulates Q_A for ONE polynomial-time SAT decider A (non-uniform in the hypothesis). Ask: is "R simulates Q_A for a fixed A" provable without knowing A is correct? 336 shows correctness indices are not r.e., so a uniform R needs optimality, and optimality is relativization-barred. This is the sharpest obstruction found; it is not a refutation.
3. Next task: state exactly which oracle in Egidy-Glasser/Egidy kills "optimal R for the mixed system R_mix341"; read primary text before relying on it.

OPEN: LOWER arrow, BRIDGE arrow, P versus NP.
