# LSPV-4 ARC-PAYLOAD-JUMP-TRADEOFF283: five-role handoff
31 October 2026, 15:36 PDT. **P versus NP OPEN.** All existing identities, status and schedules unchanged.

**Exact obstruction:** in FLMV's deterministic indexed random-access model, an indexed move erases its input index tape without resetting the index head. Treating a source query as a single unit-time jump omits the cost of preparing the binary absolute address. Global index-erasure potential was already proved by LSPV-4 ARC282 and LSPV-1 ARC283; SAT-side source sensitivity was already proved by LSPV-1 ARC284.

**New restricted theorem:** For a policy making separate indexed jumps to physical source positions a_1,...,a_R, with blank initial input index tape and at most q zero-to-one index cell edits per native step, T >= (sum_j popcount(a_j))/q. For all P consecutive payload bits after H header bits, the exact sum is B(H+P)-B(H), B(X)=sum_h [2^h floor(X/2^(h+1))+max(0,X mod 2^(h+1)-2^h)]. For H=O(log P) this is Theta(P log P), **only for the chosen indexed-access policy**. A sequential source scan reads the same payload in O(P) operations and has no such index-write charge, so no universal SAT runtime lower bound follows.

**XOR:** In a separated physical write/jump/read event trace, sum of adjacent physical tape-content XOR is 2 sum popcount(address); each completed indexed read begins/ends with blank input-index contents, giving zero endpoint XOR. Original residual logical state never changes in read-only probing. Input-head movements, index-head positions, read operations and selector/failed/replay work are separately charged. Offline coverage mask is not an internal oracle.

**Original certified controls:** Proper duplicate-free Monotone 3-SAT-(2,2) Y6 SAT (20 exhaustive models), U198 UNSAT (six 179-node local DPLL refutations plus 64 boundary-row conflicts), V198 SAT (198-bit verified witness). This run's V198 changes two **first literals at original clauses 1 and 7 (zero-based)**; it is not the prior 2/44 V198 variant. Raw original-clause-indexed signed occurrence S/U targets, inversions, clause SS/SU/US/UU pair modes, endpoints and flip trails rechecked. Independent checker passed **3,647,073 assertions**. Y6 P=80, W=254, Dphys=508, 1,184 native events; each U/V P=6600, W=40850, Dphys=81700, 196,390 native events. Same-budget UP-DPLL: Y6 4 nodes; U/V UNKNOWN at 1,200 nodes, not UNSAT by timeout.

**Exact FLMV envelope:** d*(6/5)=23/45 and d*(241/200)=11642479/23232400, both strictly uniquely maximized at k=2, with all k>=4 excluded by c^-4 tail. The hypothetical fixed point (6/5,1/2) and the numerical SAT-to-target transfer remain CONDITIONAL/OPEN.

**Scope:** only ALL valid instances of Döcker's canonical NP-complete proper monotone exact-(2,2) target; reject malformed, preserve hereditary target or charged re-encoding. Do not assume all ordinary SAT required for qualitative P/NP, nor that target NP-completeness transfers numeric FLMV. Maintain broader signed strict-(2,2) as comparative superset.

**Sources consulted:** FLMV primary JACM Theorem 5.7 and section 2.1 PDF, Döcker 2019 original, O'Donnell et al. 2005 decision-tree background. Search queries: 'FLMV indexed tape erasure', 'Döcker duplicate-free monotone 3SAT (2,2)', 'amortized binary counter', 'decision tree source sensitivity'. Separate GitHub searches j15marti/pnp 'source reads malformed', 'ARC-INDEX-RECHARGE283', 'CP22LIFT1', 'ARC-LINEAR22-SATURATION1', and github.com/openai 'Turing machine' returned no matching universal ARC. Project reads: main.tex, AGENTS, CODEX, repo pnp-research skill, REDIRECT1, CONTRACT1, affine no-go, CONSTRUCTION-STRENGTHEN17, MODELBRIDGE-0012, CP22LIFT1, ARC279–282, LSPV1 ARC283/284, LSPV2 SWITCH-GUARD282, LSPV3 GATE284, issue #3. Known result duplication explicitly acknowledged.

**Artifacts:**
- research/agents/lspv-4/2026-10-31_1536_LSPV-4_ARC_PAYLOAD_JUMP_TRADEOFF283.tex (formal report)
- experiments/arc/lspv4_283/arc_payload_jump283.py (full Python producer)
- experiments/arc/lspv4_283/verify_payload_jump283_independent.py (separate independently written verifier)
- experiments/arc/lspv4_283/U_source.json (source fixture)
- results/summaries/arc/2026-10-31_1536_LSPV4_ARC_PAYLOAD_JUMP_TRADEOFF283_summary.json
- Full independently reproduced per-native-step compressed raw traces and full original-indexed controls are in the complete local conversation ZIP because large raw JSON was not individually mirrored to GitHub. Manifest SHA-256 included.
 
**Next proof arrow:** a uniform, genuinely power-short, all-valid-target, malformed-rejecting hereditary arbitrary-A to Phi(A) contractor with fully charged child count, source probes, output accessor, guest index/work tapes, replay, policy switching, failed attempts and simultaneous peak live space, plus a numerical FLMV transfer. External review and native end-to-end FLMV measurements pending. **P versus NP OPEN.**
