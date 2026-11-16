# TMR-5 compact handoff | 2026-11-16 04:48 PST | soundness-route equivalence /067 (W_R line)

**Authority and ownership.** The END_TO_END_AGENT_MANUSCRIPTS directive governs, with the scheduled worst-case derivation objective W_R(N) and bridge B(R). TMR-5 owns only main5, its own reports, code, raw data and this handoff. Peer manuscripts, retired proof trackers, historical root files, the five identities, enabled states and Pacific schedules are unchanged. P versus NP is OPEN.

**Branch and lineage state.**
- **This branch** is `ccr-1695bd63-4ku1m3`. It contains:
  - the /060 branch `ccr-1695bd63-lh9sf9` (which already contains /057 dh8nvl and the /058-/059 drafts);
  - a merge of the previously separate W_R branch `ccr-1695bd63-l769za` (/053 ysu7ts, /055W 4oyies, /056).
- Both conflicting handoffs are archived byte-exact:
  - `archive/handoff_pre_2026-11-16_0448_branch_lh9sf9_060.md`, blob 0a1cdcb15a28f7ec84a329cdd1d6b8a546513171;
  - `archive/handoff_pre_2026-11-16_0448_branch_l769za_WR056.md`, blob 89d149d691674dfa686a9f478405eb177d77a11c.
- **Separate lineage, not merged here:** draft PR #209 (`tmr5-20261116-0121-jmv-vector-chain063`, /063-/065 JMV line), with handoff blob 0610efc4 and main5 blob 69f4d772. The two main5 lineages must be reconciled before either merges to main.
- No PR was opened for this branch.

**NEW Theorem G (PROVED/EXACT elementary; forward half KNOWN, Krajíček IPL 112 (2012) Thm 2.1, original text read; independent review OPEN).**
- **Setup.** Sound(C) = Tseitin(C) AND not out AND Sat(f,a,s), the slot-CNF reflection formula. R is closed under restriction and literal substitution (Res, Res(k), PC, CP, AC0-Frege, Frege, EF).
- **(i)** If C(F) = 0, then S_R(F) <= S_R(Sound(C)), via the restriction rho_F with s+ := a_i and s- := not a_i.
- **(ii)** If C_N is correct, then W_R(N) <= S_R(Sound(C_N)) <= W_R(O(|C_N| + N)).
- **Hence:**
  - B(R) <=> [SAT in P => some correct poly-time M lies in Alg(R)]. The soundness route is EQUIVALENT to the bridge, not a weaker step. The candidate is FALSIFIED as a weakening.
  - For Res, Res(k), PC, CP and AC0-Frege, no correct poly-size SAT circuit has short soundness proofs, unconditionally.
  - For Frege and EF the route equals B(EF) itself.

**Executed (COMPUTATIONAL).**
- Executable `experiments/tmr/tmr5_soundness_restriction067.py` (rev tmr5-soundness-restriction067.v1, seed 20261116, CPython 3.11.18, blob d2fcef19). Raw output `results/raw/tmr/2026-11-16_0448_TMR5_SOUNDNESS_RESTRICTION067_PY_RAW.json` (blob 8877d459).
- 402 authentic UNSAT F were tested, n <= 6. Brute-force circuit soundness DAGs had up to 45,899 lines; the restricted refutations had at most 25 lines. Each was accepted by the independent resolution checker.
- 60 satisfiable controls and 6 wrong-circuit controls were all rejected.
- 1338 assertions, 0 failures, 16.0 s.
- Not run: preflight, LaTeX, Lean, full Braun text, external review.

**Gates.** DISJ N/A. Relativization: oracle-free and white-box, consistent with /060 Theorem C; no separation. DTISP N/A. Configuration counting is an upper-bound guard only. /341 FAIL, /386 RESTRICTED.

**Literature.** Krajíček 2012 (Alg(P), Thm 2.1, Cor 2.2) was read. Braun arXiv:2609.23015 (DAG Res(⊕) BPHP bound): abstract only, still a CANDIDATE. Byramji–Impagliazzo arXiv:2511.20023 (bounded depth). ECCC 2026/109: abstract fragment only.

**Paths.**
- main5_PNP_MACHINE_BOTTLENECK_REDTEAM.tex: in place, new §sec:soundroute and a single consolidated next lemma. The duplicate sec:bridge label was resolved to sec:bridge053, and the two "Theorem C"s were renamed C/055 and C/060.
- research/agents/tmr-5/2026-11-16_0448_TMR5_SOUNDNESS_ROUTE_EQUIVALENCE067.md
- the executable and raw output above
- the two archives above

**ONE next lemma.** Work in the class-restricted target K = Alg(DAG Res(⊕)):
1. Independently verify Braun's BPHP bound.
2. Check that Res(⊕) is decent (restriction and literal substitution).
3. Conclude that every M in K needs superpolynomial time on not-BPHP.
4. Identify which Gaussian-elimination DPLL variants lie in K.

The result is K-only, not P vs NP. Theorem E (/056) shows that extension must be excluded from K.

END_OF_HANDOFF::TMR5::2026-11-16_0448_PST
