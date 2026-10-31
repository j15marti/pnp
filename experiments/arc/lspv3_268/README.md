# HORN-GUARD-SET-COVER-GATE268

LSPV-3, 2026-10-31 00:24 PDT. **Original source results plus independent verifier.**

```
python arc268.py --output raw268.json
python verify268.py raw268.json verification268.json
```

`arc268.py` uses `arc267.py` (bundled unchanged from the preceding verified LSPV-3 run). Python 3.11+ and no external dependencies. Each invocation finishes within 30 seconds. `raw268.json` preserves all original clauses, original source indices, local occurrence S/U target inversions, original source-indexed pair compatibility, endpoints and flip traces, paired source SAT/UNSAT outcomes, Horn guard optimization work, and fallback. `verify268.py` independently checks actual original-source clauses and exhaustive witnesses/UNSAT absence; it imports neither producer. There is no original-source UNSAT proof in DRAT/LRAT form; the Horn-UP contradiction records original clause IDs and the independent verifier checks UNSAT exhaustively on the finite cases. The NP-completeness result is a symbolic proof and is not inferred from finite experiments.

`selected work` is a declared host-language proxy, not an FLMV native machine counter. The `declared_live_bit_envelope` is a conservative *symbolic* tally for a conceptual source+controller, not a measurement or verified upper bound on Python memory. In the current run all policy-selection costs, failures and candidate queries are recorded, but diagnostic exhaustive verification is deliberately outside online controller work.

All previous agent identities, schedules, and enabled/paused states are unchanged. P vs NP OPEN.