# LSPV-3/391: signed feasible-interface quotient is not a proof-cost invariant

**November 4, 2026, 03:24 PST.** Status **PROVED/EXACT** for all-size exact mixed-system minima; finite signed controls **COMPUTATIONAL**, independent specialist referee pending. Fixed original `R_mix341`, all five task identities, states and schedules unchanged. P versus NP **OPEN**.

For every integer h>=2, let D=(NOT x_h), and define

$$
L_h^A=(x_0)\wedge\bigwedge_{i=1}^h(\neg x_{i-1}\vee x_i),\qquad
L_h^B=(x_h)\wedge\bigwedge_{i=0}^{h-1}(\neg x_i\vee x_{(i+1)\bmod h}).
$$

Both projected left interfaces at sole boundary bit x_h are exactly {1}, so **every** downstream predicate Q(x_h) has the same SAT label after either left side. Let A=L_A AND (NOT x_h), B=L_B AND (NOT x_h). Both are UNSAT Horn 2CNFs with the same h+1 variables, h+2 source clauses, two units, h binaries, exact signed per-variable occurrence vector (+1,-1), and **exact same ASCII DIMACS byte length**. Yet:

$$
\boxed{W_{R_{\mathrm{mix341}}}(A_h)=h+1,\qquad W_{R_{\mathrm{mix341}}}(B_h)=1.}
$$

Every original source clause and each literal sign of A is independently pivotal. Thus the two-premise DAG ancestry lower bound forces h+1 paid nodes, realized by h+1 strict RES steps. In B, two opposed source units give a one-node refutation; its cycle sources are irrelevant. The node-cost ratio h+1 diverges. This is **not** a counterexample to polynomial-factor simulation or B3: the gap is polynomial and both formula families are uniformly trivial to decide. It specifically falsifies any putative tight intrinsic lower-bound function of **only** the complete feasible cut image, source bits/clauses, signed degree vector and width histogram. Signed incidence *topology* and source provenance remain possible inputs to a stronger invariant.

**False claims tested:** F1 identical one-bit projection forces equal minimum: FALSE. F2 matching N,m,n, widths and signed occurrence vectors forces equal minimum: FALSE. F3 every source indispensable forces superpolynomial proof length: FALSE. F4 this proves B3 false: not established.

**Controls:** Eight cases h=2,3,4,6,8,12,24,64; 139 source deletion SAT witnesses, 262 literal sign-flip SAT witnesses, both original families UNSAT, same SAT interface, exhaustive label and image through h=8; strict source-ID/pivot proof replay and malformed/forged proof rejection. Local independent Node checker 1,566 assertions. Source bits Theta(h log h), proof evidence O(h log h) for A and O(log h) for B (excluding the common input); no FLMV T/S or machine lower bound inferred. A proof generator's search cost and the O(h^2) all-witness test ledger are separate.

**Previous corpus:** Haken ordinary Resolution unary PHP exponential lower bound, Cook polynomial Extended Resolution PHP, Braun September 2026 extension-free DAG Res(oplus) bit-PHP bound. None is an all-algorithm bound. Reviewed refocus document, issue #3, AGENTS/CODEX/skill, original LSPV-2/341 blob c87acd11, LSPV-3/386,/389,/390, LSPV-1/386, LSPV-2/385, LSPV-4/382 and LSPV-5/334. The two-way cut-size controls in LSPV-4/382 are prior related work, not this exact equal-statistics minimum gap. Inspected actual `GROKPROOF/2026-11-04_1217_PROGRESS.md` (blob cae0560d) and `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob 1f9fc727). The former does not prove a uniform fully charged circuit-cut SAT selector for all algorithms; the latter is restricted alternation trading. Neither implies B3.

**Published artifacts:** `research/agents/lspv-3/2026-11-04_0324_LSPV-3_INTERFACE_QUOTIENT_COST_GAP391.tex` (report); `experiments/arc/lspv3_391_signed_interface_producer.py` (deterministic complete witness/proof-data generator); `experiments/arc/lspv3_391_signed_interface_independent.js` (independent proof/witness verifier); `results/raw/arc/2026-11-04_0324_LSPV3_INTERFACE_QUOTIENT391_summary.json` (raw exact-case ledger). Full 322KB local reproducibility data retained separately. To reproduce: run producer with a JSON output pathname, then pass the generated pathname to the Node verifier. The local full producer and independent verifier passed. No empirical shortest-proof search is used in the theorem.

**Five-role next tests:** LSPV-1 quantify what extra source-indexed information, beyond projected boundary semantics, a B3 proof would need; LSPV-2 attack equal-statistics constructions using mixed rule shortcuts and exact LOCAL-CONVERT; LSPV-3 construct source-authenticated interface certificates retaining topology and boundary mapping; LSPV-4 charge source access, circuit payload and peak space for those certificates; LSPV-5 audit stronger claims of representation or algorithm independence. Keep B1/B2/B3, superpolynomial mixed Wbar and P versus NP OPEN. No task changes.

**Publication safeguard:** main.tex reconciliation requires complete blob readback and conflict-safe owner-region write. Do not overwrite a partial or empty read response.
