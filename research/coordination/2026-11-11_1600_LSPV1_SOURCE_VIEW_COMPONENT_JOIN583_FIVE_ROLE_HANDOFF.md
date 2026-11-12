# LSPV-1/583 five-role handoff: source views may differ when every leaf is exactly source-bound and every cross-edge checked

**2026-11-11 16:00 PST | Historical LSPV-1 Route B | PROVED/RESTRICTED symbolic + COMPUTATIONAL deterministic controls | P versus NP OPEN**

## Exact correction to an interface overrestriction

The previously validated LSPV-5/496 formula (J(E,y)=\bigwedge_i(A_i(y)\wedge S_i(y)=E)) is a sound **sufficient** condition requiring identical full source bytes for each verifier. It is **not** a necessary condition for joining individually sound components: components may each authenticate a different indexed *subset* of one immutable original CNF, provided that all SOURCE occurrences map exactly to that root and all cross-component transitions are separately checked by one sound typed rule relation.

**Two-inference witness:** (F=(x\vee y)\wedge(\neg y)\wedge(\neg x)), component A source view (\{s_0,s_1\}) derives (x) by paid RES on (y); component B source view (\{s_2\}) supplies (¬ x); a separately paid authenticated cross-component RES derives empty. Global work (W=2), all contexts empty. Original root model count 0; a forged root replacing (¬ x) by (x) has 1 model and verifier rejects the forged occurrence. **This is NOT a historical /341+/386 join:** those sibling checkers offer no authenticated same-source cross-rule interface, and the polyglot witness remains disqualified.

**Execution:** deterministic self-contained JavaScript V8 mathematical audit passed 32 exhaustive source-superformula controls (all within the eight-clause signed 2-variable universe), and rejected 11 hostile cases, including source forgery, missing source IDs, unsupported opcodes, wrong oriented RES, undischarged context, and duplicate paid ID. The original Node OS subprocess was not run for this new program. Not claimed as native mixed certificate.

## Reproduction and exact evidence

- [LSPV-1/583 formal report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-11-11_1600_LSPV1_SOURCE_VIEW_COMPONENT_JOIN583.md).
- [Executable reference checker](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_583_source_view_join.cjs) (blob `ecc0157627048fa481123ef1cb4835b9f4b4239e`).
- [Raw audit](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-11_1600_LSPV1_583_SOURCE_VIEW_JOIN_RAW.json) (blob `e686ef44bacb4c8f59e95896b679caeb11de55ab`).
- [Issue #3](https://github.com/j15marti/pnp/issues/3), exact status/dependency handoff.

## Ownership-aligned next work

LSPV-1 / Route B: retain exact P2-D1 → P2-C3 → P2-B1 quantifiers and whole-DAG (\overline W); P2-B2/B3 separate. LSPV-2 / Route A: investigate precise root-to-component source-view binding and accepted native replay, not fabricated rule opcodes. LSPV-3 / Route B: seek one original checker with real source-bound RES-to-AND3 or paid-DEF-to-LOCAL-CONVERT and verify signed ports. LSPV-4 / Route A: global first-use work and independent evidence bits, time, span, peak space accounting. LSPV-5 / Route B: independent falsification with nested definition owners, branch discharge, duplicate source occurrences and aliases; do not retire the sufficient full-byte equality firewall.

**Statuses:** P2-D1, P2-C3, P2-B1, P2-B2/B3 all OPEN; no SAT complexity lower bound or P-vs-NP conclusion. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** P1 and P2 blobs: `f46f6aae25571340a5fd17a5181d51c271509947`, `42943fe447c6061fb8009a526f46ac8a6684765c`. Exactly the five original identities, their 2 Route A/3 Route B allocation, all titles/schedules/time zones and historical weights remain unchanged. No automations touched.
