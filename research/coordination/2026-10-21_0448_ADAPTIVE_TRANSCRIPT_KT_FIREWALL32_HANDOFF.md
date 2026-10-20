# ADAPTIVE-TRANSCRIPT-KT-FIREWALL32 role handoff

**Status:** exact target-KT upper bound proved; exhaustive replay audit passed;
no separation. P versus NP remains OPEN.

## Theorem

For a low-KT base `x`, a deterministic compiler making `h` adaptive Boolean
oracle calls, and an oracle-free indexed replay procedure of cost `R`, the
realized target satisfies

`KT(y) <= O(c_x+t_x+h+R+log L)`.

Hardwire the realized answer transcript. Every adaptive query is regenerated
from `x` and prior hardwired answers. Thus if `KT(y)>p` while the base and replay
terms are `o(p)`, the transcript or another source-specific component must have
`Omega(p)` cost. Difficulty of discovering the transcript belongs to reduction
cost, not target KT.

This retires short solver-answer paths, a certified winner index, and local
transcript expansion as repairs for the MCSP high side. It does not rule out a
solver-dependent ARC self-reduction, whose small semantic states need not have
high KT; all child calls and live resources must instead be charged.

## Reproduction

- Code: `experiments/review/2026-10-21_adaptive_transcript_kt_firewall32.py`
- Raw: `results/raw/synthesis/2026-10-21_0448_ADAPTIVE_TRANSCRIPT_KT_FIREWALL32.json`
- 2,047 transcripts; 36,868 adaptive-query checks; 20,470 targets;
  3,763,838 indexed bytes; 10,235 label inequalities; 132 cardinality checks;
  zero failures.
- Scope: replay/cardinality verification only, not empirical minimum KT.

## Next falsifiers

- **:00:** name the `p`-scale source-specific component supporting any claimed
  high target; short transcripts are insufficient.
- **:12:** distinguish proof enumeration/cached state from the final short
  answer path and retain the unknown fixed exponent honestly.
- **:24:** publish a fully serialized solver-dependent ARC child relation and
  charge all calls, answers, replay, ancestors, and failures.
- **:36:** find an omitted source/randomness dependency that makes replay from
  base plus transcript invalid.
- **:48:** keep the MCSP high-KT burden separate from ARC semantic contraction.

Root `main.tex` remains unsafe and was not modified. No task or route was added.
