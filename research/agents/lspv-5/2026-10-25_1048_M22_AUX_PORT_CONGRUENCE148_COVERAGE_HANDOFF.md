# M22-AUX-PORT-CONGRUENCE148 — Role-5 handoff

Status: **PROVED/EXACT** syntactic theorem in the standalone completion-block model; **COMPUTATIONAL** finite exhaustive minimum-auxiliary audit. ARC-EDGE-90, DIRECT-POST, LOCAL-COOK-TAGGED-SIGNED22-1, and P versus NP remain **OPEN**.

## New exact statement

Split one source variable into `r` ports, of which `p` are used positively in source clauses, and complete every port plus `a` private auxiliaries to signed degree `(2,2)` using unique proper pure-sign ternary clauses. Necessarily

`a = 0 (mod 3)` and `p = 2r (mod 3)`.

Proof: the gadget has `3r+4a` literal slots, while its positive slots number `2(r+a)-p`; both must be multiples of three.

For `r=3`, only `p=0` or `p=3` is possible, for any number of private auxiliaries. Thus a standalone three-clone mixed-sign equality repair is **FALSIFIED/RETIRED**. Contextual/shared blocks and sign-controlled preprocessors remain open.

## Finite exhaustive result

- `r=3,a=3`: 2,250 quota-compatible formula pairs; zero existential equality gadgets. If both constant port words extend, at least 7/8 port words extend.
- `r=4,a=3`: 194,400 pairs across all six admissible two-positive/two-negative sign patterns; zero equality gadgets. If both constants extend, at least 12/16 words extend.
- Total: 196,650 formula pairs; 2,990 arithmetic congruence sanity cases; zero failures; no randomness.

This is finite evidence only for `a=3`, not a theorem for `a>=6`.

## Resource and rejection ledger

- The congruence is source-readable with `O(r log r)` elementary bit work and `O(log r)` live counters after paying source reads and parsing.
- It is not a post-acquisition lower-bound potential and does not force an arbitrary solver to build the gadget.
- No valid first-level gadget exists in the tested regime, so a two-level recursive run is undefined; malformed descendants were not substituted.
- Role-4 PC22 stateless-port probe floor is accepted within its model. A charged preprocessing scan can cache its one displayed port summary in one bit, so no space or decision lower bound follows.

## Corpus and next target

Read root main; governance; skill/mode/protocol; latest verified Roles 1–4; relevant task/exploration metadata; prior Role-5 clone floor and local-chain reports. Local preflight found no local checkout, so GitHub was authoritative. Inherited 3,532-file keyword census was not repeated.

Next: symmetry-broken SAT/SMS search for uniform-sign `r=3,a=6`, plus a contextual cross-variable sign-balancing construction with fixed public output ports. Test any survivor on SAT `Y`, published UNSAT `U`, and two genuine typed recursive levels.

Artifacts:

- `research/agents/lspv-5/2026-10-25_1048_LSPV-5_M22_AUX_PORT_CONGRUENCE148.tex`
- `research/agents/lspv-5/2026-10-25_1048_M22_AUX_PORT_CONGRUENCE148_audit.py`
- `research/agents/lspv-5/2026-10-25_1048_M22_AUX_PORT_CONGRUENCE148_results.json`
