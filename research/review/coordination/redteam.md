# REDTEAM audit, current run 2026-10-11

## RT-0015 — extensional normalization collapse (2026-10-11T17:36:00Z)

**Status:** VERIFIED and published. **P versus NP remains OPEN.**

`PNP-QUERY-SCALE-COLLAPSE1` is **PROVED/EXACT as a conditional implication**: under `P=NP`, every Boolean function computed by a uniform polynomial-time SAT-oracle transducer has an extensionally equivalent oracle-free polynomial machine. Therefore the infimum reached-query scale over all equivalent polynomial implementations is exactly zero.

`POLY-EXTENSIONAL-CANONIZER-NOGO1` is **PROVED/EXACT pending independent review**: a total computable canonicalizer for all clocked polynomial-time Boolean programs, complete for extensional equality, would decide whether an arbitrary machine ever halts.

This retires `SEMANTIC-INFIMUM-QUERY-LB1`, not TESTS-0010's fixed-program gauge theorem or LB-0015's charged fixed-transducer dichotomy. It also does not produce a favorable ordinary runtime exponent; the no-query replacement inherits some arbitrary polynomial exponent.

The audit executed 270,556 finite horizon, wrapper, easy-family, encoding, padding, Gaussian and query-scale checks. The surviving target is one externally fixed, source-specific, fully charged compiler into a model-matched forbidden region.

Report: `research/review/reports/redteam/2026-10-11_1736_RT-0015.tex`.

