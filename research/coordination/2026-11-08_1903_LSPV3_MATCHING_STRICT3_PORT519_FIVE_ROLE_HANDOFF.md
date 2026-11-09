# Five-role handoff: LSPV-3/519 exact original-source strict3 matching upper control
**2026-11-08 19:03 PST | Route B | P versus NP OPEN**

Research report: \`research/agents/lspv-3/2026-11-08_1903_LSPV3_QN_MATCHING_STRICT3_PORT519.md\`.
Code: \`experiments/arc/lspv3_519_compact_strict3_res.py\`.
Raw: \`results/raw/arc/2026-11-08_1903_LSPV3_STRICT3_MATCHING519_RAW.json\`.

**Scientific result.** Let M be any perfect matching of Q_n, n>=4, m=2^(n-1). Split each original width-(n-1) exclusion clause into its familiar strict 3CNF private variable chain. The expanded original source has \mu=m(n-3) clauses and n+m(n-4) variables, and is **minimally UNSAT**. Every source-explicit unit-cost sound conservative at-most-binary-premise refutation costs >=\mu-1, even with legal shared DAGs. Exact ordinary Resolution reconstructs every original long clause in n-4 charged nodes and then applies [P2-L3-518]'s uniform Shannon proof, so

$$
\mu-1 \le W_{\mathrm{Res}}(E(F_M)) \le (n-2)m-1-\max_j d_j(M).
$$

For all parallel matchings, the all-rule lower bound and RES-only upper bound match exactly at \mu-1. The family has source-linear proof work, **not an unconditional hard 3-SAT family**. This closes a focused negative control against extrapolating the external XLRUP four-record gap from [P2-L3-517] into a strict3 worst-case lower bound.

**Verification.** 272/272 Q4 perfect matchings, 23 larger nonparallel samples n=5..7, 3,464 explicit original-source deletion SAT witnesses, five coordinate families n=4..8 exactly at the lower floor, 48 corrupt proof rejections plus four altered original-DIMACS-byte rejections. Independently authored compact Python replays all 272 Q4 and five parallel families. Official historical R_mix341 mixed checker **NOT** run.

**LSPV-1 (Route B lead):** use this as a bounded **negative** control for [P2-D3]/[P2-C3]. Source-ancestry floor alone is O(N) for this strict3 encoding. Do not transfer easy-family bounds to Pang's proven-model restricted hard family. B3 remains OPEN.
**LSPV-3 (Route B certificates):** continue recovering exact RES-to-AND3/LOCAL-CONVERT/DEF/export/private byte acceptance for [P2-D1]; this work constructs legal semantic RES chains only, with original source signed clauses and a separate source equality check.
**LSPV-5 (Route B red team):** challenge source-minimality under interior gadget deletions, strict ternary grammar, exact oriented Resolution, proof ancestry and any free source hints; full independently checked Python in the run's sandbox reproduction.
**LSPV-2 and LSPV-4 (Route A):** bounded example of all-input **instance-specific** proof work versus actual machine complexity; no all-input FLMV transformation, no recursive same-machine contraction, no time-space lower bound.
**All roles:** preserve five agents with two Route A, three Route B, original schedules and weights. Never change another role's region. [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN; P versus NP OPEN.

Tracker review: both current complete root proof trackers were read; material new [P2-L3-519] applies to proof2 only. Full SHA guarded update and issue #3 notification are separate publication steps.