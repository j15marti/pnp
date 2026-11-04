# LSPV-3/403 five-role research handoff (2026-11-04, 14:24 PST)

The role-owned report proves a restricted theorem: for any fixed k, checking whether an arbitrary compact Boolean circuit has at most k essential original inputs is coNP-complete. This matters only for hypothetical semantic-support validators over arbitrary compact circuits. The unchanged fixed Rmix341 accepts explicitly local truth-table rules, not such an unrestricted oracle.

IDEA: Validate original-support typing after conservative gate promotion. SEARCH: Reviewed the Nov 2 five-role directive, original Rmix341, REFEREE341/342, LSPV-3/402, current issue 3, Grok and Claude repository analyses, Krajicek 2012, Kiesl et al. 2020, and relevant OpenAI math Lean files. Direct Google UI unavailable, so general web and authenticated GitHub queries were used. ITERATE: Proved the coNP-complete validation frontier and a safe typed-replay restriction; the unchecked general replay claim is still unsupported.

Controls: 256 exhaustively tested three-input functions; independent Node comparisons, malformed inputs, SAT/UNSAT and corrupt-proof controls. A separate 16-node DEF/RES macro is only an upper bound.

LSPV-1: Audit all reflection arguments for semantic-oracle costs.
LSPV-2: Define polynomially checkable LOCAL-CONVERT and AND3 syntax.
LSPV-3: Build source-authenticated type-preserving port compiler.
LSPV-4: Charge all parsing, validation, output and peak memory.
LSPV-5: Reconcile unrestricted unchanged-replay claims and retain B1/B2/B3 OPEN.

Primary report: research/agents/lspv-3/2026-11-04_1424_LSPV-3_SEMANTIC_PORT_VALIDATION_FIREWALL403.tex

No agent settings, proof rules, schedules or verified lower bounds changed. P versus NP remains OPEN.
