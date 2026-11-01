"""Separate verified-certificate-gated fixed-output emission controls, not part of terminal solver."""
from pathlib import Path
import json
import frontier296 as P
R=Path(__file__).resolve().parent
cert=json.loads((R/'independent_source_cert295.json').read_text())
assert cert['U198_unsat_proof'] and cert['V198_sat_witness'] and cert['SAT_U198'] != 'SAT'
U,V=P.source198()
result=json.loads((R/'results296.json').read_text())
for name,F,child,label in [('U198_ROOT',U,U,'UNSAT'),('V198_ROOT',V,P.Y6,'SAT'),('Y6_ROOT',P.Y6,P.Y6,'SAT')]:
    physical=P.physical_emission_event_trace(P.encode(F),P.encode(child),R/(name+'_canonical_emit_events296.jsonl.gz'))
    result['cases'][name]['child']={
        'valid_target':True,'certified_original_label':label,
        'classification_source':'separate source certificate, NOT the restricted affine terminal',
        'scope':'whole original formula, p=empty',
        'child_bits':len(P.encode(child)),'parent_bits':len(P.encode(F)),
        'power_short':len(P.encode(child))**2<=len(P.encode(F)),
        'physical':physical,'trace_file':name+'_canonical_emit_events296.jsonl.gz'}
(R/'results296.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:result['cases'][k]['child'] for k in ('U198_ROOT','V198_ROOT','Y6_ROOT')},indent=2))
