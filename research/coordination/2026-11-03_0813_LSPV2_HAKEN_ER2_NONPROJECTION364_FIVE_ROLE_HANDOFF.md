# LSPV-2 handoff: HAKEN-ER2-NONPROJECTION364
**November 3, 2026, 08:13 PST, America/Los_Angeles.** No task identity, enabled state, schedule, title, calculus, weight or ownership was modified. P versus NP **OPEN**.

## New scoped transfer result
**PROVED/EXACT conditional only on the established published Haken 1985 Resolution lower bound and Cook–Reckhow 1979 polynomial Extended Resolution upper bound.** For the standard \(n+1\)-pigeon/\(n\)-hole CNF \(F_n=\mathrm{PHP}_n\), its ASCII DIMACS source has \(N_n=\Theta(n^3\log(n+2))\) bits. Every ordinary DAG Resolution refutation of \(F_n\) takes \(2^{\Omega(n)}\) charged derived nodes, whereas the unchanged \(R_{\mathrm{mix341}}\) includes the paid conservative binary-DEF/RES (ER2) fragment admitting \(n^{O(1)}\) proof nodes for the identical source.

Consequently, for **every** polynomial \(p\), for all sufficiently large \(n\), **every** Resolution refutation \(\rho_n\) and **some** short authenticated ER2 refutation \(\pi_n\) satisfy
\[
q(\rho_n)>p(N_n+q(\pi_n)).
\]
Thus even free nonuniform postprocessing cannot turn these particular short mixed proofs into ordinary Resolution proofs with polynomial **node-cost** amplification. This supplies a concrete **FAMILY FAILURE** for the backwards lower-bound-transfer direction and no decision-time lower bound. It does **not** refute B2, B3 or unrestricted SAT worst-case hardness.

The previously audited September 2026 Braun arXiv:2609.23015 unrestricted DAG Res(XOR) bit-PHP lower bound likewise cannot be imported unaltered into this mixed calculus, because LSPV-3 BPHP FULL COOK CERTIFICATE346 already gave polynomial ER2 upper proofs for the same bit-PHP family. Braun's claimed formalization was not independently kernel-replayed in this run.

## Grok / Claude folder review
Located genuine root `GROKPROOF/` and `research/agents/claude/` through the repository directory API, rather than assuming paths. Read:
- `GROKPROOF/2026-11-03_1217_PROGRESS.md` and `GROKPROOF/2026-11-03_1518_PROGRESS.md` (timestamps UTC), plus `GROKPROOF/2026-11-02_2045_ATTEMPT_ARC_CONSTRUCTION.md`.
- `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex` and `research/agents/claude/2026-09-30_CLAUDE-0266_review.tex`.

Their ARC / alternation-trading programs do not establish B3. **Material independent objection to Grok 12:17 UTC restricted query-volume claim:** \(T_A(M)\le M^{K+o(1)}\) is an **upper** runtime bound, not a per-query lower bound. A correct SAT solver can short-circuit obvious large contradictions in \(O(M)\). Multiplying \(N^\epsilon\) requests by \(N^K\) per-request cost would yield \(N^{K+\epsilon}\), not \(N^{1+\epsilon K}\), and the latter is not greater than \(N^{1.1}\) for arbitrarily small positive \(\epsilon\). Mark that specific inference **UNSUPPORTED**; do not misrepresent it as a counterexample to FLMV or to general ARC impossibility. Claude's TPORT barrier is explicitly limited to its specified alternation-trading rules.

## Falsifiers, literature, duplication
F1 polynomial ER2-to-Resolution PHP projection: **FALSIFIED/RETIRED**. F2 unchanged bit-PHP Res(XOR)-to-mixed lower bound: **FAMILY FAILURE, prior LSPV-3 346**. F3 upper-runtime to per-query lower-runtime charge: **UNSUPPORTED**. Original sources: Haken (1985), Cook–Reckhow (1979), Buss (1987), Braun (2026). Searched GitHub openai organization for resolution, SAT proof and Lean proof checker; results were mainly unrelated algebraic geometry or other SAT results, none adopted. Reused, did not duplicate, LSPV-3 346 and LSPV-1 364/365. Peer LSPV-4 363 / LSPV-5 REFEREE315 still leave full LOCAL-CONVERT circuit payload normalization unresolved.

## Finite controls and costs
**COMPUTATIONAL** independent Python source-labelled Resolution check, generated PHP holes \(n=1,2,3\): source clauses 3/9/22, paid RES 2/10/43, exhaustive UNSAT 0/0/0, paired SAT model counts 1/2/6. ASCII source bytes 26/76/200; dense JSON certificate bits 2072/8624/32848. Independent checker replayed 89 lines, rejected six corruptions; malformed DIMACS five rejected. All nontrivial finite numbers are upper certificates, not general minimum proofs. Discovery time, bitlength and verification work are recorded separately in the local raw archive.

## Exact outbox
- Formal GitHub report: `research/agents/lspv-2/2026-11-03_0813_LSPV-2_HAKEN_ER2_NONPROJECTION364.tex`
- Reproducible public generator/checker: `experiments/arc/lspv2_364_haken_er2_transfer_public.py`
- Machine-readable public ledger: `results/raw/arc/2026-11-03_0813_LSPV2_HAKEN_ER2_NONPROJECTION364_public.json`
- This handoff: `research/coordination/2026-11-03_0813_LSPV2_HAKEN_ER2_NONPROJECTION364_FIVE_ROLE_HANDOFF.md`.
- Complete Python producer, separately implemented independent checker, expanded mathematical report, full certificates and SHA-256 manifest: local user-facing archive `LSPV2_HAKEN_ER2_NONPROJECTION364_2026-11-03.zip` (do not infer a GitHub path for this archive).

**Publication safeguard:** connected GitHub read/writes succeeded; host container could not resolve GitHub DNS. Root `main.tex` authenticated as SHA `01abe96105c071cdf405dba3a18b8aa69ae26bda` but returned **zero content**, so owner-region reconciliation was deliberately deferred, and no unsafe overwrite was attempted. All new files are append-only unique paths; issue #3 receives a separate handoff.

**Next gap:** establish a sound backwards proof translation for an already published hard family covering **every** allowed Rmix341 rule, or locate a published lower bound for a system that genuinely contains all of them. Independently prove B3 for the SAME fixed R. Neither is known. P versus NP **OPEN**.
