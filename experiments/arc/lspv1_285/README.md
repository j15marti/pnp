# ARC-VALID-STATE-FIREWALL285: reproducible source-bit experiment

**Scope:** exact duplicate-free proper Monotone 3-SAT-(2,2) input language; original U198/V198 SAT+UNSAT controls; a restricted fixed-header binary input-isolation theorem, not P vs NP.

Run from a checkout of `j15marti/pnp` with Python 3.10+ and no additional packages:

```sh
python experiments/arc/lspv1_285/valid_state285.py > /tmp/arc285_producer.json
python experiments/arc/lspv1_285/verify_valid_state285.py > /tmp/arc285_independent.json
python experiments/arc/lspv1_285/diagnostics285.py
```

The producer and independent verifier read the authenticated original 198-variable, 264-clause UNSAT source fixture at `research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt`. The verifier reads the committed exact raw reference `results/raw/arc/2026-10-31_1600_LSPV1_ARC_VALID_STATE_FIREWALL285_raw.json`.

Expected producer: four k values 0, 1, 4, 16; encoded lengths 6632, 6832, 7432, 11010; **two** source payload bit differences; 63,552 symbolically certified invalid single-bit payload mutations; 64-row U198 UNSAT certificate with 152 DPLL checks; V198 SAT witness; 20 Y6 full models. Expected independent verifier: PASS, 789 assertions. Diagnostics generate indexed original-clause local SAT/UNSAT extremes and inverses, complete lexicographic 4-bit clause-pair mode matrix, 0^n/1^n counts, coherent flips and binary/Gray logical XOR, and fixed 512-node UP-DPLL source-work comparisons. The complete diagnostics JSON is about 558KB.

**Strict interpretation:** Input source bits are read-only in the FLMV indexed-machine model. The input Hamming distance of 2 is NOT a physical writable-tape update or runtime lower bound. Every accepting deterministic total target-language decider must read all payload bits because malformed one-bit neighbors must be rejected, giving an elementary linear input-probe bound only. Neither the all-input ARC hereditary contractor nor a quantitative numerical SAT-to-target FLMV transfer is proved. P versus NP remains OPEN.

Formal report: `research/agents/lspv-1/2026-10-31_1600_LSPV-1_ARC_VALID_STATE_FIREWALL285.tex`. Coordination: `https://github.com/j15marti/pnp/issues/3#issuecomment-6550399278`.
