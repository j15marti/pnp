# DIFFERENTIAL-HARNESS55

**Timestamp:** 2026-10-22 04:00 Asia/Seoul (hourly scheduled check)
**Global status:** **P versus NP OPEN. P versus RP OPEN.** No root `main.tex` change.

## Repository check
Repository accessible. Since the last check: FIREWALL54 (verifier-replacement lemma 54A: a hard-looking RP verifier can decorate an easy language, so selected-verifier structure is not a language lower bound) plus Grok 4.7 review/`main.tex` restoration commits. No new substantive role construction after PARITY-AFFINE-JOINT-BYPASS53.

## This run: the harness FIREWALL54 asked for (COMPUTATIONAL)
Fixed easy language (odd parity on 3 input bits); verifiers `V_B` (parity-plus-linear-kernel balanced decorator), `V_bit`, `V_0` over 6 random bits. Exhaustive check:

| verifier | YES acceptance | min positive-subcube certificate | ANF degree |
|---|---|---|---|
| V_B | 1/2 | 5 | 2 |
| V_bit | 1/2 | 1 | 1 |
| V_0 | 1 | 0 | 0 |

Languages identical; all three invariants vary. Rule adopted for future reports: any proposed invariant must be listed with its value on all three verifiers, or a canonicalization theorem must be stated. This is a finite regression control, not a theorem about P vs RP or P vs NP.

Script: `experiments/review/2026-10-22_differential_harness55_audit.py` (runs well under 30 s).

## Next single test
Specify a uniform compiler from an arbitrary RP verifier to a deterministic decider/hitting set and check whether it needs advice to remove the decorator (this is exactly the open P=RP content).
