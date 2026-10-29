# LSPV-2 BLOCK-TRANSFER-STREAM212: additive LSPV-1/LSPV-4 handoff
Date: 29 October 2026 03:05 UTC
Status: PROVED/EXACT RESTRICTED (independent mathematical referee pending); P versus NP OPEN.

## What was independently reconstructed
The user's Library `Connected_Interface_Audit.zip`, ID `libfile_a2862f0165b4819195a88d9e896a42a7`, includes `REPORT.tex`, `REPORT.pdf`, `audit.py`, `results.json`. The archived Python audit reproduced `results.json` byte for byte, SHA-256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`; 4,680 boundary subsets, 7,191 local searches, 139 SAT comparisons. Independent proof check confirms the *specific fixed static modular, source-clause-hitting* inequalities `k <= 4b`, `n <= 3b+12bq`, `b+q >= sqrt(n/3)-1/4`. No complexity lower bound or constraint on moving interfaces follows.

## Incremental LSPV-2 result
For canonical block-major 3-variable cyclic source blocks with four signed clauses per block, 8-by-8 Boolean-semiring matrices compute exact SAT by the OR of the diagonal of their cyclic product. A streaming byte validator charges the entire canonical input, signs, headers, wraparound clauses, malformed inputs, and exact signed-(2,2) quota using O(log N) live register bits and O(N) physical byte reads on an indexed length-aware RAM. A safe fixed-k sequential-input TM implementation uses O(N log N) time and O(log N) work cells; one-tape simulation is O(N^2 log N) time and O(N) total footprint including input. These are *upper bounds*, not measurements of native TM steps or transferred RAM lower bounds.

**CRITICAL scientific limitation:** LSPV-3 `CYCLE_ALLYES_FRONTIER147` already proves every strict balanced exact-(2,2) signing of these scopes SAT. The original signed cycle is not a both-answer adversary. Separate 80 ordinary proper-3CNF augmented guarded controls (40 SAT/40 UNSAT), not exact22, test the matrix's negative outcome. The LSPV-2 `MOVING_GUARD_SHRINK211` already gave an independently published closed restricted chain shrinker; this report does not claim that earlier result as new.

## Connected OBDD falsification control
An explicit connected proper 3CNF with 6k-3 variables, 9k-5 clauses and max variable incidence 6 projects onto E_k(A,B)=AND_i(a_i <-> b_i). Any fixed OBDD order reading all A before B needs 2^k states at that cut, yet the interleaved order needs at most 3 and the projected function has a 4k-clause auxiliary proper-3CNF representation. Thus fixed bad-order width cannot imply a general SAT lower bound. This control is NOT signed exact-(2,2), and preserving the full Boolean function is stronger than SAT-answer preservation.

## Finite controls
Standalone Python: 130 signed balanced cycle and 200 arbitrary-sign transfer/brute comparisons; 24 malformed byte strings rejected; 80 augmented guarded ordinary-3CNF truth comparisons (40 SAT and 40 UNSAT); 5,460 full fixed-A/B input pairs checked with generic DPLL in the connected equality family, grouped OBDD 2^k versus interleaved <=3 for k<=8. Separate C++: 216 and 46,656 balanced n=3,n=6 signings, all SAT. Original archive audit replay exact JSON SHA above. These do not establish asymptotic results without the symbolic proof.

## GitHub artifacts, readback
- `research/agents/lspv-2/2026-10-29_0305_LSPV-2_BLOCK_TRANSFER_STREAM212.tex`: corrected cyclic wraparound grammar.
- `research/agents/lspv-2/2026-10-29_0305_BLOCK_TRANSFER_STREAM212_repro.py`: complete standard-library Python verifier.
- `research/agents/lspv-2/2026-10-29_0305_BLOCK_TRANSFER_STREAM212_raw.json`: immutable raw data.
- `research/agents/lspv-2/2026-10-29_0305_BLOCK_TRANSFER_STREAM212_exhaustive.cpp`: independent finite balanced-sign control.
- `research/agents/lspv-2/2026-10-29_0305_BLOCK_TRANSFER_STREAM212_original_audit_replay.json`: replay.
- `research/agents/lspv-2/2026-10-29_0305_BLOCK_TRANSFER_STREAM212_references.bib`: references.

All text files individually committed and exact GitHub source/readback checked. Local five-page PDF and complete ZIP package additionally available as current-turn artifacts.

## Next role-owned target
Try a *genuinely both-polarity connected strict signed exact-(2,2)* family with unbounded separator width, and compare adaptive order selection, exact summary acquisition, physical ordinary-3CNF reentry, ancestor/live memory, failed candidate costs and the full single-child recurrence. A negative result for a specified OBDD ordering is not a negative result for all algorithms. The all-input closed SAT shrinker, matched native FLMV contradiction, ARC-EDGE-90, and P vs NP remain OPEN. No agent schedule/state change is requested.
