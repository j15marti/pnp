# REPRESENTATIVE-MAINTENANCE-CEILING5 handoff

Date: 2026-10-19 21:48 KST. P versus NP remains OPEN.

## Exact theorem

For a finite enumerable witness class `W`, descriptors of at most `L` bits,
enumerator workspace `G`, evaluator workspace `V`, and `N`-bit semantic outputs,
one current witness suffices to preserve the complete observed prefix.

On source bit `x[t]`, enumerate candidates `w` and select the first satisfying
`f_w(t)=x[t]` and `f_w(j)=f_current(j)` for every `j<t`. If none exists, reject
permanently. The invariant proves exact witness-or-reject behavior.

- Workspace: `2L + G + V + O(log N)` bits.
- Update time: `O(|W|(t+1)E)` plus enumeration overhead.
- Search-MCSP specialization for `n<=s`: `O(s log s)` space and
  `2^{O(s log s)}` worst-case update time.

This falsifies space-only prefix/state-count lower bounds. It does not meet the
MMW requirement of both polynomial space and polynomial update.

## Independent audit

- All 256 witness families over 3-bit outputs against all 8 sources.
- Circuit cases: all 16 `(n,s)=(2,1)` sources; all 256 `(3,2)` sources; 64
  seeded `(4,2)` sources.
- 3,329,283 candidate trials.
- 2,750,976 prefix comparisons.
- 8,804,963 circuit bit evaluations.
- Zero failures.

## Next falsifier by role

- `:00`: actual CHMY generator, both threshold promises, tape/error accounting.
- `:12`: attack representative replacement under `poly(s)` update; do not use
  prefix count alone.
- `:24`: charge exponential update before proposing this compiler for ARC.
- `:36`: audit uniform enumeration, malformed descriptors, oracle gates and
  output serialization.
- `:48`: preserve the space ceiling and allocate to the update-time gap.

Root `main.tex` was not edited.

`FINAL_VERIFICATION_SENTINEL::HANDOFF::REPRESENTATIVE-MAINTENANCE-CEILING5::P_VS_NP_OPEN`
