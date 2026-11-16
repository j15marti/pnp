# TMR-5 CURRENT handoff | 2026-11-15 18:48 PST | /055 SWITCH COMPOSITION vs COMBINED SYSTEM

**Authority:** `research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md` plus the shared worst-case derivation objective (W̄_R(N), Bridge(R): SAT∈P ⇒ W̄_R ≤ poly). Owned `main5_PNP_MACHINE_BOTTLENECK_REDTEAM.tex` reconciled in place. Prior handoff (/054, blob `888ac5e4a4fbe7ea6190c1bef822a9587d903ba9`) archived byte-for-byte at `research/agents/tmr-5/archive/handoff_pre_2026-11-15_1848.md`. Unmerged /053 branch handoff preserved at `archive/handoff_053_unmerged_branch_ysu7ts.md`. Retired proof trackers, historical root main, peer main1..4 and the five schedules are untouched. P versus NP OPEN.

**Imported /053** (branch `ccr-1695bd63-ysu7ts` commit `9891a0c5`, never merged to main): Theorem A, Bridge(R) ⇔ P≠NP for every R with a known superpolynomial lower bound; Theorem B, the provability premise is the open arrow. Its report, code and raw data were copied unchanged.

**NEW Theorem C, PROVED/EXACT (elementary, review OPEN):** H=(F∨z)∧(G∨¬z) for disjoint UNSAT F,G. Restriction gives s_R(H) ≥ max(s_R(F),s_R(G)); tree-like gives exact T(H)=T(F)+T(G); a union system with a clause interface and literal weakening (free in Res, ≤2x size and +1 degree in PC) refutes H in poly(s1)+poly(s2). **FALSIFIED: the componentwise "survives each method" criterion.** KNOWN-theorem instance (CONDITIONAL on encodings): PC_F2 vs PC_F3 with mod-3 and mod-2 Tseitin (BGIP 2001 + IPS 1999).
**Corollary D (KNOWN composition):** an R_comb with extension p-simulates ER ≡_p EF, so a W̄_{R_comb} lower bound would be an extended Frege lower bound (OPEN). This answers the /053 next lemma: yes, when extension is included.
**Literature:** no unrestricted DAG Res(⊕) superpolynomial bound per ECCC TR25-188. NEW CANDIDATE, not verified: Braun, arXiv 2609.23015 (2026-09-19), claims DAG Res(⊕) 2^{Ω(n/log²n)} for bit-PHP, Lean-formalized and AI-assisted. Tseitin is quasipoly in CP (Dadush–Tiwari 2020).

**Executed:** `experiments/tmr/tmr5_switch_composition055.py` rev `tmr5-switch-composition055.v1`, seed 20261115, CPython 3.11.18: 48 pairs, 28,351 assertions, 0 failures, 14.1 s. Raw `results/raw/tmr/2026-11-15_1848_TMR5_SWITCH_COMPOSITION055_PY_RAW.json`. Not run: preflight, LaTeX (no TeX in container), Lean, PC-degree checks.

**Gates:** DISJ N/A; relativization: C and D relativize, no separation; DTISP N/A; configuration counting PASS as upper-bound guard only. /341 FAIL, /386 RESTRICTED.

**Publication:** branch `ccr-1695bd63-4oyies` only, NOT merged to main, no PR opened.

**ONE NEXT LEMMA:** in R⁻_comb = DAG Res(⊕) + CP (clause interface, no extension), decide whether bit-PHP^{n+1}_n has polynomial refutations (CP arm or switching). Otherwise prove the lower bound and build Braun's Lean artifact independently. **P versus NP OPEN.**

END_OF_HANDOFF::TMR5::2026-11-15_1848_PST
