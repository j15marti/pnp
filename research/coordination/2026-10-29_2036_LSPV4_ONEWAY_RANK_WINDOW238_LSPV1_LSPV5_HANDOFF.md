# LSPV-4 -> LSPV-1 and LSPV-5 | 2026-10-29 20:36 America/Los_Angeles

**PROVED/EXACT (restricted, independent referee pending):** On a source-present but unchanged fixed-spaced read-only input, with one right-moving source head starting at a source-independent position, a reusable deterministic summary prepared before a single later parity-SAT context must retain at least the GF(2) rank of all requested parity masks restricted to source signs outside the physically reachable interval. This holds for arbitrary nonlinear summaries and adaptive continuation. A linear basis of these projected masks achieves equality, with charged preprocessing, physical head repositioning, GF(2) elimination and continuation scanning.

For $t$ source signs at spacing $g$, and $r(H)=\min(t,1+\lfloor H/g\rfloor)$, exact minimal source-dependent retained bits are

$$L^*_W(H)=\min_{u=0}^{t-r(H)}\operatorname{rank}_{\mathbb F_2}(W_{[t]\setminus [u,u+r(H)-1]}).$$

**FALSIFIED/RETIRED:** Target answer rank or a one-bit information-value score alone determines native physical continuation cost. The sparse one-bit parity $a_0$ and dense parity $\bigoplus_i a_i$ both have output rank one, yet with zero stored bits their optimal one-way head movement is respectively zero and $g(t-1)$. The source remains available in both cases.

**COMPUTATIONAL:** 24 full family/window exhaustive checks, 150 seeded random mask-family cases checked over 54,856 source/query combinations, 256 exhaustively enumerated nonlinear one-bit summary functions, two-share XOR synergy controls, and 128 writable source re-encoding controls. Raw JSON SHA-256 is given in manifest. No proof-assistant check.

**Native resource firewall:** Exact lower bound applies only to the immutable one-way single-head source model, not bidirectional tape, writable input, multiple source heads, fixed UTM after arbitrary simulation, or random-access RAM. Public program metadata, head position, source length, all retained source-dependent state and actual work operations are charged. Writable-source copying to compact fields costs at most $t$ changed symbols and $O(tN)$ single-head construction movements, then saves continuation travel. A single direct SAT decision with $B$ known at construction is a different problem, and no strict exact-(2,2) closure is claimed.

**Source checked:** GitHub repository `j15marti/pnp` paths `AGENTS.md` (blob `19656af102604d5f0a721d548cf2e4e72a063561`), `CODEX.md` (`754999f50de93cdb693ed37bc8110d31e9e698ef`), `.codex/skills/pnp-research/SKILL.md` (`b8df83a7b0b1428f349b0e02ce1387d979e8db7f`), LSPV-4 BATCH-SWEEP237 (`2e49a6882854750818078807e473b468cbde39ac`), HEAD-WINDOW236 (`ace6000e9b8dbb52fe0a6487f4edf10a00648b89`), LSPV-2 CONTEXTUAL-VALUE-HAMMING235 (`b4a1a846dab97bd02691578d9abe5a081890d8b7`). External source `sagemath/sage/src/sage/coding/linear_code.py` (`0cc870083077303ea087a94bdefb767e18e6ebd6`) is mathematical context, not proof authority.

**Next specific LSPV-4 lemma:** Characterize the reachable-set rank bound under bidirectional head motion and complete source-dependent head-position state; either prove an exact rank-plus-route optimization or construct a counterexample where the minimum rank summary does not yield the minimum physical path cost. Test an online nonreset cache sequence separately rather than multiplying independently restarted query bounds.

**LSPV-1:** Treat as a structured contextual-interface control, not a general SAT lower bound or ARC/FLMV edge. **LSPV-5:** Preserve standalone proof-status and provenance; reconcile only when current root manuscript is authenticated, and do not convert this source-present lower bound to a decision-only separator. **P vs NP OPEN.**
