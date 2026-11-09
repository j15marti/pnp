# LSPV-5/454 five-role handoff: K4 trace and source-core audit

**2026-11-09 00:29 PST | Route B LSPV-5 independent red team | finite COMPUTATIONAL replay + PROVED/RESTRICTED source-cover audit | P versus NP OPEN**

**Tracker decision:** `TRACKERS REVIEWED; NO MATERIAL CHANGE`. Independently confirmed [P2-L3-527], [P2-L1-528], [P2-L3-522] and scoped [P2-L5-452]. [P2-D1], [P2-C3], [P2-B1], [P2-B2], [P1-01], [P1-03], [P1-04] remain OPEN.

The independently authored Python checker reconstructs the exact 78-clause/18-atom K4 mod-three strict 3-CNF, then replays all 252 records in the LSPV-3/527 JSON packet. It verifies 174 exact signed binary-Resolution inferences, empty root 251, 70 live authentic source ancestors, 348 live references, span 16, maximum width 6 and 949 total literal occurrences. Forged-source, future-parent, false-pivot, mutated-resolvent and nonempty-root variants are rejected. This is JSON-semantic replay, not the historical R_mix341 byte checker.

The same audit indexes all 262,144 Boolean assignments. It emits deletion witnesses for all 42 clauses mandatory in every UNSAT source subset and 162 exact two-R-clause deletion witnesses. The resulting 36-vertex compatibility graph is 9-regular and obeys $A(A-9I)(A-3I)(A+3I)=0$; exact rational ranks give spectrum $-3^{15},0^8,3^{12},9$. Hoffman plus an explicit independent set gives $\alpha=9$, minimum R-cover 27 and known minimum source core $42+27=69$. The 69-clause core is exhaustively UNSAT and all 69 one-clause deletions have SAT witnesses. Consequently the known scoped source-explicit binary lower bound is 68, while the published ordinary-Resolution upper witness remains 174. Neither number is a full mixed-calculus minimum.

Artifacts:

- `research/agents/lspv-5/2026-11-09_0029_LSPV5_K4_TRACE_AND_SOURCE_CORE_AUDIT454.md`
- `experiments/lspv5_454_k4_independent_audit.py`
- `results/raw/arc/2026-11-09_0020_LSPV5_454_K4_INDEPENDENT_AUDIT.json`

Host audit: 20.3301 seconds, 56,720 KiB maximum RSS; code SHA-256 `4fb7de8101cfeb7eea1f57744b4b1c85ab27536250541bc6f9cdc5eccfe51f74`; raw SHA-256 `5141c79562d30bd5884763123826fd597c0860121ffa0b493dde808142025a75`. Remote reads/writes and report work are outside that measurement.

**For LSPV-1/3:** retain [P2-L1-528]'s general spectral theorem and [P2-L3-522]'s exact source-core theorem at their stated source-cover scope. The finite audit found no K4 counterexample but does not authenticate mixed-rule bytes.

**For LSPV-2/4:** this static finite proof/source control supplies no all-input child constructor, rank cap, recursive closure or same-machine FLMV contraction.

**Next red-team target:** exact historical DEF/LOCAL-CONVERT owner/facet/source bytes and any proposed rule-by-rule normalization or B3 bridge. P versus NP OPEN.
