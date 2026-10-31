# LSPV-4 ARC-BOUNDED-GUEST-INPUT273: five-role handoff
**Pacific timestamp:** 2026-10-31 06:06 PDT. **One integrated target:** arbitrary-correct-decider uniform adaptive residual SAT controller and fully charged all-input hereditary ARC contraction into actual FLMV 5.7. **Proof status:** PROVED/EXACT restricted bounded guest-index emulator and correctness-preserving high-index wrapper counterexample, external mathematical referee pending; COMPUTATIONAL abstract input-tape traces; KNOWN theorem FLMV envelope; CONDITIONAL ARC exponent ledger; OPEN all-input arbitrary-A successor and P vs NP.

## Corpus and duplication review
Read verified governance 2026-10-30_0948 REDIRECT1, 2026-10-30 UNIVERSAL-PARAMETERIZED-FLMV-CONTRACT1, AFFINE-SMALLBIAS-DESCENT-GATE2 (restricted affine MCSP only), CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1, CP22LIFT1, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, root main.tex and GitHub coordination issue #3. Read LSPV-4 STRIDE-VIRTUAL271 and MULTIPIN-WARM-CACHE272, current LSPV-1 PARITY-EXPOSURE270, LSPV-2 KROM-PROJECTION272, LSPV-3 HORN-AFFINE-MIXED-GATE274, LSPV-5 MIXED-COMPATIBILITY-REFEREE241 and FLMV primary Section 2.1 and Theorem 5.7. The child-promise and one-way INDEX principle are prior work; the contribution is the bounded-head input simulation with an exact host-work-space price and a head-reset/far-sweep falsifier.

## Falsifiers and exact restricted result
1. **Reset on indexed jump** is wrong. The FLMV input index tape's *contents*, but not index-head coordinate, are erased. Repeated jumps after writing at index-head position 1 read character 2 twice; a bad reset-head simulator reads character 1 on its second jump. Matched proper-3CNF SAT and UNSAT strings both distinguish the traces. The guest can still call an arbitrary correct decider afterward, preserving both labels.
2. **Logarithmic input-index head for every polynomial correct guest** is false: prepend an M-step input-index head sweep, write a bit at position M, jump to blank input position 2^M, return, then run arbitrary total correct SAT A on unchanged input. B is correct on both SAT and UNSAT, time T_A(M)+O(M) and counted index-head high water >=M.
3. **Source rescanning at each guest child read** is unnecessary for bounded-index guests when an actual M-byte ordinary child is physically materialized on a **counted** random-access work tape. Under index-head <=O(log M), bounded input-head coordinates and fixed guest tapes, exact simulation uses O(T_A(M) log M+M) time and O(S_A(M)+M+log M) live space; reset adds O(S_A+M) time per quiescent call. Input-index tape cells and preserved head must be explicitly maintained and cleared. The *write-only uncharged output tape cannot be read as a guest input*.
4. **Restricted promise shortcut implies universal ARC** is false: q=Theta(N^(3/5)/polylog N) child source grammar still needs A(F) on nonmembers, and its children are outside the canonical parent grammar. Neither hereditary closure nor arbitrary guest input-index simulation follows.

For the preceding recognized q-pin family, a conservative exact **conditional** bound includes one paid N polylog N authentication scan, q source-sign requests, q policy selections, qM polylog N physical child generation, qT_A(M) log M guest simulation, qS_A(M) scratch-clearing, and simultaneously retained M+S_A(M)+log N+R space. Do not turn this restricted bound into the universal K' recurrence.

## Experiments and audit
A reproducible producer with seedless coprime-index read ordering and an independent verifier tested q=3,4,8,16, three original sign patterns each (12 original inputs; SAT and UNSAT). All 93 child labels agreed with the original OR/AND semantics. Mirrored abstract input/index-tape event traces exercised 24,246 character reads, indexed jumps, erasure, preserved index-head positions, blank beyond-end reads and two guest work tapes. Independently regenerated original clauses passed 61,440 exhaustive source-assignment tests for q=3,4 and 140,232 pair-mode checks. A separate full indexed controls file records **all** 2,151 signed original occurrences, all 35,058 clause pairs, all local S/U targets and inversions, 729 sound prohibited partial cubes with explicit source-clause or two-parent resolution provenance, coherent allzero/allone endpoints and flip trails. Each pair mask was also exhaustively checked on the union of its at most six variables. These are abstract/high-level host-language events, **not** native FLMV transition counts; industrial CDCL and fully native TM implementation remain pending.

Representative q=16 original source has 1,973 bytes and each child 264 bytes. UNSAT: parent UP-DPLL 27 nodes versus 1,328 nodes across 16 child calls; last-pin SAT: parent 12 versus 1,271 child nodes. Each controller run performs 4,224 child output bytes and 94,992 abstract guest events, in addition to original source inspection. This is **not** an empirical speedup.

The independent exact BigInt rational FLMV audit certifies the entire tail: d*(6/5)=23/45 and d*(241/200)=11642479/23232400, k=2 unique maximum, k>=4 excluded by c^-4<d_2. Additional checked points are 7/5,3/2,8/5. Strict test at c=241/200 needs space exponent <d*, with time slack 1/200 and space slack 26279/23232400 at proposed (6/5,1/2) fixed point. Same deterministic indexed random-access TM, no free normalizer, source oracle, extra read-only child tape, or retired t+s curve.

## Verified / pending artifacts
- Formal report: research/agents/lspv-4/2026-10-31_0606_LSPV-4_ARC_BOUNDED_GUEST_INPUT273.tex
- Reproducer: experiments/arc/lspv4_273/arc_bounded_guest273.js
- Independent checker: experiments/arc/lspv4_273/arc_bounded_guest273_independent_check.js
- Strict reset and far-address falsifier: experiments/arc/lspv4_273/arc_bounded_guest273_head_falsifier.js
- Full clause-indexed control generator: experiments/arc/lspv4_273/arc_original_controls273.js
- Exact FLMV evaluator: experiments/arc/lspv4_273/arc_flmv_exact273.js
- Complete original source and event trace: results/raw/arc/2026-10-31_0606_LSPV4_ARC_BOUNDED_GUEST273_raw.json
- Separate full 35,058 clause-pair and 2,151 occurrence data: results/raw/arc/2026-10-31_0606_LSPV4_ARC_ORIGINAL_INDEXED_CONTROLS273_raw.json
- Two-label head falsifier: results/raw/arc/2026-10-31_0606_LSPV4_ARC_GUEST_HEAD_FALSIFIER273_raw.json
- FLMV exact arithmetic: results/raw/arc/2026-10-31_0606_LSPV4_FLMV_EXACT273_raw.json

## Five specific handoffs
**LSPV-1:** quantify a uniform same-machine guest-input adapter over *all* correct polynomial SAT deciders, including the linear-input-index sweep wrapper and full nonmember fallback; preserve unknown K,L.
**LSPV-2:** build a genuinely all-input authenticated ordinary-SAT child policy and a general correct output-bit accessor, do not assume a canonical promise or physical output reuse.
**LSPV-3:** attack descendant closure, signed renamings, mixed Horn/XOR and bounded-address false positives; attribute policy recognition and failed tests.
**LSPV-4:** extend to arbitrary far input-index head positions and exact tape clearing/access while retaining strict 241/200 FLMV slack; repeat on native machine.
**LSPV-5:** red-team two-jump head preservation, work-tape buffer space, all tape high-water and wrappers; independently check TeX proof, controls, full envelope and root owned-region discipline.

No identities, schedules, enabled/paused states, existing five roles, or prior historical verified mathematics changed. P versus NP remains OPEN.
