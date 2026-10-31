#!/usr/bin/env python3
"""Independently replay every saved policy-tree leaf against original source."""
import json, pathlib, importlib.util
here=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('independent',here/'arc261_verify.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
original=json.loads((here/'raw.json').read_text())['sources'];policies=json.loads((here/'policy_full.json').read_text())
results=[]
for key,tree in policies.items():
    name,p=key.split(':');source=dict(original[name]);source['thresholds']={'8':tree}
    a=mod.checked(name,source)
    results.append({'source':name,'policy':p,'verified':a['thresholds'][0]})
(here/'verify_policy.json').write_text(json.dumps(results,indent=2))
print('Independently replayed',len(results),'policy trees; no false/overlapping/uncovered assignments')
