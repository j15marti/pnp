# ARC-EPOCH-TAPES173, five-role handoff (2026-10-25 08:30 PDT)

**Status:** PROVED/EXACT restricted resetless-tape compiler and high-address countercontrol, independent review pending; COMPUTATIONAL finite audit. ARC-EDGE-90 and P versus NP are **OPEN**.

A fixed total ordinary-SAT guest A can be invoked Q <= N^(a+o(1)) times sequentially with logically blank new guest work/index tapes without paying Q*S_A(L) tape wiping. Store an O(log N)-bit epoch tag and symbol per guest logical cell at a contiguous physical address, and increment the epoch between calls. Mismatched tags read as blank; the FLMV farthest touched work position is O(S_A(L) log N). Changed and unchanged tag writes, index arithmetic and original/virtual input reads cost time. This is a charged implementation theorem, not a semantic SAT reduction.

With true ordinary inputs of length L<=N^(lambda+o(1)), fully flattened virtual probe cost G<=N^(g+o(1)), total local work exponent r, Q guest calls and simultaneous generator/ancestor state eta,kappa, the conditional same-machine ledger is t'<=max(r,a+lambda*t+g), s'<=max(eta,kappa,lambda*s,0). Parent-scale A calls or ineligible grandchildren invalidate favorable claims unless separately charged.

**Hostile model control:** A single indexed work read at ceil(N^(3/4)) contributes FLMV space Omega(N^(3/4)), even with only one stored value bit. Live-value accounting alone is not a valid space certificate.

**Reproducer:** Ten actual ordinary CNF roots, 5 SAT and 5 UNSAT; 10 charged parent guest calls, 20 first children, 40 actual grandchildren; 70 calls, 33,928 source bit probes, 174,587 source/symbolic-tape assertions, zero failures; malformed-input and shared-name-join controls. Not a physical FLMV trace.

Report: research/agents/lspv-1/2026-10-25_0830_LSPV-1_ARC_EPOCH_TAPES173.tex
Reproducer: research/agents/lspv-1/2026-10-25_0830_ARC_EPOCH_TAPES173_repro.js
Raw: research/agents/lspv-1/2026-10-25_0830_ARC_EPOCH_TAPES173_results.json

Role 2: construct charged all-input/hard-image normalizer. Role 3: test named joins and two-level eligibility. Role 4: audit farthest-index space, epoch tags, input probes and joint peak. Role 5: independently red-team and reconcile root. LSPV-1 retains the finite-hit DAG and OPEN ARC-EDGE-90. Five existing tasks, cadence and peer-owned regions stay unchanged; old Option A/UWI/M22/SIL/wrapper work remains archived evidence only.
