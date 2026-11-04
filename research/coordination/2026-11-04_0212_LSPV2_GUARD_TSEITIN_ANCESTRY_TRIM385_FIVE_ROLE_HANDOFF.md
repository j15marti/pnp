# LSPV-2/385: source-ancestry-trimmed guarded Tseitin, five-role handoff
**November 4, 2026, 02:12 PST.** Same existing LSPV-2 role and unchanged fixed `R_mix341`. **PROVED/EXACT** a uniform linear mixed calculus envelope; **COMPUTATIONAL** four complete strict-Resolution upper certificates; **OPEN** B1/B2/B3, full mixed superpolynomial minimum and P versus NP.

For connected simple bridgeless cubic odd-charge Tseitin $F_{G,\chi}$, form $H=t\land\bigwedge_{C\in F}(\neg t\lor C)$. Every one of $4h+1$ guarded source clauses is indispensable, so two-premise DAG source ancestry gives a $4h$-node floor. Resolve $t$ against all $4h$ guarded clauses, then use the pre-existing /341 legal three-AND3-per-vertex and $(h-1)$ GF(2) sums. Therefore:
$$
\boxed{4h\le W_{R_{\mathrm{mix341}}}(H)\le8h-1.}
$$
These are explicit source and proof costs in a **fixed** mixed calculus, not arbitrary machine lower bounds.

**Material correction to /384:** its 128-node $K_4$ proof was untrimmed. Backwards terminal ancestry has **32 strict Resolution nodes, all 17 essential original source clauses, zero paid AND2 definitions and zero gate views**. A completely separate direct original-source Resolution DP producer independently produced the same bound. The older 128-node proof remains valid as an upper bound but does not show that gates are necessary.

New independent source-only strict Resolution proof upper certificates: $K_4$: 32 nodes; $K_{3,3}$: 76; cube: 184; prism$_6$: 952. None is a certified minimum. Python producer and independently implemented JS verifier passed **85,986 checks**, 24 corrupted-record rejections, per-source deletion and sign-flip SAT witnesses, odd/even and guard $t=0$ controls. A separate public JS producer/checker and four complete raw proofs were committed to `experiments/arc/lspv2_385_guarded_tseitin_public.js` and `results/raw/arc/2026-11-04_0212_LSPV2_GUARDED_TSEITIN385_*_raw.json`. Serialized proof lengths and work are **not** node counts.

The direct DP proof search is **not** polynomial for growing expander graphs. It may attempt exponentially many pair resolutions and materialize enormous intermediate clauses; one cannot extrapolate four finite measurements. Mixed upper compiler can be fully implemented in conservative polynomial bit resources, but $\rho\ge1$ for input preprocessing and no FLMV contradiction follows. Known Urquhart/Haken lower bounds are for unrestricted **ordinary DAG Resolution** on explicit CNFs, not ER, GF(2), fixed mixed R or SAT machines. The user's weakest B3 transfer remains unproved:
$$
\mathrm{SAT}\in P\Longrightarrow\overline W_{R_{\mathrm{mix341}}}(N)=N^{O(1)}.
$$

**Review:** actual Grok `GROKPROOF/2026-11-04_1217_PROGRESS.md` and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` inspected. Neither supplies unrestricted B3; Grok's claimed numerical circuit-cut barrier lacks the proof for every correct selector. Reviewed /341,/383,/384, LSPV-1/385, LSPV-3/389, LSPV-4/381, LSPV-5/333, AGENTS/CODEX/skill and issue #3. Fixed all pre-existing identity/schedule/ownership/safeguards.

**Handoffs:** LSPV-1 verify all-CNF quantifier firewall and compactness; LSPV-2 next attempt authenticated **all-graph** AND2+RES polynomial compiler with local parity rewrites, or find explicit failing graph; LSPV-3 audit reused-source DAG proof semantics under trimming; LSPV-4 separate proof-node vs fully charged DP machine costs; LSPV-5 attack the 4h lower premise and mixed upper legality. No change to task status or hours.
