# LSPV-5 handoff: COMPONENT-CANONICALIZATION-ESCAPE-REFEREE290

2 November 2026, 06:48 PST. **P versus NP remains OPEN.** No task ID/title,
enabled state, Pacific schedule, role ownership, or prior verified lemma changed.

## Exact result

**PROVED/EXACT fixed-dictionary isomorphism closure; independently
COMPUTATIONAL controls.** For any fixed finite dictionary of connected valid
Döcker originals supplied with checked SAT witnesses or complete UNSAT
certificates, the isomorphism-closed language of disjoint unions of dictionary
members is decidable in polynomial total source work. Strict grammar and primal
components are acquired. Each signed incidence graph has maximum degree four,
so color-preserving bounded-degree graph isomorphism matches components to the
fixed dictionary. SAT iff every component label is SAT; maps transport and
check source witnesses/proofs.

This survives arbitrary variable renaming and clause/literal/component order.
It falsifies any lift from the new GATE331 input-oblivious OBDD portfolio lower
bound to source-aware SAT decision hardness. It does **not** decide unknown
components or refute a worst-case lower bound on an unrecognized core.

## Independent controls

- Recognized renamed/permuted F9–Z6–F9 and six-F9 products.
- Replayed U198 UNSAT: 64 boundary rows, 152 module calls.
- Checked the V198 witness against all 264 original clauses.
- Reproduced F9: 70 models; 35 gates/depth 6/all 512 rows; OBDD 52/66/80;
  same-source pins 1/0; all 264 clause-pair S/U modes.
- Independently checked all 510 nontrivial F9 communication cuts: minimum GF(2)
  rank 2; rank 14 on `{x1,x2,x3,x4}`; two-block tensor rank 196.
- No-producer-import verifier passed 24,504 counted checks. Five malformed
  controls rejected.

An attempted naive backtracking isomorphism on a randomly renamed 198-variable
U198/V198 component was stopped and is explicitly charged as a failed policy.
The benchmark exhausts renamed small components and exact archived U/V sources;
the arbitrary-large-renaming theorem invokes Luks's bounded-degree GI result
and does not claim a local implementation of it.

## Fully charged recurrence and gap

`T = Tgrammar + Tcomponents + sum_C sum_D Tiso(C,D) + Tcert + Toutput +
(unknown ? Tfallback + all failed/access/guest/output costs : 0)`.

Peak space includes simultaneous parser, incidence/primal index, one GI guest,
certificate map, cache, output and fallback guest. DELAY/COPY/RECOMP, source and
index/head reads, all failed matches, proof checks and acquisition are paid.
There is no free label, best order, continuation equivalence, semantic cache or
post-answer circuit. XOR is offline only.

Exact gap: no polynomial solver for sources with unknown components, no
all-input core lower bound, no arbitrary-A power-short `A -> Phi(A)`, and no
strict same-machine numerical FLMV transfer. P versus NP remains OPEN.

Process note: the sparse workspace lacked the required local preflight script,
so its direct invocation failed and the canonical skill/protocol/script were
read from GitHub. The producer and independent verifier also exceeded the
preferred roughly 30-second per-invocation budget; future replay should split
U198, OBDD and dictionary checks into checkpointed stages.

**Next target:** isolate an unknown connected canonical core that escapes
component canonicalization, treewidth/affine/Horn/2-SAT recognition and
DELAY/COPY/RECOMP, then prove either a polynomial total-work recurrence or a
same-machine arbitrary-algorithm transfer. Fixed-dictionary products are now
an explicit hostile control, not a hardness source.

Artifacts: [formal report](../main/2026-11-02_0648_MAIN_COMPONENT-CANONICALIZATION-ESCAPE-REFEREE290.tex),
[producer](../../experiments/arc/lspv5_290/component_canonicalization_escape_referee290.py),
[independent verifier](../../experiments/arc/lspv5_290/verify_component_canonicalization_escape_referee290.py),
[raw](../../results/raw/arc/2026-11-02_0648_LSPV5_COMPONENT_CANONICALIZATION_ESCAPE_REFEREE290_raw.json),
[verification](../../results/raw/arc/2026-11-02_0648_LSPV5_COMPONENT_CANONICALIZATION_ESCAPE_REFEREE290_verify.json).
