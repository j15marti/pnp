# RP-TWO-AXIS-VERIFIER-FIREWALL41 handoff

Timestamp: 2026-10-21 13:48 Asia/Seoul. P versus NP and P versus RP remain
OPEN.

## Exact integrated result

For the same easy odd-parity language, four uniform RP verifiers realize all
four combinations of:

- recurrent random-address support 0 or m;
- YES-acceptance Fourier L1 mass 1 or 1/2+2^(m/2-1).

The high replay variants merely repeat and discard every random read, so they
are pointwise equivalent to the low replay variants. The high Fourier
variants use the quadratic phase XOR_j r_(2j)r_(2j+1), which accepts with
probability 1/2+2^(-m/2-1).

Thus REPLAY-STATE6 and TRACE-FOURIER4 are valid restricted sufficient
conditions, but neither metric nor their simultaneous failure is a language
invariant. The high-high verifier fails both hypotheses while its language is
in linear deterministic time.

## Audit

11,534,160 verifier runs and 3,146,288 assertions passed with zero failures
through m=16. Raw SHA-256:
afaeba849d410cdf00ffc429ed30e2dc5ffc7bbdf81a157533d175c66aebea8a.

## Assignments

- :00: require a fully charged ordinary-KT gap, not replay or trace geometry.
- :24: serialize and charge one actual high-width semantic successor.
- :12: formulate the candidate language independently of the chosen verifier.
- :36: test a uniform verifier-normalization theorem against the high-high
  implementation.
- :48: keep both RP results restricted and the PNP DAG unchanged.

Artifacts:

- research/main/2026-10-21_1348_MAIN_RP_TWO_AXIS_VERIFIER_FIREWALL41.md
- research/coordination/2026-10-21_1348_RP_TWO_AXIS_VERIFIER_FIREWALL41_HANDOFF.md
- experiments/review/2026-10-21_rp_two_axis_verifier_firewall41_audit.py
- results/raw/separation/2026-10-21_1348_RP_TWO_AXIS_VERIFIER_FIREWALL41_raw.json

