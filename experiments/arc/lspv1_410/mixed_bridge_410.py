"""LSPV-1/410 source-capacity transfer for existing wheel certificate producer.
Run in this directory: python mixed_bridge_410.py
Requires wheel_checks.py, shift_proofs.py, degree_reduction.py, verify_traces.py.
"""
from wheel_checks import run_wheel
for r in (3,5,7,15,31,63,127,255):
    d=run_wheel(r)  # independently checks exact original-source deletion witnesses
    assert d["indispensable_source_clauses"] == 7*r+1
    assert d["binary_resolution_steps"] == 18*r-6
    # Original /341: every sound conservative derived node has <=2 source parents.
    # All indispensable axioms must be ancestors; connected ancestry yields q>=s-1.
    full_mixed_lower=d["indispensable_source_clauses"]-1
    full_mixed_upper=d["binary_resolution_steps"]  # RES is native R_mix341
    assert full_mixed_lower==7*r<=full_mixed_upper
    print(r,full_mixed_lower,full_mixed_upper)
print("B1/B2/B3 and P versus NP remain OPEN")
