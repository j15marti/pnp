#!/usr/bin/env python3
"""Negative verifier regression: three deliberately corrupted raw records must fail.
The mutations are deterministic and never modify the canonical raw input.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import copy, json
from verify271 import verify
base=Path(__file__).resolve().parent
original=json.loads((base/'raw271.json').read_text())
checks=[
 ('pair_false_positive', lambda x: x['cases']['W1_UNSAT']['pair_compatibility'][0].__setitem__('SS', not x['cases']['W1_UNSAT']['pair_compatibility'][0]['SS'])),
 ('occurrence_inversion', lambda x: x['cases']['W1_UNSAT']['source_extrema'][0]['signed_occurrences'][0].__setitem__('invert_U', not x['cases']['W1_UNSAT']['source_extrema'][0]['signed_occurrences'][0]['invert_U'])),
 ('endpoint_true_count', lambda x: x['cases']['W1_UNSAT']['endpoints']['ZERO']['true_counts'].__setitem__(0, 99)),
]
with TemporaryDirectory() as tmp:
    for name,mutate in checks:
        raw=copy.deepcopy(original)
        mutate(raw)
        bad=Path(tmp)/f'{name}.json'
        bad.write_text(json.dumps(raw))
        try: verify(bad)
        except AssertionError: print(name,'REJECTED')
        else: raise AssertionError(name+' was wrongly accepted')
print('PASS: all three corruptions rejected')
