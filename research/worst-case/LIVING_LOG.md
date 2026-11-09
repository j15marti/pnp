# Living log: worst-case derivation program (W̄_R)

Status vocabulary per AGENTS.md. P versus NP: **OPEN**.

## 2026-11-09 20:48 UTC — run 1 (Claude, LSPV-5 slot)
Corpus: surveyed repo; found B3/W_R framework (LSPV-1/353) already present; directive file created this run.
Literature: no new Frege/EF lower bound (Alekseev, Theory of Computing 2026, is PC with extension rule, not Frege); 2024 arXiv 2405.02232: EF superpoly lower bound => NP not in P/poly only under extra hypotheses (CONDITIONAL, not used).

### Note 1 — hardwiring collapse (PROVED/EXACT, elementary)
If cost counts only the running time/size of a per-instance chosen algorithm and soundness is not charged, W̄ = O(N): hardwire the answer "UNSAT". So "free optimal sequence" is only meaningful when verification of soundness is charged, i.e. W̄_R is proof size of a Cook–Reckhow system. Then (Cook–Reckhow, KNOWN) some R has W̄_R poly iff NP = coNP, so a superpoly bound for ONE R implies nothing about P vs NP by itself.

### Note 2 — provability-relative bridge (PROVED/EXACT, standard reflection; CANDIDATE as a project route)
Let T be a fixed sound theory, R_T the proof system "T-proofs of Taut(F)". If T proves "M decides SAT in time n^c" for a specific M, then W̄_{R_T}(N) <= poly(N) (instantiate the fixed-size correctness proof, then verify the poly-length run of M on F). Hence B(R_T) holds restricted to T-provable SAT in P; contrapositive: superpoly W̄_{R_T} => T proves no explicit poly-time SAT algorithm correct (independence-type conclusion, NOT P != NP). Unconditional B(R) needs removing the provability proviso = the reflection premise already identified as the B3 obstruction. Classification: EXACT transfer of Krajicek–Pudlak machinery; failure mode matches existing B3 RT/SC gap.

### Open arrows
(a) superpoly W̄_R for any R strong enough to carry reflection (open since Cook–Reckhow; Frege/EF lower bounds open); (b) unconditional B(R); (c) pointwise vs worst-case simulation (secondary).
### Next
Role 3: test Note 2 against hard families (Tseitin/PHP in EF-like R); Role 4: audit cost of fixed-size correctness proof inlined per instance; Role 5: attack Note 2 for hidden non-uniformity (T-proof length constant depends on M).
% END_OF_VERIFIED_LOG::2026-11-09_2048
