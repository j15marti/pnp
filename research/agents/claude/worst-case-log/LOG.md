# Living log: worst-case derivation complexity  W̄_R(N) = max_{F UNSAT, |F|≤N} min_{π: F⊢_R ⊥} cost_R(π)

Append-only. One entry per run. **P versus NP remains OPEN.** Labels: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.
Existing fixed system and prior work: R_mix341 (research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex); LSPV-1/348 (signed-orbit quotient), /391 (encoding independence), /406 (conditional B3 via Pich–Santhanam). This log does not replace them.

---
## Entry 2026-11-05 (Claude, scheduled run 1)

**Corpus reviewed (this run):** AGENTS.md, world-ledger README, LSPV-1/348, LSPV-1/391 (grep), LSPV-1/406. Not re-read: LSPV-2..5 reports, tasks/, root main.tex (not edited: ownership regions belong to LSPV-1..5). The "shared worst-case research directive" named in the prompt was not found as a file under that wording; the nearest is the 2026-11-02_1204 five-role directive cited in LSPV-1/406.

**Literature check (standard search, one pass):**
- Cook–Reckhow 1979: a polynomially bounded proof system exists iff NP = coNP. KNOWN THEOREM.
- Pich–Santhanam, ECCC TR23-199 / arXiv 2312.08163: P ≠ NP from EF lower bounds, assuming feasible anticheckers (a fixed S^1_2 proof). CONDITIONAL; already used in LSPV-1/406.
- arXiv 2506.16956: Proof Analysis Problem for EF is NP-complete, tied to PV_1. Relevance not yet assessed (CANDIDATE clue for how hard it is to certify "shortest" derivations, i.e. the certified-minimum part of the SAT-Circuit Reduction Builder role).
- Search returned nothing new for 2025–26 on anticheckers; not evidence of absence.

**Observation 1 (bridge is system-dependent; dichotomy) — PROVED/EXACT, elementary.**
Let B(R) denote the bridge "SAT ∈ P ⇒ W̄_R(N) ≤ poly(N)".
(a) If R is Resolution (or any system with a known superpolynomial lower bound, Haken 1985), then B(R) is equivalent to P ≠ NP being decided as: B(R) true together with Haken gives SAT ∉ P. So B(R) for such R is as hard as P ≠ NP and cannot be a "weak" intermediate step.
(b) For R_ND := "π accepted iff π is empty and the fixed polynomial-time decider D rejects F", W̄_{R_ND} is polynomial whenever D decides SAT, trivially. This is a poly-bounded system depending on D, consistent with Cook–Reckhow, and shows the bridge is vacuous unless R is fixed independently of D.
Hence the useful window for B(R) is: R fixed in advance, strong enough to simulate polynomial-time computation, so that B(R) is plausible, but with lower bound still open. This is the Extended Frege neighbourhood. R_mix341 sits there only via the ER-simulation used in /406.

**Observation 2 (what the bridge actually needs) — KNOWN THEOREM, stated from memory of Cook 1975 / Krajíček–Pudlák; not rechecked against the primary this run.**
For R ⊇ EF: B(R) follows if the decider's soundness on UNSAT outputs is provable in PV (or S^1_2) with a fixed proof. Without provability, SAT ∈ P gives only that a proof exists in some system, not in R. This is exactly the Pich–Santhanam gap, so Observation 2 explains why LSPV-1/406 needs AC_k. No new theorem; this is a consistency check of the existing route.

**Consequence for assignments (CANDIDATE guidance, no claim):**
- Lower-Bound Lead: the weakest sufficient bridge is a *provability* statement about the decider, not a counting statement; target "uniform reflection for a hypothetical decider in EF".
- Red Team: test that no proposed hard family F_n is also hard for the D-dependent system R_ND (it must not be, by (b)); any lower bound argument that also "proves" hardness for R_ND is wrong.
- Resource Auditor: charge nothing for finding π (as granted), but still charge |π| bits, which is where Observation 1(b) shows the free-discovery grant is harmless.

**Status:** no new lower bound, no bridge proof. B1/B2/B3 and superpolynomial W̄_R OPEN. P versus NP OPEN.

**Next run:** read arXiv 2506.16956 for whether NP-completeness of the Proof Analysis Problem constrains certification of minimum derivations; check LSPV-2/341 for a concrete hard-family candidate against R_ND control.

% END_OF_ENTRY 2026-11-05 run1
