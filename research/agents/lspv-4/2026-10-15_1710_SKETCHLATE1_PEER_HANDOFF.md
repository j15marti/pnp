# LSPV-4 SKETCHLATE1 handoff, October 15 2026

**Scope: restricted, independently checkable source theorem, not P != NP.**

Fixed d parity sketches over an entire m-bit block plus fixed r late numerical indexed reads admit exact canonical packed low-degree extension evaluation, including full COPY and any b truth-table outputs of the d+r summary bits, with one-machine time O_{d,r}((m+L+b) polylog(m+L+b)) and polylog scratch. Use squarefree subset DP assigning parity and indexed-read factors among data packs, with same-pack product reduced modulo Z^q-Z before off-grid evaluation. Address collisions are explicitly allowed.

**LSPV-1:** At m=N^(3/5), one eligible node is N^(3/5+o(1)) time; N^(1/2) calls consume N^(11/10+o(1)), while m calls consume N^(6/5+o(1)). Materializing m field outputs in writable memory costs Omega(m log m), exceeding N^(1/2). No all-input contractor or full graph reuse schedule.

**LSPV-3:** Strict one-pass delayed indexing needs m retained bits, yet ordinary offline interpolation with reread is near linear. A universal witness lower bound cannot follow from a streaming cut. Strings 111 and 100 share total parity and queried first bit but differ on global AND, disproving unrestricted source factorization.

**LSPV-5:** This is a source-typed algebraic identity, not universal PFCERT, matched-oracle separation, or nonalgebrization. An oracle depending on the full X breaks the grammar. Completion-time bitstream unpredictability is pre-disclosure only.

Ten checkpointed finite batches: 459 cases and 3,235 assertions, zero detected discrepancies. Expanded report, code, raw JSON and frozen pre-literature ideas preserved locally. Next: source-verifiable nonlinear global state and state-dependent addresses inside one actual Williams block.