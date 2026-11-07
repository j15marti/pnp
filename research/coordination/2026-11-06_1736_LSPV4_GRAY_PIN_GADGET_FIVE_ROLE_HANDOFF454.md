# LSPV-4/454 five-role handoff | November 6, 2026 17:36 PST
**Allocation unchanged:** TWO Route A (LSPV-2 and LSPV-4) and THREE Route B (LSPV-1, LSPV-3 and LSPV-5). No task, schedule, weight or historical grammar edits.

**PROVED/RESTRICTED:** On LSPV-2/456's authenticated original strict signed 3CNF block-path source, one actual child per block can be reused across all $2^{2w}$ boundary assignments. Append fixed-layout pin literals or, for a strict-3CNF guest, four proper three-literal clauses with two fresh variables for each pin. Reflected Gray-code assignment transitions mutate only 1 or 4 paid polarity fields, never a complete child.

With $h,L_{\max}\le N^{1/2+o(1)}$, $w\le\log_2N/20+o(\log N)$ and a fixed uniform correct SAT guest A with exponents t,s, the restricted wrapper has
$$
t'\le\max(1,3/5+t/2),\qquad s'\le\max(1/2,s/2).
$$
The local construction exponent improves from 11/10 to 1. The guest-time fixed point 6/5 does not change. Child source bits, index tapes, scratch logs, guest high-water space, input authentication, head operations and all joining costs are paid. No invalid assumption-context reuse.

**COMPUTATIONAL:** 56 signed source strict 3CNF cases, 38 SAT/18 UNSAT, 243 genuine guest checks, 421 Gray transitions, 60 strict ternary-gadget tests, 168 malformed controls; independently written JS passed 639 checks, no failures. Full Python/JS and raw fixtures in local ZIP.

**Hard family ledger:** odd-charge expander Tseitin original 3CNF, 4H clauses, $N=\Theta(H\log H)$, $2^{\Omega(H)}$ ordinary DAG Resolution proofs; GF(2) parity shortcut valid. Intact source-packet path frontier $\Omega(H)$ excludes this wrapper. No R_mix341/all-machine lower bound follows.

**OPEN:** no uniform all-input recursively iterable same-machine Phi(A), no charged arbitrary-input decomposition, no Route B all-mixed-rule minimum or B3. Pin-augmented descendants need not satisfy restricted original source grammar. Root main.tex unreadable at blob d48dd0fb and unchanged.

Report: research/agents/lspv-4/2026-11-06_1736_LSPV4_GRAY_PIN_GADGET_RESOURCE454.md
Code: experiments/arc/lspv4_454_gray_pin_selfcheck.js
Raw: results/raw/arc/2026-11-06_1736_LSPV4_GRAY_PIN_GADGET_SUMMARY.json
P versus NP OPEN.