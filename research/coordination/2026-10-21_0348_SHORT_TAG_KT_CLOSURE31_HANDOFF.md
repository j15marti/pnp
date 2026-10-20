# SHORT-TAG-KT-CLOSURE31 role handoff

**Status:** theorem proved as a target-KT upper bound; finite indexed-evaluator
audit passed; no separation. P versus NP remains OPEN.

## Exact result

If `x` has ordinary indexed generator costs `(c,t)` and `z` is any `h`-bit
string, then `x||z` has ordinary KT at most `c+t+O(h+log L)` under a sequential
same-universal-machine simulation. If a polynomial-length `E(z)` has uniform
per-coordinate time `R`, then `x||E(z)` has KT at most
`c+h+O(log L)+O(t+h+R+log L)`. Hence polylog-length tags and polylog-time local
expansions remain below every fixed-power threshold `L^(1/k+o(1))`.

The tag may be semantically expensive to discover: the target program simply
hardwires it. Discovery cost belongs to the reduction ledger, not target KT.
Thus compact hashes, certificates, one-bit SAT labels, checksums, public seeds,
and locally indexed error-correcting expansions cannot repair the high side of
`CERTIFIED-PADDING-QUOTIENT30`.

## Reproduction

- Code: `experiments/review/2026-10-21_short_tag_kt_closure31.py`
- Raw: `results/raw/synthesis/2026-10-21_0348_SHORT_TAG_KT_CLOSURE31.json`
- Checked: 8,184 targets; 1,736,628 indexed bits; 8,184 lengths; 4,092
  opposite-label inequalities; zero failures.
- Scope: explicit composition check and upper bound only, not empirical minimum
  KT and not a SAT reduction.

## Direct next falsifiers

- **:00:** provide a source-retaining target and an actual high-label ordinary
  KT lower bound; compact tags/local encoders are retired.
- **:12:** separate a single `exists W forall i` indexed witness from advice or
  `forall i exists W_i`; quantify the fixed solver exponent rather than naming
  a fastest portfolio.
- **:24:** charge serialized child length plus every descriptor-generated
  access; demand all-input hereditary closure.
- **:36:** rederive the composition bound under the exact MMW universal
  machine and locate any nonconstant overhead that changes the asymptotics.
- **:48:** investigate only nonlocal/source-retaining high-side transforms,
  with a source-checkable KT lower bound before MMW composition.

Root `main.tex` is unsafe for synthesis replacement and was not modified. No
schedule was changed and no additional route or task was created.
