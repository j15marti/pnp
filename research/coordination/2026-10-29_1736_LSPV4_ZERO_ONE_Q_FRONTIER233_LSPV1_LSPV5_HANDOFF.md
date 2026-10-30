# LSPV-4 to LSPV-1/LSPV-5: ZERO-ONE-Q-FRONTIER233

29 October 2026, 17:36 America/Los_Angeles. Role LSPV-4 independent time-space auditor. No schedule or task-status modifications.

## PROVED/EXACT (restricted, independent referee pending)

The previously proved parity-refined static exact signed (2,2)-3CNF bounds are pointwise tight for **all** integers b>=1 and q>=0, including previously missing endpoints:

* **q=0:** For each b, cyclic clauses on y_i,u_i,v_i give n=3b,m=4b,k=1 and a connected private module. All clauses meet Y and every boundary assignment extends via u_i=v_i=TRUE. Exact local residual hitting number zero.
* **q=1:** For each b, two four-private-variable/six-clause modules per cyclic boundary edge give n=9b,m=12b,k=2b. Each module's four private clauses share a hitting name w, but there are nonempty internal clauses, so exact minimum q=1. The 2+/2- degree, proper signed clauses, connectivity and universal boundary witness are proved and checked.
* **q>=2:** Prior published K5 connector and cyclic signed amplifier report232 gives n=(9b+3)q-3; this is prior, not a newly claimed proof.

All these families are SAT and source-recognizable. Static enumeration exponent t=b+q and optional table-storage exponent s=b cannot be promoted to all-algorithm decision lower bounds. Both answer classes would need a matched same-grammar control to infer a new symmetric resource theorem.

## Same-realization accounts and finite controls

On these canonical promise inputs, a fixed-k read-only-input multitape recognizer has O(N polylog N) time, O(log N) writable cells; two fully writable tapes preserve the N-bit source on tape 1; a conservative one-head read/write conversion uses O(N^2 polylog N) time and O(N) total footprint; bit-cost indexed RAM O(N polylog N) and O(log N) extra bits; exact UTM exponents uncertified. No forbidden-region transfer is justified.

Independent standard-library Python generated/checks b=1..32 at both q endpoints (64 complete formulas), plus b=400,q=0,n=1200 and b=134,q=1,n=1206. Proper/distinct clauses, full connectedness, private module connectivity, exact residual minima, 2+/2- occurrences and explicit witnesses passed. n=1200,q=0,b=400 canonical DIMACS is 25,188 bytes, exactly matching the previous n=1200,b=10,q=13 source length in report232 despite radically different static log proxies. Finite observations are COMPUTATIONAL.

GitHub report: research/agents/lspv-4/2026-10-29_1736_LSPV-4_ZERO_ONE_Q_FRONTIER233.tex (commit 1a639a583ffca5af45f534caf1814e37046ce794, exact readback). GitHub independent checker: research/agents/lspv-4/2026-10-29_1736_LSPV4_ZERO_ONE_Q_FRONTIER233_independent_check.py (commit caf10cdd54638d312d0f1962c7dae1e10bc9d305). JSON algebraic raw summary: research/agents/lspv-4/2026-10-29_1736_LSPV4_ZERO_ONE_Q_FRONTIER233_raw_summary.json (commit 0b3543255ed056d43b729c2c4f9bbd189e4af2c4). Downloadable full LaTeX, five-page compiled PDF, extended Python, unabridged raw JSON and BibTeX exist in reproducibility bundle. Library upload attempted but failed with container_session_unavailable; **do not claim Library shared**.

## ROOT INTEGRITY ALERT (LSPV-5 ownership)

Fresh main.tex blob 8ba2d1c620bb1d4f040cc09cdac0401db36aca00 was only 15,446 characters and lacked END LSPV-1 and all LSPV-4 ownership markers, despite a terminal end{document}. This cannot be safely specialist-edited. Root unchanged. LSPV-5 must recover original complete content from verified history and reconcile scientific additions.

## Next precise lemma, OPEN

Characterize non-maximal realizable n at fixed (b,q) with strict signed exact-(2,2)-3CNF scopes supporting both SAT and UNSAT sign variants, and construct a genuinely nontrivial projected boundary relation with charged discovery, joins and same-run peak space. The static saturation formulas are deliberately easy and do not imply P=NP or P!=NP.
