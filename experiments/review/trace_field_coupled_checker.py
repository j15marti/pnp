#!/usr/bin/env python3
"""Separate bounded end-to-end checker for TRACEISO1; same author, not peer review."""
import hashlib
import json
from pathlib import Path
import time
import trace_field_bridge as t

start=time.monotonic()
t.DEADLINE=start+25
K=t.Field(0x43)
edges=[(0,j) for j in range(2,9)]+[(1,j) for j in range(2,9)]
n=10
_,ct,_=t.forest(n,edges)
image={t.reference_mul(t.reference_mul(z,z,K.f),z,K.f) for z in range(64)}
for c in (0,3,255):
    a=t.lift(n,edges,c,0)
    cols=[t.lift(n,edges,0,1<<i) for i in range(6)]
    for b in range(64):
        x=t.solve_coupled(n,edges,c,b,K)
        t.check((x is not None)==(b in image),'coupled_decision')
        if x is not None:
            z=sum(((x>>e)&1)<<i for i,e in enumerate(ct))
            t.check(t.boundary(n,edges,x)==c,'original_parity_check')
            t.check(t.reference_mul(t.reference_mul(z,z,K.f),z,K.f)==b,'independent_cube_check')
            t.check(x==a^t.apply(cols,z),'explicit_a_plus_Lz')
for c in (1,1<<9):
    for b in range(64):
        t.check(t.solve_coupled(n,edges,c,b,K) is None,'component_charge_rejection')
for args in [(n,edges,0,64,K),(n,edges,0,True,K),(n,edges[:-1],0,1,K)]:
    try:t.solve_coupled(*args)
    except ValueError:t.check(True,'coupled_type_rejection')
    else:t.check(False,'coupled_type_rejection')
print(json.dumps({'run_id':'TRACEISO1','status':'COMPUTATIONAL','batch':'coupled_checker',
  'assertions':sum(t.CHECKS.values()),'checks':dict(t.CHECKS),'failures':0,
  'elapsed_seconds':time.monotonic()-start,'seed':None,
  'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  'core_sha256':hashlib.sha256(Path(t.__file__).read_bytes()).hexdigest()},indent=2,sort_keys=True))
