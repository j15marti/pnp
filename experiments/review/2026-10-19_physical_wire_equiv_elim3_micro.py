#!/usr/bin/env python3
"""WIRE-EQUIV-ELIM3 minimal falsifier and gate-count arithmetic."""
from itertools import product
for y,h in product((0,1),repeat=2):
    assert ((y^h)==y)==(h==0)
for m in range(2,501):
    A,X,E=3*m,2*m,m
    assert 2*(A+X+E)==12*m
    assert 5*A+4*X+4*E==27*m
    assert 2*A+4*X+5*E==19*m
    assert 2*A+4*(X-E)==10*m
# The one-clause signed example is unsatisfied, but cyclic feedback is zero.
x=(1,0,0)
v=(x[0] and not x[1] and not x[2])
assert v==1 and (v^(x[0]&v))==0
print("PASS: equality elimination, 499 size rows, m=1 counterexample")
